# 选题与数学身份账本

本轮尚无一般性新定理被提升为可靠结果。候选精确陈述保留在候选池和各线原始卡片；A/B/C标记只说明问题来源，不代表数学真值或难度。

当前[统一候选池](candidate_pool.json)含AT01–AT14、FA01–FA16、GA01–GA15，来源和状态由[BATTLE](BATTLE.md)共同解释。第一轮稿的内部字母不是统一来源标记。

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
