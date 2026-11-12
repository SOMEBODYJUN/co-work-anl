#!/usr/bin/env python3
"""Literal v5 assembly, gated on Main's later complete-source release.

Stage 1 never executes complete assembly. No optimizer, source program execution,
candidate values, row selection, equality elimination, or freeze operation.
"""
from collections import Counter
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = HERE.parents[3]
PRESERVED = (
    'variables', 'bit_order', 'atom_columns', 'K_column', 'nonnegative_columns',
    'objective', 'equalities', 'equality_count', 'inequality_convention',
)
OUTPUTS = (
    'exact_input.json', 'numerical_scaling.json', 'source_pins.json',
    'column_routing.json', 'column_routing.tsv', 'row_catalog.json',
    'row_catalog.tsv', 'raw_identity_diagnostics.json', 'build_result.json',
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def order_sha(rows):
    names = [r['name'] for r in rows]
    payload = json.dumps(names, ensure_ascii=False, separators=(',', ':')) + '\n'
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()


def valid_digest(value):
    return (isinstance(value, str) and len(value) == 64
            and all(c in '0123456789abcdef' for c in value))


def at_path(value, keys):
    assert isinstance(keys, list) and keys
    for key in keys:
        value = value[key]
    return value


def final_pending_packages(contract, release):
    decisions = release['pending_source_decisions']
    assert set(decisions) == {p['id'] for p in contract['pending_sources']}
    included = []
    for pending in contract['pending_sources']:
        decision = decisions[pending['id']]
        assert isinstance(decision['include'], bool)
        if pending['required_in_final_input']:
            assert decision['include'] is True, pending['id']
        if decision['include']:
            package = decision['package']
            assert isinstance(package, str) and package and all(c.islower() or c.isdigit() or c == '_' for c in package)
            if pending['package'] is not None:
                assert package == pending['package']
            included.append(package)
        else:
            assert pending['required_in_final_input'] is False
            assert decision['main_reason'], 'An optional omission is an explicit Main decision.'
    assert len(included) == len(set(included))
    return included


def write_new(name, value):
    with (HERE / name).open('x', encoding='utf-8') as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write('\n')


def local_file(package, filename):
    assert isinstance(filename, str) and Path(filename).name == filename, filename
    path = WS / package / filename
    assert path.resolve().parent == (WS / package).resolve(), path
    return path


def diagnostics(rows):
    first_seen, zeros, duplicates = {}, [], []
    for index, row in enumerate(rows):
        vector = tuple(Fraction(row['a'].get(str(j), '0')) for j in range(513))
        key = (vector, Fraction(row['rhs']))
        if not any(vector) and key[1] == 0:
            zeros.append({'raw_index': index, 'name': row['name']})
        if key in first_seen:
            first = first_seen[key]
            duplicates.append({'raw_index': index, 'name': row['name'],
                               'first_raw_index': first, 'first_name': rows[first]['name']})
        else:
            first_seen[key] = index
    return {
        'raw_rows': len(rows), 'zero_rows': zeros, 'duplicate_rows': duplicates,
        'duplicate_count': len(duplicates),
        'distinct_nonzero_affine_rows': sum(bool(any(v)) or rhs != 0 for v, rhs in first_seen),
        'rhs_counts': dict(Counter(r['rhs'] for r in rows)),
        'all_raw_rows_retained': True, 'diagnostic_only': True, 'pruning_performed': False,
    }


def main():
    # The release gate is checked before reading any pending source directory.
    release_path = HERE / 'final_release.json'
    if not release_path.is_file():
        raise SystemExit('WAITING_MAIN_FINAL_RELEASE: no complete input is assembled in stage 1.')
    contract = read(HERE / 'preparation_contract.json')
    release = read(release_path)
    assert release['schema'] == 'visible_maximum_joint_v5_main_release_v1'
    assert release['status'] == 'MAIN_RELEASED_COMPLETE_SOURCE_ASSEMBLY'
    assert release['owner'] == 'Boss1/Main'
    assert release['assembly_authorized'] is True
    assert release['optimizer_authorized'] is False
    assert release['freeze_authorized'] is False
    assert release['final_source_review_complete'] is True
    assert valid_digest(release['final_source_review_sha256'])
    assert sha(HERE / 'source_review.md') == release['final_source_review_sha256']
    assert (HERE / 'source_review.md').read_text(encoding='utf-8').startswith('# FINAL_COMPLETE_SOURCE_REVIEW\n')
    assert release['baseline'] == contract['baseline']
    assert not (HERE / 'freeze_manifest.json').exists(), 'Never alter a frozen package.'
    assert not any((HERE / name).exists() for name in OUTPUTS), 'Never replace a prepared input.'

    specs = release['append_sources']
    known = contract['known_append_sources']
    assert specs[:len(known)] == known, 'The approved 181/28 prefix is immutable.'
    pending_packages = final_pending_packages(contract, release)
    assert len(specs) == len(known) + len(pending_packages)
    assert set(x['package'] for x in specs[len(known):]) == set(pending_packages)
    assert len({x['package'] for x in specs}) == len(specs)
    for spec in specs:
        assert spec['rows_key'] == 'rows', 'Source matrices use an explicit list key.'
        assert isinstance(spec['raw_count'], int) and spec['raw_count'] > 0
        assert spec['main_source_review_complete'] is True
        assert spec['new_numerical_divisor'] == '25'
        assert spec['terminal_BR_mean_weight'] == '1'
        assert spec['excluded_rows'] == [] and spec['row_order_policy'] == 'literal_source_order'
        assert valid_digest(spec['row_order_sha256'])
        assert isinstance(spec['uses_C_equality_in_source'], bool)
        assert isinstance(spec['manifest_family_sha_path'], list) and spec['manifest_family_sha_path']
        assert isinstance(spec['manifest_raw_count_path'], list) and spec['manifest_raw_count_path']
        for filename, digest in spec['files'].items():
            local_file(spec['package'], filename)
            assert valid_digest(digest), (spec['package'], filename)
        for required in ('exact_family.json', 'freeze_manifest.json', 'proof.md', 'coordinate_contract.json'):
            assert required in spec['files']
        assert valid_digest(spec['main_check_sha256'])
        assert Path(spec['main_check_file']).name == spec['main_check_file']
        assert spec['main_check_file'].startswith('main_') and spec['main_check_file'].endswith('.json')
    total = release['final_raw_count']
    assert isinstance(total, int) and total == 1586 + sum(x['raw_count'] for x in specs)

    pins = {}

    def pin(path, expected):
        key = str(path.resolve().relative_to(REPO))
        assert valid_digest(expected) and sha(path) == expected, key
        assert key not in pins or pins[key] == expected, key
        pins[key] = expected

    for path, expected in contract['direct_read_pins'].items():
        pin(REPO / path, expected)
    pin(release_path, sha(release_path))
    pin(HERE / 'source_review.md', release['final_source_review_sha256'])
    baseline = read(WS / contract['baseline']['package'] / 'exact_input.json')
    base_scales = read(WS / contract['baseline']['package'] / 'numerical_scaling.json')
    base_catalog = read(WS / contract['baseline']['package'] / 'row_catalog.json')
    assert len(baseline['raw_rows']) == baseline['raw_inequality_count'] == 1586
    assert baseline['variables'] == 513 and baseline['K_column'] == 512
    assert baseline['nonnegative_columns'] == list(range(513))
    assert baseline['equality_count'] == len(baseline['equalities']) == 2
    assert base_scales['raw_order'] == [r['name'] for r in baseline['raw_rows']]
    rows = deepcopy(baseline['raw_rows'])
    scales = deepcopy(base_scales['raw_scales'])
    catalog = deepcopy(base_catalog)
    family_metadata, source_manifests, ranges = [], {}, []
    for spec in specs:
        package = spec['package']
        for filename, expected in spec['files'].items():
            pin(local_file(package, filename), expected)
        # Main's record is identity-bound only; no point/face diagnostics are parsed.
        pin(WS / spec['main_check_file'], spec['main_check_sha256'])
        family = read(local_file(package, 'exact_family.json'))
        manifest = read(local_file(package, 'freeze_manifest.json'))
        assert at_path(manifest, spec['manifest_family_sha_path']) == spec['files']['exact_family.json']
        assert at_path(manifest, spec['manifest_raw_count_path']) == spec['raw_count']
        coordinates = read(local_file(package, 'coordinate_contract.json'))
        source_rows = family[spec['rows_key']]
        assert isinstance(source_rows, list) and len(source_rows) == spec['raw_count']
        assert family[spec['count_key']] == spec['raw_count']
        assert family['variables'] == 513 and family['K_column'] == 512
        assert family['optimizer_calls'] == 0
        assert order_sha(source_rows) == spec['row_order_sha256']
        for key in ('variables', 'K_column', 'bit_order', 'atom_columns'):
            assert coordinates[key] == baseline[key], (package, key)
        if 'nonnegative_columns' in coordinates:
            assert coordinates['nonnegative_columns'] == baseline['nonnegative_columns']
        if 'bit_order' in family:
            assert family['bit_order'] == baseline['bit_order']
        start = len(rows)
        for local_index, row in enumerate(source_rows):
            assert set(row['a']) == {str(j) for j in range(513)}
            assert row['rhs'] == '0' and row['numerical_divisor'] == '25'
            assert row[spec['terminal_BR_weight_field']] == '1'
            assert row['name'] not in scales, 'Conflicting row names require Main review; never rename.'
            for value in row['a'].values():
                assert isinstance(value, str)
                Fraction(value)
            rows.append(deepcopy(row))
            scales[row['name']] = row['numerical_divisor']
            entry = {k: deepcopy(v) for k, v in row.items() if k != 'a'}
            entry.update(raw_index=start + local_index, source_row_index=local_index,
                         source_package=package, stored_coefficient_entries=len(row['a']))
            catalog.append(entry)
        ranges.append({'package': package, 'raw_count': len(source_rows),
                       'raw_indices': [start, len(rows) - 1], 'source_row_order_sha256': spec['row_order_sha256'],
                       'uses_C_equality_in_source': spec['uses_C_equality_in_source'],
                       'additional_equality_elimination': False})
        family_metadata.append({'package': package, 'metadata': {k: deepcopy(v) for k, v in family.items() if k != spec['rows_key']}})
        source_manifests[package] = manifest
    assert len(rows) == len(catalog) == len(scales) == total
    assert all(isinstance(x, str) and Fraction(x) > 0 for x in scales.values())
    assert rows[:1586] == baseline['raw_rows']
    for name, expected in pins.items():
        assert sha(REPO / name) == expected, name

    write_new('source_pins.json', {
        'status': 'PREPARED_NO_OPTIMIZER', 'sources': dict(sorted(pins.items())),
        'source_manifests': source_manifests, 'source_manifest_binding': 'Exact final manifests, no recursive candidate-file reads.',
        'inherited_provenance': 'Baseline metadata and source manifests retained verbatim; transitive diagnostic files are not parsed.',
    })
    result = {key: deepcopy(baseline[key]) for key in PRESERVED}
    result.update({
        'schema': 'visible_maximum_joint_v5_exact_v1', 'status': 'PREPARED_NO_OPTIMIZER',
        'optimizer_calls': 0, 'raw_inequality_count': total, 'raw_rows': rows,
        'raw_row_policy': 'All baseline and full source rows retained literally, including sparse/explicit zeros, duplicates and rhs=-1.',
        'baseline_metadata': {k: deepcopy(v) for k, v in baseline.items() if k != 'raw_rows'},
        'source_family_metadata': family_metadata, 'source_bindings': release,
        'source_pins_sha256': sha(HERE / 'source_pins.json'),
        'source_review_sha256': release['final_source_review_sha256'],
        'append_contract': {'baseline_raw_count': 1586, 'complete_families': ranges, 'final_raw_count': total, 'excluded_rows': []},
        'preparation_only': {'optimization_authorized': False, 'freeze_authorized': False,
            'point_values_loaded_or_bound': False, 'support_restricted': False, 'K_fixed': False,
            'new_equality_elimination': False, 'SPE_sufficiency_claimed': False,
            'half_status': 'OPEN', 'future_release_owner': 'Boss1/Main'},
    })
    write_new('exact_input.json', result)
    write_new('numerical_scaling.json', {
        'status': 'PREPARED_NO_OPTIMIZER', 'raw_order': [r['name'] for r in rows], 'raw_scales': scales,
        'baseline_scaling_metadata': {k: deepcopy(v) for k, v in base_scales.items() if k not in ('raw_order', 'raw_scales')},
        'old_positive_scale_strings_literal': 1586, 'new_numerical_positive_divisor': '25',
        'actual_source_IC_weight_may_differ': True, 'source_raw_terminal_BR_mean_weight': '1',
        'exact_coefficients_numerically_divided': False,
    })
    for filename in ('column_routing.json', 'column_routing.tsv'):
        with (HERE / filename).open('xb') as handle:
            handle.write((WS / contract['baseline']['package'] / filename).read_bytes())
    write_new('row_catalog.json', catalog)
    columns = ('raw_index', 'name', 'family', 'numerical_divisor', 'source_package', 'source_row_index', 'source')
    with (HERE / 'row_catalog.tsv').open('x', encoding='utf-8') as handle:
        handle.write('\t'.join(columns) + '\n')
        for entry in catalog:
            handle.write('\t'.join(str(entry.get(k, '')) for k in columns) + '\n')
    write_new('raw_identity_diagnostics.json', diagnostics(rows))
    for name, expected in pins.items():
        assert sha(REPO / name) == expected, name
    output = {'status': 'PREPARED_NO_OPTIMIZER', 'result': 'COMPLETE_LITERAL_ASSEMBLY_AWAITING_CHECK',
              'input_sha256': sha(HERE / 'exact_input.json'), 'raw_rows': total,
              'columns': 513, 'equalities': 2, 'baseline_literal_rows': 1586,
              'full_source_ranges': ranges, 'optimizer_calls': 0, 'frozen': False,
              'source_programs_imported_or_executed': False, 'point_values_loaded_or_bound': False}
    write_new('build_result.json', output)
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
