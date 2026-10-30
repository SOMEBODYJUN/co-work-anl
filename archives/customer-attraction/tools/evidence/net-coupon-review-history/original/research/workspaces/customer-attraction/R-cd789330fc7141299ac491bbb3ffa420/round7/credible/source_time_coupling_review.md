# R-only 来源时间耦合：独立盲重构

2026-10-24，credible7。本文在只收到 root 的命题陈述、尚未读取作者正文时重构。适用任意人数、任意有限共同目录和每个完整历史依赖纯 SPE。**解析核对通过；不是一般 HALF、实际钱包 cap1/cap2 或福利新界。**

## 1. 所审查的精确合同

固定原实际叶 Z、实际覆盖 C。source 仅为 R⊆N\C 的客户，owner i 的源查询是 actual-prefix 下的合法主题 T_i；source 当前吸收进 actual i 行，future 份额进查询叶上的真实 natural contexts。随后使用 round5 全客户正广播，并以 round6 SAFE 从同 context 当前实际整行退款；也可使用只删原正边的 CLIP。不得把含 actual C 客户的全 O source INIT 塞入本命题。

给定一份共同 source/核选择，按 source owner i 给线性质量流附标签，令 π_ij 为 owner i 最终落入 actual 角色 j 的净券金额；M_i 为 owner i 的源质量，A_j=Σ_iπ_ij。

被审查命题是：π_ij=0 当 j<i；并且每个目标集 K 有更强 suffix-HIT 约束和单调角色价格推论。

## 2. 单来源的因果支持

owner i 的 R source 不在任何实际前缀角色的主题中，所以 INIT 没有 past actual coupon。它只会直接落 actual i，或进入角色 j>i 的真实规定 context。

源查询叶的有序历史在 i 前与 actual 相同。任一由它生成的 context，设上一次 reset 角色为 k，当前角色为 l>k，则 k≥i，且该 context 的 off-prefix 在 k 前与 actual 完全相同。因此其 past 正 coupon 只能落在 [k,l)；不可能早于 i。future 边的下一个 reset 角色为 l，仍≥i。

由严格角色递增的有限非终端 DAG 归纳，全部 terminal current/past 金额都在角色 i,…,m。SAFE 退款只动当前 l 的实际行，CLIP 只删正边，均保持此支持。不同来源合并计算 h 后仍可线性分解回来源标签：同一固定核不依来源标签改变，每个 source 的净券分解非负，故没有用互斥选择混合来制造该耦合。

结论是

\[
\pi_{ij}\ge0,\qquad \sum_j\pi_{ij}=M_i,
\qquad \pi_{ij}=0\quad(j<i). \tag{TIME}
\]

这里不声称沿途 current 角色单调等于 terminal 角色：past 出口可晚于 source 而早于当前 context。

## 3. 每个来源的 suffix-HIT

固定 owner i，令 K_i=K∩{i,…,m}。TIME 允许先删去 K 中所有 i 前角色。若 i∈K，使用命中量≤M_i。若 i∉K，记

\[
k_i=|K\cap\{i+1,\ldots,m\}|.
\]

在 source owner INIT 和它全部可到达的 contexts 上，对固定目标 K_i 使用原 PRICE 型行约束。当前角色不在 K_i 时，目标 recipient 至多 k_i 个；原全图 HIT 的逆角色归纳逐字适用，past 出口仍是 terminal、不是过去角色 IC。得到

\[
\sum_{j\in K}\pi_{ij}
\le
\begin{cases}
M_i,&i\in K,\\
\dfrac{k_i}{k_i+1}M_i,&i\notin K.
\end{cases} \tag{SOURCE-HIT}
\]

共同求和即

\[
A(K)\le M(K)+
\sum_{i\notin K}\frac{k_i}{k_i+1}M_i. \tag{SUFFIX-HIT}
\]

k_i=0 的项为零。此式同时使用同一来源、同一全客户核、同一 SAFE/CLIP 终端支付；没有给不同 K 重新选择来源或传播核。

## 4. 单调角色价格

TIME 直接给每个 prefix 的割约束

\[
A(\{1,\ldots,k\})\le M(\{1,\ldots,k\}). \tag{PREFIX}
\]

因此对任意非负非增角色价格 z_1≥…≥z_m≥0，分层或离散分部求和给

\[
\sum_jz_jA_j\le\sum_i z_iM_i. \tag{MONOTONE-PRICE}
\]

对非减价格方向相反，仅由 TIME 可得 ≥；不能把 MONOTONE-PRICE 用到任意价格后保留同一右侧。SUFFIX-HIT 对任意非负价格仍有按上水平集积分的上包络，但其一般右侧不是 Σ_i z_i M_i。

## 5. 范围核对

证明不需要 off-history slack ell≥0；它依赖真实 completion 域、actual-prefix reset、非负 SAFE 及原 PRICE。它没有控制 M_i 相对实际 u_i，故不能替换右侧 M 为 actual 钱包。它也不适用于全 O source INIT：一个 owner i 的 C 客户在源查询时就可能给 j<i 的 actual coverer 正券，直接破坏 TIME。

上述 §1–5 先冻结于未读作者正文的盲重构。未运行有限扫描或固定人数计算。

## 6. 随后对照作者正文

随后读取 [coupling 作者稿](../coupling/fresh_source_order_and_suffix_hits.md)。SOURCE-ORDER、ORDERED-HIT、PREFIX-CUT 和 DECREASING-PRICE 均与盲重构一致。

作者允许同一 source role 有任意多个查询 source alpha，并允许任意有限非负 source 质量，不要求 rho≤1 或 source 最优。本页盲重构先用通常的 owner i、T_i 记号，但证明逐 source 标签独立，未使用一角色一查询、rho≤1 或最优性；故作者这个较广范围也通过。

作者另给显式 SUFFIX-PRICE。独立重构如下：固定源 k，以 lambda_k 为基线，只有 j>k 且 lambda_j>lambda_k 的角色可能有正差。把这些高价按 lambda_(1)≥…≥lambda_(l)>lambda_k 排序，置 lambda_(l+1)=lambda_k。每个前 s 高价角色集不含 k，SUFFIX-HIT 给其总质量比例≤s/(s+1)。分层求和得到

\[
\frac1{M_\alpha}\sum_j\lambda_jA_{\alpha,j}
\le\lambda_k+
\sum_{s=1}^{l}(\lambda_{(s)}-\lambda_{(s+1)})\frac{s}{s+1}
=\frac{\lambda_k}{l+1}+
\sum_{s=1}^{l}\frac{\lambda_{(s)}}{s(s+1)}.
\]

空高价集 l=0 给 lambda_k。等价地，可先把低于基线的终价抬到 lambda_k，再对上水平集使用 SUFFIX-HIT；这是上界，没有假定原终端全在高价集。作者显示式及非增价格特化均通过。

作者明确排除依已抽轨迹事后适应选源/取消；固定核的线性 source 标签证明不能自动转为这类条件核。正文未把此限制隐去。未发现致命异议；本页审查通过的是结构耦合推论，仍没有 actual 钱包容量结论。
