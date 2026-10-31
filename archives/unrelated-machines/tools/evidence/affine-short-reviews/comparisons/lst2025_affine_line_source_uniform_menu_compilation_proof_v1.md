# LST 2025 仿射线源：pair-overlap／Hall 应用证明

候选 ID：`UM-LST2025-AFFINE-LINE-SOURCE-UNIFORM-COMPILATION-OBSTRUCTION-v1`。

2026-10-18，作者 Proof_v1，另于 Exact-first 文件冻结之后建立。对应 Exact：

`lst2025_affine_line_source_uniform_menu_compilation_exact_v1.md`

SHA256 `a1334a82f1acf7fd9562c2d44e6620b84b5a1acd37993ce3c7131b81a8e56472`。

本证明尚不发给仍在 Exact-only 阶段的独立 reviewer。本数学内容只是既有 pair-overlap/Hall 原理对实际 primary source 编译的应用，不主张新数学技巧。

## 1. 固定任意 local state 选择和任意 group 子族

沿用 Exact 的所有输入条件，尤其：group 是 indexed constraint；一个 state 是该 constraint 的一个允许 tuple；每 group 的变量恰为 k 个不同变量；每 variable 属于至多 R 个 indexed constraints；每 variable 的 incidence index `j_x(g)` 注入 F_R；不同变量资源用 tag 分离；每个非空菜单任意选 `s(g)`。

取任意子族 `F subseteq G`。对每个变量 x，令

\[
r_x=|F\cap G(x)|\le R.
\]

这里 r_x 是当前子族中涉及 x 的不同 indexed groups 数。它不是同一个 constraint 中 x 的重复次数，不计 indexed states 数，更没有把不同 allowed tuples 各自当作一个 group。

所选 state 在 U_x 内共给 r_x 条 R 点 affine lines。不同 constraints 的 intercept indices 不同，所以其中任意两条线都不可能重合。若 slopes 相同，它们平行不交；若 slopes 不同，解一个非零域系数的一次方程，恰交一项。因此任意两个所选 lines 的交集大小至多 1。

## 2. 变量内并集下界及整数配额

有限集合的前两项 inclusion-exclusion 给

\[
\begin{aligned}
\left|\bigcup_{g\in F\cap G(x)}E_{x,g,s(g)(x)}\right|
&\ge r_xR-\binom{r_x}{2}\\
&=r_x\left(R-\frac{r_x-1}{2}\right)\\
&\ge\frac{R+1}{2}r_x.
\end{aligned}
\tag{1}
\]

r_x=0 时两边均为零；任意多个 lines concurrent 只会使前两项容斥界更松，不会改变其方向。最后一步只用 r_x<=R，未要求 labels 一致。

不同 U_x 的资源身份分离，故相加得到整个资源邻域

\[
\begin{aligned}
|N(F)|
&\ge\frac{R+1}{2}\sum_xr_x\\
&=\frac{k(R+1)}2|F|.
\end{aligned}
\tag{2}
\]

中间计数 `sum_x r_x=k|F|` 使用每项 constraint 的 k 个变量互异，且每个所选 state 恰用这 k 个变量各一条 line。

令 `b=ceil(kR/2)`。因为整数 k>=1，

\[
b\le\frac{kR}{2}+\frac12\le\frac{k(R+1)}2.
\tag{3}
\]

所以对所有 group 子族 F，式(2)给 `|N(F)|>=b|F|`。capacitated Hall 或整数 maxflow 便给每 group 恰 b 项互不相交的真实资源，得到 Exact(A)。

具体 flow 网络使用 source-to-group 容量 b、group-to-member-resource 容量 1、resource-to-sink 容量 1。其可行整数流给真实 resource subsets；没有取 fractional items，没有要求 B_g 是 product 或每条 variable line 按同样比例领取。

## 3. 实际全部原 jobs 的完整调度

把每个 group selector 置于固定选中的 state machine。仅将该所选 state 中 B_g 的 incidence jobs 导出至各自 indexed resource machines，所有其余 incidence jobs 留在其自己的 private machine。

每 resource 因 subsets 不交而至多接一个 unit job，负载至多 1。每个未选 state 的全部 kR 件 jobs 均留 private，总量 `kR/(kR)=1`。每个所选 private 承 selector1 和剩下 kR-b 件 private incidence，负载为

\[
1+\frac{kR-b}{kR}=2-\frac{\lceil kR/2\rceil}{kR}\le\frac32.
\]

每个原 job 恰执行一次、每条目的资格均来自 Exact 定义，没有删除未选 state jobs，也没有把 partial allocation 本身当成完整 schedule。G 非空且 selectors 时间 1，所以真实 OPT>=1。这个 unconditional absolute schedule 因而也给该结构类至多 3/2 的 actual ratio。

## 4. 全满足 witness 与原 primary promise 不混淆

若一项原 CSP assignment 满足所有 constraints，对每 group 取其 restricted tuple。同一变量的所选 lines 全有相同 slope，而 incidence indices 不同，因此平行且两两不交。不同变量 tag 也不交，遂所有所选 state sets 不交。导出它们全部 jobs、其余 states 留 private，给真实峰 1；selector 下界使 OPT=1。

但 source §4 的 hardness promise 只给 YES CSP value `>=1-epsilon`，没有承诺所有 constraints 满足。因此上述 perfect witness 是额外条件，不由 source theorem 自动获得。本文的 unconditional 3/2 上界不需要这个条件，故不能拿 source 的普通 full-set matching soundness 来推出此 grouped partial compiler 的 near-2 NO。

这也没有改写 primary complexity 假设：这里实际查看的 source hardness 使用 `NP not subseteq BPP`，不是未经证明替换成 `P!=NP`。

## 5. 空关系、其它 grouping 和范围

当某 allowed relation 为空时，Exact 明确不定义该 group 的正常 selector compiler：仍放 selector 会无 eligible state，实例不可行。这种输入不满足“全部菜单显式非空”。若别的归约删除该 constraint 或增加 dummy，则必须另证 source completeness/soundness 和 target job 接口。本证明没有暗自处理它。

本页把 constraints 当 groups、allowed tuples 当 states。如果改成每个 allowed tuple 自成一个 group，再加全局 dummy choices，变量内可能出现来自同一 constraint、同一 incidence index 的多个已选 lines；此时 r_x<=R 和 intercept 注入不再按本证明成立。该不同 compiler 需要另行分析，不能引用本页的 3/2 数值。

同样，修改 uniform private weights、跨变量资源身份、加入其它 jobs 或一致性 gadget 都不在本证明中。本结果排除的是 Exact 的实际 grouped uniform 编译，既不否定原 k-Dimensional Matching hardness，也不证明所有 source-to-UM 归约不可能。

## 6. 显式构造复杂度和来源角色

构造时 R,k 的数值规模已在真实显式 resources/incidences 中计入。给定全部允许 tuple 表与 incidence indices，line 枚举、所选 state 的资源图以及上述整数流均在构造的显式规模内多项式。需求 b<=kR 以二进制容量存储，不进行更大隐藏数值复制。最终逐一输出 Exact 所列的 m+kR a 个原 jobs 的 eligible machine identifiers。

primary 的贡献在这里是一个真实已发表 large-gap full-set packing source 及其准确 affine-line/degree 参数。本文应用的 union 计数、ceil 处理、Hall 和 job reconstruction 是已有基础事实，不借 source 发表地位提升任何新 hardness 或新数学主定理。源 Exact 不改，未写 repo、Git 或 Work。
