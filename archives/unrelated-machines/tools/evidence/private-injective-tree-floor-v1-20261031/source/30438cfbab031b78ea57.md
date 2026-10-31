# 私有注入树共同分数证书：陈述先行独立审查

审查者：boss11 内部 cover_consistency。实际只读 Exact `private_injective_tree_fractional_floor/private_injective_tree_fractional_floor_exact_statement.md`，SHA256 `aa3ed3a09e04d291b1266468af5814ffd8bd649cac4746514f60a79e791ecf54`。本记录形成前未读同目录作者 proof、未询作者思路、未读本候选其他代理推导。背景上已熟悉私有 unit-readout 树、完整原 P 的负载转移和此前色保反馈，但本次没有假设任何 port 结构或引用前一反馈置换作为证明。

结论：未发现 standing fatal objection。通过树叶 hitting number、共同 λ 的加权计数及准确参数化的 Haxell 定理，可以证明所给所有 r 条件及五三存在性。此为有限对象存在性，不升级为一般参数 deterministic bit-poly 算法。

## 1. 单状态的精确叶 hitting number

写 R=r^h，a=(d−r+1)^h。考虑一个满 d 叉高度 h 树中全部满 r 叉、仍高度 h 的根子树的叶集。阻断所有这类子树所需删除的最少原叶数恰为 a。

独立归纳证明：高度0时唯一叶须删1。高度t时，若至少r个child分支仍各保有满r叉高度t−1子树，它们可拼成一个高度t子树；故阻断必须让至少d−r+1个child分支分别被阻断。分支叶集互不相交，每个至少需(d−r+1)^(t−1)枚删除，得下界(d−r+1)^t。反之恰挑d−r+1个child递归删除最小阻断集即可达到。于是公式精确。

单个 f_us 的注入性在此承重：对资源集合 X⊆Z，其落在该状态完整 bundle B_us=f_us([d]^h) 中的资源数，恰是被删除的不同原叶数。没有注入时一个外机可同时命中多枚叶，下述 a 下界不能照用。

## 2. 将共同 λ 转成全 root-subset 的 transversal 下界

建立一个有限 bipartite hypergraph：左侧是 roots U，右侧是实际外机 Z。对每个root u、每个state s及其中每棵满r叉高度h子树，建边{u}∪其实际外机叶集。单态注入保证每边恰有R个不同右侧资源，总edge size为R+1。相同root下重复的同资源边可去重，但保留一个真实state/subtree作见证即可。

给任意非空I⊆U，记τ_I为仅使用右侧资源打中所有incident-to-I hyperedges所需的最少资源数。注意不能用左侧root本身作hitting vertex，那将不是Haxell所需的τ。

任意这样的hitting资源集X，对每个u∈I的每个state s均打中该state所有r子树，所以由第1节，|X∩B_us|≥a。乘共同非负λ_us并求和：

 a|I| ≤ Σ_(u∈I,s) λ_us |X∩B_us|
       = Σ_(z∈X) Σ_(u∈I,s) λ_us 1[z∈B_us]
       ≤ |X|。

最后一步严格使用Exact给的**同一组**λ及每z的全roots容量≤1；不允许给不同X或z另选分布。故τ_I≥a|I|。零权state没有问题：hitting集仍命中它们，加权中其贡献为零；每u的正权总和仍是1。跨state、跨root共享资源完全允许，正是容量不等式所处理的部分。

## 3. 外部定理的实际核验和参数对齐

本次为核准确常数，实际联网读取了原始研究论文：Chidambaram Annamalai, *Finding Perfect Matchings in Bipartite Hypergraphs*, arXiv:1509.07007v2，2016-12-05，https://arxiv.org/pdf/1509.07007 ，PDF第2页、印刷页1、Theorem1.1，及相邻定义。该页明确复述Haxell[1995]：总edge size为k的uniform bipartite hypergraph，每边恰一个左点、k−1个右点；右侧最小hitting number满足τ(E_I)>(2k−3)(|I|−1)即可有饱和左侧的匹配。已实际获取该页渲染并核对公式。该研究论文引用的原作是P.E.Haxell, *A condition for matchability in hypergraphs*, Graphs and Combinatorics11(3),245–248,1995，DOI10.1007/BF01793010；本次未声称实际阅读全文原作1995证明。

此处必须取该定理的k=R+1，不是k=R。于是系数是2R−1。Exact的a≥2R−1给

 τ_I ≥ a|I| ≥ (2R−1)|I| > (2R−1)(|I|−1)。

R≥1，因此严格不等式确实成立，包括|I|=1与边界a=2R−1。I为空的条件自动成立。有限hypergraph且全部边恰同一大小R+1≥2，满足外部定理全部对象条件。匹配得到每root一条边，取其真实state/r子树见证，右侧外机全局互异。

该定理是存在性工具。不能因为资源超边可有限列举就称按原P总位长多项式；一般d,h下子树数可以很大。这里也没有调用其后加强条件下的算法定理或把它的固定rank复杂度当成变rank算法。

## 4. 五三参数条件的逐项算术

取r=floor((d+2)/3)=ceil(d/3)。d≥1给1≤r≤d，且3r≤d+2，故d−r+1≥2r−1。

对全部r,h≥1，(2r−1)^h≥2r^h−1：写r=1+x，x≥0，展开(1+2x)^h，其所有正次项系数至少是2倍(1+x)^h相应系数。因此

 (d−r+1)^h ≥ (2r−1)^h ≥ 2r^h−1。

这个条件不是只对h=1成立。又r≥d/3，所以2−r/d≤5/3。d=1时r=1、A=R=1，外部定理退化为普通Hall；完整调度C=1。d=2时r=1、C≤3/2；所有小d都合法。条件只给充分性，不宣称必要或锐界。

## 5. 全部原 P 的逐机实际负载

采用hypergraph匹配得到的每root一个state和满r子树。在其r子树内，所有选中internal edge jobs下送子机，选中leaf jobs送原外机，selector放该state根。

- 每个r子树内机器恰收到一个unit incoming（根处为selector），有r个出任务下送，另d−r个原出任务留父1/d，总负载1+(d−r)/d=2−r/d。
- 同一个选state中，未进入r子树的机器没有unit incoming：其父边被留在上方父机。该机的全部d个出任务留父，总负载1。其所有更深未选分枝也同样处理，不能删去。
- 每个未选state的全部原树任务都留parent。每机恰d个1/d，负载1，且没有unit selector。
- 选中叶资源全局互异，各外机至多一个unit job，负载≤1；未使用资源可负载0。

所有原selector、internal edges、leaf jobs各恰分配一次，只用原finite ends。因为r≤d，2−r/d≥1，以上给完整原P的Cmax≤2−r/d。没有把仅叶资源匹配当完整调度，也没有假设不同state的内部机器共享。私有性及unit/1/d处理时间是本步承重前提。

## 6. 退化、应用和未认证范围

U非空、菜单有限非空、d,h≥1保证每state有d^h≥1原叶，因此注入假设本身排除Z为空。若Z大小不足，假设不可能同时成立，不是该定理漏处理的输入。λ的有理性对有限存在性无负担，证明实际上对共同非负实λ同样成立；没有基于分母数值的运行时间声称。

将外机容量对全部z求和，还给必要条件|Z|≥|U|d^h。若恰相等，则所有容量在给定共同λ下必须恰1。这不是一个新的自动证书：某Latin/register实例是否每个单state都注入、是否存在同一共同λ，必须另证，不能从balanced source或逐resource分别可行直接推得。

本存在性不需要E保色、随机port、Latin、source label、route length等任何附加结构；若一个具体compiler输出真的符合全部私有树/注入/共同分数假设，已足以排除其实际OPT>5/3。反之若单态注入失败、共同λ不成立、存在额外资格或内部共享等，本结论没有覆盖。自然λ的另页待审结论不是本报告已认证的事实。

本结果通过已核外部定理及上述树hitting/分数桥梁得到；没有认证原创性、算法或UM-TARGET-v1。本文只给独立数学审查，不冒称代码/有限实例已经审过。
