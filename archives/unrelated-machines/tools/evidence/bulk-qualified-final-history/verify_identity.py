#!/usr/bin/env python3
"""Check original bytes, canonical slices and exact draft diff; no math run."""
from pathlib import Path
import difflib
import hashlib
import json
import sys

here = Path(__file__).resolve().parent
stage = here.parents[4]
manifest = json.loads((here / 'manifest.json').read_text())
checks = []
for group in ('originals', 'comparisons', 'derived'):
    for row in manifest[group]:
        data = (stage / row['evidence_path']).read_bytes()
        actual = hashlib.sha256(data).hexdigest()
        assert len(data) == row['size'], row.get('id', row['evidence_path'])
        assert actual == row['sha256'], row.get('id', row['evidence_path'])
        checks.append({'group': group, 'id': row.get('id'),
                       'size': len(data), 'sha256': actual})
full = (here / 'comparisons/bulk_or_commit_two_witness_interpolation.md').read_bytes()
prefix = (here / 'derived/canonical_v3_prefix_8153B.md').read_bytes()
suffix = (here / 'derived/canonical_v4_suffix_after_8153B.md').read_bytes()
assert prefix + suffix == full and len(prefix) == 8153
assert hashlib.sha256(prefix).hexdigest() == 'df8d61b09dcdce43f7b76d50c8c981e80d91cdcce5a3a28b063e4cd317004a48'
a = (here / 'comparisons/bulk_or_commit_two_witness_interpolation_append_sections_6_10_v4.md').read_text().splitlines(keepends=True)
b = suffix.decode().splitlines(keepends=True)
patch = ''.join(difflib.unified_diff(a, b, fromfile='frozen-append-baaebc27',
                                     tofile='final-suffix-from-current-fa574190'))
assert patch == (here / 'append-to-final-suffix.patch').read_text()
print(json.dumps({'kind': 'byte-and-scope-slice-check-only',
                  'python_version': sys.version, 'checked_files': checks,
                  'old_v3_prefix_bytes': len(prefix), 'v4_suffix_bytes': len(suffix),
                  'two_slices_exactly_reconstitute_current': True,
                  'exact_append_diff_verified': True, 'mathematical_programs_run': 0},
                 ensure_ascii=False, indent=2))
