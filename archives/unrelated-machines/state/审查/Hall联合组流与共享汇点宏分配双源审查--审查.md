---
id: unrelated-machines/hall-group-flow-and-shared-sink-joint-review
kind: review
title: Hall联合组流与共享汇点宏分配双源审查
status: complete-source-read-integrated
truth_status: two restricted positive interfaces with exact quantifiers and failure boundaries
scope: "common-eligibility Hall flow and one-shared-sink joint macro assignment; no general UM theorem"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/hall_group_joint_flow.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/hall_group_joint_flow.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/shared_sink_joint_macro_assignment.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/shared_sink_joint_macro_assignment.md
source_identity:
  - id: 326d6af1da65fbe4ab4c
    path: research/current/unrelated_machines/hall_group_joint_flow.md
    blob: ce975324a000a4b8c44a294cbdf5e7188c94b032
    sha256: 10aabd8e9cc0eccf10974f94e23633f6d1034313348a69ceac003bb876af5b2b
  - id: dda3c909b1a2bdff9170
    path: research/current/unrelated_machines/shared_sink_joint_macro_assignment.md
    blob: 425c1e432f9aecb5a91f9bfb0083f3ad3ddfbbdc
    sha256: 8aec1196d16fccdd5dd661d1ebfebd1f1c211d256da021aa02f433304424ef2c
frozen_commits:
  - 68fad804ec5946cb296f77dc5b336308a66abf12
  - aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c
---

# 阅读范围与对象分离

本批通过 `clean show` 完整读取 `hall_group_joint_flow.md` 与 `shared_sink_joint_macro_assignment.md`，并比较了联合匹配、价格覆盖、upper-column 拟阵舍入、固定汇点和已有配置审查。两源都在 unrelated-machines 模型内给出正面、可构造的限域接口，均明确保留 `UM-TARGET-v1` 为开放问题。它们的共同思想是把一组私有任务的撤离资格写成同一个接收池，再用一个全局整数流或一次共同宏匹配处理所有宏任务；这与逐组先舍入再修补的做法有本质区别。

第一源允许多个接收机器 (Z)、每个 home 的组有共同资格 (E_h)，并用 q 个接收槽控制每个 sink 的组数。第二源只有一个共享 sink (z)，允许每个私有任务在 home、sink 的任意非空子集上可用，先精确生成每个 home/宏任务模式的最小 sink 成本，再用一次全局匹配同时选择宏任务 home 和空模式。第一源的正面常数来自同体积任务和 Hall 计数；第二源的正面常数来自单一 sink 预算和局部覆盖成本乘性误差。不能因为二者都出现“共同汇点”就合并其量词。

# 一、Hall 联合组流接口

## 1. 定义域与准确身份

机器为显式不交的 (H\cup Z)，允许 (Z=\varnothing)。任务分成宏任务 (B) 和私有组 (J_h)；宏任务只在 home 可用，每件 (j\in J_h) 恰在 ({h}\cup E_h) 可用，且这些端点处理时间都是同一个非负有理 (w_j)。记 (W_h=\sum_{j\in J_h}w_j)。宏处理时间可随 home 改变；所有机器、任务、资格边和时间都按显式二进制输入提供，不用多重性紧凑编码。

`UM-HALL-GROUP-JOINT-FLOW-v1` 的阈值合同给整数 (q\ge2)、有理 (delta\ge0,T\ge0)，满足 (q\delta<2)，每条有限宏边 (p_{hb}>T/2)，且
\[
(1/2+1/q)T\le W_h\le T,
\qquad w_j\le\delta T.
\]
定义
\[
\tau=\frac{q-1+q\delta}{q+1},
\qquad r=\frac{q(2+\delta)}{q+1}.
\]
对所有满足合同的输入，确定性总位长多项式算法返回 FAIL 或真实完整调度；成功时 (C_{\max}\le rT)，若 (OPT\le T) 则必成功，故 FAIL 蕴含 (OPT>T)。这里成功不表示精确的 (T)-可行性。

`UM-HALL-GROUP-PROMISE-APPROX-v1` 不输入 (T)，只承诺在真实 (OPT) 尺度上满足相同宏边、组负载和单件上界；算法通过实际宏时间的瓶颈集合和有限搜索取得 (C_{\max}\le rOPT)。固定 (q,delta) 且 (q\delta<2) 时 (2-r=(2-q\delta)/(q+1)>0)，但 (q) 增长时改善趋于零，且算法不能判定任意输入是否满足关于 (OPT) 的承诺。

## 2. 从真实 T 调度得到 q-Hall 结构

设 (T>0) 且存在真实 (T)-调度。由于宏边严格大于 (T/2)，每个 home 至多接一个宏任务。令 (Ssubseteq H) 是放置宏任务的 homes。对 (h\in S)，私有任务留在 home 的量小于 (T/2)，所以撤离量 (e_h) 满足
\[
e_h>W_h-T/2\ge T/q.
\]
对任意非空 (A\subseteq S)，这些组的出口只能进入 (N(A)=\bigcup_{h\in A}E_h)。因为同组任务在 home 和 sink 端使用相同体积，
\[
|A|T/q<\sum_{h\in A}e_h\le |N(A)|T,
\]
从而 (|A|<q|N(A)|)。把每个 sink 复制 q 次即得到整数 Hall 条件：每个占用 home 可以被指派到一个共同资格 sink，每个 sink 至多接 q 个组。这是存在性见证，不是算法把 q 个副本显式展开；q 可以是二进制输入，构造按容量运行。

共同资格和同体积是不可删除的假设。只有总工作量而没有资格图时，不能把上述不等式转成接收槽；若每个任务在同组内有不同 sink 资格，取交集会丢掉可行解，取并集又可能产生非法迁移。

## 3. 一次全局整数网络与真实前缀收费

网络节点为源 (s)、每个宏任务 (b)、每个 home 的 (h_{in},h_{out})、每个 sink (z) 和汇 (t)。边容量为 (s\to b:1)；(b\to h_{in}:1) 仅在原宏边有限且 (p_{hb}\le T) 时加入；(h_{in}\to h_{out}:1)；(h_{out}\to z:1) 当 (z\in E_h)；(z\to t:\min(q,|B|))。固定节点顺序后用整数增广流求最大流。流量不足 (|B|) 时 FAIL；若 (OPT\le T)，上一节的 q-Hall 见证给出满流。

对每个流选中的 home，按固定任务顺序撤离最短前缀，使留下的真实 home 私有负载不超过 (\tau T)，撤出的任务全部去流指定的共同 sink；未占用 home 的组全部留在原 home。宏任务由同一流恢复，因而没有冻结一个宏匹配后再单独修微任务的中间步骤。

若某组需要撤离，最后一件任务加入前的撤离量严格小于 (W_h-\tau T)，再加一件至多 (delta T)，所以
\[
e_h<(W_h-\tau T)+\delta T\le(1-\tau+\delta)T.
\]
占用 home 的总负载至多 (T+\tau T=(1+\tau)T)，未占用 home 至多 (T)，每个 sink 至多接 (q) 组，因此 sink 负载至多 (q(1-\tau+delta)T)。恒等式
\[
1+\tau=q(1-\tau+delta)=r
\]
同时给出所有机器的 (rT) 界，且 (2-r=(2-q\delta)/(q+1)>0)。零尺寸任务通过扫描至多本组任务数处理，不会造成非终止循环。

## 4. 未知 OPT 搜索、退化输入与复杂度

未知 OPT 版本先逐件检查零边；若所有任务都有零边则直接输出零调度。对 (delta>0)，取实际有限宏时间去重排序表，在其中对宏边瓶颈用整数最大流二分；用
\[
t=\max\left(\max_h W_h,\max_j w_j/\delta,B\right)
\]
作为阈值，其中 (B) 是使宏任务可被 home 覆盖的最小实际宏时间瓶颈。承诺域内 (t\le OPT)，且宏边、组总量和单件上界都能在 (t) 上满足阈值合同，因此调用阈值算法得到 (rOPT) 上界。搜索只访问实际输入时间，不二分连续实数，也不调用 OPT 精度 oracle。

(T=0)、(delta=0)、空任务、(Z/E_h=\varnothing)、没有 home 和宏任务过多等分支均显式处理。网络的节点边数是输入长度的多项式；整数增广最多增加 (|B|) 次，容量按数值存储但不按 q 复制。前缀和、精确有理比较和输出任务编号的位长受显式输入总位长多项式控制。附带的指数 DFS 和有限枚举只作独立审计，不能替代生产算法的多项式证明。

## 5. 反例边界和可回收机制

共同资格是核心承重条件。两个私有任务分别只能去不同 sink 时，交集可能为空，联合流会可靠 FAIL，即便允许把任务分开看似可行。组负载下界 (W_h\ge T) 也不可省略：若每组总量低于 (T)，可以构造一个 home 负载与共同 sink 负载都不超过 (T) 的例子，但 q 槽网络不再代表该组的实际出口需求。严格 Hall 计数不能自动把 q 槽降成 q−1；存在三组、两个共同 sink 的实际 (T=1) 见证要求两个槽以上的联合容量。

任意有理 sink 容量下，满足选择条件的 home 子集也不必形成拟阵。例如三个组对四个容量半单位 sink 的资格关系可使单组与两组联合可行，但任意两组加第三组的交换条件失败。这限制了把该接口抽象成简单拟阵基的做法；它不是一般选择或 UM 硬度结论。

可复用机制是“真实占用组的最低出口体积 → 整数接收槽 → home、宏任务和接收机一次共同流 → 前缀收费把两侧负载平衡”。它允许接收机数量随输入增长，且不要求原宏匹配逐坐标保留；但一般跨 home 私有任务、同组异资格、异端点时间或缺少组负载下界时，尚无保持统一余量的转换。

# 二、共享单汇点联合宏任务

## 6. 定义域和基本模式

`UM-SHARED-SINK-JOINT-MACRO-v1` 给定显式 homes (H) 与一个共享 sink (z)。任务分成宏任务 (B) 和不交私有组 (S_h)。宏任务只在 homes 可用；私有任务的有限端点是 ({h,z}) 的非空子集，时间是二进制非负有理。给阈值 (T\ge0)、(0<\eta\le1)，每条有限宏边严格大于 (T/2)。私有任务不要求 tiny 尺寸；这一点与第一源不同。

对每个 home，先分离只在 home 可用、只在 sink 可用和两端均可用的任务。若强制 sink 部分超过 (T) 直接 FAIL。对一个允许在 home 的宏模式 (t)（或空模式），若 home 的固定私有负载为 (F_h)，令
\[
D_{ht}=\max\{0,F_h+\beta_{ht}+\sum_{j\in U_h}a_j-T\}.
\]
模式的实际 sink 成本 (c^*_{ht}) 是在两端均可用任务中选出真实子集，使 home 撤离量至少 (D_{ht}) 时的最小 sink 时间总和。模式必须保留一个实现它的任务子集；只使用互不相容的坐标包络不能替代该子集。

## 7. 保覆盖背包与一次全局宏匹配

对任意覆盖实例 ((a_j,c_j,D))，正文给出保留真实覆盖量的 FPTAS。先取零 sink 成本任务；若不足以覆盖，再对每个不同正成本 (C) 猜测最优集合的最大单件成本，令 (s=\eta C/q)，把成本向下取整为整数 (w_j=\lfloor c_j/s\rfloor)，动态规划保存每个整数成本的最大真实覆盖量及任务回溯。正确猜测下得到的集合 (X) 满足
\[
\sum_{j\in X}c_j\le(1+\eta)c^*.
\]
(D=0)、空组和零最优值走精确零成本分支，避免乘性误差在零值上失效。状态数量和回溯空间关于组内任务数、总位长和 (1/\eta) 多项式。

每个 home/宏模式都生成一个实际实现集合 (X_{ht}) 和近似成本 (hat c_{ht})。在左侧放全部真实宏任务及补齐的 dummy，在右侧放 homes；真实宏边成本为 (hat c_{ht})，dummy 边成本为空模式成本。一次最小成本完美匹配同时决定每个宏任务的 home、每个 home 是否空置和每个私有组的具体撤离集合。强制 sink 成本在匹配总成本外只加一次；若最终 sink 负载大于 ((1+\eta)T)，返回 FAIL。

若存在真实 (T)-调度，宏边 (>T/2) 保证每个 home 至多一个宏，因而可用 dummy 补完一个完美匹配。该调度的私有撤离子集给每条匹配边一个可行模式，并满足精确总 sink 成本不超过 (T)。最小成本匹配不超过该见证，局部近似误差只乘在同一总 sink 预算上，所以全局 sink 负载不超过 ((1+\eta)T)。home 负载由模式定义直接不超过 (T)，因此若 (OPT\le T) 必成功。

算法的总复杂度是所有 home/模式覆盖 DP 加一个 (O(h^3)) 级别的有理最小成本匹配；输入机器逐台显式编码，模式数与任务数均按显式长度计。它不要求 sink 数固定，因为这里只有一个共同 sink；也不把指数枚举当作生产后端。

## 8. 宏任务退出与有界 profile 扩展

`UM-SHARED-SINK-MACRO-EXIT-v1` 将宏任务有限端点放宽到 homes 与 sink 的非空子集，允许宏任务数量超过 home 数。用 (b+h) 阶匹配把宏任务、dummy、home 和退出位置一起处理：宏可进入 home 或直接在 sink 退出，dummy 补齐空 home 和退出槽。真实 (T)-调度直接产生完美匹配见证，局部覆盖误差仍只乘在总 sink 预算上，因此 home 负载不超过 (T)，sink 不超过 ((1+\eta)T)。

`UM-BOUNDED-PROFILE-EXIT-POOL-v1` 再允许多个 pool 机器，但所有 pool-enabled 任务共享完整 pool 资格，并有统一 profile
\[
a_zc_j\le p_{zj}\le\rho a_zc_j,
\qquad p_{zj}\le\beta T.
\]
把任务虚拟化到单汇点，虚拟时间为 (c_j/S)，(S=\sum_z1/a_z)，调用单汇点算法得到总虚拟 work 不超过 ((1+\eta)TS)。再按实际 pool 负载最小的机器逐件恢复；总 work 上界保证每一步至少存在某台负载不超过 (
ho(1+\eta)T)，加上单件上界后得到 pool 负载 ([\rho(1+\eta)+\beta]T)。这是真实 profile 结构的条件恢复，不是把多个 sink 任意压成单一预算。

## 9. 失败机制、证据和开放范围

第一源的独立审计包含阈值流、未知 OPT 搜索、任务逐件回填和有限 DFS；第二源的规范与独立实现分别枚举覆盖子集、宏匹配和实际分配。审计支持所列参数和边界，不能替代一般输入的证明。两个源的数学结论都是自足的限域结果，未认证外部新颖性，也没有调用配置 LP、真实最优分解或整数调度 oracle。

两源共同的开放义务是如何从一般 unrelated-machines 矩阵生成唯一 home、共同资格、同体积或完整 pool profile；如何在多汇点、跨 home 任务和多预算下保留一次共同选择的整数性；如何把这些条件接入一般近二算法。单汇点算法控制的是一个实际 sink 总预算，不能推出多 sink 的同时预算；Hall 算法控制的是 q 个接收槽和同体积组，不能在异体积/异资格输入上直接使用。

## 处置记录

两个来源均已完整读取、定义域逐项核对、与已有联合匹配和价格覆盖审查比较，并按不同对象写入本审查。Hall 源的 q-Hall 见证、联合宏/home/sink 流、前缀负载平衡、未知 OPT 搜索、反例边界和有限审计均保留；共享 sink 源的覆盖成本模式、保真实覆盖 FPTAS、一次共同宏匹配、宏退出和完整 profile pool 扩展均保留。未把条件接口升级为一般 UM-TARGET，也未删除其开放的生成结构义务。
