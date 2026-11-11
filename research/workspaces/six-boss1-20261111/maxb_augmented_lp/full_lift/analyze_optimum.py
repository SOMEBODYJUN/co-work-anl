"""Analyze an independently certified full-X optimum; never optimize.

Requires successful complete rational verification before writing output.
Extracts the new-block dual projection by cancelling all436 new columns
against their exact column residuals, and records precise scope limits.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import argparse
import gzip
import json

HERE = Path(__file__).resolve().parent
WORK = HERE.parents[1]


def sha(path): return sha256(path.read_bytes()).hexdigest()


def read(path):
    if path.suffix == '.gz':
        with gzip.open(path, 'rt') as f: return json.load(f)
    return json.loads(path.read_text())


@lru_cache(maxsize=None)
def rat(value): return Q(value)


def add(row, j, value):
    row[j] = row.get(j, Q()) + value
    if not row[j]: del row[j]


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--output', default='recovery')
    args = parser.parse_args(); out = (HERE / args.output).resolve()
    assert out.is_relative_to(HERE) and out != HERE
    verification = read(out / 'certificate_verification.json')
    assert verification['status'] == 'EXACT_OPTIMUM_VERIFIED'
    matrix = read(HERE / 'exact_matrix.json.gz')
    assert verification['matrix_sha256'] == sha(HERE / 'exact_matrix.json.gz')
    point = read(out / 'augmented_lp_exact.json'); dual = read(out / 'exact_dual_certificate.json')
    assert verification['primal_sha256'] == sha(out / 'augmented_lp_exact.json')
    assert verification['dual_sha256'] == sha(out / 'exact_dual_certificate.json')
    x = [Q(c['weight']) for c in point['columns']]; w = Q(point['W'])
    old_point = read(WORK / 'full624_augmented_lp/recovery/augmented_lp_exact.json')
    old_w = Q(old_point['W']); old_x = [Q(c['weight']) for c in old_point['columns']]
    strict = read(HERE / 'old_optimum_face/strict_lower_bound_certificate.json')
    strict_w = Q(strict['normalization_multiplier']); assert w >= strict_w > old_w
    residual = list(map(Q, dual['residuals']))
    block = {}; new_weights = []; categories = Counter(); category_sums = defaultdict(Q)
    for i, text in dual['row_multipliers']:
        if i < 20910: continue
        weight = Q(text); assert weight > 0
        name = matrix['row_names'][i]; assert name.startswith('common-max-B:')
        kind = json.loads(name[len('common-max-B:'):])[0]
        categories[kind] += 1; category_sums[kind] += weight
        new_weights.append({'row': i, 'name': name, 'weight': str(weight)})
        for j, value in matrix['rows'][i]: add(block, j, weight * rat(value))
    new_nonnegative = []
    for j in range(20585, 21021):
        if residual[j]:
            add(block, j, residual[j]); new_nonnegative.append([j, str(residual[j])])
    assert all(j < 4849 for j in block)
    projected_old = sum((v * old_x[j] for j, v in block.items()), Q())
    projected_new = sum((v * x[j] for j, v in block.items()), Q())
    assert projected_old < 0 and projected_new == 0
    xb = read(HERE / 'maxb_envelope_structure.json')
    branch_counts = Counter()
    for record in xb['auxiliaries']:
        xx = x[record['x_column']]
        query = sum((rat(v) * x[j] for j, v in record['query_marginal']), Q())
        assert x[record['column']] == min(xx, query)
        branch_counts['tie' if xx == query else 'X-bound' if xx < query else 'query-bound'] += 1
    hist = [{'hist_column': h, 'hist_mass': str(x[h]), 'X_column': j, 'X_mass': str(x[j]),
             'X_full_hist': x[h] == x[j], 'X_zero': x[j] == 0} for h, j in xb['hist_to_x']]
    compact = read(WORK / 'terminal_response_cycles/max_b_exact_certificate.json')['sparse_original4849_row_K_normalized']
    compact_slack = sum((Q(v) * x[j] for j, v in compact), Q()); assert compact_slack >= 0
    report = {
        'status': 'EXACT_OPTIMUM_ANALYZED', 'W': str(w), 'W_float': float(w),
        'old_W': str(old_w), 'strict_pre_discovery_lower': str(strict_w),
        'exact_increase_over_old': str(w - old_w), 'increase_over_old_float': float(w - old_w),
        'exact_gap_above_pre_discovery_lower': str(w - strict_w), 'gap_above_pre_discovery_lower_float': float(w - strict_w),
        'strict_half_gap': str(1 - 2 * w), 'strict_half_gap_float': float(1 - 2 * w),
        'new_dual_row_counts_by_family': dict(categories),
        'new_dual_weight_sums_by_family': {k: str(v) for k, v in category_sums.items()},
        'new_dual_rows': new_weights, 'new_column_residual_terms': new_nonnegative,
        'old_coordinate_projected_row': [[j, str(v)] for j, v in sorted(block.items())],
        'projected_old_point_value': str(projected_old), 'projected_old_point_value_float': float(projected_old),
        'projected_optimum_value': str(projected_new), 'new436_columns_canceled': True,
        'compactcut_optimum_slack': str(compact_slack), 'compactcut_optimum_slack_float': float(compact_slack),
        'common_X_histogram_masses': hist, 'common_X_min_branches': dict(branch_counts),
        'positive_original_columns': sum(v > 0 for v in x[:4849]),
        'positive_old_auxiliary_columns': sum(v > 0 for v in x[4849:15593]),
        'positive_shared624_columns': sum(v > 0 for v in x[15593:20585]),
        'positive_common_X_masses': sum(v > 0 for v in x[20585:20601]),
        'positive_common_X_min_columns': sum(v > 0 for v in x[20601:]),
        'new_zero_hist_columns': [h for h, j in xb['hist_to_x'] if x[h] == 0],
        'matrix_sha256': sha(HERE / 'exact_matrix.json.gz'),
        'verification_sha256': sha(out / 'certificate_verification.json'),
        'source_sha256': sha(Path(__file__)), 'optimizer_calls': 0,
        'scope': 'Exact optimum of the full common-X fixed16-hist necessary system only. The420 min variables are virtual; no common customer law or complete SPE is certified.'}
    path = out / 'optimality_analysis.json'; assert not path.exists()
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ('status', 'W', 'W_float', 'increase_over_old_float', 'gap_above_pre_discovery_lower_float', 'compactcut_optimum_slack_float', 'new_dual_row_counts_by_family')}, ensure_ascii=False, indent=2))


if __name__ == '__main__': main()
