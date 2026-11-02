#!/usr/bin/env python3
"""Static delivery check only: no payoff, IC, background, LP or MILP rerun."""
import ast
import gzip
import hashlib
import json
from pathlib import Path
import re


def main():
    root = Path(__file__).resolve().parents[5]
    base = Path(__file__).resolve().parent
    manifest = json.loads((base/'source-manifest.json').read_text())
    checked = []
    for row in manifest['sources']+manifest['dependencies']+manifest['comparisons']+manifest['assets']:
        path = root/row['path']
        raw = path.read_bytes()
        assert len(raw) == row['bytes'], path
        assert hashlib.sha256(raw).hexdigest() == row['sha256'], path
        if 'blob' in row:
            assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest() == row['blob'], path
        checked.append(row['path'])
    for path in base.glob('*.py'):
        ast.parse(path.read_text())
    for path in base.rglob('*.json'):
        if path.name != 'self-check.json':
            json.loads(path.read_text())
    report = json.loads((base/'exact/exact-audit.json').read_text())
    ledger = gzip.decompress((base/'exact/full-history-ledger.json.gz').read_bytes())
    assert len(ledger) == report['ledger']['decoded_bytes']
    assert hashlib.sha256(ledger).hexdigest() == report['ledger']['decoded_sha256']
    rows = json.loads(ledger)
    assert len(rows) == 2
    assert all(len(row['full_history_comparisons']) == 1554 and len(row['root_query_rows']) == 56 and len(row['tail_query_rows']) == 6 for row in rows)
    execution = json.loads((base/'execution.json').read_text())
    assert execution['inputs_before'] == execution['inputs_after']
    assert execution['returncode'] == 0 and execution['stderr']['bytes'] == 0
    broken = []
    for name in manifest['bodies']+[str((base/'README.md').relative_to(root))]:
        path = root/name
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if '://' in target or target.startswith('#'):
                continue
            resolved = (path.parent/target.split('#')[0]).resolve()
            if resolved == base/'self-check.json':
                continue  # This invocation creates its own report below.
            if not resolved.exists():
                broken.append([name, target])
    assert not broken, broken
    result = dict(status='PASS', scope='Static fingerprints, syntax, delivery links and recorded ledger shape only; no mathematical rerun',
                  source_ids=[row['id'] for row in manifest['sources']], fingerprinted_paths=checked,
                  ledger_comparison_records=3108, broken_links=broken,
                  existing_0012_mathematical_reruns=0, independent_primary_audit_runs=1, independent_review_short_scripts=2)
    (base/'self-check.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({key:result[key] for key in ('status', 'scope', 'source_ids', 'ledger_comparison_records', 'broken_links')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
