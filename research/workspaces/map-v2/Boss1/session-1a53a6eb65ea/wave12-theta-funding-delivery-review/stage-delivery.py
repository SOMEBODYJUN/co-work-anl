from pathlib import Path, PurePosixPath
import hashlib
import json
import shutil
import subprocess
import sys

B = Path('/workspace/scratch/1a53a6eb65ea')
R = B / 'co-work-anl-boss1'
W = B / 'wave12-theta-funding-worker'
A = R / 'research/workspaces/map-v2/Boss1/session-1a53a6eb65ea/wave12-theta-funding-delivery-review'
V = R / 'research/workspaces/map-v2/Boss1/session-1a53a6eb65ea/wave12-value-mmo-3d'
TID = 'customer-attraction-3a-3a-6da379517e0565e4'
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
assert rr.pin(d) == 'bf9301a5cf4ba9017905f2d28e569c85a5792ea89ff8a1bdee42aa6f6d28f127'
reg = read(R / 'research/registry.json')
obs = {o['object_id']: o for o in reg['objects']}
assert all(rr.pin(obs[k]) == v for k, v in d['input_pins'].items())
receipt_path = f'map/receipts/{TID}.json'
freeze_path = f'map/edges/{TID}/freeze.json'
assert sha(W / receipt_path) == 'ba2ddfb34877913e023d9c2bf7038bf9b5643989c832d6a4f1e9f0d07ec8e0bc'
assert sha(W / freeze_path) == 'dd5a87bcbab45adbfa0647f7f2119c80a40aff43ba3aac591a2a6b92f36260a0'
receipt = read(W / receipt_path)
freeze = read(W / freeze_path)
assert freeze['input_pins'] == d['input_pins']
assert len(receipt['assets']) == 3 and not receipt['closed_overlaps'] and not receipt['follow_up_tasks']
new_edges = []
for x in receipt['assets']:
    p = x['path']
    assert any(p == w or PurePosixPath(w) in PurePosixPath(p).parents for w in d['write_paths'])
    assert sha(W / p) == x['sha256'] and not (R / p).exists(), p
    if Path(p).suffix == '.json':
        e = read(W / p)
        if isinstance(e, dict) and 'edge_id' in e:
            new_edges.append(p)
assert len(new_edges) == 1 and not (R / receipt_path).exists()
for x in receipt['assets'] + [{'path': receipt_path}]:
    p = x['path']
    (R / p).parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(W / p, R / p)
A.mkdir(parents=True, exist_ok=True)
shutil.copyfile(W / freeze_path, A / 'worker-frozen-manifest.json')
(A / 'root-mathematical-review.md').write_text('''# Boss1：THETA-FUNDING2最终数学审读

Root实读最终worker审读、32项实际阅读台账、边与receipt；核当前八份完整登记合同，并全文读OWN、ALL/ROW、βmax、FCLC四个数学正文及两条现役canonical。ALL尾段及βmax正文在输出截断后单独补读。两个core正文已在本对话全文读。worker对1885节点输入、冻结审计报告和源码的实际范围保留；Root没有声称重新读完每个大证书数字或运行全树IC。科学新运行数为0。

## 逐人纯θ反例的精确否定范围

存在四人十二标签完整有序SPE，实际(8,4,5,0)，u1=6135345而θ=6135346。θ取纯三主题背景后最大纯查询；该min-max量词与静态混合安全值不同，不能把θ反例直接写成混合安全值或half反例。W24541476、OPT24541532，half余量24541420为正。22620含self比较中真替代20735，非self平局4555；正差最小1不表示严格SPE，更不表示唯一SPE。唯一最优覆盖计数0123也不提供策略唯一性。本包没有独立的被反驳逐人θ全称端点，另一core是共同付款资源；保持isolated-after-review合理。

## 从单个context到共同付款仍欠什么

Root重建TAME两分支代数：pk≤1，w=d+n−n_minus，pkw−n min(pd,1)≤d，故(r−Q)_+≤1/w，先合整个T_i再用一次完整IC。canonical总TAME，遗漏R上k=1所以任意归属TAME；其他OWN点不能自动初始化。H、r、初边和I补余J须在同一点重算。

ALL以h/a边cap、真实future和同客户库存保证单节点密度f≤1，L≤f/a先按客户求和，再用一次整主题IC得到单行ΣL≤u。ROW从uniform C0出发取消min(H,u)−C0的外流，因总外流H−C0足够而达到min(H,u)；输入减少后的逐客户比例缩放保边cap、守恒和整行cap。它并不把不同contexts合为一行，逐客户价格DP也不能直接用于共享ROW。

βmax中v_x=1/c_B(x)是旧份额，ALL中v=c_V(x)是负载。β_x=h_x/v_x，β*=maxβ_x，恒等式F=β*e+Σ(β*−β_x)D_x+Σβ_xN_x≥0给一次完整IC退款，来源合并拆分不增加库存。两个独立行动各有系数1且支持不交，逐客户库存仍可各为1，系数和却为2。因此逐客户库存与各行动IC本身不推出跨行动Σκ≤1；这只是该推理步骤的代数非蕴含，不是一份完整SPE反例。

同actual角色的共同剩余额度仍为2u−d−H−J；每个context分别≤u不会支付其和。FCLC去ROLE紧凸及非负价格分离是表示定理，λ=1由MASS仍给原|O|≤2W。旧canonical mandatory-NEW点能嵌入扩大族，扩大族的点不能倒推旧族可行。EG族同时有明确ROLE点，不能以它的纯保底失败指控ROLE或half。

## 判定和去重

新边只为accepted cites/context：准确记录funding资源对五合同的实质引用和未付处。两core均isolated-after-review，不把引用改称数学推导。现役ALL→ROW whole和FCLC→OWN contribution已核原path/SHA/端点，继续保留；后一边本身保conditional标签及TAME/ROLE剩余，未被本包扩张为whole。formal follow-up为空，deferred EG只是阅读提示，不制造非法closed_overlaps或同义新节点。原生bind/check及receipt校验仅核合同与证据身份，不替代上述数学审读。
''')

V.mkdir(parents=True, exist_ok=True)
for name, expected in [
    ('proof-review.md', '52dc941d6a89e88b76a63b6dcf36280d95889a73abb0c70cc49cfb793adf2930'),
    ('refs.json', '812eac18cc546559677012d74c0ca2c1384627aebcabd1e8ce0d9539e3722640'),
]:
    source = B / 'wave12-value-mmo-3d' / name
    assert sha(source) == expected
    assert not (V / name).exists()
    shutil.copyfile(source, V / name)
(V / 'root-review.md').write_text('''# Boss1：VALUE-MMO2独立3D复核

Root全文读worker审读、当前Svensson资源正文、四个完整登记合同及两条现役canonical关系；Asahiro当前正文和原文相关证明此前本对话已独立审读并修复发布，本次精确核当前边及覆盖，不假称新读两篇完整PDF。worker本次PDF定向阅读页码与继承成熟全篇审读分别保存在refs。

## Svensson数值估值

Tconf≤OPT≤(33/17)Tconf，若显式条件后端提供Tconf≤That≤(1+ε)Tconf，固定有理ε≤17η/33，则E=(33/17)That同时满足OPT≤E和E≤(33/17+η)OPT。必须保有理固定精度、零值/不可行分支及数值输出合同。有限签名和至多3|M| blocker不等于多项式局部搜索步数；阈值后端的多项式复杂度是外引未付条件，真实assignment构造又是另一责任。现役accepted/conditional/whole完整支付登记估值目标但不取消条件。e5622a5b3226206f整个单core coverage可采用。

## 阈值MMO到简单系列并行图

每个源权w_i≤B边替为一条独立三边路w_i,B,w_i；目标阈值B。中边的尾端已经负担B，正端边不能再从该点向外，因此解码中边方向可将w_i置于相应原端点，原端点负载不增。反向按源边方向设置三边路径，内部端点最多分别承B或w_i。总权2B的两个源端点负载≤B迫恰各B。空输入、非正阈值、奇总和及单权过大用明示常量分支，正权/编码位长都保留；2n+2顶点3n边和明确宽2袋构造证系列并行。三条路径会给K2,3 minor，不声称outerplanar。H_B依赖B，故只是阈值归约，不是同一固定图对全部阈值保OPT。

弱困难性配套的伪多项式算法用安全双子表枚举界O(2^{O(τ²)}(kN+1)^{2τ+2}(N+M))，并计整数位长；不借旧稿未付的快速join指数。现役accepted/transfers/unconditional/whole数学闭合。当前canonical仍为boss5-asahiro-sha-current-repair-16bd7e5e49c5be05下7bbf1422...文件（该repair实际owner Boss1）；历史original351693下8b5812...才是已替代旧物。eba225f7871d217b复用当前边的单core完整coverage可采用。

两包current定义、收据、资产及四端pin需在采用时再次精确核同。未引入源勘误、无科学重跑，无外部新颖性声明。
''')

events = []
for p in new_edges:
    for action in ['edge-bind', 'edge-check']:
        command = [sys.executable, 'work.py', 'research', action, p]
        if action == 'edge-bind':
            command.append('--write')
        result = subprocess.run(command, cwd=R, capture_output=True, text=True)
        events.append({'action': action, 'path': p, 'exit_code': result.returncode,
                       'stdout': result.stdout, 'stderr': result.stderr})
        save(A / 'native-binding-events.json', events)
        assert result.returncode == 0, result.stdout + result.stderr
for x in receipt['assets']:
    if x['path'] in new_edges:
        x['sha256'] = sha(R / x['path'])
save(R / receipt_path, receipt)
freeze['delivery_status'] = 'Root native bound and checked; receipt asset hashes refreshed'
for x in freeze['files']:
    x['sha256'] = sha(R / x['path'])
    x['bytes'] = (R / x['path']).stat().st_size
save(R / freeze_path, freeze)
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
assert len(rels) == 1 and len(receipt['coverage']) == 2
assert all(x['state'] == 'isolated-after-review' for x in receipt['coverage'].values())
assert all(e['relation_mode'] == 'context' for e in rels.values())
for x in receipt['assets']:
    assert sha(R / x['path']) == x['sha256']
summary = {'task_id': TID, 'definition_pin': rr.pin(d), 'receipt_path': receipt_path,
           'receipt_sha256': sha(R / receipt_path), 'receipt_pin': rr.pin(receipt),
           'input_pins': d['input_pins'], 'core_ids': d['object_ids'],
           'coverage': {'linked': 0, 'isolated-after-review': 2}, 'edge_count': 1,
           'new_edge_count': 1, 'new_logical_edges': 0, 'new_context_edges': 1,
           'asset_count': 3}
report = {'status': 'NATIVE_FULL_RECEIPT_VALIDATION_PASSED', 'tasks': [summary],
          'root_review_sha256': sha(A / 'root-mathematical-review.md'),
          'worker_manifest_sha256': sha(W / freeze_path),
          'bound_manifest_sha256': sha(R / freeze_path),
          'scientific_executions_by_Boss': 0,
          'native_checks': ['definition', 'edge_bind_write', 'edge_check', 'asset_refs', 'supersession', 'batch_edges', 'require_edge_result', 'edge_paths', 'coverage', 'follow_ups_final_true']}
save(A / 'validation.json', report)
save(A / 'done-records.json', [{'task_id': TID, 'receipt_file': receipt_path}])
print(json.dumps({'status': report['status'], 'task': summary}, ensure_ascii=False, indent=2))
