# 单根完整树的全局叶重数：精确配置gap上确界，仅陈述

ID UM-SINGLE-PINNED-TREE-MULTIPLICITY-EXACT-CONFIGURATION-GAP-v1。

Objects/Domain/Definitions：任意显式完整d叉有根树U，高h≥1，全部叶同深h，d≥2；每叶带binary颜色ID，整个U每色出现次数≤给定整数µ≥1。普通不可拆UM P(U)完整定义：每internal node一machine、每颜色一resource machine，两个namespace不交；root有单端time1 pin；每树边是一不同job，在parent machine时间1/d，若child internal则下端仅该child machine time1，否则下端仅叶颜色resource time1，其余∞。全部未选job也必须安排。q_rainbow(U)为最大的满r叉rooted rainbow同深子树分叉r。Tconf是此原P普通未强化configuration LP的最小可行T。

Exact Statement / Quantifiers / Conclusion：

1. 对全部上述U，OPT(P(U))=2−q_rainbow(U)/d，q_rainbow(U)≥ceil(d/µ)。存在确定性总位多项式算法，输出完整真实σ且Cmax≤2−ceil(d/µ)/d≤2−1/µ。µ可binary且大于实际重数，算法不按巨大µ值循环。
2. 对每个固定µ≥1，此完整单树类的普通configuration gap上确界恰为 2−1/µ；即所有U的OPT/Tconf≤2−1/µ，且对任意η>0有该类显式有限U使OPT/Tconf>2−1/µ−η。µ1时全部OPT=Tconf=1。
3. µ≥2时下确切参数族可实现：∀d≥2且µ整除d，∀整数h≥1满足 µ((d−1)/d)^h≤1，存在上述原P，其中每色实际恰µ次、q_rainbow=d/µ、OPT=2−1/µ、Tconf=1+1/d。给出完整普通CONFIG证书及全job调度证明，不只marginal load。可特别选h=d·ceil(log2µ)。d→∞的µ倍数给第2项下界。所有输入/证书若展开，size按真实d^h计；不按binary(d,h)承诺poly展开。

Assumptions：无复杂度假设。Dependencies：上述原P定义、已有raw q对子集并的子可加/阈值DP；完整自足证明可重建。Scope：single forced root、uniform d、global whole-input色重数；不同于多roots/multiple selector states的private-forest一般G(µ)，不改其未知固定µ精确值。该family可直接求解，非NP-hardness；µ随输入无界时此界不提供统一epsilon。无一般UM正反面升级。

Evidence/Counterevidence/Status：待陈述先行独立审查及冻结证明读后攻击，无新通用实现/有限运行或外审/新颖性认证。Related Files：private_injective_tree_configuration_floor.md、ternary_rainbow_subtree_exact_hardness.md、private_tree_branching_valuation_and_minorants.md；独立claim不能把finite族校验当一般证明。
