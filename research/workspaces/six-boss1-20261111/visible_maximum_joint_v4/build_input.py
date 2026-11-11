#!/usr/bin/env python3
"""Literal frozen-source assembly only. Standard library; zero optimizers."""
from collections import Counter
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = HERE.parents[3]
BASE = WS / 'visible_maximum_joint_v3'
FAMILY = WS / 'all_source_joint_reweighted_safe'
DIRECT = {
    'visible_maximum_joint_v3/exact_input.json': 'c5ddba49b71303083b07b96f90888d56f11b291d7c307f0c3e8280b7385d280e',
    'visible_maximum_joint_v3/freeze_manifest.json': 'f7cf345480b2d0c328a12a3485b0ad9d66c260f611b6c6e5253a16b361c857f9',
    'visible_maximum_joint_v3/numerical_scaling.json': 'bfc80e07700239cde34b2d0005e591e2abef7726dfd7e3c69db48df52375cbb9',
    'all_source_joint_reweighted_safe/exact_family.json': 'c8a40df9458e2add557ef14b8282880a1d14b05d55238ecf0715f63968907c18',
    'all_source_joint_reweighted_safe/freeze_manifest.json': '3f08170af4b678688317bdebfd8468a8c62e8a801923b3e86f7612a8873825eb',
    'all_source_joint_reweighted_safe/proof.md': '1a72e75cbcfa36d215c5030d1b86426746d068c1afc806894272b5c9aca60f70',
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def write(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def identity_report(rows):
    seen = {}
    duplicates, zeros = [], []
    for index, row in enumerate(rows):
        vector = tuple(Fraction(row['a'].get(str(j), '0')) for j in range(513))
        rhs = Fraction(row['rhs'])
        key = (vector, rhs)
        if not any(vector) and rhs == 0:
            zeros.append({'raw_index': index, 'name': row['name']})
        if key in seen:
            first = seen[key]
            duplicates.append({'raw_index': index, 'name': row['name'],
                               'first_raw_index': first, 'first_name': rows[first]['name']})
        else:
            seen[key] = index
    nonzero = sum(bool(any(vector)) or rhs != 0 for vector, rhs in seen)
    return {'raw_rows': len(rows), 'zero_rows': zeros,
            'duplicate_rows': duplicates, 'duplicate_count': len(duplicates),
            'distinct_nonzero_affine_rows': nonzero,
            'all_raw_rows_retained': True, 'diagnostic_only': True,
            'pruning_performed': False}


def main():
    assert not (HERE / 'freeze_manifest.json').exists(), 'Frozen package cannot be rebuilt.'
    assert not (HERE / 'exact_input.json').exists(), 'Refuse to replace a prepared input.'
    for name, digest in DIRECT.items():
        assert sha(WS / name) == digest, name
    baseline = read(BASE / 'exact_input.json')
    old_scales = read(BASE / 'numerical_scaling.json')
    source = read(FAMILY / 'exact_family.json')
    base_manifest = read(BASE / 'freeze_manifest.json')
    family_manifest = read(FAMILY / 'freeze_manifest.json')
    assert base_manifest['solve_consumption'] == 'NO_SOLVE_INTERMEDIATE_INPUT'
    assert family_manifest['status'] == 'FROZEN_COMPLETE_ALL_SOURCE_JOINT_REWEIGHTED_67_VERTICES_536_ROWS_NO_SOLVE'
    assert family_manifest['optimizer_calls'] == 0
    assert family_manifest['family']['sha256'] == DIRECT['all_source_joint_reweighted_safe/exact_family.json']
    assert len(baseline['raw_rows']) == 1050 and len(source['rows']) == 536

    pins = {}

    def pin(path, digest):
        key = str(path.resolve().relative_to(REPO))
        if key in pins:
            assert pins[key] == digest, key
        assert sha(path) == digest, key
        pins[key] = digest

    for name, digest in DIRECT.items():
        pin(WS / name, digest)
    for name, digest in read(BASE / 'source_pins.json')['sources'].items():
        pin(REPO / name, digest)
    for name, digest in base_manifest['artifacts'].items():
        pin(BASE / name, digest)
    pin(BASE / 'SHA256SUMS', '3153ccaa8f7e802532259af5fad37ef40ff42ff40349689af8a47cb54145cef4')
    for name, description in family_manifest['artifacts'].items():
        pin(REPO / name, description['sha256'])
    for section in ('source_sha256', 'prior_frozen_artifact_sha256'):
        for name, digest in family_manifest[section].items():
            pin(REPO / name, digest)
    if (FAMILY / 'SHA256SUMS').is_file():
        pin(FAMILY / 'SHA256SUMS', sha(FAMILY / 'SHA256SUMS'))
    source_pins = {'status': 'PREPARED_NO_OPTIMIZER', 'sources': dict(sorted(pins.items())),
                   'pinned_by_assignment': DIRECT,
                   'binding_gate': 'Both source packages were finally frozen before any input assembly.',
                   'source_packages': ['visible_maximum_joint_v3', 'all_source_joint_reweighted_safe']}
    write('source_pins.json', source_pins)

    expected_columns = {str(j) for j in range(513)}
    roles = [f'A{i}' for i in range(1, 7)] + ['X', 'C']
    assert source['T_roles'] == roles
    assert source['variables'] == baseline['variables'] == 513
    assert source['K_column'] == baseline['K_column'] == 512
    assert source['bit_order'] == baseline['bit_order']
    assert Counter(r['source'] for r in source['rows']) == {1: 312, 2: 128, 3: 64, 4: 32}
    for row in source['rows']:
        assert set(row['a']) == expected_columns
        assert row['rhs'] == '0' and row['numerical_divisor'] == '25'
        assert row['uses_C_size_equality'] is False
        assert Fraction(row['a']['512']) == Fraction(7 - row['source'], 2)
        for value in row['a'].values():
            Fraction(value)
    rows = deepcopy(baseline['raw_rows']) + deepcopy(source['rows'])
    assert len({r['name'] for r in rows}) == len(rows) == 1586
    preserved = ('variables', 'bit_order', 'atom_columns', 'K_column', 'nonnegative_columns',
                 'objective', 'equalities', 'equality_count', 'inequality_convention')
    result = {k: deepcopy(baseline[k]) for k in preserved}
    result.update({
        'schema': 'visible_maximum_joint_v4_exact_v1', 'status': 'PREPARED_NO_OPTIMIZER',
        'optimizer_calls': 0,
        'scope': 'Full 512 actual/X/O-union/C types plus independent K; unchanged 1050 raw rows followed by all536 frozen general-source pure-role rows.',
        'raw_inequality_count': 1586, 'raw_rows': rows,
        'raw_row_policy': 'All1050 baseline and all536 source dictionaries literal, including every explicit zero and duplicate; no pruning, C-equality elimination or numeric scaling of exact rows.',
        'baseline_metadata': {k: deepcopy(v) for k, v in baseline.items() if k != 'raw_rows'},
        'source_family_metadata': {k: deepcopy(v) for k, v in source.items() if k != 'rows'},
        'source_bindings': DIRECT,
        'source_pins_sha256': sha(HERE / 'source_pins.json'),
        'source_review_sha256': sha(HERE / 'source_review.md'),
        'append_contract': {'baseline_raw_count': 1050, 'complete_family_raw_count': 536,
                            'appended_raw_indices': [1050, 1585], 'source_row_counts': {'1': 312, '2': 128, '3': 64, '4': 32},
                            'source_index_plus': 1050, 'excluded_source_rows': [],
                            'new_numerical_positive_divisor': '25', 'K_column_original_ci': True},
        'preparation_only': {'optimization_authorized': False, 'point_conditioned': False,
                             'K_fixed': False, 'support_restricted': False, 'C_equality_eliminated_in_new_rows': False,
                             'SPE_sufficiency_claimed': False, 'half_status': 'OPEN',
                             'future_release_owner': 'Main', 'baseline1050_solve_status': 'NO_SOLVE'}
    })
    write('exact_input.json', result)
    for filename in ('column_routing.json', 'column_routing.tsv'):
        (HERE / filename).write_bytes((BASE / filename).read_bytes())

    raw_order = [r['name'] for r in rows]
    scales = deepcopy(old_scales['raw_scales'])
    for row in source['rows']:
        scales[row['name']] = '25'
    assert len(scales) == len(raw_order) == 1586
    assert all(Fraction(v) > 0 for v in scales.values())
    write('numerical_scaling.json', {
        'status': 'PREPARED_NO_OPTIMIZER', 'raw_order': raw_order, 'raw_scales': scales,
        'baseline_scaling_metadata': {k: deepcopy(v) for k, v in old_scales.items() if k not in ('raw_order', 'raw_scales')},
        'scope': 'Numerical divisor only; exact_input retains all original unscaled coefficient strings.',
        'v4_append': {'old_scale_strings_literal': 1050, 'new_rows': 536, 'new_positive_divisor': '25',
                      'actual_source_IC_weight_may_differ': True, 'source_raw_terminal_BR_mean_weight': '1'}
    })
    catalog = deepcopy(read(BASE / 'row_catalog.json'))
    for index, row in enumerate(source['rows']):
        entry = {k: deepcopy(v) for k, v in row.items() if k != 'a'}
        entry.update(raw_index=1050 + index, source_row_index=index,
                     source_package='all_source_joint_reweighted_safe', stored_coefficient_entries=len(row['a']))
        catalog.append(entry)
    write('row_catalog.json', catalog)
    columns = ['raw_index', 'name', 'family', 'numerical_divisor', 'source_package', 'source_row_index', 'source', 'vertex_id', 'T']
    with (HERE / 'row_catalog.tsv').open('w') as handle:
        handle.write('\t'.join(columns) + '\n')
        for entry in catalog:
            handle.write('\t'.join(str(entry.get(k, '')) for k in columns) + '\n')
    write('raw_identity_diagnostics.json', identity_report(rows))
    for name, digest in pins.items():
        assert sha(REPO / name) == digest, name
    output = {'status': 'PREPARED_NO_OPTIMIZER', 'result': 'LITERAL_ASSEMBLY_COMPLETE_AWAITING_INDEPENDENT_CHECK',
              'input_sha256': sha(HERE / 'exact_input.json'), 'raw_rows': 1586, 'columns': 513, 'equalities': 2,
              'baseline_literal_rows': 1050, 'source_literal_rows': 536, 'source_files_verified_unchanged': len(pins),
              'source_was_finally_frozen': True, 'optimizer_calls': 0, 'point_values_loaded_or_bound': False,
              'source_programs_executed_or_imported': False}
    write('build_result.json', output)
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
