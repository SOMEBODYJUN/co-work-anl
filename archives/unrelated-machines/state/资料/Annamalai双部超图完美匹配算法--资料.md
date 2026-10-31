---
id: "unrelated-machines/annamalai-bipartite-hypergraph-perfect-matching-algorithm-2016"
kind: "resource"
type_tag: "资料"
title: "Annamalai 双部超图完美匹配算法（2016）"
status: "retained-primary-literature-read"
truth_status: "primary-paper-statements-read; external-results-cited-not-reproved"
summary: "完整读取冻结的 arXiv:1509.07007v2 论文。论文在固定超边阶数与固定正强化参数下，将严格强化的 Haxell 命中数条件构造成多项式时间完美匹配算法；同时给出失败时返回命中数违约集合的版本。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/literature/unrelated_machines/annamalai_2016_hypergraph_matchings_arxiv_v2.pdf"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/literature/unrelated_machines/annamalai_2016_hypergraph_matchings_arxiv_v2.pdf"
source_ids:
  - "f32be3fb55f5e9958899"
source_sha256: "f6294a3b497e98d870ab47ceecb4a94a7e80457e9777114f59d88f321bc7dcce"
source_size_bytes: 607189
bibliography:
  author: "Chidambaram Annamalai"
  title: "Finding Perfect Matchings in Bipartite Hypergraphs"
  arxiv: "1509.07007v2 [cs.DS]"
  paper_date: "2016-12-06"
  frozen_pdf_date: "2016-12-05"
read_scope: "冻结 PDF 全文逐节核读；未把引用文献的定理当作本次重证。"
related_objects:
  - "../定理/私有菜单树有界叶重数配置界--定理.md"
---

# Annamalai 双部超图完美匹配算法（2016）

## 来源身份与阅读范围

本页登记 `history/source/literature/unrelated_machines/annamalai_2016_hypergraph_matchings_arxiv_v2.pdf` 的主文献内容。冻结清单给出同一路径的两个版本：`legacy-cleanup` 提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `main` 提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`；本次读取的字节 SHA-256 为 `f6294a3b497e98d870ab47ceecb4a94a7e80457e9777114f59d88f321bc7dcce`，大小 607189 字节。PDF 标题页给出作者 Chidambaram Annamalai、`arXiv:1509.07007v2 [cs.DS]`，正文日期为 2016-12-06（冻结文件标注 2016-12-05）。

论文是一个外部算法/定理资源，不属于客户—提供者顺序 SPE 模型：它没有提供者、客户覆盖价值或均分历史。它研究的是给定二部超图上的完美匹配，并把结果用于 Restricted Max-Min Fair Allocation 等背景。这里保留论文的精确量词、严格不等式和算法边界，不能把它的 matching 直接改写成 unrelated-machines 原问题的真实调度，也不能把论文引用的 Haxell 证明算作本页已重证。

## 模型与基本定义

一个 r-uniform bipartite hypergraph 是 H=(A,B,E)，顶点分成两侧 A、B，每条超边 e∈E 恰含一个 A 侧顶点和 r−1 个 B 侧顶点。论文假设二分割已经作为输入给算法；记 n=|A|、m=|E|。部分匹配 M⊆E 的边两两不交；覆盖全部 A 的部分匹配称完美匹配。

对 S⊆A，论文记 E_S={e∈E : |e∩S|=1}。对边族 F⊆E，τ(F) 是 B 侧最小命中集的大小，即最小的 X⊆B 使每条 e∈F 都与 X 相交。A(F)、B(F) 分别是边族在两侧的顶点并集。

相对于当前部分匹配 M，边 e 的 blocking edges 是 {f∈M : f∩e∩B≠∅}。没有 blocking edge 的边称 immediately addable。若 a∈A 已由 e∈M 匹配，而存在对 a 的 immediately addable 边 f，则可把 e 换成 f，保持已匹配的 A 侧顶点集合不变。

## 论文引用的 Haxell 条件（外部结果）

论文在 Theorem 1.1 引用 Haxell 的存在性定理：若对每个 S⊆A 都有

> τ(E_S) > (2r−3)(|S|−1)，

则 H 有完美匹配。论文说明把严格不等式改为非严格不等式后该结论不再普遍成立，并强调原始证明是非构造性的。该定理是本文的外部背景；本次没有取得 Haxell 1995 原文并重证其证明。

论文还回顾 Annamalai–Kalaitzis–Svensson（AKS15）的强化条件（Theorem 1.2）：给定固定常数 c>0、0<ε≤1、r≥2，若

> τ(E_S) ≥ (c/ε) · r · (|S|−1)

对所有 S⊆A 成立，则存在多项式时间算法，为每个 a∈A 选一条边 e_a，并从 e_a∩B 选出两两不交的 S_a，使 |S_a|≥(1−ε)(r−1)。这不是原超图的完美匹配保证；只有在额外的 ε<1/r 等条件下，大小保证才可能被解释为完整边选择。

## 主结论：固定 r 与固定强化量的可构造化

论文 Theorem 1.3 的精确量词是：对每个固定的 ε>0 和 r≥2，存在算法 A(ε,r)，在满足

> τ(E_S) > (2r−3+ε)(|S|−1) 对所有 S⊆A

的 r-uniform 二部超图上，以输入大小的多项式时间找到完美匹配。算法运行时间对 r 与 1/ε 的依赖可能是指数的；论文没有给出联合参数 r、ε 的统一多项式保证。

论文在 Theorem 5.4 给出一个稍强的判定式版本：同一固定参数下，算法 A′(ε,r) 对任意输入要么返回完美匹配，要么返回 S⊆A 使

> τ(E_S) ≤ (2r−3+ε)(|S|−1)。

因此它把“强化 Haxell 条件成立时必有完美匹配”变成了带显式违约证据的算法合同，而不是无条件解决一般超图匹配。

## 增广算法的实际结构

算法从一个不匹配的根 a₀∈A 开始，维护相对于当前部分匹配 M 的 alternating tree T=(L₀,…,L_ℓ)。其中 L₀=(∅,{a₀})；其余层 Lᵢ=(Xᵢ,Yᵢ) 中，Xᵢ⊆E∖M 是候选边，Yᵢ⊆M 恰为它们的 blocking edges，并要求每条 Yᵢ 中的阻塞边恰与一个 Xᵢ 边相交。不同层的 B 侧顶点集合不相交，且 A(Yᵢ₋₁)⊇A(Xᵢ)。

论文设置 μ=ε²/(10r²)，U=⌈1/μ⌉。`BuildLayer` 反复为最后一层 Y_ℓ 中尚未达到 U 次树内出现的 A 顶点加入一个与当前树 B 顶点集合不相交的可用边，并把该边相对于 M 的 blocking edges 一并放入 X、Y。主循环的 collapse phase 在最后一层有超过 μ|X_ℓ| 条 immediately addable 边时触发：逐个用这些边替换上一层的阻塞匹配边，丢弃当前层，并在上一层执行一次 superposed-build；只有当该上一层的 X 大小至少增加 1+μ 倍时才接受新层。

这些操作保持部分匹配和 alternating tree 的定义。若 collapse 发生在第一层，根被匹配，当前增广结束；否则继续 build/collapse。

## 终止性不变量与层数界

论文 Proposition 4.1 证明每次主循环开始时，树中没有可 collapse 的层，因此 |Yᵢ|≥(1−μ)|Xᵢ|。Proposition 4.2 证明忽略更深层的 superposed-build 满足 |Xᵢ′|<(1+μ)|Xᵢ|。

关键增长结论 Theorem 4.3 是：在新层 Lᵢ₊₁ 建成后，对每个 i=0,…,ℓ 有 |Xᵢ₊₁|>ε|Y_≤ᵢ|/(5r²)。当树中阻塞边数量较小时，若新层为空会直接违反强化的 Haxell 条件；当数量达到 ⌈5r²/ε⌉ 时，命中数上界与强化下界的比较给出同样的增长。结合 |Yᵢ|≥(1−μ)|Xᵢ|，论文 Lemma 4.7 得到 alternating tree 的层数为 O(log n)。

该增长只用于算法终止性和运行时间，不给出对任意 r、ε 的统一多项式指数。论文没有把树层数的对数界误写成常数高度，也没有把每层候选数当成输入中已显式展开的全部超边。

## Signature vector 与多项式迭代次数

为控制 build/collapse 的总次数，论文给每层定义带归一化的整数 signature。令 b=(1−μ)^(−1/3)。层 Lᵢ 的两个坐标由

- −floor(log_b(((5r²/ε)^i/(1−μ)^(i−1))·|Xᵢ|))；
- floor(log_b(((5r²/ε)^i/(1−μ)^i)·|Yᵢ|))

给出。按层串接这些坐标并在末尾附加 ∞，得到 signature vector。Lemma 5.1 证明每次未终止迭代使该向量字典序下降：若无 collapse，新层使向量延长；若有 collapse，最早被丢弃层的匹配边数下降，或上一层的 X 坐标严格改善。

Proposition 5.2 说明各坐标绝对值单调不减；结合层数 O(log n)，Lemma 5.3 给出可能的 signature vector 数量为多项式。论文还记录一个不依赖分拆函数渐近的改进：可在第 i 个坐标加减 i，使绝对值严格递增，从而用有限子集编码。

从空匹配开始，对每个未匹配 A 顶点运行该增广过程。固定 r、ε 时，每次迭代和每次边/层更新可在输入大小的多项式时间实现；运行至多 n 次后得到完美匹配，或由 Theorem 5.4 的失败分支返回命中数违约集合。

## 与本仓库 unrelated-machines 对象的关系

现有对象《私有菜单树有界叶重数配置界》把 Haxell 的 Theorem 1.1 作为外部 Paper Fact 使用，并将其总边大小记为 R+1：每条辅助超边含一个 root 和 R 个外部资源，因此论文阈值 2(R+1)−3=2R−1。这是参数映射，不是把 Annamalai 的算法直接套入配置构造。

该现有对象要求从私有树中存在选择并保留配置/资源容量不相交；其辅助超边族可能指数多，辅助树分叉数、有效 rank 和强化余量可能随输入变化。Annamalai Theorem 1.3 的算法承诺只对固定 r 和固定正 ε 给位长多项式时间，因此不能在没有额外压缩、显式边族和统一 slack 证明的情况下声称为该对象提供一般确定性调度算法。现有对象正文已经把这一点列为缺口，本页补充的是可核对的原始论文陈述与算法机制。

论文中的 Haxell、Hall、AKS15、Santa Claus 等背景不改变 unrelated-machines 当前对象的模型身份。该文没有证明客户吸引模型的半覆盖，也没有提供六人完整历史 SPE 的支付或反例。

## 处置、用途与接续

本源处置为 retained 到本页：它是已实读的外部文献资源，独有内容是固定 rank/slack 的增广算法、失败时的命中数证书以及对运行时间依赖的明确量词。它不应被退休，因为现有私有树/资源匹配对象仍需要这份 primary citation；也不应把它合并成现有定理正文的无条件算法结论。

后续若要把该算法用于本仓库的辅助匹配，必须逐项补齐：

1. 证明辅助超图的总边大小 r 与强化量 ε 是固定常数，或提供输入参数下仍为目标复杂度的显式分析；
2. 给出有限且可枚举的候选超边族，不能把指数多隐式辅助树当作已输入边集；
3. 把算法返回的边匹配还原成原任务的合法配置/调度，并核对全部未选状态和资源端点；
4. 若使用 Theorem 5.4 的失败分支，解释返回的 S 如何转成当前配置合同的真实否定，而非只作为超图层级的障碍；
5. 保留 Haxell 原始定理与 Annamalai 构造的证据层级，不能把外部引用写成仓库内部完整证明。

该文第 6 节保留的公开问题是：能否让运行时间对 1/ε 或 r 至少一个参数具有多项式依赖。该问题仍是文献层开放，不在本仓库对象中宣称已解决。
