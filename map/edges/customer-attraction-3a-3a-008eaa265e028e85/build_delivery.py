"""Build only this task's external review assets; never write the clone."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys

BASE=Path('/workspace/scratch/bbb425bb840f/co-work-anl-boss6')
ROOT=Path('/workspace/scratch/bbb425bb840f/boss6-staging/map-full156tail-round47')
TID='customer-attraction-3a-3a-008eaa265e028e85'
P=Path('map/edges')/TID
OUT=ROOT/P
CORE='customer-attraction/full156-fixed-prefix-parent-tail-report'
PAIR='customer-attraction/full156-pair-master-necessary-point'
REPAIR='M-b87610a328dc45d7ad30ca2266bbe362'
EXACT='CA-EXACT-PURE-SPE-ALL'
COMBINED='customer-attraction/combined-indexed-and-actual-B-necessary-point'
EID='boss6-full156-fixed-prefix-exact-tail-and-heterogeneous-cost-all'
CEID='boss6-full156-fixed-combined-and-pair-inputs-context-for-tail'
E='archives/customer-attraction/tools/evidence/'

def sha(raw):return hashlib.sha256(raw).hexdigest()
def pin(x):return sha(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def save(path,x):
    dest=ROOT/path
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def ref(path):
    path=str(path)
    raw=((ROOT/path) if (ROOT/path).is_file() else (BASE/path)).read_bytes()
    return {'path':path,'sha256':sha(raw)}

taskpath=f'research/operations/map-v2/tasks/{TID}.json'
task=json.loads((BASE/taskpath).read_text())
ready=json.loads(Path('/workspace/scratch/bbb425bb840f/boss6-staging/ready-full156tail-round47.json').read_text())
registry=json.loads((BASE/'research/registry.json').read_text())
objects={o['object_id']:o for o in registry['objects']}
assert task['state']=='claimed' and task['owner']=='Boss6' and task['request_id']==ready['request_id']
assert pin(task['definition'])==ready['definition_pin']
assert task['definition']['input_pins']==ready['input_pins']
assert all(pin(objects[oid])==p for oid,p in ready['input_pins'].items())
assert task['definition']['object_ids']==[CORE]

bodypaths=[
 objects[CORE]['body']['path'], objects['CAG-MODEL']['body']['path'],objects[EXACT]['body']['path'],
 objects[PAIR]['body']['path'],objects[REPAIR]['body']['path'],objects[COMBINED]['body']['path'],
 'archives/customer-attraction/state/程序/完整156主题的阈值物化收益矩生成器--程序.md',
 'archives/customer-attraction/state/程序/完整156主题的两人尾集合审计器--程序.md',
 'archives/customer-attraction/state/程序/完整156主题的作者两人尾审计器--程序.md',
 'archives/customer-attraction/state/计算/完整156主题固定前缀的收益矩数据--计算.md',
 'archives/customer-attraction/state/计算/完整156主题固定前缀的福利矩数据--计算.md',
 'archives/customer-attraction/state/计算/完整156主题的作者可信尾与实际缺陷报告--计算.md',
 'archives/customer-attraction/state/资源/完整阈值目录固定四前缀的可信尾停界--资源.md',
 'archives/customer-attraction/state/构造/回复会员阈值的共同凸抬升与对角预算拆分--构造.md',
 'archives/customer-attraction/state/程序/末回复阈值层的强配对闭包程序--程序.md',
 'archives/customer-attraction/state/反例/高收益席位与贪心终局不能替代完整可信退出--反例.md',
 'archives/customer-attraction/state/审查/前缀编译与阈值端点的真实审查读序--审查.md',
]
codepaths=[E+p for p in [
 'full156-kernel-generator/original/full156_tail2_kernel.py',
 'full156-tail-parent-report/original/audit_full156_reply_set.py',
 'full156-author-tail-auditor/original/audit_full156_tail2.py',
 'full156-payoff-kernel-data/verify_kernel_atoms.py',
 'full156-welfare-kernel-data/verify_welfare_atoms.py',
]]
structure=json.loads((OUT/'structured-native-reading.json').read_text())
native_refs=[{k:r[k] for k in ('path','sha256')} for r in structure['source_refs']]
audit_refs=[{k:r[k] for k in ('path','sha256')} for r in structure['mature_audits']]
refs={r['path']:r for r in [*map(ref,bodypaths+codepaths),*native_refs,*audit_refs]}
for r in refs.values():assert sha((BASE/r['path']).read_bytes())==r['sha256']
for r in task['definition']['context_plan']['reading_refs']:
    assert r['path'] in refs and refs[r['path']]['sha256']==r['sha256']

canonical_matches=[]
for name in registry['edge_files']:
    edge=json.loads((BASE/name).read_text())
    endpoints=set(edge.get('source_ids',[])+edge.get('target_ids',[]))
    if CORE in endpoints or PAIR in endpoints:
        canonical_matches.append({'path':name,'sha256':sha((BASE/name).read_bytes()),
            'reviewed_edge_id':edge.get('edge_id'),'source_ids':edge.get('source_ids'),
            'target_ids':edge.get('target_ids'),'scope':edge.get('scope')})
assert not canonical_matches,'Review newly canonical tail/pair relation before publishing'

freshness={'task_id':TID,'actor':'Boss6','request_id':task['request_id'],
 'task_ref':ref(taskpath),'definition_pin':pin(task['definition']),
 'input_pins':ready['input_pins'],'all_current_object_pins_match':True,
 'all_consumed_source_refs_current':list(refs.values()),
 'registry_snapshot':ref('research/registry.json'),
 'canonical_scan':{'edge_files':len(registry['edge_files']),
    'scope':'canonical endpoint metadata for exact core and PAIR; no mathematical review of unrelated edges',
    'matching':canonical_matches,'duplicate_whole_relation_found':False},
 'remote_scope':'Current shared local clone after Root pushed claim/read-add; no worker remote/Git command. Root must confirm ownership and current published versions at serial installation.',
 'prior_plan_scope':'round46 review/plan and Root proof review read as prior orientation only; no coverage inherited',
 'checked_utc':datetime.now(timezone.utc).isoformat()}
save(P/'source-freshness.json',freshness)

ledger={'schema':1,'task_id':TID,'actor':'Boss6','request_id':task['request_id'],
 'definition_pin':pin(task['definition']),'core_ids':[CORE],
 'read_object_ids':task['definition']['read_object_ids'],
 'complete_body_readings':[dict(ref(path),read_level='complete body including full model, quantified statement and bearing proof; historical run claims remain historical') for path in bodypaths],
 'complete_static_code_readings':[dict(ref(path),read_level='complete static code reading; not imported or executed') for path in codepaths],
 'structured_native_readings':[
   dict(r,read_level='complete schema/family lossless structural consumption; exact all-field and array-value decode; mathematical certificate reused rather than recalculated') for r in native_refs],
 'mature_audits_readings':[dict(r,read_level='all fields/records structurally consumed; exact input contract read and reused with its original mathematical scope') for r in audit_refs],
 'original_reading_passes':{'all_24_declared_passes_disposed':True,
   'large_file_method':'one complete lossless family representation spans all original contiguous matrix passes without trimming fields or arrays; all 18 declared refs accounted for',
   'exact_declared_refs':[{'path':r['path'],'sha256':r['sha256']} for r in task['definition']['context_plan']['reading_refs']]},
 'new_work':{'scientific_runs':0,'LP_calls':0,'row_coefficient_generations':0,'matrix_generations':0,
   'BR_enumerations':0,'full_history_or_BI_searches':0,
   'structure_program':'consume_structure.py: each native decimal/record consumed, exact family encode/decode and both matrices native byte round-trip',
   'proof_work':'self-contained(h,sigma,t)common-customer realization with rational cuts and simultaneous integerization; two-layer specialization with disjoint child assembly; m6,j5 repair application and whole-statement audit'},
 'reuse_contracts':[
   {'contract':'fixed-directory payoff and welfare correctness','inputs':native_refs[:4],
    'paid_by':'mature independent 1590-type reconstruction reports and source proofs; all 48828 payoff and24336 welfare scalar equalities are inherited exact certificates, not new worker checks'},
   {'contract':'all realizable two-player tails and common welfare','paid_by':'parent original report + field-audit + CAEXACT two-layer proof; complete E classification inherited, not recomputed'},
   {'contract':'127 last BR ties and unique A6 maximizing fifth payoff','paid_by':'author original19 fields plus replay/field-audit and all156 BR rows; later exact finite audit supplies unique maximum, not author six-query list alone'},
   {'contract':'PAIR chosen10344 finite rows at changed Z','paid_by':'original run-report and all-row-slacks at SHA090586/fixed masterd1aeba; independent5236 added-row audit stays a separate event'},
   {'contract':'heterogeneous compiler','paid_by':'full analytic proof including arbitrary marked positions, all-coordinate permanent first exit, D0 and exact OPT pairing; no old bank/product finite run re-executed'},
 ],
 'coverage_limits':['no new old5108/10344 revalidation','no root SPE prefix reachability','no general six-player half','no claim that all repairers cost at least2R+D','no 18-label to156-catalog transfer']}
save(P/'reading-ledger.json',ledger)

evidence_paths=[str(P/'review.md'),
 objects['CAG-MODEL']['body']['path'],objects[EXACT]['body']['path'],objects[REPAIR]['body']['path'],objects[PAIR]['body']['path'],
 'archives/customer-attraction/state/程序/完整156主题的阈值物化收益矩生成器--程序.md',
 'archives/customer-attraction/state/计算/完整156主题固定前缀的收益矩数据--计算.md',
 'archives/customer-attraction/state/计算/完整156主题固定前缀的福利矩数据--计算.md',
 *[r['path'] for r in native_refs[:4]],
 E+'full156-tail-parent-report/original/audit_full156_reply_set.json',E+'full156-tail-parent-report/field-audit.json',
 E+'full156-author-tail-report/original/full156_tail2_exact_audit.json',E+'full156-author-tail-report/replay/field-audit.json',
 E+'full156-author-tail-report/replay/all-156-BR-rows.json',E+'full156-tail-minimum-author-summary/original/full156_tail2_min_welfare.json',
 E+'full156-payoff-kernel-data/independent-report.json',E+'full156-welfare-kernel-data/welfare-audit.json',
 E+'full156-kernel-generator/input-contract.json']
edge={'edge_id':EID,'kind':'implies','status':'accepted',
 'source_ids':[EXACT,REPAIR],'target_ids':[CORE],'premises_mode':'all','relation_mode':'unconditional',
 'conditions':'精确固定combined SHA d1aeba67e20c8d8fc7ff38cd6566ac05c3771731f586584e5c6f1dfe233472a8和PAIR SHA090586fb86af4e80b33eb24893d72fa2d240d156d639bcb97a9f8b413eddb2d2的同一156主题阈值目录；固定有序A1至A4；所有156合法动作/重复选择/末位BR平局均保；数值使用同输入SHA的成熟完整收益、福利和BR证书。U/W/M/delta/g均在总质量1规范化坐标，真正单位客户实例统一乘lambda=S，OPT6=S而规范化OPT6=1，福利比及3delta5>g同号。m=6,j=5仅保A6真一人尾，全部所需条件已在本固定输入支付。',
 'roles':{
  EXACT:'把全部完整有序历史终局递推专化到两层，给b∈BR(a)且U[a,b]>=M、其中ell_c=min_(d∈BR(c))U[c,d],M=max_c ell_c的充要判据及逐孩子独立拼接。',
  REPAIR:'给目标真尾的异质固定Cartesian修复、全坐标永久退出及O′−2W′=O−2W−(2R+D)精确合同；支持指定旧目标成本结论。',
  CORE:'得到当前固定156/四前缀statement的全部尾分类、六尾福利/门槛、A5全部末BR失败与指定异质预算障碍。'},
 'explanation':'PAIR准确输入经共同阈值、索引平均和整数复制定义该目录，成熟1590客户证书支付其冻结F/G/U及总福利矩；六T全覆盖给规范化OPT6=1，真实单位客户实例的绝对量统一乘lambda=S。CAEXACT只剩两层时必要性用每个偏离孩子的真实BR最低收益ell，充分性在目标孩子保b、其他有序孩子各取ell最小BR，故E={(a,b):b∈BR(a),U[a,b]>=M}。绑定同kernel876f063e...f3d4和welfarefe8fb09f...e5256的成熟父方全24336对合同给E恰六(Ci,Bi)，作者/后续字段合同给每Ci唯一Bi且同规范化M=8388012242736058520526600934763351/53803364904577948332973044339329080；六尾规范化Wc=6245548492134933268269408059574569/10760672980915589666594608867865816>1/2。A5后127末BR中A6给第五位唯一最高规范化u5=6451849825785555042805063797909779/53803364904577948332973044339329080<M，故全部平局都失败；这细项由后续field-audit而非作者六query列表独自承担。规范化delta5=M-u5=484040604237625869430384284213393/13450841226144487083243261084832270。修复须m6,j5，A6真末BR已核；j4要求旧(A5,A6)是真尾而不成立。R,D各>=delta5，2R+D>=3delta5；规范化3delta5−(1−2Wold)=1472779597825877298522675300355211/20176261839216730624864891627248405>0，统一整数化保持此符号，故此compiler修复后正坏差不能保留。独立PAIR可行/共同物化不冒作尾数值证明，精确有限证书及全层策略判据共同付全目标。',
 'whole_result':'在该唯一阈值物化156主题目录、固定有序A1至A4后，全部可实现完整两人纯SPE有序终局恰(Ci,Bi),i1至6；各Ci唯一Bi且给同M，六尾W/OPT6同为6245548492134933268269408059574569/10760672980915589666594608867865816>1/2。A5后的127末BR中A6给第五位收益唯一最大仍低于M，旧尾及A5全部平局均失败。真实delta5>0且3delta5>旧1−2Wold；m6,j5给定异质前缀修复的2R+D预算至少3delta5，已耗尽旧正坏差。以上精确覆盖目标当前完整statement。',
 'scope':'一个固定完整目录及四步前缀的全部两人尾，包含前缀总覆盖；逐终局各存在一份两层完整策略。指定compiler成本结论，不给六人根前四激励、一般half、所有修复器下界或其它目录/前缀排除。',
 'reviewed_by':'Boss6','review_note':'Fresh正式worker实读完整声明/承重证明及本包无损schema-family结构；父方尾全集、后续独立客户矩、作者细BR合同分别按原SHA/事件复用。新结构读取准确命名，scientific replay0。共同前提保一条ALL；完整数值/尾分类/修复合同均已付，选择whole_result。',
 'evidence':[ref(path) for path in evidence_paths]}
edge['explanation']='合法共同客户桥在本包自足支付：对每正hist h的六词多重集遍历全部720排列sigma，在每(h,sigma)上放0<=t<m_h、质量dt/720。A会员按actual位，T/B/C按排列后的词位；g=(f,1[i=j],w_i,w_j)，R_e=1[t<q_hg]；层s=[l,u)内Z_e=1[t-l<y_sg]。绑定原输入的成熟input-contract给0<=q<=m、无缝分层、真实R常位及0<=y<=u-l，所以所有156主题同时是同一空间的子集。固定h/sigma的RR交长min(qe,qf)、RZ交长sum r_ey_f、ZZ交长sum min(y_e,y_f)同时成立。按全部有限有理端点切开，乘共同正整数lambda=S后全为不同单位客户；零hist跳过，不除零。该桥只用固定输入数据，不调用必要图PASS或阈值对象的额外行保持/预算结论；成熟独立1590客户证书再支付此同目录的全部矩整数。 '+edge['explanation']
save(P/'full156-tail-and-repair-all.json',edge)

# Exact native binding calculation with a read-only overlay: new assets resolve
# to this staged tree, all original files to the unchanged clone.  Root later
# installs and rechecks against its serial publication tree.
sys.path.insert(0,str(BASE/'tools'))
import research_runtime as research
original_safe_path=research._safe_path
def readonly_overlay(root,name):
    validated=original_safe_path(BASE,name)
    candidate=ROOT/name
    return candidate if candidate.is_file() else validated
research._safe_path=readonly_overlay
binding=research.edge_bindings(BASE,edge,objects,verify=True)
edge.update(binding)
save(P/'full156-tail-and-repair-all.json',edge)
context={'edge_id':CEID,'kind':'sourced_from','status':'accepted',
 'source_ids':[COMBINED,PAIR],'target_ids':[CORE],'premises_mode':'all','relation_mode':'context',
 'conditions':'同一冻结combined d1aeba67e20c8d8fc7ff38cd6566ac05c3771731f586584e5c6f1dfe233472a8及PAIR090586fb86af4e80b33eb24893d72fa2d240d156d639bcb97a9f8b413eddb2d2；只记录固定数据与目录/矩的实际来源和实现用途。',
 'roles':{
  COMBINED:'提供全部hist质量、实际A会员、六比较索引词桶及R边缘q=x10+x11；K、旧Z及辅助overlap不原封进入新目录。',
  PAIR:'提供同一hist/R输入上的29层364条六字段y数据，是段内嵌套Z的确切输入；其所列10344行可行是有限必要域结果。',
  CORE:'接同一输入物化156标签、冻结收益/福利矩后的真实尾报告，给必要图路线可定位的固定四前缀策略完成障碍。'},
 'explanation':'combined当前hist块与PAIR当前hist_column连接，保全部组及原六字段。于共同(h,sigma,t)空间用A/TBC原位、R=[0,q)、每层Z=[l,l+y)定义6A+18TBC+66R+66Z；有限有理切分与共同正整数化给同一单位客户目录。kernel source_sha和pair_source_sha精确绑定这两输入，福利再绑定kernel；成熟1590类型证书分别重构全部收益及总覆盖。新Z可改旧Z/RZ边缘，不继承旧5108向量不变。该边记录固定数据、物化与矩的来源链以找到tail的真实尾障碍，不把5108/10344必要行PASS升级为全历史SPE，也不以PAIR有限可行性逻辑推出尾数值。核心whole逻辑支持仍由CAEXACT+repair与固定证据的另一条ALL承担。',
 'scope':'准确固定数据到该156目录/固定四前缀矩及尾报告的来源语境；不是implies/refutes，不关闭其它前缀、目录或一般half。',
 'reviewed_by':'Boss6','review_note':'两份原生JSON全字段及数组按schema/family无损消费，完整物化桥在review自足给出，来源SHA及两矩认证合同逐项匹配。只传数据与实现用途。',
 'evidence':[ref(path) for path in [str(P/'review.md'),objects[COMBINED]['body']['path'],objects[PAIR]['body']['path'],
  'archives/customer-attraction/state/程序/完整156主题的阈值物化收益矩生成器--程序.md',
  *[r['path'] for r in native_refs[:4]],E+'full156-kernel-generator/input-contract.json',
  E+'full156-payoff-kernel-data/independent-report.json',E+'full156-welfare-kernel-data/welfare-audit.json']]}
cbinding=research.edge_bindings(BASE,context,objects,verify=True)
context.update(cbinding)
save(P/'fixed-inputs-context.json',context)
relations=research.edges(BASE,{'edge_files':[str(P/'full156-tail-and-repair-all.json'),str(P/'fixed-inputs-context.json')]},objects,verify=True)
assert set(relations)=={EID,CEID}
save(P/'binding-preview.json',{'reviewed_edge_id':EID,'status':'read-only-native-binding-preview',
 'bindings':binding,'all_evidence_bytes_independently_checked':True,
 'native_edges_validation':'passed verified runtime edge schema and current endpoint/evidence binding using a read-only staged-file overlay',
 'publication_gate':'Root install then native edge-bind --write and edge-check; this preview does not mutate clone or register an edge'})
save(P/'context-binding-preview.json',{'reviewed_edge_id':CEID,'status':'read-only-native-binding-preview',
 'bindings':cbinding,'all_evidence_bytes_independently_checked':True,
 'native_edges_validation':'passed verified context schema, source/target pins and evidence hashes; no whole_result/contribution',
 'publication_gate':'Root install and native verified edge check; no clone mutation'})

assets_files=sorted([p for p in OUT.iterdir() if p.is_file() and p.name not in {'manifest.json'}])
manifest={'task_id':TID,'actor':'Boss6','definition_pin':ready['definition_pin'],
 'request_id':ready['request_id'],'formal_edge_file':str(P/'full156-tail-and-repair-all.json'),
 'context_edge_file':str(P/'fixed-inputs-context.json'),
 'reviewed_edge_id':EID,'files':[ref(p.relative_to(ROOT)) for p in assets_files],
 'canonical_reused':[],'hash_closure':'This manifest hashes neither itself nor receipt; receipt can hash manifest and all assets without a cycle.',
 'serial_publication_gate':'Install exact mirrored files; native bind/check formal edge; refresh changed edge/preview/manifest/receipt hashes only; checkpoint pushed then done.'}
save(P/'manifest.json',manifest)

receipt={'task_id':TID,'actor':'Boss6','request_id':ready['request_id'],
 'coverage':{CORE:{'state':'linked','object_pin':ready['input_pins'][CORE],
  'comparison_scope':'完整当前tail statement与PAIR固定输入实现、CAEXACT完整两层终局判据、M-b876异质修复全证明比较；完整core及18原reading refs、全部矩schema/family值、combined1905列、PAIR364六字段和10344原slack已结构消费，原精确数学合同按输入SHA复用。',
  'reason':'一条ALL边付清完整六尾分类/同M与Wc、A5全部127BR及A6唯一最高仍失败、m6j5真尾输入及2R+D>=3delta5>g。whole_result适合当前整条statement；原作者事件、后续客户/字段核验和本轮结构读取分开记录。数学重跑0；根前四激励/其它前缀/一般half/更廉修复在目标范围外未宣称已证。',
  'edge_ids':[EID]}},
 'assets':[ref(p.relative_to(ROOT)) for p in sorted(OUT.iterdir()) if p.is_file()],
 'closed_overlaps':[{'core_id':CORE,'peer_id':REPAIR,
  'reason':'该声明的follow-up已在本包完整解决：A6∈BR(A5)给m6,j5合法真一人尾，j4旧两尾不合法；真实delta5=M-u5>0，前五缺陷非负使R,D>=delta5，故2R+D>=3delta5>1−2Wold，固定异质compiler无法保正坏差。全坐标永久first-exit及精确W′/OPT′合同已全文核。并未把此局部成本障碍扩大为所有修复器不可能。'}],
 'follow_up_tasks':[],
 'scientific_runs':0,'source_freshness':ref(P/'source-freshness.json'),
 'reading_ledger':ref(P/'reading-ledger.json'),'mathematical_review':ref(P/'review.md')}
save(Path('map/receipts')/(TID+'.json'),receipt)
research.validate_coverage(receipt['coverage'],{CORE:objects[CORE]},relations)
research.validate_map_follow_ups(task['definition'],receipt,[],objects)
for asset in receipt['assets']:
    assert sha((ROOT/asset['path']).read_bytes())==asset['sha256']
print(json.dumps({'task_id':TID,'reviewed_edge_id':EID,'files':len(manifest['files'])+2,
 'receipt':ref(Path('map/receipts')/(TID+'.json')),'edge':ref(P/'full156-tail-and-repair-all.json'),
 'context_edge':ref(P/'fixed-inputs-context.json'),
 'source_freshness':ref(P/'source-freshness.json'),'all_current_pins_match':True,
 'native_verified_edge_coverage_followup_checks':'passed; read-only overlay; no clone mutation'},ensure_ascii=False,indent=2))
