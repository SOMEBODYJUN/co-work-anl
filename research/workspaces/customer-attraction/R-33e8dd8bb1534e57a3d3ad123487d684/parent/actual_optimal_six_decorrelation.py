#!/usr/bin/env python3
"""Actual-source, distinct-optimal-six auxiliary decorrelation obstruction.

Old 34-customer policy plus three disjoint 18-customer bank topics.  A complete
six-player strategy is built, then every ordered-history IC is independently
checked.  This is NOT a half-coverage or ROW counterexample.  It rules out
repairing the unsigned decorrelation shortcut by reselecting a uniform
optimal six-slot tuple, even at a genuine actual-path source.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement
from pathlib import Path
import argparse
import json
import sys

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'work.py').exists())
sys.path.insert(0, str(ROOT))
from customer_attraction.model import Instance, CustomerType
from customer_attraction.certificate import StrategyCertificate, verify_certificate


def run():
    source = ROOT / 'examples/customer_attraction/individual_security_failure.json'
    original = Instance.from_dict(json.loads(source.read_text()))
    assert original.players == 3 and original.topic_count == 6
    banks = tuple(CustomerType(frozenset({6 + j}), 18) for j in range(3))
    instance = Instance(original.topics + ('BANK0', 'BANK1', 'BANK2'),
                        original.customers + banks, 6)
    anchor = (6, 7, 8)
    actions, cache = {}, {}

    def topic_values(leaf):
        counts = instance.counts(leaf, terminal=True)
        if counts not in cache:
            cache[counts] = instance.topic_payoffs(counts)
        return cache[counts]

    def build(h):
        if len(h) == 6:
            return h
        leaves = [build(h + (a,)) for a in range(9)]
        values = [topic_values(leaf)[a] for a, leaf in enumerate(leaves)]
        chosen = max(range(9), key=lambda a: values[a])
        if len(h) < 3 and h == anchor[:len(h)]:
            chosen = anchor[len(h)]
        elif h[:3] == anchor:
            relative = h[3:]
            if not relative:
                chosen = 0
            elif len(relative) == 1:
                chosen = (3 if relative[0] < 3 else 0) if relative[0] < 6 else 3
            elif len(relative) == 2 and max(relative) < 6:
                group = range(3) if relative[1] < 3 else range(3, 6)
                chosen = min(c for c in group if c not in relative)
            elif len(relative) == 2 and relative[0] >= 6 and relative[1] == 3:
                chosen = 4
        assert values[chosen] == max(values), (h, chosen, values)
        actions[h] = chosen
        return leaves[chosen]

    actual = build(())
    assert actual == (6, 7, 8, 0, 3, 4)
    certificate = StrategyCertificate(actions, instance.counts(actual, terminal=True))
    checked = verify_certificate(instance, certificate)
    checked.assert_valid()
    assert checked.checked_histories == 66430
    assert checked.checked_deviations == 531440
    assert instance.customer_count == 88
    optimum = instance.optimal_welfare()
    assert optimum == 88
    welfare = instance.welfare(instance.counts(actual))
    assert welfare == 86

    def follow(h):
        while len(h) < 6:
            h += (actions[h],)
        return h

    def payoff(a, leaf):
        return topic_values(leaf)[a]

    def f(a, query):
        return sum((F(c.multiplicity, 1 + sum(q in c.topics for q in anchor)
                      + int(a in c.topics))
                    for c in instance.customers if query in c.topics), F())

    def diagnostic(themes):
        tails = [follow(anchor + (a,))[-2:] for a in themes]
        diagonal = independent = first_ic = last_ic = option = F()
        for a, (b, c) in zip(themes, tails):
            diagonal += payoff(a, anchor + (a, b, c)) / 6
            for b2, c2 in tails:
                cross_last = actions[anchor + (a, b2)]
                true_leaf = anchor + (a, b, c)
                cross_leaf = anchor + (a, b2, cross_last)
                transplanted = anchor + (a, b2, c2)
                independent += payoff(a, transplanted) / 36
                first_ic += (payoff(b, true_leaf) - payoff(b2, cross_leaf)) / 36
                last_ic += (payoff(cross_last, cross_leaf) - payoff(c2, transplanted)) / 36
                option += (f(a, c) - f(a, cross_last)) / 36
        delta = diagonal - independent
        assert delta == first_ic + last_ic + option
        assert first_ic >= 0 and last_ic >= 0
        return {'optimal_six_tuple': list(themes), 'true_tails': [list(t) for t in tails],
                'diagonal': str(diagonal), 'independent': str(independent),
                'delta': str(delta), 'first_follower_IC': str(first_ic),
                'last_follower_IC': str(last_ic), 'signed_option': str(option)}

    records = []
    examined = 0
    for themes in combinations_with_replacement(range(9), 6):
        examined += 1
        if instance.welfare(instance.counts(themes)) == optimum:
            records.append(diagnostic(themes))
    assert examined == 3003
    assert len(records) == 4
    assert all(len(set(q['optimal_six_tuple'])) == 6 for q in records)
    assert all(F(q['delta']) < 0 for q in records)
    expected = {(0, 2, 5, 6, 7, 8): '-11/72', (1, 2, 5, 6, 7, 8): '-11/72',
                (2, 3, 5, 6, 7, 8): '-1/9', (2, 4, 5, 6, 7, 8): '-1/9'}
    assert {tuple(q['optimal_six_tuple']): q['delta'] for q in records} == expected
    return {
        'scope': 'auxiliary uniform-optimal-six decorrelation fails at actual source for EVERY optimal tuple; NOT half or ROW counterexample',
        'players': 6, 'catalog_size': 9, 'customers': 88,
        'source': str(source.relative_to(ROOT)),
        'source_sha256': sha256(source.read_bytes()).hexdigest(),
        'banks': {'topics': [6, 7, 8], 'disjoint_unit_customers_per_topic': 18},
        'actual_history': list(actual), 'actual_payoffs': list(map(str, instance.player_payoffs(actual))),
        'actual_source': list(anchor), 'source_remaining_players': 3,
        'actual_welfare': welfare, 'OPT6': optimum,
        'full_SPE_verified': checked.valid, 'checked_ordered_histories': checked.checked_histories,
        'checked_nonself_deviations': checked.checked_deviations,
        'examined_terminal_multisets_for_optimum': examined,
        'all_optimal_six_tuples': records,
        'strategy_recipe': 'Exact full backward induction, lexicographic best reply except stated valid tie overrides; actual banks in order; old policy at original source query; true two-player (3,4) reply after a forced bank query.'
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = run()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
