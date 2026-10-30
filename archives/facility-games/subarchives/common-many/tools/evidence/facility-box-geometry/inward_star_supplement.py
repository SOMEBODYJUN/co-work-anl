#!/usr/bin/env python3
"""Independent finite checks of the repaired inward-star queue invariant."""
import argparse
import ast
from fractions import Fraction as F
import hashlib
from itertools import combinations_with_replacement, product
import json
from pathlib import Path


def star(gamma, r, center, leaves):
    # Each leaf is (q, initial total, individually named weights).
    gamma, C = F(gamma), F(center)
    q = [v[0] for v in leaves]
    A = [F(v[1]) for v in leaves]
    queues = [sorted(map(F, v[2]), reverse=True) for v in leaves]
    assert r >= 1 and r * gamma <= C <= (r + 1) * gamma
    assert all(h >= r and h * gamma <= a <= (h + 1) * gamma
               for h, a in zip(q, A))
    assert all(0 < w < gamma for row in queues for w in row)
    assert all(a >= sum(row) for a, row in zip(A, queues))
    clients = [(l, j, w) for l, row in enumerate(queues) for j, w in enumerate(row)]
    next_index = [0] * len(leaves)
    moved = set()
    old_keys = {}
    previous = None
    trace = []
    old_key_threshold_falls = []
    while any(next_index[l] < len(queues[l]) for l in range(len(leaves))):
        heads = []
        for l in range(len(leaves)):
            j = next_index[l]
            if j < len(queues[l]):
                w = queues[l][j]
                heads.append((r * (A[l] - w) / q[l] + w, -l, l, j, w))
        U, _, l, j, w = max(heads)
        assert previous is None or U <= previous
        previous = U
        before = C
        improving = r * (A[l] - w) / q[l] > C
        if improving:
            A[l] -= w
            C += w
            moved.add((l, j))
            old_keys[(l, j)] = U
            assert C == before + w and C < U
        next_index[l] += 1
        assert r * gamma <= C <= (r + 1) * gamma
        assert all(h * gamma <= a <= (h + 1) * gamma for h, a in zip(q, A))
        for ml, mj, mw in clients:
            if (ml, mj) in moved:
                threshold = r * A[ml] / q[ml] + mw
                assert threshold >= U and C < threshold
                if threshold < old_keys[(ml, mj)]:
                    old_key_threshold_falls.append({'client': [ml, mj],
                                                   'old_entry_key': str(old_keys[(ml, mj)]),
                                                   'current_threshold': str(threshold)})
        trace.append({'leaf': l, 'client_index': j, 'weight': str(w),
                      'popped_key': str(U), 'moved': improving,
                      'center_before': str(before), 'center_after': str(C)})
    for l, j, w in clients:
        if (l, j) in moved:
            assert (C - w) * q[l] <= r * A[l]
        else:
            assert r * (A[l] - w) <= C * q[l]
    return {'trace': trace, 'center_final': str(C),
            'leaf_totals_final': list(map(str, A)), 'moves': len(moved),
            'old_entry_key_bound_failures': old_key_threshold_falls}


def family(n):
    G = n ** 3
    # Literal original-model clients, not a precomputed abstract star.
    count = n + 2
    weights, options = [], []
    for j in range(1, n + 1):
        weights += [F(3 * G - 2 * j), F(j)]
        options += [(j - 1,), (j - 1, n)]
    weights += [F(G + 1), F(G)]
    options += [(n,), (n + 1,)]
    a = [-1] * len(weights)
    q = [0] * count
    initial = [F(0)] * count
    trace = []
    for _ in range(2 * n + 2):
        scores = [initial[t] / (q[t] + 1) if q[t] else
                  sum((w for w, opts, home in zip(weights, options, a)
                       if home < 0 and t in opts), F(0)) for t in range(count)]
        best = max(scores)
        winners = [t for t, v in enumerate(scores) if v == best]
        assert len(winners) == 1
        t = winners[0]
        if not q[t]:
            for i, opts in enumerate(options):
                if a[i] < 0 and t in opts:
                    a[i] = t
                    initial[t] += weights[i]
        q[t] += 1
        trace.append([t, str(best)])
    assert q == [2] * n + [1, 1] and F(trace[-1][1]) == G
    assert [t for t, _ in trace] == list(range(n)) * 2 + [n, n + 1]
    result = star(G, 1, G + 1,
                  [(2, 3 * G - j, [j]) for j in range(1, n + 1)])
    assert result['moves'] == n
    assert F(result['center_final']) == G + 1 + F(n * (n + 1), 2) < F(3 * G, 2)
    assert list(map(F, result['leaf_totals_final'])) == [3 * G - 2 * j for j in range(1, n + 1)]
    return {'n': n, 'gamma': G, 'greedy_trace': trace,
            'initial_totals': list(map(str, initial)), 'queue_result': result}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--original', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert not args.output.exists(), 'Refuse to overwrite evidence'
    # The hard-coded height audit never reads its JSON; bridge that identity.
    script = args.original / 'tests/audits/kfac_height_two.py'
    constants = {}
    for node in ast.parse(script.read_text()).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id in {'SITES', 'K', 'CLIENTS'}:
                constants[node.targets[0].id] = ast.literal_eval(node.value)
    fixture = args.original / 'examples/multi_facility/greedy_height_two_unequal.json'
    data = json.loads(fixture.read_text())
    assert data['k'] == constants['K'] and tuple(data['sites']) == constants['SITES']
    literal = tuple((row['weight'], tuple(data['sites'].index(t) for t in row['sites']))
                    for row in data['clients'])
    assert literal == constants['CLIENTS']
    rows = []
    for q in (1, 2):
        for length in (1, 2):
            for ws in combinations_with_replacement((1, 3), length):
                for total in (4 * q, 4 * (q + 1)):
                    if sum(ws) <= total:
                        rows.append((q, total, ws))
    cases = decisions = moves = 0
    for leaves in product(rows, repeat=2):
        for center in (4, 6, 8):
            result = star(4, 1, center, leaves)
            cases += 1
            decisions += len(result['trace'])
            moves += result['moves']
    for leaves in product(((q, a, [w]) for q in (1, 2)
                           for a in (4 * q, 4 * (q + 1)) for w in (1, 3)), repeat=3):
        for center in (4, 6, 8):
            result = star(4, 1, center, leaves)
            cases += 1
            decisions += len(result['trace'])
            moves += result['moves']
    correction = star(11, 1, 11, [(2, 32, [2, 1])])
    assert correction['old_entry_key_bound_failures'] == [
        {'client': [0, 0], 'old_entry_key': '17', 'current_threshold': '33/2'}]
    report = {'scope': 'Finite independent queue and literal family checks; not a universal proof or original author audit.',
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'height_fixture_matches_hardcoded_author_clients': True,
              'height_fixture_sha256': hashlib.sha256(fixture.read_bytes()).hexdigest(),
              'finite_grid': {'gamma': 4, 'center_q': 1, 'cases': cases,
                              'decisions': decisions, 'strict_moves': moves,
                              'invariants': ['nonincreasing popped keys', 'all full boxes',
                                             'center thresholds >= most recently popped key', 'all final true NE comparisons']},
              'false_stronger_old_key_invariant': correction,
              'genuine_greedy_families': [family(n) for n in range(3, 13)]}
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'cases': cases, 'decisions': decisions, 'strict_moves': moves,
                      'genuine_family_n': [3, 12], 'corrected_invariants': 'all passed'}))


if __name__ == '__main__':
    main()
