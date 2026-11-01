#!/usr/bin/env python3
"""Structural evidence checker. Does not execute the mathematical verifier again."""
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
    evidence = stage / 'archives/customer-attraction/tools/evidence/static-module-affine-and-short-certificate-primary'
    work = stage / 'cleanup/workspaces/Boss4/r3-static-module-affine-and-short-certificate-primary'
    source = json.loads((evidence / 'source-manifest.json').read_text())
    rows = source['rows']
    assert len(rows) == 5 and sum(r['size'] for r in rows) == 16533
    assert sum(r['path'].endswith('.md') for r in rows) == 2
    assert sum(r['path'].endswith('.json') for r in rows) == 2
    assert sum(r['path'].endswith('.py') for r in rows) == 1
    claim = json.loads((evidence / 'actual-full-next8-claim.json').read_text())
    assert claim['status'] == 'pushed' and claim['actor'] == 'Boss4'
    assert claim['remote_tip'] == '2ef4ffeda474e2ed42cad04d959b39da48a3dc23'
    assert claim['local_sync']['status'] == 'needs-attention'
    preservation = json.loads((evidence / 'claim-sync-preservation.json').read_text())
    assert preservation['stash'] in claim['local_sync']['detail']
    assert preservation['untracked_count'] == 166 and not preservation['missing'] and not preservation['different']
    assert len(preservation['tracked']) == 2 and all(r['same'] for r in preservation['tracked'])
    assert preservation['unmerged'] == '' and preservation['stash_kept']
    for row in rows:
        assert row['id'] in claim['ids'] and row['full_text_read']
        path = stage / row['stage_path']
        data = path.read_bytes()
        assert len(data) == row['size'] and digest(path) == row['sha256']
        assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == row['blob']
        own = json.loads((evidence / 'ownership' / (row['id'] + '.json')).read_text())
        assert own['owner'] == 'Boss4' and own['disposition'] == 'in-progress' and own['source_sha256'] == row['sha256']
    immutable = json.loads((evidence / 'source-immutability-before-after.json').read_text())
    assert immutable['all_five_originals_unchanged'] and immutable['original_CLI_runs'] == 1
    assert {r['id'] for r in immutable['rows']} == {r['id'] for r in rows}
    for row in immutable['rows']:
        assert row['unchanged'] and row['expected_before_sha256'] == row['normal_show_source_after_sha256'] == row['staged_original_after_sha256']
    run = evidence / 'runs/one-original-cli'
    execution = json.loads((run / 'execution.json').read_text())
    assert execution['original_CLI_runs'] == 1 and execution['original_import_runs'] == 0
    assert execution['exit_code'] == 0 and execution['optimize'] == 0 and execution['all_assertions_active']
    assert execution['argv'][1:3] == ['-I', '-B'] and '-O' not in execution['argv'] and '-OO' not in execution['argv']
    assert execution['source_code_sha256'] == digest(run / 'verify_static_module_bound.py')
    assert execution['stderr_bytes'] == 0 and (run / 'stderr.txt').stat().st_size == 0
    assert execution['stdout_sha256'] == digest(run / 'stdout.txt') and execution['stderr_sha256'] == digest(run / 'stderr.txt')
    assert (run / 'stdout.txt').read_text().endswith('Short analytic certificate exact checks passed: Cauchy constants, polynomial, symmetries, 21 orbits.\n')
    by_id = {r['id']: r for r in rows}
    for output in execution['outputs']:
        path = stage / output['output_path']
        frozen = stage / by_id[output['source_id']]['stage_path']
        assert output['byte_equal_to_frozen'] and digest(path) == output['sha256'] == output['source_sha256']
        assert path.read_bytes() == frozen.read_bytes()
    receipts = json.loads((work / 'semantic-receipts.json').read_text())
    assert {r['id'] for r in receipts} == {r['id'] for r in rows}
    for row in receipts:
        assert row['disposition'] == 'retained'
        assert all(row[k] for k in ['full_file_reviewed', 'related_material_checked', 'unique_content_accounted_for'])
        for key in ['read_note', 'comparison_note', 'decision_note']:
            assert len(row[key]) >= 20
        for target in row['targets']:
            assert any((root / target).is_file() for root in roots), target
    comparisons = json.loads((evidence / 'comparison-manifest.json').read_text())['rows']
    assert len(comparisons) == 8
    for row in comparisons:
        path = stage / row['snapshot_path']
        assert path.stat().st_size == row['size'] and digest(path) == row['sha256']
    content = json.loads((evidence / 'content-manifest.json').read_text())
    for row in content:
        path = stage / row['path']
        assert path.stat().st_size == row['size'] and digest(path) == row['sha256']
    math = sorted((stage / 'archives/customer-attraction/state').rglob('*.md'))
    assert len(math) == 2
    links = 0
    for path in math + [evidence / 'README.md']:
        text = path.read_text()
        if path in math:
            for key in ['id', 'kind', 'type_tag', 'title', 'status', 'summary', 'source_refs']:
                assert re.search(r'^' + key + r':', text, re.M)
        for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
            if link.startswith(('https:', 'http:', '#')):
                continue
            rel = (path.parent / link.split('#', 1)[0]).resolve().relative_to(stage)
            assert any((root / rel).exists() for root in roots), (str(path), link)
            links += 1
    relationships = json.loads((evidence / 'relation-evidence.json').read_text())
    assert relationships['all_new_objects_have_explained_relationships'] and len(relationships['rows']) == 8
    result = {
        'status': 'PASS', 'scope': 'structural-existing-run-evidence-check; no-mathematical-entry-reexecution',
        'primary_sources': 5, 'primary_bytes': 16533, 'new_formal_markdown_files': 2,
        'formal_comparison_snapshots': 8, 'semantic_receipts': 5, 'explained_relations': 8,
        'checked_markdown_links': links, 'content_manifest_files': len(content),
        'original_CLI_runs_preserved': 1, 'new_math_entries_run_by_checker': 0,
        'complete_outputs_byte_equal': True, 'originals_unchanged': True,
        'raw_claim_sync_status': 'needs-attention', 'separate_root_zero_difference_preservation_evidence_kept': True,
        'mathematics_review': 'see full theorem and mathematical-self-check.md; not inferred from structural PASS'
    }
    (evidence / 'self-check-result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
