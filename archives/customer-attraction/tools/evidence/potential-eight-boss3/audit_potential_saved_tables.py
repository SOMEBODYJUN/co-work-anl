"""Exact definition review of two frozen finite potential tables and five logs.

No original program, LP, backward induction, or random search is executed.
"""
import argparse
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib
import json
import platform
import time


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--evidence', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    start = time.time()
    tick = time.monotonic()
    manifest = json.loads((args.evidence / 'source-manifest.json').read_text())
    objects = {}
    for row in manifest:
        p = args.evidence / 'original' / row['id'] / Path(row['path']).name
        data = p.read_bytes()
        assert len(data) == row['size'] and hashlib.sha256(data).hexdigest() == row['sha256']
        if p.suffix == '.json':
            objects[p.name] = json.loads(data)
    related = {}
    for row in json.loads((args.evidence / 'related-input-manifest.json').read_text()):
        p = args.evidence / row['evidence_path']
        data = p.read_bytes()
        assert len(data) == row['size'] and hashlib.sha256(data).hexdigest() == row['sha256']
        related[row['path']] = json.loads(data)
    histories = {}
    for source, data in related.items():
        s = data.get('strategy', data)
        actions = {tuple(v['history']): v['action'] for v in s['actions']}
        assert len(actions) == len(s['actions'])
        k = 1 + max([*actions.values(), *[a for h in actions for a in h]])
        m = max(map(len, actions)) + 1
        assert set(actions) == {h for j in range(m) for h in product(range(k), repeat=j)}
        histories[source] = (actions, k, m)
    logs = []
    for name, data in objects.items():
        if not name.startswith('potential_'):
            continue
        actions, k, m = histories[data['source']]
        assert (k, m) == (data['topics'], data['players'])
        rows = []
        for j, row in enumerate(data['queries']):
            p = tuple(map(F, row['query']))
            assert len(p) == k and sum(p) == 1 and min(p) >= 0
            if 'exact_candidate' in row:
                target = Path(row['exact_candidate']).name
                assert target in objects and objects[target]['query'] == row['query']
            rows.append({'index': j, 'query': list(map(str, p)),
                         'numerical_gap': row['numerical_gap'],
                         'exact_candidate': row.get('exact_candidate')})
        logs.append({'file': name, 'source': data['source'], 'k': k, 'm': m,
                     'complete_policy_nodes': len(actions), 'queries': rows,
                     'mode_flags_recorded_in_report': sorted(set(data) & {'strong', 'moments'}),
                     'significant_negative_indices': [i for i, row in enumerate(rows) if row['numerical_gap'] < -1e-8],
                     'all_nonzero_indices': [i for i, row in enumerate(rows) if row['numerical_gap'] != 0]})
    all_queries = [tuple(row['query']) for log in logs for row in log['queries']]
    reference = objects['potential_moments_individual.json']['queries']
    assert all([row['query'] for row in data['queries']] == [row['query'] for row in reference[:len(data['queries'])]]
               for name, data in objects.items() if name.startswith('potential_'))
    report = {'source_bytes': sum(x['size'] for x in manifest), 'primary_sources': len(manifest),
              'log_records': len(all_queries), 'distinct_query_vectors': len(set(all_queries)),
              'all_logs_share_same_query_prefix': True, 'logs': logs, 'candidates': []}
    complete_rows = {}
    original_actions = histories['evidence/certificates/customer_attraction/individual_security_failure.json'][0]
    for name in ['candidate_potential_individual.json', 'candidate_potential_strong_individual.json']:
        data = objects[name]
        k, m = data['topics'], data['players']
        assert (k, m) == (6, 3)
        domain = sorted((q for q in product(range(m + 1), repeat=k) if sum(q) <= m), key=lambda q: (sum(q), q))
        phi = {tuple(x['counts']): F(x['value']) for x in data['potential']}
        assert len(phi) == len(data['potential']) == len(domain) == 84 and set(phi) == set(domain)
        zero = (0,) * k
        assert phi[zero] == 0 and all(v.denominator == 1 for v in phi.values())
        actions = {tuple(x['history']): x['action'] for x in data['actions']}
        assert len(actions) == len(data['actions']) == 43 and actions == original_actions
        p = tuple(map(F, data['query']))
        assert sum(p) == 1 and min(p) >= 0
        value = F(data['safety_lower_bound'])
        def add(q, a):
            out = list(q); out[a] += 1; return tuple(out)
        def sub(q, a):
            out = list(q); out[a] -= 1; assert out[a] >= 0; return tuple(out)
        def delta(q, a):
            return phi[add(q, a)] - phi[q]
        def pay(q, a):
            return phi[q] - phi[sub(q, a)]
        def welfare(q):
            return sum((q[a] * pay(q, a) for a in range(k) if q[a]), F(0))
        def counts(h):
            return tuple(h.count(a) for a in range(k))
        @lru_cache(None)
        def finish(h):
            return h if len(h) == m else finish(h + (actions[h],))
        rows = defaultdict(list)
        for q in domain:
            if sum(q) < m:
                for a in range(k):
                    rows['monotonicity'].append({'q': q, 'a': a, 'slack': str(delta(q, a))})
            if sum(q) <= m - 2:
                for a in range(k):
                    for b in range(k):
                        rows['DR'].append({'q': q, 'a': a, 'b': b, 'slack': str(delta(q, a) - delta(add(q, b), a))})
                        rows['self_congestion'].append({'q': q, 'a': a, 'b': b,
                            'slack': str(delta(add(q, b), a) - delta(add(q, a), a))})
            if sum(q) == m - 1:
                expected = sum((p[a] * delta(q, a) for a in range(k)), F(0))
                rows['static_safety'].append({'background': q, 'expected': str(expected), 'slack': str(expected - value)})
            if sum(q):
                support = tuple(int(x > 0) for x in q)
                rows['common_support_efficiency'].append({'q': q, 'support': support,
                    'Wq': str(welfare(q)), 'Wsupport': str(welfare(support)), 'error': str(welfare(q) - welfare(support))})
                for a in range(k):
                    if not q[a]: continue
                    for b in range(k):
                        if b == a or not q[b]: continue
                        z = add(sub(q, b), a)
                        rows['sharp_transfer'].append({'q': q, 'a': a, 'from': b,
                            'slack': str((q[a] + 1) * pay(z, a) - q[a] * pay(q, a))})
        for a in range(k):
            singleton = add(zero, a)
            for t in range(1, m + 1):
                q = tuple(t if j == a else 0 for j in range(k))
                rows['pure_harmonic'].append({'a': a, 't': t, 'phi': str(phi[q]),
                    'expected': str(sum((F(1, j) for j in range(1, t + 1)), F(0)) * phi[singleton]),
                    'error': str(phi[q] - sum((F(1, j) for j in range(1, t + 1)), F(0)) * phi[singleton])})
        for h, chosen in sorted(actions.items(), key=lambda x: (len(x[0]), x[0])):
            on = pay(counts(finish(h)), chosen)
            for b in range(k):
                alt = pay(counts(finish(h + (b,))), b)
                rows['SPE'].append({'history': h, 'chosen': chosen, 'deviation': b,
                                    'chosen_payoff': str(on), 'deviation_payoff': str(alt), 'slack': str(on - alt)})
        required = ['monotonicity', 'DR', 'self_congestion', 'SPE', 'static_safety']
        for family in required:
            assert min(F(x['slack']) for x in rows[family]) >= 0
            assert str(min(F(x['slack']) for x in rows[family])) == data['min_slacks'][family]
        strong = data.get('strong_CAG_constraints', False)
        if strong:
            assert min(F(x['slack']) for x in rows['sharp_transfer']) >= 0
            assert not any(F(x['error']) for x in rows['pure_harmonic'])
        path = finish(())
        actual = counts(path)
        profits = [pay(actual, a) for a in path]
        W = welfare(actual)
        assert list(actual) == data['actual_counts'] and W == F(data['welfare'])
        assert W - m * value == F(data['gap']) < 0
        support_groups = defaultdict(list)
        for q in domain:
            if sum(q) == m:
                support_groups[tuple(a for a in range(k) if q[a])].append((q, welfare(q)))
        unequal = [{'support': support, 'states': [{'q': q, 'W': str(v)} for q, v in values]}
                   for support, values in sorted(support_groups.items()) if len({v for _, v in values}) > 1]
        sharp = []
        minimum_K = F(0)
        gamma_one_failures = 0
        for a in range(k):
            states = [q for q in domain if sum(q) == m and q[a]]
            subsets = [mask for mask in range(1 << k) if mask & (1 << a)]
            for q in states:
                for z in states:
                    if q == z: continue
                    gamma = max(F(sum(z[b] for b in range(k) if mask & (1 << b)),
                                  sum(q[b] for b in range(k) if mask & (1 << b))) for mask in subsets)
                    slack = gamma * pay(z, a) - pay(q, a)
                    assert gamma >= 1
                    if gamma == 1:
                        gamma_one_failures += slack < 0
                        bound = None
                    else:
                        bound = -slack / (gamma - 1)
                        minimum_K = max(minimum_K, bound)
                    sharp.append({'q': q, 'r': z, 'a': a, 'gamma': str(gamma), 'slack': str(slack),
                                  'required_shift': None if bound is None else str(bound)})
        assert len(sharp) == 2520 and gamma_one_failures == 0
        for row in sharp:
            row['slack_after_minimum_shift'] = str(F(row['slack']) + (F(row['gamma']) - 1) * minimum_K)
            assert F(row['slack_after_minimum_shift']) >= 0
        rows['all_terminal_sharp'] = sharp
        max_singleton = max(phi[add(zero, a)] for a in range(k))
        summary = {'file': name, 'raw_keys': list(data), 'strong_flag': data.get('strong_CAG_constraints'),
                   'moments_flag': data.get('common_support_efficiency'), 'potential_states': len(phi),
                   'complete_histories': len(actions), 'matches_original_individual_policy': True,
                   'actual_path': path, 'actual_counts': actual, 'profits': list(map(str, profits)),
                   'W': str(W), 'saved_lower_bound': str(value),
                   'exact_fixed_query_minimum': str(min(F(x['expected']) for x in rows['static_safety'])),
                   'gap': str(W - m * value), 'max_singleton': str(max_singleton),
                   'normalized_gap_by_max_singleton': str((W - m * value) / max_singleton),
                   'row_counts': {family: len(values) for family, values in rows.items()},
                   'row_minima': {family: str(min(F(x['slack']) for x in rows[family])) for family in required},
                   'pure_harmonic_nonzero_count': sum(F(x['error']) != 0 for x in rows['pure_harmonic']),
                   'minimum_sharp_transfer': str(min(F(x['slack']) for x in rows['sharp_transfer'])),
                   'all_population_support_efficiency_nonzero_count': sum(F(x['error']) != 0 for x in rows['common_support_efficiency']),
                   'full_population_unequal_support_groups': unequal,
                   'all_terminal_sharp_negative_count': sum(F(x['slack']) < 0 for x in sharp),
                   'all_terminal_sharp_gamma_one_count': sum(F(x['gamma']) == 1 for x in sharp),
                   'least_common_nonnegative_shift_for_all_terminal_sharp': str(minimum_K)}
        report['candidates'].append(summary)
        complete_rows[name] = rows
        print(json.dumps({k: summary[k] for k in ['file', 'W', 'exact_fixed_query_minimum', 'gap',
              'minimum_sharp_transfer', 'all_terminal_sharp_negative_count',
              'least_common_nonnegative_shift_for_all_terminal_sharp']}, ensure_ascii=False), flush=True)
    dump(args.output / 'review.json', report)
    dump(args.output / 'all-exact-rows.json', complete_rows)
    event = {'started_unix': start, 'elapsed_seconds': time.monotonic() - tick,
             'python': platform.python_version(), 'assertions_enabled': __debug__,
             'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             'checker_invocations': 1, 'original_imports_CLI_LP_MIP_BI_random_search': 0,
             'output_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                              for p in sorted(args.output.iterdir()) if p.is_file()},
             'result': 'two exact finite potential counterexamples verified; no original-customer realization claimed'}
    dump(args.output / 'event.json', event)
    print(json.dumps(event, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
