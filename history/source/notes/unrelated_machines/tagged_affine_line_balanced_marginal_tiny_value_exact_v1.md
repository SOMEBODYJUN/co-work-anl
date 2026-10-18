# Tagged affine LINE：单变量均匀边际但实际 partial value 趋零

ID：UM-TAGGED-AFFINE-LINE-BALANCED-MARGINAL-TINY-VALUE-v1。

作者：内部 rainbow_gap_source，2026-10-18。此文件仅为 statement-first Exact；不含作者证明。仅 scratch，先交 root。它是原 tagged affine-line 资源表示中的显式实际反例族，不是 hypercube slice 反例，也不是 Chan/LST 原 PCP hard image 或新 NP-hardness。

## 1. 域、资源及完整菜单语义

令 R≥3 为素数，在 F_R 上运算。对每个带标签的变量 x 建互不相交的资源块 U_x={x}×F_R²。一个 group g 若参加变量 x，给定固定 intercept b_x(g)∈F_R；同一变量参加的不同 groups 的 intercept 必须互异。state s 在该变量给一个 slope label a_{g,s}(x)∈F_R，并包含完整 tagged line

L_x(a,b)={(x,z,az+b):z∈F_R}。

state 资源集是其各变量整条 line 的不交并。每个 state-resource incidence 有显式非负有理 private 权 p_{g,s,u}；每个 state 的权总和恰1。允许并保留权0 incidences；正权并不等于完整几何 line。

partial allocation 每组选一个 indexed state，领取其资源集的任意子集，跨 groups 资源互异；所得质量是该 state 在所领资源上的 p 权和。记最大最小质量为 V。所有 group 的 indexed state 数均恰 R。给定的局部分布均为这 R 个 states 的均匀分布；“uniform marginal”指对每个 incidence (g,x) 和每个 a∈F_R，Pr_s[a_{g,s}(x)=a]=1/R。

## 2. 基础实例的精确对象

变量为 {u_a,v_a:a∈F_R}，全部带不同变量标签。groups 为一个 main group M 及 H_{a,j}，其中 a∈F_R、j∈F_R\{0}。main 的 arity 为 R；每个 helper 的 arity 为2。

M 参加所有 u_a，且 b_{u_a}(M)=0。M 的 states 以 t∈F_R 编号，在所有 u_a 上 slope label 均为 t。定义

B_a={(u_a,z,az):z∈F_R\{0}}。

M 的 state t 的正权恰放在 B_t，每点权1/(R−1)；该 state 的其余完整 line incidences 均为0。不同 B_a 属于不同变量块，因此互异。

H_{a,j} 参加 u_a 及 v_a，在两个变量的 intercept 都为 j。其 states 以 ℓ∈F_R 编号，labels 为

a_{H_{a,j},ℓ}(u_a)=ℓ，
a_{H_{a,j},ℓ}(v_a)=ℓ−a−j。

若 ℓ≠a，此 state 唯一正权为1，位于

(u_a, j/(a−ℓ), a j/(a−ℓ))。

若 ℓ=a，此 state 唯一正权为1，位于 (v_a,1,0)。所有其它完整 line incidences 权0。上述非零分母的逆在 F_R 中取；本定义不会对0求逆。

每变量的实际 groups 名单与 intercept 如下：u_a 参加 M（intercept0）及全部 H_{a,j}（intercept j≠0），度恰R；v_a 只参加全部 H_{a,j}（intercept j≠0），度R−1。没有其它变量 membership。

## 3. 待独立核查的精确结论

对每个 R≥3 素数，上述对象合法，每个 state 权总和1，每个 incidence 的局部 slope marginal 均匀，变量度至多R，且

V=1/(R−1)。

结论量化全部 state choices、全部 partial allocations，并非只核某个固定选择。达到该值的见证可确定性总位多项式构造；允许每个 helper 自由选择其 indexed state，且所有非所选 main block 的 helpers 也必须获得同样的正质量。不存在“helper 已预先绑定某个 B_a 点”的额外约束。

## 4. 完整 ordinary UM 实例及实际最优值

每个 indexed state 各一台不同 private root M_{g,s}；每个 tagged resource 各一台 resource machine R_u。每个 group 一枚 selector J_g，在该组全部 state roots 上时间1，其它机器∞。每个 state-resource incidence 一枚不同 job I_{g,s,u}，在自己的 private root 时间 p_{g,s,u}，在 R_u 时间1，其它机器∞。所有 indexed states、所有完整 line incidences（包括0权）及所有 selector 都保留；没有额外预载、虚拟任务或外部模式条件。

此完整 P 的实际最优 makespan 为

OPT(P)=2−1/(R−1)。

达到该值的完整实际 schedule 可确定性总位多项式构造。下界覆盖所有实际完整 schedules，包括未选 states 向 resource machines 额外导出的 jobs。这里使用的归一化量是绝对 unit scale；未声称该族带来任何近似困难性。

## 5. 可选共同 arity R、R-partite 显式 padding

若需所有 groups 共同 arity R，可作以下确定 padding，且保持上述 V、实际 OPT、全部 uniform incidence marginals 和变量度界。parts 以 c∈F_R 编号；u_a 属于 part a，v_a 属于 part a+1。

对每个 helper H_{a,j}、每个 c∈F_R\{a,a+1}，添加只属该 helper 的 fresh variable w_{a,j,c}，放在 part c。其 intercept 为0；helper state ℓ 在该变量的 slope label 为ℓ；这条完整 line 的全部 R 个新 incidences 权0。其它旧对象不变。main 原已每 part 一变量；padding 后每个 helper 亦每 part 恰一变量。每个 fresh variable 度1，没有额外 groups 或 selectors。

此 padding 只保证共同 arity 与 partite 结构，绝不把局部分布变成 pairwise independent。主关系是一个一维 diagonal，helper 两个旧变量 labels 为确定性 affine 关系；padding 后新变量也确定依赖同一 state label。R≥3 时这些关系不满足不同坐标 pairwise independence。

## 6. 显式规模、零权及范围

基础 group 数 n=1+R(R−1)，state 数 S=Rn，变量数2R，tagged resources 数2R³，完整 incidence 数 I=R³(2R−1)。因此完整 P 有 S+2R³ 台机器、n+I 枚 jobs。padding 后变量数为 2R+R(R−1)(R−2)，完整 incidence 数为 R³n，state/group 数不变。时间仅为0、1/(R−1)、1、∞。有限选项表与 dense 矩阵均按 R 的多项式规模显式给出；未声称仅给二进制 R 时输出按 log R 多项式。

R=3 包含在量词中，此时 V=1/2、OPT=3/2；不延伸到 R=2。0权 jobs 是完整实际任务，不能删除后再冒称原 schedule；上述 partial 目标允许不领取0质量点。均匀分布是输入显式 local distribution，不是从实际 YES witness 推出的分布。

这说明“原 tagged affine-line 表示 + 每个 incidence 标签 marginal uniform + 任意 state-dependent norm1 权”不足以保证统一正的 actual partial lower bound。它不否定额外的 Chan balanced pairwise-independent code-coset hard image，也未提供 source YES/NO 的计算困难性、未断言本实例是原 PCP 归约的像、未用该族推导任何算法不可能性。源 CSP 的最大满足比例不是本 Exact 的结论。
