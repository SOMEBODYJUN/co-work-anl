#!/usr/bin/env python3
"""Exact brute-force audit for the machine-multiplier common-size interface.

This is deliberately independent of the canonical flow implementation: tiny
support graphs are generated, the optimum is enumerated, and the finite
candidate/flow predicate is checked against it using exact Fractions.
"""
from fractions import Fraction as F
from itertools import product
from random import Random


def brute(f, p, elig):
    m = len(f)
    n = len(elig)
    best = None
    best_ass = None
    def rec(j, loads, ass):
        nonlocal best, best_ass
        if j == n:
            v = max(loads, default=F(0))
            if best is None or v < best:
                best, best_ass = v, tuple(ass)
            return
        for i in elig[j]:
            loads[i] += p[i][j]
            ass.append(i)
            rec(j + 1, loads, ass)
            ass.pop()
            loads[i] -= p[i][j]
    rec(0, list(f), [])
    return best, best_ass


def multiplier_feasible(f, q, a, elig, B):
    m = len(f); n = len(elig)
    if B < max(f, default=F(0)):
        return False
    caps = [max(0, int((B-f[i]) // (a[i]*q))) for i in range(m)]
    match = [[] for _ in range(m)]
    def aug(j, seen):
        for i in elig[j]:
            if i in seen or caps[i] == 0:
                continue
            seen.add(i)
            if len(match[i]) < caps[i]:
                match[i].append(j); return True
            for old in list(match[i]):
                if aug(old, seen):
                    match[i].remove(old); match[i].append(j); return True
        return False
    return all(aug(j, set()) for j in range(n))


def candidate_opt(f, q, a, elig):
    m = len(f); n = len(elig)
    vals = {f[i] + a[i]*q*t for i in range(m) for t in range(n+1)}
    for B in sorted(vals):
        if multiplier_feasible(f, q, a, elig, B):
            return B
    raise AssertionError("upper candidate must be feasible")


def main():
    rng = Random(2101)
    checked = 0
    for _ in range(400):
        m = rng.randrange(1, 5)
        n = rng.randrange(0, 7)
        f = [F(rng.randrange(0, 5), rng.randrange(1, 4)) for _ in range(m)]
        q = F(rng.randrange(1, 4), rng.randrange(1, 4))
        a = [F(rng.randrange(1, 5), rng.randrange(1, 4)) for _ in range(m)]
        elig = []
        for _j in range(n):
            E = [i for i in range(m) if rng.randrange(2)]
            if not E:
                E = [rng.randrange(m)]
            elig.append(E)
        p = [[a[i]*q if i in elig[j] else None for j in range(n)] for i in range(m)]
        opt, ass = brute(f, p, elig)
        got = candidate_opt(f, q, a, elig)
        assert got == opt, (f,q,a,elig,opt,got,ass)
        for B in sorted({f[i]+a[i]*q*t for i in range(m) for t in range(n+1)}):
            assert multiplier_feasible(f,q,a,elig,B) == (opt <= B)
        checked += 1
    # Explicit frozen-core guard regression.
    f=[F(2),F(0)]; q=F(1); a=[F(1),F(1)]; elig=[[1]]
    p=[[None],[F(1)]]
    opt,_=brute(f,p,elig); assert opt==2
    assert not multiplier_feasible(f,q,a,elig,F(1))
    # Two disconnected support components with different q and multipliers.
    # Component 0 has one task of size 3/2.  Component 1 has two tasks and
    # machine times 2 and 1.  The independent component optima are 3/2 and 2.
    assert candidate_opt([F(0)], F(3, 2), [F(1)], [[0]]) == F(3, 2)
    assert candidate_opt([F(0), F(0)], F(1), [F(2), F(1)], [[0, 1], [0, 1]]) == F(2)
    print({"random_instances":checked,"frozen_guard":"ok","disconnected_components":"ok"})


if __name__ == "__main__":
    main()
