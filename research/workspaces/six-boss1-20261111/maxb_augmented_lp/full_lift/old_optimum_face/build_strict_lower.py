"""Convert the exact whole-face identity into an explicit improved dual.

Only a finite rational minimum of sign-preserving step bounds is used.
No numerical optimizer is imported or called. The common-X Farkas rows
provide a valid full22297/21021 certificate, not just a compact-row bound.
"""
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import gzip
import json
import time

HERE = Path(__file__).resolve().parent
FULL = HERE.parent
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
    assert sha(BASE / 'exact_dual_certificate.json') == '22381bc9844aa5452b45a5bd8ef4a6148808388455b80666b49475df0f7377b3'
    assert sha(FULL / 'exact_matrix.json.gz') == 'c054aadf745ea4540233a3da693917498527d19d4ccecb0fdd34ad884e461e4b'
    identity = read(HERE / 'old_optimal_face_cut_identity.json')
    old = read(BASE / 'exact_dual_certificate.json'); projection = read(FULL / 'full_coordinate_farkas_projection.json')
    alpha = Q(identity['normalization_coefficient']); assert alpha < 0
    beta = {i: Q(v) for i, v in identity['row_coefficients']}
    delta = {j: Q(v) for j, v in identity['zero_column_coefficients']}
    lam = {i: Q(v) for i, v in old['row_multipliers']}
    old_r = list(map(Q, old['residuals'])); old_lower = Q(old['normalization_multiplier'])
    bounds = []
    for i, value in beta.items():
        assert i in lam and lam[i] > 0
        if value > 0: bounds.append((lam[i] / value, 'row', i))
    for j, value in delta.items():
        assert old_r[j] > 0
        if value > 0: bounds.append((old_r[j] / value, 'column', j))
    assert bounds
    step = min(value for value, kind, index in bounds); assert step > 0
    multiplier = {i: value - step * beta.get(i, Q()) for i, value in lam.items()}
    for i, value in projection['new_row_multipliers']:
        assert i not in multiplier and 20910 <= i < 22297
        multiplier[i] = step * Q(value) / 3
    assert min(multiplier.values()) >= 0
    lower = old_lower - step * alpha; assert lower > old_lower
    matrix = read(FULL / 'exact_matrix.json.gz')
    residual = [Q(c) - lower * Q(a) for c, a in zip(matrix['objective'], matrix['normalization'])]
    for i, weight in multiplier.items():
        for j, value in matrix['rows'][i]: residual[j] -= weight * rat(value)
    expected = [value - step * delta.get(j, Q()) for j, value in enumerate(old_r)] + [Q()] * 436
    for j, value in projection['new_nonnegativity_multipliers']: expected[j] += step * Q(value) / 3
    assert residual == expected and min(residual) >= 0 and len(residual) == 21021
    write('strict_lower_bound_certificate.json', {
        'verified': True, 'normalization_multiplier': str(lower),
        'row_multipliers': [[i, str(v)] for i, v in sorted(multiplier.items()) if v],
        'residuals': list(map(str, residual)), 'minimum_coefficient_residual': str(min(residual)),
        'matrix_sha256': sha(FULL / 'exact_matrix.json.gz'),
        'identity': 'objective = lower * normalization + sum_i lambda_i row_i + nonnegative residual',
        'equality_to_primal': False, 'exact_optimality_claim': False,
        'scope': 'Strict rational lower bound for the full common-X fixed16-hist necessary LP, not an exact optimum or SPE theorem.'})
    report = {
        'status': 'EXACT_STRICT_LOWER_BOUND', 'old_lower': str(old_lower), 'alpha': str(alpha),
        'step': str(step), 'step_float': float(step), 'new_lower': str(lower), 'new_lower_float': float(lower),
        'exact_improvement': str(lower - old_lower), 'improvement_float': float(lower - old_lower),
        'strict_half_gap_of_lower_bound': str(1 - 2 * lower), 'sign_preserving_bounds': len(bounds),
        'tight_step_bounds': [{'kind': kind, 'index': index, 'bound': str(value)} for value, kind, index in bounds if value == step],
        'old_positive_rows_used': len(lam), 'new_common_X_rows_used': len(projection['new_row_multipliers']),
        'all21021_dual_residuals_nonnegative': True,
        'certificate_sha256': sha(HERE / 'strict_lower_bound_certificate.json'),
        'whole_face_identity_sha256': sha(HERE / 'old_optimal_face_cut_identity.json'),
        'builder_sha256': sha(Path(__file__)), 'optimizer_calls': 0, 'seconds': time.monotonic() - start,
        'exact_optimum_not_claimed': True}
    write('strict_lower_bound_derivation.json', report)
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__': main()
