#!/usr/bin/env python3
"""Exact coefficient audit of the averaged-menu theorem; no LP or point input."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def weights(r, a=None):
    m = r - 2
    return [F(5 * (r - 1))] + [F(0)] * m + [F(r)] + [
        F(5 * r - 6, r * (r - 1)) if a is None else a
    ] * m + [F(0), F(1)]


def remainder(r, n, k, x, ys, t, theta, w):
    m = r - 2
    alpha = w[0]
    sy = w[1:1 + m]
    st = w[1 + m]
    ay = w[2 + m:2 + 2 * m]
    at, delta = w[-2:]
    C = alpha + sum(sy) + st
    j, D = sum(ys), n + r - 1
    return (alpha * F(x, n + j + t)
            + (sum(s * y for s, y in zip(sy, ys)) + st * t) / D
            - (C - 1) * F(x, D)
            - theta * (F(x, D) + F(1 - x, n))
            - (sum(a * (x - y) for a, y in zip(ay, ys))
               + at * (x - t)) / (n + k)
            - delta * F(t - theta, n + x + j))


def affine_row(r, n, k, x, ys, t, theta):
    size = 2 * r
    zero = [F(0)] * size
    const = remainder(r, n, k, x, ys, t, theta, zero)
    co = []
    for z in range(size):
        w = zero.copy()
        w[z] = F(1)
        co.append(remainder(r, n, k, x, ys, t, theta, w) - const)
    return co + [const]


def run():
    result = {"status": "PASS", "optimizer_calls": 0, "point_reads": 0,
              "scope": "coefficient identities, full customer-type domain, explicit multiplicity correction",
              "families": []}
    total = 0
    for r in (4, 5, 6):
        m, N = r - 2, 7 - r
        alpha, C = 5 * (r - 1), 6 * r - 5
        a0, astar = F(r - 1, 12), F(5 * r - 6, r * (r - 1))
        assert astar >= a0
        w = weights(r)
        count = negative_unrepaired = zero_repaired = 0
        min_positive = None
        penalty_table = []
        for n, k, d in product(range(1, N + 1), range(m + 1), range(7)):
            theta, D = F(d, 6), n + r - 1
            penalties = [j * (theta / (n * (n + j)) - astar / (n + k))
                         for j in range(m + 1)]
            penalty = max(penalties)
            assert penalty >= 0
            simple = F(max(d - 1, 0) * m, 6 * n * (n + m))
            assert penalty <= simple
            if F(d) <= 12 * astar / (r - 1):
                assert penalty == 0
            if d <= 1:
                assert penalty == 0
            # The penalty exactly repairs the worst x=0 hidden state.
            worst_xzero = min(remainder(r, n, k, 0, ys, t, theta, w)
                              for ys in product((0, 1), repeat=m) for t in (0, 1))
            assert max(F(0), -worst_xzero) == penalty
            penalty_table.append({"n": n, "k": k, "d": d,
                                  "Pi": str(penalty), "simple_upper": str(simple)})
            for bits in product((0, 1), repeat=m + 2):
                x, ys, t = bits[0], bits[1:-1], bits[-1]
                j = sum(ys)
                E = remainder(r, n, k, x, ys, t, theta, w)
                # Independent construction from target minus the four budgets.
                u = F(17, 13)  # an arbitrary formal scalar; its coefficient cancels
                target = C * u - (C - 1) * F(x, D)
                target -= theta * (F(x, D) + F(1 - x, n))
                pay = alpha * (u - F(x, n + j + t))
                pay += r * (u - F(t, D))
                pay += sum(astar * F(x - y, n + k) for y in ys)
                pay += F(t, n + x + j) - theta / (n + x + j)
                assert target - pay == E
                if x:
                    assert E >= 0
                    corner = remainder(r, n, 0, x, ys, t, F(0), w)
                    assert E >= corner >= 0
                elif t:
                    assert E >= 0
                else:
                    assert E == j * (astar / (n + k) - theta / (n * (n + j)))
                fixed = E + (1 - x) * penalty
                assert fixed >= 0
                negative_unrepaired += E < 0
                zero_repaired += fixed == 0
                if fixed > 0:
                    min_positive = fixed if min_positive is None else min(min_positive, fixed)
                # The lower endpoint a0 also works with its own exact correction.
                wa0 = weights(r, a0)
                pa0 = max(jj * (theta / (n * (n + jj)) - a0 / (n + k))
                          for jj in range(m + 1))
                assert remainder(r, n, k, x, ys, t, theta, wa0) + (1 - x) * pa0 >= 0
                assert penalty <= pa0
                count += 1
        # A three-positive-type exact dual for the full nonsymmetric 2r cone.
        theta = F(1, 6)
        A = affine_row(r, 1, 0, 0, (0,) * m, 0, theta)
        G = affine_row(r, 1, m, 0, (0,) * m, 1, theta)
        H = affine_row(r, N, 0, 1, (1,) * m, 0, theta)
        combined = [(30 * r - 5) * a + 6 * r * g + 30 * h
                    for a, g, h in zip(A, G, H)]
        B = F(30, N) - F(6 * r, r - 1)
        assert B > 0
        for q in range(1, 1 + m):
            combined[q] += 1
        combined[-3] += B  # a_T; last entries are a_T, delta, affine constant
        desired = [F(0)] * (2 * r + 1)
        desired[0] = F(1)
        for q in range(1, 2 + m):
            desired[q] = F(1)
        desired[-1] = -F(C)
        assert combined == desired
        assert remainder(r, 1, 0, 0, (0,) * m, 0, theta, w) == 0
        assert remainder(r, 1, m, 0, (0,) * m, 1, theta, w) == 0
        assert remainder(r, N, 0, 1, (1,) * m, 0, theta, w) == 0
        endpoints = [astar * F((n + m) * (n + r - 1), n) for n in (1, N)]
        assert max(endpoints) <= alpha - 1
        result["families"].append({
            "r": r, "source": 7 - r, "C": C, "alpha": alpha,
            "a_star": str(astar), "a_lower": str(a0),
            "type_count": count, "negative_without_correction": negative_unrepaired,
            "zero_after_correction": zero_repaired,
            "min_positive_after_correction": str(min_positive),
            "G_endpoints": list(map(str, endpoints)),
            "restricted_cone": {"theta": "1/6", "variables": 2 * r,
                "dual_weights_A_G_H": [30 * r - 5, 6 * r, 30],
                "middle_SAFE_reduced_cost": "1", "terminal_MAX_reduced_cost": str(B),
                "optimum": C, "all_columns_exact": True},
            "penalty_table": penalty_table})
        total += count
    assert total == 5040
    result["full_ordered_customer_types"] = total
    result["parameter_endpoint_checks"] = 2 * total
    for suffix in ("md", "py"):
        p = HERE / ("main_averaged_menu_prefix." + suffix)
        result["source_" + suffix + "_sha256"] = hashlib.sha256(p.read_bytes()).hexdigest()
    out = HERE / "main_averaged_menu_prefix.json"
    assert not out.exists(), "Do not overwrite a frozen audit; use a new output path."
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "types": total, "endpoint_checks": 2 * total,
                      "restricted_optima": [19, 25, 31], "optimizer_calls": 0,
                      "output": str(out), "sha256": hashlib.sha256(out.read_bytes()).hexdigest()}))


if __name__ == "__main__":
    run()
