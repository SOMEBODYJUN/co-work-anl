"""Independent exact audit; imports no builder, recovery module, or optimizer.

Rebuilds the 42 literal pair orbits from all 720 permutations of representatives,
the 39 nonself budgets by ungrouped literal summation, and all 5580 new rows from
the original descriptors.  No primal point is opened.  Only its audit is written.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations, product
from pathlib import Path
import gzip
import json

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
MATRIX = WORK / 'common_x_joint_lp/final/exact_matrix.json.gz'
PIN = '1b4a4e544e5b9eeea1fa64b3849a9d4cc532b997a5ad972ce33df81c224551e7'


def sha(path): return sha256(path.read_bytes()).hexdigest()


def read(path):
    with gzip.open(path, 'rt', encoding='utf-8') if path.suffix == '.gz' else path.open() as f:
        return json.load(f)


def freeze(value):
    return tuple(map(freeze, value)) if isinstance(value, (list, tuple)) else value


def encode(row): return [[j, str(a)] for j, a in sorted(row.items()) if a]


def canon(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()


def main():
    assert sha(MATRIX) == PIN
    matrix = read(MATRIX)
    manifest = read(HERE / 'build_manifest.json')
    assert manifest['matrix_sha256'] == PIN
    for item in manifest['products']:
        assert sha(HERE / item['path']) == item['sha256']
    for item in manifest['inputs']:
        assert sha(WORK / item['path']) == item['sha256']
    assert sha(HERE / 'build_interface.py') == manifest['builder_sha256']
    layer = read(HERE / 'conditioned_upper_rows.json')
    interface = read(HERE / 'column_interface.json')
    literal = read(HERE / 'literal_orbit_interface.json.gz')
    sign = read(HERE / 'old_aux_sign_audit.json')
    boolean = read(HERE / 'literal_boolean_audit.json')
    columns, rows, names = matrix['columns'], matrix['rows'], matrix['row_names']
    assert (len(rows), len(columns)) == (23676, 21021)
    assert all(x['matrix_sha256'] == PIN for x in (layer, interface, literal, sign, boolean))
    assert sha256(canon(columns)).hexdigest() == interface['descriptors_sha256']
    hist, own, last_hist = {}, defaultdict(dict), None
    for j, col in enumerate(columns[:4849]):
        if col['kind'] == 'hist':
            hist[j] = col
            last_hist = j
        elif col['kind'] == 'joint-reply':
            key = (last_hist, freeze(col['group']))
            state = tuple(col['state'])
            assert state not in own[key]
            own[key][state] = j
    assert len(hist) == 16 and len(own) == 194
    assert all(set(states) == {(0, 1), (1, 0), (1, 1)} for states in own.values())
    lookup = {name: i for i, name in enumerate(names)}
    old_upper_rows = {}
    for i, name in enumerate(names):
        if name.startswith('joint-state-upper:'):
            row = dict(rows[i])
            h = next(j for j, a in row.items() if j in hist and a == '1')
            group = freeze(columns[next(j for j, a in row.items() if a == '-1')]['group'])
            assert rows[i] == encode({h: F(1), **{j: F(-1) for j in own[h, group].values()}})
            old_upper_rows[h, group] = i
    assert set(old_upper_rows) == set(own)
    xs = {c['hist_column']: j for j, c in enumerate(columns) if c['kind'] == 'common-X-mass'}
    ys = {(c['hist_column'], freeze(c['query_token'])): j for j, c in enumerate(columns)
          if c['kind'] == 'X-query-overlap-upper'}
    assert set(xs) == set(hist) and set(ys.values()) == set(range(20601, 21021))
    for j in ys.values():
        upgrade = columns[j]['semantic_upgrade']
        assert upgrade['recovery_role'] == 'core' and not upgrade['canonical_min_permitted']
    pm = {}
    candidates = []
    inherited_nonnegative_endpoint_contracts = []
    for block in interface['blocks']:
        p = block['p_column']; col = columns[p]
        assert col['kind'] == 'ZZ-frechet-envelope-upper'
        h, source, query = col['hist_column'], freeze(col['source_group']), freeze(col['query_group'])
        assert block['H_column'] == h and block['X_column'] == xs[h]
        assert freeze(block['source_group']) == source and freeze(block['query_group']) == query
        assert block['source_own_upper_row'] == old_upper_rows[h, source]
        assert block['query_own_upper_row'] == old_upper_rows[h, query]
        assert (h, source, query) not in pm
        pm[h, source, query] = p
        q = {j: F(1) for state, j in own[h, source].items() if state[0]}
        v = {j: F(1) for state, j in own[h, query].items() if state[1]}
        r, z = ys[h, ('R', source)], ys[h, ('Z', query)]
        assert block['r_column'] == r and block['z_column'] == z
        assert block['q_marginal'] == columns[r]['query_marginal'] == encode(q)
        assert block['v_marginal'] == columns[z]['query_marginal'] == encode(v)
        # Directly write coefficients without the builder's endpoint helper.
        upper1, upper2 = {**v, r: F(1), z: F(-1), p: F(-1)}, {**q, r: F(-1), z: F(1), p: F(-1)}
        new = [encode(upper1), encode(upper2)]
        for k, expected in zip(block['new_candidate_rows'], new):
            record = layer['rows'][k]
            assert record['row'] == expected and record['p_column'] == p
            assert record['candidate_index'] == k and record['hypothetical_append_index'] == 23676+k
            candidates.append(expected)
        endpoints = [encode(q), encode(v),
                     encode({**v, r: F(1), z: F(-1)}),
                     encode({**q, r: F(-1), z: F(1)})]
        assert [e['row'] for e in block['endpoints']] == endpoints
        for i, expected in zip(block['old_upper_rows'], (encode({**q, p: F(-1)}), encode({**v, p: F(-1)}))):
            assert rows[i] == expected
        qi = lookup['common-max-B:' + json.dumps(['overlap-at-most-query', r], separators=(',', ':'))]
        vi = lookup['common-max-B:' + json.dumps(['overlap-at-most-query', z], separators=(',', ':'))]
        assert rows[qi] == encode({**q, r: F(-1)})
        assert rows[vi] == encode({**v, z: F(-1)})
        inherited_nonnegative_endpoint_contracts.append(
            dict(p_column=p, q_minus_r_row=qi, v_minus_z_row=vi,
                 nonnegative_r_column=r, nonnegative_z_column=z))
    assert set(pm.values()) == set(range(12803, 15593))
    assert len(candidates) == len({canon(row) for row in candidates}) == 5580
    assert layer['candidate_to_distinct'] == list(range(5580))
    assert layer['new_columns'] == 0 and layer['nonzeros'] == 27900
    assert layer['hypothetical_appended_shape'] == [29256, 21021]

    # Independent pair-orbit generation by applying every S6 permutation.
    nodes = [(f, i, j) for f in (0, 1) for i in range(6) for j in range(6) if f or i != j]
    assert literal['literal_nodes'] == [list(node) for node in nodes]
    index = {e: k for k, e in enumerate(nodes)}
    permutations6 = list(permutations(range(6)))
    partitions = []
    for pattern in product(range(4), repeat=4):
        if pattern[0] == 0 and all(pattern[k] <= max(pattern[:k])+1 for k in range(1, 4)):
            partitions.append(pattern)
    assert len(partitions) == 15
    orbit_pairs, covered_pairs = {}, set()
    self_orbits = []
    for family_e, family_f in product((0, 1), repeat=2):
        for pattern in partitions:
            e0 = (family_e, pattern[0], pattern[1])
            f0 = (family_f, pattern[2], pattern[3])
            if e0 not in index or f0 not in index:
                continue
            pairs = {(index[(family_e, s[pattern[0]], s[pattern[1]])],
                      index[(family_f, s[pattern[2]], s[pattern[3]])]) for s in permutations6}
            assert not covered_pairs & pairs
            covered_pairs |= pairs
            orbit = family_e, family_f, pattern
            if e0 == f0:
                assert all(a == b for a, b in pairs)
                self_orbits.append(orbit)
            else:
                assert all(a != b for a, b in pairs)
                orbit_pairs[orbit] = pairs
    assert len(orbit_pairs) == 39 and len(self_orbits) == 3
    assert covered_pairs == set(product(range(66), repeat=2))
    assert set(map(freeze, literal['zero_self_orbits'])) == set(self_orbits)
    records = {(rec['H_column'], freeze(rec['orbit']), freeze(rec['source_group']), freeze(rec['query_group'])): rec
               for rec in literal['incidences']}
    assert len(records) == len(literal['incidences']) == 5362
    hist_record = {rec['H_column']: rec for rec in literal['histograms']}
    expected_budgets = {orbit: defaultdict(F) for orbit in orbit_pairs}
    visited_incidence, visited_pairs, block_incidence = set(), Counter(), defaultdict(list)
    same_group_different_nodes = 0
    for h, col in hist.items():
        words = []
        for k, count in enumerate(col['hist']):
            words.extend([((k >> 2) & 1, (k >> 1) & 1, k & 1)]*count)
        groups = [(f, int(i == j), words[i], words[j]) for f, i, j in nodes]
        assert hist_record[h]['literal_group_by_node'] == [list((f, eq, list(a), list(b))) for f, eq, a, b in groups]
        members = defaultdict(set)
        for k, g in enumerate(groups): members[g].add(k)
        P = sum(int(bit) for bit in col['actual_bits'][:4]); D = (P+1)*(P+2)
        for orbit, pairs in orbit_pairs.items():
            class_pairs = defaultdict(set)
            for e, f in pairs:
                g, k = groups[e], groups[f]
                class_pairs[g, k].add((e, f))
                source, query = own[h, g], own[h, k]
                row = expected_budgets[orbit]
                # Ungrouped literal sum, using exactly one copy of each true IC.
                row[source[0, 1]] += F(1, P+1)
                row[source[1, 1]] += F(1, P+1)-F(1, D)
                row[query[0, 1]] -= F(1, P+1)
                row[query[1, 1]] -= F(1, P+1)
                row[pm[h, g, k]] += F(1, D)
                visited_pairs[orbit] += 1
                if g == k:
                    same_group_different_nodes += 1
            for (g, k), selected in class_pairs.items():
                key = h, orbit, g, k
                rec = records[key]; visited_incidence.add(key)
                assert set(map(tuple, rec['literal_pairs'])) == selected
                source_degree = Counter(e for e, f in selected)
                query_degree = Counter(f for e, f in selected)
                assert all(source_degree[e] == rec['source_degree'] for e in members[g])
                assert all(query_degree[f] == rec['query_degree'] for f in members[k])
                count = len(selected)
                assert rec['count'] == count
                assert count == rec['source_degree']*len(members[g]) == rec['query_degree']*len(members[k])
                assert rec['source_node_count'] == len(members[g]) and rec['query_node_count'] == len(members[k])
                assert all(rec[t+'_coefficient'] == str(count) for t in ('q', 'v', 'r', 'z'))
                assert rec['p_budget_coefficient'] == str(F(count, D))
                assert rec['p_column'] == pm[h, g, k]
                block_incidence[rec['p_column']].append(rec['incidence_index'])
    assert visited_incidence == set(records)
    assert sum(visited_pairs.values()) == 68640
    assert same_group_different_nodes == literal['same_group_distinct_literal_pair_hist_terms'] == 9944
    for block in interface['blocks']:
        assert sorted(block_incidence[block['p_column']]) == block['literal_incidence_indices']
    for rec in literal['budgets']:
        orbit = freeze(rec['orbit']); i = rec['row_index']
        assert rows[i] == encode(expected_budgets[orbit])
        assert rec['literal_pair_hist_terms'] == visited_pairs[orbit]
        assert rec['literal_pairs_per_hist']*16 == visited_pairs[orbit]
        assert rec['row_sha256'] == sha256(canon(rows[i])).hexdigest()
    assert len(literal['budgets']) == 39

    # All signs are independently scanned over the entire frozen matrix.
    appearances = defaultdict(list); max_positive = defaultdict(list); max_negative = Counter()
    for i, row in enumerate(rows):
        for j, value in row:
            if 12803 <= j < 15593:
                appearances[j].append([i, value])
            elif 4849 <= j < 12803:
                if F(value) > 0: max_positive[j].append([i, value])
                else:
                    assert F(value) < 0
                    max_negative[j] += 1
    total_positive, total_negative = 0, 0
    for rec in sign['p_appearances']:
        j = rec['column']
        actual = appearances[j]
        positive = [v for v in actual if F(v[1]) > 0]
        negative = [v for v in actual if F(v[1]) < 0]
        assert rec['positive_appearances'] == positive
        assert rec['negative_appearances'] == negative
        assert len(negative) == 2 and all(v == '-1' for i, v in negative)
        assert all(19511 <= i < 19550 for i, a in positive)
        assert matrix['objective'][j] == matrix['normalization'][j] == '0'
        total_positive += len(positive); total_negative += len(negative)
    assert len(sign['p_appearances']) == 2790 and total_negative == 5580 and total_positive == 5362
    for rec in sign['max_column_summary']:
        j, i = rec['column'], rec['threshold_row']
        assert max_positive[j] == [[i, '1']]
        assert max_negative[j] == rec['negative_old_appearances']
        assert all(k < 4849 or k == j for k, a in rows[i])
        assert matrix['objective'][j] == matrix['normalization'][j] == '0'
    assert len(sign['max_column_summary']) == 7954
    assert all(not (4849 <= j < 12803) for row in candidates for j, a in row)
    assert interface['core_columns'] == list(range(4849))+list(range(15593, 21021))
    assert interface['real_overlap_core_columns'] == list(range(20601, 21021))
    assert interface['hist_records'] == [[h, c] for h, c in hist.items()]
    assert interface['historically_zero_histograms'] == [1, 59, 366, 449, 524, 574]
    checked_types = []
    for X, R, Z in product(range(2), repeat=3):
        J, r, z = R*Z, X*R, X*Z
        a, b = r+Z-z-J, R-r+z-J
        assert a == X*R*(1-Z)+(1-X)*Z*(1-R) >= 0
        assert b == (1-X)*R*(1-Z)+X*Z*(1-R) >= 0
        rec = boolean['rows'][len(checked_types)]
        assert (rec['x'], rec['R'], rec['Z']) == (X, R, Z)
        assert rec['r_plus_v_minus_z_minus_J'] == a and rec['q_minus_r_plus_z_minus_J'] == b
        checked_types.append([X, R, Z])
    report = dict(
        status='PASS_INDEPENDENT_SYMBOLIC_INTERFACE', matrix_sha256=PIN,
        builder_imported=False, original_point_files_opened=0, optimizer_calls=0,
        candidate_rows=5580, new_columns=0, nonzeros=27900,
        old_rows_fully_sign_scanned=23676,
        old_min_columns_fully_audited=2790,
        negative_old_p_appearances=5580, positive_old_p_appearances=5362,
        old_max_columns_unchanged=7954, real_overlap_core_columns_unchanged=420,
        core_columns_retained=10277, all_21021_columns_retained=True,
        all_16_histograms_retained=True, historical_zero_histograms_retained=[1, 59, 366, 449, 524, 574],
        independent_permutation_orbits=42, permutations_per_representative=720,
        nonself_budget_rows_rebuilt_by_literal_sum=39,
        literal_nonself_pair_hist_terms=68640,
        same_group_distinct_literal_terms_retained=9944,
        incidence_classes_with_exact_uniform_source_and_query_degrees=5362,
        boolean_types_checked=checked_types,
        no_distinct_literal_nodes_identified=True,
        endpoint_nonnegativity_from_existing_core_rows=inherited_nonnegative_endpoint_contracts,
        build_manifest_sha256=sha(HERE/'build_manifest.json'),
        verifier_sha256=sha(Path(__file__)),
        scope='Exact same-X virtual upper-envelope layer only; no new point, full joint law, SPE or half theorem.')
    (HERE/'independent_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    assert sha(MATRIX) == PIN
    print(json.dumps({k: report[k] for k in
                      ('status', 'candidate_rows', 'new_columns',
                       'literal_nonself_pair_hist_terms',
                       'incidence_classes_with_exact_uniform_source_and_query_degrees')}))


if __name__ == '__main__':
    main()
