> 这是第一轮原文卡与推导记录；后续裁决以 [BATTLE](../BATTLE.md) 和 [候选池](../candidate_pool.json) 为准。全库来源统一为 A=作者明确原题、B=作者明确建议方向、C=团队派生；本稿局部使用的分级符号不得当作统一来源标签。

# boss37 重新选题：GAP、预算/容量分配、舍入结构（研究者 C）

核查日期：2026-10-20。此文件是第一轮研究底稿，供公屏 battle；不是已经完成的新定理或已经确认无人研究的选题清单。

## 0. 本轮决策原则与结论

按用户指导重新选题：问题质量、20 天能形成可包装的真实结果优先；每天约 12 小时可用高强度推理；方向限定运筹学与优化理论；从作者明确提出的问题或对强文章的工具/视角/分类的本质理解出发；广泛比较，不能搜到一个就停止。不回到一般 R||Cmax 或 Santa Claus 常数大坑。本池没有纯调度题。

本轮列出 15 个不同候选，其中有些应淘汰。按当前证据，值得进入第二轮的前三项是 C08（两种尺寸的 knapsack correlation gap）、C06（非均匀 opening cost 的可实现联合舍入）、C01（向量容量下 LP 值函数子模性失效与恢复类）。它们的共同优点是有明确的工具瓶颈、很小的玩具模型和可证伪切点；共同风险是“现成通用定理早已覆盖”，所以第一天必须先完成交叉文献审查。

已经完成的实质工作：

1. 精确有理数顶点枚举验证：即使只有一个 bin、两个资源、每个 item 的资源列有 consecutive ones，分数 LP 的启用物品值函数也可能不子模，见 §4 和 [精确向量 LP 探针](../probes/vector_capacity/exact_vector_lp.py)。因此不能把 scalar-GAP 的子模 LP 工具直接搬到交通容量向量。
2. 完成“配置地集上的 max-coverage 子模归约”的完整初稿，逐项列出指数地集、pricing、近似 oracle、预算舍入的边界，见 [配置归约与 oracle 边界](../notes/configuration_reduction_boundary.md)。
3. 找到直接去重文献：CGST 2011 Theorem 1.3、§4.2 已包含 bins 上的任意 matroid；2026 GS-Poisson Theorem 1.4–1.5 已大幅加速 GAP/SAP。这使 C05、泛泛的“快一点的 SAP continuous greedy”不适合宣称新颖。

## 1. Primary 文献与文章定性（已打开正文）

以下的“原文位置”是正文定位，不用二手综述推断作者意图。P01–P11 共 11 篇，已经打开 primary 全文。没有找到更新的解决文献，只能记为“本轮检索未发现”，不能写成已证明仍公开。

| 编号 | Primary 文献与链接 | 驱动类型 | 已核的具体位置与用途 |
|---|---|---|---|
| P01 | Kulik, Sarpatwar, Schieber, Shachnai, **Generalized Assignment via Submodular Optimization with Reserved Capacity**, ESA 2019. [正文](https://arxiv.org/html/1907.01745v2) | 工具 + 组合驱动；把 assignment LP 值函数变成次模函数，再与保留容量和 ST rounding 组合 | Theorem 1：scalar-size LP 值函数子模；Theorem 2：半容量下取原 OPT 的 1/3；Theorem 4：总量≤m/2 的 almost-feasible packing 修复保留≥1/2 利润；Theorem 5：Group GAP 1/6。§6 明确问组尺寸阈值、细小物品和 AGAP 扩展。 |
| P02 | Adany et al., **All-or-Nothing Generalized Assignment with Application to Scheduling Advertising Campaigns**, TALG 2016. [作者 PDF](https://www.openu.ac.il/personal_sites/moran-feldman/publications/TALG2016.pdf) | 问题 + 工具驱动；group all-or-nothing 与 bin 内同组互斥，使常规删除大物品失效 | §1.1、Figure 1、§2：general AGAP 1/(19+ε)，每组 cardinality≤m/2、统一容量；§3.1 固定 bins 数的随机 PTAS；§5 divisible sequence 特例；Appendix A assignment restrictions 与非同容量会造成强障碍。 |
| P03 | Jiang, Samaranayake, **Approximation Algorithm for Generalized Budgeted Assignment Problems and Applications in Transportation Systems**, DAM 2024, arXiv:2208.11832v4. [正文](https://arxiv.org/html/2208.11832v4) | 问题 + 组合驱动；interval capacity vectors、opening budget、两类 online mechanisms 耦合 | Eq.(1.4) configuration LP；§4 conservative magician；Algorithm 1；Theorem 5.2 和 5.4 的 feasible 近似界；§7 明确问改善算法分析/比值和 stochastic items。 |
| P04 | Sergeev, **On contention resolution for the hypergraph matching, knapsack, and k-column sparse packing problems**, ETH 硕士论文（写作 2020、arXiv 发布 2024）. [PDF](https://arxiv.org/pdf/2404.00041) | 工具 + 分类驱动；按 knapsack 尺寸类别分解 CRS 瓶颈 | §4.1 Theorem 4.1、Conjecture 4.1–4.2（PDF pp.23–24）；§4.2 大/小物品 CRS；§4.3 混合；§6 说不同尺寸类如何组合仍是瓶颈。注意不是“2024 刚提出”的结果。 |
| P05 | Husić, Koh, Loho, Végh, **On the Correlation Gap of Matroids**, IPCO 2023 / Math. Programming 2024. [PDF v3](https://arxiv.org/pdf/2209.09896) | 分类 + 视角驱动；从统一 1−1/e 转向 matroid 结构参数及 worst weighting | Theorem 1.3：固定 matroid 的最坏 weighted rank correlation gap 由 uniform weights 达到；Theorem 1.5：rank+girth 下界；§7 明确问特殊 matroid 类和其他结构参数。 |
| P06 | Kalaitzis, Mądry, Newman, Poláček, Svensson, **On the Configuration LP for Maximum Budgeted Allocation**, SODA 2015 / arXiv:1403.7519. [PDF](https://arxiv.org/pdf/1403.7519) | 工具 + 结构驱动；configuration LP 的强度与 big-item rounding | Theorem 1：restricted MBA 与 graph MBA 有 3/4+c；§6 graph case；§7（PDF pp.27–28）明确问怎样同时处理 many eligible players 与 nonuniform prices，并建议 GAP 等迁移。 |
| P07 | Barman, Khan, Shyam, Sreenivas, **Guaranteeing Envy-Freeness under Generalized Assignment Constraints**, arXiv:2305.01339. [PDF](https://arxiv.org/pdf/2305.01339) | 问题 + 新证明模板驱动；feasible-subset envy、density domination、minimal envied set | Theorem 1 divisible FEF；Theorems 2–4 indivisible FEFx existence、pseudo-poly、FPTAS；§4.2 Remark 1 覆盖 matroids；§5 明确问 FEF+Pareto、polyhedral constraints、matroid 精确 FEFx 的 polynomial complexity。 |
| P08 | Fairstein, Kulik, Naor, Raz, Shachnai, **An Almost Optimal Approximation Algorithm for Monotone Submodular Multiple Knapsack**, JCSS 2022 / arXiv:2004.12224. [PDF](https://arxiv.org/pdf/2004.12224) | 工具 + 组合驱动；leveled bins、block reduction、fractional grouping | §4 Conclusion（PDF p.19）：1−1/e−ε 已得；精确去 ε 和 SGAP 的 1−1/e 是作者方向；明确说 block reduction 对部分推广失效，非单调已另文处理，不能把它当新问题。 |
| P09 | Călinescu, Chekuri, Pál, Vondrák, **Maximizing a Monotone Submodular Function Subject to a Matroid Constraint**, SICOMP 2011. [作者 PDF](https://chekuri.cs.illinois.edu/papers/submod_max_sicomp.pdf) | 工具 + 视角驱动；continuous greedy + pipage rounding，并用配置覆盖刻画 SAP | Theorem 1.3、§4.2 pp.1758–1759 已写 bins 上任意 matroid；Theorem 4.1 有 α-pricing 时为 1−e^(−α)−o(1)。是本轮去重主文献。 |
| P10 | Ganz Rozenman, Kulik, Schwartz, Singh, **A Poisson Process for Submodular Maximization**, arXiv:2605.03071（2026-05-04）. [正文](https://arxiv.org/html/2605.03071v1) | 工具主导；Poisson swaps 避开离散化和单独 rounding | Theorems 1.4–1.5：GAP/SAP 快算法。SAP α 单 bin 近似、其时间 p(n,α)，总时间 Õ((n/ε+p(n,α))m)，比值 (1−ε)(1−e^(−α))。注意作者不是 Buchbinder–Feldman；后者是文中比较对象。 |
| P11 | Klimm, Knaack, **Generalized assignment and knapsack problems in the random-order model**, Mathematical Programming（2026-08-12）. [正文](https://link.springer.com/article/10.1007/s10107-026-02405-6) | 视角 + rounding 驱动；先允许每 bin 一件 overflow，再随机取 last 或 rest | §1.1 与正文算法：general random-order GAP 比值 (1−ln2)/2≈0.1534，fractional single knapsack 1/e 且最优。是在线题去过期的必要门槛。 |

补充去重：Hathcock–Jin–Patton–Sarkar–Zlatin 的 **Online Submodular Assignment** 正确版本为 [arXiv:2401.06981v2](https://arxiv.org/pdf/2401.06981)，Theorems 1.1、1.3、1.4。arXiv:2412.03826 已撤回，是误重复提交，不是错误定理撤回；不可继续引用它作最新主版本。2026 norm-budgeted packing 的搜索结果 arXiv:2607.12437 只检索到摘要，正文打开失败，故不据其任何具体 theorem 做选题判断。

## 2. 候选池（15 项）

评分是可修订的选题判断，非成功概率统计。A=应进入第二轮；B=保留；C=不建议主攻；X=本轮已经有直接去重/太易/大坑证据。每项都区分作者明确问题和我们提出的切口。

### C01. 向量容量 LP 值函数的“禁型—恢复类”分类【A；新 idea】

**精确对象。** 对 A≥0、b≥0、w≥0，定义 φ_w(S)=max{w·x: Ax≤b, 0≤x≤1_S}。对给定矩阵族，要求对所有 w,b，φ_w 都子模；先研究 consecutive-ones 二元列、两资源、laminar resource sets，及允许 assignment simplex 的推广。目标不是“rank=2 也可解”，而是找到由哪些局部交换障碍控制可扩类性。

**来源/已知界。** P01 Theorem 1 的证明来自 splitting into weighted matching；P03 的交通矩阵有连续 1。本轮 §4 给出两资源连续 1 列的精确反例，所以 TU/integrality/consecutive ones 本身不足以保住次模性。

**20 天真实输出。** 最低可接受结果：三列障碍的必要性/充分性在一个非平凡 matrix subclass 成立，外加可检验识别算法；或给一个保住 approximate submodularity 的 quantitative defect bound，并确实使 group-selection approximation 改善。先从“列支持是一条 chain”与“crossing、包含三列”做完整枚举；树/laminar 支持不能直接视作充分。

**价值判断。** 分类题要看是否有必要充分定理、是否真正解释工具为何失效、是否转成新的可用 oracle；只给反例或把 rank-one 换元后再证明一遍价值低。**致死障碍：** weighted-rank/polymatroid characterization 可能已把该分类完整包含；若是这样，必须换成 genuinely fractional、assignment-coupled 类，否则淘汰。

### C02. Group GAP 的组总尺寸阈值越过 m/2【B；作者明确 open + 限域新切口】

**对象。** P01 模型：m 个统一容量 bins、item 尺寸与 bin 无关、利润随 bin 变化、组 all-or-nothing。求对某个固定 η>0，当所有组 s(G)≤(1/2+η)m 时的 polynomial 常数近似；先另加 max_i s_i≤1/3 或“每组大物品骨架可匹配”这样的 packing invariant。

**原文/已知。** P01 §6：阈值在 [m/2,2m/3]；Theorem 5 在 m/2 为1/6；§1.1 引述 >2m/3 无任何常数，不能把全部区间主攻。**20 天输出：** 只需一个严格越过 m/2 的自然类、明确 η 与比值，或证明某看似足够的 packing invariant 仍失败并找到正确条件。**价值：** 改的是工具适用阈值而不只是 ε 改善。**致死：** 即使单组也可能包含 packing feasibility 的硬核；必须对选中组全装入且保住 assignment profit，不能只证明存在无利润的装箱。

### C03. Reserved capacity 的 finite-small-item tradeoff【X/辅助引理；作者 conjecture 的小切口】

**对象。** 非负单调子模 f，full budget B，输出成本≤ρB、比较 full-budget OPT，max cost≤δB，求显式 δ-dependent bound。P01 §6 猜 ρ=1/2 时 δ→0 达1−e^(−1/2)。

**已推进。** 标准按 marginal density 的 greedy 选到首次装不下，已得 f(S)≥[1−exp(−(ρ−δ))]OPT（见 §5 的自足证明）。因此只有“极限趋近1−e^(−1/2)”本身太容易/极可能早已是现成知识，不能包装成20天主结果。

**可留输出。** 找 tight finite-δ envelope、构造 matching lower bounds，并使它显著改进 Group GAP 实际比值；否则淘汰。**致死：** 性价比极差——证明容易而 novelty 低；value-oracle 框架的旧结果可能完整覆盖。

### C04. 保留容量修复能否改进 AGAP 的 1/19【B；作者明确方向】

**对象。** 在 P02 AGAP 中，每 bin 对每组至多一个 item；保留统一容量、每组≤m/2，并先考虑尺寸≤1/3、或组内相同尺寸的混合类。寻求 >1/19 的 explicit guarantee，不追全一般情形最优。

**原文/界。** P01 §6 最后一段明确建议 reserved capacity 用于 AGAP；P02 §2 为1/(19+ε)，P02 已有 constant-bin PTAS 和 divisible-sequence PTAS，后两者不能再作新目标。

**20 天输出。** 在 group-preserving ST slots 或 exchange graph 上给同时处理同组互斥和 overflow 的修复引理；搭出一个有限、可算的提升。**价值：** 一个新 rounding lemma 能被其他 group allocation 调用。**致死：** P01 的“移走再填”可能把同组物品放进同一 bin；只换常数、未解决该冲突不成立。

### C05. 等 opening costs 的 GBAP 获得1−1/e【X；已被通用工具覆盖的诱人伪新题】

**对象。** P03、所有 c_l=c、最多 k 个 open bins；局部可行 family 由 interval capacity 定义。目标曾考虑给 >1/8 或1−1/e rounding。

**去重。** P09 Theorem 1.3 与 §4.2 已含 bins 上 uniform matroid/任意 matroid，且同段覆盖 SAP；因此等 opening costs 理论比值提升不能声称是新 idea。P10 Theorem1.5 又覆盖快 SAP（不过是否自动覆盖外层 cardinality 约束需另核，不能偷加）。

**真实可做物。** 作为 baseline 实现支持集上的配置 max-coverage pipage rounding，并与独立抽样/丢弃对比；可给研究主线提供实验和 counterexample，单独论文价值不足。**致死：** 指数配置和 pricing 不是免费；当局部 oracle 从1降至α，1−1/e也必须随之变化。

### C06. 非均匀 opening costs 的 GBAP：联合耦合与简单算法的真实界【A；作者明确问题 + 新切口】

**对象。** 使用 P03 Eq.(1.4) 的给定稀疏 fractional support，opening costs 任意、全局 budget 必须每次满足、local configurations down-closed。研究不依赖指数配置枚举、不靠一般多重约束 continuous greedy 的显式 rounding。第一阶段只针对两种 opening costs、每 item 最多出现在两个 bins 的支持，但目标是找 coupling invariant，之后扩到一般 costs。

**原文/已知。** P03 Theorems5.2/5.4：k=B/max c_l，k<3 为1/8；k≥3 为((k−1)/(2k)) · (1−1/√k)。§7 要求改进 Algorithm1 分析，或找新算法。该值不是“所有理论方法的最优”，只是这篇算法的界。

**20 天输出。** 二种成本 toy 的 exact worst-case bound+matching obstruction；或一个联合budget/item-contention rounding lemma，严格优于把两个保留概率相乘的分析，并给支持大小多项式的实现。需要分清 approximation to input LP、approximation to OPT、运行时间三件事。

**价值判断。** 组合工具题要看是否消除一个真实乘法损失、能否超出一个小参数族；不因从1/8变1/7就自动高价值。**致死：** 现有 matroid+knapsack 次模定理可能给更强多项式比值，只有“更简单/更快/更可算且有具体量化”才剩余；不得把隐式 oracle 复杂度藏掉。

### C07. Stochastic-appearance GBAP 的两阶段 opening/recourse【B；作者明确方向】

**对象。** 独立 Bernoulli active items，已知 p_j；先选成本≤B 的 open bins，后看 activation 再 feasible assignment；目标 E[recourse profit]。先两种 opening costs、eligibility graph 为 forest/cactus、每 bin interval constraints。

**原文。** P03 §7 最后一段提出 stochastic appearing items，但未明确所有 decision timing；本候选必须把 ex ante opening 与 ex post assignment 写清。**已知界。** P03 的 deterministic rounding 不自动解决两阶段问题；DKL 2026 stochastic assignment sparsifiers 由 root 另查，可能覆盖大半，不能宣称“首个随机 GAP”。

**20 天输出。** 对一个非机械图类证明 recourse-value 子模/近似子模或构造其失败；给 small-support nonadaptive opening approximation。**价值：** 不确定需求改变模型，若 recourse 分析形成可复用工具有价值。**致死：** 只把利润乘 p_j 会错，因为 availability 与冲突/容量非线性耦合；且可能已落入 stochastic probing/coverage 的既有模型。

### C08. 两种尺寸混合 knapsack 的 correlation gap 与 CRS【A；作者大 conjecture 的可控截面】

**精确对象。** 容量1，item sizes 取 a∈(1/2,1] 和 b∈(1/3,1/2]；任意个数、任意非负 profits、任意 x∈[0,1]^n 满足 a∑_A x_i+b∑_B x_i≤1。求 E[max{w(S):S⊆R(x),s(S)≤1}]/(w·x) 的 sharp lower bound；清楚区分 a+b≤1 与 >1 两种可行集合结构。

**原文/界。** P04 Conjecture4.2 问一般自然 knapsack LP correlation gap 是否为(1−e^(−2))/2≈0.4323。§4.2 给仅大物品的0.4323、仅≤1/2物品的4/9 monotone CRS、一般0.279。P04 是2020 thesis，须补查2020–2026的后续结果。

**20 天输出。** 先 a+b>1 时的“一个大或两个小”族，证明两类内 worst weights 可统一/或给反例，再降到二维 Poisson/Binomial extremal problem；获得 sharp envelope 或 >0.279 的可构造 monotone CRS。可以先做一个固定有理数区间的完整定理，随后把界写成 a,b 的结构性分类。

**价值判断。** 新工具题要求说清“混合类耦合”到底比随机挑一个类好在哪里，并有构造与上界；仅固定 a,b 做大规模数值不够。**致死：** uniformization 在 matroids 中成立不意味着此处成立；不能拿 integral knapsack polytope 的 x 去替换 natural LP。若后续已有0.4323一般定理，则整个候选淘汰。

### C09. Sergeev Conjecture4.1 的 Binomial–Poisson 极值不等式【C/辅助；作者明确 conjecture】

**对象。** G(k,n,λ)=E[min(Bin(n,λ/n),k)]/λ，F(k,λ)=E[min(Pois(λ),k)]/λ。证明其 n、λ、k 的指定单调性，并回填 class-k knapsack correlation gap F(k,k+1)。

**原文。** P04 PDF p.24 Conjecture4.1(3)–(6) 是准确量词；Theorem4.1 只给统一0.4323。**20 天输出。** 完整证明至少一个当前未证、确实加强 knapsack 下界的子式；先用 convex order 核查是否被 Hoeffding/binomial thinning 的旧定理一行推出。**价值：** 只有它打开新 rounding/CRS 才够。**致死：** 可能是公开但过于初等的技术疑问；不能把论文暂未写证当成学界难题。

### C10. Graphic matroid 的2-sum结构能否给强 correlation gap【B；作者明确类问题 + 新 idea】

**对象。** 先 cactus 图，再 series-parallel 图的 graphic matroids；任意 x∈matroid polytope、任意 weighted rank。求统一 constant β>1−1/e，并试 sharp constant。目标通过2-sum/串并联分解建立 recurrence，不能只给treewidth当黑箱参数。

**原文/界。** P05 Theorem1.3 可降 unweighted rank；§7 问 special classes；Theorem1.5 的 rank/girth 在大秩下改善很小。cactus 的 cycle matroid 是 direct sum of uniform cycle matroids，可作已知直接推论 baseline，不可当主新定理。

**20 天输出。** 对单次2-sum证明可组合的 gap inequality，或给出series-parallel反例排除一个自然常数；再看是否能推出类别改进。**价值：** 直接解释哪种局部交换 structure 控制 correlation，而非机械限制 rank。**致死：** 2-sum 的 x-marginals 耦合可能破坏逐块独立；一般 graphic correlations 可能已有专门研究，必须补查。

### C11. MBA 的 graph-rounding 扩展到稀疏大物品超图【B；作者明确迁移方向 + 新类】

**对象。** 预算归一，configuration 每个 player 至多一个“big” item（价值>预算的一半）；把 big-item eligibility 从 graph 扩到 linear、Berge-acyclic/单圈的3-uniform hypergraph，保留非统一价格。求 configuration LP >3/4 的明确 rounding，或说明哪种3-way conflict恰好造成graph证明失效。

**来源/界。** P06 Theorem1 graphMBA为3/4+c；§7同时解除 many-players/nonuniform-prices 是作者open，明确点名 GAP迁移。此候选只是受控截面，不宣称解决一般MBA。

**20 天输出。** 一个正的相关/负相关coupling lemma和能跑的rounding；小超图exact LP gaps作证据。**价值：** 若按禁型/交换结构扩类，高于只把eligibility degree2改3。**致死：** acyclic incidence可能本来可DP/FPTAS；若去掉超图循环就只剩已知精确算法，近似题没价值；一般MBA的3/4突破仍是大坑。

### C12. SGAP 的“少数尺寸原型”与跨 bin 次模交互【C；作者 conjecture 的新截面】

**对象。** P08 的 SGAP，f 定义在(item,bin)对上；size vector 有两个原型/两条资源射线，或profit effect只依赖bin-type。求1−1/e−ε而非全SGAP1−1/e。必须允许跨bin的真实次模效应，不能退化成SMKP。

**原文/界。** P08 Conclusion p.19 明确 conjecture SGAP1−1/e；SMKP1−1/e−ε已得；non-monotone SMKP另文已处理。**20 天输出。** 验证block/fractional grouping在两原型交互处为何坏，给替代coupling；先构造一条含真正交叉效应的测试族。**价值：** 提升工具适用性。**致死：** assignment-pair上的matroid+多knapsack CRS可能早已覆盖；“低秩”如果只是换元不算有研究贡献。

### C13. Random-order GAP 的 one-overflow修复可否按结构减少1/2损失【C；最新文章的工具截面】

**对象。** P11算法先产生one-overflow preliminary assignment，最后online可实现地选last或rest；寻找利润—尺寸兼容性或有限overlap下的state-dependent coupling，改善修复因子，且整体competitive ratio超过该类既知算法。

**界/位置。** P11 §1.1及相关theorem现有general bound=(1−ln2)/2，不能仍引用旧1/6.99；fractional singleknapsack1/e已tight。**20 天输出。** 先给算法family的tightlowerexample，证明某真实结构允许因子>1/2；不要求改一般GAP常数。**价值：** 一件overflow是普适舍入视角。**致死：** unit-density/AdWords已有更强专用结果；只改善一个本来很差算法在简单特例的界，没有选题价值。

### C14. Divisible FEF与Pareto的兼容性：从二资源可交换类入手【B；作者明确open】

**对象。** P07 generalized assignment capacities、additive utilities，fairness比较agent可行子集（含charity）；问是否存在同时FEF与相对全feasible allocations Pareto efficient的fractional allocation。先两agents或agent-independent resource proportions，再尝试一条genuinely nonproportional容量方向。

**原文/界。** P07 §5明确问Weller定理analog；Theorem1有FEF但未保证PO。**20 天输出。** 一个最小反例（如果一般命题假）或一个精确自然类的存在+算法证明；记录Pareto对谁、charity是否算agent、零size/零value处理。**价值：** 明确大佬问题且可从smallpolytope得到决定性答案。**致死：** 经典competitive-equilibrium theorem可能已覆盖限域；PO提升可能破坏对charity的FEF，不能只做envy-cycle elimination。

### C15. Matroid约束下精确FEFx的strongly-poly算法边界【B/C；作者明确open】

**对象。** 每agent各自matroid、additive rationalweights，允许charity；准确P07 FEFx要求对任何严格feasible subset都不envy。先partition/laminar、两层laminar、valuations only two levels，要求迭代次数对数值大小无关。

**原文/界。** P07 §4.2 Remark1已有pseudo-poly和FPTAS；§5问exact polynomial。**20 天输出。** 证明minimal-envied-set改进过程存在combinatorial势函数，或给原算法exponentialtrajectory反例并提出正确子类。**价值：** 优化算法和公平分配直接交叉。**致死：** 一般精确问题可能和unconstrained EFX难点耦合；仅binaryvalues自动数值有界的多项式性是旧pseudo-poly的直接推论，不能当贡献。

## 3. 第二轮建议与止损机制

| 排名 | 题目 | 第1–2天的硬检查 | 第3–7天的可见证据 | 第8天停止条件 |
|---|---|---|---|---|
| 1 | C08 两尺寸knapsack correlation gap | 查2020–2026是否已有general0.4323；分别fixed(a,b)与uniform-in(a,b)量词；natural vs integral polytope分开 | 两类对称化正确与否的exact small-instance证据；一个有理参数区间的lower+upper lemma | 若只能靠random-grid数值、无法消去权值/维度，降级 |
| 2 | C06 非均匀openingcost联合舍入 | 查matroid+knapsack通用覆盖；明确输出是simple/practical bound而非首个polynomial常数 | 给support≤10的exact exhaustive adversarialtoy；得到一个不再乘两次损失的coupling inequality | 若理论比值被现成算法严格支配且时间无优势，淘汰 |
| 3 | C01 向量LP子模恢复类 | 查weightedrank/substitutes/polymatroid的现成classification；把所有w,b量词写严 | 最小禁型库、一个nontrivial positive family、识别过程 | 若正类仅rankone换元或已知matroidrank，换题 |

C02/C04适合第二梯队，不建议同时主攻，因两者共用packing repair难点。C14应交给fairness子研究者合并检查；C10可作为优化理论方向备用。第一周所有成功声明必须带“定理陈述+证明草稿+明确输入输出”，不是散点实验。

## 4. 已完成：consecutive-ones向量LP的精确反例

一个bin有两个resource positions，容量均1。三件物品a,b,c的resource列分别为(1,1)、(1,0)、(0,1)，profit均1。所有列都有consecutiveones，矩阵也全幺模。定义

φ(S)=max{x_a+x_b+x_c: x_a+x_b≤1, x_a+x_c≤1, 0≤x_i≤1_{i∈S}}。

精确值为：φ(∅)=0，三个singleton均1；φ({a,b})=φ({a,c})=1；φ({b,c})=φ({a,b,c})=2。故

φ({a,b})+φ({a,c})=2 < 3=φ({a})+φ({a,b,c})。

**证明不需要solver。** 前两项分别被第一、第二resource约束直接上界为1，取a=1达到；all-items令b=c=1、a=0得到2，而x_b≤1−x_a与x_c≤1−x_a给总利润≤2−x_a≤2。因此是exactcertificate。Python用Fraction枚举所有8个启用集的顶点，和手证完全一致。

进一步，对于ε∈[0,1)，把b,c改为(1,ε)、(ε,1)，仍有两个pair值1；all-items的最优值为2/(1+ε)，取b=c=1/(1+ε)。将两资源不等式相加给2x_a+(1+ε)(x_b+x_c)≤2，故总利润≤2/(1+ε)。子模defect=(1−ε)/(1+ε)>0。ε→1说明任意接近共同资源射线都不保证exactsubmodularity；可研究的是quantitativeapproximate性质。

这不等于“GAP fractionalLP不子模”。GAP每个assignmentedge只消耗一个bin的scalarcapacity，另有item-simplex；本反例是一个item同时消耗多个resource，模型不同。我们也对若干3×2、4×2scalarGAP随机矩阵做过失败搜索，未找到counterexample，但这种未发现不构成任何定理，不能写成positive结果。

## 5. 已完成：小物品reserved-capacity的greedy引理

设f(∅)=0单调子模，fullbudgetB下最优集合O，cost(e)≤δB；ρ>δ。greedy每步挑全地集剩余物品中marginaldensity最大的e；若加入后成本将>ρB则停止，返回当前S。未停止前总成本为C。

每一步，由子模性和cost(O)≤B，

f(O)−f(S)≤Σ_{e∈O\S}f(e|S)≤B·max_e f(e|S)/cost(e)。

所以加入e后剩余gap至多乘(1−cost(e)/B)。连乘并用1−t≤e^(−t)，得到f(S)≥(1−e^(−C/B))f(O)。若因下一件不能加入而停止，则C>ρB−cost(e)≥(ρ−δ)B；若地集耗尽则已最优。由此

f(S)≥[1−e^(−(ρ−δ))]OPT。

ρ=1/2时已经给P01 §6猜想的极限值。零成本元素先全加入；如f(∅)>0，先减去常数再加回。本引理是标准greedyanalysis在reservedbudget上的直接用法，**不宣称新颖**。它的作用是淘汰“只证明极限”这种过小选题，并提示应追tightfinite-δ或group-rounding环节。

## 6. 复查与复现

- `python reselection_gap/experiments/exact_vector_lp.py`：无第三方依赖，exactrational枚举；输出`experiments/exact_vector_lp_results.json`。
- [浮点探索脚本](../probes/vector_capacity/search_lp_submodularity.py)：原始浮点探索工具，单scalarGAP未找到反例，不作为positiveevidence；需要scipy。
- [配置归约与 oracle 边界](../notes/configuration_reduction_boundary.md)：归约与oracle边界；第二轮可独立审查。
- 原子研究者交稿时未改共享仓库；现由主研究者汇集保存。

### 检索边界

对GroupGAP/reservedcapacity、SergeevknapsackCRS、FEFxmatroid等做了2025/2026和exact-title交叉检索，未检索出明确解决文献，但检索不能证明问题仍open。MatroidFEFx和fairnesswelfare须由fairness分工做第二轮核查。特别地，2026搜索中出现“Nearly tight bounds on the price of fairness for indivisible items under budget constraints”，primary全文未成功打开，本轮不据其摘要认定C14/C15解决或未解决，也不另列welfareprice题以避免过期。
