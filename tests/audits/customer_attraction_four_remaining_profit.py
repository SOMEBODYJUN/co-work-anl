#!/usr/bin/env python3
"""Exact coefficient audit for the four-remaining arbitrary-background bound.

Imports no old audit, game solver, LP package, or polynomial library.  The
complete customer type cases audit an explicit universal symbolic identity.
"""
from __future__ import annotations

import argparse
import hashlib
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import platform
import subprocess


# (p+1)(p+2)(p+3)(p+4)/(p+j); P[0] handles zero numerators.
P = ((0, 0, 0, 0), (24, 26, 9, 1), (12, 19, 8, 1),
     (8, 14, 7, 1), (6, 11, 6, 1))
# The same common denominator divided by (p+j)(p+j+1).
Q = ((12, 7, 1, 0), (4, 5, 1, 0), (2, 3, 1, 0))


def add(*terms):
    return tuple(sum(F(weight) * poly[j] for weight, poly in terms) for j in range(4))


def evaluate(poly, p):
    return sum(F(v) * p**j for j, v in enumerate(poly))


def share(bit, denominator):
    return F(bit, denominator) if bit else F(0)


def D4(p):
    return (p + 1) * (p + 2) * (p + 3) * (p + 4)


def tax(p, v):
    return F(1, p + 1) - F(1, p + v + 1)


def delta2(p, v):
    return tax(p, v) + (F(2, 3) * p**2 / D4(p) if v == 2 else 0)


def delta3(p, v):
    return tax(p, v) + (F(p**2 + p) / D4(p) if v == 3 else 0)


def delta2_poly(v):
    return add((1, P[1]), (-1, P[v + 1]),
               (F(2, 3) if v == 2 else 0, (0, 0, 1, 0)))


def delta3_poly(v):
    return add((1, P[1]), (-1, P[v + 1]),
               (1 if v == 3 else 0, (0, 1, 1, 0)))


def pair_gap_poly(v, e):
    # 3 D4 times the exact optimal-theme-pair lower-bound gap.
    return add((e * (4 - e), P[v + 1]), (e * (e - 1), P[v + 2]),
               (3, delta2_poly(v)), (-3 * e, P[e]))


def last_gap_poly(v, e):
    # D4 times the actual last-node aggregation gap.
    return add((e, P[v + 1]), (1, delta3_poly(v)), (-e, P[e]))


def rho_poly(eta):
    a, b, c, d, q, r, s = eta
    actual, branch = a + b + c + d, d + q + r + s
    ua = [tuple(bit * x for x in P[actual]) for bit in (a, b, c, d)]
    z = [tuple(bit * x for x in P[branch]) for bit in (d, q, r, s)]
    K = lambda bit: add((1, ua[1]), (-bit, P[a + 3]))
    H = add((1, ua[2]), (1, ua[3]), (c, Q[a + b]))
    pp = add((2, H), (1, delta2_poly(a + b)))
    ee = add((4, ua[3]), (1, delta3_poly(a + b + c)))
    root = add((1, ua[0]), (-1, z[0]))
    lqs = add((1, z[1]), (-s, P[d + 3]))
    lrc = add((1, z[2]), (-c, P[d + q + 2]))
    lrs = add((1, z[2]), (-s, P[d + q + 2]))
    lsb = add((1, z[3]), (-b, P[d + q + r + 1]))
    g = add((341, K(c)), (302, K(d)), (306, K(q)), (302, K(r)),
            (355, K(s)), (354, ee), (646, pp), (1267, root),
            (24, lqs), (8, lrc), (17, lrs), (108, lsb))
    result = add((23984 * actual, P[actual]), (-12, g))
    assert all(x.denominator == 1 for x in result)
    return tuple(int(x) for x in result)


def direct_rho(eta, p):
    a, b, c, d, q, r, s = eta
    actual, branch = a + b + c + d, d + q + r + s
    u = [share(bit, p + actual) for bit in (a, b, c, d)]
    z = [share(bit, p + branch) for bit in (d, q, r, s)]
    K = lambda bit: u[1] - F(bit, p + a + 3)
    H = u[2] + u[3] + F(c, (p + a + b + 1) * (p + a + b + 2))
    pp = 2 * H + delta2(p, a + b)
    ee = 4 * u[3] + delta3(p, a + b + c)
    root = u[0] - z[0]
    lqs = z[1] - F(s, p + d + 3)
    lrc = z[2] - F(c, p + d + q + 2)
    lrs = z[2] - F(s, p + d + q + 2)
    lsb = z[3] - F(b, p + d + q + r + 1)
    g = F(1, 1000) * (
        341 * K(c) + 302 * K(d) + 306 * K(q) + 302 * K(r) + 355 * K(s)
        + 354 * ee + 646 * pp + 1267 * root
        + 24 * lqs + 8 * lrc + 17 * lrs + 108 * lsb)
    return F(1499, 750) * share(actual, p + actual) - g


def run():
    backgrounds = tuple(map(F, (0, 1, 2, 4, 17, 10**6))) + (F(5, 3),)
    pair_minima, last_minima = {}, {}
    for v in range(3):
        coeffs = [pair_gap_poly(v, e) for e in range(5)]
        assert all(min(coeff) >= 0 for coeff in coeffs)
        pair_minima[str(v)] = [str(min(c[j] for c in coeffs)) for j in range(4)]
        for e, coeff in enumerate(coeffs):
            for p in backgrounds:
                pairs = F(e * (4 - e), p + v + 1) + F(e * (e - 1), p + v + 2)
                gap = pairs / 3 + delta2(p, v) - share(e, p + e)
                assert evaluate(coeff, p) == 3 * D4(p) * gap
    for v in range(4):
        coeffs = [last_gap_poly(v, e) for e in range(5)]
        assert all(min(coeff) >= 0 for coeff in coeffs)
        last_minima[str(v)] = [str(min(c[j] for c in coeffs)) for j in range(4)]
        for e, coeff in enumerate(coeffs):
            for p in backgrounds:
                gap = F(e, p + v + 1) + delta3(p, v) - share(e, p + e)
                assert evaluate(coeff, p) == D4(p) * gap
    customer_minima = {}
    for actual in product((0, 1), repeat=4):
        coeffs = []
        for branch in product((0, 1), repeat=3):
            eta = (*actual, *branch)
            coeff = rho_poly(eta)
            assert min(coeff) >= 0, (eta, coeff)
            coeffs.append(coeff)
            for p in backgrounds:
                assert evaluate(coeff, p) == 12000 * D4(p) * direct_rho(eta, p)
        customer_minima[''.join(map(str, actual))] = [min(c[j] for c in coeffs) for j in range(4)]
    # Reconstruct six-pair sum directly from the four comparison membership bits.
    direct_pair_cases = 0
    for bits in product((0, 1), repeat=4):
        e = sum(bits)
        for v in range(3):
            for p in backgrounds:
                pair_sum = sum(share(bits[i] + bits[j], p + v + bits[i] + bits[j])
                               for i in range(4) for j in range(i + 1, 4))
                aggregate = F(e * (4 - e), p + v + 1) + F(e * (e - 1), p + v + 2)
                assert pair_sum == aggregate
                direct_pair_cases += 1
    return {'scope': 'exact_symbolic_customer_coefficient_audit',
            'theorem_claimed_by_audit': False,
            'pair_gap_coefficient_cases': 15,
            'last_gap_coefficient_cases': 20,
            'rho_coefficient_cases': 128,
            'rational_identity_cases': (15 + 20 + 128) * len(backgrounds),
            'direct_pair_cases': direct_pair_cases,
            'backgrounds': list(map(str, backgrounds)),
            'pair_gap_coefficient_minima': pair_minima,
            'last_gap_coefficient_minima': last_minima,
            'rho_coefficient_minima_by_actual': customer_minima}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = run()
    root = Path(__file__).resolve().parents[2]
    report.update(
        python_version=platform.python_version(),
        base_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip(),
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        replay_commands=['python3 tests/audits/customer_attraction_four_remaining_profit.py'],
        randomness='none; all legal binary customer types enumerated')
    print(json.dumps(report, indent=2))
    if args.output:
        if args.output.exists():
            raise FileExistsError(args.output)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    main()
