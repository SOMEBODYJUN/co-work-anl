---
title: 非负列总量拟阵基逐行加 B 舍入
kind: theorem
status: 完整证明候选（来源独立重构；未实现代码）
stable_source_ids:
  - 112a866a20d86edaa77a
---

# 非负列总量拟阵基逐行加 B 舍入

## 对象与准确合同

设 (M=(E,mathcal I)) 是有限、显式可处理的拟阵，秩为 (r)。给定非负有理矩阵 (Ainmathbb Q_{ge0}^{m	imes E})、非负有理数 (B)，并假定每一列满足

\[
\sum_{i=1}^{m}A_{ie}\le B\qquad(e\in E).
\]

输入还给出一个有理分数点

\[
x\in B(M),qquad Ax\le b,
\]

其中 (B(M)=\{y\ge0:y(S)\le r_M(S)\ (S\subseteq E),\ y(E)=r\}\) 是基多面体，(b\in\mathbb Q^m)。目标是确定性位多项式地输出一份实际基 (I) 使

\[
A\mathbf1_I\le b+B\mathbf1.
\]

该对象只承诺逐行的加性 (B) 违约；不承诺成本保持、下界、目标值、一般 unrelated-machines 调度比、或实现完成。它也不把一个隐式、压缩而未展开的 parallel-copy 宇宙免费视作显式输入。

## 核心定理（受限但闭合）

在上述合同下，若拟阵具有一个可位多项式优化的显式线性表示，并且给定分数点的坐标投影顶点可以通过精确有理 LP 求得，则存在确定性位多项式算法输出基 (I) 满足

\[
A\mathbf1_I\le b+B\mathbf1.
\]

对本源的具体输入，(M) 是由显式二部匹配图定义的 transversal matroid 的 parallel extension：每个副本 (e) 有显式原元素 (pi(e))，同一 (pi)-类至多选择一个副本，原元素集可独立当且仅当能在二部图中匹配。所有副本均显式列入输入，因此其 extended formulation 的规模是输入长度的多项式。

### 1. 紧拟阵行的维数计数

取当前剩余拟阵 (N) 的一个分数基点 (y)，设所有剩余坐标严格位于 ((0,1))。紧拟阵不等式对应的集合族

\[
\mathcal T=\{S:y(S)=r_N(S)\}
\]

在秩函数次模性和 (y) 模性的共同作用下对并、交封闭。取一条不能再细分的链

\[
\varnothing=S_0\subsetneq S_1\subsetneq\cdots\subsetneq S_t=E,
\]

令 (D_j=S_j\setminus S_{j-1})。每个块非空且

\[
y(D_j)=r_N(S_j)-r_N(S_{j-1})
\]

是正整数，所以 (t\le r_N(N))。不可再细分保证每个紧集都是这些块的并；因此所有紧拟阵行的法向量都落在至多 (t\le r) 个块指示向量的线性包络中。基总量等式只再贡献一个已包含于 (E) 紧集中的方向，坐标上界在全分数点不紧。

### 2. 至少一条紧 upper row 的全选亏缺不超过 B

考虑当前残余多面体

\[
Q=B(N)\cap\{A'y\le b'\},
\]

其中 (A') 仍为非负且每列总量不超过 (B)。若所有坐标严格分数，元素坐标空间中的一个投影顶点需要 (n) 个独立紧法向量，而紧拟阵行至多贡献 (r) 维。因此至少有 (n-r\ge1) 条不同的紧 upper rows；记其集合为 (H)。对 (i\in H) 定义

\[
F_i=\sum_{e}A'_{ie}(1-y_e)\ge0.
\]

由于每列总量约束，

\[
\sum_{i\in H}F_i
 \le \sum_e B(1-y_e)
 =B(n-r) .
\]

故存在 (i\in H) 使 (F_i\le B)。删除该行是安全的：对于任何未来的 (0/1) 补全 (z)，有

\[
A'_iz\le\sum_eA'_{ie}=A'_iy+F_i=b'_i+F_i\le b'_i+B.
\]

这里仅用 (z_e\le1) 与非负系数，不需要预测未来基或未来 LP 顶点。

### 3. 迭代舍入

维护已固定集合、已删元素和仍保留的 upper rows。每轮在当前基面与 upper rows 的交中取一个元素坐标投影顶点：

1. 若某坐标为 (0)，删除该元素；若某坐标为 (1)，选入基并收缩该元素，同时扣减仍存 rows 的右端。
2. 若全部坐标严格分数，则按上节删除一条 (F_i\le B) 的紧 row。

固定坐标对应当前非空可行 face；删 row 只扩大可行域，所以算法不会失去可行性。每步至少删除一个元素或一条 row，至多 (|E|+m) 步。若 row 从未被删，最终基直接满足原约束；若 row 在时刻 (t) 被删，则

\[
A_i\mathbf1_{F_t}+A_iy_t=b_i,qquad
\sum_{e\in R_t}A_{ie}(1-y_{t,e})\le B.
\]

最终新增元素只是 (R_t) 的子集，故

\[
A_i\mathbf1_I\le A_i\mathbf1_{F_t}+\sum_{e\in R_t}A_{ie}
\le b_i+B.
\]

### 4. 显式 transversal/parallel-copy 实现

若原元素 (v\) 由给定二部图 (G=(L,V;E_G)) 定义，先用单位容量匹配流求原秩 (r_0)。对每个副本变量 (x_e\ge0) 和匹配流变量 (z_{\ell v}\ge0) 使用

\[
\sum_{\ell:(\ell,v)\in E_G}z_{\ell v}=\sum_{e:\pi(e)=v}x_e,
\quad
\sum_{v:(\ell,v)\in E_G}z_{\ell v}\le1,
\quad
\sum_{e:\pi(e)=v}x_e\le1,
\quad
\sum_ex_e=r_0.
\]

其 (x)-投影正是 (B(M))。整数流顶点给出恰选一个副本的实际基；在迭代中保留同一 extended formulation，仅添加 (x_e=0) 或 (x_e=1) 和当前 rows，不需要声称 contraction 之后仍有同一 matching presentation。

不能只取 extended LP 的任意顶点，因为 (x)-投影顶点未必是 extended 顶点。确定性实现是对尚未固定的 (x) 坐标按编号逐一做 lexicographic 精确有理最小化，固定每一步的最优值；最后 (x) 在当前投影中唯一，因而是所需投影顶点。LP 数量至多为多项式倍数，Cramer 行列式位界保证坐标和累计右端的位长仍为多项式。

## 锐性与边界

当 (B>0) 时，取秩一拟阵、(m) 个元素、(A=B I_m)、(x_e=1/m)、(b_i=B/m)。每列总量恰为 (B)，但任何实际基只选一个元素，在对应行产生

\[
B-B/m=B(1-1/m)
\]

的违约。因此不能把普遍的 (+B) 换成统一的 (+cB)（(c<1)）。这只证明加性常数的渐近锐性，不是一个下界复杂度或 NP-hardness 结果。

允许 (B=0)、空基、loops、重复 rows；当 (B=0) 时非负列总量迫使 (A=0)，可直接输出任意最大匹配基。所有输入是二进制有理数；算法不按 (1/B) 或系数倒数进行数值迭代。

## 与邻近对象的关系及未完成事项

- 这是显式基面上的逐行加性容量证书，使用拟阵紧行的维数计数；它不同于配置 LP 的预算舍入、BMKP 的利润保持舍入和 unrelated-machines 的 makespan 近似。
- 证明没有给出整数成本保持、目标函数保持、一般拟阵 oracle 下的实现，亦没有把 transversal 的显式扩展推广到压缩副本或任意隐式 matroid。
- 来源是独立重构稿，未提供已运行的软件实现或外部新颖性确认；正式正文因此标为“完整证明候选/算法接口已闭合”，不把未实现部分写成实验事实。
