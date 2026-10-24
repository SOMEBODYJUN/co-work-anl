#!/usr/bin/env python3
"""Independent definition-level replay of the proposed optimal-prefix bill.

The source packet predates this candidate. No project solver or discovery
script is imported. All multiplicities are expanded into unit customers.
"""
from fractions import Fraction
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
INPUT = ROOT / 'examples/customer_attraction/prefix_balance_failure.json'
CERT = ROOT / 'evidence/certificates/customer_attraction/prefix_balance_failure.json'
OUTPUT = Path(__file__).with_suffix('.json')


def main():
    data = json.loads(INPUT.read_text())
    certificate = json.loads(CERT.read_text())
    m, labels = data['players'], len(data['topics'])
    clients = []
    for row in data['customers']:
        assert type(row['multiplicity']) is int and row['multiplicity'] >= 0
        clients.extend([frozenset(row['topics'])] * row['multiplicity'])
    assert len({frozenset(x for x, c in enumerate(clients) if a in c)
                for a in range(labels)}) == labels
    policy = {tuple(row['history']): row['action']
              for row in certificate['actions']}
    histories = [h for depth in range(m)
                 for h in product(range(labels), repeat=depth)]
    assert set(policy) == set(histories)

    def rollout(prefix):
        h = tuple(prefix)
        while len(h) < m:
            a = policy[h]
            assert 0 <= a < labels
            h += (a,)
        return h

    def payoff(z, i):
        return sum((Fraction(1, sum(a in c for a in z))
                    for c in clients if z[i] in c), Fraction(0))

    def coverage(z):
        return sum(any(a in c for a in z) for c in clients)

    comparisons = 0
    for h in histories:
        i = len(h)
        selected = payoff(rollout(h), i)
        for a in range(labels):
            assert selected >= payoff(rollout(h + (a,)), i), (h, a)
            comparisons += 1
    actual = rollout(())
    w = coverage(actual)
    assert sum(payoff(actual, i) for i in range(m)) == w
    opt, optimal = -1, []
    for z in product(range(labels), repeat=m):
        value = coverage(z)
        if value > opt:
            opt, optimal = value, [z]
        elif value == opt:
            optimal.append(z)
    multisets = sorted({tuple(sorted(z)) for z in optimal})
    assert len(multisets) == 1
    multiset = multisets[0]
    rows = []
    for order in sorted(set(permutations(multiset))):
        steps = []
        total = Fraction(0)
        for i in range(m):
            z = rollout(order[:i+1])
            charge = payoff(z, i)
            total += charge
            steps.append({'prefix': order[:i+1], 'terminal': z,
                          'charge': str(charge)})
        rows.append({'order': order, 'bill': str(total), 'steps': steps})
    minimum = min(Fraction(row['bill']) for row in rows)
    assert minimum > w
    output = {
        'candidate': 'exists optimal multiset and ordering with forced-optimal-prefix bill <= actual W',
        'status': 'refuted; not a Q-CAG-HALF counterexample',
        'source_sha256': {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                          for p in (INPUT, CERT)},
        'players': m, 'labels': labels, 'unit_customers': len(clients),
        'histories': len(histories), 'spe_comparisons_including_self': comparisons,
        'actual': actual, 'actual_payoffs': [str(payoff(actual, i)) for i in range(m)],
        'W': w, 'OPT': opt, 'optimal_multisets': multisets,
        'ordered_optima': len(optimal), 'bills_checked': len(rows),
        'minimum_bill': str(minimum), 'gap': str(minimum-w), 'rows': rows,
    }
    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in output.items()
                      if k not in ('rows', 'source_sha256')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
