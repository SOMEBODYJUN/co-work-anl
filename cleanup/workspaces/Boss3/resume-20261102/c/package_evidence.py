from pathlib import Path
import json,hashlib
R=Path('/workspace/scratch/cd4305a146e6/co-work-anl-boss3');W=R/'cleanup/workspaces/Boss3/resume-20261102/c';B=R/'archives/customer-attraction/tools/evidence/boss3-c16-resumed';M='archives/customer-attraction/state/'
comparisons=[M+x for x in [
'反例/实际均匀缩放负载的弱付款桥--反例.md','反例/同题冻结删位静态补贴的十三人障碍--反例.md','计算/分数负载四主题族的全历史核验--计算.md','反例/人数增加的十二客户全部均衡福利下降--反例.md','反例/成员平稳但根收益不可交换的三人见证--反例.md','反例/共同单调Shapley模型的锚弱占优与无界根比--反例.md','定理/共同客户收益的正边际与平衡贡献--定理.md','障碍/共同有符号客户的全局三标签耦合缺口--障碍.md','障碍/同支持全部梯度环不能替代共同客户表示--障碍.md','反例/完整历史与计数统一策略的严格分离--反例.md','定理/固定完整策略的二主题耦合二倍界--定理.md','资源/空根构造检查点与十三人纯查询锥探针--资源.md','障碍/R-171有符号delta选择性预算独立复核--障碍.md','计算/十三人两查询强桥与完整WP及两种背景值--计算.md']]+['archives/customer-attraction/tools/evidence/strategy-cones/original/tests/audits/customer_attraction_strategy_lp.py','archives/customer-attraction/tools/evidence/coverage-opportunity/examples/customer_attraction/coverage_opportunity_failure.json']
(B/'comparison-manifest.json').write_text(json.dumps([{'path':p,'sha256':hashlib.sha256((R/p).read_bytes()).hexdigest(),'scope':'全文实际阅读；比较用途，无来源重领或新运行'} for p in comparisons],ensure_ascii=False,indent=2)+'\n')
items=json.loads((B/'source-manifest.json').read_text());receipts=json.loads((W/'receipts.json').read_text());prefix='research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/'
table='|源ID|本工作区内原路径|处置|正式去向|\n|---|---|---|---|\n'
for x,r in zip(items,receipts):
 rel=x['path'][len(prefix):]
 links='、'.join('['+Path(t).stem+'](../../../state/'+str(Path(t).relative_to(M))+')' for t in r['targets'])
 table+=f"|{x['id']}|[{rel}](original/{x['path']})|{r['disposition']}|{links}|\n"
text='''# 完整有序历史工作区的本次来源闭包

本批48个Boss3已认领冻结来源，共1260542B：17 Python、7 Markdown、23 JSON（含workspace身份）、1 gzip。全部由父Boss串行clean show导出，本子代理再次核size/SHA；[source-manifest.json](source-manifest.json)与original/保原路径原字节。原Claim/版本量词不改，无凭据入库。

八篇正式对象保全：固定m全支持Shapley三角身份基及交换；重复互惠尾闭包；22客户全部SPE人口下降；双单例产品目录动态/静态NE分离；四人signed超二与可见负原子；count-joint MILP合同；十三人构造与审计范围；其他有限探针与版本边界。下表逐源指正文，原件与摘要不是互相替代品。

## 全文件阅读和准确比较范围

7个Markdown与17个Python全文读。全部JSON全字段消费，大动作表按完整有序history域逐条解析；人口106节点全表由本次原程序新报告整体逐字段对比，四人signed全部56权重/259常2动作由原恢复器新输出逐字节核同。十三人gzip全部27243节点字段与scope/instance/root/expected/stats解压消费，同SHA完整SPE资格复用成熟认证，未重新跑IC。

[comparison-manifest.json](comparison-manifest.json)列实际全文读的成熟对象与两份依赖源码/fixture；它们没有额外认领或重新done。[saved-field-review.json](saved-field-review.json)保原件全字段计数、人口/signed完整绑定、2801+3动作与127+3克隆、旧packet全部节点字段统计和有限记录；[signed-discovery-field-reading.json](signed-discovery-field-reading.json)只核三/五人保存动作域和候选字段，未赋新精确IC/稀释资格。

## 本次恰四个必要原程序执行

原代码复制到独立replay子目录，原件无旁写。Python3.12.14、assert开启，四入口均exit0/stderr0；各execution.json有argv/cwd/耗时/源码及stdout SHA，不把历史报告秒数当本次事件。

|入口|本次真实范围|证据|
|---|---|---|
|population_audit.py|22客户m3/m4全有序递推、21/85节点证书、84/340含self比较及106完整节点表|[执行](replay/population/execution.json)、[stdout](replay/population/stdout.txt)、[完整新报告](replay/population/population_audit.json)，全JSON等原|
|verify_signed_obstruction.py|四人六标签56型恢复、259节点1554含self IC、18480稀释/97负原子|[执行](replay/signed-obstruction/execution.json)、[stdout](replay/signed-obstruction/stdout.txt)、[exact](replay/signed-obstruction/signed_obstruction_exact.json)、[report](replay/signed-obstruction/signed_obstruction_report.json)，两文件同原字节|
|verify_all_support_shapley.py|五组参数逐类型边际/三角基秩/等计数交换|[执行](replay/shapley/execution.json)、[stdout](replay/shapley/stdout.txt)|
|audit_reciprocal_tail.py|100项系数恒等式及单位末位2对5/2|[执行](replay/reciprocal/execution.json)、[stdout](replay/reciprocal/stdout.txt)|

没有新LP/MILP、随机扫描、规范BI发现器、十三人自动机IC或NumPy/SciPy安装/import。另[review_saved_fields.py](review_saved_fields.py)是保存数据消费/绑定程序，不是新均衡求解器。

## 数学和关系状态

signed负权、真实单位客户、count子类与完整历史、固定13人与任意k、float发现与精确恢复均分清。一般问题与六人焦点没有因此被解决。源Boss8/R-c50身份和原六研究员声明只作旧资料，不当当前Boss3会话活动。

各新正文的稳定ID、条件、量词、承重论证及与成熟对象的表示/特化/反驳/来源/实现/有限验证关系已明确。当前处阶段二且全仓尚有来源未完，本批暂未调用正式图build；阶段三可按正文精确证据登记，不能为连通或旧图名字强造依赖。所有未成熟有限点均保真实缺口和接续用途。

## 逐来源去向

'''+table
(B/'README.md').write_text(text)
(W/'reading-and-handoff.md').write_text('''# C48完整实质清洗交付

接续R-c50工作区48源1260542B，17 Python/7 Markdown/23 JSON/1 gzip。全文件与全字段、全仓相关比较已完成；八正文路径见delivery-paths.json，48独立receipt见receipts.json。本子代理没有Git写入、认证、网络work.py、认领或done。

只有四个必要原有限入口各一次：22客户全有序人口审计、四人signed exact恢复、全支持Shapley、互惠尾。完整执行和范围见正式证据README。成熟十三人同SHA资格复用，0新IC；27244盲重建与27243packet分别标；五人七主题MILP仅一全兴趣客户ratio1且无精确dual；三/五人signed未恢复点不赋新完整SPE资格。

八正文均自足保存稳定ID/全条件/量词/证明或缺口，并提供阶段三真实关系材料。四人signed全56型质量和全常2策略、22客户全集递推及全部原表、产品五节点完整收益、一般三角基与任意t模板障碍均保。成熟正文未修改。

本批交付到父Boss审核后冻结修改；父方需按精确delivery路径checkpoint确认pushed，再串行clean done这48源。此记录不提前声称远端保存或done。准备接续下一批，仍是完整数学清洗者。
''')
# Source-code hash in the frozen root report is independently bound to actual source bytes.
p=B/'original'/prefix
root=json.loads((p/'root_audits/refined_tax_root.json').read_text())
assert root['checker_sha256']==hashlib.sha256((p/'root_audits/check_automaton.py').read_bytes()).hexdigest()
print('README, comparison manifest and handoff written; frozen root checker hash bound')
