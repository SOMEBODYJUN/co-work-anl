"""Current informed field reconstruction from the same frozen author kernel.

Does not import either original tail auditor or generate customer moments.
The large kernel and old point are reused at their shared evidence paths.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
SHARED = HERE.parent / 'full156-tail-parent-report' / 'original'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify():
    source = HERE / 'original/full156_tail2_exact_audit.json'
    expected = json.loads(source.read_text())
    assert source.stat().st_size == 4630
    assert digest(source) == 'a672c54c26423614174be07846777db983e2e5f7c9dcc853a26b12d776ec253d'
    kp = SHARED / 'research_5/full156_tail2_kernel_10344.json'
    raw = kp.read_bytes()
    kernel = json.loads(raw)
    kernel_sha = hashlib.sha256(raw).hexdigest()
    assert kernel_sha == expected['source_sha256'] == '876f063e9e88679c8803011775b04a4b707b8b586dfd3a840fd056f9ddcef3d4'
    labels = kernel['topics']
    n = len(labels)
    descriptors = [('A', i) for i in range(6)]
    descriptors += [(f, i) for f in ('T', 'B', 'C') for i in range(6)]
    descriptors += [(f, k, i, j) for f in ('R', 'Z') for k, i, j in product(range(2), range(6), range(6)) if k or i != j]
    def label(desc):
        if len(desc) == 2:
            return desc[0] + str(desc[1] + 1)
        return f'{desc[0]}_{desc[1]}_{desc[2]+1}_{desc[3]+1}'
    assert labels == list(map(label, descriptors))
    assert kernel['original_labels'] == labels
    assert kernel['original_descriptors'] == list(map(list, descriptors))
    assert n == 156 and len(set(labels)) == 156
    assert kernel['aliases'] == list(range(156))
    assert kernel['players'] == 6 and kernel['fixed_prefix'] == [0, 1, 2, 3]
    assert kernel['actual_last_pair'] == [4, 5]
    scale = int(kernel['unit_customer_scale'])
    den = int(kernel['payoff_denominator_for_normalized_point'])
    assert scale > 0 and den == 60 * scale
    u = [list(map(int, row)) for row in kernel['payoff_numerators']]
    g = [list(map(int, row)) for row in kernel['G_numerators']]
    f = list(map(int, kernel['F_numerators']))
    assert len(u) == len(g) == len(f) == n
    assert all(len(row) == n for row in u + g)
    for i, j in product(range(n), repeat=2):
        assert g[i][j] == g[j][i] >= 0
        assert u[i][j] == f[i] - g[i][j] >= 0
    assert all(g[i][i] + g[j][j] > 2 * g[i][j] for i in range(n) for j in range(i))

    replies, floors, minimizers = [], [], []
    # A column gives the last player's payoffs after a fixed first action.
    for i, column in enumerate(zip(*u)):
        last_max = max(column)
        choices = [j for j, value in enumerate(column) if value == last_max]
        replies.append(choices)
        low = min(u[i][j] for j in choices)
        floors.append(low)
        minimizers.append([j for j in choices if u[i][j] == low])
    threshold = max(floors)
    best_queries = [i for i, low in enumerate(floors) if low == threshold]
    aa, bb = kernel['actual_last_pair']
    raw_gap = Q(threshold - u[aa][bb], den)
    deficit = max(Q(0), raw_gap)
    old_gap = 1 - 2 * Q(kernel['source_W'])
    last_br = bb in replies[aa]
    reconstructed = {
        'status': 'one finite full-catalog r2 exact audit, not an inherited full six-player SPE',
        'source_sha256': kernel_sha,
        'topic_count': n,
        'fixed_prefix_labels': [labels[i] for i in kernel['fixed_prefix']],
        'target_last_pair_labels': [labels[aa], labels[bb]],
        'actual_last_is_BR': last_br,
        'actual_penultimate_u': str(Q(u[aa][bb], den)),
        'actual_last_u': str(Q(u[bb][aa], den)),
        'actual_last_BR_labels': [labels[i] for i in replies[aa]],
        'max_min_credible_floor': str(Q(threshold, den)),
        'penultimate_deficit': str(deficit),
        'strict_deficit': raw_gap > 0,
        'best_security_queries': [
            {'action': labels[i],
             'all_BR_labels': [labels[j] for j in replies[i]],
             'minimizing_BR_labels': [labels[j] for j in minimizers[i]],
             'guaranteed_u': str(Q(floors[i], den))} for i in best_queries
        ],
        'target_tail_is_full_SPE': last_br and u[aa][bb] >= threshold,
        'old_half_gap': str(old_gap),
        'three_times_penultimate_deficit': str(3 * deficit),
        'heterogeneous_repair_fixed_target_blocked_already_by_last_deficit': raw_gap > 0 and 3 * raw_gap >= old_gap,
        'unit_customer_scale': kernel['unit_customer_scale'],
        'payoff_common_denominator': str(den)
    }
    assert len(reconstructed) == len(expected) == 19
    assert reconstructed == expected

    # Read the old point only for its positive histogram support and actual
    # path values. This does not recheck 5108 necessary rows or the pair point.
    point_path = SHARED / 'research_5/combined_branch_master_exact.json'
    assert digest(point_path) == kernel['source_sha256']
    point = json.loads(point_path.read_text())
    all_hist = [c for c in point['columns'] if c['kind'] == 'hist']
    assert all(Q(c['weight']) >= 0 for c in all_hist)
    hist = [c for c in all_hist if Q(c['weight']) > 0]
    assert len(hist) == 10 and sum(Q(c['weight']) for c in hist) == 1
    assert all((scale * Q(c['weight'])).denominator == 1 for c in hist)
    assert all(len(c['hist']) == 8 and sum(c['hist']) == 6 for c in hist)
    assert all(sum(count for bucket, count in enumerate(c['hist']) if bucket & 4) == 1 for c in hist)
    assert all(len(c['actual_bits']) == 6 and set(c['actual_bits']) <= {'0', '1'} for c in hist)
    actual_welfare = sum((Q(c['weight']) for c in hist if '1' in c['actual_bits']), Q(0))
    actual_payoffs = [sum((Q(c['weight']) * int(c['actual_bits'][i]) / sum(map(int, c['actual_bits']))
                          for c in hist if c['actual_bits'][i] == '1'), Q(0)) for i in (4, 5)]
    assert actual_welfare == Q(kernel['source_W']) == Q(point['W'])
    assert actual_payoffs == [Q(u[aa][bb], den), Q(u[bb][aa], den)]
    assert [str(u[aa][bb]), str(u[bb][aa])] == kernel['actual_payoff_numerators']

    # The original author does not enumerate all SPE endpoints. This current
    # comparison separately applies the criterion already proved by the parent.
    endpoints = [(i, j) for i in range(n) for j in replies[i] if u[i][j] >= threshold]
    parent = json.loads((SHARED / 'audit_full156_reply_set.json').read_text())
    assert [[labels[i], labels[j]] for i, j in endpoints] == parent['SPE_tails']
    assert len(endpoints) == parent['SPE_tail_count'] == 6
    assert parent['old_actual_penultimate_deficit'] == str(deficit)
    assert parent['old_half_gap'] == str(old_gap)
    assert parent['three_times_deficit'] == str(3 * deficit)

    groups = defaultdict(list)
    for j in replies[aa]:
        name = labels[j]
        parts = name.split('_')
        category = name if len(parts) == 1 else '_'.join(parts[:2]) + ('_diagonal' if parts[2] == parts[3] else '_offdiagonal')
        groups[category].append(j)
    group_data = []
    for category, ids in groups.items():
        values = {Q(u[aa][j], den) for j in ids}
        assert len(values) == 1
        value = next(iter(values))
        group_data.append({'category': category, 'count': len(ids), 'labels': [labels[j] for j in ids],
                           'penultimate_payoff': str(value), 'decimal_for_display_only': float(value)})
    assert [x['count'] for x in group_data] == [1, 30, 6, 30, 30, 30]
    best_actual_pay = max(u[aa][j] for j in replies[aa])
    best_actual_ties = [labels[j] for j in replies[aa] if u[aa][j] == best_actual_pay]
    assert best_actual_ties == ['A6'] and best_actual_pay < threshold
    assert 3 * deficit - old_gap > 0
    table = [{'action': labels[i], 'BR_labels': [labels[j] for j in replies[i]],
              'minimizing_BR_labels': [labels[j] for j in minimizers[i]],
              'credible_floor': str(Q(floors[i], den)),
              'maximum_leader_payoff_on_BR': str(max(Q(u[i][j], den) for j in replies[i]))}
             for i in range(n)]
    audit = {
        'status': 'PASS-all-19-fields-current-reconstruction',
        'author_original_entry_run_count_by_this_verifier': 0,
        'customer_moment_generator_run_count': 0,
        'pair_point_read_or_verified': False,
        'kernel_positions_checked': n * n,
        'positive_pairwise_G_coverage_distances': n * (n - 1) // 2,
        'all_original_fields_equal': True,
        'field_checks': {key: reconstructed[key] == expected[key] for key in expected},
        'kernel_sha256': kernel_sha,
        'shared_point_sha256': digest(point_path),
        'point_read_scope': 'Positive histogram support, actual bits, mass, W and metadata; necessary graph constraints and pair-point realization were not revalidated.',
        'point_verified_rows_metadata_only': point['verified_rows'],
        'positive_histograms': len(hist),
        'all_histogram_weights_nonnegative': True,
        'positive_histogram_masses_integral_after_scale': True,
        'hist_mass_sum': '1',
        'each_hist_exactly_one_T_member': True,
        'actual_W_direct_hist': str(actual_welfare),
        'actual_u5_u6_direct_hist': list(map(str, actual_payoffs)),
        'D_equals_60_times_S': den == 60 * scale,
        'all_BR_pairs_count': sum(map(len, replies)),
        'BR_size_distribution': {str(size): count for size, count in sorted(Counter(map(len, replies)).items())},
        'actual_BR_count': len(replies[aa]),
        'actual_BR_groups': group_data,
        'actual_A5_minimum_payoff_on_BR': str(Q(floors[aa], den)),
        'actual_A5_maximum_payoff_on_BR': str(Q(best_actual_pay, den)),
        'actual_A5_maximizing_BR_labels': best_actual_ties,
        'all_A5_best_reply_ties_below_threshold': best_actual_pay < threshold,
        'three_deficit_minus_old_half_gap': str(3 * deficit - old_gap),
        'parent_endpoint_crosscheck': [[labels[i], labels[j]] for i, j in endpoints],
        'source_scope': 'All conclusions use the one shared frozen author kernel at one fixed prefix. This is not another customer-moment implementation, all six-player SPE enumeration, or original author CLI replay.'
    }
    output = HERE / 'replay'
    output.mkdir(exist_ok=True)
    (output / 'reconstructed-author-fields.json').write_text(json.dumps(reconstructed, indent=2) + '\n')
    (output / 'field-audit.json').write_text(json.dumps(audit, indent=2) + '\n')
    (output / 'all-156-BR-rows.json').write_text(json.dumps(table, indent=2) + '\n')
    print(json.dumps({key: audit[key] for key in ['status', 'kernel_positions_checked', 'all_original_fields_equal', 'actual_BR_count', 'actual_A5_maximizing_BR_labels', 'all_A5_best_reply_ties_below_threshold']}, indent=2))


if __name__ == '__main__':
    verify()
