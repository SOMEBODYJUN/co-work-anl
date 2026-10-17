#!/usr/bin/env python3
"""Independent exact audit of the defective-coloring large-bundle floor.

No normative implementation is imported.  The oracle enumerates all original
resource parents in a root -> group -> unique-label -> resource DAG, including
absence; positive-score trees are exactly the ancestors of assigned resources.
The separate construction uses integer monochromatic potential descent, then
checks every Hall subset and enumerates an actual integral quota allocation.
Finite computations do not prove the general claim or any hardness result.
"""

from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import platform


def actual_tree_optimum(bundles):
    """Full actual-root-tree oracle for this one-label-per-group test domain."""
    q = len(bundles)
    assert q and all(bundles)
    resources = sorted(frozenset().union(*bundles))
    incoming = [[-1] + [x for x, S in enumerate(bundles) if u in S]
                for u in resources]
    best = Fraction(0)
    examined = 0
    for owners in product(*incoming):
        examined += 1
        counts = Counter(x for x in owners if x != -1)
        if counts:
            score = min([Fraction(1), Fraction(len(counts), q)] +
                        [Fraction(count, len(bundles[x]))
                         for x, count in counts.items()])
            best = max(best, score)
    return best, examined


def collision_degree(bundles):
    return max(sum(u in S for S in bundles)
               for u in frozenset().union(*bundles))


def monochromatic_potential(weights, colors):
    return sum(weights[x][y] for x in range(len(colors)) for y in range(x)
               if colors[x] == colors[y])


def defective_colors(weights, c):
    q = len(weights)
    degree = list(map(sum, weights))
    colors = [0] * q
    old = monochromatic_potential(weights, colors)
    initial = old
    moves = 0
    while True:
        for x in range(q):
            costs = [sum(weights[x][y] for y in range(q) if colors[y] == col)
                     for col in range(c)]
            if c * costs[colors[x]] > degree[x]:
                colors[x] = min(range(c), key=lambda col: costs[col])
                new = monochromatic_potential(weights, colors)
                assert new < old
                old = new
                moves += 1
                break
        else:
            break
    assert moves <= initial
    for x in range(q):
        within = sum(weights[x][y] for y in range(q)
                     if colors[y] == colors[x])
        assert c * within <= degree[x]
    return colors, moves


def actual_quota_allocation(bundles, group, quotas):
    resources = sorted(frozenset().union(*bundles))
    incoming = [[-1] + [x for x in group if quotas[x] and u in bundles[x]]
                for u in resources]
    for owners in product(*incoming):
        counts = {x: owners.count(x) for x in group if quotas[x]}
        if all(counts.get(x, 0) >= k for x, k in quotas.items()):
            active = [x for x in group if counts.get(x, 0)]
            score = (min([Fraction(1), Fraction(len(active), len(bundles))] +
                         [Fraction(counts[x], len(bundles[x])) for x in active])
                     if active else Fraction(0))
            return score
    raise AssertionError(('no actual quota allocation', bundles, group, quotas))


def audit():
    resource_sets = [frozenset(S) for size in (1, 2, 3)
                     for S in combinations(range(3), size)]
    eta_grid = sorted({Fraction(a, b) for b in range(2, 17)
                       for a in range(1, b)})
    totals = Counter()
    for q in range(1, 5):
        for bundles in product(resource_sets, repeat=q):
            optimum, examined = actual_tree_optimum(bundles)
            totals['cases'] += 1
            totals['resource_parent_assignments'] += examined
            delta = collision_degree(bundles)
            weights = [[len(S & T) if x != y else 0
                        for y, T in enumerate(bundles)]
                       for x, S in enumerate(bundles)]
            degree = list(map(sum, weights))
            for x, S in enumerate(bundles):
                assert degree[x] <= (delta - 1) * len(S)
            # A complete single group always gives a 1/q-score actual tree.
            assert optimum >= Fraction(1, q)
            k_min = min(map(len, bundles))
            for eta in eta_grid:
                if optimum <= eta:
                    reciprocal = 1 / eta
                    assert q >= reciprocal
                    c_eta = -((-reciprocal.numerator) // reciprocal.denominator) - 1
                    assert 1 <= c_eta <= q and Fraction(1, c_eta) > eta
                    collision_lower = 1 + c_eta * (1 / (eta + Fraction(1, k_min)) - 1)
                    assert delta >= collision_lower
                    totals['eta_collision_necessity_checks'] += 1
            for c in range(1, q + 1):
                dc = 1 + Fraction(delta - 1, c)
                root_floor = Fraction(-((-q) // c), q)
                lower = min([root_floor] +
                            [Fraction(int(Fraction(len(S), 1) / dc), len(S))
                             for S in bundles])
                assert optimum >= lower
                totals['parameter_claim_checks'] += 1
                colors, moves = defective_colors(weights, c)
                totals['strict_defective_recolorings'] += moves
                group = max(([x for x in range(q) if colors[x] == col]
                             for col in range(c)), key=len)
                assert c * len(group) >= q
                quotas = {x: int(Fraction(len(bundles[x]), 1) / dc)
                          for x in group}
                for mask in range(1 << len(group)):
                    chosen = [x for i, x in enumerate(group) if mask >> i & 1]
                    union = frozenset().union(*(bundles[x] for x in chosen))
                    assert len(union) >= sum(quotas[x] for x in chosen)
                    totals['hall_subset_checks'] += 1
                actual_score = actual_quota_allocation(bundles, group, quotas)
                assert actual_score >= lower

    # In the all-identical q=K=t^2 family, a tree with s groups can achieve
    # exactly min(s/q, floor(K/s)/K).  Enumerating s is an exact cardinality
    # check for these finite symmetric families, not for arbitrary instances.
    benchmark = []
    for t in range(1, 41):
        q = k = t * t
        exact = max(min(Fraction(s, q), Fraction(k // s, k))
                    for s in range(1, q + 1))
        assert exact == Fraction(1, t)
        c = 1 if t == 1 else t + 1
        assert 1 <= c <= q
        dc = 1 + Fraction(q - 1, c)
        lower = min(Fraction(-((-q) // c), q),
                    Fraction(int(Fraction(k, 1) / dc), k))
        assert lower == exact
        benchmark.append({'t': t, 'c': c, 'exact': str(exact), 'lower': str(lower)})
    return {
        'status': 'pass',
        **dict(sorted(totals.items())),
        'benchmarks': benchmark,
        'python': platform.python_version(),
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope': ('independent finite audit; complete single-label bundles on '
                  'three resources, q1..4; no normative imports; '
                  'no general hardness implication'),
    }


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2, sort_keys=True))
