# chores、混合物品与约束公平分配：重新选题报告

检索截止：2026-10-20。作者：boss4/fair_chores 子研究者。已完整阅读本轮 USER_GUIDANCE.md 和仓库 AGENTS.md，按用户的重新选题指令执行，旧 UM 目标不约束本报告。所有新主张仅保存在本子目录；无 commit/push。

## 给 boss4 的判断

本线更值得进入 battle 的两个候选是 **FC-01（秩至多二的 matroid chores EFX）**、**FC-02（混合图单圈/仙人掌上的 EFX 定向分类）**。FC-01 有最新原论文明确公开问题作为入口，且本轮已在其两平行类、无 loops 的玩具模型得到一个有完整证明和构造算法的 EF 引理。FC-02 从已有树结果走向含环结构，范围较小，适合首先做结构刻画，但当前价值证据弱于 FC-01。

两者都不能承诺 20 天解决。FC-01 的致命风险是：加一个平行类或 loops 后可能立即包含困难彩色覆盖；FC-02 的致命风险是：单圈可能只是树算法的简单延伸，仙人掌又可能已被一般有界树宽方法覆盖。报告保留其他六个候选及淘汰原因，不把“没有搜到”当新颖性认证。

## 2025/2026 必须更新的研究地图

以下仅列 Paper Fact；原论文与我们猜想严格分开。

| 已核事实 | 原始入口及准确位置 | 本次 web ref |
|---|---|---|
| 一般 additive chores 不保证 EFX：四人十三件三值反例，推广任意 n≥4；公共二值 EFX 与 PO 也可冲突；四人公共二值 EFX 存在 | He–Tao, 2026, [arXiv v2](https://arxiv.org/html/2606.08872v2)，Thms 1–3、§3、§4、§5；§6 的余留问题是三人 additive、以及 n≥5 公共二值 | turn31view0, turn34view3, turn126view2 |
| 一般 additive 2-EFX 已存在，但该框架的初始化不保证多项式时间；常数 EFX 的多项式计算仍是公开问题 | Garg–Murhekar, AAAI 2026 / 2025 preprint, [arXiv](https://arxiv.org/html/2507.19461v1)，§1、Theorem 4、§5 | turn31view2, turn34view6 |
| 一般 additive EF1+PO 存在已解决，不能再选其存在性 | Mahara, SODA 2026，[作者主页](https://www.misojiro.t.u-tokyo.ac.jp/ryoga_e/)；由上述 Garg–Murhekar §1 和 He–Tao §1.2 交叉确认 | turn93search11, turn34view6 |
| binary cancelable chores EFX 已解；binary submodular 只有 2-EFX 的一般保证；binary XOS、binary supermodular 2026 已有无 EFX 反例 | Tao–Wu–Yu–Zhou, TCS 2025, [原论文](https://arxiv.org/abs/2308.12177)；Lin–Liu–Tao–Zhou 2026, [原文](https://arxiv.org/html/2608.10572v1)，§1、Thms 1–2、§4 | turn107academia33, turn107view0, turn111view2 |
| restricted additive c_ie∈{0,c_e} 已保证 EFX+MMS+2OPT；多项式版本是 EFX+4/3-MMS。price of EFX=2 已紧 | Lin–Wu–Zhou, WWW 2026, [原文](https://arxiv.org/html/2603.17270v1)，Thms 3.1、4.1、§3.3、Cor 4.5 | turn34view0, turn54view2, turn45view3 |
| lower/upper quota 的单类别 chores 有 (3n−1)/(2n)-MMS，多类别有 (2n−1)/n-MMS | Kinoshita–Igarashi, AAMAS 2026, [原文](https://arxiv.org/html/2602.08966v1)，§3、§4、§5、Appendix D | turn31view1, turn40view0, turn45view4 |
| 个性化双值 exact MMS 已有 2026-08 原始预印本声称多项式解决；本报告按“已发表预印本主张”排除旧题，不当作本队复核过证明 | Yuhao Zhang, [arXiv](https://arxiv.org/abs/2608.15822)，Abstract | turn93view0 |
| weighted binary WEFX+fPO 已有 2026-09 结果 | Lin–Wu–Zhou, [arXiv](https://arxiv.org/html/2609.13970v1)，Abstract、§1 | turn107view2 |
| Xinkai Zhang 的三人七件/八件 additive EFX 已有 2026-10-06 原始预印本；不能把 m=7/8 当新题 | [原文](https://arxiv.org/html/2609.10585v2)，Thms 1.1–1.2、§1.2，SMT 证据 | turn34view2, turn40view3 |

## 候选总表

| ID | 精确切口 | 文章类型/入口 | 当前判断 |
|---|---|---|---|
| FC-01 | 任意 n,m；每人 rank≤2 matroid rank 作为 chore cost；是否总有完整 EFX？先三平行类无 loops，再有 loops | 分类边界＋组合工具；binary submodular 公开问题 | **深挖 1，首推** |
| FC-02 | signed additive simple graphical valuations；单圈图是否总有 EFX^+_0 定向；进而仙人掌图决定其存在并构造 | 分类扩张；树与一般 NP-hard 之间 | **深挖 2，需查价值是否过薄** |
| FC-03 | m=3n、每人恰好三件；c_ie∈{0,1,2}；constrained MMS 是否总能 exact？失败则最小 n 及紧近似 | 有配额的 rounding/分类；2026 quota 工作自然延伸 | 储备，尚未认证新颖性 |
| FC-04 | n=5、公共 c_ie∈{1,r}、任意 r>1，完整 EFX 存在性 | 公开问题直接推进；He–Tao §6 | 前沿题，首轮不主攻 |
| FC-05 | 一般 additive chores 的常数 EFX 多项式算法；先有限 cost levels 的初始化 | 工具迁移；Garg–Murhekar §5 | 主题过大；仅接受明确受限初始化 |
| FC-06 | n=3、m=9 additive chores 的 EFX；手工/机器辅助结构证明 | 问题突破＋SMT 视角；接续 7/8 件 | 可试，但与整个三人 EFX 主问题距离太近 |
| FC-07 | restricted additive + 最优社会成本时最优 EFX 因子是否为 Δ=max c_e/min c_e | 组合近似/效率前沿 | **淘汰：五行 sharpΔ，属简单推论** |
| FC-08 | weighted binary chores WEFX+fPO 或个性化双值 MMS | 旧公开问题 | **淘汰：2026 已有完全相同结果** |

## 深挖一：FC-01，低秩 matroid costs 的 EFX 边界

### 精确问题与价值入口

每个 agent i 给出一个 rank≤2 matroid M_i，成本 c_i(S)=r_i(S)。允许不同 matroid、不同平行类划分和 loops。问：对所有有限 n,m 是否存在完整分配 X，使

c_i(X_i\{g})≤c_i(X_j) 对所有 i,j 和所有 g∈X_i 成立？

不是“只移除严格正边际的 chore”的较弱版本；也不额外要求 PO。rank≤2 matroid 由 loops 与若干平行类构成，其成本可写为 min{2,触达的非loop平行类数}。

**Paper Fact。** Tao–Wu–Yu–Zhou 2025 对 binary-marginal 成本区分类别；Lin–Liu–Tao–Zhou 2026 §4 明确把 binary submodular 作为余留 EFX 存在问题。后者反例使用的是 rank-two partition matroid 的 **nullity** |S|−r_i(S)，其 supermodularity 不能当作 r_i 的反例。原文：[2608.10572 §3.3、§4](https://arxiv.org/html/2608.10572v1)（turn107view0, turn111view2）。

**我们的新 idea。** 将整个 binary submodular 大问题首先压到 matroid rank≤2；先解决无 loops、三平行类，再尝试 loops。这个类的“启用一种任务类型支付一次成本，至多两单位”有明确设置/切换成本解释；不是加性二值换符号。

### 给文章定性之后如何学机制

母论文是“分类边界＋反例工具”主导，不是给某个算法加一个常数。其词编码把每个 chore 的各 agent 类型写成一个 word，再把 EFX 推成一个 matching 不可能性。应学习的是 **把 valuation class 变成组合对象并刻画可用交换**，而不是直接把 18-agent gadget 数字调小。

本轮尝试反向使用 word 视角：两平行类秩成本对应 binary word；利用缺字与 Hall 缺陷之间的交换。这个组合事实不是 nullity 的对偶翻译，因为 chore EFX 的删除发生在自己的 bundle。

### 已经可核查的玩具模型进展

本轮得到 FC-LEMMA-R2-2C-v1：若每人只有两平行类且无 loops，则 m≥n 时实际存在 **EF** complete allocation，m<n 时存在 EFX。完整证明和构造见 [rank2_two_classes_lemma.md](rank2_two_classes_lemma.md)。

关键二分：

1. 若全部 binary word types 出现，取 n 个互补 pair，让每个 bundle 对每人都成本 2；
2. 若有缺字 w，让 i 邻接第 i 位与 w 不同的 item。若 maximum matching 不能覆盖 agents，Hall 缺陷 S,T 保证某个单坐标翻字仍缺失；先沿交替路让该 agent 空出，再用一件**全局未匹配** item 增广。至多 n 次得到每人一个匹配 item，然后分配其余 items；owner 成本 1，所有人看别人的非空 bundle 至少 1，故 EF。

保守运行时间 O(n³m)、空间 O(nm)；找缺字使用 trie，不枚举指数 hypercube。原型实现 [construct_rank2.py](../../../tests/audits/topic_selection/fair_chores/construct_rank2.py) 有独立 EF/EFX 检查；seed=20261020，n=2,…,8，m∈{n−1,n,2n,4n,100}各100个随机输入，另加7个full-cube实例，共3507个构造实例通过。内部 cross-field reviewer 和 boss4 均攻击了论证；修正了任意 e∉T 不能保证未匹配的问题。**未做外部审稿、未认证新颖性。**

### 可解性依据、首义务、最危险障碍

可解性根据不是随机样例没失败，而是已找到一个会严格提高匹配大小的离散势能；它把证明从连续估值降为颜色/匹配。

先指出更强 EF 已不能沿用：两个 agent 都是 U_{2,3}，三件物品各为不同平行类时，任意2+1分配的双件者成本2而单件bundle成本1，故无EF，但仍有EFX。

首个 proof obligation：在无 loops、恰好三平行类且 rank cap=2 的情形，找出与“两类缺字/互补 pair”相对应的覆盖—共同彩虹 bundle 二分，或者给出最小反例。不能声称一般 matroid 基交换自动保存 EFX。

危险点一：三类时，“颜色不同于缺字”允许 owner bundle 同时含两种颜色，成本由 1 升为 2；原 Hall 证明的解释层失效。危险点二：loops 使别人的非空 bundle 成本可为 0；连“自己只成本 1”也不够。危险点三：原论文的 word gadget 是否可在有限秩上重新编码，尚未排除。第四个风险是 EF 小引理可能已有组合文献等价版本；目前查重仅确认没有直接相同标题命中。

### 可证伪实验与成文门槛

`rank_toys.py` 对每个抽样 cost profile 精确遍历所有 n^m 分配；结果见 `rank_toy_results.json`。当前核查了两类/三类 partition-rank costs，包含 loops；三类测试成本是“触达类数”，**不是 rank cap=2**，因此不替代下一义务。无反例只是有限证据。

补测已在 `rank2_cap_toys.py` 加入真正 rank cap=2：n=3,m=9，三平行类，无loops/有loops各1000个profiles；n=4,m=8，有loops再250个profiles，每个 profile 分别精确遍历19683或65536个分配，均有EFX（seeds 20261027–29，见 `rank2_cap_results.json`）。下一步应按 item word multiset 对称约简做 exhaustive profile 检查，并尝试 CP-SAT/ILP 找最小 counterexample。若所有 rank≤2 都可解，可自然扩到 bounded rank、laminar matroids 或通用 partition matroids；若失败，给出最小 parallel-class/loop 边界也有分类价值。单独两平行类小定理可能不足完整论文；应以“可证主引理＋一个非平凡扩大类或 sharp obstruction”作为最低成文门槛。

## 深挖二：FC-02，混合图的环与定向边界

### 精确问题

G=(N,M) 是 simple graph。边是 item，必须交给其中一个 endpoint；agent i 对其 incident edge e 有 signed rational additive utility u_ie，非 incident edge 的值为 0。使用 EFX^+_0：当 i 嫉妒 j 时，移除 i 自己 bundle 的任意非正值 item，或 j bundle 中对 i 严格正值的任意 item，均须消除嫉妒。

FC-02a：每个连通分量至多一个环（pseudoforest）时，是否总存在 EFX^+_0 定向，可否多项式构造？

FC-02b：仙人掌图中可有多个环；不能许诺普遍存在，应刻画哪些 signed instances 存在并给 polynomial decision/construction，或者证明该类已经 NP-hard。

### 母论文与机制

**Paper Fact。** Zhou–Wei–Li–Li, IJCAI 2024, [原文](https://arxiv.org/html/2409.03594v2)，Theorem 3 给树上的 EFX^+_0；§4 的一般图所有 mixed EFX 定向版本均有 NP-hard 存在性；§6 公开建议 multi-edge/hypergraph 扩张。对应 web refs：turn34view1、turn40view2、turn45view0、turn45view1。论文是 **分类图谱＋视角** 主导，关键不是 EFX 近似常数，而是区分 zero-removal 语义、任意 allocation 与 endpoint orientation。

树算法使用 BFS 层：边若对上层 endpoint 是 good 就给上层，否则给下层。得到的局部结构避免一个带 chore 的 agent 同时对外漏出无法补偿的 good。我们应先抽象“连接到父块时可容忍的两端状态”，再处理环闭合，不能把 BFS 层换成任意环序后直接宣称成立。

**我们的新 idea。** 先做 simple unicyclic；这是从树到有环的最小扩大。若单圈很短即解，把成果当工具，推进 cactus 的 block-cut tree 组成定理；再考虑最优福利或删最少边达到可行，须另查现成优化结果。

### 价值与反方

自然性：acyclic/cycle 是分类论文中最标准的孔洞边界；仙人掌仍有树状块结构，可能允许局部状态拼接，同时保留真实环冲突。它比仅换一个数值集合自然，也比“一般 mixed manna EFX”更可控。

反方：单圈可能用初等 cycle orientation 立即完成，不足成文；cactus 的二连接块宽度很低，若 DP 只是一般 bounded-treewidth 结果的直接特例，价值低。不能选“所有 cactus 都存在”：两三角共享一顶点有 5 点 6 条 all-chore 边，pigeonhole 已否定，这不是新反例。

### 第一 proof obligation 与玩具测试

PO-1：给有树枝附着的一个 cycle 提供一个有限边界状态描述，使每棵挂树可被消去，且 cycle 的约束系统完整等价于 EFX^+_0。须证明状态数不依赖 rational utility 数值大小；若只存总效用可导致 pseudo-polynomial。

PO-2：为 cactus articulation vertex 定义可组合的“own 总效用＋最小负边际＋外部正边暴露”的支配关系，证明可删去哪些状态。任何简单 local condition 必须双向验证，否则可能仅充分不必要。

测试 `toy_search.py` 精确枚举 C3/C4/C5 的 endpoint ±1 profiles（64、256、1024 个），每个 profile 检查全部 2^m orientations，未见反例。另固定 seed=20261020，对 C5 的 endpoint values∈{−2,−1,1,2} 检查 10,000 profiles，无反例。零值版本 C3/C4 还分别穷举了729/6561个 profiles；带挂树的6点单圈图以seed=20261025随机测了10,000个 profiles，同样未失败。`mixed_extension_results.json` 另保存了一个5点6边 cactus 的无 EFX^+_0 实例（第687个 profile，非新反例声明），验证了不能把仙人掌问题写成普遍存在。这些计算支持先试 unicyclic，不证明普遍存在。

## 其余候选的完整取舍

### FC-03：精确配额三值 chores MMS

精确域：m=3n，每人恰好 3 件，c_ie∈{0,1,2}。定义 μ_i=min_{partition into n triples}max_B c_i(B)。问是否总有三件一组的分配且 c_i(X_i)≤μ_i；若不是，确定最小 n 和 approximation gap。没有把 {1,2,3} 另算一个题，因为 exact quotas 下平移同一个常数不改变 exact MMS feasibility。

母论文 Kinoshita–Igarashi AAMAS2026：[2602.08966](https://arxiv.org/html/2602.08966v1)，§3–5 的 quota-aware bag filling/ordered reduction；Appendix D 明确问 quotas 是否改变保证边界，并给固定维度 MBLP 搜索框架（turn40view0, turn45view4）。文章类型为“组合运用＋舍入工具”，新 idea 是第一非平凡有限值积分边界，不是作者已明确提出的三值问题。

可解依据：固定 q=3 使所有 bundle 类型有限；二值 exact quota 情况可 flow：c_ie=a_i+(b_i−a_i)h_ie，μ_i=3a_i+(b_i−a_i)ceil(p_i/n)，把每 agent 的 high items 容量设 ceil(p_i/n)，总件数设 3；1/n fractional assignment 可行且网络 integral。因此双值题本身太轻，应主动淘汰。三值需要同时控制两种 high counts，单流 integrality 不再直接成立。

危险障碍：可能是既有 ternary-goods MMS 算法的 balanced 版本；也可能一个小不可分配例已否定。必须检查“unconstrained ternary exact MMS”是否保持 cardinality，不能自动套用。`toy_search.py` 对 n=3,m=9，三个成本集合各 10,000 profiles，精确算 280 个无标号 triple partitions、1680 个 labelled allocations，均无反例。首 proof obligation 是从 quota MBLP 的 n=3,m=9 数值证据提取极点结构，或找到最小反例；不能以随机实验当定理。价值暂低于 FC-01。

### FC-04：五人公共双值 EFX

精确域 n=5、c_ie∈{1,r}、任意 rational r>1。He–Tao §6 公开问四人以上（[2606.08872v2](https://arxiv.org/html/2606.08872v2)，turn34view3）。文章类型为“反例突破＋分类算法”；其四人证明按大成本 agent 子集分 item，使用 deficient-set multigraph 和拼接。

新 idea 可先限 r=3 或 sparse large-agent hypergraph，检查 deficient-set 工具是否能避免任意三元/四元交叠。不能加 PO：同文 Thm2 已否定某些 r 的 EFX+PO。也不能把 r=2 当首新例：Lin–Wu–Zhou 2025 的 [原文§4、Theorem4.13](https://arxiv.org/html/2501.04550v1) 已给任意人数 {1,2} 的多项式 EFX+PO（turn126view1, turn142view2）。

价值很高且确实推进公开题；最危险是 n=4 拼接已经篇幅很大，n=5 需要新机制，符合用户想避开的“稍小但仍主猜想”风险。玩具模型是五人、三种 large-agent subset 类型、m=11/12；可证伪是 exact enumeration/SMT 搜 counterexample。首义务是证明三元素 deficient set 能分解；没有依据前不主攻。

### FC-05：常数 EFX 的多项式初始化

精确域一般 positive rational additive chores；求固定 universal α 的 polynomial-bit-time α-EFX。Garg–Murhekar [2507.19461 §5](https://arxiv.org/html/2507.19461v1) 明确提出（turn34view6）。框架类型为“统一工具”：给 suitable friendly allocation 后 local swaps 多项式；瓶颈是 pEF1+PO 或 earning-restricted equilibrium 的构造。

我们的可限缩 idea 是“每 agent 至多三 cost levels、但 level 值可不同”时构造 weakly λ-EFX-friendly 初始分配；应先写出该输入域是否已经有市场算法。价值在可迁移初始化，不在重证 swapping。致命风险：求 pEF1+PO/ER equilibrium 可能携带 PPAD/固定点复杂性，直接攻一般算法过大。首测试：用整数/有理 LP 找三值 small profiles 初始不变量失败；首义务必须是多项式 initializer，不可只给存在。

### FC-06：三人九件 additive EFX

精确域 n=3,m=9, c_ie≥0 rational。Xinkai Zhang 的最新7/8件论文 [2609.10585v2](https://arxiv.org/html/2609.10585v2)，Thms1.1–1.2、§1.2（turn40view3）。类型为“计算证明视角”：把不存在任何 EFX allocation 表成 QF_LRA，每个分配对应一个 failure clause；8件先按共享最便宜 item 插入结构简化。

新 idea 可先研究 cheapest-set pairwise disjoint 的9件情况、寻找可删物 insertion lemma，再做SMT。价值是真推进明确三人 open problem；危险是 clause 数增至3^9，直接加算力不产生结构贡献，而且8件作者已有同一路线。首义务是减少有效 bundle-size patterns 的证明；母文已警告只看 balanced sizes 会漏掉 EFX allocation，不能这样“优化”。作为短期反例搜索备份，不列首推。

### FC-07：restricted costs + OPT 的 sharpΔ（主动淘汰）

精确域 c_ie∈{0,c_e}、c_e>0，Δ=max_e c_e/min_e c_e；要求 allocation 最小化社会成本并尽量 α-EFX。

母文 Lin–Wu–Zhou 2026 Table1/Observation1.2 给零成本指派与 EFX 的冲突，类型为“公平与效率的组合”。我们提出的 Δ 参数看似自然，但实际过于简单：

把每个正 cost 改成1，调用 binary EFX+PO 算法。该 allocation 把所有有免费 owner 的物品交给免费 owner，因此同时是原实例最小社会成本。binary EFX 的计数不等式乘 max c_e/min c_e 即得 Δ-EFX。反例 costs [[Δ,1,0],[Δ,0,1]] 中，两个 OPT allocations 的最小 EFX factor 都为Δ（可移除 own zero item），故界紧。

这不是可主攻的开放题；应作为 lemma/negative lesson 保留，不能包装成新论文。`toy_results.json` 用Δ=5逐一核了2^3 allocations。

### FC-08：已解旧问题筛除

weighted binary WEFX+fPO 已被 Lin–Wu–Zhou 2026-09 [2609.13970](https://arxiv.org/html/2609.13970v1) 覆盖；个性化双值 exact MMS 有 Zhang 2026-08 [2608.15822](https://arxiv.org/abs/2608.15822) 明确同题声明。二者文章分别是“lexicographic potential 工具”和“quota/envelope/flow 组合”；可学习其机制，但不能原封不动再选。若后续要扩展，必须新增被原文定理明确排除的域，并先检查 proof 是否已允许该域。

## 本轮计算的边界与复现实务

全部代码只使用整数、固定 seeds，任何 ratio demo 用 numerator/denominator 输出。`toy_search.py`、`rank_toys.py`、`mixed_extension_toys.py` 做有限成本 profile 搜索，未覆盖任意实数参数。`construct_rank2.py` 是局部引理的实际算法原型，检查 complete allocation、EFX，以及 m≥n 时 EF；不是只检查实现内部变量。

不要把“没有失败的随机 profile 数”解释为成功概率或新颖性。FC-01 的两类 no-loops 结论靠完整证明；其有loops/三类扩大版保持 OPEN。FC-02 的全局 unicyclic/cactus 结论保持 OPEN。

最后时效补核：2026-10-20 额外检索一般常数EFX多项式、3/2-EFX与mixed cactus，未找到覆盖FC-01/02的新结果；检索不是完整文献证明。Lin–Wu–Zhou2025的{1,2}exact EFX+PO已直接核到Theorem4.13。


## 代码与冻结证据的仓库位置

本报告的脚本位于 `tests/audits/topic_selection/fair_chores/`，输出位于 `evidence/runs/topic_selection/fair_chores/`。复现时复制脚本到新的临时目录运行，勿覆盖冻结输出；完整索引见[本轮复现与核验](../VERIFICATION.md)。
