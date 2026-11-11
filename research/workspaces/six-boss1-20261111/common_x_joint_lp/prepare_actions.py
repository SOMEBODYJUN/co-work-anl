"""Prepare the unique request only after Main explicitly releases this input.

This script does not dispatch. It must not be run while a final row package
is still under Main's review. All necessary runtime inputs are self-contained.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]


def sha(p): return sha256(p.read_bytes()).hexdigest()


def save(name, value):
    p = HERE/name; assert not p.exists(), ('refuse_overwrite', name)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--main-release-reference', required=True,
        help='Concrete Main message or source reference approving this exact final row set; not a self-authorization.')
    args = parser.parse_args(); assert args.main_release_reference.strip()
    audit = json.loads((HERE/'structure_and_lower_verification.json').read_text()); assert audit['status'] == 'PASS'
    m, n, nz = audit['rows'], audit['columns'], audit['nonzeros']
    names = ('actions_solve.py', 'exact_matrix.json.gz', 'floating_problem.npz', 'structure_and_lower_verification.json', 'inputs_manifest.json')
    inputs = [{'name': name, 'sha256': sha(HERE/name), 'bytes': (HERE/name).stat().st_size} for name in names]
    save('runtime_inputs_manifest.json', {'shape': [m, n], 'nonzeros': nz, 'inputs': inputs,
        'explicit_dependencies': ['Python standard library', 'numpy', 'scipy'], 'extra_repository_python_helpers': [],
        'driver_is_self_contained': True, 'method': 'highs-ds', 'time_limit_seconds': 1800, 'job_timeout_minutes': 40,
        'optimizer_calls_planned': 1, 'automatic_numeric_reruns': 0, 'main_release_reference': args.main_release_reference,
        'created_utc': datetime.now(timezone.utc).isoformat(), 'core_columns': 10277, 'canonical_auxiliary_columns': 10744,
        'scope': 'Finite fixed16-hist common-X necessary system plus local own compatibility; no full SPE model.'})
    argv = ['python3', '-B', str((HERE/'actions_solve.py').relative_to(REPO)), '--execute', '--time-limit', '1800', '--output', 'actions_discovery']
    request = {'status': 'READY_FOR_MAIN_ACTIONS_UNIQUE_DISCOVERY', 'run': 'six-boss1-20261111', 'owner': 'Boss1',
        'local_optimization_calls': 0, 'authorized_optimization_calls': 1, 'main_release_reference': args.main_release_reference,
        'method': 'highs-ds', 'time_limit_seconds': 1800, 'job_timeout_minutes': 40, 'command': ' '.join(argv),
        'argv': argv, 'cwd': 'repository root', 'required_inputs': [{'path': str((HERE/name).relative_to(REPO)),
        'sha256': sha(HERE/name), 'bytes': (HERE/name).stat().st_size} for name in names + ('runtime_inputs_manifest.json',)],
        'dependencies': ['Python standard library', 'numpy', 'scipy'], 'extra_python_helpers': [], 'driver_is_self_contained': True,
        'requires_github_actions_environment': True,
        'dimensions': {'rows': m, 'columns': n, 'nonzeros': nz, 'added_columns': 0, 'core_columns': 10277,
        'canonical_old_auxiliary_columns': 10744, 'real_overlap_core_columns': 420, 'shared624_hidden_columns_retained': 4992,
        'all_histograms_retained': 16, 'historically_zero_histograms_retained': 6},
        'output_directory': str((HERE/'actions_discovery').relative_to(REPO)),
        'outputs': ['floating_solver_arrays.npz', 'numerical_result.json', 'actions_input_manifest.json', 'optimizer_call_started.json',
        'executed_actions_solve.py', 'solver_stdout.txt', 'solver_stderr.txt', 'execution.json', 'output_manifest.json', 'progress.jsonl',
        'worker_failure.json if failure', 'driver_failure.json if failure'],
        'arrays': 'Full-shape primal, inequality/equality/lower/upper marginals and residuals, unscaled row multipliers, recomputed row and dual residuals, availability and state; unavailable values remain explicit full-shape NaNs.',
        'retain_outputs_on_failure': True, 'automatic_numeric_reruns': 0,
        'exact_postprocessing': 'Only after Main returns immutable arrays: standard-library rational primal and dual; 10744 old auxiliaries canonical; 420 real y values preserved from core; independent every-row/column verification and 210 beta=L eight-cell witnesses.',
        'failure_boundary': 'An active-face recovery failure is not an infeasibility certificate. A numerical optimum below one half is not a game-theoretic counterexample.',
        'dispatch_performed_by_this_agent': False}
    save('actions_request.json', request); print(json.dumps(request, ensure_ascii=False, indent=2))


if __name__ == '__main__': main()
