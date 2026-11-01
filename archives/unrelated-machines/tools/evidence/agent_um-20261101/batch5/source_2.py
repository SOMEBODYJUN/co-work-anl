#!/usr/bin/env python3
"""真实有限调度分布的压缩向量选择：有理 Gram 坐标核验。

输入是显式 P、T、完整分配原子和正有理权重，不调用配置/矩 oracle。
与独立审计的样本空间 Gram--Schmidt 不同，本程序选列并求 Gram 逆。
默认只输出 stdout；重复 literal 共用算子，输出证据不含探索日志。
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import platform


def inner(a, b, weights):
    return sum((w*x*y for w, x, y in zip(weights, a, b)), F())


def matvec(a, b):
    return [sum((x*y for x, y in zip(row, b)), F()) for row in a]


def inverse(a):
    n = len(a)
    z = [list(row)+[F(i == j) for j in range(n)]
         for i, row in enumerate(a)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if z[i][j])
        z[j], z[pivot] = z[pivot], z[j]
        scale = z[j][j]
        z[j] = [x/scale for x in z[j]]
        for i in range(n):
            if i != j:
                scale = z[i][j]
                z[i] = [x-scale*y for x, y in zip(z[i], z[j])]
    result = [row[n:] for row in z]
    assert all(matvec(a, col) == [F(i == j) for i in range(n)]
               for j, col in enumerate(zip(*result)))
    return result


def independent_columns(columns):
    """Plain rational column elimination; retain the original selected vectors."""
    echelon = {}
    selected = []
    for original in columns:
        residual = list(original)
        for pivot in sorted(echelon):
            scale = residual[pivot]
            residual = [x-scale*y for x, y in zip(residual, echelon[pivot])]
        pivot = next((i for i, x in enumerate(residual) if x), None)
        if pivot is not None:
            scale = residual[pivot]
            echelon[pivot] = [x/scale for x in residual]
            selected.append(original)
    return selected


def audit(path):
    raw = path.read_bytes()
    data = json.loads(raw)
    m, n = data['machines'], data['jobs']
    assert type(m) is int and type(n) is int and m >= 1 and n >= 0
    p = [[None if x is None else F(x) for x in row]
         for row in data['processing_times']]
    assert len(p) == m and all(len(row) == n for row in p)
    assert all(x is None or x >= 0 for row in p for x in row)
    target = F(data['target'])
    assert target >= 0
    atoms = [a['assignment'] for a in data['distribution']]
    weights = [F(a['weight']) for a in data['distribution']]
    assert atoms and len(atoms) == len(weights) and all(w > 0 for w in weights)
    total = sum(weights, F())
    weights = [w/total for w in weights]
    atom_loads = []
    for atom in atoms:
        assert len(atom) == n and all(type(i) is int and 0 <= i < m for i in atom)
        assert all(p[i][j] is not None for j, i in enumerate(atom))
        loads = [sum((p[i][j] for j in range(n) if atom[j] == i), F())
                 for i in range(m)]
        assert max(loads) <= target
        atom_loads.append(loads)
    order = data['job_order']
    assert sorted(order) == list(range(n))
    one = tuple(F(1) for _ in atoms)
    literals = {(i, j): tuple(F(a[j] == i) for a in atoms)
                for j in range(n) for i in range(m)}
    basis = independent_columns([one]+list(literals.values()))
    gram = [[inner(a, b, weights) for b in basis] for a in basis]
    gram_inverse = inverse(gram)

    def coefficients(function):
        return matvec(gram_inverse, [inner(b, function, weights) for b in basis])

    def evaluate(c):
        return [sum((x*b[h] for x, b in zip(c, basis)), F())
                for h in range(len(atoms))]

    # Exact reconstruction proves that this basis spans the full literal space.
    assert all(evaluate(coefficients(f)) == list(f)
               for f in [one]+list(literals.values()))
    operators = {}
    for event in set(literals.values()):
        h = [[inner(a, [e*x for e, x in zip(event, b)], weights)
              for b in basis] for a in basis]
        operators[event] = [list(row) for row in zip(
            *(matvec(gram_inverse, col) for col in zip(*h)))]
    state = coefficients(one)
    sigma = [-1]*n
    scores_record = []
    normalized_gaps = []
    true_prefix = [True]*len(atoms)
    for j in order:
        norm = sum((x*y for x, y in zip(state, matvec(gram, state))), F())
        assert norm > 0
        images = [matvec(operators[literals[i, j]], state) for i in range(m)]
        assert [sum(xs, F()) for xs in zip(*images)] == state
        scores = [sum((x*y for x, y in zip(c, matvec(gram, c))), F())
                  for c in images]
        winner = max(range(m), key=lambda i: scores[i])
        assert p[winner][j] is not None and scores[winner] > 0
        gap = scores[winner]-max([s for i, s in enumerate(scores) if i != winner]
                                or [F()])
        assert gap > 0  # These frozen witnesses deliberately avoid every tie.
        normalized_gaps.append(gap/norm)
        sigma[j] = winner
        state = images[winner]
        true_prefix = [live and a[j] == winner for live, a in zip(true_prefix, atoms)]
        if n <= 20:
            scores_record.append({'job': j, 'machine': winner,
                                  'scores': list(map(str, scores)),
                                  'strict_gap': str(gap),
                                  'true_prefix_atoms': sum(true_prefix)})
    loads = [sum((p[i][j] for j in range(n) if sigma[j] == i), F()) for i in range(m)]
    assert sigma == data['expected_assignment']
    if 'expected_loads' in data:
        assert loads == list(map(F, data['expected_loads']))
    return {'arithmetic': 'fractions.Fraction; independent columns and Gram inverse',
            'python_version': platform.python_version(),
            'input_sha256': hashlib.sha256(raw).hexdigest(),
            'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'machines': m, 'jobs': n, 'atoms': len(atoms), 'dimension': len(basis),
            'target': str(target), 'max_support_makespan': str(max(map(max, atom_loads))),
            'all_processing_times_positive_and_finite': all(
                x is not None and x > 0 for row in p for x in row),
            'all_winners_strict': True, 'strict_steps': len(order),
            'minimum_gap_over_state_norm': str(min(normalized_gaps)) if normalized_gaps else None,
            'assignment': sigma, 'loads': list(map(str, loads)), 'makespan': str(max(loads)),
            'remaining_true_prefix_atoms': sum(true_prefix), 'steps': scores_record,
            'scope': 'Exact supplied finite distribution and fixed order; not a general upper bound.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('inputs', nargs='+', type=Path)
    args = parser.parse_args()
    print(json.dumps({'runs': [audit(path) for path in args.inputs]},
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
