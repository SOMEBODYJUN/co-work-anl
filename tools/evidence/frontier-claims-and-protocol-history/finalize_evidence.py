"""New read-only source/representation checks and exact semantic receipts."""
from pathlib import Path
import collections, hashlib, json, re

E=Path(__file__).resolve().parent
S=E.parents[2]
R=S.parent.parent/'boss4-research'
W=S/'cleanup/workspaces/Boss4/r3-frontier-claims-and-protocol-history-next'
W.mkdir(parents=True,exist_ok=True)

def read(p):
    return json.loads(p.read_text())

def save(p,obj):
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

sources=read(E/'source-manifest.json')
by_id={x['id']:x for x in sources}
targets=read(E/'resource-targets.json')
fm=read(E/'formal-manifest.json')
claims=(S/by_id['2f4a0833cc651ca428c8']['saved_path']).read_text()
g=read(E/'context/graph.json')
graph={x['id']:x for x in g['nodes']}
reviews={x['id']:x for x in read(E/'context/review_status.json')['entries']}
group_ids=['WC-R2-RESOURCE-POWER-BRIDGE','WC-R2-POWER-PATH-OBSTRUCTION','WC-R2-AFFINE-TWO-TYPE']
grouped=[{'source_lines':[218,223],'id':i,'graph':graph[i],'review':reviews[i],
          'scope':'three named records grouped under R2方法资产, not three additional headings; exact records previously fully read, no mathematical source additionally done'} for i in group_ids]
save(E/'grouped-identity-comparison.json',grouped)

texts={
'2f4a0833cc651ca428c8':(
 '完整230169字节/1325行语义实读，连续十段无截断；全部130标题、125个ID标题、R2合列三身份、开头和状态使用非命题段均读。只有精确已读catalog路径缩写，人类数学、量词、状态与未命中路径未压缩。',
 '与前批完整实读同SHA的graph/640五轴/assets比较；121精确标题身份和R2合列三ID分开，不强配WC-TARGET/3文献PaperFact。全文读当前源锐渐近、三载荷定理与独审、近次数、有限权类势和成果入口；复用同SHA全状态线性证明。候选/后续证明、历史OPEN与条件定理/软件有限域准确分开。',
 '六段完整原文进入自足资料，总合同保存新旧状态及精确用途；不回写冻结账本/他人页，不认证外部PaperFact，不额外done引用证明/PDF/程序。',
 targets['claim_topics']+[targets['contract']]),
'9c659b0d4af154f5ced0':(
 '完整main版本495字节AGENTS实读；Q-CAG-HALF、三个角色、main同步/工作保存/secret/旧save/个人区/board DM/远端确认及根入口兼容转发全部保留。',
 '逐字与legacy615字节版本及当前根AGENTS/OBJECTS比较；按sourceID/commit保存不同内容，旧任务/角色/main-only不覆盖当前六人焦点或清洗授权。',
 '历史协议双版本资料完整原文及差异；不作为新执行规则，不触发Git、消息、旧clone绑定或角色动作。',
 [targets['protocol'],targets['contract']]),
'721dd7ae776978716359':(
 '完整legacy版本615字节AGENTS实读；六人焦点/repository-cleanup、当前用户优先、绑定分支安全/清洗分支不得误推main、旧状态不改和兼容入口均保存。',
 '与main495字节/当前根规则比较；两同路径文件不同SHA分别存在，不按ref名字推先后，不以它改本轮执行指令。',
 '两个冻结版本各具source_refs与原文，独有任务迁移和分支条件完整进入资料；不执行原命令或额外done被引协作源。',
 [targets['protocol'],targets['contract']]),
'a7e5c41330e627f20df3':(
 '完整1191字节PROTOCOL实读；一般人数/一般目录限定与停止特殊人数、自由研究/异步研讨、独立身份、main与board分离、失败保ID/本地及远端确认、凭据和旧绑定均保全。',
 '旧停止特殊人数与当前六人任务直接不同；明确作为历史材料，与两AGENTS/当前根规则对照，不让其取消本轮任务。发送失败不是不可能性证明，数学状态与协作身份不混合。',
 '完整协议及准确适用时态进入独立资料，不因其写可私聊就发送消息，不因旧main约定操作共享分支。',
 [targets['protocol'],targets['contract']]),
'312e661a11ae212a2a28':(
 '完整795字节README实读；当前CAG入口/三个角色、tools成熟协作实现、旧路径转发、目录名不选择题目、旧shared绑定继续读WC资产而不自动改绑、旧角色历史定位全保存。',
 '与两AGENTS/PROTOCOL和当前六人清洗规则、已读WC成果入口对照；保留资产不等于恢复旧任务，链接不证明全部目标已读/已审。',
 '独有入口/旧绑定隔离含义进入协议资源；不执行工具、不取消息或探测绑定，当前数学和历史指令分开。',
 [targets['protocol'],targets['contract']])}
receipts=[{'id':i,'full_file_reviewed':True,'related_material_checked':True,
 'unique_content_accounted_for':True,'read_note':rn,'comparison_note':cn,
 'decision_note':dn,'disposition':'integrated','targets':ts} for i,(rn,cn,dn,ts) in texts.items()]
save(W/'semantic-receipts.json',receipts)

deps=[]
for folder in ['context','comparison']:
    for p in sorted((E/folder).rglob('*')):
        if not p.is_file():
            continue
        scope='context or same SHA prior complete semantic read reused; not new primary done'
        for row in read(E/'comparison-manifest.json'):
            if row['saved']==str(p.relative_to(S)):
                scope=row['scope']
        if p.name in ['graph.json','review_status.json','assets.json','catalog.json']:
            scope='same exact frozen content fully semantically read previous Boss4 batches; this batch exact identity/range comparison only'
        deps.append({'path':str(p.relative_to(S)),'bytes':p.stat().st_size,'sha256':sha(p),'actual_read_scope':scope})
save(E/'dependency-manifest.json',deps)
save(E/'reading-scope.json',{
 'claim_confirmed_by_root':'actualclaim pushed/synced7beb5b8db38ed4a6e04f7ac670c4b5e961f03e45',
 'primary_materialization':'after that confirmation only, SHA checked against inventory cache; two AGENTS keyed by ID not shared path',
 'claims_actual_ranges':[[1,110],[111,250],[251,390],[391,530],[531,670],[671,810],[811,950],[951,1090],[1091,1210],[1211,1325]],
 'claims_all_bytes':230169,'claims_all_lines':1325,'short_primary_full_ids':list(texts)[1:],
 'source_read_truncations':[],
 'exact_path_dedup':'Cn names exact previous2099 full catalog path; all primary labels and math retained. Canonical primary preserved once under sourceID, initial identical reading alias removed after equality check.',
 'actual_new_full_related_pages':['加权拥塞成果入口的模型与结论范围','平方对数加性缺口的全状态近次数下界','有限权类别三角排序势','非负多项式三载荷精确包络','三载荷包络的独立审查范围','两攻击源参数包络的锐渐近'],
 'actual_prior_full_read_reused':'全状态线性次数无均衡族 exact SHA equal current; graph/assets/review/catalog from preceding fully read batches',
 'not_read_by_link_inference':'all further cited papers, proofs, PDFs and program bodies not individually reread in this batch',
 'new_executions':'only new resource writer and independent exact byte/line/identity/format self-check; no old math suite',
 'new_external_paper_visual_or_interaction_pass':False})
save(E/'attempts-boundaries.json',{
 'preclaim':'Root reported atomic claim conflict on a different query source; no frontier primary/receipt written before successful claim. Related snapshots/read-only formal math comparison and reader prepared meanwhile.',
 'failed_or_cancelled_primary_reads':[],
 'truncated_navigation':'one rg --files directory listing truncated; used only to find related filenames, never counted as proof/primary reading',
 'source_alias':'initial exact duplicate CLAIMS reader alias deleted after equality; ID-keyed original unchanged; reader updated to canonical ID path',
 'not_run':['Git/claim/done/sync/checkpoint/authentication','old board/tools implementation','any previous successful mathematical suite','mapper or graph import','PDF/browser/render','network or literature search'],
 'new_math':'transparent conditional comparison of already-read finite-k potential and near-degree theorem only; no new finite experiment or external certification',
 'boundary':'all five source dispositions complete; linked mathematical source status retains its own review/ownership'})

candidates=read(E/'next-candidate-snapshot.json')
for x in candidates:
    x['reason']='same frozen WC frontier governance/compatibility family; Root must check latest global owner and atomically claim before primary writes'
save(W/'next-candidates.json',candidates)
(W/'relation-review.md').write_text('''# 本批关系自查\n\n这是五份旧账本/协作协议的资源性整理，不导入旧图、不认领mapper。125个ID标题与R2合列三ID分别定位；121个精确图/五轴标题对应不能被当成全源数学完成。3PaperFact和旧WC-TARGET不造近名映射。\n\n条件势的假设、全状态下界四项共同前提、near-degree的可变n统一条件、正向d上界和大规模构造分别说明。只保存已读数学关联供后续逐边解释，不为连通或入边造关系。两AGENTS/协议里的旧命令句是历史内容，不成为本轮操作或数学前提。\n''')

checks=[]
def check(name,ok):
    checks.append({'check':name,'passed':bool(ok)})
    if not ok:
        raise AssertionError(name)

inventory={z['id']:z for z in map(json.loads,(R/'cleanup/inventory.jsonl').read_text().splitlines())}
for x in sources:
    p=S/x['saved_path']
    check('primary exact byte/SHA '+x['id'],p.stat().st_size==x['size'] and sha(p)==x['sha256'])
    check('inventory exact identity '+x['id'],all(x[k]==inventory[x['id']][k] for k in ['path','size','sha256','blob','sources']))
for z in fm:
    p=S/z['path'];t=p.read_text()
    check('formal exact SHA '+z['path'],p.stat().st_size==z['bytes'] and sha(p)==z['sha256'])
    check('formal all forbidden C0 '+z['path'],not any(ord(c)<32 and c not in '\n\r\t' for c in t))
    check('formal trailing whitespace '+z['path'],all(l==l.rstrip() for l in t.splitlines()))
    meta=t.split('---\n',2)[1]
    check('formal flat MATEK '+z['path'],all(re.search('^'+k+':',meta,re.M) for k in ['id','kind','type_tag','title','status','summary','source_refs']))

restored={}
for path in targets['claim_topics']:
    t=(S/path).read_text()
    found=re.findall(r'## 完整冻结账本第 (\d+)–(\d+) 行\n\n```markdown\n(.*?)```',t,re.S)
    check('one complete source segment '+path,len(found)==1)
    lo,hi,block=found[0];lo,hi=int(lo),int(hi)
    check('segment byte exact '+str(lo),block==''.join(claims.splitlines(keepends=True)[lo-1:hi]))
    for i,line in enumerate(block.splitlines(keepends=True),lo):
        check('source full line '+str(i),i not in restored and line==claims.splitlines(keepends=True)[i-1]);restored[i]=line
check('all1325 source lines and exact230169 bytes',''.join(restored[i] for i in sorted(restored))==claims and len(claims.encode())==230169)
protocol=(S/targets['protocol']).read_text()
for ident in list(texts)[1:]:
    check('complete short original '+ident,('```markdown\n'+(S/by_id[ident]['saved_path']).read_text()+'```') in protocol)
check('two distinct AGENTS originals preserved',by_id['9c659b0d4af154f5ced0']['path']==by_id['721dd7ae776978716359']['path'] and by_id['9c659b0d4af154f5ced0']['sha256']!=by_id['721dd7ae776978716359']['sha256'])
headings=read(E/'heading-index.json')
check('all130 original headings',headings==[{'line':i,'heading':l} for i,l in enumerate(claims.splitlines(),1) if re.match(r'^#{2,3} ',l)] and len(headings)==130)
identities=read(E/'identity-comparison.json')
check('125 ID headings and121 exact correspondences',len(identities)==125 and sum(x['resolved_graph_id'] is not None for x in identities)==121)
for row in identities:
    if row['resolved_graph_id']:
        ident=row['resolved_graph_id']
        check('identity exact five-axis '+ident,row['review']==reviews[ident] and row['graph_kind']==graph[ident]['kind'])
for row in grouped:
    check('three grouped R2 identities '+row['id'],row['id'] in claims and row['graph']==graph[row['id']] and row['review']==reviews[row['id']])
check('two frozen candidates retained',{x['resolved_graph_id'] for x in identities if x['review'] and x['review']['current_proof']=='candidate'}=={'WC-R1-LF-SHARP','WC-R1-THREELOAD-ENVELOPE'})
for x in deps:
    check('real dependency byte/SHA '+x['path'],(S/x['path']).stat().st_size==x['bytes'] and sha(S/x['path'])==x['sha256'])
pr=read(E/'reading-progress.json')
check('actual primary whole-line read acknowledgment',pr['claims_lines']==list(range(1,1326)))
check('actual four short whole reads',set(pr['short_primary_full_ids'])==set(list(texts)[1:]))
check('five exact receipts',{x['id'] for x in receipts}==set(by_id) and len(receipts)==5)
for x in receipts:
    check('full semantic receipt '+x['id'],all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note']) and all((S/p).is_file() for p in x['targets']))
controls=collections.Counter(ord(c) for x in fm for c in (S/x['path']).read_text() if ord(c)<32)
out={'scope':'new exact original/whole-line disposition/identity and format checks only; no old suite or universal mathematics certification','passed':True,'checks':len(checks),'formal_forbidden_C0':0,'all_formal_C0_counts':dict(controls),'details':checks}
save(E/'self-check.json',out);save(W/'self-check.json',out)
(E/'README.md').write_text('''# Frontier账本与协议证据\n\n五主源均核inventory SHA。两同路径AGENTS按sourceID保存独立原件；CLAIMS230169B/1325行实际完整读取，六段资源逐行可无损回读。完整阅读范围、标题/身份对应、历史状态差异与真实相关证明快照各自归档。\n\n125个ID标题不是全部命题ID数：R2段另合列三身份。121精确标题对应与三个R2对应保全；两candidate只作冻结历史，后续完整证明/独审以实际快照说明，不改旧表。\n\n新self-check仅核字节、全部行去向、identity、receipt和C0/空白。没有Git/网络、旧套件、消息发送、绑定改写、PDF/视觉PASS或外部论文认证。依赖阅读范围见dependency-manifest，不能由链接推断其全部内容已经重读。\n''')
(W/'delivery.md').write_text('''# 五源完整交付\n\n8份独立资料保全部五源原文和数学/任务迁移含义；CLAIMS全1325行、所有候选/文献/条件及后续时态完整。两AGENTS不同ref与SHA不覆盖同名路径，不用历史指令改变当前执行。\n\n5semantic receipts已齐，Root应exact copy后实际checkpoint pushed再done。self-check是原字节/完整表示/身份/格式，不是数学证明程序。没有修改其他Owner正文、旧冻结源或共享导出。下一五候选均为当时本地无progress文件的inventory记录，待Root检查全局并正式claim。\n''')
print(json.dumps({'passed':True,'checks':len(checks),'formal_files':len(fm),'formal_bytes':sum(x['bytes'] for x in fm),'receipts':len(receipts),'forbidden_C0':0},ensure_ascii=False))
