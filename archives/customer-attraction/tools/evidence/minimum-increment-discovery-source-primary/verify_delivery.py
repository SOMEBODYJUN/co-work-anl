#!/usr/bin/env python3
"""Validate provenance and links without importing/executing the mathematical source."""
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
    evidence = stage / 'archives/customer-attraction/tools/evidence/minimum-increment-discovery-source-primary'
    work = stage / 'cleanup/workspaces/Boss4/r3-minimum-increment-discovery-source-primary'
    manifest = json.loads((evidence / 'source-manifest.json').read_text())
    assert manifest['primary_count'] == 1 and manifest['primary_bytes'] == 4440
    row = manifest['rows'][0]
    original = stage / row['stage_original_path']
    data = original.read_bytes()
    assert len(data) == row['size'] == 4440 and sha(original) == row['sha256']
    assert hashlib.sha1(b'blob 4440\0' + data).hexdigest() == row['blob']
    claim = json.loads((evidence / 'root-actual-claim7-receipt.json').read_text())
    assert claim['status'] == 'pushed' and claim['actor'] == 'Boss4' and len(claim['ids']) == 7
    assert row['id'] in claim['ids'] and claim['local_sync']['status'] == 'needs-attention'
    proof = json.loads((evidence / 'root-claim7-sync-preservation.json').read_text())
    assert not proof['missing'] and not proof['different'] and not proof['unmerged']
    assert proof['stash_kept'] and all(x['same'] for x in proof['tracked'])
    gate = json.loads((evidence / 'ownership-gate.json').read_text())
    owner = gate['source_owner_record']
    assert owner['owner'] == 'Boss4' and owner['disposition'] == 'in-progress'
    assert owner['source_sha256'] == row['sha256']
    receipts = json.loads((work / 'semantic-receipts.json').read_text())
    assert len(receipts) == 1 and receipts[0]['id'] == row['id']
    for field in ['full_file_reviewed', 'related_material_checked', 'unique_content_accounted_for']:
        assert receipts[0][field] is True
    for target in receipts[0]['targets']:
        assert (stage / target).is_file(), target
    bindings = json.loads((evidence / 'dependency-and-comparison-bindings.json').read_text())['rows']
    assert len(bindings) == 8
    for binding in bindings:
        p = repo / binding['path']
        assert p.stat().st_size == binding['size'] and sha(p) == binding['sha256']
    algorithms = list((stage / 'archives/customer-attraction/state').rglob('*.md'))
    assert len(algorithms) == 1
    links = []
    for p in algorithms + [evidence / 'README.md']:
        text = p.read_text()
        for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
            target = (p.parent / dest.split('#', 1)[0]).resolve()
            if not target.exists():
                assert (repo / target.relative_to(stage)).exists(), dest
            links.append(dest)
    content = json.loads((evidence / 'content-manifest.json').read_text())
    for binding in content:
        p = stage / binding['path']
        assert p.stat().st_size == binding['size'] and sha(p) == binding['sha256']
    relations = json.loads((evidence / 'relation-review.json').read_text())
    assert len(relations['relations']) == 3
    result = {
        'status': 'PASS', 'primary_sources': 1, 'primary_bytes': 4440,
        'new_algorithm_resource_files': 1, 'semantic_receipts': 1,
        'dependency_and_comparison_bindings': 8, 'explained_relations': 3,
        'markdown_links': len(links), 'original_program_entries': 0,
        'new_mathematical_entries': 0, 'raw_claim_sync_status_preserved': 'needs-attention',
        'separate_root_local_preservation_proof_passes': True,
        'scope': 'structural-byte-owner-record-link-validation-only'
    }
    (evidence / 'self-check-result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
