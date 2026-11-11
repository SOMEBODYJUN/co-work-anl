#!/usr/bin/env python3
"""Independent edge-clipping check with exact old-vertex interpolations; no LP."""
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS = HERE.parent
SOURCE = WS / 'all_source_joint_reweighted_safe'


def read(path):
    return json.loads(path.read_text())


def save(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dot(vector, point):
    return sum((a * b for a, b in zip(vector, point)), Q(0))


def value(halfspace, point):
    c, normal = halfspace
    return c + dot(normal, point)


def matrix_rank(rows, width):
    work = [list(row) for row in rows]
    pivot_row = 0
    for column in range(width):
        selected = next((j for j in range(pivot_row, len(work)) if work[j][column] != 0), None)
        if selected is None:
            continue
        work[pivot_row], work[selected] = work[selected], work[pivot_row]
        divisor = work[pivot_row][column]
        work[pivot_row] = [x / divisor for x in work[pivot_row]]
        for j in range(pivot_row + 1, len(work)):
            factor = work[j][column]
            if factor:
                work[j] = [x - factor * y for x, y in zip(work[j], work[pivot_row])]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def independently_defined_domain(i):
    middle = list(range(i + 1, 6))
    dimension = len(middle) + 1
    result = []
    for position, j in enumerate(middle):
        lower = [Q(0)] * dimension
        lower[position] = Q(1)
        result.append((Q(0), tuple(lower)))
        upper = [Q(0)] * dimension
        upper[position] = Q(-1)
        for later_position, ell in enumerate(middle):
            if ell > j:
                upper[later_position] = -Q(1, 6 * (7 - ell) * (8 - ell))
        result.append((Q(5, 12), tuple(upper)))
    lower = [Q(0)] * dimension
    lower[-1] = Q(1)
    result.append((Q(0), tuple(lower)))
    if i > 1:
        upper = [Q(0)] * dimension
        upper[-1] = Q(-1)
        result.append((Q(9), tuple(upper)))
    else:
        for position in range(len(middle)):
            upper = [Q(0)] * dimension
            upper[position], upper[-1] = Q(5), Q(-1)
            result.append((Q(15), tuple(upper)))
    return result


def ell_form(i, j):
    vector = []
    for ell in range(i + 1, 6):
        vector.append(Q(0) if ell < j else Q(1) if ell == j else Q(1, 5 * (7 - ell) * (8 - ell)))
    return Q(-2, 5), tuple(vector + [Q(0)])


def L(i, point):
    return max([Q(0)] + [value(ell_form(i, j), point) for j in range(i + 1, 6)])


def expected_cuts(i, active):
    forms = {j: ell_form(i, j) for j in range(i + 1, 6)}
    if active == 0:
        return [(-c, tuple(-x for x in a)) for c, a in forms.values()]
    ca, aa = forms[active]
    result = [(ca, aa)]
    for j, (cj, aj) in forms.items():
        if j != active:
            result.append((ca - cj, tuple(x - y for x, y in zip(aa, aj))))
    return result


def combine_weights(left, right, left_weight, right_weight):
    result = {}
    for name, weight in left.items():
        result[name] = result.get(name, Q(0)) + left_weight * weight
    for name, weight in right.items():
        result[name] = result.get(name, Q(0)) + right_weight * weight
    return {name: weight for name, weight in sorted(result.items()) if weight}


def clip(initial_vertices, original_faces, cuts, dimension):
    vertices = {p: dict(w) for p, w in initial_vertices.items()}
    faces = list(original_faces)
    rank_cache = {}
    stages = []
    for cut_index, cut in enumerate(cuts):
        points = sorted(vertices)
        evaluations = {p: value(cut, p) for p in points}
        positive = [p for p in points if evaluations[p] > 0]
        negative = [p for p in points if evaluations[p] < 0]
        boundary = [p for p in points if evaluations[p] == 0]
        next_vertices = {p: vertices[p] for p in points if evaluations[p] >= 0}
        active_sets = {p: {j for j, face in enumerate(faces) if value(face, p) == 0} for p in points}
        crossing_edges = 0
        for left in positive:
            for right in negative:
                common = tuple(sorted(active_sets[left] & active_sets[right]))
                if len(common) < dimension - 1:
                    continue
                if common not in rank_cache:
                    rank_cache[common] = matrix_rank([faces[j][1] for j in common], dimension)
                if rank_cache[common] != dimension - 1:
                    continue
                crossing_edges += 1
                gl, gr = evaluations[left], evaluations[right]
                wl, wr = -gr / (gl - gr), gl / (gl - gr)
                assert wl > 0 and wr > 0 and wl + wr == 1
                point = tuple(wl * x + wr * y for x, y in zip(left, right))
                assert value(cut, point) == 0
                assert all(value(face, point) >= 0 for face in faces)
                if point not in next_vertices:
                    next_vertices[point] = combine_weights(vertices[left], vertices[right], wl, wr)
        assert next_vertices
        faces.append(cut)
        vertices = next_vertices
        ordered = sorted(vertices)
        affine_rank = matrix_rank([[x - y for x, y in zip(p, ordered[0])] for p in ordered[1:]], dimension)
        assert affine_rank == dimension, 'Every present cell and its preceding cuts have full dimension.'
        stages.append({'cut_index': cut_index, 'old_vertices': len(points), 'positive': len(positive),
                       'negative': len(negative), 'on_cut': len(boundary), 'crossing_edges': crossing_edges,
                       'new_vertices': len(vertices), 'affine_dimension': affine_rank})
    return vertices, stages


def main():
    assert not (HERE / 'freeze_manifest.json').exists()
    expected_domain = '1bb37527940d7765fe4b88d26eacc71198e76d78b25d50454f6080892d7d7841'
    assert sha(SOURCE / 'parameter_polytopes.json') == expected_domain
    domain_list = read(SOURCE / 'parameter_polytopes.json')['sources']
    geometry = read(HERE / 'parameter_cells.json')
    assert geometry['general_parameter_domain_sha256'] == expected_domain
    all_interpolations, cell_checks, totals = [], [], []
    all_old_ids = set()
    for domain, source in zip(domain_list, geometry['sources']):
        i = domain['source']
        assert source['source'] == i
        dimension = 6 - i
        old_points = {v['id']: tuple(Q(x) for x in v['theta']) + (Q(v['s']),) for v in domain['vertices']}
        all_old_ids.update(old_points)
        initial = {point: {old_id: Q(1)} for old_id, point in old_points.items()}
        assert len(initial) == len(old_points)
        base = independently_defined_domain(i)
        assert base == [(Q(f['constant']), tuple(Q(x) for x in f['coefficients'])) for f in domain['facets']]
        saved = {tuple(Q(x) for x in v['parameters']): v for v in source['vertices']}
        id_to_point = {record['id']: point for point, record in saved.items()}
        merged = {}
        per_source_cells = {}
        for cell in source['cells']:
            cuts = expected_cuts(i, cell['active_term'])
            serialized_faces = [(Q(f['constant']), tuple(Q(x) for x in f['coefficients'])) for f in cell['inequalities']]
            assert serialized_faces == base + cuts
            vertices, stages = clip(initial, base, cuts, dimension)
            assert set(vertices) == {id_to_point[name] for name in cell['vertex_ids']}, cell['cell_id']
            assert len(vertices) == cell['vertex_count']
            for point, weights in vertices.items():
                assert sum(weights.values(), Q(0)) == 1 and all(w > 0 for w in weights.values())
                reconstructed = tuple(sum((weights[name] * old_points[name][j] for name in weights), Q(0)) for j in range(dimension))
                assert reconstructed == point
                merged.setdefault(point, (weights, cell['cell_id']))
            cell_checks.append({'cell_id': cell['cell_id'], 'source': i, 'clipping_stages': stages,
                                'independent_vertex_count': len(vertices), 'all_vertices_match': True,
                                'all_weights_nonnegative': True, 'affine_dimension': dimension})
            per_source_cells[cell['cell_id']] = len(vertices)
        assert set(merged) == set(saved)
        strict_new_gaps = 0
        for point, (weights, interpolation_cell) in sorted(merged.items()):
            record = saved[point]
            l_actual = L(i, point)
            l_average = sum((weight * L(i, old_points[name]) for name, weight in weights.items()), Q(0))
            gap = l_average - l_actual
            assert gap >= 0
            is_old = point in initial
            if is_old:
                assert gap == 0 and weights == initial[point]
            else:
                assert gap > 0
                strict_new_gaps += 1
            assert Q(record['L']) == l_actual
            all_interpolations.append({'source': i, 'cell_vertex_id': record['id'],
                                       'parameters': [str(x) for x in point], 'from_cell': interpolation_cell,
                                       'is_original_vertex': is_old,
                                       'old_vertex_weights': [{'old_vertex_id': name, 'weight': str(weight)} for name, weight in weights.items()],
                                       'sum_weights': '1', 'parameter_residual': ['0'] * dimension,
                                       'L_at_point': str(l_actual), 'average_old_L': str(l_average),
                                       'Jensen_gap': str(gap), 'five_sixths_gap': str(Q(5, 6) * gap)})
        totals.append({'source': i, 'cell_vertex_counts': per_source_cells, 'merged_vertices': len(merged),
                       'original_vertices': len(initial), 'new_vertices': len(merged) - len(initial),
                       'new_vertices_with_strict_Jensen_gap': strict_new_gaps})
        print(json.dumps(totals[-1]), flush=True)
    inclusion = read(HERE / 'original67_inclusion.json')['records']
    assert len(inclusion) == len(all_old_ids) == 67
    assert {v['old_vertex_id'] for v in inclusion} == all_old_ids
    assert len(all_interpolations) == 181 and sum(not x['is_original_vertex'] for x in all_interpolations) == 114
    save('independent_cell_checks.json', {'status': 'PASS', 'method': 'Sequential exact edge clipping from independently reconstructed P_i facets.',
                                        'boundary_combination_enumerator_imported_or_executed': False,
                                        'optimizer_calls': 0, 'cells': cell_checks, 'by_source': totals})
    save('old_vertex_interpolations.json', {'status': 'PASS', 'records': all_interpolations,
                                          'all_parameter_interpolations_exact': True,
                                          'all114_new_points_have_strict_L_Jensen_gap': True,
                                          'scope': 'Exact parameter geometry; no ordered-row validity assumed by this checker.'})
    result = {'status': 'PASS_INDEPENDENT_CELL_GEOMETRY', 'parameter_cells_sha256': sha(HERE / 'parameter_cells.json'),
              'checker_sha256': sha(HERE / 'check_geometry.py'), 'cells': 14, 'merged_vertices': 181,
              'cell_vertex_incidences': sum(c['independent_vertex_count'] for c in cell_checks),
              'original_vertices_included': 67, 'new_vertices': 114, 'strict_new_Jensen_gaps': 114,
              'all_cells_full_dimension': True, 'by_source': totals, 'optimizer_calls': 0,
              'ordered_rows_generated': 0, 'ordered_source_bound': False}
    save('geometry_check_result.json', result)
    assert sha(SOURCE / 'parameter_polytopes.json') == expected_domain
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    main()
