"""Independent exact arithmetic audit of prefix-absence repeated-last bounds."""

import argparse
import json
from fractions import Fraction as F
from pathlib import Path


def harmonic(m):
    out = [F()]
    for i in range(1, m + 1):
        out.append(out[-1] + F(1, i))
    return out


def coefficients(m, k, H):
    d = m - k
    a = F(d + 2, d + 1)
    return [F(t) + a * (t * (H[m] - H[t]) - F((t-k)*(m-t), m))
            for t in range(k, m + 1)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    patterns = triples = old_implications = polynomial_implications = 0
    improvements = []
    for m in range(1, 101):
        H = harmonic(m)
        for k in range(1, m + 1):
            d = m - k
            a = F(d+2, d+1)
            cs = coefficients(m, k, H)
            gamma = min(cs)
            old = m*(2*d+1) >= d*d*(d+2)
            N = 2*m*d*(d+2)+(d+2)*k-2*m*m
            polynomial = max(N, 0)**2 <= 8*m*m*(d+1)*(d+2)*k
            if old:
                assert gamma >= m-1, (m, k, gamma)
                old_implications += 1
            if polynomial:
                assert gamma >= m-1, (m, k, gamma)
                polynomial_implications += 1
            if gamma >= m-1 and not old and m <= 20:
                improvements.append({'m': m, 'k': k, 'd': d, 'gamma': str(gamma)})
            for r in range(d+1):
                t = k+r
                A = F(r, m) + H[m]-H[t] - F(r, t)
                assert A == H[m]-H[t]-F((t-k)*(m-t), m*t)
                assert A >= F(k*(m-t), m*t) >= 0
                assert cs[r] == t*(1+a*A)
                q = m-t
                L = a*d/m+a*k/(2*m*m)-F(1, d+1)
                Q = a*k/(2*m*m)
                assert cs[r] >= m-L*q+Q*q*q
                assert L == F(N, 2*m*m*(d+1))
                triples += 1
            if m <= 12:
                for mask in range(1 << d):
                    r = mask.bit_count()
                    missing = 0
                    actual = F()
                    for j in range(d):
                        actual += F(1, m-missing)
                        missing += not (mask >> j & 1)
                    lower = F(r, m)+H[m]-H[k+r]
                    assert actual >= lower, (m, k, mask, actual, lower)
                    # Covering players first attains exactly the claimed minimum.
                    first = (1 << r)-1
                    missing2 = 0
                    attained = F()
                    for j in range(d):
                        attained += F(1, m-missing2)
                        missing2 += not (first >> j & 1)
                    assert attained == lower
                    patterns += 1
    report = {
        'status': 'formula_audit_passed',
        'scope': 'analytic proof is in prefix_absence_repeated_last.md; finite audit only',
        'pattern_cases_m_le_12': patterns,
        'coefficient_cases_m_le_100': triples,
        'old_criterion_implications': old_implications,
        'polynomial_criterion_implications': polynomial_implications,
        'strict_improvements_m_le_20': improvements,
    }
    if args.output:
        with args.output.open('x') as f:
            json.dump(report, f, indent=2)
            f.write('\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
