---
id: "unrelated-machines/vw2010-theorem12-backend-precheck-20261031"
kind: "review"
type_tag: "审查"
title: "VW2010 Theorem 12 双端价值后端与新桥接口预核"
status: "integrated-literature-backend-precheck"
truth_status: "published-two-approximation-backend-with-explicit-interface-boundaries"
review_level: "full-source-note-read-and-pdf-page-verification"
summary: "完整读取来源预核记录，并按记录实际渲染、核对 Verschae–Wiese 2010 configuration-LP PDF 印刷页 9–10（PDF 页 10–11）的 §5.1、Lemma 11、Theorem 12 及证明。可安全复用的是最多两正支持端点的 MaxMin-balancing 2-approximation 后端：对阈值 T 成功只给 T/2 分配，失败才给 OPT<T 证书；forced-largest、双匹配交替环和二分保证整数值下的 1/2。新 weighted-menu bridge 的 Exact/Proof 尚未读，因此接口条件不外推。"
source_refs:
  - "source:e33be1ed06ad83cde424:history/source/notes/unrelated_machines/vw2010_theorem12_backend_precheck.md"
legacy_ids:
  - "UM-VW2010-THEOREM12-BACKEND-PRECHECK-v1"
related_objects:
  - "unrelated-machines/configuration-lp-two-positive-endpoint-backend"
  - "unrelated-machines/weighted-menu-state-dummy-sc-value-bridge"
---

# 1. 来源与阅读范围

`clean show` 导出的来源 `e33be1ed06ad83cde424` 位于 `history/source/notes/unrelated_machines/vw2010_theorem12_backend_precheck.md`，5,198 bytes，SHA-256 为 `557ab3d25b7eadb9fc63bf64005586001b5a0523a7db9eca7b00464ffdf09d88`。本页逐段读取该来源，并保存原文到 `archives/unrelated-machines/tools/evidence/vw2010-theorem12-backend-precheck-20261031/original/`。

来源记录的底层文献是 `verschae_wiese_2010_configuration_lp_v1.pdf`，其 SHA-256 为 `2a5ec312fb443928b3801af830006b41ef94f4da7f9759bdab22b16a59a88a7a`。实际阅读的是 PDF 页 10–11（印刷页 9–10），包括 §5.1、Lemma 11、Theorem 12 及证明，并用 fitz 渲染两页核对图像；系统 `pdftoppm` 因缺少 `libpoppler.so.160` 未使用，也未修改 PDF。此处处置的是来源后端预核记录，不能声称本轮重新审查整篇文献。

# 2. Theorem 12 的精确语义

模型是 MaxMin-balancing：每个 item/job 至多有两个能够接收其正价值的 agent/machine，且两个端点的价值可以不同。对正整数阈值 `T`，后端 oracle 的二值语义是：

- 成功：构造一个每个 agent 价值至少 `T/2` 的完整分配；
- 失败：证明不存在每个 agent 价值至少 `T` 的完整分配，即 `OPT<T`。

成功并不证明 `OPT≥T`，所以该 oracle 的 success predicate 不是精确的 T-feasibility。二分接口必须保存“成功只给下界一半、拒绝才给严格上界证书”的区别，不能把成功当作精确可行性。

# 3. forced-largest 预分配

对 agent `i`，令 `A_i` 是当前仍可分配的双端 items，`B_i` 是已强制归属 `i` 的 items 加上原本唯一正端属于 `i` 的 items。将 `A_i` 按 `i` 端价值降序排列，`A'_i` 删除当前最大 item。

若 `value_i(A_i)+value_i(B_i)<T`，任何 T-分配都不可能存在，直接拒绝。若总和达到 T 但 `value_i(A'_i)+value_i(B_i)<T`，当前最大 item 必须给 `i`：否则即使给 `i` 其余全部 item 也达不到 T。这是逻辑 forced step，不是一般贪心近似。

强制后必须把该 item 加入 `B_i`，并从两个端点的 `A` 列表全局删除；只在 `i` 端删除会错误地让另一端继续使用同一 item。每次强制删除一个仍为双端的 item，次数至多为 item 总数；`A_i` 为空时只能检查 `B_i` 总量，不能读取不存在的最大项。若停止且未拒绝，每个 agent 都满足
\[
value_i(A'_i)+value_i(B_i)\ge T.
\]

# 4. 双匹配配对与 1/2 下界

剩余每个双端 item 建两个 occurrence 顶点，并以“同一 item 的两个端点”连成第一种匹配。对每个 agent 的降序 occurrence 列表按 `(1,2),(3,4),…` 配成第二种匹配。两类边的并图最大度为 2，分量是偶数长度的交替环（退化路径按相同规则处理）。固定顶点顺序后，用 deque BFS 二染色即可；将每个 item 的黑色 occurrence 所在 agent 作为 owner，保证每 item 恰分配一次、每个 local pair 恰取一枚 item。

设 agent `i` 的剩余价值为 `p_1\ge p_2\ge\cdots\ge p_r`。配给 `i` 的 pair 价值至少为
\[
p_2+p_4+\cdots\ge \frac{p_2+p_3+\cdots+p_r}{2}
=\frac{value_i(A'_i)}2,
\]
因为 `p_2\ge p_3,p_4\ge p_5,…`；奇数个 occurrence 的最后未配对项只增加价值。加上 `B_i` 后，最终 agent 价值至少
\[
\frac{value_i(A'_i)}2+value_i(B_i)\ge T/2.
\]
这给出失败/成功语义中的 1/2 保证。

# 5. 二分、整数化与位复杂度

整数值情形令 `U=min_i sum_j v_{i,j}`，则 `OPT≤U`，`T=U+1` 必拒绝。低端从 0 开始并保存一个零保证完整分配，高端设为已知拒绝的 `U+1`。中点成功时保存其 `T/2` 分配并提高低端；拒绝时降低高端。无需假设 success 在 OPT 上方单调：每次拒绝都有严格证书 `OPT<T`，所以高端始终大于 OPT。结束时高端=低端+1，整数性给出最终低端至少 OPT，保存分配价值至少 `OPT/2`。`U=0` 时直接返回合法完整分配。

非负二进制有理数可乘共同分母 `D` 变为整数；分母乘积或 lcm 的位长受输入分母总位长多项式控制，缩放后的 `U` 位长也受输入总位长多项式控制。二分次数是 `O(log(U+1))`，而不是按数值 `U` 线性枚举；精确整数加减、比较、排序和图遍历给出位复杂度的多项式实现。任意精度整数、确定性排序、active-item 标志、force queue 与 deque BFS 足以实现；未经单独实现分析，不能把朴素版本冒称文献引用的精确 `O(|I|^2)` 时间。

# 6. 新桥接口的条件、候选与缺口

该后端只有在新桥明确下列条件时才能接入：agent 集非空；价值非负；每 item 的正支持端至多为 2；singleton 与 zero-support items 的分配规则；完整原任务的保留规则；`OPT=0` 的收尾；以及后端 agent value 与目标调度峰值的关系。来源明确尚未收到新 weighted-menu bridge 的 Exact，也未读作者 Proof；本页不猜测这些条件已经成立，不实现新桥，不声称一般 unrelated-machines 改善。

# 7. 处置

处置为 **integrated**：把已发表来源的双端 MaxMin-balancing 2-approximation 后端、forced-largest 逻辑、双匹配 BFS 证明骨架和二分位复杂度接口纳入正式数学正文；同时保留成功/失败非精确语义和新桥待确认的边界。该页不把预核记录升级为新 bridge 的完成证明。
