"""Freeze the failed narrow span and independently verified whole-face proof.

Hashes retained raw inputs in place, every owned proof artifact, both
independent audits, and the main writeup. Does not access Git or registries.
"""
from datetime import datetime, timezone
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
PINS = {
    'maxb_augmented_lp/full_lift/exact_matrix.json.gz': 'c054aadf745ea4540233a3da693917498527d19d4ccecb0fdd34ad884e461e4b',
    'maxb_augmented_lp/full_lift/recovery/augmented_lp_exact.json': '5b1b649af5fc9d359e31dd03945d12708e599e0eeac75983ed188e60178b3bfe',
    'maxb_augmented_lp/full_lift/recovery/exact_dual_certificate.json': '4a6b6ca154ce645bcdabceb50bcb83982fead5875f257bf0a4c56f9576d7405f',
    'early_x_anchor_queries/rows_51.json': '0ad0b697193d7a8da2cc62275bbf9265912b0485d778d5edd93fc334bd8bb3eb',
}


def sha(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    for path, expected in PINS.items():
        assert sha(WORK / path) == expected
    runs = [
        (HERE, 'build_execution.json', 'build_optimum_face.py', 'build.stdout.jsonl', 'build.stderr.txt'),
        (HERE, 'verify_execution.json', 'verify_obstruction.py', 'verify.stdout.json', 'verify.stderr.txt'),
        (HERE / 'facial_zero_closure', 'build_execution.json', 'build_closure_and_span.py', 'build.stdout.jsonl', 'build.stderr.txt'),
        (HERE / 'facial_zero_closure', 'verify_execution.json', 'verify_closure_and_identity.py', 'verify.stdout.jsonl', 'verify.stderr.txt'),
    ]
    for root, record_name, script_name, stdout_name, stderr_name in runs:
        record = json.loads((root / record_name).read_text())
        assert record['exit_code'] == 0 and record['optimizer_calls'] == 0
        assert record['script_sha256'] == sha(root / script_name)
        assert record['stdout_sha256'] == sha(root / stdout_name)
        assert record['stderr_sha256'] == sha(root / stderr_name)
        assert (root / stderr_name).read_bytes() == b''
    narrow = json.loads((HERE / 'independent_audit.json').read_text())
    final = json.loads((HERE / 'facial_zero_closure/independent_audit.json').read_text())
    assert narrow['status'] == 'PASS_EXACT_REQUESTED_SPAN_OBSTRUCTION'
    assert final['status'] == 'PASS_EXACT_WHOLE_W10_OPTIMUM_FACE_EXCLUDED_BY_AP39'
    assert Fraction(final['whole_W10_optimum_face_AP39_value']) < 0
    assert final['strict_quantitative_lower_bound_derived'] is False
    assert final['optimizer_calls'] == 0 and final['displayed_primal_zeros_used_as_premises'] is False
    manifest_path = HERE / 'freeze_manifest.json'
    sums_path = HERE / 'SHA256SUMS'
    assert not manifest_path.exists() and not sums_path.exists()
    files = sorted(p for p in HERE.rglob('*') if p.is_file())
    files.append(WORK / 'early_ap_optimum_face.md')
    entries = [{'path': str(p.relative_to(WORK)), 'sha256': sha(p), 'bytes': p.stat().st_size}
               for p in sorted(files)]
    manifest = {
        'status': 'FROZEN', 'frozen_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'early_ap_optimum_face/ and early_ap_optimum_face.md only',
        'source_sha256': PINS,
        'raw_inputs_retained_unchanged_at_pinned_paths': True,
        'narrow_span_result': narrow['status'],
        'facial_closure_result': final['status'],
        'whole_W10_optimum_face_AP39_value': final['whole_W10_optimum_face_AP39_value'],
        'old_W10': final['old_W10'],
        'strict_quantitative_lower_bound_derived': False,
        'exact_new_optimum_claim': False, 'SPE_claim': False,
        'optimizer_calls': 0, 'git_writes': 0, 'registry_writes': 0,
        'all_four_executions_exit_zero_and_source_hashes_match': True,
        'files': entries,
        'manifest_and_SHA256SUMS_excluded_from_recursive_file_list': True,
    }
    with manifest_path.open('x') as out:
        json.dump(manifest, out, ensure_ascii=False, indent=2)
        out.write('\n')
    sums = [entry['sha256'] + '  ' + entry['path'] for entry in entries]
    sums.append(sha(manifest_path) + '  ' + str(manifest_path.relative_to(WORK)))
    with sums_path.open('x') as out:
        out.write('\n'.join(sums) + '\n')
    for entry in entries:
        assert sha(WORK / entry['path']) == entry['sha256']
    print(json.dumps({'status': 'FROZEN_AND_HASHES_RECHECKED', 'artifacts': len(entries),
                      'manifest_sha256': sha(manifest_path), 'SHA256SUMS_sha256': sha(sums_path),
                      'whole_face_identity_sha256': final['expanded_identity_sha256'],
                      'independent_audit_sha256': sha(HERE / 'facial_zero_closure/independent_audit.json')},
                     ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    main()
