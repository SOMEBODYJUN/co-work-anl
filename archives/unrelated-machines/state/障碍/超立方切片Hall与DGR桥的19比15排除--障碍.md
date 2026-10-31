---
id: "unrelated-machines/grouped-hypercube-slice-hall-dgr-bridge-obstruction"
kind: obstacle
type_tag: 障碍
title: "超立方切片 Hall 与 DGR 桥的 19/15 排除"
status: proved-scoped-obstruction
truth_status: "elementary-Hall-and-UM-construction-proved; bridge-excluded-under-explicit-slices; no-hardness-or-novelty"
review_level: "full-16574-byte-source-and-proof-read"
scope: "tagged hypercube slice menus with incidence degree d, binary degree-five specialization, and the direct ordinary-UM construction"
summary: "在变量标签互异、每变量每组至多一次切片且每变量至多 d 组的显式超立方域内，任意状态选择满足 union-to-slice ratio c_d=1-(1-1/d)^d，并可由 capacitated Hall 保留 floor(c_d k_g) 个资源。标准 d=5,Q=2、三变量每组菜单因此给出完整 ordinary-UM 调度峰值至多 19/15；该具体 DGR/hypercube 桥不能产生 1 对近二 gap。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/grouped_hypercube_slice_scheduling_v1_exact_and_proof.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/grouped_hypercube_slice_scheduling_v1_exact_and_proof.md"
  - "clean:a391f8716be276dbd8a1"
related_objects:
  - "../资源/Davies-Guruswami-Ren受限拒绝双标准--资料.md"
  - "../定理/三坐标零权切片的精确菜单嵌入--定理.md"
  - "../审查/三坐标与三态路径正规形范围审查--审查.md"
  - "../审查/加权菜单组交互匹配双源续审查--审查.md"
source_sha256: "e380618458138f3c43f9692673f19b208c604112dd41a31c89b92e3b297987bf"
source_size: 16574
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/grouped-hypercube-dgr-v1/original/grouped_hypercube_slice_scheduling_v1_exact_and_proof.md"

# 1. 对象和处置范围

来源 `grouped_hypercube_slice_scheduling_v1_exact_and_proof.md` 冻结大小 16,574 字节，SHA-256 为
`e380618458138f3c43f9692673f19b208c604112dd41a31c89b92e3b297987bf`；原字节已复制到 evidence 并核得同一 SHA。它是 2026-10-18 的 candidate statement + proof，明确说这些是超立方分区的初等推导，不把任何结论归给 DGR，也不声称文献新颖性。本文将其作为已给出证明的**受限结构障碍**整理：A/B/C 的数学证明在本页保留，DGR 论文事实和普通 UM 桥的模型分离；不把它升级为一般 unrelated-machines 硬度或新近似算法。

## 2. 超立方切片输入与 Hall 定理

固定整数 d>=1、Q>=1。变量集 X 与非空有限组集 G 显式给出。每组 g 有非空、由 distinct variables 构成的 X_g 和显式 indexed state 集 A_g。每个变量 x 的参与组集合 G(x) 满足 |G(x)|<=d，并有 injective incidence-index map j_x:G(x)->[d]。state s 给 X_g 中每个变量一个 label ell_{g,s}(x) in [Q]；不同 state 即使 label vector 相同仍按不同 index 保留。

对每个变量建立带 tag 的互不相交资源宇宙

`U_x = {x} x [d]^[Q]`,  `U = disjoint_union_x U_x`.

在坐标 i、label j 的 slice 为

`P_(x,i,j) = {(x,a): a(i)=j}`.

组 g 的 state s 选取

`S_(g,s) = disjoint_union_(x in X_g) P_(x, ell_(g,s)(x), j_x(g))`.

令 h=d^(Q-1)、q_g=|X_g|、k_g=q_g h，并令

`c_d = 1 - (1-1/d)^d`.

**A1（任意状态选择和任意子族）**：对每个 choice function s(g)，以及每个 F subseteq G，

`|union_(g in F) S_(g,s(g))| >= c_d * sum_(g in F) k_g`.

令 b_g=floor(c_d k_g)，则有 pairwise disjoint B_g subseteq S_(g,s(g))，|B_g|=b_g；同时，不取 floor 的 fractional demand c_d k_g 也可由同一 Hall 条件实现。保证对所有 state choices 成立，不需要 YES/CSP 可满足性。

退化边界：d=1 时各变量只属于一个组，c_1=1 且 selected sets 已不交；Q=1 时单一 partition 也已不交，可将常数提高为 1；Q=0、d=0、空 X_g 不在此对象域内。

### A 的证明要点

固定 F 和单个变量 x，令 r_x=|F intersect G(x)|<=d。对每个 label i，令 t_i 为 F 中在 x 上选 label i 的组数。injective index 使同一坐标 i 的 t_i 个 slices 取 distinct coordinate cells；sum_i t_i=r_x。补集大小是 product_i(d-t_i)，故该 gadget 的 union 为

`d^Q * (1 - product_i(1-t_i/d))`.

当 d>1 时，设 z=1-1/d。由于每个 t_i 是整数，Bernoulli 给
`1-t_i/d <= z^(t_i)`，于是补集乘积不超过 z^(r_x)。序列 `(1-z^r)/r` 在正整数 r 上非增，而 r_x<=d，因此

`d(1-z^(r_x))/r_x >= 1-z^d = c_d`.

单变量 union 至少 c_d r_x d^(Q-1)=c_d r_x h；对 tag-disjoint 的变量求和得到 A1。积分版把组 g clone 成 b_g 个 unit-demand copies，任意 copy 子集的邻居资源至少其 demand 总量，故 capacitated Hall 成立；integral max flow 找到 B_g。证明只依赖整数 t_i、injective indices 和 tagged universes。

## 3. d=5、Q=2 的 19/25 特化

在一个 binary d=5 gadget 中，若选两个 label 的 a、b 条 slices，r=a+b<=5，union 大小为 5r-ab、总 slice size 为 5r。固定 r 时 ab 最大为 floor(r^2/4)，得到精确最小比值：

| r | max ab | min union/total |
|---:|---:|---:|
| 1 | 0 | 1 |
| 2 | 1 | 9/10 |
| 3 | 2 | 13/15 |
| 4 | 4 | 4/5 |
| 5 | 6 | 19/25 |

所以任意 state choice 和任意子族都满足 19/25。若每组有三个 distinct variables，k_g=3*5=15，Hall 给 floor((19/25)*15)=floor(57/5)=11 个互不相交资源。19/25 是该 local binary gadget 的精确最小比值；11 不被声称为优化状态 choices 后的最佳全局整数保证。

## 4. 直接 ordinary-UM 构造及 19/15 上界

对任意显式 indexed set menus S_(g,s)（这里不需要超立方结构或 equal sizes），令 k_(g,s)=|S_(g,s)|>=1。构造完整 ordinary R||Cmax：

* 每 indexed state 一台 private machine M_(g,s)；
* 每 resource 一台 R_u；
* 每组 selector J_g，在本组每台 state machine 上耗时 1；
* 每个 incidence (g,s,u) 一件 distinct job I_(g,s,u)，在 M_(g,s) 上耗时 1/k_(g,s)，在 R_u 上耗时 1；
* 其他 processing times 全是 infinity，所有 jobs 必须执行一次。

若某 choice 的 entire state sets 已 pairwise disjoint，选中 state 的所有 incidences 外送、未选 state jobs 留 private，可得 OPT=1（selector 给下界 1）。更一般，若选中 state 的每组都有 pairwise disjoint B_g，大小 b_g，则把 B_g 对应 jobs 外送，其余留 private，得到

`Cmax <= max{1, max_g(2 - b_g/k_(g,s(g)))}`.

把 A2 代入，任意输入都有 unconditional bound。d=5,Q=2、每组三变量时 b_g=11,k_g=15，因此

`Cmax <= 2 - 11/15 = 19/15`.

这是对 concrete ordinary-UM construction 的真实输出峰值，不是把 set-packing 或 bicriteria rejection objective 偷换为 UM。因界对所有输入成立，无论底层 CSP 是 YES 还是 NO，该 bridge 都不能给 `OPT=1` 对 `OPT` 接近 2 的 gap。

## 5. 显式规模和算法边界

令 n_U=|X| d^Q、a=sum_g |A_g|、L=sum_g sum_s |S_(g,s)|。资源、state memberships、labels 和 set incidences 必须显式 materialize；A2 用 source-to-group capacity b_g、group-to-resource capacity 1、resource-to-sink capacity 1 的 integral max flow。网络规模按 |G|+n_U+sum k_g 计多项式。UM 有 a+n_U 台机器、|G|+L 件 jobs，每 incidence 只有两个有限端；时间为 1 和 1/k_(g,s)，位长为 O(log(k+1))。

d>1 时 c_d=(d^d-(d-1)^d)/d^d，精确 floor 计算的位长为 O(d log(d+1))；非空显式 cube 有 n_U>=d，故按 explicit input size 可行。d,Q 以 binary 给出而只保留 compact labels 时 d^Q 可能指数，本对象不声称 succinct-model polynomial。DGR specialization 固定 d=5,Q=2，materialization 对公式规模线性。

## 6. 与 DGR 受限拒绝问题的区别

全仓 `Davies-Guruswami-Ren受限拒绝双标准--资料` 读的是 Davies--Guruswami--Ren, *Scheduling Problems with Constrained Rejections* arXiv:2511.00184v1；其 Theorem 4 是 ungrouped set-selection hardness，degree-five 3-CNF、每 clause 七 sets、binary labels、每 set size 15。m clauses 对应 7m sets 和 15m resources；YES 的 m sets partition universe；其参数是 alpha=1/7、beta=(1-epsilon_0)/7、epsilon<1/30，Section 3 再加入 6m universal dummy items 并讨论 constrained rejection loss。

本仓库的 grouped construction 是额外定义：每 clause 作为一个 group，七个 satisfying local assignments 作为 states，每个 state 使用该 clause 的三变量各一个 slice。DGR 的文献对象是 ungrouped set selection/rejection，不是本页的 state-menu ordinary UM。对 d=5,Q=2、三变量菜单，B/C 的 19/25 和 19/15 对每个 formula 无条件成立，不依赖 SAT。因 set size 15 且 1-epsilon 的 DGR 取值在 epsilon<1/30 时等于要求接近全部 15，DGR 的常数不自动成为低 retention 的 UM gap；任何严格 decision gap 仍需独立选取中间 packing threshold。

本页只保存 DGR 的来源身份和适用范围，不把其 constrained-rejection hardness 转写成一般 R||Cmax hardness，也不声称 19/15 是文献结果或新颖性结果。

## 7. 准确的逃逸位置和接续义务

A--C 排除的是同时满足以下合同的 bridge：tagged disjoint variable cubes、每组每变量至多一个 slice、每变量至多 d 组且 indices injective、set membership 不重复、ordinary UM jobs 为 selector + private/resource 两端。以下变化能避开本障碍，但都需要重新证明 YES、NO 和实际处理时间：

1. 使用非 product 的 slice system 或重复 incidence indices，使 product complement 或 r_x<=d 失效；
2. 识别不同变量的资源名，或在一个 state 中重复同一 global resource，使 tagged-universe additivity 失效；
3. 使用多个 processing scales、state-dependent additive values 或不同机器端时间，直接追踪 weighted offload，而不是把全局 item size 当 unrelated processing time；
4. 采用真正跨测试/跨组一致性约束或 source-related decoder，而不是仅增加 Q、clause arity、d 或 uniform copies。

这些只是超出本障碍假设的 escape mechanisms，不是已找到的新 hardness source。现有三坐标 zero-cell embedding、资源度三路径和三态正规形对象保留原任务身份与 scope，但它们也不自动提供 DGR 的 near-two NO 解码；本页只说明该具体 hypercube/DGR route 已有 19/15 的 unconditional UM upper bound。

## 8. 处置

该来源处置为 `integrated` 的 proved-scoped obstruction：A 的 general Hall allocation、B 的 19/25 local specialization、C 的 ordinary-UM construction、D 的 explicit-bit limits 和 DGR objective separation 均写入本页，并保留原字节证据。第三阶段可建立“排除特定桥/依赖 DGR source”关系，但不能建立“一般 UM hardness 已证”关系。外审、新颖性、其他 slice systems 和一般 UM-TARGET-v1 仍开放。
