---
id: "fair-allocation/complete-multipartite-uniform-maximal-ef1"
kind: lemma
type_tag: 引理
title: "完全多部图均匀最大 EF1"
status: "internally-proved-with-scope; no-novelty-certification"
truth_status: "proof-checked-in-source-report; finite-implementation-audit-only"
summary: "在 complete multipartite 冲突图、统一基数价值和允许留空的 maximal partial allocation 模型中，任意正整数代理数都有大小差至多一的 maximal 分配；证明为前缀分拆，未外推到 cactus/cograph 全类。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/lanes/fair.md#已完成的证明"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/multi_lane/research/topic_selection/lanes/fair.md#已完成的证明"
source_ids:
  - "e341a8cf73b1d0385717"
source_sha256:
  - "5bda1ca4fab88dda59d3274e4cd82e7b2a568cbff74183b8abb21c64fcfd782c"
related_objects:
  - "../审查/近似公平分配首轮候选池与边界--审查.md"
  - "../资料/可加公平与副本前缀目标的候选反例分层--资料.md"
---

# 模型

冲突图是 complete multipartite 图，其 part 大小为
`s_1 >= s_2 >= ... >= s_k`。物品必须分给 `n>=1` 个有标签代理的 bundle，bundle 必须是独立集，
允许物品不分配。每个代理的统一价值为 bundle 的基数。分配称 **maximal**，若任何未分配顶点都不能
加入任何已有 bundle（或尚有的空 bundle）而不违反独立性；称 **EF1**，若任意两个代理的 bundle
大小在删除被比较 bundle 中至多一件后不再产生基数嫉妒。在统一价值下，EF1 等价于已分配 bundle
大小的最大值与最小值之差至多 1（空 bundle 也按大小 0 计）。

# 命题

对任意 complete multipartite 图和任意 `n>=1`，存在一个 maximal EF1 分配；给定显式顶点列表和
part 划分，可在输入位长多项式时间内构造。

# 证明

记 `M=sum_i s_i`。

**情形 1：`M<n`。** 把每个顶点单独给不同代理，其余代理留空。所有物品都已分配，因而 maximal；
每个 bundle 大小均为 0 或 1，EF1 成立。

**情形 2：`s_1>=n`。** 只使用最大 part，把其中 `s_1` 个顶点分成 `n` 个非空 bundle，大小为
`floor(s_1/n)` 或 `ceil(s_1/n)`。同一 part 内无冲突，所以 bundle 合法；其他 parts 的任一顶点与
这 `n` 个 bundle 的每个顶点都相邻，不能加入任何 bundle。所有代理非空且大小差至多一，故 maximal EF1。

**情形 3：`M>=n` 且 `s_1<n`。** 取最短前缀 `s_1,...,s_l` 使

\[
S=\sum_{i=1}^{l}s_i\ge n,
\qquad S_{\rm prev}=\sum_{i<l}s_i\le n-1.
\]

这里 `l>=2`。令 `r=s_l`；由于序列非增，前缀中每个 `s_i>=r`。对 part `i`，若要把它的全部
`s_i` 个顶点切成大小仅为 1 或 2 的非空 bundle，允许的 bundle 数正好是

\[
\left\lceil{s_i\over2}\right\rceil\le k_i\le s_i.
\]

只需证明可以选择 `k_i` 使 `sum_i k_i=n`。上界 `n<=S=sum_i s_i` 已由前缀定义给出。对下界，
对 `i<l` 使用 `s_i>=r`，把每个 `ceil(s_i/2)` 的最坏值按 `r` 估计，得到

\[
\begin{aligned}
\sum_{i=1}^{l}\left\lceil{s_i\over2}\right\rceil
&\le S_{\rm prev}-(l-1)\left\lfloor{r\over2}\right\rfloor
       +\left\lceil{r\over2}\right\rceil\\
&=S_{\rm prev}-(l-2)\left\lfloor{r\over2}\right\rfloor+(r\bmod 2)\le n.
\end{aligned}
\]

最后一步：若 `l=2` 且 `r` 奇，右式为 `S_prev+1<=n`；若 `l=2` 且 `r` 偶，右式为 `S_prev<=n-1`；
若 `l>=3`，减项使右式不超过 `S_prev+1<=n`。因此从每个 `k_i=ceil(s_i/2)` 开始，逐个增加某个
`k_i`（每次增加一件大小 1 的 bundle）即可把总数补到 `n`，并且始终不超过 `s_i`。

对每个选中的 part，按所选 `k_i` 把其顶点分成 `k_i` 个大小 1 或 2 的 bundle。未选中 part 的全部顶点
都与每个已构造 bundle 相邻；由于 `sum_i k_i=n` 且每个 `k_i>=1`，所有代理都有非空 bundle，
故未分配顶点不能加入任何 bundle。每个 bundle 大小为 1 或 2，最大值和最小值差至多 1，统一价值
下即为 EF1。命题得证。

# 算法与复杂度

排序 part 大小、找最短前缀和、计算各 `ceil(s_i/2)` 后逐个补足 `k_i` 即可。分组时同一 part 内任意
顶点均不相邻，可线性输出 bundles。所有计数是显式顶点数的整数，运行时间和输出空间为
`poly(M,n)`；没有按数值权重或指数枚举。报告中的 343,536 个分拆实例测试是实现核对，不是本证明的前提。

# 适用范围和缺口

该命题只处理统一基数价值、complete multipartite 冲突和 maximal **partial** allocation。它不能推出：

* cactus、cograph 或任意图上的 maximal equitable partial coloring；
* 异质 additive/monotone 价值、EFX 或 PO/WEFX 兼容性；
* 端点 goods orientation、rank-2 chores 或 copies SD-EF1；
* 任何关于六人共同目录半覆盖的结论。

它的接续用途是为候选 F03/F04 提供一个模块级测试：若模块合成不能保留“每个已选 part 的 bundle 数
区间”，应给出最小障碍，而不能把本引理的前缀分拆误当 cactus 全类证明。来源没有声称该引理的
外部新颖性，当前状态保持内部证明、范围清楚。
