#!/usr/bin/env python3
"""Tiny exact regression for extension.md; not a replacement for its proof."""
from fractions import Fraction as Q
from itertools import product
import json


def run():
    r, s = Q(11, 12), Q(5, 4)  # m=3 prefix loads, normalized at H.
    attaining = minorants = comparisons = 0
    for n in range(6):
        xn, xnext = r**n, r**(n + 1)
        yn, ynext = s**n, s**(n + 1)
        slope = (yn - ynext) / (xn - xnext)

        def line(x):
            return yn + slope * (x - xn)

        assert slope < 0
        for k in range(13):
            assert line(r**k) <= s**k
            assert (line(r**k) == s**k) == (k in (n, n + 1))
            minorants += 1
        for theta in (Q(0), Q(1, 4), Q(1, 2), Q(3, 4), Q(1)):
            epsilon = theta * xn + (1 - theta) * xnext
            optimum = theta * yn + (1 - theta) * ynext
            assert line(epsilon) == optimum
            attaining += 1
            for coefficients in product(range(3), repeat=5):
                total = sum(coefficients)
                if not total:
                    continue
                z = sum((Q(a, total) * r**k
                         for k, a in enumerate(coefficients)), Q(0))
                y = sum((Q(a, total) * s**k
                         for k, a in enumerate(coefficients)), Q(0))
                if z <= epsilon:
                    assert y >= optimum
                    comparisons += 1
    # Exact counterexample to extending the coarse exponent to m=2.
    lo, mid, hi, epsilon = Q(5, 4), Q(3, 2), Q(7, 4), Q(5, 6)
    assert lo == epsilon * mid
    assert hi < mid / epsilon
    return {
        'tool': 'sharp adjacent-monomial three-load tradeoff',
        'arithmetic': 'fractions.Fraction',
        'attaining_polynomial_cases': attaining,
        'affine_minorant_cases': minorants,
        'feasible_polynomial_comparisons': comparisons,
        'm2_coarse_exponent_counterexample': 'verified exactly',
        'result': 'all exact checks passed',
    }


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
