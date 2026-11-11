#!/usr/bin/env python3
"""Exactly one authorized full-raw LP; the exclusive marker forbids any retry."""
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
SOURCE = BASE / "visible_maximum_joint"
INPUT_SHA = "b0610bb00298a4ee953423a8066dab050cb9d515fd6d5dde41f5117116f2ba33"
PREPARATION_SHA = "31af8bc9ddfa35fd0a62b546cdf095fbd2cc76dfde76fc5ccfc010967f735966"
SCALING_SHA = "b29bb0136b9153a14d223ba44eee51f5b94b607705e16b952ee147b7e2fec31c"
sha = lambda p: sha256(p.read_bytes()).hexdigest()
dump = lambda p, x: p.write_text(json.dumps(x, indent=2) + "\n")
now = lambda: datetime.now(timezone.utc).isoformat()

assert sha(SOURCE / "exact_input.json") == INPUT_SHA
assert sha(SOURCE / "freeze_manifest.json") == PREPARATION_SHA
assert sha(SOURCE / "numerical_scaling.json") == SCALING_SHA
release = json.loads((HERE / "main_release.json").read_text())
assert release["authorized_by"] == "/root"
assert release["optimizer_calls_authorized"] == 1
assert release["input_sha256"] == INPUT_SHA
assert release["status"] == "MAIN_EXPLICIT_FULL_RAW_RELEASE"
assert not (HERE / "single_lp_consumed.json").exists(), "Single authorized call already consumed; no retry."
assert not (HERE / "discovery_output.json").exists(), "Discovery already recorded; no retry."

data = json.loads((SOURCE / "exact_input.json").read_text())
scale_data = json.loads((SOURCE / "numerical_scaling.json").read_text())
prep = json.loads((SOURCE / "freeze_manifest.json").read_text())
precheck = json.loads((SOURCE / "independent_precheck_result.json").read_text())
maincheck = json.loads((BASE / "main_visible_c_preflight.json").read_text())
assert prep["independent_precheck"] == "PASS"
assert precheck["result"].startswith("PASS") and precheck["input_sha256"] == INPUT_SHA
assert maincheck["status"] == "PASS_MAIN_FULL_1002_INPUT_REPLAY"
assert maincheck["input_sha256"] == INPUT_SHA and maincheck["optimizer_calls"] == 0
assert data["variables"] == 513 and data["K_column"] == 512
assert data["nonnegative_columns"] == list(range(513))
assert len(data["atom_columns"]) == 512 and len(data["raw_rows"]) == 1002
assert len(data["equalities"]) == 2
rows = data["raw_rows"]
assert [r["name"] for r in rows] == scale_data["raw_order"]
scales = [F(scale_data["raw_scales"][r["name"]]) for r in rows]
assert all(s > 0 for s in scales)
assert data["inequality_convention"] == "a dot z >= rhs"
assert [F(e["rhs"]) for e in data["equalities"]] == [F(1), F(0)]

source_pins = {
    "../visible_maximum_joint/" + name: sha(SOURCE / name)
    for name in prep["artifacts"]
    if (SOURCE / name).is_file()
}
for name, entry in prep["artifacts"].items():
    target = SOURCE / name
    assert target.is_file() and sha(target) == entry["sha256"], (name, "frozen artifact changed")
source_pins.update({
    "../visible_maximum_joint/freeze_manifest.json": PREPARATION_SHA,
    "../main_visible_c_preflight.py": sha(BASE / "main_visible_c_preflight.py"),
    "../main_visible_c_preflight.json": sha(BASE / "main_visible_c_preflight.json"),
})
dump(HERE / "source_pins_at_solve.json", source_pins)

import numpy as np
import scipy
from scipy.optimize import linprog

N = 513
A = np.array([
    [-float(F(r["a"].get(str(j), "0")) / divisor) for j in range(N)]
    for r, divisor in zip(rows, scales)
], dtype=float)
b = np.array([-float(F(r["rhs"]) / divisor) for r, divisor in zip(rows, scales)])
cost = np.array([float(F(data["objective"].get(str(j), "0"))) for j in range(N)])
eq = np.array([[float(F(e["a"].get(str(j), "0"))) for j in range(N)] for e in data["equalities"]])
eqrhs = np.array([float(F(e["rhs"])) for e in data["equalities"]])
assert A.shape == (1002, 513) and eq.shape == (2, 513)
options = {"time_limit": 60.0, "presolve": False,
           "primal_feasibility_tolerance": 1e-9, "dual_feasibility_tolerance": 1e-9}
record = {
    "authorized_by": "/root", "RUN": "six-boss1-20261111", "owner": "Boss1",
    "input_sha256": INPUT_SHA, "preparation_manifest_sha256": PREPARATION_SHA,
    "release_sha256": sha(HERE / "main_release.json"),
    "solver_script_sha256": sha(HERE / "solve_once.py"),
    "source_review_sha256": sha(SOURCE / "source_review.md"),
    "scaling_sha256": SCALING_SHA,
    "independent_precheck_sha256": sha(SOURCE / "independent_precheck_result.json"),
    "main_preflight_sha256": sha(BASE / "main_visible_c_preflight.json"),
    "optimizer_calls_consumed": 1, "status": "CONSUMED_BEFORE_OPTIMIZER_ENTRY",
    "raw_inequalities": 1002, "nonnegative_columns": 513, "equalities": 2,
    "solver": "scipy.optimize.linprog/highs-ds", "scipy_version": scipy.__version__,
    "options": options, "start_utc": now(),
    "model_policy": "Every raw row and all columns passed without pruning; no support restriction, fixed K, or point completion."
}
with (HERE / "single_lp_consumed.json").open("x") as handle:
    handle.write(json.dumps(record, indent=2) + "\n")
try:
    result = linprog(cost, A_ub=A, b_ub=b, A_eq=eq, b_eq=eqrhs,
                     bounds=(0, None), method="highs-ds", options=options)
except BaseException as error:
    dump(HERE / "discovery_output.json", dict(record, optimizer_calls=1,
        success=False, status="EXCEPTION", exception_type=type(error).__name__,
        message=str(error), finish_utc=now()))
    raise

as_list = lambda value: None if value is None else value.tolist()
out = dict(record, optimizer_calls=1, status=int(result.status), success=bool(result.success),
    message=result.message, iterations=int(result.nit),
    objective=None if result.fun is None else float(result.fun),
    x=as_list(result.x), raw_row_order=[r["name"] for r in rows],
    raw_row_divisors=[str(s) for s in scales],
    inequality_residual_scaled=as_list(result.ineqlin.residual),
    inequality_marginals_scaled=as_list(result.ineqlin.marginals),
    equality_residual=as_list(result.eqlin.residual),
    equality_marginals=as_list(result.eqlin.marginals),
    lower_residual=as_list(result.lower.residual),
    lower_marginals=as_list(result.lower.marginals),
    upper_residual=as_list(result.upper.residual),
    upper_marginals=as_list(result.upper.marginals), finish_utc=now())
dump(HERE / "discovery_output.json", out)
summary = {k: out[k] for k in ["success", "status", "objective", "iterations", "raw_inequalities", "nonnegative_columns", "equalities"]}
summary["positive_columns"] = [] if result.x is None else [[j, float(v)] for j, v in enumerate(result.x) if v > 1e-9]
summary["positive_raw_rows"] = [] if result.ineqlin.marginals is None else [
    {"raw_index": i, "name": rows[i]["name"], "scaled_weight": -float(v),
     "raw_weight_numeric": -float(v) / float(scales[i])}
    for i, v in enumerate(result.ineqlin.marginals) if -v > 1e-9]
dump(HERE / "numerical_summary.json", summary)
print(json.dumps(summary, indent=2))
