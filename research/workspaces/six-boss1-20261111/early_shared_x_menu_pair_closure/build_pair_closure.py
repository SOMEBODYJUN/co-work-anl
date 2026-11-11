#!/usr/bin/env python3
"""All visible same-branch PAIRs, with exact duplicate/trivial-row removal.

The old four-source layer is a frozen read-only input.  There are no new
columns, no point values, and no optimizer.  Indexed menu products mean the
literal full Cartesian 6-by-6 average, including same-menu self-products.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement
from pathlib import Path
import gzip
import json

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = WORK.parents[2]
OLD_LAYER = WORK / 'early_shared_x_joint'
INPUTS = {
    'old_append': OLD_LAYER / 'symbolic_append.json.gz',
    'old_columns': OLD_LAYER / 'columns_22941.json.gz',
    'old_freeze': OLD_LAYER / 'freeze_manifest.json',
    'base_matrix': WORK / 'common_x_joint_lp/final/exact_matrix.json.gz',
    'model': REPO / 'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
    'PAIR_owner': REPO / 'archives/customer-attraction/state/引理/跨族末两人菜单的共同锚点与运输界--引理.md',
}
PINS = {
    'old_append': '1ff17a93dc319e05c366424214a722a86577773599ac5692a1fabb6cfaa3a5e0',
    'old_columns': 'dad7364e606539391a455f30bcf743ec6f3f5b7d59cf58221b1aedec18434b49',
    'old_freeze': 'ec50991df761fbe82c22814abae71c7ba6a57d354803ecd59a44eea414c87ec1',
    'base_matrix': '1b4a4e544e5b9eeea1fa64b3849a9d4cc532b997a5ad972ce33df81c224551e7',
}


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def read(path):
    with gzip.open(path, 'rt') if path.suffix == '.gz' else path.open() as f:
        return json.load(f)


def save(name, value):
    path = HERE / name
    assert not path.exists(), ('refuse_overwrite', str(path))
    data = (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()
    if path.suffix == '.gz':
        with path.open('wb') as stream:
            with gzip.GzipFile(filename='', mode='wb', fileobj=stream, mtime=0) as f:
                f.write(data)
    else:
        path.write_bytes(data)


def sparse(row):
    return [[j, str(a)] for j, a in sorted(row.items()) if a]


def vector_key(row):
    return tuple((int(j), str(F(a))) for j, a in row if F(a))


def query_name(q):
    if q['kind'] == 'X':
        return 'X'
    if q['kind'] == 'actual':
        return 'A' + str(q['player'])
    if q['kind'] == 'indexed-average':
        return q['family'] + '_mean6'
    return q['name']


def main():
    before = {key: digest(path) for key, path in INPUTS.items()}
    assert all(before[key] == pin for key, pin in PINS.items())
    old = read(INPUTS['old_append'])
    assert old['old_columns'] == 21021 and old['total_columns'] == 22941
    assert len(old['new_columns']) == 1920
    assert len(old['inequalities']) == 436 and len(old['equalities']) == 128
    hist = {v['hist_column']: v for v in old['base_contract']['histograms']}
    old_index = {}
    for row in old['inequalities']:
        old_index.setdefault(vector_key(row['row']), []).append(row['id'])
    old_raw = old['raw_inequality_provenance']
    states = {}
    for offset, c in enumerate(old['new_columns']):
        i = c['source_player']
        b = hist[c['hist_column']]['actual_backgrounds'][i - 1]
        x, ys, t = c['X_bit'], c['middle_bits'], c['terminal_bit']
        z = ys[-1]
        d = b + x + sum(ys[:-1]) + 1
        assert 1 <= d <= 5
        H = F(z, d + t) + F(t, d + z) + F(z, d * (d + 1))
        states.setdefault(i, []).append({'column': 21021 + offset, 'hist': c['hist_column'],
                                        'x': x, 'tail': ys + [t], 'd': d, 'H': H})

    def membership(q, s):
        h = hist[s['hist']]
        if q['kind'] == 'X':
            return F(s['x'])
        if q['kind'] == 'actual':
            return F(int(h['actual_bits'][q['player'] - 1]))
        if q['kind'] == 'new-tail':
            return F(s['tail'][q['tail_index']])
        return F(h['indexed_membership_counts'][q['family']], 6)

    def literal_members(q, s):
        if q['kind'] != 'indexed-average':
            return [membership(q, s)]
        slot = ('T', 'B', 'C').index(q['family'])
        return [F(word[slot]) for word in hist[s['hist']]['literal_words']]

    groups, group_index, raw, queries_by_source = [], {}, [], {}
    literal_checks = Counter()
    for branch in old['branches']:
        i = branch['source_player']
        fixed = old['fixed_known_queries']
        queries = [{'kind': 'X'}] + fixed[:6] + branch['ordered_tail_labels'] + fixed[6:]
        assert len(queries) == branch['m'] + 11
        queries_by_source[str(i)] = queries
        for left, right in combinations_with_replacement(range(len(queries)), 2):
            q, r = queries[left], queries[right]
            row = {}
            for state in states[i]:
                d = state['d']
                qv, rv = membership(q, state), membership(r, state)
                coef = state['H'] - (qv + rv) / d + qv * rv / (d * (d + 1))
                if coef:
                    row[state['column']] = coef
                # Exact Cartesian averaging: only count known Boolean words.
                # This establishes products without positing random independence.
                qbits, rbits = literal_members(q, state), literal_members(r, state)
                n = len(qbits) * len(rbits)
                sum_qr = sum(a * b for a in qbits for b in rbits)
                sum_q_plus_r = sum(a + b for a in qbits for b in rbits)
                assert sum_qr / n == qv * rv
                assert sum_q_plus_r / n == qv + rv
                assert state['H'] - sum_q_plus_r / (n * d) + sum_qr / (n * d * (d + 1)) == coef
                literal_checks['coefficient_states'] += 1
                literal_checks['literal_ordered_pairs'] += n
                literal_checks['menu_menu_states' if n == 36 else 'pure_menu_states' if n == 6 else 'pure_pure_states'] += 1
            exact = vector_key(sparse(row))
            group_id = group_index.get(exact)
            if group_id is None:
                group_id = len(groups)
                group_index[exact] = group_id
                old_matches = old_index.get(exact, [])
                groups.append({'group_id': group_id, 'row': sparse(row), 'rhs': '0',
                               'is_zero': not row,
                               'mu_coefficientwise_nonnegative': all(a >= 0 for a in row.values()),
                               'old436_exact_row_ids': old_matches, 'raw_pair_ids': [],
                               'old23676_exact_duplicate_possible': not row,
                               'old23676_exclusion_reason': 'Nonzero support lies entirely in mu columns 21021..22940, while every zero-extended old23676 row has zero coefficients there.' if row else 'Zero vector classified separately; no old-core scan is needed to omit it.'})
            record = {'raw_pair_id': len(raw), 'source_player': i, 'left_query_index': left,
                      'right_query_index': right, 'left_query': q, 'right_query': r,
                      'query_names': [query_name(q), query_name(r)], 'vector_group_id': group_id,
                      'averaging_rule': 'full Cartesian product of literal query lists; menu-menu uses all36 ordered index pairs, including self-menu',
                      'provenance': {'history': branch['last_two_prefix'],
                                     'actual_penultimate': branch['ordered_tail_labels'][-2]['name'],
                                     'actual_terminal': branch['ordered_tail_labels'][-1]['name'],
                                     'wallet': 'branch U5+U6+g(penultimate,penultimate), all from this branch mu',
                                     'payment': ['U5-U(L,J_L)', 'U(J_L,L)-U(R,L)', 'U6-U(J_L,penultimate)', 'g(penultimate,penultimate)-g(penultimate,J_L)'],
                                     'hidden_true_reply': 'J_L=sigma6(this exact last-two prefix,L)',
                                     'actual_u5_u6_used': False, 'cross_forced_branch_overlap_used': False}}
            groups[group_id]['raw_pair_ids'].append(record['raw_pair_id'])
            raw.append(record)
    assert len(raw) == 394
    assert Counter(v['source_player'] for v in raw) == {1: 120, 2: 105, 3: 91, 4: 78}

    append_rows = []
    for group in groups:
        is_new = not group['is_zero'] and not group['old436_exact_row_ids'] and not group['mu_coefficientwise_nonnegative']
        group['usable_append_row_id'] = len(append_rows) if is_new else None
        if is_new:
            append_rows.append({'id': len(append_rows), 'global_ge_row_index': 24112 + len(append_rows),
                                'vector_group_id': group['group_id'], 'raw_pair_ids': group['raw_pair_ids'],
                                'row': group['row'], 'rhs': '0', 'sense': '>='})
    for record in raw:
        group = groups[record['vector_group_id']]
        record['flags'] = {k: group[k] for k in ('is_zero', 'mu_coefficientwise_nonnegative', 'old436_exact_row_ids')}
        record['same_vector_raw_pair_ids'] = group['raw_pair_ids']
        record['usable_append_row_id'] = group['usable_append_row_id']
        if group['is_zero']:
            outcome = 'zero'
        elif group['old436_exact_row_ids']:
            outcome = 'exact_duplicate_old436'
        elif record['raw_pair_id'] != group['raw_pair_ids'][0]:
            outcome = 'exact_duplicate_new_candidates'
        elif group['mu_coefficientwise_nonnegative']:
            outcome = 'trivial_from_mu_nonnegativity'
        else:
            outcome = 'new_nontrivial_candidate'
        record['primary_outcome'] = outcome

    diagonal_dominance = []
    for i in range(1, 5):
        for family in ('T', 'B', 'C'):
            matches = [v for v in old_raw if v['family'] == 'branch-true-PAIR' and v['branch_source_player'] == i
                       and v['mode'] == 'Q,Q' and v['query_left'].get('family') == family]
            assert len(matches) == 1
            oldrow_id = matches[0]['unique_row_id']
            oldrow = {j: F(a) for j, a in old['inequalities'][oldrow_id]['row']}
            new_record = next(v for v in raw if v['source_player'] == i
                              and v['left_query'].get('family') == family
                              and v['right_query'].get('family') == family)
            newrow = {j: F(a) for j, a in groups[new_record['vector_group_id']]['row']}
            difference = {}
            for state in states[i]:
                theta = F(hist[state['hist']]['indexed_membership_counts'][family], 6)
                value = theta * (1 - theta) / (state['d'] * (state['d'] + 1))
                j = state['column']
                assert oldrow.get(j, F()) - newrow.get(j, F()) == value >= 0
                if value:
                    difference[j] = value
            assert difference
            diagonal_dominance.append({'source_player': i, 'menu': family,
                                       'old_diagonal_raw_row_id': matches[0]['raw_id'], 'old_diagonal_unique_row_id': oldrow_id,
                                       'new_full36_raw_pair_id': new_record['raw_pair_id'],
                                       'new_full36_append_row_id': new_record['usable_append_row_id'],
                                       'old_minus_full36_nonnegative_row': sparse(difference),
                                       'formula': 'sum_mu theta*(1-theta)/(dloc*(dloc+1))',
                                       'claim': 'The full36 row implies the old same-index diagonal row using mu>=0; no strict feasible-set separation is claimed.'})
    assert len(diagonal_dominance) == 12
    assert before == {key: digest(path) for key, path in INPUTS.items()}
    common = {'base_old_matrix': {'shape': [23676, 21021], 'sha256': before['base_matrix']},
              'frozen_four_source_layer': {'shape_ge': [24112, 22941], 'new_eq': 128,
                                           'sha256': before['old_append'], 'freeze_sha256': before['old_freeze']},
              'columns': 22941, 'new_columns': 0, 'new_equalities': 0,
              'all_existing_equalities_bounds_and_normalization_retained': True,
              'scope': 'Fixed16-hist necessary layer; general TP formulas are universal. Fourteen tail labels are roles, with possible aliases. No full old RZ law or full SPE characterization.',
              'no_cone_independence_claim': True, 'optimizer_calls': 0, 'point_values_read': False}
    save('all_pair_candidates.json.gz', {'schema': 'visible-menu-pair-candidates/v1', **common,
                                        'queries_by_source': queries_by_source, 'raw_pairs': raw,
                                        'exact_vector_groups': groups, 'literal_checks': dict(literal_checks),
                                        'classification_order': ['zero', 'old436 exact duplicate', 'earlier candidate exact duplicate', 'mu-coefficientwise nonnegative', 'new nontrivial candidate']})
    save('usable_pair_append.json.gz', {'schema': 'visible-menu-pair-append/v1', **common,
                                       'row_count': len(append_rows), 'rows': append_rows,
                                       'new_GE_shape': [24112 + len(append_rows), 22941],
                                       'nonzeros': sum(len(v['row']) for v in append_rows),
                                       'support_excludes_old23676_duplicates_without_large_matrix_scan': True})
    save('diagonal_menu_dominance.json.gz', {'schema': 'full36-vs-diagonal-menu-PAIR/v1',
                                           'old_bytes_unchanged': True, 'records': diagonal_dominance})
    save('source_manifest.json', {'sources': {key: {'path': str(path.relative_to(REPO)), 'sha256': before[key],
                                                  'bytes': path.stat().st_size} for key, path in INPUTS.items()},
                                  'old_input_bytes_unchanged': True, 'optimizer_calls': 0, 'point_files_read': 0})
    summary = {'status': 'BUILT_EXACT_PAIR_CLOSURE_NO_SOLVE', 'raw_candidates': len(raw),
               'raw_candidates_by_source': dict(Counter(v['source_player'] for v in raw)),
               'unique_candidate_vectors': len(groups),
               'primary_outcomes': dict(Counter(v['primary_outcome'] for v in raw)),
               'unique_group_classification': {'zero': sum(v['is_zero'] for v in groups),
                                               'old436_exact_duplicates': sum(bool(v['old436_exact_row_ids']) for v in groups),
                                               'mu_coefficientwise_nonnegative_including_zero': sum(v['mu_coefficientwise_nonnegative'] for v in groups),
                                               'usable_new_nontrivial': len(append_rows)},
               'usable_append_rows': len(append_rows), 'usable_nonzeros': sum(len(v['row']) for v in append_rows),
               'new_columns': 0, 'new_equalities': 0, 'all_columns': 22941,
               'literal_checks': dict(literal_checks), 'exact_old_diagonal_dominance_records': 12,
               'old23676_deduplication': 'Every nonzero candidate has a nonzero mu coefficient; all old rows have zero mu coefficients. Zero candidates are discarded separately.',
               'no_cone_independence_claim': True, 'optimizer_calls': 0, 'old_bytes_unchanged': True,
               'usable_append_sha256': digest(HERE / 'usable_pair_append.json.gz'),
               'all_candidates_sha256': digest(HERE / 'all_pair_candidates.json.gz')}
    save('pair_closure_summary.json', summary)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
