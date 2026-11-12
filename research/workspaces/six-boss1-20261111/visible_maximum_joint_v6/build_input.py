#!/usr/bin/env python3
"""Lossless v6 preparation only. No optimizer and no LP consumption authority.

The literal v5 prefix is never altered. Each later source is adapted through a
named schema, retaining its original identifier, source index and all metadata.
This program only assembles after every source has an explicit Main admission.
"""
import argparse
import copy
import hashlib
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = WS.parents[2]
BITS = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'x', 'o', 'c']
COEFFICIENT_FIELDS = {'a', 'raw_coefficients', 'coefficients_divided_by_25'}


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(',', ':')) + '\n').encode('utf-8')


def object_sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def dump(name, value):
    assert not (HERE / 'freeze_manifest.json').exists(), 'Package is frozen'
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n',
                             encoding='utf-8')


def verify_pins():
    pins = read(HERE / 'source_pins.json')
    for rec in pins['files']:
        assert sha(REPO / rec['path']) == rec['sha256'], rec['path']
    return pins


def source_rows(spec):
    data = read(WS / spec['package'] / spec['file'])
    rows = [data] if spec['schema_adapter'] == 'root_sparse_literal' else data['rows']
    assert len(rows) == spec['raw_count'], spec['package']
    return data, rows


def coefficients(spec, row):
    adapter = spec['schema_adapter']
    if adapter == 'source2_lambda_raw_coefficients_list':
        assert row['family'] in ('six_general', 'six_C_only', 'ordered_five')
        values = row['raw_coefficients']
        assert isinstance(values, list) and len(values) == 513
        assert len(row['coefficients_divided_by_25']) == 513
        assert all(Fraction(x) / 25 == Fraction(y)
                   for x, y in zip(values, row['coefficients_divided_by_25']))
        return {str(k): v for k, v in enumerate(values)}
    if adapter == 'later_lambda_sparse_a':
        assert row['kind'] in ('six_general', 'six_C_only', 'ordered')
        assert isinstance(row['a'], dict)
        return copy.deepcopy(row['a'])
    if adapter == 'source2_delta_a_list':
        assert row['mode'] in ('pure', 'ordered')
        assert isinstance(row['a'], list) and len(row['a']) == 513
        return {str(k): v for k, v in enumerate(row['a'])}
    if adapter == 'root_sparse_literal':
        assert isinstance(row['a'], dict)
        return copy.deepcopy(row['a'])
    raise AssertionError('Unrecognized frozen source schema: ' + adapter)


def original_id(row):
    return row['id'] if 'id' in row else row['name']


def output_name(spec, row):
    if spec['schema_adapter'] == 'root_sparse_literal':
        return row['name']
    return spec['package'] + '::' + original_id(row)


def original_metadata(row):
    return {k: copy.deepcopy(v) for k, v in row.items() if k not in COEFFICIENT_FIELDS}


def row_family(spec, row):
    if 'family' in row:
        return row['family']
    if 'kind' in row:
        return row['kind']
    assert spec['schema_adapter'] == 'source2_delta_a_list'
    return 'SOURCE2_CONDITIONAL_REDISTRIBUTION_' + row['mode'].upper()


def adapted(spec, row, local_index):
    if spec['schema_adapter'] == 'root_sparse_literal':
        # No collision: the Main row is appended as its exact original object.
        return copy.deepcopy(row)
    result = {
        'name': output_name(spec, row),
        'id': original_id(row),
        'family': row_family(spec, row),
        'a': coefficients(spec, row),
        'rhs': row.get('rhs', '0'),
        'numerical_divisor': spec['numerical_divisor'],
        'source_package': spec['package'],
        'source_file': spec['file'],
        'source_row_index': local_index,
        'source_row_id': original_id(row),
        'source_row_metadata': original_metadata(row),
        'source_row_object_sha256': object_sha(row),
        'source_coefficient_encoding': spec['schema_adapter'],
    }
    return result


def check_schema(contract):
    verify_pins()
    base = read(WS / 'visible_maximum_joint_v5' / 'exact_input.json')
    assert base['variables'] == 513 and len(base['raw_rows']) == 3056
    names = [r['name'] for r in base['raw_rows']]
    reports = []
    for spec in contract['append_sources']:
        data, rows = source_rows(spec)
        report = {'package': spec['package'], 'schema_adapter': spec['schema_adapter'],
                  'raw_count': len(rows), 'schema_from_file': data.get('schema'),
                  'first_original_id': original_id(rows[0]),
                  'last_original_id': original_id(rows[-1]),
                  'original_row_keys': sorted({k for r in rows for k in r}),
                  'coefficient_entry_counts': {}, 'metadata_preserved': True}
        counts = Counter()
        for row in rows:
            a = coefficients(spec, row)
            assert all(isinstance(k, str) and k == str(int(k)) and 0 <= int(k) < 513 for k in a)
            assert all(isinstance(v, str) for v in a.values())
            for val in a.values():
                Fraction(val)
            assert Fraction(row.get('rhs', '0')) == 0
            names.append(output_name(spec, row))
            counts[len(a)] += 1
        report['coefficient_entry_counts'] = dict(sorted(counts.items()))
        reports.append(report)
    assert len(names) == contract['expected_raw_count'] == 4177
    assert len(names) == len(set(names)), 'Assembled names collide'
    verify_pins()
    result = {'status': 'PASS_SCHEMA_ADAPTATION_ONLY', 'optimizer_calls': 0,
              'candidate_or_face_reads': 0, 'final_input_written': False,
              'raw_count_if_all_admitted': len(names), 'new_source_schemas': reports,
              'name_mapping': 'package::original id; final Main root name literal',
              'source_metadata_policy': 'all non-coefficient fields literal; whole source-row canonical SHA binds coefficients too',
              'source_pins_sha256': sha(HERE / 'source_pins.json')}
    dump('schema_adaptation_check.json', result)
    return result


def assemble(contract):
    admissions = read(HERE / 'source_admission.json')
    assert admissions['assembly_authorized'] is True, 'Main assembly admission is pending'
    assert admissions['optimizer_authorized'] is False
    assert admissions['freeze_authorized'] is True
    for spec in contract['append_sources']:
        item = admissions['sources'][spec['package']]
        assert item['admitted'] is True, spec['package']
        assert item['manifest_sha256'] == spec['manifest_sha256']
        if item.get('main_check_file'):
            path = WS / item['main_check_file']
            assert sha(path) == item['main_check_sha256']
            checked = read(path)
            assert checked['status'].startswith('PASS'), str(path)
    verify_pins()
    base = read(WS / 'visible_maximum_joint_v5' / 'exact_input.json')
    base_scale = read(WS / 'visible_maximum_joint_v5' / 'numerical_scaling.json')
    base_catalog = read(WS / 'visible_maximum_joint_v5' / 'row_catalog.json')
    rows = copy.deepcopy(base['raw_rows'])
    catalog = copy.deepcopy(base_catalog)
    raw_order = copy.deepcopy(base_scale['raw_order'])
    raw_scales = copy.deepcopy(base_scale['raw_scales'])
    provenance = []
    for index, row in enumerate(base['raw_rows']):
        provenance.append({'raw_index': index, 'name': row['name'],
            'package': 'visible_maximum_joint_v5', 'source_row_index': index,
            'source_row_id': row['name'], 'row_object_sha256': object_sha(row),
            'adaptation': 'entire object literal',
            'source_row_metadata': original_metadata(row)})
    family_metadata = []
    ranges = []
    for spec in contract['append_sources']:
        data, originals = source_rows(spec)
        first = len(rows)
        source_catalog = None
        if spec.get('catalog_file'):
            source_catalog = read(WS / spec['package'] / spec['catalog_file'])
            assert len(source_catalog) == len(originals)
        for local, original in enumerate(originals):
            row = adapted(spec, original, local)
            index = len(rows)
            assert row['name'] not in raw_scales
            rows.append(row)
            raw_order.append(row['name'])
            raw_scales[row['name']] = spec['numerical_divisor']
            rec = {'raw_index': index, 'name': row['name'], 'family': row['family'],
                   'rhs': row['rhs'], 'stored_coefficient_entries': len(row['a']),
                   'numerical_divisor': spec['numerical_divisor'],
                   'source_package': spec['package'], 'source_row_index': local,
                   'source_row_id': original_id(original),
                   'source_row_metadata': original_metadata(original),
                   'source_row_object_sha256': object_sha(original)}
            if source_catalog is not None:
                rec['original_source_catalog_entry'] = copy.deepcopy(source_catalog[local])
            catalog.append(rec)
            provenance.append({'raw_index': index, 'name': row['name'],
                'package': spec['package'], 'file': spec['file'],
                'source_row_index': local, 'source_row_id': original_id(original),
                'source_row_object_sha256': object_sha(original),
                'source_row_metadata': original_metadata(original),
                'source_coefficient_encoding': spec['schema_adapter'],
                'row_object_sha256': object_sha(row),
                'adaptation': spec['metadata_and_name_policy']})
        ranges.append({'package': spec['package'], 'raw_count': len(originals),
                       'raw_indices': [first, len(rows) - 1],
                       'source_ids_order_sha256': object_sha([original_id(r) for r in originals]),
                       'manifest_sha256': spec['manifest_sha256'],
                       'schema_adapter': spec['schema_adapter'],
                       'numerical_divisor': spec['numerical_divisor']})
        if spec['schema_adapter'] != 'root_sparse_literal':
            family_metadata.append({'package': spec['package'],
                                    'metadata': {k: v for k, v in data.items() if k != 'rows'}})
    assert len(rows) == contract['expected_raw_count'] == 4177
    assert len(raw_order) == len(set(raw_order)) == len(raw_scales) == len(rows)
    assert sum(Fraction(r['rhs']) == -1 for r in rows) == 30
    preserved = ['variables', 'bit_order', 'atom_columns', 'K_column',
                 'nonnegative_columns', 'objective', 'equalities',
                 'equality_count', 'inequality_convention']
    output = {k: copy.deepcopy(base[k]) for k in preserved}
    output.update({'schema': 'visible_maximum_joint_v6_exact_v1',
        'status': 'PREPARED_NO_OPTIMIZER', 'optimizer_calls': 0,
        'raw_inequality_count': len(rows), 'raw_rows': rows,
        'raw_row_policy': 'All 3056 parent objects literal; all 1121 appended source occurrences retained in declared order.',
        'parent_input_sha256': contract['baseline']['input_sha256'],
        'parent_manifest_sha256': contract['baseline']['manifest_sha256'],
        'parent_metadata': {k: copy.deepcopy(v) for k, v in base.items() if k != 'raw_rows'},
        'source_family_metadata': family_metadata,
        'append_contract': {'baseline_raw_count': 3056, 'complete_families': ranges,
                            'final_raw_count': len(rows), 'excluded_rows': [],
                            'separate_delta_helper_files_not_members_of_rows': ['epsilon_rows.json', 'affine_family.json']},
        'source_pins_sha256': sha(HERE / 'source_pins.json'),
        'model_contract_sha256': sha(HERE / 'model_contract.json'),
        'source_admission_sha256': sha(HERE / 'source_admission.json'),
        'preparation_only': {'optimization_authorized': False,
            'point_values_loaded_or_bound': False, 'support_restricted': False,
            'K_fixed': False, 'new_equality_elimination': False,
            'SPE_sufficiency_claimed': False, 'half_status': 'OPEN',
            'LP_release_created_or_consumed': False}})
    scale = {'status': 'PREPARED_NO_OPTIMIZER', 'raw_order': raw_order,
        'raw_scales': raw_scales,
        'baseline_scaling_metadata': {k: copy.deepcopy(v) for k, v in base_scale.items()
                                      if k not in ('raw_order', 'raw_scales')},
        'old_positive_scale_strings_literal': 3056,
        'new_lambda_delta_divisor': '25', 'new_root_divisor': '1',
        'actual_source_IC_weight_may_differ': True,
        'exact_coefficients_numerically_divided': False}
    dump('exact_input.json', output)
    dump('row_catalog.json', catalog)
    dump('provenance.json', {'schema': 'v6_lossless_provenance_v1',
         'baseline': contract['baseline'], 'append_ranges': ranges,
         'canonical_object_digest': 'SHA256 of sorted-key compact UTF-8 JSON plus LF',
         'rows': provenance})
    dump('numerical_scaling.json', scale)
    lines = ['raw_index\tname\tfamily\trhs\tnumerical_divisor\tsource_package\tsource_row_index\tsource_row_id']
    for rec in catalog:
        i = rec['raw_index']
        prov = provenance[i]
        lines.append('\t'.join(map(str, [i, rec['name'], rec['family'], rec['rhs'],
            raw_scales[rec['name']], prov['package'], prov['source_row_index'], prov['source_row_id']])))
    (HERE / 'row_catalog.tsv').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    verify_pins()
    result = {'status': 'PASS_ASSEMBLED_PREPARATION_ONLY', 'raw_rows': len(rows),
        'columns': 513, 'equalities': 2, 'rhs_minus_one_rows': 30,
        'base_objects_literal': rows[:3056] == base['raw_rows'],
        'input_sha256': sha(HERE / 'exact_input.json'), 'append_ranges': ranges,
        'optimizer_calls': 0, 'LP_release_created_or_consumed': False}
    dump('build_result.json', result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--assemble', action='store_true')
    args = parser.parse_args()
    assert not (HERE / 'freeze_manifest.json').exists(), 'Package is frozen; use a replay copy'
    contract = read(HERE / 'preparation_contract.json')
    result = assemble(contract) if args.assemble else check_schema(contract)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        if not (HERE / 'freeze_manifest.json').exists():
            log = read(HERE / 'failure_log.json') if (HERE / 'failure_log.json').exists() else {'events': []}
            log['events'].append({'program': 'build_input.py', 'error_type': type(error).__name__,
                                  'message': str(error), 'resolved': False})
            dump('failure_log.json', log)
        raise
