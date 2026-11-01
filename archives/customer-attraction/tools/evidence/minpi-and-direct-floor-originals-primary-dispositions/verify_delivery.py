#!/usr/bin/env python3
"""Structural provenance validation only; never import or execute mathematical sources."""
import argparse
import hashlib
import json
import re
from pathlib import Path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage-root', type=Path, default=Path(__file__).resolve().parents[5])
    parser.add_argument('--repository-root', type=Path)
    args = parser.parse_args()
    stage = args.stage_root.resolve()
    repo = (args.repository_root or stage).resolve()
    evidence = stage / 'archives/customer-attraction/tools/evidence/minpi-and-direct-floor-originals-primary-dispositions'
    work = stage / 'cleanup/workspaces/Boss4/r3-minpi-and-direct-floor-originals-primary-dispositions'
    binding = json.loads((evidence / 'source-binding.json').read_text())
    rows = binding['rows']
    assert len(rows) == 5 and sum(row['size'] for row in rows) == 22262
    claim = json.loads((evidence / 'root-actual-claim12-receipt.json').read_text())
    assert claim['status'] == 'pushed' and claim['actor'] == 'Boss4'
    assert claim['local_sync']['status'] == 'synced' and len(claim['ids']) == 12
    gate = json.loads((evidence / 'ownership-gate.json').read_text())
    owners = {x['id']: x for x in gate['actual_local_owner_records']}
    for row in rows:
        assert row['id'] in claim['ids']
        original = repo / row['published_original_path']
        data = original.read_bytes()
        assert len(data) == row['size'] and sha(original) == row['sha256']
        assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == row['blob']
        assert row['current_role'] == 'primary-first-disposition'
        assert row['published_bytes_reused_without_copy'] is True
        assert owners[row['id']]['owner'] == 'Boss4'
        assert owners[row['id']]['disposition'] == 'in-progress'
        assert owners[row['id']]['source_sha256'] == row['sha256']
    receipts = json.loads((work / 'semantic-receipts.json').read_text())
    assert {x['id'] for x in receipts} == {x['id'] for x in rows}
    for receipt in receipts:
        assert receipt['disposition'] == 'duplicate'
        for key in ['full_file_reviewed', 'related_material_checked', 'unique_content_accounted_for']:
            assert receipt[key] is True
        for target in receipt['targets']:
            assert (stage / target).is_file() or (repo / target).is_file(), target
    allbindings = json.loads((evidence / 'comparison-and-dependency-bindings.json').read_text())
    assert len(allbindings['formal_whole_reads']) == 7
    assert len(allbindings['supporting_whole_reads']) == 2
    for row in allbindings['formal_whole_reads'] + allbindings['supporting_whole_reads']:
        target = repo / row['path']
        assert target.stat().st_size == row['size'] and sha(target) == row['sha256']
    coverage = json.loads((evidence / 'duplicate-coverage.json').read_text())
    assert {x['id'] for x in coverage['rows']} == {x['id'] for x in rows}
    for row in coverage['rows']:
        assert len(row['covers']) >= 4
        assert (repo / row['semantic_target']).is_file()
    links = []
    for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)', (evidence / 'README.md').read_text()):
        target = (evidence / dest.split('#', 1)[0]).resolve()
        if not target.exists():
            relative = target.relative_to(stage)
            assert (repo / relative).exists(), dest
        links.append(dest)
    content = json.loads((evidence / 'content-manifest.json').read_text())
    for row in content:
        p = stage / row['path']
        assert p.stat().st_size == row['size'] and sha(p) == row['sha256']
    result = {
        'status': 'PASS', 'primary_sources': 5, 'primary_source_bytes': 22262,
        'duplicate_receipts': len(receipts), 'formal_full_read_bindings': 7,
        'supporting_full_read_bindings': 2, 'markdown_links': len(links),
        'new_mathematical_objects': 0, 'original_bytes_newly_copied': 0,
        'original_mathematical_entries': 0, 'new_mathematical_entries': 0,
        'scope': 'byte-owner-record-link-check; mathematics-in-self-check-and-existing-bodies'
    }
    (evidence / 'self-check-result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
