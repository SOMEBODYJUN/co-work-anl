"""Exact replay of the general optimal-portfolio replacement identities.

This audits one explicitly stated all-input lemma; finite catalogues below
are boundary fixtures, not a proof of the sequential half-coverage target.
No SPE solver, payoff library, floating point or author code is imported.
Output is summary-only unless --output names a new, nonexisting file.
"""
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, product
from math import comb, factorial
from pathlib import Path
import argparse
import json


def beta(a, b):
    assert a >= 1 and b >= 1
    return F(factorial(a-1)*factorial(b-1), factorial(a+b-1))


def union(profile):
    result = 0
    for mask in profile:
        result |= mask
    return result


def check_case(n, optimum, profile, check_realizations):
    m = len(optimum)
    O = union(optimum)
    a = [sum((T >> x) & 1 for T in optimum) for x in range(n)]
    c = [sum((B >> x) & 1 for B in profile) for x in range(n)]
    paired = [any(((T & B) >> x) & 1 for T, B in zip(optimum, profile))
              for x in range(n)]
    J = [x for x in range(n) if a[x] and not paired[x]]
    outside = [x for x in range(n) if not a[x]]
    for p in [F(0), F(1, 3), F(1, 2), F(2, 3), F(1)]:
        gain = sum((1-(1-p)**c[x] for x in outside), F())
        loss = sum((p**a[x]*(1-p)**c[x] for x in J), F())
        assert gain <= loss
        if check_realizations and p == F(1, 2):
            expected = F()
            for bits in product([0, 1], repeat=m):
                chosen = [profile[i] if bits[i] else optimum[i]
                          for i in range(m)]
                expected += F(union(chosen).bit_count(), 2**m)
            assert expected == O.bit_count()+gain-loss
    harmonic = [sum((F(1, j) for j in range(1, k+1)), F())
                for k in range(m+1)]
    left = sum((harmonic[c[x]] for x in outside), F())
    right = sum((beta(a[x], c[x]+1) for x in J), F())
    assert left <= right
    averaged_right = F()
    for x in range(n):
        if a[x] and a[x]+c[x] <= m:
            averaged_right += (F(comb(m-a[x], c[x]), comb(m, c[x]))
                               * beta(a[x], c[x]+1))
    assert left <= averaged_right
    anchored = 0
    for j in range(m):
        if optimum[j] != profile[j]:
            continue
        fixed = optimum[j]
        anchored_right = F()
        for x in range(n):
            if not a[x] or ((fixed >> x) & 1):
                continue
            if a[x]+c[x] <= m-1:
                anchored_right += (F(comb(m-1-a[x], c[x]), comb(m-1, c[x]))
                                   * beta(a[x], c[x]+1))
        assert left <= anchored_right
        anchored += 1
    for alpha in [1, 2, 3]:
        left_alpha = sum((F(1, alpha)-beta(alpha, c[x]+1)
                          for x in outside), F())
        right_alpha = sum((beta(a[x]+alpha, c[x]+1) for x in J), F())
        assert left_alpha <= right_alpha
    return int(left > 0), int(any(c[x] for x in J)), anchored


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    counts = dict(catalogues=0, optimal_portfolios=0, paired_profiles=0,
                  nonzero_outside_harmonic=0, covered_loss_terms=0,
                  anchored_profile_checks=0)
    for n in range(5):
        masks = range(1 << n)
        for size in range(1, min(3, len(masks))+1):
            for catalogue in combinations(masks, size):
                counts['catalogues'] += 1
                for m in [1, 2, 3]:
                    multisets = list(combinations_with_replacement(catalogue, m))
                    opt = max(union(q).bit_count() for q in multisets)
                    for T in multisets:
                        if union(T).bit_count() != opt:
                            continue
                        counts['optimal_portfolios'] += 1
                        for B in product(catalogue, repeat=m):
                            nz, covered, anchored = check_case(n, T, B, m <= 2)
                            counts['paired_profiles'] += 1
                            counts['nonzero_outside_harmonic'] += nz
                            counts['covered_loss_terms'] += covered
                            counts['anchored_profile_checks'] += anchored
    result = dict(status='pass', scope='explicit finite boundary replay only',
                  **counts,
                  kernels='Bernoulli p=0,1/3,1/2,2/3,1; harmonic; alpha=1,2,3; random matching',
                  limitations='No SPE property or general half coverage is inferred.')
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
            f.write('\n')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
