from pathlib import Path
from datetime import datetime, timezone
import json,hashlib,copy
ROOT=Path('/workspace/scratch/d5435ebfeb39/co-work-anl-boss7')
OUT=Path('/workspace/scratch/d5435ebfeb39/worker-staging/r2_mandatory_audit')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(o): return hashlib.sha256(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ref(s):
 p=ROOT/s
 return {'path':s,'sha256':sha(p),'bytes':len(p.read_bytes())}
regpath='research/registry.json'; reg=json.loads((ROOT/regpath).read_text()); objs={o['object_id']:o for o in reg['objects']}
source='archives/unrelated-machines/state/审查/稀释逃逸行度与共享终端局部审计--审查.md'
old='* `only_mandatory_job=0`，因而该展开没有把单个“强制作业”当作逃逸来源；'
new='* `only_mandatory_job=0` 的 `0` 是 bridge 作业编号；唯一必走大边任务集合恰为 `{bridge}`，并非 mandatory 作业数量为零；'
original=(ROOT/source).read_text(); assert original.count(old)==1
proposed=original.replace(old,new); proposed_sha=hashlib.sha256(proposed.encode()).hexdigest()
metadata=json.loads((OUT.parent/'r1_shared_z/source-minimal-metadata.json').read_text())
assert sha(ROOT/source)==metadata['old_sha256']; assert proposed_sha==metadata['proposed_sha256']
assert original[original.index('## 3. '):]==proposed[proposed.index('## 3. '):]
ids=['UM-DILUTED-ESCAPE-PROBE-GAP-v1','UM-DILUTED-SHARED-TERMINAL-RAW-K2-GAP-v1','UM-DILUTED-SHARED-TERMINAL-ROW-DEGREE-GAP-v1']
endpoint_ids=['UM-BIG-CARDINALITY-PROBE-v1','UM-DILUTED-SINK-PROBE-GAP-v1','UM-MODEL-v1']
edge_paths=['map/edges/unrelated-machines-3a-3a-1b7557db7c2d59cd/shared-z-row-count-boundary.json','map/edges/unrelated-machines-3a-3a-1b7557db7c2d59cd/sink-certificate-extension-shared-z.json']
receipt_path='map/receipts/boss6-rho-source-repair-repair-449d548146e03e73.json'; receipt=json.loads((ROOT/receipt_path).read_text())
task_path='research/operations/map-v2/tasks/boss6-rho-source-repair-repair-449d548146e03e73.json'; task=json.loads((ROOT/task_path).read_text())
assets=[]
for a in receipt['assets']:
 e=json.loads((ROOT/a['path']).read_text()); current=sha(ROOT/a['path']); assert current==a['sha256']
 mismatches={i:{'published':v,'current':pin(objs[i]) if i in objs else None} for i,v in e.get('endpoint_pins',{}).items() if i not in objs or v!=pin(objs[i])}
 assets.append({**a,'edge_id':e['edge_id'],'file_sha_matches':True,'endpoint_pin_mismatches':mismatches,'planned_disposition':'replaced' if a['path'] in edge_paths else 'retained','replacement_filename':Path(a['path']).name if a['path'] in edge_paths else None})
assert not any(a['endpoint_pin_mismatches'] for a in assets)
cover=[]
for i,c in receipt['coverage'].items():
 cp=pin(objs[i]); assert cp==c['object_pin']
 cover.append({'object_id':i,'current_version':objs[i]['version'],'object_pin':cp,'state':c['state'],'edge_ids':c.get('edge_ids',[]),'audit_scope':'inherited valid reviewed coverage; not re-read in this worker' if i not in ids else 'registry record and two shared-z relations directly re-reviewed'})
active=[]
for tid in ['um-shared-z-probe-exact-primary-3a-b64889f2acdd728c','unrelated-machines-3a-3a-e5b7b2ae27def807','um-shared-z-probe-exact-comparison-3b-bd367f07d65e25be']:
 p='research/operations/map-v2/tasks/'+tid+'.json'; t=json.loads((ROOT/p).read_text()); active.append({**ref(p),'task_id':tid,'state':t['state'],'owner':t['owner'],'object_ids':t['definition'].get('object_ids',[]),'read_object_ids':t['definition'].get('read_object_ids',[]),'input_pins':t['definition'].get('input_pins',{})})
program_root='archives/unrelated-machines/tools/evidence/um-following-actual-code-primary/original/tests/audits/unrelated_machines/'
programs=[ref(program_root+f) for f in ['diluted_escape_probe_gap.py','diluted_sink_probe_gap.py','heavy_matching_residual.py']]
raw=ref('archives/unrelated-machines/tools/evidence/diluted-escape-row-20261030/source/diluted_escape_probe_gap_audit.json')
rawj=json.loads((ROOT/raw['path']).read_text())
assert [p['sha256'] for p in programs]==[rawj['extension_sha256'],rawj['base_sha256'],rawj['peer_sha256']]
refs=[]
for ep in edge_paths:
 e=json.loads((ROOT/ep).read_text())
 for er in e['evidence']:
  rr={**er,'current_file_sha256':sha(ROOT/er['path'])}; assert rr['current_file_sha256']==er['sha256']
  if rr not in refs: refs.append(rr)
loc=[]
def walk(x,jpath='$'):
 if isinstance(x,dict):
  if x.get('path')==source: loc.append({'json_pointer':jpath,'reference':x})
  for k,v in x.items(): walk(v,jpath+'/'+str(k))
 elif isinstance(x,list):
  for i,v in enumerate(x): walk(v,jpath+'/'+str(i))
walk(reg)
payload={
 'worker':'r2-mandatory-audit','captured_utc':datetime.now(timezone.utc).isoformat(),'clone_read_only':str(ROOT),'registry_snapshot':ref(regpath),
 'conclusion':'Confirmed one-line secondary-source erratum; all three registered mathematical statements and both current shared-z relations remain valid. Refresh source references and endpoint bindings without changing mathematics.',
 'source_erratum':{'current':ref(source),'proposed_sha256':proposed_sha,'old_line':old,'new_line':new,'old_line_occurrences':1,'r1_patch_verified':True,'section_3_and_later_byte_identical_in_proposal':True,'program_and_raw_json_unchanged':True,'patch':{'path':str(OUT.parent/'r1_shared_z/source-minimal.patch'),'sha256':sha(OUT.parent/'r1_shared_z/source-minimal.patch')},'metadata':{'path':str(OUT.parent/'r1_shared_z/source-minimal-metadata.json'),'sha256':sha(OUT.parent/'r1_shared_z/source-minimal-metadata.json')}},
 'affected_objects':[{**{'object_id':i,'version':objs[i]['version'],'registration_pin':pin(objs[i]),'statement_change_required':False,'evidence_sha_refresh_required':True},'record':objs[i]} for i in ids],
 'other_edge_endpoints':[{ 'object_id':i,'version':objs[i]['version'],'registration_pin':pin(objs[i])} for i in endpoint_ids],
 'source_registry_reference_locations':loc,
 'original_programs':programs,'raw_json':raw,'raw_expanded_fields':rawj['expanded'],
 'edges':[ {**ref(p),'edge_id':json.loads((ROOT/p).read_text())['edge_id'],'current_record':json.loads((ROOT/p).read_text()),'mathematical_change_required':False,'post_erratum_action':'write a new task asset with same mathematical content and edge_id, renew reviewed_by/review_note and run edge-bind/edge-check after new escape endpoint pin exists'} for p in edge_paths],
 'full_edge_evidence_read_and_sha_verified':refs,
 'valid_done_predecessor':{**ref(task_path),'task_id':task['definition']['task_id'],'state':task['state'],'owner':task['owner'],'receipt':ref(receipt_path),'core_count':len(cover),'asset_count':len(assets),'all_coverage_pins_match_current':True,'all_asset_sha_and_endpoint_pins_match_current':True,'coverage_inheritance':cover,'asset_inheritance_plan':assets,'retained_asset_count':sum(a['planned_disposition']=='retained' for a in assets),'replaced_asset_count':sum(a['planned_disposition']=='replaced' for a in assets),'replacement_paths_pending_boss_generated_repair_task':True,'supersedes_must_name':'boss6-rho-source-repair-repair-449d548146e03e73','coverage_policy':'inherit all 17 valid reviewed cores; only escape coverage pin changes for this source erratum; do not claim these cores were all reread by this worker'},
 'active_tasks_do_not_claim_or_edit':active,
 'actions_not_performed':['Git commands or writes','queue or registry writes','map-draft','scientific experiments or source-program execution','claims on other Boss tasks'],
 'revalidation_required_at_publication':'Snapshot is exact at captured_utc only; Boss must compare current registry and task metadata before forming grouped repair.'}
(OUT/'pins-and-inheritance-plan.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
report=f'''# mandatory 字段最小勘误与共享 z 两边审读

审读者：Boss7 / r2-mandatory-audit。快照时间：{payload['captured_utc']}。clone 全程只读；成果只写 worker-staging。没有执行 Git、队列、registry、map-draft、源程序或科学实验。

## 可直接执行的结论

r1 的最小 patch 逐字核验通过：只替换原页 §2.1 的一行，把 `only_mandatory_job=0` 解释为 bridge 的任务编号。唯一必走大边任务集合为 `{{bridge}}`，不是空集。当前页 SHA 为 `{sha(ROOT/source)}`，纯此单句修正后的 SHA 为 `{proposed_sha}`，两者与 r1 metadata 完全一致。§3 开始直到文件末尾的字节在该提案中完全不变。

三项登记的数学陈述本来已与正确语义相容。两条现行边的数学内容也无须修改：一条维持 checks/context 比较；另一条维持 ALL 前提下覆盖完整目标的 transfers/unconditional。发布后需要刷新证据页 SHA、对象记录版本和 registration pins，以及受影响边的端点绑定和 review digest。边自己的显式 evidence 文件均未变。

## 程序、raw JSON 与原句

完整读取扩展程序与底座程序；核对 peer 的 mandatory 分类段。底座从空 edges 列表开始，bridge 是第一次 `edge(...)` 返回的索引，故 bridge 编号为 0。扩展代码定义 `mandatory={{j for j in range(n) if not small[j]}}`，随后在 `ghmr_certificate` 中断言 `mandatory=={{bridge}}`；输出字段字面为 `'only_mandatory_job':d['bridge']`。原 JSON 的字段确为数值 0。三份代码的原始字节 SHA 与 raw JSON 声明逐项一致：

* extension：`{programs[0]['sha256']}`。
* base：`{programs[1]['sha256']}`。
* peer：`{programs[2]['sha256']}`。
* raw JSON：`{raw['sha256']}`。

因此误读只在旧审查一句解释文字。原程序、原 JSON、k4 4562 旧边 / 352 新边 / 4394 大边 / 4914 星查询及 raw 限定均应保持原字节。

## 三项当前登记的影响

| 对象 | 版本 | 当前 registration pin | 本次判断 |
|---|---:|---|---|
| UM-DILUTED-ESCAPE-PROBE-GAP-v1 | {objs[ids[0]]['version']} | `{pin(objs[ids[0]])}` | objections 已明确“mandatory=0是bridge编号而非零个”；陈述不改，只刷新本页两处证据引用 |
| UM-DILUTED-SHARED-TERMINAL-RAW-K2-GAP-v1 | {objs[ids[1]]['version']} | `{pin(objs[ids[1]])}` | 本页只以 §4 的 k=2 单分量有限 frame 接证；本次不改变主构造、一般 raw 合同或有限证书范围 |
| UM-DILUTED-SHARED-TERMINAL-ROW-DEGREE-GAP-v1 | {objs[ids[2]]['version']} | `{pin(objs[ids[2]])}` | 本页只以 §3 的四个显式 (d,k) 及 replay 接证；固定 d / 先固定 d 再取 k 极限等量词不改 |

后两者的主证明并不由这份有限审计独立承担。本轮实审三条登记、相关 §3/§4 及共享 z 关系；没有重新宣称独立重证 rawK2 或任意固定 d 的完整主定理。原页 §3/§4 不改，只因全文 SHA 变化而更新其 section 引用的文件 SHA。

## 共享 z 的大件计数阈值边

路径：`{edge_paths[0]}`。SHA：`{sha(ROOT/edge_paths[0])}`。edge_id：`um-r37-shared-z-row-count-boundary`。

这条边是 accepted / checks / context，不是把扩展实例当作无 z 定理的反例。目标 UM-BIG-CARDINALITY-PROBE-v1 的完整陈述限于无 global z 底座，仍准确成立；扩展实例只增加所有组共用的一台半时 z，其接口精确阈值另有限定 k≥8。当前类型与范围正确，不需 whole_result 或 contribution 冒称逻辑支持目标。

数学下界逐项成立：1≤C<2 时严格大件规则把 unit 计为大件，半时 z 不计为大件。强制底父 incoming unit 后，外送普通质量 a 满足 a≥k(2−C)。本组 N 个终端的大件计数扣 N−1−e 阻塞质量后得 a≤1+e，而同一台全局 z 的容量给本组 e≤2C，故 C≥C*=(2k−1)/(k+2)。C<C* 时删全部底父 incoming，逐层上传到 bridge；C<1 时 bridge 直接无域。这里不能给每组独立 2C 预算并同时相加使用：下界只对被强制的一个组使用其 e≤全局逃逸总量≤2C。

反向 k≥8 给 C*≥3/2。基点是 bridge 两根各 1/2、普通全在小端、各组阻塞注入终端。强制 bridge 或非底父 incoming，令被激活父每条出边外送 δ=2−C*，其负载 C*，孩子负载 1+δ≤C*。强制底父 incoming 时同样外送，a=kδ=1+2C*。若终端普通质量为 u_t，每枚本组阻塞在 t 取 (1−u_t)/(N−1)，在 z 取 (a−1)/(N−1)，则列和 1，终端大件计数及负载均为 1，唯一 z 总负载 (a−1)/2=C*。其余组 z 质量为 0。强制普通小端、普通 unit 端、阻塞终端端、阻塞 z 端的各类点分别可由基点或注入得到。各查询分别存在一个点；未拼成多查询联合点。更高 C 可复用这些点且严格大件集只缩小。

因此精确阈值结论闭合，保留 k≥8、共同 z、同一条件 LP 和每边分别存在的量词即可；本次修正不改变它。

## 无 z 分离证书到共享 z 的迁移边

路径：`{edge_paths[1]}`。SHA：`{sha(ROOT/edge_paths[1])}`。edge_id：`um-r37-sink-certificate-extension-shared-z`。

ALL 前提是 UM-DILUTED-SINK-PROBE-GAP-v1 与 UM-MODEL-v1：前者给完整原矩阵与分离证书，后者固定不可拆、列守恒、真实配置及同一有限任务宇宙。不能只迁移配置证书就声称完整间隙。边另付了新增边证书与整数下界，因此其 unconditional 是该完整迁移论证无未付前提，不是一般 UM 算法结论。

旧 CONFIG 在 z 放空配置、旧 LST 点 z 边际为零，覆盖不变。新增阻塞到 z 的查询固定其 z 质量为 1，z 负载 1/2；每组默认普通任务全去大端时终端剩余总容量 NT−k=N−1。被强制组只剩 N−2 枚待填阻塞，其余组仍 N−1 枚，按余量比例填可得完整 LST 点。旧星的 F 集因新增小备选只会缩小；新 z 星把各组 N−1 阻塞注入各自 N 终端，跨组终端物理互异。

GHMR 的唯一 mandatory 是 bridge。核心父的唯一小端普通任务有互异大备选；强制某条大边后仍能安排 bridge（必要时去另一根）。终端没有这类 U_i 任务；z 没有大边查询，另有全部 z 唯一小端阻塞到互异终端的匹配证书。这里恰与正确的 mandatory 语义一致。

真实 OPT 不能仅由删去 z 前的下界继承。边已重新证明：若 B<2−1/k，则每个活跃父至少外送两任务，k≥4 对应 h≥3，故至少四个不同活跃底组。每组至少两普通 unit 进入终端，迫一枚不同阻塞去共同 z，总负载≥4·1/2=2>B。旧单路径调度不使用 z 给上界。因此同一完整扩展矩阵 OPT=2−1/k；T=1+1/k 下 CONFIG、所有独立 LST、现行 GHMR 与星皆通过，ratio=2−3/(k+1)趋2。现行 whole_result 覆盖完整 escape 目标，无须降成 contribution，也不能增强为联合 CONFIG/多边同条件系统结论。

## 17 core / 20 assets 的定向继承

有效前驱是 `boss6-rho-source-repair-repair-449d548146e03e73`，任务快照为 done / Boss6。其 receipt 的 17 个 coverage pins 全部与当前 registry 一致；20 个 asset SHA 与当前文件一致，且这 20 条边的 endpoint pins 逐项均匹配当前 registry。本 worker 没有重读 17 个未变 core 的全部正文，而是继承前驱既有有效已审覆盖；直接数学实审限于本次三记录与上述两边。

Boss 新 repair 应 supersede 此有效前驱，覆盖全部 17 个现役 core，保全原比较理由和状态；对 escape 更新新 object_pin 并加本次勘误审读说明，其他 16 项沿用有效覆盖。20 资产的处理为：18 项按原 path/SHA retained；上述两项在新 repair 的 write_paths 内写同 edge_id 的重绑定文件并 listed as replaced，旧 path 各给准确 replacement_paths。不要直接修改被旧 done 回执钉住的旧边文件。18 保留和2替代的完整精确清单及17 core pins已放 JSON，未替 Boss 生成 repair ID 或运行 map-draft。

当前三个相关活跃任务仍分别归 Boss7、Boss2、Boss5；完整 task 文件 SHA、端点范围和 input_pins 已放 JSON。本轮不认领或修改他人任务。三对象证据引用更新后应按现行规则刷新各自已认领任务的版本/pins，原 worker 只续补受影响部分。

全局 registry 快照 SHA：`{sha(ROOT/regpath)}`。发布前若其他 Boss 已推进 registry 或任务元数据，以最新状态重核；本报告的精确 pins 只对快照时间负责。
'''
(OUT/'审读报告.md').write_text(report)
print(json.dumps({'report':str(OUT/'审读报告.md'),'pins':str(OUT/'pins-and-inheritance-plan.json'),'registry_sha256':sha(ROOT/regpath),'source_proposed_sha256':proposed_sha,'retained':18,'replaced':2,'coverage':len(cover),'assets':len(assets)},ensure_ascii=False))
