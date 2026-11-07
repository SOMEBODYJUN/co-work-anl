import pathlib,json,hashlib,collections
ROOT=pathlib.Path('.').resolve();OUT=ROOT/'research/workspaces/p25-register-v2/Boss3/0019-evidence-closure'
def read(p):return json.loads(pathlib.Path(p).read_text())
def write(n,d):(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def ref(p):
 p=pathlib.Path(p);return {'path':str(p.relative_to(ROOT)) if p.is_absolute() else str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
b=read(OUT/'original-batch.json');receipt=read(OUT/'original-receipt.json')
# Record only actually observed nontruncated intervals, deduplicated. Older full reading stays a receipt reuse, not a fresh raw revalidation.
ranges={0:[[18,40],[183,200]],1:[[46,126]],2:[[18,75],[247,269]],3:[[18,113],[215,287]],4:[[20,58],[85,173]],5:[[14,73]],6:[[1,34]],7:[[19,88]],8:[[1,57],[97,113]],9:[[14,52],[77,145],[166,180]],10:[[17,49],[106,128]],11:[[1,73]],12:[[18,45],[150,175]],13:[[17,30],[132,178],[214,223]],14:[[24,30],[63,83],[99,105],[119,127]],15:[[18,60],[144,185],[212,225]],16:[[19,73],[167,248]],17:[[20,35],[49,79],[143,168],[218,238]],18:[[26,89],[148,166]],19:[[20,43],[117,132],[167,177]],20:[[14,33],[102,112],[173,181]],21:[[1,114]],22:[[1,148]],23:[[1,97]],24:[[1,86]],25:[[1,119]],26:[[1,151]],27:[[1,88]],28:[[22,165],[175,181]],29:[[1,72]],30:[[13,93]],31:[[1,103]]}
rows=[]
for i,m in enumerate(b['materials']):
 text=(ROOT/m['path']).read_text().splitlines(keepends=True);selected=''.join(''.join(text[a-1:z]) for a,z in ranges[i])
 rows.append({'index':i,'material':{'path':m['path'],'sha256':m['sha256']},'new_observed_continuous_ranges':ranges[i],'new_distinct_lines':sum(z-a+1 for a,z in ranges[i]),'new_range_characters':len(selected),'new_range_utf8_bytes':len(selected.encode()),'prior_complete_mature_reading_reused':receipt['reading_scope']['assigned_materials'][i],'reuse_receipt':ref(ROOT/'research/registration/receipts/register-ab98f323ad-0019.json'),'boundary':'Old complete receipt reading reused at exact same SHA; new ranges are supplemental mathematical comparison only. Not claiming fresh full raw proof or replay validation.'})
shared=ROOT/'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md'
extra=[{'path':str(shared.relative_to(ROOT)),'ranges':[[1,100]],'scope':'Fresh shared model, full model/quantifiers through type compression start; old receipt supplies whole shared mature read.'},
{'path':'archives/customer-attraction/state/反例/四人实际根总税--反例.md','ranges':[[21,172]]},
{'path':'archives/customer-attraction/state/定理/完整策略锥的静态安全值对偶--定理.md','ranges':[[23,138]]},
{'path':'archives/customer-attraction/state/审查/指定完整策略锥安全证书与预算边界--审查.md','ranges':[[34,118]]},
{'path':'archives/customer-attraction/state/障碍/完整策略树平均与独立同分布福利桥--障碍.md','ranges':[[123,174]]},
{'path':'archives/customer-attraction/state/审查/个体安全去相关与尾部流增量--审查.md','ranges':[[66,99]],'scope':'Current evidence source routes and exact raw source IDs compared.'},
{'path':'archives/customer-attraction/tools/evidence/incremental-security-flow/3aee25998e06b261a8b5.raw','ranges':[[129,227]],'scope':'Independent mathematical proof §§3–4 actual read; no LP executed.'},
{'path':'archives/customer-attraction/tools/evidence/incremental-security-flow/c7b73d6fbb280dc7583b.raw','ranges':[[36,145],[195,269]],'scope':'Tail proof and independent average-flow proofs; not whole raw reread.'},
{'path':'archives/customer-attraction/tools/evidence/root-tax-upload-20261030/RootTax-summary.raw','ranges':[[1,194]],'scope':'Complete saved summary read; otherCSV hash/structure comparison only.'},
{'path':'archives/customer-attraction/tools/evidence/incremental-security-flow/a4dd82aa41fb5665aec0.raw','ranges':[[1,42]],'scope':'JSON top metadata and structural inspection; not4914-coordinate raw revalidation.'},
{'path':'archives/customer-attraction/tools/evidence/gb-sign-correction/README.md','ranges':[[1,9]]},
{'path':'archives/customer-attraction/tools/evidence/gb-sign-correction/correction-evidence.md','ranges':[[1,81]]},
{'path':'archives/customer-attraction/state/计算/指定策略安全锥与七极大来源边界--计算.md','ranges':[[1,9]]},
{'path':'archives/customer-attraction/state/程序/安全锥合同与共同Q认证边界--程序.md','ranges':[[1,41]]}]
for r in extra:r['ref']=ref(ROOT/r['path'])
write('reading-and-budget.json',{'planning':{'engineering_context_tokens':500000,'正文及元数据阅读预算':300000,'其它预留':200000,'actual_system_prefix_or_used_tokens':None,'is_runtime_telemetry':False,'source_chars_are_tokens':False},'materials32':rows,'extra_new_exact_ranges':extra,'metadata_reading':['AGENTS.md full','research/IMPLEMENTATION.md registration section and full double-object example45–390','research/PHASE3_READINESS.md full','prompts/02.5-3-worker.md full','original0019 definition/batch/receipt complete JSON metadata','all30 complete original/current mathematical record interfaces and refs; index6 reread complete','actualDONE task-state/receipt.batch_file/SHA metadata scan','0013 prepared candidate complete objectIDs/versions only; not claimed accepted/DONE','foreign preimages and addedrefs complete JSON metadata','missing principal frontmatter and original exact text preserved for routing; no whole proof reread claim'], 'raw_evidence_limit':'Bytes hashed and manifest/JSON structure inspected where recorded. No mathematical program/search/LP/certificate replay executed. Older manifest wording about full bytes read belongs to that old author, not this worker.','new_material_distinct_lines':sum(r['new_distinct_lines'] for r in rows),'new_material_characters':sum(r['new_range_characters'] for r in rows),'new_material_utf8_bytes':sum(r['new_range_utf8_bytes'] for r in rows),'token_estimate':None,'continuity':'Budget is planning only; no actual runtime/prefix measurement available. No cutoff of this whole task.'})
# Add exact21 fixed-cone route with actual0009 authority and0036 followup status.
routes=read(OUT/'missing-principal-source-routes.json')
cp=ROOT/'archives/customer-attraction/state/计算/指定策略安全锥与七极大来源边界--计算.md';tp=ROOT/'research/operations/p25-register-v2/tasks/register-ab98f323ad-0009.json';t=read(tp)
fp=ROOT/'research/operations/p25-register-v2/tasks/register-boss3-evidence-followup-0036-20261107.json';ft=read(fp);br=ft['receipt']['batch_file'];assert ref(ROOT/br['path'])['sha256']==br['sha256']
routes.append({'requested_legacy_claim':'CA-NEW-POLICY-CONE-SECURITY','exact_statement':'固定21棵完整形式策略σ，各自所有非负客户类型重数w只要Γσw≥0，均有Wσ(w)≥n v_n(w)；19棵n5m7、1棵n5m8、1棵n6m8。共同Q和非负Γ乘子不依w或查询分布p；不量化所有策略。','principal_source_route':ref(cp),'exact_body_text_for_route_only':cp.read_text(),'actual_task':{'file':ref(tp),'state':t['state'],'owner':t.get('owner')},'actual0036_followup':{'task':ref(fp),'state':ft['state'],'receipt_batch_file':br,'objects':read(ROOT/br['path'])['objects'],'disposition':'needs-decision pending0009 principal identity, not a mother record'},'source_ids':['a81b9371d7fa4a4d022d','760834c0f64c80b5ccc1'],'full_certificate':ref(ROOT/'archives/customer-attraction/tools/evidence/security-cones-new/original/new_policy_security_cones.json.gz'),'policy':'Exact claim and actual route only, no stub or arbitrary new ID.'})
write('missing-principal-source-routes.json',routes)
# Correct approximate raw line-range in historical request comparison to actual complete194.
q=read(OUT/'foreign-requests.json')
for x in q:
 if x['object_id']=='CA-ROOT-TAX-NO':x['comparison_read_ranges']['raw_summary']=[[1,194]]
write('foreign-requests.json',q)
# Full current preimage snapshots for candidate material rows and pure deltas.
can={x['path']:x for x in read(ROOT/'research/registry.json')['materials']}
c=read(OUT/'schema2-supplement-candidate.json')
write('candidate-complete-preimages-and-deltas.json',[{'path':m['path'],'original_done_row':next(x for x in b['materials'] if x['path']==m['path']),'current_registry_complete_preimage':can[m['path']],'next_complete_row':m,'fields_changed_against_current':{k:{'before':can[m['path']].get(k),'after':m.get(k)} for k in set(can[m['path']])|set(m) if can[m['path']].get(k)!=m.get(k)},'mathematical_record_changes':[]} for m in c['materials']])
readme='''# 0019 整包证据闭合准备

本私有包审计原 DONE/Boss3 0019 的 **32 材料 / 30 身份**。30 完整数学 record 与 current registry 逐字段相同，且未发现更高实际 DONE 母件；全部沿用唯一完整 v1。保持 model、量词、前提、truth_status、body、evidence、sources，不更改原 DONE 文件、不新 ID、不建超边、不执行数学程序。

## 唯一 schema2 candidate

`schema2-supplement-candidate.json` 为 **0 records / 5 materials / edge_files:[]**，沿用 af99 冻结基线。仅改 M1/M9/M11/M27/M31 的 disposition 与 reason，所有旧 owner 数组逐项保留：M1 与 M27 因重复正文及同实现/输入输出而 excluded，M11 是重复 B7 导航 excluded，M9 为已全文接证的程序 attachment，M31 为已接 B9/HF attachment。excluded 是排除重复登记职责，不是否定数学。M1/M27 无需为闭合导航而给原主 record 升版。

纯 `registration.validate_batch` 已通过，未调用 map_tasks、compose、Git、网络、队列或任何登记写入。未来 `task-draft.json` 仅标准数组草案，由 lead 合法 plan，绝非已认领或已 DONE。

## 数学完整性与旧 needs

`objects-30-audit.json` 保存每份原/当前完整 preimage、精确接口比较和实际母件绑定。`materials-32-audit.json` 覆盖所有材料，`old-needs-substantive-comparison.json` 逐项处理旧 receipt 的 15 条待路由记录。保留两个 open 合同、一个 conditional、一个 finite 与一个 definition；不把阴性有限搜索当全称反证，亦不要求开放命题先证明才能登记。

裸 BG 与 UNION/GLOBAL、新增覆盖补偿、附加二倍旧覆盖预算、真实有序续局、合法 H 与任意并集、三种排序失败、指定75客户路径拒绝、FLOOR 与平方信用、RET代数与累计L付款分别保全。B9 的 m=s 均匀配对/连续 t 曲线只复用 current0018v1，不能吞入0020的 J/锚点/alpha/s≤m/NU/FL 量词。

## 外主件与剩余请求

`foreign-requests.json` 保留四份完整历史 preimage/next union：ROOT 与 SELECTED 撤回，不纳入 candidate；存续的两个 request 仅为 3aee 独立对偶证明 §§3–4、c7b 独立流障碍证明 §§4–5，均 request-not-accepted。原379 JSON已被现988135精确节覆盖，未再请求。完整 old source/body/evidence保全，未给 candidate 添未实际接证的 foreign reverse owner。`request-five-upper.json` 保存父撤回的历史请求：same-byte duplicate already linked by current full body。

实际母件：ROOT 为0010；SECURITY-CONE-DUAL 为 owner-acceptance-20261107-04 的 v2；full-tree 稳定身份为 customer-attraction/full-tree-averaging-obstruction 的0049v1；SELECTED 为0013v1。0013/0017新补证已pushed但prepared，不是实际DONE；未作为母件。

尚缺主发布身份只在 `missing-principal-source-routes.json` 保存精确原件、稳定 frontmatter/legacy Claim 与实际 task 路由，不造 stub。0001-5已withdrawn，实际后继0001-5-evidence是claimed；0002、0009、0069均claimed，不能当DONE或可抢。21锥的0036 followup实际DONE但objects空，明确原主仍0009，不能将0036当数学主母件。

## 证据、阅读与保护

`path-sha-unique-atx-checks.json` 对原30record全部body/evidence、32原材料及请求精确refs执行文件SHA与section唯一ATX检查，全部通过。`foreign-byte-comparison.json` 保存具体逐字节重复位置。原task/batch/receipt和受保护ready的SHA均再次核对。

`reading-and-budget.json` 将本次实际读取区间与旧receipt成熟全文复用分开；不将旧manifest的“full bytes read”冒称本次raw全文验证。本次0搜索/LP/全树枚举/证书重放。500K总/300K正文元数据/200K其它为工程计划；系统prefix和实际used未知，字符与token不等价，未伪造token遥测。

只写 research/workspaces/p25-register-v2/Boss3/0019-evidence-closure/。此包尚未获正式窗口，未写正式workspace/batch/receipt/registry/ready。父验收后本实例结束；本实例不接下一批。
'''
# exact unresolved count from oldreceipt
readme=readme.replace('15 条待路由记录',str(len(receipt['summary']['unresolved_identity_or_source']))+' 条待路由记录')
(OUT/'README.md').write_text(readme)
files=[ref(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='finish-manifest.json']
write('finish-manifest.json',{'schema':1,'package':'0019-evidence-closure-private-preparation','original_task':ref(ROOT/'research/operations/p25-register-v2/tasks/register-ab98f323ad-0019.json'),'original_batch':ref(ROOT/'research/registration/batches/register-ab98f323ad-0019.json'),'original_receipt':ref(ROOT/'research/registration/receipts/register-ab98f323ad-0019.json'),'candidate':ref(OUT/'schema2-supplement-candidate.json'),'objects_audited':30,'materials_audited':32,'candidate_records':0,'candidate_materials':5,'foreign_requests_unaccepted':2,'withdrawn_requests_in_foreign_file':2,'withdrawn_five_upper_request':1,'files':files,'permission_state':'private-only; no formal write window','mathematical_executions':0,'git_commands':0,'new_ids':0,'edges':[]})
print(json.dumps({'candidate':ref(OUT/'schema2-supplement-candidate.json'),'manifest':ref(OUT/'finish-manifest.json'),'foreign_requests':ref(OUT/'foreign-requests.json'),'reading':ref(OUT/'reading-and-budget.json'),'old_needs_count':len(receipt['summary']['unresolved_identity_or_source'])},ensure_ascii=False,indent=2))
