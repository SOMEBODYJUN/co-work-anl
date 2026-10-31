---
id: "unrelated-machines/lovasz-schrijver-matrix-cones-setfunctions"
kind: "literature"
type_tag: "文献"
title: "Lovász–Schrijver：矩阵锥、N/N+层次与格上集合函数"
status: "complete-source-read-integrated"
truth_status: "primary-report-theorems-read; relaxation and separation results; not a claim about unrelated-machine hardness"
review_level: "full-38-page-report-read-with-definition-theorem-boundary-audit"
summary: "1989 报告把 0–1 锥提升到矩阵并投影，定义 N 与 N+ 操作；N 迭代至 n 层恢复 0–1 凸锥，固定层可分离。对 stable-set polytope，N 一层恰给非负、边和奇洞约束，N+ 一层覆盖 clique/odd-hole/odd-wheel/odd-antihole 与正交约束；随后用格的 Möbius 函数统一描述更高层。"
scope: "0-1 optimization, stable-set polyhedra, convex-cone liftings, Boolean/lattice set-functions"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/literature/unrelated_machines/lovasz_schrijver_1989_matrix_cones_report.pdf#全文"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/literature/unrelated_machines/lovasz_schrijver_1989_matrix_cones_report.pdf#全文"
source_ids:
  - "a8e1bb258e684814182b"
source_sha256: "79334a891179b60f78f6708401193616c657b05a53e021da8856f61977810b73"
source_version: "CWI Report BS-R8925, October 1989, 38 pages"
---

# Lovász–Schrijver：矩阵锥与 0–1 优化

## 来源和核心对象

本对象实际导出并通读冻结的 38 页 CWI Report BS-R8925《Cones of Matrices and Setfunctions, and 0-1 Optimization》。报告从一般 0–1 可行向量的凸锥 `K` 出发，讨论如何在 `(n+1)^2` 个矩阵变量中表达乘积 `xx^T` 的线性约束，再投影回原坐标得到保留所有 0–1 点的收紧。主要结果分三层：矩阵切割算子 `N/N+`，stable-set polytope 应用，及任意有限格上的集合函数/Möbius 统一描述。

这里的“优化可行”指给定一个固定层、且底层锥有多项式时间 separation 时，可用椭球法做线性优化；它不是把任意 0–1 问题变成多项式时间可解，也不是对不相关机 `R||C_max` 的困难性或近似比结论。

## §1 矩阵提升、投影和基本性质

把 `x_0=1` 的 0–1 向量嵌入 `R^{n+1}`，令 `Q` 为所有此类向量张成的锥，`K⊆Q` 为给定凸锥，`K_0` 为 K 中 0–1 点张成的目标锥。对 `K_1,K_2⊆Q`，报告定义矩阵锥 `M(K_1,K_2)`：矩阵 Y 对称，满足 `Y_{ii}=Y_{0i}`，并且每个 `u∈K_1`、`v∈K_2` 都有 `u^T Y v≥0`（等价于 Y 把 `K_2` 映入 `K_1`）。`M_+(K_1,K_2)` 在此基础上增加 Y 半正定。投影
\[
N(K_1,K_2)=\{Ye_0:Y\in M(K_1,K_2)\},
\quad
N_+(K_1,K_2)=\{Ye_0:Y\in M_+(K_1,K_2)\}
\]
满足
\[
K_0\subseteq N_+(K_1,K_2)\subseteq N(K_1,K_2)\subseteq K_1\cap K_2.
\]
常用简写为 `N(K)=N(K,Q)`；此时每列 Y 属于 K，第一列减任一列仍属于 K。线性锥 K1、K2 的极锥给出 `M` 的线性极描述；加入半正定后通常不再多面体，但仍是凸锥。

对 `N(K)`，每个坐标 i 的几何分解是
\[
N(K)\subseteq (K\cap H_i)+(K\cap G_i),
\quad H_i=\{x:x_i=0\},\;G_i=\{x:x_i=x_0\}.
\]
这说明 N 一步保留 0/1 面的分解结构，并产生部分 Gomory–Chvátal 型切割。定义迭代 `N^0(K)=K`、`N^t(K)=N(N^{t-1}(K))`；Theorem 1.4 证明
\[
N^n(K)=K_0.
\]
上界是维数 n，而非统一常数；证明按单位立方体的面维数归纳。报告同时给出极锥生成向量的判据，说明如何从底层 K 的有效不等式构造 N 层有效不等式。

若 K1、K2 为多面体，N 仍为多面体且面数可按两者面数乘积控制；N+ 包含半正定约束，通常非多面体。报告保留一个重要未知：Theorem 1.6 的某些完整性质当把 N 替换为 N+ 时未完全成立，不能把两层级混为同一算子。

## §2 stable-set polytope 的精确层次

对无孤立点图 G，`FRAC(G)` 由 `x_i≥0` 和边约束 `x_i+x_j≤1` 定义，`STAB(G)` 是稳定集指示向量的凸包。将其齐次化并套用 N 得到 `N(G)`；固定层的 separation 由底层显式线性规划与椭球法给出（Theorem 2.1：对每个固定 r，`N_r(G)` 与 `N_+` 均可多项式时间分离）。

报告 Theorem 2.3 给出一层精确刻画：`N(G)` 恰为非负约束、边约束和奇洞约束的解集。证明把矩阵变量的两两约束化成图上的 walk 系统；除奇洞外的 walk 由边约束闭合，唯一需要奇洞不等式的是两端在边集中的奇长度情形。由此 t-perfect 图的 `STAB(G)` 是多项式面数多面体的投影（Corollary 2.5）。

对一般有效不等式 `a^T x≤b`，定义 defect
\[
r=2\max\{a^Tx-b:x\in FRAC(G)\},
\]
它是整数且可由显式 FRAC 线性规划计算。若其 N-index 为最小 k（即该不等式首次在 `N_k(G)` 中有效），Theorem 2.13 给出
\[
\frac r b\le k\le r.
\]
这里下界利用 `k!2^{-k}\mathbf1\in N_k(G)`，上界按删除/收缩顶点并逐层降低 defect 归纳。报告进一步得到完全图、奇洞、奇反洞和 perfect/critically imperfect 图的 N-index 边界。

N+ 的强度不同。对 clique、odd-hole、odd-wheel、odd-antihole 约束，收缩正系数顶点后正支撑变成二部图，因此这些约束的 N+-index 都是 1（Corollary 2.15）；h-perfect（包括 perfect、t-perfect）图因此在一层 N+ 内得到。正交表示给出的 Lovász theta body `TH(G)` 也可写成满足对称、`Y_{ii}=Y_{0i}`、边项 `Y_{ij}=0`、Y 半正定的矩阵锥投影（Lemma 2.17），正交约束的 N+-index 为 1（Corollary 2.18）。若每个正系数支撑的独立数至多 r，则相应不等式 N+-index 至多 r（Corollary 2.19），固定 N+-index 的图上最大权稳定集可多项式求解（Corollary 2.20）。

这些结论的量词是固定层/指定图类；报告没有声称所有图的 STAB 都有常数层，也没有把“可分离的 relaxation”误说成原多面体本身已有多项式大小描述。

## §3 格上集合函数和 Möbius 结构

令 L 为有限格，zeta 矩阵 `Z_{ij}=1[i≤j]`，其逆 `M=Z^{-1}` 的条目是 Möbius 函数 `μ(i,j)`。对函数 f，若 `g=Mf`，则 `W_f=(f(i∨j))` 满足 Lindström–Wilf 分解
\[
W_f=Z\,D_g\,Z^T.
\]
报告称 f **strongly decreasing** 当且仅当 `Mf≥0`；等价地 f 是 zeta 列向量的非负组合、非负/单调递减/超模，并且 `W_f` 半正定。进一步，`x^T W_f x=\sum_i g(i)(Z^Tx(i))^2` 给出 Selberg-sieve 型平方和不等式。对 Boolean 格，f(∅)=1 时这一条件等价于存在一族随机事件，其交集概率为 f(X)。

格上的半群乘法 `a∨b` 使极锥闭合：若 `a,b∈cone(F)^*`，则 `a∨b` 仍在极锥；结合 Möbius 行向量得到有限层 `N_r` 的生成元。对 Boolean 格取兴趣集合为 `∅` 与单元素，投影 `cone(F)` 恰恢复通常 0–1 凸包；Theorem 3.3（与 Sherali–Adams 相关）给出任意集合族 `F⊆2^S` 的凸包是由 Möbius 不等式在高维空间中的投影。报告还说明矩阵锥是大 Möbius 矩阵的主子矩阵，Lovász theta 体与 N+ 是同一高维框架的不同投影/松弛。

对固定 r，`N_r(K)` 只需检查长度至多 r 的 Möbius 生成元，因此若 K 有 separation oracle，则 `N_r(K)` 也可分离；这里的多项式性依赖 r 固定，随着 r 增大变量和约束会迅速增长，最终恢复精确 0–1 锥但不保证常数层。

## 与本存档的关系和边界

本报告可为配置 LP、Sherali–Adams/N+ 松弛、Möbius 势和正半定证书提供历史来源锚点；它解释“高维 lift + 投影 + 固定层 separation”为什么能产生有效不等式，但不提供 `R||C_max` 的二近似算法、NP-hardness 或任何普通调度 decoder。当前不相关机正文若使用矩阵层次或 Möbius 反演，必须给出自己的对象域、输入位复杂度、层数及从松弛解到完整时间表的合同；不能因引用该报告就把 relaxation 当可行排程或原问题最优值。

与已有 `customer-attraction` 的 Möbius 正文无模型合并：后者研究六人 SPE 的策略/福利函数，本文献讨论 0–1 多面体和稳定集，不共享玩家/客户量词。与 `unrelated-machines` 中配置 LP 和高维匹配障碍对象的关系仅是“松弛/投影工具来源”，不是逻辑依赖；第三阶段可建立来源边，但不能把来源边当定理推导边。

## 证据、处置与接续

`a8e1bb258e684814182b` 的冻结 PDF 已实际导出、逐页通读（页 1–38），SHA-256 为 `79334a891179b60f78f6708401193616c657b05a53e021da8856f61977810b73`。两个冻结提交路径内容一致，来源合一；其独有内容（M/K 矩阵定义、N^n=K_0、stable-set 一层精确刻画、defect/N-index、N+ 与 TH、Möbius/strongly-decreasing 条件和固定层 separation 边界）均保留在本文。未执行报告外代码、未将历史引用升级为新的调度定理，也没有宣称外部同行评审。建议将该源逐源登记为 integrated（同一 PDF 的重复路径可标 duplicate），并在后续图中作为“来源”节点连接到使用 N/N+ 或 Möbius 工具的对象。
