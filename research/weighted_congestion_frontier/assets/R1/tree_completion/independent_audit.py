#!/usr/bin/env python3
"""Independent exact audit of the symmetric tree/DAG step model.

No production proof or verifier is imported.  Loads are constructed from
the actual strategies with integer-scaled positive dyadic weights.
"""
from fractions import Fraction as F
from itertools import product
import json
import random


def incoming(m, edges):
    ins = [[] for _ in range(m + 1)]
    for u, v in edges:
        assert 1 <= u < v <= m
        ins[v].append(u)
    return ins


def path_counts(m, ins):
    ends = [[0] * (m + 1) for _ in range(m + 1)]
    for v in range(1, m + 1):
        ends[v][1] = 1
        for u in ins[v]:
            for k in range(1, m):
                ends[v][k + 1] += ends[u][k]
    return [sum(ends[v][k] for v in range(1, m + 1))
            for k in range(1, m + 1)]


def h_values(m, ins, r):
    h = [F(0)] * (m + 1)
    for v in range(1, m + 1):
        h[v] = (1 + sum((h[u] for u in ins[v]), F(0))) / r
    return h


def threshold_residual(m, ins, r):
    return r - 1 - sum(h_values(m, ins, r))


def threshold_bracket(m, ins, steps=72):
    if not m:
        return F(1), F(1)
    lo, hi = F(1), F(m + 1)
    for _ in range(steps):
        mid = (lo + hi) / 2
        if threshold_residual(m, ins, mid) < 0:
            lo = mid
        else:
            hi = mid
    assert threshold_residual(m, ins, lo) <= 0
    assert threshold_residual(m, ins, hi) >= 0
    return lo, hi


def legal_weights(m, edges):
    w = [2 ** (m - v) for v in range(m + 1)]
    assert sum(w[1:]) < w[0]
    for u in range(1, m + 1):
        assert sum(w[v] for a, v in edges if a == u) < w[u]
    return w


def direct_masks(m, ins, state, w):
    strategies = []
    strategies.append([(v, state[0]) for v in range(m + 1)])
    for v in range(1, m + 1):
        # bit 0 uses own a_v and incoming b; bit 1 uses own b_v
        # and incoming a.  The root resource is always an incoming one.
        strategies.append([(v, state[v])] +
                          [(u, 1 - state[v]) for u in [0] + ins[v]])
    loads = {(v, side): 0 for v in range(m + 1) for side in (0, 1)}
    for i, strategy in enumerate(strategies):
        for resource in strategy:
            loads[resource] += w[i]
    thresholds = [w[0]] + [w[0] + w[v] for v in range(1, m + 1)]
    return [frozenset(v for v, side in strategy
                      if loads[v, side] >= thresholds[v])
            for strategy in strategies]


def reduced_masks(m, ins, state):
    z = {v for v in range(1, m + 1) if state[v] == state[0]}
    return [frozenset({0} | z)] + [
        frozenset({v}) if v in z else
        frozenset({0} | (set(ins[v]) & z))
        for v in range(1, m + 1)]


def mask_cost(mask, amplitudes):
    return sum((amplitudes[v] for v in mask), F(0))


def stable(masks, state, amplitudes, r):
    for i in range(len(state)):
        deviated = list(state)
        deviated[i] ^= 1
        if mask_cost(masks[state][i], amplitudes) > r * mask_cost(
                masks[tuple(deviated)][i], amplitudes):
            return False
    return True


def greedy(m, ins, amplitudes, r):
    # Heavy is fixed to side a.  This uses multiplication, never 0/0.
    state = [0] + [1] * m
    for v in range(1, m + 1):
        p = amplitudes[0] + sum(
            (amplitudes[u] for u in ins[v] if state[u] == 0), F(0))
        if r * amplitudes[v] <= p:
            state[v] = 0
    return tuple(state)


def best_factor(masks, amplitudes):
    best = None
    for state in masks:
        ratio = F(1)
        for i in range(len(state)):
            deviated = list(state)
            deviated[i] ^= 1
            current = mask_cost(masks[state][i], amplitudes)
            target = mask_cost(masks[tuple(deviated)][i], amplitudes)
            if target == 0:
                if current > 0:
                    ratio = None
                    break
            else:
                ratio = max(ratio, current / target)
        if ratio is not None and (best is None or ratio < best):
            best = ratio
    assert best is not None
    return best


def audit_graph(m, edges, amplitude_vectors, totals):
    ins = incoming(m, edges)
    w = legal_weights(m, edges)
    masks = {}
    for state in product((0, 1), repeat=m + 1):
        real = direct_masks(m, ins, state, w)
        expected = reduced_masks(m, ins, state)
        assert real == expected, (m, edges, state, real, expected)
        masks[state] = real
        totals['real_load_profiles'] += 1
    counts = path_counts(m, ins)
    lo, hi = threshold_bracket(m, ins)
    for r in (F(1), F(3, 2), F(2), F(3), hi):
        assert sum(h_values(m, ins, r)) == sum(
            (F(pk) / r ** k for k, pk in enumerate(counts, 1)), F(0))
    delta = max((len(ins[v]) for v in range(1, m + 1)), default=0)
    # An exact rational upper bracket for the claimed quadratic bound.
    bound_lo, bound_hi = F(max(1, delta)), F(m + delta + 1)
    for _ in range(72):
        mid = (bound_lo + bound_hi) / 2
        if (mid - 1) * (mid - delta) < m:
            bound_lo = mid
        else:
            bound_hi = mid
    assert threshold_residual(m, ins, bound_hi) >= 0
    for values in amplitude_vectors:
        amplitudes = tuple(F(x) for x in values)
        state = greedy(m, ins, amplitudes, hi)
        assert stable(masks, state, amplitudes, hi)
        if amplitudes[0] == 0:
            assert stable(masks, state, amplitudes, F(1))
        beta = best_factor(masks, amplitudes)
        assert beta <= hi
        totals['amplitude_instances'] += 1
        totals['all_state_amplitude_profiles'] += len(masks)
    # Rational path-balanced instances check an exact attained threshold,
    # including at parameters above the optimal universal threshold.
    for r in (F(1), F(3, 2), F(2), F(3), F(m + 2)):
        if not m:
            expected_beta = F(1)
        else:
            expected_beta = min(r, 1 + sum(h_values(m, ins, r)))
        amplitudes = [F(1)] + h_values(m, ins, r)[1:]
        assert best_factor(masks, amplitudes) == expected_beta
        totals['balanced_exact_instances'] += 1
    totals['graphs'] += 1
    return masks, ins


def check_tree_reduction(totals):
    for m in range(6):
        for parents in product(*(range(v) for v in range(1, m + 1))):
            ancestors = [[] for _ in range(m + 1)]
            depths = [0] * (m + 1)
            for v, p in enumerate(parents, 1):
                ancestors[v] = ([] if p == 0 else ancestors[p] + [p])
                depths[v] = depths[p] + 1
            for r in (F(1), F(3, 2), F(2), F(3)):
                h = h_values(m, ancestors, r)
                for v in range(1, m + 1):
                    assert h[v] == (1 / r) * (1 + 1 / r) ** (depths[v] - 1)
                assert sum(h) >= F(m) / r
                assert sum(h) <= sum(((1 / r) * (1 + 1 / r) ** k
                                     for k in range(m)), F(0))
            totals['tree_symbolic_specializations'] += 1


def check_strictness_fixtures(totals):
    # Strict descendant inequality is essential when amplitudes are positive.
    m, edges = 2, [(1, 2)]
    ins = incoming(m, edges)
    state = (0, 1, 1)
    assert direct_masks(m, ins, state, [4, 1, 1]) != reduced_masks(m, ins, state)
    # Strict total-light inequality keeps the no-heavy root side inactive.
    ins = incoming(2, [])
    state = (0, 0, 0)
    assert direct_masks(2, ins, state, [2, 1, 1]) != reduced_masks(2, ins, state)
    totals['rejected_boundary_fixtures'] = 2


def main():
    totals = dict(graphs=0, real_load_profiles=0, amplitude_instances=0,
                  all_state_amplitude_profiles=0, balanced_exact_instances=0,
                  tree_symbolic_specializations=0)
    for m in range(5):
        possible = [(u, v) for u in range(1, m + 1) for v in range(u + 1, m + 1)]
        values = (0, 1, 2) if m <= 3 else (0, 1)
        for bits in product((0, 1), repeat=len(possible)):
            edges = [e for e, bit in zip(possible, bits) if bit]
            audit_graph(m, edges, product(values, repeat=m + 1), totals)
    random_source = random.Random(200207466)
    for m in (5, 6, 7):
        for _ in range(8):
            edges = [(u, v) for u in range(1, m + 1) for v in range(u + 1, m + 1)
                     if random_source.randrange(3) == 0]
            amplitudes = [tuple(F(random_source.randrange(5), random_source.randrange(1, 5))
                                for _ in range(m + 1)) for _ in range(8)]
            audit_graph(m, edges, amplitudes, totals)
    # Exact optimal endpoint with both branching and merging.
    for m, edges, q in ((2, [], F(2)),
                         (5, [(1, 3), (1, 4), (2, 5)], F(3)),
                         (5, [(1, 3), (2, 3), (2, 4)], F(3))):
        masks, ins = audit_graph(m, edges, [], totals)
        assert threshold_residual(m, ins, q) == 0
        amplitudes = [F(1)] + h_values(m, ins, q)[1:]
        assert best_factor(masks, amplitudes) == q
        assert stable(masks, tuple([0] * (m + 1)), amplitudes, q)
        assert stable(masks, tuple([0] + [1] * m), amplitudes, q)
    totals['exact_optimal_endpoints'] = 3
    check_tree_reduction(totals)
    check_strictness_fixtures(totals)
    print(json.dumps({'status': 'PASS', 'seed': 200207466,
                      'arithmetic': 'integer loads; Fraction costs and comparisons',
                      'coverage': totals}, indent=2))


if __name__ == '__main__':
    main()
