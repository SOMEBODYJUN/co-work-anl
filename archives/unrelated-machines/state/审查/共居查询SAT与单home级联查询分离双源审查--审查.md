---
id: unrelated-machines/direct-cohabiting-query-and-single-home-cascade-review
kind: review
title: 共居查询SAT与单home级联查询分离双源审查
status: complete-source-read-integrated
scope: "direct cohabiting query/return strict-SAT bridge, sharp 3/2 escape, and single-home cascade query separation"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/direct_cohabiting_query_return_strict_sat_and_sharp_escape.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/direct_cohabiting_query_return_strict_sat_and_sharp_escape.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/single_home_cascade_query_separation.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/single_home_cascade_query_separation.md
source_ids:
  - 75907aeeb2a6c9fb95c6
  - 225ef3334a360f0e3f0d
inventory_sha256:
  75907aeeb2a6c9fb95c6: 3e6ac499c73cf5c084ed5623ede2cb921214192c8f5e3aa9f859ecdc80147607
  225ef3334a360f0e3f0d: 679f77588505455e5810e2c8e6e147274d0cddef6eff05bb383fce67945d49d1
---

# 阅读范围与身份

本批完整读取两个当前正文，并将其与 `near_unit_implication_pcsp_and_physical_copy_obligation.md`、`unit_presence_two_witness_sharp_gluing.md`、`partial_minrep_linear_degree_source_and_fee_bridge.md` 以及已有查询分离/级联审查比较。两个来源都研究把源约束或查询身份编译进 unrelated-machines 的实际任务，但适用合同不同。第一源是直接共居的 query/return SAT 桥：严格峰值一保留 SAT 等价，弱端却能在所有公式上构造三半调度，并在固定半权时得到精确三半阈值。第二源假定同一矩阵已经给出两份严格见证，研究单个正小端、任意深级联和非查询 unit 费用能否被简洁地分摊到所有查询。两者都没有解决一般 `UM-TARGET-v1`，也没有为六人 SPE 的覆盖目标提供结论。

稳定身份是 `UM-WEIGHTED-DIRECT-COHABITING-QUERY-RETURN-ALL-FORMULA-FAILURE-v1`、`UM-DIRECT-COHABITING-SAT-COMPILER-SHARP-THREE-HALVES-v1` 与 `UM-SINGLE-HOME-CASCADE-QUERY-SEPARATION-v2`。v2 明确强化了旧 v1：同一批不交支持要同时实现全部子集查询，并另外记录剩余查询质量 (delta(S))。

# 一、直接共居 query/return SAT 桥

## 1. 矩阵、量词和严格 SAT 等价

源输入是显式有限 CNF。每个 clause 至少有两枚 occurrence，重复文字和重复变量允许；每个变量的 occurrences 排成环并补 dummy 至环长至少 3。每个索引 (i) 有两台不同原机器 (M_i,C_i)，两个原任务 (q_i,b_i)，每个 clause 另有 (u_c)。给 (1/2<\rho<1)，真实索引给 (x_i,y_i>0)、(x_i+y_i\le1)，dummy 固定 (x_i=1)。端点只有：(q_i) 在 (M_i) 时间 (
ho)、后继 (M_{i^+}) 时间 1、(C_i) 时间 (x_i)；(b_i) 在固定极性 `pin(i)` 时间 (
ho)、(C_i) 时间 1；(u_c) 在 clause 中每个 occurrence 的 (C_i) 时间 (y_i)。全部任务不可拆、无预载、未列边不可用。

严格实际峰值不超过 1 当且仅当原 CNF 可满足。正向给定变量赋值：每个 clause 选一枚满足 occurrence，把 (q_i) 导出到 (C_i)、(b_i) 放到其 pin、(u_c) 放同一 (C_i)，其余 (q_i) 沿变量环方向放到 (M_i) 或 (M_{i^+})，剩余 (b_i) 留在 (C_i)。每台 (M) 恰一件时间至多 1，选中的 (C) 的 (q+b) 质量为 (x_i+y_i\le1)。

反向从任意峰值不超过 1 的完整分配读取身份：(M) 至多接一件 (q/b)，令 (E) 为 (q_i) 在自身 (C_i) 的索引，(R) 为 (b_i) 在 pin 的索引。因为 (x_i>0)，(E\subseteq R)；而 (M) 的总任务数给出 (|E|=|R|)，所以 (E=R)，每台 (M) 恰有一个环任务。由环计数 ((1-z_i)+z_{i^-}=1)，每个变量整环方向一致。每个 clause 的 (u_c) 不能与 unit (b_i) 共居，只能读取同编号导出的 (q_i)，得到一枚真文字。因此严格端的 SAT 等价是完整推导，不依赖有限枚举。

## 2. 任意异权的共同三半调度

对任意正异权参数，不需要源赋值或未知严格见证。把存在某个 (y_i\le1/2) 的 clause 设为 baseline，其余 active clause 的 (y_i>1/2)，所以这些 occurrence 的 (x_i<1/2)。构造一个只用于分析的二部图：左侧为所有 (q_i,b_i) 和 active (u_c)，右侧为所有 (M_i,C_i) 以及 active clause 标签 (V_c)；(q_i\) 只连两个环端和 active 的 (V_c)，不连 (C_i)。按 (1/2) 流量分配两环端，再以 (\theta_i=1/k_c) 调整到 active 标签，给 (b_i) 在 pin/C 之间补足，给 active (u_c) 分到各 (C_i)。这是同一份 fractional perfect matching，整数容量网络给一个共同 perfect matching。

将匹配中到 (V_c) 的 (q_j) 改回其自身 (C_j)，恢复所有 baseline (u_c)，得到完整实际任务分配。每台 (M) 至多一件；baseline (C_i) 负载至多 (1+y_i\le3/2)；active 返回 pin 的 (b_i) 所在 (C_i) 仅承载相应 (u) 与 (q_i) 的 (x_i)，总和不超过 1；其余 (C) 不超过 (1+x_i<3/2)。因此所有公式（包括 UNSAT）都有确定性位多项式 (3/2) 调度。关键失败机制是弱端只保留“某个 active clause 选到某个 q”而丢掉了 q 与该 occurrence 的同编号关系；virtual 标签不进入最终调度，不能被误写成物理机器。

这项结果的准确范围是具体共居矩阵和任意正异权；它不否定其他同机异权接口，也不从 strict SAT 等价推出接近 2 的困难性。所有 dense 端点和有理分母都显式计入复杂度，算法不按 (1/x_i) 或分母数值展开。

## 3. 固定半权的锐三半阈值

当全部真实 (x_i=y_i=1/2)、dummy (x_i=1)、且 (3/4<\rho<1) 时，另一个稳定身份给出精确结果：非空 SAT 实例的真实 OPT 为 1，非空 UNSAT 实例的真实 OPT 为 (3/2)。上界把 (q_i) 留在 (M_i)、(b_i) 放 (C_i)，每个 (u_c) 任取真实 (C_i)，故每台 (C) 至多 (1+1/2)。

若完整峰值 (C<3/2)，则 (2\rho>3/2) 强制每台 (M) 至多一件 (q/b)，而 (q_i+b_i) 在 (C_i) 恰为 (3/2)，所以所有 (2N) 个环任务必须在 (2N) 台机器上恰一件。由此恢复与上一节相同的环方向；每个 clause 的 (u_c) 不能与 (b_i) 共居，只能读同编号 (q_i)，于是 (C<3/2) 可解码 SAT。对于 UNSAT，这给出下界；对于 SAT，strict 构造给上界。非空 OPT 的下界 (1) 还需单独说明：若 (C<1)，任意 clause 的 (u_c) 所在 (C_i) 若有 (b_i) 则至少 (3/2)，若有真实 (q_i) 则它不能承载 (u_c)，矛盾。

因此该固定半权族是一个真实整数的精确 (3/2) gap，而非“某次有限搜索找到 15/10”的猜测。现有小例枚举只作交叉核验，不代替环计数证明；它也没有转化成任意 ((2-\varepsilon)) hardness。

# 二、单正小端级联查询分离

## 4. v2 的精确合同

给显式 unrelated-machines 矩阵，任务分为 (U,J)。每枚 (u\in U) 的有限端全部为单位时间；每枚 (j\in J) 有唯一正小端 (h(j)) 时间 (a_j\in(0,1))，其他有限端只能是 0 或 1。输入同一矩阵上的两份完整调度 (\sigma_0,\sigma_1)，都满足峰值不超过 1；(\sigma_0) 把所有 (J) 留在各自 home，给定非空查询集 (Q\subseteq J)，(\sigma_1) 将所有 (Q) 放在单位端。令 (D) 是 (\sigma_1) 上单位端的 (J)，(Z) 是其零端的 (J)，则 (Q\subseteq D)、(Q\cap Z=\varnothing)。

对 (S\subseteq Q) 定义未激活查询在每台机器的残余小负载
\[
\delta(S)=\max_i\sum_{q\in Q\setminus S:h(q)=i}a_q,
\qquad \delta=\delta(\varnothing).
\]
正文给出同一组两两不交 (A_q\subseteq D\setminus Q)，对每个 (S) 输出完整调度 (\tau_S)，使实际走单位端的 (J) 恰为 (S\cup\bigcup_{q\in S}A_q)，(Z) 固定在 (\sigma_1) 的零端，其余 (J) 回 home，且
\[
C_{\max}(\tau_S)\le1+\delta(S)\le1+\delta.
\]
若 (c_q=\sum_{j\in A_q}w_j) 是任意给定非负费用，则
\[
\mathrm{fee}(\tau_S)=\sum_{q\in S}c_q,qquad sum_{q\in Q}c_q\le W,
\]
其中 (W) 是全部非查询单位任务费用。于是同一构造同时支持全部子集查询；这不是分别为每个 (S) 求一份可能不相容的调度。

## 5. 单 parent 可达域的构造和证明

把每个 (d\in D) 画为 (h(d)\to\sigma_1(d)) 的带任务弧，删掉全部 (Q) 弧得到 (H)。每个查询根 (r_q=\sigma_1(q)) 入度为零；因为 (\sigma_1) 是单位任务匹配，根的可达域 (R_q) 两两不交，且不会进入有向圈。令
\[
A_q=\{d\in D\setminus Q:h(d)\in R_q\}.
\]
给定 (S)，在 (R(S)=\bigcup_{q\in S}R_q) 内沿 (\sigma_1) 弧使用单位任务；(U) 任务若其 (\sigma_0) 端在 (R(S)) 就改用 (\sigma_1) 端，否则留在 (\sigma_0)；(Z) 使用零端，其余 (J) 回 home。每台 (R(S)) 机器恰有一枚选中单位任务，且这些目标互异。若机器 (i\in R(S))，其 (\sigma_1) 已占一个单位任务，能留在 (i) 的查询小任务最多是 (Q\setminus S)，故负载至多 (1+\sum_{q\notin S,h(q)=i}a_q\le1+\delta(S))；域外机器负载不超过 1。这给出负载和费用公式。

证明允许任意多级 home→unit 级联、平行弧、自环和 U 任务的全局重排；只用同一矩阵的两份严格见证，不需要查询 home 互异或为每个 home 单独付费。图规模和所有输出按显式弧数及有理位长多项式，零端任务保留为原生零负载。

## 6. 费用分离的确切解释和边界

非负费用的可加性只描述这族构造产生的支持，不等于最优费用函数可加。如果每个 home 的查询小负荷至多 \(\eta\)，而某个候选编译器声称单查询在峰值 (1+\eta) 内必须支付至少 (F>0) 的非查询单位费用，则 (\sum_qc_q\le W) 强制 (W\ge|Q|F)。这说明“同一标签只支付一次、随后无限复用”的级联机制在该合同下无法成立。

本结果依赖两个完整严格见证、唯一正小端、\(\sigma_0) 全部小任务在 home、\(\sigma_1) 的单位任务目标互异、给定的费用对象和残余负载阈值。多正小端、\(\sigma_0) 已预先导出、仅有峰值 (T_0>1) 的见证、a_j=0、不同收费对象或不满足单 parent 结构的输入均需另证。(\delta=1) 时统一界可能达到 2；不能把该族写成固定改善。

# 三、关系、用途和开放义务

1. 直接共居源把“严格 SAT 可解码”与“弱端全公式 (3/2) 调度”放在同一实际矩阵上，准确说明同机异权和 clause 共居不足以制造接近二的困难性。固定半权版本进一步给出精确 (3/2) 阈值，属于原模型反例/障碍，而非一般 hardness。
2. 单 home 级联源保留更多查询任务身份和同一矩阵的两份严格见证，并把所有子集模式一次性构造出来。它适合检验共享标签费用和多级级联的解码义务，但没有提供寻找两份见证、从源输入生成其结构或优化任意费用的算法。
3. 两源不可相互替代：第一源的 SAT 环方向和 clause unit 约束不是第二源的单 parent 可达域；第二源的费用分解也不能修复第一源弱端丢失的 occurrence 同编号关系。旧摘要不能自动升级成共同物理任务合同。
4. 后续若要继续近二路线，需明确哪一项假设被放宽：允许多个正小端、只给一个近严格见证、加入跨 home 共享容量，或要求从未知源 assignment 生成两份实际调度。每种变化都需重新证明负载、任务身份、费用支持与复杂度。
5. 两份来源都没有关闭 `UM-TARGET-v1`、没有证明一般近二困难性，也没有触及六人 SPE 的“完整历史纯 SPE 覆盖至少半数主题”目标。清洗结果的完成含义是稳定身份、完整量词、正反机制、证据范围和可接续义务均已准确保留。

# 处置记录

两个来源均已通过 `clean show` 完整阅读；与相关 current/review/证据对象比较后，直接共居源归入 query/return SAT 与 sharp 3/2 障碍，单 home 源归入级联查询分离与费用支持。成熟证明、反例机制、有限审计和开放条件均保留，没有将有限枚举、作者见证或审查摘要代替一般数学证明。
