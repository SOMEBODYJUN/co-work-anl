#!/usr/bin/env python3
"""One bounded LP discovery call; every later certificate check is rational.

This program only reads the formulas below. It neither loads a game point nor
imports any prior numerical artifact. Run once with scipy.optimize.linprog.
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
NAMES = ["alpha0", "sY", "sZ", "sT", "aY", "aZ", "aT", "delta"]
COST = [1, 1, 1, 1, 0, 0, 0, 0]
OLD = list(map(F, [15, 2, 2, 4, 0, 0, 0, 1]))


def sf(value):
    return str(F(value))


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


rows = []
for n, k, x, y, z, t, q in product(range(1, 4), range(3), *([range(2)] * 5)):
    h = q * (F(x, n + 3) + F(1 - x, n)) - F(x, n + 3)
    g = [
        F(x, n + y + z + t) - F(x, n + 3),
        F(y - x, n + 3),
        F(z - x, n + 3),
        F(t - x, n + 3),
        F(y - x, n + k),
        F(z - x, n + k),
        F(t - x, n + k),
        F(q - t, n + x + y + z),
    ]
    old_e = dot(g, OLD) - h
    assert old_e >= 0, (n, k, x, y, z, t, q, old_e)
    rows.append({"index": len(rows), "type": [n, k, x, y, z, t, q],
                 "G": list(map(sf, g)), "h": sf(h), "old_E": sf(old_e)})
assert len(rows) == 288
assert dot(COST, OLD) == 23

matrix = [[float(F(a)) for a in row["G"]] for row in rows]
rhs = [float(F(row["h"])) for row in rows]
inputs = {"variable_order": NAMES, "row_type_order": ["n", "k", "x", "y", "z", "t", "q"],
          "objective": COST, "constraint_orientation": "G*p >= h; p >= 0", "rows": rows}
(OUT / "local_table_288.json").write_text(json.dumps(inputs, indent=2) + "\n")
(OUT / "numerical_input.json").write_text(json.dumps({"c": COST, "A_ub": (-np.array(matrix)).tolist(),
    "b_ub": (-np.array(rhs)).tolist(), "bounds": [[0, None]] * 8,
    "method": "highs", "options": {"time_limit": 60.0}}, indent=2) + "\n")
started = time.perf_counter()
result = linprog(COST, A_ub=-np.array(matrix), b_ub=-np.array(rhs), bounds=[(0, None)] * 8,
                 method="highs", options={"time_limit": 60.0})
elapsed = time.perf_counter() - started
raw = {"elapsed_seconds": elapsed, "optimizer_calls": 1, "result": plain(dict(result))}
(OUT / "numerical_result.json").write_text(json.dumps(raw, indent=2) + "\n")
assert result.success, result.message

primal = [F(float(a)).limit_denominator(1_000_000) for a in result.x]
dual = [F(float(-a)).limit_denominator(1_000_000) for a in result.ineqlin.marginals]
g_exact = [[F(a) for a in row["G"]] for row in rows]
h_exact = [F(row["h"]) for row in rows]
slacks = [dot(g, primal) - h for g, h in zip(g_exact, h_exact)]
reduced = [F(COST[j]) - sum((dual[i] * g_exact[i][j] for i in range(288)), F(0)) for j in range(8)]
primal_obj = dot(COST, primal)
dual_obj = dot(h_exact, dual)
assert min(primal) >= 0
assert min(dual) >= 0
assert min(slacks) >= 0, min(slacks)
assert min(reduced) >= 0, reduced
assert primal_obj == dual_obj, (primal_obj, dual_obj)
assert all(p * r == 0 for p, r in zip(primal, reduced))
assert all(lam * slack == 0 for lam, slack in zip(dual, slacks))

certificate = {"claim": "Exact optimum of the specified eight-weight pointwise cone only",
    "variable_order": NAMES, "primal": list(map(sf, primal)), "C": sf(primal_obj),
    "dual_nonzero": [{"index": i, "type": rows[i]["type"], "lambda": sf(lam)}
                     for i, lam in enumerate(dual) if lam],
    "dual_reduced_cost": list(map(sf, reduced)), "dual_objective": sf(dual_obj),
    "zero_primal_slack_indices": [i for i, a in enumerate(slacks) if not a],
    "positive_primal_slack_min": sf(min(a for a in slacks if a)),
    "old_guard": {"C": "23", "primal": list(map(sf, OLD)), "min_E": sf(min(F(row["old_E"]) for row in rows)),
                  "zero_E_count": sum(F(row["old_E"]) == 0 for row in rows)},
    "optimizer": {"calls": 1, "elapsed_seconds": elapsed, "time_limit_seconds": 60.0}}
(OUT / "exact_certificate.json").write_text(json.dumps(certificate, indent=2) + "\n")
for row, slack in zip(rows, slacks):
    row["optimal_E"] = sf(slack)
(OUT / "local_table_288.json").write_text(json.dumps(inputs, indent=2) + "\n")
print(json.dumps(certificate, indent=2))
