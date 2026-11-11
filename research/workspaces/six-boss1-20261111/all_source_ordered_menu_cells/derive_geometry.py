#!/usr/bin/env python3
"""Enumerate rational cells by boundary combinations. No ordered rows or LP."""
from fractions import Fraction as F
from itertools import combinations
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS = HERE.parent
DOMAIN = WS / 'all_source_joint_reweighted_safe/parameter_polytopes.json'
DOMAIN_SHA = '1bb37527940d7765fe4b88d26eacc71198e76d78b25d50454f6080892d7d7841'
GENERAL_MANIFEST = WS / 'all_source_joint_reweighted_safe/freeze_manifest.json'
GENERAL_MANIFEST_SHA = '3f08170af4b678688317bdebfd8468a8c62e8a801923b3e86f7612a8873825eb'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def evaluate(face, point):
    constant, vector = face
    return constant + sum((x * y for x, y in zip(vector, point)), F(0))


def intersection(faces):
    size = len(faces)
    matrix = [list(vector) + [-constant] for constant, vector in faces]
    for column in range(size):
        pivot = next((r for r in range(column, size) if matrix[r][column]), None)
        if pivot is None:
            return None
        matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
        divisor = matrix[column][column]
        matrix[column] = [v / divisor for v in matrix[column]]
        for row in range(size):
            if row != column and matrix[row][column]:
                factor = matrix[row][column]
                matrix[row] = [x - factor * y for x, y in zip(matrix[row], matrix[column])]
    return tuple(matrix[row][-1] for row in range(size))


def main():
    assert not (HERE / 'freeze_manifest.json').exists()
    assert sha(DOMAIN) == DOMAIN_SHA and sha(GENERAL_MANIFEST) == GENERAL_MANIFEST_SHA
    domains = json.loads(DOMAIN.read_text())['sources']
    source_results, counts, inclusion = [], [], []
    for domain in domains:
        i, dimension = domain['source'], domain['dimension']
        assert dimension == 6 - i
        js = list(range(i + 1, 6))
        base = [(F(row['constant']), tuple(F(x) for x in row['coefficients'])) for row in domain['facets']]
        base_names = [row['name'] for row in domain['facets']]
        linear = {}
        for position, j in enumerate(js):
            vector = [F(0)] * dimension
            vector[position] = F(1)
            for other_position, ell in enumerate(js):
                if ell > j:
                    vector[other_position] = F(1, 5 * (7 - ell) * (8 - ell))
            linear[j] = (F(-2, 5), tuple(vector))
        cells = []
        points_to_cells = {}
        total_attempts = 0
        for active in [0] + js:
            if active == 0:
                cuts = [(-constant, tuple(-x for x in vector)) for constant, vector in linear.values()]
                cut_names = [f'ell{j}_nonpositive' for j in js]
            else:
                constant, vector = linear[active]
                cuts = [(constant, vector)]
                cut_names = [f'ell{active}_nonnegative']
                for j in js:
                    if j != active:
                        other_constant, other_vector = linear[j]
                        cuts.append((constant - other_constant, tuple(x - y for x, y in zip(vector, other_vector))))
                        cut_names.append(f'ell{active}_ge_ell{j}')
            faces = base + cuts
            names = base_names + cut_names
            found = set()
            attempts = 0
            for chosen in combinations(faces, dimension):
                attempts += 1
                point = intersection(chosen)
                if point is not None and all(evaluate(face, point) >= 0 for face in faces):
                    found.add(point)
            assert found, (i, active)
            cell_id = f'I{i}_CELL{active}'
            for point in found:
                points_to_cells.setdefault(point, []).append(cell_id)
            cells.append({'cell_id': cell_id, 'active_term': active,
                          'boundary_intersection_attempts': attempts,
                          'inequalities': [{'name': name, 'constant': str(face[0]),
                                            'coefficients': [str(x) for x in face[1]]}
                                           for name, face in zip(names, faces)],
                          '_vertices': found})
            total_attempts += attempts
        sorted_points = sorted(points_to_cells)
        point_id = {point: f'I{i}_M{index:03}' for index, point in enumerate(sorted_points)}
        vertex_records = []
        for point in sorted_points:
            ell_values = {j: evaluate(face, point) for j, face in linear.items()}
            maximum = max([F(0)] + list(ell_values.values()))
            active_cells = ([f'I{i}_CELL0'] if maximum == 0 else []) + [f'I{i}_CELL{j}' for j in js if ell_values[j] == maximum]
            assert set(active_cells) == set(points_to_cells[point]), (i, point, active_cells, points_to_cells[point])
            vertex_records.append({'id': point_id[point], 'parameters': [str(x) for x in point],
                                   'theta_by_true_source': {str(j): str(point[k]) for k, j in enumerate(js)},
                                   's': str(point[-1]), 'a': str(F(25) + sum(point[:-1], F(0)) - point[-1]),
                                   'ell_values': {str(j): str(v) for j, v in ell_values.items()},
                                   'L': str(maximum), 'active_cells': active_cells,
                                   'enumerated_vertex_cells': points_to_cells[point]})
        for cell in cells:
            found = cell.pop('_vertices')
            cell['vertex_ids'] = [point_id[point] for point in sorted(found)]
            cell['vertex_count'] = len(found)
        original = []
        for old in domain['vertices']:
            point = tuple(F(x) for x in old['theta']) + (F(old['s']),)
            assert point in point_id, old['id']
            record = {'source': i, 'old_vertex_id': old['id'], 'cell_vertex_id': point_id[point],
                      'parameters': [str(x) for x in point], 'active_cells': points_to_cells[point],
                      'exact_interpolation': [{'vertex_id': point_id[point], 'weight': '1'}]}
            original.append(record)
            inclusion.append(record)
        summary = {'source': i, 'dimension': dimension, 'cell_count': len(cells),
                   'cell_vertex_counts': {cell['cell_id']: cell['vertex_count'] for cell in cells},
                   'merged_vertices': len(sorted_points), 'original_vertices': len(original),
                   'new_subdivision_vertices': len(sorted_points) - len(original),
                   'boundary_intersection_attempts': total_attempts}
        counts.append(summary)
        source_results.append({'source': i, 'parameter_order': domain['parameter_order'],
                               'dimension': dimension,
                               'ell_forms': {str(j): {'constant': str(c), 'coefficients': [str(x) for x in v]} for j, (c, v) in linear.items()},
                               'cells': cells, 'vertices': vertex_records,
                               'original_vertex_inclusion': original})
        print(json.dumps(summary, ensure_ascii=False), flush=True)
    result = {'status': 'PREPARED_GEOMETRY_ONLY_NO_ORDERED_SOURCE_BOUND',
              'general_parameter_domain_sha256': DOMAIN_SHA, 'general_manifest_sha256': GENERAL_MANIFEST_SHA,
              'inequality_convention': 'constant+coefficients dot parameters >=0',
              'cell_definition': 'L=max(0,ell_j); cell0:all ell<=0; cellj:ell_j>=0 and ell_j>=ell_k.',
              'sources': source_results, 'optimizer_calls': 0, 'ordered_source_bound': False}
    write('parameter_cells.json', result)
    write('original67_inclusion.json', {'status': 'PASS', 'count': len(inclusion), 'records': inclusion})
    total = {'status': 'PREPARED_GEOMETRY_ONLY_NO_ORDERED_SOURCE_BOUND', 'by_source': counts,
             'total_cells': sum(x['cell_count'] for x in counts),
             'merged_vertices': sum(x['merged_vertices'] for x in counts),
             'original_vertices': sum(x['original_vertices'] for x in counts),
             'new_subdivision_vertices': sum(x['new_subdivision_vertices'] for x in counts),
             'boundary_intersection_attempts': sum(x['boundary_intersection_attempts'] for x in counts),
             'parameter_cells_sha256': sha(HERE / 'parameter_cells.json'),
             'optimizer_calls': 0, 'ordered_rows_generated': 0}
    assert total['original_vertices'] == 67
    write('geometry_counts.json', total)
    assert sha(DOMAIN) == DOMAIN_SHA and sha(GENERAL_MANIFEST) == GENERAL_MANIFEST_SHA
    print(json.dumps(total, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    main()
