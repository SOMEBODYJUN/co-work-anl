"""Freeze exact runtime inputs for Main to dispatch; does not dispatch."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]


def sha(path):
    return sha256(path.read_bytes()).hexdigest()


def save(name, obj):
    p = HERE / name
    assert not p.exists(), ('refuse_overwrite', str(p))
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


def main():
    audit = json.loads((HERE / 'structure_and_lower_verification.json').read_text())
    assert audit['status'] == 'PASS'
    names = ('actions_solve.py', 'exact_matrix.json.gz', 'floating_problem.npz',
             'structure_and_lower_verification.json', 'inputs_manifest.json')
    inputs = [{'name': name, 'sha256': sha(HERE / name), 'bytes': (HERE / name).stat().st_size} for name in names]
    save('runtime_inputs_manifest.json', {
        'shape': [20911, 20585], 'nonzeros': 3208814, 'inputs': inputs,
        'explicit_dependencies': ['Python standard library', 'numpy', 'scipy'],
        'extra_repository_python_helpers': [], 'driver_is_self_contained': True,
        'method': 'highs-ds', 'time_limit_seconds': 1800, 'job_timeout_minutes': 40,
        'optimizer_calls_planned': 1, 'automatic_numeric_reruns': 0,
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Complete fixed16-hist necessary system; not a complete SPE model.'})
    argv = ['python3', '-B', str((HERE / 'actions_solve.py').relative_to(REPO)),
            '--execute', '--time-limit', '1800', '--output', 'actions_discovery']
    required = names + ('runtime_inputs_manifest.json',)
    request = {
        'status': 'READY_FOR_MAIN_ACTIONS_UNIQUE_DISCOVERY', 'run': 'six-boss1-20261111',
        'owner': 'Boss1', 'local_optimization_calls': 0, 'authorized_optimization_calls': 1,
        'method': 'highs-ds', 'time_limit_seconds': 1800, 'job_timeout_minutes': 40,
        'command': ' '.join(argv), 'argv': argv, 'cwd': 'repository root',
        'required_inputs': [{'path': str((HERE / name).relative_to(REPO)), 'sha256': sha(HERE / name),
                             'bytes': (HERE / name).stat().st_size} for name in required],
        'dependencies': ['Python standard library', 'numpy', 'scipy'], 'extra_python_helpers': [],
        'driver_is_self_contained': True, 'requires_github_actions_environment': True,
        'dimensions': {'rows': 20911, 'columns': 20585, 'nonzeros': 3208814,
                       'added_rows': 1, 'added_columns': 0, 'zero_histograms_retained': 6,
                       'shared624_hidden_columns_retained': 4992},
        'output_directory': str((HERE / 'actions_discovery').relative_to(REPO)),
        'outputs': ['floating_solver_arrays.npz', 'numerical_result.json', 'actions_input_manifest.json',
                    'optimizer_call_started.json', 'executed_actions_solve.py', 'solver_stdout.txt',
                    'solver_stderr.txt', 'execution.json', 'output_manifest.json', 'progress.jsonl',
                    'worker_failure.json if failure', 'driver_failure.json if failure'],
        'arrays': 'Complete x, inequality/equality/lower/upper marginals and residuals, unscaled row multipliers, recomputed row/dual residuals, availability and state. Missing solutions are full-shape NaN arrays with explicit failure status.',
        'retain_outputs_on_failure': True, 'automatic_numeric_reruns': 0,
        'exact_postprocessing': 'After Main returns immutable arrays: sameW only if numerically compatible, then justified freeW if needed; exact dual; independent all20911 rows and20585 columns with10744 canonical auxiliary checks.',
        'failure_boundary': 'An active-face recovery failure is not infeasibility of the whole optimum face. Numerical optimal status is not an exact optimum certificate.',
        'dispatch_performed_by_this_agent': False}
    save('actions_request.json', request)
    print(json.dumps(request, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
