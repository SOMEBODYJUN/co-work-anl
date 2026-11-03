---
id: customer-attraction/count-joint-MILP-full-history-expansion-and-time-limit-record
kind: program
type_tag: 程序
title: 计数联合MILP的完整历史展开与限时证据
status: source-contract-complete; exact-trivial-saved-primal; five-player-dual-unrecovered; no-fresh-optimization
summary: count-dependent共同策略为真子类；保存五人七标签45秒限时ratio1点仅一全兴趣客户，完整2801动作有330计数态且无精确对偶；二人自测另有可读3/2对偶。
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/credible/count_joint.py#candidate"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/credible/count_joint.py#main"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/credible/count_joint_7_5_00112.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/credible/count_joint_selftest.json"
---

# 真子类、变量与归一化

6287B原count_joint.py全文读。它在p标签、m人共同非负客户模型中联合选择类型质量及一份依计数的完整策略。每个非空兴趣mask对应w_B≥0，共2^p−1个；每个深度<m的计数k和标签a有连续U_(k,a)及二元z_(k,a)。U表示从该状态按所选共同计数策略完成后，一位a标签者的终局收益行，不是仅当前动作的短视收益。每状态Σ_a z_(k,a)=1。

给定有序目标path，沿其每个计数固定z_(k,path_i)=1。代码先累加整条path所得root变量实际上是**目标终局计数**；真正空根另名zero。不能把root误读成未走过的前缀。实际覆盖行c取该终局支持，指定比较支持O取portfolio；归一化c·w=1。

全部连续U置于[0,m]，空根被指定行动的U≤1。对每个主题T加|T|≤mU_(zero,path0)，及Σ_B w_B≤mp。前者是任何真实SPE可由根改T得到|T|/m保底的必要约束；实际总收益为1使实际根收益≤1，所以这些界在其所拟域中合理。再加Σ_a q_actual,a U_(zero,a)=1作终局效率。比较可选threshold仅加O·w≥threshold；它不是已有证明。

对每个状态k、可能指定动作a及每个标签t，用z_(k,a)激活U_(k,t)=U_(k+e_a,t)，若孩子深度已m则直接代单位客户最终收益线性行。对每个偏离b激活U_(k,a)≥U_(k+e_b,b)。两方向等式和真实激励都用m作条件常数；当z=0约束松弛。当索引合法、path长度m、portfolio为合法不同标签时，当前两份报告满足这些输入前提；程序没有额外的通用非法CLI容错证明。

所有同计数历史被强制共用一个动作和同一未来映射，所以它是真正的count-dependent子类。输出后明确展开每个h∈{0,…,p−1}^{<m}，令action(h)=policy(count(h))，再交给固定完整策略客户锥恢复/核验。不能从该MILP的阴性、最优值或限时界推到全部历史依赖SPE；一般净化已被[三人五主题严格分离](../反例/完整历史与计数统一策略的严格分离--反例.md)否定。

# 浮点发现与精确固定策略检查的边界

SciPy milp最小化−O·w，保存status/message/count_states/binary_actions/rows/variables/elapsed、float objective及float dual bound；floating_only恒true。有incumbent就按z最大者提策略，即使因时限停止也可进入后续；若res.x为空则proof=null。

后续StrategyCone.optimize只针对已经选定的完整策略重新优化客户质量，若精确primal恢复成功才整数克隆、独立逐历史检查，并用规范verify_certificate再验一次。saved ratio来自这个整数输入的实际全目录OPT/W，不是把MILP float目标直接改成定理。精确对偶失败时primal仍可保存，dual_bound=null且exact_dual_optimal=false。已经对读仓内[固定策略锥源码副本](../../tools/evidence/strategy-cones/original/tests/audits/customer_attraction_strategy_lp.py)，理解其βc−Gᵀμ≥O且μ≥0合同；本批没有将该比较副本冒成本次实际import绑定，没有运行或安装NumPy/SciPy/MILP。

# 五人七标签的全部保存字段及真实内容

count_joint_7_5_00112.json共有381649B。m5/p7，path=(0,0,1,1,2)，portfolio=(2,3,4,5,6)。保存MILP：

|字段|原值|
|---|---|
|status/message|1 / Time limit reached. (HiGHS Status 13: Time limit reached)|
|count_states/binary_actions|330 / 2310|
|rows/variables|46540 / 4747|
|elapsed|45.219719317秒|
|floating_objective|1.0|
|floating_dual_bound|3.7234042553191466|
|floating_only|true|

这些计数相合：Σ_(d=0)^4 binom(d+6,6)=330，每态7个z与7个U，加127个w，得4747变量。时限上界只是该数值子类搜索的float界，绝不是全历史SPE的严格上界。

proof保存127项integer_clones，前126项全0、最后mask127恰1，即唯一一位对全部七标签感兴趣的单位客户。全部2801个有序history→action行逐项消费，required set恰Σ_(d=0)^4 7^d=2801、无重复/缺漏、每动作合法；同计数共用330个动作，实际follow为00112，声明终局(2,2,1,0,0,0,0)一致。

对该真实输入，不论所有人如何行动，同一客户最终总负载恒5，故每位收益恒1/5；任意完整策略在每个历史均最优。这一直接理由自足认证保存策略的完整SPE，毋须再跑19607项逐节点比较。W=OPT=1、ratio=cone_comparison_optimum=1。exact_dual_optimal=false、dual_support=[]、dual_bound=null、all_ordered_histories=2801，全部字段按原样保。它只给一个平凡可行点，没有证得该策略锥最优，更没有证得整个MILP最优或五人坏比率不存在。

# 二人两标签自测的可读精确对偶

1185B count_joint_selftest.json：m2/p2、path00、portfolio01，MILP status0、3计数态、6二元动作、38行、15变量、elapsed0.00461382000003141，float objective=dual bound=1.5。完整三节点动作全0；整数类型(w_0,w_1,w_01)=(2,1,0)，实际两人选0、每人1，W2，OPT3，ratio3/2。

在该固定策略锥，末位历史0的真实比较是w_0/2−w_1≥0，历史1的比较是w_0−w_1/2≥0；根重复第一条。按排序的唯一非零IC行，row0=(1/2,−1,0)。令c=(1,0,1)、O=(1,1,1)，则
\[
 \tfrac32c-row0-O=(0,0,\tfrac12)\ge0.
\]
这对应保存dual_support=[[0,1]]、dual_bound3/2及exact_dual_optimal=true。配合(2,1,0)取等给该固定锥精确值3/2；没有从一份自测冒推出全部任意p,m。此对偶已直接解码，不需重跑旧优化器。

# 文件使用、依赖与关系

main guard保护import；命令默认p7/path00112/portfolio23456/45秒，有可选threshold，output必填且已存在拒写。ROOT由脚本parents[5]指仓根，sys.path加入仓根及tests/audits；依赖customer_attraction、customer_attraction_strategy_lp、NumPy/SciPy及稀疏矩阵。输出以serializable保存有理数为字符串，并另打印删去大proof或大动作/dual的摘要；stdout不是完整证书。

本次原件全字节保存，JSON所有字段、全部2801+3动作及127+3克隆项均完成解析和语义核对，数据阅读程序只核保存结构/平凡理由，0原MILP/LP/随机扫描。见[证据](../../tools/evidence/boss3-c16-resumed/README.md)。关系可登记为“实现：计数子类→完整历史展开”“有限验证：自测及保存primal”“限制：历史净化反例排除全域推论”；不得把文件名7_5或status1当一个一般数学结论。
