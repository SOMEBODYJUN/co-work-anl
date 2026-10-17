#!/usr/bin/env python3
"""Exact finite audit for the k-uniform bundle-matching formula.

All arithmetic is Fraction.  The instance has root r, q X-nodes of demand
1, hyperedge nodes of demand K, and zero-demand resources.  A selected
hyperedge may send any nonempty subset of its resource set.  The formula
max_t min(nu_t/q,t/K) is checked against exhaustive positive-score trees.
"""
from fractions import Fraction
from itertools import combinations, product
import random


def bundle_choices(S, t):
    return [frozenset(c) for c in combinations(sorted(S), t)]


def nu_t(q, edges, t):
    by_x = {x: [] for x in range(q)}
    for e in edges:
        by_x[e[0]].append(e[1])
    best = 0
    def rec(x, used, got):
        nonlocal best
        if x == q:
            best = max(best, got)
            return
        rec(x + 1, used, got)
        for S in by_x[x]:
            for B in bundle_choices(S, t):
                if B.isdisjoint(used):
                    rec(x + 1, used | B, got + 1)
    rec(0, frozenset(), 0)
    return best


def formula(q, K, edges, k):
    if q == 0:
        return Fraction(0)
    return max((min(Fraction(nu_t(q, edges, t), q), Fraction(t, K))
                for t in range(1, min(k, K) + 1)), default=Fraction(0))


def brute_b(q, K, edges):
    by_x = {x: [] for x in range(q)}
    for x, S in edges:
        by_x[x].append(S)
    best = Fraction(0)
    for mask in range(1 << q):
        xs = [x for x in range(q) if (mask >> x) & 1]
        if not xs or any(not by_x[x] for x in xs):
            continue
        for parents in product(*(by_x[x] for x in xs)):
            child_lists = [sum((bundle_choices(S, t) for t in range(1, len(S) + 1)), [])
                           for S in parents]
            for bundles in product(*child_lists):
                used = frozenset().union(*bundles)
                if sum(map(len, bundles)) != len(used):
                    continue
                score = min([Fraction(len(xs), q)] +
                            [Fraction(len(B), K) for B in bundles])
                best = max(best, score)
    return best


def audit():
    # Exhaustive set systems for q=1, two resources, and K=1..4.
    q, resources = 1, [0, 1]
    universe = [(0, frozenset(S)) for t in (1, 2)
                for S in combinations(resources, t)]
    for mask in range(1 << len(universe)):
        edges = [e for i, e in enumerate(universe) if mask >> i & 1]
        for K in range(1, 5):
            got = brute_b(q, K, edges)
            want = formula(q, K, edges, 2)
            assert got == want, (q, K, edges, got, want)

    # Random q=2 systems with 4 resources, bundle sizes 1..3.
    rng = random.Random(20261017)
    q, resources, k = 2, list(range(4)), 3
    universe = [(x, frozenset(S)) for x in range(q)
                for t in range(1, k + 1)
                for S in combinations(resources, t)]
    for _ in range(1200):
        edges = [e for e in universe if rng.randrange(4) == 0]
        for K in (1, 2, 3, 4, 7):
            got = brute_b(q, K, edges)
            want = formula(q, K, edges, k)
            assert got == want, (q, K, edges, got, want)

    # The local floor: if nu_1=q then b* >= 1/K.
    for K in range(1, 10):
        edges = [(0, frozenset({0})), (1, frozenset({1}))]
        assert formula(2, K, edges, 1) == min(Fraction(1), Fraction(1, K))
    print("PASS exhaustive_q1=16*4, random_q2=1200*5, one_bundle_floor")


if __name__ == "__main__":
    audit()
