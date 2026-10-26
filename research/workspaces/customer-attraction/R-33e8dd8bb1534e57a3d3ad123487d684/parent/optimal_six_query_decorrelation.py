#!/usr/bin/env python3
"""Exact six-provider attack on an auxiliary decorrelation claim.

This is NOT a counterexample to half coverage or to ROW.  It embeds the
existing 34-customer three-provider policy at a genuine six-provider history,
then uses a uniform globally optimal SIX-slot comparison tuple.  The complete
ordered strategy is constructed by backward induction and checked by the
repository's separate definition-level verifier.  No outcome-set solver is
used.  All mathematical comparisons use Fraction.
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
from customer_attraction.model import Instance
from customer_attraction.certificate import StrategyCertificate, verify_certificate


def run():
    source = ROOT / 'examples/customer_attraction/individual_security_failure.json'
    original = Instance.from_dict(json.loads(source.read_text()))
    assert original.players == 3 and original.topic_count == 6
    instance = Instance(original.topics + ('EMPTY',), original.customers, 6)
    empty = 6
    anchor = (empty,) * 3
    actions = {}
    payoff_cache = {}

    def topic_values(leaf):
        counts = instance.counts(leaf, terminal=True)
        if counts not in payoff_cache:
            payoff_cache[counts] = instance.topic_payoffs(counts)
        return payoff_cache[counts]

    def last(a, b):
        group = range(3) if b < 3 else range(3, 6)
        return min(c for c in group if c not in (a, b))

    def build(history):
        if len(history) == 6:
            return history
        leaves = [build(history + (a,)) for a in range(7)]
        values = [topic_values(leaf)[a] for a, leaf in enumerate(leaves)]
        chosen = max(range(7), key=lambda a: values[a])
        if history[:3] == anchor:
            relative = history[3:]
            if not relative:
                chosen = 0
            elif len(relative) == 1 and relative[0] < 6:
                chosen = 3 if relative[0] < 3 else 0
            elif len(relative) == 2 and max(relative) < 6:
                chosen = last(*relative)
        assert values[chosen] == max(values), (history, chosen, values)
        actions[history] = chosen
        return leaves[chosen]

    actual = build(())
    cert = StrategyCertificate(actions, instance.counts(actual, terminal=True))
    checked = verify_certificate(instance, cert)
    checked.assert_valid()
    assert checked.checked_histories == sum(7 ** j for j in range(6))
    assert checked.checked_deviations == 6 * checked.checked_histories

    def follow(history):
        while len(history) < 6:
            history += (actions[history],)
        return history

    def payoff(topic, leaf):
        return topic_values(leaf)[topic]

    def f(a, query):
        # The option value after deleting the middle follower, at old b=0.
        return sum((F(c.multiplicity, 1 + int(a in c.topics))
                    for c in instance.customers if query in c.topics), F())

    def diagnostic(themes):
        M = len(themes)
        tails = [follow(anchor + (a,))[-2:] for a in themes]
        diagonal = independent = first_ic = last_ic = option = F()
        for a, (b, c) in zip(themes, tails):
            diagonal += payoff(a, anchor + (a, b, c)) / M
            for b2, c2 in tails:
                cross_last = actions[anchor + (a, b2)]
                leaf = anchor + (a, b, c)
                cross_true = anchor + (a, b2, cross_last)
                transplanted = anchor + (a, b2, c2)
                independent += payoff(a, transplanted) / (M * M)
                first_ic += (payoff(b, leaf) - payoff(b2, cross_true)) / (M * M)
                last_ic += (payoff(cross_last, cross_true) - payoff(c2, transplanted)) / (M * M)
                option += (f(a, c) - f(a, cross_last)) / (M * M)
        delta = diagonal - independent
        assert delta == first_ic + last_ic + option
        assert first_ic >= 0 and last_ic >= 0
        coverage = instance.welfare(instance.counts(themes))
        assert coverage == instance.optimal_welfare() == 34
        return {'comparison_tuple': list(themes), 'coverage': coverage,
                'diagonal': str(diagonal), 'independent': str(independent),
                'delta': str(delta), 'first_follower_IC': str(first_ic),
                'last_follower_IC': str(last_ic), 'signed_option': str(option)}

    triple_checks = []
    for themes in combinations_with_replacement(range(6), 3):
        if instance.welfare(instance.counts(themes)) == 34:
            triple_checks.append(diagnostic(themes))
    assert len(triple_checks) == 4
    assert {q['delta'] for q in triple_checks} == {'-5/18'}
    six = diagnostic((0, 2, 2, 5, 5, 5))
    assert six['delta'] == '-3/8'
    distinct = diagnostic(tuple(range(6)))
    assert distinct['delta'] == '0'
    actual_welfare = instance.welfare(instance.counts(actual, terminal=True))
    assert 2 * actual_welfare >= instance.optimal_welfare()
    return {
        'scope': 'auxiliary uniform optimal-query decorrelation obstruction; NOT half or ROW counterexample',
        'players': 6, 'catalog_size': 7, 'customers': 34,
        'source': str(source.relative_to(ROOT)),
        'source_sha256': sha256(source.read_bytes()).hexdigest(),
        'distinguished_history': list(anchor),
        'background_load': 0, 'remaining_players': 3,
        'full_SPE_verified': checked.valid,
        'checked_ordered_histories': checked.checked_histories,
        'checked_nonself_deviations': checked.checked_deviations,
        'actual_history': list(actual), 'actual_welfare': actual_welfare,
        'OPT6': instance.optimal_welfare(),
        'distinct_optimal_six_tuple': distinct,
        'repeated_optimal_six_tuple': six,
        'all_optimal_triples': triple_checks,
        'strategy_recipe': 'Complete backward induction; inside EMPTY^3 preserve the old policy whenever its first two relative actions are original topics; lexicographic best replies elsewhere.'
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
