"""Check all states of the pure-menu SPE DAG using only exact raw shares.

This file does not import the canonical model, solver, or certificate verifier.
Every edge is an available action, and every local inequality follows the edge's
actual descendant target.  Thus backward induction checks the entire unfolding.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input', type=Path, default=Path(__file__).with_name('pure_menu_two_block_dag.json'))
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    path = args.input
    raw = json.loads(path.read_text())
    assert raw['schema'] == 'CA_COMPLETE_SPE_DAG_v1'
    inst, nodes = raw['instance'], raw['nodes']
    p, m = len(inst['topics']), inst['players']
    types = [(set(c['topics']), c['multiplicity']) for c in inst['customers']]
    customers = [likes for likes, number in types for _ in range(number)]
    assert m == p == 8 and len(customers) == 32

    def utility(action, q, extra=False):
        return sum((Fraction(1, int(extra) + sum(q[a] for a in likes))
                    for likes in customers if action in likes), Fraction())

    def welfare(q):
        return sum(any(q[a] for a in likes) for likes in customers)

    seen = set()
    comparisons = 0
    strict, equal = 0, 0
    minimum = None

    def check(identity):
        nonlocal comparisons, strict, equal, minimum
        if identity in seen:
            return
        assert isinstance(identity, int) and 0 <= identity < len(nodes)
        seen.add(identity)
        node = nodes[identity]
        q, target = tuple(node['counts']), tuple(node['target'])
        assert len(q) == len(target) == p
        assert all(isinstance(v, int) and v >= 0 for v in q + target)
        assert sum(q) <= m and sum(target) == m
        assert all(a <= b for a, b in zip(q, target))
        if sum(q) == m:
            assert q == target and node['action'] is None and node['children'] == []
            return
        action = node['action']
        assert isinstance(action, int) and 0 <= action < p
        children = node['children']
        assert len(children) == p
        assert tuple(nodes[children[action]]['target']) == target
        actual = utility(action, target)
        for alternative, child_id in enumerate(children):
            child = nodes[child_id]
            expected = tuple(c + int(a == alternative) for a, c in enumerate(q))
            assert tuple(child['counts']) == expected
            check(child_id)
            gain = actual - utility(alternative, tuple(child['target']))
            assert gain >= 0, (identity, alternative, gain)
            comparisons += 1
            strict += gain > 0
            equal += gain == 0
            minimum = gain if minimum is None else min(minimum, gain)

    check(raw['root'])
    assert len(seen) == len(nodes)
    root = nodes[raw['root']]
    assert root['counts'] == [0] * 8 and root['action'] == 3
    columns = [tuple(nodes[identity]['target']) for identity in root['children']]
    assert columns == [tuple(q) for q in raw['root_columns']]
    u = utility(root['action'], tuple(root['target']))
    assert u == Fraction(13, 4)
    matrix = [[utility(a, q, extra=True) for q in columns] for a in range(p)]
    for b in range(p):
        assert matrix[7 if b < 4 else 3][b] == Fraction(37, 10) > u
    mixed = [sum((matrix[a][b] for b in (3, 7)), Fraction()) / 2 for a in range(p)]
    assert max(mixed) == Fraction(123, 40) < u
    q = tuple(root['target'])
    assert welfare(q) == 32
    optimum = max(welfare(tuple(int(a in support) for a in range(p)))
                  for size in range(min(m, p) + 1) for support in combinations(range(p), size))
    assert optimum == 32
    actual_path = []
    current = raw['root']
    while nodes[current]['action'] is not None:
        a = nodes[current]['action']
        actual_path.append(a)
        current = nodes[current]['children'][a]
    assert tuple(actual_path.count(a) for a in range(p)) == q
    output = {'nodes': len(nodes), 'terminal_nodes': sum(n['action'] is None for n in nodes),
              'comparisons_including_self': comparisons, 'strict': strict, 'equal': equal,
              'minimum_slack': str(minimum), 'root_utility': str(u),
              'actual_path': actual_path, 'actual_terminal_counts': list(q),
              'actual_payoffs': [str(utility(a, q)) for a in actual_path],
              'welfare': 32, 'optimum': 32,
              'root_column_own_utilities': [str(utility(b, columns[b])) for b in range(p)],
              'extra_query_matrix_rows_queries_columns_root_actions':
                  [[str(v) for v in row] for row in matrix],
              'uniform_D_column_mixture_query_values': [str(v) for v in mixed],
              'pure_menu_blocker_refuted': True, 'mixed_menu_blocker_refuted': False,
              'half_coverage_refuted': False}
    if args.output:
        with args.output.open('x') as stream:
            json.dump(output, stream, indent=2)
            stream.write('\n')
    print(json.dumps(output))


if __name__ == '__main__':
    main()
