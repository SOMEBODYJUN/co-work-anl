#!/usr/bin/env python3
"""Exact finite checks for WC-R1-PREFIX-SMOOTHING v1; not its general proof.

Run from any directory: python3 verify.py
Only Python standard library is required. All comparisons use Fraction/integer.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json
import platform


def evaluate(coefficients, x):
    value = Q(0)
    for coefficient in reversed(coefficients):
        value = value * x + coefficient
    return value


def literal_load(m, one_second, later_first):
    weights = [Q(1, 2**i) for i in range(m + 1)]
    state = [0, int(one_second)] + [0 if later_first else 1] * (m - 1)
    strategies = []
    for i, action in enumerate(state):
        if i == 0:
            strategies.append({(j, action) for j in range(m + 1)})
        else:
            strategies.append({(j, action) for j in range(i)} | {(i, 1 - action)})
    return sum((weights[i] for i, s in enumerate(strategies) if (1, 0) in s), Q(0))


def run():
    geometry = 0
    literal = 0
    polynomial = 0
    degree_bound = 0
    zero_constant = 0
    for m in range(3, 41):
        delta = Q(1, 2**m)
        lo, mid, hi = Q(3, 2) - delta, Q(3, 2), 2 - delta
        r = 2**(m - 2)
        assert (hi - mid) / hi >= Q(3, 16)
        assert (mid - lo) / lo <= 8 * delta / 11
        assert Q(33, 128) / delta > r
        geometry += 1
        assert literal_load(m, False, True) == lo
        assert literal_load(m, True, False) == mid
        assert literal_load(m, True, True) == hi
        literal += 3
    # Enumerate every nonzero coefficient vector in {0,1,2}^6, including
    # constants, internal zero coefficients, and all single monomials.
    vectors = [c for c in product(range(3), repeat=6) if any(c)]
    for m in range(3, 9):
        lo, mid, hi = Q(3, 2) - Q(1, 2**m), Q(3, 2), 2 - Q(1, 2**m)
        r = 2**(m - 2)
        # Independent exact check of the load-spacing implication used in (3).
        assert hi * lo**r >= mid**(r + 1)
        for c in vectors:
            pl, ph, pu = (evaluate(c, x) for x in (lo, mid, hi))
            assert pu * pl**r >= ph**(r + 1)
            polynomial += 1
            d = max(i for i, a in enumerate(c) if a)
            assert ph * lo**d <= pl * mid**d
            degree_bound += 1
    for c in ((0,), (1,), (7, 0, 0)):
        for x in (Q(1, 3), Q(3, 2), Q(7)):
            assert evaluate(c, x) == c[0]
            zero_constant += 1
    # Reversible demonstration of the distortion statement at epsilon=1/2.
    m = 6
    r = 2**(m - 2)
    minimum_K = 2**r
    assert minimum_K.bit_length() - 1 == r
    assert Q(1, 2)**r * minimum_K == 1
    return {
        'claim': 'WC-R1-PREFIX-SMOOTHING v1',
        'arithmetic': 'fractions.Fraction and arbitrary-precision integers',
        'python': platform.python_version(),
        'seed': None,
        'geometry_m': [3, 40],
        'geometry_cases': geometry,
        'literal_load_cases': literal,
        'polynomial_m': [3, 8],
        'coefficient_vectors': len(vectors),
        'coefficient_domain': '{0,1,2}^6 excluding zero',
        'polynomial_inequality_cases': polynomial,
        'degree_bound_cases': degree_bound,
        'zero_constant_cases': zero_constant,
        'epsilon_half_example': {'m': m, 'r': r, 'minimum_K': minimum_K},
        'result': 'all exact checks passed',
        'scope': 'finite regression evidence; the universal claim uses proof.md',
    }


if __name__ == '__main__':
    result = run()
    output = Path(__file__).with_name('results.json')
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
