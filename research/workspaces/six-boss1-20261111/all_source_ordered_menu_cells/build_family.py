#!/usr/bin/env python3
"""Bind the final continuous source and instantiate every subdivision vertex."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = HERE.parents[3]
ORDERED = WS / 'all_source_ordered_joint_menu'
GENERAL = WS / 'all_source_joint_reweighted_safe'
REQUIRED = {
    'all_source_ordered_joint_menu/freeze_manifest.json': 'eb01d5539bc6b6182871df3e14fa800896e46ba63fa3f52176cb2aee562052fe',
    'all_source_ordered_joint_menu/proof.md': 'b9049f3c6b9faec5360d17acdcff6f2a16d8900674538b200fcd20ec713f3f08',
    'all_source_ordered_joint_menu/exact_family.json': 'd405ead895234dcaa9355cbd61056a7f81013f230d214b108578ead068784510',
    'all_source_ordered_joint_menu/continuous_G_contract.json': 'f9ea0d2788925965a999a204c3b9b4ad6eded30a529f962f1f0355eb5be15b85',
    'all_source_joint_reweighted_safe/freeze_manifest.json': '3f08170af4b678688317bdebfd8468a8c62e8a801923b3e86f7612a8873825eb',
    'all_source_joint_reweighted_safe/parameter_polytopes.json': '1bb37527940d7765fe4b88d26eacc71198e76d78b25d50454f6080892d7d7841',
    'all_source_joint_reweighted_safe/coordinate_contract.json': '95621205eab550affe69dc148e9cce49176b8d2c74b9207511583096d1b60b32',
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def write(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def actual_share(bits, i):
    return F(bits[i - 1], sum(bits[:6])) if bits[i - 1] else F(0)


def main():
    assert not (HERE / 'freeze_manifest.json').exists()
    assert not (HERE / 'exact_family.json').exists(), 'Refuse to replace an already prepared family.'
    for name, digest in REQUIRED.items():
        assert sha(WS / name) == digest, name
    source_manifest = read(ORDERED / 'freeze_manifest.json')
    assert source_manifest['status'] == 'FROZEN_ORDERED_OUTER6_INNER5_CONTINUOUS_FORMULA_AND_67_SAMPLES_NO_SOLVE'
    assert source_manifest['optimizer_calls'] == 0 and not source_manifest['outstanding_errors']
    contract = read(ORDERED / 'continuous_G_contract.json')
    assert contract['status'] == 'PROVED_ON_FULL_PARENT_CONTINUOUS_DOMAINS'
    assert contract['67_samples_complete_finite_generator'] is False
    geometry = read(HERE / 'parameter_cells.json')
    geometry_check = read(HERE / 'geometry_check_result.json')
    assert geometry_check['status'] == 'PASS_INDEPENDENT_CELL_GEOMETRY'
    assert geometry_check['parameter_cells_sha256'] == sha(HERE / 'parameter_cells.json')
    assert geometry_check['merged_vertices'] == 181
    pins = {}

    def pin(path, digest):
        name = str(path.resolve().relative_to(REPO))
        assert name not in pins or pins[name] == digest
        assert sha(path) == digest, name
        pins[name] = digest

    for name, digest in REQUIRED.items():
        pin(WS / name, digest)
    for package in (GENERAL, ORDERED):
        manifest = read(package / 'freeze_manifest.json')
        for section in ('source_sha256', 'prior_frozen_artifact_sha256'):
            for name, digest in manifest[section].items():
                pin(REPO / name, digest)
        for name, description in manifest['artifacts'].items():
            pin(REPO / name, description['sha256'])
        if (package / 'SHA256SUMS').exists():
            pin(package / 'SHA256SUMS', sha(package / 'SHA256SUMS'))
    write('source_pins.json', {
        'status': 'PREPARED_NO_OPTIMIZER', 'sources': dict(sorted(pins.items())),
        'direct_bindings': REQUIRED, 'final_ordered_source_bound': True,
        'Main_review_required_before_this_package_freeze': True,
        'new_1586_or_later_LP_point_values_loaded': False,
    })
    definitions = {source['i']: source for source in contract['sources']}
    original67 = read(ORDERED / 'exact_family.json')
    inclusion = read(HERE / 'original67_inclusion.json')['records']
    old_to_new = {record['old_vertex_id']: record['cell_vertex_id'] for record in inclusion}
    source_coordinates = read(GENERAL / 'coordinate_contract.json')
    coordinate = {key: source_coordinates[key] for key in
                  ('variables', 'K_column', 'bit_order', 'atom_columns', 'nonnegative_columns')}
    coordinate.update(schema='ordered_menu_cells_513_coordinates_v1', normalization_used=False,
                      C_size_equality_used=False, source_coordinate_sha256=REQUIRED['all_source_joint_reweighted_safe/coordinate_contract.json'])
    write('coordinate_contract.json', coordinate)
    with (HERE / 'column_routing.tsv').open('w') as out:
        out.write('column\tkind\ta1\ta2\ta3\ta4\ta5\ta6\tx\to\tc\n')
        for j in range(513):
            entries = ['K', '-', '-', '-', '-', '-', '-', '-', '-', '-'] if j == 512 else \
                      ['atom'] + [str((j >> shift) & 1) for shift in range(8, -1, -1)]
            out.write(str(j) + '\t' + '\t'.join(entries) + '\n')
    rows, affine_cells = [], []
    row_by_vertex = {}
    for source in geometry['sources']:
        i = source['source']
        definition = definitions[i]
        ci = F(definition['ci'])
        g_forms = {form['p']: form for form in definition['G_by_prefix']}
        losses = {form['index']: form for form in definition['loss_affines']}
        for vertex in source['vertices']:
            theta = {j: F(x) for j, x in vertex['theta_by_true_source'].items()}
            s, loss = F(vertex['s']), F(vertex['L'])
            a = F(25) + sum(theta.values(), F(0)) - s
            assert a == F(vertex['a']) and a > 0
            G = {}
            for p, form in g_forms.items():
                G[p] = (F(form['constant']) + F(form['s_coefficient']) * s + F(form['loss_coefficient']) * loss
                        + sum((F(form['theta_coefficients'][j]) * v for j, v in theta.items()), F(0)))
            coefficients = {}
            for column in range(512):
                bits = [(column >> shift) & 1 for shift in range(8, -1, -1)]
                prefix, o = sum(bits[:i - 1]), bits[7]
                coefficients[str(column)] = str(a * actual_share(bits, i) - o * G[prefix])
            coefficients['512'] = str(ci)
            row = {
                'name': 'ORDERED_MENU_CELL_' + vertex['id'],
                'family': 'ORDERED_OUTER6_INNER5_COMPLETE_CELL_VERTEX',
                'source': i, 'cell_vertex_id': vertex['id'], 'active_cells': vertex['active_cells'],
                'theta_by_source': {j: str(v) for j, v in theta.items()}, 's': str(s),
                'source_IC_weight': str(a), 'K_weight': str(ci), 'loss_L': str(loss),
                'G_by_prefix_load': {str(p): str(v) for p, v in G.items()},
                'outer_average_divisor': '6', 'inner_average_divisor': '5',
                'inner_excludes_same_index': True, 'terminal_BR_average_weight': '1',
                'a': coefficients, 'rhs': '0', 'numerical_divisor': '25',
            }
            row_by_vertex[vertex['id']] = row
            rows.append(row)
        for cell in source['cells']:
            active = cell['active_term']
            ell_constant = F(0) if active == 0 else F(losses[active]['constant'])
            ell_theta = {str(j): F(0) if active == 0 else F(losses[active]['theta_coefficients'][str(j)])
                         for j in range(i + 1, 6)}
            intercept = {}
            parameter_vectors = {name: {} for name in source['parameter_order']}
            for column in range(513):
                if column == 512:
                    intercept[str(column)] = str(ci)
                    for name in parameter_vectors:
                        parameter_vectors[name][str(column)] = '0'
                    continue
                bits = [(column >> shift) & 1 for shift in range(8, -1, -1)]
                prefix, o, u = sum(bits[:i - 1]), bits[7], actual_share(bits, i)
                form = g_forms[prefix]
                g_constant = F(form['constant']) + F(form['loss_coefficient']) * ell_constant
                intercept[str(column)] = str(25 * u - o * g_constant)
                for j in range(i + 1, 6):
                    g_parameter = F(form['theta_coefficients'][str(j)]) + F(form['loss_coefficient']) * ell_theta[str(j)]
                    parameter_vectors[f'theta{j}'][str(column)] = str(u - o * g_parameter)
                parameter_vectors['s'][str(column)] = str(-u - o * F(form['s_coefficient']))
            affine_cells.append({'cell_id': cell['cell_id'], 'source': i, 'active_term': active,
                                 'parameter_order': source['parameter_order'], 'intercept': intercept,
                                 'parameter_coefficients': parameter_vectors, 'rhs': '0',
                                 'vertex_ids': cell['vertex_ids']})
    assert len(rows) == 181 and len(affine_cells) == 14
    old_routes = []
    new_index = {row['cell_vertex_id']: j for j, row in enumerate(rows)}
    for old in original67['rows']:
        new_id = old_to_new[old['parent_vertex_id']]
        new = row_by_vertex[new_id]
        assert new['a'] == old['a'] and new['rhs'] == old['rhs']
        assert new['numerical_divisor'] == old['numerical_divisor'] == '25'
        old_routes.append({'old_vertex_id': old['parent_vertex_id'], 'old_row_name': old['name'],
                           'new_vertex_id': new_id, 'new_raw_index': new_index[new_id],
                           'new_row_name': new['name'], 'all513_coefficient_strings_equal': True})
    write('old67_row_route.json', {'status': 'PASS', 'records': old_routes, 'columns_checked': 34371})
    write('cell_affine_forms.json', {'schema': 'exact_cell_affine_row_forms_v1', 'cells': affine_cells,
                                     'variables': 513, 'optimizer_calls': 0})
    family = {
        'schema': 'all_source_ordered_menu_cells_181x513_v1', 'status': 'PREPARED_NO_OPTIMIZER',
        'raw_row_count': 181, 'variables': 513, 'K_column': 512, 'bit_order': coordinate['bit_order'],
        'inequality_convention': 'a dot z >=0', 'numerical_positive_divisor': '25',
        'scope': 'Complete finite generator for the specified full continuous ordered-menu family on all four parent domains.',
        'source_vertex_counts': {'1': 119, '2': 40, '3': 16, '4': 6}, 'cells': 14,
        'cell_vertex_incidences': 369, 'old_parameter_vertices': 67, 'new_subdivision_vertices': 114,
        'all_root_vertices_retained': True, 'row_pruning': False,
        'rows': rows, 'source_bindings': REQUIRED,
        'source_pins_sha256': sha(HERE / 'source_pins.json'),
        'parameter_cells_sha256': sha(HERE / 'parameter_cells.json'),
        'geometry_check_sha256': sha(HERE / 'geometry_check_result.json'),
        'proof_sha256': sha(HERE / 'proof.md'), 'cell_affine_forms_sha256': sha(HERE / 'cell_affine_forms.json'),
        'optimizer_calls': 0, 'point_values_loaded_or_bound': False,
        'all_possible_SPE_wallet_optimality_claimed': False, 'half_status': 'OPEN',
    }
    write('exact_family.json', family)
    catalog = []
    for index, row in enumerate(rows):
        record = {k: v for k, v in row.items() if k != 'a'}
        record['raw_index'] = index
        catalog.append(record)
    write('row_catalog.json', catalog)
    with (HERE / 'row_catalog.tsv').open('w') as out:
        out.write('raw_index\tname\tsource\tvertex_id\tactive_cells\ts\ta\tK\tL\tdivisor\n')
        for index, row in enumerate(rows):
            fields = [index, row['name'], row['source'], row['cell_vertex_id'], ';'.join(row['active_cells']),
                      row['s'], row['source_IC_weight'], row['K_weight'], row['loss_L'], '25']
            out.write('\t'.join(str(x) for x in fields) + '\n')
    write('numerical_scaling.json', {'raw_order': [row['name'] for row in rows],
                                    'raw_scales': {row['name']: '25' for row in rows},
                                    'raw_scale': 'inner terminal BR-average weight1; outer six-branch average',
                                    'optimizer_calls': 0})
    seen, duplicates = {}, []
    for index, row in enumerate(rows):
        key = tuple(F(row['a'][str(j)]) for j in range(513))
        if key in seen:
            duplicates.append({'raw_index': index, 'first_raw_index': seen[key]})
        else:
            seen[key] = index
    write('raw_duplicate_report.json', {'raw_rows': 181, 'distinct_vectors': len(seen),
                                        'duplicates': duplicates, 'all181_parameter_rows_retained': True})
    for name, digest in pins.items():
        assert sha(REPO / name) == digest, name
    result = {'status': 'PREPARED_NO_OPTIMIZER', 'family_sha256': sha(HERE / 'exact_family.json'),
              'rows': 181, 'columns': 513, 'source_pins_checked': len(pins),
              'ordered_source_finally_frozen': True, 'independent_literal_check_pending': True,
              'Main_source_review_required_before_freeze': True, 'optimizer_calls': 0,
              'point_values_loaded_or_bound': False}
    write('family_build_result.json', result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
