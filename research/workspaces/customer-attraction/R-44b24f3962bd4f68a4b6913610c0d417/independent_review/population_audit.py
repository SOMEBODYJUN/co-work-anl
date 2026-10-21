"""Independent unit-client audit of the population monotonicity obstruction.

No import of customer_attraction, the discovering code, or max-min recurrence.
Every node explicitly enumerates the Cartesian product of its children's
attainable ordered leaves and chooses every maximizing action in that menu.
Disjoint child witnesses are glued into full ordered-history strategies.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import argparse
import json

BASE = ((frozenset({0}), 3), (frozenset({1}), 3),
        (frozenset({2}), 1), (frozenset({0, 1}), 1),
        (frozenset({0, 2}), 2), (frozenset({1, 2}), 2))


def enumerate_game(players, scale=1):
    clients = tuple(B for B, count in BASE for _ in range(count * scale))

    @lru_cache(None)
    def utility(terminal, player):
        return sum((F(1, sum(a in B for a in terminal))
                    for B in clients if terminal[player] in B), F(0))

    @lru_cache(None)
    def menu_tree(history):
        if len(history) == players:
            return {history: {}}
        child_sets = [menu_tree(history + (a,)) for a in range(3)]
        answer = {}
        for menu in product(*(tuple(child) for child in child_sets)):
            payoffs = [utility(terminal, len(history)) for terminal in menu]
            best = max(payoffs)
            for action, payoff in enumerate(payoffs):
                if payoff != best:
                    continue
                witness = {history: action}
                for child, terminal in zip(child_sets, menu):
                    witness.update(child[terminal])
                answer.setdefault(menu[action], witness)
        return answer

    attainable = menu_tree(())
    expected_histories = {h for depth in range(players)
                          for h in product(range(3), repeat=depth)}
    certificates = []
    comparisons = 0
    for terminal, actions in sorted(attainable.items()):
        assert set(actions) == expected_histories

        def follow(history):
            while len(history) < players:
                history += (actions[history],)
            return history

        assert follow(()) == terminal
        slacks = []
        for history in expected_histories:
            actual = follow(history)
            for alternative in range(3):
                deviation = follow(history + (alternative,))
                slack = utility(actual, len(history)) - utility(deviation, len(history))
                assert slack >= 0
                slacks.append(slack)
                comparisons += 1
        certificates.append({
            'terminal': terminal,
            'payoffs': [str(utility(terminal, i)) for i in range(players)],
            'welfare': sum(any(a in B for a in terminal) for B in clients),
            'minimum_spe_slack': str(min(slacks)),
            'actions': [{'history': h, 'action': a} for h, a in sorted(actions.items())],
        })

    tables = []
    for depth in range(players - 1, -1, -1):
        rows = {}
        for history in product(range(3), repeat=depth):
            prefix = tuple(history.count(a) for a in range(3))
            outputs = tuple(sorted({tuple(t.count(a) for a in range(3))
                                    for t in menu_tree(history)}))
            if prefix in rows:
                assert rows[prefix] == outputs
            rows[prefix] = outputs
        tables.append({'depth': depth, 'rows': [
            {'prefix_counts': q, 'attainable_terminal_counts': t}
            for q, t in sorted(rows.items())]})

    return {'players': players, 'scale': scale, 'unit_clients': len(clients),
            'attainable_ordered_paths': sorted(attainable),
            'decision_histories_per_certificate': len(expected_histories),
            'all_action_comparisons': comparisons,
            'certificates': certificates, 'tables': tables}


def run():
    records = [enumerate_game(m) for m in (1, 2, 3, 4)]
    by_m = {r['players']: r for r in records}
    assert {tuple(t.count(a) for a in range(3)) for t in by_m[3]['attainable_ordered_paths']} == {(1, 1, 1)}
    assert {tuple(t.count(a) for a in range(3)) for t in by_m[4]['attainable_ordered_paths']} == {(2, 2, 0)}
    assert {c['welfare'] for c in by_m[3]['certificates']} == {12}
    assert {c['welfare'] for c in by_m[4]['certificates']} == {11}
    for m in (3, 4):
        scaled = enumerate_game(m, scale=2)
        assert scaled['attainable_ordered_paths'] == by_m[m]['attainable_ordered_paths']
        assert [c['welfare'] for c in scaled['certificates']] == [2*c['welfare'] for c in by_m[m]['certificates']]
    # Zero-client boundary: every action is a tie, so every path is possible.
    zero = enumerate_game(2, scale=0)
    assert len(zero['attainable_ordered_paths']) == 9
    assert all(c['welfare'] == 0 for c in zero['certificates'])
    return {'status': 'independently_verified',
            'main_half_coverage_status': 'unchanged OPEN; not a target counterexample',
            'method': 'all ordered histories, Cartesian child menus, explicit unit clients, Fraction',
            'records': records, 'boundary_checks': {'double_scale': True, 'zero_clients': True}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run()
    if args.output:
        with args.output.open('x') as stream:
            json.dump(result, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'records'}, ensure_ascii=False))
    for record in result['records']:
        print(json.dumps({k: v for k, v in record.items()
                          if k not in {'certificates', 'tables'}}, ensure_ascii=False))
