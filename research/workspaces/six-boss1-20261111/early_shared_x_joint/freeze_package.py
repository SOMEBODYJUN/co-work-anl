#!/usr/bin/env python3
"""Seal the audited generic layer; no point binding or optimization."""
from hashlib import sha256
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = WORK.parents[2]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def save(name, value):
    path = HERE / name
    assert not path.exists(), ('refuse_overwrite', str(path))
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def entry(path):
    return {'path': str(path.relative_to(REPO)), 'bytes': path.stat().st_size, 'sha256': digest(path)}


def main():
    for name in ('freeze_manifest.json', 'SHA256SUMS', 'release_receipt.json'):
        assert not (HERE / name).exists(), ('already_frozen', name)
    source_manifest = read(HERE / 'source_manifest.json')
    for source in source_manifest['sources'].values():
        assert digest(REPO / source['path']) == source['sha256'], ('source_changed', source['path'])
    audit_path = HERE / 'audit/independent_verification.json'
    projection_audit_path = HERE / 'audit/visible_projection_verification.json'
    source_audit_path = WORK / 'early_shared_x_source_audit/source_audit.json'
    audit = read(audit_path)
    projection = read(projection_audit_path)
    source_audit = read(source_audit_path)
    assert audit['matrix_audit']['status'] == audit['universal_budget_audit']['status'] == 'PASS'
    assert projection['status'] == projection['saved_certificate_audit']['status'] == 'PASS'
    assert source_audit['status'] == 'PASS_INDEPENDENT_MATHEMATICAL_SOURCE_AUDIT'
    assert source_audit['matrix_changing_mathematical_flaws_found'] == []
    assert read(HERE / 'template_entry_verification.json')['status'] == 'PASS'
    for value in source_audit['sources'].values():
        assert digest(REPO / value['path']) == value['sha256'], ('source_audit_anchor_changed', value['path'])
    receipt = {
        'status': 'FROZEN_RELEASED_GENERIC_LAYER_NO_SOLVE', 'run': 'six-boss1-20261111',
        'owner': 'Boss1', 'workspace': str(HERE.relative_to(REPO)),
        'new_hidden_columns': 1920, 'new_inequalities_raw_and_unique': 436,
        'new_mass_equalities': 128, 'new_nonzero_coefficients': 166069,
        'ge_shape_after_symbolic_append': [24112, 22941], 'new_eq_shape': [128, 22941],
        'old_normalization_retained_separately': True,
        'source_audit': entry(source_audit_path), 'literal_audit': entry(audit_path),
        'visible_projection_audit': entry(projection_audit_path),
        'visible_prefix_projection': {'rows': 36, 'C_star': 27, 'H3': 9,
                                      'artifact': entry(HERE / 'visible_prefix_projection.json.gz')},
        'symbolic_append': entry(HERE / 'symbolic_append.json.gz'),
        'fixed_point_template': entry(HERE / 'fixed_point_feasibility_template.json.gz'),
        'report': entry(WORK / 'early_shared_x_joint.md'),
        'input_binding': {'base_matrix_sha256': source_manifest['sources']['final_matrix']['sha256'],
                          'base_shape': [23676, 21021], 'old_core_mutations': 0},
        'fixed_point_template_unfilled': True, 'optimizer_calls': 0,
        'scope_boundary': 'A fixed-16-hist necessary extension, not full SPE; 14 tail label roles need not be distinct; product gluing over hist/X does not certify full old RZ laws or conditional aliases.',
        'next_authorized_stage': 'No solve in this package. Bind only the next exact 23676 point explicitly released by Main; any actual solve requires its own Main task.'}
    save('release_receipt.json', receipt)
    paths = sorted(p for p in HERE.rglob('*') if p.is_file())
    paths.append(WORK / 'early_shared_x_joint.md')
    manifest = {'status': 'FROZEN_RELEASED', 'scope': receipt['scope_boundary'],
                'dimensions': {'base': [23676, 21021], 'appended_GE': 436, 'appended_EQ': 128,
                               'appended_columns': 1920, 'total_columns': 22941},
                'raw_source_provenance_records': 436, 'exact_duplicate_rows_removed': 0,
                'file_count': len(paths), 'files': [entry(p) for p in paths],
                'external_source_review': entry(source_audit_path),
                'external_source_review_freeze': entry(WORK / 'early_shared_x_source_audit/freeze_manifest.json'),
                'all_source_inputs_unchanged': True, 'no_numeric_gamepoint_bound': True,
                'optimizer_calls': 0}
    save('freeze_manifest.json', manifest)
    sum_paths = paths + [HERE / 'freeze_manifest.json']
    sums = ''.join(digest(p) + '  ' + str(p.relative_to(REPO)) + '\n' for p in sum_paths)
    (HERE / 'SHA256SUMS').write_text(sums)
    print(json.dumps({'status': 'FROZEN_RELEASED', 'artifacts': len(paths),
                      'manifest_sha256': digest(HERE / 'freeze_manifest.json'),
                      'sha256sums_sha256': digest(HERE / 'SHA256SUMS'),
                      'receipt_sha256': digest(HERE / 'release_receipt.json'),
                      'report_sha256': digest(WORK / 'early_shared_x_joint.md'),
                      'symbolic_append_sha256': digest(HERE / 'symbolic_append.json.gz'),
                      'template_sha256': digest(HERE / 'fixed_point_feasibility_template.json.gz'),
                      'projection_sha256': digest(HERE / 'visible_prefix_projection.json.gz')}, indent=2))


if __name__ == '__main__':
    main()
