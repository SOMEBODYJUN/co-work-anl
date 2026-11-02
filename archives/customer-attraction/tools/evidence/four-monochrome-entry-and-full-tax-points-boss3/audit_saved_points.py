"""Four saved witnesses only: exact ordered-tree IC and static target audit.

Independent standard-library implementation. No discovery source imports,
canonical solver, LP, random generation, or change to original reports.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, combinations
from pathlib import Path
import gzip
import hashlib
import json

BASE = Path(__file__).resolve().parent


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        assert key not in result, key
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(), object_pairs_hook=unique_object)


def run():
    manifest = read_json(BASE / 'source-manifest.json')
    for source in manifest:
        raw = (BASE / source['saved_path']).read_bytes()
        assert len(raw) == source['size']
        assert hashlib.sha256(raw).hexdigest() == source['sha256']
    result, complete = [], {}
    for source in manifest:
        if not source['path'].endswith('.json') or source['path'].endswith('workspace.json'):
            continue
        report = read_json(BASE / source['saved_path'])
        assert set(report) == {'players', 'topics', 'seed', 'Q_CAG_HALF',
                              'tested_bridge', 'best_exact_score',
                              'positive_bridge_violation', 'witness', 'history',
                              'elapsed_seconds'}
        n, p = report['players'], report['topics']
        witness = report['witness']
        assert set(witness) == {'root', 'target', 'types', 'actions',
                                'exact_score', 'complete_common_nonnegative_customers'}
        mass = {int(b): F(v) for b, v in witness['types'].items()}
        assert all(0 < b < 1 << p and v > 0 for b, v in mass.items())
        actions = {}
        for item in witness['actions']:
            assert set(item) == {'h', 'a'}
            h, a = tuple(item['h']), item['a']
            assert h not in actions and 0 <= a < p
            assert len(h) < n and all(type(t) is int and 0 <= t < p for t in h)
            actions[h] = a
        expected = {h for depth in range(n) for h in product(range(p), repeat=depth)}
        assert set(actions) == expected
        assert set(actions.values()) == {0}

        @lru_cache(None)
        def finish(h):
            return h if len(h) == n else finish(h + (actions[h],))

        @lru_cache(None)
        def payoff(leaf, topic):
            return sum((v / sum(bool(b & (1 << a)) for a in leaf)
                        for b, v in mass.items() if b & (1 << topic)), F(0))

        rows, all_differences = [], []
        for h in sorted(expected, key=lambda h: (len(h), h)):
            a = actions[h]
            prescribed = payoff(finish(h), a)
            profits = [payoff(finish(h + (b,)), b) for b in range(p)]
            diff = [prescribed - v for v in profits]
            assert all(v >= 0 for v in diff), (source['id'], h, diff)
            all_differences.extend(diff)
            rows.append({'h': h, 'a': a, 'prescribed_profit': str(prescribed),
                         'deviation_profits': list(map(str, profits)),
                         'slacks': list(map(str, diff))})
        leaf = finish(())
        root = tuple(leaf.count(a) for a in range(p))
        assert root == tuple(witness['root'])
        load = {b: sum(bool(b & (1 << a)) for a in leaf) for b in mass}
        welfare = sum((v for b, v in mass.items() if load[b]), F(0))
        tau = sum((v * F(load[b], load[b] + 1) for b, v in mass.items()), F(0))
        support_values = []
        for support in combinations(range(p), min(n, p)):
            mask = sum(1 << a for a in support)
            value = sum((v for b, v in mass.items() if b & mask), F(0))
            support_values.append({'mask': mask, 'topics': support, 'coverage': str(value)})
        optimum = max(F(t['coverage']) for t in support_values)
        entry = [sum((v / (load[b] + 1) for b, v in mass.items()
                      if b & (1 << a)), F(0)) for a in range(p)]
        if 'entry_' in source['path']:
            target_value = n * entry[witness['target']]
            true_score = n * max(entry) / welfare
            assert target_value == n * max(entry)
        else:
            target_coverage = sum((v for b, v in mass.items()
                                   if b & witness['target']), F(0))
            target_value = target_coverage - tau
            true_score = (optimum - tau) / welfare
            assert target_coverage == optimum
        assert welfare == 1
        assert target_value == true_score == F(witness['exact_score']) == F(report['best_exact_score'])
        assert report['positive_bridge_violation'] is (true_score > 1)

        # All prior themes contribute to h_b. This sufficient condition uses
        # only h_b + remaining <= n and h_b + 1 >= 1, never h_A alone.
        monochrome_conditions = []
        for a in range(p):
            only_a = sum((v for b, v in mass.items()
                          if b & 1 and not b & (1 << a)), F(0))
            only_t = sum((v for b, v in mass.items()
                          if b & (1 << a) and not b & 1), F(0))
            assert only_a >= n * only_t
            monochrome_conditions.append({'topic': a, 'A_minus_topic': str(only_a),
                                           'topic_minus_A': str(only_t),
                                           'uniform_slack_lower_bound': str(only_a / n - only_t)})

        exact_rounds, missing_rounds, score_records = [], [], []
        for step, row in enumerate(report['history']):
            assert row['round'] == step
            assert set(row) in ({'round', 'root', 'target', 'unique_true_rows',
                                 'ordered_histories', 'LP_success'},
                                {'round', 'root', 'target', 'unique_true_rows',
                                 'ordered_histories', 'LP_success', 'exact_O_minus_tau_over_W'})
            assert row['LP_success'] is True and row['ordered_histories'] == len(actions)
            assert len(row['root']) == p and sum(row['root']) == n
            if 'exact_O_minus_tau_over_W' in row:
                exact_rounds.append(step)
                score_records.append(F(row['exact_O_minus_tau_over_W']))
            else:
                missing_rounds.append(step)
        assert max(score_records) == F(report['best_exact_score'])
        hist = {'records': len(report['history']), 'LP_success_true': len(report['history']),
                'exact_score_records': len(exact_rounds), 'missing_exact_score_rounds': missing_rounds,
                'original_elapsed_seconds': report['elapsed_seconds']}
        strict = sum(v > 0 for v in all_differences)
        ties = len(all_differences) - strict
        result.append({'source_id': source['id'], 'source_sha256': source['sha256'],
                       'players': n, 'topics': p, 'positive_types': witness['types'],
                       'complete_ordered_keys': len(actions), 'depth_counts': dict(Counter(map(len, actions))),
                       'all_actions_zero': True, 'IC_comparisons_including_self': len(all_differences),
                       'strict_comparisons': strict, 'tie_comparisons_including_self': ties,
                       'minimum_slack': str(min(all_differences)), 'actual_leaf': leaf,
                       'root': root, 'actual_profits': [str(payoff(leaf, a)) for a in leaf],
                       'W': str(welfare), 'tau_full': str(tau), 'OPT': str(optimum),
                       'full_tax_slack': str(welfare + tau - optimum),
                       'entry_values': list(map(str, entry)),
                       'entry_ratio': str(n * max(entry) / welfare),
                       'entry_gap': str(n * max(entry) - welfare),
                       'all_max_cover_supports': [v for v in support_values if F(v['coverage']) == optimum],
                       'saved_target_score': str(target_value), 'score_is_true_target_maximum_at_point': True,
                       'monochrome_pairwise_sufficient_conditions': monochrome_conditions,
                       'source_history_scope': hist})
        complete[source['id']] = {'all_ordered_IC_rows': rows, 'all_comparison_supports': support_values}
        finish.cache_clear()
        payoff.cache_clear()
    out = {'scope': 'four frozen saved points only; no LP or cone optimality claim',
           'source_manifest_sha256': hashlib.sha256((BASE / 'source-manifest.json').read_bytes()).hexdigest(),
           'original_main_runs': 0, 'LP_runs': 0, 'BI_runs': 0, 'random_runs': 0,
           'new_saved_point_audit_passes': 1, 'results': result}
    (BASE / 'replay/exact-saved-point-review.json').write_text(json.dumps(out, indent=2) + '\n')
    raw = (json.dumps(complete, separators=(',', ':')) + '\n').encode()
    with (BASE / 'replay/complete-ordered-IC-and-comparison-supports.json.gz').open('wb') as f:
        with gzip.GzipFile(fileobj=f, mode='wb', mtime=0) as z:
            z.write(raw)
    print(json.dumps({'saved_points': len(result),
                      'complete_ordered_keys': sum(v['complete_ordered_keys'] for v in result),
                      'exact_IC_comparisons': sum(v['IC_comparisons_including_self'] for v in result),
                      'original_history_records_read': sum(v['source_history_scope']['records'] for v in result),
                      'complete_IC_uncompressed_bytes': len(raw),
                      'complete_IC_uncompressed_sha256': hashlib.sha256(raw).hexdigest(),
                      'all_passed': True}))


if __name__ == '__main__':
    run()
