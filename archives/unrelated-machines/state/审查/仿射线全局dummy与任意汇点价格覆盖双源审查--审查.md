---
id: unrelated-machines/affine-line-global-dummy-and-arbitrary-sink-price-cover-review
kind: review
title: 仿射线全局dummy与任意汇点价格覆盖双源审查
status: complete-source-read-integrated
scope: "tuple-group global-dummy escape and arbitrary-sink private-group price-cover rounding; restricted unrelated-machines interfaces"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/affine_line_tuple_groups_global_dummy_compilation_escape.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/affine_line_tuple_groups_global_dummy_compilation_escape.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/arbitrary_sink_private_group_price_cover_rounding.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/arbitrary_sink_private_group_price_cover_rounding.md
source_ids:
  - b055f6c18bcbb55590a2
  - d7bf0f8e0e037822ff23
inventory_sha256:
  b055f6c18bcbb55590a2: edc0c8437260085bfcb408099f724306531a88b360d27811b0a8e70762fc2c65
  d7bf0f8e0e037822ff23: 6c23677ab25afb0db3f0c6ced6b1fb16bb8993a541c875d6b3ee2dfaf3d6e580
---

# 阅读范围和对象分离

本批用 `clean show` 完整读取两个当前正文，并将其与已有的 line-set-packing、shared-sink、upper-column、配置匹配和周期修复审查比较。两源共享 unrelated-machines 语境，但合同完全不同：第一源研究带仿射线几何的 tuple-group 编译，在加入全局 dummy 后构造一个无需源 assignment 的至多 (3/2) 实际调度；第二源研究已给定唯一 home 私有分组和任意 sink 资格时的条件舍入算法。第一源是一个编译路线的负面边界兼正面逃逸，第二源是限定输入类的正面算法。两者都没有解决 `UM-TARGET-v1`，也不能直接转成六人 SPE 的结论。

稳定身份分别为 `UM-AFFINE-LINE-TUPLE-GROUP-GLOBAL-DUMMY-ESCAPE-v1` 与 `UM-ARBITRARY-SINK-PRIVATE-GROUP-PRICE-COVER-v1`，后者另有未知 OPT 承诺版本 `UM-ARBITRARY-SINK-PRIVATE-GROUP-PROMISE-APPROX-v1`。下文按实际量词区分完整证明、条件承诺、有限审计和开放缺口。

# 一、仿射线 tuple 分组与全局 dummy 逃逸

## 1. 输入和编译合同

取素数 (R\ge2)、(k\ge1)，有限变量集 (X) 和 indexed relations (G)，每个关系 (g) 含 (k) 个不同变量 (X_g)，每变量 relation-degree 至多 (R)。给每个变量注入 (j_x:G(x)\to\mathbb F_R)。每个允许 indexed tuple (e=(g,s)) 具有 full set
\[
S_e=\biguplus_{x\in X_g}\{(x,z,s(x)z+j_x(g)):z\in\mathbb F_R\},\qquad |S_e|=D=kR.
\]
不同变量的资源带 tag，因此线交叉只发生在同一变量的 (R^2) 资源层。令 (n) 为 allowed tuples 的总数，(m_0) 为非空 relations 的数目，整数 (1\le q\le m_0)，并令 (d=n-q)。每个 tuple 是一个独立 group；它的菜单含自身原 state 和 (d) 个共享 global dummy singleton state。dummy 资源、private 机器、selector、incidence 任务和不可用边都显式构造，所有任务不可拆分。

关键是同一 dummy 被所有 groups 共享，而不是每个 group 各有一枚私有 dummy。该设计使算法只需从不同 relations 中挑 (q) 个 tuple 进入原 state，其余 (d) 个 group 用 dummy 一一配对。它关闭的是“每个 tuple 都必须携带原 relation-degree 证明”的统一编译规则；没有关闭所有 source-to-UM 桥梁。

## 2. 至多三半调度的完整证明

从输入次序挑 (q) 个不同非空 relations，每个取其第一 tuple；其余 groups 与 (d) 枚 dummy 做确定性双射。对所选原 tuple 的任意子族 (F)，固定变量 (x) 的被选线数 (r_x\le R)。同斜率线平行，异斜率线在素域至多交一个点，故二阶容斥给出
\[
|\bigcup \text{ selected lines in }U_x|
\ge r_xR-\binom{r_x}{2}
\ge \frac{R+1}{2}r_x.
\]
不同变量的 tag 分离，(sum_xr_x=k|F|)，于是资源邻域满足
\[
|N(F)|\ge \frac{k(R+1)}2|F|\ge \lceil kR/2\rceil |F|.
\]
整数 capacitated Hall 定理给每个选中原 group 选出 (b=\lceil kR/2\rceil) 枚共同不交的真实资源 (B_e)。这一步没有要求 (B_e) 是整条 line，也不需要求 source assignment 或枚举 Hall 子集。

将选中原 state 的 (b) 个 incidence 任务送到对应资源机，其余原 incidence 留在 private 机；dummy state 只外送自己的 singleton incidence，所有未选 state 的 incidence 全部留在 private。selector 送到所选 state 的 private 机。选中原 private 负载为 (2-b/D)，dummy private 只承担 selector，资源机至多一件单位任务，未选 private 负载为 1。因此全部任务一次合法执行，且
\[
C_{\max}\le 2-\frac{\lceil kR/2\rceil}{kR}\le\frac32.
\]
这是真实不可拆分调度，不是 LP 证书。

反向的 unit 端同样是完整证明：若存在 (q) 个原 full sets 两两不交，选这些原 state、其余选不同 dummy 并把所有 selected incidences 外送，可得峰值 1。反之，任意峰值不超过 1 的完整调度中，selector 已在某个 private 上占单位负载；被选 state 的全部正 private incidence 不能再保留，否则超出 1，因此它们必须外送。资源机容量 1 强制 selected groups 的原 full sets 两两不交；至多 (d) 个 groups 用 dummy，所以至少 (q) 个 groups 用原 state，从而得到大小至少 (q) 的 packing。这个等价关系覆盖未选 state 可能额外外送的情形。

因此 unit 端的精确身份是“峰值 1 当且仅当原 indexed full sets 有 (q)-packing”；但至多 (3/2) 的算法并不求该 packing，也不能把固定 (q) 的 set-packing 困难性直接移植成近二 NO 结论。

## 3. 规模、边界和否定范围

(q=n) 时 (d=0)，没有 dummy，证明仍成立；空 relation 不产生 group，(m_0=0) 或 (q>m_0) 属于域外分支。构造的 private/resource/job 数量按 (n,D,k,R,d) 显式展开，有限时间只有 (1/D) 和 1；资源机规模含 (vR^2)，其中 (v=|X|)。因此当 (R) 是二进制输入时，必须按显式 (R^2) 资源和 incidence 输出收费，不能把该编译描述成只对 (log R) 多项式的 succinct 过程。

第一源只否定 uniform private 权、共享 (d=n-q) 个 global dummy、固定 (1\le q\le m_0) 这一具体编译合同的近二 soundness。它没有否定更换资源权、激活阈值、任务守卫、dummy 结构或其它源桥。引用的 line-set-packing 文献只作背景定位，源文和本审查均未认证外部困难性或全球新颖性。

# 二、任意汇点私有组的价格覆盖舍入

## 4. 单侧拟阵基舍入接口

第一身份给定二分图 (G=(B,H;E))，存在覆盖 (B) 的匹配；每个 home (h) 有显式模式集合 (Q_h)，模式扩张后的横截拟阵基大小为 (|B|)。模式不允许同一 home 多选，且非空模式 home 集 (H_Q) 仍需能在 (G) 中匹配全部 (B)。给非负有理矩阵 (A=(a_{zq}))、预算 (c_z)、常数列预算 (b\ge0)，每列总量至多 (b)，以及可核查分数基 (x) 满足 (Ax\le c)。确定性位多项式算法输出实际基 (I) 和覆盖 (B) 的宏匹配，使
\[
\sum_{q\in I}a_{zq}\le c_z+b
\]
对每个资源行成立。它只给上界；不保持任意成本或严格最优负载。

证明的关键是逐坐标精确 lex LP 取得 (x) 投影顶点，而不是任取扩展流顶点。固定 0、收缩 1 后，剩余基多面体的极大紧集链给出最小面维数 (d\ge\sum_e(1-x_e))。若有 (k) 条尚未删除的资源行，交切顶点的维数约束给 (d\le k)，所以剩余分数缺额总和不超过 (k)。列预算推出总未来增量至多 (bk)，因此至少有一行的未来上增包络不超过 (b)；删去该行并永久保留当前预算，重复即可到达整数基。最终再用整数匹配恢复真实宏身份。

边界包括 (b=0)、秩零、空资源行和显式模式。直接复制 (G) 的邻接而不保 home 容量会允许同 home 多选，不能套用该拟阵证明。小菜单例表明统一加性误差 (cb)（(c<1)）在一般接口上不能保证；此加一界是该接口的自然锐界。该证明是标准上界型拟阵计数的有理加权重构，正文已把文献结果作为背景扣除，没有声称新舍入原理。

## 5. 唯一 home 私有组与任意 sink 算法

第二身份给定不交 home 集 (H)、sink 集 (Z)、宏任务 (B) 和不交私有任务组 (J_h)。每个私有任务在唯一 home 有 (a_j\ge0)，可另在任意合法 sink 子集 (E_j) 运行；宏任务只在 home 上。合同参数为 (T>0)、(ho\ge1)、(delta\ge0)、(\tau\in[1/2,1))、(\eta\in(0,1])，并满足
\[
b_0=\rho(1-\tau+\delta)\le1,
\]
每个 home 总私有量 (W_h\le T)、单件 (a_j\le\delta T)、合法 sink 时间 (p_{zj}\le\rho a_j)，宏有限边大于 (T/2)。宏边大于 (T) 先剪掉；合同允许任意 home/sink 数和有理分母。

算法返回 FAIL 或完整实际分配。成功时
\[
L_h\le(1+\tau)T,qquad L_z\le[1+\eta+b_0]T.
\]
若 (OPT\le T)，必成功，因此 FAIL 是 (OPT>T) 的声音证书，但成功不代表精确 (T)-可行。固定 (ho,delta,eta) 且 (ho\delta+\eta<1) 时选
\[
\tau=\frac{\rho(1+\delta)+\eta}{1+\rho}
\]
得到统一系数
\[
\alpha=2-\frac{1-\rho\delta-\eta}{1+\rho}<2.
\]

给定价格向量 (pi)（非负且和为 1），每个 home 以 (D_h=(W_h-\tau T)_+) 为覆盖需求，只允许有 sink 端的私有任务参加。取 inclusion-minimal 覆盖，保留实际覆盖量，则总私有量严格小于 (D_h+\delta T)；选定每件任务的合法 sink 后，该模式的 sink 向量总量至多 (b_0T)。对全部 home 用同一价格最小覆盖，并以二分匹配共同选择宏占位 home；不能逐 home 独立选后再修补，因为宏身份和 sink 负载是耦合的。

单次价格查询用覆盖 FPTAS（(epsilon=\eta/4)）、真实处理时间回溯和最小成本宏匹配；若所得 sink 向量的价格成本大于 ((1+\epsilon)T) 则 FAIL。若 (OPT\le T)，最优调度删冗余后提供共同 home/macro 见证，故该 FAIL 不会发生。随后用 multiplicative weights 进行 (N=\lceil16RK/\eta^2\rceil) 次价格查询，保留全部真实整数方案并按频率平均，得到模式扩张基的显式分数点；单侧基舍入把每个 sink 增量再限制在 (b_0T) 内。最终得到 home 和 sink 的整数负载界，所有任务都在原始合法端点执行。

复杂度关于总输入位长和 (1/\eta) 多项式；不声称关于 (log(1/\eta)) 多项式。零端、(T=0)、无 sink、空组、零处理时间和大分母都有独立分支。所有模式和 MW 输出都由真实任务回溯产生，未把指数 Pareto 菜单或精确 LP oracle 当作免费输入。

## 6. 未知 OPT 承诺版本与限制

未知 OPT 版本先用整数 makespan 网格和二分搜索调用同一阈值程序。它依赖额外 promise：以真实 OPT 为尺度时 (W_h\le OPT)、(a_j\le\delta OPT)、宏有限边大于 (OPT/2)。算法不能一般性验证该 promise；在 promise 内，每次 FAIL 说明当前阈值低于 OPT，成功阈值给出 \(\alpha OPT) 上界。所有有限时间分母的乘积给出多项式位长的网格，二分查询次数多项式。

这一路线取消了固定 sink 数、同组共同资格和接收时间下包络，但保留唯一 home、私有分组、统一 (ho,delta) 和可计算的宏占位结构。它不能从任意 unrelated-machines 矩阵自动生成这些角色或 promise；知道最优调度后可以删边得到有利结构，也不等于存在多项式结构提取器。因而它是限定接口的条件算法，不是 `UM-TARGET-v1` 的一般近二算法。

# 三、比较、用途和接续

* 第一源的核心机制是“只选不同 relation 的 (q) 个原 tuple，其余用共享 global dummy”，用线交叉的二阶容斥恢复 (lceil kR/2\rceil) 资源匹配；它正面展示了一个具体编译如何绕开 tuple-level 统一计数障碍，同时保留 unit 端 packing 等价。
* 第二源的核心机制是“价格查询生成有限真实模式 + 一次共同宏匹配 + 上界型拟阵舍入”。它把任意 sink 资格纳入共同占位，但不提供从一般矩阵恢复 home 分组、宏身份或统一比率的办法。
* 两源都强调全局耦合：第一源的 dummy 由所有 groups 共享，第二源的宏匹配、sink 价格和 home 模式必须联合处理。逐组独立舍入或把每个 tuple 当作独立 relation 会丢掉关键不变量。
* 有限枚举、覆盖 FPTAS、MW 回放和顶点审计只验证列出的接口与参数；它们不能替代一般 LP 后端、源 assignment 求解器、复杂度困难性或全局新颖性证明。
* 第三阶段可把第一源接到“仿射归约/全局 dummy/packing 解码”关系，把第二源接到“private group/price cover/matroid upper rounding”关系；二者之间不得添加无前提的同构边。

两个来源均已完整阅读、比较并写入本审查。独有的几何匹配、共享 dummy 编译、完整 unit 提取、单侧基舍入、价格覆盖和未知 OPT promise 均保留；没有因不在主线或缺一般定理而丢弃。`UM-TARGET-v1` 和从任意输入生成这些条件结构的义务继续开放。
