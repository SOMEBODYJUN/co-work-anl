# 保护环外接 Ci/Rc/unit-clause OR 的全公式严格可行：冻结 Exact v1

ID: UM-PROTECTED-CYCLE-CIRCUIT-CLAUSE-OR-FAILURE-v1。
提出者：boss11 内部 typed_edge_gap，2026-10-18。本文件只含完整显式变体与待独立攻击的结论，不含作者证明。它与 root 的两个 D-pool/clause 共池变体不同。

## Domain 与实际矩阵 P

输入任意有限显式 CNF 公式 Φ。每个 clause c 有 k_c≥2 个 literal occurrences；允许同一变量重复、同一文字重复或同一 clause 同时出现正负文字，但每 occurrence 是不同的物理索引。变量只保留实际出现者。给有理 a∈(0,1)。如需与弱阈值 B∈[1,2) 的保护环合同相连，可额外选 a∈(B/2,1)；本结论声称所有 a∈(0,1) 都成立。

对每变量 v，把其所有真实 occurrences 任意排序成环，若少于3则添 dummy occurrences 使 n_v≥3。dummy 不属于任何 clause，polarity 任取。每个 occurrence i 有唯一变量 v(i)、环后继 i^+、环所用内部端口机器 M_i，及私有读出机器 C_i。所有 M_i、C_i 互异。

真实 occurrence i 的 polarity s_i∈{0,1}：0为正文字、1为负文字。记 pin(i)=M_i（s_i=0）或 M_{i^+}（s_i=1）。dummy 同样给 s_i 并定义 pin。

对每个原 clause c，再添一台私有机器 R_c。机器集恰为全部 M_i、全部 C_i、全部 R_c；记 N=Σ_v n_v、m=clause数，总数2N+m。

jobs 恰为每 occurrence 的 q_i、b_i，以及每 clause 的 u_c，总数2N+m。下列端有限，其余全部∞：

- q_i：M_i 时间a；M_{i^+} 时间1；C_i 时间1。若 i 是真实 occurrence 且属于 clause c，再增加 R_c 时间1。dummy q_i 没有 R 端。
- b_i：C_i 时间1；pin(i) 时间a。
- u_c：可在恰好该 clause 的所有 occurrence 私有机器 C_i（i∈c）上耗时1；没有 R_c 端，没有任何其它端。

所有 job 身份独立且只能安排一次。所有时间属于{a,1}且≤1，全部资格为原矩阵中的实际有限端，不用抽象 OR、外部预载、费用oracle或复制的 activation 位。

此变体的意图是：u_c 占某 C_j、迫 b_j 返回内部；每 R_c 因总 jobs/机器饱和由某 q_i 占据，尝试用 q_i@R_c 作为 clause 的真实任务身份读出。u_c 所选择的 j 与 R_c 上的 i 没有预设相等；这正是待检的物理编译步骤，不能作为额外约束免费加入。

## Exact Statement

对每个上述 Φ、任意 occurrence 排序、任意 dummy padding/polarity、任意有理 a∈(0,1)，整个显式 P(Φ,a) 总有完整实际调度 σ 满足

    Cmax(σ)≤1。

并且可在总输入位长的确定性多项式时间构造 σ，使每台机器恰一原 job。特别每 R_c 确实由该 clause 的某枚原 q_i 以其实际 unit 端占据，所有 clauses 都有真实 q_i 身份读出；却仍对任意 UNSAT 公式如此。

因此该 Ci+Rc+unit-clause-OR 变体不能保持源 NO：即使每个私有保护环在尚未外接 clause 时能精确保持二进制读出，新增本页的 clause 资格与 u_c 之后，返回 blocker 与导出 query 的身份可能错配，不能再沿用旧环 decoder。

这是这个明确变体的精确失败合同，不声称所有 near-unit identity copy、所有 medium 加权保护、其它共享 clause 结构或一般 UM 归约均不可能。没有 NP/ETH/UGC 假设；没有把“fractional调度”当实际输出。
