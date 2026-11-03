#!/usr/bin/env python3
"""Replay the three frozen LP entrypoints in a private original-layout tree.

This checks original/source binding and floating matrix consistency, not SPE
realizability.  The input's old 557-row certificate is not revalidated here.
"""
from pathlib import Path
import ast
import contextlib
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import time

sys.dont_write_bytecode = True

import numpy as np
import scipy

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
EVIDENCE = HERE.relative_to(REPO)
RUN = HERE / "replay-001"
ACTOR = "R-c8ca54e5f2854c2c93bf83abc2f24f5c"
PRIMAL = "R-c4732bee2f7b4e50a70568170e3334ae"
IDS = {
    "601948aa4935a200c07c": "original/cycle_common_topic_probe.json",
    "9d5f35cb2e94fbc0bf5d": "original/cycle_common_topic_probe.py",
    "30c4ba70baeb823a44d2": "original/max_topic_branch_lp.json",
    "66398c8866fa531dbd47": "original/max_topic_branch_lp.py",
    "e7530579718c435359f9": "original/max_topic_credible_lp.json",
    "e5afe8841789c0d58d75": "original/max_topic_credible_lp.py",
    "ad8f834b0f07716b86d5": "dependencies/exact_optimum_primal_overlap1.json",
    "025d347c4aae890194fd": "dependencies/audit_root_share_interface.py",
    "54073af62ec20375659f": "dependencies/feedback_cycle.md",
    "a419a809dda8464edcd2": "dependencies/root_share_interface.md",
}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def dump(p, x):
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2) + "\n")


def build_namespace(path, stop):
    """Execute source definitions, stopping before its optimization loop."""
    tree = ast.parse(path.read_text(), filename=str(path))
    nodes = []
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == stop for t in node.targets
        ):
            break
        nodes.append(node)
    ns = {"__file__": str(path), "__name__": "frozen_matrix_inspection"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(ast.Module(nodes, type_ignores=[]), str(path), "exec"), ns)
    return ns


def matrix_inspection(name, path, report):
    ns = build_namespace(path, "res" if name == "max_topic_branch_lp" else "out")
    if name == "max_topic_branch_lp":
        A = np.asarray(ns["A0"], float)
        b = np.asarray(ns["b0"], float)
        eq = ns["size"][0]
        opt = ns["opt"]
        root = ns["util"][0]
        cols = ns["cols"]
        names = ["size_" + str(i) for i in range(1, 5)]
        names += ["last_" + str(i) for i in range(5)]
        names += ["lastopt"] + ["floor_" + str(i) for i in range(1, 4)]
    else:
        A = np.asarray(ns["rows"], float)
        b = np.asarray(ns["rhs"], float)
        eq = ns["eq"]
        opt = ns["opt"]
        root = ns["us"][0]
        cols = ns["vs"]
        names = ns["names"]
    index = {tuple(c): i for i, c in enumerate(cols)}
    result = []
    for entry in report:
        x = np.zeros(len(cols))
        for c, mass in entry["support"]:
            x[index[tuple(c)]] = mass
        Ab = np.vstack([A, root])
        bb = np.r_[b, entry["t"]]
        if name == "max_topic_branch_lp":
            dual = np.asarray(entry["dual"], float)
        else:
            vals = dict(s.rsplit(":", 1) for s in entry["dual"])
            dual = np.asarray([float(vals.get(n, 0)) for n in names + ["root_threshold"]])
        dual_eq = entry["eq"][0]
        reduced = -opt - Ab.T @ dual - eq * dual_eq
        value = float(opt @ x)
        dual_upper = -float(bb @ dual) - dual_eq
        residual = max(0.0, float(np.max(Ab @ x - bb)))
        equal_residual = abs(float(eq @ x) - 1)
        assert residual < 1e-7 and equal_residual < 1e-7
        assert float(np.min(reduced)) > -1e-7
        assert abs(value - entry["O"]) < 1e-7
        assert abs(dual_upper - value) < 1e-7
        result.append({"t": entry["t"], "O": entry["O"], "support_size": len(entry["support"]),
                       "maximum_primal_violation": residual, "equality_residual": equal_residual,
                       "minimum_reduced_cost": float(np.min(reduced)),
                       "floating_primal_dual_gap": dual_upper - value})
    return {"columns": len(cols), "inequalities_with_threshold": len(b) + 1, "points": result}


def main():
    if RUN.exists():
        raise SystemExit("Refusing to overwrite replay-001; use a new evidence directory for a fresh run.")
    inventory = {j["id"]: j for j in map(json.loads, (REPO / "cleanup/inventory.jsonl").read_text().splitlines())}
    manifest = []
    for ident, rel in IDS.items():
        p = HERE / rel
        item = inventory[ident]
        assert sha(p) == item["sha256"] and p.stat().st_size == item["size"]
        manifest.append({**item, "local_path": str(EVIDENCE / rel),
                         "role": "primary" if rel.startswith("original/") else "related-required-or-explanatory"})
    dump(HERE / "source-manifest.json", manifest)
    n5 = RUN / "research/workspaces/customer-attraction" / ACTOR / "n5"
    for d in (n5 / "reply_feedback", n5 / "threshold_payment", n5 / "induction", RUN / "customer_attraction"):
        d.mkdir(parents=True)
    (RUN / "customer_attraction/__init__.py").write_text("")
    source_path = RUN / "research/workspaces/customer-attraction" / PRIMAL / "round4_pricing/exact_optimum_primal_overlap1.json"
    source_path.parent.mkdir(parents=True)
    shutil.copyfile(HERE / "dependencies/exact_optimum_primal_overlap1.json", source_path)
    shutil.copyfile(HERE / "dependencies/audit_root_share_interface.py", n5 / "induction/audit_root_share_interface.py")
    jobs = [("cycle_common_topic_probe", "reply_feedback"), ("max_topic_branch_lp", "threshold_payment"),
            ("max_topic_credible_lp", "threshold_payment")]
    records = []
    for name, folder in jobs:
        script = n5 / folder / (name + ".py")
        shutil.copyfile(HERE / "original" / script.name, script)
        target = script.with_suffix(".json")
        assert not target.exists()
        started = time.monotonic()
        process = subprocess.run([sys.executable, str(script)], cwd=RUN, capture_output=True, text=True,
                                 env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        elapsed = time.monotonic() - started
        (RUN / (name + ".stdout.txt")).write_text(process.stdout)
        (RUN / (name + ".stderr.txt")).write_text(process.stderr)
        assert process.returncode == 0, process.stderr
        frozen = HERE / "original" / target.name
        old, new = json.loads(frozen.read_text()), json.loads(target.read_text())
        if isinstance(old, list):
            assert [(z["t"], z["O"]) for z in old] == [(z["t"], z["O"]) for z in new]
            inspect = matrix_inspection(name, script, old)
        else:
            assert old == new
            ns = build_namespace(script, "unused_stop")
            names, aa, bb = ns["build"]()
            x = np.asarray(old["mean_cycle_membership"])
            eps = old["minimum_uniform_violation"]
            violation = np.asarray(aa, float) @ x - np.asarray(bb, float) - eps
            assert float(np.max(violation)) < 1e-7
            inspect = {"columns": len(x), "inequalities": len(names),
                       "maximum_saved_point_violation": float(np.max(violation)),
                       "saved_minimum_uniform_violation": eps,
                       "nonzero_dual": old["nonzero_dual"]}
        records.append({"name": name, "argv": [sys.executable, str(script.relative_to(HERE))],
                        "cwd": str(RUN.relative_to(HERE)), "seconds": elapsed,
                        "exit_code": process.returncode, "stderr_bytes": len(process.stderr.encode()),
                        "script_sha256": sha(script), "generated_report_sha256": sha(target),
                        "frozen_report_sha256": sha(frozen), "byte_identical": target.read_bytes() == frozen.read_bytes(),
                        "matrix_consistency": inspect})
    dump(HERE / "replay-inspection.json", {"python": sys.version, "numpy": np.__version__, "scipy": scipy.__version__,
         "scope": "Three original entrypoint replays and saved floating matrix primal/dual checks; no rational LP optimality or SPE certification.",
         "input_557_rows_reaudited": False, "runs": records})
    print(json.dumps({"runs": len(records), "all_exit_zero": True,
                      "all_reports_byte_identical": all(r["byte_identical"] for r in records)}, indent=2))


if __name__ == "__main__":
    main()
