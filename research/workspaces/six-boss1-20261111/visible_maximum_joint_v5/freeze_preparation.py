#!/usr/bin/env python3
"""Freeze the approved complete 3056-row preparation, with zero optimization.

The immutable assembly release itself did not authorize freezing. Main's later
explicit repair/check/freeze task is separately recorded and required here.
All `artifacts` keys are package-local basenames for the frozen solver reader.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
RELEASE_SHA = '653e43d66feda8874fef8230fe95d689aa00378bca327284ddee43fcf300f821'
INPUT_SHA = '12f456dfbc789a5c1826d248e4851b84f66b428554d181b7ba12cbfdb920f3ac'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(name):
    return json.loads((HERE / name).read_text(encoding='utf-8'))


def main():
    assert not (HERE / 'freeze_manifest.json').exists(), 'This preparation is already frozen.'
    assert not (HERE / 'SHA256SUMS').exists(), 'Never replace frozen checksums.'
    assert sha(HERE / 'final_release.json') == RELEASE_SHA
    assert sha(HERE / 'exact_input.json') == INPUT_SHA
    release = read('final_release.json')
    authority = read('preparation_freeze_authorization.json')
    assert release['owner'] == 'Boss1/Main' and release['assembly_authorized'] is True
    assert release['optimizer_authorized'] is release['freeze_authorized'] is False
    assert authority['followup_freeze_authorized'] is True and authority['optimizer_authorized'] is False
    assert authority['assembly_release_sha256'] == RELEASE_SHA and authority['required_raw_rows'] == 3056
    assert authority['authorization_is_not_a_solve_release'] is True
    assert sha(HERE / 'source_review.md') == release['final_source_review_sha256']

    inp, build, checked = read('exact_input.json'), read('build_result.json'), read('literal_check_result.json')
    assert inp['raw_inequality_count'] == len(inp['raw_rows']) == release['final_raw_count'] == 3056
    assert inp['variables'] == len(inp['nonnegative_columns']) == 513
    assert inp['K_column'] == 512 and len(inp['atom_columns']) == 512
    assert inp['equality_count'] == len(inp['equalities']) == 2
    assert inp['source_bindings'] == release
    assert build['input_sha256'] == checked['input_sha256'] == INPUT_SHA
    assert checked['status'] == 'PASS_COMPLETE_LITERAL_PREPARATION'
    assert checked['checker_sha256'] == sha(HERE / 'check_preparation.py')
    assert checked['appended_formula_columns_reconstructed'] == 754110
    assert checked['total_full_columns_examined'] == 1567728
    assert checked['all_source_row_dictionaries_and_order_literal'] is True
    assert checked['old_rhs_minus_one_rows'] == 30
    assert checked['raw_duplicate_rows'] == 123
    assert checked['raw_zero_rows'] == [{'raw_index': 45, 'name': 'SAFE_6_6'}]
    assert checked['all_zero_and_duplicate_rows_retained'] is True
    assert all(x['Main_final_source_review_complete'] for x in checked['source_checks'])
    assert inp['optimizer_calls'] == build['optimizer_calls'] == checked['optimizer_calls'] == 0
    assert inp['preparation_only']['optimization_authorized'] is False

    failed = read('build_attempt1_failure.json')
    success = read('build_attempt2_execution.json')
    check_run = read('assembled_check_attempt1_execution.json')
    assert failed['error_type'] == 'KeyError' and failed['missing_key'] == 'K_column'
    assert sha(HERE / 'build_attempt1_source.py') == failed['builder_sha256']
    assert success['returncode'] == check_run['returncode'] == 0
    assert success['builder_sha256'] == sha(HERE / 'build_input.py')
    assert check_run['checker_sha256'] == checked['checker_sha256']
    assert check_run['input_sha256'] == INPUT_SHA

    pins = read('source_pins.json')['sources']
    assert sha(HERE / 'source_pins.json') == inp['source_pins_sha256']
    for path, expected in pins.items():
        assert sha(REPO / path) == expected, path
    expected_packages = ['all_source_ordered_menu_cells', 'source2_cap_coupled_internal_safe',
                         'source2_minimal_cap_safe', 'all_source_minimal_cap_safe', 'ordered_minimal_cap']
    assert [s['package'] for s in release['append_sources']] == expected_packages
    assert [s['raw_count'] for s in release['append_sources']] == [181, 28, 28, 1096, 137]

    package_files = sorted(p for p in HERE.iterdir() if p.is_file())
    assert all(p.name not in ('freeze_manifest.json', 'SHA256SUMS') for p in package_files)
    artifacts = {p.name: sha(p) for p in package_files}
    assert all(Path(name).name == name and '/' not in name for name in artifacts)
    adjacent_summary = HERE.parent / 'visible_maximum_joint_v5.md'
    manifest = {
        'schema': 'visible_maximum_joint_v5_frozen_preparation_v1',
        'status': 'PREPARED_NO_OPTIMIZER', 'frozen': True, 'frozen_preparation_only': True,
        'owner': 'Boss1', 'RUN': 'six-boss1-20261111',
        'frozen_utc': datetime.now(timezone.utc).isoformat(),
        'raw_rows': 3056, 'raw_inequalities': 3056, 'columns': 513, 'nonnegative_columns': 513,
        'atom_columns': 512, 'K_column': 512, 'equalities': 2,
        'input_file': 'exact_input.json', 'input_sha256': INPUT_SHA,
        'baseline_input_sha256': release['baseline']['input_sha256'],
        'final_release_sha256': RELEASE_SHA,
        'assembly_release_freeze_authorized': False,
        'later_Main_task_preparation_freeze_authorized': True,
        'freeze_authorization_record': 'preparation_freeze_authorization.json',
        'freeze_authorization_record_sha256': sha(HERE / 'preparation_freeze_authorization.json'),
        'assembly_release_and_Main_source_review_bytes_unchanged': True,
        'source_review_sha256': release['final_source_review_sha256'],
        'baseline_raw_rows_literal': 1586, 'complete_new_raw_rows_literal': 1470,
        'full_source_ranges': build['full_source_ranges'],
        'source_packages': expected_packages, 'source_row_exclusions': [],
        'all_source_metadata_and_coefficient_strings_literal': True,
        'old_positive_scale_strings_preserved': 1586, 'new_positive_scale_strings': 1470,
        'new_numerical_positive_divisor': '25', 'new_raw_terminal_BR_average_weight': '1',
        'source_IC_weight_is_not_the_numerical_divisor': True,
        'original_objective_preserved': True, 'original_equalities_preserved': True,
        'all_512_atoms_and_independent_K_retained': True,
        'new_C_equality_elimination': False, 'raw_zero_rows_retained': checked['raw_zero_rows'],
        'raw_duplicate_rows_retained': 123, 'rhs_minus_one_rows_retained': 30,
        'distinct_nonzero_affine_rows_diagnostic_only': 2932,
        'independent_preparation_check': checked['status'],
        'checker_sha256': checked['checker_sha256'],
        'checker_result_sha256': sha(HERE / 'literal_check_result.json'),
        'all_full_columns_examined': 1567728, 'new_formula_columns_independently_rebuilt': 754110,
        'source2_general_C_signed_identity_columns': 14364,
        'source_files_verified_unchanged': len(pins),
        'source_pins_sha256': sha(HERE / 'source_pins.json'),
        'real_build_failure_count': 1, 'successful_build_attempt': 2,
        'first_real_build_failure_record': 'build_attempt1_failure.json',
        'first_assembled_check_passed': True,
        'coordinate_schema_fix': 'Explicit columns/bits/type_string/independent_K adapter for ordered_minimal_cap; first four source schemas remain literal.',
        'builder_or_source_code_imported_by_checker': False, 'external_blind_review_claimed': False,
        'optimizer_calls': 0, 'numerical_optimization_authorized': False,
        'solve_consumption': 'UNRELEASED_INPUT', 'point_values_loaded_or_bound': False,
        'support_restriction': False, 'fixed_K': False,
        'lambda230_family_included': False, 'SPE_sufficiency_claimed': False, 'half_status': 'OPEN',
        'artifacts_path_convention': 'Package-local basenames only; values are SHA256 strings.',
        'artifacts': artifacts,
        'artifact_bytes': {p.name: p.stat().st_size for p in package_files},
        'adjacent_summary': {'repo_relative_path': str(adjacent_summary.relative_to(REPO)),
                             'sha256': sha(adjacent_summary)},
        'checksum_file': 'SHA256SUMS',
        'future_release': 'Boss1/Main independently preflights this exact frozen3056 input before any separate single-call numerical authorization.',
    }
    with (HERE / 'freeze_manifest.json').open('x', encoding='utf-8') as handle:
        json.dump(manifest, handle, ensure_ascii=False, indent=2)
        handle.write('\n')
    sums = dict(artifacts)
    sums['freeze_manifest.json'] = sha(HERE / 'freeze_manifest.json')
    with (HERE / 'SHA256SUMS').open('x', encoding='utf-8') as handle:
        for filename in sorted(sums):
            handle.write(f'{sums[filename]}  {filename}\n')
    for filename, expected in sums.items():
        assert sha(HERE / filename) == expected, filename
    for path, expected in pins.items():
        assert sha(REPO / path) == expected, path
    print(json.dumps({'status': 'FROZEN_COMPLETE3056_PREPARATION_NO_OPTIMIZER',
                      'raw_rows': 3056, 'columns': 513, 'equalities': 2,
                      'input_sha256': INPUT_SHA, 'manifest_sha256': sums['freeze_manifest.json'],
                      'SHA256SUMS_sha256': sha(HERE / 'SHA256SUMS'),
                      'package_local_artifacts': len(artifacts), 'source_pins_verified': len(pins),
                      'optimizer_calls': 0, 'numerical_optimization_authorized': False}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
