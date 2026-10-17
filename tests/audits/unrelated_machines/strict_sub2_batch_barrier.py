#!/usr/bin/env python3
"""Exact Fraction audit for the strict-sub-2 batch barrier."""
from fractions import Fraction as F


def loads(k, x, y, u, v):
    a = F(8 * k - 1, 8 * k)
    return (1 + a - a * (x + y) + a * (u + v) / (4 * k),
            1 + a + a * x - a * u / k,
            1 + a + a * y - a * v / k)


def audit_parameters():
    for k in (2, 3, 7, 100):
        a = F(8 * k - 1, 8 * k)
        assert max(loads(k, 0, 0, 0, 0)) == 1 + a < 2
        assert loads(k, 1, 1, 2 * k, 2 * k) == (F(1), F(1), F(1))
        # Every one-sided leaf release of fewer than k jobs crosses 2.
        for u in range(k):
            assert loads(k, 1, 0, u, 0)[1] >= 2
        for v in range(k):
            assert loads(k, 0, 1, 0, v)[2] >= 2
        # The first legal strict-sub-2 exit uses exactly k+1 jobs.
        assert max(loads(k, 1, 0, k, 0)) < 2
        assert max(loads(k, 1, 0, k - 1, 0)) >= 2
        assert F(a, 4 * k) > 1 - a
    print("PASS k=2,3,7,100; OPT=1 witness; strict-sub-2 batch threshold k+1")


if __name__ == "__main__":
    audit_parameters()
