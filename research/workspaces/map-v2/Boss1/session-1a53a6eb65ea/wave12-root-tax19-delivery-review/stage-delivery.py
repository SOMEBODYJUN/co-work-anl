from pathlib import Path, PurePosixPath
import hashlib
import json
import shutil
import subprocess
import sys

B = Path('/workspace/scratch/1a53a6eb65ea')
R = B / 'co-work-anl-boss1'
W = B / 'wave12-root-tax19-repair-worker'
A = R / 'research/workspaces/map-v2/Boss1/session-1a53a6eb65ea/wave12-root-tax19-delivery-review'
TID = 'boss1-wave12-ret-source-repair-8324c735e389d989'
OLD = 'boss6-bank-status-repair-repair-5f402448a1964e8e'
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
assert rr.pin(d) == '85abf2d87473d579498cc7df43e9cfc38f0c55976703ec9751b7fe12d196e777'
assert d['supersedes'] == [OLD]
reg = read(R / 'research/registry.json')
obs = {o['object_id']: o for o in reg['objects']}
assert all(rr.pin(obs[k]) == v for k, v in d['input_pins'].items())
rp = f'map/receipts/{TID}.json'
fp = f'map/edges/{TID}/freeze.json'
assert sha(W / rp) == 'c7805f8418e8a1da0a8d5f42d15f525d350dbf8bff4090275f31c0aae1730424'
assert sha(W / fp) == '55d66e24209db8f8f61437a6f1b39035659bbe3070056bdd23ac0e211a9ff016'
receipt = read(W / rp)
freeze = read(W / fp)
assert freeze['input_pins'] == d['input_pins']
assert set(receipt['supersession']) == {OLD}
dispositions = receipt['supersession'][OLD]['assets']
assert len(dispositions) == 20
assert sum(x['disposition'] == 'retained' for x in dispositions.values()) == 17
assert sum(x['disposition'] == 'replaced' for x in dispositions.values()) == 3
assert not receipt.get('closed_overlaps') and not receipt.get('follow_up_tasks')
new_assets = [x for x in receipt['assets'] if (W / x['path']).exists()]
reused = [x for x in receipt['assets'] if not (W / x['path']).exists()]
assert len(new_assets) == 6 and len(reused) == 17
new_edges = []
for x in new_assets:
    p = x['path']
    assert any(p == w or PurePosixPath(w) in PurePosixPath(p).parents for w in d['write_paths'])
    assert sha(W / p) == x['sha256'] and not (R / p).exists(), p
    if Path(p).suffix == '.json':
        e = read(W / p)
        if isinstance(e, dict) and 'edge_id' in e:
            new_edges.append(p)
for x in reused:
    assert sha(R / x['path']) == x['sha256']
assert len(new_edges) == 3 and not (R / rp).exists()
for x in new_assets + [{'path': rp}]:
    p = x['path']
    (R / p).parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(W / p, R / p)
A.mkdir(parents=True, exist_ok=True)
shutil.copyfile(W / fp, A / 'worker-frozen-manifest.json')
shutil.copyfile(Path(__file__), A / 'stage-delivery.py')
(A / 'root-mathematical-review.md').write_text('''# Boss1：ROOT-TAX19当前源版本替代主审

Root全文审读本次review、三条新边、19核心coverage及supersession结构，重新全文读未改诊断，结合本对话已完整核读的新RET、CA-PREFIX与四人证书；原227包的独立数学本就由Boss1建立。27当前端点逐一核pin，保13未受影响canonical和4历史辅助资产。worker按69pass区分新读与继承；Root没有以文件hash替代数学审读，也未声称重跑全历史IC、1971扫描或77静态尾。

## 局部私块、全前缀与终点分离

AAAF真实h=A后当前A的收益为18/3+12/4=9。A/B/C/D分割61客户；BCD在A外，背景补全达全部61，故每个删除独有损失为10、11、10。当前A已在前缀内，SWAP退款new=0，最小损失10>9，固定该池均匀一步的条件期望31/3>9。这个条件池不足以单独证明根无条件RET的全前缀失败，故贡献只标这一步收费障碍。

独立CA-PREFIX一般n≥4完整SPE族已经给全前缀反驳：n个叶各有私有n−2客户，达到全覆盖的n槽池只能各叶一次，不能换一个最优池规避。d=1使L1=2(n−2)>n−1/n=P1，n4差1/4。该族仍有W=n²−2、OPT=2n²−2n−2、终点half余量2(n−1)>0。因此旧remaining里的“全prefix仍待证明/可能换池”必须删除；SWAP/RET代数、终点付款和不同非局部机制的义务继续保留。诊断“没有由此否定”说的是本局部点的推出范围，仍真，无需改它的历史证据。

## 平方信用whole见证

静态背景F3(A)=36与F2(2A)=21分别由56/21个合法多重集最大化确定；它们的最大者ABC/ACD与AC/BC/CD不是实际尾。真正AAAF当前后的tail=AF覆盖全部30名A客户，旧负载1给ΔH=30(1/4−1/9)=25/6。因此u+ΔH−(F3−F2)=9+25/6−15=−11/6。目标只是指数2的这一Bellman模板，不能推广成一切信用或half反例。两条root-tax specializes完整提供登记的全部负点，whole保持。

## 不受影响覆盖与谱系

19core中17linked、2isolated。继承的常值/双锚、UV调和、固定链重赋、背景正掩码、末位近饱和界、完整菜单/覆盖商/耦合产品、根平局切换、强PAIR/两人共同query、LAST/TAME与银行root-only均不以被否全prefix付款为前提。两isolated分别仍是计划函数非次模和窄SAFE加载模板，不凭源改版添加假依赖。继承只指有效Boss6 holder的成熟合同与证据，不冒称重读大证书。

20prior逐项17retained/3replaced，稳定edge_id保留而新路径绑定当前版本。四Boss6辅助文件原SHA只作历史，不能把旧binding-preview当当前验证。原227/round18只保provenance，唯一supersedes现役Boss6 holder；三历史closures留supersession而不冒作新formal pairs。原生完整校验与push之后才可done。科学新运行0。
''')
events = []
for p in new_edges:
    for action in ['edge-bind', 'edge-check']:
        cmd = [sys.executable, 'work.py', 'research', action, p]
        if action == 'edge-bind':
            cmd.append('--write')
        c = subprocess.run(cmd, cwd=R, text=True, capture_output=True)
        events.append({'action': action, 'path': p, 'exit_code': c.returncode,
                       'stdout': c.stdout, 'stderr': c.stderr})
        save(A / 'native-binding-events.json', events)
        assert c.returncode == 0, c.stdout + c.stderr
freeze['new_files_after_binding'] = [{'path': x['path'], 'sha256': sha(R / x['path'])}
                                     for x in freeze['new_files_before_binding']]
freeze['publication_status'] = 'Root native bound and checked; original pre-bind snapshot retained; await pushed checkpoint then done'
save(R / fp, freeze)
for x in receipt['assets']:
    if x['path'] in new_edges or x['path'] == fp:
        x['sha256'] = sha(R / x['path'])
save(R / rp, receipt)
rows = [read(p) for p in (R / 'research/operations/map-v2/tasks').glob('*.json')]
mt.validate(R, d, 'map', objects=obs)
mt._asset_refs(R, d, receipt, canonical=set(reg['edge_files']))
mt._supersession(R, d, receipt, rows, 'map')
rels, files = mt.batch_edges(R, d, receipt, obs)
for e in rels.values():
    rr.require_edge_result(e)
ep = {read(R / p)['edge_id']: p for p in files}
mt._check_edge_paths(R, d, receipt, [x for x in rows if x['definition']['task_id'] != TID], ep, reg['edge_files'])
mt._map_receipt_coverage(d, receipt, obs, rels)
rr.validate_map_follow_ups(d, receipt, rows, obs, final=True)
assert len(rels) == 16 and len(receipt['coverage']) == 19
assert sum(x['state'] == 'linked' for x in receipt['coverage'].values()) == 17
for x in receipt['assets']:
    assert sha(R / x['path']) == x['sha256']
summary = {'task_id': TID, 'definition_pin': rr.pin(d), 'receipt_path': rp,
           'receipt_sha256': sha(R / rp), 'receipt_pin': rr.pin(receipt),
           'input_pins': d['input_pins'], 'core_ids': d['object_ids'],
           'coverage': {'linked': 17, 'isolated-after-review': 2},
           'edge_count': 16, 'new_edge_count': 3, 'asset_count': 23,
           'retained_canonical_edges': 13, 'retained_historical_support': 4,
           'supersedes': [OLD], 'prior_dispositions': {'retained': 17, 'replaced': 3}}
report = {'status': 'NATIVE_FULL_RECEIPT_VALIDATION_PASSED', 'tasks': [summary],
          'root_review_sha256': sha(A / 'root-mathematical-review.md'),
          'worker_manifest_sha256': sha(W / fp), 'bound_manifest_sha256': sha(R / fp),
          'scientific_executions_by_Boss': 0,
          'native_checks': ['definition', 'edge_bind_write', 'edge_check', 'asset_refs', 'supersession', 'batch_edges', 'require_edge_result', 'edge_paths', 'coverage', 'follow_ups_final_true']}
save(A / 'validation.json', report)
save(A / 'done-records.json', [{'task_id': TID, 'receipt_file': rp}])
print(json.dumps({'status': report['status'], 'task': summary}, ensure_ascii=False, indent=2))
