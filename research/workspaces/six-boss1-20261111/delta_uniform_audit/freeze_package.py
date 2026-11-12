#!/usr/bin/env python3
"""Freeze this completed audit exactly once, then perform read-only checks."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

OUT = Path(__file__).resolve().parent
WS = OUT.parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


assert not (OUT/'freeze_manifest.json').exists(), 'Already frozen; do not overwrite.'
assert not (OUT/'SHA256SUMS').exists(), 'Already frozen; do not overwrite.'
checks = {
    'audit_result.json':'PASS_MAIN72_AND_STRICTER_GAMMA36_UNIVERSAL_CERTIFICATE',
    'second_literal_check_result.json':'PASS_SECOND_LITERAL_CHECK_NO_PRODUCER_IMPORTS',
    'positive_source_scope_check.json':'PASS_ALL_OLD_POSITIVE_ROWS_ARBITRARY_LEGAL_SIX_QUERY_UNION',
    'source_pins_and_immutability.json':'PASS_ALL_PINNED_BYTES_UNCHANGED',
    'proof_transcription_check.json':'PASS_FULL_PROOF_READ_AND_EXACT_VALUES',
}
for f,status in checks.items():
    assert read(OUT/f)['status']==status,(f,status)
pins = read(OUT/'source_pins_and_immutability.json')['source_pins']
for f,h in read(OUT/'positive_source_scope_check.json')['source_pins'].items():
    assert f not in pins or pins[f]==h
    pins[f]=h
for f,h in pins.items():
    assert sha(WS/f)==h,('source changed',f)
main_manifest = read(WS/'main_delta_uniform_improvement/freeze_manifest.json')
for f,h in main_manifest['artifacts'].items():
    assert sha(WS/f)==h,('Main frozen artifact changed',f)
all_files = sorted([p for p in OUT.rglob('*') if p.is_file()] + [WS/'delta_uniform_audit.md'])
artifacts = {str(p.relative_to(WS)):sha(p) for p in all_files}
manifest = {
    'status':'FROZEN_INDEPENDENT_GAMMA36_UNIFORM_IMPROVEMENT',
    'audit_id':'B1-DELTA-UNIFORM-AUDIT-20261112',
    'actual_agent_id':'/root/delta_uniform_audit',
    'RUN':'six-boss1-20261111',
    'frozen_utc':datetime.now(timezone.utc).isoformat(),
    'optimizer_calls':0,'producer_python_imports':0,
    'source_pins':pins,
    'Main_frozen_package_byte_unchanged':True,
    'raw_rows_retained':3056,'columns_retained':513,'affine_rhs_minus_one_rows_retained':30,
    'certificate_gamma36_sha256':sha(OUT/'certificate_gamma36.json'),
    'certificate_gamma72_sha256':sha(OUT/'certificate_gamma72.json'),
    'alpha36':read(OUT/'certificate_gamma36.json')['alpha_new'],
    'scope':'Original full-history common-catalog six-player pure SPE, arbitrary six legal query union. Half remains OPEN.',
    'artifacts':artifacts,
    'write_scope':['delta_uniform_audit/','delta_uniform_audit.md'],
    'stop_policy':'No writes after this manifest and SHA256SUMS are completed.',
}
manifest_path=OUT/'freeze_manifest.json'
with manifest_path.open('x') as f:
    f.write(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
all_hashes={**artifacts,'delta_uniform_audit/freeze_manifest.json':sha(manifest_path)}
sums_path=OUT/'SHA256SUMS'
with sums_path.open('x') as f:
    f.write(''.join(f'{h}  {p}\n' for p,h in sorted(all_hashes.items())))
assert all(sha(WS/f)==h for f,h in all_hashes.items())
assert all(sha(WS/f)==h for f,h in pins.items())
print(json.dumps({'status':manifest['status'],'audit_id':manifest['audit_id'],
                  'actual_agent_id':manifest['actual_agent_id'],
                  'artifact_count_excluding_manifest_and_sums':len(artifacts),
                  'manifest_sha256':sha(manifest_path),'SHA256SUMS_sha256':sha(sums_path),
                  'certificate_gamma36_sha256':manifest['certificate_gamma36_sha256'],
                  'certificate_gamma72_sha256':manifest['certificate_gamma72_sha256'],
                  'proof_sha256':sha(OUT/'proof.md'),
                  'adjacent_summary_sha256':sha(WS/'delta_uniform_audit.md'),
                  'source_checks':'PASS','writes_stopped':True},ensure_ascii=False,indent=2))
