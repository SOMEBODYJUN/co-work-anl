# 私有注入树共同分数证书：独立陈述先行重构审查

## 读取目的与隔离记录

本稿审查 `UM-Q-PRIVATE-INJECTIVE-TREE-FRACTIONAL-FLOOR-v1`。只先读了 Exact 文件：

`/workspace/scratch/038d9dcc4cac/private_injective_tree_fractional_floor/private_injective_tree_fractional_floor_exact_statement.md`

实际 SHA256：`aa3ed3a09e04d291b1266468af5814ffd8bd649cac4746514f60a79e791ecf54`。

冻结本稿前未读同目录作者证明，未向作者或 shared 询问证明思路。此前已经独立审查 typed balanced Latin 的共同 λ 配置证书及单状态全 leafmap 的注入性；这是来源披露，不替代本次一般私有树命题的证明。下文从本次 Exact 对象独立重构。

## 审查结论

未发现 fatal objection。所述一般存在性、数值条件及完整实际调度负载均成立。核心外部依赖是 Haxell 的有限二部均匀超图匹配充分条件；必须把本次每条超边的总顶点数记成 `r^h+1`，而不是分叉数 r。结论仅为存在性，不认证一般参数下的确定性位多项式构造。

本稿没有建立新颖性、外部复审、一般 UM 五三算法，或 UM-TARGET-v1 的反面。

## 对象、量词与前提

令 d,h≥1，U 为非空有限集合，每 u 有非空有限 S_u。每 (u,s) 的完整 d 叉高 h 树内部机器完全私有；全部 d^h 个叶 job 的外端映射 f_us 单射。共同 λ_us≥0 满足每 u 的 Σ_s λ_us=1，并且每 z 的共同外机容量为

\[
 \sum_{u,s}\lambda_{us}|f_{us}^{-1}(z)|\le 1.
\]

固定任意整数 1≤r≤d，记

\[
 k=r^h,\qquad b=(d-r+1)^h.
\]

需要审查的准确前提为 b≥2k−1。零权重状态仍是 P 的真实状态，不能删去其 jobs；下文最终调度覆盖这些状态。

## 1. 单状态精确 blocker 数

对满 d 叉高 h 树，命中每一棵满 r 叉高 h 根子树的最少叶数恰为 b。

独立归纳：高度零时只有一个叶，最小 blocker 数为 1。高度 t≥1 时，若某叶集 X 在少于 d−r+1 个根孩子下面阻断全部 r 叉高 t−1 子树，则至少 r 个孩子各有一棵避开 X 的 r 叉子树，合起来得到一棵避开 X 的根子树。因此必须在至少 d−r+1 个孩子下面各使用一个高 t−1 blocker。孩子叶域两两不交，得到下界 `(d−r+1)b_(t−1)`。反过来任选 d−r+1 个孩子并各放最小 blocker，任何 r 个孩子的选择必包含其中一个，故达到下界。于是 b_t=(d−r+1)^t。

单射 f_us 使上述叶 cardinality 与实际外机集合 cardinality 完全一致。这一步若没有完整状态内单射，不能按同一公式从叶 blocker 推到资源 blocker。

## 2. 有限超图及外部定理适用条件

构造二部超图 A=U，B=Z。对每 (u,s) 和每一棵满 r 叉高 h 子树 T，加入超边

\[
 e_{u,s,T}=\{u\}\cup f_{us}(\operatorname{leaves}(T)).
\]

每边恰含一个 A 顶点及 k 个不同的 B 顶点，因此总均匀度 R=k+1≥2。可能重复的超边可去重，并保留一份真实 (s,T) 见证。超图有限；显式列出所有超边不承诺多项式规模。

对任意非空 D⊆U，设 X⊆Z 命中所有 incident 于 D 的超边。每个 u∈D 的每个状态树都被 X 命中其全部 r 子树，故第 1 节给出

\[
 |f_{us}^{-1}(X)|\ge b.
\]

使用同一份共同 λ，得到

\[
\begin{aligned}
 b|D|
 &\le \sum_{u\in D,s}\lambda_{us}|f_{us}^{-1}(X)|\\
 &=\sum_{z\in X}\sum_{u\in D,s}\lambda_{us}|f_{us}^{-1}(z)|\\
 &\le |X|.
\end{aligned}
\]

所以 τ(E_D)≥b|D|≥(2k−1)|D|>(2k−1)(|D|−1)。空 D 时 τ=0，也严格大于负的右端。

Haxell 条件对总均匀度 R 的常数为 2R−3，此处正是 2(k+1)−3=2k−1。故得到覆盖全部 U 的匹配。它对每 u 选一条真实见证 (s,T)，并使不同 u 的全部选中叶资源全局不交。匹配同时保留同一个真实状态，而不是对不同叶各选状态。

### 外部定理的实际核查边界

亲读了研究者原始论文 Chidambaram Annamalai, *Finding Perfect Matchings in Bipartite Hypergraphs*, arXiv:1509.07007v2，PDF 第 2 页／印刷第 1 页的定义与 Theorem 1.1；PDF 第 3 页／印刷第 2 页的算法范围。

- 原始下载 URL：`https://arxiv.org/pdf/1509.07007v2`。
- 本地未改写 PDF：`/workspace/scratch/038d9dcc4cac/annamalai_2016_hypergraph_matchings_arxiv_v2.pdf`。
- 607189 bytes，SHA256 `f6294a3b497e98d870ab47ceecb4a94a7e80457e9777114f59d88f321bc7dcce`。
- 该文定义 r-uniform bipartite hypergraph 的边含一个 A 顶点及 r−1 个 B 顶点，τ 只允许从 B 选 hitting set；Theorem 1.1 明确复述 Haxell [1995] 的严格条件 `τ(E_D)>(2r−3)(|D|−1)`。
- Haxell 1995 原论文 *A condition for matchability in hypergraphs*, Graphs and Combinatorics 11, 245–248，官方 DOI 页面 `https://link.springer.com/article/10.1007/BF01793010` 及 PDF 路由转订阅预览。本次未取得、未声称亲读其原全文；这里亲核的是上述原始研究论文中的明确复述与适用定义。
- Annamalai 的算法 Theorem 1.3 要求固定总均匀度及额外正 ε 的加强条件，且其运行时间对这些参数为指数依赖。它不能从此处隐式超图直接给出全参数总位多项式算法；本审查不作此升级。

## 3. 从超图匹配到完整原 P 的实际 σ

每个 selector 放到为该 u 匹配选出的状态树根。对该状态的选中满 r 叉子树，恰把其树边 jobs 和末层叶 jobs 向下安排：内部端为时间 1，外机端也为时间 1。其余所有原树 jobs 统统放到自身父端，时间 1/d；这包括全部未选状态、全部未选分枝及 λ=0 的状态。

每个原 job 恰分配一次，且用原 P 允许端。负载逐类为：

1. 活跃内部机器：根有 selector 单位负载，非根有其唯一向下 incoming job 单位负载；恰 r 个 outgoing jobs 向下，所以另有 d−r 个 small 父置 jobs，负载为 `1+(d−r)/d=2−r/d`。
2. 非活跃内部机器：没有 selector 或 incoming unit；其 d 个 outgoing jobs 全部父置，总负载为 1。选中子树前缀闭合，故不会有非活跃机器的后代仍被活跃使用。
3. 外机：匹配保证所有被下送的叶资源全局不同，最多一枚 unit job，负载≤1。

因此完整 P 的实际 σ 满足 Cmax≤2−r/d。这里没有只计算叶资源，也没有遗漏未选状态的原任务。

## 4. 默认参数与退化情形

取 r=⌊(d+2)/3⌋=⌈d/3⌉。有 d−r+1≥2r−1。对 h≥1，函数 x↦x^h 在非负域凸，r 是 1 与 2r−1 的中点，所以 `(2r−1)^h+1≥2r^h`。因而 b≥2r^h−1。又 r/d≥1/3，故 Cmax≤5/3。

- d=1 时 r=1，k=b=1；超图是普通二部图，条件就是 Hall 的整数条件。选中链全下送，其他所有私有链 jobs 全父置，完整负载为 1。
- r=1 时每候选子树是一条根叶路径，k=1，超图总均匀度为 2；b=d^h≥1，条件合法。
- h=1 时精确 blocker 为 d−r+1，所有负载公式不变。
- r=d 的数值前提只有 d=1 才可成立；不对一般全分叉匹配作额外主张。
- U、菜单非空和 d,h≥1 是原陈述域；无需补入空根、空状态、h=0 结论。h=0 只作为归纳辅助基例。
- λ=0、共享外机在不同状态间重复、以及菜单大小或 rational 编码长均不破坏存在证明。

## 5. 范围与后续用途

此结果对所有满足共同 λ 与完整状态注入假设的私有树实例有效，不依赖外机映射来自 Latin、是否保色、随机 E、源值或局部标签语义。已核的 typed CONFIG 共同证书一旦与这些对象准确对接，就排除此类编译产生 OPT>5/3；这是一项方法范围限制。

没有证明全部配置可行实例满足该私有注入结构，也没有处理共享内部机器、非均匀处理时间、非注入叶映射或额外 jobs/preloads。有限超图存在定理不等于提供高效实际 σ 算法，本稿不标记 production implementation 或一般位多项式实现。

Status：Exact-first independent reconstruction completed；未发现 fatal；依赖定理已按上述亲读来源核条件；作者 proof 尚未读；无代码、有限实验或新颖性认证。
