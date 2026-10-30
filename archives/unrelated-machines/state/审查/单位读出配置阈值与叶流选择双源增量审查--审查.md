---
id: "unrelated-machines/unit-readout-config-leaf-flow-increment-review"
kind: "review"
type_tag: "审查"
title: "单位读出配置阈值与叶流选择双源增量审查"
status: "integrated-with-scoped-positive-and-boundary-results"
truth_status: "general-proofs-scoped-to-private-unit-readout-forest; finite-evidence-separated; no-general-UM-hardness"
review_level: "full-source-read-and-prior-four-source-review-comparison"
scope: "exact positive-part configuration polytope/strict-unit gap and fixed-height leaf-flow/selector mixing"
source_refs:
  - "source:40a75aa26f402db03c39:research/current/unrelated_machines/unit_readout_configuration_threshold_polytope.md"
  - "source:dce12333944853ff579d:research/current/unrelated_machines/unit_readout_global_leaf_flow_and_selector_mixing.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/unit_readout_configuration_threshold_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/unit_readout_global_leaf_flow_and_selector_mixing_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/unrelated_machines/unit_readout_configuration_threshold_audit.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/unrelated_machines/unit_readout_global_leaf_flow_and_selector_mixing_audit.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/unit_readout_configuration_threshold_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/unit_readout_global_leaf_flow_and_selector_mixing_audit.json"
legacy_ids:
  - "UM-UNIT-READOUT-CONFIG-POSITIVE-PART-v1"
  - "UM-UNIT-READOUT-STRICT-UNIT-GAP-v1"
  - "UM-UNIT-READOUT-CLOSED-TREES-EXACT-CONFIG-v1"
  - "UM-UNIT-READOUT-FIXED-HEIGHT-APPROX-v1"
  - "UM-UNIT-READOUT-SELECTOR-MIXING-v1"
---

# 1. 阅读范围、版本指纹和已有审查的关系

本批完整读取了 `clean show` 的两份 canonical 正文、冻结版本元数据、正文链接的配置阈值/全局叶流旧审查、相关单位读出槽和修剪森林审查、两套审计代码与冻结 JSON。当前 inventory 指纹为：`40a75aa26f402db03c39`，SHA-256 `b29c1500da407a86c3172c6738f22c5b10c073d0270aeac9acd668260983967a`，13292 bytes；`dce12333944853ff579d`，SHA-256 `425af66b7eaa6c8317398f1806aceeae869459ffb57ee9b89c2a6fd2d029070f`，12766 bytes。两份都来自冻结提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 的 `research/current/unrelated_machines/` 路径。

旧的《单位读出槽配置流与修剪森林四源审查》已经整合过相同数学对象的 evidence JSON。本页不把旧 evidence ID 当成当前 canonical ID，也不重复制造“有限 audit passed = 定理”。本页将当前两个源的完整正文按对象重读，写出它们各自的数学合同、证明量词、边界反例和两源连接；当前源 ID 的独有处置在第 6 节列明。两源都属于私有单位读出双满 `k` 叉树模型，输入显式列出叶地址；不属于一般不相关机器，也不属于六人客户/共同目录 SPE。

# 2. 配置正部多面体与严格单位阈值

## 2.1 模型和正部多面体的精确量词

模型中每个变量有两棵私有满 `k` 叉深 `h` 树和一枚 selector。selector 只能在两根耗时 1；内部边任务在父端耗时 `1/k`、子端耗时 1；叶任务在父端耗时 `1/k`，或在所属 clause 的任一 unit 机器耗时 1。不同 clause 的 unit 机器互异，容量 `A_c` 为非负整数，叶 wiring 可重复且不限制 clause 密度；无 pins、额外任务和资格。输入显式列出叶地址，`A_c` 可二进制编码，外部 unit 机器只需截取到 `min(A_c,d_c)`。

稳定身份 `UM-UNIT-READOUT-CONFIG-POSITIVE-PART-v1` 对每个这样的有限显式实例、每个有理 `T in [1,2)` 成立。令 `s=floor(k(T-1))`。若根的 selector 边际为 `y_vs`、内部或叶的下传边际为 `t_e`，根入边际 `q_u=y_vs`、非根 `q_u=t_parent`，则完整 CONFIG(T) 可行当且仅当存在多项式大小的有理系统

\[
y_{v0}+y_{v1}=1,\quad y_{vs}\ge0,\quad 0\le t_e\le1,
\]
\[
\sum_{e\in out(u)}(q_u-t_e)_+\le s q_u,
\qquad
\sum_{e\in ports(c)}t_e\le A_c.
\tag{P_s}
\]

第二组按 clause 计外部 unit port 质量；`T<2` 时每台外机至多承担一个 unit。第一组把“入任务存在时还能留下多少个 small”写成精确正部下界。这个结论是结构类的配置描述，不是一般配置 LP 的小描述，也不自动给整数调度或近似比。

## 2.2 必要性和充分性

必要性取内部机 incoming 事件 `I` 和每个 outgoing 任务留在父机的事件 `B_e`。其概率分别为 `q` 和 `1-t_e`，故 `Pr(I and B_e) >= (q-t_e)_+`；有 incoming 的配置最多再放 `s` 个 small，得到正部行。外部机在 `T<2` 下至多一个 unit，得到 clause 行。所有原 job 的边际覆盖 1 迫使这些局部边际属于同一配置 LP 点。

充分性用一个有理区间构造，而不是随机抽样。令 `a_e=1-t_e`、`c_e=(q-t_e)_+`，把长度 `c_e` 的 incoming 区间按顺序串接，再模 `q` 投到长度 `q` 的环上；总长度不超过 `s q`，所以任一点至多被 `s` 段覆盖，从覆盖断点取配置。剩余长度 `1-q` 的区间不含 incoming，在前缀区间放置 small；每个 small 的总边际为 `a_e`，总负载不超过 1。`q=0` 和 `q=1` 分支分别省略对应区间，避免模零。每行断点数 `O(k)`、有理位长多项式。

外部 port 质量按 clause 串接成 unit 槽，每槽映射到不同真实 unit 机器，空配置补齐；只需 `ceil(sum t_e) <= min(A_c,d_c)` 个 unit。selector、父端、子端和外端的列质量均为 1。构造的是每机配置分布和共同边际，未构造跨机器的一个全局联合采样；要求后一对象会把配置 LP 误读成整数调度凸包。

把 `(q-t_e)_+` 引入 `z_ue >= q_u-t_e` 的线性化后，`(P_s)` 是有理 LP。阈值只在 `T=1+s/k` 网格变化；在 `T=2` 已有全父置调度，因此二分网格可得精确配置阈值。输入为空时阈值为 0，`k=1` 单独处理，不能因巨大二进制 `A_c` 展开不存在的树。

## 2.3 严格单位阈值、整轨 LP和五三承诺算法

令 `n_cvs` 为变量 `v` 的 sign `s` 全部叶接入 clause `c` 的数目。严格 `T=1` 时，CONFIG 可行等价于整轨选择 LP
\[
y_{v0}+y_{v1}=1,
\qquad \sum_{v,s} n_{cvs}y_{vs}\le A_c.
\tag{L}
\]
正部行 `s=0` 沿每轨归纳出每叶外送边际至少对应根 selector 边际，得到必要性；反向把每轨所有深度的下传边际都设为 `y_vs`，内部行用 incoming 单任务配置和全 small 配置，外部按端口槽构造，得到充分性。

给定 `(L)` 可行解，选每个变量 `y_vs>=1/2` 的 sign 并固定 selector。设 `r=floor(k/2)`、`L=k-r+1`，递推 `x_0=1`、`x_l=(r-1+x_(l-1))/k`。选轨深 `l` 的分数任务数恰为 `x_(l-1)+k(1-x_l)=L`。把 incoming 放首槽，small 放余槽，按 clause 的外送质量串槽，用一次 Hall matching 覆盖全部原任务。含 incoming 的机器至多再接 `k-r` small，负载至多 `2-r/k`；未含 incoming 的机器总 small 负载至多 1，外部 unit 每槽至多一个 task。因 `r/k>=1/3`（奇 `k>=3`）或 `1/2`（偶 `k`），得到 `Cmax<=5/3`；`k=1` 用整数容量流得到负载 1。

因此该结构有一个确定性位多项式的 YES `OPT<=1`、NO `OPT>5/3` 承诺判定/构造。它不是所有输入的五三近似，更不是一般不相关机难度上界；若 `P=NP`，该严格单位模型不能直接承载 `rho>5/3` 的源 gap 归约。未选轨全部父置，不能把 active-only 槽条件强加给未选轨。

## 2.4 闭合两树族的精确配置阈值

对单变量两棵私有满 `k` 叉深 `h` 树、每个底层内部节点的 `k` 枚叶共享独有 terminal、`A=1` 的闭合族，实际
\[
OPT=2-1/k,
\]
而配置阈值精确为
\[
T_{CONF}=1+s_*/k,
\quad s_* = \min\{s\in\{0,\ldots,k-1\}:(k-s)^h\le2k^{h-1}\}.
\]
正部必要性沿轨逐层给出 `(k-s)^h y_vs <= k^(h-1)`，两根边际和为 1；充分性用两根各 `1/2`、层边际 `x_l=(1/2)((k-s)/k)^l` 和前述配置分解。已知严格单位 gap 族在满足 `(k-1)^h <= 2k^(h-1)` 时的精确配置阈值就是 `1+1/k`，所以其配置/整数比为 `2-3/(k+1)`，趋近 2。这个结论只针对闭合树对象；不能把阈值余量移植到非私有树、pins 或一般 UM。

# 3. 完整叶流与 selector 多见证重组

## 3.1 固定高度叶流近似

稳定身份 `UM-UNIT-READOUT-FIXED-HEIGHT-APPROX-v1`。对任意显式输入、任意密度和任意 `k,h>=1`，整数最大流先决定每变量能向 clause slots 送出的最大叶数 `b`。网络为 source→variable（容量 `b`）→该变量叶（容量 1）→clause（容量 `A_c`）→sink；二分 `b` 并只取实际叶数，得到整数叶选择。

若 `b=0`，任何 `C<2` 调度都会给每变量至少一条下传根叶路径，从而产生 `b>=1` 的可行流，故只能有 `OPT=2`，全父置即为最优。若 `b>=1`，每变量一轨至少保留 `m=ceil(b/2)` 枚流叶。令
\[
q=\lfloor(N-m)^{1/h}\rfloor,\qquad \hat r=k-q,
\]
其中 `N=k^h`。既有叶命中递推保证该轨标记叶中含一棵每内部 `rhat` 分叉的深 `h` rooted 子树；只删除流中已送叶，保留同一外部注入。沿该子树下传全部祖先和叶任务，其他任务父置，得到 `Cmax<=2-rhat/k`。

若 `OPT=2-r_*/k` 且 `x=r_*/k`，有 `b>=r_*^h`，从而
\[
\hat r/k\ge1-(1-x^h/2)^{1/h}.
\]
令 `c=2^{-1/h}`，利用 `f(x)=(1-x^h/2)^{1/h}` 的导数下界可得
\[
Cmax/OPT\le(1+f(x))/(2-x)\le1+2^{-1/h}.
\]
这个比值在固定 `h` 为严格小于 2，`h=1` 为 `3/2`；`h` 无界时余量趋 0，不能关闭一般近 2 目标。算法只用整数流、整数根比较和真实树 DP，复杂度按显式叶输入计；不需要 LP/OPT oracle。

## 3.2 给定 p 份完整 YES 的 selector mixing

稳定身份 `UM-UNIT-READOUT-SELECTOR-MIXING-v1`。给同一实例 `P` 的 `p>=1` 份完整真实调度，每份负载不超过 1，并为每变量指定一个 sign，要求该 sign 至少在一份调度的 selector 中出现；另假设非空 `N=k^h>=p`。则可在见证总编码位长多项式时间内输出满足全部指定 selector 根的完整调度，负载
\[
Cmax\le2-1/(2p-1).
\]
更细地，`k>=p` 时 `r=floor(k/p)` 给 `2-r/k`；`k<p` 且 `N>=p` 时取 `r=1`，给 `2-1/k`。`p=1` 直接保留给定 YES。

证明先从 p 份真实完整负载 1 的见证取指定轨。指定轨的所有叶在至少一份见证中外送，因此共同 clause 容量满足 `d_c^*<=pA_c`。其他未被任何见证选中的轨全部父置，不把它们错误地放进 active-only strong LP。对指定轨使用 `x_0=1`、`x_l=(r-1+x_(l-1))/k` 的校准槽；每行有 `L=k-r+1` 个分数槽，incoming 放在首槽。外部指定轨质量为 `d_c^* x_h<=A_c`，一次 Hall matching 覆盖全部未固定原任务，含 incoming 的机负载至多 `2-r/k`。

当 `k>=p` 时 `r=floor(k/p)` 且 `r/k>=1/(2p-1)`；当 `k<p` 取 `r=1` 并用 `N>=p` 得 `x_h=1/N<=1/p`。因此统一界成立。其前提是同一 P 的 p 份完整 YES 和共同容量，不能用不同输入的局部可行见证拼接；算法不负责寻找这些见证。

## 3.3 锐例和边界反例

`p` 个变量、`k=2p-1`、`h=1`，所有正轨叶共用一个容量 `A=k` 的 clause，各负轨有私有 clause。第 `i` 份 YES 只选变量 `i` 的正轨，其余选负轨；所有 YES 负载 1。指定全正时，若 `C<2-1/k`，每个正根至少外送两枚叶，共需 `2p` 台 shared unit 而只有 `2p-1`，所以精确负载为 `2-1/k`。这是满足指定 selector 模式的锐值，原实例全局 OPT 仍为 1。

`N>=p` 不能省略：`k=1,h=1`、两变量分别交换两个容量为 1 的 clause 时，两份完整 YES 存在，但指定第一变量正、第二变量负的模式强制两叶争同一 clause，真实最优为 2。这个反例也说明 selector mixing 不能被描述为“只要每个变量独立可用就能重组”。若输入是 NO、没有完整 YES，不能用该定理反驳一般归约。

# 4. 两源之间的关系和不能合并之处

两源共享同一私有树模型和单位外部端口，但证明接口不同。配置阈值源给出所有机器的**边际配置 LP** 的精确正部多面体，并在严格 `T=1` 时消元成整轨 LP；它允许每机配置分布只共享 job 边际。叶流源使用真实整数流和真实完整调度，把叶任务保留在共同 clause 容量中，再用树命中结构恢复祖先兼容性；它不把边际 LP 当作跨机器联合分布。

因此不能用叶流近似直接证明配置阈值等价于整数调度，也不能把严格单位 `5/3` 承诺算法写成任意阈值的配置 gap 结论。闭合树族的 `T_CONF=1+s_*/k` 解释了为什么只多一点 small 余量就可过配置 LP，而严格单位整轨仍受外部容量约束；该解释不消除叶流算法在高度无界时因子趋 2 的边界。

与既有四源审查相比，本页新增的可追溯对象是当前两份 canonical source ID、精确源指纹、正部多面体的区间/模构造细节、闭合树 `s_*` 阈值和叶流/selector mixing 的量词分离。校准槽、修剪森林 identity、half-density 和 leaf-hitting 的一般结果仅作为已审相关材料；本页不把它们重新登记成当前两个 source 的独有数学。

# 5. 证据层级、用途与未闭义务

**一般证明（在明示模型内）：** `P_s` 配置正部的必要充分性及有理区间分解；严格单位 CONFIG 与整轨 LP 等价；给定整轨见证的 `5/3` 承诺构造；闭合两树的精确 `T_CONF`；固定高度叶流的 `1+2^{-1/h}` 保证；给定 p 份完整 YES 的 selector mixing 界、`d_c^*<=pA_c` 推导和 `2-1/(2p-1)` 锐例。

**有限精确证据：** 配置阈值审计列出的完整调度、单行分解、wiring/weight、边界和非法输入检查；叶流审计列出的关键实际 schedule、361 jobs 的 selector mixing、独立 sharp-profile 矩阵回算和 root literal 回算。它们使用 Fraction/整数并保留空、零容量、巨大分母、`N<p` 等边界，但不替代一般证明，也不实现通用 LP/OPT oracle。

**开放义务：** 尚无未知 YES witness 的寻找算法、一般不相关机器的近二 gap/硬度、无 pins 与 private pins 的统一合同、任意阈值的全局配置联合分布、selector mixing 对 NO 实例的解码结论。若继续接入第三阶段关系图，应保留以下有向关系：

- `正部配置 LP --严格 T=1 消元--> 整轨选择 LP --active-only 槽--> 给定 witness 的 5/3 读出`；
- `完整 YES 叶流 --共同 clause 容量--> 祖先兼容子树 --> 固定高度 1+2^{-1/h}`；
- `p 份完整 YES + N>=p --selector mixing--> 指定 profile 负载 2-1/(2p-1)`。

这些边都带有来源模型、共同容量、完整 witness 和高度/`N` 条件，不能从旧图摘要直接泛化。

# 6. 逐源处置

- `40a75aa26f402db03c39`：`integrated`。完整源的 `P_s` 正部系统、区间分解、严格单位整轨 LP、`5/3` 承诺算法、闭合树精确配置阈值及有限证据边界写入第 2、4、5 节；与旧配置/槽审查的重复仅作为比较材料。
- `dce12333944853ff579d`：`integrated`。完整源的固定高度整数流、叶祖先命中、`1+2^{-1/h}` 比值证明、p 份 YES selector mixing、锐例 `k=2p-1` 和 `N<p` 反例写入第 3、4、5 节；不把完整 YES 条件扩展到 NO 实例或未知见证。

两源均全文件实读；相关 canonical/review/程序/evidence 已比较；数学独有内容、重复内容去向、有限证据和开放边界均已明确记录。
