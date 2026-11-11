#!/usr/bin/env python3
"""Read-only exact certificate/face replay, all181 diagnostics and119 root payments."""
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = HERE.parents[3]
CELLS = WS / 'all_source_ordered_menu_cells'
REQUIRED = {
    'visible_maximum_joint_v4/exact_input.json': 'fbd3b0cb65736b5c41b64dd630b442e9647b701e446c36819e3f726c620ac839',
    'visible_maximum_joint_v4_solve/exact_certificate.json': '6049aba7ddb134159f95adea1f3bc6470bdfcb902a111e702e52b9b6f3cec34b',
    'visible_maximum_joint_v4_solve/optimal_face.json': 'b3cb7c3c611267204e04bcc5e7e15a721af7b366013a4fabde3b368d226396ac',
    'visible_maximum_joint_v4_solve/proof.md': '74c44f77ac0f6986c1cae020f5b60432968867bf2343233197612a67f3bef0f7',
    'main_visible_c_v4_certificate_check.json': '626f48dcb0ff1cafbffe0dad362af66f6d3a00ee5b65f581871dadb01c7187e4',
    'all_source_ordered_menu_cells/exact_family.json': 'f1bca409d9927f9721764a327f1fcd52a18c38f0968d9c240fa20288aa95eac3',
    'all_source_ordered_menu_cells/freeze_manifest.json': '313e3fe07138c1ecf0b42bd8fbafa4e4f334f583141f0a950eeb71bb09ad6430',
    'all_source_ordered_menu_cells/proof.md': 'd5be7d17de3b3dd16ffd68b61a812127c94dd74e6e36ea9c9d8f80a639ca36d4',
    'main_root270_global_bridge/ROOT270_TRUE_BRANCH_P25.json': 'd4ee988b28e897bcb836811c45e1c27a9728c64e352d2e30c79c93fded71a834',
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def save(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def vector(row):
    return [F(row['a'].get(str(j), '0')) for j in range(513)]


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def solve_many(matrix, rhs):
    n = len(matrix)
    width = len(rhs[0])
    work = [list(a) + list(b) for a, b in zip(matrix, rhs)]
    for column in range(n):
        pivot = next((r for r in range(column, n) if work[r][column]), None)
        assert pivot is not None
        work[column], work[pivot] = work[pivot], work[column]
        divisor = work[column][column]
        work[column] = [x / divisor for x in work[column]]
        for row in range(n):
            if row != column and work[row][column]:
                factor = work[row][column]
                work[row] = [x - factor * y for x, y in zip(work[row], work[column])]
    assert all(work[r][c] == int(r == c) for r in range(n) for c in range(n))
    return [row[n:n + width] for row in work]


def pullback(coefficients, rhs, coordinates):
    result = [-rhs] + [F(0)] * 7
    for column, affine in coordinates.items():
        result = [a + coefficients[column] * b for a, b in zip(result, affine)]
    return result


def main():
    assert not (HERE / 'freeze_manifest.json').exists()
    pins = {}

    def pin(path, expected):
        name = str(path.resolve().relative_to(REPO))
        assert name not in pins or pins[name] == expected
        assert sha(path) == expected, name
        pins[name] = expected

    for name, expected in REQUIRED.items():
        pin(WS / name, expected)
    cells_manifest = read(CELLS / 'freeze_manifest.json')
    for name, expected in read(CELLS / 'source_pins.json')['sources'].items():
        pin(REPO / name, expected)
    for name, expected in cells_manifest['artifacts'].items():
        pin(CELLS / name, expected)
    pin(CELLS / 'SHA256SUMS', '6f65f6d115a177f225cb320e928a728d7f473c532ef57264c17ad2141c80df84')
    pin(REPO / cells_manifest['Main_review_evidence_path'], cells_manifest['Main_review_evidence_sha256'])
    save('source_pins.json', {'status': 'EXACT_DIAGNOSTIC_NO_OPTIMIZER', 'direct_bindings': REQUIRED,
                             'sources': dict(sorted(pins.items())),
                             'new_read_authorization': 'Main explicitly released the frozen1586 certificate and complete optimal face for this diagnostic only.'})
    inp = read(WS / 'visible_maximum_joint_v4/exact_input.json')
    cert = read(WS / 'visible_maximum_joint_v4_solve/exact_certificate.json')
    face = read(WS / 'visible_maximum_joint_v4_solve/optimal_face.json')
    family = read(CELLS / 'exact_family.json')
    A = [vector(row) for row in inp['raw_rows']]
    rhs = [F(row['rhs']) for row in inp['raw_rows']]
    E = [vector(row) for row in inp['equalities']]
    h = [F(row['rhs']) for row in inp['equalities']]
    objective = [F(inp['objective'].get(str(j), '0')) for j in range(513)]
    point = list(map(F, cert['primal']))
    y = list(map(F, cert['dual']['raw_row_weights']))
    eta = list(map(F, cert['dual']['equality_multipliers']))
    assert len(A) == len(y) == 1586 and len(point) == 513 and len(E) == len(eta) == 2
    assert cert['input_sha256'] == face['input_sha256'] == REQUIRED['visible_maximum_joint_v4/exact_input.json']
    assert face['certificate_sha256'] == REQUIRED['visible_maximum_joint_v4_solve/exact_certificate.json']
    assert all(x >= 0 for x in point + y)
    slacks = [dot(row, point) - b for row, b in zip(A, rhs)]
    assert all(x >= 0 for x in slacks)
    assert slacks == list(map(F, cert['raw_row_slacks']))
    assert all(dot(row, point) == b for row, b in zip(E, h))
    positive = [j for j, weight in enumerate(y) if weight > 0]
    residual = [objective[c] - sum((y[j] * A[j][c] for j in positive), F(0))
                - sum((eta[k] * E[k][c] for k in range(2)), F(0)) for c in range(513)]
    assert residual == list(map(F, cert['dual']['nonnegative_column_residual']))
    assert all(x >= 0 for x in residual)
    assert all(a * b == 0 for a, b in zip(y, slacks))
    assert all(a * b == 0 for a, b in zip(residual, point))
    optimum = dot(objective, point)
    assert optimum == dot(y, rhs) + dot(eta, h) == F(cert['objective']) == F(face['objective'])
    zero = [j for j, r in enumerate(residual) if r == 0]
    forced = [j for j, r in enumerate(residual) if r > 0]
    assert zero == face['zero_residual_columns'] and forced == face['forced_zero_columns']
    assert len(zero) == 20 and positive == face['positive_dual_raw_indices'] and len(positive) == 11
    save('certificate_replay.json', {'status': 'PASS_FULL1586_513_2_EXACT', 'objective': str(optimum),
                                    'raw_slacks': list(map(str, slacks)), 'equality_residuals': ['0', '0'],
                                    'dual_column_residuals': list(map(str, residual)),
                                    'all_complementarity_products_zero': True, 'zero_residual_columns': zero,
                                    'positive_dual_raw_indices': positive, 'optimizer_calls': 0})
    # Solve anew on all20 zero residual columns, including returned-point zero columns.
    free = [p['column'] for p in face['parameters']]
    assert free == [0, 11, 15, 19, 23, 51, 75]
    pivots = [j for j in zero if j not in free]
    equations = E + [A[j] for j in positive]
    equation_rhs = h + [rhs[j] for j in positive]
    equation_names = [r['name'] for r in inp['equalities']] + [inp['raw_rows'][j]['name'] for j in positive]
    assert equation_names == face['equation_names'] and list(map(str, equation_rhs)) == face['equation_rhs']
    assert len(pivots) == len(equations) == 13
    solved = solve_many([[row[c] for c in pivots] for row in equations],
                        [[b] + [-row[c] for c in free] for row, b in zip(equations, equation_rhs)])
    coordinates = {}
    for position, column in enumerate(free):
        coordinates[column] = [F(0)] + [F(int(j == position)) for j in range(7)]
    coordinates.update({column: values for column, values in zip(pivots, solved)})
    stored_coordinates = {row['column']: [F(row['constant'])] + list(map(F, row['parameter_coefficients']))
                          for row in face['coordinates']}
    assert coordinates == stored_coordinates
    parameters = [point[c] for c in free]
    assert parameters == list(map(F, face['point_parameters']))
    assert all(dot([F(1)] + parameters, coordinates.get(c, [F(0)] * 8)) == point[c] for c in range(513))
    assert all(pullback(row, b, coordinates) == [F(0)] * 8 for row, b in zip(equations, equation_rhs))
    assert pullback(objective, optimum, coordinates) == [F(0)] * 8
    old_restrictions = []
    for index, (row, b) in enumerate(zip(A, rhs)):
        expression = pullback(row, b, coordinates)
        stored = face['all1586_raw_inequality_restrictions'][index]
        assert expression == [F(stored['constant'])] + list(map(F, stored['parameter_coefficients']))
        assert dot([F(1)] + parameters, expression) == slacks[index]
        old_restrictions.append({'raw_index': index, 'name': inp['raw_rows'][index]['name'],
                                 'constant': str(expression[0]), 'parameter_coefficients': list(map(str, expression[1:])),
                                 'required_nonnegative': True})
    face_replay = {'status': 'PASS_FULL_FACE_RECONSTRUCTION', 'rank': 13, 'zero_residual_column_count': 20,
                   'free_parameter_count': 7, 'parameters': face['parameters'], 'point_parameters': list(map(str, parameters)),
                   'coordinates': [{'column': c, 'constant': str(coordinates[c][0]),
                                    'parameter_coefficients': list(map(str, coordinates[c][1:])),
                                    'required_nonnegative': True} for c in zero],
                   'forced_zero_columns': forced, 'all1586_inequality_restrictions': old_restrictions,
                   'nonconstant_original_inequalities': sum(any(F(v) for v in r['parameter_coefficients']) for r in old_restrictions),
                   'affine_space_alone_not_claimed_feasible': True, 'optimizer_calls': 0}
    save('reconstructed_face.json', face_replay)
    ordered_records = []
    for index, row in enumerate(family['rows']):
        a = vector(row)
        value = dot(a, point) - F(row['rhs'])
        expression = pullback(a, F(row['rhs']), coordinates)
        assert dot([F(1)] + parameters, expression) == value
        nonconstant = any(expression[1:])
        ordered_records.append({
            'raw_index_in_181': index, 'name': row['name'], 'source': row['source'],
            'cell_vertex_id': row['cell_vertex_id'], 'active_cells': row['active_cells'],
            'theta_by_source': row['theta_by_source'], 's': row['s'], 'numerical_divisor': row['numerical_divisor'],
            'point_slack': str(value), 'point_sign': 'negative' if value < 0 else 'positive' if value > 0 else 'zero',
            'face_constant': str(expression[0]), 'face_parameter_coefficients': list(map(str, expression[1:])),
            'nonconstant_on_affine_hull': nonconstant, 'strict_fixed_negative': not nonconstant and expression[0] < 0,
            'retained': True,
        })
    assert len(ordered_records) == 181
    fixed_negative = [r for r in ordered_records if r['strict_fixed_negative']]
    nonconstant = [r for r in ordered_records if r['nonconstant_on_affine_hull']]
    save('all181_point_and_face_rows.json', {'status': 'PASS_EXACT_POINT_AND_COMPLETE_FACE', 'parameters': face['parameters'],
                                           'rows': ordered_records, 'all181_retained': True})
    save('strict_fixed_negative_rows.json', {'count': len(fixed_negative), 'rows': fixed_negative,
                                            'consequence': 'Each listed valid row strictly separates the entire frozen1586 optimal face.'})
    save('nonconstant_rows.json', {'count': len(nonconstant), 'rows': nonconstant, 'none_discarded': True})
    with (HERE / 'all181_point_and_face_rows.tsv').open('w') as out:
        out.write('index\tname\tsource\tpoint_slack\tface_constant\tz0\tz11\tz15\tz19\tz23\tz51\tz75\tclassification\n')
        for r in ordered_records:
            fields = [r['raw_index_in_181'], r['name'], r['source'], r['point_slack'], r['face_constant'],
                      *r['face_parameter_coefficients'],
                      'strict_fixed_negative' if r['strict_fixed_negative'] else 'nonconstant' if r['nonconstant_on_affine_hull'] else 'constant_' + r['point_sign']]
            out.write('\t'.join(map(str, fields)) + '\n')
    # True homogeneous root payments, independent of the diagnostic point/normalization.
    b = F(1767904008200582, 16877573861922720)
    c = F(337340181272013, 16877573861922720)
    O, U1 = [], []
    for column in range(512):
        bits = [(column >> shift) & 1 for shift in range(8, -1, -1)]
        O.append(F(bits[7]))
        U1.append(F(bits[0], sum(bits[:6])) if bits[0] else F(0))
    O.append(F(0)); U1.append(F(0))
    K = [F(0)] * 512 + [F(1)]
    root = [u - b * k - c * o for u, k, o in zip(U1, K, O)]
    menu = [k - o / 6 for k, o in zip(K, O)]
    assert root == A[868] and inp['raw_rows'][868]['name'] == 'ROOT270_TRUE_BRANCH_P25'
    assert menu == A[1001] and inp['raw_rows'][1001]['name'] == 'MENU_MAX_SIZE_LOWER_BOUND'
    assert rhs[868] == rhs[1001] == 0
    bridge = read(WS / 'main_root270_global_bridge/ROOT270_TRUE_BRANCH_P25.json')
    assert root[:512] == [F(bridge['a'].get(str(column // 2), '0')) for column in range(512)]
    assert root[512] == F(bridge['a']['256'])
    root_records = []
    for index, row in enumerate(family['rows']):
        if row['source'] != 1:
            continue
        a, G = F(row['source_IC_weight']), F(row['G_by_prefix_load']['0'])
        beta = 3 + a * b
        gamma = a * c + beta / 6 - G
        residuals = [value - a * rr - beta * mm - gamma * oo for value, rr, mm, oo in zip(vector(row), root, menu, O)]
        assert all(r == 0 for r in residuals)
        root_records.append({'raw_index_in_181': index, 'name': row['name'], 'cell_vertex_id': row['cell_vertex_id'],
                             'active_cells': row['active_cells'], 'theta_by_source': row['theta_by_source'], 's': row['s'],
                             'ROOT270_weight': str(a), 'menu_K_lower_bound_weight': str(beta), 'O_weight': str(gamma),
                             'all_three_weights_strictly_positive': a > 0 and beta > 0 and gamma > 0,
                             'residual_513': list(map(str, residuals))})
    assert len(root_records) == 119
    all_paid = all(r['all_three_weights_strictly_positive'] for r in root_records)
    min_gamma = min(F(r['O_weight']) for r in root_records)
    min_rows = [r['name'] for r in root_records if F(r['O_weight']) == min_gamma]
    root_result = {'status': 'PASS_ALL119_ROOT_POSITIVE_PAYMENTS' if all_paid else 'SOME_PAYMENT_WEIGHTS_NONPOSITIVE',
                   'ROOT270_b': str(b), 'ROOT270_c': str(c),
                   'identity': 'R=a ROOT270+(3+a*b)(K-O/6)+(a*c+(3+a*b)/6-G)O',
                   'rows': root_records, 'full_column_checks': 61047,
                   'minimum_O_weight': str(min_gamma), 'minimum_O_weight_attainers': min_rows,
                   'all119_checked_not_old39_extrapolation': True,
                   'entire_root_continuous_family_implied_using_complete_frozen_cell_affinity': all_paid,
                   'no_point_values_or_O_normalization_used_in_payment': True}
    save('root119_positive_payments.json', root_result)
    negative_counts = Counter(r['source'] for r in fixed_negative)
    signs = Counter(r['point_sign'] for r in ordered_records)
    minimum = min(ordered_records, key=lambda r: F(r['point_slack']))
    for name, expected in pins.items():
        assert sha(REPO / name) == expected, name
    result = {'status': 'PASS_EXACT_181_ON_1586_DIAGNOSTIC_NO_OPTIMIZER',
              'input_sha256': REQUIRED['visible_maximum_joint_v4/exact_input.json'],
              'certificate_sha256': REQUIRED['visible_maximum_joint_v4_solve/exact_certificate.json'],
              'optimal_face_sha256': REQUIRED['visible_maximum_joint_v4_solve/optimal_face.json'],
              'ordered_family_sha256': REQUIRED['all_source_ordered_menu_cells/exact_family.json'],
              'checker_sha256': sha(HERE / 'check_exact.py'), 'certificate_raw_rows_checked': 1586,
              'certificate_columns_checked': 513, 'certificate_equalities_checked': 2,
              'face_equation_rank': 13, 'face_zero_residual_columns': 20, 'face_parameters': 7,
              'face_original_inequalities_checked': 1586, 'original_nonconstant_face_restrictions': face_replay['nonconstant_original_inequalities'],
              'ordered_rows_checked': 181, 'constant_ordered_rows': 181 - len(nonconstant),
              'nonconstant_ordered_rows': len(nonconstant), 'strict_fixed_negative_rows': len(fixed_negative),
              'strict_fixed_negative_by_source': dict(negative_counts), 'point_sign_counts': dict(signs),
              'most_negative_row': minimum, 'root_rows_checked': 119, 'root_full_column_checks': 61047,
              'all119_root_payments_strictly_positive': all_paid, 'minimum_root_O_payment': str(min_gamma),
              'minimum_root_O_payment_rows': min_rows, 'entire_root_continuous_family_redundant': all_paid,
              'source_files_unchanged': len(pins), 'optimizer_calls': 0,
              'source_programs_imported_or_executed': False, 'new_input_prepared': False,
              'existing1586_or181_modified': False, '734_touched': False, 'new_optimum_claimed': False, 'half_status': 'OPEN'}
    save('check_result.json', result)
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    main()
