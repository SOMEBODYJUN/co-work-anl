"""Exact finite audit of the anchored cut lift; no SPE or LP oracle.

The general claims are proved in anchored_cut_lift.md. This script compares
direct customer shares with independent Boolean interpolation and enumerates
all auxiliary bit assignments in small lifts, including inconsistent ones.
"""

from fractions import Fraction as F
from itertools import combinations, product
from math import ceil
import argparse
import json
from pathlib import Path


def subsets(s, nonempty=False):
    s = tuple(sorted(s))
    for k in range(1 if nonempty else 0, len(s) + 1):
        yield from map(frozenset, combinations(s, k))


def counts(p, m):
    if p == 1:
        yield (m,)
        return
    for first in range(m + 1):
        for rest in counts(p - 1, m - first):
            yield (first,) + rest


def family(p, m):
    return tuple(a for a in subsets(range(p), True) if len(a) <= ceil(m / 2))


def penalties(z):
    result = []
    for a, y in z.items():
        if len(a) < 2:
            continue
        b = frozenset((max(a),))
        d = a - b
        x, v = z[d], z[b]
        result.append(x * v - 2 * x * y - 2 * v * y + 3 * y)
    return result


def lifted_moment(z, a):
    if len(a) == 1:
        return z[a]
    ordered = sorted(a)
    first = frozenset(ordered[: len(ordered) // 2])
    second = frozenset(ordered[len(ordered) // 2 :])
    # Compute through anchored distances, rather than multiplying directly.
    d = abs(z[first] - z[second])
    return F(z[first] + z[second] - d, 2)


def theta(q, a, support):
    result = {}
    for t in subsets(support, True):
        if a not in t:
            continue
        value = F(0)
        for r in subsets(t - {a}):
            sign = (-1) ** (len(t) - 1 - len(r))
            value += F(sign, q[a] + sum(q[b] for b in r))
        result[t] = value
    return result


def audit():
    report = {
        "status": "finite exact formula audit; not a proof of general half",
        "and_truth_table": [],
        "face_cases": [],
        "payoff_checks": 0,
        "coverage_checks": 0,
        "distance_inverse_checks": 0,
        "complete_ordered_history_comparison_checks": 0,
        "penalty_completion_checks": 0,
    }
    for x, v, y in product((0, 1), repeat=3):
        p = x * v - 2 * x * y - 2 * v * y + 3 * y
        assert p >= 0 and ((p == 0) == (y == x * v))
        report["and_truth_table"].append([x, v, y, p])

    # Includes all 2^14 assignments of the (p,m)=(4,5) auxiliary system.
    for p, m in ((1, 1), (3, 2), (3, 3), (3, 4), (4, 4), (4, 5)):
        aa = family(p, m)
        zero_count = 0
        for bits in product((0, 1), repeat=len(aa)):
            z = dict(zip(aa, bits))
            pp = penalties(z)
            assert min(pp, default=0) >= 0
            expected = all(z[a] == product_bit(z, a) for a in aa)
            assert (sum(pp) == 0) == expected
            zero_count += sum(pp) == 0
        assert zero_count == 2**p
        report["face_cases"].append(
            {"p": p, "m": m, "auxiliary_labels": len(aa),
             "all_assignments": 2**len(aa), "zero_face_assignments": zero_count}
        )

    # Direct reciprocals are independent of the interpolation implementation.
    for p in range(1, 5):
        original_types = tuple(subsets(range(p)))
        for m in range(1, 7):
            aa = family(p, m)
            for b in original_types:
                z = {a: int(a <= b) for a in aa}
                for t in subsets(range(p), True):
                    if len(t) > m:
                        continue
                    assert lifted_moment(z, t) == int(t <= b)
                    coverage = sum(
                        (-1) ** (len(a) + 1) * lifted_moment(z, a)
                        for a in subsets(t, True)
                    )
                    assert coverage == int(bool(t & b))
                    report["coverage_checks"] += 1
                if m % 2 == 0:
                    for a, d in combinations(aa, 2):
                        direct = abs(z[a] - z[d])
                        inverse = (
                            lifted_moment(z, a) + lifted_moment(z, d)
                            - 2 * lifted_moment(z, a | d)
                        )
                        assert direct == inverse
                        report["distance_inverse_checks"] += 1
            for q in counts(p, m):
                support = frozenset(a for a in range(p) if q[a])
                for a in support:
                    coeff = theta(q, a, support)
                    for b in original_types:
                        direct = F(1, sum(q[t] for t in b)) if a in b else F(0)
                        z = {t: int(t <= b) for t in aa}
                        lifted = sum(v * lifted_moment(z, t) for t, v in coeff.items())
                        assert direct == lifted
                        report["payoff_checks"] += 1

    # Formal policies deliberately distinguish ordered histories with equal
    # counts. A policy need not be an SPE for this coefficient identity.
    for p, m in ((3, 3), (3, 4), (4, 3)):
        aa = family(p, m)

        def action(h):
            return (len(h) + sum((i + 1) * (a + 1) for i, a in enumerate(h))) % p

        def terminal(h):
            h = tuple(h)
            while len(h) < m:
                h += (action(h),)
            return tuple(h.count(a) for a in range(p))

        for length in range(m):
            for h in product(range(p), repeat=length):
                selected = action(h)
                actual_q = terminal(h)
                actual_coeff = theta(actual_q, selected, frozenset(a for a in range(p) if actual_q[a]))
                for alternative in range(p):
                    alternative_q = terminal(h + (alternative,))
                    alternative_coeff = theta(alternative_q, alternative, frozenset(a for a in range(p) if alternative_q[a]))
                    for b in subsets(range(p)):
                        z = {t: int(t <= b) for t in aa}
                        direct_actual = F(1, sum(actual_q[a] for a in b)) if selected in b else F(0)
                        direct_alternative = F(1, sum(alternative_q[a] for a in b)) if alternative in b else F(0)
                        lifted_actual = sum(v * lifted_moment(z, t) for t, v in actual_coeff.items())
                        lifted_alternative = sum(v * lifted_moment(z, t) for t, v in alternative_coeff.items())
                        assert direct_actual - direct_alternative == lifted_actual - lifted_alternative
                        report["complete_ordered_history_comparison_checks"] += 1

    # Positive original polynomials with auxiliary AND inconsistencies.
    # R=x_0(1-x_1), R=(x_0-x_1)^2 and a coverage row.
    p, m = 3, 4
    aa = family(p, m)
    rows = (
        {frozenset((0,)): F(1), frozenset((0, 1)): F(-1)},
        {frozenset((0,)): F(1), frozenset((1,)): F(1), frozenset((0, 1)): F(-2)},
        {a: F((-1) ** (len(a) + 1)) for a in subsets(range(p), True)},
    )
    for row in rows:
        lifted_coeff = {}
        for a, value in row.items():
            if len(a) == 1:
                term = (a,)
            else:
                ordered = sorted(a)
                term = (frozenset(ordered[:len(a)//2]), frozenset(ordered[len(a)//2:]))
            term = tuple(sorted(term, key=lambda s: tuple(sorted(s))))
            lifted_coeff[term] = lifted_coeff.get(term, F(0)) + value
        big_m = sum(-v for v in lifted_coeff.values() if v < 0)
        for bits in product((0, 1), repeat=len(aa)):
            z = dict(zip(aa, bits))
            value = sum(v * multiply(z[t] for t in term) for term, v in lifted_coeff.items())
            assert value + big_m * sum(penalties(z)) >= 0
            report["penalty_completion_checks"] += 1
    return report


def product_bit(z, a):
    return multiply(z[frozenset((b,))] for b in a)


def multiply(values):
    result = 1
    for value in values:
        result *= value
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = json.dumps(audit(), indent=2)
    print(result)
    if args.output:
        with args.output.open("x") as target:
            target.write(result + "\n")
