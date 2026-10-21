"""Exact witness recovery for the indexed relaxation plus terminal closure rows.

Optimization is restricted to the old 64 atom types, so a feasible point above
two is a valid obstruction for the enlarged row system. Its restricted optimum
must not be described as the unrestricted optimum, or as an SPE realization.
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import ast
import json
import sys

import numpy as np
from scipy.linalg import qr
from scipy.optimize import linprog

from offdiagonal_closure import ROOT, SOURCE, rows


def load_evaluator():
    # Load function definitions without executing the existing exhaustive audit.
    source = ROOT / 'tests/audits/customer_attraction_five_indexed.py'
    tree = ast.parse(source.read_text())
    nodes = []
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module == 'pathlib':
            break
        nodes.append(node)
    namespace = {}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(source), 'exec'), namespace)
    return namespace


def fraction_solve(matrix, rhs):
    mat = [list(map(F, row)) + [F(value)] for row, value in zip(matrix, rhs)]
    n = len(mat)
    for col in range(n):
        pivot = next(i for i in range(col, n) if mat[i][col])
        mat[col], mat[pivot] = mat[pivot], mat[col]
        value = mat[col][col]
        mat[col][col:] = [x / value for x in mat[col][col:]]
        for row in range(col + 1, n):
            value = mat[row][col]
            if value:
                mat[row][col:] = [x - value * y for x, y in
                                  zip(mat[row][col:], mat[col][col:])]
    solution = [F(0)] * n
    for row in range(n - 1, -1, -1):
        solution[row] = mat[row][-1] - sum((mat[row][j] * solution[j]
                                          for j in range(row + 1, n)), F(0))
    return solution


def main():
    ns = load_evaluator()
    primal = json.loads(SOURCE.read_text())['primal']
    names = primal['rows'] + list(rows(primal['atoms'][0]))
    columns, welfare, comparison = [], [], []
    for atom in primal['atoms']:
        bits = tuple(map(int, atom['bits']))
        rr = ns['evaluate'](bits, [atom['AB_hist'], atom['AE_hist'], atom['second_hist']],
                            atom['menus_lh'], True)
        rr.update(rows(atom))
        columns.append([rr[n] for n in names])
        welfare.append(F(int(any(bits[:5]))))
        comparison.append(F(int(sum(n * ty[0] for n, ty in
                                      zip(atom['AB_hist'], ns['types'])) > 0)))
    matrix = np.array(columns, dtype=float).T
    out = linprog(-np.asarray(comparison, dtype=float), A_ub=-matrix,
                  b_ub=np.zeros(len(names)), A_eq=[np.asarray(welfare, dtype=float)],
                  b_eq=[1], bounds=(0, None), method='highs')
    assert out.success, out.message
    support = np.where(out.x > 1e-8)[0]
    active = np.where(abs(matrix @ out.x) < 1e-7)[0]
    floating_equations = np.vstack([np.asarray(welfare, dtype=float)[support],
                                    matrix[active][:, support]])
    _, R, piv = qr(floating_equations.T, pivoting=True, mode='economic')
    assert np.count_nonzero(abs(np.diag(R)) > 1e-8) == len(support)
    selected = list(piv[:len(support)])
    equations = [[welfare[k] for k in support]] + [
        [columns[k][r] for k in support] for r in active]
    exact_matrix = [equations[i] for i in selected]
    rhs = [int(i == 0) for i in selected]
    solution = fraction_solve(exact_matrix, rhs)
    values = [F(0)] * len(columns)
    for k, value in zip(support, solution):
        values[k] = value
    assert all(value >= 0 for value in values)
    slacks = [sum((v * columns[k][r] for k, v in enumerate(values)), F(0))
              for r in range(len(names))]
    assert min(slacks) >= 0
    assert sum((v * w for v, w in zip(values, welfare)), F(0)) == 1
    ratio = sum((v * o for v, o in zip(values, comparison)), F(0))
    assert ratio > 2
    report = {
        'scope': 'Exact feasible point for 437 original plus 10 terminal off-diagonal rows; no SPE',
        'row_count': len(names), 'source_support_types': len(columns),
        'positive_masses': len(support), 'welfare': '1', 'comparison_cover': str(ratio),
        'ratio_float': float(ratio), 'gap_above_two': str(ratio - 2),
        'minimum_slack': str(min(slacks)), 'zero_slacks': sum(s == 0 for s in slacks),
        'atoms': [dict(atom, mass_numerator=None, exact_mass=str(value))
                  for atom, value in zip(primal['atoms'], values) if value],
        'slacks': {name: str(slack) for name, slack in zip(names, slacks)},
        'conclusion': 'These ten added rows do exclude the old optimal point, but still do not imply half coverage.'}
    output = Path(__file__).with_suffix('.json')
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('atoms', 'slacks')}, indent=2))


if __name__ == '__main__':
    main()
