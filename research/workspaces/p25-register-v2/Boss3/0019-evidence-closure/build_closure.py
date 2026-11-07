import json,pathlib,copy,hashlib,re,sys,collections
ROOT=pathlib.Path('.').resolve();OUT=ROOT/'research/workspaces/p25-register-v2/Boss3/0019-evidence-closure'
def read(p):return json.loads(pathlib.Path(p).read_text())
def write(n,d): (OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def ref(p):
 p=pathlib.Path(p);return {'path':str(p.relative_to(ROOT)) if p.is_absolute() else str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
b=read(OUT/'original-batch.json');oldr=read(OUT/'original-receipt.json');reg=read(ROOT/'research/registry.json');canonical={o['object_id']:o for o in reg['objects']}
requests=read(OUT/'foreign-requests.json')
for q in requests:
 if q['object_id'] in ['CA-ROOT-TAX-NO','CA-SELECTED-SECURITY-CONES']:
  q['status']='withdrawn-duplicate-existing-input-implementation-and-proof-responsibility'
  q['withdrawal_reason']= ('Six CSVs byte-identical to existing tax-interfaces/replay/root_independent; summary has no different input, implementation or mathematical duty from full current body lines164–170 and the directly referenced independent code. No version increment for repeat output/navigation.' if q['object_id']=='CA-ROOT-TAX-NO' else 'Current full body60 and106–118 already accounts for this old 4914-coordinate audit on the same13 original certificates; current gb-sign-correction README and correction-evidence52–71 directly preserve a further independent Fraction verification. No new input or proof duty is supplied by the historical success summary.')
 elif q['object_id']=='customer-attraction/full-tree-averaging-obstruction':
  q['added_evidence']=[r for r in q['added_evidence'] if '379d7599' not in r['path']]
  q['next_complete_union']=copy.deepcopy(q['preimage']);q['next_complete_union']['version']+=1;q['next_complete_union']['evidence']+=q['added_evidence']
  q['excluded_duplicate']='379 original JSON already integrated by current evidence988135 section66–76, line74 exact source ID, lines91–99 frozen manifest routing. Request only c7b independent proof sections4–5, not a new output.'
 q['comparison_read_ranges']=({'current_body':[[21,172]],'new_review':[[1,88]],'raw_summary':[[1,189]]} if q['object_id']=='CA-ROOT-TAX-NO' else {'current_body':[[23,138]],'independent_proof':[[129,227]]} if q['object_id']=='CA-SECURITY-CONE-DUAL' else {'current_body':[[123,174]],'independent_proof':[[195,269]],'already_accepted_review':[[66,99]]} if 'full-tree' in q['object_id'] else {'current_body':[[34,118]],'correction_evidence':[[1,81]],'raw_report_read':'top42 lines plus JSON structural inspection; not full raw proof revalidation'})
write('foreign-requests.json',requests)
# Complete private primary audit; actual scan only accepted task.state done + receipt SHA.
scan=read(OUT/'actual-mothers-scan.json')
# Refresh exact mother data from the checked task; own records have no newer actual DONE version.
taskp=ROOT/'research/operations/p25-register-v2/tasks/register-ab98f323ad-0019.json';task=read(taskp);mother={'task_file':ref(taskp),'state':task['state'],'owner':task['owner'],'receipt_batch_file':task['receipt']['batch_file']}
objnotes=[
'恰五人真实回复菜单的规范24行界，原真实集合目录域保留；不把同覆盖标签主模型强加到该旧证书。',
'双根460行模板及负向分离只否定该模板，不是假half反例。',
'四人1499/750界；正文48–113自足导出固定背景两人税及一般接口，无额外导航批准门。',
'四极大Γ动态阈值独立合同，完整旧域/参数保全。',
'五极大n≥5半覆盖；n3/4基例与别名安全范围沿旧receipt全文审读复用。',
'五极大混合动态界与半覆盖是不同精确结论，参数和适用人数不吞并。',
'三人七客户反驳全并集二倍外推，但OPT3=5≤2W，绝非half反例。',
'关联LP对真实前缀包络，最优β和真实后继递归保全。',
'旧玩家双边终局包络不需SPE；保持有序前缀及终局约束。',
'有界联合MILP是M=m/W=1/整数客户表示，不从浮点成功推全局最优。',
'九客户完整SPE构造保全部平局与离轨续局。',
'有限19^4参数网格指定尾路径排除，不量化任意目录或所有可信前缀。',
'合法单题H比较恒等式，不允许向共同目录任意添加并集；P保旧人利润。',
'旧覆盖系数Farkas条件证书与数值搜索分开。',
'附加2u≥C_old下仍失败的GLOBAL合同；比原52客户一般GLOBAL有更强前提，不合并丢内容。',
'τ=1条件接口保持conditional，不把开放一般税预算写成proved。',
'fresh两人模板定义；有限未命中/LP infeasible不是一般不可能证明。',
'任意末回复策略锥非空保真实末位最佳回应。',
'BG/UNION-BG分开；UNION全称失败重复GLOBAL路由，已全文正文保全。',
'裸BG全称仍open，保|H\\O|新增覆盖补偿；不能要求先证完才登记。',
'PRIVATE-ROOT61客户合同与CA-ROOT-TAX根税结论不同。',
'等大小相邻交换失败的精确量词，不吞可信AB/BA条件的正接口。',
'递减排序失败与等大小交换失败各自保独有数据/量词。',
'递增排序失败保其完整输入与弱SPE，不因同研究路线合并。',
'r=2最大单例正端点不外推r≥3；R4阈值缺主身份另路由。',
'75客户2+3指定目标路径的必要可信拒绝，不是所有五人路径或half失败。',
'最优比较池净交换/RET恒等式不需SPE；随机保留与退款净额量词保全。',
'累计L全前缀付款仍open；账本代数不证明SPE付款。',
'61客户真实h=A局部FLOOR失败，1971扫描/最小性不重验。',
'同真实h=A平方旧负载credit失败，与FLOOR分立，保原完整SPE入口。']
assert len(objnotes)==len(b['objects'])==30
write('objects-30-audit.json',[{'index':i,'object_id':o['object_id'],'original_complete_preimage':o,'current_complete_record':canonical[o['object_id']],'current_equals_original':canonical[o['object_id']]==o,'actual_highest_done_mother':mother,'actual_highest_done_complete_record':o,'interface_comparison':'All existing fields, model, statement, quantifiers, assumptions, truth_status, body/evidence/source retained exactly; no independent mathematical or evidence increment found.','mathematical_judgment':objnotes[i],'decision':'reuse-unique-highest-complete-record-without-version-change','delta':[]} for i,o in enumerate(b['objects'])])
# Per-material substantive closure, all32 remain in audit; candidate only changed rows.
notes={
1:'相同21乘子/1024/43/2048及独立节点重建职责已由CA-FIVE-UPPER当前完整body§4直接链接的同字节两JSON接证；24/460行由原本批owner收证。排除重复导航/重放材料，不否定数学，保所有既有owner，不升版、不等外作者批准。',
3:'固定背景两人税与(10)–(12)由本页48–113完整自足给出；CA-TWO-REMAINING-TAX外依赖已实际DONE0004。不是新独立结论待批准。',
9:'本页完整算法实现是有限网格排除record既有全文evidence；全量词递推主身份尚未发布，另存0001-5-evidence实际claimed路由。无独有数学未被现正文覆盖，闭合为attachment，保原owner，不造程序节点。',
11:'B7全m反例与倒二统一逃生/归档入口重复0047实际DONE稳定B7主body；本资源无独有数学，excluded，无批准门、无新owner。',
14:'17/39/69列infeasible及有限人工探针不贡献一般反证；主定义record已全文收证。一般52客户GLOBAL现0004精确身份，不为失败搜索向其加新证据或节点。',
16:'附加2u≥C_old的独立反例域已在本批M1ff0完整保全；一般GLOBAL与其不同前提；重复导航闭合，不覆盖任一合同。',
21:'UNION-BG与0004 GLOBAL代数相同，11客户局部q损失同CA-COVERAGE-OPPORTUNITY-NO；本页完整会计接口已归本批body/evidence，裸BG保open和新增覆盖补偿，无导航接收门。',
22:'可信交换在0013实际v1且preparedv2另记非DONE；三个排序反例与r2端点由本批各自收证。R4阈值/全菜单递推尚缺主发布身份，准确路由保存，不吞量词、不造stub。',
23:'R4最大单例36客户10→12反例的原测试器/输入执行链；稳定frontmatter及完整原body保route，0001-5-evidence为claimed非DONE。确缺可引用主身份，needs-decision不等于待数学证明。',
24:'静态不观察安全值2n−1界本页全文已被0003实际DONECA-OBLIVIOUS接证。36客户θ、全n聚合族、尾最小移位各自不同量词且主身份缺失；0001-5-evidence/0002/0069当前claimed，仅保存路由，不合成脚本节点。',
25:'去相关/菜单原JSON与现0008证据同字节；四尾提升c7§§1–2已在CA-TAIL-FOUR全body保存；379流原JSON由现988135精确节已并入；a4dd4914旧审计重复现body责任撤回请求。唯3aee独立对偶证明及c7§§4–5独立流证明请求未接。34/360逐人桥缺0001-5-evidence主身份，保原已有3owners不加未接foreignowner。',
26:'21固定锥真实条件定理的主CA-NEW-POLICY-CONE-SECURITY仍缺；0036已DONE的后续包objects空且路由0009，不当其主母件。86/113/链分别0009claimed；75目标路径拒绝是本批独立数学，已完整收证。',
27:'6CSV与现root_independent完全同字节；summary重复当前CA-ROOT主body164–170同输入/实现/边界。传输整合PASS无新节点；本批FLOOR旧evidence已收整页。excluded重复证据材料并保既有owners，无ROOT升版/批准门。',
29:'15客户2u<F_r−F_next是既有首步税桥同输入的普通数值投影，不独造节点、不等原作者批准；净账本、累计L开放义务、61客户FLOOR/POWER2分别完整保全。',
31:'HF保重数准确核已由0027实际DONE收该精确节，B9均匀m=s连续t/二项/积分/端点已由0018v1实际收证；钱包/ROOT/SELF/PB/freeMfull为重复导航与模型警戒，无新独有数学。attachment保原两owner；不把0020 J/anchor/alpha/s≤m/NU/FL混入B9。'}
changed={1:'excluded',9:'attachment',11:'excluded',27:'excluded',31:'attachment'}
audit=[];mats=[]
for i,m in enumerate(b['materials']):
 n=copy.deepcopy(m)
 if i in changed:n['disposition']=changed[i];n['reason']=notes[i];mats.append(n)
 audit.append({'index':i,'material':{'path':m['path'],'sha256':m['sha256']},'old_complete_preimage':m,'next_complete_row':n,'math_comparison':notes.get(i,'原完整数学接口和全部proof/evidence入口无增量；原全文成熟审读按receipt及同SHA复用。'),'decision':'candidate-disposition-update' if i in changed else 'retain-original-row-with-clarified-audit','existing_owners_preserved':n.get('object_ids',[])==m.get('object_ids',[]),'new_owners':[],'changed_fields':[k for k in n if n[k]!=m.get(k)]})
write('materials-32-audit.json',audit)
needs=oldr['summary']['unresolved_identity_or_source'];write('old-needs-substantive-comparison.json',[{'original':n,'decision':notes[n['material_number']],'material_candidate_change':n['material_number'] in changed} for n in needs])
baseline={'path':'research/registration/baseline-5cd4b9018.json','sha256':'af99fb773928f3fc6bcd577ade37fbb07e8f84befbb2304158b99894ab1e56a3'}
candidate={'schema':2,'baseline':baseline,'objects':[],'materials':mats,'edge_files':[]};write('schema2-supplement-candidate.json',candidate)
# Prepared-only source routes: exact frontmatter and full immutable source text saved, never fake records.
route_names=['完整历史纯SPE终局全集--算法.md','R4最大单例阈值失败证书--反例.md','三人聚合末位保底--反例.md','三人及以上聚合末位保底--反例.md','三人逐人混合安全值--反例.md','最小收益移至末两位的福利代价--障碍.md','五人首位收益低于真正混合安全值--反例.md','真实前缀逐步安全值付款--反例.md','真实路径安全值链的嵌入与债务恒等式--定理.md']
tasks=[]
for p in (ROOT/'research/operations/p25-register-v2/tasks').glob('*.json'):
 t=read(p);tasks.append((p,t))
routes=[]
for p in (ROOT/'archives/customer-attraction/state').rglob('*.md'):
 if p.name not in route_names:continue
 text=p.read_text();front=text.split('---',2)[1] if text.startswith('---') else ''
 actual=[{'task_file':ref(tp),'state':t['state'],'owner':t.get('owner'),'assignment_material':m,'receipt_batch_file':t.get('receipt',{}).get('batch_file')} for tp,t in tasks for m in t.get('definition',{}).get('materials',[]) if m['path']==str(p.relative_to(ROOT))]
 routes.append({'principal_body':ref(p),'exact_frontmatter':front,'exact_body_text_for_route_only':text,'actual_task_routes':actual,'canonical_records_with_exact_body':[o['object_id'] for o in reg['objects'] if o['body']['path']==str(p.relative_to(ROOT))],'policy':'Source routing only; no stub, allocation, claim, acceptance or ownership inferred from claimed/prepared.'})
write('missing-principal-source-routes.json',routes)
# Future definition draft uses standard task-array only and is not an issued task.
write('task-draft.json',[{'task_id':'register-boss3-evidence-followup-0019-closure-20261107','stage':'registration','baseline':baseline,'materials':[{'path':m['path'],'sha256':m['sha256']} for m in mats],'shared_read_refs':task['definition'].get('shared_read_refs',[]),'instruction':'Prepare exactly this minimal0019 disposition closure; compare the full retained original30 records and current highest actualDONE mothers. No edges or new IDs. Foreign independent-proof requests remain unaccepted and outside this candidate. This array is a draft for future lead plan only, not a claim or completion.'}])
# SHA + exact ATX heading checks for all own refs, old materials, foreignpreimage/newrefs, baseline/protected.
refs=[ref(taskp),task['receipt']['batch_file'],ref(ROOT/'research/registration/receipts/register-ab98f323ad-0019.json'),baseline]
refs += [{'path':m['path'],'sha256':m['sha256']} for m in b['materials']]
for o in b['objects']:refs +=[o['body']]+o['evidence']
for q in requests:refs +=[q['preimage']['body']]+q['preimage']['evidence']+q['added_evidence']
checks=[]
for r in {json.dumps(x,sort_keys=True):x for x in refs}.values():
 p=ROOT/r['path'];actual=ref(p)['sha256'];row={'ref':r,'sha_match':actual==r['sha256']}
 if r.get('section'):
  matches=[i for i,l in enumerate(p.read_text().splitlines(),1) if re.match(r'^#{1,6}\s+',l) and re.sub(r'^#{1,6}\s+','',l).strip()==r['section']]
  row['exact_ATX_heading_lines']=matches;row['unique_ATX']=len(matches)==1
 checks.append(row)
assert all(x['sha_match'] and x.get('unique_ATX',True) for x in checks)
protected=ROOT/'research/registration/ready-boss3-recovered-17.json';assert ref(protected)['sha256']=='29fdadda602ee776545beeee6693c6807257340276e5b7072fa1c9a3aa076c47'
write('path-sha-unique-atx-checks.json',{'checks':checks,'all_pass':True,'protected_ready':ref(protected),'original_done_task':ref(taskp),'original_done_batch':ref(ROOT/task['receipt']['batch_file']['path']),'original_done_receipt':ref(ROOT/'research/registration/receipts/register-ab98f323ad-0019.json'),'same_baseline_reused':baseline})
# file-only pure validation, avoid pycache writes outside private runtime.
sys.dont_write_bytecode=True;sys.path.insert(0,str(ROOT/'tools'));import registration
result=registration.validate_batch(ROOT,candidate,expected_materials=candidate['materials'],baseline_ref=baseline)
write('validation.json',{'method':'registration.validate_batch pure files only','result':result,'no_git_network_queue_registry_write':True})
print(json.dumps({'candidate':ref(OUT/'schema2-supplement-candidate.json'),'counts':{'objects':len(candidate['objects']),'materials':len(mats),'audited_objects':len(b['objects']),'audited_materials':len(b['materials'])},'validation':result,'remaining_foreign_requests':[q['object_id'] for q in requests if q['status']=='request-not-accepted']},ensure_ascii=False,indent=2))
