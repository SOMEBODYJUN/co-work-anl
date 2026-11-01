"""Reproduce a population-deletion boundary from unit customers and ordered histories.

The direct oracle below does not import customer_attraction.  It computes all
SPE-achievable terminal histories, keeping each ordered prefix separate.  A
separate direct check replays every action in the frozen complete certificates.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, combinations
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
TOPICS = ('A', 'B', 'C', 'D')
TYPES = ((0, 1), (2,), (1, 2), (0, 3), (0, 1, 3), (2, 3))


def customer_sets(weights):
    return tuple(frozenset(t) for t, w in zip(TYPES, weights) for _ in range(w))


def payoffs(customers, history):
    result = [F(0)] * len(history)
    for c in customers:
        users = [i for i, a in enumerate(history) if a in c]
        if users:
            for i in users:
                result[i] += F(1, len(users))
    return tuple(result)


def welfare(customers, history):
    return sum(any(a in c for a in history) for c in customers)


def ordered_oracle(customers, m):
    @lru_cache(None)
    def solve(h):
        if len(h) == m:
            return frozenset((h,))
        children = [solve(h + (a,)) for a in range(4)]
        i = len(h)
        floor = max(min(payoffs(customers, z)[i] for z in ch) for ch in children)
        return frozenset(z for ch in children for z in ch
                         if payoffs(customers, z)[i] >= floor)
    return solve(())


def verify_certificate(customers, m, actions):
    expected = {h for d in range(m) for h in product(range(4), repeat=d)}
    assert set(actions) == expected
    def follow(h):
        while len(h) < m:
            h = h + (actions[h],)
        return h
    table, slacks = [], []
    for h in sorted(expected, key=lambda h: (len(h), h)):
        a = actions[h]
        values = [payoffs(customers, follow(h + (b,)))[len(h)] for b in range(4)]
        assert values[a] == max(values)
        other = [values[a] - values[b] for b in range(4) if b != a]
        slacks.extend(other)
        table.append({'history': ''.join(TOPICS[x] for x in h),
                      'chosen': TOPICS[a], 'values': [str(v) for v in values],
                      'strict': all(v > 0 for v in other)})
    z = follow(())
    return {'nodes': len(expected), 'comparisons': 4 * len(expected),
            'minimum_nonself_slack': str(min(slacks)),
            'all_nodes_strict': all(s > 0 for s in slacks),
            'path': ''.join(TOPICS[x] for x in z),
            'payoffs': [str(x) for x in payoffs(customers, z)],
            'welfare': welfare(customers, z), 'table': table}


def run():
    report = {'scope': 'Population-monotonicity and support-preserving deletion boundaries only; Q-CAG-HALF remains OPEN', 'examples': []}
    for name, weights in [('thirteen', [3, 1, 2, 1, 3, 3]), ('strict_forty', [9, 1, 7, 2, 11, 10])]:
        customers = customer_sets(weights)
        rec = {'name': name, 'types': [{'topics': [TOPICS[a] for a in t], 'multiplicity': w} for t, w in zip(TYPES, weights)], 'unit_customers': len(customers), 'players': {}}
        for m in (2, 3):
            terminals = ordered_oracle(customers, m)
            cert_obj = json.loads((HERE / f'{name}_m{m}_certificate.json').read_text())
            actions = {tuple(row['history']): row['action'] for row in cert_obj['actions']}
            checked = verify_certificate(customers, m, actions)
            all_counts = sorted({tuple(z.count(a) for a in range(4)) for z in terminals})
            optimal = max(welfare(customers, z) for z in product(range(4), repeat=m))
            minimum = min(welfare(customers, z) for z in terminals)
            checked.update({'all_SPE_terminal_counts': all_counts, 'minimum_SPE_welfare': minimum, 'OPT': optimal, 'ordered_SPE_paths': [''.join(TOPICS[a] for a in z) for z in sorted(terminals)]})
            assert optimal == len(customers)
            assert minimum == len(customers) - (m == 3) * weights[1]
            if m == 2:
                assert all_counts == [(1, 0, 1, 0)]
            if name == 'strict_forty':
                assert checked['all_nodes_strict']
                assert len(terminals) == 1
            rec['players'][str(m)] = checked
        report['examples'].append(rec)
    # An even smaller support-preserving deletion failure, used only as a diagnostic.
    tiny = (frozenset((0,)),) + (frozenset((0,2)),)*2 + (frozenset((1,2)),)*2
    one = ordered_oracle(tiny, 1)
    two = ordered_oracle(tiny, 2)
    assert one == frozenset(((2,),))
    assert (1,0) in two
    report['support_deletion_tiny'] = {'types': {'A':1,'AC':2,'BC':2}, 'two_player_SPE_path':'BA', 'only_one_player_SPE_path':'C', 'scope':'Deleting either BA player cannot give a one-player SPE on the same menu'}
    (HERE / 'population_exchange_audit.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status':'passed','examples':[{ 'name': r['name'], 'W2':r['players']['2']['minimum_SPE_welfare'],'W3':r['players']['3']['minimum_SPE_welfare'],'strict':r['players']['3']['all_nodes_strict']} for r in report['examples']]}))

if __name__ == '__main__':
    run()
