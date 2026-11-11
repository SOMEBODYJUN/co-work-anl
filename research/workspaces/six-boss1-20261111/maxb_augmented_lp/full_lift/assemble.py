"""Append all1387 common-X rows and436 columns to the frozen20910 system.

The one-cut20911 preparation is preserved and is not solved. This complete
lift contains all old20585 columns,16 shared X masses and420 overlap uppers.
No optimizer is imported or called, and no point RHS is substituted.
"""
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
WORK = HERE.parents[1]
REPO = WORK.parents[2]
BASE = WORK / 'full624_augmented_lp/recovery'
OLDM, OLDN, ORIGINAL, ADDM, ADDN = 20910, 20585, 4849, 1387, 436
PINS = {
    'full624_augmented_lp/recovery/exact_matrix.json.gz': '96388092e21621f157b4428ce99f98b93afa99ed3a0c12c72b1d6475c26fba30',
    'full624_augmented_lp/recovery/augmented_lp_exact.json': 'cb45ee6f8df153764c91bd77d0543527cc44719ff7cc43646ffce06a7921a932',
    'full624_augmented_lp/recovery/exact_dual_certificate.json': '22381bc9844aa5452b45a5bd8ef4a6148808388455b80666b49475df0f7377b3',
    'terminal_response_cycles/max_b_symbolic_lift.json': '52129dc848cf47f569f61442962a01aec61c6317531be0d24837d41071c96a5c',
    'terminal_response_cycles/max_b_exact_certificate.json': 'f6189600d6ccccdbd9fcbc4ae4af9e768c9382af8de1ae41d6e6a7ee7662f664',
    'actual_pair_20910/symbolic_rows.json.gz': '423bf2c92d9c85c7e6086a193365ed80cd2427d7f7ee406972e1faf1813ea62f',
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
def rat(s):
    return F(s)


def mapped(j):
    assert 0 <= j < ORIGINAL + ADDN
    return j if j < ORIGINAL else j + OLDN - ORIGINAL


def row_name(name):
    name = list(name)
    if name[0] in ('overlap-at-most-X', 'overlap-at-most-query'):
        name[1] = mapped(name[1])
    return 'common-max-B:' + json.dumps(name, ensure_ascii=False, separators=(',', ':'))


def main():
    started = time.monotonic()
    for relative, pin in PINS.items():
        assert sha(WORK / relative) == pin, relative
    old = read(BASE / 'exact_matrix.json.gz')
    point = read(BASE / 'augmented_lp_exact.json')
    dual = read(BASE / 'exact_dual_certificate.json')
    lift = read(WORK / 'terminal_response_cycles/max_b_symbolic_lift.json')
    cert = read(WORK / 'terminal_response_cycles/max_b_exact_certificate.json')
    preflight = read(WORK / 'terminal_response_cycles/max_b_independent_preflight.json')
    independent = read(WORK / 'terminal_response_cycles/max_b_independent_certificate_audit.json')
    assert preflight['status'] == 'passed' and independent['status'] == 'PASS'
    assert preflight['symbolic_lift_sha256'] == PINS['terminal_response_cycles/max_b_symbolic_lift.json']
    assert independent['certificate_sha256'] == PINS['terminal_response_cycles/max_b_exact_certificate.json']
    assert (lift['row_count'], lift['new_column_count']) == (ADDM, ADDN)
    assert lift['row_constants'] == 0 and lift['all_new_columns_nonnegative'] is True
    assert len(old['rows']) == len(old['row_names']) == OLDM
    assert len(old['columns']) == len(old['objective']) == len(old['normalization']) == OLDN
    assert [{k: v for k, v in c.items() if k != 'weight'} for c in point['columns']] == old['columns']
    new_rows = [[[mapped(j), a] for j, a in record['row']] for record in lift['rows']]
    assert sum(map(len, new_rows)) == 87264
    assert all(j < ORIGINAL or OLDN <= j < OLDN + ADDN for row in new_rows for j, a in row)
    new_cols = lift['new_columns']
    assert len(new_cols) == 436 and all(c['kind'] == 'common-X-mass' for c in new_cols[:16])
    assert all(c['kind'] == 'X-query-overlap-upper' for c in new_cols[16:])
    xcols = {c['hist_column']: OLDN + i for i, c in enumerate(new_cols[:16])}
    hist = [j for j, c in enumerate(old['columns'][:ORIGINAL]) if c['kind'] == 'hist']
    assert list(xcols) == hist and len(hist) == 16
    structure = []
    for k, c in enumerate(new_cols[16:], 16):
        column = OLDN + k
        source_column = ORIGINAL + k
        xrow = OLDM + 16 + 2 * (k - 16)
        qrow = xrow + 1
        assert lift['rows'][xrow - OLDM]['name'] == ['overlap-at-most-X', source_column]
        assert lift['rows'][qrow - OLDM]['name'] == ['overlap-at-most-query', source_column]
        assert new_rows[xrow - OLDM] == [[xcols[c['hist_column']], '1'], [column, '-1']]
        assert new_rows[qrow - OLDM] == c['query_marginal'] + [[column, '-1']]
        structure.append({'column': column, 'source_compressed_column': source_column,
                          'hist_column': c['hist_column'], 'x_column': xcols[c['hist_column']],
                          'x_upper_row': xrow, 'query_upper_row': qrow,
                          'query_marginal': c['query_marginal'], 'query_token': c['query_token']})
    metadata = {k: v for k, v in old.items() if k not in ('rows', 'row_names', 'columns', 'objective', 'normalization')}
    matrix = {**old, 'rows': old['rows'] + new_rows,
              'row_names': old['row_names'] + [row_name(record['name']) for record in lift['rows']],
              'columns': old['columns'] + new_cols, 'objective': old['objective'] + ['0'] * ADDN,
              'normalization': old['normalization'] + ['0'] * ADDN,
              'baseline_rows': OLDM, 'baseline_columns': OLDN,
              'this_round_added': ADDM, 'this_round_added_columns': ADDN,
              'appended_unique_rows': OLDM + ADDM - old['original_rows'],
              'auxiliary_columns': OLDN + ADDN - ORIGINAL,
              'canonical_min_auxiliaries': old['canonical_min_auxiliaries'] + 420,
              'inherited_matrix_metadata': metadata, 'maxb_common_mass_columns': 16,
              'maxb_canonical_min_columns': 420, 'maxb_lift_sha256': PINS['terminal_response_cycles/max_b_symbolic_lift.json'],
              'maxb_compressed_to_full_offset': OLDN - ORIGINAL, 'all_columns_nonnegative': True,
              'inequality_convention': 'Each exact sparse row has value >=0; no constant RHS.',
              'scope': 'Entire20910 by20585 fixed16-hist necessary LP plus the complete common-X1387-row436-column lift; no SPE sufficiency.'}
    assert matrix['rows'][:OLDM] == old['rows'] and matrix['row_names'][:OLDM] == old['row_names']
    assert matrix['columns'][:OLDN] == old['columns']
    assert matrix['objective'][:OLDN] == old['objective'] and matrix['normalization'][:OLDN] == old['normalization']
    target = HERE / 'exact_matrix.json.gz'
    assert not target.exists()
    with target.open('wb') as raw:
        with gzip.GzipFile(fileobj=raw, filename='', mode='wb', mtime=0) as gz:
            with io.TextIOWrapper(gz, encoding='utf-8') as f:
                json.dump(matrix, f, ensure_ascii=False, separators=(',', ':'))
    write('maxb_envelope_structure.json', {
        'core_columns': list(xcols.values()), 'hist_to_x': [[h, j] for h, j in xcols.items()],
        'auxiliaries': structure, 'upper_rows': [i for r in structure for i in (r['x_upper_row'], r['query_upper_row'])],
        'semantics': 'Each virtual upper is canonically min(common-X mass, fixed old-query marginal); not a physical joint customer law.',
        'compressed_start': ORIGINAL, 'full_start': OLDN, 'column_offset': OLDN - ORIGINAL,
        'lift_sha256': PINS['terminal_response_cycles/max_b_symbolic_lift.json']})
    lower = F(dual['normalization_multiplier'])
    assert lower == F(point['W'])
    objective = list(map(F, matrix['objective']))
    norm = list(map(F, matrix['normalization']))
    residual = [c - lower * a for c, a in zip(objective, norm)]
    for i, v in dual['row_multipliers']:
        assert 0 <= i < OLDM and F(v) > 0
        for j, a in matrix['rows'][i]:
            residual[j] -= F(v) * rat(a)
    assert residual[:OLDN] == list(map(F, dual['residuals']))
    assert residual[OLDN:] == [F()] * ADDN and min(residual) >= 0
    write('inherited_dual_lower_bound.json', {
        'verified': True, 'normalization_multiplier': str(lower), 'row_multipliers': dual['row_multipliers'],
        'source_sha256': PINS['full624_augmented_lp/recovery/exact_dual_certificate.json'],
        'added_row_multipliers_all_zero': ADDM, 'added_column_residuals_all_zero': ADDN,
        'residuals': list(map(str, residual)), 'columns_checked': OLDN + ADDN,
        'minimum_coefficient_residual': str(min(residual)), 'matrix_sha256': sha(target),
        'identity': 'objective = lower * normalization + sum_i lambda_i row_i + nonnegative residual',
        'scope': 'Exact inherited lower bound; no claim that the old point has a full-X extension.'})
    for name in ('epigraph_structure.json', 'zz_envelope_structure.json'):
        p = HERE / name
        assert not p.exists()
        p.write_bytes((BASE / name).read_bytes())
    nnz = sum(map(len, matrix['rows']))
    assert nnz == 3296061
    data = np.empty(nnz, dtype=np.float64)
    indices = np.empty(nnz, dtype=np.int32)
    indptr = np.empty(OLDM + ADDM + 1, dtype=np.int32)
    scales = np.empty(OLDM + ADDM, dtype=np.float64)
    k = 0
    for i, row in enumerate(matrix['rows']):
        indptr[i] = k
        values = [float(rat(a)) for j, a in row]
        scales[i] = max([abs(v) for v in values] + [1e-50])
        for (j, a), v in zip(row, values):
            indices[k] = j
            data[k] = -v / scales[i]
            k += 1
    indptr[-1] = k
    assert k == nnz
    with np.load(WORK / 'full624_augmented_lp/floating_problem.npz', allow_pickle=False) as raw:
        old_float = {name: raw[name] for name in raw.files}
    assert np.array_equal(data[:3208797], old_float['data']) and np.array_equal(indices[:3208797], old_float['indices'])
    assert np.array_equal(indptr[:OLDM + 1], old_float['indptr']) and np.array_equal(scales[:OLDM], old_float['scales'])
    assert np.array_equal(np.asarray(list(map(float, objective[:OLDN]))), old_float['objective'])
    assert np.array_equal(np.asarray(list(map(float, norm[:OLDN]))), old_float['normalization'])
    np.savez_compressed(HERE / 'floating_problem.npz', data=data, indices=indices, indptr=indptr,
                        shape=np.asarray([OLDM + ADDM, OLDN + ADDN]), objective=np.asarray(list(map(float, objective))),
                        normalization=np.asarray(list(map(float, norm))), scales=scales,
                        inequality_rhs=np.zeros(OLDM + ADDM), normalization_rhs=np.asarray([1.0]))
    # Re-express the existing10-row Farkas combination in the full21021 columns.
    combined = {}
    def add(j, a):
        combined[j] = combined.get(j, F()) + a
        if not combined[j]:
            del combined[j]
    full_weights = []
    for record in cert['row_multipliers']:
        i = record['row_index']
        weight = F(record['multiplier'])
        assert weight > 0 and record['name'] == lift['rows'][i]['name']
        for j, a in matrix['rows'][OLDM + i]:
            add(j, weight * rat(a))
        full_weights.append([OLDM + i, str(weight)])
    nonnegative = []
    for record in cert['new_nonnegativity_multipliers']:
        j = mapped(record['column'])
        weight = F(record['multiplier'])
        assert weight > 0 and matrix['columns'][j] == record['descriptor']
        add(j, weight)
        nonnegative.append([j, str(weight)])
    normalized = [[j, str(a / 3)] for j, a in sorted(combined.items())]
    assert normalized == cert['sparse_original4849_row_K_normalized']
    assert len(combined) == 17 and all(j < ORIGINAL for j in combined)
    xold = [F(c['weight']) for c in point['columns']]
    value = sum((a * xold[j] / 3 for j, a in combined.items()), F())
    assert value == F(cert['K_normalized_point_value']) < 0
    write('full_coordinate_farkas_projection.json', {
        'status': 'PASS', 'matrix_sha256': sha(target), 'new_row_multipliers': full_weights,
        'new_nonnegativity_multipliers': nonnegative, 'divide_combination_by': '3',
        'projected_row': normalized, 'all436_new_coefficients_zero': True,
        'all15736_old_auxiliary_coefficients_zero': True,
        'old_point_value': str(value), 'old_point_value_float': float(value),
        'certificate_sha256': PINS['terminal_response_cycles/max_b_exact_certificate.json'],
        'scope': 'Excludes every common-X extension of the fixed old point, not the old optimum face.'})
    source_paths = [WORK / relative for relative in PINS]
    source_paths += [WORK / 'terminal_response_cycles/max_b_independent_preflight.json',
                     WORK / 'terminal_response_cycles/max_b_independent_certificate_audit.json',
                     WORK / 'terminal_response_cycles/max_b_audit.py', WORK / 'terminal_response_cycles/max_b_lift.py',
                     WORK / 'terminal_response_cycles/max_b_certify.py', WORK / 'main_maxb_cut_audit.json',
                     WORK / 'main_verify_maxb_cut.py', WORK / 'full624_augmented_lp/recovery_report.md',
                     REPO / 'archives/customer-attraction/state/引理/真实末回复的共同潜力上限与重叠参数端点--引理.md', Path(__file__)]
    write('inputs_manifest.json', {
        'source_files': [{'path': str(p.relative_to(REPO)), 'sha256': sha(p), 'bytes': p.stat().st_size} for p in source_paths],
        'generated_inputs': {name: sha(HERE / name) for name in ('exact_matrix.json.gz', 'floating_problem.npz',
                              'epigraph_structure.json', 'zz_envelope_structure.json', 'maxb_envelope_structure.json',
                              'inherited_dual_lower_bound.json', 'full_coordinate_farkas_projection.json')},
        'shape': [OLDM + ADDM, OLDN + ADDN], 'nonzeros': nnz,
        'all_columns_nonnegative': True, 'all_16_histograms_retained': True,
        'all_4992_shared624_hidden_columns_retained': True, 'fixed_point_rhs_substitutions': 0,
        'optimizer_calls': 0, 'python': platform.python_version(), 'numpy': np.__version__,
        'created_utc': datetime.now(timezone.utc).isoformat()})
    report = {'status': 'PASS', 'rows': OLDM + ADDM, 'columns': OLDN + ADDN, 'nonzeros': nnz,
              'old_rows_unchanged': OLDM, 'old_column_descriptors_unchanged': OLDN,
              'added_rows': ADDM, 'added_columns': ADDN, 'added_nonzeros': 87264,
              'old_floating_csr_prefix_bitwise_unchanged': True, 'old_auxiliary_columns_retained': 10744,
              'shared624_hidden_columns_retained': 4992, 'histograms_retained': 16, 'zero_histograms_retained': 6,
              'new_common_X_core_columns': 16, 'new_canonical_min_columns': 420,
              'fixed_point_rhs_substitutions': 0, 'compactcut_not_separately_appended': True,
              'inherited_dual_columns_checked': OLDN + ADDN, 'new_dual_row_weights_zero': ADDM,
              'new_dual_column_residuals_zero': ADDN, 'lower_bound': str(lower),
              'full_coordinate_Farkas_recovers_compactcut': True,
              'matrix_sha256': sha(target), 'floating_problem_sha256': sha(HERE / 'floating_problem.npz'),
              'seconds': time.monotonic() - started, 'optimizer_calls': 0}
    write('assembly_verification.json', report)
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    main()
