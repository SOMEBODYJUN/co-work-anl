#!/usr/bin/env python3
"""Weight-free OPT6/shared-X exchange audit; no optimization or point reads.

Read only the pinned formal model, support descriptors and exact matrices.
Construct the bounded 64-subset family, reject its k=7 member, and certify
every valid row from unchanged old rows/nonnegative columns.  All writes
stay here and refuse to replace an existing output.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from math import comb
from pathlib import Path
import gc
import gzip
import json

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = WORK.parents[2]
INPUTS = {
    'spec': ('research/workspaces/six-boss1-20261111/spec.json',
             '1557ca3c6b61c32e99ab9edef64085bec573f3917c4ff326c9b1867046927844'),
    'model': ('archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
              'cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88'),
    'problem': ('archives/customer-attraction/subarchives/six-providers/问题--问题.md',
                '21391fbaaa2893fef7b228a345fcf1d7f5c5d1dc8a42cc642d6bfbbeccc7c065'),
    'original_OPT_source': ('archives/customer-attraction/tools/evidence/cross-source-graph-program/original/cross_source_graph.py',
                            '295b4f11935a8ca241cef50541b30078000f8e67bea4f2301a2032914e3cc249'),
    'lift': ('research/workspaces/six-boss1-20261111/terminal_response_cycles/max_b_symbolic_lift.json',
             '52129dc848cf47f569f61442962a01aec61c6317531be0d24837d41071c96a5c'),
    'old_matrix': ('research/workspaces/six-boss1-20261111/maxb_augmented_lp/full_lift/exact_matrix.json.gz',
                   'c054aadf745ea4540233a3da693917498527d19d4ccecb0fdd34ad884e461e4b'),
    'final_matrix': ('research/workspaces/six-boss1-20261111/common_x_joint_lp/final/exact_matrix.json.gz',
                     '1b4a4e544e5b9eeea1fa64b3849a9d4cc532b997a5ad972ce33df81c224551e7'),
}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':')).encode()


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def read(path):
    if path.suffix == '.gz':
        with gzip.open(path, 'rt') as f:
            return json.load(f)
    return json.loads(path.read_text())


def save(name, value):
    path = HERE / name
    assert not path.exists(), ('refuse_overwrite', str(path))
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def sparse(row):
    return [[j, str(a)] for j, a in sorted(row.items()) if a]


def unpack(raw):
    row = {j: F(a) for j, a in raw}
    assert len(row) == len(raw) and all(row.values())
    return row


def key(row):
    return tuple(sorted((j, F(a)) for j, a in row.items() if a))


def ray(row):
    out = key(row)
    assert out
    scale = abs(out[0][1])
    return tuple((j, a / scale) for j, a in out)


def add(row, j, a):
    if a:
        row[j] = row.get(j, F()) + a
        if not row[j]:
            del row[j]


def hit(actual, mask):
    return any(mask & (1 << i) and actual[i] == '1' for i in range(6))


def exchange(hist, xcols, mask):
    k = 1 + mask.bit_count()
    assert 1 <= k <= 6
    row = {}
    for h, c in hist.items():
        d, a_hit = c['d'], hit(c['actual_bits'], mask)
        if d == 0:
            add(row, h if a_hit else xcols[h], -F(comb(6, k)))
        elif d <= k and not a_hit:
            coefficient = F(comb(6 - d, k - d))
            add(row, h, coefficient)
            add(row, xcols[h], -coefficient)
    return row


def union_cap(hist, xcols, actual_mask, includes_x):
    row = {}
    for h, c in hist.items():
        a_hit, inside_opt = hit(c['actual_bits'], actual_mask), int(c['d'] > 0)
        add(row, h, F(inside_opt - int(a_hit)))
        if includes_x and not a_hit:
            add(row, xcols[h], -F(1))
    return row


def scan_matrix(path, expected_rows):
    # Fractions are created only on the 32-coordinate support that can match
    # a candidate.  No optimizer is imported, and no primal/dual point is read.
    m = read(path)
    assert (len(m['rows']), len(m['columns'])) == (expected_rows, 21021)
    assert len(m['row_names']) == expected_rows
    hist = {j: c for j, c in enumerate(m['columns']) if c['kind'] == 'hist'}
    xcols = {c['hist_column']: j for j, c in enumerate(m['columns'])
             if c['kind'] == 'common-X-mass'}
    assert len(hist) == len(xcols) == 16 and set(hist) == set(xcols)
    allowed = set(hist) | set(xcols.values())
    matches = defaultdict(list)
    kept = {}
    for i, raw in enumerate(m['rows']):
        if len(raw) <= 32 and all(j in allowed for j, _ in raw):
            r = unpack(raw)
            if r:
                matches[ray(r)].append(i)
                kept[i] = r
    xrows = {}
    for h, x in xcols.items():
        want = {h: F(1), x: -F(1)}
        exact = [i for i in matches[ray(want)] if kept[i] == want]
        assert len(exact) == 1
        xrows[h] = exact[0]
    summary = {
        'columns': m['columns'], 'hist': hist, 'xcols': xcols,
        'objective': m['objective'], 'normalization': m['normalization'],
        'names': m['row_names'], 'kept': kept, 'ray_matches': matches,
        'xrows': xrows, 'all_nonnegative': m['all_columns_nonnegative'],
        'all_rows_sha256': sha256(canonical(m['rows'])).hexdigest(),
        'old_prefix_rows_sha256': sha256(canonical(m['rows'][:22297])).hexdigest(),
        'row_count': expected_rows,
    }
    del m
    gc.collect()
    return summary


def main():
    sources = {}
    for role, (name, pin) in INPUTS.items():
        path = REPO / name
        assert digest(path) == pin, (role, 'input_changed')
        sources[role] = {'path': name, 'sha256': pin, 'bytes': path.stat().st_size}
    model = (REPO / INPUTS['model'][0]).read_text()
    opt_source = (REPO / INPUTS['original_OPT_source'][0]).read_text()
    assert '\\operatorname{OPT}_m' in model and '\\max_' in model
    assert 'valid only when the T tuple is optimal' in opt_source
    lift = read(REPO / INPUTS['lift'][0])
    old = scan_matrix(REPO / INPUTS['old_matrix'][0], 22297)
    final = scan_matrix(REPO / INPUTS['final_matrix'][0], 23676)
    assert old['all_nonnegative'] is final['all_nonnegative'] is True
    assert old['columns'][:20601] == final['columns'][:20601]
    for a, b in zip(old['columns'][20601:], final['columns'][20601:]):
        assert a == {k: v for k, v in b.items() if k != 'semantic_upgrade'}
    assert old['columns'][20585:] == lift['new_columns']
    assert old['all_rows_sha256'] == final['old_prefix_rows_sha256']
    assert old['objective'] == final['objective']
    assert old['normalization'] == final['normalization']
    hist, xcols, xrows = final['hist'], final['xcols'], final['xrows']
    assert xrows == old['xrows'] and set(xrows.values()) == set(range(20910, 20926))
    assert set(c['d'] for c in hist.values()) == {1}
    assert all(sum(c['hist']) == 6 and sum(c['hist'][4:]) == c['d'] for c in hist.values())
    assert final['normalization'] == ['1' if j in hist else '0' for j in range(21021)]
    assert final['objective'] == ['1' if j in hist and '1' in hist[j]['actual_bits'] else '0'
                                   for j in range(21021)]
    # Independently confirm the old optimum-single-replacement convention:
    # six times the summed exchange row for A_i; averaged B/C sum over slots.
    opt_rows = []
    for pos, query in enumerate(list(range(6)) + ['B', 'C']):
        row = {}
        for h, c in hist.items():
            if isinstance(query, int):
                membership_sum = 6 * int(c['actual_bits'][query])
            else:
                bit = 1 if query == 'B' else 2
                membership_sum = sum(n * ((word >> (2 - bit)) & 1)
                                     for word, n in enumerate(c['hist']))
            value = 6 * int(c['d'] == 1) - membership_sum * int(c['d'] == 1) - 6 * membership_sum * int(c['d'] == 0)
            add(row, h, F(value))
        i = 3959 + pos
        assert old['names'][i] == final['names'][i] == f'OPT-one-replace:{query}'
        assert row == old['kept'][i] == final['kept'][i]
        opt_rows.append({'row_index': i, 'name': final['names'][i], 'row': sparse(row)})
    records, subset_table = [], []
    for mask in range(64):
        selected = [i + 1 for i in range(6) if mask & (1 << i)]
        k = len(selected) + 1
        if k == 7:
            subset_table.append({'mask': mask, 'actual_positions': selected, 'k': k,
                                 'status': 'excluded_k7_not_an_OPT6_exchange'})
            continue
        row = exchange(hist, xcols, mask)
        coefficient = comb(5, k - 1)
        certificate = [[xrows[h], str(coefficient)] for h, c in hist.items()
                       if not hit(c['actual_bits'], mask)]
        rec = {'candidate_id': f'exchange-X-A{mask:02d}', 'family': 'averaged_k_exchange',
               'actual_mask': mask, 'actual_positions': selected, 'new_label_slots': k,
               'row': sparse(row), 'rhs': '0', 'old_row_multipliers': certificate,
               'nonnegative_column_multipliers': []}
        records.append(rec)
        subset_table.append({'mask': mask, 'actual_positions': selected, 'k': k,
                             'candidate_id': rec['candidate_id'], 'status': 'valid_redundant'})
    for omitted in range(7):
        includes_x = omitted != 6
        mask = 63 ^ (1 << omitted) if includes_x else 63
        row = union_cap(hist, xcols, mask, includes_x)
        outside = [h for h, c in hist.items() if not hit(c['actual_bits'], mask)]
        records.append({'candidate_id': f'cap6-omit-{omitted + 1 if includes_x else "X"}',
                        'family': 'six_of_seven_legal_label_union_cap',
                        'actual_mask': mask, 'includes_X': includes_x,
                        'row': sparse(row), 'rhs': '0',
                        'old_row_multipliers': [[xrows[h], '1'] for h in outside] if includes_x else [],
                        'nonnegative_column_multipliers': [] if includes_x else [[h, '1'] for h in outside]})
    exact_groups, ray_groups = defaultdict(list), defaultdict(list)
    for rec in records:
        target = unpack(rec['row'])
        rebuilt = {}
        for i, value in rec['old_row_multipliers']:
            value = F(value)
            assert value > 0 and final['kept'][i] == old['kept'][i]
            for j, a in final['kept'][i].items():
                add(rebuilt, j, value * a)
        for j, value in rec['nonnegative_column_multipliers']:
            assert F(value) > 0
            add(rebuilt, j, F(value))
        assert rebuilt == target
        for label, matrix in [('old22297', old), ('final23676', final)]:
            proportional = []
            for i in matrix['ray_matches'].get(ray(target), []):
                pivot = min(target)
                multiplier = target[pivot] / matrix['kept'][i][pivot]
                assert multiplier > 0
                assert target == {j: multiplier * a for j, a in matrix['kept'][i].items()}
                proportional.append({'row_index': i, 'target_equals_multiplier_times_old_row': str(multiplier),
                                     'name': matrix['names'][i], 'exact_equal': multiplier == 1})
            rec[label + '_single_row_matches'] = proportional
        exact_groups[key(target)].append(rec['candidate_id'])
        ray_groups[ray(target)].append(rec['candidate_id'])
        rec['status'] = 'certified_redundant_no_append'
    exchanges = [r for r in records if r['family'] == 'averaged_k_exchange']
    counts = {
        'subset_masks_examined': 64, 'valid_exchange_candidates': len(exchanges),
        'excluded_k7_masks': 1, 'six_label_union_candidates': 7,
        'total_candidates': len(records),
        'exchange_distinct_exact_vectors': len({key(unpack(r['row'])) for r in exchanges}),
        'exchange_distinct_positive_rays': len({ray(unpack(r['row'])) for r in exchanges}),
        'all_distinct_exact_vectors': len(exact_groups), 'all_distinct_positive_rays': len(ray_groups),
        'single_old_row_or_positive_multiple_matches': sum(bool(r['old22297_single_row_matches']) for r in records),
        'single_final_row_or_positive_multiple_matches': sum(bool(r['final23676_single_row_matches']) for r in records),
        'exact_conic_certificates': len(records), 'new_nonderived_rows': 0,
        'rows_to_append': 0, 'new_columns': 0, 'optimizer_calls': 0, 'point_files_read': 0,
    }
    assert counts['exchange_distinct_exact_vectors'] == 39
    assert counts['exchange_distinct_positive_rays'] == 29
    assert counts['all_distinct_exact_vectors'] == 40 and counts['all_distinct_positive_rays'] == 30
    assert counts['total_candidates'] == 70
    save('candidate_rows_and_certificates.json', {
        'status': 'ALL_CANDIDATES_REDUNDANT_DO_NOT_APPEND', 'counts': counts,
        'inequality_convention': 'row >= 0; homogeneous zero RHS',
        'mask_convention': 'bit i selects actual position A_(i+1); actual_bits is in A1..A6 order',
        'subset_table': subset_table, 'rows': records,
        'exact_vector_classes': [{'row': sparse(dict(k)), 'members': v} for k, v in exact_groups.items()],
        'positive_ray_classes': [{'primitive_row': sparse(dict(k)), 'members': v} for k, v in ray_groups.items()],
        'scope': 'Fixed original16 hist and all21021 preserved coordinates. No point evaluation or optimization.'})
    save('old_row_evidence.json', {
        'old_matrix_sha256': sources['old_matrix']['sha256'],
        'final_matrix_sha256': sources['final_matrix']['sha256'],
        'unchanged_old_prefix_rows': 22297,
        'old_prefix_rows_canonical_sha256': old['all_rows_sha256'],
        'X_bounds': [{'hist_column': h, 'X_column': xcols[h], 'row_index': xrows[h],
                      'name': final['names'][xrows[h]], 'row': sparse(final['kept'][xrows[h]])}
                     for h in hist],
        'old_optimum_single_exchange_rows': opt_rows,
        'nonnegative_columns': True,
        'actual_only_six_union_cap_column_bound_indices': [h for h, c in hist.items() if c['actual_bits'] == '000000'],
        'single_row_match_search': 'All old22297 and final23676 rows scanned; exact support and positive rational proportionality checked.',
        'combination_coefficients_verified_exactly': True})
    save('descriptor_contract.json', {
        'columns': 21021, 'hist_count': 16,
        'hist': [{'column': h, **c, 'X_column': xcols[h], 'old_X_upper_row': xrows[h]} for h, c in hist.items()],
        'd_distribution': dict(Counter(c['d'] for c in hist.values())),
        'old_columns_sha256': sha256(canonical(old['columns'])).hexdigest(),
        'final_columns_sha256': sha256(canonical(final['columns'])).hexdigest(),
        'all_descriptor_indices_retained': True,
        'original_20601_descriptors_equal': True,
        'remaining420_legacy_descriptor_fields_equal': True,
        'original16_hist_including_recorded_zero_hist_retained': True,
        'recorded_zero_hist_from_weight_free_lift_metadata': lift['zero_histograms'],
        'normalization': [[h, '1'] for h in hist], 'normalization_rhs': '1',
        'K_column_is_not_the_OPT_normalizer': True,
        'OPT_equals_total_represented_client_mass_on_this_support': True,
        'generic_support_claim': 'None. General clients may have d=0 or d=2..6; the general proof retains them.'})
    save('source_manifest.json', {'sources': sources, 'no_point_file_read': True,
                                 'frozen_input_writes': 0, 'optimizer_calls': 0,
                                 'generator_sha256': digest(Path(__file__))})
    save('verification.json', {'status': 'PASS_ALL70_EXACT_REDUNDANCY_CERTIFICATES', **counts,
                               'formal_OPT_is_true_six_label_maximum': True,
                               'old_optimum_row_semantics_reconstructed': 8,
                               'literal_client_audit_pending': True})
    print(json.dumps(counts, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
