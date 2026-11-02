"""Exact fixed-input audit; no native discovery import, random search, or LP."""
import argparse
import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

P, M = 7, 5
SOURCE_IDS = ('0cb147cb164868b3ce3d', '373f8d3e4214a69041c0', '4a775c14bcf81f04c4f2')

def compact(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()

def sha(value):
    return hashlib.sha256(compact(value)).hexdigest()

def types(instance):
    assert instance['players'] == M and len(instance['topics']) == P
    weights = [0] * ((1 << P) - 1)
    for row in instance['customers']:
        mask = sum(1 << a for a in row['topics'])
        assert mask and isinstance(row['multiplicity'], int) and row['multiplicity'] > 0
        weights[mask - 1] += row['multiplicity']
    return weights

def sparse(weights):
    assert len(weights) == 127 and all(isinstance(w, int) and w >= 0 for w in weights)
    return [[i + 1, w] for i, w in enumerate(weights) if w]

def profit(weights, leaf, player):
    a = leaf[player]
    return sum((F(w, sum(bool(mask >> b & 1) for b in leaf))
                for mask, w in sparse(weights) if mask >> a & 1), F(0))

def query(weights, counts):
    return [sum((F(w * M, M + (M - 1) * sum(counts[b] for b in range(P) if mask >> b & 1))
                 for mask, w in sparse(weights) if mask >> a & 1), F(0)) for a in range(P)]

def welfare(weights, counts):
    support = sum(1 << a for a, count in enumerate(counts) if count)
    return sum(w for mask, w in sparse(weights) if mask & support)

def optimum(weights):
    return max(sum(w for mask, w in sparse(weights) if mask & support)
               for support in range(1 << P) if support.bit_count() <= M)

def audit(weights, policy, histories):
    def finish(history):
        h = tuple(history)
        while len(h) < M:
            h += (policy[h],)
        return h
    actual = finish(())
    counts = [actual.count(a) for a in range(P)]
    payloads, payload_index, by_depth = [], {}, [[] for _ in range(M)]
    strict = ties = including = proper = 0
    min_proper = None
    for h in histories:
        i = len(h)
        prescribed = profit(weights, finish(h), i)
        forced = [profit(weights, finish(h + (a,)), i) for a in range(P)]
        key = tuple(str(x) for x in [prescribed, *forced])
        if key not in payload_index:
            payload_index[key] = len(payloads)
            payloads.append(list(key))
        by_depth[i].append(payload_index[key])
        for a, alternative in enumerate(forced):
            gap = prescribed - alternative
            assert gap >= 0, (h, a, gap)
            including += 1
            if a != policy[h]:
                proper += 1
                strict += gap > 0
                ties += gap == 0
                min_proper = gap if min_proper is None else min(min_proper, gap)
    W = welfare(weights, counts)
    qs = query(weights, counts)
    return {
        'sparse_types': sparse(weights), 'unit_customers': sum(weights),
        'actual_path': list(actual), 'terminal_counts': counts, 'welfare': W,
        'optimum_at_most_five_labels': optimum(weights), 'actual_query_values': [str(x) for x in qs],
        'weak_score': str(F(2 * M - 1, 2) * max(qs) / W),
        'histories': len(histories), 'comparisons_including_prescribed': including,
        'proper_comparisons': proper, 'strict_proper': strict, 'tied_proper': ties,
        'minimum_proper_gap': str(min_proper),
        'payoff_payload_format': ['prescribed', 'forced_0', 'forced_1', 'forced_2', 'forced_3', 'forced_4', 'forced_5', 'forced_6'],
        'payoff_payloads': payloads,
        'payoff_indices_by_depth_lex_history': by_depth,
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads((args.evidence / 'source-manifest.json').read_text())
    loaded, bindings = {}, []
    for item in manifest:
        tail = Path(item['preserved_path']).relative_to(Path('archives/customer-attraction/tools/evidence/r8e450-counter-fractional-primary'))
        raw = (args.evidence / tail).read_bytes()
        assert len(raw) == item['size'] and hashlib.sha256(raw).hexdigest() == item['sha256']
        blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        assert blob == item['blob']
        bindings.append({k: item[k] for k in ('id', 'size', 'sha256', 'blob', 'path')})
        loaded[item['id']] = raw
    assert set(loaded) == set(SOURCE_IDS)
    best = json.loads(loaded[SOURCE_IDS[1]])
    results = json.loads(loaded[SOURCE_IDS[2]])
    assert set(results) == {'scope', 'seed', 'records'} and results['seed'] == 21010951
    records = results['records']
    assert len(records) == 8 and best == records[0]
    strategy = best['strategy']
    assert set(strategy) == {'terminal_counts', 'actions'}
    histories = [h for depth in range(M) for h in itertools.product(range(P), repeat=depth)]
    actions = strategy['actions']
    assert all(set(x) == {'history', 'action'} for x in actions)
    policy = {tuple(x['history']): x['action'] for x in actions}
    assert len(actions) == len(policy) == len(histories) == 2801 and set(policy) == set(histories)
    assert set(policy.values()) == {0} and strategy['terminal_counts'] == [5, 0, 0, 0, 0, 0, 0]
    normal_actions = [{'history': list(h), 'action': policy[h]} for h in histories]
    rows, nonnull = [], 0
    for step, record in enumerate(records):
        expected = {'step', 'source', 'root', 'stats', 'query_scores', 'top'} | ({'strategy'} if step == 0 else set())
        assert set(record) == expected and record['step'] == step
        assert set(record['stats']) == {'non_minimal_off_path_nodes', 'off_path_nodes'}
        assert record['stats']['off_path_nodes'] == 16806
        source = types(record['source'])
        assert len(record['root']) == P and sum(record['root']) == M
        probes = record['query_scores']
        assert len(probes) == P and [r['a'] for r in probes] == list(range(P))
        for probe in probes:
            assert set(probe) == {'a', 'value', 'score', 'dual_bound'}
            assert F(probe['value']) == F(1, 5) and F(probe['score']) == F(9, 10)
            assert probe['dual_bound'] is None or F(probe['dual_bound']) == F(1, 5)
            nonnull += probe['dual_bound'] is not None
        top = record['top']
        assert set(top) == {'a', 'value', 'score', 'clones', 'dual_bound'}
        assert {k: v for k, v in top.items() if k != 'clones'} == probes[0]
        top_weights = top['clones']
        assert sum(top_weights) == 1
        top_W = welfare(top_weights, record['root'])
        top_queries = query(top_weights, record['root'])
        assert top_W == 1 and top_queries[0] == F(1, 5)
        rows.append({
            'step': step, 'source_types': sparse(source), 'source_vector_sha256': sha(source),
            'source_customers': sum(source), 'root': record['root'], 'stats': record['stats'],
            'source_actual_welfare_from_reported_root': welfare(source, record['root']),
            'source_optimum': optimum(source),
            'top_types': sparse(top_weights), 'top_vector_sha256': sha(top_weights),
            'top_W_from_reported_root': top_W, 'top_actual_query_vector': [str(x) for x in top_queries],
            'reported_query_scores': probes,
            'original_full_policy_present': 'strategy' in record,
        })
    assert nonnull == 22
    audits = {
        'step0_source_eleven': audit(types(best['source']), policy, histories),
        'step0_top_one': audit(best['top']['clones'], policy, histories),
    }
    # A separate exact certificate for the seven objectives in this fixed constant-0 cone.
    coefficients = []
    for a in range(P):
        entries = []
        for mask in range(1, 1 << P):
            c = F(bool(mask & 1))
            prescribed = c / M
            obj = F(M, M + (M - 1) * M * bool(mask & 1)) if mask >> a & 1 else F(0)
            actual_root_deviation = F(1, 1 + (M - 1) * bool(mask & 1)) if mask >> a & 1 else F(0)
            gamma = prescribed - actual_root_deviation
            assert obj == actual_root_deviation and c / M - obj == gamma
            entries.append([str(c), str(obj), str(gamma)])
        coefficients.append({'query': a, 'columns_c_objective_root_IC': entries})
    # One all-interest unit customer is a common normalized lower point: every leaf payoff is 1/5.
    lower = [0] * 126 + [1]
    assert query(lower, [5, 0, 0, 0, 0, 0, 0]) == [F(1, 5)] * P
    output = {
        'status': 'pass', 'method': 'Python standard library exact Fraction; two fixed input games only',
        'native_discovery_runs': 0, 'LP_runs': 0, 'random_runs': 0,
        'source_bindings': bindings, 'best_equals_record_zero': True,
        'complete_policy': {'decision_histories': 2801, 'actions_sorted_depth_lex_compact_sort_keys_sha256': sha(normal_actions),
                            'terminal_counts': strategy['terminal_counts'], 'constant_action': 0,
                            'off_actual_decision_histories': 2796},
        'saved_prefix': {'records': 8, 'source_loop_steps': 18, 'full_strategy_records': [0],
                         'query_entries': 56, 'nonnull_scalar_bounds': 22, 'null_scalar_bounds': 34,
                         'original_dual_multipliers_saved': False, 'record_details': rows},
        'fixed_game_audits': audits,
        'independent_step0_cone_certificate': {
            'scope': 'the complete constant-0 policy cone, not later unsaved policies',
            'normalization': 'actual welfare=1', 'upper_beta': '1/5',
            'upper_proof': 'query 0 identity; each other query uses the corresponding root IC with multiplier 1',
            'all_889_column_identities': coefficients,
            'common_feasible_lower_point_types': sparse(lower),
            'lower_point_argument': 'all seven labels cover this one customer, so every terminal has five coverers and every player payoff is 1/5 at every history',
            'all_seven_exact_optima': ['1/5'] * P,
            'original_saved_dual_reconstructed': False,
        },
        'limitations': ['records 1..7 lack original full strategies',
                        'scalar dual bounds lack original multipliers and row indexing',
                        'top clones are only the winning query point; the other six per-query clone vectors were not saved',
                        'no explanation for eight saved records versus eighteen source iterations is inferred'],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': output['status'], 'fixed_games': {k: {a: v[a] for a in ('histories', 'proper_comparisons', 'strict_proper', 'tied_proper', 'welfare', 'optimum_at_most_five_labels')} for k, v in audits.items()}, 'query_entries': 56, 'nonnull_scalar_bounds': nonnull, 'output_sha256': hashlib.sha256(args.output.read_bytes()).hexdigest()}, sort_keys=True))

if __name__ == '__main__':
    main()
