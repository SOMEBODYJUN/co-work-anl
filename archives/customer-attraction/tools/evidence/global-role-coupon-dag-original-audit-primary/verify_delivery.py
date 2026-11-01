"""Structural delivery check only; no mathematical source imports or evaluation."""
from pathlib import Path
import hashlib
import json
import re
import sys


def main():
    stage = Path(sys.argv[1]).resolve()
    repository = Path(sys.argv[2]).resolve()
    er = 'archives/customer-attraction/tools/evidence/global-role-coupon-dag-original-audit-primary'
    wr = 'cleanup/workspaces/Boss4/r3-global-role-coupon-dag-original-audit-primary'
    evidence, workspace = stage / er, stage / wr
    read = lambda p: json.loads(p.read_text())
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    resolve = lambda rel: stage / rel if (stage / rel).is_file() else repository / rel
    for row in read(evidence / 'content-manifest.json')['files']:
        p = stage / row['path']
        assert p.is_file() and p.stat().st_size == row['size'] and digest(p) == row['sha256'], row['path']
    raw = read(evidence / 'root-actual-claim3-receipt.json')
    proof = read(evidence / 'root-independent-local-recovery-proof.json')
    gate = read(evidence / 'ownership-gate.json')
    assert raw['status'] == gate['claim_status'] == 'pushed'
    assert raw['actor'] == gate['actor'] == 'Boss4' and len(raw['ids']) == 3
    assert raw['remote_tip'] == gate['remote_tip']
    assert raw['local_sync']['status'] == gate['raw_local_sync_status'] == 'needs-attention'
    assert raw['local_sync'] == gate['raw_local_sync_unmodified']
    assert proof['receipt'] == 'boss4-resume-next3ug-claim'
    assert proof['stash'] in raw['local_sync']['detail']
    assert proof['untracked_count'] == 11 and proof['missing'] == proof['different'] == []
    assert len(proof['tracked']) == 2 and all(r['same'] is True for r in proof['tracked'])
    assert not proof['unmerged'] and proof['stash_kept'] is True
    assert gate['independent_root_recovery_proof'] == er + '/root-independent-local-recovery-proof.json'
    assert gate['proof_is_not_rewritten_raw_synced_status'] is True
    sources = read(evidence / 'source-manifest.json')['rows']
    by_id = {row['id']: row for row in gate['owner_records']}
    assert len(sources) == 3 and {r['id'] for r in sources} <= set(raw['ids'])
    for row in sources:
        p = stage / row['target_path']
        assert p.stat().st_size == row['size'] and digest(p) == row['sha256']
        b = p.read_bytes()
        assert hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() == row['blob']
        assert (p.read_bytes() == Path(row['local_path']).read_bytes())
        assert (stage / row['acquisition_target']).read_bytes() == Path(row['actual_normal_show_capture']).read_bytes()
        o = by_id[row['id']]
        assert (o['owner'], o['disposition'], o['source_sha256']) == ('Boss4', 'in-progress', row['sha256'])
    dependencies = read(evidence / 'dependency-bindings.json')['rows']
    for row in dependencies:
        p = repository / row['published_path']
        assert p.stat().st_size == row['size'] and digest(p) == row['sha256']
        assert not row['copied_again'] and not row['primary_or_done_by_this_batch']
    comparisons = read(evidence / 'comparison-bindings.json')['full_formal_objects_read']
    for row in comparisons:
        p = repository / row['path']
        assert p.stat().st_size == row['size'] and digest(p) == row['sha256']
    reportrow = next(r for r in sources if r['path'].endswith('global_role_coupon_hitting_audit.json'))
    report = read(stage / reportrow['target_path'])
    assert set(report) == {'status', 'scope', 'roles', 'history_contexts', 'local_threshold_mixtures',
                           'global_target_set_checks', 'global_weighted_price_checks', 'multisource_cut_checks',
                           'claims_actual_wallet_capacity', 'claims_half'}
    assert report['claims_actual_wallet_capacity'] is False and report['claims_half'] is False
    assert read(evidence / 'dependency-bindings.json')['external_runtime_input_files'] == 0
    receipts = read(workspace / 'semantic-receipts.json')
    assert {r['id'] for r in receipts} == {r['id'] for r in sources}
    for row in receipts:
        assert row['full_file_reviewed'] and row['related_material_checked'] and row['unique_content_accounted_for']
        assert row['current_original_mathematical_entries'] == row['current_new_mathematical_entries'] == 0
        assert row['raw_claim_local_sync'] == 'needs-attention'
        for path in row['targets']:
            assert resolve(path).is_file(), path
    links, ids = 0, []
    for p in stage.rglob('*.md'):
        if '/original/' in str(p):
            continue
        t = p.read_text()
        if '/state/' in str(p):
            assert t.startswith('---\n')
            front = t.split('---', 2)[1]
            for key in ['id', 'kind', 'type_tag', 'title', 'status', 'summary', 'source_refs']:
                assert re.search(r'^' + key + r':', front, re.M), (p, key)
            ids.append(re.search(r'^id:\s*(.+)$', front, re.M).group(1))
        for path in re.findall(r'\[[^\]]*\]\(([^)]+)\)', t):
            if path.startswith(('http:', 'https:', '#')):
                continue
            path = path.split('#')[0]
            q = (p.parent / path).resolve()
            try:
                rel = q.relative_to(stage)
            except ValueError:
                raise AssertionError(('outside-stage-relative-link', p, path))
            assert resolve(rel).is_file(), (p, path)
            links += 1
    assert len(ids) == len(set(ids)) == 1
    copylist = read(workspace / 'copy-files.json')
    assert sorted(copylist) == sorted(str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file())
    result = dict(status='PASS-STRUCTURE-ONLY', primary_files=len(sources), primary_bytes=sum(r['size'] for r in sources),
                  dependency_files=len(dependencies), dependency_bytes=sum(r['size'] for r in dependencies),
                  comparison_objects=len(comparisons), semantic_receipts=len(receipts), formal_objects=len(ids),
                  checked_markdown_links=links, copy_files=len(copylist), original_report_fields=len(report), external_runtime_input_files=0,
                  raw_claim_local_sync='needs-attention', independent_Root_zero_loss_proof_consistent=True,
                  original_source_imports=0, original_mathematical_CLI_runs=0, original_numeric_audit_runs=0, LP_or_MILP_runs=0, solver_runs=0,
                  IC_replay_runs=0, new_mathematical_program_runs=0,
                  note='Hashes, JSON/JSONL structure, owner snapshots, Root proof consistency and links only; no mathematical evaluation, solver or Git verification.')
    (evidence / 'self-check-result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
