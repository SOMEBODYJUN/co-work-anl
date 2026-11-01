#!/usr/bin/env python3
"""Definition-level Fraction audit; no game solver or LP is imported."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from fractions import Fraction as Q
from itertools import product
from math import comb
from pathlib import Path


def vector_add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def vector_sub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def rank(rows):
    if not rows:
        return 0
    mat = [list(row) for row in rows]
    pivot = 0
    for col in range(len(mat[0])):
        at = next((k for k in range(pivot, len(mat)) if mat[k][col]), None)
        if at is None:
            continue
        mat[pivot], mat[at] = mat[at], mat[pivot]
        scale = mat[pivot][col]
        mat[pivot] = [x / scale for x in mat[pivot]]
        for k in range(len(mat)):
            if k != pivot:
                scale = mat[k][col]
                mat[k] = [x - scale * y for x, y in zip(mat[k], mat[pivot])]
        pivot += 1
    return pivot


def analyse_strategy(p, n, sigma):
    types = range(1, 1 << p)
    histories = [h for depth in range(n) for h in product(range(p), repeat=depth)]
    assert set(sigma) == set(histories)

    def terminal(history):
        history = tuple(history)
        while len(history) < n:
            history += (sigma[history],)
        return history

    def vertex(history, action):
        leaf = terminal(history + (action,))
        return tuple(leaf.count(a) for a in range(p)), action

    def payoff(v):
        q, a = v
        assert q[a] > 0 and sum(q) == n
        return tuple(Q(1, sum(q[b] for b in range(p) if mask >> b & 1))
                     if mask >> a & 1 else Q(0) for mask in types)

    graph = defaultdict(set)
    witness = {}
    rows = {}
    endpoints = {}
    for h in histories:
        for a in range(p):
            u, v = vertex(h, a), vertex(h, sigma[h])
            graph[u].add(v)
            graph[v]
            witness.setdefault((u, v), (h, a))
            rows[h, a] = vector_sub(payoff(v), payoff(u))
            endpoints[h, a] = (u, v)

    def reach(start):
        visited, stack = {start}, [start]
        while stack:
            for v in graph[stack.pop()]:
                if v not in visited:
                    visited.add(v)
                    stack.append(v)
        return visited

    reachable = {v: reach(v) for v in graph}
    remaining, components = set(graph), []
    while remaining:
        first = min(remaining)
        component = {v for v in reachable[first] if first in reachable[v]}
        components.append(tuple(sorted(component)))
        remaining -= component
    component_id = {v: i for i, comp in enumerate(components) for v in comp}
    representatives = [comp[0] for comp in components]

    def path(source, target):
        queue = deque([source])
        previous = {source: None}
        while queue:
            u = queue.popleft()
            if u == target:
                break
            for v in sorted(graph[u]):
                if v not in previous:
                    previous[v] = u
                    queue.append(v)
        assert target in previous
        pairs = []
        v = target
        while previous[v] is not None:
            u = previous[v]
            pairs.append((u, v))
            v = u
        return tuple(witness[edge] for edge in reversed(pairs))

    zero = (Q(0),) * ((1 << p) - 1)
    internal_rows = []
    route_checks = 0
    for comp in components:
        for u in comp:
            for v in comp:
                chosen_path = path(u, v)
                summed = zero
                for key in chosen_path:
                    summed = vector_add(summed, rows[key])
                assert summed == vector_sub(payoff(v), payoff(u))
                route_checks += 1
            internal_rows.append(vector_sub(payoff(u), payoff(comp[0])))

    condensation = set()
    for (u, v), key in witness.items():
        ci, cj = component_id[u], component_id[v]
        ri, rj = representatives[ci], representatives[cj]
        # Exact proof identity for every distinct graph edge, including loops.
        delta = vector_sub(payoff(rj), payoff(ri))
        error = vector_sub(vector_sub(payoff(v), payoff(rj)),
                           vector_sub(payoff(u), payoff(ri)))
        assert vector_add(delta, error) == rows[key]
        if ci != cj:
            condensation.add((ci, cj))

    # A DAG certificate by explicit reachability on the condensation.
    cg = defaultdict(set)
    for ci, cj in condensation:
        cg[ci].add(cj)
    for start in range(len(components)):
        todo, seen = list(cg[start]), set()
        while todo:
            ci = todo.pop()
            assert ci != start
            if ci not in seen:
                seen.add(ci)
                todo.extend(cg[ci])

    terminal_ties = []
    for h in product(range(p), repeat=n - 1):
        for g in product(range(p), repeat=n - 1):
            if sorted(h) == sorted(g) and sigma[h] != sigma[g]:
                terminal_ties.append(rows[h, sigma[g]])

    return {
        'terminal': terminal, 'payoff': payoff, 'rows': rows,
        'endpoints': endpoints, 'components': components, 'path': path,
        'internal_rows': internal_rows, 'terminal_ties': terminal_ties,
        'condensation': condensation, 'graph_edges': len(witness),
        'path_checks': route_checks, 'vertices': len(graph),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    p, n = 3, 3
    sigma = {(): 2, (0,): 1, (1,): 1, (2,): 1}
    table = [[1, 1, 1], [1, 0, 0], [1, 1, 1]]
    sigma.update({(a, b): table[a][b] for a, b in product(range(p), repeat=2)})
    data = analyse_strategy(p, n, sigma)
    rows = data['rows']
    w = (3, 5, 3, 3, 1, 3, 0)
    slacks = {key: sum(a * b for a, b in zip(row, w)) for key, row in rows.items()}
    assert len(slacks) == 39 and min(slacks.values()) == 0
    assert all(x >= 0 for x in slacks.values())
    terminal_rank = rank(data['terminal_ties'])
    scc_rank = rank(data['internal_rows'])
    assert (terminal_rank, scc_rank) == (1, 3)
    assert rank(data['terminal_ties'] + [rows[(), 0], rows[(1,), 0]]) == 3
    cycle1 = [((), 0), ((1, 1), 2)]
    cycle2 = [((1,), 0), ((), 1), ((1, 1), 2)]
    for cycle in [cycle1, cycle2]:
        assert tuple(sum(rows[key][i] for key in cycle) for i in range(7)) == (0,) * 7
    root = data['terminal'](())
    qroot = tuple(root.count(a) for a in range(p))
    payoffs = [sum(a * b for a, b in zip(data['payoff']((qroot, a)), w)) for a in root]
    welfare = sum(w[mask - 1] for mask in range(1, 8)
                  if any(qroot[a] for a in range(p) if mask >> a & 1))
    assert root == (2, 1, 1) and payoffs == [5, 5, 5] and welfare == 15
    assert sum(w) == 18
    boundary_cases = []
    for bp, bn in [(1, 1), (1, 7), (3, 1), (4, 1)]:
        bsigma = {h: bp - 1 for depth in range(bn)
                  for h in product(range(bp), repeat=depth)}
        boundary = analyse_strategy(bp, bn, bsigma)
        expected_vertices = bp * comb(bn + bp - 2, bp - 1)
        assert boundary['vertices'] == expected_vertices
        if bp == 1:
            assert all(not any(row) for row in boundary['rows'].values())
        boundary_cases.append({'topics': bp, 'players': bn,
                               'vertices': boundary['vertices'],
                               'formula': expected_vertices,
                               'all_rows': len(boundary['rows'])})
    report = {
        'status': 'exact_fixed_strategy_representation_audit_passed',
        'general_half': 'OPEN', 'players': n, 'topics': p,
        'type_masks': list(range(1, 8)), 'multiplicities': w,
        'actions': [{'history': h, 'action': a} for h, a in sigma.items()],
        'root': root, 'root_payoffs': list(map(str, payoffs)),
        'W': welfare, 'OPT': sum(w), 'history_comparisons': len(slacks),
        'minimum_spe_slack': str(min(slacks.values())),
        'payoff_vertices': data['vertices'], 'distinct_edges': data['graph_edges'],
        'sccs': data['components'], 'scc_count': len(data['components']),
        'condensation_arcs': sorted(data['condensation']),
        'scc_ordered_pair_path_checks': data['path_checks'],
        'terminal_tie_space_rank': terminal_rank, 'all_tree_scc_image_rank': scc_rank,
        'new_cycle1_rows': cycle1, 'new_cycle2_rows': cycle2,
        'boundary_cases': boundary_cases,
        'rows': [{'history': h, 'deviation': a, 'coefficients': list(map(str, row)),
                  'slack': str(slacks[h, a])} for (h, a), row in rows.items()],
        'limits': 'SCC image need not exhaust mapped cone lineality; no universal half certificate constructed.',
    }
    text = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        with args.output.open('x', encoding='utf-8') as handle:
            handle.write(text + '\n')
    print(text)


if __name__ == '__main__':
    main()
