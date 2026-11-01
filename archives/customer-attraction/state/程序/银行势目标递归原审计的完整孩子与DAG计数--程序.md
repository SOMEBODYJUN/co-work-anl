---
id: customer-attraction/bank-punishment-original-target-dag-audit-and-complete-child-scope
kind: program
type_tag: 程序
title: 银行势目标递归原审计的完整孩子与DAG计数
status: full-original-code-and-report-read; no-replay
truth_status: finite-exact-implementation-of-existing-general-potential-construction
review_level: informed-source-contract-and-full-report-analysis
scope: m2-through7-contiguous-distinct-bank-prefix-forced-children
summary: 2869原顶层Fraction递归与4213全报告，21参数组322强制孩子/27061目标记忆DAG状态/92788含self比较；完整后继构造非全SPE枚举，0新run。
source_ids: [916c94139ba5f592eb22, a28eed438c13f7e5feab]
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/security_aggregate/audit_bank_punishment.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/security_aggregate/audit_bank_punishment.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/security_aggregate/bank_punishment_audit.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/security_aggregate/bank_punishment_audit.json
---

# 银行势目标递归原审计的完整孩子与DAG计数

2869B原程序与4213B完整报告共7082B，均actual normal取得并全文读；本次补[势最大与银行低退出定理](../定理/不交资源的势最大计数与银行可信低退出--定理.md)此前仅据README记录的实现/输出身份。原程序的有限构造审计与现一般解析证明分开，不重授bank工具、盲审或全m定理；本次原CLI/import/solver/DAG重放/LP/IC/新数学实现运行均0。

## 实际入口、参数与客户表达

代码只stdlib Fraction/lru_cache/Path/json，没有main guard。模块顶层遍历所有参数、计算、断言、写JSON和打印，**import本身即执行完整审计并覆盖输出**，不能当作只读函数加载。无argv、外部输入文件、原证明或项目model/solver导入；docstring提到bank_punishment_blind_proof.md只是数学出处，不是运行时读取。OUT=Path(__file__).resolve().parent，固定覆盖同目录bank_punishment_audit.json。

实际m=2,…,7，每m的j=1,…,m−1，共21组。记k=m−j，a=(2,…,2,k,1,…,1)，前j块B大小2，core Y大小k，末k−1叶各1，p=len(a)=m。块两两不交、玩家每次选一个块；整数块大小代表不同单位客户的精确聚合，不是加权玩家，也不是逐客户ID展开。全客户2m−1，测试s=1；正有理s同倍缩放可共同清分母，报告不声称测试了所有尺度。

每组初始nodes/rows/cases=0、mingap=None，并重定义带缓存的greedy和visit；故缓存只在本(m,j)组内复用，跨全部i/D共享，不跨不同参数组。m1、j0/j=m和i>j不在强制入口域；j=m−1的k1无叶边界真实包含。

## 势最大目标怎样被精确表示

对固定过去负载b、r个新增玩家，调和势为

\[
 \Phi_b(q)=\sum_d\sum_{t=1}^{q_d}\frac{a_d}{b_d+t},\qquad \sum_dq_d=r.
\]

greedy(b,r)逐次选最大a_d/(b_d+q_d+1)，同值取最小d。它用于挑新增**目标计数**；各资源边际席位单调不增，选全局最大下一席构成r个最大可行席位且保每资源前缀，故该目标势最大。phi精确按Fraction求和；visit的首条断言phi(b,q)==phi(b,greedy(b,r))，用这个正确的比较目标验证当前q全局势最大，没有枚举全部计数。

这不是把myopic当前行动当SPE策略。真正处方star在q_d>0的资源中最大化最终份额a_d/(b_d+q_d)，也用最小标签破平局；即时选最高下一席和按最终份额选star是两个角色。既有[3、2两资源例](../反例/高收益席位与贪心终局不能替代完整可信退出--反例.md)的势最优计数可实现，但myopic有序路径根IC失败，不能以“greedy目标正确”省略下面完整孩子。

## visit(b,q)保目标记忆并递归全部真实孩子

r=sum(q)，visit每个未缓存状态先nodes加1、核势最大；r0直接返回全0新增计数，也计为DAG状态。r>0先选star，再对全部p=m行动d构造：

- nb=b+e_d；若q_d>0，目标nq=q−e_d；
- 若q_d=0，目标改为greedy(nb,r−1)；
- tail=visit(nb,nq)递归定义这个孩子的完整续局，并仅返回其实际新增计数；当前强制d的最终收益pays[d]=a_d/(nb_d+tail_d)。

然后对每个d断言pays[star]−pays[d]≥0。规定star的实际新增终局term=children[star]+e_star还断言恰q，再返回term。没有冻结规定后继后作静态偏离；每个候选都沿**它自己的真实递归孩子**完成。

这正实现已证归纳：q_d>0时势减去同一首席常数，q−e_d仍为nb背景势最大；q_d0时用交换q−e_R+e_d得a_d/(b_d+1)≤a_R/(b_R+q_R)，任意后继都将该偏离封顶。故目标内孩子保目标、目标外孩子重选目标，所有孩子SPE，star对全部真实孩子理性。当前程序在有限参数实际逐状态做这些精确比较，**不枚举全部SPE终局**，也不是只查PNE或在轨叶。

缓存键为(b,q)，同一b的不同目标可能给不同处方；不能称count-only Markov策略。给每个强制入口固定初始q后，沿有序历史更新(b,q)即得完整策略，DAG可展开为全有序树。报告只存汇总，不存各star/边/整张动作表；代码可定义完整构造与“报告已有序策略证书”不同。

## 外层全部i/D强制孩子与四种目标

固定i=1,…,j，正常前缀是B0,…,B_(i−2)各一次；prefix[d]=int(d<i−1)。当前强制任意D=0,…,m−1，b=prefix+e_D，后继r=m−i≥1。

|强制动作D|初始目标q|强制者最终上界|
|---|---|---|
|尚空B|每仍空B一次，另D再一次，Y取k−1次，其它0|2/(1+1)=1|
|Y（D=j）|每仍空B一次，Y再k−1次，其它0|k/[1+(k−1)]=1|
|前缀已用B|greedy(b,r)|当前已有负载2，任意后继≤1|
|leaf|greedy(b,r)|总块1，任意后继≤1|

每个初始目标先assert sum(q)==r，terminal=visit(b,q)后检查强制者current=a_D/(b_D+terminal_D)≤1，再cases加1。这些强制行动自身不要求理性；IC检查只在**后继策略**的全部决策状态，外层只核强制者收益cap。所有D包括该正常位置原本的下一未用银行（0基标签i−1），不只异常bank标签：联合编译若只改变旧坐标而bank标签未改，也需要这份低退出孩子。它不与正常奖励继续路径混同。

k1且D=Y时q_Y=0，目标取全部r个仍空B首席，各2>1；严格>1席位数是r而非r−1。代码直接构造目标、核phi，无错误“总是r−1”的计数假设。[现解析证明](../定理/不交资源的势最大计数与银行可信低退出--定理.md)已把这个边界独立写清；本次不是修复原源码或新发现反例。

## 原4213B报告全部六字段、21行和总表

|原根字段|原值或完整去向|
|---|---|
|status|`"PASS"`|
|scope|`"finite exact implementation audit of all-parameter proof; not the general proof"`|
|parameter_range|`"2<=m<=7, all 1<=j<m, all 1<=i<=j, all forced bank labels"`|
|scale|`"s=1; rational positive s rescales every comparison"`|
|rows|下列21行，所有6字段|
|totals|下列3字段总表|


rows的21项各恰m/j/forced_children/construction_DAG_states/nonterminal_action_comparisons/minimum_IC_gap六字段，原顺序全部如下：

|m|j|forced_children|construction_DAG_states|nonterminal_action_comparisons|minimum_IC_gap|
|---|---|---|---|---|---|
|2|1|2|5|4|0|
|3|1|3|20|30|0|
|3|2|6|20|30|0|
|4|1|4|71|144|0|
|4|2|8|74|156|0|
|4|3|12|74|156|0|
|5|1|5|254|640|0|
|5|2|10|260|670|0|
|5|3|15|268|710|0|
|5|4|20|268|710|0|
|6|1|6|927|2790|0|
|6|2|12|936|2844|0|
|6|3|18|952|2940|0|
|6|4|24|972|3060|0|
|6|5|30|972|3060|0|
|7|1|7|3436|12040|0|
|7|2|14|3448|12124|0|
|7|3|21|3472|12292|0|
|7|4|28|3512|12572|0|
|7|5|35|3560|12908|0|
|7|6|42|3560|12908|0|


totals完整三字段：

|totals字段|完整原整数|
|---|---:|
|forced_children|322|
|construction_DAG_states|27061|
|nonterminal_action_comparisons|92788|


forced_children每组jm，合322；不是322个互不共享状态的独立实验。construction_DAG_states在visit的cache miss时加1，包括终端q0；各同组强制入口共享可重用(b,q)。nonterminal_action_comparisons仅每个未缓存非终端状态的m个行动比较，含规定star与自身，故也不是92788个不同有序历史或求解器运行。

每个非终端必有star自比0；只要其它IC非负，该组minimum_IC_gap就为0。这21个零不是严格激励裕量或float容差证据；原代码Fraction精确比较，但汇总min不展示正margin或每个强制者具体收益。每行比较数/m才是该组未缓存非终端状态数，DAG状态与有序历史数不可互换。总表只汇总21行，封包结构核会检查存储计数求和，不执行phi、greedy或visit。

## 有限检查、全参数证明与其它bank审计的区别

已全文实读7590B原blind proof及4969B securityREADME，共12559B，与当前冻结metadata字节/SHA/blob一致。原证明在未读credible_attack推导时按新任务独立重构，这是原先验；当前先已知全仓定理再读code/report，是知情源码清洗。README前部安全探索“无新增一般承重关系”与后来银行任务分段，不把前部状态抹掉后加证明，也不把源码不导规范solver升级为本次新blind。

一般不交资源势最大可实现和全m,j银行低退出由[完整解析归纳](../定理/不交资源的势最大计数与银行可信低退出--定理.md)承担，不由m2…7样本外推。该原实现是目标势递归；[任意标记clean/永久BI原审计](任意标记保险与两个不等缺陷产品的原审计--程序.md)则有不同marked入口、模式与历史计数。它们不是同一代码、同一输出或可相加的新增运行；本程序只测连续distinct B前缀i≤j，不覆盖interleaved marked位置。

本程序没有计算正常奖励路径的u/W/OPT、真正静态安全值v的原始/对偶证书、产品旧坐标或联合完整σ。奖励路径W=(m+j)s、OPT=(2m−1)s、[静态v=s双证](../定理/前缀保险的静态安全双证与聚合稀释--定理.md)及[全坐标永久模式前缀修复](../定理/真实退出缺陷的统一与异质前缀修复--定理.md)均为独立解析对象；不能由低退出cap自动付更早祖先或旧坐标未来IC。它也没有给强/弱聚合桥或half新的严格种子或证明。

## 输出、原执行身份与处置

所有正确性核（p==m、目标势/槽数、每动作IC、term==q、forced cap）是assert，python -O会删除；status='PASS'在循环结束后硬编码。源和JSON没有原运行的解释器flags、argv/cwd、代码hash、exit、耗时、stdout/stderr或环境版本绑定，不补造当时assert启用或本次重跑认证。导入即执行又会覆盖原报告，因此本次不import或执行它。

原写文件与print都json.dumps(report,indent=2)各补一个LF；按代码合同序列化相同，但无原stdout就不声称已逐字比对历史stdout成功。4213B报告原字节保留，完整嵌套字段转存只作数据阅读，不归一化原件。两primary均retained至本程序页及[来源闭包](../../tools/evidence/bank-punishment-original-audit-two-primary/README.md)；相关旧proof/README与七正式对象仅比较不额外done。

15XL原完整15ID claim pushed，raw needs-attention与独立2untracked/2tracked全same、无missing/different/unmerged且stash保留的证明并列，不把raw改synced、不裁成两ID回执。Boss4未Git/claim/done，原import/CLI/solver/DAG重放/IC/LP/新数学实现0，交Root串行审阅发表。
