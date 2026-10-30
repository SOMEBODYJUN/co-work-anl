---
id: unrelated-machines/k-uniform-bundle-and-single-layer-quota-review
kind: review
title: k均匀束与单层配额超图双源审查
status: complete-source-read-integrated
scope: "exact layered matching-floor identities and the cross-layer consistency obligation for shared-resource demand trees"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/k_uniform_bundle_matching_floor.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/k_uniform_bundle_matching_floor.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/single_layer_quota_hypergraph_obstruction.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/single_layer_quota_hypergraph_obstruction.md
source_ids:
  - 88372ae03e17e85bcd21
  - 45d6cfc725027933917a
inventory_sha256:
  88372ae03e17e85bcd21: f369ffab36ccb70419a61318d8b10bdbacb4b92a81406c3abce58eeeaec63381
  45d6cfc725027933917a: 9d9caa01d0b949145a4a55f402ee8c353bc0e44e052f525662b6175ed0434b5e
---

# 阅读范围与对象

本批完整读取 `k_uniform_bundle_matching_floor.md` 和 `single_layer_quota_hypergraph_obstruction.md`，并与三维匹配需求树、根树—调度桥梁、标签碰撞和全层配额审查比较。两份正文都研究共享资源需求树，但对象层次不同：第一份允许每条超边携带至多 (k) 个资源并给出所有 (t)-子集层的精确公式及固定层复杂度地板；第二份固定每个选择点一个 (K)-需求中间节点，给出同一公式的最简接口、逐层 soundness 义务和有限精确审计。

两源的稳定结论都是自足的组合恒等式和方法边界。经既有需求树桥梁，它们能翻译成 (OPT=2-b^*) 的受限调度值；它们没有给一般 (R\|C_{\max}) 困难性，也没有关闭 `UM-TARGET-v1`。正文中的有限枚举只核验公式实现，不能替代全称证明。

# 一、k-均匀资源束的分层匹配地板

## 1. 定义域和精确恒等式

令 (X) 有 (q) 个选择点，资源集为 (R)。超边 (e=(x,S)) 满足 (1\le|S|\le k)。需求 DAG 的根需求为 (q)，每个 (x) 需求为 1，每个超边节点需求为 (K\ge1)，资源需求为 0，边为 (r\to x\to e\to u)（(u\in S)）。对 (1\le t\le\min(k,K))，令 (\nu_t(E)) 为最多有多少个不同 (x) 能各自选一条超边和一个大小 (t) 的资源子集，且这些子集两两不交。

精确命题是
\[
 b^*(D_{K,k}(E))=
 \max_{1\le t\le\min(k,K)}
 \min\left\{\frac{\nu_t(E)}q,\frac tK\right\}.
\tag{1}
\]
当 (q=0) 时按空根分支定义两边为 0。通过既有调度桥梁，对应实际实例的值为 (OPT=2-b^*)。这一定义把“每个选中束只取 (t) 件”作为一个真实层，而不是把完整 (K)-束和单资源边混成同一对象。

## 2. 完整证明机制

下界取达到 (\nu_t) 的束匹配，把根接到这些 (x)，再接到对应超边，并让每个超边只展开其 (t) 个互不相交资源；根、选择点和超边的比例分别为 (\nu_t/q,1,t/K)，所以得到右侧对应项。

上界任取评分为 (\beta>0) 的根树。若根选中 (s) 个点，则 (s/q\ge\beta)。每个被选点的超边节点必须有至少 (K\beta) 个资源子节点，令 (t=\lceil K\beta\rceil)，任取其中 (t) 个。树的单父条件保证这些资源子集两两不交，因此 (s\le\nu_t)，同时 (\beta\le t/K)，从而 (\beta\) 不超过式 (1) 的右侧。这个证明对所有 (k,K,q) 有效，不依赖有限枚举。

## 3. 归约含义：所有层都要控制

\(t=1\) 层是普通二分图匹配。即使完整 \(K\)-层匹配很小，只要 \(\nu_1=q\)，就有 \(b^*\ge1/K\)，这给出单资源逃逸的普遍地板。\(k=K=2\) 时，公式退化为三维匹配接口的 \(\mu,\nu\) 表达式。

若希望 YES 达到 \(b^*=1\)，必须有 \(t=K\) 且 \(\nu_K=q\)，所以 \(K\le k\)；若 NO 要求 \(b^*\le\varepsilon/2\)，必须同时压低每个 \(t=1,\ldots,K\) 层的 \(\nu_t/q\)，而不只是完整 \(K\)-束。增大需求、复制资源或只加强完整超边张量，都不能自动消除中间层逃逸。固定 \(\varepsilon\) 时若让 \(k\) 随 \(1/\varepsilon\) 增长，资源束宽度和一致性编码的位复杂度也必须计入。

正文还给出固定层的复杂度筛选。令 \(t_0=\lfloor K\delta\rfloor+1\)。YES 的完整 \(K\)-匹配可截成 \(t_0\)-匹配，故 \(\nu_{t_0}=q\)；NO 若 \(b^*\le\delta\)，则 \(\nu_{t_0}\le\delta q\)。把候选 \(t_0\)-束看作大小 \(t_0+1\) 的超边，任意极大匹配 \(M\) 满足
\[
|M|\ge\frac{\nu_{t_0}}{t_0+1}. \tag{2}
\]
当 \(\delta<1/(t_0+1)\) 时，极大匹配和阈值可在固定 \(K,\delta\) 下区分 YES/NO；因此直接 bundle 接口若想承载假设的 gap，至少要避开这一固定层多项式地板，近似为 \(K\delta^2\gtrsim1\)。这只是该接口的复杂度筛选，不是一般调度 hardness。

## 4. 证据和边界

k_uniform_bundle_matching_floor.py 用精确 Fraction 检查 \(q=1\)、两资源全集合系统、\(K=1,\ldots,4\)，以及 \(q=2\)、四资源、1200 个固定种子随机集合系统和 \(K\in\{1,2,3,4,7\}\)，另核对 \(\nu_1=q\) 时的 \(1/K\) 地板。有限运行只支持公式实现；恒等式的全称性来自树结构证明。外部评审、新颖性和一般复杂度结论均未认证。

# 二、单层配额超图的最小接口

## 5. 精确值与证明

令 \(X\) 为选择点，\(Z\) 为零需求资源，每个 \(x\) 有非空邻域 \(A_x\subseteq Z\)。DAG 为 \(r\to x\to e_x\to z\)，根需求 \(q\)，选择点需求 1，中间点需求 \(K\)，资源需求 0。对 \(t=1,\ldots,K\)，令 \(\nu_t(A)\) 为最多有多少选择点可各取一个 \(t\)-元资源子集，且所有子集两两不交；另设 \(\nu_0=|X|\)。正文证明
\[
b^*(Q(A;q,K))
=\max_{0\le t\le K}
 \min\left\{1,\frac{\nu_t(A)}q,\frac tK\right\}. \tag{3}
\]
\(t=0\) 项用于空邻域和 \(b^*=0\) 边界。经桥梁，实际调度值为 \(OPT=2-b^*\)。

上界从评分 \(b>0\) 的任意根树取 \(t=\lceil Kb\rceil\) 和 \(s=\lceil qb\rceil\)：根比例给 \(s/q\ge b\)，每个中间点至少给 \(t\) 个资源，单父性保证子集不交，因而 \(\nu_t\ge s\)。下界取达到 \(\nu_t\) 的子集族直接构造根树，三类正需求点比例为 \(\nu_t/q,1,t/K\)。两步闭合式 (3)，不依赖调度求解器。

## 6. 对近二归约的必要义务

若某接口要求 YES 具有 \(b^*=1\)，则必须有 \(t=K\) 且 \(\nu_K=q\)：需要 \(q\) 个完整 \(K\)-元领取。NO 要求 \(b^*\le\delta\) 时，所有 \(t=1,\ldots,K\) 都必须满足
\[
\min\left\{\frac{\nu_t}{q},\frac tK\right\}\le\delta. \tag{4}
\]
只证明 \(\nu_K/q\le\delta\) 不足；所有中间 \(t>\delta K\) 层也必须压低 \(\nu_t/q\)。三维匹配需求树是特例，其一终端逃逸正是低层 \(t=1\) 或 \(t=2\) 没有被完整匹配 soundness 排除的情形。

若每个 \(A_x\) 的大小恰为 \(K\)，\(\nu_K\) 只是最大不交邻域子族，公式 (4) 仍要求所有部分领取层；给每个邻域增加私有资源会同时抬高多个 \(\nu_t\)，不能只改善 YES。正文没有声称一般二进制 \(K\) 下这些层的判定容易或困难，也没有把它们升级为复杂度下界。

## 7. 证据、用途与开放项

single_layer_quota_hypergraph.py 一方面枚举小宇宙中的全部根树，另一方面独立枚举不交 \(t\)-元子集族，覆盖宇宙大小 3、\(q\le3\)、\(K\le4\) 的全枚举和固定随机种子的 100 个边界实例，全部使用 Fraction。这是实现核验，不代替式 (3) 的一般证明。

两源共同的可回收用途是把“单层共享资源障碍”改写为一组明确的层级义务：若要建立近二 gap，必须给 YES 一个完整 \(K\)-层领取，并让 NO 的每个中间层同时缺乏大规模不交领取；若要接到真实 UM，还需提供任务身份、资源资格和从高评分树到源见证的可计算解码。它们没有给共享标签/高距离一致性构造，也没有证明一般近二 hardness。

# 处置与接续

两个来源均已完整读取、与三维匹配、标签碰撞、全层配额和需求树桥梁审查比较，并归入“分层配额/共享资源”对象。第一源的 \(k\)-束精确恒等式、固定层极大匹配地板和可扩展束宽边界均保留；第二源的最小单层恒等式、所有中间层 soundness 义务和有限审计范围均保留。UM-TARGET-v1 与六人 SPE 目标仍开放，不能把本批恒等式或有限实验写成一般算法或困难性结论。
