---
id: "unrelated-machines/partial-minrep-pdm-threshold-review"
kind: "review"
type_tag: "审查"
title: "部分MinRep费用桥与pDM阈值双源审查"
status: "integrated-with-explicit-conditional-boundaries"
truth_status: "source-level general proofs plus scoped bridge/finite counterexample; no-UM-hardness"
review_level: "full-source-read-and-related-review-comparison"
scope: "partial Min-Rep sparsification/regularization and p-dimensional matching integer threshold bridge"
source_refs:
  - "source:782a8563344b6f317c3e:research/current/unrelated_machines/partial_minrep_linear_degree_source_and_fee_bridge.md"
  - "source:4edaa33bd4a272da6a6a:research/current/unrelated_machines/pdm_threshold_scheduling_bridge.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/partial_minrep_linear_degree_source_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/pdm_threshold_domain_and_gap_review.md"
legacy_ids:
  - "UM-PARTIAL-MINREP-SPARSIFICATION-BRIDGE-v2"
  - "UM-PARTIAL-MINREP-REGULAR-HIGH-GIRTH-SOURCE-v3"
  - "UM-PARTIAL-MINREP-DEGREE-MASS-REGULARIZATION-v5"
  - "UM-PERFECT-COMPLETE-SEED-CERTIFICATE-v1"
  - "UM-PDM-THRESHOLD-EXACT-v1"
---

# 1. 实读范围与两源关系

本批完整读取两个当前 canonical 正文及其全部尾部，回读正文链接的审查、模型/账本相关页、PCP/Min-Rep 文献定位和 pDM 反例审计入口。源 `782a8563344b6f317c3e` 的路径为 `research/current/unrelated_machines/partial_minrep_linear_degree_source_and_fee_bridge.md`，SHA-256 `33f5fb337e3d002e91aad79c6fb99f273ed01c1978d02fd0131e995a948e2114`，33322 bytes；源 `4edaa33bd4a272da6a6a` 的路径为 `research/current/unrelated_machines/pdm_threshold_scheduling_bridge.md`，SHA-256 `eae74ed7730533a0ae6531acb79ff88dc47663dfc06884a1fe70bcefd2e668f2`，6816 bytes。两源均来自冻结提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`。

两源都试图把源问题的完备/不完备差异转成普通 unrelated-machines 的真实调度义务，但证明层级不同。部分 Min-Rep 源给出随机删边、正规化、高围长和任意 degree-mass 复制的 source-level soundness，并推导一个“若未来有 UM 编译器则可支付费用”的条件桥；它没有给出实际 UM 编译器。pDM 源给出一个整数阈值的精确 `OPT<=bd` 当且仅当完美 d-dimensional matching 的桥，但无完美匹配时只得 `OPT>=bd+1`，并以有限实例展示 NO 侧仍可能只高出阈值一个单位。两项不能拼成近二困难性。

本页将两个 source ID 均处置为 `integrated`，把 source 证明、条件费用桥、随机种子复杂度后果、pDM 整数阈值、有限反例和未闭的物理解码义务分别保留。

# 2. 部分 Min-Rep：随机删边和线性度数 source

## 2.1 v2 原图删边合同

稳定身份为 `UM-PARTIAL-MINREP-SPARSIFICATION-BRIDGE-v2`。输入是两侧各 n 个顶点的显式 D-regular 二部投影游戏，N=2n，公共字母表大小 Q>=2，每条边带全映射投影，允许平行约束。单标签值 `val` 是满足边比例；多标签列表 cost 是所有顶点列表长度之和，边被覆盖当且仅当端点列表存在一对满足投影。

给二进制 `g>=2`、有理 `0<rho<=1`，令
\[
\ell=\lfloor\log_2 g\rfloor,\quad
\lambda=1+\lceil\log_2Q\rceil,\quad
\tau=\rho/(100g^2),\quad
\gamma=\rho^3/(10^9g^8),
\]
\[
\mu=\left\lceil1000g\lambda/(\rho\ell)\right\rceil,
\qquad \Delta=1000\mu.
\]

随机保留每条边（若原 D<2mu 直接保留；否则以 dyadic probability p=2^{-s} 采样），再删去端点中间度数超过 Delta 的全部关联边。每个 seed 的最大度数均 <=Delta；`val=1` 时原 singleton assignment 对每个 seed 保留全部剩余边；若 `val<=gamma`，以至少 .9 概率输出非空图且任一 cost<=gN 列表覆盖比例严格小于 rho。其位复杂度按显式输入、binary g/rho 总位长为多项式，不按 mu、g、1/rho 数值循环。

廉价列表的原图覆盖率先压到 tau：长度大于 H=4g/tau 的顶点只占少数关联边；对剩余短列表独立抽标签，若覆盖至少 tau/2 的边则得到单标签 value 至少 tau/(2H^2)=rho^3/(32*10^6 g^8)>gamma，矛盾。廉价列表数量用生成函数上界 `K<=exp(gN lambda)`，不实际枚举。

采样中间边数 Y 的共同事件只做一次；固定列表的覆盖边数用 Chernoff，所有列表再 union bound。高度边删除以条件期望和 Markov 控制。三类坏事件总概率小于约 .018，最终边集非空且覆盖率小于 rho。这里必须保留“总边数事件只控制一次”的概率结构；不能把一次对 Y 的保证误写成每个列表独立的额外事件。

## 2.2 v3 正规/简单/高围长与 v5 typed 不正规修复

`UM-PARTIAL-MINREP-REGULAR-HIGH-GIRTH-SOURCE-v3` 固定 G>=2，先建立每个原顶点的 z slots，按 edge type 分组，在 d layers 中做独立随机 permutations，形成 d-regular template matching；枚举长度 2..G 的短环，若短环数超过 B 返回 FAIL，否则在同 type/layer bucket 内找远距干净边做双边交换。交换保持 projection type 和每层 perfect matching，消除短环，输出 simple girth>G source。sampling failures 有硬位上界，FAIL 事件概率小于 .1；NO 侧对所有 cost<=gN' copy lists 同时控制 covered<rho M' 的概率至少 .8，YES 侧非 FAIL 时复制原标签完美满足。

随机 soundness 的关键是 arbitrary copy lists 的同时性：heavy copies 总数受总 cost 控制；light lists 逐原点抽样给单标签期望 value<=gamma，模板边覆盖边际平均小于 tau；不同 permutations 对 distinct slots 的密度至多 e^j，factorial-moment/Chernoff 对全部 lists 一次控制。repair 每换两条边最多增加两条 covered edges，参数 `M'>=8B/rho` 支付该误差。G 固定时 bit complexity polynomial；G 变参时指数依赖 G 不被隐藏。

`UM-PARTIAL-MINREP-DEGREE-MASS-REGULARIZATION-v5` 不要求原图 regular、两侧同大或有界 degree。删孤点后每个原点建立 `t_v=deg(v)z` copies，按 incident edge type 各分 z slots；因此抽一条原 edge 再抽两端 copy 时，heavy mass 以
\[
\frac1{M_0}\sum_{e=(a,b)}(h_a/t_a+h_b/t_b)=\frac{2h}{N'}
\]
精确抵消 degree，不需要原 regularity。保留 typed 左右 alphabet、投影 surjectivity/equal-fiber 和平行 edge type，输出 balanced exact d-regular simple girth>G source。v5 的 Qgamma>=1 域、硬位数、FAIL 处理和 fixed-parameter PCP corollary 必须单独写明；不能把 fixed-parameter alphabet padding 改写成任意 binary g/rho 的 uniform polynomial routine。

## 2.3 费用桥和种子复杂度后果

source 本身不是 UM 编译器。它只给出一个条件桥：若未来有真实 UM 编译器，对每个好 source 输出完整实际调度 `sigma`，在弱阈值下提取 covered>=rho M 的列表，且
\[
cost(psi)\le N+B(\sigma)/F,
\qquad0\le B(\sigma)\le cM,
\]
则 `F>=c Delta/[2(g-1)]` 与 `M<=Delta N/2` 足以推出 cost<=gN，违反 source NO。v3 中 N/M 应替换为复制后的 N'/M'；更多复制、高围长或 Hamming 距离本身不支付固定 F，若同时放大 B 的系数 c，收益可能消失。真实 trigger、同一源点列表一致性、投影接口、B 的不重复计数和固定费用仍未构造。

正文另立 `UM-PERFECT-COMPLETE-SEED-CERTIFICATE-v1`：若随机完备 source 生成器 R 每条 seed 返回合法显式实例或 FAIL，SAT 对所有 seeds 都被确定性判别器接受，而 UNSAT 至少有一个 seed 被拒，则 UNSAT 有 NP 证书，得到 NP=coNP；若 UNSAT 有固定逆多项式拒绝概率，则得到 NP=RP=coRP=coNP。FAIL 直接按 YES，且该推论不能把随机 source 的 `NP subseteq BPP` 写成 P!=NP。

对 UM-TARGET 的条件推论还需真实编译器：SAT 所有非 FAIL seed 的 OPT<=T；某个好 seed 上每个低于 `beta_k T` 的完整实际调度都导出违反 source NO 的列表，其中 `beta_k=2-1/k`。只有这项全输出 decoder 和逆多项式好 seed 概率同时成立，才能从 `(2-epsilon)` 算法得到复杂度矛盾。单个 LP certificate、某个低负载 schedule 或 source 好事件概率不足以支付这项义务。

## 2.4 证据和范围

v2/v3/v5 的 source soundness 来自符号概率证明和明确的位复杂度；随机删边、short-cycle repair 和 list tail 分析中保留所有 FAIL/好事件量词。PCP 文献只作为完美完备、投影、重复和 exact k-to1 的 Paper Fact，不把文献摘要当本稿完整证明。source 没有生产 UM 编译代码，也没有完成一般近二硬度；高围长本身不是调度费用。

# 3. pDM 整数阈值桥

## 3.1 精确构造和 iff

稳定身份为 `UM-PDM-THRESHOLD-EXACT-v1`。固定 d>=3，给 d 个互不相交、各大小 n 的顶点集及 m 条 d-超边；每条超边机器 m_e 一台。每个顶点 v 产生任务 g_v：只在包含 v 的超边机器上可用，处理时间 b；每台机器再有 b(m-n) 个 dummy 任务，每个机器处理时间 d。取整数 b>d 且 gcd(b,d)=1。

总工作量为
\[
dn\,b+b(m-n)d=bdm.
\]
完美 d-dimensional matching 取 n 条互不相交超边：对应机器各放 d 个顶点任务，未选机器各放 b 个 dummy，峰值 bd。反向若调度峰值 <=bd，由总工作量等于 m*bd，每台机器恰负载 bd。写一台机器收到 k 个顶点任务、ell 个 dummy，负载 `bk+d ell=bd`；互素性推出 d|k，且机器最多接 d 个 incident 顶点，故 k 是 0 或 d。恰 n 台机器接 d 个顶点任务，组成完美匹配。因此无完美匹配只推出 OPT>=bd+1。

该构造是精确阈值 NP-hard 的受限整数 R||Cmax 桥，不能把加一下界误写成乘性 gap。`b`、`d` 是固定参数时，任务/机器显式规模多项式；若 b 是 binary 可变并且显式复制 dummy，必须另核输出大小。合法域还需处理 `m<n`、孤立源顶点和 `n=m=0`，不能默默加入完备性假设。

## 3.2 低负载逃逸与已知槽上界

有限控制实例 d=3,n=2,m=3,b=4 的三条边两两相交，没有完美匹配；阈值 T=bd=12，10 个任务的全部合法分配用 Fraction 穷举得到 OPT=13、机器 loads `(12,11,13)`，比值 `13/12`。它保留阈值定理，却反驳“没有完美匹配自动产生近二 NO”。

相关审查还指出合法编译的 `max p=b=T/d`，assignment LP(T) 不可行可可靠拒绝，可行时普通槽舍入给 `C<= (1+1/d)T <=4T/3`。这只限制本形状的近二方向，不是一般 UM 的新算法。

二值 max-min 文献通过 BLMRS 两值等价最多传递 `2-1/(pq/(pq-1))=1+1/(pq)` 级调度阈值，最小允许 pq 已给 `13/12`，随 pq 增大趋 1。它不能替代统一 `(2-epsilon)` 反面，也不提供 gap amplification。

# 4. 双源比较、第三阶段用途和开放义务

部分 Min-Rep 源的核心对象是“完美完备、列表覆盖 soundness、随机 source 和未来实际 decoder”；pDM 源的核心对象是“总工作量锁定的整数阈值 iff”。前者的 degree/girth/regularization 只保证 source 的组合性质，后者的 gcd 只保证恰 bd 阈值。两者都没有把每个 NO 实例的所有部分调度排除在接近二之外，因此不能合并成 UM-TARGET 反例。

第三阶段可记录三条关系：

- `source list soundness + 真实 UM 编译费用` -> `低负载调度导出 cheap lists`；边是条件桥，当前缺 trigger/decoder/F。
- `完美 complete seed certificate + 全输出 UM decoder` -> `NP=coNP 或 NP=RP=coRP=coNP`；边的概率、FAIL 和严格阈值方向必须保留。
- `pDM perfect matching` -> `OPT<=bd`，`OPT<=bd` -> `perfect matching`；只有阈值判定，不能标为近二 gap。

开放义务是：为部分 Min-Rep source 提供完整、真实、位多项式 UM 编译和全输出低负载 decoder；控制 source copy 的同一原点标签、成本和 projection 接口；处理 Qgamma 域、固定 G/PCP 参数、FAIL 语义及费用常数。pDM 方向需要真正的乘性 gap amplification，同时阻止普通调度中的分数/部分分配逃逸。两源都没有六人客户/共同目录 SPE 含义。

逐源处置：

- `782a8563344b6f317c3e`：`integrated`。v2 原图删边、v3 regular/simple/high-girth、v5 degree-mass typed 复制、degree 必要性、seed certificate、条件费用桥和 UM 编译缺口写入第 2、4 节。
- `4edaa33bd4a272da6a6a`：`integrated`。pDM 的整数阈值 iff、gcd/总工作量证明、合法域限制、13/12 逃逸实例、槽舍入边界和不能升级近二的结论写入第 3、4 节。

两源均已完整实读，相关审查、代码/证据入口和外部 Paper Fact 的适用范围已比较；独有内容去向及所有真实运行边界已明确记录。
