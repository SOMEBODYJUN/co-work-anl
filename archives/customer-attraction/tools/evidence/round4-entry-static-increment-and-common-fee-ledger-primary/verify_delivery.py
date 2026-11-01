#!/usr/bin/env python3
"""Byte, ownership, disposition and link checks; no mathematical source execution."""
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
    evidence = stage / 'archives/customer-attraction/tools/evidence/round4-entry-static-increment-and-common-fee-ledger-primary'
    work = stage / 'cleanup/workspaces/Boss4/r3-round4-entry-static-increment-and-common-fee-ledger-primary'
    source = json.loads((evidence / 'source-manifest.json').read_text())
    rows = source['rows']
    assert len(rows) == 2 and sum(row['size'] for row in rows) == 9220
    claim = json.loads((evidence / 'root-actual-claim14-receipt.json').read_text())
    assert claim['actor'] == 'Boss4' and claim['status'] == 'pushed'
    assert claim['local_sync']['status'] == 'synced' and len(claim['ids']) == 14
    gate = json.loads((evidence / 'ownership-gate.json').read_text())
    owners = {row['id']: row for row in gate['owner_records']}
    for row in rows:
        assert row['id'] in claim['ids']
        original = stage / row['stage_original_path']
        data = original.read_bytes()
        assert len(data) == row['size'] and sha(original) == row['sha256']
        assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == row['blob']
        assert owners[row['id']]['owner'] == 'Boss4'
        assert owners[row['id']]['disposition'] == 'in-progress'
        assert owners[row['id']]['source_sha256'] == row['sha256']
    receipts = json.loads((work / 'semantic-receipts.json').read_text())
    assert {row['id'] for row in receipts} == {row['id'] for row in rows}
    for receipt in receipts:
        assert receipt['disposition'] == 'integrated'
        for field in ['full_file_reviewed', 'related_material_checked', 'unique_content_accounted_for']:
            assert receipt[field] is True
        for target in receipt['targets']:
            assert (stage / target).is_file(), target
    comparison = json.loads((evidence / 'comparison-bindings.json').read_text())
    assert len(comparison['formal_whole_reads']) == 14
    for row in comparison['formal_whole_reads']:
        p = repo / row['repository_path']
        assert p.stat().st_size == row['size'] and sha(p) == row['sha256']
    bodies = sorted((stage / 'archives/customer-attraction/state').rglob('*.md'))
    assert len(bodies) == 3
    links = []
    for path in bodies + [evidence / 'README.md']:
        text = path.read_text()
        if path in bodies:
            assert text.startswith('---\n')
            for field in ['id', 'kind', 'type_tag', 'title', 'status', 'summary', 'source_refs']:
                assert re.search(r'^' + field + r':', text, re.M)
        for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
            target = (path.parent / dest.split('#', 1)[0]).resolve()
            if not target.exists():
                assert (repo / target.relative_to(stage)).exists(), (str(path), dest)
            links.append(dest)
    relations = json.loads((evidence / 'relation-review.json').read_text())
    assert relations['all_new_objects_have_explained_relationships']
    assert len(relations['rows']) == 8
    for row in json.loads((evidence / 'content-manifest.json').read_text()):
        p = stage / row['path']
        assert p.stat().st_size == row['size'] and sha(p) == row['sha256']
    result = {
        'status': 'PASS', 'primary_sources': 2, 'primary_bytes': 9220,
        'mathematical_body_files': 3, 'formal_full_read_bindings': 14,
        'semantic_receipts': 2, 'explained_relations': 8, 'markdown_links': len(links),
        'original_mathematical_entries': 0, 'new_mathematical_entries': 0,
        'only_assigned_two_claim_ids_processed': True,
        'scope': 'structural-byte-owner-record-link-check-only'
    }
    (evidence / 'self-check-result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
