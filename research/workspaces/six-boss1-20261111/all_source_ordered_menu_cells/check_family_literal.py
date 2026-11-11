#!/usr/bin/env python3
"""Reconstruct all181 rows from true conditional five-query wallet shares."""
from fractions import Fraction as F
from itertools import product
import hashlib
import json
from pathlib import Path
from interpolate_cell import interpolate

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = HERE.parents[3]
SOURCE = WS / 'all_source_ordered_joint_menu'
GENERAL = WS / 'all_source_joint_reweighted_safe'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text())


def save(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def share(member, total):
    if total == 0:
        assert member == 0
        return F(0)
    return F(member, total)


def loss(i, theta):
    forms = [F(0)]
    for j in range(i + 1, 6):
        forms.append(theta[j] + sum((theta[h] / (5 * (7 - h) * (8 - h))
                                    for h in range(j + 1, 6)), F(0)) - F(2, 5))
    return max(forms)


def closed_G(i, theta, s, p):
    n, ci = 6 - i, F(7 - i, 2)
    D = p + n + 1
    affine = (ci + F(24, D) + F(1, p + 1) - s / min(D, 5)
              + sum((theta[j] / (p + 7 - j) for j in theta), F(0))) / 6
    return affine - (F(5, 6) * loss(i, theta) if p == 0 else F(0))


def true_cost(i, theta, s, p, t, inner_mean, tail):
    a = F(25) + sum(theta.values(), F(0)) - s
    total = p + t + sum(tail)
    source_part = a * share(t, total)
    last_part = -share(tail[-1], total) + tail[-1]
    internal_parts = sum((-theta[j] * share(tail[j - i - 1], total)
                          + F(tail[j - i - 1], 2) for j in theta), F(0))
    last_query = inner_mean / (p + t + sum(tail[:-1]) + 1)
    safe_queries = sum((theta[j] * inner_mean /
                        (p + t + sum(tail[:j - i - 1]) + 7 - j) for j in theta), F(0))
    return source_part + last_part + internal_parts + last_query + safe_queries


def row_at(i, theta, s, G):
    a = F(25) + sum(theta.values(), F(0)) - s
    vector = []
    for column in range(512):
        bits = [(column >> shift) & 1 for shift in range(8, -1, -1)]
        vector.append(a * share(bits[i - 1], sum(bits[:6])) - bits[7] * G[sum(bits[:i - 1])])
    return vector + [F(7 - i, 2)]


def main():
    assert not (HERE / 'freeze_manifest.json').exists()
    assert sha(SOURCE / 'freeze_manifest.json') == 'eb01d5539bc6b6182871df3e14fa800896e46ba63fa3f52176cb2aee562052fe'
    assert sha(SOURCE / 'proof.md') == 'b9049f3c6b9faec5360d17acdcff6f2a16d8900674538b200fcd20ec713f3f08'
    assert sha(SOURCE / 'exact_family.json') == 'd405ead895234dcaa9355cbd61056a7f81013f230d214b108578ead068784510'
    assert sha(SOURCE / 'continuous_G_contract.json') == 'f9ea0d2788925965a999a204c3b9b4ad6eded30a529f962f1f0355eb5be15b85'
    pins = load(HERE / 'source_pins.json')['sources']
    for name, expected in pins.items():
        assert sha(REPO / name) == expected, name
    family = load(HERE / 'exact_family.json')
    geometry = load(HERE / 'parameter_cells.json')
    proof_hash = sha(HERE / 'proof.md')
    assert family['proof_sha256'] == proof_hash
    assert family['parameter_cells_sha256'] == sha(HERE / 'parameter_cells.json')
    assert family['source_pins_sha256'] == sha(HERE / 'source_pins.json')
    assert family['geometry_check_sha256'] == sha(HERE / 'geometry_check_result.json')
    assert family['cell_affine_forms_sha256'] == sha(HERE / 'cell_affine_forms.json')
    assert family['raw_row_count'] == len(family['rows']) == 181 and family['variables'] == 513
    assert family['K_column'] == 512 and family['optimizer_calls'] == 0
    assert family['all_root_vertices_retained'] is True and family['row_pruning'] is False
    domains = {d['source']: d for d in load(GENERAL / 'parameter_polytopes.json')['sources']}
    rows = family['rows']
    rows_by_id = {row['cell_vertex_id']: row for row in rows}
    assert len(rows_by_id) == 181
    assert [row['cell_vertex_id'] for row in rows] == [v['id'] for source in geometry['sources'] for v in source['vertices']]
    coordinates = load(HERE / 'coordinate_contract.json')
    baseline_coordinates = load(GENERAL / 'coordinate_contract.json')
    for key in ('variables', 'K_column', 'bit_order', 'atom_columns', 'nonnegative_columns'):
        assert coordinates[key] == baseline_coordinates[key]
    assert coordinates['nonnegative_columns'] == list(range(513))
    assert coordinates['normalization_used'] is False and coordinates['C_size_equality_used'] is False
    contract = load(SOURCE / 'continuous_G_contract.json')
    for source in contract['sources']:
        i = source['i']
        assert F(source['ci']) == F(7 - i, 2)
        for form in source['loss_affines']:
            j = form['index']
            assert F(form['constant']) == -F(2, 5)
            for h, saved in form['theta_coefficients'].items():
                h = int(h)
                expected = F(0) if h < j else F(1) if h == j else F(1, 5 * (7 - h) * (8 - h))
                assert F(saved) == expected
        for form in source['G_by_prefix']:
            p, D = form['p'], form['p'] + 7 - i
            assert F(form['constant']) == (F(7 - i, 2) + F(24, D) + F(1, p + 1)) / 6
            assert F(form['s_coefficient']) == -F(1, 6 * min(D, 5))
            assert F(form['loss_coefficient']) == (-F(5, 6) if p == 0 else F(0))
            for j, saved in form['theta_coefficients'].items():
                assert F(saved) == F(1, 6 * (p + 7 - int(j)))
    generic_index_checks = 0
    menus = list(product((0, 1), repeat=6))
    for menu in menus:
        d = sum(menu)
        for k, t in enumerate(menu):
            actual_inner_members = [menu[l] for l in range(6) if l != k]
            assert len(actual_inner_members) == 5
            for denominator in range(1, 7):
                literal = sum((F(member, denominator) for member in actual_inner_members), F(0)) / 5
                assert literal == F(d - t, 5 * denominator)
                generic_index_checks += 1
    assert generic_index_checks == 2304

    hidden, conditional, outer, projections, menu_records = [], [], [], [], []
    rebuilt = {}
    outer_indices = 0
    for source in geometry['sources']:
        i = source['source']
        faces = [(F(f['constant']), [F(x) for x in f['coefficients']]) for f in domains[i]['facets']]
        for vertex in source['vertices']:
            point = [F(x) for x in vertex['parameters']]
            assert all(c + dot(normal, point) >= 0 for c, normal in faces)
            theta = {int(j): F(x) for j, x in vertex['theta_by_true_source'].items()}
            s = F(vertex['s'])
            assert F(vertex['L']) == loss(i, theta)
            assert F(vertex['a']) == F(25) + sum(theta.values(), F(0)) - s > 0
            all_G = {}
            for p in range(i):
                minima = {}
                for d in range(7):
                    physical_t = [0] if d == 0 else [1] if d == 6 else [0, 1]
                    for t in physical_t:
                        q = F(d - t, 5)
                        assert 0 <= q <= 1
                        values = [(tail, true_cost(i, theta, s, p, t, q, tail))
                                  for tail in product((0, 1), repeat=6 - i)]
                        minimum = min(v for tail, v in values)
                        minima[d, t] = minimum
                        attainers = [list(tail) for tail, v in values if v == minimum]
                        conditional.append({'vertex_id': vertex['id'], 'source': i, 'p': p, 'd': d, 't': t,
                                            'inner_mean': str(q), 'minimum': str(minimum), 'all_attainers': attainers})
                        for tail, cost in values:
                            hidden.append([vertex['id'], p, d, t, list(tail), str(cost), str(minimum), str(cost - minimum)])
                f = {}
                for d in range(7):
                    f[d] = ((6 - d) * minima[d, 0] if d < 6 else F(0))
                    f[d] += d * minima[d, 1] if d > 0 else F(0)
                    f[d] /= 6
                    outer.append({'vertex_id': vertex['id'], 'p': p, 'd': d, 'f': str(f[d])})
                assert f[0] == 0
                G = min(f[d] for d in range(1, 7))
                assert [d for d in range(1, 7) if f[d] == G] == [1]
                assert G == closed_G(i, theta, s, p)
                assert G == F(rows_by_id[vertex['id']]['G_by_prefix_load'][str(p)])
                for d in range(2, 7):
                    assert f[d] - G >= (d - 1) * F(16613, 30240)
                all_G[p] = G
                projections.append({'vertex_id': vertex['id'], 'p': p, 'G': str(G), 'minimizing_d': [1],
                                    'all_positive_d_gaps': [str(f[d] - G) for d in range(1, 7)]})
                for mask, menu in enumerate(menus):
                    d = sum(menu)
                    inner_means, six_minima = [], []
                    for k, t in enumerate(menu):
                        q = F(sum(menu[l] for l in range(6) if l != k), 5)
                        assert q == F(d - t, 5)
                        inner_means.append(str(q))
                        six_minima.append(minima[d, t])
                        outer_indices += 1
                    literal_average = sum(six_minima, F(0)) / 6
                    assert literal_average == f[d]
                    assert literal_average >= int(d > 0) * G
                    menu_records.append([vertex['id'], p, mask, d, inner_means, str(literal_average), str(literal_average - int(d > 0) * G)])
            rebuilt[vertex['id']] = row_at(i, theta, s, all_G)
        print(json.dumps({'source': i, 'vertices': len(source['vertices']), 'hidden_so_far': len(hidden)}), flush=True)
    assert len(hidden) == 66816 and len(conditional) == 3252
    assert len(outer) == 1897 and len(projections) == 271 and len(menu_records) == 17344
    assert outer_indices == 104064
    assert all(F(record[-1]) >= 0 for record in hidden)
    save('hidden_state_checks.json', {'status': 'PASS', 'columns': ['vertex_id', 'p', 'd', 't', 'tail', 'cost', 'minimum', 'residual'],
                                     'records': hidden})
    save('conditional_minimum_tables.json', {'status': 'PASS', 'records': conditional})
    save('outer_average_tables.json', {'status': 'PASS', 'records': outer})
    save('union_projection_tables.json', {'status': 'PASS', 'records': projections})
    save('all_64_menu_checks.json', {'status': 'PASS', 'columns': ['vertex_id', 'p', 'mask', 'd', 'six_true_inner_means', 'average', 'projection_slack'],
                                    'records': menu_records, 'same_index_excluded': True, 'label_aliases_allowed': True,
                                    'independence_or_partition_assumed': False, 'outer_indices_checked': outer_indices,
                                    'generic_five_query_share_checks': generic_index_checks})
    column_count = 0
    with (HERE / 'full_column_checks.tsv').open('w') as out:
        out.write('raw_index\tvertex_id\tcolumn\tstored\ttrue_wallet_expected\tresidual\n')
        for index, row in enumerate(rows):
            assert set(row['a']) == {str(j) for j in range(513)}
            assert row['rhs'] == '0' and row['numerical_divisor'] == '25'
            assert row['outer_average_divisor'] == '6' and row['inner_average_divisor'] == '5'
            assert row['inner_excludes_same_index'] is True and row['terminal_BR_average_weight'] == '1'
            vector = rebuilt[row['cell_vertex_id']]
            for column, expected in enumerate(vector):
                stored = F(row['a'][str(column)])
                assert stored == expected
                out.write(f'{index}\t{row["cell_vertex_id"]}\t{column}\t{stored}\t{expected}\t0\n')
                column_count += 1
    assert column_count == 92853
    old_rows = {row['parent_vertex_id']: row for row in load(SOURCE / 'exact_family.json')['rows']}
    old_routes = load(HERE / 'old67_row_route.json')['records']
    assert len(old_routes) == 67
    old_by_new = {}
    for route in old_routes:
        old, new = old_rows[route['old_vertex_id']], rows_by_id[route['new_vertex_id']]
        assert old['a'] == new['a'] and old['numerical_divisor'] == new['numerical_divisor'] == '25'
        old_by_new[route['new_vertex_id']] = route['old_vertex_id']

    affine_file = load(HERE / 'cell_affine_forms.json')
    affine_by_id = {cell['cell_id']: cell for cell in affine_file['cells']}
    affine_piece_count = incidence_count = centroid_columns = 0
    centroid_maps = []
    with (HERE / 'cell_incidence_column_checks.tsv').open('w') as out:
        out.write('cell_id\tvertex_id\tcolumn\tstored_row\tcell_affine_value\tresidual\n')
        for source in geometry['sources']:
            i = source['source']
            vertex_lookup = {v['id']: [F(x) for x in v['parameters']] for v in source['vertices']}
            for cell in source['cells']:
                affine = affine_by_id[cell['cell_id']]
                active = cell['active_term']
                assert affine['parameter_order'] == source['parameter_order']
                for column in range(513):
                    if column == 512:
                        intercept = F(7 - i, 2)
                        coefficients = [F(0)] * source['dimension']
                    else:
                        bits = [(column >> shift) & 1 for shift in range(8, -1, -1)]
                        p, o, u = sum(bits[:i - 1]), bits[7], share(bits[i - 1], sum(bits[:6]))
                        D = p + 7 - i
                        intercept = 25 * u - o * (F(7 - i, 2) + F(24, D) + F(1, p + 1)) / 6
                        if p == 0 and active:
                            intercept -= F(o, 3)
                        coefficients = []
                        for j in range(i + 1, 6):
                            ell_coefficient = (F(0) if not active or j < active else F(1) if j == active
                                               else F(1, 5 * (7 - j) * (8 - j)))
                            coefficient = u - F(o, 6 * (p + 7 - j))
                            if p == 0:
                                coefficient += F(5 * o, 6) * ell_coefficient
                            coefficients.append(coefficient)
                        coefficients.append(-u + F(o, 6 * min(D, 5)))
                    assert F(affine['intercept'][str(column)]) == intercept
                    for name, coefficient in zip(source['parameter_order'], coefficients):
                        assert F(affine['parameter_coefficients'][name][str(column)]) == coefficient
                    affine_piece_count += len(coefficients) + 1
                    for vertex_id in cell['vertex_ids']:
                        affine_value = intercept + dot(coefficients, vertex_lookup[vertex_id])
                        expected = rebuilt[vertex_id][column]
                        assert affine_value == expected
                        out.write(f'{cell["cell_id"]}\t{vertex_id}\t{column}\t{expected}\t{affine_value}\t0\n')
                        incidence_count += 1
                centroid = [sum((vertex_lookup[name][j] for name in cell['vertex_ids']), F(0)) /
                            len(cell['vertex_ids']) for j in range(source['dimension'])]
                interpolation = interpolate(i, [str(x) for x in centroid], cell['cell_id'], geometry)
                weights = {term['vertex_id']: F(term['weight']) for term in interpolation['weights']}
                theta = {j: centroid[k] for k, j in enumerate(range(i + 1, 6))}
                s = centroid[-1]
                expected_vector = row_at(i, theta, s, {p: closed_G(i, theta, s, p) for p in range(i)})
                for column, expected in enumerate(expected_vector):
                    assert sum((weight * rebuilt[name][column] for name, weight in weights.items()), F(0)) == expected
                    centroid_columns += 1
                interpolation['coefficient_residual_513'] = ['0'] * 513
                centroid_maps.append(interpolation)
    assert affine_piece_count == 34884 and incidence_count == 189297 and centroid_columns == 7182
    save('cell_centroid_interpolations.json', {'status': 'PASS', 'records': centroid_maps, 'full_column_checks': centroid_columns})
    old_interpolations = load(HERE / 'old_vertex_interpolations.json')['records']
    row_gap_records = []
    for record in old_interpolations:
        i, new_id = record['source'], record['cell_vertex_id']
        weights = {term['old_vertex_id']: F(term['weight']) for term in record['old_vertex_weights']}
        assert sum(weights.values(), F(0)) == 1 and all(x > 0 for x in weights.values())
        gap = F(record['Jensen_gap'])
        assert gap == 0 if record['is_original_vertex'] else gap > 0
        residuals = []
        for column in range(513):
            mean = sum((weight * F(old_rows[name]['a'][str(column)]) for name, weight in weights.items()), F(0))
            if column == 512:
                indicator = 0
            else:
                bits = [(column >> shift) & 1 for shift in range(8, -1, -1)]
                indicator = bits[7] if sum(bits[:i - 1]) == 0 else 0
            residual = mean - rebuilt[new_id][column] - F(5, 6) * gap * indicator
            assert residual == 0
            residuals.append(str(residual))
        row_gap_records.append({'vertex_id': new_id, 'Jensen_gap': str(gap), 'residual_513': residuals})
    assert len(row_gap_records) == 181
    save('old_vertex_row_interpolation_checks.json', {'status': 'PASS', 'columns_checked': 92853,
                                                     'identity': 'sum(mu*R_old)-R_new=(5/6)Jensen_gap*sum(o at p=0)',
                                                     'records': row_gap_records, 'cone_independence_claimed': False})
    scaling = load(HERE / 'numerical_scaling.json')
    assert scaling['raw_order'] == [row['name'] for row in rows]
    assert len(scaling['raw_scales']) == 181 and all(x == '25' for x in scaling['raw_scales'].values())
    catalog = load(HERE / 'row_catalog.json')
    assert catalog == [{**{k: v for k, v in row.items() if k != 'a'}, 'raw_index': index} for index, row in enumerate(rows)]
    for name, expected in pins.items():
        assert sha(REPO / name) == expected, name
    result = {
        'status': 'PASS_INDEPENDENT_TRUE_ORDERED_MENU_CELLS', 'family_sha256': sha(HERE / 'exact_family.json'),
        'checker_sha256': sha(HERE / 'check_family_literal.py'), 'own_interpolation_helper_sha256': sha(HERE / 'interpolate_cell.py'),
        'rows': 181, 'columns': 513, 'full_column_checks': 92853, 'old67_column_checks': 34371,
        'hidden_states': 66816, 'physical_conditionals': 3252, 'outer_f_values': 1897, 'G_contexts': 271,
        'all64_menu_patterns': 17344, 'true_outer_indices': 104064, 'literal_five_query_shares': 2304,
        'cell_affine_scalar_coefficients': 34884, 'cell_vertex_full_column_checks': 189297,
        'cell_centroid_full_column_checks': 7182, 'old_vertex_interpolation_full_column_checks': 92853,
        'strict_new_Jensen_gaps': 114, 'source_files_unchanged': len(pins),
        'same_menu_index_dependence_preserved': True, 'all_root119_rows_retained': True,
        'builder_or_source_program_imported_or_executed': False, 'own_exact_interpolation_helper_imported': True,
        'optimizer_calls': 0, 'new_LP_point_values_loaded_or_bound': False,
        'complete_generator_for_specified_continuous_family': True, 'minimal_generator_or_cone_independence_claimed': False,
        'Main_source_review_required_before_freeze': True, 'half_status': 'OPEN',
    }
    save('literal_check_result.json', result)
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    main()
