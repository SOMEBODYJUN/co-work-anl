"""Independent small synthetic probes; never a solver or a feasibility claim.

Load only the standard-library recovery/verifier modules under review. All test
fixtures and outputs live in this audit directory. Baseline source snapshots
preserve the exact code in which the provenance gaps were found.
"""
from contextlib import redirect_stdout
from fractions import Fraction as F
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import argparse
import io
import json
import struct
import sys
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def load_module(path, name):
    spec = spec_from_file_location(name, path)
    module = module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def npy(values, descr='<f8', scalar=False):
    formats = {'<f8': 'd', '<i8': 'q', '|b1': '?', '|i1': 'b'}
    shape = () if scalar else (len(values),)
    header = repr({'descr': descr, 'fortran_order': False, 'shape': shape})
    encoded = header.encode('latin1')
    padding = (-(10 + len(encoded) + 1)) % 64
    encoded += b' ' * padding + b'\n'
    if descr.startswith('|S'):
        width = int(descr[2:])
        body = b''.join(value.encode('ascii').ljust(width, b'\x00') for value in values)
    else:
        body = struct.pack('<' + formats[descr] * len(values), *values)
    return b'\x93NUMPY\x01\x00' + len(encoded).to_bytes(2, 'little') + encoded + body


def write_npz(path, arrays):
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, triple in arrays.items():
            values, descr, scalar = triple
            archive.writestr(name + '.npy', npy(values, descr, scalar))


def probe_canonical(source):
    model = load_module(source / 'recovery_model.py', 'recovery_model')
    recover = load_module(source / 'recover.py', 'audit_recover')
    verifier = load_module(source / 'verify_certificates.py', 'audit_verify')
    rows = []
    maxima = []
    minima = []
    for j in range(4849, 12803):
        maxima.append([j, len(rows)])
        rows.append([[0, '-1'], [j, '1']])
    for j in range(12803, 15593):
        i = len(rows)
        rows.extend([[[0, '1'], [j, '-1']], [[1, '1'], [j, '-1']]])
        minima.append({'column': j, 'q_upper_row': i, 'v_upper_row': i + 1})
    structure = {'max_thresholds': maxima, 'min_auxiliaries': minima,
                 'auxiliary_columns': list(range(4849, 15593)),
                 'core_columns': list(range(4849)) + list(range(15593, 21021)),
                 'real_overlap_columns': list(range(20601, 21021))}
    matrix = {'rows': rows}
    initial = [F((j % 19) + 1, 97) for j in range(21021)]
    initial[0], initial[1] = F(3, 5), F(1, 5)
    for j in range(4849, 15593):
        initial[j] = F(99)
    for j in range(20601, 21021):
        initial[j] = F(j - 20600, 4201)
    exact = initial[:]
    recover.canonical_old(matrix, exact, structure)
    assert all(exact[j] == initial[j] for j in structure['core_columns'])
    assert all(exact[j] == F(3, 5) for j in range(4849, 12803))
    assert all(exact[j] == F(1, 5) for j in range(12803, 15593))
    assert verifier.canonical_old(matrix, exact, structure) == 10744
    floating = list(map(float, initial))
    before = floating[:]
    recover.canonical_old(matrix, floating, structure, True)
    assert all(floating[j] == before[j] for j in structure['core_columns'])
    assert all(floating[j] == 0.6 for j in range(4849, 12803))
    assert all(floating[j] == 0.2 for j in range(12803, 15593))

    # Exact own-completion counterexample to the former virtual-min policy.
    x = [F(1), F(0), F(1, 2), F(1, 2), F(0), F(1, 2), F(1, 4), F(1, 4)]
    block = {'block': 0, 'key': ['synthetic'], 'H_column': 0, 'X_column': 5,
             'yQ_column': 6, 'yR_column': 7,
             'mass_by_QR': {'00': [[1, '1']], '10': [[2, '1']], '01': [[3, '1']], '11': [[4, '1']]}}
    witness = verifier.eight_cells(x, [block])[0]
    assert witness['beta'] == '0' and witness['all_eight_cells_nonnegative']
    invalid = x[:]
    invalid[6] = invalid[7] = F(1, 2)
    rejected = False
    try:
        verifier.eight_cells(invalid, [block])
    except AssertionError:
        rejected = True
    assert rejected
    return {'status': 'PASS', 'canonical_max_recomputed': 7954, 'canonical_min_recomputed': 2790,
            'exact_core_values_preserved': 10277, 'float_core_values_preserved': 10277,
            'exact_real_y_values_preserved': 420, 'float_real_y_values_preserved': 420,
            'independent_verifier_old_canonical_checks': 10744,
            'eight_cells_noncanonical_y_accepted': True,
            'eight_cells_invalid_simultaneous_min_rejected': True,
            'synthetic_local_only': True}


def fixture(parent, case):
    root = parent / case
    root.mkdir()
    source = root / 'discovery'
    source.mkdir()
    (root / 'actions_solve.py').write_text('# Synthetic provenance fixture, never executed.\n')
    static = ('exact_matrix.json.gz', 'coordinate_structure.json', 'own_blocks.json',
              'inherited_dual_lower_bound.json', 'recover.py', 'recovery_model.py')
    for name in static:
        (root / name).write_bytes(b'SYNTHETIC_ONLY\n')
    m, n = 2, 21021
    write_npz(root / 'floating_problem.npz', {'scales': ([1., 1.], '<f8', False), 'shape': ([m, n], '<i8', False)})
    inputs = [{'name': name, 'sha256': digest(root / name), 'bytes': (root / name).stat().st_size}
              for name in ('actions_solve.py', 'exact_matrix.json.gz', 'floating_problem.npz')]
    planned = {'shape': [m, n], 'inputs': inputs}
    save(root / 'runtime_inputs_manifest.json', planned)
    actual = {'runtime_inputs_manifest': planned, 'inputs': inputs,
              'driver_sha256': digest(root / 'actions_solve.py'),
              'runtime_inputs_manifest_sha256': digest(root / 'runtime_inputs_manifest.json')}
    save(source / 'actions_input_manifest.json', actual)
    (source / 'executed_actions_solve.py').write_bytes((root / 'actions_solve.py').read_bytes())
    execution = {'source_sha256': digest(root / 'actions_solve.py'), 'exit_code': 0,
                 'status': 'NUMERICAL_DISCOVERY_COMPLETE_NOT_EXACT'}
    if case == 'failed_execution':
        execution.update(exit_code=1, status='FAILED_OUTPUTS_RETAINED')
    save(source / 'execution.json', execution)
    arrays = {'shape': ([m, n], '<i8', False), 'optimizer_calls': ([1], '<i8', True),
              'solver_success': ([True], '|b1', True), 'solver_status_code': ([0], '<i8', True),
              'availability': ([1, 1, 1, 1], '|i1', False),
              'availability_order': (['primal', 'row_dual', 'normalization_dual', 'column_lower_dual'], '|S32', False)}
    for name, size in [('primal', n), ('lower_marginals', n), ('upper_marginals', n),
                       ('inequality_marginals', m), ('equality_marginals', 1),
                       ('computed_row_slacks', m), ('computed_dual_residual', n),
                       ('inequality_residual', m), ('equality_residual', 1),
                       ('lower_residual', n), ('upper_residual', n),
                       ('computed_scaled_slacks', m), ('row_multipliers_unscaled', m),
                       ('normalization_residual', 1)]:
        arrays[name] = ([0.] * size, '<f8', False)
    arrays['scales'] = ([2., 2.] if case == 'wrong_scales' else [1., 1.], '<f8', False)
    write_npz(source / 'floating_solver_arrays.npz', arrays)
    numerical = {'matrix_sha256': digest(root / 'exact_matrix.json.gz'),
                 'floating_problem_sha256': digest(root / 'floating_problem.npz'),
                 'runtime_inputs_manifest_sha256': digest(root / 'runtime_inputs_manifest.json'),
                 'method': 'highs-ds', 'optimizer_calls': 1, 'success': True, 'status_code': 0,
                 'arrays_sha256': digest(source / 'floating_solver_arrays.npz'),
                 'rows': m, 'columns': n}
    if case == 'numerical_array_digest_mismatch':
        numerical['arrays_sha256'] = '0' * 64
    save(source / 'numerical_result.json', numerical)
    save(source / 'optimizer_call_started.json', {'calls': 1, 'method': 'highs-ds', 'time_limit': 1800, 'automatic_reruns': 0})
    for name in ('solver_stdout.txt', 'solver_stderr.txt', 'progress.jsonl'):
        (source / name).write_text('')
    files = [{'name': p.name, 'sha256': digest(p), 'bytes': p.stat().st_size}
             for p in sorted(source.iterdir()) if p.is_file()]
    if case == 'missing_manifest_array':
        files = [record for record in files if record['name'] != 'floating_solver_arrays.npz']
    if case == 'duplicate_manifest_name':
        files.append(dict(files[0]))
    save(source / 'output_manifest.json', {'files': files, 'exact_verified': False})
    return root, source


def probe_prepare(source, expected):
    load_module(source / 'recovery_model.py', 'recovery_model')
    prepare = load_module(source / 'prepare_recovery.py', 'audit_prepare_recovery')
    result = {}
    with tempfile.TemporaryDirectory(prefix='probe-fixtures-', dir=HERE) as tmp:
        for case in ('control_valid', 'missing_manifest_array', 'numerical_array_digest_mismatch',
                     'wrong_scales', 'failed_execution', 'duplicate_manifest_name'):
            root, discovery = fixture(Path(tmp), case)
            prepare.HERE = root
            prepare.WORK = root.parent
            old_argv = sys.argv
            sys.argv = ['prepare_recovery.py', '--discovery', str(discovery), '--output', 'accepted']
            rejected = False
            reason = None
            try:
                with redirect_stdout(io.StringIO()):
                    prepare.main()
            except (AssertionError, KeyError, ValueError) as exc:
                rejected = True
                reason = repr(exc)
            finally:
                sys.argv = old_argv
            report_path = root / 'accepted/recovery_input_manifest.json'
            eligible = json.loads(report_path.read_text()).get('eligible_for_standard_recovery') if report_path.exists() else False
            result[case] = {'rejected': rejected, 'eligible': eligible, 'rejection_reason': reason}
            if expected == 'baseline' or case == 'control_valid':
                assert not rejected and eligible, (case, result[case])
            else:
                assert rejected or not eligible, (case, result[case])
    return {'status': 'GAPS_REPRODUCED' if expected == 'baseline' else 'MALFORMED_DISCOVERY_REJECTED',
            'cases': result, 'optimizer_calls': 0, 'synthetic_only': True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=HERE / 'baseline_sources')
    parser.add_argument('--expected', choices=('baseline', 'hardened'), default='baseline')
    parser.add_argument('--output', type=Path, default=HERE / 'baseline_probe_results.json')
    args = parser.parse_args()
    args.source = args.source.resolve()
    args.output = args.output.resolve()
    assert args.output.is_relative_to(HERE) and not args.output.exists()
    result = {'source_directory': str(args.source),
              'probe_sha256': digest(Path(__file__)),
              'source_sha256': {name: digest(args.source / name) for name in
                                ('recover.py', 'recovery_model.py', 'prepare_recovery.py', 'verify_certificates.py')},
              'canonical_and_eight_cells': probe_canonical(args.source),
              'discovery_acceptance': probe_prepare(args.source, args.expected),
              'optimizer_calls': 0, 'matrix_generator_called': False,
              'new_feasible_point_claimed': False}
    save(args.output, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
