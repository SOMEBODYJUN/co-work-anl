# 选题与数学身份账本

本轮尚无一般性新定理被提升为可靠结果。候选精确陈述保留在候选池和各线原始卡片；A/B/C标记只说明问题来源，不代表数学真值或难度。

当前[统一候选池](candidate_pool.json)含AT01–AT14、NA01–NA06、FA01–FA20、GA01–GA19，共59条记录，含被覆盖、合并和已闭合子题。来源和状态由[BATTLE](BATTLE.md)共同解释。第一轮稿的内部字母不是统一来源标记。

## 第二轮新增的精确数学身份

以下均有自足正文，并经[root独立复核](notes/round2_independent_root_review.md)；除明确标为已有覆盖者外，新颖性尚未认证。内部正确性证据与能否独立成稿分开记录。

| ID/version | Exact Statement / Domain / Quantifiers | Dependencies / Evidence / Scope / Status |
| --- | --- | --- |
| SEL-RESOURCE-LP-SUBMODULAR-v2 | 固定非负2×n矩阵A；对所有b,w≥0，启用集LP值子模 iff 非零列≤2正比例射线 | [二维完整证明](notes/two_resource_lp_submodularity.md)；LP dual、min/max与三列反例。全容量/全利润分类，不是固定b刻画；内部证明完成/新颖性未知 |
| SEL-RESOURCE-LP-SUBMODULAR-v3 | 任意d×n非负A，非零列≤2射线时，对所有b,w≥0启用LP归一单调子模 | [全维充分性](notes/two_profile_lp_in_arbitrary_dimension.md)；互补系数分裂原对偶保持和。v2充分方向推广，**不声称高维必要性**；内部证明完成/新颖性未知 |
| FP-COUNTER-BALANCE-v1 | 5顶点、k=1的整数对称多重图有EF方向，但强制普通内部平行包全平分后不可行 | [重边正文§1](notes/heavy_edge_residual_and_charity.md)；全部可见价值精确反算。仅否定指定压缩，不否定一般FPT；完整反例 |
| FP-FOREST-THRESHOLD-v1 | 任意非负整数s,h与二进制单位包重数；unit简单支持forest时，完整EF残差可在poly(bits)内判定并输出计数方向 | [重边正文§2](notes/heavy_edge_residual_and_charity.md)；向上阈值消息、4200整数oracle核程序。推出受限2^k，非一般multigraph；内部证明完成/新颖性未知 |
| FP-CHARITY-SIMPLE-v1 | 任意simple loopless endpoint整数估值图，k-heavy、非负二进制删除cost；最优EF partial orientation可3^k poly(bits)构造 | [重边正文§3](notes/heavy_edge_residual_and_charity.md)；补全lemma、无锚点树、quota flow，1200完整oracle。simple承重；成本版本靠证明而非实验；内部证明完成/新颖性未知 |
| BN-CLONE-v1 | 对u=min_R a_r·δ及非负有理A，所有D/等预算clones/外部环境/每个NE的合并保持性可2^R poly(m,R,bits)识别 | [几何与算法§5](notes/budget_cloning_and_concave_geometry.md)；shared supergradient、active-cell LP、严格margin、压缩等预算反例；内部证明完成/新颖性未知 |
| BN-CLONE-v2 | 同一矩阵语言的补语言有polybit有理/超梯度/Farkas证书，因此CLONE-INVARIANT在coNP | [证书正文](notes/budget_cloning_complexity_certificate.md)；rational LP与Hadamard；未给hardness/complete；内部证明完成/新颖性未知 |
| SEL-FINITE-WEIGHT-ENVELOPE-v2 | 任意有限人数和策略、weights={1,2}、非负二次多项式延迟；type-scaled资源势可达64/59 | [全人数证明](notes/finite_weight_scaled_potential.md)；共享类型缩放、61206条Fraction核验。改变v1缩放/人口范围，另立v2；不保证poly步数/最佳比；旧工具来源明确 |
| SEL-KNAPSACK-FIXED-X-OBSTRUCTION-v1 | 指定两尺寸5物品、固定独立激活概率x，非均类权重ratio严格低于所有类内统一权重，允许零权sub-support | [连续权比断点与Fraction证书](notes/two_size_knapsack_obstructions.md)；不否定可改变x的全局归约，不否定一般CRS猜想；完整方法反例/新颖性未知 |
| NE-FISHER-TRANSFER-v1 | 同一非负有理v与预算b，public Leontief的NE支出矩阵等于private linear Fisher的均衡spending矩阵 | [自足两向归约与来源](notes/leontief_fisher_known_interface.md)；Brandt、Tao–Zheng、Orlin已覆盖；**已知工具重构，NA02新算法题淘汰** |

一般heavy-multigraph FPT、cloning一般R的tight complexity、GA01到实际GAP新近似的桥仍未解决。共同光滑凹偏好的log-gradient规划只是标准KKT地基，详见同一几何正文；不另包装主成果。

## SEL-FINITE-WEIGHT-ENVELOPE-v1

对象：weights={1,2}且各类型至多2人、任意有限策略族、非负系数二次多项式延迟。结论：以真实权重作为玩家缩放的单资源边际夹逼可达37/33，且这个指定模板内最优。证据：12条边的Fraction证书、两条到达(2,1)的路径下界。范围：有限人口但任意策略；不是最优PNE存在阈值，不给多项式改善步数。第二轮自由类型缩放已有全人数64/59草案，故37/33仅保留模板边界价值。定义、证明与异议见[原子卡](lanes/atomic.md)；Status=内部可核验证书/新颖性未定。

## SEL-VECTOR-LP-SUBMODULAR-OBSTRUCTION-v1

对象：一个bin、两个单位容量、三物品列(1,1),(1,0),(0,1)、利润均1，启用集S的分数LP值。结论：φ(ab)+φ(ac)=2<3=φ(a)+φ(abc)。8集值由手证及Fraction顶点枚举确定，另有正向量连续扰动版。Scope：向量容量，不是scalarGAP；Status=方法边界toy，新颖性未确认。见[GAP卡§4](lanes/gap.md)及[程序](probes/vector_capacity/exact_vector_lp.py)。

每个进入试攻的候选须记录：ID/version、Exact Statement、Objects、Domain、Quantifiers、Assumptions、Definitions、Scope、Conclusion、Dependencies、Evidence、Counterevidence/Objections、Status、Related Files。

文献本身证明的结果为Paper Fact；工具含义为Interpretation；新问题/猜想为Hypothesis；有限实验为Observation/Evidence；状态提升需自足证明并核查实质异议。探索和准确标级的候选保存无需等待审查。

## CS-THETA-EXACT-v1

身份：B作者建议自然类细化 → C团队等长theta派生题。精确对象、全量词、公式、定义、依赖、证据、异议与结果文件均在[自足证明候选](notes/combinatorial_equal_theta_correlation.md)。Status=proof candidate；不是可靠新定理，新颖性未确认。原文Thm4.3的support-tight结论与全图base结论严格区分。

## SEL-FAIR-FPO-PROBE-v1

精确对象、WEFX和fPO定义、量词范围、两份原文的关系、独立oracle、边界输入、证据及未决新颖性见[兼容边界探针](notes/fair_fpo_compatibility_boundary.md)。Status=已知反例复现/有限Observation，非新定理；新分类题尚未锁定。无条件personalized bivalued WEFX+fPO存在版本受已知反例阻断。

## SEL-CHORES-TRIVALUED-AUDIT-v1

[三类chores反例与有限近似边界](notes/chores_trivalued_exact_boundary.md)固定四代理/三类型/完全分配/同权/可加成本及α-EFX定义。Status=已知反例复现与有限精确Observation；完整枚举不升级一般定理。原参数的固定例最优α为23/22，±1邻域并非单调；代码、输入、独立小例oracle和反算见正文。

## SEL-MATROID-EXCHANGE-DISTANCE-v1

[公共基交换图围长距离界](notes/matroid_exchange_distance_and_girth.md)固定全部有限拟阵、公共基profile与完整可行单交换图，候选结论dist≤rank−girth+3。已有完整证明草案、statement-first独立重构及全小抽象拟阵审计；Status=proof candidate，新颖性及全部PoA应用合同未闭合。对应Hao–Michini明确猜想的端点指数候选由2δ+2改善到δ+2；不是UM算法或一般已认证新定理。

## SEL-LAMINAR4-KEY-v1：boss0有限核探针

沿用[已有精确A类问题](notes/source_frontier_checks.md)，新增[有限枚举与顺序贪心障碍](notes/boss0_laminar_key_probe.md)。Domain/quantifiers不变：全部非负可加实估值、四代理预指定顺序、两个key同时要求EF1及ordered no-envy。代码仅检验指定整数输入；所有见证的核验与一个朴素算法反例均不解决一般存在命题。Status=probe/finite Observation；下一义务是全估值证书或新构造。

## SEL-PB-EFX-MONOTONE-COMPLETION-OBSTRUCTION-v1

C类强方法合同反例；精确参数族、量词、证明、独立Fraction核查、适用范围及新颖性限制见[个性化双值的单调补全障碍](notes/personalized_bivalued_monotone_completion_obstruction.md)。它不否定EFX+普通PO存在性；未进入可靠新一般定理层。

## 题源修正，数学身份不变

[来源审计](notes/source_authority_audit.md)将FA09直接题源修正为Jin–Tao WINE2025 §5，He–Tao2026为后续转述。A是一般EFX+普通PO问题，少人数/少件/两ratio仍为C；未改量词或结论。其余题源评价不构成数学Claim状态提升。
