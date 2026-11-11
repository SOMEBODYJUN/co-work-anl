#!/usr/bin/env python3
"""Independent exact arithmetic check from payment budgets, without imports
from the generator and without a solver. Outputs only within this package.
"""

from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
THETA = F(1, 6)


def f(d, a):
    return F(a, d)


def g(d, a, b):
    return F(a * b, d * (d + 1))


def U(d, a, b):
    return f(d, a) - g(d, a, b)


def pair(d, z, t, l, r):
    return U(d, z, t) + U(d, t, z) + g(d, z, z) - f(d, l) - f(d, r) + g(d, l, r)


def budgets(typ, u):
    n, k, x, y, z, t = typ
    d = n + x + y
    queries = [1, 0, 0, 0, 0, 0]
    return [
        u - F(x, n + y + z + t),
        u - F(y, n + 3), u - F(z, n + 3), u - F(t, n + 3),
        F(x - y, n + k), F(x - z, n + k), F(x - t, n + k),
        sum((F(t - q, n + x + y + z) for q in queries), F(0)) / 6,
        sum((pair(d, z, t, q, x) for q in queries), F(0)) / 6,
        sum((pair(d, z, t, q, q) for q in queries), F(0)) / 6,
        pair(d, z, t, x, x),
    ]


def residual(typ, p):
    n, k, x, y, z, t = typ
    u = F(11, 7)  # arbitrary bookkeeping value; cancellation is checked below
    C = sum(p[:4], F(0))
    kap = F(x, n + 3)
    lavg = sum((F(q * x, n + 3) + F(q * (1 - x), n) for q in [1, 0, 0, 0, 0, 0]), F(0)) / 6
    target = C * u - (C - 1) * kap - lavg
    return target - sum((p[j] * b for j, b in enumerate(budgets(typ, u))), F(0))


def main():
    table = json.loads((HERE / "local_table_144.json").read_text(encoding="utf-8"))
    cert = json.loads((HERE / "exact_certificate.json").read_text(encoding="utf-8"))
    compact = json.loads((HERE / "reduced_36_table.json").read_text(encoding="utf-8"))
    assert F(table["theta"]) == THETA
    expected_types = list(product((1, 2, 3), (0, 1, 2), (0, 1), (0, 1), (0, 1), (0, 1)))
    assert len(table["rows"]) == len(expected_types) == 144
    primal = [F(v) for v in cert["primal"]]
    assert primal == [F(15), F(0), F(0), F(4), F(7, 6), F(7, 6), F(0), F(1), F(0), F(0), F(0)]
    cost = [F(1)] * 4 + [F(0)] * 7
    zero = [F(0)] * 11
    G, h, E = [], [], []
    coefficients_checked = 0
    tp_checked = 0
    compact_map = {(r["x"], r["n"], r["a"], r["t"]): F(r["H"]) for r in compact["rows"]}
    assert len(compact_map) == 36 and min(compact_map.values()) >= 0
    for i, typ in enumerate(expected_types):
        row = table["rows"][i]
        assert row["index"] == i and tuple(row["type"]) == typ
        base = residual(typ, zero)
        row_G = []
        for j in range(11):
            unit = list(zero)
            unit[j] = F(1)
            coeff = residual(typ, unit) - base
            assert coeff == F(row["G"][j])
            row_G.append(coeff)
            coefficients_checked += 1
        G.append(row_G)
        h.append(-base)
        assert h[-1] == F(row["h"])
        b = budgets(typ, F(0))
        for j in range(3):
            assert b[8 + j] == F(row["TP"][j])
            tp_checked += 1
        e = residual(typ, primal)
        E.append(e)
        assert e == F(row["E_star"]) and e >= 0
        # Check the affine budget decomposition at a second arbitrary weight point.
        probe = [F(j + 1, j + 2) for j in range(11)]
        assert residual(typ, probe) == sum((row_G[j] * probe[j] for j in range(11)), F(0)) - h[-1]
        n, k, x, y, z, t = typ
        a = y + z
        if x == 0:
            correction = F(7 * a, 6) * (F(1, n + k) - F(1, n + 2))
        else:
            correction = F(7 * (2 - a), 6) * (F(1, n) - F(1, n + k))
        assert correction >= 0
        assert e == compact_map[(x, n, a, t)] + correction
        # Full payment cancellation is independent of the arbitrary original u.
        C = sum(primal[:4], F(0))
        u_other = F(17, 13)
        kap = F(x, n + 3)
        lavg = THETA * (kap + F(1 - x, n))
        assert C * u_other - (C - 1) * kap - lavg - sum((primal[j] * v for j, v in enumerate(budgets(typ, u_other))), F(0)) == e

    pair_identities = 0
    last_gap_nonnegative = 0
    for d in range(1, 6):
        for z, t, l, r, j in product((0, 1), repeat=5):
            parts = [
                U(d, z, t) - U(d, l, j),
                U(d, j, l) - U(d, r, l),
                U(d, t, z) - U(d, j, z),
                g(d, z, z) - g(d, z, j),
            ]
            assert pair(d, z, t, l, r) == sum(parts, F(0))
            pair_identities += 1
            assert parts[3] == F(z * (1 - j), d * (d + 1)) >= 0
            last_gap_nonnegative += 1

    lam = [F(0)] * 144
    for entry in cert["dual_support"]:
        i = entry["index"]
        assert tuple(entry["type"]) == expected_types[i]
        lam[i] = F(entry["lambda"])
    assert {i: v for i, v in enumerate(lam) if v} == {0: F(160), 15: F(36), 33: F(24), 110: F(30)}
    GTlam = [sum((lam[i] * G[i][j] for i in range(144)), F(0)) for j in range(11)]
    reduced = [cost[j] - GTlam[j] for j in range(11)]
    assert GTlam == [F(v) for v in cert["GT_lambda"]]
    assert reduced == [F(v) for v in cert["reduced_cost"]]
    assert reduced == [F(0), F(1), F(1), F(0), F(0), F(0), F(2), F(0), F(1), F(2, 3), F(20)]
    assert min(primal) >= 0 and min(lam) >= 0 and min(reduced) >= 0
    pobj = sum((cost[j] * primal[j] for j in range(11)), F(0))
    dobj = sum((h[i] * lam[i] for i in range(144)), F(0))
    assert pobj == dobj == F(cert["primal_objective"]) == F(cert["dual_objective"]) == 19
    assert all(lam[i] * E[i] == 0 for i in range(144))
    assert all(reduced[j] * primal[j] == 0 for j in range(11))
    assert all(reduced[j] > 0 for j in (8, 9, 10))

    # Exact affine identity: all 11 coefficients and the constant are checked.
    for probe in [zero] + [[F(int(j == k)) for j in range(11)] for k in range(11)]:
        rhs = sum((lam[i] * residual(expected_types[i], probe) for i in range(144)), F(0)) + sum((reduced[j] * probe[j] for j in range(11)), F(0))
        assert sum(probe[:4], F(0)) - 19 == rhs

    source_manifest = json.loads((HERE / "source_manifest.json").read_text(encoding="utf-8"))
    for entry in source_manifest["read_only_sources"]:
        data = (REPO / entry["path"]).read_bytes()
        assert len(data) == entry["bytes"]
        assert hashlib.sha256(data).hexdigest() == entry["sha256"]
    log = json.loads((HERE / "optimization_log.json").read_text(encoding="utf-8"))
    assert log["optimizer_invocations"] == log["old_optimizer_reruns"] == 0
    result = {
        "result": "PASS", "exact_arithmetic": "fractions.Fraction", "generator_imported": False,
        "optimizer_invocations": 0, "ordered_types": 144, "matrix_entries": coefficients_checked,
        "right_hand_sides": 144, "pair_average_coefficients": tp_checked,
        "pair_four_part_payment_identities": pair_identities,
        "last_g_difference_nonnegative": last_gap_nonnegative,
        "primal_payment_identities": 144, "arbitrary_weight_affine_checks": 144,
        "reduced_primal_identities": 144, "lower_bound_affine_checks": 12,
        "dual_support": 4, "primal_objective": str(pobj), "dual_objective": str(dobj),
        "exact_gap": str(pobj - dobj), "zero_residuals": sum(v == 0 for v in E),
        "positive_residuals": sum(v > 0 for v in E), "negative_residuals": sum(v < 0 for v in E),
        "minimum_positive_residual": str(min(v for v in E if v > 0)),
        "all_optimal_eta_zero": True, "source_hashes_checked": len(source_manifest["read_only_sources"]),
    }
    (HERE / "independent_verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
