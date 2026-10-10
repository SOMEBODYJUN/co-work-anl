#!/usr/bin/env python3
"""Independent exact arithmetic for the three-remaining background bound.

Does not import the game solver, sharp-three audit, or LP exploration.  The
proof's finite membership cases concern one customer, not sampled games.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import hashlib
import platform
import subprocess


P = ((0, 0, 0), (6, 5, 1), (3, 4, 1), (2, 3, 1))


def share(bit, denominator):
    return F(bit, denominator) if bit else F(0)


def coefficients(a, b, c, q, r, d, ell):
    s = a + b + c
    terms = (
        (50 * s - 29 * a - 36 * b - 57 * c, P[s]),
        (-30 * d, P[d]),
        (6 * q + 9 * r, P[3]),
        (17 * d + 2 * ell, P[a + b + 1]),
        (12 * d, P[a + 1]),
        (-4 * d * ell, (3 - 2 * a, 1, 0)),
        (14 * c - 3 * r, P[c + q + r]),
        (d, P[c + q + 1]),
    )
    return tuple(sum(weight * polynomial[j] for weight, polynomial in terms)
                 for j in range(3))


def expanded_g(p, a, b, c, q, r, d, ell):
    s = a + b + c
    alpha, beta, gamma = (share(bit, p + s) for bit in (a, b, c))
    return (
        29 * alpha + 36 * beta + 57 * gamma
        - F(6 * q + 9 * r, p + 3)
        - F(17 * d + 2 * ell, p + a + b + 1)
        - F(12 * d, p + a + 1)
        + F(4 * d * ell, (p + a + 1) * (p + a + 2))
        - 14 * share(c, p + c + q + r)
        + 3 * share(r, p + c + q + r)
        - F(d, p + c + q + 1)
    )


def direct_slack_g(p, a, b, c, q, r, ts, ls):
    s = a + b + c
    alpha, beta, gamma = (share(bit, p + s) for bit in (a, b, c))
    Kq = 3 * alpha - F(3 * q, p + 3)
    Kr = 3 * alpha - F(3 * r, p + 3)
    Psum = sum(gamma - F(t, p + 1 + a + b) for t in ts)
    Zsum = sum(gamma - F(l, p + 1 + a + b) for l in ls)
    Ssum = sum(beta - F(t, p + 1 + a + l) for t, l in zip(ts, ls))
    Vsum = sum(F(ls[i] - ls[j], p + 1 + a + ts[i])
               for i in range(3) for j in range(3) if i != j)
    root = alpha - share(c, p + c + q + r)
    Jsum = sum(share(r, p + c + q + r) - F(t, p + 1 + c + q) for t in ts)
    return 2 * Kq + 3 * Kr + 17 * Psum + 2 * Zsum + 12 * Ssum + 4 * Vsum + 14 * root + Jsum


def run():
    minima = {}
    all_coefficient_cases = 0
    identity_cases = 0
    backgrounds = tuple(map(F, (0, 1, 2, 7, 101, 10**6))) + (F(5, 3),)
    for a, b, c, q, r in product((0, 1), repeat=5):
        row_min = [None] * 3
        for d, ell in product(range(4), repeat=2):
            coeff = coefficients(a, b, c, q, r, d, ell)
            assert min(coeff) >= 0, (a, b, c, q, r, d, ell, coeff)
            for j in range(3):
                row_min[j] = coeff[j] if row_min[j] is None else min(row_min[j], coeff[j])
            all_coefficient_cases += 1
            for p in backgrounds:
                G = expanded_g(p, a, b, c, q, r, d, ell)
                target = 50 * share(a + b + c, p + a + b + c) - 30 * share(d, p + d)
                polynomial = sum(F(z) * p**j for j, z in enumerate(coeff))
                assert target - G == polynomial / ((p + 1) * (p + 2) * (p + 3))
                identity_cases += 1
        minima[f'{a}{b}{c}{q}{r}'] = row_min
    direct_cases = 0
    for bits in product((0, 1), repeat=11):
        a, b, c, q, r = bits[:5]
        ts, ls = bits[5:8], bits[8:]
        d, ell = sum(ts), sum(ls)
        for p in backgrounds:
            assert direct_slack_g(p, a, b, c, q, r, ts, ls) == expanded_g(p, a, b, c, q, r, d, ell)
            direct_cases += 1
    root = Path(__file__).resolve().parents[2]
    return {'scope': 'exact_customer_identity_and_complete_coefficient_cases',
            'python_version': platform.python_version(),
            'base_commit': subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
            'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'replay_commands': ['python3 tests/audits/customer_attraction_three_remaining_profit.py'],
            'randomness': 'none; all coefficient and binary membership cases enumerated',
            'theorem_claimed_by_audit': False,
            'coefficient_cases': all_coefficient_cases,
            'rational_identity_cases': identity_cases,
            'direct_slack_cases': direct_cases,
            'backgrounds': [str(p) for p in backgrounds],
            'coefficient_minima_by_abcqr': minima}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = run()
    print(json.dumps(report, indent=2))
    if args.output:
        if args.output.exists():
            raise FileExistsError(args.output)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    main()
