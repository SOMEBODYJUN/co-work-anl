#!/usr/bin/env python3
"""Exact definition-level audit of the saved 0123 joint report, never an optimizer.

The two raw number interpretations are kept separate. No coordinates are
rounded, normalized, repaired, or replaced. No original module is imported.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
import gzip
import hashlib
from itertools import combinations_with_replacement, product
import json
from math import comb
from pathlib import Path


def fingerprint(path):
    raw = Path(path).read_bytes()
    return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(),
                git_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest())


def load(path, mode):
    parser = F if mode == 'decimal_tokens' else lambda token: F(float(token))
    return json.loads(Path(path).read_text(), parse_float=parser)


def count(h, k):
    return tuple(h.count(a) for a in range(k))


def analyze(path, mode):
    data = load(path, mode)
    k, n = data['k'], data['n']
    weights = list(map(F, data['weights']))
    p, q = list(map(F, data['p'])), list(map(F, data['Q']))
    histories = [h for depth in range(n) for h in product(range(k), repeat=depth)]
    nodes = [count(h, k) for depth in range(n)
             for h in combinations_with_replacement(range(k), depth)]
    policy = {tuple(row['history']): row['action'] for row in data['full_policy']}
    counted = {tuple(row['counts']): row['action'] for row in data['count_policy']}
    assert len(policy) == len(data['full_policy']) == len(histories)
    assert len(counted) == len(data['count_policy']) == len(nodes)
    assert set(policy) == set(histories) and set(counted) == set(nodes)
    assert all(0 <= policy[h] < k and policy[h] == counted[count(h, k)] for h in histories)
    assert len(weights) == (1 << k)-1 and len(p) == k
    assert all(weight == 0 for weight in weights[:-1]) and weights[-1] > 0
    rivals = list(combinations_with_replacement(range(k), n-3))
    assert list(map(tuple, data['tail_rivals'])) == rivals and len(q) == len(rivals)

    @lru_cache(None)
    def finish(h):
        return h if len(h) == n else finish(h+(policy[h],))

    def payoff(action, leaf):
        total = F(0)
        for mask, mass in enumerate(weights, 1):
            if mass and mask & (1 << action):
                load = sum(bool(mask & (1 << a)) for a in leaf)
                assert load > 0
                total += mass/load
        return total

    ledger = []
    for h in histories:
        prescribed = policy[h]
        actual_leaf = finish(h)
        actual = payoff(prescribed, actual_leaf)
        for deviation in range(k):
            deviation_leaf = finish(h+(deviation,))
            alternative = payoff(deviation, deviation_leaf)
            ledger.append(dict(history=h, prescribed=prescribed, deviation=deviation,
                               actual_leaf=actual_leaf, deviation_leaf=deviation_leaf,
                               actual_payoff=str(actual), deviation_payoff=str(alternative),
                               slack=str(actual-alternative)))
    values = [F(row['slack']) for row in ledger]
    assert all(value == 0 for value in values)
    leaf = finish(())
    assert list(leaf) == data['path'] == [0, 1, 2, 3]
    assert list(count(leaf, k)) == data['actual_root_counts']

    def query(action, background):
        return sum((mass/(1+sum(bool(mask & (1 << a)) for a in background))
                    for mask, mass in enumerate(weights, 1) if mask & (1 << action)), F(0))

    root_rows = []
    for background in combinations_with_replacement(range(k), n-1):
        pure = [query(action, background) for action in range(k)]
        root_rows.append(dict(background=background, pure_payoffs=list(map(str, pure)),
                              mixed=str(sum((x*y for x, y in zip(p, pure)), F(0)))))
    tail_rows = []
    for action in range(k):
        pure = [query(action, leaf[:2]+rival) for rival in rivals]
        tail_rows.append(dict(action=action, by_rival=list(map(str, pure)),
                              mixed=str(sum((x*y for x, y in zip(q, pure)), F(0)))))
    ell = min(F(row['mixed']) for row in root_rows)
    cap = max(F(row['mixed']) for row in tail_rows)
    pair = payoff(leaf[0], leaf)+payoff(leaf[1], leaf)
    formal_gap = pair-n*ell+(n-2)*cap
    mass = weights[-1]
    assert all(F(value) == mass/n for row in root_rows for value in row['pure_payoffs'])
    assert all(F(value) == mass/n for row in tail_rows for value in row['by_rival'])
    assert sum(p) == sum(q) < 1
    assert ell == cap == mass*sum(p)/n
    assert formal_gap == mass*(1-sum(p))/2 > 0
    stats = dict(
        interpretation=mode, mass=str(mass), mass_minus_one=str(mass-1),
        mass_nonnegative=True, zero_weights=62, positive_weights=1, negative_weights=0,
        p_sum=str(sum(p)), q_sum=str(sum(q)), probability_sum_minus_one=str(sum(p)-1),
        count_nodes=len(counted), count_depths=dict(Counter(map(sum, counted))),
        ordered_nodes=len(policy), ordered_depths=dict(Counter(map(len, policy))),
        all_count_to_ordered_actions_equal=True, actual_path=leaf, actual_counts=count(leaf, k),
        comparisons=len(ledger), self_comparisons=len(histories), nonself_comparisons=len(ledger)-len(histories),
        negative_IC=sum(value < 0 for value in values), zero_IC=sum(value == 0 for value in values),
        positive_IC=sum(value > 0 for value in values), minimum_IC=str(min(values)),
        stored_floating_min_full_Gamma=str(data['floating_min_full_Gamma']),
        every_actual_and_deviation_payoff=str(mass/n), root_backgrounds=len(root_rows), tail_queries=len(tail_rows),
        root_min_formal=str(ell), tail_max_formal=str(cap), actual_pair_payoff=str(pair),
        reconstructed_tight_formal_surrogate=str(formal_gap), reconstructed_tight_formal_surrogate_float=float(formal_gap),
        stored_objective=str(data['objective']), actual_welfare=str(mass), static_opt_4=str(mass),
        legal_distribution_root_and_tail_security=str(mass/n), legal_distribution_PAIR_gap='0',
        search_mass_equality_satisfied=False, frozen_source_universal_zero_bound_satisfied=False,
        raw_p_and_q_are_probability_distributions=False,
        note='Nonnegative rational label-game masses and zero IC; not a feasible saved vector for the current normalized, universal-stripped MILP. Formal mixed rows use raw nonunit p/Q, not probability/security certificates.')
    details = dict(interpretation=mode, full_history_comparisons=ledger,
                   root_query_rows=root_rows, tail_query_rows=tail_rows)
    return stats, details


def main():
    parser = argparse.ArgumentParser()
    for key in ('normal', 'strip', 'source', 'out'):
        parser.add_argument('--'+key, type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    normal = json.loads(args.normal.read_text())
    strip = json.loads(args.strip.read_text())
    tokenized = json.loads(args.normal.read_text(), parse_float=str)
    common = ('status', 'k', 'n', 'path', 'p', 'Q', 'tail_rivals', 'milp_status', 'variables', 'binaries', 'rows')
    assert all(normal[key] == strip[key] for key in common)
    assert len(normal) == 19 and len(strip) == 14
    assert strip['objective'] is None and 'weights' not in strip and 'full_policy' not in strip
    assert 'upper[s.k-1]=0' in args.source.read_text()
    k, n = normal['k'], normal['n']
    count_nodes = comb(k+n-1, n-1)
    dimensions = dict(types=(1 << k)-1, count_nodes=count_nodes,
                      variables=(1 << k)-1+2*k*count_nodes+2, binaries=k*count_nodes,
                      rows=1+count_nodes*(1+k*(3*k-1))+comb(k+n-2, n-1)+k)
    assert all(normal[key] == dimensions[key] for key in ('variables', 'binaries', 'rows'))
    cases, ledgers = [], []
    for mode in ('decimal_tokens', 'decoded_binary_floats'):
        stats, details = analyze(args.normal, mode)
        cases.append(stats)
        ledgers.append(details)
    raw = (json.dumps(ledgers, ensure_ascii=False, indent=2)+'\n').encode()
    packed = gzip.compress(raw, mtime=0)
    (args.out/'full-history-ledger.json.gz').write_bytes(packed)
    report = dict(
        status='PASS: 0123 report structure and definition-level exact audit; all saved IC zero, current MILP feasibility not established',
        scope=dict(original_main=0, original_functions=0, MILP=0, LP=0, random_search=0,
                   independent_standard_library_audit=1, primary_incumbents=1, input_interpretations=2,
                   full_history_comparisons=sum(case['comparisons'] for case in cases),
                   other_0012_report_mathematical_reruns=0, rounded_repaired_or_normalized_inputs=0),
        inputs={key:dict(path=str(getattr(args, key)), **fingerprint(getattr(args, key))) for key in ('normal', 'strip', 'source')},
        normal_all_field_names=list(normal), normal_weight_original_tokens=tokenized['weights'],
        normal_zero_token_counts=dict(Counter(tokenized['weights'][:-1])),
        dimensions=dimensions, strip_all_fields=strip,
        strip_conclusion='Time limit with no saved incumbent; not infeasibility or an optimality certificate',
        interpretations=cases,
        ledger=dict(path='full-history-ledger.json.gz', compressed=fingerprint(args.out/'full-history-ledger.json.gz'),
                    decoded_bytes=len(raw), decoded_sha256=hashlib.sha256(raw).hexdigest()))
    (args.out/'exact-audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(dict(status=report['status'], comparisons=report['scope']['full_history_comparisons'],
                          cases=[{key:case[key] for key in ('interpretation', 'negative_weights', 'negative_IC', 'zero_IC', 'positive_IC', 'mass', 'reconstructed_tight_formal_surrogate')} for case in cases]), ensure_ascii=False))


if __name__ == '__main__':
    main()
