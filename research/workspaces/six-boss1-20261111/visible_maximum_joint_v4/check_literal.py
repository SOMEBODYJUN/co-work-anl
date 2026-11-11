#!/usr/bin/env python3
"""Independent Fraction replay from real shares. No builder/source imports or LP."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = HERE.parents[3]
BASE = WS / 'visible_maximum_joint_v3'
SOURCE = WS / 'all_source_joint_reweighted_safe'
REQUIRED = {
    'visible_maximum_joint_v3/exact_input.json': 'c5ddba49b71303083b07b96f90888d56f11b291d7c307f0c3e8280b7385d280e',
    'visible_maximum_joint_v3/freeze_manifest.json': 'f7cf345480b2d0c328a12a3485b0ad9d66c260f611b6c6e5253a16b361c857f9',
    'visible_maximum_joint_v3/numerical_scaling.json': 'bfc80e07700239cde34b2d0005e591e2abef7726dfd7e3c69db48df52375cbb9',
    'all_source_joint_reweighted_safe/exact_family.json': 'c8a40df9458e2add557ef14b8282880a1d14b05d55238ecf0715f63968907c18',
    'all_source_joint_reweighted_safe/freeze_manifest.json': '3f08170af4b678688317bdebfd8468a8c62e8a801923b3e86f7612a8873825eb',
    'all_source_joint_reweighted_safe/proof.md': '1a72e75cbcfa36d215c5030d1b86426746d068c1afc806894272b5c9aca60f70',
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text())


def save(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def share(bit, load):
    if load == 0:
        assert bit == 0
        return F(0)
    return F(bit, load)


def facets(i):
    middle = list(range(i + 1, 6))
    dimension = len(middle) + 1
    inequalities = []
    for position, j in enumerate(middle):
        lower = [F(0)] * dimension
        lower[position] = F(1)
        inequalities.append((F(0), lower))
        upper = [F(0)] * dimension
        upper[position] = F(-1)
        for later, ell in enumerate(middle):
            if ell > j:
                upper[later] = -F(1, 6 * (7 - ell) * (8 - ell))
        inequalities.append((F(5, 12), upper))
    lower_s = [F(0)] * dimension
    lower_s[-1] = F(1)
    inequalities.append((F(0), lower_s))
    if i == 1:
        for position in range(len(middle)):
            upper_s = [F(0)] * dimension
            upper_s[position], upper_s[-1] = F(5), F(-1)
            inequalities.append((F(15), upper_s))
    else:
        upper_s = [F(0)] * dimension
        upper_s[-1] = F(-1)
        inequalities.append((F(9), upper_s))
    return inequalities


def affine(inequality, point):
    constant, coefficients = inequality
    return constant + sum((a * b for a, b in zip(coefficients, point)), F(0))


def solve_square(equations):
    dimension = len(equations)
    matrix = [list(coefficients) + [-constant] for constant, coefficients in equations]
    for column in range(dimension):
        pivot = next((r for r in range(column, dimension) if matrix[r][column]), None)
        if pivot is None:
            return None
        matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
        divisor = matrix[column][column]
        matrix[column] = [x / divisor for x in matrix[column]]
        for row in range(dimension):
            if row != column and matrix[row][column]:
                factor = matrix[row][column]
                matrix[row] = [x - factor * y for x, y in zip(matrix[row], matrix[column])]
    return tuple(matrix[j][-1] for j in range(dimension))


def rank(rows, width):
    matrix = [list(row) for row in rows]
    lead = 0
    for column in range(width):
        pivot = next((r for r in range(lead, len(matrix)) if matrix[r][column]), None)
        if pivot is None:
            continue
        matrix[lead], matrix[pivot] = matrix[pivot], matrix[lead]
        divisor = matrix[lead][column]
        matrix[lead] = [x / divisor for x in matrix[lead]]
        for row in range(len(matrix)):
            if row != lead and matrix[row][column]:
                factor = matrix[row][column]
                matrix[row] = [x - factor * y for x, y in zip(matrix[row], matrix[lead])]
        lead += 1
        if lead == len(matrix):
            break
    return lead


def denominators(i, p, t, tail):
    last = p + t + sum(tail[:-1]) + 1
    internal = {j: p + t + sum(tail[:j - i - 1]) + 7 - j for j in range(i + 1, 6)}
    assert last > 0 and all(d > 0 for d in internal.values())
    return last, internal


def true_cost(i, theta, s, p, t, o, tail):
    # Construct each actual payoff and each size/query contribution separately.
    a = F(25) + sum(theta.values(), F(0)) - s
    total = p + t + sum(tail)
    source_payment = a * share(t, total)
    last_payment = share(tail[-1], total)
    internal_payments = sum((theta[j] * share(tail[j - i - 1], total) for j in theta), F(0))
    middle_sizes = F(sum(tail[:-1]), 2)
    last_size = F(tail[-1])
    last_den, internal_den = denominators(i, p, t, tail)
    last_query = F(o, 6 * last_den)
    internal_queries = sum((theta[j] * F(o, 6 * internal_den[j]) for j in theta), F(0))
    return source_payment - last_payment - internal_payments + middle_sizes + last_size + last_query + internal_queries


def asserted_minimum(i, theta, s, p, t, o):
    n = 6 - i
    D = p + n + 1
    return (F(n + 1, 2) * t + F(24 * t, D) - s * F(t, min(D, 5))
            + F(o, 6 * (p + 1 + n * t))
            + sum((theta[j] * F(o, 6 * (p + (j - i) * t + 7 - j)) for j in theta), F(0)))


def main():
    assert not (HERE / 'freeze_manifest.json').exists(), 'Do not overwrite frozen check outputs.'
    for path, expected in REQUIRED.items():
        assert digest(WS / path) == expected, path
    pins = load(HERE / 'source_pins.json')['sources']
    for path, expected in pins.items():
        assert digest(REPO / path) == expected, path
    inp = load(HERE / 'exact_input.json')
    baseline = load(BASE / 'exact_input.json')
    family = load(SOURCE / 'exact_family.json')
    domains = load(SOURCE / 'parameter_polytopes.json')['sources']
    rows = inp['raw_rows']
    assert len(rows) == inp['raw_inequality_count'] == 1586
    assert rows[:1050] == baseline['raw_rows']
    assert rows[1050:] == family['rows']
    assert inp['baseline_metadata'] == {k: v for k, v in baseline.items() if k != 'raw_rows'}
    assert inp['source_family_metadata'] == {k: v for k, v in family.items() if k != 'rows'}
    assert inp['source_bindings'] == REQUIRED
    assert inp['source_pins_sha256'] == digest(HERE / 'source_pins.json')
    assert inp['source_review_sha256'] == digest(HERE / 'source_review.md')
    assert inp['optimizer_calls'] == 0 and inp['preparation_only']['optimization_authorized'] is False
    assert inp['preparation_only']['C_equality_eliminated_in_new_rows'] is False
    coordinate_keys = ('variables', 'bit_order', 'atom_columns', 'K_column', 'nonnegative_columns',
                       'objective', 'equalities', 'equality_count', 'inequality_convention')
    for key in coordinate_keys:
        assert inp[key] == baseline[key], key
    assert inp['variables'] == 513 and inp['K_column'] == 512
    assert inp['nonnegative_columns'] == list(range(513))
    assert inp['bit_order'] == ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'x', 'o', 'c']
    assert inp['equality_count'] == len(inp['equalities']) == 2
    source_coordinates = load(SOURCE / 'coordinate_contract.json')
    for key in ('variables', 'bit_order', 'atom_columns', 'K_column', 'nonnegative_columns'):
        assert source_coordinates[key] == inp[key], key
    for filename in ('column_routing.json', 'column_routing.tsv'):
        assert (HERE / filename).read_bytes() == (BASE / filename).read_bytes()
    for index, atom in enumerate(inp['atom_columns']):
        bits = [(index >> shift) & 1 for shift in range(8, -1, -1)]
        assert atom == {'index': index, 'old_index': index // 2, 'a': bits[:6], 'x': bits[6], 'o': bits[7], 'c': bits[8]}

    old_scaling = load(BASE / 'numerical_scaling.json')
    scaling = load(HERE / 'numerical_scaling.json')
    assert scaling['raw_order'] == [row['name'] for row in rows]
    assert len(set(scaling['raw_order'])) == 1586
    assert scaling['raw_order'][:1050] == old_scaling['raw_order']
    assert scaling['baseline_scaling_metadata'] == {k: v for k, v in old_scaling.items() if k not in ('raw_order', 'raw_scales')}
    for row in rows[:1050]:
        assert scaling['raw_scales'][row['name']] == old_scaling['raw_scales'][row['name']]
    for row in rows[1050:]:
        assert scaling['raw_scales'][row['name']] == row['numerical_divisor'] == '25'
    assert all(F(x) > 0 for x in scaling['raw_scales'].values())
    catalog = load(HERE / 'row_catalog.json')
    assert catalog[:1050] == load(BASE / 'row_catalog.json')
    for j, row in enumerate(family['rows']):
        expected = {key: value for key, value in row.items() if key != 'a'}
        expected.update(raw_index=1050 + j, source_row_index=j,
                        source_package='all_source_joint_reweighted_safe', stored_coefficient_entries=513)
        assert catalog[1050 + j] == expected

    # Independently reconstruct the full bounded domains and enumerate all vertices.
    parameter_checks, vertices = [], []
    for domain in domains:
        i = domain['source']
        dimension = 6 - i
        inequalities = facets(i)
        saved_inequalities = [(F(face['constant']), [F(x) for x in face['coefficients']]) for face in domain['facets']]
        assert inequalities == saved_inequalities
        interior = [F(1, 10)] * (dimension - 1) + [F(1)]
        assert all(affine(face, interior) > 0 for face in inequalities)
        found = set()
        attempts = 0
        for active in combinations(inequalities, dimension):
            attempts += 1
            point = solve_square(active)
            if point is not None and all(affine(face, point) >= 0 for face in inequalities):
                found.add(point)
        given = {tuple(F(x) for x in v['theta']) + (F(v['s']),) for v in domain['vertices']}
        assert found == given
        assert len(found) == {1: 39, 2: 16, 3: 8, 4: 4}[i]
        face_ranks = []
        for face in inequalities:
            active_points = [v for v in found if affine(face, v) == 0]
            assert active_points
            differences = [[x - y for x, y in zip(v, active_points[0])] for v in active_points[1:]]
            face_rank = rank(differences, dimension)
            assert face_rank == dimension - 1
            face_ranks.append(face_rank)
        for vertex in domain['vertices']:
            theta = {j: F(x) for j, x in zip(range(i + 1, 6), vertex['theta'])}
            s = F(vertex['s'])
            a = F(25) + sum(theta.values(), F(0)) - s
            assert a == F(vertex['a']) and a > 0
            assert sum(theta.values(), F(0)) == F(vertex['Theta'])
            vertices.append((i, vertex['id'], theta, s, a))
        parameter_checks.append({'source': i, 'dimension': dimension, 'facet_count': len(inequalities),
                                 'all_facet_ranks': face_ranks, 'intersection_attempts': attempts,
                                 'vertex_count': len(found), 'all_vertices': [[str(x) for x in point] for point in sorted(found)]})
    assert len(vertices) == 67 and sum(x['facet_count'] for x in parameter_checks) == 31
    save('parameter_checks.json', {'status': 'PASS', 'optimizer_calls': 0, 'domains': parameter_checks})

    # Literal expansion of the SAME six legal query indices; no partition assumption.
    menu_counts = {}
    for i in range(1, 5):
        state_count = query_budget_count = 0
        for p in range(i):
            for t in (0, 1):
                for tail in product((0, 1), repeat=6 - i):
                    last_den, internal_den = denominators(i, p, t, tail)
                    query_denominators = [last_den] + list(internal_den.values())
                    for menu in product((0, 1), repeat=6):
                        d, o = sum(menu), int(any(menu))
                        for den in query_denominators:
                            literal = sum((F(member, den) for member in menu), F(0)) / 6
                            assert literal == F(d, 6 * den)
                            assert literal - F(o, 6 * den) == F(d - o, 6 * den) >= 0
                            query_budget_count += 1
                        state_count += 1
        menu_counts[str(i)] = {'membership_states': state_count, 'individual_query_budgets': query_budget_count}
    assert sum(x['membership_states'] for x in menu_counts.values()) == 13312
    assert sum(x['individual_query_budgets'] for x in menu_counts.values()) == 50176
    save('literal_six_query_checks.json', {'status': 'PASS', 'same_six_index_list': True,
          'independence_or_partition_assumed': False, 'by_source': menu_counts,
          'total_membership_states': 13312, 'total_individual_query_budgets': 50176})

    # True wallet costs first; the coefficient reconstruction below uses their minima.
    hidden_records, minimum_records, minima = [], [], {}
    for i, vertex_id, theta, s, a in vertices:
        for p in range(i):
            for t, o in product((0, 1), repeat=2):
                expected = asserted_minimum(i, theta, s, p, t, o)
                values = []
                for tail in product((0, 1), repeat=6 - i):
                    cost = true_cost(i, theta, s, p, t, o, tail)
                    assert cost >= expected, (vertex_id, p, t, o, tail)
                    hidden_records.append([vertex_id, i, p, t, o, list(tail), str(cost), str(expected), str(cost - expected)])
                    values.append((tail, cost))
                minimum = min(value for tail, value in values)
                assert minimum == expected
                attainers = [list(tail) for tail, value in values if value == minimum]
                common = ([0] * (6 - i) if t == 0 else
                          [1] * (6 - i) if p + 7 - i <= 5 else [1] * (5 - i) + [0])
                assert common in attainers
                minima[(vertex_id, p, t, o)] = minimum
                minimum_records.append({'source': i, 'vertex_id': vertex_id, 'p': p, 't': t, 'o': o,
                                        'minimum': str(minimum), 'common_attainer': common, 'all_attainers': attainers})
    assert len(hidden_records) == 8064 and len(minimum_records) == 444
    save('hidden_state_checks.json', {'status': 'PASS', 'columns': ['vertex_id', 'source', 'p', 't', 'o', 'tail', 'cost', 'minimum', 'residual'],
                                     'records': hidden_records, 'all_residuals_nonnegative': True})
    save('minimum_tables.json', {'status': 'PASS', 'all_minima_exact': True, 'records': minimum_records})

    roles = [f'A{i}' for i in range(1, 7)] + ['X', 'C']
    ordered_routes = [(i, vertex_id, role) for i, vertex_id, theta, s, a in vertices for role in roles]
    assert [(r['source'], r['vertex_id'], r['T']) for r in family['rows']] == ordered_routes
    parameter_lookup = {vertex_id: (i, theta, s, a) for i, vertex_id, theta, s, a in vertices}
    columns_checked = 0
    with (HERE / 'appended_column_checks.tsv').open('w') as out:
        out.write('raw_index\tsource_row_index\tvertex_id\tT\tcolumn\tstored\ttrue_wallet_expected\tresidual\n')
        for local_index, row in enumerate(family['rows']):
            i, theta, s, a = parameter_lookup[row['vertex_id']]
            assert row['source'] == i and row['uses_C_size_equality'] is False
            assert {int(j): F(v) for j, v in row['theta_by_true_source'].items()} == theta
            assert F(row['source_IC_weight']) == a and F(row['s']) == s
            assert row['middle_cap_weight'] == '1/2' and row['terminal_cap_weight'] == '1'
            assert row['terminal_BR_average_weight'] == '1' and row['query_menu'] == 'Omean_from_six_legal_labels'
            assert row['rhs'] == '0' and set(row['a']) == {str(j) for j in range(513)}
            role_index = int(row['T'][1:]) - 1 if row['T'].startswith('A') else 6 if row['T'] == 'X' else 8
            for column in range(513):
                if column == 512:
                    expected = F(7 - i, 2)
                else:
                    bits = [(column >> shift) & 1 for shift in range(8, -1, -1)]
                    p, t, o = sum(bits[:i - 1]), bits[role_index], bits[7]
                    actual_share = share(bits[i - 1], sum(bits[:6]))
                    expected = a * actual_share - minima[(row['vertex_id'], p, t, o)]
                stored = F(row['a'][str(column)])
                assert stored == expected, (row['name'], column, stored, expected)
                assert F(rows[1050 + local_index]['a'][str(column)]) == expected
                out.write(f'{1050 + local_index}\t{local_index}\t{row["vertex_id"]}\t{row["T"]}\t{column}\t{row["a"][str(column)]}\t{expected}\t{stored - expected}\n')
                columns_checked += 1
    assert columns_checked == 274968

    # Retain, and explicitly verify, all16 rows equivalent to old source2 C modulo E_C.
    old_endpoints = {}
    for row in baseline['raw_rows'][1003:1019]:
        key = (tuple(F(x) for x in row['theta3_theta4_theta5']), F(row['s']))
        old_endpoints[key] = row
    comparisons = []
    for local_index, row in enumerate(family['rows']):
        if row['source'] != 2 or row['T'] != 'C':
            continue
        key = (tuple(F(row['theta_by_true_source'][str(j)]) for j in (3, 4, 5)), F(row['s']))
        old = old_endpoints[key]
        multiplier = F(row['s']) / 5 - F(5, 2)
        residuals = []
        for column in range(513):
            ec = F(-1) if column == 512 else F(column & 1)
            residual = F(row['a'][str(column)]) - F(old['a'].get(str(column), '0')) - multiplier * ec
            assert residual == 0
            residuals.append(str(residual))
        comparisons.append({'raw_index': 1050 + local_index, 'new_name': row['name'], 'old_name': old['name'],
                            'E_C_multiplier': str(multiplier), 'residual_513': residuals})
    assert len(comparisons) == 16
    save('source2_C_equivalence_checks.json', {'status': 'PASS', 'identity': 'new=old+(s/5-5/2)(|C|-K)',
                                             'rows_retained': True, 'columns_checked': 8208, 'records': comparisons})

    seen, zero_rows, duplicates = {}, [], []
    for index, row in enumerate(rows):
        assert all(0 <= int(key) <= 512 for key in row['a'])
        vector = tuple(F(row['a'].get(str(column), '0')) for column in range(513))
        rhs = F(row['rhs'])
        key = (vector, rhs)
        if not any(vector) and rhs == 0:
            zero_rows.append({'raw_index': index, 'name': row['name']})
        if key in seen:
            first = seen[key]
            duplicates.append({'raw_index': index, 'name': row['name'], 'first_raw_index': first, 'first_name': rows[first]['name']})
        else:
            seen[key] = index
    diagnostic = load(HERE / 'raw_identity_diagnostics.json')
    assert diagnostic['zero_rows'] == zero_rows and diagnostic['duplicate_rows'] == duplicates
    distinct_nonzero = sum(bool(any(vector)) or rhs != 0 for vector, rhs in seen)
    assert diagnostic['distinct_nonzero_affine_rows'] == distinct_nonzero
    assert diagnostic['all_raw_rows_retained'] and not diagnostic['pruning_performed']
    assert Counter(row['source'] for row in family['rows']) == {1: 312, 2: 128, 3: 64, 4: 32}
    for path, expected in pins.items():
        assert digest(REPO / path) == expected, path
    result = {
        'status': 'PREPARED_NO_OPTIMIZER', 'result': 'PASS_INDEPENDENT_LITERAL_PREPARATION_CHECK',
        'input_sha256': digest(HERE / 'exact_input.json'), 'checker_sha256': digest(HERE / 'check_literal.py'),
        'optimizer_calls': 0, 'builder_or_source_code_imported': False, 'external_blind_review_claimed': False,
        'raw_rows': 1586, 'columns': 513, 'equalities': 2, 'baseline_raw_dictionaries_literal': 1050,
        'baseline_coefficient_entries_checked': 538650, 'source_raw_dictionaries_literal': 536,
        'appended_column_checks': 274968, 'parameter_vertices_independently_enumerated': 67, 'full_facets_checked': 31,
        'vertex_hidden_states': 8064, 'exact_minimum_types': 444, 'literal_six_query_membership_states': 13312,
        'literal_individual_query_budgets': 50176, 'source2_C_equivalence_rows': 16, 'source2_C_equivalence_columns': 8208,
        'old_positive_scale_strings_preserved': 1050, 'new_positive_scales_checked': 536,
        'K_column_kept_ci_in_all_new_rows': True, 'C_equality_eliminated_in_new_rows': False,
        'raw_zero_rows_retained': zero_rows, 'raw_duplicate_rows_retained': len(duplicates),
        'distinct_nonzero_affine_rows': distinct_nonzero, 'source_files_unchanged': len(pins),
        'point_values_loaded_or_bound': False, 'new_system_feasibility_or_optimality_claimed': False, 'half_status': 'OPEN'
    }
    save('literal_check_result.json', result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
