from pathlib import Path
import json,hashlib,copy,re
ROOT=Path('.').resolve(); OUT=ROOT/'research/workspaces/p25-register-v2/Boss3/0020-evidence-closure'
def load(p):return json.loads((ROOT/p).read_text())
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def ref(p):return {'path':p,'sha256':sha(p)}
def write(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
tp='research/operations/p25-register-v2/tasks/register-ab98f323ad-0020.json';bp='research/registration/batches/register-ab98f323ad-0020.json';rp='research/registration/receipts/register-ab98f323ad-0020.json';basep='research/registration/baseline-5cd4b9018.json'
task=load(tp); old=load(bp); canonical=load('research/registry.json'); base=load(basep); obs=canonical['objects']; obs=list(obs.values()) if isinstance(obs,dict) else obs; by={o['object_id']:o for o in obs}; frozen={m['path']:m['sha256'] for m in base['materials']}
oldids=[o['object_id'] for o in old['objects']]
extra=['CA-HISTORY-TIES','customer-attraction/full-tail-stationary-additive-defect-sharp-envelope-and-four-label-realization','customer-attraction/five-client-true-successor-clone-incumbent-gain','M-b7973e6d9dce4a3888f955e70d567a51']
ids=set(oldids+extra+[i for r in old['materials'] for i in r.get('object_ids',[])]+[i for r in task['receipt']['pending_routes'] for i in r['owner_ids']]); done={i:[] for i in ids}
for p in (ROOT/'research/operations/p25-register-v2/tasks').glob('*.json'):
 d=json.loads(p.read_text());receipt=d.get('receipt',{});br=receipt.get('batch_file',{})
 if d.get('state')!='done' or not br:continue
 if sha(br['path'])!=br['sha256']:raise ValueError('DONE batch byte mismatch: '+str(p))
 b=load(br['path'])
 for o in b.get('objects',[]):
  if o['object_id'] in ids:
   done[o['object_id']].append({'task':ref(str(p.relative_to(ROOT))),'task_id':d['definition']['task_id'],'owner':d.get('owner'),'state':d['state'],'receipt':copy.deepcopy(receipt),'batch_file':br,'record':o})
for k,v in done.items():v.sort(key=lambda x:x['record']['version'],reverse=True)
def mother(oid):
 ds=done.get(oid,[]);c=by.get(oid)
 if not ds:return {'origin':'canonical-only','record':c} if c else None
 top=ds[0]
 for x in ds:
  if x['record']['version']==top['record']['version'] and x['record']!=top['record']:raise ValueError('Same version differing DONE records: '+oid)
 if c and c['version']>top['record']['version']:return {'origin':'canonical-above-visible-DONE','record':c}
 return {'origin':'actual-DONE-exact-receipt-batch-bound',**top}
notes={
1:'34客户57节点空根稀释仅否D≥C：29/30<41/40，而u1−C=1037/120>0；不能改为弱u≥C、三角色或half失败。v2多接six-providers强菜单停界，保全部旧证据。',
2:'九主题两层Cartesian指定完整SPE族、n≥2及d≤b、nd≤2s下，一张ZA逐纯查询支配dT，所以全部p成立；不是同目录所有SPE的DB。含空菜单只给同菜单齐次缩放。',
3:'真自由分数鞍点双KKT给Fi−δ的非负余项；真实账含可负κ_i，故强W≥mδ与弱W≥(m−1/2)δ独立open，不以635坏p或PB非零背景局部平台否定。',
4:'固定完整σ/p/q后IC、双KKT和ΣFi−W均为类型重数线性；固定孩子qc给δchild上界而非下界，数值0不证明FG-all-optimal。与M3共享证据而模型仍是自由背景。',
5:'近113/817只是两个固定有理定点与全部有限报告的程序证据；没有精确dual不能把零目标变成普遍无反例，也不为这两PASS造对象。',
6:'2464发现器仅读817包的players/topics/policy，在63型重数锥重优化成635；目标是先跨角色平均负载再倒数的mG−W，不是817逐角色ΣFi−W。725的新21型/40617/340340与原635对象精确同一输入；这是需唯一635主owner接收的新发现程序/报告来源。其PB、SC、16及KKT链接是成熟重复导航。',
7:'94变量大M2系统在归一化固定策略锥中恰表达六纯查询各有严格挑战；DΔ≥1是整数严格化，不能外推16全局最小。local算法与16反例分立；发现报告12型确同原16输入，来源请求不改变16全单纯形结论。',
8:'固定p半2/5、同43节点策略的20λ/63r及支持等式g2=g5付款对全非负类型锥成立；ν0保齐次。16作者/独审合同含43/258、36g与完整输出，属同16来源；根4124 SC存在与旧635三个源为明确duplicate，不另增版。',
9:'固定policy/p的258IC、SC支持等式、solver-free逐列证书与5239输入相互闭合；只是M8主定理实现与精确证据，不另给发现程序节点，也不外推一般paid-SC。',
10:'m5单客户208 membership、108非零/92正future和九对代表f/θ只核STRICT-FUTURE算术及半recipient项；非208客户/游戏/IC或SPE。一般COPY-IC/WEIGHTED已在0033主body；3388原码/484输出是尚未入其母件的新证据请求，清楚的共同钱包open不是needs原因。',
11:'PUSH为一对子父同孩子全部prefix请求列次随机、非减价及纯祖先栈有限修域；不保多孩子共同钱包。最高实际DONE v3已接0e28基础PUSH三节，不能重复同页增版或退回canonical v2。',
12:'任意两合法叶M矩阵保共享客户总量及双边marginal，同一W合并系数共同cap；可能向过去角色回流，不继承PUSH价格/TIME/HIT。0033补证DONE v2已接0e28 H/M节，完整保留。',
13:'COMMON只接受每客户共同coverer已有合并密度，保指定同角色+新增coverer支持；固定父静态新列另一矩阵给同时COLUMN与严格ROW，两命题不合并。接受six-providers证据的v2完整保全。',
14:'PREFIX、合成完整利润QUERY-PROJECTION、REVERSE是不同方向：每条q≤a不推出Σq≤a；REVERSE保第一正边、截current≤1，不自动修假过去或全SD网络。各最高v2/v3完整保全，普通同页组件不再增版。',
15:'两个有守卫完整实现归同一35单位客户反例；full-tree补全和35相对33参数差异重要，不能按实现数另立数学对象。',
16:'无守卫ROOT实现的17字段/31动作审计是同35输入的第三来源；复用成熟原执行，当前不import或覆盖原报告。',
17:'35客户actual AED利润18/8/9，第二位复制A真叶AAF1得8<9；它同时否COPY2与全利润先后两倍，却因actual A∩E空不否交集PCAP。TEST逐源独立消元与PCAP2 open、有限十一控制器记录分立。',
18:'TEST对每固定目标消去全部SRC权重、源可选不同孩子；26目标的达优见证不是跨目标共一请求。11控制器/2911节点的有限记录保持finite；ρ≤1/2不能单独付2ul。',
19:'激活前固定Hall-B λ使用R/I-query联合库存、I条件删且actual信用不动；SOURCE初始化同时已付，总正费incoming开放。与逐world随机赢家B(U)、LOCAL-TOTAL另域，不被后者替代。',
20:'COVER对每行唯一混合与自由G取消，恰等价全部非负PRICE；均匀ROW-MASS逐式等于0010 NR-MAX。该段仅重复同模型/任意最优O/同σ真续和half推论，无独立新证明或程序证书，登记为重复导航，不人为制造外作者审批或新ID。',
21:'同一priority世界B→A只保送R子流再residual增广，保每R终点并节省至少N_I；固定原R路线和完整IC价格≥1。不能拆相关均值或据随机收入买IC。现v2新增合同史完整保留。',
22:'固定等分Hall-B到固定ΓA的投影节省κ−，与M21随机unit图分立；不保SOURCE-NET/localδ或root-regret。现v2合同史证据保留。',
23:'OFF-IC需真父规定a、包括全部fresh/outside并扣ell；同A同recipient多父半系数不等于总费半收缩，阈值只约束同客户。0047来源闭合v2已纳双回归与合同史整页，不能因同页段落再增版。',
24:'SRC-MARGIN/POOL是既有η−Ksrc的普通同叶代数重排；HIT与抽象VISIT各有已证owner，BG的52>34+17只是同一GLOBAL反例复述。1736导航不含新独立证明/程序输入/证书；按重复来源导航排除，不再needs或为其新写外主记录，原三个owner指向保作可追溯去向。',
25:'抽象严格递增等分DAG的vk精确递推、同链同时达到及vk/√k→1已在唯一主body整页证明，source_refs恰3687原审查。无需SPE实现；本页保持objects复用主owner，不复制一个异主record。',
26:'原7381 BG合同被实际AB前缀52>51否定，但两本批自足小反例仍独立：A3/B2的M2=3>M1(A)=2；六客户四主题等实际收益2仍不许可BA。3687链摘要、背景GLOBAL/Cartesian必要条件与别条路由是已有来源的重复导航，不另授链或root half。',
27:'两原Fraction实现有限域支撑0021两因果删位主owner且母件已整页接收；M最差首位、终局额外query亦已有本批主owner整页接收。Cartesian3787原source与0068主body/证据包同源，精确同末位合同及G差，无新独立证明；可作attachment，不再把重复导航挂needs。',
28:'十一客户三人31节点AAB、W8、Mextra3而3Mextra−W1，LAST同输入Mb7/3；四处D/E平局决定策略身份。0024 M18正例节已在原0020 v1 evidence接受，不为同节再增版。',
29:'E2全部子列表的Bernoulli/无放回两证明，s≤m、任意锚J、a>0、NU非均匀与FL辅助质量全保；税只付Lout，不付Rout。B9的s=m均匀配对特例不足覆盖这些量词，维持原身份。',
30:'固定同槽配对J的Beta势、单位边际和真实最优前缀H_(a−1)信用；不能同leaf/跨prefix双花，与owner势H_a−1不同。不将形式空槽当真实新行动。',
31:'固定owner势四类边际给同叶I/G精确共同预算；first-owner重复信用不能倒填任意/分数owner。当前canonical仍v1，但0034补证实际DONE v2已接081ca/c2f7四节，必须完整保更高母件。',
32:'完整IC原积分2t−1为0，非负权1−t改为−1/6，是局部真实末位障碍；它不否静态BER/HARM，却禁止无证逐t/Beta重权。未重跑有限基线。',
33:'同槽J的BER/HARM、共同α参数稳定核、随机MATCH、任意q锚及FIRST唯一块容量全保；它们是静态合法替槽。B9只共同s=m配对特例，不吞本J/anchor/α域。',
34:'E1全索引、E2谱平均、E3粗联合并集、E4逐主题关联和E5唯一块不是五个重复对象；外部并集不能换关联数，插值必须连同合法列表混合。B9 all-r双向调和母件另属0018，不重复。',
35:'十四客户完整两人策略Φ2=W9<OPT10，负载只有0/1，改高负载cap不能修该全人数候选；恰六人受限式不由该例裁定，half仍18>10。',
36:'原三固定策略26节点57真备选与补W8证据不枚举全SPE；CA-RESIDUAL-NO和CA-HISTORY-TIES最高DONE都已整页引用本页，直接复用并修旧页ID路由。CA-SPE-NON-PNE当前v2另保47客户第二证书，若补本页必须以完整v2母件并集，不回退三客户v1。',
37:'任合法有序背景当前余r人，ui≥maxTΣ1/(b+r)，真后继IC给每节点统一粗保底；非最终残余M(C)或跨枝旧持有者原收益。解析证明而非有限审计支撑全称。',
38:'不交安全锚Ci、风险Ai⊇Ci、统一λ和每Y至少d次均为承重；最后正锚给λ≤m−p，全零锚Y空，OPT结论另需O∖U⊆Y。非统一/非超集不在域内。',
39:'Kqq风险+q+1 safe，q≥2/M偶，指定全有序完整SPE通过裸上界/末位BR/非结构子树粘合；不能全safe或少席重启。另整数背景θ=v=M/2用均匀风险查询和整数倒数切线匹配，不推广自由分数或一般rank2。',
40:'根CLAIMS三精确对象不能汇成账本节点：stationary形式全参数sharp不等于SPE sharp；真实clone15节点旧人增益；十客root-menu仅粗压缩且未补SPE、排序023非有序路径。前两已DONE且本页仅同Claim摘要/原证明导航，按准确主ID归位，不重复增版外请；第三0069仍claimed/Boss2无母件，保needs真实路由；不将别的已否逐人旧OPEN恢复。',
41:'G=C∖O份额真枝L=A+R−Z，R有符号且零分母端点单列；半覆盖净目标为|D|≤W+|G|。逐枝各≤|G|不能跨枝合为一份G，940B标量程序较真分支更宽且无当前执行。'
}
spans=[json.loads(s) for s in (OUT/'reading-spans.jsonl').read_text().splitlines()]
source_scope={}
for s in spans:source_scope.setdefault(s['path'],[]).append({k:s[k] for k in ['line_start','line_end','byte_start','byte_end','bytes']})
materials=[]; audits=[]
for i,m in enumerate(task['definition']['materials'],1):
 assert sha(m['path'])==m['sha256'] and frozen[m['path']]==m['sha256']
 row=copy.deepcopy(old['materials'][i-1]); current=[x for x in canonical['materials'] if x['path']==m['path'] and x['sha256']==m['sha256']]
 for x in current:
  row['object_ids']=list(dict.fromkeys(row.get('object_ids',[])+x.get('object_ids',[])))
 if i==24:row['disposition']='excluded'
 if i==27:row['disposition']='attachment'
 if i==36:
  for oid in ['CA-RESIDUAL-NO','CA-HISTORY-TIES']:
   mo=mother(oid)
   assert mo and any(r['path']==m['path'] and r['sha256']==m['sha256'] for r in [mo['record']['body']]+mo['record']['evidence'])
   row['object_ids']=list(dict.fromkeys(row['object_ids']+[oid]))
 row['reason']=notes[i]+' 本轮复用原0020精确DONE收据中的成熟正文/证明读取；不把旧作者的全文阅读或运行记作本worker fresh全读/新执行。'
 if i in [6,10,36,40]:
  bound={6:['M-f55fd1a56f574bcbac6960e92f693c59'],10:['customer-attraction/first-deviation-source-copy-strict-future-migration-and-weighted-remainder'],36:['CA-RESIDUAL-NO','CA-HISTORY-TIES','CA-SPE-NON-PNE'],40:['customer-attraction/full-tail-stationary-additive-defect-sharp-envelope-and-four-label-realization','customer-attraction/five-client-true-successor-clone-incumbent-gain']}[i]
  bindings=[]
  for oid in bound:
   mm=mother(oid)
   accepted=[r for r in [mm['record']['body']]+mm['record']['evidence'] if r['path']==m['path'] and r['sha256']==m['sha256']]
   bindings.append({'object_id':oid,'version':mm['record']['version'],'actual_DONE_task':mm['task'],'actual_DONE_batch':mm['batch_file'],'unique_body':mm['record']['body'],'accepted_this_material_refs':accepted})
  row['reason']+=' 准确主身份/完整最高母件及本页既有接收绑定：'+json.dumps(bindings,ensure_ascii=False,separators=(',',':'))+'。'
 if i==40:
  row['reason']+=' ROOT-MENU-TAIL-SAFETY-PLUS-LAST-NO-v1的唯一候选正文为'+json.dumps(ref('archives/customer-attraction/state/障碍/根菜单尾总安全与末位最优的压缩障碍--障碍.md'),ensure_ascii=False,separators=(',',':'))+'；对应0069任务当前claimed/Boss2，无实际DONE收据，不加入未接受foreign owner。'
 if i in [6,10]:row['reason']+=' 仍留needs的唯一原因是本页独有程序/报告来源尚未由所列唯一主owner实际接收，不是已识别模型/命题自身开放；本批不冒充接收。'
 if i==40:row['reason']+=' stationary/clone为相同原Claim的成熟重复导航，不制造审批或新版本；仍留needs只因0069未刊主身份尚无实际DONE完整母件，不是已明确数学开放。'
 materials.append(row)
 audits.append({'number':i,'material':m,'bytes':(ROOT/m['path']).stat().st_size,'lines':len((ROOT/m['path']).read_bytes().splitlines()),'baseline_sha_match':True,'current_file_sha_match':True,'old_material_complete':old['materials'][i-1],'current_material_complete':current,'candidate_material_complete':row,'mathematical_comparison':notes[i],'fresh_source_spans':source_scope.get(m['path'],[]),'mature_proof_reuse':{'task':ref(tp),'standalone_receipt':ref(rp),'actual_task_receipt_batch':task['receipt']['batch_file'],'assigned_ref':m,'fresh_full_text_claimed':any(s['line_start']==1 and s['line_end']==len((ROOT/m['path']).read_bytes().splitlines()) for s in spans if s['path']==m['path'])}})
objects=[]; identityaudit=[]
for i,o in enumerate(old['objects'],1):
 mo=mother(o['object_id']); assert mo and mo['record']; chosen=copy.deepcopy(mo['record']);objects.append(chosen)
 changed=[k for k in set(o)|set(chosen) if o.get(k)!=chosen.get(k)]
 canonical_delta=[k for k in set(chosen)|set(by.get(o['object_id'],{})) if chosen.get(k)!=by.get(o['object_id'],{}).get(k)]
 # Full old record, canonical, all exact DONE bindings and chosen record are saved. No field truncation.
 identityaudit.append({'old_index':i,'object_id':o['object_id'],'old_complete_record':o,'canonical_complete_record':by.get(o['object_id']),'all_actual_done_mothers':done[o['object_id']],'selected_unique_mother':mo,'candidate_complete_record':chosen,'fields_different_from_old':sorted(changed),'fields_different_from_observed_canonical':sorted(canonical_delta),'math_fields_preserved':all(o.get(k)==chosen.get(k) for k in ['object_id','title','kind','truth_status','model','statement','quantifiers','assumptions','scope','body']),'statement_action':'精确模型、量词、前提、结论及body均保留；仅保已实际DONE的完整来源/objection增量，不重证成熟正文。','new_version_created_here':False})
write('all-41-material-audit.json',audits);write('all-41-identity-audit.json',identityaudit)
write('preimages-and-highest-mothers.json',{'observed_canonical':ref('research/registry.json'),'original_task':{'ref':ref(tp),'complete':task},'original_batch':{'ref':ref(bp),'complete':old},'original_receipt':{'ref':ref(rp),'complete':load(rp)},'highest_unique_mothers':{i:mother(i) for i in sorted(ids)},'all_refs_current_bytes_checked':True,'forbidden_actions_performed':[]})
snapshot={'purpose':'audit-only complete original41 highest-record snapshot; not a publication batch','schema':2,'baseline':ref(basep),'objects':objects,'materials':materials,'edge_files':[]};write('whole-41-review-snapshot.json',snapshot)
main_numbers=[6,10,24,27,36,40]
candidate={'schema':2,'baseline':ref(basep),'objects':[],'materials':[materials[i-1] for i in main_numbers],'edge_files':[]};write('schema2-review-candidate.json',candidate)
write('main-candidate-scope.json',{'publication_candidate':'schema2-review-candidate.json','main_material_numbers':main_numbers,'objects':0,'materials':6,'why_no_original_objects_repeated':'本轮无自己新版本；高于canonical的PUSH v3/owner-potential v2与全部其他最高母件完整存preimages和全41审计。它们没有本轮新必要反向关联，不为保留旧数学而重复提交。','unchanged_material_numbers_skipped':[i for i in range(1,42) if i not in main_numbers],'snapshot_is_not_publication':'whole-41-review-snapshot.json仅为逐项审计，不可当main发布。'})
# These are requests, never accepted material owners or published records.
requests=[]
def req(oid,numbers,why,priority='required-new-source'):
 mo=mother(oid); assert mo and mo['record'];pre=copy.deepcopy(mo['record']);union=copy.deepcopy(pre);adds=[]
 for n in numbers:
  rr=task['definition']['materials'][n-1]
  # An existing whole-page body/evidence already subsumes every section of that exact byte version.
  whole=any(r['path']==rr['path'] and r['sha256']==rr['sha256'] and 'section' not in r for r in [pre['body']]+pre['evidence'])
  if whole:continue
  if rr not in union['evidence']:union['evidence'].append(rr);adds.append(rr)
  if rr['path'] not in union['sources']:union['sources'].append(rr['path'])
 if adds:union['version']=pre['version']+1
 requests.append({'object_id':oid,'status':'prepared-not-accepted-not-canonical','priority':priority,'material_numbers':numbers,'mathematical_comparison':why,'unique_primary_body':pre['body'],'actual_highest_complete_mother':mo,'complete_preimage':pre,'proposed_complete_union_record':union,'only_new_evidence':adds,'new_version_needed_only_if_accepted':bool(adds),'no_mathematical_statement_change':all(union[k]==pre[k] for k in pre if k not in ['version','evidence','sources']),'routing_instruction':'父Boss先核数学并协调唯一主owner/lead；接收前绝不将此foreign owner新增到candidate materials。若母件在发送前更高，先保高版本全部字段重基。'})
req('M-f55fd1a56f574bcbac6960e92f693c59',[6],'M6独有2464发现器/725全输出及817原输入消费合同；同21型635、43节点策略、pooled目标和40617/340340精确匹配，未新授635，不把非SC坏p挪给自由真鞍点。')
req('customer-attraction/six-label-pure-self-consistency-failure-and-unique-mixed-support',[7,8],'M7给6069发现/1567大小证书与整数严格化来源，M8给2798/5772与5444/10502/9101的完整输入、矩阵与阅读先验合同；12型16个单位客户/43节点/六差精确同一见证。保其完整单纯形唯一混合SC和全p付款主证明，不由发现器认证最小性或重奖旧审查。')
req('customer-attraction/first-deviation-source-copy-strict-future-migration-and-weighted-remainder',[10],'M10独有3388/484有限单客户算术audit来源，m5/208/九权只支持已证明迁移恒等及半recipient列；不认证COPY-IC、真实游戏、全θ/f或多history钱包。')
req('CA-SPE-NON-PNE',[36],'同三客户13节点CAC真SPE、静态4/3与真实CBB的5/6的旧原审计字节入口；完整当前v2另含47客户四人第二见证，union保它全部字段及证据，不能拿原0013 v1盖回。','source-byte-binding-for-existing-mature-proof')
write('external-owner-full-record-requests.json',requests)
# Exact routes which need no new primary record. Their present physical-page status stays explicit.
routes=[
 {'materials':[8],'old_owner':'M-a02226aa71044f5eabc247e5f2d01943','action':'duplicate-navigation-no-version','reason':'根4124的混合SC存在由原母body整页softmax/Brouwer证明，M8末段明确duplicate；固定p锥付款不反推一般付款。'},
 {'materials':[20],'old_owner':'M-a7b0caa09f434cc4bb2ae6bc171465ae','action':'exact-statement-duplicate-no-version','reason':'ROW-MASS=NR-MAX逐式同模型、任意最优O、原actual-prefix同σ真续，未加独立证明或必要证书。COVER全价格仍留两个本批owner。'},
 {'materials':[24],'old_owner':'customer-attraction/actual-cancellation-simultaneous-source-payment-and-incoming-balance','action':'ordinary-algebra-navigation-no-version','reason':'SRC-MARGIN/POOL只是同一η/Ksrc普通代数；不需为重复式申请外作者批准。原SOURCE-NET/incoming两个身份保量词。'},
 {'materials':[24,26],'old_owner':'customer-attraction/equal-splitting-increasing-absorption-visit-extremum','action':'same-source-duplicate-no-version','reason':'9f0240主body全页完整引用同3687原审查并自足给vk递推/同时达到/渐近证明，M24/26仅摘要。'},
 {'materials':[24,26],'old_owner':'customer-attraction/actual-prefix-fresh-coverage-global-counterexample','action':'same-counterexample-navigation-no-version','reason':'C*≤W+V与GLOBAL同式；M24/26转述已证52>34+17，不增加第二独立反例或证书。'},
 {'materials':[26,27],'old_owner':'customer-attraction/cartesian-fixed-plan-terminal-boundary-and-continuation-reset-gap','action':'same-original-proof-navigation-no-version','reason':'同人数/不交/完整Cartesian/保旧全树及末位G差，与0068 whole body和virtual-replay证据包同源；不产生新独立证明。'},
 {'materials':[36],'old_owner':'customer-attraction/equal-load-histories-distinct-continuations','resolved_owner':'CA-HISTORY-TIES','action':'reuse-existing-accepted-whole-page-evidence','reason':'实际DONE0003精确CA-HISTORY-TIES已整页绑定M36；页ID不新建身份。同理CA-RESIDUAL-NO亦已整页接受。'},
 {'materials':[40],'old_owner':'LOCAL-STATIONARY-FULLTAIL-SHARP-v1','resolved_owner':'customer-attraction/full-tail-stationary-additive-defect-sharp-envelope-and-four-label-realization','action':'same-claim-proof-navigation-no-version','reason':'本页37–65只复述同原Claim公式/漂移配对/四标签与SPE分界，并链接已有主body及354/160/377来源；无独立新证明、程序输入或证书，不为仅新增来源导航要求foreign增版。'},
 {'materials':[40],'old_owner':'CLONE-INCUMBENT-MONOTONICITY-NO','resolved_owner':'customer-attraction/five-client-true-successor-clone-incumbent-gain','action':'same-claim-proof-navigation-no-version','reason':'本页67–73只是同5客户15节点ABAA到AABB及1/4、3/4分解摘要，链接原主body和程序并明确没有新重跑输出；原Claim映射至已DONE稳定ID，无独立新证书不增版。'},
 {'materials':[40],'old_owner':'ROOT-MENU-TAIL-SAFETY-PLUS-LAST-NO-v1','action':'unpublished-owner-real-routing-gap','reason':'主body0e5706及十客户虚菜单精确存在，但0069仍claimed/Boss2，无可绑定的DONE完整母件；不得发明完整record或添foreign owner。','pending_task':ref('research/operations/p25-register-v2/tasks/register-ab98f323ad-0069.json'),'pending_body':ref('archives/customer-attraction/state/障碍/根菜单尾总安全与末位最优的压缩障碍--障碍.md')}
]
write('old-routes-substantive-dispositions.json',routes)
# Legitimate draft array only; it does not plan/claim, supersede, or mutate any original task.
draftid='register-boss3-evidence-closure-0020-review'
draft=[{'task_id':draftid,'stage':'registration','baseline':ref(basep),'materials':[{k:r[k] for k in ['path','sha256']} for r in candidate['materials']],'goal':'仅为父Boss审核后的合法plan草稿，未plan/claim。原DONE0020整41审计已完成，本局部批只更新M6/M10/M24/M27/M36/M40六行，objects为空；不重复提交已有主record。M24/M27消解重复导航，M36回填已实际接受的反向owner，M6/M10/M40准确写明稳定主身份、实际母件及尚未接受的独有来源。未接受foreign不得添object_ids。原DONE/task/batch/receipt不可改；以baseline-5cd4b9018做必要小增量，非跨baseline supersedes。不得将prepared外请或0069 claimed当已接受/DONE。','write_paths':['research/registration/batches/'+draftid+'.json','research/registration/receipts/'+draftid+'.json'],'context_plan':{'model':'gpt-6.1-sol','history_mode':'same-package-review-preparation','budget_is_runtime_measurement':False,'original_engineering_plan':task['definition']['context_plan']['budget'],'used_tokens':None,'instruction':'本worker已有真实读取和推理历史，不能当fresh0；500K/300K/200K只复用原工程规划，非本平台实报。新合法task应明确接续当前准备与精确未读断点，不重领原DONE。'}}]
write('legal-task-array-draft.json',draft)
# Byte-only validation inventory, with sections checked via exact ATX boundaries.
refs={}
for o in objects:
 for rr in [o['body']]+o['evidence']:refs[json.dumps(rr,sort_keys=True)]=rr
for q in requests:
 for rr in [q['proposed_complete_union_record']['body']]+q['proposed_complete_union_record']['evidence']:refs[json.dumps(rr,sort_keys=True)]=rr
refcheck=[]
for rr in refs.values():
 p=ROOT/rr['path'];b=p.read_bytes();ok=hashlib.sha256(b).hexdigest()==rr['sha256'];heads=[]
 if 'section' in rr:
  for n,line in enumerate(b.decode().splitlines(),1):
   mt=re.match(r'^ {0,3}(#{1,6})\s+(.+?)\s*#*\s*$',line)
   if mt and mt.group(2)==rr['section']:heads.append(n)
  assert len(heads)==1,(rr,heads)
 assert ok,rr
 refcheck.append({'ref':rr,'sha_match':ok,'atx_heading_lines':heads,'full_page_subsumes_sections':'section' not in rr})
write('all-reference-byte-and-section-audit.json',refcheck)
write('reading-scope-and-budget.json',{'new_worker_fresh_source_spans':spans,'prior_mature_proofs_reused':{'task':ref(tp),'receipt':ref(rp),'batch':ref(bp),'explicit_boundary':'原receipt宣称41成熟正文全文及related/raw阅读，已实际读取其完整reading元数据；本worker当前只新读spans中明确连续区间和全部41完整旧records/母件差异，不将历史阅读当自己fresh全读，也不重跑程序。'},'instructions_fresh_read':[{**ref(p),'line_start':1,'line_end':len((ROOT/p).read_bytes().splitlines())} for p in ['AGENTS.md','research/PHASE3_READINESS.md','prompts/02.5-3-worker.md']]+[{**ref('research/IMPLEMENTATION.md'),'line_start':1,'line_end':171}], 'task_definition_context_plan':'完整读取definition及context_plan；task receipt和standalone receipt的完整reading元数据另独立补读。','additional_workflow_source_spans':[{'path':'research/IMPLEMENTATION.md','line_start':274,'line_end':286},{'path':'tools/map_tasks.py','line_start':433,'line_end':472},{'path':'tools/map_tasks.py','line_start':476,'line_end':506},{'path':'tools/registration.py','line_start':1,'line_end':373}],'planning_only':{'original_declared_window_tokens':500000,'original_reading_tokens':300000,'original_reserve_tokens':200000,'actual_used_history_tokens':'unknown; not zero','runtime_remaining_tokens':None,'no_runtime_telemetry_claim':True},'source_span_bytes_before_dedup':sum(s['bytes'] for s in spans),'no_new_mathematical_programs':True,'no_git_network_credentials_queue_registry_or_other_batch_mutations':True,'truncation_handling':'开头过大聚合输出曾被截断，随后全部旧41对象用4个有界区块补读；母件差异去重按字段补读。完整task definition/context_plan在单独有界输出中已完整看到。其它大型source未冒称全新读取。'})
print('WROTE',len(objects),'objects',len(materials),'materials','NEEDS',[i+1 for i,m in enumerate(materials) if m['disposition']=='needs-decision'],'requests',len(requests),'refs',len(refcheck))
