#!/usr/bin/env python3
"""Weight-free four-source shared-X layer.  No point reader or optimizer.

Read frozen descriptor inputs, append 1920 nonnegative hidden-tail columns,
and emit exact rows with complete source-wallet provenance.  Every write is
inside this directory; neither a baseline matrix nor any gamepoint is changed.
The fixed-point template intentionally has no values or supplied point path.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement, product
from pathlib import Path
import gzip
import json

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = WORK.parents[2]
OLD = 21021
BASE_ROWS = 23676
FILES = {
    'full_matrix': WORK / 'maxb_augmented_lp/full_lift/exact_matrix.json.gz',
    'final_matrix': WORK / 'common_x_joint_lp/final/exact_matrix.json.gz',
    'symbolic_X_lift': WORK / 'terminal_response_cycles/max_b_symbolic_lift.json',
    'literal_label_builder': WORK / 'actual_pair_20910/build.py',
    'literal_label_catalog': WORK / 'actual_pair_20910/labels_and_orbits.json',
    'model': REPO / 'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
    'main_maxx_family': WORK / 'main_prefix_safety_maxx_family.md',
    'actual_MX_RC_owner': REPO / 'archives/customer-attraction/state/引理/真实末回复的共同潜力上限与重叠参数端点--引理.md',
    'PAIR_owner': REPO / 'archives/customer-attraction/state/引理/跨族末两人菜单的共同锚点与运输界--引理.md',
    'true_tail_PAIR': WORK / 'early3_pair_cone.md',
    'original_new_reply': REPO / ('archives/customer-attraction/tools/evidence/explicit-joint-rz-and-root-extension-primary/dependencies-original/research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra/new_reply_budget.py'),
    'original_word_patterns': REPO / ('archives/customer-attraction/tools/evidence/explicit-joint-rz-and-root-extension-primary/dependencies-original/research/workspaces/customer-attraction/R-964def22ed03479582e83410444f2ea2/parent/fourth_indexed_projection.py'),
}
PINS = {
    'full_matrix': 'c054aadf745ea4540233a3da693917498527d19d4ccecb0fdd34ad884e461e4b',
    'final_matrix': '1b4a4e544e5b9eeea1fa64b3849a9d4cc532b997a5ad972ce33df81c224551e7',
    'symbolic_X_lift': '52129dc848cf47f569f61442962a01aec61c6317531be0d24837d41071c96a5c',
    'model': 'cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88',
    'main_maxx_family': '4d3f24e686ae38a8593b62abe1807249de6bd3884b428d52198180798ea73b81',
    'actual_MX_RC_owner': 'f358a161eed5f02f243223bc590a41b3247834f842ab251060e380f5cd1fed39',
    'PAIR_owner': '8caa0131fc5a517bbdf8001a44bc00cc6741bb5255a35e413016e4a7319779ba',
    'original_new_reply': '5be0586e5b013a8bd7dacc197874b6b4549d700a383bbd12726fe2b8f0245773',
}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def digest(path):
    h = sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            h.update(block)
    return h.hexdigest()


def save(name, value):
    path = HERE / name
    assert not path.exists(), ('refuse_overwrite', str(path))
    data = json.dumps(value, indent=2, ensure_ascii=False).encode() + b'\n'
    if path.suffix == '.gz':
        with path.open('wb') as out:
            with gzip.GzipFile(filename='', mode='wb', fileobj=out, mtime=0) as packed:
                packed.write(data)
    else:
        path.write_bytes(data)


def add(row, j, a):
    if a:
        row[j] = row.get(j, F()) + a
        if not row[j]:
            del row[j]


def sparse(row):
    return [[j, str(a)] for j, a in sorted(row.items()) if a]


def unpack(row):
    return {j: F(a) for j, a in row}


def descriptor_array(path):
    """Read only the leading columns array, not the multi-million-entry rows."""
    decoder = json.JSONDecoder()
    with gzip.open(path, 'rt', encoding='utf-8') as stream:
        prefix = stream.read(65536)
        assert prefix.startswith('{"columns":['), path
        value_start = len('{"columns":')
        while True:
            try:
                columns, end = decoder.raw_decode(prefix, value_start)
                assert prefix[end:end + 1] == ','
                return columns
            except json.JSONDecodeError:
                more = stream.read(65536)
                assert more, 'unfinished descriptor array'
                prefix += more


def query_name(q):
    if q['kind'] == 'actual':
        return 'A' + str(q['player'])
    if q['kind'] == 'indexed-average':
        return q['family'] + '_mean6'
    if q['kind'] == 'X':
        return 'X'
    return q['name']


def build():
    before = {key: digest(path) for key, path in FILES.items()}
    for key, pin in PINS.items():
        assert before[key] == pin, ('input_sha_mismatch', key, before[key])
    full = descriptor_array(FILES['full_matrix'])
    final = descriptor_array(FILES['final_matrix'])
    assert len(full) == len(final) == OLD
    assert full[:20601] == final[:20601]
    changes = []
    for j, (old, new) in enumerate(zip(full, final)):
        assert all(k in new and new[k] == v for k, v in old.items())
        if old != new:
            changes.append({'column': j, 'added_fields': {k: v for k, v in new.items() if k not in old}})
    assert len(changes) == 420
    assert full[0] == {'kind': 'K'}
    assert all('weight' not in c for c in final)
    final_sha = sha256(canonical(final)).hexdigest()
    assert final_sha == 'ba3b16824a91488eb93122f265eae7eb48f732eec66925bf9e2f50bfe98b96ce'
    hist = {j: c for j, c in enumerate(final) if c['kind'] == 'hist'}
    xcols = {c['hist_column']: j for j, c in enumerate(final) if c['kind'] == 'common-X-mass'}
    assert len(hist) == len(xcols) == 16 and set(hist) == set(xcols)
    assert sorted(xcols.values()) == list(range(20585, 20601))
    assert all(sum(c['hist']) == 6 for c in hist.values())
    with FILES['symbolic_X_lift'].open() as f:
        lift = json.load(f)
    zero_hist = lift['zero_histograms']
    assert set(zero_hist) == {1, 59, 366, 449, 524, 574}
    labels = json.loads(FILES['literal_label_catalog'].read_text())['labels']
    indexed = {}
    for slot, kind in enumerate(('T', 'B', 'C')):
        literal = [v for v in labels if v['kind'] == kind]
        assert [v['name'] for v in literal] == [kind + str(k) for k in range(1, 7)]
        assert [v['indices'] for v in literal] == [[k] for k in range(6)]
        assert all(v['word_slot'] == slot for v in literal)
        indexed[kind] = literal
    words = tuple(product((0, 1), repeat=3))
    hist_data = {}
    for h, c in hist.items():
        actual = tuple(map(int, c['actual_bits']))
        menu = tuple(w for w, count in zip(words, c['hist']) for _ in range(count))
        assert len(actual) == len(menu) == 6
        counts = {k: sum(w[slot] for w in menu) for slot, k in enumerate(('T', 'B', 'C'))}
        assert counts['T'] == c['d']
        hist_data[h] = {'hist_column': h, 'actual_bits': c['actual_bits'], 'd': c['d'],
                        'hist': c['hist'], 'X_column': xcols[h],
                        'P': sum(actual[:4]), 'actual_total_load': sum(actual),
                        'actual_backgrounds': [sum(actual[:j]) for j in range(6)],
                        'indexed_membership_counts': counts,
                        'literal_words': [list(w) for w in menu]}
    incomes = {i: {h: F(int(c['actual_bits'][i - 1]), sum(map(int, c['actual_bits'])))
                   for h, c in hist.items() if c['actual_bits'][i - 1] == '1'}
               for i in range(1, 7)}
    assert all(sparse(incomes[i]) == lift['incomes'][i - 1] for i in range(1, 7))
    max_x = {xcols[h]: F(1, d['P'] + 1) for h, d in hist_data.items()}
    fixed_queries = [{'kind': 'actual', 'player': j} for j in range(1, 7)]
    fixed_queries += [{'kind': 'indexed-average', 'family': kind,
                       'members': [kind + str(j) for j in range(1, 7)],
                       'weights': ['1/6'] * 6, 'not_a_pure_action': True}
                      for kind in ('T', 'B', 'C')]
    new_columns, branches, states_by_branch = [], [], {}
    for i in range(1, 5):
        r, m = 7 - i, 5 - i
        tails = [{'kind': 'new-tail', 'source_player': i, 'tail_index': ell,
                  'name': 'Y' + str(ell + 1) + '_at_source' + str(i),
                  'player': i + ell + 1} for ell in range(m)]
        tails.append({'kind': 'new-tail', 'source_player': i, 'tail_index': m,
                      'name': 'T_at_source' + str(i), 'player': 6})
        source_history = ['A' + str(j) for j in range(1, i)]
        forced_history = source_history + ['X']
        terminal_history = forced_history + [q['name'] for q in tails[:-1]]
        pair_history = forced_history + [q['name'] for q in tails[:-2]]
        assert len(terminal_history) == 5 and len(pair_history) == 4
        start = OLD + len(new_columns)
        states = []
        for h in hist:
            for x in (0, 1):
                for tail in product((0, 1), repeat=m + 1):
                    j = OLD + len(new_columns)
                    c = {'kind': 'early-common-X-hidden-tail', 'source_player': i,
                         'remaining_players': r, 'hist_column': h, 'X_column': xcols[h],
                         'X_bit': x, 'middle_bits': list(tail[:-1]), 'terminal_bit': tail[-1],
                         'tail_bits': list(tail), 'ordered_tail_labels': [q['name'] for q in tails]}
                    new_columns.append(c)
                    states.append((j, h, x, tail))
        states_by_branch[i] = states
        branches.append({'source_player': i, 'r': r, 'm': m, 'source_history': source_history,
                         'forced_X_history': forced_history, 'terminal_history': terminal_history,
                         'last_two_prefix': pair_history, 'ordered_tail_labels': tails,
                         'column_range_half_open': [start, OLD + len(new_columns)],
                         'hidden_columns': len(states),
                         'original_source_wallet': 'actual u' + str(i),
                         'forced_X_player_income': 'sum mu*x/(b+1+sum(ys)+t)',
                         'branch_penultimate_income': 'sum mu*z/(b+x+sum(ys[:-1])+1+t)',
                         'branch_terminal_income': 'sum mu*t/(b+x+sum(ys)+1)'})
    assert len(new_columns) == 1920

    def member(q, h, x, tail):
        if q['kind'] == 'X':
            return F(x)
        if q['kind'] == 'new-tail':
            return F(tail[q['tail_index']])
        if q['kind'] == 'actual':
            return F(int(hist_data[h]['actual_bits'][q['player'] - 1]))
        return F(hist_data[h]['indexed_membership_counts'][q['family']], 6)

    raw_rows, unique_rows, exact_lookup, raw_map = [], [], {}, []

    def emit(family, branch, row, wallet, provenance, **metadata):
        assert all(0 <= j < OLD + len(new_columns) for j in row)
        assert all(row.values())
        raw_id = len(raw_rows)
        exact = tuple((j, str(a)) for j, a in sorted(row.items()))
        key = (exact, '0')
        uid = exact_lookup.get(key)
        if uid is None:
            uid = len(unique_rows)
            exact_lookup[key] = uid
            unique_rows.append({'id': uid, 'row': sparse(row), 'rhs': '0',
                                'sense': '>=', 'provenance_raw_row_ids': []})
        unique_rows[uid]['provenance_raw_row_ids'].append(raw_id)
        record = {'raw_id': raw_id, 'unique_row_id': uid, 'family': family,
                  'branch_source_player': branch['source_player'], 'wallet': wallet,
                  'provenance': provenance, **metadata}
        raw_rows.append(record)
        raw_map.append(uid)

    X = {'kind': 'X'}
    for branch in branches:
        i, r, m = branch['source_player'], branch['r'], branch['m']
        states, tails = states_by_branch[i], branch['ordered_tail_labels']
        row = dict(incomes[i])
        for j, h, x, tail in states:
            b = hist_data[h]['actual_backgrounds'][i - 1]
            add(row, j, -F(x, b + 1 + sum(tail)))
        emit('source-IC', branch, row, 'actual u' + str(i),
             {'history': branch['source_history'], 'forced_label': 'X',
              'continuation': 'the original full strategy after this exact forced-X history',
              'payment': ['original source IC'], 'frozen_actual_tail': False})

        for q in tails:
            qname = q['name']
            for actual_j in range(1, 7):
                row = dict(incomes[actual_j])
                for j, h, x, tail in states:
                    b_j = hist_data[h]['actual_backgrounds'][actual_j - 1]
                    add(row, j, -member(q, h, x, tail) / (b_j + 7 - actual_j))
                emit('actual-source-SAFE', branch, row, 'actual u' + str(actual_j),
                     {'history': ['A' + str(k) for k in range(1, actual_j)],
                      'forced_label': qname,
                      'continuation': "that label's own true sigma continuation at the stated actual source",
                      'payment': ['actual-source deviation IC', 'per-member denominator upper bound b_j+7-j'],
                      'actual_terminal_IC_when_j6': actual_j == 6,
                      'frozen_forced_X_tail': False}, query=q, actual_source_player=actual_j)
            row = dict(max_x)
            for j, h, x, tail in states:
                add(row, j, -member(q, h, x, tail) / (hist_data[h]['P'] + 1))
            emit('same-P-MAX', branch, row, 'F_X at actual first-four P',
                 {'history': ['A1', 'A2', 'A3', 'A4'], 'maximizer': 'the one global X',
                  'payment': ['full-catalog f_P maximum'], 'no_hist_dependent_maximizer': True}, query=q)
            row = {0: F(1)}
            for j, h, x, tail in states:
                add(row, j, -member(q, h, x, tail))
            emit('catalog-capacity', branch, row, 'global K',
                 {'payment': ['K bounds every legal label size'], 'legal_label': qname}, query=q)
            row = dict(incomes[5])
            for j, h, x, tail in states:
                add(row, j, -member(q, h, x, tail) / (hist_data[h]['P'] + 1 + x))
            emit('actual-MX-cap', branch, row, 'actual u5',
                 {'history': ['A1', 'A2', 'A3', 'A4'], 'hidden_true_reply': 'V=sigma6(actual h4,X)',
                  'payment': ['u5-U_P(X,V)', 'U_P(V,X)-U_P(Q,X)', 'F_X-f_P(V)'],
                  'not_a_forced_branch_income': True, 'maximum_background': 'actual first-four P'}, query=q)

        terminal_queries = [X] + fixed_queries[:6] + tails[:-1] + fixed_queries[6:]
        for q in terminal_queries:
            row = {}
            for j, h, x, tail in states:
                b = hist_data[h]['actual_backgrounds'][i - 1]
                add(row, j, (F(tail[-1]) - member(q, h, x, tail)) / (b + x + sum(tail[:-1]) + 1))
            emit('branch-terminal-BR', branch, row, 'branch terminal income reconstructed from mu',
                 {'history': branch['terminal_history'], 'chosen_label': tails[-1]['name'],
                  'payment': ['true terminal IC'], 'average_is_literal_query_average': q['kind'] == 'indexed-average',
                  'uses_actual_u6': False}, query=q)

        pair_queries = fixed_queries[:6] + tails[:-1] + fixed_queries[6:]
        pairs = [(q, X, 'Q,X') for q in pair_queries]
        pairs += [(q, q, 'Q,Q') for q in pair_queries]
        pairs += [(X, X, 'X,X')]
        for q, s, mode in pairs:
            row = {}
            for j, h, x, tail in states:
                b = hist_data[h]['actual_backgrounds'][i - 1]
                z, t = tail[-2], tail[-1]
                d = b + x + sum(tail[:-2]) + 1
                qv, sv = member(q, h, x, tail), member(s, h, x, tail)
                overlap = qv if mode == 'Q,Q' else qv * sv
                H = F(z, d + t) + F(t, d + z) + F(z, d * (d + 1))
                add(row, j, H - (qv + sv) / d + overlap / (d * (d + 1)))
            emit('branch-true-PAIR', branch, row, 'branch U5+U6+g(z,z), all from mu',
                 {'history': branch['last_two_prefix'], 'actual_penultimate_label': tails[-2]['name'],
                  'actual_terminal_label': tails[-1]['name'],
                  'hidden_true_reply': 'J_Q=sigma6(this exact prefix,Q)',
                  'payment': ['U5-U(Q,J_Q)', 'U(J_Q,Q)-U(R,Q)', 'U6-U(J_Q,z)', 'g(z,z)-g(z,J_Q)'],
                  'last_payment_pointwise_nonnegative': 'z*(1-j_Q)/(d*(d+1))',
                  'uses_actual_u5_or_u6': False, 'diagonal_average_is_q_not_q_squared': True},
                 query_left=q, query_right=s, mode=mode)

        actual_pairs = [(q, s, 'new-tail-unordered') for q, s in combinations_with_replacement(tails, 2)]
        actual_pairs += [(q, s, 'new-tail-known') for q in tails for s in fixed_queries]
        for q, s, kind in actual_pairs:
            row = dict(incomes[5])
            for j, a in max_x.items():
                add(row, j, a)
            for j, h, x, tail in states:
                p = hist_data[h]['P']
                qv, sv = member(q, h, x, tail), member(s, h, x, tail)
                add(row, j, -(qv + sv) / (p + 1) + qv * sv / ((p + 1) * (p + 2)))
            emit('actual-RC', branch, row, 'actual u5 + F_X',
                 {'history': ['A1', 'A2', 'A3', 'A4'], 'hidden_true_reply': 'V_Q=sigma6(actual h4,Q)',
                  'payment': ['u5-U_P(Q,V_Q)', 'U_P(V_Q,Q)-U_P(R,Q)', 'F_X-f_P(V_Q)'],
                  'not_a_branch_PAIR_wallet': True, 'maximum_background': 'actual first-four P',
                  'cross_branch_unknown_intersections': False},
                 query_left=q, query_right=s, pair_class=kind)

    eq_rows = []
    for branch in branches:
        i = branch['source_player']
        for h in hist:
            for x in (0, 1):
                row = {j: F(1) for j, hh, xx, tail in states_by_branch[i] if (hh, xx) == (h, x)}
                if x:
                    add(row, xcols[h], F(-1))
                else:
                    add(row, h, F(-1))
                    add(row, xcols[h], F(1))
                eq_rows.append({'id': len(eq_rows), 'name': ['common-X-tail-mass', i, h, x],
                                'row': sparse(row), 'rhs': '0', 'sense': '=',
                                'provenance': {'source_player': i, 'hist_column': h, 'X_bit': x,
                                               'required_identity': 'sum_tail mu = x_h' if x else 'sum_tail mu = H_h-x_h',
                                               'shared_X_column': xcols[h]}})
    assert len(eq_rows) == 128
    family_counts = Counter(v['family'] for v in raw_rows)
    assert family_counts == {'source-IC': 4, 'actual-source-SAFE': 84, 'same-P-MAX': 14,
                             'catalog-capacity': 14, 'actual-MX-cap': 14, 'branch-terminal-BR': 50,
                             'branch-true-PAIR': 96, 'actual-RC': 160}
    assert len(raw_rows) == 436
    base_contract = {
        'base_matrix_path': str(FILES['final_matrix'].relative_to(REPO)),
        'base_matrix_sha256': before['final_matrix'], 'base_rows': BASE_ROWS, 'base_columns': OLD,
        'base_nonzeros': 3313758, 'all_base_columns_nonnegative': True,
        'base_descriptors_sha256': final_sha,
        'old_full_descriptors_sha256': sha256(canonical(full)).hexdigest(),
        'first_20601_descriptors_identical': True,
        'final_420_descriptors_keep_all_legacy_fields': True,
        'final_added_semantic_fields': changes,
        'histograms': list(hist_data.values()), 'zero_histograms_retained': zero_hist,
        'actual_income_rows': {str(i): sparse(v) for i, v in incomes.items()},
        'F_X_row': sparse(max_x), 'K_column': 0,
        'indexed_literal_labels': indexed,
        'existing_normalization': {'row': [[h, '1'] for h in hist], 'rhs': '1'},
        'support_boundary': 'Fixed 16-hist support; universal formulas cover all true SPE, this finite matrix covers those whose old projection has this support.',
    }
    packet = {
        'schema': 'early-shared-X-joint-symbolic-append/v1', 'status': 'WEIGHT_FREE_GENERIC_LAYER_NO_SOLVE',
        'base_contract': base_contract, 'old_columns': OLD, 'new_columns': new_columns,
        'total_columns': OLD + len(new_columns), 'branches': branches,
        'fixed_known_queries': fixed_queries, 'raw_inequality_provenance': raw_rows,
        'raw_to_unique_inequality': raw_map, 'inequalities': unique_rows, 'equalities': eq_rows,
        'all_new_columns_nonnegative': True,
        'nonnegativity_representation': '1920 lower bounds; no 1920 redundant identity matrix rows appended',
        'deduplication': 'Exact rational sparse-vector and RHS equality only, with every raw source record retained; no assumed label inequality or alias.',
        'baseline_append_semantics': 'Keep all 23676 old rows, old normalization and old columns exactly; pad them with 1920 zero coefficients, then append these >= and = rows.',
        'not_modeled': ['cross-forced-X-branch intersection tables', 'full old R/Z joint client law',
                        'all off-path histories', 'complete SPE feasibility', 'a new gamepoint'],
        'optimizer_calls': 0, 'fixed_point_values_loaded': False,
    }
    template_rows = []
    for kind, records in (('>=', unique_rows), ('=', eq_rows)):
        for record in records:
            old_part, mu_part = [], []
            for j, a in record['row']:
                if j < OLD:
                    old_part.append([j, str(-F(a))])
                else:
                    mu_part.append([j - OLD, a])
            template_rows.append({'id': record['id'], 'sense': kind, 'hidden_coefficients': mu_part,
                                  'rhs_old_linear_form': old_part, 'rhs_constant': '0'})
    template = {
        'schema': 'early-shared-X-fixed-point-template/v1', 'status': 'UNFILLED_AWAIT_MAIN_NEXT_23676_EXACT_POINT',
        'base_contract': base_contract, 'hidden_columns': new_columns, 'hidden_column_count': 1920,
        'hidden_lower_bounds': ['0'] * 1920, 'rows': template_rows,
        'objective': None, 'optimizer_authorization': False,
        'point_binding': {'main_release_reference': None, 'exact_point_sha256': None,
                          'base_matrix_sha256': before['final_matrix'],
                          'base_descriptors_sha256': final_sha, 'old_vector': None},
        'fill_rule': 'Fill only after Main explicitly supplies the NEXT exact point for the unchanged 23676x21021 matrix; supply all 21021 rational coordinates, not merely hist/X marginals.',
        'interpretation': 'At a fixed complete old vector, infeasibility rejects that fixed extension only; it does not reject all reselected X/overlaps or the projected old feasible face.',
        'standalone': 'All hidden coefficients and symbolic RHS linear forms are included; no baseline or generator import is required to bind an explicitly released exact old vector.',
    }
    after = {key: digest(path) for key, path in FILES.items()}
    assert before == after, 'read-only source changed during build'
    save('symbolic_append.json.gz', packet)
    save('columns_22941.json.gz', final + new_columns)
    save('base_coordinate_contract.json', base_contract)
    save('fixed_point_feasibility_template.json.gz', template)
    save('main_point_release_template.json', {
        'schema': 'main-next-23676-point-release/v1', 'main_release_reference': None,
        'exact_point_sha256': None, 'base_matrix_sha256': before['final_matrix'],
        'base_descriptors_sha256': final_sha, 'old_vector': None,
        'required_old_vector_length': OLD, 'format': 'Every coordinate is a nonnegative exact rational string.',
        'no_point_is_authorized_or_loaded': True})
    save('source_manifest.json', {'sources': {key: {'path': str(path.relative_to(REPO)), 'sha256': before[key],
                                                  'bytes': path.stat().st_size} for key, path in FILES.items()},
                                  'no_point_file_read': True, 'optimizer_calls': 0,
                                  'frozen_input_writes': 0, 'source_hashes_unchanged_after_build': True})
    summary = {
        'status': 'BUILT_EXACT_WEIGHT_FREE_LAYER', 'base_shape': [BASE_ROWS, OLD],
        'new_hidden_columns': len(new_columns), 'total_columns': OLD + len(new_columns),
        'hidden_columns_by_source': {str(b['source_player']): b['hidden_columns'] for b in branches},
        'raw_inequalities': len(raw_rows), 'unique_inequalities': len(unique_rows),
        'exact_duplicate_inequalities_removed': len(raw_rows) - len(unique_rows),
        'new_equalities': len(eq_rows), 'new_nonnegative_bounds': len(new_columns),
        'inequality_counts_by_family': dict(family_counts),
        'new_inequality_nonzeros': sum(len(v['row']) for v in unique_rows),
        'new_equality_nonzeros': sum(len(v['row']) for v in eq_rows),
        'append_shape_with_equalities_separate': {'ge': [BASE_ROWS + len(unique_rows), OLD + len(new_columns)],
                                                 'new_eq': [len(eq_rows), OLD + len(new_columns)],
                                                 'old_normalization_retained': True},
        'all_rows_shape_excluding_bounds': [BASE_ROWS + len(unique_rows) + len(eq_rows), OLD + len(new_columns)],
        'used_old_column_indices': sorted({j for records in (unique_rows, eq_rows) for v in records for j, a in v['row'] if j < OLD}),
        'fixed_point_template_unfilled': True, 'optimizer_calls': 0,
        'base_matrix_sha256': before['final_matrix'], 'base_descriptors_sha256': final_sha,
        'new_columns_sha256': sha256(canonical(new_columns)).hexdigest(),
        'all_columns_sha256': sha256(canonical(final + new_columns)).hexdigest(),
        'symbolic_append_sha256': digest(HERE / 'symbolic_append.json.gz'),
        'fixed_point_template_sha256': digest(HERE / 'fixed_point_feasibility_template.json.gz'),
    }
    save('build_summary.json', summary)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    build()
