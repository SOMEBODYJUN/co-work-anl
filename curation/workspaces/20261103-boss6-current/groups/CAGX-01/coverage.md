# CAGX-01 数学覆盖说明（EF1 与 reserved-capacity）

## 结论先行

这张跨档审查页承载两条互不相同的数学陈述。

1. **完全多部图 EF1** 已有可直接复用的正式引理：
   `archives/fair-allocation/state/引理/完全多部图均匀最大EF1--引理.md`。
   它处理完全多部冲突图、统一基数价值、允许留空的 maximal partial allocation；通过最大 part 或最短前缀把每个 bundle 做成大小 1/2，得到任意正整数代理数的 maximal EF1。该引理的证明、复杂度和范围已自足，无需重写。
2. **保留容量小物品密度贪心** 目前只在
   `archives/bottleneck-knapsack/state/审查/退役GAP选题底稿与数学边界--审查.md` §C03 以辅助推导出现，还没有独立正式引理。它是单调子模单预算模型的标准密度贪心界，不能直接当作 Group GAP、BMKP 或任何 CAG/SPE 结果。若第二步要求两项都落正式数学正文，应在父 Boss 预留后把下面的 C03 说明抽成新 `state/引理` 页；本工作区先保留精确草稿。

## A. 完全多部图的统一价值 maximal EF1

### 输入与量词

冲突图是 complete multipartite，part 大小按
`s_1 >= ... >= s_k` 排列。物品须分配给 `n>=1` 个有标签代理，每个 bundle 是独立集，允许物品留在外面。每个代理的价值是 bundle 的基数（同一件物品对所有代理价值均为 1）。分配称 maximal，若任何未分配顶点都不能加入任一已有 bundle 或空 bundle而保持独立性。统一价值下，EF1 等价于已分配 bundle 的最大、最小大小相差至多 1（空 bundle 大小为 0）。

### 构造与证明骨架

令 `M=sum_i s_i`。

* 若 `M<n`，把物品各自给不同代理，剩余代理留空；所有物品均已分配，bundle 大小为 0/1，故 maximal 且 EF1。
* 若 `s_1>=n`，只用最大 part，把其中 `s_1` 顶点拆成 `n` 个非空 bundle，大小为 `floor(s_1/n)` 或 `ceil(s_1/n)`。其它 part 的顶点与这些 bundle 中任一顶点相邻，不能再加入；大小差至多 1。
* 若 `M>=n` 且 `s_1<n`，取最短前缀 `s_1,...,s_l` 使 `S=sum_{i<=l}s_i>=n`，且 `S_prev=sum_{i<l}s_i<=n-1`。对选中的 part `i`，选 bundle 数 `k_i` 满足 `ceil(s_i/2)<=k_i<=s_i`。由 `s_i>=r=s_l`，
  `sum ceil(s_i/2) <= S_prev-(l-2)floor(r/2)+(r mod 2) <= n`；从这些下界逐步增加 `k_i` 直到总数 `n`。每个 part 内分成 `k_i` 个大小 1 或 2 的 bundle。未选 part 的顶点与所有 bundle 相邻，因而不能加入；bundle 大小差至多 1，得到 maximal EF1。

排序、最短前缀、`k_i` 补足和按 part 输出均为显式顶点数的多项式时间；343,536 个 partition 检查只是实现核对，不是证明前提。

### 必须保留的边界

该引理只覆盖统一基数、complete multipartite 冲突和 maximal **partial** allocation。它没有推出任意 cactus/cograph/一般图的 equitable coloring，也没有异质 additive/monotone 价值、EFX、PO/WEFX、端点 goods/chores、copies SD-EF1 或六人共同目录 half 覆盖。来源状态是内部证明、未做外部新颖性认证。

## B. Reserved-capacity 小物品密度贪心

### 精确模型

有限物品集 `E`，成本 `c_e>=0`，单预算 `B>0`。目标函数 `f:2^E -> R_{>=0}` 单调子模，先假定归一化 `f(empty)=0`。每件成本至多 `delta B`，其中 `0<=delta<rho`；算法只允许使用保留容量 `rho B`（通常 `rho<=1`）。令 `OPT=max{f(T): c(T)<=B}`。

零成本物品先全部加入（单调性保证不损失）；对正成本物品，在当前成本不超过 `rho B` 的集合中，反复选取仍能放入保留容量的物品，按边际密度
`Delta_e(S)/c_e` 最大者加入；不能再放入时停止。返回集的成本自动不超过 `rho B`。

### 可复用保证与推导

若停止时 `c(S)<(rho-delta)B`，则剩余容量 `rho B-c(S)>delta B`，而每个未选物品成本至多 `delta B`，所以所有未选正成本物品都应可放入，和“不能再放入”矛盾。因此
`c(S)>=(rho-delta)B`。

设 `S_t` 为第 `t` 步集合，`g_t` 为所选物品，`O` 为最优集。密度选择和子模性给出

`f(O)-f(S_t) <= sum_{e in O\S_t} Delta_e(S_t)`
`<= (c(O)/c(g_t)) Delta_{g_t}(S_t)`
`<= (B/c(g_t)) (f(S_{t+1})-f(S_t))`.

于是缺口 `G_t=f(O)-f(S_t)` 满足
`G_{t+1} <= (1-c(g_t)/B) G_t`。连乘并用 `1-x<=exp(-x)`，结合 `sum_t c(g_t)=c(S)>=(rho-delta)B`，得到

`f(S) >= (1-exp(-(rho-delta))) * OPT`。

若 `f(empty)>0`，先用 `f'(A)=f(A)-f(empty)` 做归一化；由 `f(S)=f'(S)+f(empty)` 可把同一乘法界传回原函数。若有零成本正边际项，应先全取后再做密度比。

### 作用与缺口

这条界只说明单调子模、单预算、单物品成本上界和保留容量下的 density-greedy tradeoff。C03 原页明确它可能是标准知识，尚无 tight envelope、matching lower bound 或外部新颖性认证。它没有处理 Group GAP 的 all-or-nothing group 完成、多个 bin、bin-dependent profit、组内互斥或最终装箱舍入；不能把 `1-exp(-(rho-delta))` 与母文 1/6、候选 1/5 直接相乘后宣称总算法。

## 两条陈述为何不能合并

EF1 引理的对象是图独立集分配和代理间公平性；C03 的对象是可弃置物品的子模价值与容量约束。前者 bundle 合法性由冲突图决定，后者可行性只由一个标量预算决定。二者的“greedy/前缀拆分”字样不构成模型转换，也不能用于 CAG/SPE、加权拥塞、BMKP 或其它档案的量词迁移。

## 当前交付与后续

EF1 正式正文可按原字节复用；其 SHA256 应以当前文件计算。C03 在本草稿中已给出输入域、输出、保证、证明和边界，但正式登记前需父 Boss 对新 `state/引理` 路径执行 `extend` 后再写入；若不扩展，则只能把 C03 作为现有审查页的精确复用和未覆盖单元，不能把工作区说明冒充正式数学资产。
