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
def save(p, d):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')

configs = [
    ('0aa9e3e24287bba0', 'early-promotion', '054a363db68502978b67b753057ae2d422956cb4ccf3085735cb743a12e66a49', 1, 0),
    ('02c430616062bf42', 'cross-pair-point', '310731857dad9a24f3219938f10fad7be1391c9ce4e9c1bbd5129fbee63d54a7', 3, 2),
    ('0afd81e591a14e22', 'new60-envelope', 'f1b4bbe39d10f0b0b96a472a4c281f8ff48c7b1558b8324faf21969fd81846bb', 1, 0)
]
review_names = {'early-promotion': 'early-promotion', 'cross-pair-point': 'cross-pair', 'new60-envelope': 'new60'}
reg = read(R / 'research/registry.json'); obs = {o['object_id']: o for o in reg['objects']}
prepared = []
for suffix, name, defpin, edge_count, closed_count in configs:
    tid = 'customer-attraction-3a-3a-' + suffix
    w = B / ('wave14-' + name + '-worker')
    rp = f'map/receipts/{tid}.json'; ep = f'map/edges/{tid}'
    t = read(R / 'research/operations/map-v2/tasks' / (tid + '.json')); d = t['definition']
    assert t['state'] == 'claimed' and t['owner'] == 'Boss1', tid
    assert rr.pin(d) == defpin and all(rr.pin(obs[k]) == v for k, v in d['input_pins'].items()), tid
    receipt = read(w / rp)
    assert len(receipt.get('closed_overlaps', [])) == closed_count and not receipt.get('follow_up_tasks'), tid
    for a in receipt['assets']:
        assert sha(w / a['path']) == a['sha256'], a
    files = sorted(str(p.relative_to(w)) for p in (w / ep).rglob('*') if p.is_file())
    edges = []
    for path in files:
        assert any(path == wp or PurePosixPath(wp) in PurePosixPath(path).parents for wp in d['write_paths']), path
        assert not (R / path).exists(), path
        if Path(path).suffix == '.json':
            item = read(w / path)
            if isinstance(item, dict) and 'edge_id' in item:
                assert not any(k in item for k in ('endpoint_pins', 'evidence_pins', 'review_digest')), path
                edges.append(path)
    assert len(edges) == edge_count and not (R / rp).exists(), tid
    audit = A / ('wave14-' + name + '-delivery-review')
    assert not audit.exists()
    prepared.append((tid, name, w, rp, ep, d, receipt, files, edges, audit))

summaries = []; done = []
for tid, name, w, rp, ep, d, receipt, files, edges, audit in prepared:
    audit.mkdir()
    for path in files + [rp]:
        (R / path).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(w / path, R / path)
    shutil.copyfile(w / rp, audit / 'worker-original-receipt.json')
    shutil.copyfile(w / ep / 'prebind-freeze.json', audit / 'worker-frozen-manifest.json')
    shutil.copyfile(B / ('wave14-' + review_names[name] + '-root-review.md'), audit / 'root-mathematical-review.md')
    shutil.copyfile(Path(__file__), audit / 'stage-delivery.py')
    events = []
    for path in edges:
        for action in ('edge-bind', 'edge-check'):
            cmd = [sys.executable, 'work.py', 'research', action, path]
            if action == 'edge-bind': cmd.append('--write')
            p = subprocess.run(cmd, cwd=R, capture_output=True, text=True)
            events.append({'action': action, 'path': path, 'exit_code': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr})
            save(audit / 'native-binding-events.json', events)
            assert p.returncode == 0, p.stdout + p.stderr
    # Keep the worker's prebinding freeze byte-for-byte. Bindings and expanded
    # publication assets are recorded separately, without circular hashes.
    assert sha(R / ep / 'prebind-freeze.json') == sha(w / ep / 'prebind-freeze.json')
    receipt['assets'] = [{'path': path, 'sha256': sha(R / path)} for path in files]
    receipt['root_validation'] = {
        'reviewer': 'Boss1',
        'scope': 'Substantive source/target, derivation, finite-input identity and whole/contribution scope review; full evidence-reading responsibilities stated in root review.',
        'native_binding': 'Every new relation bound and checked; final SHA values recorded.',
        'asset_scope': 'All worker write-path proof, read-ledger, lossless-reading and prebinding materials are preserved, including additions to an initially edge-only receipt.',
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
    assert len(rels) == len(edges) and len(receipt['coverage']) == 1
    assert all(row['state'] == 'linked' for row in receipt['coverage'].values())
    assert all(edge['status'] == 'accepted' and edge['relation_mode'] == 'unconditional' for edge in rels.values())
    for asset in receipt['assets']: assert sha(R / asset['path']) == asset['sha256']
    summary = {
        'task_id': tid, 'definition_pin': rr.pin(d), 'receipt_path': rp,
        'receipt_sha256': sha(R / rp), 'receipt_pin': rr.pin(receipt),
        'input_pins': d['input_pins'], 'core_ids': d['object_ids'],
        'edge_count': len(edges), 'asset_count': len(files),
        'coverage': {'linked': 1, 'isolated-after-review': 0},
        'logical_edges': len(edges), 'context_edges': 0
    }
    save(audit / 'final-binding-manifest.json', {
        'worker_freeze_preserved_sha256': sha(R / ep / 'prebind-freeze.json'),
        'original_receipt_sha256': sha(w / rp),
        'final_receipt_sha256': sha(R / rp),
        'final_edges': [{'path': p, 'sha256': sha(R / p)} for p in edges],
        'original_asset_count': len(read(w / rp)['assets']), 'final_asset_count': len(files),
        'stage': 'Native bound/checked and receipt fully validated; checkpoint and done follow separately.'
    })
    save(audit / 'validation.json', {
        'status': 'NATIVE_FULL_RECEIPT_VALIDATION_PASSED', 'tasks': [summary],
        'root_review_sha256': sha(audit / 'root-mathematical-review.md'),
        'worker_freeze_sha256': sha(audit / 'worker-frozen-manifest.json'),
        'native_checks': ['definition', 'edge_bind_write', 'edge_check', 'asset_refs', 'supersession', 'batch_edges', 'require_edge_result', 'edge_paths', 'coverage', 'follow_ups_final_true'],
        'scientific_executions_by_Boss': 0
    })
    save(audit / 'done-records.json', [{'task_id': tid, 'receipt_file': rp}])
    summaries.append(summary); done.append({'task_id': tid, 'receipt_file': rp})
save(A / 'wave14-three-mature-done-records.json', done)
print(json.dumps({'status': 'NATIVE_FULL_RECEIPT_VALIDATION_PASSED', 'tasks': summaries}, ensure_ascii=False, indent=2))
