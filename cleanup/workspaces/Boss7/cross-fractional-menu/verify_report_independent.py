#!/usr/bin/env python3
"""Verify every frozen report field from the separate input and full policy.

No import of the original audit, canonical payoff code, or SPE outcome solver.
Payoffs use the input's 18 compressed unit-customer types, independently of the
original audit's combinations-based construction of 36 unit records.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
report = json.loads((HERE / 'original/fractional_root_menu_audit.json').read_text())
instance = json.loads((HERE / 'original/aggregate_theta_input.json').read_text())
certificate = json.loads((HERE / 'original/aggregate_theta_strategy.json').read_text())
policy = {tuple(row['history']): row['action'] for row in certificate['strategy']['actions']}
types = {frozenset(row['topics']): row['multiplicity'] for row in instance['customers']}
k, n = len(instance['topics']), instance['players']
histories = [h for d in range(n) for h in product(range(k), repeat=d)]
assert set(policy) == set(histories) and len(policy) == 43
assert n == 3 and k == 6 and len(types) == 18 and sum(types.values()) == 36
assert all((len(C) == 2 and len(C & {0, 1, 2}) == 1 and w == 1) or
           (len(C) == 4 and len(C & {0, 1, 2}) == 2 and w == 3)
           for C, w in types.items())
for h in histories:
    expected_action = (0 if not h else (3 if h[0] < 3 else 0) if len(h) == 1
                       else min(a for a in (range(3) if h[1] < 3 else range(3, 6)) if a not in h))
    assert policy[h] == expected_action


def finish(h):
    while len(h) < n:
        h = h + (policy[h],)
    return h


def payoff(h, position):
    action = h[position]
    return sum((F(w, sum(t in C for t in h)) for C, w in types.items()
                if action in C), F(0))


def welfare(h):
    return sum(w for C, w in types.items() if C.intersection(h))


def query(load, action, size=None):
    return sum((F(w) / (1 + sum((load[t] for t in C), F(0)))
                for C, w in types.items() if action in C and (size is None or len(C) == size)), F(0))


all_terminals = list(product(range(k), repeat=n))
assert len(all_terminals) == 216
assert all(sum((payoff(h, i) for i in range(n)), F(0)) == welfare(h) for h in all_terminals)
gaps, ic_rows = [], []
for h in histories:
    prescribed = finish(h)
    u = payoff(prescribed, len(h))
    for action in range(k):
        deviation = finish(h + (action,))
        gap = u - payoff(deviation, len(h))
        gaps.append(gap)
        ic_rows.append({'history': list(h), 'action': action, 'prescribed_leaf': list(prescribed),
                        'deviation_leaf': list(deviation), 'gap': str(gap)})
assert min(gaps) >= 0
path = finish(())
root = payoff(path, 0)
payoffs = [payoff(path, i) for i in range(n)]
assert [sum(t == a for t in path) for a in range(k)] == certificate['strategy']['terminal_counts']
menus = sorted({finish((a,))[1:] for a in range(k)})
midpoint = [F(1, 2), F(1, 2), F(0), F(1, 2), F(1, 2), F(0)]
mid = [query(midpoint, a) for a in range(k)]
free = [query([F(1, 3)] * k, a) for a in range(k)]

# Finite certificates for the analytic convexity and exchange argument.
swapped_types = {frozenset((t + 3) % 6 for t in C): w for C, w in types.items()}
assert swapped_types == types
curvatures = []
for C, w in types.items():
    slope = len(C & {0, 1}) - len(C & {3, 4})
    intercept = 1 + len(C & {3, 4})
    assert min(intercept, intercept + slope) >= 1
    numerator = 2 * w * slope * slope
    assert numerator >= 0
    curvatures.append({'type': sorted(C), 'multiplicity': w, 'denominator_intercept': intercept,
                       'denominator_slope': slope, 'second_derivative_numerator': numerator})

scope = ('Only a restricted-menu fractional leader-cap failure. FF-LEADER, extra-mass leader, '
         'aggregate security and Q-CAG-HALF remain OPEN.')
expected = {
    'status': 'PASS', 'players': n, 'topics': k, 'unit_customers': sum(types.values()),
    'complete_ordered_histories': len(histories), 'comparisons_including_self': len(gaps),
    'minimum_spe_gap': str(min(gaps)), 'path': list(path), 'payoffs': list(map(str, payoffs)),
    'root_tail_menu': [list(x) for x in menus], 'fractional_menu_midpoint_values': list(map(str, mid)),
    'fractional_menu_minmax': str(max(mid)), 'root_utility': str(root),
    'strict_menu_gap': str(max(mid) - root), 'free_fractional_values': list(map(str, free)),
    'scope': scope,
}
assert set(expected) == set(report) and len(report) == 16
assert expected == report

# Different comparison objects, for the report's scope and interpretation.
menu_matrix = []
for a in range(k):
    menu_matrix.append([str(query([F(b in tail) for b in range(k)], a)) for tail in menus])
competitor_pairs = list(product(range(k), repeat=2))
uniform_query_values = []
for pair in competitor_pairs:
    load = [F(sum(t == a for t in pair)) for a in range(k)]
    uniform_query_values.append(sum((query(load, a) for a in range(k)), F(0)) / k)
dual_pairs = [pair for group in [(0, 1, 2), (3, 4, 5)] for pair in combinations(group, 2)]
dual_values = []
for a in range(k):
    dual_values.append(sum((query([F(t in pair) for t in range(k)], a)
                            for pair in dual_pairs), F(0)) / len(dual_pairs))
assert min(uniform_query_values) == 10 and dual_values == [F(10)] * 6
assert welfare(path) == 34 and max(map(welfare, all_terminals)) == 36

result = {
    'status': 'PASS', 'scope': 'all 16 report fields from separate frozen input/policy; no general welfare inference',
    'checked_fields': list(report), 'derived_report': expected,
    'ordered_terminal_count': len(all_terminals), 'checked_histories': len(histories),
    'self_comparisons': len(histories), 'nonself_comparisons': len(gaps) - len(histories),
    'zero_gaps': sum(x == 0 for x in gaps), 'positive_gaps': sum(x > 0 for x in gaps),
    'minimum_positive_gap': str(min(x for x in gaps if x > 0)),
    'actual_welfare': welfare(path), 'optimum_welfare': max(map(welfare, all_terminals)),
    'policy_matches_described_group_rule_at_all_histories': True,
    'integer_true_tail_menu_query_matrix': menu_matrix,
    'midpoint_pair_and_quad_contributions': [[str(query(midpoint, a, size)) for size in [2, 4]] for a in range(k)],
    'convexity_coefficient_records': curvatures,
    'group_exchange_preserves_input': True,
    'continuous_minmax_basis': 'analytic convexity plus lambda-to-one-minus-lambda symmetry; no parameter grid or optimizer',
    'integer_static_safety_primal_uniform_query_floor': str(min(uniform_query_values)),
    'integer_static_safety_dual_each_query': list(map(str, dual_values)),
    'scope_string_is_historical_not_current_open_status': True,
}
(HERE / 'replay/independent-field-audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
(HERE / 'replay/independent-ic-table.json').write_text(json.dumps(ic_rows, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({key: result[key] for key in [
    'status', 'checked_fields', 'ordered_terminal_count', 'checked_histories', 'self_comparisons',
    'nonself_comparisons', 'zero_gaps', 'positive_gaps', 'minimum_positive_gap',
    'actual_welfare', 'optimum_welfare', 'integer_static_safety_primal_uniform_query_floor']}, indent=2))
