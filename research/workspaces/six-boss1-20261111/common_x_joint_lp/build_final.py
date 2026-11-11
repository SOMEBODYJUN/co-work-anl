"""Append only Main's approved, frozen 51 stronger prefix rows.

The 23625-row baseline is read-only. This builds a separate final/ version;
it does not dispatch, optimize, or perform rational recovery.
"""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import copy
import gzip
import io
import json
import shutil
import numpy as np

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = WORK.parents[2]
OUT = HERE/'final'
BASE_SHA = '77781e837b86d7ec8e85634935377fd8183e4c3e945120dc4dd368a40bb1d09c'
ROWS_SHA = '1a1876a01a505e74b1497fc1ac1ad62400b93bf648f53bf9966fc630f13b770c'
FREEZE_SHA = 'f62812138600f7be7d1670f3455522989e01dbefd87eb692afce6cea4d868065'
RELEASE = 'Main message authorizing the independently reviewed frozen main_prefix_maxx_interface 51 rows: final23676 x21021,3313758 nnz, zero new columns; no duplicate early3 packet.'


def sha(p): return sha256(p.read_bytes()).hexdigest()


def read(p):
    with gzip.open(p, 'rt', encoding='utf-8') if p.suffix == '.gz' else p.open() as f: return json.load(f)


def save(name, value):
    p = OUT/name; assert not p.exists(); p.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')


def main():
    assert not OUT.exists(), 'Never overwrite a final version.'
    assert sha(HERE/'exact_matrix.json.gz') == BASE_SHA
    assert sha(WORK/'main_prefix_maxx_interface/rows_51.json') == ROWS_SHA
    assert sha(WORK/'main_prefix_maxx_interface/freeze_manifest.json') == FREEZE_SHA
    original_manifest = read(HERE/'inputs_manifest.json')
    for name, pin in original_manifest['generated_inputs'].items(): assert sha(HERE/name) == pin, name
    independent = read(WORK/'early3_maxx_cone/audit_main_family.json')
    assert independent['status'] == 'PASS_INDEPENDENT_MAIN_FAMILY_AUDIT'
    assert independent['raw_ordered_boolean_types'] == 1440 and independent['actual_share_payment_checks'] == 2880
    for name, pin in independent['source_sha256'].items(): assert sha(WORK/name) == pin
    stronger = read(WORK/'main_prefix_maxx_interface/rows_51.json')
    assert (stronger['row_count'], stronger['nonzero_count'], stronger['new_columns'], stronger['full_dimension']) == (51, 5124, 0, 21021)
    for name, pin in stronger['source_sha256'].items(): assert sha(WORK/name) == pin, name
    matrix = read(HERE/'exact_matrix.json.gz'); assert len(matrix['rows']) == 23625
    additions = [r['row'] for r in stronger['rows']]
    assert sum(map(len, additions)) == 5124
    assert all(F(r['rhs']) == 0 for r in stronger['rows'])
    assert all(j < 4849 or 20585 <= j < 21021 for row in additions for j, v in row)
    matrix['rows'] = matrix['rows'] + additions
    matrix['row_names'] = matrix['row_names'] + [json.dumps(r['name'], separators=(',', ':')) for r in stronger['rows']]
    assert len(matrix['rows']) == len(set(matrix['row_names'])) == 23676
    assert sum(map(len, matrix['rows'])) == 3313758
    matrix['baseline_rows'] = 23625; matrix['this_round_added_rows'] = 51
    matrix['last_frozen_baseline_sha256'] = BASE_SHA
    matrix['stronger_prefix_rows_sha256'] = ROWS_SHA
    matrix['stronger_prefix_constants'] = stronger['constants_by_actual_player']
    matrix['main_release_reference'] = RELEASE
    OUT.mkdir()
    with (OUT/'exact_matrix.json.gz').open('wb') as raw:
        with gzip.GzipFile(fileobj=raw, filename='', mode='wb', mtime=0) as z:
            with io.TextIOWrapper(z, encoding='utf-8') as f: json.dump(matrix, f, ensure_ascii=False, separators=(',', ':'))
    matrix_sha = sha(OUT/'exact_matrix.json.gz')
    structure = read(HERE/'coordinate_structure.json'); structure['shape'] = [23676, 21021]; structure['matrix_sha256'] = matrix_sha
    save('coordinate_structure.json', structure)
    own = read(HERE/'own_blocks.json'); own['matrix_sha256'] = matrix_sha; save('own_blocks.json', own)
    mapping = read(HERE/'append_mapping.json'); mapping['row_ranges_half_open']['stronger_prefix_SAFE_MAX'] = [23625, 23676]
    mapping['records'] += [{'source': 'stronger_prefix_SAFE_MAX', 'source_local_row': k, 'global_row': 23625+k,
        'name': matrix['row_names'][23625+k], 'source_hypothetical_append_index': None} for k in range(51)]
    save('append_mapping.json', mapping)
    dual = read(HERE/'inherited_dual_lower_bound.json'); dual['zero_extended_row_range_half_open'] = [22297, 23676]
    dual['zero_extended_row_count'] = 1379; dual['matrix_sha256'] = matrix_sha; save('inherited_dual_lower_bound.json', dual)
    with np.load(HERE/'floating_problem.npz', allow_pickle=False) as archive: arrays = {k: archive[k] for k in archive.files}
    indices = []; data = []; scales = []; ends = []; count = len(arrays['data'])
    for row in additions:
        values = [float(F(v)) for j, v in row]; scale = max(map(abs, values)); scales.append(scale)
        indices.extend(j for j, v in row); data.extend(-v/scale for v in values); count += len(row); ends.append(count)
    arrays['indices'] = np.concatenate((arrays['indices'], np.asarray(indices, dtype=np.int64)))
    arrays['data'] = np.concatenate((arrays['data'], np.asarray(data)))
    arrays['indptr'] = np.concatenate((arrays['indptr'], np.asarray(ends, dtype=np.int64)))
    arrays['scales'] = np.concatenate((arrays['scales'], np.asarray(scales)))
    arrays['shape'] = np.asarray([23676, 21021], dtype=np.int64); arrays['inequality_rhs'] = np.zeros(23676)
    np.savez_compressed(OUT/'floating_problem.npz', **arrays)
    sources = {record['path']: record for record in original_manifest['source_files']}
    extra = ['main_prefix_maxx_interface/rows_51.json', 'main_prefix_maxx_interface/freeze_manifest.json',
        'main_prefix_safety_maxx_family.md', 'main_prefix_safety_maxx_family.py', 'main_prefix_safety_maxx_family.json',
        'early3_maxx_cone/audit_main_family.json', 'early3_maxx_cone/audit_main_family.py', 'early3_maxx_cone/rows_17.json']
    extra += ['common_x_joint_lp/'+name for name in ['exact_matrix.json.gz', 'floating_problem.npz',
        'structure_and_lower_verification.json', 'coordinate_structure.json', 'own_blocks.json',
        'inherited_dual_lower_bound.json', 'append_mapping.json', 'inputs_manifest.json']]
    for name in extra:
        path = str((WORK/name).relative_to(REPO)); sources[path] = {'path': path, 'sha256': sha(WORK/name), 'bytes': (WORK/name).stat().st_size}
    generated = ('exact_matrix.json.gz', 'floating_problem.npz', 'coordinate_structure.json', 'own_blocks.json', 'append_mapping.json', 'inherited_dual_lower_bound.json')
    save('inputs_manifest.json', {'source_files': list(sources.values()), 'generated_inputs': {name: sha(OUT/name) for name in generated},
        'shape': [23676, 21021], 'nonzeros': 3313758, 'assembler_sha256': sha(Path(__file__)),
        'main_release_reference': RELEASE, 'optimizer_calls': 0})
    for name in ('recover.py', 'recovery_model.py', 'prepare_recovery.py', 'recovery_contract.md'):
        text = (HERE/name).read_text()
        if name == 'prepare_recovery.py': text = text.replace('WORK = HERE.parent\n', 'WORK = HERE.parents[1]\n')
        (OUT/name).write_text(text)
    for name in ('actions_solve.py', 'prepare_actions.py'):
        text = (HERE/name).read_text().replace('REPO = HERE.parents[3]', 'REPO = HERE.parents[4]')
        text = text.replace('23625', '23676').replace('3308634', '3313758')
        (OUT/name).write_text(text)
    save('assembly_verification.json', {'status': 'ASSEMBLED_REQUIRES_INDEPENDENT_FINAL_AUDIT', 'rows': 23676, 'columns': 21021,
        'nonzeros': 3313758, 'unchanged_baseline_rows': 23625, 'unchanged_baseline_columns': 21021, 'added_rows': 51,
        'added_columns': 0, 'matrix_sha256': matrix_sha, 'baseline_matrix_sha256': BASE_SHA,
        'stronger_prefix_rows_sha256': ROWS_SHA, 'main_release_reference': RELEASE, 'optimizer_calls': 0})
    assert sha(HERE/'exact_matrix.json.gz') == BASE_SHA
    print(json.dumps(read(OUT/'assembly_verification.json'), indent=2))


if __name__ == '__main__': main()
