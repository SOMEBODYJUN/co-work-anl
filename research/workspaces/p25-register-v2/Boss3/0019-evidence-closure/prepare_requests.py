import json,pathlib,hashlib,copy
OUT=pathlib.Path('research/workspaces/p25-register-v2/Boss3/0019-evidence-closure')
def read(p):return json.loads(pathlib.Path(p).read_text())
def ref(p,section=None):
 d={'path':str(p),'sha256':hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()}
 if section:d['section']=section
 return d
registry=read('research/registry.json');canonical={o['object_id']:o for o in registry['objects']}
all_done={}
for p in pathlib.Path('research/operations/p25-register-v2/tasks').glob('*.json'):
 t=read(p);br=t.get('receipt',{}).get('batch_file')
 if t.get('state')!='done' or not br:continue
 bp=pathlib.Path(br['path'])
 if not bp.is_file() or ref(bp)['sha256']!=br['sha256']:continue
 for o in read(bp).get('objects',[]):all_done.setdefault(o['object_id'],[]).append({'task_file':ref(p),'state':'done','owner':t.get('owner'),'receipt_batch_file':br,'record':o})
def request(oid,refs,reason):
 rows=all_done.get(oid,[]);mx=max(x['record']['version'] for x in rows);top=[x for x in rows if x['record']['version']==mx]
 assert len({json.dumps(x['record'],sort_keys=True,ensure_ascii=False) for x in top})==1
 pre=copy.deepcopy(top[0]['record']);nxt=copy.deepcopy(pre);added=[]
 for r in refs:
  if any(q['path']==r['path'] and q['sha256']==r['sha256'] and (not q.get('section') or q.get('section')==r.get('section')) for q in [pre['body']]+pre['evidence']):continue
  nxt['evidence'].append(r);added.append(r)
 if added:nxt['version']=pre['version']+1
 return {'object_id':oid,'status':'request-not-accepted','reason':reason,'actual_highest_done_mothers':top,'canonical_equal_preimage':canonical.get(oid)==pre,'preimage':pre,'next_complete_union':nxt,'added_evidence':added,'old_fields_preserved':[k for k in pre if k not in ['version','evidence']],'claim':'Full field union is prepared only; validate/prepared do not imply author acceptance or DONE.'}
mat1='archives/customer-attraction/state/计算/五人中途偏离与菜单证书--计算.md'
req=request('CA-FIVE-UPPER-221-100',[ref(mat1,'中途偏离证书核验了什么'),ref('archives/customer-attraction/tools/evidence/five-player-old/replay/customer_attraction_five_player.json'),ref('archives/customer-attraction/tools/evidence/five-player-old/replay/customer_attraction_five_player_independent.json')],'同一21乘子/1024会员余项的主与独立原字节重放执行链；完整成熟计算正文解释两脚本不同重构职责，非新福利命题。保原真实集合目录、恰五人、零背景及弱平局域，不扩到同覆盖异标签。')
(OUT/'request-five-upper.json').write_text(json.dumps(req,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'file':ref(OUT/'request-five-upper.json'),'actual_mothers':[(x['task_file'],x['receipt_batch_file'],x['record']['version']) for x in req['actual_highest_done_mothers']],'new_evidence':req['added_evidence']},ensure_ascii=False,indent=2))
# Full inventory is metadata; records are not replayed as proofs.
(OUT/'done-record-index.json').write_text(json.dumps(all_done,ensure_ascii=False,indent=2)+'\n')
# Parent's mathematical comparison: the proposed five-player v2 is withdrawn.
req['status']='withdrawn-same-byte-duplicate-already-linked-by-current-full-body'
req['parent_judgment']='Parent read full main body d0db..., exact 01e12 section and both replay JSONs. Body section 4 already links evidence/runs/2026-10-10/customer_attraction_five_player{,_independent}.json with identical bytes to the replay copies (2281/859 bytes), and states 1024/43/2048 and independent node reconstruction. No new independent evidence or scope.'
(OUT/'request-five-upper.json').write_text(json.dumps(req,ensure_ascii=False,indent=2)+'\n')
rootdir=pathlib.Path('archives/customer-attraction/tools/evidence/root-tax-upload-20261030')
rootrefs=[ref('archives/customer-attraction/state/审查/四人根税独立上传与传输接口增量审计--审查.md','2. 61 客户四人完整 SPE 的独立单位客户重放')]
rootrefs += [ref(rootdir/name) for name in ['RootTax-all_deviations.raw','RootTax-all_nodes.raw','RootTax-comparison_21_pairs.raw','RootTax-last_replies.raw','RootTax-numeric_claims.raw','RootTax-static_safety_56_multisets.raw','RootTax-summary.raw']]
flowdir=pathlib.Path('archives/customer-attraction/tools/evidence/incremental-security-flow')
requests=[
 request('CA-ROOT-TAX-NO',rootrefs,'原主body已含相同独立脚本及核心数值；这里仅请求其原始独立上传执行链的七份CSV/JSON输出，而非重复结论。259节点/1295非自身偏离/216末回复/56静态背景及负向控制完整原字节未见于当前record直接证据。若父确认这些字节已由主body现有链接全文接证，则本请求撤回，不为导航增版。'),
 request('CA-SECURITY-CONE-DUAL',[ref(flowdir/'3aee25998e06b261a8b5.raw','3. 完整树证书 (T) 的正确性'),ref(flowdir/'3aee25998e06b261a8b5.raw','4. (GL) 与“没有证书即真反例”的精确前提')],'独立内部数学稿完整重构固定(σ,p)的minimax/闭多面体锥对偶双向证明与有理严格分离提取；明确Q不依w、同覆盖标签与不同覆盖实现w0扰动两域。非五固定游戏PASS。当前v2保全；该独立证明source不在其已有body/evidence字节引用中。'),
 request('customer-attraction/full-tree-averaging-obstruction',[ref(flowdir/'379d7599d93910cb6dc4.raw'),ref(flowdir/'c7b73d6fbb280dc7583b.raw','4. 固定流和深度平均流：两个不同层次的否定'),ref(flowdir/'c7b73d6fbb280dc7583b.raw','5. 15 类型、43 节点平均障碍')],'已有988135审查section保379字段摘要；本请求为其独立定义级重建的原结果及c7b逐节点/逐客户独立数学证明全文。保两种受限模板、负完整IC而非SPE反例、q固定和不排全Gamma。若最高实际母件已收原文全文则不用重增版。'),
 request('CA-SELECTED-SECURITY-CONES',[ref(flowdir/'a4dd82aa41fb5665aec0.raw')],'当前record持三策略13证书原输入48eba...；此ff8c...为原独立4914项逐类型有理恒等式输出，非该输入同字节。只补执行/验收链，不将五个固定游戏的指定最优p有限表纳入全锥数学，不改version以外任何旧数学字段。')]
(OUT/'foreign-requests.json').write_text(json.dumps(requests,ensure_ascii=False,indent=2)+'\n')
keep={o['object_id'] for o in read('research/registration/batches/register-ab98f323ad-0019.json')['objects']}|{r['object_id'] for r in requests}|{'CA-FIVE-UPPER-221-100','B7-ROBUST-PREFIX-FLOOR-UNBOUNDED-v1','CA-COVERAGE-OPPORTUNITY-NO','CA-TAX-BRIDGE-NO','CA-TAIL-FOUR-ALL-N'}
(OUT/'done-record-index.json').write_text(json.dumps({k:v for k,v in all_done.items() if k in keep},ensure_ascii=False,indent=2)+'\n')
print('foreign-requests',ref(OUT/'foreign-requests.json'))
for r in requests:print(r['object_id'],r['preimage']['version'],'->',r['next_complete_union']['version'],len(r['added_evidence']),[x['receipt_batch_file']['path'] for x in r['actual_highest_done_mothers']])
