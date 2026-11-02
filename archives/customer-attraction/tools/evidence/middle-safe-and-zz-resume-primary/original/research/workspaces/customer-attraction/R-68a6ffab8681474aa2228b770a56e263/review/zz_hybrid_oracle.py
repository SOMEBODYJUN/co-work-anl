"""Exact reviewer oracle for local four-state blocks and attractive cross edges.

This audits a representation tool, not Q-CAG-HALF-6. All arithmetic is integer.
The positive quadratic part is reduced to maximum-weight closure, a formulation
different from the previous factor-two Ising cut implementation.
"""
from collections import deque
from itertools import product
from pathlib import Path
import json
import random


def positive_quadratic_max(constant, unary, edges):
    """Maximize constant + sum a_i*x_i + sum J_ij*x_i*x_j, J>=0."""
    assert all(j >= 0 for _, _, j in edges)
    nonzero = [(i, k, j) for i, k, j in edges if j]
    weights = list(unary) + [j for _, _, j in nonzero]
    n = len(weights)
    source, sink = n, n+1
    residual = [dict() for _ in range(n+2)]

    def arc(a, b, capacity):
        residual[a][b] = residual[a].get(b, 0) + capacity
        residual[b].setdefault(a, 0)

    positive = sum(max(w, 0) for w in weights)
    infinity = positive + 1
    for i, w in enumerate(weights):
        if w > 0:
            arc(source, i, w)
        elif w < 0:
            arc(i, sink, -w)
    for e, (i, k, _) in enumerate(nonzero, len(unary)):
        arc(e, i, infinity)
        arc(e, k, infinity)
    flow = 0
    while True:
        parent = {source: None}
        queue = deque([source])
        while queue and sink not in parent:
            a = queue.popleft()
            for b, c in residual[a].items():
                if c > 0 and b not in parent:
                    parent[b] = a
                    queue.append(b)
        if sink not in parent:
            break
        amount = infinity
        b = sink
        while b != source:
            a = parent[b]
            amount = min(amount, residual[a][b])
            b = a
        b = sink
        while b != source:
            a = parent[b]
            residual[a][b] -= amount
            residual[b][a] += amount
            b = a
        flow += amount
    return constant + positive - flow


def evaluate(tables, cross_edges, bits):
    return sum(table[2*bits[2*e]+bits[2*e+1]]
               for e, table in enumerate(tables)) + sum(
                   j*bits[i]*bits[k] for i, k, j in cross_edges)


def hybrid_max(tables, cross_edges):
    """Branch only on blocks with negative local mixed difference."""
    constant = sum(t[0] for t in tables)
    unary = []
    edges = list(cross_edges)
    bad = []
    for e, (v00, v01, v10, v11) in enumerate(tables):
        unary.extend((v10-v00, v01-v00))
        delta = v11+v00-v10-v01
        if delta:
            edges.append((2*e, 2*e+1, delta))
        if delta < 0:
            bad.append(2*e)
    assert all(j >= 0 and i//2 != k//2 for i, k, j in cross_edges)
    best = None
    for values in product((0, 1), repeat=len(bad)):
        fixed = dict(zip(bad, values))
        free = [i for i in range(len(unary)) if i not in fixed]
        reindex = {i: j for j, i in enumerate(free)}
        b = constant + sum(unary[i]*v for i, v in fixed.items())
        a = [unary[i] for i in free]
        attractive = []
        for i, k, j in edges:
            if i in fixed and k in fixed:
                b += j*fixed[i]*fixed[k]
            elif i in fixed:
                a[reindex[k]] += j*fixed[i]
            elif k in fixed:
                a[reindex[i]] += j*fixed[k]
            else:
                assert j >= 0
                attractive.append((reindex[i], reindex[k], j))
        candidate = positive_quadratic_max(b, a, attractive)
        best = candidate if best is None else max(best, candidate)
    return best


def main():
    rng = random.Random(681061)
    checked = 0
    bad_counts = set()
    for n in range(1, 6):
        for case in range(24):
            tables = [[rng.randrange(-8, 9) for _ in range(4)]
                      for _ in range(n)]
            if case == 0:
                tables = [[0, 0, 0, 0] for _ in range(n)]
            if case == 1:
                tables = [[0, 2, 2, 0] for _ in range(n)]
            edges = [(i, k, rng.randrange(7))
                     for i in range(2*n) for k in range(i+1, 2*n)
                     if i//2 != k//2]
            expected = max(evaluate(tables, edges, bits)
                           for bits in product((0, 1), repeat=2*n))
            actual = hybrid_max(tables, edges)
            assert actual == expected, (tables, edges, actual, expected)
            bad_counts.add(sum(t[3]+t[0]-t[2]-t[1] < 0 for t in tables))
            checked += 1
    # A local negative interaction forbids orbit-constant assignments even
    # when every cross-block coupling is attractive. Never use the old
    # invariant-orbit proof on these four-state blocks without a new argument.
    tables = [[0, 1, 1, 0], [0, 1, 1, 0]]
    edges = [(0, 2, 2), (1, 3, 2)]
    assert hybrid_max(tables, edges) == max(
        evaluate(tables, edges, b) for b in product((0, 1), repeat=4))
    report = {
        "status": "PASS",
        "scope": "exact representation/implementation audit; no six-player welfare conclusion",
        "seed": 681061,
        "random_and_boundary_cases": checked,
        "negative_local_block_counts_tested": sorted(bad_counts),
        "method": "branch negative local blocks, then exact maximum closure",
    }
    path = Path(__file__).with_name("zz_hybrid_audit.json")
    path.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
