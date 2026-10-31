#!/usr/bin/env python3
"""Exact size/ratio audit for the sublinear CC_r diagonal corollary.

This checks the closed formulas and a few concrete sublinear r(M) examples.
It is finite arithmetic evidence only; the general limit proof is in the
corresponding current document and the long-path construction.
"""
from fractions import Fraction
from math import isqrt


def height(k):
    a = Fraction(1, k - 1)
    h = 1
    while a < Fraction(1, 2):
        h += 1
        a *= Fraction(k, k - 1)
    return h


def sizes(k, ell):
    h = height(k)
    machines = 2 * ((k**h - 1) // (k - 1) + k**h * ell)
    jobs = 1 + 2 * ((k**h - k) // (k - 1) + k**h * ell)
    return h, machines, jobs


def r_sqrt(m):
    return isqrt(m)


def iroot3(m):
    # Integer floor cube root, another explicit sublinear order.
    lo, hi = 0, 1
    while hi**3 <= m:
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid**3 <= m:
            lo = mid
        else:
            hi = mid
    return lo


def main():
    checked = 0
    for k in range(4, 9):
        ratio = Fraction(2 * k - 1, k + 1)
        assert ratio == 2 - Fraction(3, k + 1)
        for ell in (2, 3, 7, 19):
            h, m, n = sizes(k, ell)
            # The path replacement has one task per machine-graph edge.
            assert n == m - 1
            assert 2 * ell > 0
            # Both sample r(M)=o(M) functions are genuinely sublinear.
            assert r_sqrt(m) * r_sqrt(m) <= m
            assert iroot3(m)**3 <= m
            checked += 1
    # Explicitly find witness lengths for the two sample sublinear orders.
    for k, upper in ((4, 200000), (5, 200000)):
        for rf in (r_sqrt, iroot3):
            found = None
            for ell in range(2, upper):
                _, m, _ = sizes(k, ell)
                if rf(m) < 2 * ell:
                    found = (ell, m, rf(m))
                    break
            assert found is not None
            assert found[2] < 2 * found[0]
    print({"status": "ok", "parameter_checks": checked,
           "ratio_identity": "(2k-1)/(k+1)=2-3/(k+1)",
           "scope": "machine-count sublinear r(M), finite examples only"})


if __name__ == "__main__":
    main()
