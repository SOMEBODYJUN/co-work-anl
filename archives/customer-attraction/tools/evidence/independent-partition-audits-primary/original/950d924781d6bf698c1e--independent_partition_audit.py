"""Definition-level independent audit of the parent's PFR-OPT witness.

Reads only customer types and the complete strategy, expands all unit clients,
and imports neither the parent's audit nor the canonical CAG implementation.
"""

import argparse
import json
from fractions import Fraction as F
from itertools import permutations, product
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--large', action='store_true', help='audit original 127-client version')
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    source = here.parent/'next_boss/partition_attack'/(
        'exact_witness.json' if args.large else 'small_exact_witness.json')
    data = json.loads(source.read_text())
    p, m = data['topics'], data['players']
    assert m == 2
    clients = []
    for item in data['types']:
        clients.extend([frozenset(item['topics'])] * item['multiplicity'])
    topics = [set(x for x, likes in enumerate(clients) if a in likes) for a in range(p)]
    root = data['root_action']
    replies = data['complete_replies']
    assert len(replies) == p and all(0 <= a < p for a in replies)

    def pay(profile, i):
        return sum((F(1, sum(x in topics[a] for a in profile))
                    for x in topics[profile[i]]), F())

    def final(h):
        if not h:
            h = (root,)
        if len(h) == 1:
            h = h + (replies[h[0]],)
        return h

    payoff_rows = []
    checked = 0
    for history in [()] + [(a,) for a in range(p)]:
        i = len(history)
        assigned = root if i == 0 else replies[history[0]]
        values = [pay(final(history+(a,)), i) for a in range(p)]
        assert all(values[assigned] >= v for v in values), (history, values)
        checked += p
        payoff_rows.append({'history': history, 'chosen': assigned,
                            'payoffs': list(map(str, values))})

    actual = final(())
    actual_union = topics[actual[0]] | topics[actual[1]]
    actual_load = [sum(x in topics[a] for a in actual) for x in range(len(clients))]
    coverages = {pair: len(topics[pair[0]] | topics[pair[1]])
                 for pair in product(range(p), repeat=m)}
    optimum = max(coverages.values())
    optimal_ordered = [pair for pair, value in coverages.items() if value == optimum]
    assert optimal_ordered == [(2, 3), (3, 2)]
    assert not (topics[2] & topics[3])
    frozen = []
    for comparison in optimal_ordered:
        O = topics[comparison[0]] | topics[comparison[1]]
        for match in permutations(range(m)):
            # A client can choose any eligible occurrence independently.
            # This directly minimizes over all partitions, with empty blocks legal.
            value = F()
            owner_counts = [0] * m
            for x in O:
                candidates = [(F(1, actual_load[x]+1-(x in topics[actual[i]])), j)
                              for i, j in enumerate(match) if x in topics[comparison[j]]]
                assert candidates
                cheapest, owner = min(candidates)
                value += cheapest
                owner_counts[owner] += 1
            assert value > len(actual_union)
            frozen.append({'comparison': comparison, 'matching': match,
                           'minimum_over_all_partitions': str(value),
                           'assigned_client_counts': owner_counts})

    report = {
        'status': 'independent_definition_level_audit_passed',
        'scope': 'PFR-OPT-v1 is refuted; Q-CAG-HALF is not refuted',
        'unit_clients_expanded': len(clients),
        'checked_ordered_strategy_nodes': len(payoff_rows),
        'checked_exact_action_comparisons': checked,
        'payoff_rows': payoff_rows,
        'actual_path': actual,
        'actual_payoffs': [str(pay(actual, i)) for i in range(m)],
        'actual_W': len(actual_union),
        'all_ordered_comparison_tuples_including_repetitions': len(coverages),
        'OPT': optimum,
        'all_optimal_ordered_portfolios': optimal_ordered,
        'optimal_themes_are_disjoint': True,
        'partition_minima': frozen,
        'minimum_partition_excess_over_W': str(min(F(r['minimum_over_all_partitions']) for r in frozen)
                                               -len(actual_union)),
        'half_coverage_holds': 2*len(actual_union) >= optimum,
    }
    target = here/('independent_partition_large_audit.json' if args.large
                  else 'independent_partition_small_audit.json')
    with target.open('x') as f:
        json.dump(report, f, indent=2)
        f.write('\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
