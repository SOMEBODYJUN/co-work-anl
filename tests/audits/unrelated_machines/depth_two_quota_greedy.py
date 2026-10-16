"""两层异质需求的半配额贪心与实际调度审计。

Exact integers/Fraction only. The constructive functions are polynomial in
binary input length; bounded enumeration in audit() is an independent oracle.
Writes stdout only, and never overwrites frozen records.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import platform
import random

from rooted_dag_token_bridge import (
    validate, candidate_thresholds, score, tree_to_schedule, loads,
)


def half_stars(neighbors, demands):
    """Return disjoint stars of ceil(d_u/2), selecting smallest feasible quota."""
    if set(neighbors) != set(demands):
        raise ValueError("centers/demands mismatch")
    if any(type(d) is not int or d <= 0 for d in demands.values()):
        raise ValueError("positive integer demands required")
    available = set().union(*(set(a) for a in neighbors.values()))
    pending = set(neighbors)
    result = {}
    quota = {u: (d + 1) // 2 for u, d in demands.items()}
    while True:
        candidates = [u for u in pending
                      if len(set(neighbors[u]) & available) >= quota[u]]
        if not candidates:
            return result
        u = min(candidates, key=lambda v: (quota[v], v))
        chosen = sorted(set(neighbors[u]) & available)[:quota[u]]
        result[u] = chosen
        available.difference_update(chosen)
        pending.remove(u)


def depth_two_half(n, edges, demands, root=0):
    """For r->positive-demand U->zero-demand W, output b(H)>=b*/2."""
    out = validate(n, edges, demands, root)
    if any(not ((u == root and demands[v] > 0)
                or (u != root and demands[u] > 0 and demands[v] == 0))
           for u, v in edges):
        raise ValueError("requires the stated depth-two layers")
    if demands[root] == 0:
        return []
    neighbors = {u: out[u] for u in out[root]}
    best, best_score = [], F(0)
    for tau in candidate_thresholds(n, edges, demands, root):
        full = {u: -(-(tau * demands[u]).numerator //
                      (tau * demands[u]).denominator) for u in neighbors}
        stars = half_stars(neighbors, full)
        tree = [(root, u) for u in stars]
        tree.extend((u, w) for u, leaves in stars.items() for w in leaves)
        value = score(n, tree, demands, root)
        if value > best_score:
            best, best_score = tree, value
    return best


def independent_optimum(n, edges, demands, root=0):
    """Small edge-subset oracle; deliberately independent of bridge.score."""
    best = F(0) if demands[root] else F(1)
    for bits in product((0, 1), repeat=len(edges)):
        selected = [e for e, keep in zip(edges, bits) if keep]
        incoming = [0] * n
        degree = [0] * n
        adjacency = [[] for _ in range(n)]
        for u, v in selected:
            incoming[v] += 1
            degree[u] += 1
            adjacency[u].append(v)
        if incoming[root] or max(incoming, default=0) > 1:
            continue
        reach, todo = {root}, [root]
        while todo:
            for v in adjacency[todo.pop()]:
                if v not in reach:
                    reach.add(v)
                    todo.append(v)
        if any(u not in reach for u, v in selected):
            continue
        value = min([F(1)] + [F(degree[u], demands[u])
                              for u in reach if demands[u]])
        best = max(best, value)
    return best


def audit_case(n, edges, demands, root=0):
    chosen = depth_two_half(n, edges, demands, root)
    value = score(n, chosen, demands, root)
    optimum = independent_optimum(n, edges, demands, root)
    assert 2 * value >= optimum
    jobs, assignment = tree_to_schedule(n, edges, demands, chosen, root)
    actual = max(loads(n, jobs, assignment))
    assert actual <= 2 - value <= 2 - optimum / 2
    assert actual <= F(3, 2) * (2 - optimum)
    return optimum, value, actual


def audit():
    count = 0
    for nu, nw in ((0, 0), (1, 2), (2, 2)):
        possible = [(0, u) for u in range(1, nu + 1)]
        possible += [(u, w) for u in range(1, nu + 1)
                     for w in range(nu + 1, nu + nw + 1)]
        for bits in product((0, 1), repeat=len(possible)):
            edges = [e for e, keep in zip(possible, bits) if keep]
            for positive in product(range(1, 4), repeat=nu + 1):
                audit_case(1 + nu + nw, edges,
                           list(positive) + [0] * nw)
                count += 1
    seed = 916202610
    rng = random.Random(seed)
    for _ in range(250):
        nu, nw = rng.randrange(1, 4), rng.randrange(1, 5)
        possible = [(0, u) for u in range(1, nu + 1)]
        possible += [(u, w) for u in range(1, nu + 1)
                     for w in range(nu + 1, nu + nw + 1)]
        edges = [e for e in possible if rng.randrange(2)]
        ds = [rng.randrange(1, 8) for _ in range(nu + 1)] + [0] * nw
        audit_case(1 + nu + nw, edges, ds)
    boundaries = [
        (1, [], [0], 0), (1, [], [10**1000], 0),
        (4, [(2, 0), (0, 1), (0, 3)], [10**1000, 0, 10**999, 0], 2),
        (5, [(0, 1), (1, 3), (2, 4)], [2, 2, 10**1000, 0, 0], 0),
    ]
    for args in boundaries:
        audit_case(*args)
    invalid = [
        (2, [(0, 1)], [1, 0]),
        (3, [(0, 1), (1, 2)], [1, 1, 1]),
        (3, [(0, 1), (1, 2)], [0, 1, 0]),
    ]
    for args in invalid:
        try:
            depth_two_half(*args)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid layered contract accepted")
    print(json.dumps({
        "title": "两层异质需求半配额构造的精确核验",
        "python": platform.python_version(), "seed": seed,
        "arithmetic": "integers / fractions.Fraction; exact",
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "exhaustive_inputs": count, "random_inputs": 250,
        "boundary_inputs": len(boundaries), "invalid_rejected": len(invalid),
        "limits": "Finite implementation checks only. General proof is separate; no general DAG or UM-target algorithm.",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    audit()
