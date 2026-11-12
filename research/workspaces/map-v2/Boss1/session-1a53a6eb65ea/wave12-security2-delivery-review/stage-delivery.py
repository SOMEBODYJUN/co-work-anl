from pathlib import Path, PurePosixPath
import hashlib
import json
import shutil
import subprocess
import sys

B = Path('/workspace/scratch/1a53a6eb65ea')
R = B / 'co-work-anl-boss1'
W = B / 'wave12-security2-current-worker'
A = R / 'research/workspaces/map-v2/Boss1/session-1a53a6eb65ea/wave12-security2-delivery-review'
TID = 'customer-attraction-3a-3a-c385b158f346250d'
sys.path.insert(0, str(R / 'tools'))
import research_runtime as rr
import map_tasks as mt

def read(p):
    return json.loads(p.read_text())

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def save(p, x):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n')

t = read(R / 'research/operations/map-v2/tasks' / (TID + '.json'))
d = t['definition']
assert t['state'] == 'claimed' and t['owner'] == 'Boss1'
assert rr.pin(d) == 'f4b232d911a1edb3270d88e2ef6d05daca2965f5019caaa1172822394c248226'
reg = read(R / 'research/registry.json')
obs = {o['object_id']: o for o in reg['objects']}
assert all(rr.pin(obs[k]) == v for k, v in d['input_pins'].items())
rp = f'map/receipts/{TID}.json'
fp = f'map/edges/{TID}/freeze-manifest.json'
assert sha(W / rp) == '7cb4daf4ebded57bd3d0b5b0a77b8e384190901ee35faf24a8135967d7caec07'
assert sha(W / fp) == '476d8714be83a7faf0ea39d0b026ee96c63abbbfdf49d1cb30495df1a3609aed'
receipt = read(W / rp)
freeze = read(W / fp)
assert freeze['input_pins'] == d['input_pins']
assert not receipt.get('closed_overlaps') and not receipt.get('follow_up_tasks')
assert len(receipt['assets']) == 7
new_edges = []
for x in receipt['assets']:
    p = x['path']
    assert any(p == w or PurePosixPath(w) in PurePosixPath(p).parents for w in d['write_paths'])
    assert sha(W / p) == x['sha256'] and not (R / p).exists(), p
    if Path(p).suffix == '.json':
        e = read(W / p)
        if isinstance(e, dict) and 'edge_id' in e:
            new_edges.append(p)
assert len(new_edges) == 4 and not (R / rp).exists()
for x in receipt['assets'] + [{'path': rp}]:
    p = x['path']
    (R / p).parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(W / p, R / p)
A.mkdir(parents=True, exist_ok=True)
shutil.copyfile(W / fp, A / 'worker-frozen-manifest.json')
shutil.copyfile(Path(__file__), A / 'stage-delivery.py')
(A / 'root-mathematical-review.md').write_text('''# Boss1：SECURITY2当前源版本数学主审

Root全文读四条新边、当前review、两core coverage、八当前合同的全部数学字段，并全文重读selected、固定GB owner、完整菜单生成器和通用对偶正文。本对话已全文读CA-PREFIX全历史解析、n4证书及修改后的RET，并主导最小源勘误。旧成熟4914系数审计和大证书的逐数读取不冒称本轮Root重跑；fresh worker按26完整pass明确新读/无损投影/成熟继承。当前版本是先保全旧稿、handoff、源修改、reclaim并read-add后交fresh worker所得。

## 联合反驳及条件路线

n≥4族每叶有n−2名独占客户；最优n槽满覆盖只可能各叶一次，排除存在另一最优池规避。因每客户d=1、O为全客户且A⊂O，RET给L1=|O\\A|/n=2(n−2)；完整σ给P1=n−1/n，差n−4+1/n>0。n4差1/4而2W−OPT=6。ALL同时使用完整实例/SPE及RET余额公式，目标准确指Mdfcc所记录被否原全称，不是否定其当前refuted记录。

保留的条件边推导无缺步：i=m的RET概率均为1，L_m=|O\\C|−|C\\O|=OPT−W；客户均分使P_m=Σu=W。假设原全前缀付款则取终点即2W≥OPT，保零值、重复和任意平局。该前提已被完整族反驳，边明确为被切断的反事实充分关系，不能转作half无条件支持或可行开放路线。只支付终点仍等价原half净遗漏；族的i≥2付款成立及正终点余量不否暂欠后结。静态S≤L不自动提供实际收益，局部重启也不能冒充固定根随机池。RET21和ROOT-TAX19各自承担已存在桥的替代，不重复造边。

## 三策略公共Q与通用等价

纯查询的c/n−E_Q f(a)=Γᵀλ_a+r_a对p平均再乘n，确给c−nE_Qβ(p)=Γᵀ[nΣp_aλ_a]+nΣp_ar_a。Q同时固定于w和p，非负性保留，故三固定σ有通用(T)的具体解。它不证明一般(A)⇔(T)：后者还要归一客户锥、全兴趣点非空、有限minimax与Farkas以及有理点恢复，故checks=context、核心isolated合理。三人只末两人逐人安全，十三证书3+5+5、4914坐标，不能升级三人首位或所有σ。

## 五游戏GB量词与拼接

M(h)阈值max_b min_{z∈M(hb)}u_current(z)为完整菜单精确递归，因为不同有序孩子的SPE可以独立选。固定真实路径后，各首次偏离子树互不相交；在不超过actual当前收益的子菜单中独立最大化查询，能够装配为一份完整σ并达到总值。计数菜单不强制同计数历史共用策略，仍须逐位置核路径可实现。

五项是固定G、一个保存的安全最优p、全部SPE；三锥是固定σ、全部非负客户质量，二者无推导。正确有序路径数为48/40/23/102/6；正W−ΣC依次17/6、60/41、55088965/3710088、3/2、70429743611/10570351740。特别root-tax是102条及3/2，不是10条及23/2。负ΣC−W绝非预算反例。GB的0004/5002/043与锥0005/2500/034不能因游戏同名而替换。individual34不属于原四项生成器的run循环。cites=context只闭合finite owner。

## 覆盖与证据

2core恰1linked、1isolated；4边为2逻辑+2context，7资产。无formal overlap，closed/followup都空；不凭一般阅读线索伪造已解决对象对。所有证据section与SHA由native绑定重核，当前8pins与definition匹配。科学新运行0；原生检查与推送后方可done。
''')
events = []
for p in new_edges:
    for action in ['edge-bind', 'edge-check']:
        cmd = [sys.executable, 'work.py', 'research', action, p]
        if action == 'edge-bind':
            cmd.append('--write')
        c = subprocess.run(cmd, cwd=R, text=True, capture_output=True)
        events.append({'action': action, 'path': p, 'exit_code': c.returncode, 'stdout': c.stdout, 'stderr': c.stderr})
        save(A / 'native-binding-events.json', events)
        assert c.returncode == 0, c.stdout + c.stderr
freeze['payload_assets_before_binding'] = freeze['payload_assets']
freeze['payload_assets'] = [{'path': x['path'], 'sha256': sha(R / x['path'])} for x in freeze['payload_assets']]
freeze['freeze_state'] = 'Root native bound and checked; await pushed checkpoint then done'
freeze['boss_finalization'] = 'Root bound/checks all four edges; complete receipt validation follows. No scientific rerun. Original pre-bind manifest separately retained.'
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
assert len(rels) == 4 and len(receipt['coverage']) == 2
assert sum(x['state'] == 'linked' for x in receipt['coverage'].values()) == 1
assert sum(x['relation_mode'] == 'context' for x in rels.values()) == 2
for x in receipt['assets']:
    assert sha(R / x['path']) == x['sha256']
summary = {'task_id': TID, 'definition_pin': rr.pin(d), 'receipt_path': rp,
           'receipt_sha256': sha(R / rp), 'receipt_pin': rr.pin(receipt),
           'input_pins': d['input_pins'], 'core_ids': d['object_ids'],
           'coverage': {'linked': 1, 'isolated-after-review': 1},
           'edge_count': 4, 'new_edge_count': 4, 'asset_count': 7,
           'logical_edges': 2, 'context_edges': 2}
report = {'status': 'NATIVE_FULL_RECEIPT_VALIDATION_PASSED', 'tasks': [summary],
          'root_review_sha256': sha(A / 'root-mathematical-review.md'),
          'worker_manifest_sha256': sha(W / fp), 'bound_manifest_sha256': sha(R / fp),
          'scientific_executions_by_Boss': 0,
          'native_checks': ['definition', 'edge_bind_write', 'edge_check', 'asset_refs', 'supersession', 'batch_edges', 'require_edge_result', 'edge_paths', 'coverage', 'follow_ups_final_true']}
save(A / 'validation.json', report)
save(A / 'done-records.json', [{'task_id': TID, 'receipt_file': rp}])
print(json.dumps({'status': report['status'], 'task': summary}, ensure_ascii=False, indent=2))
