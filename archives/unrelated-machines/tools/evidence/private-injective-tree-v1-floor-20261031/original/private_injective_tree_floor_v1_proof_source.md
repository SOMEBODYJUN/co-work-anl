# 私有注入树共同分数证书的五三存在性：冻结证明

对应 Exact SHA256 `aa3ed3a09e04d291b1266468af5814ffd8bd649cac4746514f60a79e791ecf54`、候选 `UM-Q-PRIVATE-INJECTIVE-TREE-FRACTIONAL-FLOOR-v1`。

阅读来源：shared_label_attack 自行从 typed CONFIG1 的状态单射性质寻找任意E下 actual escape，先冻结 Exact、发 root；root 随后独立重构同一 hitting/Haxell 链（其阅读来源是已知Exact和旧CFG，不称零信息新Claim盲审）。本证明不发给 root 另外安排的 Exact-only 审查者。

## 1. 一棵满树的精确叶 hitting 阈值

令 ℱ_{d,h,r} 为满 d 叉高 h 树全部满 r 叉高 h rooted pruned subtree 的 leaf sets；每一集合大小 a=r^h。使每个集合都被击中的最小原叶集合大小恰

`b_h=(d−r+1)^h`。

h=1 时，必须删除 d−r+1 叶才能使剩余子树少于r个children。一般情形：将 d 个根孩子各自子树称为“好”当其尚含 r-pruned subtree。若有≥r个好孩子，则可选r个好子树，组合为完整r-pruned subtree；反过来，要破坏所有这样的子树，至少 d−r+1 个孩子必须坏。各孩子叶集合互异，按归纳每个坏孩子至少被击中 b_{h−1} 个叶，故总数至少(d−r+1)b_{h−1}。选这许多孩子、每个取一个最小hitting集合可达下界。

这段是纯树叶计数；尚未合并不同状态的资源。

## 2. 资源 hitting number 的共同分数下界

对每 root u，把所有状态 s 的全部真实 r-pruned subtree leaf images 组成资源 hyperedges 家族 ℋ_u。由于每 f_us 单射，每 edge 恰有 a=r^h 个**不同**外资源。

任取非空 root 子集 I⊆U，以及一个资源集合 Z0 击中 ∪_{u∈I}ℋ_u 的每一条 edge。对每 u∈I、每状态s，Z0在该完整状态树上的逆像是一个击中所有r-pruned叶集的原叶集合；单射给

`|Z0 ∩ f_us([d]^h)| = |f_us^{-1}(Z0)| ≥ b_h`。

按共同 λ 加权并交换有限求和，

`b_h |I| ≤ Σ_{u∈I,s} λ_us |Z0 ∩ f_us([d]^h)|`
`= Σ_{z∈Z0} Σ_{u∈I,s} λ_us 1[z∈f_us([d]^h)] ≤ |Z0|`。

最后一项只用原共同外资源边际≤1；没有为不同 Z0/资源重新选λ。因此资源 transversal number 满足

`τ(∪_{u∈I}ℋ_u) ≥ b_h |I|`。

单状态非注入时第一行不成立：同一资源可能一次击中许多原叶；这正是此结论不能套经典两树近二间隙的原因。

## 3. Haxell 适用条件与实际全root森林

使用 Haxell 的资源-transversal criterion：有限资源 hypergraph 家族，所有 edges 大小≤a；若对每非空 I 都有

`τ(∪_{u∈I}ℋ_u) > (2a−1)(|I|−1)`，

则可从每 ℋ_u 选一条 edge，彼此资源不交。

已实际核对可读 primary author paper 的明确陈述：Asadpour–Feige–Saberi，*Santa Claus Meets Hypergraph Matchings*，2008-06-17作者稿，PDF页5 Theorem2（总hyperedge大小记作r，该稿资源侧≤r−1，因此常数2r−3转换为资源侧rank a时恰2a−1）：
https://www.wisdom.weizmann.ac.il/~feige/mypapers/santaclaus1.pdf 。其Theorem3/PDF页6对普通k-element sets的constant relaxed matching给出相同transversal机制；本稿把“击中所有固定大小子集”换成第1节的“击中所有rooted子树”。

原始定理来源 P.E. Haxell，*A condition for matchability in hypergraphs*，Graphs and Combinatorics11 (1995),245–248，DOI10.1007/BF01793010。已打开原始publisher摘要/书目信息，原全文未取得；未虚称重构该外部定理的完整证明。这里依赖上述作者原论文明确写出的定理，适用的finite/rank/全部I/严格大于均已检查，不是只凭题名借用。

若 b_h≥2a−1，上一节给

`τ ≥ b_h|I| ≥ (2a−1)|I| > (2a−1)(|I|−1)`，

最后严格差为2a−1>0，连a=1也成立。于是得到所有root的资源不交edges。每条edge按其定义带有一个真实状态s与真实满r叉subtree见证（多个见证时任选）。单射保证叶到资源的合法注入。

## 4. 全部原机器/任务回填

每root selector放选中状态根。每active内部节点恰r个选中outgoing jobs下传，其余d−r枚留父；所有inactive分枝、所有未选状态的全部jobs都放其父端。root/active child有且仅有一unit incoming；active负载

`1+(d−r)/d=2−r/d`。

Inactive无unit incoming、恰全部d个small留父，负载1。全部选中leaf jobs外送到Haxell给出的互异真实外机，外负载≤1；未选leaf留父。每原任务恰一次，资格未改。因为r≤d，2−r/d≥1，完整 σ 达到claimed upper bound。

## 5. 五三与退化边界

令 r=⌊(d+2)/3⌋。d≥1时1≤r≤d、3r≤d+2，所以 d−r+1≥2r−1。函数 x↦x^h 在非负轴凸，或直接二项式归纳，给

`(2r−1)^h+1 ≥ 2r^h`。

因此(d−r+1)^h≥2r^h−1，满足criterion。另r≥d/3（按d模3三种情况立即核）而得C≤5/3。

d=1时r=1，a=b_h=1，Haxell退普通Hall，所得实际C1；h=1仍全部leaf直接从根外送，不漏任何child层。λ=0状态可忽略其概率项，但其原P任务仍全部父置。U非空给selector负载下界1；空U不在Exact实质域，可另返回空σ。Z若为空不可能满足非空U共同λ条件，不偷加不存在资源。

## 6. 构造性与准确身份

本Exact只声称存在性。ℋ_u 可以通过有限穷举全部r-pruned trees显式构造、用有限搜索取得匹配，因此给实际P上的有限可构造见证；不称此穷举为参数变化下的总位多项式。

Haxell原criterion本身仅给存在性/有限局部搜索，不在此稿导入未核现代算法。如后续要加固定d,h或有slack的多项式版本，应另核算法定理及展开规模，不能从当前证明静默升级。

机制的已有部分已扣除：经典Haxell transversal condition与普通uniform relaxed matching的证明不是本组原创。当前价值是识别“私有树单状态完整leaf map注入＋共同full-state分数点”这一精确、覆盖任意E的合同，直接封闭该Latin编译的近二NO可能性。全球新颖性、独立论文价值未认证；主目标仍OPEN。
