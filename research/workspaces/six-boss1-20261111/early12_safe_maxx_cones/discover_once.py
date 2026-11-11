#!/usr/bin/env python3
"""Exactly one <=60-second all-ordered-type LP for each r=5,6.

This script is discovery only. It refuses to repeat a completed optimizer call.
Inputs and complete floating results are saved before rational reconstruction.
The independent standard-library verifier is the reproduction entry point.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import time

import numpy as np
from scipy.optimize import linprog

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
SOURCES = [
    "archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md",
    "research/workspaces/six-boss1-20261111/main_prefix_safety_maxx_family.md",
    "research/workspaces/six-boss1-20261111/main_prefix_safety_maxx_family.py",
    "research/workspaces/six-boss1-20261111/main_prefix_safety_maxx_family.json",
    "research/workspaces/six-boss1-20261111/early3_maxx_cone.md",
    "research/workspaces/six-boss1-20261111/early3_maxx_cone/discover_once.py",
]


def dump(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def plain(value):
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {key: plain(val) for key, val in value.items()}
    if isinstance(value, (list, tuple)):
        return [plain(val) for val in value]
    return value


def run(r):
    assert not (OUT / f"numerical_result_r{r}.json").exists(), "Do not rerun LP"
    assert not (OUT / f"call_started_r{r}.json").exists(), "One call was already started"
    m = r - 2
    names = ["alpha0"] + [f"s{j+1}" for j in range(m)] + ["sT"]
    names += [f"a{j+1}" for j in range(m)] + ["aT", "delta"]
    cost = [1] * r + [0] * r
    alpha, s, a = {5: (F(20), F(7, 4), F(3, 5)),
                   6: (F(25), F(51, 20), F(3, 8))}[r]
    old = [alpha] + [s] * m + [F(r)] + [a] * m + [F(0), F(1)]
    rows = []
    for n in range(1, 8-r):
        for k in range(r-1):
            for bits in product((0, 1), repeat=r+1):
                x, *ys, t, q = bits
                j, D = sum(ys), n+r-1
                g = [F(x, n+j+t) - F(x, D)]
                g += [F(y-x, D) for y in ys] + [F(t-x, D)]
                g += [F(y-x, n+k) for y in ys] + [F(t-x, n+k)]
                g += [F(q-t, n+x+j)]
                h = q * (F(x, D) + F(1-x, n)) - F(x, D)
                e = dot(g, old) - h
                assert e >= 0
                rows.append({"index": len(rows), "type": [n, k, *bits],
                             "G": list(map(str, g)), "h": str(h), "main_guard_E": str(e)})
    assert len(rows) == {5: 512, 6: 640}[r]
    assert len(names) == 2*r
    exact = {"r": r, "actual_player": 7-r, "variable_order": names,
             "row_type_order": ["n", "k", "x"] + [f"y{j+1}" for j in range(m)] + ["t", "q"],
             "orientation": "G*p >= h; p >= 0", "objective": cost, "rows": rows}
    dump(OUT / f"all_types_r{r}.json", exact)
    G = [[F(v) for v in row["G"]] for row in rows]
    h = [F(row["h"]) for row in rows]
    A = -np.array([[float(v) for v in row] for row in G])
    b = -np.array([float(v) for v in h])
    bounds = [(0, None)] * (2*r)
    options = {"time_limit": 60.0}
    dump(OUT / f"numerical_input_r{r}.json", {"c": cost, "A_ub": A.tolist(),
        "b_ub": b.tolist(), "bounds": bounds, "method": "highs", "options": options})
    dump(OUT / f"call_started_r{r}.json", {"r": r, "calls_authorized": 1,
        "time_limit_seconds": 60, "input_sha256": hashlib.sha256(
            (OUT / f"numerical_input_r{r}.json").read_bytes()).hexdigest()})
    started = time.perf_counter()
    res = linprog(cost, A_ub=A, b_ub=b, bounds=bounds, method="highs", options=options)
    elapsed = time.perf_counter() - started
    dump(OUT / f"numerical_result_r{r}.json", {"elapsed_seconds": elapsed,
        "optimizer_calls": 1, "result": plain(dict(res))})
    if not res.success:
        print(json.dumps({"r": r, "recovery": "NO_OPTIMUM", "message": res.message}))
        return
    p = [F(float(v)).limit_denominator(1000000) for v in res.x]
    lam = [F(float(-v)).limit_denominator(1000000) for v in res.ineqlin.marginals]
    avg_s = sum(p[1:1+m], F(0)) / m
    avg_a = sum(p[r:r+m], F(0)) / m
    sym = [p[0]] + [avg_s]*m + [p[r-1]] + [avg_a]*m + p[-2:]
    slack = [dot(g,p)-v for g,v in zip(G,h)]
    symslack = [dot(g,sym)-v for g,v in zip(G,h)]
    reduced = [F(cost[c])-sum((lam[i]*G[i][c] for i in range(len(rows))), F(0))
               for c in range(2*r)]
    primal_value, dual_value = dot(cost,p), dot(h,lam)
    ok = (min(p) >= 0 and min(lam) >= 0 and min(slack) >= 0 and min(symslack) >= 0
          and min(reduced) >= 0 and primal_value == dual_value == dot(cost,sym)
          and all(v*z == 0 for v,z in zip(p,reduced))
          and all(v*z == 0 for v,z in zip(lam,slack)))
    cert = {"status": "EXACT_PRIMAL_DUAL_PASS" if ok else "RATIONAL_RECOVERY_FAILED",
        "r": r, "claim_scope": "Specified nonnegative all-ordered-type cone only; no SPE sharpness claim",
        "variable_order": names, "primal": list(map(str,p)), "symmetric_primal": list(map(str,sym)),
        "C": str(primal_value), "main_C": str(dot(cost,old)),
        "main_primal": list(map(str,old)), "improvement_from_main": str(dot(cost,old)-primal_value),
        "dual_objective": str(dual_value), "dual_reduced_cost": list(map(str,reduced)),
        "dual_nonzero": [{"index": i, "type": rows[i]["type"], "lambda": str(v)}
                         for i,v in enumerate(lam) if v],
        "all_type_count": len(rows), "primal_zero_count": sum(v == 0 for v in slack),
        "primal_min_E": str(min(slack)), "symmetric_zero_count": sum(v == 0 for v in symslack),
        "symmetric_min_E": str(min(symslack)),
        "symmetric_min_positive_E": str(min(v for v in symslack if v > 0)),
        "optimizer_calls": 1, "time_limit_seconds": 60.0, "elapsed_seconds": elapsed}
    dump(OUT / f"exact_certificate_r{r}.json", cert)
    for row,e,se in zip(rows,slack,symslack):
        row["primal_E"] = str(e)
        row["symmetric_E"] = str(se)
    dump(OUT / f"all_types_r{r}.json",exact)
    print(json.dumps(cert, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    assert not (OUT / "source_manifest.json").exists(), "Discovery already started"
    dump(OUT / "source_manifest.json", {"sources": [{"path": p,
        "sha256": hashlib.sha256((ROOT / p).read_bytes()).hexdigest()} for p in SOURCES],
        "point_reads": 0, "planned_optimizer_calls": 2})
    run(5)
    run(6)
