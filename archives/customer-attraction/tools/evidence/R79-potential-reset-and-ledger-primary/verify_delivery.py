#!/usr/bin/env python3
"""Check delivery bytes, ownership evidence, records and links; not mathematical truth."""
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
    repo = (args.repository_root or stage).resolve()
    evidence = stage / 'archives/customer-attraction/tools/evidence/R79-potential-reset-and-ledger-primary'
    work = stage / 'cleanup/workspaces/Boss4/r3-R79-potential-reset-and-ledger-primary'
    source = json.loads((evidence / 'source-manifest.json').read_text())
    primary = [r for r in source['rows'] if r['primary']]
    related = [r for r in source['rows'] if not r['primary']]
    assert len(primary) == 5 and sum(r['size'] for r in primary) == 18680
    assert len(related) == 2 and sum(r['size'] for r in related) == 9987
    for row in source['rows']:
        path = stage / row['stage_path']
        data = path.read_bytes()
        assert len(data) == row['size']
        assert digest(path) == row['sha256']
        assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == row['blob']
        assert row['full_text_read'] and not row['code_or_json_source']
        capture = evidence / 'acquisition/normal-show' / Path(row['actual_normal_show_capture']).name
        observed = json.loads(capture.read_text())['source']
        assert observed['id'] == row['id'] and observed['sha256'] == row['sha256']
    active = {r['id']: r for r in json.loads((evidence / 'boss4-resumed-active36.json').read_text())}
    for row in primary:
        assert active[row['id']]['owner'] == 'Boss4'
        assert active[row['id']]['state'] == 'in-progress'
    receipts = json.loads((work / 'semantic-receipts.json').read_text())
    assert {r['id'] for r in receipts} == {r['id'] for r in primary}
    for receipt in receipts:
        for key in ['full_file_reviewed', 'related_material_checked', 'unique_content_accounted_for']:
            assert receipt[key] is True
        for key in ['read_note', 'comparison_note', 'decision_note']:
            assert len(receipt[key]) >= 20
        assert receipt['disposition'] == 'retained'
        for target in receipt['targets']:
            assert (stage / target).is_file()
    content = json.loads((evidence / 'content-manifest.json').read_text())
    for entry in content:
        path = stage / entry['path']
        assert path.stat().st_size == entry['size'] and digest(path) == entry['sha256']
    comparison = json.loads((evidence / 'comparison-manifest.json').read_text())['rows']
    assert len(comparison) == 16
    for entry in comparison:
        snapshot = stage / entry['snapshot_path']
        assert digest(snapshot) == entry['sha256'] and snapshot.stat().st_size == entry['size']
    math_paths = sorted((stage / 'archives/customer-attraction/state').rglob('*.md'))
    assert len(math_paths) == 3
    checked_links = []
    for path in math_paths + [evidence / 'README.md']:
        text = path.read_text()
        if path in math_paths:
            assert text.startswith('---\n')
            for field in ['id', 'kind', 'type_tag', 'title', 'status', 'summary', 'source_refs']:
                assert re.search(r'^' + field + r':', text, re.M)
        for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
            if link.startswith(('https:', 'http:', '#')):
                continue
            target = (path.parent / link.split('#', 1)[0]).resolve()
            if not target.exists():
                rel = target.relative_to(stage)
                assert (repo / rel).exists(), (str(path), link)
            checked_links.append({'from': str(path.relative_to(stage)), 'target': link})
    relations = json.loads((evidence / 'relation-evidence.json').read_text())
    assert relations['all_new_objects_have_explained_relationships']
    assert len(relations['rows']) == 8
    result = {
        'status': 'PASS', 'primary_count': 5, 'primary_bytes': 18680,
        'related_count': 2, 'related_bytes': 9987, 'new_math_objects': 3,
        'content_manifest_files': len(content), 'formal_comparison_snapshots': 16,
        'semantic_receipts': len(receipts), 'explained_relations': len(relations['rows']),
        'checked_markdown_links': len(checked_links), 'original_math_runs': 0,
        'new_mathematical_runs': 0, 'scope': 'structural-byte-record-check-only',
        'mathematics_review': 'see mathematical-self-check.md; not replaced by this program'
    }
    (evidence / 'self-check-result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
