from pathlib import Path
from collections import Counter
import json,hashlib,shutil
R=Path('/workspace/scratch/cd4305a146e6/co-work-anl-boss3');W=R/'cleanup/workspaces/Boss3/resume-20261102/c2';B=R/'archives/customer-attraction/tools/evidence/direct-coverage-source-resumed-boss3';M='archives/customer-attraction/state/';PFX='research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/direct_coverage/'
items=json.loads((B/'source-manifest.json').read_text());objs=json.loads((W/'object-index.json').read_text());targets={}
for rel,meta in objs.items():
 for src in meta['sources']:targets.setdefault(src.split('#')[0],[]).append(M+rel)
notes={
'README.md':('1059B全文，ROW3准确开放合同、精确物化/全SPE动作证书、float发现与peer两项接受范围全部读取。','旧前缀账本与当前五人half已证明相比较；入口所述原20终局是内存枚举，不冒另存全向量文件。','将真实S复制、185型诊断、税/D7独审及探针边界分别归四对象，不据旧OPEN重开五人。'),
'audit_peer_relations.py':('3715B全文；64六会员符号分母系数恒等式，旧64原子的AB/AE/second重数一致性、七真实行、512新会员型/64 maxima和有理负总和。','独立对读同行crossed_reply_tax及separate_second_D源码/2030B证书；旧primal仅相应字段使用，无437/dual重审。','原样一次输出494B同原，保无优化器/同行helper的实现独立性，非盲审/外审；一般tax与固定D7分锚点。'),
'credible_cross_query_reply.md':('5600B全文；完整五人actualAB后五最优槽、ROW3、min位置3条件、旧人B_i改变量、复制S_j真末回复/BR势差、严格物化诊断。','与成熟五人普遍证书/旧ROW3接口、六索引投影及新S/R两类crossed reply比较；同名K按复制对象区分。','自足写必要门槛/精确中继及未付势差，指定坏点失败不授一般ROW3或六人证明。'),
'exact_materialized_audit.json':('2392B全部status/scale/18主题/185型/单位数/O/拟CDE/门槛/五min/20终局/最小余额/五子审/343与5831/证书路径字段读取。','本次原精确入口新报告逐字节相同；与float210型/10根结果明确为不同输入版本。','保完整三人固定诊断及严格唯一末回复，五比较并集不命名OPT3；不把三人证书前置空行动当五人。'),
'exact_materialized_relaxation.py':('3966B全码；冻结11支持整数轨道/不同排列、18标签185型构造、规范集合值BI、所有可行(z,a)真行修正、唯一末BR及独立certificate模块。','四规范模块逐冻结SHA核同并全文读；完整动作验证器不调用solver，但不是第二套全集实现。','一次原样运行生成三文件均同原字节，保全部依赖和overwrite输出行为；0发现优化。'),
'frozen_row3_source_support.json':('3186B全部scope/scale及11支持各五元state、八格h、float weight、integer orbit weight读取；每行h和5及质量整除排列数核。','与精确代码185型整数构造及float materializer可变父输入区别；冻结记录明示恢复自integer catalog。','完整11轨道表入计算正文，可自足重建32,164,464,720单位客户；不声称舍入保原77行。'),
'materialize_row3_relaxation.py':('3104B全码；读取可变parent/row3_relaxation、float轨道、count集合值递推/1e−10容差、全18形式pay列、拟尾/真行摘要。','对读精确入口使用frozen integer support，210型报告不可乘scale核同185型；父输入本批未取、未新跑。','保不同版本发现器与输入依赖缺口，不把float成功当精确证书；未占用列不当实际玩家收益。'),
'materialized_relaxation_audit.json':('2068B全字段含18项pay列、五min、五拟尾失败、best true ROW的18counts/firstaction/W/row/slack等读取。','与对应float代码逐字段解释，210型/10outcomes及1.5084908438为另版本，不归185型精确输出。','保全部旧float数据与真实范围，前三pay才对应CDE角色，其余非占用形式列；不授普遍阴性。'),
'materialized_row3_catalog.json':('30049B全部18标签、185条不同正整数topics/multiplicity和players3消费；单位数/重数范围核明。','本次原整数轨道构造新catalog逐字节同SHA ecbde1a…，与11行定义逐型绑定。','完整输入原字节保，正文给全轨道生成规则；这是合法单位客户而非signed/带权客户。'),
'materialized_row3_true_spe.json':('27968B全部343 history/action及18维终局计数读取，required历史无缺重，follow为S1,R1,R0。','本次原入口新certificate逐字节相同，独立verify模块核全部5831真偏离；与只拟CDE叶分清。','保一个完整三人SPE而非唯一均衡或全20列表；不冒完整五人根。'),
'peer_relations_independent_audit.json':('494B全部七字段读取：status passed/64符号案例/general tax scope/64旧atoms/512split/精确负有理数/fixed scope。','本次原audit输出逐字节同SHA4fa94fd…；64是会员符号恒等式，不是64个背景值。','保精确内部实现成功及D7固定非延拓范围，后补去对角/锚定不倒填旧报告覆盖。'),
'peer_relations_independent_review.md':('3908B全文；三IC精确有序节点、调和差/非负余项、符号背景表示、七行合法性/512分型最大包络与固定点限制。','亲读同行三个真实依赖及成熟根饱和/去对角对同64点的其他排除；既有五人half别证。','保存两项独立审查锚点、完整七式/乘子/反证逻辑，不把不同排除互造依赖或称全LP界。'),
'probe_allbig_cone.py':('1993B全文；7标签5人、big5+四leaf1种子、330count策略first tie、1980floatIC、W=1、ROW普通目标与输出。','对照随机普通/0.8加强两入口；allbig传rng但实际选ties[0]，不是完整历史净化。','保固定子类发现合同；一单客户全0保存点可直接解析SPE，0重跑LP。'),
'probe_row3_strong_cone.py':('2402B全码；seed510257/16%随机、每8次重启、count策略、.8W−O+row目标、噪声和负分早停、覆盖best文件。','逐段与普通W系数1程序区别，保存点的5.55e−17按单客户模型是精确0。','保更强目标与有限发现范围，不能把近零当严格正或普通ROW3最优。'),
'probe_row_cone.py':('2391B全码；全count真实分支IC、种子下最优五支持后固定、非负类型floatLP、W归一、迭代/扰动/停止/写出。','与历史/计数严格分离全文比较；质量重优后比较J不自动仍OPT，源码无Fraction恢复/dual。','保普通ROW3固定count锥合同，不给一般阴性或精确最优。'),
'probe_true_row.py':('2238B全文；60整数收益/全集递推、21个比较求OPT、前30低W根终局、前三步可达状态、真实在轨修正、随机默认200及输出。','与保存14型整数记录算术对照；count缓存全集不同于固定count政策，未保存该五人全动作证书。','保精确有限探索合同及前30限制，未占用pay列不当玩家收益；0本次随机/函数重跑。'),
'row3_allbig_cone.json':('45880B全330合法count/动作、path00000/actualcounts、opt01234、mask1唯一质量1及score.2消费。','与原allbig代码和single-customer直接论证比较；330动作全0，展开为2801有序历史。','保固定合法平凡SPE点与ROW1/5，非一般界或全锥dual。'),
'row3_strong_cone_best.json':('45900B全部330政策、path46666、opt01234、actualcounts/mask112质量1/score5.55e−17读取；动作只4/6。','按该唯一客户兴趣456，所有政策动作兴趣内，row1/5；.8W−O+row精确0。','保边界点原float残差和完整政策，不报严格正、负例或加强式普遍成立。'),
'row_cone_best.json':('46425B全330政策及10个正float质量、path60000/opt01234/counts/score.311728…读取；316次0/13次6/1次2。','按保存小数与真实follow求W/O/row重现分值，但未恢复全部IC/dual；与两单客点资格不同。','保完整浮点候选，分数字符串解释小数不自动授精确SPE/最优。'),
 'true_row_probe_best.json':('797B全部iteration91/score60、14个正整数mask重数、OPT119/W108/prefix22/action1/counts、七pay/minima、row4492/gap660读取。','总客户119与J覆盖全体给OPT119；3×1208+2×1428=60W，row−gap3832，缺全五人动作证书。','保有限正余额958/15，完整原输入与精确算术入正文，不把一个保存例子当全域ROW3。')
}
assert len(notes)==20
receipts=[];retained={'frozen_row3_source_support.json','materialized_relaxation_audit.json','materialized_row3_catalog.json','materialized_row3_true_spe.json','row3_allbig_cone.json','row3_strong_cone_best.json','row_cone_best.json','true_row_probe_best.json'}
for x in items:
 name=x['path'].removeprefix(PFX);a,b,c=notes[name];ts=list(dict.fromkeys(targets['direct_coverage/'+name]))
 if name=='README.md':ts=[M+p for p in objs]
 for t in ts:assert (R/t).is_file()
 receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a,'comparison_note':b,'decision_note':c+' 原字节及逐字段去向保完整证据。','disposition':'retained' if name in retained else 'integrated','targets':ts})
(W/'receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n');(W/'delivery-paths.json').write_text(json.dumps([M+p for p in objs]+[str(B.relative_to(R)),str(W.relative_to(R))],ensure_ascii=False,indent=2)+'\n')
comparisons=[M+p for p in ['定理/五人半覆盖--定理.md','引理/真实第三位六索引菜单的完整直方图投影--引理.md','资源/五人前缀信用接口与内部独审的历史范围--资源.md','审查/五人前缀账本与父审程序的恢复核对--审查.md','引理/真实菜单去对角比较与五人索引点分离--引理.md','障碍/五人索引松弛点的根饱和不相容--障碍.md','反例/完整历史与计数统一策略的严格分离--反例.md','反例/四主题二十二客户的人数福利下降--反例.md']]
(B/'comparison-manifest.json').write_text(json.dumps([{'path':p,'sha256':hashlib.sha256((R/p).read_bytes()).hexdigest(),'scope':'全文实际比较；无重新认领/旧审计重跑'} for p in comparisons],ensure_ascii=False,indent=2)+'\n')
for p in list(B.rglob('__pycache__')):shutil.rmtree(p)
table='|ID|direct_coverage原路径|处置|正式正文|\n|---|---|---|---|\n'
for x,rec in zip(items,receipts):
 name=x['path'].removeprefix(PFX);links='、'.join('['+Path(t).stem+'](../../../state/'+str(Path(t).relative_to(M))+')' for t in rec['targets'])
 table+=f"|{x['id']}|[{name}](original/{x['path']})|{rec['disposition']}|{links}|\n"
readme='''# 真实第三位查询来源闭包

20份已归Boss3来源共235535B，3 Markdown/7 Python/10 JSON。父方clean show导出，本代理逐件再次核size/SHA，全部原路径原字节见original/及[source-manifest.json](source-manifest.json)。三MD、七代码全文读，所有JSON全字段消费，185型/343有序动作/三个330政策全部记录均处理，逐源独有内容和版本进入四篇自足正文。

八份比较依赖见[dependency-manifest.json](dependency-manifest.json)：同行crossed_reply_tax.md、separate_second_D.py/JSON；四规范模块；旧five_player_indexed_bound.json。全部核冻结SHA。三同行依赖由父方另show，无新认领/done；规范代码全文读，旧索引JSON仅消费primal的质量/会员/直方图用于D7，不重审旧437矩阵/对偶。成熟正文比较见[comparison-manifest.json](comparison-manifest.json)。

## 两次实际原入口

隔离replay/source-root只放必要原代码/输入/依赖，原件不覆盖。Python3.12.14、assert开启，两次均exit0/stderr0：

|原入口|实际检查|执行与完整输出|
|---|---|---|
|exact_materialized_relaxation.py|冻结11轨道整数重建、185型三人全部终局集合及独立完整343历史/5831偏离验证|[execution](replay/exact_materialized_relaxation-execution.json)、[stdout](replay/exact_materialized_relaxation-stdout.txt)|
|audit_peer_relations.py|64会员符号背景恒等式、64旧原子×8新型七行最大包络及精确负总数|[execution](replay/audit_peer_relations-execution.json)、[stdout](replay/audit_peer_relations-stdout.txt)|

[完整新报告目录](replay/source-root/research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/direct_coverage/)中的catalog、三人完整策略、2392B exact报告及494B peer报告，四文件全部逐字节同冻结源。[saved-field-review.json](saved-field-review.json)绑定每个输出/原件SHA，并保全部保存字段阅读与简单分值算术；[read_saved_fields.py](read_saved_fields.py)不做优化器、随机扫描或重复均衡求解。

没有新LP/MILP、float materializer、四probe、随机扫描、同行发现器或旧437全域认证。规范求解器与不调用它的certificate模块分开，当前重放不是另一研究员或另一套全集实现。

## 必须保留的版本和量词

浮点210型/10outcomes与冻结整数185型/20outcomes是不同输入版本，不是仅舍入差；float父输入未纳本次运行闭包。直接诊断复制S_j后的K^S与税证明复制R_j后的K^R分名。185型是三人真实实例，五T比较并集不是OPT3，空前缀不能自动构成五人根SPE。D7排的是另一个旧64原子点的指定second→D延拓，不是全域上界。

当前五人half已有普遍证明；旧ROW3仍仅按其独立辅助合同说明，六人目标未被本批解决。税、D7、物化诊断和探针按稳定ID/锚点区分；阶段三据真实条件建立来源/必要行/反驳/实现/有限验证关系，目前尚处阶段二、未build正式图。未有外审、新颖性或锐性认证。

## 逐源正式去向

'''+table
(B/'README.md').write_text(readme)
(W/'reading-and-handoff.md').write_text('''# C2交付范围

20主源235535B全文件/全字段完成；四正式对象、全部原件/八依赖、两次实际原重放及20逐源receipt已写。准确checkpoint路径见delivery-paths.json；receipts.json为父方串行done输入。当前尚未声称pushed或done，本子代理没有Git、认证、work.py联网或远端写。

重点：真实S复制门槛/旧人利润差不漏；整数185型与浮点210型分版本；税R复制与S复制分节点；64符号恒等式不是有限背景抽样；D7 λ不需归一（实际和1.000001）且只排一个旧点；三个count策略固定子类/0.8加强目标不混普通ROW3；真行记录未占用pay列不当玩家利润。五人已证与旧OPEN、当前六人焦点分清。

本批完成后停止改动，待父Boss审阅、显式checkpoint确认pushed再20done；随后立即接下一批，非常驻检查岗。成熟正文未修改。
''')
print(json.dumps({'objects':len(objs),'receipts':len(receipts),'primary_bytes':sum(x['size'] for x in items),'dispositions':dict(Counter(x['disposition'] for x in receipts))},ensure_ascii=False))
