"""Freeze the same-X/ZZ extension without opening a point or running a solver.

All source/query maps come from the frozen coordinate descriptors and the
literal 66-node query set.  joint-state-upper rows locate current hist columns;
legacy hist numbers and another task's mapping are never used as coordinates.
Only this owned directory is written.  The 23676-row cloud input is read-only.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import gzip
import json

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
MATRIX = WORK / 'common_x_joint_lp/final/exact_matrix.json.gz'
MATRIX_SHA = '1b4a4e544e5b9eeea1fa64b3849a9d4cc532b997a5ad972ce33df81c224551e7'
M, N = 23676, 21021
P_COLUMNS = set(range(12803, 15593))
MAX_COLUMNS = set(range(4849, 12803))
CORE = list(range(4849)) + list(range(15593, N))
Y_COLUMNS = list(range(20601, 21021))
HISTORICAL_ZERO_HIST = [1, 59, 366, 449, 524, 574]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def frozen(value):
    return tuple(map(frozen, value)) if isinstance(value, (list, tuple)) else value


def encoded(row):
    return [[j, str(v)] for j, v in sorted(row.items()) if v]


def combine(*terms):
    out = defaultdict(F)
    for scale, row in terms:
        for j, value in row.items():
            out[j] += scale * value
    return {j: value for j, value in out.items() if value}


def write(name, value):
    destination = HERE / name
    if destination.suffix == '.gz':
        raw = json.dumps(value, ensure_ascii=False, separators=(',', ':')).encode()
        with destination.open('wb') as stream:
            with gzip.GzipFile(filename='', mode='wb', fileobj=stream, mtime=0) as gz:
                gz.write(raw)
    else:
        destination.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def partition(values):
    labels = {}
    return tuple(labels.setdefault(value, len(labels)) for value in values)


def main():
    assert digest(MATRIX) == MATRIX_SHA
    with gzip.open(MATRIX, 'rt', encoding='utf-8') as stream:
        matrix = json.load(stream)
    columns, rows, names = matrix['columns'], matrix['rows'], matrix['row_names']
    assert (len(rows), len(columns)) == (M, N) and len(names) == M
    assert matrix['all_columns_nonnegative'] and matrix['normalization_rhs'] == '1'
    assert len(set(names)) == M
    name_index = {name: i for i, name in enumerate(names)}
    hist = {j: col for j, col in enumerate(columns) if col['kind'] == 'hist'}
    assert len(hist) == 16 and set(HISTORICAL_ZERO_HIST) <= set(hist)
    groups, legacy, covered = {}, {}, set()
    for i, name in enumerate(names):
        if not name.startswith('joint-state-upper:'):
            continue
        row = {j: F(a) for j, a in rows[i]}
        hs = [j for j, a in row.items() if j in hist and a == 1]
        js = [j for j, a in row.items()
              if a == -1 and columns[j]['kind'] == 'joint-reply']
        assert len(hs) == 1 and len(js) == 3 and len(row) == 4
        h = hs[0]
        gs = {frozen(columns[j]['group']) for j in js}
        assert len(gs) == 1
        group = next(iter(gs))
        assert (h, group) not in groups
        states = {}
        for j in js:
            col = columns[j]
            state = tuple(col['state'])
            assert state not in states and j not in covered
            assert legacy.setdefault(col['hist_column_old'], h) == h
            states[state] = j
            covered.add(j)
        assert set(states) == {(0, 1), (1, 0), (1, 1)}
        groups[h, group] = dict(states=states, row=i)
    assert len(groups) == 194 and len(covered) == 582
    assert covered == {j for j, col in enumerate(columns) if col['kind'] == 'joint-reply'}
    # Independent layout cross-check only; it does not define the mapping.
    h = None
    for j, col in enumerate(columns[:4849]):
        if col['kind'] == 'hist':
            h = j
        elif col['kind'] == 'joint-reply':
            assert groups[h, frozen(col['group'])]['states'][tuple(col['state'])] == j

    xmap, ymap = {}, {}
    for j, col in enumerate(columns):
        if col['kind'] == 'common-X-mass':
            h = col['hist_column']
            assert h in hist and h not in xmap
            xmap[h] = j
        elif col['kind'] == 'X-query-overlap-upper':
            h, token = col['hist_column'], frozen(col['query_token'])
            assert (h, token) not in ymap
            upgrade = col['semantic_upgrade']
            assert upgrade['effective_kind'] == 'real-common-X-query-overlap'
            assert upgrade['recovery_role'] == 'core'
            assert upgrade['canonical_min_permitted'] is False
            ymap[h, token] = j
    assert set(xmap) == set(hist) and list(xmap.values()) == list(range(20585, 20601))
    assert list(ymap.values()) == Y_COLUMNS

    def marginal(h, group, role):
        states = groups[h, group]['states']
        bit = 0 if role == 'R' else 1
        return {j: F(1) for state, j in states.items() if state[bit]}

    rz_query_count = 0
    for (h, token), j in ymap.items():
        if token[0] in ('R', 'Z'):
            assert columns[j]['query_marginal'] == encoded(marginal(h, token[1], token[0]))
            rz_query_count += 1
    assert rz_query_count == 388
    assert {token for h, token in ymap if token[0] == 'H'} == {('H', 0), ('H', 1)}

    pmap, blocks, upper_candidates = {}, [], []
    old_upper_set = set()
    for j, col in enumerate(columns):
        if col['kind'] != 'ZZ-frechet-envelope-upper':
            continue
        assert j in P_COLUMNS
        h = col['hist_column']
        source, query = frozen(col['source_group']), frozen(col['query_group'])
        assert (h, source, query) not in pmap
        pmap[h, source, query] = j
        q, v = marginal(h, source, 'R'), marginal(h, query, 'Z')
        r, z = ymap[h, ('R', source)], ymap[h, ('Z', query)]
        assert r in CORE and z in CORE and r != z
        endpoints = [q, v,
                     combine((1, {r: F(1)}), (1, v), (-1, {z: F(1)})),
                     combine((1, q), (-1, {r: F(1)}), (1, {z: F(1)}))]
        old_upper = []
        for tag, endpoint in zip(('q', 'v'), endpoints[:2]):
            i = name_index[f'ZZ-upper:{j}:{tag}']
            assert rows[i] == encoded(combine((1, endpoint), (-1, {j: F(1)})))
            old_upper.append(i)
            old_upper_set.add(i)
        new_upper = []
        for tag, endpoint in zip(('r+v-z', 'q-r+z'), endpoints[2:]):
            k = len(upper_candidates)
            new_upper.append(k)
            upper_candidates.append(dict(
                candidate_index=k, hypothetical_append_index=M+k,
                name=f'X-conditioned-ZZ-upper:{j}:{tag}', p_column=j,
                H_column=h, X_column=xmap[h], endpoint=tag,
                inequality='>=0', constant='0',
                row=encoded(combine((1, endpoint), (-1, {j: F(1)})))))
        blocks.append(dict(
            block=len(blocks), p_column=j, H_column=h, X_column=xmap[h],
            source_group=source, query_group=query,
            source_query_token=['R', source], query_query_token=['Z', query],
            r_column=r, z_column=z, q_marginal=encoded(q), v_marginal=encoded(v),
            source_own_upper_row=groups[h, source]['row'],
            query_own_upper_row=groups[h, query]['row'],
            endpoints=[dict(name=tag, row=encoded(endpoint)) for tag, endpoint in
                       zip(('q', 'v', 'r+v-z', 'q-r+z'), endpoints)],
            old_upper_rows=old_upper, new_candidate_rows=new_upper))
    assert set(pmap.values()) == P_COLUMNS and len(blocks) == 2790
    assert len(old_upper_set) == len(upper_candidates) == 5580
    signatures = [canonical(record['row']) for record in upper_candidates]
    assert len(set(signatures)) == 5580
    # No old row contains both a ZZ p and a real X overlap, so none is an old duplicate.
    for row in rows:
        js = {j for j, _ in row}
        assert not (js & P_COLUMNS and js & set(Y_COLUMNS))

    literal_nodes = [(f, i, j) for f in (0, 1) for i in range(6) for j in range(6)
                     if f == 1 or i != j]
    assert len(literal_nodes) == 66
    full_orbits, nonself_orbits = defaultdict(list), defaultdict(list)
    for ei, e in enumerate(literal_nodes):
        for fi, f in enumerate(literal_nodes):
            orbit = (e[0], f[0], partition((e[1], e[2], f[1], f[2])))
            full_orbits[orbit].append((ei, fi))
            if e != f:
                nonself_orbits[orbit].append((ei, fi))
    assert len(full_orbits) == 42 and len(nonself_orbits) == 39
    self_orbits = set(full_orbits) - set(nonself_orbits)
    assert self_orbits == {(0, 0, (0, 1, 0, 1)), (1, 1, (0, 0, 0, 0)),
                           (1, 1, (0, 1, 0, 1))}
    assert sum(map(len, nonself_orbits.values())) == 4290
    budgets, orbit_totals = defaultdict(lambda: defaultdict(F)), Counter()
    literal_records, hist_records, omitted_self_pairs = [], [], []
    pair_use = defaultdict(list)
    distinct_same_group_pairs = 0
    for h, col in hist.items():
        words = [word for word, count in zip(product((0, 1), repeat=3), col['hist'])
                 for _ in range(count)]
        assert len(words) == 6
        node_group = [(e[0], int(e[1] == e[2]), words[e[1]], words[e[2]])
                      for e in literal_nodes]
        group_nodes = defaultdict(list)
        for node, group in enumerate(node_group):
            group_nodes[group].append(node)
        assert set(group_nodes) == {g for hh, g in groups if hh == h}
        hist_records.append(dict(H_column=h, X_column=xmap[h], descriptor=col,
                                 words=words, literal_group_by_node=node_group,
                                 groups=[dict(group=g, node_indices=ns, size=len(ns))
                                         for g, ns in sorted(group_nodes.items())],
                                 all_66_nodes_retained=True))
        actual_pairs = set()
        P = sum(map(int, col['actual_bits'][:4]))
        D = (P+1)*(P+2)
        for orbit, pairs in sorted(nonself_orbits.items()):
            grouped_pairs = defaultdict(list)
            for ei, fi in pairs:
                grouped_pairs[node_group[ei], node_group[fi]].append((ei, fi))
            for (source, query), selected in sorted(grouped_pairs.items()):
                count = len(selected)
                actual_pairs.add((source, query))
                p = pmap[h, source, query]
                source_degrees = Counter(ei for ei, fi in selected)
                query_degrees = Counter(fi for ei, fi in selected)
                assert set(source_degrees) == set(group_nodes[source])
                assert set(query_degrees) == set(group_nodes[query])
                assert len(set(source_degrees.values())) == len(set(query_degrees.values())) == 1
                source_degree = next(iter(source_degrees.values()))
                query_degree = next(iter(query_degrees.values()))
                assert count == source_degree*len(group_nodes[source])
                assert count == query_degree*len(group_nodes[query])
                if source == query:
                    distinct_same_group_pairs += count
                local_index = len(literal_records)
                pair_use[p].append(local_index)
                literal_records.append(dict(
                    incidence_index=local_index, H_column=h, orbit=orbit,
                    source_group=source, query_group=query, p_column=p,
                    literal_pairs=selected, count=count,
                    source_node_count=len(group_nodes[source]),
                    query_node_count=len(group_nodes[query]),
                    source_degree=source_degree, query_degree=query_degree,
                    q_coefficient=str(F(count)), v_coefficient=str(F(count)),
                    r_coefficient=str(F(count)), z_coefficient=str(F(count)),
                    p_budget_coefficient=str(F(count, D))))
                row = budgets[orbit]
                source_states = groups[h, source]['states']
                query_states = groups[h, query]['states']
                for state in ((0, 1), (1, 1)):
                    row[source_states[state]] += F(count, P+1)
                    row[query_states[state]] -= F(count, P+1)
                row[source_states[1, 1]] -= F(count, D)
                row[p] += F(count, D)
                orbit_totals[orbit] += count
        expected_pairs = {(g, k) for g in group_nodes for k in group_nodes
                          if g != k or len(group_nodes[g]) > 1}
        assert actual_pairs == expected_pairs
        omitted = [(g, k) for g in group_nodes for k in group_nodes
                   if (g, k) not in actual_pairs]
        assert len(omitted) == 1 and omitted[0][0] == omitted[0][1]
        g = omitted[0][0]
        assert len(group_nodes[g]) == 1
        omitted_self_pairs.append(dict(H_column=h, group=g,
                                       sole_literal_node=literal_nodes[group_nodes[g][0]]))
    assert sum(orbit_totals.values()) == 68640
    assert set(pair_use) == P_COLUMNS and len(omitted_self_pairs) == 16
    budget_records = []
    budget_set = set()
    for orbit, row in sorted(budgets.items()):
        name = 'ZZ-full-min:' + json.dumps(orbit, separators=(',', ':'))
        i = name_index[name]
        assert encoded(row) == rows[i]
        assert all(a > 0 for j, a in row.items() if j in P_COLUMNS)
        assert all(j < 4849 or j in P_COLUMNS for j, a in row.items() if a)
        assert orbit_totals[orbit] == 16*len(nonself_orbits[orbit])
        budget_set.add(i)
        budget_records.append(dict(
            row_index=i, name=name, orbit=orbit,
            literal_pairs_per_hist=len(nonself_orbits[orbit]),
            literal_pair_hist_terms=orbit_totals[orbit],
            row_sha256=sha256(canonical(rows[i])).hexdigest(),
            p_terms=[[j, str(a)] for j, a in sorted(row.items()) if j in P_COLUMNS]))
    assert budget_set == set(range(19511, 19550))

    # Scan every coefficient of every old row, not only rows named "ZZ".
    p_appearances = defaultdict(list)
    max_positive, max_negative = defaultdict(list), Counter()
    for i, row in enumerate(rows):
        assert len(row) == len({j for j, _ in row})
        for j, value in row:
            if j in P_COLUMNS:
                assert F(value)
                p_appearances[j].append([i, value])
            elif j in MAX_COLUMNS:
                value = F(value)
                if value > 0:
                    max_positive[j].append([i, str(value)])
                else:
                    assert value < 0
                    max_negative[j] += 1
    appearance_records = []
    for block in blocks:
        j = block['p_column']
        negative = [a for a in p_appearances[j] if F(a[1]) < 0]
        positive = [a for a in p_appearances[j] if F(a[1]) > 0]
        assert negative == [[i, '-1'] for i in block['old_upper_rows']]
        assert positive and all(i in budget_set for i, a in positive)
        assert F(matrix['objective'][j]) == F(matrix['normalization'][j]) == 0
        block['literal_incidence_indices'] = pair_use[j]
        appearance_records.append(dict(
            column=j, negative_appearances=negative, positive_appearances=positive,
            objective_coefficient='0', normalization_coefficient='0',
            nonnegative_column=True, new_negative_candidate_rows=block['new_candidate_rows']))
    max_records = []
    for j in sorted(MAX_COLUMNS):
        assert len(max_positive[j]) == 1 and max_positive[j][0][1] == '1'
        i = max_positive[j][0][0]
        assert all(k < 4849 or k == j for k, a in rows[i])
        assert F(matrix['objective'][j]) == F(matrix['normalization'][j]) == 0
        max_records.append(dict(column=j, threshold_row=i,
                                negative_old_appearances=max_negative[j],
                                new_layer_appearances=0))
    assert matrix['canonical_max_auxiliaries'] == len(max_records) == 7954
    assert matrix['canonical_min_auxiliaries'] == len(blocks) == 2790
    assert matrix['core_columns'] == len(CORE) == 10277
    assert matrix['canonical_auxiliary_columns'] == len(P_COLUMNS | MAX_COLUMNS) == 10744
    assert not set(CORE) & (P_COLUMNS | MAX_COLUMNS)
    assert set(CORE) | P_COLUMNS | MAX_COLUMNS == set(range(N))
    assert not set(j for rec in upper_candidates for j, a in rec['row']) & MAX_COLUMNS

    boolean_rows = []
    for x, R, Z in product((0, 1), repeat=3):
        J, r, z = R*Z, x*R, x*Z
        lhs1, lhs2 = r+Z-z-J, R-r+z-J
        rhs1 = x*R*(1-Z) + (1-x)*Z*(1-R)
        rhs2 = (1-x)*R*(1-Z) + x*Z*(1-R)
        assert lhs1 == rhs1 >= 0 and lhs2 == rhs2 >= 0
        boolean_rows.append(dict(x=x, R=R, Z=Z, J=J,
                                 r_plus_v_minus_z_minus_J=lhs1,
                                 q_minus_r_plus_z_minus_J=lhs2,
                                 nonnegative_identity_1=rhs1,
                                 nonnegative_identity_2=rhs2))
    # Exact algebra check on all nonnegative integer quadrant masses through 4.
    # The proof is the independent choice of one term from each minimum.
    identity_checks = 0
    for r, z, qr, vz in product(range(5), repeat=4):
        q, v = r+qr, z+vz
        assert min(q, v, r+v-z, q-r+z) == min(r, z)+min(qr, vz)
        identity_checks += 1

    common = dict(schema='same-X-conditioned-ZZ-interface-v1',
                  status='FROZEN_SYMBOLIC_INTERFACE_NO_POINT_USED',
                  run='six-boss1-20261111', matrix_sha256=MATRIX_SHA,
                  base_matrix='common_x_joint_lp/final/exact_matrix.json.gz',
                  base_shape=[M, N], optimizer_calls=0, point_files_opened=0,
                  descriptors_sha256=sha256(canonical(columns)).hexdigest())
    write('conditioned_upper_rows.json', dict(
        **common, candidate_count=5580, distinct_count=5580, new_columns=0,
        nonzeros=sum(len(record['row']) for record in upper_candidates),
        hypothetical_appended_shape=[M+5580, N], larger_matrix_assembled=False,
        deduplication='none; all 5580 exact sparse vectors are distinct and new',
        candidate_to_distinct=list(range(5580)), rows=upper_candidates))
    write('column_interface.json', dict(
        **common, blocks=blocks, block_count=2790,
        core_columns=CORE, real_overlap_core_columns=Y_COLUMNS,
        X_columns=list(xmap.values()), unchanged_max_columns=sorted(MAX_COLUMNS),
        changed_canonical_rule_columns=sorted(P_COLUMNS),
        canonical_endpoint_order=['q', 'v', 'r+v-z', 'q-r+z'],
        canonical_rule='min(q,v,r+v-z,q-r+z)',
        canonical_min_for_real_420_forbidden=True,
        hist_records=[[h, c] for h, c in hist.items()],
        historically_zero_histograms=HISTORICAL_ZERO_HIST,
        all_16_histograms_and_all_21021_columns_retained=True,
        legacy_hist_mapping_crosscheck=sorted(legacy.items())))
    write('literal_orbit_interface.json.gz', dict(
        **common, literal_nodes=literal_nodes, histograms=hist_records,
        full_orbit_count=42, nonself_orbit_count=39,
        literal_nonself_pair_hist_terms=68640,
        same_group_distinct_literal_pair_hist_terms=distinct_same_group_pairs,
        zero_self_orbits=sorted(self_orbits),
        omitted_singleton_self_group_pairs=omitted_self_pairs,
        all_incidence_classes_biregular=True, incidence_class_count=len(literal_records),
        incidences=literal_records, budgets=budget_records,
        X_identity='One fixed label X; no comparison index and no per-orbit reselection.',
        grouped_event_identification=False,
        average_identity='sum_S XR_e=count*r_hg and sum_S XZ_f=count*z_hk'))
    write('old_aux_sign_audit.json', dict(
        **common, scanned_rows=M,
        scanned_nonzero_coefficients=sum(map(len, rows)),
        p_column_count=2790,
        negative_p_appearance_count=sum(len(r['negative_appearances']) for r in appearance_records),
        positive_p_appearance_count=sum(len(r['positive_appearances']) for r in appearance_records),
        all_negative_old_p_rows_are_two_upper_bounds=True,
        all_positive_old_p_rows_are_true_ZZ_budgets=True,
        old_p_objective_and_normalization_zero=True,
        p_appearances=appearance_records,
        unchanged_max_count=7954, max_column_summary=max_records,
        new_layer_contains_no_max_column=True))
    write('literal_boolean_audit.json', dict(
        **(common | {'status': 'PASS_EIGHT_BOOLEAN_TYPES_AND_SYMBOLIC_INTERFACE'}),
        rows=boolean_rows, eight_types_retained=True,
        min_identity_integer_probes=identity_checks,
        weak_ties_empty_labels_duplicate_coverage_and_zero_mass_allowed=True))
    products = ['conditioned_upper_rows.json', 'column_interface.json',
                'literal_orbit_interface.json.gz', 'old_aux_sign_audit.json',
                'literal_boolean_audit.json']
    inputs = ['main_X_conditioned_ZZ.md', 'main_X_conditioned_ZZ_literal_audit.json',
              'common_coupling_math.md', 'root_x_joint_contract.md',
              'terminal_response_cycles.md', 'common_x_own_lift/build_sparse_layer.py',
              'zz_closure_lp/round2/solve_full.py',
              'common_x_joint_lp/final/verify_certificates.py']
    summary = dict(**(common | {'status': 'READY_FOR_INDEPENDENT_INTERFACE_AUDIT'}),
                   candidate_rows=5580, new_columns=0,
                   nonzeros=sum(len(r['row']) for r in upper_candidates),
                   old_ZZ_budgets_reconstructed=39,
                   literal_terms=68640, incidence_classes=len(literal_records),
                   same_group_distinct_literal_terms=distinct_same_group_pairs,
                   all_old_p_signs_audited=True, all_7954_max_contracts_unchanged=True,
                   all_420_real_core_columns_unchanged=True,
                   all_16_histograms_retained=True,
                   point_diagnostic='NOT_RUN; waiting for a new exact 23676-row point',
                   no_old_point_evaluation=True,
                   products=[dict(path=p, sha256=digest(HERE/p), bytes=(HERE/p).stat().st_size)
                             for p in products],
                   inputs=[dict(path=p, sha256=digest(WORK/p)) for p in inputs],
                   builder_sha256=digest(Path(__file__)))
    write('build_manifest.json', summary)
    assert digest(MATRIX) == MATRIX_SHA
    print(json.dumps({k: summary[k] for k in
                      ('status', 'candidate_rows', 'new_columns', 'nonzeros',
                       'incidence_classes', 'literal_terms', 'same_group_distinct_literal_terms')}))


if __name__ == '__main__':
    main()
