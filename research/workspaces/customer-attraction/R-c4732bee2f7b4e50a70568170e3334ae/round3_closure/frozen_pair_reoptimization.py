"""Restricted old-64-type optimization, with exact primal and dual recovery.

The upper certificate is only for these 64 permitted types. It does not price
the unrestricted histogram universe and is not a universal SPE welfare bound.
"""
from fractions import Fraction as F
from pathlib import Path
import ast
import json
import sys

import numpy as np
from scipy.linalg import qr
from scipy.optimize import linprog

from partition_pair_closure import ROOT, ACTOR, SOURCE, rows as pair_rows
sys.path.insert(0, str(ACTOR / 'continuation_completion'))
from offdiagonal_closure import rows as terminal_rows


def load_evaluator():
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
    n = len(matrix)
    assert all(len(row) == n for row in matrix) and len(rhs) == n
    mat = [[F(v) for v in row] + [F(b)] for row, b in zip(matrix, rhs)]
    for col in range(n):
        pivot = next(i for i in range(col, n) if mat[i][col])
        mat[col], mat[pivot] = mat[pivot], mat[col]
        div = mat[col][col]
        mat[col][col:] = [v/div for v in mat[col][col:]]
        for i in range(col+1, n):
            div = mat[i][col]
            if div:
                mat[i][col:] = [v-div*w for v, w in zip(mat[i][col:], mat[col][col:])]
    result = [F(0)]*n
    for i in range(n-1, -1, -1):
        result[i] = mat[i][-1] - sum((mat[i][j]*result[j] for j in range(i+1, n)), F(0))
    return result


def independent_rows(equations, width):
    a = np.asarray(equations, dtype=float)
    _, r, piv = qr(a.T, pivoting=True, mode='economic')
    rank = np.count_nonzero(abs(np.diag(r)) > 1e-8)
    assert rank == width, (rank, width)
    return list(piv[:width])


def optimize(overlap):
    evaluator = load_evaluator()['evaluate']
    src = json.loads(SOURCE.read_text())['primal']
    names = src['rows'] + list(terminal_rows(src['atoms'][0])) + list(pair_rows(src['atoms'][0], overlap=overlap))
    columns, welfare, comparison = [], [], []
    for atom in src['atoms']:
        bits = tuple(map(int, atom['bits']))
        rr = evaluator(bits, [atom['AB_hist'], atom['AE_hist'], atom['second_hist']], atom['menus_lh'], True)
        rr.update(terminal_rows(atom))
        rr.update(pair_rows(atom, overlap=overlap))
        columns.append([rr[name] for name in names])
        welfare.append(F(int(any(bits[:5]))))
        comparison.append(F(int(any(atom['AB_hist'][4:]))))
    matrix = np.asarray(columns, dtype=float).T
    out = linprog(-np.asarray(comparison, dtype=float), A_ub=-matrix,
                  b_ub=np.zeros(len(names)), A_eq=[np.asarray(welfare, dtype=float)],
                  b_eq=[1], bounds=(0, None), method='highs')
    if out.status == 2:
        # A nonnegative sum of necessary rows is bounded by -W on every
        # permitted column. The resulting exact contradiction certifies that
        # this support cannot contain any normalized feasible point.
        farkas = linprog(np.ones(len(names)), A_ub=matrix.T,
                         b_ub=-np.asarray(welfare, dtype=float),
                         bounds=(0, None), method='highs')
        assert farkas.success, farkas.message
        support = list(np.where(farkas.x > 1e-8)[0])
        binding = list(np.where(abs(matrix.T @ farkas.x + np.asarray(welfare, dtype=float)) < 1e-7)[0])
        equations = [[columns[k][r] for r in support] for k in binding]
        pick = independent_rows(equations, len(support))
        lambdas = fraction_solve([equations[r] for r in pick], [-welfare[binding[r]] for r in pick])
        assert min(lambdas) >= 0
        residuals = [-welfare[k]-sum((v*columns[k][r] for r, v in zip(support, lambdas)), F(0))
                     for k in range(len(columns))]
        assert min(residuals) >= 0
        return {
            'scope': 'Exact infeasibility only over the frozen 64 atom types; no unrestricted SPE conclusion',
            'overlap_subtraction': overlap, 'row_count': len(names), 'permitted_types': len(columns),
            'normalized_feasible': False, 'positive_farkas_multipliers': len(support),
            'certificate': 'sum(lambda_r * row_r(z)) <= -w(z) for each of the 64 permitted types',
            'minimum_certificate_residual': str(min(residuals)),
            'farkas_multipliers': {names[r]: str(v) for r, v in zip(support, lambdas)},
            'certificate_residuals': [str(v) for v in residuals],
        }
    assert out.success, out.message
    support = list(np.where(out.x > 1e-8)[0])
    active = list(np.where(abs(matrix @ out.x) < 1e-7)[0])
    equations = [[welfare[k] for k in support]] + [[columns[k][r] for k in support] for r in active]
    pick = independent_rows(equations, len(support))
    exact = fraction_solve([equations[r] for r in pick], [int(r == 0) for r in pick])
    primal = [F(0)]*len(columns)
    for k, value in zip(support, exact):
        primal[k] = value
    assert min(primal) >= 0
    assert sum(v*w for v, w in zip(primal, welfare)) == 1
    slacks = [sum((primal[k]*columns[k][r] for k in range(len(columns))), F(0)) for r in range(len(names))]
    assert min(slacks) >= 0
    ratio = sum((v*o for v, o in zip(primal, comparison)), F(0))

    positive = list(np.where(-out.ineqlin.marginals > 1e-8)[0])
    binding = list(np.where(out.lower.marginals < 1e-7)[0])
    dual_eq = [[welfare[k]] + [-columns[k][r] for r in positive] for k in binding]
    pick = independent_rows(dual_eq, 1+len(positive))
    dual = fraction_solve([dual_eq[r] for r in pick], [comparison[binding[r]] for r in pick])
    beta, lambdas = dual[0], dual[1:]
    assert min(lambdas) >= 0
    residual = [beta*welfare[k]-comparison[k]-sum((value*columns[k][r] for r, value in zip(positive, lambdas)), F(0))
                for k in range(len(columns))]
    assert min(residual) >= 0
    assert beta == ratio
    return {
        'scope': 'Exact optimum only over the frozen 64 atom types, not all histograms or any SPE claim',
        'overlap_subtraction': overlap, 'row_count': len(names), 'permitted_types': len(columns),
        'positive_masses': len(support), 'welfare': '1', 'comparison_cover': str(ratio),
        'ratio_float': float(ratio), 'gap_above_two': str(ratio-2),
        'minimum_primal_slack': str(min(slacks)), 'minimum_dual_residual': str(min(residual)),
        'positive_dual_multipliers': len(positive), 'dual_beta': str(beta),
        'atoms': [dict(atom, mass_numerator=None, exact_mass=str(v)) for atom, v in zip(src['atoms'], primal) if v],
        'slacks': {name: str(value) for name, value in zip(names, slacks)},
        'dual_multipliers': {names[r]: str(v) for r, v in zip(positive, lambdas)},
        'dual_residuals': [str(v) for v in residual],
    }


if __name__ == '__main__':
    report = {'weak_pair_tax': optimize(2), 'retained_overlap_pair_tax': optimize(1)}
    Path(__file__).with_suffix('.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({name: {k: v for k, v in r.items() if k not in ('atoms', 'slacks', 'dual_multipliers', 'dual_residuals', 'certificate_residuals')}
                      for name, r in report.items()}, indent=2))
