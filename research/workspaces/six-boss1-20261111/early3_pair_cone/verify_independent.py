#!/usr/bin/env python3
"""Independent standard-library exact verification, with no builder import.

Reconstruct residuals as target minus the eleven actual budget coefficients.
Recover all matrix entries by affine basis evaluations, independently of the
builder's displayed matrix. The pair contribution is independently computed
from U=f-g, and its four-term true-history payment is checked algebraically.
Only writes independent_verification.json in this directory.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import csv
import hashlib
import json

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
ORDER = ["alpha0", "sY", "sZ", "sT", "aY", "aZ", "aT", "delta",
         "eta1", "eta2", "eta3"]
KINDS = list(product(range(1, 4), range(3), *([range(2)] * 5)))
COST = [Q(1)] * 4 + [Q(0)] * 7


def read(name):
    return json.loads((HERE / name).read_text())


def pair_atom(d, z, t, l, r):
    def f(a):
        return Q(a, d)

    def g(a, b):
        return Q(a * b, d * (d + 1))

    def u(a, b):
        return f(a) - g(a, b)

    return u(z, t) + u(t, z) + g(z, z) - f(l) - f(r) + g(l, r)


def pair_values(kind):
    n, k, x, y, z, t, q = kind
    d = n + x + y
    return [pair_atom(d, z, t, q, x), pair_atom(d, z, t, q, q),
            pair_atom(d, z, t, x, x)]


def budget_sum(kind, weights, u3):
    n, k, x, y, z, t, q = kind
    alpha, sy, sz, st, ay, az, at, delta, eta1, eta2, eta3 = weights
    actual_deviation = alpha * (u3 - Q(x, n + y + z + t))
    safe = sy * (u3 - Q(y, n + 3)) + sz * (u3 - Q(z, n + 3)) + st * (u3 - Q(t, n + 3))
    maximum = ay * Q(x - y, n + k) + az * Q(x - z, n + k) + at * Q(x - t, n + k)
    last = delta * Q(t - q, n + x + y + z)
    pairs = sum((a * b for a, b in zip((eta1, eta2, eta3), pair_values(kind))), Q(0))
    return actual_deviation + safe + maximum + last + pairs


def target(kind, weights, u3):
    n, k, x, y, z, t, q = kind
    c = sum(weights[:4], Q(0))
    return c * u3 - (c - 1) * Q(x, n + 3) - q * (Q(x, n + 3) + Q(1 - x, n))


def residual(kind, weights):
    return target(kind, weights, Q(0)) - budget_sum(kind, weights, Q(0))


def base(n, x, m, t):
    if x == 0:
        return Q(2 * m, 3 * (n + 3)) + Q(4 * t, n + 3) + Q(m, n + 2) + Q(1 - t, n + m) - Q(1, n)
    return Q(15, n + m + t) + Q(2 * m + 12 * t - 58, 3 * (n + 3)) - Q(2 - m, n) - Q(t, n + 1 + m)


table = read("local_table_288.json")
certificate = read("exact_certificate.json")
extension = read("old_dual_extension.json")
assert table["variable_order"] == certificate["variable_order"] == ORDER
assert table["constraint_orientation"] == "G*p >= h; p >= 0"
assert table["type_order"] == ["n", "k", "x", "y", "z", "t", "q"]
assert table["objective"] == COST
assert table["yz_quotient_used"] is False
assert len(table["rows"]) == len(KINDS) == 288
primal = list(map(Q, certificate["primal"]))
assert primal == [Q(15), Q(2, 3), Q(2, 3), Q(4), Q(1), Q(1), Q(0), Q(1)] + [Q(0)] * 3
assert all(value >= 0 for value in primal)
assert sum(primal[:4]) == Q(certificate["C"]) == Q(61, 3)

# Check the true-history PAIR algebra at every possible local background.
# IC brackets are only globally nonnegative; only the final g-gap is local.
pair_identity_count = 0
for d in range(1, 6):
    def u(a, b):
        return Q(a, d + b)

    def g(a, b):
        return Q(a * b, d * (d + 1))

    for z, t, l, r, j in product(range(2), repeat=5):
        s_pay, t_pay = u(z, t), u(t, z)
        four_terms = ((s_pay - u(l, j)) + (u(j, l) - u(r, l))
                      + (t_pay - u(j, z)) + (g(z, z) - g(z, j)))
        assert four_terms == pair_atom(d, z, t, l, r)
        assert g(z, z) - g(z, j) == Q(z * (1 - j), d * (d + 1)) >= 0
        for a, b in product(range(2), repeat=2):
            assert u(a, b) == Q(a, d) - g(a, b)
        pair_identity_count += 1
assert pair_identity_count == 160

zero = [Q(0)] * 11
matrix, rhs, slacks = [], [], []
for index, kind in enumerate(KINDS):
    row = table["rows"][index]
    assert row["index"] == index and row["type"] == list(kind)
    constant = residual(kind, zero)
    coefficients = []
    for j in range(11):
        basis = [Q(0)] * 11
        basis[j] = Q(1)
        coefficients.append(residual(kind, basis) - constant)
        # The target and payment have identical u3 coefficient at every basis.
        assert target(kind, basis, Q(1)) - budget_sum(kind, basis, Q(1)) == residual(kind, basis)
    assert coefficients == list(map(Q, row["G"]))
    assert -constant == Q(row["h"])
    assert pair_values(kind) == list(map(Q, row["T"]))
    slack = residual(kind, primal)
    assert slack == Q(row["optimal_E"]) >= 0
    assert target(kind, primal, Q(1)) == budget_sum(kind, primal, Q(1)) + slack
    matrix.append(coefficients)
    rhs.append(-constant)
    slacks.append(slack)

    # This reduction applies only to the exhibited eta=0 optimum.
    n, k, x, y, z, t, q = kind
    m = y + z
    value = base(n, x, m, t)
    if x == 0:
        correction_k = m * (Q(1, n + k) - Q(1, n + 2))
        correction_q = (1 - q) * Q(m, n * (n + m))
    else:
        correction_k = (2 - m) * (Q(1, n) - Q(1, n + k))
        correction_q = q * Q(2 - m, (n + 1 + m) * (n + 3))
    assert min(value, correction_k, correction_q) >= 0
    assert slack == value + correction_k + correction_q

expected_base = [{"x": x, "n": n,
                  "values": [str(base(n, x, m, t)) for m, t in product(range(3), range(2))]}
                 for x, n in product(range(2), range(1, 4))]
base_table = read("reduced_36_table.json")
assert base_table["rows"] == expected_base
assert base_table["columns_m_t"] == list(map(list, product(range(3), range(2))))

dual = [Q(0)] * 288
for entry in certificate["dual_nonzero"]:
    i = entry["index"]
    assert entry["type"] == list(KINDS[i]) and dual[i] == 0
    dual[i] = Q(entry["lambda"])
assert all(value >= 0 for value in dual)
columns = [sum((dual[i] * matrix[i][j] for i in range(288)), Q(0)) for j in range(11)]
reduced = [cost - column for cost, column in zip(COST, columns)]
objective = sum((dual[i] * rhs[i] for i in range(288)), Q(0))
assert columns == list(map(Q, certificate["dual_column_sums"]))
assert reduced == list(map(Q, certificate["dual_reduced_cost"])) == [Q(0)] * 8 + [Q(6), Q(1, 3), Q(139, 6)]
assert objective == Q(certificate["dual_objective"]) == Q(61, 3)
assert all(value >= 0 for value in reduced)
assert all(a * b == 0 for a, b in zip(dual, slacks))
assert all(a * b == 0 for a, b in zip(reduced, primal))
assert certificate["zero_primal_slack_indices"] == [i for i, value in enumerate(slacks) if value == 0]
assert Q(certificate["positive_primal_slack_min"]) == min(value for value in slacks if value > 0) == Q(1, 45)
assert sum(value == 0 for value in slacks) == 52
assert certificate["optimizer"]["calls"] == 0
assert Q(certificate["exact_primal_dual_gap"]) == 0

# Check the entire affine lower-bound identity, not merely the optimal vector.
for weights in [zero] + [[Q(int(i == j)) for i in range(11)] for j in range(11)]:
    lhs = sum(weights[:4], Q(0)) - Q(61, 3)
    rhs_identity = (sum((dual[i] * residual(KINDS[i], weights) for i in range(288)), Q(0))
                    + sum((a * b for a, b in zip(reduced, weights)), Q(0)))
    assert lhs == rhs_identity
identity = certificate["lower_bound_identity"]
assert identity["scale"] == 6
assert identity["scaled_dual_support"] == [
    {"index": e["index"], "coefficient": str(6 * Q(e["lambda"]))} for e in certificate["dual_nonzero"]]
assert list(map(Q, identity["scaled_eta_coefficients"])) == [6 * a for a in reduced[8:]]
assert all(value > 0 for value in reduced[8:])
assert certificate["optimal_pair_weights_forced_zero"] == ["eta1", "eta2", "eta3"]

# Recheck the first calculation and its sign convention column by column.
for row in extension["rows"]:
    i = row["index"]
    assert row["type"] == list(KINDS[i])
    assert Q(row["lambda"]) == dual[i]
    terms = pair_values(KINDS[i])
    assert list(map(Q, row["T"])) == terms
    assert list(map(Q, row["weighted_T"])) == [dual[i] * value for value in terms]
assert extension["remains_dual_feasible"] is True
assert extension["optimizer_calls"] == 0
assert list(map(Q, extension["dual_new_column_sums"])) == columns[8:]
assert list(map(Q, extension["new_dual_reduced_cost"])) == reduced[8:]

with (HERE / "local_table_288.csv").open(newline="") as stream:
    csv_rows = list(csv.reader(stream))
assert csv_rows[0] == ["index", "n", "k", "x", "y", "z", "t", "q"] + ORDER + ["h", "T1", "T2", "T3", "E_optimal"]
assert len(csv_rows) == 289
for actual, row in zip(csv_rows[1:], table["rows"]):
    assert actual == list(map(str, [row["index"]] + row["type"] + row["G"] + [row["h"]] + row["T"] + [row["optimal_E"]]))

manifest = read("source_manifest.json")
for entry in manifest["sources"]:
    path = REPO / entry["path"]
    assert path.stat().st_size == entry["bytes"]
    assert hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"]
original_path = REPO / "research/workspaces/six-boss1-20261111/early3_maxx_cone"
original = json.loads((original_path / "local_table_288.json").read_text())
original_certificate = json.loads((original_path / "exact_certificate.json").read_text())
assert original_certificate["dual_nonzero"] == certificate["dual_nonzero"]
assert list(map(Q, original_certificate["primal"])) == primal[:8]
for row, old in zip(table["rows"], original["rows"]):
    assert row["index"] == old["index"] and row["type"] == old["type"]
    assert list(map(Q, row["G"][:8])) == list(map(Q, old["G"]))
    assert Q(row["h"]) == Q(old["h"])
    assert Q(row["optimal_E"]) == Q(old["optimal_E"])
log = read("optimization_log.json")
assert log["optimizer_calls"] == 0 and log["numerical_optimization_performed"] is False
assert log["conditional_288x11_lp_needed"] is False
assert log["game_point_files_read"] == log["additional_queries_scanned"] == []

output = {
    "status": "PASS", "arithmetic": "fractions.Fraction; Python standard library only",
    "imports_builder": False, "optimizer_calls": 0, "reads_game_point": False,
    "checked_types": 288, "checked_matrix_entries": 3168,
    "checked_original_eight_entries": 2304, "checked_pair_coefficients": 864,
    "checked_payment_affine_basis_coefficients": 3168,
    "checked_optimal_payment_identities": 288,
    "checked_true_history_pair_algebra_cases": pair_identity_count,
    "checked_nonnegative_pair_gap_cases": pair_identity_count,
    "checked_eta_zero_reduction_identities": 288, "reduced_base_cases": 36,
    "dual_support_size": sum(value > 0 for value in dual),
    "dual_column_sums": list(map(str, columns)), "dual_reduced_cost": list(map(str, reduced)),
    "primal_objective": "61/3", "dual_objective": str(objective), "exact_primal_dual_gap": "0",
    "negative_primal_residuals": sum(value < 0 for value in slacks),
    "zero_primal_residuals": sum(value == 0 for value in slacks),
    "positive_primal_residuals": sum(value > 0 for value in slacks),
    "minimal_positive_primal_residual": str(min(value for value in slacks if value > 0)),
    "all_optima_have_eta_zero": True, "yz_quotient_used_for_eleven_weight_cone": False,
    "source_fingerprints_unchanged": True,
    "scope": "Specified eleven-weight pointwise cone only; does not assert SPE sharpness"}
(HERE / "independent_verification.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(output, ensure_ascii=False, indent=2))
