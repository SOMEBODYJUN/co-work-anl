#!/usr/bin/env python3
"""Finite Fraction audit for UM-INDEPENDENT-SET-BIG-RESIDUAL-INTERFACE-v1.

Checks the exact threshold reduction on every graph with n<=4 and
maximum degree <=3, for (q,r)=(3,0),(3,1),(4,2).
This is evidence only; the two-way proof is in the companion Markdown.
"""
from __future__ import annotations
from fractions import Fraction
from itertools import combinations, product


def independent_number(n: int, edges: list[tuple[int, int]]) -> int:
    edge_set = {tuple(sorted(e)) for e in edges}
    best = 0
    for mask in range(1 << n):
        S = [v for v in range(n) if (mask >> v) & 1]
        if all(not ((mask >> u) & 1 and (mask >> v) & 1) for u, v in edge_set):
            best = max(best, len(S))
    return best


def jobs_for(n: int, edges: list[tuple[int, int]], k: int, q: int, r: int):
    h = Fraction(1, q)
    jobs: list[list[tuple[int, Fraction]]] = []
    # Big jobs: all graph machines, time 1.
    for _ in range(k):
        jobs.append([(v, Fraction(1)) for v in range(n)])
    # Private jobs.
    for v in range(n):
        for _ in range(r):
            jobs.append([(v, h)])
    # Edge jobs.
    for u, v in edges:
        jobs.append([(u, h), (v, h)])
    return jobs


def exact_opt(n: int, jobs: list[list[tuple[int, Fraction]]]) -> Fraction:
    best = None
    # n<=4 exhaustive instances are deliberately tiny.
    for assignment in product(*jobs):
        loads = [Fraction(0) for _ in range(n)]
        for machine, time in assignment:
            loads[machine] += time
        value = max(loads, default=Fraction(0))
        if best is None or value < best:
            best = value
    assert best is not None
    return best


def all_graphs(n: int):
    all_edges = list(combinations(range(n), 2))
    for mask in range(1 << len(all_edges)):
        edges = [all_edges[i] for i in range(len(all_edges)) if (mask >> i) & 1]
        degree = [0] * n
        for u, v in edges:
            degree[u] += 1
            degree[v] += 1
        if max(degree, default=0) <= 3:
            yield edges


def check_instance(n: int, edges: list[tuple[int, int]], k: int, q: int, r: int):
    alpha_cap = Fraction(1) + Fraction(r, q)
    opt = exact_opt(n, jobs_for(n, edges, k, q, r))
    alpha = independent_number(n, edges)
    assert (opt <= alpha_cap) == (alpha >= k), (n, edges, k, r, opt, alpha_cap, alpha)
    if k >= 1 and alpha >= k:
        assert opt == alpha_cap, ("YES value", n, edges, k, r, opt, alpha_cap)
    if k >= 1 and alpha < k:
        assert opt >= alpha_cap + Fraction(1, q), ("NO gap", n, edges, k, r, opt, alpha_cap)


def main():
    checked = 0
    for n in range(1, 5):
        for edges in all_graphs(n):
            for k in range(n + 1):
                for q, r in ((3, 0), (3, 1), (4, 2)):
                    check_instance(n, edges, k, q, r)
                    checked += 1
    print(f"independent-set big-residual audit passed: {checked} instances")


if __name__ == "__main__":
    main()
