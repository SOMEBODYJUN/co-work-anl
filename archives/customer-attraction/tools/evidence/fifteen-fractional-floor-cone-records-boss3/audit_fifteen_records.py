"""Exact saved-data identity and special full-count-policy audit, no optimizer.

Never imports the discovery programs, Search, NumPy, SciPy, or canonical BI.
All original decimal/binary floats are retained; exact source-row recovery and
new rational static witnesses are separately identified.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement, product
from pathlib import Path
import gzip
import hashlib
import json
import math

BASE = Path(__file__).resolve().parent


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        assert key not in obj
        obj[key] = value
    return obj


def compact(value):
    return json.dumps(value, separators=(',', ':'), allow_nan=False)


def sha(value):
    return hashlib.sha256(compact(value).encode()).hexdigest()


def counts(length, topics):
    return [tuple(labels.count(a) for a in range(topics))
            for labels in combinations_with_replacement(range(topics), length)]


def inc(q, a):
    return tuple(v + (j == a) for j, v in enumerate(q))


def run():
    manifest = json.loads((BASE / 'source-manifest.json').read_text())
    source = manifest[0]
    raw = (BASE / source['saved_path']).read_bytes()
    assert len(raw) == source['size'] and hashlib.sha256(raw).hexdigest() == source['sha256']
    data = json.loads(raw, object_pairs_hook=unique_object)
    assert set(data) == {'status', 'results'}
    assert data['status'] == 'NUMERIC_EXPLORATION_ONLY'
    records = data['results']
    assert len(records) == 15
    fields = ('status', 'n', 'k', 'kind', 'initial', 'root_counts', 'root_action',
              'weights', 'trace', 'root_query', 'root_z', 'root_fractional_q',
              'policy', 'rows')
    groups = {}
    for field in fields:
        values = {}
        for index, record in enumerate(records):
            assert set(record) == set(fields)
            key = compact(record[field])
            if key not in values:
                values[key] = {'indices': [], 'canonical_field_sha256': sha(record[field])}
            values[key]['indices'].append(index)
        groups[field] = list(values.values())
    assert all(len(groups[key]) == (2 if key in ('initial', 'trace') else 1)
               for key in fields)
    full_groups = {}
    for i, r in enumerate(records):
        full_groups.setdefault(sha(r), []).append(i)

    # Do not treat a compressed (q,target) map as generally count-Markov.
    # The current file is exceptional: every nonterminal count appears once.
    first = records[0]
    n, k = first['n'], first['k']
    assert n == 4 and k == 6
    final = counts(n, k)
    all_prefixes = {q for depth in range(n) for q in counts(depth, k)}
    policy = {}
    for item in first['policy']:
        assert set(item) == {'prefix', 'target', 'action'}
        q, t, a = tuple(item['prefix']), item['target'], item['action']
        assert q not in policy and q in all_prefixes
        assert type(t) is int and 0 <= t < len(final)
        assert type(a) is int and 0 <= a < k
        policy[q] = (a, t)
    assert set(policy) == all_prefixes and len(policy) == 84

    @lru_cache(None)
    def finish(q):
        return q if sum(q) == n else finish(inc(q, policy[q][0]))

    target_review = []
    for q, (a, t) in policy.items():
        assert finish(q) == final[t]
        target_review.append({'prefix': q, 'action': a, 'source_target_index': t,
                              'indexed_terminal': final[t], 'reconstructed_terminal': finish(q)})
    zero = (0,) * k
    assert finish(zero) == tuple(first['root_counts'])
    assert policy[zero][0] == first['root_action']

    scale = math.lcm(*range(1, n + 1))
    def unit_coefficient(leaf, action, mask):
        return F(1, sum(leaf[j] for j in range(k) if mask & (1 << j))) if mask & (1 << action) else F(0)
    expected_rows = set()
    row_locations = {}
    for q, (a, _) in policy.items():
        for alternative in range(k):
            left, right = finish(q), finish(inc(q, alternative))
            row = tuple(unit_coefficient(left, a, mask) - unit_coefficient(right, alternative, mask)
                        for mask in range(1, 1 << k))
            if any(row):
                integers = tuple(int(v * scale) for v in row)
                assert all(F(v, scale) == x for v, x in zip(integers, row))
                expected_rows.add(integers)
                row_locations.setdefault(integers, []).append({'prefix': q, 'alternative': alternative})
    expected_rows = sorted(expected_rows)
    assert len(expected_rows) == 306
    coefficient_checks = 0
    for record in records:
        assert record['status'] == 'NUMERIC_CANDIDATE_ONLY'
        assert record['n'] == n and record['k'] == k and record['kind'] == 'floor'
        assert len(record['initial']) == len(record['weights']) == len(record['root_z']) == 63
        assert all(type(v) is int and v >= 0 for v in record['initial'])
        assert all(math.isfinite(v) for v in record['weights'] + record['root_z'] + record['root_query'] + record['root_fractional_q'])
        assert len(record['rows']) == 306
        for given, expected in zip(record['rows'], expected_rows):
            assert len(given) == 63
            for x, y in zip(given, expected):
                assert x == float(F(y, scale))
                coefficient_checks += 1
    weights = list(map(F, first['weights']))
    assert {b: w for b, w in enumerate(weights, 1) if w} == {47: F(1)}
    assert all(w >= 0 for w in weights)
    active = [a for a in range(k) if 47 & (1 << a)]
    assert active == [0, 1, 2, 3, 5]

    # A complete ordered-history expansion, retaining all six action labels.
    @lru_cache(None)
    def finish_history(h):
        if len(h) == n:
            return h
        q = tuple(h.count(a) for a in range(k))
        return finish_history(h + (policy[q][0],))

    def point_pay(leaf, action):
        if action not in active:
            return F(0)
        return F(1, sum(a in active for a in leaf))

    ordered = []
    all_slacks = []
    for depth in range(n):
        for h in product(range(k), repeat=depth):
            q = tuple(h.count(a) for a in range(k))
            a = policy[q][0]
            chosen = point_pay(finish_history(h), a)
            deviations = [point_pay(finish_history(h + (b,)), b) for b in range(k)]
            slacks = [chosen - v for v in deviations]
            assert all(v >= 0 for v in slacks)
            all_slacks.extend(slacks)
            ordered.append({'h': h, 'a': a, 'terminal': finish_history(h),
                            'profit': str(chosen), 'deviation_profits': list(map(str, deviations)),
                            'slacks': list(map(str, slacks))})
    assert len(ordered) == 259 and len(all_slacks) == 1554
    assert finish_history(()) == (1, 2, 2, 2)
    assert all(a in active for a, _ in policy.values())
    exact_row_slacks = [sum((F(c, scale) * w for c, w in zip(row, weights)), F(0))
                        for row in expected_rows]
    assert min(exact_row_slacks) == 0

    # This is exact evaluation of the original binary floats, not normalization
    # or repair.  p is exactly valid here; q's exact sum is recorded as given.
    p = list(map(F, first['root_query']))
    q = list(map(F, first['root_fractional_q']))
    assert sum(p) == 1 and all(v >= 0 for v in p)
    z47 = F(first['root_z'][46])
    original_fenchel_lower = 2 * z47 - n * z47 * z47
    assert original_fenchel_lower == F(1, 4) - F(1, 2**106)
    qstar = [F(1, 5) if a in active else F(0) for a in range(k)]
    zstar = [1 / (1 + 3 * sum(qstar[a] for a in range(k) if b & (1 << a)))
             for b in range(1, 1 << k)]
    field_ledger = []
    for i, r in enumerate(records):
        assert len(r['trace']) == 2
        for j, row in enumerate(r['trace']):
            assert set(row) == {'iteration', 'linear_upper', 'actual_debt', 'root_value',
                                'root_Fenchel_lower', 'next_value', 'root_utility',
                                'min_spe_margin', 'support'}
            assert row['iteration'] == j and row['next_value'] is None
            assert row['actual_debt'] == -2**-53 and row['root_utility'] == .25
            assert row['root_value'] == .25 + 2**-53
            assert row['root_Fenchel_lower'] == .25
            assert row['support'] == 1 and row['min_spe_margin'] == 0
        field_ledger.append({'index': i, 'full_record_sha256': sha(r),
                             'initial_sum': sum(r['initial']), 'initial_mask47': r['initial'][46],
                             'initial_mask63': r['initial'][62], 'trace': r['trace'],
                             'each_field_sha256': {field: sha(r[field]) for field in fields},
                             'negative_zero_weight_positions': [j + 1 for j, v in enumerate(r['weights'])
                                                                if v == 0 and math.copysign(1, v) < 0]})
    result = {
        'source_id': source['id'], 'source_sha256': source['sha256'],
        'all_15_records_all_14_fields_read': True, 'field_equality_groups': groups,
        'complete_record_groups': list(full_groups.values()), 'per_record_ledger': field_ledger,
        'total_saved_policy_items': 15 * 84, 'unique_policy_items': 84,
        'total_saved_rows': 15 * 306, 'unique_exact_rows': 306,
        'source_coefficient_comparisons': coefficient_checks,
        'exact_row_scale': scale, 'exact_row_integer_alphabet': sorted(set(v for row in expected_rows for v in row)),
        'source_row_identity_scope': 'all cells equal expected rational true IC rounded by the source float conversion; not decimal floats treated as exact thirds',
        'all_84_target_index_checks_passed': True, 'ordered_decision_nodes': len(ordered),
        'ordered_IC_comparisons_including_self': len(all_slacks),
        'strict_IC_comparisons': sum(v > 0 for v in all_slacks),
        'tie_IC_comparisons_including_self': sum(v == 0 for v in all_slacks),
        'minimum_IC_slack': str(min(all_slacks)),
        'positive_unit_customer_masks': {'47': '1'}, 'covering_labels': active, 'empty_labels': [4],
        'actual_history': finish_history(()), 'root_profits': ['1/4'] * 4,
        'W': '1', 'OPT': '1', 'independent_analytic_free_t4': '1/4',
        'independent_analytic_floor_debt': '0',
        'original_p_exact_sum': str(sum(p)), 'original_p_min': str(min(p)),
        'original_q_exact_sum': str(sum(q)), 'original_q_exact_sum_minus_one': str(sum(q) - 1),
        'original_q_min': str(min(q)), 'original_z47_exact': str(z47),
        'original_p_z_exact_Fenchel_lower': str(original_fenchel_lower),
        'original_p_z_exact_floor_upper': str(F(1, 4) - original_fenchel_lower),
        'new_separate_rational_background_qstar': list(map(str, qstar)),
        'new_separate_rational_inverse_denominators_zstar': list(map(str, zstar)),
        'max_original_z_vs_new_zstar_exact_difference': str(max(abs(F(x) - y) for x, y in zip(first['root_z'], zstar))),
        'original_reports_rewritten_or_repaired': False,
        'original_main_runs': 0, 'LP_runs': 0, 'SLSQP_runs': 0, 'BI_runs': 0,
        'new_saved_record_exact_audit_passes': 1,
    }
    (BASE / 'replay/exact-review.json').write_text(json.dumps(result, indent=2) + '\n')
    details = {'terminal_index_order': final, 'all_count_targets': target_review,
               'all_ordered_IC': ordered, 'all_exact_rows_integer_scale12': expected_rows,
               'exact_row_slacks_at_saved_point': list(map(str, exact_row_slacks)),
               'row_origins': [row_locations[tuple(row)] for row in expected_rows]}
    payload = (compact(details) + '\n').encode()
    with (BASE / 'replay/complete-exact-ledger.json.gz').open('wb') as f:
        with gzip.GzipFile(fileobj=f, mode='wb', mtime=0) as z:
            z.write(payload)
    print(json.dumps({'saved_records': 15, 'unique_complete_records': len(full_groups),
                      'policy_count_prefixes': 84, 'ordered_nodes': 259,
                      'ordered_IC_comparisons': 1554, 'unique_exact_rows': 306,
                      'source_coefficient_comparisons': coefficient_checks,
                      'exact_floor_debt': '0', 'ledger_uncompressed_bytes': len(payload),
                      'ledger_uncompressed_sha256': hashlib.sha256(payload).hexdigest(),
                      'all_passed': True}))


if __name__ == '__main__':
    run()
