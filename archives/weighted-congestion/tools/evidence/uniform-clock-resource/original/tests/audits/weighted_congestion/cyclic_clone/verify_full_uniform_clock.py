"""Exact independent literal reconstruction of the fixed full uniform clock.

The input is the canonical degree-43 fixture's BASE ONLY. Its clocks are ignored.
We instead add all three anchored pairs, common amplitude M=2 alpha B, degree 80.
No repository audit implementation or output is imported. This is a fixed
instance certificate, not a degree optimum or an asymptotic lower bound.
"""
from fractions import Fraction as Q
from itertools import product, combinations
from pathlib import Path
import argparse
import hashlib
import json
import platform
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo', type=Path, default=None,
                    help='repository root; by default inferred from canonical audit location')
parser.add_argument('--output', type=Path, default=None,
                    help='new output path; created exclusively and never overwritten')
args = parser.parse_args()
REPO = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[4]
INPUT = REPO / 'examples/weighted_congestion/anchored_actual_clock_degree43.json'
data = json.loads(INPUT.read_text())
weights = list(map(Q, data['weights']))
alpha = Q(data['alpha'])
n = len(weights)
assert weights == [Q(1), Q(1, 2), Q(1, 4), Q(1, 8)]
assert alpha == Q(21, 20)

# Pair literal: (action-zero resource index for each participant,
#                coefficient, nonnegative integral degree).
base = []
for entry in data['base_pairs']:
    incidence = [(i, 0 if sign == 1 else 1)
                 for i, sign in enumerate(entry['signature']) if sign]
    base.append((incidence, Q(entry['coefficient']), int(entry['degree'])))
assert len(base) == 4 and all(k == 3 for ids, c, k in base)


def cost(resources, state, player):
    answer = Q(0)
    for incidence, coefficient, degree in resources:
        own_resource = [state[i] ^ bit for i, bit in incidence if i == player]
        if not own_resource:
            continue
        assert len(own_resource) == 1
        load = sum((weights[i] for i, bit in incidence
                    if state[i] ^ bit == own_resource[0]), Q(0))
        answer += coefficient * load ** degree
    return answer


def margin(resources, state, player):
    after = list(state)
    after[player] ^= 1
    return cost(resources, state, player) - alpha * cost(resources, after, player)


states = list(product((0, 1), repeat=n))
ring = {}
state = [0] * n
for turn in range(2 * n):
    player = turn % n
    ring[tuple(state)] = player
    state[player] ^= 1
assert state == [0] * n and len(ring) == 2 * n
base_bound = max(cost(base, s, i) for s in states for i in range(n))
base_minimum = min(margin(base, s, i) for s, i in ring.items())
assert base_bound == Q(56643761, 70312500)
assert base_minimum == Q(49676111, 6750000000)
amplitude = 2 * alpha * base_bound
assert amplitude == Q(396506327, 234375000)
degree = 80
clocks = []
clock_descriptions = []
for i, j in combinations(range(1, n), 2):
    full_load = weights[0] + weights[i] + weights[j]
    coefficient = amplitude / full_load ** degree
    clocks.append(([(0, 0), (i, 1), (j, 0)], coefficient, degree))
    clock_descriptions.append({'players': [0, i, j], 'target': [0, 1, 0],
                               'full_load': str(full_load),
                               'amplitude': str(amplitude), 'degree': degree,
                               'coefficient': str(coefficient)})
assert len(clocks) == 3
resources = base + clocks
rows = []
complement_cost_checks = 0
for s in states:
    legal = s in ring
    if legal:
        player = ring[s]
    else:
        player = next(i for i in range(1, n) if s[i] != s[0])
        assert any(s[j] == s[0] for j in range(player + 1, n))
    base_margin = margin(base, s, player)
    clock_margin = margin(clocks, s, player)
    combined_margin = margin(resources, s, player)
    assert combined_margin == base_margin + clock_margin
    assert combined_margin > 0
    complement = tuple(1 - bit for bit in s)
    all_margins = [margin(resources, s, i) for i in range(n)]
    assert all(margin(resources, complement, i) == value
               for i, value in enumerate(all_margins))
    after = list(s)
    after[player] ^= 1
    current_base = cost(base, s, player)
    after_base = cost(base, after, player)
    current_clock = cost(clocks, s, player)
    after_clock = cost(clocks, after, player)
    current_total = cost(resources, s, player)
    after_total = cost(resources, after, player)
    assert current_total == current_base + current_clock
    assert after_total == after_base + after_clock
    assert combined_margin == current_total - alpha * after_total
    all_player_costs = []
    for i in range(n):
        other = list(s)
        other[i] ^= 1
        complemented_after = tuple(1 - bit for bit in other)
        current = cost(resources, s, i)
        post = cost(resources, other, i)
        assert current == cost(resources, complement, i)
        assert post == cost(resources, complemented_after, i)
        complement_cost_checks += 1
        all_player_costs.append({'player': i, 'current': str(current),
                                 'post': str(post),
                                 'margin': str(current - alpha * post)})
    rows.append({'state': ''.join(map(str, s)),
                 'kind': 'legal_ring' if legal else 'illegal_first_opposite',
                 'player': player,
                 'post_state': ''.join(map(str, after)),
                 'base_current': str(current_base), 'base_post': str(after_base),
                 'clock_current': str(current_clock), 'clock_post': str(after_clock),
                 'total_current': str(current_total), 'total_post': str(after_total),
                 'base_margin': str(base_margin),
                 'clock_margin': str(clock_margin),
                 'combined_margin': str(combined_margin),
                 'all_player_costs_and_margins': all_player_costs})
assert sum(row['kind'] == 'legal_ring' for row in rows) == 8
minimum = min(Q(row['combined_margin']) for row in rows)
assert minimum > Q(1, 500)

number_of_pairs = len(clocks)
delta = max(1 - min(weights[0], weights[i], weights[j]) /
            (weights[0] + weights[i] + weights[j])
            for i, j in combinations(range(1, n), 2))
threshold = base_minimum / (4 * alpha ** 2 * base_bound * number_of_pairs)
assert delta == Q(12, 13)
assert delta ** degree > threshold
assert delta ** 91 <= threshold < delta ** 90
budget_degree = 0
while delta ** budget_degree > threshold:
    budget_degree += 1
assert budget_degree == 91
assert complement_cost_checks == 64
result = {
    'scope': 'fixed four-player full anchored uniform clock certificate only',
    'input': str(INPUT.relative_to(REPO)),
    'input_sha256': hashlib.sha256(INPUT.read_bytes()).hexdigest(),
    'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'python': platform.python_version(), 'arithmetic': 'Fraction exact',
    'seed': None, 'command': ' '.join(sys.argv),
    'weights': list(map(str, weights)), 'alpha': str(alpha),
    'base_B': str(base_bound), 'base_eta': str(base_minimum),
    'amplitude_M': str(amplitude), 'degree': degree,
    'clock_pairs': clock_descriptions,
    'all_states': rows, 'minimum_selected_margin': str(minimum),
    'minimum_selected_margin_strictly_above': '1/500',
    'minimum_margin_states': [row['state'] for row in rows
                              if Q(row['combined_margin']) == minimum],
    'uniform_budget': {'delta': str(delta), 'L': number_of_pairs,
                       'threshold': str(threshold),
                       'delta_power_80': str(delta ** degree),
                       'delta_power_91': str(delta ** 91),
                       'delta_power_90': str(delta ** 90),
                       'budget_fails_at_degree_80': True,
                       'budget_minimum_integer_degree': budget_degree},
    'coverage': {'all_state_count': len(states), 'legal_state_count': len(ring),
                 'illegal_state_count': len(states) - len(ring),
                 'complement_cost_and_margin_checks': complement_cost_checks,
                 'selected_deviations_all_strict': True,
                 'contains_no_alpha_PNE': True,
                 'degree_optimality_claimed': False},
    'result': 'PASS: all 16 states have a specified strict 21/20 improvement; (U) fails',
}
output_text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
if args.output:
    with args.output.open('x') as stream:
        stream.write(output_text)
    print(json.dumps({'output': str(args.output), 'result': result['result']},
                     ensure_ascii=False))
else:
    print(output_text, end='')
