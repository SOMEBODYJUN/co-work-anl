#!/usr/bin/env python3
"""Exact audit for the D_K(A) demand-tree formula.

The oracle enumerates every positive-score root tree for q<=3, while the
closed-form side computes the X--(Y union Z) matching mu and 3DM matching nu.
All arithmetic is Fraction; this is a finite audit, not a general hardness
proof.
"""
from fractions import Fraction
from itertools import combinations, product
import random


def max_bipartite_mu(q, edges):
    resources = [("y", i) for i in range(q)] + [("z", i) for i in range(q)]
    adj = {x: set() for x in range(q)}
    for x, y, z in edges:
        adj[x].update({("y", y), ("z", z)})
    best = 0
    def rec(x, used, got):
        nonlocal best
        if x == q:
            best = max(best, got)
            return
        rec(x + 1, used, got)
        for r in sorted(adj[x]):
            if r not in used:
                rec(x + 1, used | {r}, got + 1)
    rec(0, set(), 0)
    return best


def max_3dm_nu(q, edges):
    by_x = {x: [] for x in range(q)}
    for e in edges:
        by_x[e[0]].append(e)
    best = 0
    def rec(x, ys, zs, got):
        nonlocal best
        if x == q:
            best = max(best, got)
            return
        rec(x + 1, ys, zs, got)
        for _, y, z in by_x[x]:
            if y not in ys and z not in zs:
                rec(x + 1, ys | {y}, zs | {z}, got + 1)
    rec(0, set(), set(), 0)
    return best


def closed_form(q, K, edges):
    if q == 0:
        return Fraction(0)
    mu = max_bipartite_mu(q, edges)
    nu = max_3dm_nu(q, edges)
    return max(min(Fraction(mu, q), Fraction(1, K)),
               min(Fraction(nu, q), Fraction(2, K)))


def brute_b(q, K, edges):
    by_x = {x: [] for x in range(q)}
    for e in edges:
        by_x[e[0]].append(e)
    best = Fraction(0)
    # A positive-score tree chooses a nonempty set of X vertices, one parent
    # triple for each, and one or both children of each chosen triple.
    for mask in range(1 << q):
        xs = [x for x in range(q) if (mask >> x) & 1]
        if not xs:
            continue
        if any(not by_x[x] for x in xs):
            continue
        for parents in product(*(by_x[x] for x in xs)):
            # Distinct x coordinates already make parent triple vertices distinct.
            for child_choices in product((1, 2), repeat=len(xs)):
                options = []
                for e, t in zip(parents, child_choices):
                    _, y, z = e
                    options.append([(y,), (z,)] if t == 1 else [(y, z)])
                for chosen in product(*options):
                    resources = [(side, r) for pair in chosen
                                 for side, r in zip(("y", "z"), pair)]
                    if len(resources) != len(set(resources)):
                        continue
                    score = min([Fraction(1), Fraction(len(xs), q)] +
                                [Fraction(len(pair), K) for pair in chosen])
                    best = max(best, score)
    return best


def audit():
    # Exhaustive q<=2; random exact samples q=3, including empty and full cases.
    for q in (1, 2):
        universe = [(x, y, z) for x in range(q) for y in range(q) for z in range(q)]
        for mask in range(1 << len(universe)):
            edges = [e for i, e in enumerate(universe) if (mask >> i) & 1]
            for K in range(2, 7):
                got = brute_b(q, K, edges)
                want = closed_form(q, K, edges)
                assert got == want, (q, K, edges, got, want)
    rng = random.Random(20261017)
    q = 3
    universe = [(x, y, z) for x in range(q) for y in range(q) for z in range(q)]
    samples = [[], universe]
    samples += [[e for e in universe if rng.randrange(3) == 0] for _ in range(600)]
    for edges in samples:
        for K in (2, 3, 4, 7):
            got = brute_b(q, K, edges)
            want = closed_form(q, K, edges)
            assert got == want, (q, K, edges, got, want)
    # Shared-pool Hall target: exact integer maximization for Q_{q,K}.
    def pool_value(q, K):
        return max((min(Fraction(r, q), Fraction(K // r, K))
                    for r in range(1, min(q, K) + 1)), default=Fraction(0))
    assert pool_value(20, 20) == Fraction(1, 5)
    assert pool_value(40, 40) == Fraction(3, 20)
    assert pool_value(80, 80) == Fraction(1, 10)
    # Perfect matching instances show the scaling floor exactly: b*=2/K.
    for q in range(1, 5):
        edges = [(i, i, i) for i in range(q)]
        for K in range(2, 9):
            assert closed_form(q, K, edges) == Fraction(2, K)
    print("PASS exhaustive_q<=2=256*5 and random_q3=602*4; perfect_floor_checked")


if __name__ == "__main__":
    audit()
