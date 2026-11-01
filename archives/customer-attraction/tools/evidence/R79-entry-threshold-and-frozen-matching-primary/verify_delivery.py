#!/usr/bin/env python3
"""Byte/identity/record/link checks only; mathematical proof is in the Markdown."""
import argparse
import hashlib
import json
import re
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage-root', type=Path, default=Path(__file__).resolve().parents[5])
    parser.add_argument('--repository-root', type=Path)
    args = parser.parse_args()
    stage = args.stage_root.resolve()
    roots = [stage, (args.repository_root or stage).resolve()]
    evidence = stage / 'archives/customer-attraction/tools/evidence/R79-entry-threshold-and-frozen-matching-primary'
    work = stage / 'cleanup/workspaces/Boss4/r3-R79-entry-threshold-and-frozen-matching-primary'
    rows = json.loads((evidence / 'source-manifest.json').read_text())['rows']
    assert len(rows) == 4 and sum(r['size'] for r in rows) == 14958
    claim = json.loads((evidence / 'actual-full-next23-claim.json').read_text())
    assert claim['actor'] == 'Boss4' and claim['status'] == 'pushed'
    assert claim['local_sync']['status'] == 'synced'
    assert claim['remote_tip'] == 'ceb4c5bbd4e8b695a901d6b56709169e75c1dd60'
    for row in rows:
        assert row['id'] in claim['ids'] and row['full_text_read']
        path = stage / row['stage_path']
        data = path.read_bytes()
        assert len(data) == row['size'] and digest(path) == row['sha256']
        assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == row['blob']
        owner = json.loads((evidence / 'ownership' / (row['id'] + '.json')).read_text())
        assert owner['owner'] == 'Boss4' and owner['disposition'] == 'in-progress'
        assert owner['source_sha256'] == row['sha256']
        capture = json.loads((evidence / 'acquisition/normal-show' / Path(row['actual_normal_show_capture']).name).read_text())['source']
        assert capture['id'] == row['id'] and capture['sha256'] == row['sha256']
    receipts = json.loads((work / 'semantic-receipts.json').read_text())
    assert {r['id'] for r in receipts} == {r['id'] for r in rows}
    assert sum(r['disposition'] == 'duplicate' for r in receipts) == 1
    assert sum(r['disposition'] == 'retained' for r in receipts) == 3
    for row in receipts:
        assert all(row[k] for k in ['full_file_reviewed', 'related_material_checked', 'unique_content_accounted_for'])
        for key in ['read_note', 'comparison_note', 'decision_note']:
            assert len(row[key]) >= 20
        for target in row['targets']:
            assert any((root / target).is_file() for root in roots), target
    comparisons = json.loads((evidence / 'comparison-manifest.json').read_text())['rows']
    assert len(comparisons) == 14
    for row in comparisons:
        path = stage / row['snapshot_path']
        assert path.stat().st_size == row['size'] and digest(path) == row['sha256']
    duplicate = json.loads((evidence / 'duplicate-mapping.json').read_text())
    assert len(duplicate) == 1
    for row in duplicate:
        assert any((root / row['target']).is_file() and digest(root / row['target']) == row['target_sha256'] for root in roots)
        assert len(row['covered_unique_content']) == 4
    content = json.loads((evidence / 'content-manifest.json').read_text())
    for row in content:
        path = stage / row['path']
        assert path.stat().st_size == row['size'] and digest(path) == row['sha256']
    math = sorted((stage / 'archives/customer-attraction/state').rglob('*.md'))
    assert len(math) == 2
    links = 0
    for path in math + [evidence / 'README.md']:
        body = path.read_text()
        if path in math:
            for field in ['id', 'kind', 'type_tag', 'title', 'status', 'summary', 'source_refs']:
                assert re.search(r'^' + field + r':', body, re.M)
        for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', body):
            if link.startswith(('https:', 'http:', '#')):
                continue
            target = (path.parent / link.split('#', 1)[0]).resolve().relative_to(stage)
            assert any((root / target).exists() for root in roots), (str(path), link)
            links += 1
    relationships = json.loads((evidence / 'relation-evidence.json').read_text())
    assert relationships['all_new_objects_have_explained_relationships'] and len(relationships['rows']) == 8
    updates = json.loads((evidence / 'state-updates.json').read_text())
    assert len(updates) == 3 and all(r['original_bytes_changed'] is False for r in updates)
    supplement = json.loads((evidence / 'supplement-provenance.json').read_text())
    assert supplement['original_source_had_full_strategy'] is False
    assert supplement['decision_nodes'] == 21 and supplement['math_program_runs'] == 0
    result = {
        'status': 'PASS', 'scope': 'structural-byte-identity-record-check-only',
        'primary_count': 4, 'primary_bytes': 14958, 'new_formal_markdown_files': 2,
        'receipts': 4, 'duplicate': 1, 'retained': 3, 'formal_snapshots': 14,
        'explained_relations': 8, 'source_state_updates': 3,
        'checked_markdown_links': links, 'content_manifest_files': len(content),
        'original_code_JSON_source_reads': 0, 'math_program_runs': 0,
        'mathematics_review': 'full Markdown and mathematical-self-check.md, not established by this checker'
    }
    (evidence / 'self-check-result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
