#!/usr/bin/env python3
"""Exact literal-resource regression for the acyclic step dependency model.

No random choices, floating arithmetic, external packages, or imported verifier.
Finite checks are evidence, not the general proof in proof.md.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json


def predecessors(m, edges):
    assert len(set(edges)) == len(edges)
    assert all(0 <= u < v < m for u, v in edges)
    return [tuple(u for u, v in edges if v == j) for j in range(m)]


def path_polynomial(m, edges):
    pred = predecessors(m, edges)
    endpoint = [[0] * (m + 1) for _ in range(m)]
    for v in range(m):
        endpoint[v][1] = 1
        for u in pred[v]:
            for k in range(1, m):
                endpoint[v][k + 1] += endpoint[u][k]
    return [sum(row[k] for row in endpoint) for k in range(1, m + 1)]


def h_values(m, edges, r):
    pred = predecessors(m, edges)
    h = []
    for v in range(m):
        h.append((1 + sum((h[u] for u in pred[v]), F(0))) / r)
    assert sum(h, F(0)) == sum((F(p) / r**k for k, p in
                                            enumerate(path_polynomial(m, edges), 1)), F(0))
    return h


def strategies(m, edges):
    pred = predecessors(m, edges)
    root = [frozenset((v, b) for v in range(m + 1)) for b in (0, 1)]
    light = []
    for v in range(m):
        light.append([frozenset([(0, b), (v + 1, 1 - b)] +
                               [(u + 1, b) for u in pred[v]]) for b in (0, 1)])
    return [root] + light


def literal_costs(m, edges, amplitudes, bits):
    weights = [F(1)] + [F(1, 2**(v + 1)) for v in range(m)]
    thresholds = [F(1)] + [1 + w for w in weights[1:]]
    menus = strategies(m, edges)
    chosen = [menus[i][b] for i, b in enumerate(bits)]
    loads = {(v, b): sum((weights[i] for i, s in enumerate(chosen) if (v, b) in s), F(0))
             for v in range(m + 1) for b in (0, 1)}
    latency = {e: amplitudes[e[0]] if x >= thresholds[e[0]] else F(0)
               for e, x in loads.items()}
    return [sum((latency[e] for e in s), F(0)) for s in chosen]


def reduced_costs(m, edges, amplitudes, bits):
    pred = predecessors(m, edges)
    selected = {v for v in range(m) if bits[v + 1] != bits[0]}
    costs = [amplitudes[0] + sum((amplitudes[v + 1] for v in selected), F(0))]
    costs += [amplitudes[v + 1] if v in selected else
              amplitudes[0] + sum((amplitudes[u + 1] for u in pred[v] if u in selected), F(0))
              for v in range(m)]
    return costs


def profile_factor(m, edges, amplitudes, bits):
    costs = literal_costs(m, edges, amplitudes, bits)
    assert costs == reduced_costs(m, edges, amplitudes, bits)
    best = F(1)
    for i in range(m + 1):
        deviated = list(bits)
        deviated[i] ^= 1
        after = literal_costs(m, edges, amplitudes, deviated)
        assert after == reduced_costs(m, edges, amplitudes, deviated)
        if not after[i]:
            if costs[i]:
                return None  # positive/zero, infinite improvement
        else:
            best = max(best, costs[i] / after[i])
    return best


def greedy(m, edges, amplitudes, r):
    pred = predecessors(m, edges)
    selected = set()
    for v in range(m):
        p = amplitudes[0] + sum((amplitudes[u + 1] for u in pred[v] if u in selected), F(0))
        if amplitudes[v + 1] <= p / r:
            selected.add(v)
    return [0] + [int(v in selected) for v in range(m)]


def run():
    counts = dict(graphs=0, balanced_profiles=0, real_deviations=0, greedy_profiles=0)
    samples = []
    for m in range(5):
        possible = list(combinations(range(m), 2))
        for mask in range(2**len(possible)):
            edges = [edge for k, edge in enumerate(possible) if (mask >> k) & 1]
            counts['graphs'] += 1
            for r in (F(1), F(3, 2), F(2), F(5, 2)):
                h = h_values(m, edges, r)
                amplitudes = [F(1)] + h
                expected = min(r, 1 + sum(h, F(0))) if m else F(1)
                values = []
                for bits in product((0, 1), repeat=m + 1):
                    ratio = profile_factor(m, edges, amplitudes, bits)
                    assert ratio is not None and ratio >= expected
                    values.append(ratio)
                    counts['balanced_profiles'] += 1
                    counts['real_deviations'] += m + 1
                actual = min(values)
                assert actual == expected
                # Back-check both explicitly claimed attaining states.
                assert profile_factor(m, edges, amplitudes, [0] + [0] * m) == (r if m else 1)
                assert profile_factor(m, edges, amplitudes, [0] + [1] * m) == 1 + sum(h, F(0))
                if m == 4 and mask in (0, 63) and r == 2:
                    samples.append(dict(m=m, edges=edges, paths=path_polynomial(m, edges),
                                        r=str(r), best_factor=str(actual)))
            r = F(1)
            while 1 + sum(h_values(m, edges, r), F(0)) > r:
                r += 1
            tests = [[F(0)] * (m + 1), [F(0)] + [F(v + 1) for v in range(m)],
                     [F(1)] + [F(0)] * m, [F(2)] + [F((v * 7) % 11, 5) for v in range(m)],
                     [F(1)] + h_values(m, edges, r)]
            for amplitudes in tests:
                bits = greedy(m, edges, amplitudes, r)
                current = literal_costs(m, edges, amplitudes, bits)
                for i in range(m + 1):
                    after_bits = bits.copy()
                    after_bits[i] ^= 1
                    after = literal_costs(m, edges, amplitudes, after_bits)
                    assert current[i] <= r * after[i]
                    if amplitudes[0] == 0:
                        assert current[i] <= after[i]
                counts['greedy_profiles'] += 1
    # Larger finite examples, without enumerating all DAGs.
    for m in (5, 7, 9):
        for edges in ([], [(i, i + 1) for i in range(m - 1)], list(combinations(range(m), 2))):
            r = F(3)
            amplitudes = [F(1)] + h_values(m, edges, r)
            target = min(r, sum(amplitudes, F(0)))
            values = [profile_factor(m, edges, amplitudes, bits)
                      for bits in product((0, 1), repeat=m + 1)]
            assert all(v is not None and v >= target for v in values)
            assert min(values) == target
            counts['balanced_profiles'] += len(values)
            counts['real_deviations'] += len(values) * (m + 1)
    return dict(claim='WC-R1-DAG-STEP v1', arithmetic='fractions.Fraction', seed=None,
                floating_point=False, counts=counts, samples=samples,
                conclusion='all stated finite literal-resource checks passed',
                limits='finite regression; the general result is proved separately in proof.md')


if __name__ == '__main__':
    result = run()
    destination = Path(__file__).with_name('verification.json')
    destination.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
