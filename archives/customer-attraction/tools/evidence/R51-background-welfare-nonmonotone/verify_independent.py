"""Definition-level two-active-player audit; no customer_attraction imports.

Expand the integer multiplicities into distinct unit customers and enumerate
every complete pure suffix strategy (one root action and one response per child).
This checks the fixed saved JSON, not the source's randomized discovery domain.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import json

BASE = Path(__file__).resolve().parent
SOURCE = (BASE / 'original/research/workspaces/customer-attraction/'
          'R-51ca8c2b36184c41818099bc490374ca/independent/'
          'background_welfare_nonmonotone.json')


def main():
    saved = json.loads(SOURCE.read_text())
    instance = saved['instance']
    k = len(instance['topics'])
    assert saved['r'] == 2
    clients = tuple(frozenset(row['topics'])
                    for row in instance['customers']
                    for _ in range(row['multiplicity']))

    def utility(action, terminal):
        return sum((Fraction(1, sum(topic in client for topic in terminal))
                    for client in clients if action in client), Fraction(0))

    def welfare(terminal):
        return sum(any(topic in client for topic in terminal) for client in clients)

    def counts(terminal):
        return tuple(terminal.count(a) for a in range(k))

    def audit(background):
        past = tuple(a for a, n in enumerate(background) for _ in range(n))
        last_values = [tuple(utility(j, past + (a, j)) for j in range(k))
                       for a in range(k)]
        last_best = [tuple(j for j, value in enumerate(row) if value == max(row))
                     for row in last_values]
        accepted = []
        for responses in product(range(k), repeat=k):
            if any(responses[a] not in last_best[a] for a in range(k)):
                continue
            root_values = tuple(utility(a, past + (a, responses[a])) for a in range(k))
            for root_action in range(k):
                if root_values[root_action] != max(root_values):
                    continue
                terminal = past + (root_action, responses[root_action])
                # All five decision nodes and all four actions, including self.
                comparisons = [last_values[a][responses[a]] - value
                               for a in range(k) for value in last_values[a]]
                comparisons += [root_values[root_action] - value for value in root_values]
                assert len(comparisons) == k * (k + 1)
                assert min(comparisons) >= 0
                accepted.append({
                    'root_action': root_action,
                    'responses_by_first_action': list(responses),
                    'terminal': list(terminal),
                    'terminal_counts': list(counts(terminal)),
                    'welfare': welfare(terminal),
                    'active_payoffs': [str(utility(a, terminal)) for a in terminal[-2:]],
                    'past_payoffs': [str(utility(a, terminal)) for a in past],
                    'root_action_values': list(map(str, root_values)),
                    'minimum_incentive_margin': str(min(comparisons)),
                    'all_payoffs_sum_to_welfare': sum(utility(a, terminal) for a in terminal)
                        == welfare(terminal),
                })
                assert accepted[-1]['all_payoffs_sum_to_welfare']
        assert accepted
        outcomes = sorted({tuple(item['terminal_counts']) for item in accepted})
        paths = sorted({tuple(item['terminal'][-2:]) for item in accepted})
        minimum_pair = min((item['welfare'], tuple(item['terminal_counts'])) for item in accepted)
        worst = next(item for item in accepted
                     if (item['welfare'], tuple(item['terminal_counts'])) == minimum_pair)
        return {
            'background': list(background),
            'total_players': len(past) + 2,
            'all_candidate_complete_strategies': k ** (k + 1),
            'accepted_complete_spe_strategies': len(accepted),
            'last_action_values_by_first_action': [list(map(str, row)) for row in last_values],
            'last_best_actions_by_first_action': [list(row) for row in last_best],
            'ordered_active_paths': [list(path) for path in paths],
            'terminal_count_outcomes': [list(outcome) for outcome in outcomes],
            'minimum_welfare_pair': [minimum_pair[0], list(minimum_pair[1])],
            'welfare_values': sorted({item['welfare'] for item in accepted}),
            'representative_minimum_welfare_complete_strategy': worst,
            'all_accepted_complete_strategies': accepted,
        }

    before = tuple(saved['base'])
    after = tuple(n + int(a == saved['add']) for a, n in enumerate(before))
    original = audit(before)
    added = audit(after)
    assert instance['players'] == sum(before) + saved['r']
    assert original['minimum_welfare_pair'] == saved['original']
    assert added['minimum_welfare_pair'] == saved['added']
    assert added['minimum_welfare_pair'][0] < original['minimum_welfare_pair'][0]
    report = {
        'status': 'PASS',
        'method': 'unit-customer direct payoffs; every complete pure two-player suffix strategy',
        'canonical_solver_imported': False,
        'customer_count': len(clients),
        'customer_type_count': len(instance['customers']),
        'topic_sizes': [sum(a in client for client in clients) for a in range(k)],
        'r': saved['r'],
        'added_topic': saved['add'],
        'background_coverage_before': welfare(tuple(a for a, n in enumerate(before) for _ in range(n))),
        'background_coverage_after': welfare(tuple(a for a, n in enumerate(after) for _ in range(n))),
        'original': original,
        'added': added,
        'exact_original_json_pairs_match': True,
    }
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
