"""Verify one immutable Main-returned Actions discovery before recovery.

Standard library only. Refuses partial arrays as exact-recovery inputs,
retains discovery untouched, and never invokes an optimizer or recovery.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import argparse
import json
import math
import shutil
from recovery_model import load_npz

HERE = Path(__file__).resolve().parent
WORK = HERE.parents[1]


def sha(p): return sha256(p.read_bytes()).hexdigest()


def read(p): return json.loads(p.read_text())


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--discovery', required=True)
    parser.add_argument('--output', default='recovery'); args = parser.parse_args()
    source = Path(args.discovery).resolve(); out = (HERE/args.output).resolve()
    assert source.is_relative_to(WORK) and source.is_dir()
    assert out.is_relative_to(HERE) and out != HERE and not out.exists()
    planned = read(HERE/'runtime_inputs_manifest.json'); actual = read(source/'actions_input_manifest.json')
    assert actual['runtime_inputs_manifest'] == planned and actual['inputs'] == planned['inputs']
    assert actual['runtime_inputs_manifest_sha256'] == sha(HERE/'runtime_inputs_manifest.json')
    assert actual['driver_sha256'] == sha(HERE/'actions_solve.py')
    for record in planned['inputs']:
        p = HERE/record['name']; assert sha(p) == record['sha256'] and p.stat().st_size == record['bytes']
    output_manifest = read(source/'output_manifest.json')
    required_outputs = {'floating_solver_arrays.npz', 'numerical_result.json', 'actions_input_manifest.json',
        'optimizer_call_started.json', 'executed_actions_solve.py', 'solver_stdout.txt', 'solver_stderr.txt',
        'execution.json', 'progress.jsonl'}
    records = output_manifest['files']; names = [record['name'] for record in records]
    assert len(names) == len(set(names)), 'duplicate output-manifest entries'
    assert required_outputs.issubset(names), ('missing_required_outputs', sorted(required_outputs-set(names)))
    for record in output_manifest['files']:
        name = record['name']; assert isinstance(name, str) and Path(name).name == name and name not in ('', '.', '..')
        p = (source/name).resolve(); assert p.is_relative_to(source) and p.is_file()
        assert sha(p) == record['sha256'] and p.stat().st_size == record['bytes']
    execution = read(source/'execution.json'); numerical = read(source/'numerical_result.json')
    assert execution['source_sha256'] == sha(HERE/'actions_solve.py') == sha(source/'executed_actions_solve.py')
    assert numerical['matrix_sha256'] == sha(HERE/'exact_matrix.json.gz')
    assert numerical['floating_problem_sha256'] == sha(HERE/'floating_problem.npz')
    assert numerical['runtime_inputs_manifest_sha256'] == sha(HERE/'runtime_inputs_manifest.json')
    assert numerical['arrays_sha256'] == sha(source/'floating_solver_arrays.npz')
    assert numerical['method'] == 'highs-ds' and numerical['optimizer_calls'] == 1
    started = read(source/'optimizer_call_started.json')
    assert started['calls'] == 1 and started['method'] == 'highs-ds' and started['time_limit'] == 1800 and started['automatic_reruns'] == 0
    arrays, shapes = load_npz(source/'floating_solver_arrays.npz')
    m, n = planned['shape']; assert n == 21021 and arrays['shape'] == [m, n]
    for key, size in [('primal', n), ('lower_marginals', n), ('upper_marginals', n), ('inequality_marginals', m),
                      ('scales', m), ('equality_marginals', 1), ('computed_row_slacks', m), ('computed_dual_residual', n),
                      ('inequality_residual', m), ('equality_residual', 1), ('lower_residual', n), ('upper_residual', n),
                      ('computed_scaled_slacks', m), ('row_multipliers_unscaled', m), ('normalization_residual', 1)]:
        assert shapes[key] == (size,)
    frozen, frozen_shapes = load_npz(HERE/'floating_problem.npz', names=('scales', 'shape'))
    assert frozen['shape'] == [m, n] and frozen_shapes['scales'] == (m,)
    assert arrays['scales'] == frozen['scales'] and all(math.isfinite(v) and v > 0 for v in arrays['scales'])
    assert arrays['availability_order'] == ['primal', 'row_dual', 'normalization_dual', 'column_lower_dual']
    assert arrays['optimizer_calls'] == [1]
    eligible = bool(numerical['success'] and numerical['status_code'] == 0 and arrays['solver_status_code'] == [0]
        and arrays['solver_success'] == [True] and arrays['availability'] == [1, 1, 1, 1]
        and execution['exit_code'] == 0 and execution['status'] == 'NUMERICAL_DISCOVERY_COMPLETE_NOT_EXACT')
    if eligible:
        for key in ('primal', 'inequality_marginals', 'equality_marginals', 'lower_marginals', 'scales'):
            assert all(math.isfinite(v) for v in arrays[key])
    out.mkdir()
    static = ('exact_matrix.json.gz', 'coordinate_structure.json', 'own_blocks.json',
              'inherited_dual_lower_bound.json', 'recover.py', 'recovery_model.py')
    for name in static: shutil.copyfile(HERE/name, out/name)
    for name in ('floating_solver_arrays.npz', 'numerical_result.json'): shutil.copyfile(source/name, out/name)
    report = {'status': 'PREPARED_FOR_EXACT_RECOVERY' if eligible else 'DISCOVERY_RETAINED_REQUIRES_REVIEW',
        'discovery_directory': str(source.relative_to(WORK)), 'discovery_output_manifest_sha256': sha(source/'output_manifest.json'),
        'verified_discovery_output_files': len(output_manifest['files']), 'verified_actual_runtime_inputs': len(planned['inputs']),
        'required_output_set_verified': sorted(required_outputs), 'unique_safe_output_paths_verified': True,
        'numerical_arrays_digest_matched': True, 'returned_scales_match_frozen_input': True,
        'source_driver_sha256': sha(HERE/'actions_solve.py'), 'shape': [m, n],
        'recovery_inputs': {name: sha(out/name) for name in static + ('floating_solver_arrays.npz', 'numerical_result.json')},
        'eligible_for_standard_recovery': eligible, 'W_float': numerical.get('W_float'),
        'core_columns': 10277, 'real_overlap_core_columns': 420, 'canonical_old_auxiliaries': 10744,
        'optimizer_calls_in_recovery': 0, 'recovery_not_executed': True, 'discovery_unchanged': True,
        'prepared_utc': datetime.now(timezone.utc).isoformat()}
    (out/'recovery_input_manifest.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__': main()
