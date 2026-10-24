"""Targeted refutation test of AP-extra's pairwise sufficient claim.

One fixed six-topic, three-player complete strategy, with variable nonnegative
integer-type weights relaxed to reals; the fixed pair is X2,Y2. This is not an
instance scan and a nonpositive optimum is not a general result.
"""
import itertools
import json
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

K = 6
M = 3
PAIR = (2, 5)
TYPES = list(range(1, 1 << K))


def action(h):
    if not h:
        return 0
    if len(h) == 1:
        return 3 if h[0] < 3 else 0
    group = range(0, 3) if h[-1] < 3 else range(3, 6)
    return next(a for a in group if a not in h)


def leaf(h):
    h = tuple(h)
    while len(h) < M:
        h += (action(h),)
    return h


def payoff_coeff(z, i):
    a = z[i]
    return [
        Fraction(bool(mask & (1 << a)), sum(bool(mask & (1 << b)) for b in z))
        if mask & (1 << a)
        else Fraction(0)
        for mask in TYPES
    ]


def extra_coeff(z, a):
    return [
        Fraction(bool(mask & (1 << a)), 1 + sum(bool(mask & (1 << b)) for b in z))
        for mask in TYPES
    ]


def main():
    actual = leaf(())
    welfare = [int(any(mask & (1 << a) for a in actual)) for mask in TYPES]
    rows = []
    for depth in range(M):
        for h in itertools.product(range(K), repeat=depth):
            u = payoff_coeff(leaf(h), depth)
            for a in range(K):
                v = payoff_coeff(leaf(h + (a,)), depth)
                rows.append([x - y for x, y in zip(u, v)])
    pairwise = [Fraction(0) for _ in TYPES]
    a, b = PAIR
    for i in range(M):
        first = extra_coeff(leaf(actual[:i] + (b,)), a)
        second = extra_coeff(leaf(actual[:i] + (a,)), b)
        pairwise = [s + x + y for s, x, y in zip(pairwise, first, second)]
    objective = [x - 2 * w for x, w in zip(pairwise, welfare)]
    result = linprog(
        -np.array(objective, dtype=float),
        A_ub=-np.array(rows, dtype=float),
        b_ub=np.zeros(len(rows)),
        A_eq=[welfare],
        b_eq=[1],
        bounds=(0, None),
        method="highs",
    )
    out = {
        "precise_candidate": "for every complete SPE and every A,B, sum_i(extra(Z_i(B),A)+extra(Z_i(A),B)) <= 2W",
        "fixed_strategy": "group opposite then last-action group fresh topic; root X0",
        "fixed_pair": list(PAIR),
        "status": result.message,
        "success": result.success,
        "actual": list(actual),
    }
    if result.success:
        out["numeric_max_pairwise_minus_2W_at_W1"] = -float(result.fun)
        out["numeric_nonzero_type_weights"] = {
            str(mask): float(v) for mask, v in zip(TYPES, result.x) if v > 1e-8
        }
    print(json.dumps(out, indent=2))
    Path(__file__).with_suffix(".json").write_text(json.dumps(out, indent=2) + "\n")


if __name__ == "__main__":
    main()
