"""Append exactly the certified common-max-B row to the entire 20910 system.

This is a generic homogeneous 20911 by 20585 necessary LP. No optimizer is
imported or called here. All old rows, columns, zero histograms and hidden
conditional masses remain, and no point value is substituted into a row.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import gzip
import io
import json
import platform
import time

import numpy as np

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = WORK.parents[2]
BASE = WORK / 'full624_augmented_lp/recovery'
OLD_ROWS, COLUMNS, ORIGINAL = 20910, 20585, 4849
PINS = {
    'full624_augmented_lp/recovery/exact_matrix.json.gz': '96388092e21621f157b4428ce99f98b93afa99ed3a0c12c72b1d6475c26fba30',
    'full624_augmented_lp/recovery/augmented_lp_exact.json': 'cb45ee6f8df153764c91bd77d0543527cc44719ff7cc43646ffce06a7921a932',
    'full624_augmented_lp/recovery/exact_dual_certificate.json': '22381bc9844aa5452b45a5bd8ef4a6148808388455b80666b49475df0f7377b3',
    'terminal_response_cycles/max_b_exact_certificate.json': 'f6189600d6ccccdbd9fcbc4ae4af9e768c9382af8de1ae41d6e6a7ee7662f664',
    'full624_augmented_lp/floating_problem.npz': 'bdf06ee0ac8e10d4a7e8b19c6b90ab7f85b170a3ee87179816103ceea5074c52',
    'full624_augmented_lp/recovery/epigraph_structure.json': '90a7673d817cbfcbca79c876b608e9d307c47b52897c795cfe8655c145ffa6f0',
    'full624_augmented_lp/recovery/zz_envelope_structure.json': 'b2136933db4b6c5f939d3218959b27c8bad012ff27cf9b14a1ecb01a7845f0bb',
}


def sha(path):
    return sha256(path.read_bytes()).hexdigest()


def read(path):
    if path.suffix == '.gz':
        with gzip.open(path, 'rt', encoding='utf-8') as f:
            return json.load(f)
    return json.loads(path.read_text())


def write(name, value):
    p = HERE / name
    assert not p.exists(), ('refuse_overwrite', str(p))
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


@lru_cache(maxsize=None)
def rational(s):
    return F(s)


def dot(row, x):
    return sum((rational(v) * x[j] for j, v in row if x[j]), F())


def main():
    start = time.monotonic()
    for relative, pin in PINS.items():
        assert sha(WORK / relative) == pin, relative
    old = read(BASE / 'exact_matrix.json.gz')
    point = read(BASE / 'augmented_lp_exact.json')
    dual = read(BASE / 'exact_dual_certificate.json')
    certificate = read(WORK / 'terminal_response_cycles/max_b_exact_certificate.json')
    independent = read(WORK / 'terminal_response_cycles/max_b_independent_certificate_audit.json')
    main_audit = read(WORK / 'main_maxb_cut_audit.json')
    assert independent['status'] == 'PASS'
    assert independent['certificate_sha256'] == PINS['terminal_response_cycles/max_b_exact_certificate.json']
    assert main_audit['status'] == 'MAIN_INDEPENDENT_ANALYTIC_MAXB_CUT_PASS'
    assert main_audit['certificate_sha256'] == independent['certificate_sha256']
    assert len(old['rows']) == len(old['row_names']) == OLD_ROWS
    assert len(old['columns']) == len(old['objective']) == len(old['normalization']) == COLUMNS
    assert [{k: v for k, v in c.items() if k != 'weight'} for c in point['columns']] == old['columns']
    cut = certificate['sparse_original4849_row_K_normalized']
    assert cut == main_audit['row'] and len(cut) == 17
    assert len({j for j, v in cut}) == 17 and cut[0] == [0, '1']
    assert old['columns'][0] == {'kind': 'K'}
    assert all(0 <= j < ORIGINAL and rational(v) for j, v in cut)
    hist = [j for j, c in enumerate(old['columns'][:ORIGINAL]) if c['kind'] == 'hist']
    assert len(hist) == 16 and set(j for j, v in cut) == {0, *hist}
    x = [F(c['weight']) for c in point['columns']]
    cut_value = dot(cut, x)
    assert cut_value == F(certificate['K_normalized_point_value']) == F(main_audit['exact_old_point_value']) < 0
    mapping = [{'column': j, 'descriptor': old['columns'][j], 'coefficient': v,
                'old_weight': str(x[j]), 'old_term': str(F(v) * x[j])} for j, v in cut]
    metadata = {k: v for k, v in old.items() if k not in ('rows', 'row_names', 'columns', 'objective', 'normalization')}
    row_name = 'common-max-B:universal-K-normalized:f6189600d6ccccdb'
    matrix = {**old, 'rows': old['rows'] + [cut], 'row_names': old['row_names'] + [row_name],
              'baseline_rows': OLD_ROWS, 'baseline_columns': COLUMNS,
              'this_round_added': 1, 'this_round_added_columns': 0,
              'appended_unique_rows': OLD_ROWS + 1 - old['original_rows'],
              'inherited_matrix_metadata': metadata,
              'maxb_cut_certificate_sha256': PINS['terminal_response_cycles/max_b_exact_certificate.json'],
              'maxb_cut_field': 'sparse_original4849_row_K_normalized',
              'maxb_cut_row': OLD_ROWS, 'all_columns_nonnegative': True,
              'inequality_convention': 'Each exact sparse row has value >= 0; no constant RHS.',
              'scope': 'Entire frozen 20910 by 20585 fixed16-hist necessary LP plus one universal common-max-B row; no SPE sufficiency.'}
    target = HERE / 'exact_matrix.json.gz'
    assert not target.exists()
    with target.open('wb') as raw:
        with gzip.GzipFile(fileobj=raw, filename='', mode='wb', mtime=0) as gz:
            with io.TextIOWrapper(gz, encoding='utf-8') as f:
                json.dump(matrix, f, ensure_ascii=False, separators=(',', ':'))
    assert matrix['rows'][:OLD_ROWS] == old['rows']
    assert matrix['row_names'][:OLD_ROWS] == old['row_names']
    assert all(matrix[k] == old[k] for k in ('columns', 'objective', 'normalization'))

    lower = F(dual['normalization_multiplier'])
    assert lower == F(point['W'])
    objective = list(map(F, matrix['objective']))
    norm = list(map(F, matrix['normalization']))
    residual = [c - lower * a for c, a in zip(objective, norm)]
    for i, v in dual['row_multipliers']:
        weight = F(v)
        assert 0 <= i < OLD_ROWS and weight > 0
        for j, a in matrix['rows'][i]:
            residual[j] -= weight * rational(a)
    assert residual == list(map(F, dual['residuals'])) and min(residual) >= 0
    write('inherited_dual_lower_bound.json', {
        'verified': True, 'normalization_multiplier': str(lower),
        'source_sha256': PINS['full624_augmented_lp/recovery/exact_dual_certificate.json'],
        'row_multipliers': dual['row_multipliers'], 'added_row_multiplier': [OLD_ROWS, '0'],
        'residuals': list(map(str, residual)), 'columns_checked': COLUMNS,
        'minimum_coefficient_residual': str(min(residual)), 'matrix_sha256': sha(target),
        'identity': 'objective = lower * normalization + sum_i lambda_i row_i + nonnegative residual',
        'scope': 'Exact lower bound only; the old primal violates the appended row.'})
    for name in ('epigraph_structure.json', 'zz_envelope_structure.json'):
        p = HERE / name
        assert not p.exists()
        p.write_bytes((BASE / name).read_bytes())

    nnz = sum(map(len, matrix['rows']))
    assert nnz == 3208814
    data = np.empty(nnz, dtype=np.float64)
    indices = np.empty(nnz, dtype=np.int32)
    indptr = np.empty(OLD_ROWS + 2, dtype=np.int32)
    scales = np.empty(OLD_ROWS + 1, dtype=np.float64)
    k = 0
    for i, row in enumerate(matrix['rows']):
        indptr[i] = k
        values = [float(rational(v)) for j, v in row]
        scales[i] = max([abs(v) for v in values] + [1e-50])
        for (j, _), v in zip(row, values):
            indices[k] = j
            data[k] = -v / scales[i]
            k += 1
    indptr[-1] = k
    assert k == nnz
    old_float = np.load(WORK / 'full624_augmented_lp/floating_problem.npz', allow_pickle=False)
    assert np.array_equal(data[:3208797], old_float['data'])
    assert np.array_equal(indices[:3208797], old_float['indices'])
    assert np.array_equal(indptr[:OLD_ROWS + 1], old_float['indptr'])
    assert np.array_equal(scales[:OLD_ROWS], old_float['scales'])
    assert np.array_equal(np.asarray(list(map(float, objective))), old_float['objective'])
    assert np.array_equal(np.asarray(list(map(float, norm))), old_float['normalization'])
    np.savez_compressed(HERE / 'floating_problem.npz', data=data, indices=indices, indptr=indptr,
                        shape=np.asarray([OLD_ROWS + 1, COLUMNS]), objective=np.asarray(list(map(float, objective))),
                        normalization=np.asarray(list(map(float, norm))), scales=scales,
                        inequality_rhs=np.zeros(OLD_ROWS + 1), normalization_rhs=np.asarray([1.0]))
    write('maxb_cut_mapping.json', {
        'row_index': OLD_ROWS, 'row_name': row_name, 'sparse_row': cut,
        'mapping': mapping, 'all_auxiliary_coefficients_zero': COLUMNS - ORIGINAL,
        'old_point_exact_value': str(cut_value), 'old_point_value_float': float(cut_value),
        'certificate_sha256': PINS['terminal_response_cycles/max_b_exact_certificate.json'],
        'hist_columns': hist, 'zero_hist_columns_retained': [j for j in hist if x[j] == 0]})
    source_paths = [WORK / relative for relative in PINS]
    source_paths += [WORK / 'terminal_response_cycles/max_b_independent_certificate_audit.json',
                     WORK / 'terminal_response_cycles/max_b_symbolic_lift.json',
                     WORK / 'terminal_response_cycles/max_b_lift.py',
                     WORK / 'terminal_response_cycles/max_b_certify.py',
                     WORK / 'terminal_response_cycles/max_b_audit.py',
                     WORK / 'main_maxb_cut_audit.json', WORK / 'main_verify_maxb_cut.py',
                     WORK / 'full624_augmented_lp/recovery_report.md',
                     REPO / 'archives/customer-attraction/state/引理/真实末回复的共同潜力上限与重叠参数端点--引理.md',
                     Path(__file__)]
    write('inputs_manifest.json', {
        'source_files': [{'path': str(p.relative_to(REPO)), 'sha256': sha(p), 'bytes': p.stat().st_size} for p in source_paths],
        'generated_inputs': {name: sha(HERE / name) for name in ('exact_matrix.json.gz', 'floating_problem.npz',
                              'epigraph_structure.json', 'zz_envelope_structure.json', 'inherited_dual_lower_bound.json',
                              'maxb_cut_mapping.json')},
        'shape': [OLD_ROWS + 1, COLUMNS], 'nonzeros': nnz, 'all_columns_nonnegative': True,
        'all_16_histograms_retained': True, 'all_4992_shared624_hidden_columns_retained': True,
        'fixed_point_rhs_substitutions': 0, 'optimizer_calls': 0,
        'python': platform.python_version(), 'numpy': np.__version__,
        'created_utc': datetime.now(timezone.utc).isoformat()})
    report = {
        'status': 'PASS', 'rows': OLD_ROWS + 1, 'columns': COLUMNS, 'nonzeros': nnz,
        'old_rows_unchanged': OLD_ROWS, 'old_row_names_unchanged': OLD_ROWS,
        'old_column_descriptors_unchanged': COLUMNS, 'added_rows': 1, 'added_columns': 0,
        'added_nonzeros': len(cut), 'old_floating_csr_prefix_bitwise_unchanged': True,
        'old_auxiliary_columns_retained': 10744, 'shared624_hidden_columns_retained': 4992,
        'histograms_retained': len(hist), 'zero_histograms_retained': len([j for j in hist if x[j] == 0]),
        'new_row_old_auxiliary_coefficients_zero': 15736, 'fixed_point_rhs_substitutions': 0,
        'inherited_dual_columns_checked': COLUMNS, 'inherited_dual_new_row_multiplier': '0',
        'lower_bound': str(lower), 'lower_bound_float': float(lower),
        'new_row_old_point_value': str(cut_value), 'new_row_old_point_value_float': float(cut_value),
        'matrix_sha256': sha(target), 'floating_problem_sha256': sha(HERE / 'floating_problem.npz'),
        'seconds': time.monotonic() - start, 'optimizer_calls': 0}
    write('assembly_verification.json', report)
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    main()
