# 私有 clause 查询—返回网络的全公式三半上界：作者 Proof v1

对应 Exact：`private_clause_query_return_universal_three_halves_exact_v1.md`，SHA256 `21b334eec1ca8af9e368604552d93dd5b36eff9b75738e97db07f7097035fd2c`。

作者 rainbow，2026-10-18。仅 clone 外冻结，先只发 root；未经 root 解封不直接给 Exact-only reviewer。本证明使用已冻结任意异权三半交换与旧共同匹配技术，不回写旧来源或冒称新的查询分离/匹配算法。

## 1. 空公式与局部完整测试封装

空 Φ 按 Exact 输出一台 idle 原机与空调度，实际 OPT0。以下非空，所有原对象与第2节资格严格按 Exact，不增加真实机器或真实任务。

固定 clause c。建立一个只用于调用局部交换定理的完整测试封装：真实内部部分正是原 H_c 与原 jobs A_c、Q_c、R_c；每枚边界 q/b 再接其独有 outside 测试机，时间T，辅助 A_c 没有 outside 端。这些测试机器不在最终实际 P 中。

给定 λ_{c,i} 完整覆盖内部 A_c+q_i+(R_c\{b_i})、峰≤T。把该模式其它边界 jobs 全放各自 outside 测试机，真实时间T，得到测试封装内全部 jobs 的 actual strict aligned_i 调度。由此局部交换定理的两完整实际见证前件完全满足，不是只给一个分数点或未知源赋值。

## 2. 可计算分类与所有所需模式库

对 c 的全部 ordered pairs i≠j，按固定次序运行 `UM-GENERAL-WEIGHTED-QUERY-RETURN-THREE-HALVES-EXCHANGE-v1`，以 aligned_i、aligned_j 为输入。每次实际输出 inactive 或指定 mismatch(j,i)，峰≤3T/2。

- 若任一次输出 inactive，令 c 为 baseline，保存该输出在 H_c 的完整内部 assignment，并停止处理该 clause。保存的内部原 jobs 恰 A_c∪R_c，所有 q 均不在 H_c。
- 若所有 ordered pairs 均没有输出 inactive，令 c 为 active。每个有序对都已获得 mismatch(j,i) 的完整实际内部 assignment；对 j=i 另保存输入 λ_{c,i}。因此 active 模式库对任意 query j 与 return i 都有一份 H_c 内部原 assignment，负载≤3T/2，实际覆盖恰 A_c+q_j+(R_c\{b_i})。

k_c≥2 使 ordered pairs 非空。这里没有求解任意异权 inactive 可行性，也没有把不可行性判定作 oracle：只看局部构造实际返回的模式。即使某个 active 的 inactive 实际也可行，仍不影响它已经拥有全部 cross 模式库的事实。

所有保存的内部目的地都是原 H_c 有限端，全部 A_c 固定在内部。丢弃测试 outside 目的地时尚不宣称全局负载可行；下面单独为原变量环确定所有边界 jobs 的真实外部目的地。

## 3. 原变量环上共同选择 query / return 的分析图

令 active clauses 集为 C_1，h=|C_1|。建立一个纯组合二部图，并明确与实际 P 区分：

- 左侧 labels 为全部原 q_i、b_i，以及每 active c 的一个 virtual demand label w_c。
- 右侧 labels 为全部原 ring 机 M_i、每索引一个 virtual label K_i、每 active c 一个 virtual label V_c。

两边均2N+h。K_i、V_c、w_c 都不是原 P 的机器或任务，只为选择边界模式，最终不执行。图边为：

1. 每 q_i 可到 M_i、M_{i^+}；若真实 i 属于 active c，再可到 V_c。没有 q_i→K_i 边。
2. 每真实 b_i 可到其原 pin(i) 或 K_i；dummy b_i 仅可到 K_i，符合它最终不返回原 ring 的限制。
3. Virtual w_c 可到该 active clause 的全部 K_i。

特别 baseline/dummy K_i 在此图只有 b_i 一个邻居。这个图只记录资格与任务数量，下面分数值都是无权 matching 质量，**不是**实际 UM 处理时间或可分执行。

对 active i∈c 取 θ_i=1/k_c≤1/2，其余 θ_i=0。给图上的同一全局 fractional perfect matching：

- 每 q_i 的两个 ring 端先各质量1/2，从其 pin(i) 对应端扣 θ_i，再向 V_c 放 θ_i（只对 active i）。
- 每真实 b_i 向 pin(i) 放 θ_i、向 K_i 放1−θ_i；dummy b_i 向 K_i 放1。
- Active w_c 向每个 i∈c 的 K_i 放 θ_i。

所有值非负，每个左侧 label 总质量1。每 M_i 原有相邻两个 q 的基数质量1；每从 q 的某 pin 端扣 θ_i，都恰被同编号 b_i 的 pin 质量补回，因此该原机的 matching 总质量恰1。每 active K_i 为1−θ_i+θ_i=1，baseline/dummy K_i 为1；每 V_c 收 Σ_i1/k_c=1。

于是这是同一个完整 fractional perfect matching。对任意左侧 labels 子集求质量和，右侧容量1推出 Hall；确定性整数匹配得到同一图上的一个 perfect matching。不枚举所有 subsets，也不把 fractional 质量输出成调度。

## 4. 整数 matching 强制的真实外部模式

该同一 perfect matching 同时具有：

- 每 M_i 恰接一枚原 q 或真实 b；dummy b 没有 ring 边。
- Baseline/dummy K_i 只有 b_i 邻居，故 b_i→K_i；对应 q 没有 V 资格，必取自己的 ring 端。
- 每 active V_c 恰接一枚 q_{j(c)}；这恰是该 clause 唯一读入内部的 query。
- 每 active w_c 恰取某 K_{r(c)}。该处 b_{r(c)} 不能也取 K，故返回 pin；反向任一 active b 不取 K 时，它的 K 只能由本 clause 的唯一 w_c 占据。因此每 active clause 恰一枚真实 b 返回，其索引为 r(c)。

所有返回 pins 与 ring 上其它 q 的实际 destinations 已在这个共同 matching 中互不冲突；没有分别为每个 clause 独立选一个看来可用的 pin。每台 ring 机恰一件，是后续真实外部负载界的承重事实。

## 5. 用原模式库回填所有实际 H_c / ring / dummy 机器

现构造最终原 P 调度 τ，完全消去所有 virtual labels 与测试机器：

1. Baseline c：使用第2节保存的 inactive assignment，把全部原 A_c、R_c 放各自原 H_c；该 clause 全部 q 按第3–4节 matching 所选的真实 ring 端执行。
2. Active c：取模式库中的 query j(c)、return r(c) assignment，在原 H_c 执行恰 A_c+q_{j(c)}+(R_c\{b_{r(c)}})。实际 b_{r(c)} 按 matching 指定的原 pin 执行；该 clause 其它 q 按 matching 的原 ring 端执行。
3. 每 dummy q 按 matching 所选原 ring 端执行；每 dummy b 在其唯一原 D_i 以时间T执行。

这些步骤按实际 job 身份互斥且覆盖全部原 2N+a 件任务：每 A_c 一直在自身 H_c；每真实 q 或在唯一被选 H_c、或在 ring；每真实 b 或在 H_c、或在唯一原 pin；dummy 两 jobs 也各一次。Virtual w_c/K_i/V_c 不是真实执行对象，从未补入实际 jobs 清单；不存在遗留的 outside 测试执行。

逐台真实机器核负载：

- 各 H_c 使用保存的同一实际内部 assignment，峰≤3T/2。H_c 两两私有且与 ring / dummy 私有机不交，因此不同 clauses 的内部回填不会互相增加负载。
- 每原 M_i 恰执行一个 matching 指定的原 q 或真实 b，该原端在 Exact 中有限且时间≤T，故全部 ring 机同时负载≤T。这个界来自真实共同选择，而非免费引用测试 outside≤T。
- 每原 D_i 只有自身 dummy b，负载T。

所以完整实际 C_max(τ)≤3T/2。源 Φ 是否 SAT、变量环顺序、内部异权或0端都没有参与 source 解求解。

## 6. 无证书时的存在量词与反面范围

若仅假设每个局部 aligned 证书存在，可以在数学上为有限多 (c,i) 任选一份，再应用上述构造，故同一全局 actual 上界仍存在。不据此声明可从原 P 找到未知 strict 局部 witness；计算结论明确把它们作为显式输入。

若某 compiler 对每个源 Φ 均给上述私有接口、所有索引 strict 局部可选，则每个输出 P（包括源 NO）都满足 OPT≤3T/2。即使该 compiler 另证明 SAT YES 的全局 OPT≤T，也不能对 NO 宣称 OPT>(2−δ)T、δ<1/2。该反证是所有原 jobs 的真实调度上界，不依赖 LP gap、两份源 NO 的假 strict 调度、NP 假设或某个坏 greedy。

若 A_c 可以到 ring / 其它 clause，或不同 H_c 共享真实机器 / jobs，则第5节私有内部回填不再自动可叠加。若模式不再为单 q / 单 b，或并非全部索引 strict 可选，则第2节完整库也不一定得到。若 q 的外部资格不是自己变量环两有限端、b 不是指定单 pin，第3节 matching 选择不一定对应原端。这些都是准确未覆盖出口，不从本 Proof 推出任意 global gadget 或所有 identity compiler 不可能。

## 7. 显式位复杂度与技术扣除

原 P 的计数为机器 N+H+d、jobs2N+a、finite条目3N+E_int，dense条目 (N+H+d)(2N+a)。每 q 两个 ring finite端计2N，每个真实 b 的单 pin 与每个 dummy b 的唯一 D 端合计N，内部 finite资格计 E_int。

局部分类最多 Σ_c k_c(k_c−1)≤L² 次交换调用，每次测试封装只复制原局部机器 / jobs / 给定有理时间并加2k_c个时间T的测试端。旧查询分离及局部三半交换都按完整显式输入位长多项式；模式库输出规模仍多项式。分析 matching 只有2N+h个左右 labels与线性于N+L的资格，θ分母为 k_c、位长 O(log L)，整数 matching 多项式。

最后逐原 job 输出一个原机编号、按原真实处理时间回算全部负载亦多项式；不按某个 p 的倒数、T/s、分母或隐式 padding 数值展开。原 finite时间>T 只可能不在局部 strict 输入所用端，对调用与输出合法性无害。Empty Φ 单列保证普通 UM 至少一原机。

本证明是任意异权局部三半交换与旧保护环共同匹配的直接组合。查询分离、匹配与 Hall 都是既有技术；新增的准确合同是任意私有 clause 辅助网络与原变量环的完整实际组合上界。无新软件或有限枚举前提、外审、全球新颖性或主 near-2 困难性认证；越出该范围的真实 source 问题保持 OPEN。
