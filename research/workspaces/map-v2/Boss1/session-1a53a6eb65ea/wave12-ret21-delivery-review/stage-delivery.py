from pathlib import Path, PurePosixPath
import hashlib
import json
import shutil
import subprocess
import sys

B = Path('/workspace/scratch/1a53a6eb65ea')
R = B / 'co-work-anl-boss1'
W = B / 'wave12-ret21-repair-worker'
A = R / 'research/workspaces/map-v2/Boss1/session-1a53a6eb65ea/wave12-ret21-delivery-review'
TID = 'boss1-wave12-ret-source-repair-1559410bdf704b13'
OLD = 'boss5-eta-status-round55-repair-6cda1bce3d48b546'
sys.path.insert(0, str(R / 'tools'))
import research_runtime as rr
import map_tasks as mt

def read(p):
    return json.loads(p.read_text())

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def save(p, data):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

t = read(R / 'research/operations/map-v2/tasks' / (TID + '.json'))
d = t['definition']
assert t['state'] == 'claimed' and t['owner'] == 'Boss1'
assert rr.pin(d) == '711c01b839c5e9f6c62677f218630852dad6f4ddc2436f032731a4a6f19540da'
assert d['supersedes'] == [OLD]
reg = read(R / 'research/registry.json')
obs = {o['object_id']: o for o in reg['objects']}
assert all(rr.pin(obs[k]) == v for k, v in d['input_pins'].items())
rp = f'map/receipts/{TID}.json'
ep = f'map/edges/{TID}/retained-comparison-pool-controls-static-private-block-loss.json'
fp = f'map/edges/{TID}/freeze-inputs.json'
assert sha(W / rp) == '2fa9755f360493925613767542e0b37d0dac4ecf4434eb4f4bb053962b88ef43'
assert sha(W / fp) == 'df3cee8b212b15cf8b12446ba8e321834f7daa0ef7cdecb8c93598c46ce4967c'
assert sha(W / ep) == '7c6774e92d9923876522406a87e60002ba0f236b3eecd6efc8055dc11f6bf103'
receipt = read(W / rp)
freeze = read(W / fp)
assert freeze['input_pins'] == d['input_pins']
assert set(receipt['supersession']) == {OLD}
dispositions = receipt['supersession'][OLD]['assets']
assert len(dispositions) == 19
assert sum(x['disposition'] == 'retained' for x in dispositions.values()) == 18
assert sum(x['disposition'] == 'replaced' for x in dispositions.values()) == 1
assert not receipt.get('closed_overlaps') and not receipt.get('follow_up_tasks')
assert len(receipt['assets']) == 19
for x in receipt['assets']:
    assert sha((W if x['path'] == ep else R) / x['path']) == x['sha256'], x['path']
new_files = sorted((W / f'map/edges/{TID}').iterdir()) + [W / rp]
assert len(new_files) == 6
for f in new_files:
    p = f.relative_to(W).as_posix()
    assert any(p == w or PurePosixPath(w) in PurePosixPath(p).parents for w in d['write_paths'])
    assert not (R / p).exists(), p
for f in new_files:
    p = f.relative_to(W)
    (R / p).parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(f, R / p)
A.mkdir(parents=True, exist_ok=True)
shutil.copyfile(W / fp, A / 'worker-frozen-manifest.json')
shutil.copyfile(Path(__file__), A / 'stage-delivery.py')
(A / 'root-mathematical-review.md').write_text('''# Boss1：RET21当前源版本替代主审

Root完整审读本次review、新边、21核心coverage、19资产与唯一替代的supersession，补读工具曾截断的中间三核心；原00c291数学包由Boss1建立。本对话已完整核读RET v3、CA-PREFIX与n4字面证书，并重新推导以下比较。33当前对象pin与93证据引用的冻结清单逐一核验；worker的14新读与79成熟继承不混称全面重读。没有重跑科学程序。

## 固定根池的静态比较

固定根最优m槽索引元组，O为其覆盖并集。沿actual前缀C_t，随机均匀保留m−t个比较索引所得J是一个合法补全，因此F_{m−t}(C_t)至少为E|C_t∪T_J|。客户在d个索引出现，被全删概率是binom(t,d)/binom(m,d)。所以S_t=OPT−F_{m−t}(C_t)≤L_t，L_t必须含−|C_t\\O|退款。重复标签仍按索引计，不需要SPE；t=0两者零，t=m二者均OPT−W。它只给静态上界，未付实际钱包。

局部重启须另固定当前P及r槽最优T：令O_h=P∪T、D_j为该池私块、e=|S\\O_h|、H=F_{r−1}(P∪S)、δ=F_r(P)−H。每个删除j的合法补全给ε_j=H−[F_r(P)+e−|D_j\\S|]≥0，故lost_j−new=δ+ε_j，均匀一步L1=δ+平均ε。这个局部池不能在全根随机保留过程中默换；完整private ledger仍要同枝SHARE、IC与共同付款。边只贡献这些精确公式，remaining明示开放的共同终点义务。

## 对已被否全前缀的准确处置

独立CA-PREFIX族n≥4中，每叶有n−2名独占客户，任意最优n槽池只能各叶一次，所以每客户d=1。首步S1=L1=2(n−2)>P1=n−1/n；n4为4>15/4。i≥2时C_i=A∪B、F=W+(n−i)(n−2)，S_i=L_i=i(n−2)，而P_i−L_i=i(2−1/n)−(i−1)/(n−1)>0。全前缀付款已被否，不再作为开放普遍前提；终点2W−OPT=2(n−1)>0，half与允许暂欠后结的机制未被否。该族同时否两个全前缀谓词，不声称严格分离RET全前缀与动态全前缀。m2数值L>S且两边均已支付也不能提供谓词分离。

## 未受影响的十八关系与谱系

当前B?加private ledger到half仍是条件终点总账，不依赖每一前缀都非负。regular/singleton价格、最后响应交换、静态query与安全成本、reply identity、ordered joint tail、有限价格、七maxima遗漏支持、root菜单信用、ETA修正、重赋/均匀收缩和two-remaining分别保持自身量词、背景、真实后继及剩余义务。ETA保当前round55边e272aaa对应修正，不能复活旧14fd历史。waterfill两个核心仍因自由三客户与固定高尾质量语境不同而隔离，已有context保引用作用，不强添数学边。

19prior逐项18retained/1replaced，唯一supersedes是现役round55 holder；旧00c291和14fd仅历史谱系。四历史closure留在supersession.retained_closed_overlaps，不冒作当前任务formal follow-up。21core精确19linked、2isolated；新边稳定ID保留，旧路径已退出canonical，新路径绑定当前版本。审读文档不伪造为receipt数学edge资产，均由同一write_paths独立保存。原生完整检查与推送成功后才可done。
''')
events = []
for action in ['edge-bind', 'edge-check']:
    cmd = [sys.executable, 'work.py', 'research', action, ep]
    if action == 'edge-bind':
        cmd.append('--write')
    c = subprocess.run(cmd, cwd=R, text=True, capture_output=True)
    events.append({'action': action, 'path': ep, 'exit_code': c.returncode, 'stdout': c.stdout, 'stderr': c.stderr})
    save(A / 'native-binding-events.json', events)
    assert c.returncode == 0, c.stdout + c.stderr
freeze['bound_new_edge'] = {'path': ep, 'sha256': sha(R / ep)}
freeze['publication_status'] = 'Root native bound and checked; original frozen snapshot retained; await pushed checkpoint then done'
save(R / fp, freeze)
for x in receipt['assets']:
    if x['path'] == ep:
        x['sha256'] = sha(R / ep)
save(R / rp, receipt)
rows = [read(p) for p in (R / 'research/operations/map-v2/tasks').glob('*.json')]
mt.validate(R, d, 'map', objects=obs)
mt._asset_refs(R, d, receipt, canonical=set(reg['edge_files']))
mt._supersession(R, d, receipt, rows, 'map')
rels, files = mt.batch_edges(R, d, receipt, obs)
for e in rels.values():
    rr.require_edge_result(e)
epaths = {read(R / p)['edge_id']: p for p in files}
mt._check_edge_paths(R, d, receipt, [x for x in rows if x['definition']['task_id'] != TID], epaths, reg['edge_files'])
mt._map_receipt_coverage(d, receipt, obs, rels)
rr.validate_map_follow_ups(d, receipt, rows, obs, final=True)
assert len(rels) == 19 and len(receipt['coverage']) == 21
assert sum(x['state'] == 'linked' for x in receipt['coverage'].values()) == 19
for x in receipt['assets']:
    assert sha(R / x['path']) == x['sha256']
summary = {'task_id': TID, 'definition_pin': rr.pin(d), 'receipt_path': rp,
           'receipt_sha256': sha(R / rp), 'receipt_pin': rr.pin(receipt),
           'input_pins': d['input_pins'], 'core_ids': d['object_ids'],
           'coverage': {'linked': 19, 'isolated-after-review': 2},
           'edge_count': 19, 'new_edge_count': 1, 'asset_count': 19,
           'retained_canonical_edges': 18, 'supersedes': [OLD],
           'prior_dispositions': {'retained': 18, 'replaced': 1}}
report = {'status': 'NATIVE_FULL_RECEIPT_VALIDATION_PASSED', 'tasks': [summary],
          'root_review_sha256': sha(A / 'root-mathematical-review.md'),
          'worker_manifest_sha256': sha(W / fp), 'bound_manifest_sha256': sha(R / fp),
          'scientific_executions_by_Boss': 0,
          'native_checks': ['definition', 'edge_bind_write', 'edge_check', 'asset_refs', 'supersession', 'batch_edges', 'require_edge_result', 'edge_paths', 'coverage', 'follow_ups_final_true']}
save(A / 'validation.json', report)
save(A / 'done-records.json', [{'task_id': TID, 'receipt_file': rp}])
print(json.dumps({'status': report['status'], 'task': summary}, ensure_ascii=False, indent=2))
