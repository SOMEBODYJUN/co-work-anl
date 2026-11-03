#!/usr/bin/env python3
"""Read every stored array and audit this finite necessary-condition LP exactly.

This verifies a relaxation certificate, never the existence of a full SPE.
Only the 16 primal support columns and 14 active dual rows need rational work.
The original generator independently rebuilds every float matrix entry.
"""
from __future__ import annotations

import argparse
import contextlib
from fractions import Fraction as F
import hashlib
import importlib.util
import io
from itertools import combinations_with_replacement, product
import json
from math import comb
import os
from pathlib import Path
import platform
import runpy
import sys
from types import SimpleNamespace

import numpy as np
import scipy
from scipy import optimize

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
LABELS = 'ABCDEQRST'
PATHS = (tuple(range(5)), (4, 5, 6, 7, 8))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def share(n, den):
    return F(n, den) if n else F(0)


def tables():
    dep = HERE / 'original/tests/audits'
    three = load_module('profiles_three', dep / 'customer_attraction_three_remaining_profit.py')
    four = load_module('profiles_four', dep / 'customer_attraction_four_remaining_profit.py')
    r3 = {(p, *a, d): min(
        sum(F(v) * F(p)**j for j, v in enumerate(three.coefficients(*a, q, r, d, ell)))
        / (30 * (p + 1) * (p + 2) * (p + 3))
        for q, r in product((0, 1), repeat=2) for ell in range(4))
        for p in range(3) for a in product((0, 1), repeat=3) for d in range(4)}
    r4 = {(p, *a): min(four.direct_rho((*a, *b), p)
                       for b in product((0, 1), repeat=3))
          for p in range(2) for a in product((0, 1), repeat=4)}
    assert min(r3.values()) >= 0 and min(r4.values()) >= 0
    return r3, r4


def state(bits):
    result = []
    for path in PATHS:
        count = sum(bits[j] for j in path)
        result.append([share(bits[j], count) for j in path])
    return result


def tail_data(bits, e, h, k, r3, r4):
    path = PATHS[h]
    i = 5 - k
    p = sum(bits[j] for j in path[:i])
    actual = tuple(bits[j] for j in path[i:])
    V = sum(state(bits)[h][i:])
    beta = {2: F(1), 3: F(5, 3), 4: F(1499, 750)}[k]
    if k == 2:
        V += F(actual[0], (p + 1) * (p + 2))
    if k == 4:
        V -= r4[(p, *actual)] / beta
    rhs = sum(choose(e, j) * choose(5 - e, k - j) * share(j, p + j)
              for j in range(1, k + 1))
    if k == 3:
        rhs += sum(choose(e, j) * choose(5 - e, k - j) * r3[(p, *actual, j)]
                   for j in range(4))
    return p, actual, beta * V, rhs


def exact_column(bits, e, r3, r4):
    rows, names = [], []
    us = state(bits)
    for h, path in enumerate(PATHS):
        for i in range(5):
            if h and i == 0:
                continue
            p = sum(bits[j] for j in path[:i])
            rem = 5 - i
            for j, label in enumerate(LABELS):
                names.append(f'{h}:{i}:K{label}')
                rows.append(us[h][i] - F(bits[j], p + rem))
            names.append(f'{h}:{i}:opt')
            rows.append(5 * us[h][i] - F(e, p + rem))
        for k in (2, 3, 4):
            p, actual, lhs, rhs = tail_data(bits, e, h, k, r3, r4)
            names.append(f'{h}:tail{k}:opt')
            rows.append(comb(5, k) * lhs - rhs)
            for inds in combinations_with_replacement(range(9), k):
                q = sum(bits[j] for j in inds)
                rhs = share(q, p + q)
                if k == 3:
                    rhs += r3[(p, *actual, q)]
                names.append(f'{h}:tail{k}:cmp' + ''.join(LABELS[j] for j in inds))
                rows.append(lhs - rhs)
    names.append('rootE')
    rows.append(us[0][0] - us[1][0])
    return names, rows


def selected_coeff(name, bits, e, r3, r4):
    us = state(bits)
    if name == 'rootE':
        return us[0][0] - us[1][0]
    h, at, query = name.split(':')
    h = int(h)
    if at.startswith('tail'):
        k = int(at[4:])
        assert query == 'opt', name
        _, _, lhs, rhs = tail_data(bits, e, h, k, r3, r4)
        return comb(5, k) * lhs - rhs
    i = int(at)
    path = PATHS[h]
    p = sum(bits[j] for j in path[:i])
    if query == 'opt':
        return 5 * us[h][i] - F(e, p + 5 - i)
    assert query.startswith('K')
    return us[h][i] - F(bits[LABELS.index(query[1:])], p + 5 - i)


def solve_unique(equations, width):
    """Fraction Gaussian elimination, ignoring dependent consistent equations."""
    basis = {}
    for vals, rhs in equations:
        row = list(vals) + [F(rhs)]
        for pivot in sorted(basis):
            factor = row[pivot]
            if factor:
                row = [a - factor * b for a, b in zip(row, basis[pivot])]
        pivot = next((j for j in range(width) if row[j]), None)
        if pivot is None:
            assert row[-1] == 0, ('inconsistent', row[-1])
            continue
        scale = row[pivot]
        basis[pivot] = [x / scale for x in row]
    assert len(basis) == width, ('not unique', len(basis), width)
    solution = [F(0)] * width
    for pivot in sorted(basis, reverse=True):
        row = basis[pivot]
        solution[pivot] = row[-1] - sum(row[j] * solution[j] for j in range(pivot + 1, width))
    return solution


def run(input_path):
    # All eight arrays are eagerly loaded, including all 4,629,504 M entries.
    with np.load(input_path, allow_pickle=False) as z:
        arrays = {k: z[k].copy() for k in z.files}
    assert list(arrays) == ['x', 'e', 'w', 'M', 'names', 'primal', 'dual', 'beta']
    x, e, w, M, names, primal, dual, beta = [arrays[k] for k in arrays]
    o = (e > 0).astype(float)
    array_report = {}
    for key, a in arrays.items():
        item = {'shape': list(a.shape), 'dtype': str(a.dtype), 'nbytes': a.nbytes,
                'array_c_order_sha256': hashlib.sha256(a.tobytes(order='C')).hexdigest()}
        if a.dtype.kind in 'iufb':
            item.update(min=float(np.min(a)), max=float(np.max(a)), sum=float(np.sum(a)),
                        nonzero=int(np.count_nonzero(a)), all_finite=bool(np.all(np.isfinite(a))))
            assert item['all_finite']
        array_report[key] = item
    expected = np.repeat(np.array(list(product(range(2), repeat=9)), float), 6, axis=0)
    assert np.array_equal(x, expected)
    assert np.array_equal(e, np.tile(np.arange(6), 512))
    assert np.array_equal(w, (x[:, :5].sum(axis=1) > 0).astype(float))
    # Execute unchanged source for full matrix construction, substituting no solver result.
    old_solver, old_cwd = optimize.linprog, Path.cwd()
    try:
        optimize.linprog = lambda *a, **kw: SimpleNamespace(message='matrix-rebuild-only', success=False)
        os.chdir(HERE / 'original')
        with contextlib.redirect_stdout(io.StringIO()):
            rebuilt = runpy.run_path(str(HERE / 'original/test_profiles.py'))
    finally:
        optimize.linprog = old_solver
        os.chdir(old_cwd)
    for key in ('x', 'e', 'w', 'M'):
        assert np.array_equal(arrays[key], rebuilt[key]), key
    assert list(names) == rebuilt['rnames']
    r3, r4 = tables()
    support = np.flatnonzero(primal > 1e-7).tolist()
    active = np.flatnonzero(dual > 1e-7).tolist()
    columns = []
    max_error = 0.
    for index in support:
        row_names, col = exact_column(tuple(map(int, x[index])), int(e[index]), r3, r4)
        assert row_names == list(names)
        max_error = max(max_error, float(np.max(np.abs(M[:, index] - np.array(list(map(float, col)))))))
        columns.append(col)
    tight = np.flatnonzero(np.abs(M @ primal) < 1e-9).tolist()
    equations = [([F(int(w[i])) for i in support], F(1))]
    equations.extend(([columns[j][r] for j in range(len(support))], F(0)) for r in tight)
    p_exact = solve_unique(equations, len(support))
    assert min(p_exact) > 0
    primal_slacks = [sum(columns[j][r] * p_exact[j] for j in range(len(support)))
                     for r in range(len(names))]
    assert min(primal_slacks) >= 0
    objective = sum(p_exact[j] for j, i in enumerate(support) if e[i] > 0)
    assert objective > 2
    # Positive primal columns have zero reduced cost; recover 14 multipliers and beta.
    d_eq = [([-columns[j][r] for r in active] + [F(int(w[i]))], F(int(e[i] > 0)))
            for j, i in enumerate(support)]
    d_solution = solve_unique(d_eq, len(active) + 1)
    d_exact, beta_exact = d_solution[:-1], d_solution[-1]
    assert min(d_exact) > 0 and beta_exact == objective
    reduced_costs = []
    dual_float_error = 0.
    for i in range(len(x)):
        bits, ee = tuple(map(int, x[i])), int(e[i])
        coeffs = [selected_coeff(str(names[r]), bits, ee, r3, r4) for r in active]
        dual_float_error = max(dual_float_error, max(abs(float(c) - M[r, i])
                                                     for c, r in zip(coeffs, active)))
        reduced_costs.append(beta_exact * int(w[i]) - int(ee > 0)
                             - sum(a * b for a, b in zip(d_exact, coeffs)))
    assert min(reduced_costs) >= 0
    assert max_error < 1e-12 and dual_float_error < 1e-12
    float_p = M @ primal
    float_d = float(beta) * w - o - M.T @ dual
    report = {
        'scope': 'exact optimum of this 1507-row rational relaxation; no full-SPE realizability claim',
        'source_npz_sha256': '9eaf0df61efb2d3c46da26294450f7fca94d88abf86550e1f5a5af9340cefb7f',
        'input_sha256': sha(input_path), 'arrays': array_report,
        'full_float_matrix_rebuilt_entrywise_identically': True,
        'exact_primal_support_columns_checked': len(support),
        'exact_primal_inequalities_checked': len(names),
        'exact_dual_active_rows': len(active), 'exact_dual_columns_checked': len(x),
        'exact_objective': str(objective), 'exact_objective_decimal': float(objective),
        'exact_objective_minus_two': str(objective - 2),
        'exact_min_primal_slack': str(min(primal_slacks)),
        'exact_min_reduced_cost': str(min(reduced_costs)),
        'exact_primal_normalization': str(sum(F(int(w[i])) * v for i, v in zip(support, p_exact))),
        'rational_float_max_support_error': max_error,
        'rational_float_max_active_row_error': dual_float_error,
        'frozen_float_min_primal_slack': float(float_p.min()),
        'frozen_float_min_reduced_cost': float(float_d.min()),
        'frozen_float_max_complementarity_error': max(float(np.max(np.abs(primal * float_d))),
                                                     float(np.max(np.abs(dual * float_p)))),
        'primal': [{'column': i, 'membership_ABCDEQRST': ''.join(map(str, map(int, x[i]))),
                    'optimal_multiplicity': int(e[i]), 'mass': str(v)} for i, v in zip(support, p_exact)],
        'dual': [{'row': i, 'name': str(names[i]), 'multiplier': str(v)} for i, v in zip(active, d_exact)],
        'python': platform.python_version(), 'numpy': np.__version__, 'scipy': scipy.__version__,
        'randomness': 'none; all stored arrays, all 1507 primal rows, all 3072 dual columns',
        'dependency_files': {str(p.relative_to(HERE)): sha(p) for p in sorted((HERE / 'original').rglob('*.py'))},
    }
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=HERE / 'test_profiles.arrays.npz')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = run(args.input.resolve())
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ('scope', 'exact_objective', 'exact_objective_decimal',
                                           'exact_min_primal_slack', 'exact_min_reduced_cost')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
