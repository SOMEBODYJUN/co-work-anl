"""Fixed cubic base: exact audit of unavoidable actual ring-margin dependence.

The proof is the coefficient-cone inequality in the accompanying note. This
finite exact audit does not enumerate arbitrary polynomial coefficients or D.
Only the canonical input JSON's BASE is read; its degree-43 clocks are ignored.
The alpha=1 boundary is excluded; this certificate fixes alpha=21/20.
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
parser.add_argument('--repo', type=Path, default=None)
parser.add_argument('--output', type=Path, default=None)
args = parser.parse_args()
repo = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[4]
source = repo / 'examples/weighted_congestion/anchored_actual_clock_degree43.json'
data = json.loads(source.read_text())
weights = list(map(Q, data['weights']))
alpha = Q(data['alpha'])
assert weights == [Q(1), Q(1, 2), Q(1, 4), Q(1, 8)]
assert alpha == Q(21, 20)
n = len(weights)

# A literal SINGLE resource is (per-player action sets, coefficient, degree).
# Canonical padding uses two different private resources, one on each action.
def resource_pair(participants, coefficient, degree):
    return [({i: {bit ^ side} for i, bit in participants}, coefficient, degree)
            for side in range(2)]


base = []
for entry in data['base_pairs']:
    participants = [(i, 0 if sign == 1 else 1)
                    for i, sign in enumerate(entry['signature']) if sign]
    base += resource_pair(participants, Q(entry['coefficient']), entry['degree'])
assert len(base) == 8


def cost(resources, state, player):
    result = Q(0)
    for users, coefficient, degree in resources:
        if player not in users or state[player] not in users[player]:
            continue
        load = sum((weights[i] for i, actions in users.items()
                    if state[i] in actions), Q(0))
        assert load >= weights[player] > 0
        result += coefficient * load ** degree
    return result


def margin(resources, state, player):
    after = list(state)
    after[player] ^= 1
    return cost(resources, state, player) - alpha * cost(resources, after, player)


states = list(product((0, 1), repeat=n))
ring = []
state = [0] * n
for turn in range(2 * n):
    player = turn % n
    ring.append((tuple(state), player))
    state[player] ^= 1
assert state == [0] * n
gamma = [min(margin(base, s, i) for s, j in ring if j == i) for i in range(n)]
assert gamma == [Q(55201793, 7500000000), Q(1725121, 234375000),
                 Q(248398189, 33750000000), Q(49676111, 6750000000)]
assert all(margin(base, s, i) == gamma[i] for s, i in ring)
b = (0, 1, 0, 1)
K = [-margin(base, b, i) for i in range(n)]
assert K == [Q(122240519, 625000000), Q(17706129787, 33750000000),
             Q(234206903, 312500000), Q(1009308211, 6750000000)]
eta = min(gamma)
Kmin = min(K)
assert eta > 0 and Kmin > 0
assert Kmin / 160 < eta / 2
degrees = [0, 1, 2, 3, 7, 20, 80, 100]
rows = []
column_checks = 0
complement_checks = 0
for D in degrees:
    ratio_bound = Q(3, 2) ** D
    epsilon = min(eta / 2, (alpha - 1) * Kmin / (8 * ratio_bound))
    assert epsilon == Kmin / (160 * ratio_bound)
    private_costs = [(gamma[i] - epsilon) / (alpha - 1) for i in range(n)]
    assert all(t > 0 for t in private_costs)
    common_private = [({i: {0, 1}}, private_costs[i] / weights[i] ** 3, 3)
                      for i in range(n)]
    private = [({i: {act}}, private_costs[i] / weights[i] ** 3, 3)
               for i in range(n) for act in (0, 1)]
    padded = base + private
    assert len(base) == 8 and len(private) == 8 and len(padded) == 16
    assert all(coefficient > 0 and degree == 3 for users, coefficient, degree in padded)
    for s in states:
        complement = tuple(1 - bit for bit in s)
        for i in range(n):
            assert cost(private, s, i) == private_costs[i]
            assert cost(common_private, s, i) == cost(private, s, i)
            assert cost(padded, s, i) == cost(base, s, i) + private_costs[i]
            assert cost(padded, s, i) == cost(base+common_private, s, i)
            assert margin(padded, s, i) == margin(base+common_private, s, i)
            assert cost(padded, s, i) == cost(padded, complement, i)
            assert margin(padded, s, i) == margin(padded, complement, i)
            complement_checks += 1
    for i in range(n):
        action_resources = [set(k for k, (users, coef, deg) in enumerate(padded)
                                if i in users and act in users[i]) for act in (0, 1)]
        assert action_resources[0] and action_resources[1]
        assert not action_resources[0].intersection(action_resources[1])
        assert not action_resources[0] <= action_resources[1]
        assert not action_resources[1] <= action_resources[0]
    padded_ring = [margin(padded, s, i) for s, i in ring]
    assert padded_ring == [epsilon] * 8
    Kp = [-margin(padded, b, i) for i in range(n)]
    assert Kp == [K[i] + gamma[i] - epsilon for i in range(n)]
    assert all(gap > Kmin for gap in Kp)
    budget_cap = 4 * epsilon / (alpha - 1)
    clock_margin_cap = ratio_bound * budget_cap
    assert clock_margin_cap <= Kmin / 2
    kappas = [Q(0)] * n
    minimum_m_over_W = Q(1)
    for i, j in combinations(range(1, n), 2):
        ids = [(0, 0), (i, 1), (j, 0)]
        W = weights[0] + weights[i] + weights[j]
        pairloads = [weights[0] + weights[i], weights[0] + weights[j],
                     weights[i] + weights[j]]
        m = max(pairloads)
        assert 3 * m >= 2 * W
        minimum_m_over_W = min(minimum_m_over_W, m / W)
        for k in range(D + 1):
            clock_column = resource_pair(ids, Q(1), k)
            S = sum((load ** k for load in pairloads), Q(0))
            ring_g = [margin(clock_column, ring[h][0], h) for h in range(n)]
            assert sum(ring_g, Q(0)) == -(alpha - 1) * S
            for player in (0, i, j):
                value = margin(clock_column, b, player) / S
                assert value <= ratio_bound
                kappas[player] = max(kappas[player], value)
                column_checks += 1
    assert minimum_m_over_W == Q(6, 7)
    assert all(kappa * budget_cap <= clock_margin_cap for kappa in kappas)
    assert all(gap - clock_margin_cap > Kmin / 2 for gap in Kp)
    rows.append({'D': D, 'coarse_efficiency_Q': str(ratio_bound),
                 'epsilon': str(epsilon), 'private_costs': list(map(str, private_costs)),
                 'private_cubic_coefficients_by_player':
                     [str(private_costs[i]/weights[i]**3) for i in range(n)],
                 'padded_ring_margins': list(map(str, padded_ring)),
                 'padded_b_stability_gaps': list(map(str, Kp)),
                 'actual_kappas_b': list(map(str, kappas)),
                 'strict_total_S_budget_cap': str(budget_cap),
                 'strict_clock_margin_cap': str(clock_margin_cap),
                 'all_total_margins_strictly_below': str(-Kmin / 2)})
result = {'scope': 'fixed cubic base, fixed alpha; finite audit of general padding proof',
          'input': str(source.relative_to(repo)),
          'input_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
          'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'python': platform.python_version(), 'command': ' '.join(sys.argv),
          'arithmetic': 'fractions.Fraction exact', 'seed': None,
          'weights': list(map(str, weights)), 'alpha': str(alpha),
          'gamma': list(map(str, gamma)), 'base_K': list(map(str, K)),
          'eta': str(eta), 'K_min': str(Kmin),
          'degree_caps_checked': degrees, 'column_player_checks': column_checks,
          'all_state_player_complement_checks': complement_checks,
          'padding_is_pure_cubic': True,
          'padding_uses_same_private_resource_both_actions': False,
          'common_private_implementation_cost_equivalence_checked': True,
          'padded_base_resource_count': 16,
          'every_player_two_nonempty_disjoint_antichain_actions': True,
          'alpha_one_in_scope': False,
          'cases': rows,
          'result': 'PASS; finite exact checks support but do not replace the all-D proof'}
text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
if args.output:
    with args.output.open('x') as stream:
        stream.write(text)
    print(json.dumps({'output': str(args.output), 'result': result['result']}))
else:
    print(text, end='')
