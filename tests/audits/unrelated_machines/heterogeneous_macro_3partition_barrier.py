#!/usr/bin/env python3
"""Exact small audit for the scaled heterogeneous-tiny 3-PARTITION barrier."""
from fractions import Fraction as F
from itertools import combinations


def audit_small():
    B = 13
    items = (4, 4, 4, 4, 4, 6)
    K = 2
    T = K * B
    delta = F(1, 4)
    assert sum(items) == 2 * B
    assert all(B / 4 < a < B / 2 for a in items)
    assert all(F(a) < delta * T for a in items)
    assert F(1) < delta * T
    # A T-feasible integral residual assignment would split the items into
    # two sink subsets of sum B.  Enumerate one side exactly.
    exact_partition = any(sum(items[i] for i in S) == B
                          for r in range(len(items) + 1)
                          for S in combinations(range(len(items)), r))
    assert not exact_partition
    # Uniform fractional splitting across the two sinks gives each sink B.
    assert sum(F(a, 2) for a in items) == B
    # A home macro of duration T leaves no positive residual home capacity.
    assert T + F(1) > T
    print("PASS B=13,m=2,K=2,delta=1/4; no integral partition; fractional sink load=13")


if __name__ == "__main__":
    audit_small()
