#!/usr/bin/env python3
"""Persist the two omitted lower-end duals and a literal 16-state counterexample."""
import argparse
from fractions import Fraction as Q
import hashlib
import heapq
import importlib.util
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'original/tests/audits/weighted_congestion/decision_methods/calibration_audit.py'


def encoded(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {str(k): encoded(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [encoded(v) for v in value]
    return value


def dual_record(A, b, y):
    assert len(A) == len(b) == len(y) and all(v >= 0 for v in y)
    columns = len(A[0]) if A else 0
    product_ = [sum((A[i][j] * y[i] for i in range(len(A))), Q(0)) for j in range(columns)]
    scalar = sum((b[i] * y[i] for i in range(len(b))), Q(0))
    assert all(v >= 0 for v in product_) and scalar < 0
    return {'A': A, 'b': b, 'y': y, 'A_transpose_y': product_, 'b_transpose_y': scalar,
            'independent_original_row_check': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=HERE / 'extra-witnesses.json')
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Output exists; refusing to overwrite')
    spec = importlib.util.spec_from_file_location('preserved_calibration', SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    original_solver = module.solve_feasibility
    captured = []

    def capturing_solver(A, b, nvars=None, pivot_cap=20000):
        result = original_solver(A, b, nvars, pivot_cap)
        captured.append((A, b, result))
        return result

    module.solve_feasibility = capturing_solver
    weights = [Q(3), Q(1)]
    resources = [module.local_resource((0, 1), weights, c, [(0, 1), (1, 0)])
                 for c in [(0, 0, 1), (0, 0, 0, 1), (1,), (0,)]]
    lower_duals = []
    for name, alpha, oracle in [('dictionary', Q(311, 256), module.dictionary_lp),
                                 ('full_local', Q(135, 128), module.full_local_lp)]:
        before = len(captured)
        result = oracle(resources, 2, alpha)
        assert len(captured) == before + 1 and result['status'] == 'INFEASIBLE'
        A, b, raw = captured[-1]
        lower_duals.append({'interface': name, 'alpha': alpha, 'result': result,
                            **dual_record(A, b, raw['farkas'])})

    # Independent literal costs, not the author's polynomial/resource routine.
    weights = (Q(1), Q(2))
    menus = (frozenset(), frozenset({0}), frozenset({1}), frozenset({0, 1}))
    profiles = list(product(range(4), repeat=2))
    index = {p: i for i, p in enumerate(profiles)}
    costs = []
    for p in profiles:
        loads = [sum((weights[i] for i in range(2) if e in menus[p[i]]), Q(0)) for e in range(2)]
        fees = (loads[0], loads[1] ** 2)
        costs.append([sum((fees[e] for e in menus[p[i]]), Q(0)) for i in range(2)])
    edges = []
    for s, p in enumerate(profiles):
        for i in range(2):
            for action in range(4):
                if action != p[i]:
                    target = list(p)
                    target[i] = action
                    edges.append((s, index[tuple(target)], i))
    adapter = module.enumerate_game(weights, [[set(x) for x in menus]] * 2,
                                    [(0, 1), (0, 0, 1)])
    assert adapter['profiles'] == profiles and adapter['costs'] == costs and adapter['edges'] == edges
    strict = [(s, t, i) for s, t, i in edges if costs[s][i] > costs[t][i]]
    assert len(profiles) == 16 and len(edges) == 96 and len(strict) == 47
    outgoing = [[] for _ in profiles]
    degree = [0] * len(profiles)
    for s, t, _ in strict:
        outgoing[s].append(t)
        degree[t] += 1
    ready = [i for i, n in enumerate(degree) if n == 0]
    heapq.heapify(ready)
    order = []
    while ready:
        s = heapq.heappop(ready)
        order.append(s)
        for t in outgoing[s]:
            degree[t] -= 1
            if degree[t] == 0:
                heapq.heappush(ready, t)
    assert len(order) == 16
    rank = {s: i for i, s in enumerate(order)}
    assert all(rank[s] < rank[t] for s, t, _ in strict)
    sinks = [s for s, row in enumerate(outgoing) if not row]
    assert sinks == [0]
    frozen = json.loads((HERE / 'original/evidence/runs/weighted_congestion/decision_methods/calibration_audit.json').read_text())
    y = list(map(Q, frozen['real_game_calibration_no_despite_exact_pne']['graph_lp']['farkas']))
    A, b = [], []
    for s, t, i in edges:
        budget = costs[t][i] - costs[s][i]
        row = [Q(0)] * 18
        row[t] += 1
        row[s] -= 1
        row[16 + i] -= budget
        A.append(row)
        b.append(budget)
    graph_dual = dual_record(A, b, y)
    result = {'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              'exporter_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'scope': 'Two additional dual exports and independent literal/topological checks; not a repeat of the complete author audit.',
              'lower_endpoint_duals': lower_duals,
              'unique_empty_pne_counterexample': {'weights': weights, 'menus_resource_indices': [sorted(x) for x in menus],
                  'profiles': profiles, 'costs': costs, 'all_real_deviations': edges,
                  'strict_improvement_edges': strict, 'topological_order': order,
                  'unique_sink': 0, 'graph_alpha1_dual': graph_dual}}
    with args.output.open('x', encoding='utf-8') as stream:
        json.dump(encoded(result), stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps({'status': 'PASS', 'persisted_lower_duals': 2,
                      'literal_states': 16, 'all_deviations': 96, 'strict_edges': 47,
                      'topological_order_verified': True}))


if __name__ == '__main__':
    main()
