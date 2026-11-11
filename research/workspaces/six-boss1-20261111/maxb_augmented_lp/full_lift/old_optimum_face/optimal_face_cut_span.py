"""Exact algebra only: is the compact cut fixed on the whole old optimum face?

An old exact optimum satisfies every strictly-positive old-dual row at zero
and every strictly-positive old residual column at zero. A signed identity
using only those equalities can prove a constant cut value on that entire
face. A failed span attempt is retained without an infeasibility claim.
"""
from datetime import datetime, timezone
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import gzip
import json
import time
import traceback

HERE = Path(__file__).resolve().parent
WORK = HERE.parents[2]
BASE = WORK / 'full624_augmented_lp/recovery'


def sha(path): return sha256(path.read_bytes()).hexdigest()


def read(path):
    if path.suffix == '.gz':
        with gzip.open(path, 'rt') as f: return json.load(f)
    return json.loads(path.read_text())


@lru_cache(maxsize=None)
def rat(v): return Q(v)


def write(name, value):
    p = HERE / name; assert not p.exists()
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    start = time.monotonic()
    pins = {BASE / 'exact_matrix.json.gz': '96388092e21621f157b4428ce99f98b93afa99ed3a0c12c72b1d6475c26fba30',
            BASE / 'exact_dual_certificate.json': '22381bc9844aa5452b45a5bd8ef4a6148808388455b80666b49475df0f7377b3',
            BASE / 'augmented_lp_exact.json': 'cb45ee6f8df153764c91bd77d0543527cc44719ff7cc43646ffce06a7921a932',
            WORK / 'terminal_response_cycles/max_b_exact_certificate.json': 'f6189600d6ccccdbd9fcbc4ae4af9e768c9382af8de1ae41d6e6a7ee7662f664'}
    for p, pin in pins.items(): assert sha(p) == pin
    matrix = read(BASE / 'exact_matrix.json.gz'); dual = read(BASE / 'exact_dual_certificate.json')
    point = read(BASE / 'augmented_lp_exact.json'); cutcert = read(WORK / 'terminal_response_cycles/max_b_exact_certificate.json')
    cut = {j: Q(v) for j, v in cutcert['sparse_original4849_row_K_normalized']}
    alpha = Q(cutcert['K_normalized_point_value']); assert alpha < 0
    row_support = [i for i, v in dual['row_multipliers'] if Q(v) > 0]
    old_residuals = list(map(Q, dual['residuals'])); assert min(old_residuals) >= 0
    keep = [j for j, value in enumerate(old_residuals) if value == 0]
    keep.sort(key=lambda j: (0 if j >= 15593 else 1 if j >= 4849 else 2, j))
    n = len(row_support); assert n == 531
    columns = {j: {} for j in keep}
    for k, i in enumerate(row_support):
        for j, value in matrix['rows'][i]:
            if j in columns: columns[j][k] = rat(value)
    equations = []; equation_columns = []; seen = set()
    for j in keep:
        equation = columns[j]
        rhs = cut.get(j, Q()) - alpha * Q(matrix['normalization'][j])
        if rhs: equation[n] = rhs
        if not equation: continue
        pivot = min(equation); scale = equation[pivot]
        sig = tuple((k, v / scale) for k, v in sorted(equation.items()))
        if sig in seen: continue
        seen.add(sig); equations.append(equation); equation_columns.append(j)
    write('old_optimal_face_span_inputs.json', {
        'source_sha256': {str(p.relative_to(WORK)): pin for p, pin in pins.items()},
        'script_sha256': sha(Path(__file__)), 'old_positive_dual_rows': row_support,
        'old_zero_residual_columns': keep, 'fixed_normalization_coefficient': str(alpha),
        'cut': [[j, str(v)] for j, v in cut.items()], 'unknowns': n,
        'equation_columns': equation_columns,
        'equations': [[[j, str(v)] for j, v in sorted(eq.items())] for eq in equations],
        'scope': 'Signed linear-span test only, no optimization and no restriction to the old point positive support.'})
    basis = {}; last = time.monotonic()
    try:
        for processed, encoded in enumerate(equations, 1):
            row = dict(encoded)
            while row:
                pivot = min(row)
                if pivot == n:
                    raise ArithmeticError(('cut_not_in_this_equality_span', processed, equation_columns[processed - 1], str(row[n])))
                if pivot not in basis:
                    scale = row[pivot]; basis[pivot] = {j: v / scale for j, v in row.items()}; break
                scale = row[pivot]
                for j, v in basis[pivot].items():
                    value = row.get(j, Q()) - scale * v
                    if value: row[j] = value
                    else: row.pop(j, None)
            now = time.monotonic()
            if now - last > 15:
                print(json.dumps({'event': 'exact_span_progress', 'equations': processed, 'rank': len(basis), 'seconds': now - start}), flush=True)
                last = now
            if now - start > 120: raise TimeoutError('Exact signed-span elimination exceeded120 seconds; no optimizer is running.')
        solution = [Q()] * n
        for pivot in sorted(basis, reverse=True):
            row = basis[pivot]
            solution[pivot] = row.get(n, Q()) - sum((v * solution[j] for j, v in row.items() if pivot < j < n), Q())
        remainder = [cut.get(j, Q()) - alpha * Q(matrix['normalization'][j]) for j in range(20585)]
        for i, weight in zip(row_support, solution):
            for j, a in matrix['rows'][i]: remainder[j] -= weight * rat(a)
        assert all(value == 0 for j, value in enumerate(remainder) if old_residuals[j] == 0)
        x = [Q(c['weight']) for c in point['columns']]
        assert sum((Q(a) * v for a, v in zip(matrix['normalization'], x)), Q()) == 1
        for i in row_support: assert sum((rat(a) * x[j] for j, a in matrix['rows'][i]), Q()) == 0
        assert all(x[j] == 0 for j, value in enumerate(old_residuals) if value > 0)
        assert sum((value * x[j] for j, value in cut.items()), Q()) == alpha
        write('old_optimal_face_cut_identity.json', {
            'status': 'EXACT_SIGNED_IDENTITY', 'normalization_coefficient': str(alpha),
            'row_coefficients': [[i, str(v)] for i, v in zip(row_support, solution) if v],
            'zero_column_coefficients': [[j, str(v)] for j, v in enumerate(remainder) if v],
            'identity': 'compactcut = alpha * normalization + signed combination of old-positive-dual rows + signed combination of old-positive-residual columns',
            'all20585_coefficients_checked': True, 'whole_old_optimum_face_cut_value': str(alpha),
            'whole_old_optimum_face_excluded_by_compactcut': True,
            'rank': len(basis), 'unknowns': n, 'equations': len(equations),
            'source_sha256': {str(p.relative_to(WORK)): pin for p, pin in pins.items()},
            'optimizer_calls': 0, 'seconds': time.monotonic() - start,
            'scope': 'Whole old W9 optimum face only. New feasible optimum must exceed W9; no new optimum value or SPE claim.'})
        print(json.dumps({'status': 'EXACT_SIGNED_IDENTITY', 'whole_old_optimum_face_value': str(alpha), 'rank': len(basis), 'seconds': time.monotonic() - start}), flush=True)
    except BaseException:
        failure = {'status': 'SPAN_RECOVERY_FAILED', 'traceback': traceback.format_exc(), 'processed_equations': processed,
                   'rank': len(basis), 'unknowns': n, 'total_equations': len(equations), 'optimizer_calls': 0,
                   'seconds': time.monotonic() - start, 'failure_does_not_exclude_any_optimum_face': True}
        write('old_optimal_face_span_failure.json', failure)
        print(json.dumps(failure, ensure_ascii=False, indent=2), flush=True)
        raise


if __name__ == '__main__': main()
