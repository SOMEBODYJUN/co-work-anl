#!/usr/bin/env python3
"""Verify source/slice/snapshot bytes and version diffs, no math programs."""
from pathlib import Path
import hashlib
import difflib
import json
import sys

here = Path(__file__).resolve().parent
stage = here.parents[4]
manifest = json.loads((here / 'manifest.json').read_text())
checked = []
for group in ('originals', 'comparisons', 'derived', 'derived_page_snapshots'):
    for row in manifest[group]:
        data = (stage / row['evidence_path']).read_bytes()
        actual = hashlib.sha256(data).hexdigest()
        assert len(data) == row['size']
        assert actual == row['sha256']
        checked.append({'group': group, 'id': row.get('id'),
                        'size': len(data), 'sha256': actual})
full = (here / 'comparisons/bulk_or_commit_two_witness_interpolation.md').read_bytes()
prefix = (here / 'derived/canonical_v3_prefix_8153B.md').read_bytes()
suffix = (here / 'derived/canonical_v4_suffix_after_8153B.md').read_bytes()
assert prefix + suffix == full and len(prefix) == 8153
assert hashlib.sha256(prefix).hexdigest() == 'df8d61b09dcdce43f7b76d50c8c981e80d91cdcce5a3a28b063e4cd317004a48'
for row in json.loads((here / 'version-differences.json').read_text()):
    a = stage / row['old_path']
    b = stage / row['new_path']
    patch = ''.join(difflib.unified_diff(a.read_text().splitlines(keepends=True),
                                       b.read_text().splitlines(keepends=True),
                                       fromfile=row['old_path'], tofile=row['new_path']))
    assert patch == (stage / row['patch']).read_text()
print(json.dumps({'kind': 'source-byte-and-version-identity-only',
                  'python_version': sys.version, 'checked_files': checked,
                  'old_v3_prefix_exact': True, 'two_version_diffs_exact': True,
                  'mathematical_programs_executed': 0}, ensure_ascii=False, indent=2))
