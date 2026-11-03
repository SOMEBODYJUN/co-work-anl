from pathlib import Path
from collections import Counter
import json,hashlib
R=Path('/workspace/scratch/cd4305a146e6/co-work-anl-boss3');W=R/'cleanup/workspaces/Boss3/resume-20261102/c3';B=R/'archives/customer-attraction/tools/evidence/branch-geometry-source-resumed-boss3';M='archives/customer-attraction/state/';PFX='research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/branch_geometry/'
items=json.loads((B/'source-manifest.json').read_text());objects=json.loads((W/'object-index.json').read_text());targets={}
for rel,meta in objects.items():
 for p in meta['source_paths']:targets.setdefault(p,[]).append(M+rel)
old_review=M+'审查/交叉回复税与第二步D分支的独立七行排除--审查.md'
notes={
'audit_commuting_prefix.py':('2116B全码，share/lower、AB/AE两索引和、nonindexed_B、四λ折点/64旧原子有理加权及仅stdout输出。','与4190B同行完整证明、旧前缀接口和同计数门槛/收益不可交换边界比较；本次原样一次12有理检查均正。','保完整三族12折点实现与新2409B输出；未排旧点不是half支持或新版557/728结论。'),
'commuting_prefix_tool.md':('4190B全文：真三人节点/已知同负载双尾、任意λ端点下界、λ1恒等式、AB/AE/nonindexed应用和全λ折点逻辑。','与成熟两人税及交叉有序历史对称化/一般收费审查逐条件比较，转移F2上界而非原政策。','一般引理完整入正文，保p≥1/零项及整行λ限制；历史root重构不改称当前新增盲审。'),
'second_D_envelope.md':('5808B全文：真second→D三尾、七真行、任意非负权的逐客户八态max、δ=ε六态、固定点负证书、133/283前史。','C2固定七行独审已读/成功，本批比较其scope；新保一般M(z)族及max方向，不重跑旧D7。','独有普遍必要包络入新引理，固定权精确分离作为既有实例关系；不提升全型最优或SPE。'),
'separate_second_D.py':('2831B已在C2全文实读，本批按主源ID/冻结SHA核同并读入原依赖third_D_completion，理解七行、float找权/有理round及max。','与C2独审及新一般包络逐式同一数据；代码依赖NumPy/SciPy发现器，不冒独立std-only包。','本次正式主源保完整程序/依赖出处，数学资格复用C2七行独审，0本入口/peer重跑。'),
'separate_second_D.json':('2030B在C2全部字段已实读，本批SHA核同；七λ、64 maxima、numeric minimax、精确/近似projected slack及status均保。','与C2同字节及283行正最小最大违量相近但不同旧float值比较；λ和1.000001不需归一。','保精确固定点证书与一般包络的特例，不重授独审或精确LP最优。'),
 'third_D_completion.py':('7410B全文：第三位→D真双尾P/Q、旧真角色/索引/菜单全部133行、四角1024分型、质量守恒及自由ε minmax、输出83split。','与真两人税/旧索引模板及第二位D扩张逐角色比较，强制D不借最优性，ε值与solver optimal分清。','完整必要补全合同/133行族在正文展开；0LP重跑，必要行可行不构造SPE。'),
 'third_D_completion.json':('10826B全字段与83个atom/P/Q/ell/h/mass消费；14活动行、133/1024、negative epsilon/status/scope全保。','各split域/64原子归并核，最大float质量差3.608e−16仅账簿；与283行正epsilon和旧点其他真实排除对照。','保数值可行域及全83记录，不以负floatε授精确可行或完整SPE。'),
 'two_D_completion.py':('5679B全码：保旧P/Q/menu加新R/S/T、实际/旧索引反查、新角色全查询、背景三人两利润行、8192分型/ε及--source输入。','与133行、一般七行包络、成熟全背景三人5/3定理比较，283行活动七式与C2一致。','将真第二/第三位不同分支及自由ε LP完整说明，0原优化，正minmax不是求解器infeasible返回。'),
 'two_D_completion.json':('550B全七字段：历史source绝对路径、HiGHS Optimal、283行/8192、+0.013551301796009453/scope及七活动名。','对照源码加ε实际8193变量及C2精确排旧点；未读取日志中旧scratch路径。','保成功数值正违量诊断，不称solver无解，精确非延拓由既有有理七行承担。'),
 'second_D_rows.py':('4198B全文：extras零dummy后删第三D/menu/PQ行、131留下行+220重复三元、decomposition各case与raw常数/menu、120局部特征。','与two_D全部extras和908完整351行名逐族对应，真三人利润定理用于AD真三尾，非重排政策。','完整351行来源、过滤理由及尺度分解写程序，保共同j和独立hist可加条件。'),
 'price_second_D.py':('6919B全文：动态载full_pricing/Universe1、旧557+7、八D2位/分族最大/菜单角、float阈值和直接候选校对、种子/零补质量写出。','全文读15042B基类并比较成熟557合同；初始1002逐值绑定旧64与67去重+锚，未仅猜源数量。','保564完整类型定价算法和缺精确dual/新primal恢复的边界，0import/LP。'),
 'price_second_D_full.py':('6367B全文：557+351、依赖decomposition、count特征×120、49152外条件、缓存/float新列/输出与maxiter25。','与七行price、基类120单位、完整908行名/1862原子及11轮记录比较；序列化dual不是全原向量。','保908全面新行定价及真实停止/保存时点；0新full-price或优化器。'),
 'cg_second_D.json':('731110B全564行名/1002原子全部字段/1002质量（70正932零）/全部51 sparse dual/单轮7字段history消费。','前437同canonical、557同908、全部1002原子同908前缀；正支撑19个actual未覆盖不可丢。','完整旧输出保且字段阅读给全部坐标/hex/域，beta2.042155不授新精确最优；新七dual无序列化正项。'),
 'cg_second_D_full.json':('1358160B全908行名/1862原子全部字段/1862质量（74正1788零）/全部60 sparse dual/全部11轮history消费。','旧557名逐字同564、前1002原子同，新增860；正支撑21 actual未覆盖，14新dual全部列出。','保全部数值和原子而非只beta2.038674，末负7.626e−11不改精确0，无908精确证书或SPE。')
}
assert len(notes)==14
retained={'separate_second_D.py','separate_second_D.json','third_D_completion.json','two_D_completion.json','cg_second_D.json','cg_second_D_full.json'};receipts=[]
for x in items:
 n=x['path'].removeprefix(PFX);a,b,c=notes[n];ts=list(dict.fromkeys(targets[x['path']]))
 if n.startswith('separate_second_D.'):ts.append(old_review)
 assert all((R/t).is_file() for t in ts)
 receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a,'comparison_note':b,'decision_note':c+' 完整原字节与承重去向保在本批证据。','disposition':'retained' if n in retained else 'integrated','targets':ts})
(W/'receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n');(W/'delivery-paths.json').write_text(json.dumps([M+x for x in objects]+[str(B.relative_to(R)),str(W.relative_to(R))],ensure_ascii=False,indent=2)+'\n')
comparisons=[M+x for x in ['引理/交叉有序历史的均匀净成本对称化--引理.md','审查/一般目录全局收费交接与索引二层真实节点--审查.md','定理/固定背景三人利润界--定理.md','程序/五人保交叠全型与常锚点跨族定价的精确恢复合同--程序.md','计算/五人五百五十七行列生成的原始轨迹与点版本--计算.md','审查/交叉回复税与第二步D分支的独立七行排除--审查.md','障碍/五人索引松弛点的根饱和不相容--障碍.md','引理/真实菜单去对角比较与五人索引点分离--引理.md']]
(B/'comparison-manifest.json').write_text(json.dumps([{'path':p,'sha256':hashlib.sha256((R/p).read_bytes()).hexdigest(),'role':'actual full current text compared; prior C2 texts remain known and unmodified; no old audit rerun'} for p in comparisons],ensure_ascii=False,indent=2)+'\n')
oldB=R/'archives/customer-attraction/tools/evidence/direct-coverage-source-resumed-boss3';reused=[]
for n in ['separate_second_D.py','separate_second_D.json']:
 p=B/'original'/PFX/n;q=oldB/'dependencies'/PFX/n;assert p.read_bytes()==q.read_bytes();reused.append({'path':PFX+n,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'current_primary_id':next(x['id'] for x in items if x['path']==PFX+n),'previous_role':'C2 comparison dependency fully read; old peer/D7 qualification reused','previous_evidence':'archives/customer-attraction/tools/evidence/direct-coverage-source-resumed-boss3/README.md','new_runtime':False})
(B/'reused-D7-review.json').write_text(json.dumps(reused,ensure_ascii=False,indent=2)+'\n')
exports=json.loads(Path('/workspace/scratch/cd4305a146e6/boss3-session/c3-agent-exports.json').read_text());(B/'read-export-summary.json').write_text(json.dumps([{'id':x['id'],'path':x['path'],'status':x['status']} for x in exports],ensure_ascii=False,indent=2)+'\n')
assert sum(x['status']=='clean-show-read-only-exported' for x in exports)==12
rows='|源ID|branch_geometry原件|处置|正式去向|\n|---|---|---|---|\n'
for x,rec in zip(items,receipts):
 n=x['path'].removeprefix(PFX);links='、'.join('['+Path(t).stem+'](../../../state/'+str(Path(t).relative_to(M))+')' for t in rec['targets']);rows+=f"|{x['id']}|[{n}](original/{x['path']})|{rec['disposition']}|{links}|\n"
text='''# 分支几何的完整来源闭包

Boss3实际claim的14源2148194B，2 Markdown/7 Python/5 JSON，原claim tip由父方确认。按父方明确授权，本代理只读clean show导出12份；另两separate原件复用C2同SHA。全部主源原字节按原路径保在original/，逐件size/SHA核同：[source-manifest.json](source-manifest.json)、[只读导出摘要](read-export-summary.json)。没有代理claim/checkpoint/done、凭据读取或远端写入。

四篇新正文自足保一般λ前缀迁移、任意非负权七行max包络、133/283固定点诊断及564/908完整列生成合同。七代码全文实读，两separate在C2完整读过、本批核同并补其真实依赖；两MD全文、五JSON所有域字段/全部原子与零/正坐标均处理，非只取beta。

## 依赖与成熟资格

[dependency-manifest.json](dependency-manifest.json)保七个冻结依赖：旧64原子JSON、full_pricing.py、67原子精确点、partition/offdiagonal两个helper、canonical indexed定义、package路径标记init。基类15042B全文读，旧557辅助行按成熟解析/精确认证对象复用；没有将这些依赖另认领或重新授整套审计。旧JSON只消费相关primal/行名，67点只用其原子结构绑定种子，未重审其mass/slack/dual。

[comparison-manifest.json](comparison-manifest.json)列实际比较正文。C2的两separate当时是比较源，本次成为主源；[reused-D7-review.json](reused-D7-review.json)证明字节相同，固定七行负证书及C2 peer审计资格复用，0额外D7/peer/separate运行。

## 唯一一次新原程序

原audit_commuting_prefix.py在隔离源树执行一次，仅依已冻结旧64点。Python3.12.14、assert开启、exit0/stderr0；[execution](replay/commuting/execution.json)、[完整2409B stdout](replay/commuting/stdout.json)保三族×四折点全部有理数。它是固定点工具诊断，不是SPE/437重审或一般half证明。

所有LP、price、third/two completion、separate、旧C2 peer、旧437/557全域、原始/对偶恢复都0新运行；未import/install NumPy/SciPy。[read_saved_fields.py](read_saved_fields.py)只作保存数据全字段/坐标/来源绑定，[saved-field-review.json](saved-field-review.json)是完整结果。

## 大JSON确切阅读范围

564：全部564行名、1002个六字段原子、70正/932零质量、51 sparse dual、1轮history。908：全部908行名、1862个原子、74正/1788零、60 sparse dual、11轮history。每个bits/8/8/16直方图/共同j/三菜单/D2_bits均验证完整合法域；保所有正值小数和float.hex、所有零坐标、全部dual和历史记录。正支撑的19/21个actual未覆盖原子保留。

两报告前557名同一冻结序列，前437同canonical；908前1002原子等564全部原子。初始seed精确绑定旧64+67结构去重125，再×8 D2及2锚=1002；不是猜测另一个61点。third报告全部83split/14活动行和two报告全部字段都消费。正/负最小最大违量与HiGHS optimal成功区分，任何float近零均未改为精确0。

## 关系与逐源去向

一般λ工具转移同负载F2上界，不转移政策；一般七行是独立权族，D7是其已精确认证特例；133到283是必要系统扩张；564/908在更大类型域重新分配质量，旧点排除不代全域证明。当前五人half已另证，六人目标未闭合。阶段三按稳定ID/正文保表示、特化、实现、来源、固定点反驳及数值发现关系，当前阶段二不build正式图，不借旧图造边。

'''+rows
(B/'README.md').write_text(text)
(W/'reading-and-handoff.md').write_text('''# C3实质交付

14实际Boss3来源2148194B全文件与全JSON域字段完成；四正式正文、全部原件/七依赖/完整大数据字段记录和14receipt已写。精确checkpoint清单delivery-paths.json，逐源done输入receipts.json。当前未声称远端pushed/done。

父方授权的12次clean show只读导出已完成，无失败/重试；两separate复用C2同字节。只有audit_commuting_prefix新运行一次，12有理折点均正；0LP/CG/补全/旧D7/peer/437/557重审。C2与其他成熟正文均未修改。

关键边界：迁移双尾利润上界不交换策略；逐客户max包络方向与λ全局一致；third负minmax与two正minmax均solver optimal，正数不是solver返回infeasible；564/908全字段而非beta摘要，正质量未覆盖客户与浮点dual截断/负停止余量保真。五人旧OPEN与现已证/六人焦点分开。

待父方全读、自行串行checkpoint确认pushed、再14done。本批ready后冻结修改并立即接下一批。
''')
print(json.dumps({'objects':len(objects),'receipts':len(receipts),'dispositions':dict(Counter(x['disposition'] for x in receipts)),'read_only_exports':12,'new_original_runtime_entries':1},ensure_ascii=False))
