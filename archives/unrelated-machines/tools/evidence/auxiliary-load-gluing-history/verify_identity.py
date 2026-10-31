#!/usr/bin/env python3
"""Verify eight preserved source byte identities, without running mathematics."""
import hashlib
import json
from pathlib import Path
import sys

here = Path(__file__).resolve().parent
stage = here.parents[4]
manifest = json.loads((here / 'manifest.json').read_text())
checks = []
for group in ('originals', 'comparisons'):
    for row in manifest[group]:
        data = (stage / row['evidence_path']).read_bytes()
        actual = hashlib.sha256(data).hexdigest()
        assert len(data) == row['size'], row['id']
        assert actual == row['sha256'], row['id']
        checks.append({'id': row['id'], 'size': len(data), 'sha256': actual})
print(json.dumps({'kind': 'source-byte-identity-only', 'python_version': sys.version,
                  'checked_sources': checks, 'mathematical_programs_run': 0},
                 ensure_ascii=False, indent=2))
