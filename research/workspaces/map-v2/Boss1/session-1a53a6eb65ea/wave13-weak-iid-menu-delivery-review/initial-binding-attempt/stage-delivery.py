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
    {
        'task': 'customer-attraction-3a-3a-2262055787552638', 'worker': 'wave13-weak-iid-menu-worker',
        'definition': 'b8d9c106e0a2b87152078b9a334194c07647bd276970adc429049234270233b7',
        'receipt': '7d0c036c13b3bfe97a8e71613f828b57e05febf98b0bee7b983753b4e9a2b99c',
        'freeze': 'worker-freeze.json', 'freeze_sha': '83612fc9d05ce65b04cd3bb4e75e1c5f46d771eebac5ab7a0405991769c5dd84',
        'root_review': 'wave13-weak-iid-root-review.md', 'audit': 'wave13-weak-iid-menu-delivery-review',
        'assets': 4, 'linked': 2, 'context': 0
    },
    {
        'task': 'customer-attraction-3a-3a-2046e308df0b7867', 'worker': 'wave13-role-refund-worker',
        'definition': '78c0aec39ca443c9698ca05af8ee84e5b4b0b082f01450ecb0e642cc8de34f74',
        'receipt': '9493eaeb6f8b53505b3a4773cfb716db5d822f6a21f0b95cf13230f467bff698',
        'freeze': 'freeze.json', 'freeze_sha': '21c5d437bd8c99c5db017079a167b8b218f5fca4ddf9d3d8f7f585ad3f2cb765',
        'root_review': 'wave13-role-refund-root-review.md', 'audit': 'wave13-role-refund-delivery-review',
        'assets': 6, 'linked': 1, 'context': 1
    }
]
reg = read(R / 'research/registry.json')
obs = {o['object_id']: o for o in reg['objects']}
prepared = []
for c in configs:
    tid = c['task']; w = B / c['worker']; rp = f'map/receipts/{tid}.json'; fp = f'map/edges/{tid}/{c["freeze"]}'
    t = read(R / 'research/operations/map-v2/tasks' / (tid + '.json')); d = t['definition']
    assert t['state'] == 'claimed' and t['owner'] == 'Boss1', tid
    assert rr.pin(d) == c['definition'], tid
    assert all(rr.pin(obs[k]) == v for k, v in d['input_pins'].items()), tid
    assert sha(w / rp) == c['receipt'] and sha(w / fp) == c['freeze_sha'], tid
    receipt = read(w / rp)
    assert len(receipt['assets']) == c['assets'], tid
    assert not receipt.get('closed_overlaps') and not receipt.get('follow_up_tasks'), tid
    assert not d.get('overlap_comparisons'), tid
    edges = []
    for asset in receipt['assets']:
        path = asset['path']
        assert any(path == wp or PurePosixPath(wp) in PurePosixPath(path).parents for wp in d['write_paths']), path
        assert sha(w / path) == asset['sha256'] and not (R / path).exists(), path
        if Path(path).suffix == '.json':
            item = read(w / path)
            if isinstance(item, dict) and 'edge_id' in item: edges.append(path)
    assert len(edges) == 2 and not (R / rp).exists(), tid
    assert not (A / c['audit']).exists(), tid
    prepared.append((c, w, rp, fp, d, receipt, edges))

all_summaries = []; done = []
for c, w, rp, fp, d, receipt, edges in prepared:
    tid = c['task']; audit = A / c['audit']; audit.mkdir()
    for asset in receipt['assets'] + [{'path': rp}]:
        path = asset['path']; (R / path).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(w / path, R / path)
    if not (R / fp).exists(): shutil.copyfile(w / fp, R / fp)
    shutil.copyfile(w / fp, audit / 'worker-frozen-manifest.json')
    shutil.copyfile(B / c['root_review'], audit / 'root-mathematical-review.md')
    shutil.copyfile(Path(__file__), audit / 'stage-delivery.py')
    events = []
    for path in edges:
        for action in ['edge-bind', 'edge-check']:
            cmd = [sys.executable, 'work.py', 'research', action, path]
            if action == 'edge-bind': cmd.append('--write')
            p = subprocess.run(cmd, cwd=R, capture_output=True, text=True)
            events.append({'action': action, 'path': path, 'exit_code': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr})
            save(audit / 'native-binding-events.json', events)
            assert p.returncode == 0, p.stdout + p.stderr
    freeze = read(R / fp)
    freeze['boss_binding'] = {
        'scope': 'Original worker fields and hashes above remain a pre-binding semantic snapshot. These final edge hashes record the subsequent native binding.',
        'edges': [{'path': path, 'sha256': sha(R / path)} for path in edges],
        'status': 'Native bound and checked; receipt validation and pushed checkpoint are separate subsequent gates',
        'scientific_reruns': 0
    }
    save(R / fp, freeze)
    for asset in receipt['assets']:
        if asset['path'] in edges or asset['path'] == fp: asset['sha256'] = sha(R / asset['path'])
    receipt['root_validation'] = {
        'reviewer': 'Boss1', 'scope': 'Full source/target/derivation and coverage review with evidence scopes in the audit report',
        'native_binding': 'All two new relations bound and checked; final asset hashes recorded',
        'scientific_reruns': 0
    }
    save(R / rp, receipt)
    rows = [read(p) for p in (R / 'research/operations/map-v2/tasks').glob('*.json')]
    mt.validate(R, d, 'map', objects=obs)
    mt._asset_refs(R, d, receipt, canonical=set(reg['edge_files']))
    mt._supersession(R, d, receipt, rows, 'map')
    rels, files = mt.batch_edges(R, d, receipt, obs)
    for edge in rels.values(): rr.require_edge_result(edge)
    edge_paths = {read(R / path)['edge_id']: path for path in files}
    mt._check_edge_paths(R, d, receipt, [row for row in rows if row['definition']['task_id'] != tid], edge_paths, reg['edge_files'])
    mt._map_receipt_coverage(d, receipt, obs, rels)
    rr.validate_map_follow_ups(d, receipt, rows, obs, final=True)
    assert len(rels) == 2 and len(receipt['coverage']) == 2
    assert sum(row['state'] == 'linked' for row in receipt['coverage'].values()) == c['linked']
    assert sum(edge['relation_mode'] == 'context' for edge in rels.values()) == c['context']
    for asset in receipt['assets']: assert sha(R / asset['path']) == asset['sha256']
    summary = {
        'task_id': tid, 'definition_pin': rr.pin(d), 'receipt_path': rp,
        'receipt_sha256': sha(R / rp), 'receipt_pin': rr.pin(receipt),
        'input_pins': d['input_pins'], 'core_ids': d['object_ids'],
        'edge_count': 2, 'asset_count': len(receipt['assets']),
        'coverage': {'linked': c['linked'], 'isolated-after-review': 2-c['linked']},
        'logical_edges': 2-c['context'], 'context_edges': c['context']
    }
    save(audit / 'validation.json', {
        'status': 'NATIVE_FULL_RECEIPT_VALIDATION_PASSED', 'tasks': [summary],
        'root_review_sha256': sha(audit / 'root-mathematical-review.md'),
        'worker_freeze_sha256': c['freeze_sha'], 'bound_freeze_sha256': sha(R / fp),
        'native_checks': ['definition', 'edge_bind_write', 'edge_check', 'asset_refs', 'supersession', 'batch_edges', 'require_edge_result', 'edge_paths', 'coverage', 'follow_ups_final_true'],
        'scientific_executions_by_Boss': 0
    })
    save(audit / 'done-records.json', [{'task_id': tid, 'receipt_file': rp}])
    all_summaries.append(summary); done.append({'task_id': tid, 'receipt_file': rp})
save(A / 'wave13-two-mature-done-records.json', done)
print(json.dumps({'status': 'NATIVE_FULL_RECEIPT_VALIDATION_PASSED', 'tasks': all_summaries}, ensure_ascii=False, indent=2))
