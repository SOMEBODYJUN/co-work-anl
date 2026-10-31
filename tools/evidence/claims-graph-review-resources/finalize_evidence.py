"""New batch evidence, receipts and independent representation self-check.

Only reads frozen inputs and this independent staging tree. No Git/network,
legacy builder execution, shared output mutation or mathematical suite.
"""
from pathlib import Path
import ast, collections, hashlib, json, re

E = Path(__file__).resolve().parent
S = E.parents[2]
R = S.parent.parent / 'boss4-research'
W = S / 'cleanup/workspaces/Boss4/r3-claims-graph-review-resources-next'

def read(p):
    return json.loads(p.read_text())

def save(p, obj):
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

sources = read(E/'source-manifest.json')
fm = read(E/'formal-manifest.json')
targets = read(E/'resource-targets.json')
g = read(E/'original/research/graph.json')
claims = (E/'original/research/current/claims.md').read_text()
progress = read(E/'reading-progress.json')

notes = [
('8cebb6932c909f78d976',
 '完整385407字节、1535行实际逐段语义读取；632个规则前数据行覆盖640不同身份，规则后第1535行另有完整incidence-LP解析候选；全部非表格段落和逻辑规则已读。未读尾部未被640计数代替。',
 '与完整旧graph/review/assets的身份、实际build_map声明截取范围以及五人/四人/iid/WC和单交叠、极大花瓣正式证明比较。保人数/单位客户/真有序历史/背景收益、条件、有限实现和外审时态，发现末行未进入旧declared集合。',
 '四个模型资源无损保全部原行及来源；独立总合同保存过时时态和尾部候选漏登记。候选仍候选，不把全部所引证明额外done或自动认证。',
 list(targets['claims'].values())+[targets['contract']]),
('8ed5860d6389f1b02cb0',
 '完整1794179字节顶层元数据、1153节点与1353超边逐字段语义实读；含所有共同前提、statement/refs/status及仅2条额外detail。精确重复字符串仅复用已实际全文读过的同值catalog/assets/review/claims；新U字符串首见完整输出。两次截断均补读，现无未读对象。',
 '逐关系比较原声明、review五轴、实际条件证明、当前AGENTS/OBJECTS/map规则及HTML消费者。旧attacks有不满足应用前提而非推翻条件定理，checks不代全称证明；旧OPEN与同版后续完整结果的时态纠正另记。',
 '九track自足资源完整保全2506对象的全部字段、角色及来源，顶层legend完整另存；本批不导入map、不认领mapper、不延续旧强制连通/入边规则。未额外done1420种refs。',
 list(targets['tracks'].values())+[targets['contract']]),
('cf043baed7c94e8b9d9c',
 '完整1530181字节HTML语义读取：全部实际外壳8972字节/CSS/JS，1521223字节graph payload通过全对象结构相等绑定到已全部字段实读的图；整HTML独立静态字节替换相等，不是只读DOM摘要。',
 '与实际build_map字面HTML模板及完整graph逐对象比较，明确legend/2edge.detail未显示、search不含node.detail/refs/status、清除保其它过滤与旧检查栏；无外部视觉资源或字体语义资产。未运行旧builder或浏览器。',
 '完整原件与全部shell保留，数据语义在九track完整记录，独立HTML资源说明实际消费与未显示范围。静态表示PASS不声称浏览器/交互/公式渲染或数学证明PASS。',
 [targets['html'],*targets['tracks'].values(),targets['contract']]),
('60a1e44478763577c7a6',
 '全文1244字节审查README实读，全部模型表、cleaner/Boss/editor角色、实际版本覆盖/未覆盖要求及票数不代数学证明均保全。',
 '与当前六人AGENTS、平坦MATEK对象规则和640五轴ledger比较；旧任意m active任务为历史，不作为本轮工作或数学前提。旧审查不自动失效，也不自动跨模型移用。',
 '独立审查/模板资源保全部原文及可复用审查合同；内审/外审/实现和候选分别说明，不发送外部消息或新增审查认证。',
 [targets['review_template'],targets['contract']]),
('b88083a7e4a324b4defa',
 '全文1371字节template实读，精确输入、上下界量词、合取假设、推导缺口、位复杂度、构造/最优/达到区分、代码/输入/证书/冻结结果及新材料溯源全部保存。Root实际clean show导出的同SHA原件已核。',
 '与当前OBJECTS/模板格式、CAG完整历史模型和旧审查协议比较，设施示例字段不强套CAG，程序/历史/审查状态不作数学前提。',
 '完整原文和现行适配边界进入独立资源；保原模板，不将写作合同当定理，不把未实现canonical后端写成已交付。',
 [targets['review_template'],targets['contract']]),
]
receipts = [{'id':i,'full_file_reviewed':True,'related_material_checked':True,
             'unique_content_accounted_for':True,'read_note':rn,'comparison_note':cn,
             'decision_note':dn,'disposition':'integrated','targets':ts}
            for i,rn,cn,dn,ts in notes]
save(W/'semantic-receipts.json',receipts)

dep = []
for dirname in ['related','comparison']:
    for p in sorted((E/dirname).rglob('*')):
        if not p.is_file():
            continue
        rel = str(p.relative_to(S))
        scope = 'complete prior full read reused by exact SHA; this batch no additional source done'
        if dirname == 'comparison':
            for row in read(E/'comparison-manifest.json'):
                if row['path'] == rel:
                    scope = row['read_scope']
        dep.append({'path':rel,'bytes':p.stat().st_size,'sha256':sha(p),'read_scope':scope})
save(E/'dependency-manifest.json',dep)

save(E/'reading-scope.json',{
 'primary':sources,
 'actual_read':{'claims_lines':[1,1535],'graph_nodes_indices':[0,1152],
                'graph_hyperedges_indices':[0,1352],'graph_all_top_level_fields':True,
                'review_README_complete':True,'claim_template_complete':True,
                'actual_HTML_shell_complete':True,'HTML_payload_complete_via_exact_whole_graph_binding':True},
 'exact_dedup_sources':[
   {'path':z['path'],'sha256':z['sha256'],'scope':z['read_scope']}
   for z in dep if '/related/research/' in z['path'] and Path(z['path']).name in ['catalog.json','assets.json','review_status.json']],
 'dictionary':'graph-string-dictionary.json contains exact original string -> C/CT/A/V/L/U code; L positions refer to whole fully read claims; only exact repeats omitted from subsequent tool output',
 'source_objects_not_automatically_reviewed':'1420 distinct graph refs; primary semantic graph read does not reread or mark done all linked mathematical sources',
 'new_external_paper_reads':[],'new_browser_visual_interaction_runs':[],
 'related_new_read_scope':'two complete local formal pages (rho, disjoint maxima); greedy-unopened independent section354–395 only; other five formal math snapshots fully read previous batch and current SHA equal',
 'truncated_primary_views_repaired':[
   'graph nodes0–89 first outer2500 truncation: not acknowledged; reread0–44 and45–99 fully',
   'graph nodes200–299 middle output truncation:200–263 actual safe,264–299 reread complete'],
 'claim_first_block':'lines1–90 were read directly before compact views; no separate saved view existed initially; original primary preserves exact bytes',
 'status':'all five primary semantic scopes complete; tests do not prove this human reading statement'
})
save(E/'attempts-boundaries.json',{
 'operations':'read/copy/SHA and new resource/static representation checks only',
 'git_network_operations_by_this_batch':[],
 'template_export':'Root reported actual clean show to exact original/research/templates/claim.md;1371B/SHA2007b99d656cfbb2d83830af7e6870eaa4b4f4e9d834cb89241475f90035ba78 checked',
 'corrected_preparation_failures':[
  'claims compact-view initial sibling Path(.) lookup FileNotFoundError corrected by resolve; no source modification',
  'graph summary sibling lookup with relative E FileNotFoundError corrected by resolve; no source modification',
  'optional related self-check path absent in an rg query; used actual existing comparison evidence instead'],
 'output_boundaries':'Two primary node-view output truncations explicitly repaired; later diagnostic dumps of prior selfcheck/progress listing were truncated and are not primary read evidence.',
 'not_run':['legacy build_map.validate/main','build_crosswalk/main','check_assets chain','any old mathematical suite','browser/PDF/render/interaction'],
 'not_retried':'previous canceled141 Git object verification not retried; no lazy fetch here',
 'new_checks':['read-only full HTML static byte binding once','lossless formal record/line roundtrip and exact source/format/receipt checks'],
 'math_scope':'author historical statements preserved; targeted written-proof comparison only; no universal proof certification by structural tests'
})

inventory = {x['id']:x for x in map(json.loads,(R/'cleanup/inventory.jsonl').read_text().splitlines())}
candidate_ids=['2f4a0833cc651ca428c8','9c659b0d4af154f5ced0','721dd7ae776978716359','a7e5c41330e627f20df3','312e661a11ae212a2a28']
candidates=[]
for ident in candidate_ids:
    z=inventory[ident]
    candidates.append({k:z[k] for k in ['id','path','size','sha256','sources']} | {
      'local_progress_file_exists':(R/'cleanup/progress'/(ident+'.json')).exists(),
      'reason':'same WC frontier root governance/claim ledger family; both AGENTS versions distinguished; available local snapshot only, Root must verify and claim atomically before primary writes'})
save(W/'next-candidates.json',candidates)

(W/'relation-review.md').write_text('''# 本批关系自查\n\n五源属于旧命题/图/HTML/审查模板资源。完整原节点、共同前提及各类关系按九track保全；不是新数学图，不认领mapper，也不导入旧图。旧attacks可限制应用前提而非反驳条件定理，checks不提供全称证明，implements方向不统一，limits可仅为review/document边界。641/18/318/16/360仅为旧类型计数，不能替代逐边语义。\n\n当前AGENTS不强制连通或claim入边，旧validate的两个gate不沿用。完整数学相关性和精确例子见独立总合同；引用来源没有额外done。当前六人CAG主问题不因历史任意m/UM/WC任务字段改变。\n''')

checks=[]
def check(name, ok):
    checks.append({'check':name,'passed':bool(ok)})
    if not ok:
        raise AssertionError(name)

for x in sources:
    p=S/x['saved_path'];inv=inventory[x['id']]
    check('primary byte/SHA '+x['id'],p.stat().st_size==x['size'] and sha(p)==x['sha256'])
    check('inventory identity '+x['id'],all(inv[k]==x[k] for k in ['path','size','sha256','blob','sources']))

for x in fm:
    p=S/x['path'];s=p.read_text()
    check('formal exact hash '+x['path'],p.stat().st_size==x['bytes'] and sha(p)==x['sha256'])
    check('formal forbidden C0 '+x['path'],not any(ord(c)<32 and c not in '\n\t\r' for c in s))
    check('formal trailing whitespace '+x['path'],all(l.rstrip()==l for l in s.splitlines()))
    meta=s.split('---\n',2)[1]
    check('formal flat MATEK '+x['path'],all(re.search('^'+k+':',meta,re.M) for k in ['id','kind','type_tag','title','status','summary','source_refs']))

rebuilt={'nodes':{},'hyperedges':{}}
for track,path in targets['tracks'].items():
    blocks=re.findall(r'```json\n(.*?)\n```',(S/path).read_text(),re.S)
    check('track two complete arrays '+track,len(blocks)==2)
    for group,block in zip(['nodes','hyperedges'],blocks):
        for x in json.loads(block):
            i=x['source_index'];obj=x['record']
            check(group+' complete fields '+str(i),obj==g[group][i] and i not in rebuilt[group])
            rebuilt[group][i]=obj
for group in rebuilt:
    check('complete graph '+group,[rebuilt[group][i] for i in sorted(rebuilt[group])]==g[group])
metadata=json.loads(re.findall(r'```json\n(.*?)\n```',(S/targets['contract']).read_text(),re.S)[0])
check('complete graph metadata',metadata=={k:v for k,v in g.items() if k not in ['nodes','hyperedges']})

restored={}
for tag,path in targets['claims'].items():
    text=(S/path).read_text()
    parts=re.findall(r'## 原登记第 (\d+)–(\d+) 行\n\n```markdown\n(.*?)```',text,re.S)
    for lo,hi,block in parts:
        lo,hi=int(lo),int(hi)
        expected=''.join(claims.splitlines(keepends=True)[lo-1:hi])
        check('claim segment exact '+str(lo)+'-'+str(hi),block==expected)
        for i,line in enumerate(block.splitlines(keepends=True),lo):
            check('claim line preserved '+str(i),i not in restored and line==claims.splitlines(keepends=True)[i-1])
            restored[i]=line
check('entire claims byte-for-byte',''.join(restored[i] for i in sorted(restored))==claims)
check('640 pre-rule identities and one tail candidate',len({i for z in read(E/'claim-row-index.json') if z['old_registration_included'] for i in z['ids']})==640 and read(E/'claim-row-index.json')[-1]['ids']==['CA-INCIDENCE-LP-DYNAMIC-BUDGET-v1'])

rt=(S/targets['review_template']).read_text()
for p in ['research/reviews/README.md','research/templates/claim.md']:
    check('complete short primary preserved '+p,('```markdown\n'+(E/'original'/p).read_text()+'```') in rt)
html=(E/'original/research/index.html').read_text()
m=re.search(r'(<script id="graph-data" type="application/json">)(.*?)(</script>)',html,re.S)
check('HTML actual complete JSON payload equals graph',bool(m) and json.loads(m.group(2))==g)
shell=html[:m.start(2)]+'__GRAPH_DATA__'+html[m.end(2):]
check('HTML actual complete shell preserved',shell==(E/'html-shell.html').read_text() and '```html\n'+shell+'```' in (S/targets['html']).read_text())
check('prior new static binding actualPASS',all(read(E/'html-static-binding.json')[k] for k in ['html_payload_equals_whole_graph','complete_shell_equals_literal_builder','complete_html_equals_exact_static_substitution']))
check('only two extra edge details',[e['id'] for e in g['hyperedges'] if 'detail' in e]==['E-UM-COMMON-SIZE-UNKNOWN-B-EXACT-v1','E-UM-UNKNOWN-TARGET-PARTITION-SEARCH-OBSTRUCTION-v1'])
for k,n in [('claims_read_lines',1535),('graph_nodes_read_indices',1153),('graph_edges_read_indices',1353)]:
    check('actual acknowledged complete range '+k,progress[k]==list(range(1,n+1)) if k=='claims_read_lines' else progress[k]==list(range(n)))
check('actual all primary booleans',all(progress[k] for k in ['reviewREADME_full','template_full','HTML_shell_full','graph_header_full','HTML_payload_full_via_exact_graph_binding']))
for z in dep:
    check('dependency exact snapshot '+z['path'],(S/z['path']).stat().st_size==z['bytes'] and sha(S/z['path'])==z['sha256'])
check('exact five source receipts',{x['id'] for x in receipts}=={x['id'] for x in sources} and len(receipts)==5)
for row in receipts:
    check('full semantic receipt '+row['id'],all(row[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note']) and all((S/p).is_file() for p in row['targets']))
controls=collections.Counter(ord(c) for z in fm for c in (S/z['path']).read_text() if ord(c)<32)
result={'scope':'new exact source/whole representation/semantic disposition and format only; no legacy suite or universal mathematical certification',
 'passed':True,'checks':len(checks),'formal_forbidden_C0':0,'all_formal_C0_codepoint_counts':dict(controls),'details':checks}
save(E/'self-check.json',result)
save(W/'self-check.json',result)
(E/'README.md').write_text('''# 命题、旧图、HTML与审查模板资源证据\n\n五主源原件完整保存，source-manifest绑定冻结inventory。graph/claims全文实读范围、精确字符串去重字典、全部对象去向与相关数学比较分别保存；不能把原作者状态或结构PASS当新数学认证。\n\n资源正文在formal-manifest的16个独立页，原graph2506对象及claims1535行均可无损回读。html-static-binding是一次新只读整表示检查，没有运行旧生成器。dependency-manifest逐文件说明真实读取/复用范围；尤其polytime_frontier只读独立greedy-unopened节，不声称重读其全部数学。\n\nself-check检查字节/表示/receipt/格式，明确C0扫描。没有Git、网络、旧数学suite、浏览器渲染或外审认证。attempts-boundaries保失败/截断补读；reading-scope解释如何实际全文阅读而非仅计数。\n''')
(W/'delivery.md').write_text('''# 五源语义交付\n\n五源已完整实读、相关比较、独有去向与自足资源完成；本地独立staging，无Git/claim/done。Root应按copy-files精确复制，先checkpoint实际pushed再done。\n\n16份资源保全全部1535行命题、1153节点/1353超边、HTML全部shell与整图payload、两份短协议。尾部incidence-LP候选在旧declared之外，仍candidate；旧OPEN、条件应用与实际证明/软件/显示范围另表。原件和其他Owner页不修改，不导入map。\n\n实际新self-check只认证字节、全字段/全文去向、五receipt及格式；没有旧suite或新视觉/交互PASS。下一五候选仅为本地无progress文件的inventory记录，Root核全局并claim确认后再开展主源。\n''')
print(json.dumps({'passed':True,'checks':len(checks),'formal_files':len(fm),'formal_bytes':sum(x['bytes'] for x in fm),'forbidden_C0':0,'receipts':5},ensure_ascii=False))
