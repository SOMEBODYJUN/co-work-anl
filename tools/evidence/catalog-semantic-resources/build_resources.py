"""New derivative resource writer; frozen sources and old generators are never modified/run."""
from pathlib import Path
import ast,collections,hashlib,json,posixpath
E=Path(__file__).resolve().parent;B=E.parents[2]
x=json.loads((E/'original/research/catalog.json').read_text());a=json.loads((E/'related/research/assets.json').read_text());bind=json.loads((E/'full-md-binding.json').read_text())
base=Path('archives/customer-attraction/state/资源');R=B/base;R.mkdir(parents=True,exist_ok=True)
labels={'customer_attraction':'顺序客户吸引','unrelated_machines':'不相关并行机','weighted_congestion':'加权拥塞','positive_kernels':'正占用核','shared':'共同目录双设施','heterogeneous':'异构目录双设施','local_and_exact':'局部与精确算法','multi_facility':'多设施','foundation':'公共基础','facility_review':'设施审查','customer_attraction_review':'客户吸引审查','publication':'投稿判断'}
files={k:v+'旧目录的逐项用途--资源.md' for k,v in labels.items()};main='旧研究总目录的字段语义与版本边界--资源.md'
commits=['68fad804ec5946cb296f77dc5b336308a66abf12','aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c']
refs=['source:'+c+':research/'+p for c in commits for p in ['catalog.json','CATALOG.md']]
roles=bind['role_labels'];pt=bind['package_label_dictionary'];pi={r['path']:i for i,r in enumerate(x['entries'])};purposes=list(dict.fromkeys(r['purpose'] for r in x['entries']));pm={q:i for i,q in enumerate(purposes)};claims={}
for z in a['entries']:
 for k in ['proof','tests','records','examples','reviews','candidates','sources','implementation']:
  for p in z.get(k,[]):claims.setdefault(p,set()).update(z['claims'])
def dump(p,o):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
def cell(s):return str(s).replace('|',r'\|').replace('\n','<br>')
def fm(id,title,summary):return '\n'.join(['---','id: '+id,'kind: resource','type_tag: 资源','title: '+json.dumps(title,ensure_ascii=False),'status: historical-resource-semantically-integrated','summary: '+json.dumps(summary,ensure_ascii=False),'source_refs:']+['  - '+json.dumps(q,ensure_ascii=False) for q in refs]+['---',''])
records=[]
for i,r in enumerate(x['entries']):
 cs=sorted(claims.get(r['path'],[]));state=roles[r['role']]
 if cs:state+='；关联 '+'、'.join('`'+z+'`' for z in cs[:3])+'；命题合同'+('（共 '+str(len(cs))+' 项）' if len(cs)>3 else '')
 elif r['role'] in {'account','obstruction','counterexample'}:state+='；精确范围见本页正文'
 records.append({'original_index':i,'source_record':r,'target':str(base/files[r['topic']]),'purpose_id':'P'+str(pm[r['purpose']]),'md_display_claims':cs[:3],'md_claim_total':len(cs),'md_display_state_semantics':state,'related_paths_indices':[pi[p] for p in r.get('related_paths',[])],'related_indices':[pi[p] for p in r.get('related',[])]})
dump(E/'catalog-semantic-records.json',records)
intro={
'customer_attraction':'这是单位客户、共同主题目录、完整有序历史纯SPE及其静态/动态工具的旧文件用途索引。五人与六人、静态Nash与动态SPE、给定背景与零根背景必须分开。原索引第60/100条的“当前较强”“仍开放”需按总资源的实际正式正文校正；原文字逐字保留。',
'unrelated_machines':'这是一般不相关并行机与大量受限结构、归约、矩证书和修复接口的旧用途索引。给定LP/矩/目标的输出接口、产生这些证书的一般算法、数学位复杂度和已交付软件各是不同义务。三半/十三八等受限结构界、固定层间隙、局部能垒和条件hardness均不自动解决一般UM-TARGET。第794/795条的UM默认路由已与同冻结来源的schema2实际配置不符。',
'weighted_congestion':'这是加权原子拥塞的旧用途索引。真实全状态无近似PNE、仅有改善环、指定selector/clock架构障碍、局部势存在界和有限审计分别保留。原目录同时包含奇环拓扑、线性全状态下界和后续结构方法；“全类OPEN”须回到精确命题，而不能拿某个旧标签覆盖后续相反结果。此页未重新证明全部下界或认证论文优先权。',
'positive_kernels':'这是正占用核的函数、锥、闭包、秩及禁支撑质量资源索引。其非负表示工具可独立于博弈使用；目录角色和与拥塞的启发不构成一般均衡桥。',
'shared':'这是共同目录双设施的旧用途索引。设施分配的同时均衡与顺序客户吸引完整SPE是不同模型；目录共同存放不产生跨模型推论。',
'heterogeneous':'这是异构目录双设施的旧用途索引。各提供者允许集合、权、目标与复杂度依具体精确正文，不从共同目录结果直接升级。',
'local_and_exact':'这是局部均衡、弦条件、参数化和精确算法的旧用途索引。有限局部稳定、一般均衡、算法实际输入及多项式位复杂度分别核对。',
'multi_facility':'这是任意设施数、连续/整数cap、冻结超载、盒构造及复杂度的旧用途索引。子集Nash化保持极大不增/极小不减的独立RANGE引理，并不交付一般逐坐标盒求解器或canonical实现；候选与原OPEN范围保留。',
'foundation':'这是模型定义、精确命题、来源与研究入口的旧用途索引。共同名词不替代模型；旧根目标/清洗/图要求不能覆盖现行恰六人与三阶段规则。',
'facility_review':'这是设施模型的旧审查文件用途索引。独立性、审查版本、实际输入与已执行范围要回到审查原件，不由目录role=review授予全稿或外审认证。',
'customer_attraction_review':'这是客户吸引的旧审查用途索引。只审陈述先行重构、读后攻击、最终指定章节、有限实现及当时缺件等事实按原级别保存，不能借共页或新标签追认。',
'publication':'这是历史投稿判断、选刊与交接用途索引。作者当时的期刊范围、定位、篇幅及优先权看法作为历史判断，不能当成当前门户规则、已外审或数学证明。'}
for topic,label in labels.items():
 rs=[z for z in records if z['source_record']['topic']==topic];ps=list(dict.fromkeys(z['source_record']['purpose'] for z in rs));usedroles=list(dict.fromkeys(z['source_record']['role'] for z in rs))
 lines=[fm('catalog-'+topic.replace('_','-')+'-semantic-resource',label+'旧目录的逐项用途','完整保存本主题'+str(len(rs))+'条人类名称、用途与角色；精确重复用途去重，原关联与导出状态不提升数学真值。'),'# '+label+'旧目录的逐项用途','',intro[topic],'',f'本页处置原目录的 {len(rs)} 条记录，不处置这些路径所指源文件的全部数学。记录编号是原 JSON 的零起始 `entries[index]`。完整字段原文、字段是否存在、原路径及两种关联键见[逐项绑定数据](../../../../tools/evidence/catalog-semantic-resources/catalog-semantic-records.json)；[总合同与当前校正]('+main+')解释版本、字节和证据层级。','', '## 角色解释','', '| 原 role | 原 Markdown 角色含义 |','| --- | --- |']
 lines += ['| `'+k+'` | '+cell(roles[k])+' |' for k in usedroles]
 lines += ['', '## 完整用途字典','', '相同用途仅在字符串逐字相等时合并；每个记录仍单独保留名称、路径、角色、包和关联。用途中的“已证明”“独立”“实际运行”“未取得”“OPEN”等是目录作者的版本化描述，不是本次对该目标的独立认证。','', '| 用途 ID | 完整原文 |','| --- | --- |']
 lines += ['| P'+str(pm[q])+' | '+cell(q)+' |' for q in ps]
 lines += ['', '## 全部记录去向','', '以下每行包含原索引、人类名称、原路径、role、可选package和用途ID；`∅`表示原字段缺席。package保原值，其旧导出显示名由总合同的字典给出。','', '| index | 完整中文名称 | 原路径 | role | package | 用途 |','| --- | --- | --- | --- | --- | --- |']
 for z in rs:
  r=z['source_record'];lines.append('| '+str(z['original_index'])+' | '+cell(r['title'])+' | `'+cell(r['path'])+'` | `'+r['role']+'` | '+cell(r.get('package','∅'))+' | '+z['purpose_id']+' |')
 lines += ['', '## 原导出状态与关联','', 'Claim列只保旧 Markdown 实际显示的前三个按字典序 ID 与总数；它们来自资产包8角色路径的聚合，不能解释成该文件证明全部Claim。`related_paths`会成为“配套”链接，`related`是另一个未被旧生成器读取的键。编号精确引用原JSON，不是已接受数学边。缺席与空数组在逐项绑定数据中保持不同。','', '| index | 实际可见Claim ID | 聚合总数 | related_paths | related |','| --- | --- | --- | --- | --- |']
 for z in rs:
  r=z['source_record'];rel=lambda key,ind: ', '.join('#'+str(j) for j in ind) if key in r and ind else ('[]' if key in r else '∅')
  lines.append('| '+str(z['original_index'])+' | '+('、'.join('`'+q+'`' for q in z['md_display_claims']) or '无')+' | '+str(z['md_claim_total'])+' | '+rel('related_paths',z['related_paths_indices'])+' | '+rel('related',z['related_indices'])+' |')
 lines += ['', '## 复用边界','', '本资源保完整名称/用途/角色/版本路由，已做逐项语义阅读与全Markdown表示绑定；未执行被链审计、未读取所有2099目标证明、未签署历史独立性或外审。后续按具体Claim读取真实模型、正文、审查版本及软件合同。此页为资源对象，不为所有目录链接生成推导边；关系审查见总合同。','']
 (R/files[topic]).write_text('\n'.join(lines))
# Hidden-field mechanism: explicit schema key checks and a concrete same-source record.
related=[{'index':i,'path':r['path'],'related':r['related'],'related_paths_present':'related_paths' in r} for i,r in enumerate(x['entries']) if 'related' in r]
dump(E/'hidden-related-fields.json',{'records':related,'nonempty':sum(bool(r['related']) for r in x['entries'] if 'related' in r),'validation_reads':'row.get(related_paths,[]) only; build_catalog.py125','renderer_reads':'row.get(related_paths,[]) only; build_catalog.py163','minimal_reproduction':{'index':779,'source_has_related':[779,780,783],'old_md_has_no_added_companion_from_this_key':True},'scope':'schema and visible export omission, not missing mathematical dependency proof; both empty and nonempty raw fields retained'})
dump(E/'topic-destinations.json',[{'topic':k,'count':sum(r['topic']==k for r in x['entries']),'target':str(base/files[k])} for k in labels])
dump(E/'purpose-dictionary.json',[{'id':'P'+str(i),'text':q} for i,q in enumerate(purposes)])
print(json.dumps({'pages':12,'records':len(records),'unique_purposes':len(purposes),'resource_bytes':sum((R/q).stat().st_size for q in files.values()),'B':str(B)},ensure_ascii=False))
