"""Record exact new-row activity and project the optimum to the single cut.

Does not assemble a new matrix or optimize. Uses the preserved20911 matrix
and a positive exact multiple of its cut extracted from the full dual.
The pre-existing independent single-cut verifier is run separately.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import gzip
import json

HERE = Path(__file__).resolve().parent
SINGLE = HERE.parent
WORK = HERE.parents[1]
RECOVERY = HERE / 'recovery'


def sha(path): return sha256(path.read_bytes()).hexdigest()


def read(path):
    if path.suffix == '.gz':
        with gzip.open(path, 'rt') as f: return json.load(f)
    return json.loads(path.read_text())


@lru_cache(maxsize=None)
def rat(v): return F(v)


def dot(row, x): return sum((rat(v) * x[j] for j, v in row if x[j]), F())


def write(path, value):
    assert not path.exists()
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    verified = read(RECOVERY / 'certificate_verification.json'); assert verified['status'] == 'EXACT_OPTIMUM_VERIFIED'
    analysis = read(RECOVERY / 'optimality_analysis.json')
    matrix = read(HERE / 'exact_matrix.json.gz')
    point = read(RECOVERY / 'augmented_lp_exact.json'); x = [F(c['weight']) for c in point['columns']]
    dual = read(RECOVERY / 'exact_dual_certificate.json'); weights = {i: F(v) for i, v in dual['row_multipliers']}
    pairs = {r['orbit_id']: r for r in read(WORK / 'actual_pair_20910/symbolic_rows.json.gz')['rows']}
    compact = read(WORK / 'terminal_response_cycles/max_b_exact_certificate.json')['sparse_original4849_row_K_normalized']
    projected = {j: F(v) for j, v in analysis['old_coordinate_projected_row']}
    gamma = projected[0]; assert gamma > 0
    assert projected == {j: gamma * F(v) for j, v in compact}
    families = {}; rows = []; positive = []
    for i in range(20910, 22297):
        name = json.loads(matrix['row_names'][i][len('common-max-B:'):])
        kind = name[0]; slack = dot(matrix['rows'][i], x); assert slack >= 0
        weight = weights.get(i, F()); assert weight * slack == 0
        if kind not in families:
            families[kind] = {'rows': 0, 'tight': 0, 'strict': 0, 'positive_dual_rows': 0}
        entry = families[kind]; entry['rows'] += 1; entry['tight' if slack == 0 else 'strict'] += 1
        entry['positive_dual_rows'] += int(weight > 0)
        record = {'row': i, 'name': name, 'slack': str(slack), 'slack_float': float(slack),
                  'tight': slack == 0, 'dual_weight': str(weight)}
        if kind == 'common-B-pair':
            record['representative_names'] = pairs[name[1]]['representative_names']
            record['orbit_size'] = pairs[name[1]]['orbit_size']
        if kind in ('overlap-at-most-X', 'overlap-at-most-query'):
            record['column_descriptor'] = matrix['columns'][name[1]]
        if weight:
            record['weight_divided_by_gamma'] = str(weight / gamma)
            positive.append(record)
        rows.append(record)
    activity = {'status': 'EXACT_ACTIVITY', 'gamma': str(gamma), 'gamma_float': float(gamma),
                'new_dual_projection_exactly_gamma_times_original_compactcut': True,
                'family_counts': families, 'positive_new_dual_rows': positive,
                'tight_non_overlap_rows': [r for r in rows if r['tight'] and r['name'][0] not in ('overlap-at-most-X', 'overlap-at-most-query')],
                'all_new_rows': rows, 'maximum_B_rows': [r for r in rows if r['name'][0] == 'maximum-B'],
                'cap_query_rows': [r for r in rows if r['name'][0] == 'X-caps-query'],
                'matrix_sha256': sha(HERE / 'exact_matrix.json.gz'),
                'point_sha256': sha(RECOVERY / 'augmented_lp_exact.json'),
                'dual_sha256': sha(RECOVERY / 'exact_dual_certificate.json'), 'optimizer_calls': 0}
    write(RECOVERY / 'new_row_activity.json', activity)
    single = read(SINGLE / 'exact_matrix.json.gz')
    assert sha(SINGLE / 'exact_matrix.json.gz') == 'b2ef1da774412ac42a951931914afcd31fd917ef261fd28d2e7b5072ed125682'
    assert single['rows'][:20910] == matrix['rows'][:20910]
    assert single['columns'] == matrix['columns'][:20585] and single['rows'][-1] == compact
    out = HERE / 'compact_projection'; assert not out.exists(); out.mkdir()
    single_x = x[:20585]; slacks = [dot(row, single_x) for row in single['rows']]
    assert min(single_x) >= 0 and min(slacks) >= 0 and slacks[-1] == 0
    new_point = {**point, 'columns': point['columns'][:20585], 'verified_rows': 20911,
                 'positive_columns': sum(v > 0 for v in single_x), 'minimum_slack': str(min(slacks)),
                 'scope': 'Exact optimum candidate for the preserved20911 by20585 single-compactcut necessary LP, obtained by projecting the full-X point.',
                 'source_full_point_sha256': sha(RECOVERY / 'augmented_lp_exact.json')}
    write(out / 'augmented_lp_exact.json', new_point)
    multipliers = [[i, str(v)] for i, v in weights.items() if i < 20910] + [[20910, str(gamma)]]
    lower = F(dual['normalization_multiplier'])
    residual = [F(c) - lower * F(a) for c, a in zip(single['objective'], single['normalization'])]
    for i, v in multipliers:
        for j, a in single['rows'][i]: residual[j] -= F(v) * rat(a)
    assert residual == list(map(F, dual['residuals'][:20585])) and min(residual) >= 0
    write(out / 'exact_dual_certificate.json', {
        'verified': True, 'normalization_multiplier': str(lower), 'row_multipliers': multipliers,
        'residuals': list(map(str, residual)), 'minimum_coefficient_residual': str(min(residual)),
        'equality_to_primal': True, 'matrix_sha256': sha(SINGLE / 'exact_matrix.json.gz'),
        'identity': 'objective = lower * normalization + sum_i lambda_i row_i + nonnegative residual',
        'source_full_dual_sha256': sha(RECOVERY / 'exact_dual_certificate.json'),
        'projection_coefficient_gamma': str(gamma),
        'scope': 'Single-cut objective optimum equality only; no equality of the two feasible projections is claimed.'})
    write(out / 'projection_derivation.json', {
        'status': 'EXACT_PROJECTED_PRIMAL_DUAL', 'W': str(lower), 'W_float': float(lower),
        'gamma': str(gamma), 'gamma_float': float(gamma),
        'single_matrix_sha256': sha(SINGLE / 'exact_matrix.json.gz'),
        'full_matrix_sha256': sha(HERE / 'exact_matrix.json.gz'),
        'single_positive_dual_rows': len(multipliers), 'single_primal_rows_checked': len(slacks),
        'single_dual_columns_checked': len(residual), 'optimizer_calls': 0,
        'same_optimal_value_does_not_mean_same_projected_feasible_set': True,
        'full_verification_sha256': sha(RECOVERY / 'certificate_verification.json'),
        'source_sha256': sha(Path(__file__))})
    print(json.dumps({'gamma': str(gamma), 'family_activity': families, 'single_projected_dual_rows': len(multipliers),
                      'single_primal_path': str(out / 'augmented_lp_exact.json'), 'optimizer_calls': 0}, ensure_ascii=False, indent=2))


if __name__ == '__main__': main()
