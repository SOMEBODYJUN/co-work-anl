#!/usr/bin/env python3
"""锚定时钟真实资源审计；标准库、Fraction、独立 literal 用户群实现。"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import platform
import random


def evaluate(coefficients, load):
    value = F(0)
    for coefficient in reversed(coefficients):
        value = value * load + coefficient
    return value


def literal_costs(state, weights, clocks):
    """Build both actual resources, then charge users at their actual load."""
    costs = [F(0)] * len(state)
    for (i, j), coefficients in clocks.items():
        groups = [[], []]
        for player, target in ((0, 0), (i, 1), (j, 0)):
            groups[state[player] ^ target].append(player)
        for users in groups:
            load = sum((weights[player] for player in users), F(0))
            fee = evaluate(coefficients, load)
            for player in users:
                costs[player] += fee
    return costs


def actual_margin(state, player, weights, clocks, alpha):
    changed = list(state)
    changed[player] ^= 1
    return (literal_costs(state, weights, clocks)[player]
            - alpha * literal_costs(changed, weights, clocks)[player])


def fraction_string(value):
    return str(value)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output')
    args = parser.parse_args()
    totals = dict(cases=0, states=0, illegal_states=0, half_edges=0,
                  pair_efficiencies=0, ordered_pair_efficiencies=0,
                  kappa_state_player_bounds=0, full_trigger_highest_degree=0)
    for n in range(3, 8):
        for alpha in (F(1), F(3, 2), F(2)):
            for seed in range(4):
                rng = random.Random(1000 * n + seed)
                if seed == 0:
                    weights = [F(2 ** (n-k-1)) for k in range(n)]
                else:
                    weights = [F(rng.randint(1, 11), rng.randint(1, 5))
                               for _ in range(n)]
                    if seed == 3:
                        weights.sort(reverse=True)
                clocks = {}
                for i in range(1, n):
                    for j in range(i + 1, n):
                        # First case zero, second constant, then genuinely mixed.
                        degree = 0 if seed < 2 else (2 if seed == 2 else 4)
                        coefficients = [F(rng.randint(0, 4), rng.randint(1, 5))
                                        for _ in range(degree + 1)]
                        if seed == 0:
                            coefficients = [F(0)]
                        clocks[i, j] = coefficients
                # Independently evaluate actual full resource games at each edge.
                observed_g = []
                for i in range(n):
                    state = [0] * n if i == 0 else [int(k >= i) for k in range(n)]
                    observed = actual_margin(state, i, weights, clocks, alpha)
                    opposite = [1 - bit for bit in state]
                    assert actual_margin(opposite, i, weights, clocks, alpha) == observed
                    observed_g.append(observed)
                    totals['half_edges'] += 2
                # Reconstruct symbolic formulas only as a separately checked target.
                analytic_g = [F(0)] * n
                total_pair_budget = F(0)
                gains = {}
                for (i, j), coefficients in clocks.items():
                    a, b, c = weights[0], weights[i], weights[j]
                    fee = lambda load: evaluate(coefficients, load)
                    analytic_g[0] += fee(a+c) - alpha * fee(a+b)
                    analytic_g[i] += fee(a+b) - alpha * fee(b+c)
                    analytic_g[j] += fee(b+c) - alpha * fee(a+c)
                    budget = fee(a+b) + fee(a+c) + fee(b+c)
                    total_pair_budget += budget
                    gains[i, j] = (fee(a+b+c) - fee(a+b)
                                   + alpha * (fee(b+c) - fee(b)))
                    assert gains[i, j] >= 0
                    ratios = []
                    ell_ratios = []
                    D = len(coefficients) - 1
                    for k in range(D + 1):
                        unit = [F(0)] * k + [F(1)]
                        singleton = {(i, j): unit}
                        legal = [0] * n
                        legal[i:] = [1] * (n-i)
                        illegal = legal.copy()
                        illegal[j] = 0
                        gain = (actual_margin(illegal, i, weights, singleton, alpha)
                                - actual_margin(legal, i, weights, singleton, alpha))
                        monomial_budget = (a+b)**k + (a+c)**k + (b+c)**k
                        ratios.append(gain / monomial_budget)
                        assert gain == ((a+b+c)**k - (a+b)**k
                                        + alpha*((b+c)**k - b**k))
                        if alpha > 1 and a >= b >= c:
                            loss = alpha*(a+b)**k - (a+c)**k
                            assert loss > 0
                            ell_ratios.append(gain / loss)
                    assert gains[i, j] <= max(ratios) * budget
                    totals['pair_efficiencies'] += 1
                    if alpha > 1 and a >= b >= c:
                        loss = alpha*fee(a+b) - fee(a+c)
                        assert gains[i, j] <= max(ell_ratios) * loss
                        r = c/(a+b)
                        degree_bound = ((1+r)**D-1+alpha*D*r)/(alpha-1)
                        assert max(ell_ratios) <= degree_bound
                        totals['ordered_pair_efficiencies'] += 1
                assert observed_g == analytic_g
                assert sum(observed_g) == -(alpha-1)*total_pair_budget
                for state in product((0, 1), repeat=n):
                    totals['states'] += 1
                    if alpha > 1:
                        kappas = [F(0)] * n
                        for (u, v), coefficients in clocks.items():
                            D = len(coefficients) - 1
                            triple = (0, u, v)
                            full = [0] * n
                            full[u] = 1
                            for player in triple:
                                full_ratios = []
                                for k in range(D + 1):
                                    singleton = {(u, v): [F(0)] * k + [F(1)]}
                                    budget = ((weights[0]+weights[u])**k
                                              + (weights[0]+weights[v])**k
                                              + (weights[u]+weights[v])**k)
                                    value = actual_margin(state, player, weights, singleton, alpha) / budget
                                    kappas[player] = max(kappas[player], value)
                                    full_ratios.append(max(F(0), actual_margin(
                                        full, player, weights, singleton, alpha) / budget))
                                assert max(full_ratios) == full_ratios[-1]
                                totals['full_trigger_highest_degree'] += 1
                        for player in range(n):
                            assert actual_margin(state, player, weights, clocks, alpha) <= kappas[player]*total_pair_budget
                            totals['kappa_state_player_bounds'] += 1
                    changes = sum(state[k] != state[k-1] for k in range(1, n))
                    if changes <= 1:
                        continue
                    totals['illegal_states'] += 1
                    anchor = state[0]
                    first = next(k for k in range(1, n) if state[k] != anchor)
                    returned = [j for j in range(first+1, n) if state[j] == anchor]
                    assert returned
                    actual = actual_margin(state, first, weights, clocks, alpha)
                    assert actual == observed_g[first] + sum(
                        (gains[first, j] for j in returned), F(0))
                totals['cases'] += 1
    # Explicit nonmonotonic sharp monomial efficiency, including reversal check.
    a, b, c, alpha = map(F, (10, 1, 1, 2))
    ratios = [((a+b+c)**k - (a+b)**k + alpha*((b+c)**k - b**k)) /
              ((a+b)**k + (a+c)**k + (b+c)**k) for k in range(3)]
    assert ratios == [F(0), F(1, 8), F(29, 246)]
    assert ratios[1] > ratios[2]
    assert ratios[1] * F(8) == 1
    assert ratios[2] * F(246) == 29
    fixture_path = Path(__file__).resolve().parents[4] / 'examples/weighted_congestion/anchored_actual_clock_degree43.json'
    fixture = json.loads(fixture_path.read_text())
    weights = list(map(F, fixture['weights']))
    alpha = F(fixture['alpha'])
    clocks = {}
    for entry in fixture['clock_pairs']:
        i, j = entry['pair']
        degree = entry['degree']
        load = weights[0] + weights[i] + weights[j]
        clocks[i, j] = [F(0)] * degree + [F(entry['amplitude']) / load**degree]

    def fixture_base_costs(state):
        costs = [F(0)] * len(weights)
        for entry in fixture['base_pairs']:
            groups = [[], []]
            for player, sign in enumerate(entry['signature']):
                if sign:
                    groups[state[player] ^ int(sign < 0)].append(player)
            for users in groups:
                load = sum((weights[player] for player in users), F(0))
                fee = F(entry['coefficient']) * load**entry['degree']
                for player in users:
                    costs[player] += fee
        return costs

    def fixture_margin(state, player):
        changed = list(state)
        changed[player] ^= 1
        old = fixture_base_costs(state)[player] + literal_costs(state, weights, clocks)[player]
        new = fixture_base_costs(changed)[player] + literal_costs(changed, weights, clocks)[player]
        return old - alpha * new

    fixture_records = []
    for state in product((0, 1), repeat=4):
        changes = sum(state[k] != state[k-1] for k in range(1, 4))
        if changes <= 1:
            if len(set(state)) == 1:
                player = 0
            else:
                player = next(k for k in range(1, 4) if state[k] != state[0])
            kind = 'ring'
        else:
            player = next(k for k in range(1, 4) if state[k] != state[0])
            kind = 'first_opposite'
        margin = fixture_margin(state, player)
        assert margin > 0
        fixture_records.append({'state': ''.join(map(str, state)), 'player': player,
                                'kind': kind, 'margin': str(margin)})
    B = max(value for state in product((0, 1), repeat=4)
            for value in fixture_base_costs(state))
    base_ring_margins = []
    for player in range(4):
        state = [int(k < player) for k in range(4)]
        changed = state.copy()
        changed[player] ^= 1
        base_ring_margins.append(fixture_base_costs(state)[player]
                                 - alpha*fixture_base_costs(changed)[player])
    eta = min(base_ring_margins)
    delta = max(1 - min(weights[0], weights[i], weights[j]) /
                (weights[0]+weights[i]+weights[j])
                for i in range(1, 4) for j in range(i+1, 4))
    threshold = eta / (4*alpha*alpha*B*3)
    uniform_degree = 0
    while delta**uniform_degree > threshold:
        uniform_degree += 1
    assert uniform_degree == 91
    assert delta**uniform_degree <= threshold < delta**(uniform_degree-1)
    payload = {
        'status': 'all_exact_assertions_passed',
        'scope': 'finite audit of literal costs; general statements use written proof',
        'arithmetic': 'fractions.Fraction; no floating point or imported author code',
        'parameters': {'n': list(range(3, 8)), 'alpha': ['1', '3/2', '2'],
                       'seed': list(range(4)), 'degree_by_seed': [0, 0, 2, 4]},
        'counts': totals,
        'nonmonotonic_efficiency': list(map(fraction_string, ratios)),
        'degree43_fixture': {'input_sha256': hashlib.sha256(fixture_path.read_bytes()).hexdigest(),
                             'states': fixture_records,
                             'uniform_budget_comparison': {'B': str(B), 'eta': str(eta),
                                                           'delta': str(delta),
                                                           'minimal_budget_degree': uniform_degree},
                             'minimum_margin': str(min(F(row['margin']) for row in fixture_records))},
        'python': platform.python_version(),
        'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    data = json.dumps(payload, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        with Path(args.output).open('x', encoding='utf-8') as stream:
            stream.write(data)
    print(data, end='')


if __name__ == '__main__':
    main()
