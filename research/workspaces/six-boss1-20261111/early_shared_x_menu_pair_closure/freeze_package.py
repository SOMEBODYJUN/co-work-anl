#!/usr/bin/env python3
"""Freeze the new closure/projection package after independent exact audit."""
from hashlib import sha256
from pathlib import Path
import gzip
import json

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = WORK.parents[2]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def read(path):
    with gzip.open(path, 'rt') if path.suffix == '.gz' else path.open() as f:
        return json.load(f)


def entry(path):
    return {'path': str(path.relative_to(REPO)), 'bytes': path.stat().st_size, 'sha256': digest(path)}


def save(name, value):
    path = HERE / name
    assert not path.exists(), ('refuse_overwrite', str(path))
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def main():
    for name in ('freeze_manifest.json', 'release_receipt.json', 'SHA256SUMS'):
        assert not (HERE / name).exists(), ('already_frozen', name)
    for source in read(HERE / 'source_manifest.json')['sources'].values():
        assert digest(REPO / source['path']) == source['sha256'], ('input_changed', source['path'])
    projection_summary = read(HERE / 'averaged_prefix_projection_summary.json')
    for source in projection_summary['input_sources'].values():
        assert digest(REPO / source['path']) == source['sha256'], ('projection_input_changed', source['path'])
    old_manifest_path = WORK / 'early_shared_x_joint/freeze_manifest.json'
    assert digest(old_manifest_path) == 'ec50991df761fbe82c22814abae71c7ba6a57d354803ecd59a44eea414c87ec1'
    old_manifest = read(old_manifest_path)
    for oldfile in old_manifest['files']:
        assert digest(REPO / oldfile['path']) == oldfile['sha256'], ('old_frozen_file_changed', oldfile['path'])
    pair_audit_path = HERE / 'audit/independent_verification.json'
    projection_audit_path = HERE / 'audit/averaged_prefix_verification.json'
    pair_audit, projection_audit = read(pair_audit_path), read(projection_audit_path)
    assert pair_audit['universal_literal_identities']['status'] == 'PASS'
    assert pair_audit['packet_audit']['status'] == 'PASS'
    assert pair_audit['direct_BR_redundancy']['status'] == 'PASS'
    assert projection_audit['universal']['status'] == 'PASS'
    assert projection_audit['projections']['status'] == 'PASS_INDEPENDENT_PROJECTIONS'
    assert projection_audit['saved_certificate_audit']['status'] == 'PASS'
    assert read(HERE / 'audit/freeze_manifest.json')['status'] == 'PASS_FROZEN'
    for auditfile in read(HERE / 'audit/freeze_manifest.json')['files']:
        assert digest(REPO / auditfile['path']) == auditfile['sha256'], ('audit_changed', auditfile['path'])
    closure_summary = read(HERE / 'pair_closure_summary.json')
    reduced = read(HERE / 'direct_BR_redundancy.json.gz')
    assert closure_summary['raw_candidates'] == 394
    assert closure_summary['usable_append_rows'] == 306 and closure_summary['usable_nonzeros'] == 131721
    assert reduced['retained_rows'] == 264 and reduced['retained_nonzeros'] == 116034
    receipt = {
        'status': 'FROZEN_RELEASED_NEW_MENU_PAIR_CLOSURE_NO_SOLVE', 'run': 'six-boss1-20261111',
        'owner': 'Boss1', 'workspace': str(HERE.relative_to(REPO)),
        'raw_candidates': 394, 'unique_candidates': 394, 'old436_exact_duplicates': 84,
        'zero_rows': 0, 'internal_exact_duplicates': 0, 'direct_mu_nonnegative_rows': 4,
        'direct_filtered_append': {'rows': 306, 'nonzeros': 131721, 'result_GE_shape': [24418, 22941],
                                   'artifact': entry(HERE / 'usable_pair_append.json.gz')},
        'further_exact_BR_reduction': {'redundant_rows': 42, 'retained_rows': 264, 'retained_nonzeros': 116034,
                                      'result_GE_shape': [24376, 22941],
                                      'certificate': entry(HERE / 'direct_BR_redundancy.json.gz')},
        'new_columns': 0, 'new_equalities': 0, 'old_mass_equalities_retained': 128,
        'old_normalization_and_bounds_retained': True,
        'nine_projected_rows': {'count': 9, 'constants': ['31', '25', '19'],
                                'rows_artifact': entry(HERE / 'averaged_prefix_rows_9.json'),
                                'certificate': entry(HERE / 'averaged_prefix_projection.json.gz'),
                                'derived_from_old436_only': True, 'not_counted_as_extra_PAIR_append_rows': True},
        'pair_audit': entry(pair_audit_path), 'prefix_projection_audit': entry(projection_audit_path),
        'old_package_all_frozen_artifact_hashes_checked': len(old_manifest['files']),
        'old_package_changed_files': 0, 'old_package_manifest': entry(old_manifest_path),
        'report': entry(WORK / 'early_shared_x_menu_pair_closure.md'),
        'additional_Main_pair_proof_crosscheck': entry(WORK / 'main_full_average_pair.md'),
        'scope': 'Full visible same-branch PAIR closure at fixed16 hist support; all36 menu pairing is separate from old same-index diagonal. Universal proofs do not certify a full SPE. Neither306 nor264 is claimed cone-independent.',
        'point_files_read': 0, 'optimizer_calls': 0,
        'next_stage': 'Released generic append and projection inputs; no fixed-point evaluation or numeric solve was performed.'}
    save('release_receipt.json', receipt)
    files = sorted(p for p in HERE.rglob('*') if p.is_file())
    files.append(WORK / 'early_shared_x_menu_pair_closure.md')
    manifest = {'status': 'FROZEN_RELEASED', 'scope': receipt['scope'],
                'files': [entry(p) for p in files], 'file_count': len(files),
                'independent_audit_frozen': True, 'old_frozen_package_fully_unchanged': True,
                'old_package_files_checked': len(old_manifest['files']),
                'all_current_input_source_hashes_match': True, 'point_files_read': 0, 'optimizer_calls': 0}
    save('freeze_manifest.json', manifest)
    sums_paths = files + [HERE / 'freeze_manifest.json']
    (HERE / 'SHA256SUMS').write_text(''.join(digest(p) + '  ' + str(p.relative_to(REPO)) + '\n' for p in sums_paths))
    print(json.dumps({'status': 'FROZEN_RELEASED', 'frozen_artifacts': len(files),
                      'manifest_sha256': digest(HERE / 'freeze_manifest.json'),
                      'sha256sums_sha256': digest(HERE / 'SHA256SUMS'),
                      'receipt_sha256': digest(HERE / 'release_receipt.json'),
                      'report_sha256': digest(WORK / 'early_shared_x_menu_pair_closure.md'),
                      'append306_sha256': digest(HERE / 'usable_pair_append.json.gz'),
                      'BR_reduction_sha256': digest(HERE / 'direct_BR_redundancy.json.gz'),
                      'nine_projection_sha256': digest(HERE / 'averaged_prefix_projection.json.gz')}, indent=2))


if __name__ == '__main__':
    main()
