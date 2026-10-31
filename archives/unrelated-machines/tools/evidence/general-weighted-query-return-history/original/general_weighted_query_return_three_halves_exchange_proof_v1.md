# 任意异权查询—返回接口的三半交换：作者 Proof v1

对应 Exact：`general_weighted_query_return_three_halves_exchange_exact_v1.md`，SHA256 `bda34c6f0abcbbb3fafad8fbadbec8c2e89f940ddef8e3a8f6d9ab92b04cbd41`。

作者 rainbow，2026-10-18。只在 clone 外冻结；先仅发 root，不直接给 Exact-only reviewer。旧各版本原字节不改。本证明严格扣除已存 `UM-TWO-WITNESS-QUERY-SEPARATION-v2`，不给一般 source-gap 或主目标结论。

## 1. 从两份完整真实 strict 调度提取所需内部部分

令 i≠j，写

    A' = A ∪ (R\{b_i,b_j})。

在给定原 σ_i 中，内部 jobs 恰 A'、b_j、q_i；在 σ_j 中，内部 jobs 恰 A'、b_i、q_j，二者全部原机实际峰≤T。

从 σ_i 仅删去 q_i 的内部执行，保留 A'、b_j 的原内部目的机，得到这些 jobs 的真实内部调度峰≤T，因处理时间非负。从 σ_j 保留 A'、b_i、q_j 的全部内部执行，同样峰≤T。以下这些删减仅为分析用子实例；第4节完整恢复原 P 的每枚其它任务，绝不将它们从最终调度遗漏。

## 2. 一个分析性完整实例及两份实际见证

建立分析性普通 UM P*，内部仍为原 H，jobs 恰为

    A' ∪ {b_i,b_j,q_j}。

对每个 A' job，仅保留它在 σ_i、σ_j 中实际使用过的原内部有限端；b_i、q_j 各保留其 σ_j 内部端，b_j 保留其 σ_i 内部端。所有保留时间沿用原 P 的真实值，不更改内部资格或处理时间。

另增三台仅用于分析的互异 outside 机 Z_i、Z_j、Z_b，与 H 不交。b_i 在 Z_i 时间0，q_j 在 Z_j 时间0，b_j 在 Z_b 时间0。A' 没有 outside 端，三 special jobs 没有其它 outside 端。P* 全部 jobs 均有实际合法端。

定义同一 P* 的两份完整实际调度 ρ_0、ρ_1：

- ρ_0 将 A'、b_j 放原 σ_i 的内部端，将 b_i、q_j 分别放 Z_i、Z_j。
- ρ_1 将 A'、b_i、q_j 放原 σ_j 的内部端，将 b_j 放 Z_b。

全部 P* jobs 均整件恰一次执行。内部负载由第1节的真实子分配界≤T，outside 时间0，所以两份完整 ρ 的实际峰均≤T。新增0端是证明中的辅助实例，不是原 P 的新合法端；最后输出原 P 时不在任何 Z 执行任务。

## 3. 两查询的支持不交迫一份保留 b_j

在 P* 上调用已经自足证明的 `UM-TWO-WITNESS-QUERY-SEPARATION-v2`，查询族取

    Q*={b_i,q_j}。

两枚 query 都从各自 Z 机的0端变到原 H 内部，所以都属于 owner 改变集 D。每个 query 的 δ 值（其它 query 在 ρ_0 的逐机初态负载最大值）均为0。已有定理因此输出两份完整实际 single-query 调度 τ_i*、τ_j*，二者峰都≤3T/2，并输出两两不交的非query改派支持 S_i、S_j⊆D\Q*。

τ_i* 恰将 query b_i 与 S_i 中 jobs 改用 ρ_1 端，其余用 ρ_0 端；τ_j* 恰将 q_j 与 S_j 改用 ρ_1 端。每份恰一个 query 内部化，另一枚仍在其 Z 的0端。此处引用的不只是费用平均，而是已有定理对具体原任务身份的**不交支持**合同。

b_j 是一个非query job，从 ρ_0 的内部端变到 ρ_1 的 Z_b。因为 S_i、S_j 不交，b_j 至多属于一个支持；所以至少一份 single-query 调度中 b_j 仍保持 ρ_0 的原内部端。检查两个输出，选这样一份；若两份都保留则按固定顺序选。

所有 A' jobs 在两份 ρ 的端都在 H，因此选中的 τ* 也把每枚 A' job 留在 H，不论其它辅助任务如何重排。只有 b_j 这枚非query有 outside 端，而它刚好被选定留内部。于是选中 τ* 的内部 jobs 精确为以下二者之一：

- 若选 b_i single-query：A'∪{b_j,b_i}=A∪R，即 inactive；
- 若选 q_j single-query：A'∪{b_j,q_j}=A∪(R\{b_i})∪{q_j}，即指定 mismatch(j,i)。

完整 τ* 的所有机器已同时≤3T/2；特别这些内部原机器同时受控。没有将不同机器的见证或期望分别拼接。

## 4. 恢复同一原 P 的全部 jobs 与 outside 真实负载

保持选中 τ* 内部每枚原 job 的 H 目的地，它们全部是原 σ_i / σ_j 实际使用过的原有限端。对原 P 中不在该内部模式的每枚边界 z，放原 P 自身 O_z，真实时间 T。辅助 A 全部已经在内部。

这一步包括分析实例没列出的 q_i、其它 Q jobs，以及未内部化的那枚 query；不能把它们仍放分析性0端或直接丢弃。原 R 在 inactive 情况全部内部，在 mismatch 情况只有 b_i 外部；原 Q 在 inactive 情况全外部，在 mismatch 情况只有 q_j 内部。这精确符合 Exact 的两种模式。

每枚原 N 件任务恰一次、全部原资格合法。内部每机负载与 τ* 相同≤3T/2；不同边界 jobs 的 O_z 物理互异且只有各自 z 可执行，所以每台原 outside 负载≤T。原完整 τ 的峰因此≤max(3T/2,T)=3T/2。所有分析性 Z 机器与未选 P* outside 放置均不作为原输出。

这证明精确二选一算法，而非仅存在内部投影。

## 5. inactive 禁止、反方向与存在量词

若 inactive 在峰≤3T/2 不可行，则二选一输出不可能是 inactive，故必为指定 mismatch(j,i)。交换 i,j 重新应用整个论证，得到 mismatch(i,j)。

如果所有 aligned strict 见证存在，且 inactive 在3T/2不可行，每个有序对都存在所述 mismatch。给出全部 k 份实际见证时，可对 k(k−1) 对运行算法得到全部输出；没有给出见证时，仅存在量词成立，本证明没有求未知 strict 调度的算法。

任意 B≥3T/2 若禁止 B 内 inactive，就更禁止3T/2内 inactive，而 mismatch 已在3T/2≤B存在。这准确否定同一封装接口的弱身份同步合同；不声称任意源 NO 具有所需 strict 见证，更不将两份见证当源 hardness。

## 6. 时间、零端、外部边界与技术归属

P* 的 jobs 数为 |A|+k+1≤N，机器数 |H|+3，所有新端时间0，其余数值来自原 P 与给定 T。有限内部时间可以异权、有0或>T，但两见证实际使用的内部端都≤T；本算法只在这些已核端之间选择。T>0是 Exact 前提，不作除以任何处理时间的操作。空 A、零端、unused machines 不造成例外；空 H 若有合法 aligned 实际输入则仍按同一论证，实际 k≥2 下这样的前件不可能。

既有查询分离定理的实现只需有限有理部分和、比较与其显式染色过程，按 P*、两份见证的总位长多项式。建立 P*、检查支持中 b_j、恢复全部 N 个原目的地与原 outside 时间T同样多项式。Dense 原矩阵全部 (|H|+2k)N 项必须计入读入；没有按时间值、T的倒数或分母数值展开，也无新增软件或有限枚举证明。

若 O_z 被真实共享变量 / clause 机器替代，恢复外部的第4步不再保证这些机器负载≤T，因此不能免费把局部 mismatch 拼成全公式调度。若辅助 A 也可外送，或者一个标签由多枚边界 query / return bundle 表示，b_j 不再是当前唯一可外送非query的精确合同，不能直接套用此证明。这些机制须另有真实全局解码。

本结论是已存 query-separation 的直接结构推论。新的可复用范围是任意异权单 query / 单 return 接口与 inactive / 指定 mismatch 二选一，不是新的 query-separation 算法、一般 UM 改进或 near-2 source。全球新颖性、外审与独立成文价值未认证，主目标保持 OPEN。
