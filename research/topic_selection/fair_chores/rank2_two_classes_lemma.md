# 两平行类无圈秩成本的无嫉妒构造

状态：本轮新推导；下述完整论证已由 cross_field_battle 子研究者和 boss4 逐步攻击，修正了“增广物品必须全局未匹配”的细节。尚无外部审稿，也未认证文献新颖性。这里只是局部数学引理，不升级仓库 canonical claim。

## 模型和结论（FC-LEMMA-R2-2C-v1）

有 n 个 agent、m 个 indivisible chores。对每个 i，A_i⊔B_i=M，允许其中一类为空，但不允许 loops，即每件物品的 singleton cost 都是 1。定义

c_i(S)=1[S∩A_i≠∅]+1[S∩B_i≠∅].

这是两个容量 1 的平行类组成的 partition matroid 的秩函数。结论：

* 当 m≥n，存在 complete EF 分配，并且可在多项式时间构造。
* 当 m<n，存在 complete EFX 分配（每个 agent 至多一件）。

EF 使用 c_i(X_i)≤c_i(X_j)，EFX 使用对每个 g∈X_i 有 c_i(X_i\{g})≤c_i(X_j)，包括 removal 的边际为零的情况。此处完全不要求 PO。

n=1 时任意 complete allocation 都 EF，因此下文假定 n≥2。

## 把每件 chore 写成一个 bit word

给每个 item e 一个 word b(e)∈{0,1}^n，其中第 i 位标识它属于 A_i 还是 B_i。输入可有重复 word。

**情况一：全部 2^n 个 word type 都出现。**

互补 word pair 有 2^(n−1) 对；对 n≥2 有 2^(n−1)≥n。选 n 个互不重叠的 pair type，每个 type 各取一件 item，给每个 agent 一对。剩余物品任意分配。每个 bundle 对每个 agent 都同时触达两个类，成本均为 2，所以 EF。

枚举 2^n 不破坏多项式性：进入此情况时 2^n≤m，因而最多处理 m 个 distinct word。

**情况二：有一个未出现 word w。**

构造二部图 H_w：左侧是 agents，右侧是 items，i 与 e 相邻 iff b_i(e)≠w_i。因为 w 没出现，每件 item 至少有一个邻居。

如果 H_w 有覆盖所有 agents 的 matching，先按 matching 分配一件给每人，再把剩余物品交给任意邻居。每个 i 的 bundle 都只含 bit 1−w_i，因此自己的成本是 1；所有 bundle 非空，所以任何 agent 对任何别人的 bundle 的成本至少 1。这给出 EF。

剩下证明，总能把一个缺字 w 变成具有该 matching 的缺字。

## Hall 缺陷与单坐标翻转

取 H_w 的一个 maximum matching F，大小 k<n。从所有未匹配 agents 出发沿交替路遍历，设可达 agent 集为 S、可达 item 集为 T。maximum matching 保证 T 中没有未匹配 item，且 |T|<|S|。对每个 i∈S：

1. i 的所有 H_w 邻居都属于 T；
2. 沿一条交替路翻转，可以保持 matching 大小 k，同时让 i 变为未匹配。

令 w^(i) 是只翻转 w 第 i 位的 word。若对所有 i∈S，w^(i) 都出现，则从每个 type 取一件 e_i。这些 e_i 互不相同，且在 H_w 中 e_i 只邻接 i，所以 e_i∈T。于是 |T|≥|S|，矛盾。

故有 i∈S 使 w^(i) 也未出现。先用交替路让 i 未匹配，再把 w 改成 w^(i)。只有 agent i 的邻接关系改变，其他已匹配边仍在。必须选择一件**全局未匹配 item** e：因为 m≥n>k，这样的 item 存在；因为 F maximum，e∉T。由 i 的所有原邻居都在 T 得 b_i(e)=w_i，所以翻转后 i 与 e 相邻。加入 (i,e)，matching 大小至少变为 k+1。

重复至多 n 次，得到覆盖所有 agents 的 matching。每一步都保持 w 为缺字。

## 实现与复杂度

维护 distinct word 的 hash/trie。若完整 hypercube 出现，直接构造互补 pairs；否则沿 trie 找一个缺字，时间 O(nm)，不扫描指数个候选。

对每个缺字构造 O(nm) 条边，使用普通增广路 maximum matching，保守每次 O(n²m)。每轮至少增加 1 个匹配，总轮数至多 n，保守总复杂度 O(n³m)，空间 O(nm)。使用匹配 warm start 可进一步改善，但不是结论所需。

## 为何不能直接外推

有 loops 时，别人的非空 bundle 对 i 的成本可能为 0，“自己成本 1 即 EF”的末步失效。三平行类的 rank-2 matroid 是 r_i(S)=min{2,触达的非loop类数}；word 的“与缺字不同”不能保证 owner 的物品都落在单一类，因此 Hall 翻转的最后解释失效。这两个障碍就是 FC-01 的首个边界。


## 代码与冻结证据的仓库位置

本报告的脚本位于 `tests/audits/topic_selection/fair_chores/`，输出位于 `evidence/runs/topic_selection/fair_chores/`。复现时复制脚本到新的临时目录运行，勿覆盖冻结输出；完整索引见[本轮复现与核验](../VERIFICATION.md)。
