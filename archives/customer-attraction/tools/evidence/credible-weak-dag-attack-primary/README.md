# 逐人净覆盖缺口weak-DAG五主源证据

正式认领pushed15d5611461fa75b3b7fc657783e87cb40b28fb93，Boss4/synced；唯一capture为boss4-r3-credible-next5aw-claim.json，五期望ID与实际claim交集全五。确认后逐源clean show全文读/双冻结SHA。五主源共5441B：2688B驱动及676/676/697/704B四报告；原件保original/完整相对路径，primary-manifest.json不含依赖额外done。

对应[自足计算正文](../../../state/计算/逐人净覆盖缺口的完整终局见证攻击--计算.md)。原目标是m u_a(q)≥OPT−W，a是终局中有人选择的主题，非固定首人，也非旧OPT/(2m−1)。DAG保(k,desired outcome)联合选择，不强制一般策略为count-Markov。完整变量/约束、有效M1、展开与集合值递推、四报告状态、精确验收层级和真实未付接口均在正文。

## 完整真实导入闭包

runtime-manifest.json保6个依赖55820B、原件及两冻结SHA：outcome_dag_milp.py9778B、customer_attraction_strategy_lp.py20567B、canonical的__init__691B/model8640B/exact9943B/certificate6201B。outcome helper本次全读，五个旧同SHA依赖已完整实读并在本批重核有理恢复/全历史/导入分支。依赖读不充primary；source-manifest.json共11源，原main无实例输入文件，参数来自CLI。

规范包确被导入，但本新run无incumbent，因此没有调用exact_optimize、Fraction恢复、independently_verify、规范verify_certificate或ExactSPESolver。helper main/self_test、outcome helper独立main和所有旧审计亦未执行。不能以代码拥有这些功能就宣称精确候选或认证已产生。

## 仅一个新的原main

replay-tree/复制未改原码与全部导入闭包，不预放输出。本批只运行代表性五标签case一次：

`--root 1,1,1,0,0 --topic 0 --portfolio 2,3,4 --seconds 30 --output 新空路径`。

Python3.12.14/numpy2.3.5/scipy1.17.0，wall8.969099521636963秒，MILP内部8.201410982001107秒，exit0/stderr空，1次MILP；822变量/770二元/1397行，status2、无incumbent、无精确候选。源码和全部导入依赖运行前后字节不变。剩余三个冻结case未重跑，旧实际命令/时间上限未记录，不能由旧elapsed字段补造。

新676B报告SHA04a77e06a03bef3bd16cd440c40d0dc1260f8d81d03f6778bf0d26e25607e76f，旧SHA8830c2617adcf78cbf4e6f5a16f84d5cd4e326d0b87b4165664c2204815bc673；逐字段仅milp.seconds不同，**非全字节复现**。replay/保新报告/stdout/stderr/execution；原件独立保，不篡改时间追求一致。

四冻结报告前两status2/infeasible、后两status1/time limit且primal None，floating_value与exact_candidate均null；universal_bound_proved均false。四人文件名j345实际portfolio是(1,3,4,5)，按字段保全。

## 数学与输入边界

W归一化后硬编码正gap≥10^−6，因此不覆盖任意微小正缺口。helper coverage_row用位求和，当前四distinct J安全，但重复输入会进位，CLI未完整验证，不能扩大为任意重复元组接口。软件允许同覆盖标签，未来严格原集合目录反例需另核覆盖互异或合法转换。

即使exact_candidate.certified为true，它也只表示固定动作表的精确SPE可行；源码没有断言value或weak_gap_integer严格正。未来弱合同反例必须另核正gap，half反例还须OPT>2W。当前没有任何候选，浮点无解/超时不是数学上界。

check_frozen_model_structure.py是新标准库辅助检查，实际执行1次、0求解器/0原main：核四组合法distinct输入、完整目标Fraction系数和Y/Z/T/行数公式，并保全兴趣类型精确可行SPE的目标−1以说明“无正gap候选”不等于无SPE。其结果不承担不可行证明。传输验证只读现有结果，不再执行数学检查。

全仓比较指纹在related-material.json；五receipt、自查、关系判断及实际下一候选保cleanup工作区。本批没有未理解/来源缺口，数值未闭合及严格验收边界均已明确。无外审/新颖性认证，不声称weak bridge或六人half已解决；串行复制/推送/done由Boss执行。
