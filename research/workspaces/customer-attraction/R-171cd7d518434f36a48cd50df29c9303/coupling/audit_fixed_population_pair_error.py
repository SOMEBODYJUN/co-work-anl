#!/usr/bin/env python3
"""Exact direct-payoff audit, without importing any other author script."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import json


def own(numerator, denominator):
    return F(numerator, denominator) if numerator else F(0)


def error(h, r, s, a, b):
    return (r * s * own(a, h + r * a + s * b)
            + r * (r - s) * own(b, h + s * a + r * b)
            - s * s * own(a, h + s * a + r * b)
            - (r - s) * F(b, h + 1))


def ghost(h, a, b):
    return h * (F(1, h + 1) - F(1, h + 1 + a + b))


def run():
    local_cases = 0
    for h in (*range(33), 64, 127, 1000):
        for r in range(2, 17):
            for s in range(1, r):
                for a, b in product((0, 1), repeat=2):
                    e = error(h, r, s, a, b)
                    if not a and not b:
                        table = F(0)
                    elif a and not b:
                        table = F((r - s) * h * s, (h + r) * (h + s))
                    elif b and not a:
                        table = F((r - s) * h * (r - 1), (h + r) * (h + 1))
                    else:
                        table = F((r - s) * h * (r + s - 1),
                                  (h + r + s) * (h + 1))
                    assert e == table
                    assert 0 <= e <= (r - s) * (r - 1) * ghost(h, a, b)
                    if r == 2 and s == 1:
                        assert e == ghost(h, a, b)
                    local_cases += 1
    path_cases = 0
    for m in range(1, 12):
        for bits in product((0, 1), repeat=m):
            for mode in (0, 1):
                b = 0
                weighted = F(0)
                dominating_ghost = F(0)
                for j in range(1, m - 2):
                    b += bits[j - 1]
                    n = m - j
                    s = 1 if mode == 0 else (n - 1) // 2
                    r = n - s
                    assert r > s >= 1 and j + r + s == m
                    beta = (r - s) * (r - 1)
                    weighted += error(b, r, s, bits[j], bits[j + 1]) / (j * beta)
                    dominating_ghost += ghost(b, bits[j], bits[j + 1]) / j
                c = sum(bits)
                cap = 1 - F(2, c + 1) if c else F(0)
                assert weighted <= dominating_ghost <= cap
                assert cap <= (1 if c else 0)
                path_cases += 1
    return {'status': 'all direct-payoff and fixed-population path checks passed',
            'scope': 'algebraic errors and arbitrary actual paths; no SPE transport constructed',
            'local_membership_cases': local_cases, 'fixed_population_path_cases': path_cases,
            'all_primary_pair_profiles_have_exactly_m_players': True,
            'uniform_comparison_factor': '(r-s)*(r-1)'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = json.dumps(run(), ensure_ascii=False, indent=2)
    if args.output:
        with args.output.open('x', encoding='utf-8') as out:
            out.write(result + '\n')
    print(result)
