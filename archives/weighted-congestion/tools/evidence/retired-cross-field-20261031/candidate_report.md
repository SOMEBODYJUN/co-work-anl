# 跨域工具迁移与独立反方：本轮重新选题报告

日期：2026-10-20。已完整逐字阅读本轮 USER_GUIDANCE.md 及仓库 AGENTS.md；用户已切题，本文不把 UM 当研究目标。模型配置只可确认继承父任务且未覆盖；工具未暴露可独立核验的型号/推理参数，不能伪称完成型号审计。

本文的职责是寻找交叉机制并反打另外五条子线，不要求把同一个问题换名列为独立成果。所有候选都保持 OPEN；下文唯一已有完整局部论证的是 CB04 的无 loops、两个平行类特例，证明原创草稿来自 fair_chores，本文独立攻击及计算复核，不能据此宣布文献新颖或一般 rank-2 已解。

## 本轮排序与决定

| ID | 精确切口 | 类型与迁移 | 当前决定 | 最危险问题 |
|---|---|---|---|---|
| CB01 | 两种容量 BMKP 的硬容量 `(2/3−ε)` | 结构化舍入＋联合标签＋匹配 | 前二；深入，须完整证明审查 | 独立分组存在性不等于可同时恢复；matching 与 LP 的共同可行性 |
| CB02 | goods with copies 的 SD-EF1，先三人 `c_g∈{1,2}` | 公平分配→多序 prefix b-matching | 前二；深入 | 共同顺序易解；异质顺序可能含多排列 discrepancy 难核 |
| CB03 | 四人 laminar 的 K8/K12 ordered-no-envy EF1 | 小障碍分类→有限多面体覆盖 | 强备选 | 排名信息不够；母文已否定更强 top-i 分离 |
| CB04 | loopless rank-2 matroid chores，先三个平行类 | 二元词→Hall 翻转→边界扩大 | 当前最有实质 lemma 的工具苗头 | 两平行类过短；三平行类不能直接翻译二元补词 |
| CB05 | ladder graphic matroid 的 weighted prefix basis | matroid exchange＋ordered discrepancy | 储备 | 固定 rank/corank 常数界是平凡的；cactus 只是 partition matroid |
| CB06 | 同时 RM+ 的随机全信息反馈，先二元协调 | 镜像下降提升空间＋随机近似 | 研究兴趣强，低于前二 | 泛化成 generic SGD 换符号；不能遗漏 clipping bias |
| CB07 | 非对称 size-2 monotone congestion PNE | 局部优化＋稀疏 Gram 二次势 | 明确公开问题，边界风险大 | 可能碰 Local Max-Cut 的长期边界；不能乱用 PSD QUBO |

检索未找到完全相同的后续结果不等于证明不存在；每题开工前仍须追踪母文最新版本和引用链。

## CB01：两容量 BMKP 的联合类型舍入（深入）

**模型与量词。** 输入二进制有理数 `w_e,p_e≥0`、`m_1` 个容量 1 背包、`m_2` 个容量 `C≥1` 背包。每个物品至多使用一次，可剩余；严格不超容量；最大化各背包所得 profit 的最小值。对每个固定 `ε>0`，目标是关于输入位长多项式时间的 `(2/3−ε)` 算法；`C` 是输入，不能假设常数或允许资源扩张。

**Paper Fact。** Chen–Hu–Mao–Chen–Mei–Zhang–Chen–Zhang，ICALP 2026，§7 最后明确提出常数种容量的问题。§6 Thm3 的 `1/2+ε` 硬度使用 `B_j=t−u_j`，并未限制为两种容量。§4 Lemma8 构造 constant profile 的 slack solution，Lemma13/18 作 critical-item separation。全文：[正式版](https://drops.dagstuhl.de/storage/00lipics/lipics-vol374-icalp2026/html/LIPIcs.ICALP.2026.60/LIPIcs.ICALP.2026.60.html)，[完整稿](https://arxiv.org/html/2605.05233v1)。本次 refs：turn94view0、turn95view1/2、turn106view0/3。

**文章定性。** 这是问题突破＋结构化舍入工具：先付出允许的 profit 损失以制造容量 slack，再对敏感重物品用数据依赖代表元。核心不是普通 max-sum knapsack PTAS；后者可牺牲少数 bins，max-min 不允许。

**我们的新 idea，与已知分开。** 对未知最优解按容量分组，分别应用母文的存在性变换，得到两份小 profile。每个 item 同时记录两套 capacity-specific label，连同全局 profit bucket/expensive 标记，形成联合类型。critical 不按容量分别选，而定义为所有 long bins（至少三项）中的 expensive items 之并集；给出每联合类型的 critical 总数后，尝试全局选该类型最重的这些 items。

**一个有条件的交换引理。** 假设联合标签已固定、long bins 对其自身容量的 rounded weights 可行、同类型 profit 差 `<δ`，且 long 中所有 expensive items 都算 critical。同类型中若 critical `e` 比 noncritical `f` 轻，将 `f` 换入 `e` 的 long slot；`f` 原来只能在 short bin 或未使用。该 long slot 的 rounded weight 不变，short 中换入较轻 `e` 不破坏实际容量。每个受影响 slot 损失 `<δ` profit。重复可恢复全局最重集合。这个论证只解决“已提供正确联合标签和 rounding 可行性”后的 canonicalization，**没有解决整个 BMKP**。

**first proof obligation。** 从母文精确定义重建两容量 joint-label construction，并证明每种容量的正确 rounded feasibility 同时存在、联合类型数只依赖 `ε`，且可枚举的 counts/configurations 完整覆盖上述解。之后必须分别核预算、short matching 和 cheap LP；不能只说“复制同容量证明”。

**其他真边界。** small-eligible pair edges 包含于 large-eligible edges，故“固定总 matching 边数且至少指定条 small edges”可转最大权 matching；不是一般 Exact Matching。母文 cheap LP 的式 (13) 已允许 `B_j`，但使用前必须核分数见证与所选 matching 仍相容。高 profit singleton 的 preprocessing 在母文用了同容量假设；若改用最小可容纳背包的交换，必须重写残余 OPT 不变证明。

**价值判断。** 是原作者明确问题的最小非同质扩张，若闭合则直接推进原问题；联合类型工具可迁移到有少数资源模式的 max-min rounding。反方：关键步骤也可能是母文的短推论，仍需做完整算法而非把条件引理包装成定理。未给成功率或二十天可解承诺。

**最小玩具。** 两个 bins 容量 1、2；同一物品可在小 bin 中被标作 heavy、在大 bin 中被标作 light。分别选最重 critical 集会抢同一物品，是检验“全局 union”必要性的最小模式。再用两种容量、4–8 项的整数枚举，专门对比正确结构解与 canonical 后的 matching/LP 见证；目前尚未完成此算法级实验。

## CB02：copies SD-EF1 的多序 prefix 形式（深入）

**模型。** `n` 人、类型集合 `G`，每型有 `1≤c_g≤n` 个 identical copies；每人至多得每型一份；每人对类型有任意弱序（可以来自非负 additive 值）。完整分配要求 `x_ig∈{0,1}`、`Σ_i x_ig=c_g`。先研究 `n=3,c_g∈{1,2}`、类型数不固定的存在性或算法，不能把“四型有限枚举”当一般定理。

**Paper Fact。** Cookson–Ebadian–Shah，AAAI 2025《Constrained Fair and Efficient Allocations》，§3.3.2 Definition5、Theorem6 及紧随其后的 Open Question。partition matroid 的 SD-EF1 被否定，但 copies 特例被单独保留为开放。[作者稿](https://www.cs.toronto.edu/~nisarg/papers/constrained-fair-efficient.pdf)，refs turn51view1、turn53view4/5。

**定性与机制。** 母文是分类/边界论文：同一个 cardinality constraint 不能保证 ordinal EF1，copies 的“同型同值且每人至多一份”留下特殊结构。我们迁移 b-matching 与多序 prefix discrepancy，不是重新分析 MNW。

**我们的等价改写。** 对每 `i,j` 及 `i` 的每个 top-type prefix `P`，要求

`Σ_{g∈P}x_jg − Σ_{g∈P}x_ig ≤ 1`。

此条件等价于 SD-EF1：从 `j` 的 bundle 删掉在 `i` 看来最高的一项；凡 `j` 的 prefix count 为正，该最高项都在 prefix 中，故减一即可；反向由删除一项立即得到。弱序只需检查完整 tie blocks，任一严格细化的充分解也适用于原序。

**first proof obligation。** 三人对所有 `c∈{1,2}` 的上述 0/1 系统是否总可行？先证明某个可保持 feasibility 的交换/增广不变量，或构造五型以上最小反例。两人时 `c=2` 对所有人强制分配可消去、`c=1` 是无约束问题；共同顺序也可按顺序循环分配，所以这些不是足够的主结果。

**具体可证伪测试。** `toy_checks.py` 独立枚举三人四型：用类型重命名固定第一人顺序，`2^4·(4!)^2=9216` 个严格 profile，每个 `3^4=81` 个 allocation，全部有解。forced full-copy 类型可以消去。结果没有证明任意型数、任意人数；亦没有估计概率。随机检索到更大 profile 无反例只作为探索，不写成下界。

**近邻反查。** Haviv 2026-07 [2607.01059](https://arxiv.org/abs/2607.01059) 是 common preferences 的 conflict-constraint SD-EF1；不能转成 heterogeneous orders 的解。2026-07 [2607.10232](https://arxiv.org/abs/2607.10232) 的 mixed-manna ordinal 不相容涉及 ex-ante 与 ex-post 的组合，也不是本问题反例。refs turn51academia21、turn73search0（后者原文入口须再打开核实，不作为定理依赖）。

**价值/风险。** 推进一个明确公开问题；若先得到三人全型数，可独立描述有意义的结构边界。风险是一般多序 discrepancy 的经典障碍，简单 round-robin 会因每人不能重复领取同型而卡住；任意 partition 的负例不能直接复用，因为那里面同一类别两物品值不同。

## CB03：laminar key matroid 的有限多面体覆盖

**模型。** 四人 additive 非负值；K8：类别尺寸 `(3,3,2)`、每类 cap1、总 cap2；K12：四类各3、每类 cap1、总 cap3。找完整可行 EF1 且固定次序 `i<j` 时 `i` 不 envy `j` 的 allocation。

**Paper Fact/原位置。** Cookson–Shah 2026-08 [2608.31121](https://arxiv.org/html/2608.31121v1)，Appendix B Definition13/14、Lemma11；§5 明确讨论两 key 问题，Lemma12 反驳 top-i favorite 分离策略。refs turn112view0、turn132view0/1/2。三人 laminar 和任意人数 transversal 已解，必须避开。

**类型/idea。** 结构分类论文把无限族压到两个有限障碍。新路线是对每个 feasible allocation 写出 EF1＋ordered-no-envy 的 valuation 多面体，再尝试证明其并覆盖整个非负正交锥；或寻找不覆盖点给出有理反例。EF1 的 favorite-deletion 要作 disjunction 或先细分 value-order chambers，不能错写成一个 LP。

**首义务/玩具。** 先 K8：864 个 feasible allocations；把遗漏 valuation chambers 转成严格线性不等式不可行证书。独立复核 seed20261020、值域0..20 的1000个 profile 全有解。不能由此推出普适存在，且母文电脑尝试已失败，维度32的 chamber 数是致命障碍。两个 key 均解决才推进四人全部 laminar；只解K8是中间模块。

## CB04：二元词的 Hall 翻转与 rank-2 chores 边界

**模型。** 首特例无 loops、每个 agent 有二分 `M=A_i⊔B_i`，成本 `r_i(S)=1[S∩A_i≠∅]+1[S∩B_i≠∅]`。主研究切口扩大为无 loops rank-2 matroid、允许三个平行类：`r_i(S)=min{2,触达的平行类数}`；再考虑 loops。完整 EFX，无 PO 要求。

**Paper Fact。** Lin–Liu–Tao–Zhou 2026-08 [2608.10572](https://arxiv.org/html/2608.10572v1) §4 留 binary-submodular chores exact EFX。该文 rank-2 partition 的反例成本是 **nullity** `|S|−r_i(S)`，不是 rank。Tao–Wu–Yu–Zhou TCS2025 [DOI](https://doi.org/10.1016/j.tcs.2025.115248) Thm5.2 给 cancelable EFX，Thm6.7/Cor6.8 对 submodular 只有2-EFX。refs turn113view0、turn127search0/2。

**局部已有论证，来源须记清。** fair_chores 提出二平行类 Hall 翻转证明，本文独立审阅并指出纯色非空分配实际是 EF。`m≥n` 时，把 chore 写作 n 位词。若全部词出现，可给 n 人互不相交的互补词对，使每 bundle 从每人看 rank2，得到 EF（`n≥2` 时 `2^(n−1)≥n`）。否则对 missing word `w` 建 agent-item 图，`i` 邻接第i位异于 `w_i` 的项。在 missing words 中取最大 matching 最优者；若未覆盖全体 agent，交替可达集 `S,T` 满足 `|T|<|S|`。若 `w⊕i` 仍 missing，可先换 matching 使 `i∈S` 未配，再选**全局未匹配** item `e`（不能随便选 `e∉T`）并翻第i位增广。故所有 `w⊕i` 必出现；这些不同的 items 原来仅邻i、都在T，矛盾。于是得到每人非空且 owner-pure 的分配，成本own1、他人非空成本至少1，即 EF。`m<n` 单件分配给出 EFX。找到 missing word可用显式类型 trie；full-word 分支 `2^n≤m` 不破坏多项式性。

**独立计算。** 三人、3到8 chores 的全部12825个 word multisets，代码构造 witness 并逐对整数复核 EF，没有失败。这是对论证的回归，不是其证明，也不认证文献新颖。

**价值与反方。** 二元词＋Hall-flip 是可迁移的小工具，证明超出 cancelable，但体量很短。三平行类中“异于 missing coordinate”不再保证 owner-pure，正好暴露机制边界。首义务：找对三平行类有用的替代 Hall 障碍或最小 EFX 反例；不要声称二元证明已解一般rank2。可先枚举三人、7–10项的 type multisets，使用精确 EFX 判据。

## CB05：weighted prefix basis 的真正非平凡图类

**模型。** `G` 为任意长度 ladder graph，边任意排列，`x` 在 spanning-tree base polytope，边权 `w≥0`；找 spanning tree `T` 满足每个边序 prefix 的 weighted discrepancy `≤C·max w`，`C` 与图长无关。先不加 cost，随后用 cost-augmentation。

**母文/类型。** Bérczi–Liu–Reis–Tarnawski 2026-08 [2608.13983](https://arxiv.org/html/2608.13983v1) §6 Conj5/6，Prop15 binary、Thm16 uniform；工具型 matroid exchange＋partial coloring。refs turn51view0、turn53view1/2/3。2026-10 [2610.16079](https://arxiv.org/html/2610.16079v1) §2.1/Appendix B 的 hard-H rounding 限定 partition 或 block-TU，不自动覆盖所有 graphic matroids；refs turn70view3/4。

**我们的判断。** 固定 rank r 或 corank r 时 `C=r` 只是总权重界，不能当研究进展。cactus 的 spanning-tree bases 是“桥必选、每cycle删一边”的 partition matroid，作为新graphic theorem只是换符号。ladder 有无界 rank/corank、共享cycles，较自然。首义务：用 ladder 的局部交换/路径分解得到不随高度累积的 weighted prefix error。玩具：3–5格 ladder 枚举 spanning trees、`x` 为它们的有理平均、权值1/2/3和随机边序，先找C=1是否已假；尚未执行。风险：任意边序可把图结构优势抹平，和一般 prefix conjecture依然接近。

## CB06：随机 RM+ 的 clipping-稳健性

**模型。** 两人二元 identical-interest game，potential `Φ(p,q)` 多线性、有界；每轮 agent 得到无偏、条件方差有界的全信息 utility-vector 估计，同时作标准 `r←[r+estimated regret]_+`，`x=r/||r||_1`。目标先证明到 ε-NE 的可说明复杂度，或给明确反例；不要悄悄改成预先知道精度的lazy/mini-batch variant。

**Paper Fact。** Tewolde 等 ICLR2026 [2510.17067v2](https://arxiv.org/html/2510.17067v2) §5 明确提出 stochastic/bandit feedback；Thm3.12 已覆盖零初始化lazy simultaneous 收敛，Appendix C.11 已覆盖指定大初始化 simultaneous，不能重新提出。refs turn113view2、turn115view1/2。另 [2608.17417](https://arxiv.org/abs/2608.17417) 2026-09被管理员以作者/机构不可核实撤回；它的旧 bounded-regret claim不能作定理依赖，也不能假装它未存在，ref turn114view1。

**类型/新idea/义务。** 势函数→提升空间镜像下降的工具迁移到随机近似。首义务是定量控制 clipping 在无偏噪声下的偏差与 potential drift；仅把 deterministic norm monotonicity 放入期望是错误的。最小玩具用二元协调、无偏对称±noise，记录 regret-state范数、势、last-iterate gap。真正价值是对原算法的稳健性；generic SGD 的直接替换不够。未执行玩具；前二题优先。

## CB07：size-2 PNE 与受约束局部二次优化

**模型。** 非加权 atomic congestion；每人的显式策略集合中每策略至多两个资源；延迟非负单调非减。计算任一PNE，不是全局最小Rosenthal potential。先精确限制每人两策略、affine latencies。

**Paper Fact。** Bilò 等 AAMAS2025 [Minimizing Rosenthal's Potential](https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p343.pdf) §6 p350 明确问 size2一般策略、size3对称策略的PNE复杂性。Thm2 symmetric size2 global minimum易，Thm3 asymmetric size2 global minimum NP-hard；全局困难不等于PNE困难。refs turn112view1、turn113view3、turn114view0。

**分类/机制与风险。** 二元策略affine时可写 `Φ=const+h·z+ΣQ_ij z_i z_j`，差分 incidence矩阵每列至多四个非零，Gram型 `Q` 受结构限制。工具迁移是识别稀疏局部优化边界，不是声称任意PSD QUBO可嵌入。经典Max-Cut构造每策略大小等于顶点度，不能因为每资源仅两人使用就称size2已PLS-hard。首义务：精确表征可表示的带场二次型，并确认已知LocalMaxCut低度结果是否覆盖。最小玩具枚举2–5人、每人两条size2策略和小affine整数系数，比较flip graph；尚未执行。该题可能靠近长期复杂性边界，不能轻率排在BMKP之前。

## 及时 battle 的淘汰记录

- NeurIPS2025 [2502.08519](https://arxiv.org/html/2502.08519v2) 已给3人adversarial-team ε-NE 的CLS-completeness；更早论文的“常数队员”问题不能重提。其two-team polymatrix开放又被2026-06 [2606.16139](https://arxiv.org/abs/2606.16139)更新，须用新文而非旧open list（本次refs turn11view0、turn70view1）。
- unrestricted rank2 bimatrix不宜直接当开放题：Adsul等 [1812.04611](https://arxiv.org/html/1812.04611v4)参考文献包含Chen–Paparas2019 rank2-hardness personal communication；公开状态未彻查，属于风险题。§10 output-sensitive rank1 enumeration与smoothed path analysis确有明确问题，但更大、更远于本轮目标，故不进前七。
- restricted-additive chores 的最小社会成本＋Δ-EFX前沿，经fair_chores自反查是binary算法缩放的短推论，且母文小例给sharp Δ，不再作为论文题。
- balanced EF1+fPO 的三类 additive 扩张已被2026-08 [2608.06325](https://arxiv.org/abs/2608.06325) 的全additive结论覆盖（本项由fair_goods核实，本报告未独立重建该文，不能当本文核心依赖）。

## 文件与证据边界

`toy_checks.py`、`toy_results.json` 仅在本子线目录；计算可重现、全整数、没有调用优化浮点容差。输出包括copies的9216个profile、rank2-chore的12825个multisets、K8的1000个随机profile。所有一般新结论仍需正式证明重建和独立审读。没有git操作、外部消息或凭据访问。


## 代码与冻结证据的仓库位置

本报告的脚本位于 `tests/audits/topic_selection/cross_field_battle/`，输出位于 `evidence/runs/topic_selection/cross_field_battle/`。复现时复制脚本到新的临时目录运行，勿覆盖冻结输出；完整索引见[本轮复现与核验](../VERIFICATION.md)。
