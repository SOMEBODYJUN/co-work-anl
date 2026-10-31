# 任意异权查询—返回接口的三半交换：Exact v1

ID/version：`UM-GENERAL-WEIGHTED-QUERY-RETURN-THREE-HALVES-EXCHANGE-v1`。

作者 rainbow，2026-10-18。仅冻结真实对象、输入输出合同与范围，不含作者证明或证明策略，供独立 Exact-only 审查。仅 clone 外 scratch；未改 repo / Work / Git。旧单容量 v1、machine-uniform v2 的原字节及更强 strict 交换结论不变；本版允许任意异权，交换负载改为3T/2，故另立 ID。

## 1. 同一完整普通 UM 与所有原 jobs

给显式有限内部机器集 H、显式辅助原任务集 A，以及 Q={q_1,...,q_k}、R={b_1,...,b_k} 两族边界原任务，k≥2。A、Q、R 两两不交，各族内任务身份也不同。给正二进制有理数 T>0。

每个原 job 在 H 上的时间为任意非负二进制有理数或∞，可逐 job、逐 machine 完全不同；允许0、任意资格数、同机不同大小共居及内部有限端>T。没有内部预载或本合同之外的 jobs。每个 A job 至少有一内部有限端；各边界 job 可以没有内部端，这种情况可能令所需 aligned 见证不存在。

为使全部原任务及 outside 负载完全明确，给每个边界原 job z∈Q∪R 一台互异的私有原 outside 机器 O_z，与 H 不交；只有该 z 可在 O_z 执行，真实时间 T。A 没有 outside 端，边界 job 也没有其它 outside 端。这是本 Claim 的全部普通 P；jobs 总数 N=|A|+2k、机器数 |H|+2k≥1，其余有限端仅为已给内部资格。每件原任务必须整件且恰一次执行，不增加、删除、复制原 jobs。

对 X⊆Q∪R，模式 X 要求恰 X 中的边界 jobs 在 H 执行，其余边界 jobs 在自身 O_z；全部 A 在 H。模式可行始终指这个完整原 P 的全部 N 件任务有合法实际调度且峰不超过所述阈值。outside 机器每台最多接自己一件 T job，故每个模式的外部负载确定≤T。

H 允许空（此时 aligned 前件通常不可能），A 允许空，零内部端与各类不使用机器允许；上述定义仍给合法完整 UM，且不对∞作算术。

## 2. 给定两严格实际见证的精确二选一输出

定义 inactive 模式 X_∅=R；aligned_i 模式 X_i={q_i}∪(R\{b_i})；指定 mismatch(j,i) 模式 X_{j,i}={q_j}∪(R\{b_i})。这些模式读取具体原 q_i、b_i 的身份与实际内外目的地，不是 machine unit-presence。

输入还给不同索引 i≠j，以及同一完整 P 的两份已核合法实际完整分配 σ_i、σ_j：分别实现 aligned_i 与 aligned_j，且两者 C_max≤T。

**Exact Statement。** 存在确定性总位多项式算法，输出同一原 P 的一份完整合法实际 τ，并准确标明其实现以下至少一种模式：

1. inactive，即所有 R 在 H、所有 Q 在各自 outside；
2. 指定 mismatch(j,i)，即 q_j 与 R\{b_i} 在 H，b_i 与其它 Q 在各自 outside。

输出始终满足

    C_max(τ)≤3T/2。

全部 A 在 H，全部 N 件原任务各恰一次；所有真实原 outside 机同时负载≤T。内部目的地不需要新增资格：每个输出内部 job 的端点可以仅取它在两份对应输入见证中实际用过的内部端（存在该端时），不把见证以外的有限端当作额外前提。

不要求 inactive 或 mismatch 在 strict T 可行；本版不能替换旧 uniform 类的 strict T 交换。也不要求两份见证在其它原任务上的 owner 相同。

## 3. 禁止 inactive 后的指定错配及所有索引

若 inactive 模式在峰≤3T/2 时不可行，则上述算法必输出指定 mismatch(j,i)≤3T/2。交换 i,j 另运行一遍得到反方向 mismatch(i,j)。

若全部 k 个 aligned 模式在 T 都可行，而 inactive 在3T/2不可行，则每个 i≠j 的 mismatch(j,i) 都已在3T/2可行。如果实际提供全部 k 份严格见证，可以对全部有序对确定性多项式输出这些完整调度；若只知道见证存在，则这里只给对应存在量词，不声称可以计算未知 strict 调度。

同理，对任意显式弱阈值 B≥3T/2，若某局部合同同时要求所有 aligned strict 可行、inactive 在峰≤B禁止、并要求峰≤B的任何 query / return 必同编号，则该合同不可能成立：inactive 的弱禁止蕴含3T/2不可行，指定错配则在3T/2≤B已经存在。这是有限完整物理接口的存在性限制，不是给定源 NO 自动存在两份 strict 见证。

## 4. 外部封装与真正未覆盖范围

私有 O_z 仅把未在内部执行的原任务以及其负载写完整，不承担源标签约束。如果真实 compiler 将边界任务接到共享变量环、共享 clause 机器或其它外部锁定系统，本结论只保证内部模式的可替换性；换模式后那些真实共享机器的负载不在本 Claim 保证内，不能将它们免费视为 O_z。

因此本结论封闭的是：任意异权局部辅助网络，全部辅助 A 固定留内部，单个 q 被读入、单个 b 被返回，全部索引 strict 可选，并用 inactive 弱禁止来保证 OR。仅添加满足该准确合同的私有辅助 jobs，不能在 B≥3T/2 修复索引同步。它没有证明所有 global identity / block coherence compiler 不可能，也没有给一般 UM 或 source-gap 算法。

若辅助任务可跨不同局部网络/真实源机器外送、边界不再是每次一个 query 和一个 return、或源依赖额外不可分的共同外部负载，本 Claim 不自动适用。它也不假设输入只含两种时间、不要求 uniform slots 或行预算；同机异权本身已被纳入。

## 5. 位复杂度、依赖扣除与状态

算法输入包括原显式 P、T、两份实际完整见证及索引。给定见证可逐任务核资格、模式及全机有理负载；不合法输入可报告合同外。所有保证仅对上述合法输入，不将求未知 strict witness 的问题藏在多项式算法中。

运行时间与输出按原完整输入的总编码长度多项式；若使用 dense 矩阵就计全部 (|H|+2k)N 项，不能只按稀疏边声称线性。有限有理数0/正数、T、部分和与比较均用二进制精确算术，不按处理时间数值、T的倒数或分母展开任务。T=0不在当前 ID 域，零内部端则明确在域内。

唯一非平凡依赖是已在 current 正文自足证明的 `UM-TWO-WITNESS-QUERY-SEPARATION-v2`（`two_witness_query_separation.md`）及它的实际完整调度、不交非query改派支持合同。本 Claim 是该既有定理的直接结构推论，非新查询分离算法，不冒称全球原创匹配或一般近似突破。本 Exact 不附调用策略，以保独立陈述先行次序。

无软件、有限枚举、源 NP-hardness 或任意小δ的 NO decoder；未认证外审、全球新颖性及独立成文价值。真实 near-2 source 与 UM-TARGET-v1 仍 OPEN。
