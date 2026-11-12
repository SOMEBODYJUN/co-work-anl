"""Root-only staging of already reviewed, frozen wave16 deliveries."""
from pathlib import Path, PurePosixPath
import hashlib, json, shutil, subprocess, sys

B = Path('/workspace/scratch/1a53a6eb65ea')
R = B / 'co-work-anl-boss1'
A = R / 'research/workspaces/map-v2/Boss1/session-1a53a6eb65ea'
sys.path.insert(0, str(R / 'tools'))
import research_runtime as rr
import map_tasks as mt

def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

conf_path = Path(sys.argv[1])
conf = read(conf_path)
reg = read(R / 'research/registry.json')
obs = {o['object_id']: o for o in reg['objects']}
prepared = []
for c in conf['deliveries']:
    tid = c['task_id']
    w = B / c['worker_dir']
    rp = f'map/receipts/{tid}.json'
    ep = f'map/edges/{tid}'
    t = read(R / 'research/operations/map-v2/tasks' / (tid + '.json'))
    d = t['definition']
    assert (t['state'], t['owner']) == ('claimed', 'Boss1'), tid
    assert rr.pin(d) == c['definition_pin'], tid
    assert all(rr.pin(obs[k]) == v for k, v in d['input_pins'].items()), tid
    receipt = read(w / rp)
    for asset in receipt['assets']:
        assert sha(w / asset['path']) == asset['sha256'], asset
    files = sorted(str(p.relative_to(w)) for p in (w / ep).rglob('*') if p.is_file())
    assert set(files) == {a['path'] for a in receipt['assets']}, (tid, 'Unlisted or nonlocal asset')
    assert (w / ep / c['freeze']).exists(), tid
    edges = []
    for path in files:
        assert any(path == wp or PurePosixPath(wp) in PurePosixPath(path).parents for wp in d['write_paths']), path
        assert not (R / path).exists(), path
        if Path(path).suffix == '.json':
            item = read(w / path)
            if isinstance(item, dict) and 'edge_id' in item:
                assert not any(k in item for k in ('endpoint_pins', 'evidence_pins', 'review_digest')), path
                assert item['reviewed_by'] == 'Boss1' and item['status'] == 'accepted', path
                edges.append(path)
    assert len(edges) == c['edge_count'] and not (R / rp).exists(), tid
    assert set(receipt['coverage']) == set(d['object_ids']), tid
    audit = A / c['audit_name']
    assert not audit.exists(), audit
    root_review = B / c['root_review']
    assert root_review.exists(), root_review
    prepared.append((c, tid, w, rp, ep, d, receipt, files, edges, audit, root_review))

summaries = []
done = []
for c, tid, w, rp, ep, d, receipt, files, edges, audit, root_review in prepared:
    audit.mkdir()
    for path in files + [rp]:
        (R / path).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(w / path, R / path)
    shutil.copyfile(w / rp, audit / 'worker-original-receipt.json')
    shutil.copyfile(w / ep / c['freeze'], audit / 'worker-frozen-manifest.json')
    shutil.copyfile(root_review, audit / 'root-mathematical-review.md')
    shutil.copyfile(Path(__file__), audit / 'stage-delivery.py')
    shutil.copyfile(conf_path, audit / 'stage-config.json')
    if c.get('read_add_log'):
        shutil.copyfile(B / c['read_add_log'], audit / 'read-add-receipt.txt')
    events = []
    for path in edges:
        for action in ('edge-bind', 'edge-check'):
            cmd = [sys.executable, 'work.py', 'research', action, path]
            if action == 'edge-bind': cmd.append('--write')
            p = subprocess.run(cmd, cwd=R, capture_output=True, text=True)
            events.append({'action': action, 'path': path, 'exit_code': p.returncode,
                           'stdout': p.stdout, 'stderr': p.stderr})
            save(audit / 'native-binding-events.json', events)
            assert p.returncode == 0, p.stdout + p.stderr
    assert sha(R / ep / c['freeze']) == sha(w / ep / c['freeze'])
    receipt['assets'] = [{'path': path, 'sha256': sha(R / path)} for path in files]
    receipt['root_validation'] = {
        'reviewer': 'Boss1',
        'scope': 'Source/target, derivation, fixed-input identity, actual model and whole/contribution/context scope substantively reviewed; reading responsibilities recorded in root review.',
        'native_binding': 'Every new relation bound and checked. Final bound hashes are separate from the preserved original worker freeze.',
        'asset_scope': 'All original worker proof, input contracts, read-ledgers, reversible reading views and prebinding manifests preserved.',
        'scientific_reruns': 0,
        'root_review_path': str((audit / 'root-mathematical-review.md').relative_to(R))
    }
    save(R / rp, receipt)
    rows = [read(p) for p in (R / 'research/operations/map-v2/tasks').glob('*.json')]
    mt.validate(R, d, 'map', objects=obs)
    mt._asset_refs(R, d, receipt, canonical=set(reg['edge_files']))
    mt._supersession(R, d, receipt, rows, 'map')
    rels, edge_files = mt.batch_edges(R, d, receipt, obs)
    for edge in rels.values(): rr.require_edge_result(edge)
    edge_paths = {read(R / p)['edge_id']: p for p in edge_files}
    mt._check_edge_paths(R, d, receipt, [row for row in rows if row['definition']['task_id'] != tid], edge_paths, reg['edge_files'])
    mt._map_receipt_coverage(d, receipt, obs, rels)
    rr.validate_map_follow_ups(d, receipt, rows, obs, final=True)
    assert len(rels) == c['edge_count']
    assert all(e['status'] == 'accepted' for e in rels.values())
    assert sum(e['relation_mode'] == 'unconditional' for e in rels.values()) == c['logical_edges']
    assert sum(e['relation_mode'] == 'context' for e in rels.values()) == c['context_edges']
    for asset in receipt['assets']: assert sha(R / asset['path']) == asset['sha256']
    summary = {
        'task_id': tid, 'definition_pin': rr.pin(d), 'receipt_path': rp,
        'receipt_sha256': sha(R / rp), 'receipt_pin': rr.pin(receipt),
        'input_pins': d['input_pins'], 'core_ids': d['object_ids'],
        'edge_count': len(edges), 'asset_count': len(files),
        'coverage': {s: sum(v['state'] == s for v in receipt['coverage'].values()) for s in ('linked', 'isolated-after-review')},
        'logical_edges': c['logical_edges'], 'context_edges': c['context_edges']
    }
    save(audit / 'final-binding-manifest.json', {
        'worker_freeze_preserved_sha256': sha(R / ep / c['freeze']),
        'original_receipt_sha256': sha(w / rp), 'final_receipt_sha256': sha(R / rp),
        'final_edges': [{'path': p, 'sha256': sha(R / p)} for p in edges],
        'original_asset_count': len(read(w / rp)['assets']), 'final_asset_count': len(files),
        'stage': 'Native bound/checked and full receipt validated; checkpoint and done follow separately.'
    })
    save(audit / 'validation.json', {
        'status': 'NATIVE_FULL_RECEIPT_VALIDATION_PASSED', 'tasks': [summary],
        'root_review_sha256': sha(audit / 'root-mathematical-review.md'),
        'worker_freeze_sha256': sha(audit / 'worker-frozen-manifest.json'),
        'native_checks': ['definition', 'edge_bind_write', 'edge_check', 'asset_refs', 'supersession', 'batch_edges', 'require_edge_result', 'edge_paths', 'coverage', 'follow_ups_final_true'],
        'scientific_executions_by_Boss': 0
    })
    save(audit / 'done-records.json', [{'task_id': tid, 'receipt_file': rp}])
    summaries.append(summary)
    done.append({'task_id': tid, 'receipt_file': rp})
save(A / conf['done_filename'], done)
print(json.dumps({'status': 'NATIVE_FULL_RECEIPT_VALIDATION_PASSED', 'tasks': summaries}, ensure_ascii=False, indent=2))
