"""Install a reviewed source-status correction after preserving and handing off its live core."""
from pathlib import Path
import copy
import hashlib
import json
import subprocess
import sys

R = Path.cwd()
A = R / 'research/workspaces/map-v2/Boss1/session-1a53a6eb65ea'
F = R.parent / 'wave11-security2-worker/feedback-prefix-refutation'
sys.path.insert(0, str(R / 'tools'))
import research_runtime as rr

def read(p):
    return json.loads(p.read_text())

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def save(p, data):
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

tid = 'customer-attraction-3a-3a-c385b158f346250d'
t = read(R / 'research/operations/map-v2/tasks' / (tid + '.json'))
assert t['state'] == 'handoff' and t.get('owner') is None
assert rr.pin(t['definition']) == 'f7b9f8987dbf6000ab2e96a7536dd058c7931b99b5a32893742379e3c4a678e0'
preserved = A / 'wave11-security2-preserved-v1'
assert sha(preserved / f'map/receipts/{tid}.json') == '17af932a94d7440bf41bba5f55bd6539db498e988a981aaff7d4cd38d9d94732'
proposal = read(F / 'proposed-records.json')
path = proposal['source_path']
assert sha(R / path) == proposal['expected_old_source_sha256']
assert sha(F / 'ret-source-proposed.md') == proposal['proposed_source_sha256'] == '400665b8ed3932fb36b7562ced86c182c79852c58d2d2e254ccc87b77c0e0cbe'
regpath = R / 'research/registry.json'
reg = read(regpath)
before_reg_sha = sha(regpath)
before_baseline = copy.deepcopy(reg['baseline'])
basepath = R / before_baseline['path']
assert sha(basepath) == before_baseline['sha256']
baseline = read(basepath)
objects = {o['object_id']: o for o in reg['objects']}
before = {c['object_id']: copy.deepcopy(objects[c['object_id']]) for c in proposal['changes']}
affected = {o['object_id'] for o in reg['objects'] if any(ref['path'] == path for ref in [o['body'], *o['evidence']])}
assert affected == set(before)
for c in proposal['changes']:
    assert rr.pin(before[c['object_id']]) == c['old_pin']
for o in proposal['objects']:
    c = next(c for c in proposal['changes'] if c['object_id'] == o['object_id'])
    assert rr.pin(o) == c['proposed_pin']
    assert o['version'] == before[o['object_id']]['version'] + 1
    for ref in [o['body'], *o['evidence']]:
        if ref['path'] != path: assert sha(R / ref['path']) == ref['sha256']
    if o['object_id'] in ['M-140da849797c486ba0ad22e4dfbe2631', 'M-8a98d8d3ca9a42089dbad81715d6f020']:
        expected = copy.deepcopy(before[o['object_id']]); expected['version'] += 1
        for ref in expected['evidence']:
            if ref['path'] == path: ref['sha256'] = proposal['proposed_source_sha256']
        assert expected == o
    if o['object_id'] == 'optimal-comparison-pool-net-exchange-and-random-retention-identity':
        for k in ['title', 'kind', 'truth_status', 'model', 'statement', 'quantifiers', 'assumptions', 'sources']:
            assert o[k] == before[o['object_id']][k], k

for rows in [reg['materials'], baseline['materials']]:
    hits = [x for x in rows if x['path'] == path]
    assert len(hits) == 1 and hits[0]['sha256'] == proposal['expected_old_source_sha256']
old_text = (R / path).read_text()
(R / path).write_bytes((F / 'ret-source-proposed.md').read_bytes())
assert sha(R / path) == proposal['proposed_source_sha256']
replacement = {o['object_id']: copy.deepcopy(o) for o in proposal['objects']}
reg['objects'] = [replacement.get(o['object_id'], o) for o in reg['objects']]
for rows in [reg['materials'], baseline['materials']]:
    next(x for x in rows if x['path'] == path)['sha256'] = proposal['proposed_source_sha256']
newbase = R / 'research/registration/baseline-boss1-ret-prefix-refutation-20261112.json'
assert not newbase.exists()
baseline['coverage_note'] = baseline.get('coverage_note', '') + '；Boss1以既有完整SPE负前缀族纠正RET全前缀付款候选状态；SWAP/RET及两个局部反例数学保持，四个同页引用记录同步。'
baseline['commit'] = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=R, capture_output=True, text=True, check=True).stdout.strip()
save(newbase, baseline)
reg['baseline'] = {'path': newbase.relative_to(R).as_posix(), 'sha256': sha(newbase)}
rp = A / 'ret-prefix-source-proposed-registry.json'
save(rp, reg)
result = subprocess.run([sys.executable, 'work.py', 'research', 'register', '--record-file', rp.relative_to(R).as_posix()], cwd=R, capture_output=True, text=True)
print(result.stdout, end=''); print(result.stderr, end='')
assert result.returncode == 0
rp.unlink()
audit = {
    'status': 'registered-local-not-pushed', 'actor': 'Boss1',
    'preserved_task': tid, 'preservation_commit': '45fe2b5f844a87fe3a10bb6dd6f19ffc7c3e5e76',
    'before_registry_sha256': before_reg_sha, 'after_registry_sha256': sha(regpath),
    'old_baseline': before_baseline, 'new_baseline': reg['baseline'],
    'path': path, 'old_source_sha256': proposal['expected_old_source_sha256'],
    'new_source_sha256': proposal['proposed_source_sha256'],
    'changes': proposal['changes'], 'before_objects': list(before.values()),
    'after_objects': proposal['objects'],
    'mathematical_reason': 'Existing proved CA-PREFIX full-SPE family gives every n>=4 a unique optimal leaf support, d=1, L1=2(n-2)>n-1/n=P1; n4 gap1/4 while half margin6. Old00c291 coverage already identified L1>u1; this repairs a missed exact target/state connection, not a new counterexample discovery.',
    'unchanged_results': ['SWAP', 'RET', 'M140 local private-floor failure', 'M8a98 square-credit local failure', 'Q-CAG-HALF open target', 'D individual endpoint candidate'],
    'effective_done_holders_requiring_targeted_repair': ['boss5-eta-status-round55-repair-6cda1bce3d48b546', 'boss6-bank-status-repair-repair-5f402448a1964e8e'],
    'scientific_program_runs': 0,
    'next': 'Checkpoint source/registry/baseline, native refresh the handoff task, native repair both effective done holders, claim actual free slots and assign fresh workers; retain unaffected historical assets unchanged.'
}
save(A / 'ret-prefix-source-correction.json', audit)
print(json.dumps({'status': audit['status'], 'source_sha256': sha(R / path), 'changes': proposal['changes']}, ensure_ascii=False))
