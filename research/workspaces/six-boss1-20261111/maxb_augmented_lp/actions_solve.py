"""Self-contained single HiGHS-DS discovery for the full max-B augmentation.

Only standard-library, NumPy and SciPy dependencies are used. The default
is read-only input validation. --execute requires a real Actions runner,
allows one 1800-second linprog call, and retains all outputs on failure.
No dispatch, authentication, git action, or exact-optimum claim occurs here.
"""
from datetime import datetime, timezone
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import argparse
import gzip
import json
import os
import platform
import subprocess
import sys
import time
import traceback

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
ROWS, COLS, NONZEROS = 20911, 20585, 3208814


def utc():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    return sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def log(out, event, **fields):
    record = {'event': event, 'utc': utc(), **fields}
    line = json.dumps(record, ensure_ascii=False)
    print(line, flush=True)
    if out is not None:
        with (out / 'progress.jsonl').open('a') as f:
            f.write(line + '\n')


def verified_inputs(check_coefficients=True):
    import numpy as np
    manifest = json.loads((HERE / 'runtime_inputs_manifest.json').read_text())
    assert manifest['shape'] == [ROWS, COLS] and manifest['nonzeros'] == NONZEROS
    for record in manifest['inputs']:
        p = HERE / record['name']
        assert p.is_file() and sha(p) == record['sha256'], record['name']
        assert p.stat().st_size == record['bytes']
    report = json.loads((HERE / 'structure_and_lower_verification.json').read_text())
    assert report['status'] == 'PASS' and (report['rows'], report['columns']) == (ROWS, COLS)
    assert report['matrix_sha256'] == sha(HERE / 'exact_matrix.json.gz')
    with np.load(HERE / 'floating_problem.npz', allow_pickle=False) as compressed:
        p = {name: compressed[name] for name in compressed.files}
    assert tuple(map(int, p['shape'])) == (ROWS, COLS)
    assert p['indptr'].shape == (ROWS + 1,) and p['scales'].shape == (ROWS,)
    assert p['indices'].shape == p['data'].shape == (NONZEROS,)
    assert p['objective'].shape == p['normalization'].shape == (COLS,)
    assert p['inequality_rhs'].shape == (ROWS,) and np.all(p['inequality_rhs'] == 0)
    assert np.array_equal(p['normalization_rhs'], np.asarray([1.0]))
    assert np.all(p['scales'] > 0)
    if check_coefficients:
        with gzip.open(HERE / 'exact_matrix.json.gz', 'rt') as f:
            exact = json.load(f)
        assert len(exact['rows']) == ROWS and len(exact['columns']) == COLS
        assert np.array_equal(p['objective'], np.asarray([float(Fraction(v)) for v in exact['objective']]))
        assert np.array_equal(p['normalization'], np.asarray([float(Fraction(v)) for v in exact['normalization']]))
        cache = {}
        for i, row in enumerate(exact['rows']):
            lo, hi = int(p['indptr'][i]), int(p['indptr'][i + 1])
            assert hi - lo == len(row)
            values = []
            for j, text in row:
                if text not in cache:
                    cache[text] = float(Fraction(text))
                values.append(cache[text])
            scale = max([abs(v) for v in values] + [1e-50])
            assert p['scales'][i] == scale
            assert np.array_equal(p['indices'][lo:hi], np.asarray([j for j, v in row]))
            assert np.array_equal(p['data'][lo:hi], -np.asarray(values) / scale)
    return manifest, p


def worker(out):
    import numpy as np
    import scipy
    from scipy.optimize import linprog
    from scipy.sparse import csr_matrix
    assert os.environ.get('GITHUB_ACTIONS') == 'true'
    manifest, p = verified_inputs()
    sparse = csr_matrix((p['data'], p['indices'], p['indptr']), shape=(ROWS, COLS))
    calls = 0
    options = {'primal_feasibility_tolerance': 1e-10, 'dual_feasibility_tolerance': 1e-10,
               'time_limit': 1800.0, 'presolve': True, 'disp': True}
    arrays = {
        'primal': np.full(COLS, np.nan), 'inequality_marginals': np.full(ROWS, np.nan),
        'equality_marginals': np.full(1, np.nan), 'lower_marginals': np.full(COLS, np.nan),
        'upper_marginals': np.full(COLS, np.nan), 'inequality_residual': np.full(ROWS, np.nan),
        'equality_residual': np.full(1, np.nan), 'lower_residual': np.full(COLS, np.nan),
        'upper_residual': np.full(COLS, np.nan), 'computed_scaled_slacks': np.full(ROWS, np.nan),
        'computed_row_slacks': np.full(ROWS, np.nan), 'computed_dual_residual': np.full(COLS, np.nan),
        'row_multipliers_unscaled': np.full(ROWS, np.nan), 'normalization_residual': np.full(1, np.nan),
        'scales': p['scales'], 'shape': np.asarray([ROWS, COLS]),
        'availability': np.zeros(4, dtype=np.int8),
        'availability_order': np.asarray(['primal', 'row_dual', 'normalization_dual', 'column_lower_dual']),
        'solver_status_code': np.asarray(-999), 'solver_success': np.asarray(False),
        'optimizer_calls': np.asarray(0), 'state': np.asarray('PREPARED_BEFORE_SOLVER_CALL')}
    np.savez_compressed(out / 'floating_solver_arrays.npz', **arrays)
    report = {'success': False, 'status_code': None, 'exact_verified': False,
              'matrix_sha256': sha(HERE / 'exact_matrix.json.gz'),
              'floating_problem_sha256': sha(HERE / 'floating_problem.npz'),
              'runtime_inputs_manifest_sha256': sha(HERE / 'runtime_inputs_manifest.json'),
              'method': 'highs-ds', 'options': options, 'rows': ROWS, 'columns': COLS,
              'nonzeros': NONZEROS, 'python': platform.python_version(),
              'numpy': np.__version__, 'scipy': scipy.__version__,
              'optimizer_calls': 0, 'started_utc': utc()}
    write(out / 'numerical_result.json', report)
    try:
        assert not (out / 'optimizer_call_started.json').exists()
        write(out / 'optimizer_call_started.json', {'utc': utc(), 'calls': 1, 'method': 'highs-ds',
                                                   'time_limit': 1800, 'automatic_reruns': 0})
        calls = 1
        report['optimizer_calls'] = 1
        arrays['optimizer_calls'] = np.asarray(1)
        arrays['state'] = np.asarray('SOLVER_RUNNING_NO_RETURNED_SOLUTION')
        np.savez_compressed(out / 'floating_solver_arrays.npz', **arrays)
        write(out / 'numerical_result.json', report)
        log(out, 'single_highs_ds_started', options=options, shape=[ROWS, COLS])
        start = time.monotonic()
        solution = linprog(p['objective'], A_ub=sparse, b_ub=p['inequality_rhs'],
                           A_eq=csr_matrix(p['normalization'].reshape(1, -1)),
                           b_eq=p['normalization_rhs'], bounds=(0, None),
                           method='highs-ds', options=options)
        elapsed = time.monotonic() - start
        assert calls == 1

        def vector(value, size):
            if value is None:
                return np.full(size, np.nan)
            value = np.asarray(value, dtype=np.float64)
            assert value.shape == (size,)
            return value

        arrays['primal'] = vector(solution.x, COLS)
        for name, size in [('inequality', ROWS), ('equality', 1), ('lower', COLS), ('upper', COLS)]:
            section = solution.get({'inequality': 'ineqlin', 'equality': 'eqlin'}.get(name, name), {})
            arrays[name + '_marginals'] = vector(section.get('marginals'), size)
            arrays[name + '_residual'] = vector(section.get('residual'), size)
        available = [bool(np.all(np.isfinite(arrays[key]))) for key in
                     ('primal', 'inequality_marginals', 'equality_marginals', 'lower_marginals')]
        arrays['availability'] = np.asarray(available, dtype=np.int8)
        if available[0]:
            arrays['computed_scaled_slacks'] = p['inequality_rhs'] - sparse @ arrays['primal']
            arrays['computed_row_slacks'] = arrays['computed_scaled_slacks'] * p['scales']
            arrays['normalization_residual'] = p['normalization_rhs'] - p['normalization'] @ arrays['primal']
        if available[1]:
            arrays['row_multipliers_unscaled'] = -arrays['inequality_marginals'] / p['scales']
        if available[1] and available[2]:
            arrays['computed_dual_residual'] = (p['objective'] - arrays['equality_marginals'][0] * p['normalization']
                                                - sparse.T @ arrays['inequality_marginals'])
        arrays['solver_status_code'] = np.asarray(int(solution.status))
        arrays['solver_success'] = np.asarray(bool(solution.success))
        arrays['state'] = np.asarray('OPTIMAL_FLOAT_ONLY' if solution.success else 'SOLVER_RETURNED_FAILURE')
        np.savez_compressed(out / 'floating_solver_arrays.npz', **arrays)
        report.update(success=bool(solution.success), status_code=int(solution.status), message=str(solution.message),
                      W_float=None if solution.fun is None else float(solution.fun), nit=int(solution.nit),
                      crossover_nit=int(getattr(solution, 'crossover_nit', 0)), solver_seconds=elapsed,
                      finished_utc=utc(), array_availability=dict(zip(arrays['availability_order'].tolist(), available)),
                      arrays_sha256=sha(out / 'floating_solver_arrays.npz'))
        if available[0]:
            report.update(minimum_scaled_slack=float(np.min(arrays['computed_scaled_slacks'])),
                          minimum_unscaled_row_slack=float(np.min(arrays['computed_row_slacks'])),
                          minimum_primal_column=float(np.min(arrays['primal'])),
                          normalization_residual=float(arrays['normalization_residual'][0]),
                          positive_original_columns=int(np.sum(arrays['primal'][:4849] > 1e-11)),
                          positive_shared624_columns=int(np.sum(arrays['primal'][15593:] > 1e-11)),
                          maxb_cut_slack=float(arrays['computed_row_slacks'][-1]))
        if available[1] and available[2]:
            report.update(minimum_dual_row_multiplier=float(np.min(arrays['row_multipliers_unscaled'])),
                          minimum_computed_dual_residual=float(np.min(arrays['computed_dual_residual'])))
        write(out / 'numerical_result.json', report)
        log(out, 'single_highs_ds_finished', **report)
        if not solution.success:
            raise RuntimeError('The only numerical solve did not return optimal status. All arrays retained; no numerical rerun.')
        assert all(available), 'Successful solve lacks complete primal/row/column dual arrays.'
    except BaseException:
        failure = {'utc': utc(), 'optimizer_calls': calls, 'traceback': traceback.format_exc(),
                   'automatic_reruns': 0, 'exact_verified': False,
                   'failure_is_not_an_infeasibility_certificate': True}
        write(out / 'worker_failure.json', failure)
        raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--worker', action='store_true')
    parser.add_argument('--output', default='actions_discovery')
    parser.add_argument('--time-limit', type=int, default=1800)
    args = parser.parse_args()
    assert args.time_limit == 1800
    out = (HERE / args.output).resolve()
    assert out.is_relative_to(HERE) and out != HERE
    if args.worker:
        assert not args.execute and out.is_dir()
        return worker(out)
    manifest, arrays = verified_inputs()
    plan = {'status': 'EXECUTING' if args.execute else 'READY_INPUTS_VERIFIED_NO_OPTIMIZATION',
            'rows': ROWS, 'columns': COLS, 'nonzeros': NONZEROS, 'method': 'highs-ds',
            'time_limit_seconds': 1800, 'job_timeout_minutes': 40,
            'optimizer_calls_planned': 1, 'automatic_numeric_reruns': 0,
            'matrix_sha256': sha(HERE / 'exact_matrix.json.gz'),
            'floating_problem_sha256': sha(HERE / 'floating_problem.npz'),
            'runtime_inputs_manifest_sha256': sha(HERE / 'runtime_inputs_manifest.json'),
            'output': str(out.relative_to(REPO)), 'exact_verified': False}
    print(json.dumps(plan, ensure_ascii=False, indent=2), flush=True)
    if not args.execute:
        return
    assert os.environ.get('GITHUB_ACTIONS') == 'true', 'Large numerical discovery is authorized only on Actions.'
    assert not out.exists(), ('refuse_output_reuse', str(out))
    out.mkdir()
    (out / 'executed_actions_solve.py').write_bytes(Path(__file__).read_bytes())
    write(out / 'actions_input_manifest.json', {
        **plan, 'inputs': manifest['inputs'], 'driver_sha256': sha(Path(__file__)),
        'runtime_inputs_manifest': manifest, 'python': platform.python_version(), 'started_utc': utc()})
    argv = [sys.executable, '-B', str(Path(__file__).resolve()), '--worker', '--time-limit', '1800', '--output', args.output]
    record = {'argv': argv, 'cwd': str(REPO), 'source_sha256': sha(Path(__file__)),
              'source_snapshot': 'executed_actions_solve.py', 'python': platform.python_version(),
              'started_utc': utc(), 'subprocess_timeout_seconds': 1980,
              'thread_environment': {k: '1' for k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS')}}
    start = time.monotonic()
    exit_code = 1
    try:
        with (out / 'solver_stdout.txt').open('w') as stdout, (out / 'solver_stderr.txt').open('w') as stderr:
            process = subprocess.run(argv, cwd=REPO, stdout=stdout, stderr=stderr, timeout=1980,
                                     env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', **record['thread_environment']})
        exit_code = process.returncode
    except BaseException:
        write(out / 'driver_failure.json', {'utc': utc(), 'traceback': traceback.format_exc(),
                                           'all_partial_outputs_retained': True, 'automatic_reruns': 0})
    finally:
        record.update(exit_code=exit_code, elapsed_seconds=time.monotonic() - start, finished_utc=utc(),
                      status='NUMERICAL_DISCOVERY_COMPLETE_NOT_EXACT' if exit_code == 0 else 'FAILED_OUTPUTS_RETAINED',
                      stdout_sha256=sha(out / 'solver_stdout.txt'), stderr_sha256=sha(out / 'solver_stderr.txt'))
        write(out / 'execution.json', record)
        write(out / 'output_manifest.json', {
            'files': [{'name': p.name, 'sha256': sha(p), 'bytes': p.stat().st_size}
                      for p in sorted(out.iterdir()) if p.is_file() and p.name != 'output_manifest.json'],
            'exact_verified': False, 'required_next': 'Exact rational primal/dual recovery and independent full20911/20585 verification.'})
        print(json.dumps(record, ensure_ascii=False, indent=2), flush=True)
    raise SystemExit(exit_code)


if __name__ == '__main__':
    main()
