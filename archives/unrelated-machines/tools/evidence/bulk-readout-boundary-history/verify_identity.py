#!/usr/bin/env python3
"""Verify preserved bytes and a historical prefix; execute no math programs."""
from pathlib import Path
import hashlib
import json
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
current = (here / 'comparisons/bulk_or_commit_two_witness_interpolation.md').read_bytes()
old = (here / 'derived/bulk_or_commit_canonical_v3_sections_1_5.md').read_bytes()
assert current[:8153] == old
assert len(old) == 8153 and old.endswith(b'\n')
assert hashlib.sha256(old).hexdigest() == 'df8d61b09dcdce43f7b76d50c8c981e80d91cdcce5a3a28b063e4cd317004a48'
print(json.dumps({'kind': 'source-byte-and-prefix-identity-only',
                  'python_version': sys.version, 'checked_sources': checks,
                  'old_v3_prefix_size': len(old),
                  'old_v3_prefix_sha256': hashlib.sha256(old).hexdigest(),
                  'old_v3_prefix_exact': True, 'mathematical_programs_run': 0},
                 ensure_ascii=False, indent=2))
