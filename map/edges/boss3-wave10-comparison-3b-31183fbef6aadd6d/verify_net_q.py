#!/usr/bin/env python3
"""Replay both full ordered policy trees and check signed and unsigned matching."""

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product
from math import lcm
from pathlib import Path


LABELS = tuple(range(7))
PLAYERS = 5
MASKS = tuple(range(1, 1 << len(LABELS)))
SCALE = lcm(*range(1, PLAYERS + 2))
BASE = Path('archives/customer-attraction/tools/evidence')
ORIGINAL = BASE / 'whole-subtree-nine-endpoints-primary/original'
CERTIFICATE = BASE / 'fixed-five-player-omission-payments/fixed-policy-net-q-exact.json'
INPUTS = {
    'sigma252': ('m5p7_residual.json', '2a154303b023acfdc7b09c8576f63b3acb50abb02bd8e3cca6a793152ad07233',
                 (0, 0, 0, 1, 1), 432),
    'sigma48': ('m5p7_reentry_incumbent_half.json', 'e6269ea7551820d0d2c6192dd96d60b7bd2ce1f92b6ffd463fd8a13f89da0565',
                (0, 1, 0, 1, 0), 402),
}


def read_json(path, digest=None):
    raw = path.read_bytes()
    if digest is not None:
        assert hashlib.sha256(raw).hexdigest() == digest, path
    return json.loads(raw)


def membership(leaf):
    return tuple(sum((mask >> action) & 1 for action in leaf) for mask in MASKS)


def payoff_row(leaf, action):
    return tuple(SCALE // load if (mask >> action) & 1 else 0
                 for mask, load in zip(MASKS, membership(leaf), strict=True))


def dot(row, weights):
    return sum(coefficient * weight for coefficient, weight in zip(row, weights, strict=True))


def verify_policy(repo, spec, archived):
    name, digest, expected_actual, expected_total = spec
    exact = read_json(repo / ORIGINAL / name, digest)['exact']
    strategy = exact['strategy']
    entries = strategy['actions']
    actions = {tuple(entry['history']): entry['action'] for entry in entries}
    histories = {history for depth in range(PLAYERS) for history in product(LABELS, repeat=depth)}
    assert len(actions) == len(entries) == len(histories) == 2801
    assert actions.keys() == histories and set(actions.values()) <= set(LABELS)

    def complete(prefix):
        while len(prefix) < PLAYERS:
            prefix = (*prefix, actions[prefix])
        return prefix

    actual = complete(())
    assert actual == expected_actual
    assert [actual.count(a) for a in LABELS] == strategy['terminal_counts']
    original = exact['integer_clones']
    assert len(original) == len(MASKS) and all(isinstance(x, int) and x >= 0 for x in original)
    original_summary = exact['independent_check']
    assert original_summary['path'] == list(actual)
    assert original_summary['client_count'] == sum(original)
    assert original_summary['positive_types'] == sum(x > 0 for x in original)

    def audit_points(weights):
        comparisons = Counter()
        for history, prescribed in actions.items():
            real = dot(payoff_row(complete((*history, prescribed)), prescribed), weights)
            for alternate in LABELS:
                if alternate == prescribed:
                    continue
                forced = dot(payoff_row(complete((*history, alternate)), alternate), weights)
                assert real >= forced, (history, prescribed, alternate, real, forced)
                comparisons['strict' if real > forced else 'ties'] += 1
        assert comparisons.total() == 16806
        return comparisons

    comparisons = audit_points(original)
    assert all(comparisons[key] == original_summary[key] for key in ('strict', 'ties'))
    assert original_summary['histories'] == len(histories)
    assert original_summary['nonself_comparisons'] == comparisons.total()
    zero_comparisons = audit_points([0] * len(MASKS))
    assert zero_comparisons['ties'] == comparisons.total()

    actual_load = membership(actual)
    welfare = dot([int(c > 0) for c in actual_load], original)
    individual_payoffs = [dot(payoff_row(actual, action), original) for action in actual]
    assert sum(individual_payoffs) == SCALE * welfare == SCALE * original_summary['welfare']
    forced = {(index, action): complete((*actual[:index], action))
              for index in range(PLAYERS) for action in LABELS}
    price = {key: payoff_row(leaf, key[1]) for key, leaf in forced.items()}
    supports = list(combinations(LABELS, PLAYERS))
    assert len(supports) == len(archived) == 21
    rows = []
    passes = {}
    permutations_checked = 0
    coefficients_checked = 0
    for support, old in zip(supports, archived, strict=True):
        support_load = membership(support)
        unsigned = [d * (SCALE // (c + 1)) for c, d in zip(actual_load, support_load, strict=True)]
        credit = [SCALE * (c > 0 and d == 0) for c, d in zip(actual_load, support_load, strict=True)]
        selected_order = None
        passing = []
        for order in permutations(support):
            per_player = [price[index, action] for index, action in enumerate(order)]
            payment = list(map(sum, zip(*per_player, strict=True)))
            unsigned_slack = [p - q for p, q in zip(payment, unsigned, strict=True)]
            signed_slack = [s + e for s, e in zip(unsigned_slack, credit, strict=True)]
            for d, p, q, us, ss, e in zip(support_load, payment, unsigned, unsigned_slack,
                                            signed_slack, credit, strict=True):
                if d == 0:
                    assert p == q == us == 0
                else:
                    assert e == 0 and us == ss
            assert (min(unsigned_slack) >= 0) == (min(signed_slack) >= 0)
            if min(unsigned_slack) >= 0:
                passing.append(order)
                if selected_order is None:
                    selected_order = order
                    chosen = (per_player, unsigned_slack, signed_slack)
            permutations_checked += 1
            coefficients_checked += len(MASKS)
        assert selected_order is not None
        assert list(support) == old['support'] and list(selected_order) == old['order']
        assert len(passing) == old['paying_count']
        assert [list(forced[index, action]) for index, action in enumerate(selected_order)] == old['true_leaves']
        per_player, unsigned_slack, signed_slack = chosen
        assert [str(Fraction(s, SCALE)) for s in signed_slack] == old['slacks']
        query = Fraction(dot(unsigned, original), SCALE)
        payoff_parts = [dot(row, original) for row in per_player]
        assert all(pay <= actual_pay for pay, actual_pay in zip(payoff_parts, individual_payoffs, strict=True))
        total_payoff = Fraction(sum(payoff_parts), SCALE)
        assert query <= total_payoff <= welfare
        harmonic = sum((Fraction(weight, c + slot)
                        for c, d, weight in zip(actual_load, support_load, original, strict=True)
                        for slot in range(1, d + 1)), Fraction())
        assert harmonic <= query
        rows.append({'support': support, 'paying_count': len(passing), 'order': selected_order,
                     'true_leaves': old['true_leaves'], 'unsigned_slacks_times_60': unsigned_slack,
                     'original_clients': {'coverage': dot([int(d > 0) for d in support_load], original),
                                          'payoff': str(total_payoff), 'Q': str(query),
                                          'F': str(harmonic), 'E': dot([e // SCALE for e in credit], original)}})
        passes[support] = set(passing)

    assert permutations_checked == len(supports) * 120
    assert coefficients_checked == permutations_checked * len(MASKS)
    assert sum(len(passing) for passing in passes.values()) == expected_total
    optimum = max(row['original_clients']['coverage'] for row in rows)
    assert optimum == original_summary['optimum']
    return {'actual': actual, 'histories': len(histories), 'original_IC': comparisons,
            'zero_point_IC': zero_comparisons, 'clients': sum(original), 'W': welfare, 'OPT5': optimum,
            'permutations_checked': permutations_checked, 'type_comparisons_checked': coefficients_checked,
            'supports': rows}, passes


def main(repo):
    task_path = repo / 'research/operations/map-v2/tasks/boss3-wave10-comparison-3b-31183fbef6aadd6d.json'
    task = read_json(task_path)['definition']
    for ref in task['context_plan']['reading_refs']:
        raw = (repo / ref['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == ref['sha256'], ref
    archived = read_json(repo / CERTIFICATE, '0ade06e0a301b0a83c4d23859711fde5617acd0cdc3b0afaa7a5b65c77bfd3a4')
    audits = {name: verify_policy(repo, spec, archived[name]) for name, spec in INPUTS.items()}
    first, second = (audits[name][1] for name in INPUTS)
    common = [{'support': support, 'count': len(first[support] & second[support])} for support in first]
    print(json.dumps({'scale': SCALE, 'types': MASKS, 'task_reading_refs': len(task['context_plan']['reading_refs']),
                      'policies': {name: result for name, (result, _) in audits.items()},
                      'common_pointwise_order_counts': common}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repo', type=Path)
    main(parser.parse_args().repo)
