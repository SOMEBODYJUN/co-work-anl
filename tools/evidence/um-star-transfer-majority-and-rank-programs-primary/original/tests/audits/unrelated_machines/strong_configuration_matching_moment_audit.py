#!/usr/bin/env python3
"""Exact finite checks for the proved odd-slice matching-law obstruction.

No scheduling hardness or general rounding guarantee is inferred from these checks.
The universal proof is the harmonic decomposition in the accompanying manuscript.
"""
from fractions import Fraction as F
from itertools import combinations
from math import comb
import hashlib
import json
import platform
from pathlib import Path


def falling(x, k):
    value = F(1)
    for j in range(k):
        value *= x - j
    return value


def mu(n, k):
    return falling(F(n, 2), k) / falling(n, k)


def cylinder(n, a, b):
    return falling(F(n, 2), a) * falling(F(n, 2), b) / falling(n, a + b)


def basis(n, r):
    return [sum(1 << i for i in a) for k in range(r + 1)
            for a in combinations(range(n), k)]


def psd_rank(matrix):
    """Independent exact Schur elimination, including the zero-pivot case."""
    a = [row[:] for row in matrix]
    rank = 0
    for k in range(len(a)):
        pivot = a[k][k]
        assert pivot >= 0, ('negative pivot', k, pivot)
        if not pivot:
            assert all(a[k][j] == 0 for j in range(k, len(a)))
            continue
        rank += 1
        for i in range(k + 1, len(a)):
            if not a[i][k]:
                continue
            factor = a[i][k] / pivot
            for j in range(i, len(a)):
                a[i][j] -= factor * a[k][j]
                a[j][i] = a[i][j]
    return rank


def audit():
    records = []
    # Small exact matrices check the general proof; no expanding search campaign.
    for n, r in [(5, 2), (7, 2), (11, 3)]:
        monomials = basis(n, r)
        matrix = [[mu(n, (a | b).bit_count()) for b in monomials]
                  for a in monomials]
        rank = psd_rank(matrix)
        assert rank == comb(n, r)
        t = F(n, 2)
        mean = n * mu(n, 1)
        second = n * mu(n, 1) + n * (n - 1) * mu(n, 2)
        assert mean == t and second == t*t
        m = n//2
        repaired_pair = (falling(m,2)+falling(m+1,2))/(2*falling(n,2))
        radius = F(1,4*n*(n-1))
        assert repaired_pair-mu(n,2) == radius
        assert radius*4*n*(n-1) == 1
        assert second - n*mean + F(n*n, 4) == 0
        # On every actual bit string, (2S-n)^2 >= 1 because n is odd.
        assert all((2*s-n)**2 >= 1 for s in range(n+1))
        for a in range(2*r):
            assert a*mu(n, a)+(n-a)*mu(n, a+1) == t*mu(n, a)
        gram = []
        for k in range(r+1):
            overlap = sum((-1)**(k-s)*comb(k,s)*mu(n, 2*k-s)
                          for s in range(k+1))
            expected = falling(t,k)*falling(n-t,k)/falling(n,2*k)
            assert overlap == expected > 0
            gram.append(str(expected))
        cylinders_positive = n >= 4*r-1
        for a in range(2*r+1):
            for b in range(2*r+1-a):
                expanded = sum((-1)**j*comb(b,j)*mu(n,a+j)
                               for j in range(b+1))
                assert expanded == cylinder(n,a,b)
                if cylinders_positive:
                    assert expanded > 0
        records.append(dict(N=n, degree=2*r, matrix_dimension=len(matrix),
                            rank=rank, gram_coefficients=gram,
                            all_short_cylinders_positive=cylinders_positive,
                            second_moment=str(second), variance='0', sharp_pair_repair_radius=str(radius)))
    return dict(python=platform.python_version(), arithmetic='fractions.Fraction',
                seed=None, scope='three exact PSD fixtures and algebraic identities; not a proof by search',
                records=records,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())


if __name__ == '__main__':
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
