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
WORK = HERE.parent


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
    for record in planned['inputs']:
        p = HERE/record['name']; assert sha(p) == record['sha256'] and p.stat().st_size == record['bytes']
    output_manifest = read(source/'output_manifest.json')
    for record in output_manifest['files']:
        p = source/record['name']; assert p.is_file() and sha(p) == record['sha256'] and p.stat().st_size == record['bytes']
    execution = read(source/'execution.json'); numerical = read(source/'numerical_result.json')
    assert execution['source_sha256'] == sha(HERE/'actions_solve.py') == sha(source/'executed_actions_solve.py')
    assert numerical['matrix_sha256'] == sha(HERE/'exact_matrix.json.gz')
    assert numerical['floating_problem_sha256'] == sha(HERE/'floating_problem.npz')
    assert numerical['method'] == 'highs-ds' and numerical['optimizer_calls'] == 1
    arrays, shapes = load_npz(source/'floating_solver_arrays.npz')
    m, n = planned['shape']; assert n == 21021 and arrays['shape'] == [m, n]
    for key, size in [('primal', n), ('lower_marginals', n), ('upper_marginals', n), ('inequality_marginals', m),
                      ('scales', m), ('equality_marginals', 1), ('computed_row_slacks', m), ('computed_dual_residual', n)]:
        assert shapes[key] == (size,)
    assert arrays['optimizer_calls'] == [1]
    eligible = bool(numerical['success'] and arrays['solver_success'] == [True] and arrays['availability'] == [1, 1, 1, 1])
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
        'source_driver_sha256': sha(HERE/'actions_solve.py'), 'shape': [m, n],
        'recovery_inputs': {name: sha(out/name) for name in static + ('floating_solver_arrays.npz', 'numerical_result.json')},
        'eligible_for_standard_recovery': eligible, 'W_float': numerical.get('W_float'),
        'core_columns': 10277, 'real_overlap_core_columns': 420, 'canonical_old_auxiliaries': 10744,
        'optimizer_calls_in_recovery': 0, 'recovery_not_executed': True, 'discovery_unchanged': True,
        'prepared_utc': datetime.now(timezone.utc).isoformat()}
    (out/'recovery_input_manifest.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__': main()
