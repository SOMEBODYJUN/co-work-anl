---
id: "unrelated-machines/uniform-cardinality-first-pair-fisher-yates-compression"
kind: "theorem"
type_tag: "定理"
title: "均匀定基数 Fisher–Yates 交换压缩"
status: "proved-scoped-independent-construction"
truth_status: "complete-scoped-mathematical-claim"
review_level: "full-source-read-and-cross-object-comparison"
summary: "给定显式 d,h，沿 Fisher–Yates 交换链逐阶段保持 first/pair 特征均值并作有理依赖消列，确定性输出至多 D=1+d+binom(d,2) 个真实 h-subsets 及有理权；只保 singleton/pair 边际，不保高阶矩或共同 assignment law。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_uniform_cardinality_pair_design_independent_reconstruction_v1.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_uniform_cardinality_pair_design_independent_reconstruction_v1.md"
related_objects:
  - "unrelated-machines/uniform-cardinality-first-pair-sparse-support"
  - "unrelated-machines/seven-state-star-global-quadratic-local"
legacy_ids:
  - "UM-UNIFORM-CARDINALITY-PAIR-FISHER-YATES-v1"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/uniform-cardinality-fisher-yates-20261031/original.md"
---

# 均匀定基数 Fisher–Yates 交换压缩

## 1. 结论和量词

给定显式整数 $d\ge1$ 与 $0\le h\le d$，令
\[
D=1+d+\binom d2.
\]
存在确定性算法（复杂度按显式 $d$ 计）输出至多 $D$ 个实际的 $h$-子集 $S_\ell\subseteq[d]$ 及非负二进制有理权 $w_\ell$，满足
\[
\sum_\ell w_\ell=1,\qquad
\sum_{\ell:i\in S_\ell}w_\ell=h/d,
\]
并且在 $d>1$ 时
\[
\sum_{\ell:\{i,j\}\subseteq S_\ell}w_\ell
 =\frac{h(h-1)}{d(d-1)}\quad(i\ne j).
\]
每个输出集合都保持大小 $h$；算法显式列出支持，不是抽样或未列集合的 separation oracle。复杂度只声称关于显式 $d$ 的多项式，不声称关于 $\log d$ 的多项式。

边界 $d=1$ 没有 pair 约束；$h=0$ 或 $h=d$ 直接输出唯一集合。

## 2. 交换链和特征的线性传递

对每个 $h$-子集定义
\[
\phi(S)=\bigl(1,(1_{i\in S})_{i\in[d]},
 (1_{\{i,j\}\subseteq S})_{i<j}\bigr)\in\{0,1\}^{D}.
\]
从 $S_0=\{1,\ldots,h\}$ 出发。对于 $i=d,d-1,\ldots,2$，均匀选择 $j\in[i]$，交换标签 $i,j$。这就是显式的 Fisher–Yates 链：每个排列有唯一的交换序列，故终点子集服从均匀的 $h$-子集分布。

任意标签置换 $\tau$ 只置换 $\phi$ 的 singleton/pair 坐标，故存在显式置换矩阵 $A_\tau$ 使
\[
\phi(\tau S)=A_\tau\phi(S).
\]
因此只要当前支持分布给出同一个 $\mathbb E[\phi]$，下一次交换后的 $\mathbb E[\phi]$ 也相同：交换阶段是线性算子
\[
\frac1i\sum_{j=1}^{i}A_{\tau_{i,j}}.
\]
这允许在每一阶段压缩支持而不改变最终的 first/pair 均值。

## 3. 只在已列候选上的有理压缩

若当前支持至多 $D$ 列，展开第 $i$ 阶段后至多 $iD$ 个真实 $h$-子集，权为旧权的 $1/i$。当候选列数 $N>D$ 时，在已列的 $\phi(S_\ell)$ 中用普通有理线性代数找到一个非零整数依赖
\[
\sum_\ell u_\ell\phi(S_\ell)=0.
\]
常数坐标保证 $\sum_\ell u_\ell=0$，所以依赖同时含正、负坐标；可取基本依赖，支持至多 $D+1$，其系数由 $0/1$ 子式的 Cramer/Hadamard 界确定。

将当前权写为 $a_\ell/Q$。选
\[
k\in\arg\min_{u_\ell>0}a_\ell/u_\ell,
\]
并置
\[
Q'=Qu_k,\qquad a'_\ell=a_\ell u_k-a_k u_\ell.
\]
则所有 $a'_\ell\ge0$，至少 $a'_k=0$，且
\[
\sum_\ell a'_\ell=Q',\qquad
\sum_\ell a'_\ell\phi(S_\ell)=Q'\sum_\ell a_\ell\phi(S_\ell)/Q.
\]
删去零权列并重复，最终回到至多 $D$ 个真实支持点。整个过程从未引入未显式列出的子集，也没有优化任意二次目标。

## 4. 位长和时间范围

每阶段候选数至多 $iD$，阶段总候选和消元次数为多项式量级（粗界 $O(d^2D)$ 次依赖消除）。依赖系数来自维数 $D$ 的 $0/1$ 子式，位长由 Hadamard 界控制；分支时只乘以 $i$，消元时只乘一个依赖系数。因而共同分母、所有中间分子以及输出权均有关于显式 $d$ 的多项式位长。用标准确定性有理线性代数完成依赖搜索、比较和更新，得到确定性 poly($d$) 算法。

这里的复杂度证明需要逐阶段维护至多 $D$ 支持；若每个父状态都重新递归而不缓存，不能直接推出总多项式时间。本构造本身是单条 Fisher–Yates 交换链，避免了枚举全部 $\binom dh$ 个子集。

## 5. 在七态行配置中的准确用法

若某个固定 $(C,H)$ 类别只需要均匀 $H$-子集的 first/pair 边际，可在该类别内用上述支持替换原均匀 slice；当 $C=1$ 时附上指定的 incoming job。每个配置仍是合法真实配置，$H$ 不变，行负载不变；由于类别内 $C$ 固定，$CY_i$ 以及所有 $Y_i,Y_iY_j$ 的 first/pair 也保持。按类别混合时，支持规模可取至多类别数乘 $D$（七态星的六类即至多 $6D$，按实际非零类别缩减）。

该替换只提供 row CONFIG 的 first/pair 证书。它不保持三阶或更高阶矩，不生成七态原星所用的共同 assignment law $L$，也不能替换 global degree-two localizer、共同 $M_3$ 或固定次数矩生成；这些仍须使用原均匀子集 law。它也不推出一般 unrelated-machines 调度算法、近二 gap、hardness 或六人半覆盖结论。

## 6. 与既有递归稀疏支撑对象的关系

既有《均匀定基数 first/pair 稀疏支撑》同样给出至多 $D$ 支持和 poly($d$) 有理权，但采用二分块、超几何混合和候选列上的基本有理 LP。当前来源的独有内容是 Fisher–Yates 交换链、$A_\tau$ 对特征均值的逐阶段线性传递，以及直接在每阶段展开候选后消列的独立构造。两种方法量词和边界相同；当前来源不引入更强的高阶矩保持或更小的支持上界，也没有软件运行证据。故保留为同一数学对象的独立构造附录，不能把它误记为与递归定理相同字节的 duplicate。

## 7. 处置与接续

建议对源 `b8137e324aa77306db69` 采用 `integrated`，目标为本页；同时在既有稀疏支撑正文中保留交叉链接。后续若需要可实现证据，应单独编写并运行 Fisher–Yates/有理消列程序；本源只有数学构造，没有作者代码或有限审计输出。任何依赖高阶矩、共同跨行 law 或 growing-depth 接线的论证都必须继续引用原均匀 law 并重新证明，不能由本稀疏支持替代。
