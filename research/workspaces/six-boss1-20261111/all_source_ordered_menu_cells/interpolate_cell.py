#!/usr/bin/env python3
"""Exact barycentric map inside a chosen cell, by repeated boundary descent.

Accept one JSON argument {"source":i,"parameters":[...],"cell_id":optional}.
Only local geometry is read. No optimization or project code is imported.
"""
from fractions import Fraction as F
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent


def dot(left, right):
    return sum((a * b for a, b in zip(left, right)), F(0))


def null_direction(normals, dimension):
    work = [list(row) for row in normals]
    pivots = []
    for column in range(dimension):
        row = len(pivots)
        selected = next((j for j in range(row, len(work)) if work[j][column]), None)
        if selected is None:
            continue
        work[row], work[selected] = work[selected], work[row]
        divisor = work[row][column]
        work[row] = [x / divisor for x in work[row]]
        for j in range(len(work)):
            if j != row and work[j][column]:
                factor = work[j][column]
                work[j] = [x - factor * y for x, y in zip(work[j], work[row])]
        pivots.append(column)
    free = next((j for j in range(dimension) if j not in pivots), None)
    if free is None:
        return None
    direction = [F(0)] * dimension
    direction[free] = F(1)
    for row, column in enumerate(pivots):
        direction[column] = -work[row][free]
    assert all(dot(normal, direction) == 0 for normal in normals)
    return tuple(direction)


def interpolate(source, parameters, cell_id=None, geometry=None):
    if geometry is None:
        geometry = json.loads((HERE / 'parameter_cells.json').read_text())
    definition = next(item for item in geometry['sources'] if item['source'] == source)
    dimension = definition['dimension']
    point = tuple(F(x) for x in parameters)
    assert len(point) == dimension
    selected = None
    for cell in definition['cells']:
        if cell_id is not None and cell['cell_id'] != cell_id:
            continue
        faces = [(F(f['constant']), tuple(F(x) for x in f['coefficients'])) for f in cell['inequalities']]
        if all(c + dot(normal, point) >= 0 for c, normal in faces):
            selected = cell
            break
    if selected is None:
        raise ValueError('The rational point is outside the requested parameter cell/domain.')
    all_points = {v['id']: tuple(F(x) for x in v['parameters']) for v in definition['vertices']}
    vertices = {all_points[name]: name for name in selected['vertex_ids']}
    cache = {}
    calls = 0

    def descend(current, depth):
        nonlocal calls
        calls += 1
        if current in vertices:
            return {vertices[current]: F(1)}
        if current in cache:
            return cache[current]
        assert depth < dimension
        slacks = [c + dot(normal, current) for c, normal in faces]
        assert all(x >= 0 for x in slacks)
        active = [normal for slack, (_, normal) in zip(slacks, faces) if slack == 0]
        direction = null_direction(active, dimension)
        assert direction is not None
        lower, upper = None, None
        for slack, (_, normal) in zip(slacks, faces):
            slope = dot(normal, direction)
            if slope > 0:
                bound = -slack / slope
                lower = bound if lower is None else max(lower, bound)
            elif slope < 0:
                bound = -slack / slope
                upper = bound if upper is None else min(upper, bound)
        assert lower is not None and upper is not None and lower < 0 < upper
        low_point = tuple(x + lower * direction[j] for j, x in enumerate(current))
        high_point = tuple(x + upper * direction[j] for j, x in enumerate(current))
        low_weight, high_weight = upper / (upper - lower), -lower / (upper - lower)
        low = descend(low_point, depth + 1)
        high = descend(high_point, depth + 1)
        weights = {}
        for name, weight in low.items():
            weights[name] = weights.get(name, F(0)) + low_weight * weight
        for name, weight in high.items():
            weights[name] = weights.get(name, F(0)) + high_weight * weight
        cache[current] = {name: weight for name, weight in sorted(weights.items()) if weight}
        return cache[current]

    weights = descend(point, 0)
    assert all(w > 0 for w in weights.values()) and sum(weights.values(), F(0)) == 1
    reconstructed = tuple(sum((weight * all_points[name][j] for name, weight in weights.items()), F(0)) for j in range(dimension))
    assert reconstructed == point
    return {'source': source, 'cell_id': selected['cell_id'], 'parameters': [str(x) for x in point],
            'weights': [{'vertex_id': name, 'weight': str(weight)} for name, weight in weights.items()],
            'sum_weights': '1', 'parameter_residual': ['0'] * dimension,
            'boundary_descent_calls': calls, 'optimizer_calls': 0}


if __name__ == '__main__':
    request = json.loads(sys.argv[1])
    print(json.dumps(interpolate(request['source'], request['parameters'], request.get('cell_id')), indent=2))
