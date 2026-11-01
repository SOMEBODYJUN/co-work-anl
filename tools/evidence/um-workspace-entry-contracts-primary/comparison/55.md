# 全局行基数过滤与多外层单态小 home 双源审查

## 来源身份与实读范围

本页完整读取并比较两个冻结来源：

- `8e7fbfe13b8dcfeb9ec6`，`research/current/unrelated_machines/row_count_escape_gap.md`，blob `5beb58d8907a9854d3cebe7f7b1656f8101c248c`，SHA-256 `a075bf8984891b4c557aa491329f087a3b0d539e5de2babe6bec2e3f7b83aa1e`；
- `c43c08d4bf6fe07ad2bf`，`research/current/unrelated_machines/multi_outer_single_state_tiny_home_rounding.md`，blob `ced8586c536a63bc86dc2c30e4ba6779fb016380`，SHA-256 `f91b32aba8da447fb0838849fb1a63a1d48296b96e5bb156646eb01c67c27aec`。

两源均冻结于 `68fad804ec5946cb296f77dc5b336308a66abf12`（legacy-cleanup）与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`（main）。同步读取了全局行计数、紧凑共享逃逸、条件块切面、normalized-flat 值桥、共享 UD/tiny-home 审查及有限审计。第一源是必要的全局行基数过滤和一族通过所有逐机计数/配置探针但整数值趋二的反例；第二源包含 v1、v4、v5 三个明确版本的单态 outer、小 home 和共享 fallback 限定域算法。版本身份、量词和证据范围保持分开，不能把后续扩域结果回写为旧 v1 的结论。

## 一、全局行基数过滤的安全性和紧凑逃逸

### 1. 精确过滤合同

给合法不相关机输入 (P,T)，先保留每个任务 (j) 的当前域 (D_j={i:p_{ij}\le T})。对每台机器取
\[
h_i=\min\{p_{ij}:i\in D_j\},qquad
c_i=\begin{cases}0& D_j\text{均为空},\\ n&h_i=0,\\\min(n,\lfloor T/h_i\rfloor)&h_i>0.\end{cases}
\]
(c_i) 只是任何 (T)-调度在该机上能放的任务数上限，不是负载容量。

对存活边 (j\to v)，暂时固定 (j) 在 (v)，把其余任务分成必须离开 (v) 的 (Q_{vj}) 与可留可送的 (B_{vj})。在 (M\setminus\{v\}) 上按每机容量 (c_i) 求覆盖 (Q_{vj}) 的 b-matching，并最大化从 (B_{vj}) 卸出的真实权 (p_{va})。若无覆盖或
\[
p_{vj}+\sum_{a\in B_{vj}}p_{va}-W>T,
\]
则删边；同步重算行最小值并迭代至稳定。`UM-GLOBAL-ROW-COUNT-FILTER-v1` 的结论是确定性位多项式、保留所有 (T)-可行调度的全部边；拒绝蕴含 (OPT>T)，接受不保证已有调度。

安全性来自任意保留边的 (T)-调度：其余任务限制到匹配，(v) 上的真实负载不小于公式左侧，所以不会误删。匹配按容量槽增广、按 (p_{va}) 非增次序最大化可卸载权；槽数截到 (n)，不按二进制容量数值展开。对同一固定行下界得到的任意资源子池，全球 (M\setminus\{v\}) 查询支配子池查询；若子池重新改变下界，则不在本等价合同内。

### 2. 紧凑多项式族和整数值

固定 (k\ge2)、(N=2k^2)、(G=N-2k)。有 (N) 个中心 (V_a)、(G) 个全局机、每块 (k+1) 个局部机及共享机 (z)。任务 (X_a) 可去自身中心或任意全局机，(Y_{a,s}) 可去本块局部机或 (z) 用 (1/k)，(Z_{a,s}) 可去本中心用 (1/k) 或本块局部机用1。输入规模和时间均为 (k) 的显式多项式，时间值只用 (1/k,1,\infty)。

任何 (B<2-1/k) 的调度中每个全局机至多接一个 (X)，至少 (2k) 个中心接 (X)；若中心不把至少两个 (Z) 外送，就达到 (2-1/k)。每个活跃块因此至少把一枚 (Y) 送到共享 (z)，使 (z) 负载至少2，矛盾。显式上界达到
\[
OPT=\theta_k=2-1/k.
\]

在 (T=1) 有完整单机配置和全部 GPC(_2(1)) 两机联合证书；(G)-(G)、块内 (R)-(R)、(V)-(R)、(V)-(G) 的联合分布逐项满足边际和不双选。不同 pair 证书不要求共用一个全局分布，故不升级为完整高阶一致性。

### 3. 所有逐机计数和配置探针仍通过

对任意指定机器 (v)，来源构造避开 (v) 的完整任务分配，使其它机器只满足 (c_i) 计数上界；从该分配移走任意单机配置 (C\in\mathcal C_v(1)) 并固定在 (v)，得到每台机器的单配置计数延伸见证。故第一轮全局 row-count filter 不删除任何边；极小超载星、单/双域基数闭包也均无起点。

进一步的 `UM-COMPACT-MULTIROW-EXTENSION-v1` 在同一族给定机器集 (U) 上要求 (U) 内真实负载不超过1、全机仍满足 (c_i)。当 (U) 中中心数不超过 (G) 时，每个 (v,C) 均能显式构造延伸；当中心数为 (G+1)、固定 (v=z,C=\varnothing) 时，所有 (Y) 只能去局部槽，中心和全局机的槽数不足以容纳全部 (X)，故精确失败。这个 (G) 是该族该合同的最大中心预算。

`UM-MACHINE-CONFIG-PROBE-GAP-v1` 更强地要求：对每台机器和每个合法配置 (C)，存在完整 machine CONFIG LP 点且该机行固定为 (C)。本族 (T=1) 通过所有此类独立探针而 (OPT=2-1/k)，所以逐机配置延伸、GPC(_2)、行基数过滤的合取仍可保持趋二整数 gap。不同探针允许不同全局点，不要求跨探针联合一致；不能把它误写成完整层级。

## 二、多外层 single-state tiny-home 的限定算法

### 1. v1：(k^4) tiny-home 域

正式身份 `UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v1`。输入是 normalized-flat typed (Q)：有 (k) 个 single-state outer，每个 outer 的正 home 权重和为1、所有 home 物理互异；每个 home 有一个 unit-own helper；helper 可有任意显式共享 (B)-资源 fallback 菜单，所有 state 权非负且和为1。要求最大 home 权重
\[
\nu=\max w_j\le1/(4096k^4).
\]
完整普通 UM 保留所有 selector、未选 state incidence、zero/duplicate payload 和 unused resources。

来源给出不输入 OPT、可行点、联合 law 或调度 oracle 的确定性位多项式算法，输出全部原 jobs，峰值
\[
C_{\max}\le(19/10)OPT.
\]
定义 disjoint bundle welfare (V) 后有精确值桥 (OPT=2-V\)。算法先解一个有限二阶 rational LP：每 state 质量至少固定阈值 (\varepsilon=15/16)。LP 失败可可靠推出 (V<15/16)、(OPT>17/16)，直接输出全部 jobs 的 baseline 峰值至多2，且 (2/OPT<32/17<19/10)。

LP 可行时，按 singleton identities 提取 helper fallback 的一阶/资源 claims；用独立 helper profile、资源规则、weighted CDF 下界、Floored rational MW，随后对所有 helper state 和 resource-rule coins 做逐项条件期望，保留每个 outer 的实际资源值 (W_i>1/5)。不得在条件期望后删除请求 coins 再取 chosen state 的最大 bundle，否则会破坏逐 outer 平方势。取 (q=1/10) 的 Good helpers，保留其真实不交 fallback bundles，其余 helper 回 own home；所有原 jobs 按原 finite endpoints 回填，得到 (C\le2-q=19/10)。

证明依赖 helper 独立 profile、逐资源独立规则、tiny 上界、共享 (B) 与 homes 不交、完整源矩阵和有理公共分母。有限 backend 只核两个小实例的 moments/条件期望，未运行完整 LP、(N) 轮 MW、tiny 域或全部原 jobs，不能当端到端实现。

### 2. v4：共享 UD 叶、k1 greedy 与 k2 曲率

v4 另立 `UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v4`。它仍要求 single-state outers、互异 homes 和共享 (B)-only fallback；允许额外 B-only exact-threshold UD leaves。(k=1) 使用确定性 helper greedy，不需 tiny 上界；(k\ge2) 要求
\[
\nu\le1/(16384k^2).
\]
算法用固定 profile 的普通 matching linear oracle 做 rational Frank–Wolfe，再用 (k^2) 型凹 reciprocal 势和局部替换搜索；若所有 outer 值达到 (25/128) 则 prefix-flow 与叶 matching 回填全部原 jobs，若无足够实际势进展则可靠推出 (V\le18/19)，baseline 峰值2仍满足 (19/10) 比值。prefix-flow 采用整数 lower-bound circulation，保持叶完整匹配和 outer 资源前缀计数。

这是独立于 v1 的 typed 算法身份，不能把 v1 的 CDF/MW 证明自动替换成 v4 的 (k^2) 证明。v4 的作者稿、独立重构和有限交换审计分别记录，软件只覆盖交换 lemma 小实例，没有运行完整 profile 搜索、FW、prefix-flow、k1 greedy 或全 jobs 输出。

### 3. v5：(O(1/k)) home 与全有理实际分配

v5 再立 `UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v5`，把 (k\ge2) 的 home 上界放宽为
\[
\nu\le1/(1024k),
\]
并保留 single-state outer、互异 homes、shared UD leaves、all indexed/zero/inactive jobs。它用 weighted matroid rank 的次模性、每 helper 线性最优 state candidate、分段有理 reciprocal 势和固定 (\tau=1/100) 的真实势进展；停止时若任一 outer 低于 (q=19/100)，反证给 (V\le18/19)，否则用 Good helpers、完整叶 matching 和 prefix-flow 回填，仍得到 (C\le19/10)。k1 另用无 tiny 的同一实际候选势分支。

v5 的计算逐候选调用普通 matching independence oracle，不调用非线性 profile 最优化、SDP 或指数枚举；分段势跨线性/倒数区间的余项以有理不等式控制。它仍只在 typed v5 域成立，未覆盖多 state outer、home 重叠、home 上 extra groups、一般 non-UD 叶或任意 UM。作者算法正文和有限软件分别处置，不能把该后端称为一般可执行程序。

## 三、比较、证据和开放边界

第一源独有的是安全的全局行计数过滤、固定下界下所有资源子池由全局查询支配、完整 GPC(_2)/单机配置/多行探针仍通过的紧凑趋二族，以及共享中心预算 (G) 的精确失败阈值。第二源独有的是 normalized-flat 单态 outer 的 v1/v4/v5 三套明确域算法、(19/10) 实际比、可靠 FAIL 语义、helper profile/条件期望或 reciprocal 势、整数 prefix-flow 和 tiny-home 位复杂度。

两源共同说明：完整资源任务身份、多槽匹配和每个单机配置的独立延伸，仍不能代替跨机器共同负载与跨探针联合一致性；反例族可以通过所有这些逐点检查而整数最优趋近2。相应算法的正面结果依赖 very narrow typed domains、互异 homes、single-state outer、共享 B 资源与 tiny 权重上界，不能推广为一般 UM 近二算法。

有限审计、Fraction 回算、作者/独立重构及 root replay 只支持指定范围；尚未实现或证明一般 source profile 搜索、全局共同条件分布、任意多 state outer 的解码，也没有把任何失败分支写成一般不可行判据。两源都不含六人 SPE 客户目录、六提供者完整历史、终局均分或任意平局语义；`UM-TARGET-v1` 与六人 SPE 覆盖目标继续开放。

## 处置

两源均 `integrated`。第一源的 row-count filter、紧凑逃逸、multirow/config probe 和阈值边界写入第一节；第二源的 v1/v4/v5 版本身份、算法步骤、位复杂度与证据边界写入第二节。未成熟的跨 profile 联合算法、一般 source decoder 和近二 hardness 保留为开放问题，没有因已通过逐机检查而丢弃。
