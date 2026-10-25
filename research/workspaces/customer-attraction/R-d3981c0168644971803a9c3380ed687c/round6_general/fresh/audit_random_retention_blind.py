"""Independent finite arithmetic regression for random-retention identities.

This does not test or prove Q-CAG-HALF.  General proofs and the precise
auxiliary-game scope are in random_retention_blind_review.md.
Only Python's standard library is used; no author or repository model import.
"""

from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path
import json


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def resource(b, t):
    return F(t, b + t) if t else F(0)


def d_op(r, n, values):
    denominator = choose(r, n)
    result = []
    for t in range(r + 1):
        mean = sum(
            (F(choose(t, k) * choose(r - t, n - k), denominator) * values[k]
             for k in range(n + 1)), F(0)
        )
        result.append(F(r, n) * mean)
    return result


def is_concave(values):
    increments = [v - u for u, v in zip(values, values[1:])]
    return all(a >= b >= 0 for a, b in zip(increments, increments[1:]))


coefficient_checks = 0
subset_samples = 0
for r in range(1, 9):
    for n in range(1, r + 1):
        retained = list(combinations(range(r), n))
        for t in range(1, r + 1):
            covered = set(range(t))
            conditional = [R for R in retained if 0 in R]
            for b in range(5):
                direct = sum((F(1, b + len(covered.intersection(R)))
                              for R in conditional), F(0)) / len(conditional)
                subset_samples += len(conditional)
                pooled = sum((resource(b, len(covered.intersection(R)))
                              for R in retained), F(0)) / len(retained)
                conditional_formula = sum(
                    (F(choose(t - 1, j) * choose(r - t, n - 1 - j),
                       choose(r - 1, n - 1)) / (b + 1 + j)
                     for j in range(n)), F(0)
                )
                a = F(r, n * t) * pooled
                u = F(1, b + t)
                q = F(r, n) * u - a
                assert direct == a == conditional_formula
                assert u <= a <= F(r, n) * u
                assert 0 <= q <= F(r - n, n) * u
                assert t * q == F(r, n) * (resource(b, t) - pooled)
                if b == 0:
                    p_zero = F(choose(r - t, n), choose(r, n))
                    assert a == F(r, n * t) * (1 - p_zero)
                    assert t * q == F(r, n) * p_zero
                if n == r:
                    assert q == 0
                if n == 1:
                    assert a == F(1, b + 1)
                if r > 1 and n == r - 1:
                    assert q == (resource(b, t) - resource(b, t - 1)) / (r - 1)
                coefficient_checks += 1


operator_checks = 0
cocycle_checks = 0
for r in range(1, 9):
    examples = [[resource(b, t) for t in range(r + 1)] for b in range(5)]
    examples.append([F(t) for t in range(r + 1)])
    examples.append([F(min(t, 3)) for t in range(r + 1)])
    examples.append([sum((F(1, j) for j in range(1, t + 1)), F(0))
                     for t in range(r + 1)])
    for values in examples:
        assert is_concave(values)
        for n in range(1, r + 1):
            d_rn = d_op(r, n, values)
            assert is_concave(d_rn)
            q_rn = [F(r, n) * f - d for f, d in zip(values, d_rn)]
            assert all(0 <= q <= F(r - n, n) * f
                       for f, q in zip(values, q_rn))
            assert all(d >= f for f, d in zip(values, d_rn))
            operator_checks += 1
            for k in range(1, n + 1):
                d_nk = d_op(n, k, values)
                d_rk = d_op(r, k, values)
                assert d_op(r, n, d_nk) == d_rk
                q_nk = [F(n, k) * f - d
                        for f, d in zip(values[:n + 1], d_nk)]
                propagated = d_op(r, n, q_nk)
                q_rk = [F(r, k) * f - d for f, d in zip(values, d_rk)]
                assert q_rk == [F(n, k) * q + p
                                for q, p in zip(q_rn, propagated)]
                cocycle_checks += 1


five_table = {}
for n in range(1, 6):
    d = d_op(5, n, [resource(0, t) for t in range(6)])
    five_table[str(n)] = [str(F(5, n) - d[t]) for t in range(1, 6)]

result = {
    "status": "passed",
    "scope": "finite independent coefficient regression only; no SPE/half theorem",
    "coefficient_domain": {"r": [1, 8], "n": "1..r", "t": "1..r", "b": [0, 4]},
    "coefficient_checks": coefficient_checks,
    "enumerated_conditional_samples": subset_samples,
    "concavity_operator_checks": operator_checks,
    "semigroup_and_cocycle_checks": cocycle_checks,
    "five_player_total_defect_by_n_and_positive_t": five_table,
}
target = Path(__file__).with_suffix(".json")
target.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
