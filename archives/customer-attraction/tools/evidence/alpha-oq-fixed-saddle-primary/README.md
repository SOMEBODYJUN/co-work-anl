# 固定原安全鞍点的查询锥证据

正式对象为[固定原安全鞍点下的完整策略查询锥审计](../../../state/计算/固定原安全鞍点下的完整策略查询锥审计--计算.md)。原件保留repo相对路径在original下，新运行在replay-tree，生成报告另存replay；冻结报告未覆盖。

本5主源claim由Boss确认pushed6976742b9e0d64b0fd6ea8cbd7dd34e3acac5bd2。root当时另记local sync needs-attention，本stage没有据此声称已sync，仍只external写并保原件；源的两冻结定位均已按inventory逐字节核SHA。工作室不执行Git写、claim/done、认证或新代理动作。

| 主源ID | 大小 | 语义处置 |
|---|---:|---|
| 9edffc6508386d059f3a | 2459B | alpha-one原码全部算术/断言/输出，已有同SHA原执行及正式对象充分吸收，duplicate复用 |
| a33dd82cb4d23fab6163 | 976B | alpha-one全JSON字段及源packet SHA，已有同SHA充分输出和对象，duplicate复用 |
| 8b9cf44d16a024398ef3 | 4981B | 指定安全最优p的准确OQ量词、原值、固定p/Q锥、复制停止点、m5条件句，integrated |
| 17bad95333c2be5f6402 | 5092B | 真正导入helper的原main、三次LP、精确鞍点及恢复点检查、输出，integrated |
| 34930f098ddd0db955e8 | 1766B | 全部p/Q/值/原C与W、float状态/目标、精确恢复点和scope，integrated |

主源共15274B；真实运行的两个外部资源是4990B helper 847a210188334e25b4bd和372216B gzip 8d74fd183eba467a811f，共377206B。它们本批仅runtime依赖，不额外done。helper只调用load('all')与query_lp；其cone_lp、交替main、root/onpath/weak模式和随机starts均未执行。运行树完整保留parents[6]及helper路径所需层级，代码无需打补丁。

## 新运行与复用事件分开

一次原OQ main：Python3.12.14、numpy2.3.5、scipy1.17.0，9.433801651000977秒，exit0/stderr空。它内部三次linprog：原归一化质量的p、原对偶Q、固定鞍点C−W攻击。新1766B报告SHA 9aec63918e9ce9996247a45bcab089e53dea091e7a2e960254e363a1fda61876，与冻结报告全字节相同。程序/helper/packet运行前后不变。

[execution](replay/execution.json)、[stdout](replay/stdout.txt)、[stderr](replay/stderr.txt)、[新报告](replay/optimal_query_fixed_cone_attack.json)、[runtime manifest](runtime-input-manifest.json)和[source manifest](source-manifest.json)可逐项核实。prepare_and_run.py的--run有已有执行记录保护；check_package.py只核静态证据记录，不调用任何数学入口。

旧alpha-one main和旧全自动机审计本批均未重跑。旧13的充分原执行来自[既有计算对象](../../../state/计算/分数负载四主题族的全历史核验--计算.md)，同SHA原码/JSON/packet与执行报告身份保存在[复用清单](reused-old13-evidence.json)。完整SPE认证核27243节点/112050含self IC；alpha-one只是实际叶的精确标量，两者不能互相冒充。

本OQ main生成Γ并用于优化和恢复点检查，未逐条assert旧36客户质量的IC。因此新main复现不替代旧SPE认证。浮点最优0、恢复点精确可行0和整个锥精确上界0也不能互换；本批没有最后一种证书。全兴趣点的准确可行性另由正式正文直接证明：13角色分享一个喜欢全部六标签的客户，各IC0、v1/13、W1、总C1。

## 数学比较与停止点

完整读当前跨分支预算定义、完整策略锥不受限静态对偶、固定完整策略价格合同、静态安全值锐界、全p/逐人安全反例、指定锥/固定游戏正预算核验以及完整槽范数和内部审查。上一批named/history对象用于历史对照，和本批实际OQ入口不同。此处以新独有固定鞍点资源接已有一般对象，不重复创建预算定义或alpha-one反例。

OQ目标C−W与helper另有的n·v−W不同；后者本批未优化。若未来得到前者正有理点，只先否定指定p的OQ，还需完整单位客户重构；未证明p唯一时不能否定存在安全最优p版本。C≥n·v方向还阻止把正OQgap直接升级真正聚合安全桥或half反例。

13人固定锥不覆盖m5，更不覆盖m6。原m5条件推导保留，五人half有另证而不认证本OQ；六人half与真正安全总付款仍开放。没有外审、新颖性或一般方法不可能性主张。每个比较对象的读取范围和当前SHA在source-manifest记录；下一候选仅本地只读progress检查，Boss需核实际owner并正式claim。
