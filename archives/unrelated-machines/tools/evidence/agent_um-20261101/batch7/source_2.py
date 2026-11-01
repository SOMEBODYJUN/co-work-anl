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


def audit_fixed_epsilon():
    # For any target epsilon, choose k > 1/(8*epsilon).  Then the
    # existing family starts above 2-epsilon while retaining the k+1 exit barrier.
    for eps in (F(1, 100), F(1, 50), F(1, 20), F(1, 19)):
        k = max(2, (1 // (8 * eps)) + 1)
        a = F(8 * k - 1, 8 * k)
        # Bad state and optimal witness loads.
        assert max(loads(k, 0, 0, 0, 0)) == 1 + a > 2 - eps
        assert loads(k, 1, 1, 2 * k, 2 * k) == (F(1), F(1), F(1))
        # A first small move, or a big move with fewer than k escorts,
        # crosses the strict 2 barrier.
        assert k > 1 / (8 * eps)
        assert 1 + a + a / k > 2
        assert max(loads(k, 1, 0, k, 0)) < 2
        assert max(loads(k, 1, 0, k - 1, 0)) > 2
    print("PASS fixed-epsilon support corollary for eps=1/100,1/50,1/20,1/19")


if __name__ == "__main__":
    audit_parameters()
    audit_fixed_epsilon()
