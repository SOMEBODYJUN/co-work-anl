"""Exact primal/dual recovery after Main returns one frozen cloud discovery.

All 10277 potential core coordinates include the 420 real common-X overlaps.
Only old columns 4849..15592 are eliminated and canonically recomputed.
No optimizer, NumPy, SciPy, network, Git, or source-matrix generation import.
"""
from collections import defaultdict
from fractions import Fraction as F
import math
import os
import sys
import time
import traceback
from recovery_model import HERE, ORIGINAL, AUX_END, SHARED_END, X_END, TOTAL, digest, read, write, log, frac, dot, load_npz


def sparse_affine_solve(equations, n, seed, label):
    basis = {}; started = time.monotonic(); last = started; largest = 0
    limit = float(os.environ.get('COMMON_X_EXACT_TIME_LIMIT', '600')); assert 0 < limit <= 7200
    for processed, encoded in enumerate(equations, 1):
        row = {j: v for j, v in encoded.items() if v}
        while row:
            pivot = min(row)
            if pivot == n: raise AssertionError(('inconsistent_exact_equations', label, processed, str(row[n])))
            if pivot not in basis:
                scale = row[pivot]; basis[pivot] = {j: v/scale for j, v in row.items()}; largest = max(largest, len(row)); break
            scale = row[pivot]
            for j, v in basis[pivot].items():
                value = row.get(j, F()) - scale*v
                if value: row[j] = value
                else: row.pop(j, None)
        now = time.monotonic()
        if now - last > 15:
            log('exact_elimination_progress', label=label, equations=processed, rank=len(basis), variables=n, seconds=now-started); last=now
        if now - started > limit: raise TimeoutError(('exact_elimination_local_limit', label, processed, len(basis), n))
    free = sorted(set(range(n)) - set(basis)); result = [F()] * n
    for j in free: result[j] = F(seed[j]).limit_denominator(10**12)
    for pivot in sorted(basis, reverse=True):
        row = basis[pivot]
        result[pivot] = row.get(n, F()) - sum((v*result[j] for j, v in row.items() if pivot < j < n), F())
    return result, {'variables': n, 'rank': len(basis), 'processed_equations': len(equations),
        'largest_sparse_basis_row': largest, 'free_variables': free, 'free_values': [[j, str(result[j])] for j in free],
        'elimination_seconds': time.monotonic()-started, 'elimination_time_limit': limit}


def load():
    binding = read(HERE/'recovery_input_manifest.json')
    assert binding['eligible_for_standard_recovery'] is True
    for name, pin in binding['recovery_inputs'].items(): assert digest(HERE/name) == pin, name
    matrix = read(HERE/'exact_matrix.json.gz'); structure = read(HERE/'coordinate_structure.json')
    arrays, shapes = load_npz(HERE/'floating_solver_arrays.npz')
    m = len(matrix['rows']); assert arrays['shape'] == structure['shape'] == [m, TOTAL]
    assert len(matrix['columns']) == TOTAL
    assert structure['core_columns'] == list(range(ORIGINAL)) + list(range(AUX_END, TOTAL))
    assert structure['real_overlap_columns'] == structure['forbidden_canonical_min_columns'] == list(range(X_END, TOTAL))
    assert structure['auxiliary_columns'] == list(range(ORIGINAL, AUX_END))
    assert arrays['optimizer_calls'] == [1] and arrays['solver_success'] == [True] and arrays['availability'] == [1, 1, 1, 1]
    for key, size in [('primal', TOTAL), ('inequality_marginals', m), ('scales', m), ('lower_marginals', TOTAL)]:
        assert shapes[key] == (size,) and all(math.isfinite(v) for v in arrays[key])
    assert all(v > 0 for v in arrays['scales'])
    assert structure['matrix_sha256'] == digest(HERE/'exact_matrix.json.gz')
    return matrix, structure, arrays


def canonical_old(matrix, values, structure, floating=False):
    before = [values[j] for j in structure['real_overlap_columns']]
    number = (lambda value: float(frac(value))) if floating else frac; zero = 0.0 if floating else F()
    def expr(i): return sum((number(v)*values[k] for k, v in matrix['rows'][i] if k < ORIGINAL), zero)
    touched = set()
    for j, i in structure['max_thresholds']:
        assert ORIGINAL <= j < AUX_END; values[j] = max(zero, -expr(i)); touched.add(j)
    for record in structure['min_auxiliaries']:
        j = record['column']; assert ORIGINAL <= j < AUX_END and j not in touched
        values[j] = min(expr(record['q_upper_row']), expr(record['v_upper_row'])); touched.add(j)
    assert touched == set(structure['auxiliary_columns'])
    assert before == [values[j] for j in structure['real_overlap_columns']]


def primal(attempt):
    started = time.monotonic(); matrix, structure, floats = load(); rows = matrix['rows']
    obj = list(map(F, matrix['objective'])); norm = list(map(F, matrix['normalization']))
    numerical = list(floats['primal']); canonical_old(matrix, numerical, structure, True)
    potential_core = set(structure['core_columns']); auxiliaries = set(structure['auxiliary_columns'])
    support = [j for j in list(range(AUX_END, TOTAL)) + list(range(ORIGINAL)) if numerical[j] > 1e-11]
    assert set(support).issubset(potential_core) and not set(support).intersection(auxiliaries)
    local = {j: k for k, j in enumerate(support)}; seed = [numerical[j] for j in support]
    equations = []; descriptions = []; seen = set(); representation = {}
    def restrict_original(encoded, sign=1):
        return {local[j]: sign*frac(v) for j, v in encoded if j in local and j < ORIGINAL}
    def add(eq, description, forced=False):
        eq = {j: v for j, v in eq.items() if v}
        if not eq: return
        if not forced:
            scale = max(abs(float(v)) for v in eq.values())
            slack = sum(float(v)*seed[j] for j, v in eq.items())
            if abs(slack) > 1e-10*scale: return
        pivot = min(eq); factor = eq[pivot]; signature = tuple((j, v/factor) for j, v in sorted(eq.items()))
        if signature in seen: return
        seen.add(signature); equations.append(eq); descriptions.append(description)
    def project(encoded):
        result = defaultdict(F)
        for j, text in encoded:
            v = frac(text)
            if j in local: result[local[j]] += v
            elif j in representation:
                assert j in auxiliaries
                for k, a in representation[j].items(): result[k] += v*a
            else: assert j in potential_core and j not in local, ('unclassified_column', j)
        return {j: v for j, v in result.items() if v}
    equality_rows = structure['shared624_equality_positive_rows'] + structure['B4_equality_positive_rows']
    for i in equality_rows:
        add({local[j]: frac(v) for j, v in rows[i] if j in local}, {'kind': 'exact_old_mass_equality', 'row': i}, True)
    for j, i in structure['max_thresholds']:
        hinge = restrict_original(rows[i], -1); representation[j] = hinge if numerical[j] > 1e-12 else {}
        add(hinge, {'kind': 'canonical_old_max_zero', 'auxiliary': j, 'threshold_row': i})
    for record in structure['min_auxiliaries']:
        q = restrict_original(rows[record['q_upper_row']]); v = restrict_original(rows[record['v_upper_row']])
        qn = sum(float(a)*seed[k] for k, a in q.items()); vn = sum(float(a)*seed[k] for k, a in v.items())
        representation[record['column']] = q if qn <= vn else v
        difference = defaultdict(F, q)
        for k, a in v.items(): difference[k] -= a
        add(dict(difference), {'kind': 'canonical_old_min_tie', 'auxiliary': record['column']})
    assert set(representation) == auxiliaries and not set(representation).intersection(structure['real_overlap_columns'])
    skipped = {i for j, i in structure['max_thresholds']} | set(structure['min_upper_rows'])
    skipped |= {k for i in equality_rows for k in (i, i+1)}
    multiplier = [-v/s for v, s in zip(floats['inequality_marginals'], floats['scales'])]
    order = sorted((i for i in range(len(rows)) if i not in skipped), key=lambda i: (multiplier[i] < 1e-10, -multiplier[i], i))
    for i in order: add(project(rows[i]), {'kind': 'projected_full_row', 'row': i, 'numerical_dual_weight': multiplier[i]})
    equation = {local[j]: norm[j] for j in support if norm[j]}; equation[len(support)] = F(1)
    add(equation, {'kind': 'normalization'}, True)
    inherited = read(HERE/'inherited_dual_lower_bound.json'); oldW = F(inherited['normalization_multiplier'])
    if attempt == 'sameW':
        equation = {local[j]: obj[j] for j in support if obj[j]}; equation[len(support)] = oldW
        add(equation, {'kind': 'fixed_old_exact_W', 'W': str(oldW)}, True)
    write('primal_'+attempt+'_recovery_inputs.json', {
        'input_sha256': {name: digest(HERE/name) for name in ('exact_matrix.json.gz', 'floating_solver_arrays.npz', 'coordinate_structure.json', 'recover.py', 'recovery_model.py')},
        'attempt': attempt, 'support': support, 'unknowns': len(support), 'potential_core_count': len(potential_core),
        'potential_core_columns': structure['core_columns'], 'forbidden_canonical_min_columns': structure['real_overlap_columns'],
        'positive_original_unknowns': sum(j < ORIGINAL for j in support),
        'positive_shared624_unknowns': sum(AUX_END <= j < SHARED_END for j in support),
        'positive_X_mass_unknowns': sum(SHARED_END <= j < X_END for j in support),
        'positive_real_overlap_unknowns': sum(X_END <= j < TOTAL for j in support),
        'selected_equations': [[[j, str(v)] for j, v in sorted(eq.items())] for eq in equations],
        'descriptions': descriptions, 'mass_equality_pairs_forced': len(equality_rows),
        'canonical_old_auxiliaries': 10744, 'canonical_real_overlap_auxiliaries': 0,
        'optimizer_calls': 0, 'support_threshold': 1e-11, 'active_equation_threshold': 1e-10})
    log('exact_primal_recovery_started', attempt=attempt, variables=len(support), equations=len(equations), positive_real_y=sum(j >= X_END for j in support))
    answer, recovery = sparse_affine_solve(equations, len(support), seed, 'primal_'+attempt)
    full = [F()] * TOTAL
    for j, v in zip(support, answer): full[j] = v
    assert min(full) >= 0, ('negative_core_mass', full.index(min(full)), str(min(full)))
    raw_core = [[j, str(full[j])] for j in structure['core_columns']]
    canonical_old(matrix, full, structure)
    assert raw_core == [[j, str(full[j])] for j in structure['core_columns']]
    assert min(full) >= 0 and sum((a*b for a, b in zip(norm, full)), F()) == 1
    slacks = [dot(row, full) for row in rows]
    assert min(slacks) >= 0, ('negative_exact_row_slack', slacks.index(min(slacks)), str(min(slacks)), float(min(slacks)))
    W = sum((a*b for a, b in zip(obj, full)), F()); assert W >= oldW
    if attempt == 'sameW': assert W == oldW
    recovery.update(support=support, attempt=attempt, seconds=time.monotonic()-started,
        core_solution_before_auxiliary_completion=raw_core,
        method='All 420 real overlaps are core unknowns; only 7954 old max and 2790 old min auxiliaries are recomputed.')
    write('augmented_lp_exact.json', {'scope': 'Exact finite common-X necessary LP point with 210 local own completions; no SPE sufficiency.',
        'O': '1', 'W': str(W), 'W_float': float(W), 'strict_half_gap': str(1-2*W),
        'verified_rows': len(rows), 'minimum_slack': str(min(slacks)), 'exact_verified': True,
        'core_columns': 10277, 'canonical_auxiliary_columns': 10744, 'positive_columns': sum(v > 0 for v in full),
        'columns': [{**c, 'weight': str(v)} for c, v in zip(matrix['columns'], full)]})
    write('primal_exact_audit.json', {'W': str(W), 'W_float': float(W), 'old_W': str(oldW), 'exact_increase': str(W-oldW),
        'row_slacks': list(map(str, slacks)), 'minimum_slack': str(min(slacks)), 'recovery': recovery})
    if W == oldW:
        write('exact_dual_certificate.json', {**inherited, 'equality_to_new_primal': True,
            'recovery': {'method': 'Unchanged old exact dual with zero multipliers on every appended row.'}})
    log('exact_primal_saved', W=str(W), W_float=float(W), exact_increase=str(W-oldW), rank=recovery['rank'], free=len(recovery['free_variables']))


def dual():
    started = time.monotonic(); matrix, structure, floats = load(); rows = matrix['rows']
    point = read(HERE/'augmented_lp_exact.json'); full = [F(c['weight']) for c in point['columns']]
    W = F(point['W']); slacks = [dot(row, full) for row in rows]; assert min(slacks) >= 0 and min(full) >= 0
    numerical = [-v/s for v, s in zip(floats['inequality_marginals'], floats['scales'])]
    simple = {i for j, i in structure['max_thresholds']} | set(structure['min_upper_rows'])
    mass_rows = {i for r in structure['shared624_equality_positive_rows'] + structure['B4_equality_positive_rows'] for i in (r, r+1)}
    keep = [i for i, v in enumerate(numerical) if v > 1e-12 and slacks[i] == 0]
    keep.sort(key=lambda i: (0 if i in mass_rows else 1 if i in simple else 2, i))
    local = {i: k for k, i in enumerate(keep)}; n = len(keep)+1; lower_index = n-1; rhs_index = n
    obj = list(map(F, matrix['objective'])); norm = list(map(F, matrix['normalization']))
    cols = [j for j, v in enumerate(full) if v > 0 or abs(floats['lower_marginals'][j]) < 1e-12]
    aux = set(structure['auxiliary_columns'])
    cols.sort(key=lambda j: (0 if j in aux else 1 if j >= X_END else 2 if j >= AUX_END else 3, j))
    trans = {j: {} for j in cols}
    for i in keep:
        for j, v in rows[i]:
            if j in trans: trans[j][local[i]] = frac(v)
    equations = []; descriptions = []; seen = set()
    for j in cols:
        eq = trans[j]
        if norm[j]: eq[lower_index] = norm[j]
        if obj[j]: eq[rhs_index] = obj[j]
        if not eq: continue
        signature = tuple(sorted(eq.items()))
        if signature in seen: continue
        seen.add(signature); equations.append(eq); descriptions.append(j)
    equations.append({lower_index: F(1), rhs_index: W})
    write('dual_recovery_inputs.json', {'sha256': {name: digest(HERE/name) for name in ('recover.py', 'recovery_model.py',
        'exact_matrix.json.gz', 'floating_solver_arrays.npz', 'augmented_lp_exact.json', 'primal_exact_audit.json')},
        'support_rows': keep, 'zero_residual_columns': cols, 'equation_columns': descriptions,
        'candidate_row_threshold': 1e-12, 'zero_reduced_cost_threshold': 1e-12,
        'exact_positive_slack_rows_removed': True, 'optimizer_calls': 0})
    log('exact_dual_recovery_started', variables=n, equations=len(equations), rows=len(keep), columns=len(cols))
    answer, recovery = sparse_affine_solve(equations, n, [numerical[i] for i in keep]+[float(W)], 'dual')
    multipliers, lower = answer[:-1], answer[-1]; assert min(multipliers) >= 0 and lower == W
    residual = [c-lower*a for c, a in zip(obj, norm)]
    for i, weight in zip(keep, multipliers):
        assert weight*slacks[i] == 0
        for j, v in rows[i]: residual[j] -= weight*frac(v)
    assert min(residual) >= 0, ('negative_dual_residual', residual.index(min(residual)), str(min(residual)))
    assert all(a*b == 0 for a, b in zip(residual, full))
    recovery.update(support_rows=keep, zero_residual_column_indices=cols,
        method='Exact sparse elimination on one cloud candidate, then all-column residual and complementarity checks.')
    write('exact_dual_certificate.json', {'verified': True, 'normalization_multiplier': str(lower),
        'row_multipliers': [[i, str(w)] for i, w in zip(keep, multipliers) if w],
        'minimum_coefficient_residual': str(min(residual)), 'residuals': list(map(str, residual)),
        'equality_to_new_primal': True, 'identity': 'objective = lower * normalization + sum_i lambda_i row_i + nonnegative residual',
        'recovery': recovery, 'matrix_sha256': digest(HERE/'exact_matrix.json.gz'), 'seconds': time.monotonic()-started})
    log('exact_dual_saved', W=str(W), W_float=float(W), positive_rows=sum(v > 0 for v in multipliers), rank=recovery['rank'])


if __name__ == '__main__':
    assert len(sys.argv) == 2 and sys.argv[1] in ('sameW', 'freeW', 'dual')
    attempt = sys.argv[1]
    try:
        if attempt == 'dual': dual()
        else: primal(attempt)
    except BaseException:
        write('recovery_'+attempt+'_failure.json', {'attempt': attempt, 'traceback': traceback.format_exc(),
              'optimizer_calls': 0, 'failure_is_not_an_infeasibility_certificate': True})
        raise
