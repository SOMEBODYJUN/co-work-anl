"""Exact AP39 whole-W10-face span test and, if possible, strict dual bound.

Only standard-library rational arithmetic is used. All 21021 coordinates
are retained. Positive-residual coordinates are eliminated only because
their independent signed coefficients are allowed in the requested
identity; no primal-support restriction or optimizer is used.

Run from any directory with Python 3. Existing outputs are never replaced.
An inconsistent span produces an exact annihilator and a normalization-
preserving algebraic direction. Such a direction is NOT asserted feasible.
"""
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import gzip
import json
import time

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
N = 21021
M = 22297
AP_INDEX = 39
EXPECTED_ALPHA = Q('-2387360308883849167939463658247160398139890481107232380975950684899327/167642800338353195761909644781419248132422636155436956133783540969055432')
PINS = {
    'maxb_augmented_lp/full_lift/exact_matrix.json.gz': 'c054aadf745ea4540233a3da693917498527d19d4ccecb0fdd34ad884e461e4b',
    'maxb_augmented_lp/full_lift/recovery/augmented_lp_exact.json': '5b1b649af5fc9d359e31dd03945d12708e599e0eeac75983ed188e60178b3bfe',
    'maxb_augmented_lp/full_lift/recovery/exact_dual_certificate.json': '4a6b6ca154ce645bcdabceb50bcb83982fead5875f257bf0a4c56f9576d7405f',
    'early_x_anchor_queries/rows_51.json': '0ad0b697193d7a8da2cc62275bbf9265912b0485d778d5edd93fc334bd8bb3eb',
}


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def read(path):
    with gzip.open(path, 'rt') if path.suffix == '.gz' else path.open() as f:
        return json.load(f)


@lru_cache(maxsize=None)
def q(value):
    return Q(value)


def write(name, data):
    path = HERE / name
    if path.exists():
        raise FileExistsError(path)
    if path.suffix == '.gz':
        with path.open('xb') as raw:
            with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) as compressed:
                compressed.write((json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n').encode())
    else:
        with path.open('x') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write('\n')


def sparse(values):
    return [[i, str(v)] for i, v in enumerate(values) if v]


def add_scaled(target, source, scale):
    for i, value in source.items():
        result = target.get(i, Q()) + scale * value
        if result:
            target[i] = result
        else:
            target.pop(i, None)


def annihilator(column, reductions, records):
    """Replay a failed equation's exact elimination recipe backwards."""
    witness = {column: Q(1)}
    pending = {}
    for pivot, factor in reductions:
        pending[pivot] = pending.get(pivot, Q()) - factor
    for record in reversed(records):
        pivot = record['pivot']
        coefficient = pending.pop(pivot, Q())
        if not coefficient:
            continue
        scale = coefficient / record['scale']
        add_scaled(witness, {record['column']: Q(1)}, scale)
        for previous, factor in record['reductions']:
            pending[previous] = pending.get(previous, Q()) - scale * factor
    assert not any(pending.values())
    return witness


def encode_trace(records):
    return [dict(pivot=r['pivot'], input_column=r['column'],
                 normalization_scale=str(r['scale']),
                 reductions=[[p, str(v)] for p, v in r['reductions']],
                 normalized_augmented_equation=[[k, str(v)] for k, v in sorted(r['row'].items())])
            for r in records]


def main():
    start = time.monotonic()
    for relative, expected in PINS.items():
        assert digest(WORK / relative) == expected, relative
    matrix = read(WORK / 'maxb_augmented_lp/full_lift/exact_matrix.json.gz')
    primal = read(WORK / 'maxb_augmented_lp/full_lift/recovery/augmented_lp_exact.json')
    dual = read(WORK / 'maxb_augmented_lp/full_lift/recovery/exact_dual_certificate.json')
    package = read(WORK / 'early_x_anchor_queries/rows_51.json')
    assert len(matrix['columns']) == len(matrix['objective']) == len(matrix['normalization']) == N
    assert len(matrix['rows']) == len(matrix['row_names']) == M
    assert len(primal['columns']) == N and len(dual['residuals']) == N
    ap = package['rows'][AP_INDEX]
    assert ap['name'] == ['common-X-early-arbitrary-anchor-AP', 3, 'A', 5]
    assert ap['C'] == '23' and ap['query_members'] == [['A', 5]]
    assert len(ap['row']) == 25 and all(j < 20601 for j, _ in ap['row'])
    assert package['base_matrix_sha256'] == PINS['maxb_augmented_lp/full_lift/exact_matrix.json.gz']
    cut = dict((j, q(value)) for j, value in ap['row'])
    assert len(cut) == 25
    x = [q(column['weight']) for column in primal['columns']]
    normalization = list(map(q, matrix['normalization']))
    old_residual = list(map(q, dual['residuals']))
    weights = dict((i, q(v)) for i, v in dual['row_multipliers'])
    support = sorted(weights)
    assert len(weights) == len(dual['row_multipliers']) == 463
    assert min(weights.values()) > 0 and min(old_residual) >= 0 and min(x) >= 0
    alpha = sum((value * x[j] for j, value in cut.items()), Q())
    assert alpha == EXPECTED_ALPHA < 0
    old_lower = q(dual['normalization_multiplier'])
    assert old_lower == q(primal['W'])
    assert sum((a * value for a, value in zip(normalization, x)), Q()) == 1
    assert all(x[j] == 0 for j, residual in enumerate(old_residual) if residual > 0)
    for i in support:
        assert sum((q(a) * x[j] for j, a in matrix['rows'][i]), Q()) == 0

    zero_residual = [j for j, value in enumerate(old_residual) if value == 0]
    positive_residual = [j for j, value in enumerate(old_residual) if value > 0]
    # The order affects sparsity only. Every zero-residual coordinate is checked.
    zero_residual.sort(key=lambda j: (0 if j >= 20601 else 1 if j >= 4849 else 2, j))
    n = len(support)
    column_equations = {j: {} for j in zero_residual}
    for k, i in enumerate(support):
        for j, value in matrix['rows'][i]:
            if j in column_equations:
                column_equations[j][k] = q(value)
    all_equations = []
    unique_equations = []
    zero_equations = []
    duplicates = []
    signatures = {}
    for j in zero_residual:
        equation = dict(column_equations[j])
        rhs = cut.get(j, Q()) - alpha * normalization[j]
        if rhs:
            equation[n] = rhs
        all_equations.append([j, [[k, str(v)] for k, v in sorted(equation.items())]])
        if not equation:
            zero_equations.append(j)
            continue
        scale = equation[min(equation)]
        signature = tuple((k, v / scale) for k, v in sorted(equation.items()))
        if signature in signatures:
            duplicates.append([j, signatures[signature], str(scale)])
        else:
            signatures[signature] = j
            unique_equations.append((j, equation))

    write('input_manifest.json', {
        'source_sha256': PINS,
        'source_bytes': {p: (WORK / p).stat().st_size for p in PINS},
        'builder_sha256': digest(Path(__file__)),
        'matrix_dimensions': [M, N], 'positive_dual_rows': support,
        'positive_residual_columns': positive_residual,
        'all_histogram_columns': [entry['hist_column'] for entry in ap['histogram_frequencies']],
        'all_six_original_zero_histograms_retained': package['all_zero_histograms_retained'],
        'selected_AP_row_index': AP_INDEX, 'selected_AP_row': ap,
        'old_W10': str(old_lower), 'AP39_at_verified_primal': str(alpha),
        'scope': 'Exact algebra on the complete fixed16-hist necessary LP; no optimizer or SPE claim.'
    })
    write('span_inputs.json.gz', {
        'unknown_row_indices': support, 'unknowns': n, 'rhs_index': n,
        'alpha': str(alpha), 'all_zero_residual_column_equations': all_equations,
        'equation_form': 'sum_k A[support[k],j]*beta[k] = C[j]-alpha*normalization[j]',
        'homogeneous_zero_equation_columns': zero_equations,
        'proportional_duplicate_columns': duplicates,
        'unique_equation_columns_in_order': [j for j, _ in unique_equations],
        'no_primal_support_restriction': True,
        'retained_column_count': N,
    })
    basis = {}
    records = []
    last_log = time.monotonic()
    failure = None
    for processed, (j, encoded) in enumerate(unique_equations, 1):
        row = dict(encoded)
        reductions = []
        while row:
            pivot = min(row)
            if pivot == n:
                failure = (j, row[n], reductions)
                break
            if pivot not in basis:
                scale = row[pivot]
                row = {k: value / scale for k, value in row.items()}
                basis[pivot] = row
                records.append(dict(pivot=pivot, column=j, scale=scale,
                                    reductions=reductions, row=row))
                break
            factor = row[pivot]
            reductions.append((pivot, factor))
            add_scaled(row, basis[pivot], -factor)
        if failure:
            break
        if time.monotonic() - last_log > 15:
            print(json.dumps(dict(event='exact_span_progress', processed=processed,
                                  total=len(unique_equations), rank=len(basis),
                                  seconds=time.monotonic() - start)), flush=True)
            last_log = time.monotonic()
    write('elimination_trace.json.gz', {
        'arithmetic': 'Python fractions.Fraction; exact rational Gaussian elimination',
        'basis': encode_trace(records), 'rank': len(basis),
        'processed_unique_equations': processed,
        'unique_equation_count': len(unique_equations),
        'optimizer_calls': 0,
    })

    if failure:
        column, contradiction, reductions = failure
        witness = annihilator(column, reductions, records)
        assert set(witness).issubset(zero_residual)
        for i in support:
            assert sum((q(a) * witness.get(j, Q()) for j, a in matrix['rows'][i]), Q()) == 0
        norm_w = sum((normalization[j] * value for j, value in witness.items()), Q())
        rhs_w = sum(((cut.get(j, Q()) - alpha * normalization[j]) * value for j, value in witness.items()), Q())
        assert rhs_w == contradiction != 0
        direction = [witness.get(j, Q()) - norm_w * x[j] for j in range(N)]
        assert sum((normalization[j] * direction[j] for j in range(N)), Q()) == 0
        assert all(direction[j] == 0 for j in positive_residual)
        for i in support:
            assert sum((q(a) * direction[j] for j, a in matrix['rows'][i]), Q()) == 0
        cut_change = sum((value * direction[j] for j, value in cut.items()), Q())
        assert cut_change == contradiction
        write('exact_span_obstruction.json', {
            'status': 'EXACT_NOT_IN_REQUESTED_SIGNED_SPAN',
            'failed_column': column, 'nonzero_contradiction': str(contradiction),
            'column_annihilator': [[j, str(v)] for j, v in sorted(witness.items())],
            'annihilator_normalization_value': str(norm_w),
            'normalization_preserving_algebraic_direction': sparse(direction),
            'AP39_directional_change': str(cut_change),
            'alpha': str(alpha), 'rank': len(basis), 'unknowns': n,
            'processed_unique_equations': processed,
            'failure_reductions': [[p, str(v)] for p, v in reductions],
            'whole_optimum_face_feasibility_not_decided': True,
            'direction_not_claimed_feasible': True,
            'strict_lower_bound_not_derived': True,
            'optimizer_calls': 0, 'seconds': time.monotonic() - start,
        })
        print(json.dumps(dict(status='EXACT_NOT_IN_REQUESTED_SIGNED_SPAN',
                              rank=len(basis), contradiction=str(contradiction),
                              witness_columns=len(witness), seconds=time.monotonic() - start)), flush=True)
        return

    solution = [Q()] * n
    for pivot in sorted(basis, reverse=True):
        row = basis[pivot]
        solution[pivot] = row.get(n, Q()) - sum((value * solution[k] for k, value in row.items() if pivot < k < n), Q())
    beta = {i: value for i, value in zip(support, solution) if value}
    delta = [cut.get(j, Q()) - alpha * normalization[j] for j in range(N)]
    for i, value in beta.items():
        for j, a in matrix['rows'][i]:
            delta[j] -= value * q(a)
    assert all(delta[j] == 0 for j in zero_residual)
    assert all(old_residual[j] > 0 for j, value in enumerate(delta) if value)
    write('signed_identity.json', {
        'status': 'EXACT_SIGNED_IDENTITY', 'normalization_coefficient': str(alpha),
        'row_coefficients': [[i, str(v)] for i, v in sorted(beta.items())],
        'positive_residual_column_coefficients': sparse(delta),
        'identity': 'AP39 = alpha*normalization + sum_i beta_i*A_i + sum_j delta_j*e_j',
        'all21021_coefficients_checked': True, 'whole_W10_optimum_face_AP39_value': str(alpha),
        'whole_W10_optimum_face_excluded_by_AP39': True,
        'positive_dual_rows_available': len(support), 'positive_residual_columns_available': len(positive_residual),
        'rank': len(basis), 'unknowns': n, 'free_variables_set_to_zero': sorted(set(range(n)) - set(basis)),
        'all_zero_residual_equations': len(zero_residual), 'unique_equations': len(unique_equations),
        'source_sha256': PINS, 'optimizer_calls': 0,
        'scope': 'Entire old W10 optimum face, independent of the displayed primal support.'
    })

    bounds = []
    for i, value in beta.items():
        if value > 0:
            bounds.append((weights[i] / value, 'row', i, weights[i], value))
    for j, value in enumerate(delta):
        if value > 0:
            bounds.append((old_residual[j] / value, 'column', j, old_residual[j], value))
    assert bounds
    step = min(value for value, *_ in bounds)
    assert step > 0
    lower = old_lower - step * alpha
    assert lower > old_lower
    new_weights = {i: weights.get(i, Q()) - step * beta.get(i, Q()) for i in range(M)}
    new_weights[M] = step
    assert min(new_weights.values()) >= 0
    residual = [q(c) - lower * a for c, a in zip(matrix['objective'], normalization)]
    for i, weight in new_weights.items():
        if not weight:
            continue
        row = matrix['rows'][i] if i < M else ap['row']
        for j, a in row:
            residual[j] -= weight * q(a)
    expected_residual = [value - step * d for value, d in zip(old_residual, delta)]
    assert residual == expected_residual and min(residual) >= 0
    write('augmented_system.json', {
        'base_matrix_path_relative_to_workspace': 'maxb_augmented_lp/full_lift/exact_matrix.json.gz',
        'base_matrix_sha256': PINS['maxb_augmented_lp/full_lift/exact_matrix.json.gz'],
        'construction': 'Append exactly this one homogeneous inequality to the complete frozen base; retain all objective, normalization and column descriptors.',
        'dimensions': [M + 1, N], 'appended_row_index': M,
        'appended_row_name': ap['name'], 'appended_row': ap['row'],
        'inequality': 'row_value >= 0', 'all_columns_nonnegative': True,
        'new_columns': 0, 'deleted_rows': [], 'deleted_columns': [],
        'AP_package_sha256': PINS['early_x_anchor_queries/rows_51.json'], 'AP_package_index': AP_INDEX,
    })
    write('strict_lower_certificate.json', {
        'status': 'EXACT_STRICT_DUAL_LOWER_BOUND', 'normalization_multiplier': str(lower),
        'row_multipliers': [[i, str(v)] for i, v in new_weights.items() if v],
        'all_row_multiplier_count': M + 1, 'omitted_row_multipliers': 'exactly zero',
        'residuals': list(map(str, residual)), 'residual_count': N,
        'minimum_row_multiplier_including_zeros': str(min(new_weights.values())),
        'minimum_coefficient_residual': str(min(residual)),
        'base_matrix_sha256': PINS['maxb_augmented_lp/full_lift/exact_matrix.json.gz'],
        'augmented_system_sha256': digest(HERE / 'augmented_system.json'),
        'identity': 'objective = lower*normalization + sum_i nonnegative_lambda_i*row_i + nonnegative_residual',
        'exact_optimum_claim': False, 'SPE_claim': False,
    })
    write('strict_lower_derivation.json', {
        'status': 'EXACT_STRICT_LOWER_BOUND', 'old_W10': str(old_lower), 'alpha': str(alpha),
        'step': str(step), 'step_float': float(step), 'new_lower': str(lower), 'new_lower_float': float(lower),
        'exact_improvement': str(lower - old_lower), 'improvement_float': float(lower - old_lower),
        'half_minus_lower': str(Q(1, 2) - lower),
        'step_definition': 'min({lambda_i/beta_i: beta_i>0} union {r_j/delta_j: delta_j>0})',
        'all_positive_ratio_bounds': [{'kind': kind, 'index': i, 'numerator': str(a), 'denominator': str(b), 'bound': str(v)} for v, kind, i, a, b in bounds],
        'tight_step_bounds': [{'kind': kind, 'index': i, 'bound': str(v)} for v, kind, i, a, b in bounds if v == step],
        'new_positive_row_multipliers': sum(v > 0 for v in new_weights.values()),
        'new_positive_residuals': sum(v > 0 for v in residual),
        'all22298_row_multipliers_nonnegative': True, 'all21021_residuals_nonnegative': True,
        'signed_identity_sha256': digest(HERE / 'signed_identity.json'),
        'strict_lower_certificate_sha256': digest(HERE / 'strict_lower_certificate.json'),
        'builder_sha256': digest(Path(__file__)), 'optimizer_calls': 0,
        'seconds': time.monotonic() - start,
        'scope': 'Strict necessary-LP lower bound only; no new exact optimum and no original six-player SPE conclusion.'
    })
    print(json.dumps(dict(status='EXACT_STRICT_LOWER_BOUND', rank=len(basis),
                          alpha=str(alpha), step=str(step), new_lower=str(lower),
                          new_lower_float=float(lower), improvement_float=float(lower-old_lower),
                          seconds=time.monotonic() - start)), flush=True)


if __name__ == '__main__':
    main()
