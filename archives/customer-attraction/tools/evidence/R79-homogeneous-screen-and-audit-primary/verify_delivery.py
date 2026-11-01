#!/usr/bin/env python3
"""Structural evidence check only. It does not certify mathematical truth or push state."""
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
    parser.add_argument('--prior-stage', type=Path)
    args = parser.parse_args()
    stage = args.stage_root.resolve()
    roots = [stage]
    if args.repository_root:
        roots.append(args.repository_root.resolve())
    if args.prior_stage:
        roots.append(args.prior_stage.resolve())
    evidence = stage / 'archives/customer-attraction/tools/evidence/R79-homogeneous-screen-and-audit-primary'
    work = stage / 'cleanup/workspaces/Boss4/r3-R79-homogeneous-screen-and-audit-primary'
    rows = json.loads((evidence / 'source-manifest.json').read_text())['rows']
    assert len(rows) == 5 and sum(r['size'] for r in rows) == 26643
    claim = json.loads((evidence / 'actual-full-next20-claim.json').read_text())
    assert claim['status'] == 'pushed' and claim['actor'] == 'Boss4'
    assert claim['local_sync']['status'] == 'synced'
    assert claim['remote_tip'] == 'c526dcd14714c47beab04912f6746d7b35a734e3'
    for row in rows:
        assert row['id'] in claim['ids']
        path = stage / row['stage_path']
        raw = path.read_bytes()
        assert len(raw) == row['size'] and digest(path) == row['sha256']
        assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == row['blob']
        own = json.loads((evidence / 'ownership' / (row['id'] + '.json')).read_text())
        assert own['owner'] == 'Boss4' and own['disposition'] == 'in-progress'
        assert own['source_sha256'] == row['sha256']
        assert row['full_text_read'] is True
    receipts = json.loads((work / 'semantic-receipts.json').read_text())
    assert {r['id'] for r in receipts} == {r['id'] for r in rows}
    assert sum(r['disposition'] == 'duplicate' for r in receipts) == 2
    assert sum(r['disposition'] == 'retained' for r in receipts) == 3
    for row in receipts:
        assert all(row[k] for k in ['full_file_reviewed', 'related_material_checked', 'unique_content_accounted_for'])
        for key in ['read_note', 'comparison_note', 'decision_note']:
            assert len(row[key]) >= 20
        for target in row['targets']:
            assert any((root / target).is_file() for root in roots), target
    comparisons = json.loads((evidence / 'comparison-manifest.json').read_text())['rows']
    assert len(comparisons) == 10
    for row in comparisons:
        snap = stage / row['snapshot_path']
        assert snap.stat().st_size == row['size'] and digest(snap) == row['sha256']
    duplicate = json.loads((evidence / 'duplicate-mapping.json').read_text())
    assert len(duplicate) == 2
    for row in duplicate:
        candidates = [root / row['target'] for root in roots if (root / row['target']).is_file()]
        assert any(digest(path) == row['target_sha256_at_comparison'] for path in candidates)
        assert len(row['whole_source_unique_sections_covered']) == 6
    content = json.loads((evidence / 'content-manifest.json').read_text())
    for row in content:
        path = stage / row['path']
        assert path.stat().st_size == row['size'] and digest(path) == row['sha256']
    math = sorted((stage / 'archives/customer-attraction/state').rglob('*.md'))
    assert len(math) == 2
    checked_links = 0
    for path in math + [evidence / 'README.md']:
        text = path.read_text()
        if path in math:
            for field in ['id', 'kind', 'type_tag', 'title', 'status', 'summary', 'source_refs']:
                assert re.search(r'^' + field + r':', text, re.M)
        for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
            if link.startswith(('https:', 'http:', '#')):
                continue
            target = (path.parent / link.split('#', 1)[0]).resolve()
            rel = target.relative_to(stage)
            assert any((root / rel).exists() for root in roots), (str(path), link)
            checked_links += 1
    relations = json.loads((evidence / 'relation-evidence.json').read_text())
    assert len(relations['rows']) == 7 and relations['all_new_objects_have_explained_relationships']
    supplement = json.loads((evidence / 'supplement-provenance.json').read_text())
    assert supplement['original_source_content'] is False and supplement['new_program_runs'] == 0
    assert supplement['decision_nodes'] == 7 and supplement['including_self_action_values'] == 14
    result = {
        'status': 'PASS', 'scope': 'structural-byte-identity-record-check-only',
        'primary_sources': 5, 'primary_bytes': 26643, 'sameSHA_prior_related_reuses': 2,
        'new_whole_MD_reads': 3, 'new_formal_markdown_files': 2,
        'exact_duplicate_receipts': 2, 'retained_receipts': 3,
        'formal_comparison_snapshots': 10, 'explained_relations': 7,
        'checked_markdown_links': checked_links, 'content_manifest_files': len(content),
        'original_code_JSON_source_reads': 0, 'math_program_runs': 0,
        'prior_PS_checkpoint_is_required_before_duplicate_done': True,
        'mathematics_review': 'see mathematical-self-check.md and full proofs; not proved by checker'
    }
    (evidence / 'self-check-result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
