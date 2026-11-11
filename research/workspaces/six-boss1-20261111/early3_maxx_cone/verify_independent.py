#!/usr/bin/env python3
"""Independent exact checker: standard library only; no generator import.

The original displayed residual is evaluated literally. Matrix coefficients
are recovered by affine basis evaluations, independently of discover_once.py.
This script never invokes any optimizer and never reads any feasible-point file.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import csv
import hashlib
import json

HERE = Path(__file__).resolve().parent
ORDER = ["alpha0", "sY", "sZ", "sT", "aY", "aZ", "aT", "delta"]
COST = [Q(1)] * 4 + [Q(0)] * 4


def residual(kind, weights):
    n, k, x, y, z, t, q = kind
    alpha, sy, sz, st, ay, az, at, delta = weights
    c = alpha + sy + sz + st
    return (alpha * Q(x, n + y + z + t)
            + Q(sy * y + sz * z + st * t, n + 3)
            - (c - 1) * Q(x, n + 3)
            - q * (Q(x, n + 3) + Q(1 - x, n))
            - Q(ay * (x - y) + az * (x - z) + at * (x - t), n + k)
            - delta * Q(t - q, n + x + y + z))


def base_residual(n, x, m, t):
    if x == 0:
        return Q(2 * m, 3 * (n + 3)) + Q(4 * t, n + 3) + Q(m, n + 2) + Q(1 - t, n + m) - Q(1, n)
    return Q(15, n + m + t) + Q(2 * m + 12 * t - 58, 3 * (n + 3)) - Q(2 - m, n) - Q(t, n + 1 + m)


table = json.loads((HERE / "local_table_288.json").read_text())
certificate = json.loads((HERE / "exact_certificate.json").read_text())
assert table["variable_order"] == ORDER == certificate["variable_order"]
assert table["constraint_orientation"] == "G*p >= h; p >= 0"
assert table["objective"] == [1, 1, 1, 1, 0, 0, 0, 0]
expected_types = list(product(range(1, 4), range(3), *([range(2)] * 5)))
assert len(table["rows"]) == len(expected_types) == 288
primal = list(map(Q, certificate["primal"]))
assert primal == [Q(15), Q(2, 3), Q(2, 3), Q(4), Q(1), Q(1), Q(0), Q(1)]
assert all(value >= 0 for value in primal)
old = list(map(Q, [15, 2, 2, 4, 0, 0, 0, 1]))
assert sum(primal[:4]) == Q(61, 3)
zero = [Q(0)] * 8
matrix, rhs, old_slacks, new_slacks = [], [], [], []
for index, kind in enumerate(expected_types):
    row = table["rows"][index]
    assert row["index"] == index and row["type"] == list(kind)
    constant = residual(kind, zero)
    coefficients = []
    for position in range(8):
        basis = [Q(0)] * 8
        basis[position] = Q(1)
        coefficients.append(residual(kind, basis) - constant)
    assert coefficients == list(map(Q, row["G"]))
    assert -constant == Q(row["h"])
    matrix.append(coefficients)
    rhs.append(-constant)
    old_e = residual(kind, old)
    new_e = residual(kind, primal)
    assert old_e == Q(row["old_E"]) >= 0
    assert new_e == Q(row["optimal_E"]) >= 0
    old_slacks.append(old_e)
    new_slacks.append(new_e)

    # The reduced 36-entry table plus these corrections proves all 288 cases.
    n, k, x, y, z, t, q = kind
    m = y + z
    base = base_residual(n, x, m, t)
    if x == 0:
        correction_k = m * (Q(1, n + k) - Q(1, n + 2))
        correction_q = (1 - q) * Q(m, n * (n + m))
    else:
        correction_k = (2 - m) * (Q(1, n) - Q(1, n + k))
        correction_q = q * Q(2 - m, (n + 1 + m) * (n + 3))
    assert min(base, correction_k, correction_q) >= 0
    assert new_e == base + correction_k + correction_q

    # Independently expand the global payment coefficient for this customer.
    budget_customer_coefficient = (
        -primal[0] * Q(x, n + y + z + t)
        -Q(primal[1] * y + primal[2] * z + primal[3] * t, n + 3)
        +Q(primal[4] * (x - y) + primal[5] * (x - z) + primal[6] * (x - t), n + k)
        +primal[7] * Q(t - q, n + x + y + z))
    target_customer_coefficient = -Q(58 * x, 3 * (n + 3)) - q * (Q(x, n + 3) + Q(1 - x, n))
    assert budget_customer_coefficient + new_e == target_customer_coefficient

dual = [Q(0)] * 288
for entry in certificate["dual_nonzero"]:
    index = entry["index"]
    assert entry["type"] == list(expected_types[index])
    assert dual[index] == 0
    dual[index] = Q(entry["lambda"])
assert all(value >= 0 for value in dual)
dual_columns = [sum((dual[i] * matrix[i][j] for i in range(288)), Q(0)) for j in range(8)]
reduced_cost = [cost - column for cost, column in zip(COST, dual_columns)]
dual_objective = sum((multiplier * value for multiplier, value in zip(dual, rhs)), Q(0))
assert reduced_cost == [Q(0)] * 8
assert list(map(Q, certificate["dual_reduced_cost"])) == reduced_cost
assert dual_objective == Q(certificate["dual_objective"]) == Q(certificate["C"]) == Q(61, 3)
assert all(multiplier * slack == 0 for multiplier, slack in zip(dual, new_slacks))
assert all(value * slack == 0 for value, slack in zip(primal, reduced_cost))
assert certificate["zero_primal_slack_indices"] == [i for i, value in enumerate(new_slacks) if not value]
assert Q(certificate["positive_primal_slack_min"]) == min(value for value in new_slacks if value > 0)
assert certificate["old_guard"]["zero_E_count"] == sum(value == 0 for value in old_slacks)

base_rows = []
for x, n in product(range(2), range(1, 4)):
    base_rows.append({"x": x, "n": n, "values": [str(base_residual(n, x, m, t)) for m, t in product(range(3), range(2))]})
(HERE / "reduced_36_table.json").write_text(json.dumps({"columns_m_t": list(map(list, product(range(3), range(2)))), "rows": base_rows}, indent=2) + "\n")
with (HERE / "local_table_288.csv").open("w", newline="") as stream:
    writer = csv.writer(stream)
    writer.writerow(["index", "n", "k", "x", "y", "z", "t", "q"] + ORDER + ["h", "E_old23", "E_new61_3"])
    for row in table["rows"]:
        writer.writerow([row["index"]] + row["type"] + row["G"] + [row["h"], row["old_E"], row["optimal_E"]])

output = {"status": "PASS", "arithmetic": "fractions.Fraction only", "optimizer_calls": 0,
          "imports_generator": False, "reads_game_point": False,
          "checked_types": 288, "checked_matrix_entries": 2304,
          "checked_payment_coefficients": 288, "checked_envelope_identities": 288,
          "reduced_base_cases": 36, "old_C": "23", "new_C": "61/3", "improvement": "8/3",
          "old_min_residual": str(min(old_slacks)), "new_min_residual": str(min(new_slacks)),
          "old_zero_residuals": sum(value == 0 for value in old_slacks),
          "new_zero_residuals": sum(value == 0 for value in new_slacks),
          "new_min_positive_residual": str(min(value for value in new_slacks if value > 0)),
          "dual_support_size": sum(bool(value) for value in dual),
          "dual_column_sums": list(map(str, dual_columns)), "dual_reduced_cost": list(map(str, reduced_cost)),
          "dual_objective": str(dual_objective), "exact_primal_dual_gap": "0"}
(HERE / "independent_verification.json").write_text(json.dumps(output, indent=2) + "\n")
print(json.dumps(output, indent=2))
print("Reduced base table: columns (m,t)=(0,0),(0,1),(1,0),(1,1),(2,0),(2,1)")
for row in base_rows:
    print("|", row["x"], "|", row["n"], "|", " | ".join(row["values"]), "|")
