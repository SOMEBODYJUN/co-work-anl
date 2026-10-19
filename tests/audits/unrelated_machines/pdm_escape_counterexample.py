#!/usr/bin/env python3
"""Exact finite audit of a low-load NO instance for the pDM threshold bridge.

This is deliberately a finite witness.  It does not prove a general upper
bound for NO instances; it records that the threshold construction alone does
not force a near-two makespan when a perfect matching is absent.
"""

from fractions import Fraction as F
from itertools import product


def build_instance():
    # Three parts A,B,C, two vertices per part, and three hyperedges.  Every
    # pair of hyperedges intersects, so no 3-dimensional perfect matching can
    # exist (a perfect matching here would need all three edges).
    edges = (("a1", "b1", "c1"), ("a1", "b2", "c2"), ("a2", "b1", "c2"))
    d, n, b = 3, 2, 4
    m = len(edges)
    vertices = tuple(v for part in zip(*edges) for v in part)
    # zip(*edges) is grouped by coordinate; remove the accidental tuple
    # flattening ambiguity explicitly while retaining deterministic order.
    vertices = ("a1", "a2", "b1", "b2", "c1", "c2")
    jobs = []
    options = []
    for v in vertices:
        support = tuple(i for i, e in enumerate(edges) if v in e)
        jobs.append((f"vertex:{v}", F(b), support))
        options.append(support)
    dummy_count = b * (m - n)
    for k in range(dummy_count):
        jobs.append((f"dummy:{k}", F(d), tuple(range(m))))
        options.append(tuple(range(m)))
    T = F(b * d)
    return edges, d, n, b, m, T, jobs, options


def exhaustive_optimum(m, jobs, options):
    best = None
    best_assignment = None
    best_loads = None
    checked = 0
    for assignment in product(*options):
        checked += 1
        loads = [F(0) for _ in range(m)]
        for (_, p, _), machine in zip(jobs, assignment):
            loads[machine] += p
        value = max(loads, default=F(0))
        if best is None or value < best:
            best, best_assignment, best_loads = value, assignment, loads
    return best, best_assignment, best_loads, checked


def main():
    edges, d, n, b, m, T, jobs, options = build_instance()
    assert all(set(edges[i]) & set(edges[j]) for i in range(m) for j in range(i + 1, m))
    assert not any(len({edges[i][part] for i in range(m)}) == m for part in range(d))
    total_work = sum((p for _, p, _ in jobs), F(0))
    assert total_work == F(b * d * m)
    optimum, assignment, loads, checked = exhaustive_optimum(m, jobs, options)
    assert optimum == F(13)
    assert max(loads) == optimum
    assert optimum > T
    assert optimum / T == F(13, 12)
    print({
        "edges": edges,
        "d": d,
        "n": n,
        "b": b,
        "machines": m,
        "dummy_jobs": b * (m - n),
        "total_work": str(total_work),
        "threshold_T": str(T),
        "assignments_checked": checked,
        "optimum": str(optimum),
        "best_loads": [str(x) for x in loads],
        "best_assignment": assignment,
        "ratio_opt_over_T": str(optimum / T),
        "status": "ok",
    })


if __name__ == "__main__":
    main()
