#!/usr/bin/env python3
"""Enumerate every two-player tail BR map from expanded unit customers.

The Fraction calculation below imports neither the probe nor canonical payoff
or solver code. A final, separate comparison invokes the frozen solver.
"""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
data = json.loads((HERE / 'original/background_welfare_nonmonotone.json').read_text())
raw = data['instance']
units = [frozenset(t['topics']) for t in raw['customers']
         for _ in range(t['multiplicity'])]
k = len(raw['topics'])
assert k == 4 and data['r'] == 2 and len(units) == 13


def terminal(base, first, last):
    c = list(base)
    c[first] += 1
    c[last] += 1
    return tuple(c)


def payoff(c, action):
    return sum((F(1, sum(c[t] for t in unit))
                for unit in units if action in unit), F(0))


def welfare(c):
    return sum(any(c[t] for t in unit) for unit in units)


def all_tail_spes(base):
    last_values = [[payoff(terminal(base, a, b), b) for b in range(k)]
                   for a in range(k)]
    br = [tuple(b for b in range(k) if row[b] == max(row))
          for row in last_values]
    witnesses = {}
    map_count = 0
    strategy_count = 0
    for replies in product(*br):
        map_count += 1
        first_values = [payoff(terminal(base, a, replies[a]), a) for a in range(k)]
        for first in range(k):
            if first_values[first] != max(first_values):
                continue
            strategy_count += 1
            c = terminal(base, first, replies[first])
            witnesses.setdefault(c, {'first_action': first, 'last_replies_by_first_action': list(replies)})
    worst = min((welfare(c), c) for c in witnesses)
    witness = witnesses[worst[1]]
    first = witness['first_action']
    replies = witness['last_replies_by_first_action']
    first_values = [payoff(terminal(base, a, replies[a]), a) for a in range(k)]
    differences = []
    for a in range(k):
        for b in range(k):
            differences.append(last_values[a][replies[a]] - last_values[a][b])
    differences += [first_values[first] - value for value in first_values]
    assert len(differences) == 20 and min(differences) >= 0
    return {
        'base': list(base), 'remaining_players': 2, 'total_players': sum(base) + 2,
        'all_outcomes': [list(c) for c in sorted(witnesses)],
        'outcome_welfare': [{'counts': list(c), 'welfare': welfare(c)} for c in sorted(witnesses)],
        'last_best_reply_sets_by_first_action': [list(x) for x in br],
        'last_payoff_matrix_by_first_action': [[str(x) for x in row] for row in last_values],
        'follower_best_reply_maps_enumerated': map_count,
        'complete_pure_tail_spes_including_root_ties': strategy_count,
        'lexicographic_worst': [worst[0], list(worst[1])],
        'worst_witness': witness,
        'first_payoffs_under_witness_replies': [str(x) for x in first_values],
        'witness_checked_decision_histories': 5,
        'witness_checked_action_comparisons_including_self': 20,
        'witness_minimum_incentive_difference': str(min(differences)),
        'witness_tail_path': [first, replies[first]],
    }


base = tuple(data['base'])
added = tuple(v + int(i == data['add']) for i, v in enumerate(base))
old = all_tail_spes(base)
new = all_tail_spes(added)
assert old['all_outcomes'] == [[1, 1, 1, 0]]
assert new['all_outcomes'] == [[2, 1, 0, 1], [2, 1, 1, 0]]
assert old['lexicographic_worst'] == data['original']
assert new['lexicographic_worst'] == data['added']

optima = {}
for players in [3, 4]:
    best = 0
    for size in range(min(k, players) + 1):
        for support in combinations(range(k), size):
            best = max(best, welfare(tuple(int(a in support) for a in range(k))))
    optima[str(players)] = best
assert optima == {'3': 13, '4': 13}

# Compare, after the independent values and outcome sets have been established.
sys.path.insert(0, str(HERE / 'original'))
from customer_attraction import Instance, ExactSPESolver
canonical = []
for report in [old, new]:
    inst = dict(raw, players=report['total_players'])
    obj = Instance.from_dict(inst)
    outcomes = sorted(ExactSPESolver(obj).outcomes(tuple(report['base'])))
    assert [list(c) for c in outcomes] == report['all_outcomes']
    assert min((obj.welfare(c), c) for c in outcomes) == (
        report['lexicographic_worst'][0], tuple(report['lexicographic_worst'][1]))
    canonical.append({'total_players': obj.players, 'outcome_sets_equal': True})

result = {'scope': 'all complete pure two-player tail strategies in two fixed legal backgrounds; no full root SPE claimed',
          'unit_customers': len(units), 'original_background': old, 'added_background': new,
          'optimum_complete_coverage': optima, 'canonical_comparison': canonical}
(HERE / 'replay/independent-unit-tail-audit.json').write_text(
    json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
