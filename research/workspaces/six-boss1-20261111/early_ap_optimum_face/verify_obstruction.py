"""Independent exact verification of the five-coordinate AP39 span obstruction.

No builder or elimination module is imported. Reconstructs AP39 from the
literal six-player histogram descriptors, checks the complete old primal
and dual, and directly annihilates every allowed generator. Also records
why an algebraic null direction must not be treated as a feasible direction.
Only the Python standard library is used; there are no optimizer calls.
"""
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from math import gcd, lcm
from pathlib import Path
import gzip
import json
import time

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
N = 21021
M = 22297
PINS = {
    'maxb_augmented_lp/full_lift/exact_matrix.json.gz': 'c054aadf745ea4540233a3da693917498527d19d4ccecb0fdd34ad884e461e4b',
    'maxb_augmented_lp/full_lift/recovery/augmented_lp_exact.json': '5b1b649af5fc9d359e31dd03945d12708e599e0eeac75983ed188e60178b3bfe',
    'maxb_augmented_lp/full_lift/recovery/exact_dual_certificate.json': '4a6b6ca154ce645bcdabceb50bcb83982fead5875f257bf0a4c56f9576d7405f',
    'early_x_anchor_queries/rows_51.json': '0ad0b697193d7a8da2cc62275bbf9265912b0485d778d5edd93fc334bd8bb3eb',
}


def sha(path):
    return sha256(path.read_bytes()).hexdigest()


def read(path):
    with gzip.open(path, 'rt') if path.suffix == '.gz' else path.open() as stream:
        return json.load(stream)


def write(name, obj):
    path = HERE / name
    if path.exists():
        raise FileExistsError(path)
    if path.suffix == '.gz':
        with path.open('xb') as raw:
            with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) as compressed:
                compressed.write((json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + '\n').encode())
    else:
        with path.open('x') as stream:
            json.dump(obj, stream, ensure_ascii=False, indent=2)
            stream.write('\n')


@lru_cache(maxsize=None)
def frac(value):
    return F(value)


def main():
    started = time.monotonic()
    for name, expected in PINS.items():
        assert sha(WORK / name) == expected
    matrix = read(WORK / 'maxb_augmented_lp/full_lift/exact_matrix.json.gz')
    primal = read(WORK / 'maxb_augmented_lp/full_lift/recovery/augmented_lp_exact.json')
    dual = read(WORK / 'maxb_augmented_lp/full_lift/recovery/exact_dual_certificate.json')
    package = read(WORK / 'early_x_anchor_queries/rows_51.json')
    obstruction = read(HERE / 'exact_span_obstruction.json')
    inputs = read(HERE / 'input_manifest.json')
    assert inputs['source_sha256'] == PINS
    assert len(matrix['rows']) == len(matrix['row_names']) == M
    assert len(matrix['columns']) == len(primal['columns']) == len(dual['residuals']) == N
    assert matrix['all_columns_nonnegative'] is True
    x = list(map(lambda c: frac(c['weight']), primal['columns']))
    assert min(x) >= 0
    for descriptor, weighted in zip(matrix['columns'], primal['columns']):
        assert descriptor == {k: v for k, v in weighted.items() if k != 'weight'}
    normal = list(map(frac, matrix['normalization']))
    objective = list(map(frac, matrix['objective']))
    assert len(normal) == len(objective) == N
    assert sum((a * b for a, b in zip(normal, x)), F()) == 1
    old_W = sum((a * b for a, b in zip(objective, x)), F())
    assert old_W == frac(primal['W']) == frac(dual['normalization_multiplier'])

    # Literal AP39 reconstruction, independent of its saved sparse coefficients.
    histogram_indices = [i for i, c in enumerate(matrix['columns']) if c['kind'] == 'hist']
    common_X_indices = [i for i, c in enumerate(matrix['columns']) if c['kind'] == 'common-X-mass']
    assert len(histogram_indices) == len(common_X_indices) == 16
    rebuilt = [F()] * N
    for j in histogram_indices:
        bits = list(map(int, matrix['columns'][j]['actual_bits']))
        assert len(bits) == 6
        b = bits[0] + bits[1]
        if bits[2]:
            rebuilt[j] += F(23, sum(bits))
        if bits[5]:
            rebuilt[j] -= F(1, b + 1)
    for j in common_X_indices:
        h = matrix['columns'][j]['hist_column']
        assert h in histogram_indices
        bits = list(map(int, matrix['columns'][h]['actual_bits']))
        b = bits[0] + bits[1]
        rebuilt[j] = -F(22, b + 4) + bits[5] * F(3, (b + 1) * (b + 4))
    row = package['rows'][39]
    assert row['name'] == ['common-X-early-arbitrary-anchor-AP', 3, 'A', 5]
    saved_cut = [F()] * N
    for j, value in row['row']:
        assert saved_cut[j] == 0
        saved_cut[j] = frac(value)
    assert rebuilt == saved_cut
    assert sum(v != 0 for v in rebuilt) == 25
    assert all(rebuilt[j] == 0 for j in range(20601, N))
    alpha = sum((a * b for a, b in zip(rebuilt, x)), F())
    assert alpha == frac(obstruction['alpha']) == frac(inputs['AP39_at_verified_primal']) < 0

    annihilator = {j: frac(v) for j, v in obstruction['column_annihilator']}
    assert len(annihilator) == len(obstruction['column_annihilator']) == 5
    denominator = lcm(*(v.denominator for v in annihilator.values()))
    ints = {j: int(v * denominator) for j, v in annihilator.items()}
    divisor = gcd(*ints.values())
    primitive = {j: F(v // divisor) for j, v in ints.items()}
    if sum((rebuilt[j] * v for j, v in primitive.items()), F()) < 0:
        primitive = {j: -v for j, v in primitive.items()}
    assert primitive == {20585: F(1), 20590: F(4), 20592: F(-12), 20594: F(-3), 20598: F(10)}
    direction = [primitive.get(j, F()) for j in range(N)]
    assert sum((a * b for a, b in zip(normal, direction)), F()) == 0
    assert sum((a * b for a, b in zip(objective, direction)), F()) == 0
    change = sum((a * b for a, b in zip(rebuilt, direction)), F())
    assert change == 5
    assert sum((normal[j] * v for j, v in annihilator.items()), F()) == frac(obstruction['annihilator_normalization_value']) == 0
    assert sum((rebuilt[j] * v for j, v in annihilator.items()), F()) == frac(obstruction['nonzero_contradiction']) == F(1, 2)
    assert {j: frac(v) for j, v in obstruction['normalization_preserving_algebraic_direction']} == annihilator

    # Recompute every old primal row and, separately, every old dual column.
    row_slacks = []
    row_direction_values = []
    for encoded in matrix['rows']:
        seen = set()
        slack = F()
        derivative = F()
        for j, text in encoded:
            assert 0 <= j < N and j not in seen
            seen.add(j)
            a = frac(text)
            if x[j]:
                slack += a * x[j]
            if j in primitive:
                derivative += a * primitive[j]
        row_slacks.append(slack)
        row_direction_values.append(derivative)
    assert len(row_slacks) == M and min(row_slacks) >= 0
    lam = {}
    residual = [a - old_W * b for a, b in zip(objective, normal)]
    for i, text in dual['row_multipliers']:
        value = frac(text)
        assert 0 <= i < M and i not in lam and value > 0
        lam[i] = value
        for j, a in matrix['rows'][i]:
            residual[j] -= value * frac(a)
    assert len(lam) == 463
    assert residual == list(map(frac, dual['residuals'])) and min(residual) >= 0
    assert len(residual) == N
    positive_residual = [j for j, value in enumerate(residual) if value > 0]
    assert len(positive_residual) == 5379
    assert all(row_slacks[i] == 0 for i in lam)
    assert all(row_direction_values[i] == 0 for i in lam)
    assert all(x[j] == 0 and direction[j] == 0 for j in positive_residual)
    assert sorted(lam) == inputs['positive_dual_rows']
    assert positive_residual == inputs['positive_residual_columns']

    # The span certificate is already complete: d annihilates every allowed
    # generator but not C. Check the saved full equation interface as well.
    span = read(HERE / 'span_inputs.json.gz')
    assert span['unknown_row_indices'] == sorted(lam) and span['unknowns'] == 463
    eqs = span['all_zero_residual_column_equations']
    assert len(eqs) == 15642
    zero_indices = {j for j, value in enumerate(residual) if value == 0}
    assert {j for j, _ in eqs} == zero_indices
    column_map = {j: {} for j in zero_indices}
    for k, i in enumerate(sorted(lam)):
        for j, text in matrix['rows'][i]:
            if j in column_map:
                column_map[j][k] = frac(text)
    encoded_eqs = {}
    for j, encoded in eqs:
        expected = dict(column_map[j])
        rhs = rebuilt[j] - alpha * normal[j]
        if rhs:
            expected[463] = rhs
        actual = {k: frac(v) for k, v in encoded}
        assert actual == expected
        encoded_eqs[j] = actual
    trace = read(HERE / 'elimination_trace.json.gz')
    previous_basis = {}
    for record in trace['basis']:
        current = dict(encoded_eqs[record['input_column']])
        for pivot, text in record['reductions']:
            scale = frac(text)
            assert current[pivot] == scale and pivot in previous_basis
            for k, value in previous_basis[pivot].items():
                result = current.get(k, F()) - scale * value
                if result:
                    current[k] = result
                else:
                    current.pop(k, None)
        p = record['pivot']
        assert p not in previous_basis and p == min(current)
        scale = frac(record['normalization_scale'])
        assert current[p] == scale
        normalized = {k: value / scale for k, value in current.items()}
        assert normalized == {k: frac(v) for k, v in record['normalized_augmented_equation']}
        previous_basis[p] = normalized
    assert len(previous_basis) == trace['rank'] == obstruction['rank'] == 280
    final = dict(encoded_eqs[obstruction['failed_column']])
    for pivot, text in obstruction['failure_reductions']:
        scale = frac(text)
        assert final[pivot] == scale
        for k, value in previous_basis[pivot].items():
            result = final.get(k, F()) - scale * value
            if result:
                final[k] = result
            else:
                final.pop(k, None)
    assert final == {463: F(1, 2)}

    # Record blockers only to prevent an incorrect feasible-face inference.
    positive_row_blockers = [i for i in range(M) if row_slacks[i] == 0 and row_direction_values[i] < 0]
    negative_column_blockers = [j for j, value in primitive.items() if value > 0 and x[j] == 0]
    assert positive_row_blockers and negative_column_blockers
    hist_zero = [1, 59, 366, 449, 524, 574]
    assert all(j in histogram_indices for j in hist_zero)
    zero_hist_mass = [{'column': j, 'weight': str(x[j])} for j in hist_zero]
    direction_columns = []
    for j, value in primitive.items():
        hist_j = matrix['columns'][j]['hist_column']
        direction_columns.append({'column': j, 'coefficient': str(value),
                                  'descriptor': matrix['columns'][j],
                                  'histogram_descriptor': matrix['columns'][hist_j],
                                  'primal_weight': str(x[j]),
                                  'old_dual_residual': str(residual[j]),
                                  'AP39_coefficient': str(rebuilt[j]),
                                  'AP39_directional_term': str(rebuilt[j] * value)})
    write('primitive_obstruction.json', {
        'status': 'EXACT_SPAN_OBSTRUCTION', 'dimension': N,
        'direction': [[j, str(v)] for j, v in primitive.items()],
        'column_details': direction_columns,
        'normalization_dot_direction': '0', 'objective_dot_direction': '0',
        'all463_positive_dual_row_dot_products': [[i, str(row_direction_values[i])] for i in sorted(lam)],
        'positive_residual_column_support_intersection': [],
        'all5379_positive_residual_coordinate_generators_annihilated': True,
        'AP39_dot_direction': '5',
        'not_in_signed_span_even_with_arbitrary_alpha': True,
        'positive_direction_tight_row_blockers': [
            {'row_index': i, 'row_name': matrix['row_names'][i],
             'row': matrix['rows'][i], 'primal_slack': str(row_slacks[i]),
             'directional_change': str(row_direction_values[i]),
             'old_dual_multiplier': str(lam.get(i, F()))}
            for i in positive_row_blockers],
        'negative_direction_nonnegativity_blockers': [
            {'column': j, 'primal_weight': str(x[j]), 'minus_direction_value': str(-primitive[j])}
            for j in negative_column_blockers],
        'neither_sign_is_a_feasible_direction_at_the_displayed_primal': True,
        'whole_optimum_face_AP39_feasibility': 'NOT_DECIDED',
        'new_strict_lower_bound': 'NOT_DERIVED',
        'source_sha256': PINS,
    })
    write('independent_full_checks.json.gz', {
        'old_primal_row_slacks_all22297': list(map(str, row_slacks)),
        'old_dual_residuals_all21021': list(map(str, residual)),
        'primitive_direction_all21021': list(map(str, direction)),
        'all22297_row_directional_derivatives': list(map(str, row_direction_values)),
        'independently_rebuilt_AP39_all21021': list(map(str, rebuilt)),
        'histogram_indices_all16': histogram_indices,
        'zero_histogram_masses': zero_hist_mass,
        'source_sha256': PINS,
    })
    audit = {
        'status': 'PASS_EXACT_REQUESTED_SPAN_OBSTRUCTION',
        'matrix_dimensions': [M, N],
        'source_sha256': PINS,
        'old_primal_rows_independently_checked': M,
        'old_dual_columns_independently_checked': N,
        'primal_column_descriptors_compared': N,
        'AP39_literal_formula_columns_checked': N,
        'all16_histograms_retained': True, 'all_six_zero_histogram_columns_retained': hist_zero,
        'old_W10': str(old_W), 'old_W10_float': float(old_W),
        'AP39_at_primal': str(alpha), 'AP39_at_primal_float': float(alpha),
        'positive_dual_row_generators_annihilated': len(lam),
        'positive_residual_coordinate_generators_annihilated': len(positive_residual),
        'normalization_annihilated': True, 'objective_annihilated': True,
        'primitive_obstruction_columns': len(primitive), 'AP39_dot_primitive_direction': str(change),
        'all15642_zero_residual_equations_rebuilt': True,
        'saved_elimination_basis_replayed': 280,
        'exact_inconsistent_equation': '0 = 1/2',
        'requested_signed_identity_impossible_for_every_alpha': True,
        'algebraic_direction_not_a_feasible_direction_at_given_primal': True,
        'positive_direction_tight_row_blocker_count': len(positive_row_blockers),
        'negative_direction_nonnegative_column_blocker_count': len(negative_column_blockers),
        'whole_W10_optimum_face_excluded_by_AP39': 'NOT_DECIDED',
        'AP39_satisfying_point_on_whole_W10_optimum_face': 'NOT_ESTABLISHED',
        'strictly_larger_necessary_LP_bound': 'NOT_DERIVED',
        'exact_new_optimum_claim': False, 'SPE_claim': False, 'optimizer_calls': 0,
        'obstruction_sha256': sha(HERE / 'exact_span_obstruction.json'),
        'primitive_obstruction_sha256': sha(HERE / 'primitive_obstruction.json'),
        'verifier_sha256': sha(Path(__file__)),
        'seconds': time.monotonic() - started,
        'scope': 'Failure of the specified complementary-slackness generator span only; no conclusion about feasibility after adding AP39.'
    }
    write('independent_audit.json', audit)
    print(json.dumps(audit, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    main()
