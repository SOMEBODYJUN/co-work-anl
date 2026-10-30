#!/usr/bin/env python3
"""Exact polynomial checks plus explicitly finite envelope exploration.

Standard library only. Run from any directory; output goes beside this file.
No numerical result is used to certify the universal parameter ceiling.
"""

from fractions import Fraction as R
from pathlib import Path
import json
import math

# Sparse polynomials in (n,w,beta), with exact rational coefficients.
ZERO = (0, 0, 0)


def constant(x):
    return {ZERO: R(x)} if x else {}


def variable(i):
    e = [0, 0, 0]
    e[i] = 1
    return {tuple(e): R(1)}


def add(*polys):
    out = {}
    for p in polys:
        for e, c in p.items():
            out[e] = out.get(e, R(0)) + c
    return {e: c for e, c in out.items() if c}


def scale(p, x):
    return {e: c * R(x) for e, c in p.items() if c * R(x)}


def mul(*polys):
    out = constant(1)
    for p in polys:
        nxt = {}
        for e, c in out.items():
            for f, d in p.items():
                g = tuple(x + y for x, y in zip(e, f))
                nxt[g] = nxt.get(g, R(0)) + c * d
        out = {e: c for e, c in nxt.items() if c}
    return out


def square(p):
    return mul(p, p)


def evaluate_variable(p, i, x):
    out = {}
    for e, c in p.items():
        f = list(e)
        f[i] = 0
        f = tuple(f)
        out[f] = out.get(f, R(0)) + c * R(x) ** e[i]
    return {e: c for e, c in out.items() if c}


def derivative(p, i):
    out = {}
    for e, c in p.items():
        if e[i]:
            f = list(e)
            f[i] -= 1
            out[tuple(f)] = c * e[i]
    return out


n, w, beta = (variable(i) for i in range(3))
one = constant(1)
q = add(one, w)
a = square(q)
w2, w3 = square(w), mul(w, w, w)
nw = mul(n, w)


def F(t):
    return add(
        mul(n, add(a, constant(-t)), add(q, scale(nw, -t))),
        scale(mul(add(scale(add(one, nw), t), constant(-1)),
                  add(scale(a, t), scale(w2, -1))), -1),
    )


def assert_same(p, r, name):
    difference = add(p, scale(r, -1))
    assert not difference, (name, difference)
    return name


def exact_checks():
    checked = []
    t = R(19, 18)
    fn = F(t)
    f1 = evaluate_variable(fn, 0, 1)
    f2 = evaluate_variable(fn, 0, 2)
    delta = add(f2, scale(f1, -1))
    Q = scale(mul(w, add(a, constant(-t))), t)
    m = add(n, constant(-1))
    reconstructed = add(f1, mul(m, delta),
                        scale(mul(m, add(n, constant(-2)), Q), -1))
    checked.append(assert_same(fn, reconstructed, 'integer finite difference'))
    cert1 = add(scale(w3, 148),
                scale(square(add(scale(w, 24), constant(-7))), 3),
                scale(w2, 12), scale(w, 8), one)
    cert2 = add(scale(w3, 721),
                square(add(scale(w, 42), constant(-4))),
                scale(w2, 38), scale(w, 10), constant(2))
    checked.append(assert_same(scale(f1, -1296), cert1, '19/18 first square'))
    checked.append(assert_same(scale(delta, -324), cert2, '19/18 delta square'))

    # The elementary k=2 comparison's residual polynomial.
    k2diff = add(one, mul(n, beta, a), scale(square(add(one, nw)), -1),
                 scale(mul(n, beta), -1))
    k2expanded = add(mul(n, beta, add(scale(w, 2), w2)),
                     scale(mul(n, w), -2), scale(mul(n, n, w2), -1))
    checked.append(assert_same(k2diff, k2expanded, 'k=2 residual identity'))

    t = R(17, 16)
    f = F(t)
    checked.append(assert_same(
        scale(evaluate_variable(f, 0, 1), 256),
        add(constant(-33), scale(w, 190), scale(w2, -355), scale(w3, -33)),
        '17/16 endpoint'))
    checked.append(assert_same(
        scale(evaluate_variable(derivative(f, 0), 0, 1), 256),
        add(constant(-16), scale(w, 241), scale(w2, -898), scale(w3, -305)),
        '17/16 derivative'))
    assert 190**2 - 4 * 33 * 355 == -10760
    assert 241**2 - 4 * 16 * R(14673, 16) == -611

    t = R(16, 15)
    m = add(n, constant(-1))
    first = add(constant(31), scale(w, -163), scale(w2, 318), scale(w3, 31))
    second = add(constant(15), scale(w, -211), scale(w2, 797), scale(w3, 271))
    last = scale(mul(square(m), w,
                     add(scale(w2, 15), scale(w, 30), constant(-1))), -16)
    cert = add(scale(first, -1), scale(mul(m, second), -1), last)
    checked.append(assert_same(scale(F(t), 225), cert, '16/15 m expansion'))
    checked.append(assert_same(
        add(constant(31), scale(w, -163), scale(w2, 318)),
        scale(add(square(add(scale(w, 636), constant(-163))), constant(12863)),
              R(1, 1272)), '16/15 endpoint square'))
    checked.append(assert_same(
        add(constant(15), scale(w, -211), scale(w2, 797)),
        scale(add(square(add(scale(w, 1594), constant(-211))), constant(3299)),
              R(1, 3188)), '16/15 derivative square'))

    assert 19 * 50 < 53 * 18
    assert 53 * 16 < 17 * 50
    assert 17 * 15 < 16 * 16
    assert 286 * 18 - 267 * 19 == 75
    assert R(286, 267) - R(19, 18) == R(25, 1602)
    return {'identities': checked, 'all_exact_assertions_passed': True,
            'main_certificate_t': '19/18',
            'integer_n_condition': '(n-1)(n-2) >= 0 for integer n >= 1'}


def rational_grid():
    # Every cost is represented over common denominator M^3, so the strict
    # cost comparisons, including zero denominators, use only integers.
    M = 100
    ns = list(range(1, 101)) + [1000, 10000, 1000000]
    total, zero_d2 = 0, 0
    for ni in ns:
        for j in range(M + 1):
            q2 = (M + j) ** 2
            for b in range(M + 1):
                N1 = M**3 + ni * b * q2
                for k in (1, 2):
                    if k == 1:
                        D1 = M**3 + ni * j * M**2 + ni * b * M**2
                        N2 = (M + j) * M**2 + b * j*j
                        D2 = ni * j * M**2 + b * q2
                    else:
                        D1 = (M + ni*j)**2 * M + ni*b*M**2
                        N2 = q2 * M + b*j*j
                        D2 = (ni*j)**2 * M + b*q2
                    total += 1
                    zero_d2 += D2 == 0
                    assert not (18*N1 > 19*D1 and 18*N2 > 19*D2), (ni,j,b,k)
    return {'arithmetic': 'integer cross multiplication',
            'n_values': {'range': [1, 100], 'extra': [1000, 10000, 1000000]},
            'w_beta_grid': 'j/100, j=0,...,100', 'k_values': [1, 2],
            'parameter_combinations': total, 'zero_second_denominators': zero_d2,
            'strict_inequality_counterexamples': 0}


def beta_optimum(ni, wi):
    # Supporting floating-point exploration, only for k=1.
    if wi == 0:
        return 1.0, 1.0
    q = 1.0 + wi
    u = ni * wi
    if u >= q:
        return 1.0, 0.0  # B <= 1 on this region; not an exact optimum claim.

    def ratios(b):
        return ((1 + ni*b*q*q)/(1 + u + ni*b),
                (q + b*wi*wi)/(u + b*q*q))

    aa, bb = ratios(1.0)
    if aa <= bb:
        return aa, 1.0
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi)/2
        aa, bb = ratios(mid)
        if aa < bb:
            lo = mid
        else:
            hi = mid
    b = (lo + hi)/2
    return min(ratios(b)), b


def numerical_exploration():
    def refine(ni, lo, hi):
        g = (math.sqrt(5) - 1)/2
        x, y = hi-g*(hi-lo), lo+g*(hi-lo)
        fx, fy = beta_optimum(ni, x)[0], beta_optimum(ni, y)[0]
        for _ in range(90):
            if fx < fy:
                lo, x, fx = x, y, fy
                y = lo+g*(hi-lo)
                fy = beta_optimum(ni, y)[0]
            else:
                hi, y, fy = y, x, fx
                x = hi-g*(hi-lo)
                fx = beta_optimum(ni, x)[0]
        wi = (lo+hi)/2
        value, b = beta_optimum(ni, wi)
        return {'n': ni, 'w': wi, 'beta': b, 'minimum': value}

    count = 500
    results = []
    ns = list(range(1, 101)) + [1000, 10000, 1000000]
    for ni in ns:
        upper = 1.0 if ni <= 2 else 1.0/(ni-1)
        candidates = [(beta_optimum(ni, upper*j/count)[0], j)
                      for j in range(count+1)]
        best = None
        for _, j in sorted(candidates, reverse=True)[:3]:
            row = refine(ni, upper*max(0,j-1)/count,
                         upper*min(count,j+1)/count)
            if best is None or row['minimum'] > best['minimum']:
                best = row
        results.append(best)
    results.sort(key=lambda row: row['minimum'], reverse=True)
    assert results[0]['minimum'] < 19/18
    return {'arithmetic': 'Python binary64; supporting evidence only',
            'n_count': len(ns), 'w_initial_grid_intervals_per_n': count,
            'beta_bisection_iterations': 60,
            'w_refinement': '90 golden-section iterations in each top-three grid bracket',
            'coverage_limit': 'finite n list and finite numerical search; no global optimizer certificate',
            'top_ten_observations': results[:10],
            'large_n_observations': [r for r in results if r['n'] >= 1000]}


def main():
    report = {'claim_id': 'WC-R1-SOURCE-D2-ENVELOPE v1',
              'date_utc': '2026-10-14',
              'exact': exact_checks(),
              'rational_grid': rational_grid(),
              'numerical': numerical_exploration()}
    path = Path(__file__).resolve().with_name('verification.json')
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'exact_identities_checked': len(report['exact']['identities']),
                      'rational_grid_combinations': report['rational_grid']['parameter_combinations'],
                      'strict_counterexamples': 0,
                      'best_finite_numerical_observation': report['numerical']['top_ten_observations'][0],
                      'output': str(path)}, indent=2))


if __name__ == '__main__':
    main()
