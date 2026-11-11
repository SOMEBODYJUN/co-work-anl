"""Verify and copy one immutable Actions discovery for exact postprocessing.

Only a directory already returned inside this run workspace is accepted.
No optimizer, network, git operation or mutation of the discovery occurs.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import argparse
import json
import shutil

import numpy as np

HERE = Path(__file__).resolve().parent
WORK = HERE.parent


def sha(path):
    return sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--discovery', required=True)
    parser.add_argument('--output', default='recovery')
    args = parser.parse_args()
    source = Path(args.discovery).resolve()
    out = (HERE / args.output).resolve()
    assert source.is_relative_to(WORK) and source.is_dir()
    assert out.is_relative_to(HERE) and out != HERE and not out.exists()
    actual_input = read(source / 'actions_input_manifest.json')
    planned = read(HERE / 'runtime_inputs_manifest.json')
    assert actual_input['runtime_inputs_manifest'] == planned
    assert actual_input['inputs'] == planned['inputs']
    assert actual_input['runtime_inputs_manifest_sha256'] == sha(HERE / 'runtime_inputs_manifest.json')
    for record in planned['inputs']:
        assert sha(HERE / record['name']) == record['sha256']
    output_manifest = read(source / 'output_manifest.json')
    for record in output_manifest['files']:
        p = source / record['name']
        assert p.is_file() and sha(p) == record['sha256']
        assert p.stat().st_size == record['bytes']
    execution = read(source / 'execution.json')
    numerical = read(source / 'numerical_result.json')
    assert execution['source_sha256'] == sha(HERE / 'actions_solve.py') == sha(source / 'executed_actions_solve.py')
    assert numerical['matrix_sha256'] == sha(HERE / 'exact_matrix.json.gz')
    assert numerical['floating_problem_sha256'] == sha(HERE / 'floating_problem.npz')
    assert numerical['method'] == 'highs-ds' and numerical['optimizer_calls'] == 1
    arrays = np.load(source / 'floating_solver_arrays.npz', allow_pickle=False)
    assert tuple(map(int, arrays['shape'])) == (20911, 20585)
    assert arrays['primal'].shape == arrays['lower_marginals'].shape == (20585,)
    assert arrays['inequality_marginals'].shape == arrays['scales'].shape == (20911,)
    assert int(arrays['optimizer_calls']) == 1
    eligible = bool(numerical['success'] and np.all(arrays['availability'] == 1))
    out.mkdir()
    static = ('exact_matrix.json.gz', 'epigraph_structure.json', 'zz_envelope_structure.json',
              'inherited_dual_lower_bound.json', 'recover.py', 'recovery_model.py')
    for name in static:
        shutil.copyfile(HERE / name, out / name)
    for name in ('floating_solver_arrays.npz', 'numerical_result.json'):
        shutil.copyfile(source / name, out / name)
    report = {'status': 'PREPARED_FOR_EXACT_RECOVERY' if eligible else 'DISCOVERY_RETAINED_REQUIRES_REVIEW',
              'discovery_directory': str(source.relative_to(WORK)),
              'discovery_output_manifest_sha256': sha(source / 'output_manifest.json'),
              'verified_discovery_output_files': len(output_manifest['files']),
              'verified_actual_runtime_inputs': len(planned['inputs']),
              'source_driver_sha256': sha(HERE / 'actions_solve.py'),
              'recovery_inputs': {name: sha(out / name) for name in static + ('floating_solver_arrays.npz', 'numerical_result.json')},
              'eligible_for_standard_recovery': eligible, 'W_float': numerical.get('W_float'),
              'optimizer_calls_in_recovery': 0, 'discovery_unchanged': True,
              'prepared_utc': datetime.now(timezone.utc).isoformat()}
    (out / 'recovery_input_manifest.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
