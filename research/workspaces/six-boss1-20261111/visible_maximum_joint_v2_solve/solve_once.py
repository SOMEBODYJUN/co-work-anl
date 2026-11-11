#!/usr/bin/env python3
"""The one Main-authorized v2 full-raw LP. An exclusive pre-entry marker forbids retry."""
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
REPO = HERE.parents[3]
SOURCE = BASE / "visible_maximum_joint_v2"
INPUT_SHA = "0d80f56ac0b1f82350ae5e307370d9860b21382c7059b688904230a3b80f20a4"
PREP_SHA = "61428a95a0798e755694e659eba215f3910ad6e698f8d2a8ed26d5d398a376fd"
SCALE_SHA = "db5f70c7e531fc9feafc66806523713d917838f614eb35a7a5b096fa2b88293e"
sha = lambda p: sha256(p.read_bytes()).hexdigest()
now = lambda: datetime.now(timezone.utc).isoformat()
dump = lambda p,v: p.write_text(json.dumps(v,indent=2)+"\n")
assert sha(SOURCE / "exact_input.json") == INPUT_SHA
assert sha(SOURCE / "freeze_manifest.json") == PREP_SHA
assert sha(SOURCE / "numerical_scaling.json") == SCALE_SHA
release = json.loads((HERE / "main_release.json").read_text())
assert release["authorized_by"] == "/root" and release["optimizer_calls_authorized"] == 1
assert release["input_sha256"] == INPUT_SHA and release["status"] == "MAIN_EXPLICIT_FULL1003_RAW_RELEASE"
assert not (HERE / "single_lp_consumed.json").exists(), "Call consumed: no retry permitted."
assert not (HERE / "discovery_output.json").exists(), "Existing discovery: no retry permitted."
data = json.loads((SOURCE / "exact_input.json").read_text())
scaling = json.loads((SOURCE / "numerical_scaling.json").read_text())
prep = json.loads((SOURCE / "freeze_manifest.json").read_text())
check = json.loads((SOURCE / "independent_precheck_result.json").read_text())
maincheck = json.loads((BASE / "main_visible_c_v2_preflight.json").read_text())
audit = json.loads((BASE / "main_source2_maximum_nested_safe_audit/audit_result.json").read_text())
assert prep["independent_precheck"] == "PASS"
assert check["status"].startswith("PASS") and check["new_input_sha256"] == INPUT_SHA
assert maincheck["status"] == "PASS_MAIN_1003_LITERAL_EXTENSION_AFTER_DIRECT_NS5_PROOF"
assert maincheck["input_sha256"] == INPUT_SHA and maincheck["optimizer_calls"] == 0
assert audit["status"].startswith("PASS") and audit["full_hidden_payment_atom_checks"] == 8192
assert data["variables"] == 513 and data["nonnegative_columns"] == list(range(513))
assert len(data["raw_rows"]) == 1003 and len(data["equalities"]) == 2
assert len(data["atom_columns"]) == 512 and data["K_column"] == 512
rows = data["raw_rows"]
assert scaling["raw_order"] == [r["name"] for r in rows]
divisors = [F(scaling["raw_scales"][r["name"]]) for r in rows]
assert all(d > 0 for d in divisors) and divisors[-1] == 300
assert [F(e["rhs"]) for e in data["equalities"]] == [1,0]
pins = dict(json.loads((SOURCE / "source_pins.json").read_text())["sources"])
for filename, entry in prep["artifacts"].items():
    target = (SOURCE / filename).resolve()
    assert sha(target) == entry["sha256"], filename
    pins[str(target.relative_to(REPO))] = entry["sha256"]
for path in [SOURCE / "freeze_manifest.json", BASE / "main_visible_c_v2_preflight.json",
             BASE / "main_source2_maximum_nested_safe_audit/audit_result.json"]:
    pins[str(path.relative_to(REPO))] = sha(path)
for path, digest in pins.items():
    assert sha(REPO / path) == digest, path
dump(HERE / "source_pins_at_solve.json", pins)

import numpy as np
import scipy
from scipy.optimize import linprog
N = 513
A = np.array([[-float(F(r["a"].get(str(j),"0"))/d) for j in range(N)] for r,d in zip(rows,divisors)])
b = np.array([-float(F(r["rhs"])/d) for r,d in zip(rows,divisors)])
cost = np.array([float(F(data["objective"].get(str(j),"0"))) for j in range(N)])
E = np.array([[float(F(e["a"].get(str(j),"0"))) for j in range(N)] for e in data["equalities"]])
h = np.array([float(F(e["rhs"])) for e in data["equalities"]])
assert A.shape == (1003,513) and E.shape == (2,513)
options = {"time_limit":60.0,"presolve":False,"primal_feasibility_tolerance":1e-9,"dual_feasibility_tolerance":1e-9}
record = {"authorized_by":"/root","owner":"Boss1","RUN":"six-boss1-20261111",
    "input_sha256":INPUT_SHA,"preparation_manifest_sha256":PREP_SHA,"scaling_sha256":SCALE_SHA,
    "release_sha256":sha(HERE/"main_release.json"),"solver_script_sha256":sha(HERE/"solve_once.py"),
    "source_review_sha256":sha(SOURCE/"source_review.md"),"source_pins_sha256":sha(HERE/"source_pins_at_solve.json"),
    "main_preflight_sha256":sha(BASE/"main_visible_c_v2_preflight.json"),
    "NS5_independent_audit_sha256":sha(BASE/"main_source2_maximum_nested_safe_audit/audit_result.json"),
    "optimizer_calls_consumed":1,"status":"CONSUMED_BEFORE_OPTIMIZER_ENTRY",
    "raw_inequalities":1003,"nonnegative_columns":513,"equalities":2,
    "solver":"scipy.optimize.linprog/highs-ds","scipy_version":scipy.__version__,"options":options,
    "model_policy":"All raw rows and columns passed, no pruning, no fixed K, no support restriction or point completion.","start_utc":now()}
with (HERE/"single_lp_consumed.json").open("x") as f:
    f.write(json.dumps(record,indent=2)+"\n")
try:
    result = linprog(cost,A_ub=A,b_ub=b,A_eq=E,b_eq=h,bounds=(0,None),method="highs-ds",options=options)
except BaseException as error:
    dump(HERE/"discovery_output.json",dict(record,optimizer_calls=1,success=False,status="EXCEPTION",
        exception_type=type(error).__name__,message=str(error),finish_utc=now()))
    raise
alist = lambda x: None if x is None else x.tolist()
out = dict(record,optimizer_calls=1,status=int(result.status),success=bool(result.success),message=result.message,
    iterations=int(result.nit),objective=None if result.fun is None else float(result.fun),x=alist(result.x),
    raw_row_order=[r["name"] for r in rows],raw_row_divisors=[str(d) for d in divisors],
    inequality_residual_scaled=alist(result.ineqlin.residual),inequality_marginals_scaled=alist(result.ineqlin.marginals),
    equality_residual=alist(result.eqlin.residual),equality_marginals=alist(result.eqlin.marginals),
    lower_residual=alist(result.lower.residual),lower_marginals=alist(result.lower.marginals),
    upper_residual=alist(result.upper.residual),upper_marginals=alist(result.upper.marginals),finish_utc=now())
dump(HERE/"discovery_output.json",out)
summary = {k:out[k] for k in ["success","status","objective","iterations","raw_inequalities","nonnegative_columns","equalities"]}
summary["positive_columns"] = [] if result.x is None else [[j,float(v)] for j,v in enumerate(result.x) if v>1e-9]
summary["positive_raw_rows"] = [] if result.ineqlin.marginals is None else [
    {"raw_index":i,"name":rows[i]["name"],"scaled_weight":-float(v),"raw_weight_numeric":-float(v)/float(divisors[i])}
    for i,v in enumerate(result.ineqlin.marginals) if -v>1e-9]
dump(HERE/"numerical_summary.json",summary)
print(json.dumps(summary,indent=2))
