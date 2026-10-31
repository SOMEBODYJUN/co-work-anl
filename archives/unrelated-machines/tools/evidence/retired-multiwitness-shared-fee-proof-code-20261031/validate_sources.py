#!/usr/bin/env python3
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MAN = json.loads((ROOT / 'manifest.json').read_text())
checks = {}
for item in MAN['sources']:
    p = ROOT / item['evidence_file']
    checks[item['evidence_file']] = {
        'exists': p.exists(),
        'size': p.stat().st_size if p.exists() else None,
        'sha256': hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None,
        'matches_manifest': p.exists() and hashlib.sha256(p.read_bytes()).hexdigest() == MAN['evidence_hashes'][item['evidence_file']]['sha256'],
        'matches_source_fingerprint': p.exists() and hashlib.sha256(p.read_bytes()).hexdigest() == item['source_sha256'],
    }
status = all(v['exists'] and v['matches_manifest'] and v['matches_source_fingerprint'] for v in checks.values())
out = {'status': 'pass' if status else 'fail', 'checks': checks, 'scope': MAN['scope']}
print(json.dumps(out, ensure_ascii=False, indent=2))
if not status:
    raise SystemExit(1)
