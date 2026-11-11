"""Targeted final-51 interface and inherited-core audit; standard library only.

This does not redo the 3.3M-coefficient baseline audit or any optimization.
It checks all 5124 new coefficients, the fixed column partition, and exact
frozen input hashes. Final NPZ checks inspect only its 51-row appended tail.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import argparse
import ast
import gzip
import json
import struct
import sys
import zipfile

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = WORK.parents[2]
BASE = WORK / 'common_x_joint_lp'
NEW_PIN = '1a1876a01a505e74b1497fc1ac1ad62400b93bf648f53bf9966fc630f13b770c'
BASE_PIN = '77781e837b86d7ec8e85634935377fd8183e4c3e945120dc4dd368a40bb1d09c'


def sha(p):
    return sha256(p.read_bytes()).hexdigest()


def read(p):
    with gzip.open(p, 'rt') if p.suffix == '.gz' else p.open() as stream:
        return json.load(stream)


def encoded(values):
    return [[j, str(v)] for j, v in sorted(values.items()) if v]


def npy_tail(path, name, start_index):
    with zipfile.ZipFile(path) as archive:
        with archive.open(name + '.npy') as stream:
            magic = stream.read(8)
            assert magic[:6] == b'\x93NUMPY' and magic[6:] in (b'\x01\x00', b'\x02\x00', b'\x03\x00')
            hlen_size = 2 if magic[6] == 1 else 4
            hlen = int.from_bytes(stream.read(hlen_size), 'little')
            header = ast.literal_eval(stream.read(hlen).decode('latin1').strip())
            assert header['fortran_order'] is False and len(header['shape']) == 1
            descr = header['descr']
            assert descr in ('<f8', '<i8')
            count = header['shape'][0]
            assert 0 <= start_index <= count
            stream.seek(8 + hlen_size + hlen + 8 * start_index)
            tail = stream.read()
            assert len(tail) == 8 * (count - start_index)
            return [v[0] for v in struct.iter_unpack('<d' if descr == '<f8' else '<q', tail)]


def interface_check():
    new_path = WORK / 'main_prefix_maxx_interface/rows_51.json'
    assert sha(new_path) == NEW_PIN
    package = read(new_path)
    old = read(WORK / 'early_x_anchor_queries/rows_51.json')
    columns = read(WORK / 'early_x_anchor_queries/columns_21021.json.gz')
    third = read(WORK / 'early3_maxx_cone/rows_17.json')
    assert len(columns) == 21021
    hist = {j: c for j, c in enumerate(columns[:4849]) if c['kind'] == 'hist'}
    xc = {c['hist_column']: j for j, c in enumerate(columns) if c['kind'] == 'common-X-mass'}
    assert len(hist) == len(xc) == 16
    safe = {}
    for i in (1, 2, 3):
        values = defaultdict(F)
        for h, desc in hist.items():
            bits = tuple(map(int, desc['actual_bits']))
            if bits[i - 1]:
                values[h] += F(1, sum(bits))
            values[xc[h]] -= F(1, sum(bits[:i - 1]) + 7 - i)
        safe[i] = dict(values)
        assert encoded(values) == package['safe_rows_from_raw_bits'][str(i)]
    constants = {1: F(206, 5), 2: F(121, 4), 3: F(61, 3)}
    deltas = {1: F(9, 5), 2: F(9, 4), 3: F(8, 3)}
    assert len(package['rows']) == len(old['rows']) == 51
    assert len(third['rows']) == 17
    occurrence = Counter()
    for k, (new_row, old_row) in enumerate(zip(package['rows'], old['rows'])):
        i = new_row['actual_player']
        assert i == old_row['actual_player'] == k // 17 + 1
        assert F(new_row['C']) == constants[i]
        assert F(new_row['safe_subtraction']) == deltas[i]
        assert F(old_row['C']) - constants[i] == deltas[i]
        assert new_row['query_members'] == old_row['query_members']
        assert new_row['histogram_frequencies'] == old_row['histogram_frequencies']
        assert F(new_row['rhs']) == 0
        expected = defaultdict(F, {j: F(v) for j, v in old_row['row']})
        for j, value in safe[i].items():
            expected[j] -= deltas[i] * value
        assert encoded(expected) == new_row['row']
        assert all(not (4849 <= j < 15593) for j, value in new_row['row'])
        assert {j for j, value in new_row['row'] if 20585 <= j < 20601} == set(range(20585, 20601))
        old_y = {j: value for j, value in old_row['row'] if j >= 20601}
        new_y = {j: value for j, value in new_row['row'] if j >= 20601}
        assert old_y == new_y and all(F(value) > 0 for value in new_y.values())
        occurrence.update(new_y.keys())
        if i == 3:
            assert new_row['row'] == third['rows'][k - 34]['row']
    assert set(occurrence) == set(range(20601, 21021)) and set(occurrence.values()) == {3}
    assert sum(len(row['row']) for row in package['rows']) == 5124
    return package, {'status': 'PASS', 'rows': 51, 'nonzeros': 5124,
        'new_package_sha256': NEW_PIN, 'constants': {str(i): str(v) for i, v in constants.items()},
        'safe_rows_rebuilt_from_raw_descriptors': 3, 'all_new_equals_old_minus_delta_safe': 51,
        'third_rows_equal_independent_early3_packet': 17, 'all16_X_columns_in_every_row': True,
        'all420_real_overlap_coefficients_unchanged': True, 'each_real_overlap_appears': 3,
        'old_auxiliary_coefficients_in_new_rows': 0, 'old_point_weights_read': False,
        'mathematical_1440_atom_enumeration_rerun': False}


def final_check(package):
    final = BASE / 'final'
    assert final.is_dir()
    assert sha(BASE / 'exact_matrix.json.gz') == BASE_PIN
    structure = read(final / 'coordinate_structure.json')
    base_structure = read(BASE / 'coordinate_structure.json')
    assert structure['shape'] == [23676, 21021]
    assert structure['matrix_sha256'] == sha(final / 'exact_matrix.json.gz')
    for key, value in base_structure.items():
        if key not in ('shape', 'matrix_sha256'):
            assert structure[key] == value, key
    assert len(structure['core_columns']) == 10277 and len(structure['auxiliary_columns']) == 10744
    assert structure['real_overlap_columns'] == structure['forbidden_canonical_min_columns'] == list(range(20601, 21021))
    old_blocks = read(BASE / 'own_blocks.json')
    blocks = read(final / 'own_blocks.json')
    assert len(blocks['blocks']) == len(old_blocks['blocks']) == 210
    assert blocks['blocks'] == old_blocks['blocks']
    assert blocks['matrix_sha256'] == structure['matrix_sha256']
    for key in ('row_multipliers', 'residuals', 'normalization_multiplier'):
        assert read(final / 'inherited_dual_lower_bound.json')[key] == read(BASE / 'inherited_dual_lower_bound.json')[key]

    spec = spec_from_file_location('audit_final_npz_reader', final / 'recovery_model.py')
    mod = module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    selected = ('shape', 'scales', 'indptr', 'objective', 'normalization', 'inequality_rhs', 'normalization_rhs')
    floating, shapes = mod.load_npz(final / 'floating_problem.npz', names=selected)
    old_float, _ = mod.load_npz(BASE / 'floating_problem.npz', names=selected)
    assert floating['shape'] == [23676, 21021]
    assert floating['scales'][:23625] == old_float['scales']
    assert floating['indptr'][:23626] == old_float['indptr']
    assert floating['objective'] == old_float['objective']
    assert floating['normalization'] == old_float['normalization']
    assert floating['normalization_rhs'] == [1.0] and all(v == 0.0 for v in floating['inequality_rhs'])
    offset = floating['indptr'][23625]
    assert offset == 3308634 and floating['indptr'][-1] == 3313758
    tail_data = npy_tail(final / 'floating_problem.npz', 'data', offset)
    tail_indices = npy_tail(final / 'floating_problem.npz', 'indices', offset)
    for k, row in enumerate(package['rows']):
        lo, hi = floating['indptr'][23625 + k] - offset, floating['indptr'][23626 + k] - offset
        values = [float(F(value)) for j, value in row['row']]
        scale = max(abs(v) for v in values)
        assert floating['scales'][23625 + k] == scale
        assert tail_indices[lo:hi] == [j for j, value in row['row']]
        assert tail_data[lo:hi] == [-value / scale for value in values]

    runtime = read(final / 'runtime_inputs_manifest.json')
    request = read(final / 'actions_request.json')
    assert runtime['shape'] == [23676, 21021] and runtime['nonzeros'] == 3313758
    expected = {'actions_solve.py', 'exact_matrix.json.gz', 'floating_problem.npz',
                'structure_and_lower_verification.json', 'inputs_manifest.json'}
    assert {r['name'] for r in runtime['inputs']} == expected and len(runtime['inputs']) == 5
    for record in runtime['inputs']:
        path = final / record['name']
        assert sha(path) == record['sha256'] and path.stat().st_size == record['bytes']
    required = request['required_inputs']
    assert len(required) == 6
    assert {Path(r['path']).name for r in required} == expected | {'runtime_inputs_manifest.json'}
    for record in required:
        path = REPO / record['path']
        assert path.resolve().parent == final.resolve()
        assert sha(path) == record['sha256'] and path.stat().st_size == record['bytes']
    audit = read(final / 'structure_and_lower_verification.json')
    assert audit['status'] == 'PASS' and audit['rows'] == 23676 and audit['columns'] == 21021
    assert audit['matrix_sha256'] == structure['matrix_sha256']
    assert request['argv'][2] == str((final / 'actions_solve.py').relative_to(REPO))
    return {'status': 'PASS', 'shape': [23676, 21021], 'nonzeros': 3313758,
        'matrix_sha256': structure['matrix_sha256'], 'floating_sha256': sha(final / 'floating_problem.npz'),
        'all_core_and_auxiliary_metadata_inherited': True, 'own_blocks_inherited': 210,
        'inherited_dual_multipliers_and_all_residuals_unchanged': True,
        'old_scales_indptr_objective_normalization_unchanged': True,
        'appended_npz_rows_independently_checked': 51, 'appended_npz_coefficients_checked': 5124,
        'five_runtime_files_plus_manifest_bound': True,
        'runtime_manifest_sha256': sha(final / 'runtime_inputs_manifest.json'),
        'actions_request_sha256': sha(final / 'actions_request.json'),
        'independent_existing_full_verification_sha256': sha(final / 'structure_and_lower_verification.json'),
        'whole_old_matrix_coefficients_rerun': False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--final', action='store_true')
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    out = args.output.resolve()
    assert out.is_relative_to(HERE) and not out.exists()
    package, interface = interface_check()
    result = {'interface': interface, 'optimizer_calls': 0,
              'probe_sha256': sha(Path(__file__)), 'new_feasible_point_claimed': False}
    if args.final:
        result['final'] = final_check(package)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
