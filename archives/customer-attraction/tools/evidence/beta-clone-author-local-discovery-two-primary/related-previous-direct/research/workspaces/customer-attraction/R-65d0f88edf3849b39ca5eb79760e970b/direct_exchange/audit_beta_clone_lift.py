"""Definition-level finite rational Beta-clone witness, independent of authors.

Only the task's four customer types and the integral Beta(1,1) patterns are
used. No model, solver, prior verifier, or author manuscript is imported.
"""
import itertools
import json
import math
from fractions import Fraction as F
from pathlib import Path


def payoff(customers, b, leaf, player):
    a = leaf[player]
    ans = F(0)
    for customer, weight in customers:
        if a in customer:
            load = b.get(id(customer), 0) + sum(x in customer for x in leaf)
            ans += weight / load
    return ans


def original():
    catalog = ['A', 'B', 'C'] + [f'P{i}' for i in range(36)]
    customers = [(frozenset(['A', 'B']), F(36)),
                 (frozenset(['C']), F(3)),
                 (frozenset(['B', 'C']), F(10))]
    b = {}
    for i in range(36):
        customer = frozenset(['A', 'C', f'P{i}'])
        customers.append((customer, F(1)))
        b[id(customer)] = 1
    for customer, _ in customers:
        assert b.get(id(customer), 0) == sum(f'P{i}' in customer for i in range(36))
    replies, current_values = {}, {}
    chosen = {'A': 'B', 'B': 'A', 'C': 'A'}
    comparisons = 0
    for a in catalog:
        vals = {z: payoff(customers, b, ('A', a, z), 2) for z in catalog}
        best = max(vals.values())
        br = [z for z in catalog if vals[z] == best]
        z = chosen.get(a, br[0])
        assert z in br
        replies[a] = {'best_value': str(best), 'all_BR': br,
                      'A_B_C_values': {x: str(vals[x]) for x in ['A', 'B', 'C']}}
        current_values[a] = payoff(customers, b, ('A', a, z), 1)
        comparisons += len(catalog)
    assert current_values['A'] == 24
    assert current_values['B'] == current_values['C'] == 22
    assert all(current_values[a] <= 24 for a in catalog)
    comparisons += len(catalog)
    return {'catalog_size': len(catalog), 'nodes': 1 + len(catalog),
            'comparisons': comparisons,
            'A_B_C_last_rows': {a: replies[a] for a in ['A', 'B', 'C']},
            'current_payoffs': {a: str(v) for a, v in current_values.items()},
            'max_singleton_current': str(max(current_values[a] for a in catalog[3:]))}


def cloned():
    catalog = ['A0', 'A1', 'B0', 'C0'] + [f'P{i}_0' for i in range(36)]
    D = 60
    customers = [(frozenset(['A0', 'A1', 'B0']), F(36)),
                 (frozenset(['C0']), F(3)),
                 (frozenset(['B0', 'C0']), F(10))]
    for i in range(36):
        labels = ['A0', 'A1', 'C0', f'P{i}_0']
        for pattern in itertools.product([False, True], repeat=4):
            size = sum(pattern)
            weight = F(math.factorial(size) * math.factorial(4 - size), math.factorial(5))
            assert (weight * D).denominator == 1
            customer = frozenset(x for x, present in zip(labels, pattern) if present)
            customers.append((customer, weight))
    assert sum(w for _, w in customers) == 85
    assert all((w * D).denominator == 1 for _, w in customers)
    # This explicitly constructs 5100 distinct unit customers, including those
    # interested in no clone. Their empty-pattern presence changes no utility.
    units = [customer for customer, weight in customers for _ in range(int(weight * D))]
    assert len(units) == 5100

    def unit_u(leaf, player):
        a = leaf[player]
        return sum((F(1, sum(x in customer for x in leaf)) for customer in units
                    if a in customer), F(0)) / D

    rows = {}
    for a in ['A0', 'A1', 'B0', 'C0']:
        vals = {z: payoff(customers, {}, ('A0', a, z), 2) for z in catalog}
        # Cross-check every row/action against the expanded integer customers.
        for z in catalog:
            assert vals[z] == unit_u(('A0', a, z), 2)
        best = max(vals.values())
        br = [z for z in catalog if vals[z] == best]
        current = {z: payoff(customers, {}, ('A0', a, z), 1) for z in br}
        for z in br:
            assert current[z] == unit_u(('A0', a, z), 1)
        rows[a] = {'last_values': {z: str(vals[z]) for z in catalog[:4]},
                   'singleton_last_max': str(max(vals[z] for z in catalog[4:])),
                   'best_value': str(best), 'all_BR': br,
                   'current_payoff_by_BR': {z: str(v) for z, v in current.items()}}
    assert rows['A0']['all_BR'] == ['C0']
    assert rows['A0']['best_value'] == '23'
    assert rows['A0']['current_payoff_by_BR'] == {'C0': '25'}
    assert rows['A1']['all_BR'] == ['B0', 'C0']
    assert rows['A1']['current_payoff_by_BR']['B0'] == '24'
    assert rows['B0']['all_BR'] == ['A1']
    assert rows['C0']['all_BR'] == ['A1']
    return {'clone_catalog_size': len(catalog), 'scale': D, 'unit_customers': len(units),
            'rows': rows, 'strict_improvement': '25-24=1',
            'encoded_background_not_replayed': True}


if __name__ == '__main__':
    report = {'original': original(), 'clone': cloned()}
    dest = Path(__file__).with_name('beta_clone_lift_review.json')
    dest.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
