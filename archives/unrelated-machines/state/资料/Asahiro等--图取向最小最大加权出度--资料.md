---
id: "unrelated-machines/asahiro-miyano-ono-2011-weighted-orientation"
kind: "resource"
type_tag: "资料"
title: "Asahiro–Miyano–Ono 2011：图类上的最小最大加权出度"
status: "source-read-draft"
summary: "作者稿全文实读：定义带正整数边权的最小最大出度（MMO），给出仙人掌图精确算法、有界树宽伪多项式动态规划，以及外平面/系列并行/平面二部等图类的弱或强 NP-困难性；保留简单外平面图开放边界。"
truth_status: "literature-results-read; no independent external citation verification"
review_level: "full-pdf-text-read-with-proof-sections"
scope: "restricted unrelated-machines scheduling/orientation literature; separate from six-provider customer SPE"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/literature/unrelated_machines/asahiro_miyano_ono_2011_cactus_orientation_author.pdf"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/literature/unrelated_machines/asahiro_miyano_ono_2011_cactus_orientation_author.pdf"
source_sha256: "5db93652d80fd92b6440e0a0e22edfdeb09f78e2b886c95cb4adf171c67ee147"
source_size_bytes: 271837
source_title: "Graph Classes and the Complexity of the Graph Orientation Minimizing the Maximum Weighted Outdegree"
authors: "Yuichi Asahiro, Eiji Miyano, Hirotaka Ono"
source_date: "2010-10-29 preprint; author manuscript made available 2011"
license_notice: "PDF states CC-BY-NC-ND 4.0 for this manuscript version"
related_objects:
  - "../定义/不相关机器与两个调度松弛--定义.md"
---

# 阅读边界与对象身份

本条目对应冻结作者稿 `history/source/literature/unrelated_machines/asahiro_miyano_ono_2011_cactus_orientation_author.pdf`，两个冻结提交的字节相同；`clean show` 报告源 SHA-256 为 `5db93652d80fd92b6440e0a0e22edfdeb09f78e2b886c95cb4adf171c67ee147`，大小 271,837 字节。PDF 从摘要、定义、全部算法章节、三个困难性归约、结论和参考文献逐段转写阅读。本文档保存论文声称和其在稿件中给出的证明机制；没有对参考文献外部网页、期刊最终排版或作者身份做独立核验。

这是一项图取向/受限调度文献资源，不是当前六人共同目录、客户均分效用、完整有序历史纯 SPE 的证明。论文的 scheduling 对照把节点看作机器、边看作任务，每个任务只能在预先给定的两个端点机器中选一个，且该任务在两个端点的处理时间相同（等于边权）。因此它只是一般 unrelated-machines 模型的一个很窄的二端点子类，不能把下述图类结论直接代入六提供者问题。

# 1. MMO 模型和调度对应

给无向边加权图 (G=(V,E,w))，其中 (w:E\to\mathbb Z_{>0})。一个 orientation \(\Lambda\) 给每条边选一个方向；节点 (v) 的加权出度是
\[
 d_G^+(\Lambda,v)=\sum_{(v,u)\in\Lambda}w(\{u,v\}),
\]
目标是最小化
\[
 \Delta_\Lambda(G)=\max_{v\in V}d_G^+(\Lambda,v),\qquad
 \Delta^*(G)=\min_\Lambda\Delta_\Lambda(G).
\]
记 `S-MMO` 为边权取值在 (S\) 的版本；无权函数限制时是 \(\mathbb Z_{>0}\)-MMO，论文主要研究 (S=\{1,2,\ldots,k\})。任意 orientation 都有 \(\Delta_\Lambda\ge w_{\max}\)。

调度翻译为受限的 (R\|C_{\max})：节点是机器、边是作业、边的两个端点是该作业仅有的两台可选机器，且两端处理时间同为边权。论文明确指出，这种限制与一般 unrelated-machines 的任意资格集合和机器相关处理时间不同。

## 1.1 带节点初载的推广

为处理仙人掌算法，作者引入 `(S,T)-MMO`：输入 (G=(V,E,f,w))，其中正整数边权 (w:E\to S)，节点初载 (f:V\to T)，并定义
\[
 d_G^+(\Lambda,v)=f(v)+\sum_{(v,u)\in\Lambda}w(\{u,v\}).
\]
`(S,T)-MMO(K)` 问是否存在 orientation 使每个节点出度不超过 (K)。当所有 (f(v)=0) 时退化回 `S-MMO`。节点初载是算法删边、转移边权时的账本；它不是客户价值或提供者效用。

# 2. 仙人掌图：精确决策和优化

仙人掌图的每条边至多属于一个简单环；其二连通分量只能是单边或环，分量块构成树。论文的 `AlgCactus(G,K)` 先在线性时间构造块树，然后反复处理一片叶块：

* 对叶环，若存在非 gate 节点 (u) 使 (f(u)+w(e_u)+w(e'_u)\le K)，把两条环边都定向离开 (u)，删去 (u) 和这两边（2-1a）。
* 若某端点满足 (f(u)+w(e)>K)，则在任何成本至多 (K) 的解中该边必须指向 (u)；算法固定方向 (v\to u)，把边权加到另一端的节点初载并删边（2-1b）。
* 若前两种均不能用，令 g 为 gate（无 gate 时任取环上一点）；将 g 的两条环边中较重者定向进入 g、较轻者定向离开 g（等权任取），转移相应初载并删去这两条边（2-1c），再把环余部按路径处理，最终得到同向的整环取向。gate 因而只支付较轻边；这与冻结稿印页8的 Fig. 3 及 Step 2-1c 的 (x,g)、(g,y) 方向一致。
* 对叶路径，若叶 (u) 的 (f(u)+w(e)\le K)，定向 (u\to v)；否则定向 (v\to u) 并把边权转到 (v) 的初载，逐叶剥离。

若过程中某剩余节点初载超过 (K)，输出 `No`；否则输出 `Yes` 及完整 orientation。正确性依赖四个单调性事实：增大节点初载不会降低最优值；删边或删点不会增加最优值；以及若 (f(u)+w(e)>K) 且原图可行于 (K)，该边方向被迫指向 (u)，可把它转为另一端的初载。环的 2-1c 用顺/逆时针比较 gate 初载来保持可行性。

每个块只被剥离一次，`AlgCactus` 决策运行时间为 (O(|V|))（仙人掌图有 (O(|V|)) 条边）。对边权 (\{1,\ldots,k\})、节点初载全零的优化问题，论文证明任意仙人掌图有
\[
 \Delta^*(G)\le f_{\max}+2w_{\max},
\]
并用决策算法二分 (K)，得到 `Theorem 9`：`{1,…,k}-MMO` 在仙人掌图上可于 (O(|V|\log k)) 时间精确求解。论文还指出开放问题：能否把该优化运行时间降到 (O(|V|))。

# 3. 有界树宽：伪多项式动态规划

对于树宽为 \(\tau\) 的图，论文取宽度 \(\tau\) 的树分解并二叉化，按分解树的边分区定义子图 (G[i])。状态
\[
 W_{BT}(G[i],a)=\min\{\Delta_\Lambda(G[i]):d^+_{G[i]}(\Lambda,u)=a_u\ \forall u\in X_i\}
\]
（不存在的状态为 (+\infty)），其中袋向量每一坐标的范围至多为该点的总 incident 权。父节点把两个子状态和当前常数大小的袋内边所有 orientation 枚举结合；共享袋点的出度向量相加，新出现点的子贡献为零。状态数为 (O((k|V|)^{\tau+1}))。论文 `Theorem 10` 声称
\[
 O((k|V|)^{\tau+1}|E|)
\]
时间；但冻结稿印页12–13的递推对两个子袋向量取最小，随后把单节点费用直接界为一张表的大小，没有支付这些向量的配对费用。常数级袋内边方向枚举只支付每个子状态对的本地检查，不能据此证明整个 join 为常数次检查。这里不把该精确时间声称当作已经独立核实，也没有给出否定该时间界的复杂度下界。

可直接确认的实现如下。令 n=|V|、m=|E|；在简单图、给定宽度至多τ且有 O(n+m) 个节点的二叉树分解中，每个袋负载坐标至多 k(n−1)，单表状态数至多 S=(kn+1)^(τ+1)。枚举两个子状态和本地 E_i 的全部 2^{O(τ²)} 种方向，计算唯一的父袋负载向量，并以两子表值与全部父袋负载的最大值更新该父状态。父袋以外的点至多出现在一个子树，否则树分解的连通性会迫使它也在父袋；所以子表中的旧最大值和父袋合并负载已经包括所有真实顶点。反过来，固定两个兼容接口时分别取达到子表最小值的取向即可合并，故这一递推双向精确。保存达到更新值的两个子状态和本地方向即可回溯完整取向。

因此安全时间界为 O(2^{O(τ²)}(kn+1)^(2τ+2)(n+m)) 次整数算术与比较，表值和负载的位长为 O(log(km+1))，还须支付相应位运算费用。孤立点直接输出负载0，空边图也保留读取及输出费用。若允许任意平行边，应以 nice decomposition 每次只 introduce 一条边，局部只枚举两方向，坐标上界改为 km；可得 O(poly(τ)(km+1)^(2τ+2)(n+m)) 的安全算术界，不能继续把多重图的度界成 n−1。分解未给定时另付构造费用。

这些明确界足以保留固定树宽下的伪多项式精确算法；系列并行图树宽至多2，因此仍适用，也仍与下节弱 NP-困难性相容。二进制大权值并未变成输入位长多项式。更快的 join 若由卷积、特殊表结构或其他实现获得，仍须给出该加速及位长的证明；这是所印精确指数目前未付的义务。

# 4. 困难性归约和精确边界

## 4.1（多重）外平面图：弱 NP-困难

`Theorem 11` 从 `PARTITION` 归约：取两个节点 (s,s')，对每个整数 (s_i) 建一条平行边，边权为 (s_i)，令 (W=\frac12\sum_i s_i)。存在总和为 (W) 的子集，当且仅当可把边分向两端使两端出度都为 (W)。因此带平行边的 outerplanar（multi-outerplanar）版本弱 NP-困难。该构造不证明简单 outerplanar 图的困难性；论文结论明确把简单 outerplanar 的复杂度留为开放问题。

## 4.2 简单系列并行图：弱 NP-困难

`Theorem 12` 仍从 `PARTITION` 归约，但使用简单图：对每个 (s_i) 建 (s-v_i-v'_i-s') 三边路径，外侧两边权为 (s_i)，中间边权为 (W)。图无 (K_4) minor，故为 series-parallel。若分割存在，则按子集方向使 (s,s') 各得 (W)，每个中间节点至多 (W)；反向推导说明任何成本不超过 (W) 的 orientation 都给出精确分割。因此简单 series-parallel 版本弱 NP-困难。

## 4.3 平面二部图：强 NP-困难

`Theorem 13` 对任意整数 (k\ge2)，从 Planar 3SAT 构造 \(\{1,k\}\)-MMO。每个变量是一个交替的 (4|x_i|)-环，权为 (k,k,1,1)；每个子句是一个节点；每个出现和每个子句另接一个 (2k)-环 special gadget，环边权为 (k)，并用若干权 1 边连接。special gadget 在成本至多 (k) 时被迫沿环同向，变量环也只能顺/逆时针，分别编码真/假；子句节点必须把至少一条变量连边指入，恰对应一个满足文字。于是公式可满足当且仅当构造图有 orientation 成本至多 (k)，得到平面二部图上的强 NP-困难。

由二部图同时是 (P_4)-bipartite、house-free、diamond-free，`Corollary 15` 将强 NP-困难和“除非 (P=NP)，不存在比 (1+1/k) 更好的伪多项式近似”传播到这些超类。`Corollary 14` 给出平面二部图同样的近似下界。

# 5. 与本仓库模型的衔接、用途和缺口

* 可复用的模型桥是“两个可选端点 + 端点无关处理时间”这一受限调度子类；它可作为 unrelated-machines 文献索引和小图算法背景，尤其是仙人掌块树剥离、series-parallel 的 Partition 归约、以及树宽 DP 的状态设计。
* 论文并未处理任意机器相关处理时间、任意资格集合、分数配置、客户覆盖均分、六名提供者按完整历史选目录客户子集、SPE 或 `OPT_m/2` 目标。不得把 MMO 的方向等价、图类困难性或 cactus 算法写成 Q-CAG-HALF-6 的结论。
* 论文证明了 simple outerplanar 仍处于 “P 或弱 NP-hard” 的开放区间（因为 series-parallel 有伪多项式 DP），所以清洗时不能把“outerplanar NP-hard”无条件写成简单图版本；必须保留 multi/simple 区分。
* 参考文献中的其他近似算法、图识别复杂度和早期 CATS 版本只按论文内引用记录，未在本条目中独立核验；如需建立外部文献边，应另读对应冻结源。

本条目是 `资料` 资源，不构成当前六人模型的证明、反例或算法。第三阶段若建关系，建议将其作为“文献/背景”节点连到《不相关机器与两个调度松弛》定义，边语义限定为“受限二端点子类的来源与算法背景”。
