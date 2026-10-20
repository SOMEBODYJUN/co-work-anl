# 选题阶段的精确数学身份

本账本只登记本轮可复用问题与候选模块，不把选题排名升级为定理，也不改main的旧Claim。

| ID/version | Exact statement / objects / domain / quantifiers | Dependencies / evidence / objections / status / files |
| --- | --- | --- |
| TS-BMKP-2CAP-APPROX-v1 | 对所有仅两种正容量的BMKP，物品公共正有理重量、非负有理利润、可不用物品；每固定ε>0给确定性总位多项式算法输出硬容量可行且每bin利润至少(2/3−ε)OPT | 依赖原文profile结构、联合canonical、嵌套matching及discard小物品舍入；有候选证明与局部精确审计，仍缺整稿/算法级重放/新颖性核验。CANDIDATE；generalized_assignment/TWO_CAPACITY_LEMMA.md、cross_field_battle/bmkp_algorithm_review.md |
| FC-LEMMA-R2-2C-v1 | n≥1、m≥0，每i有A_i⊔B_i=M，成本为触达类别数且无loops；m≥n存在可多项式构造complete EF，m<n每人至多一件给complete EFX | Hall缺字翻转+互补pair；独立内部逐步攻击及构造核查，未外审/未认证新颖性。PROOF_DRAFT_INTERNALLY_CHECKED；fair_chores/rank2_two_classes_lemma.md。有loops或三平行类不在结论中 |
| TS-CHORES-RANK2-EFX-v1 | 任意有限n,m、个性化rank≤2 matroid的rank为成本，允许loops，求完整EFX且删除任意own item（含零边际） | 上项只覆盖两平行类无loops；true rank-cap2有限枚举不是一般证明。OPEN；fair_chores/candidate_report.md FC01 |
| TS-COPIES-3-SDEF1-v1 | 三人，类型g有1/2/3个等值副本，每人每类型至多一件；任意类型数和非负估值/序，求complete SD-EF1 | AAAI25明确公开问题的三人切片，前缀b-matching表示；有限域独立枚举，交换未闭合。OPEN；fair_goods/candidate_report.md FG02 |
| TS-LAMINAR-4-KEY-v1 | 任意指定四人次序和非负additive估值，K8/K12均存在complete feasible EF1且v_i(A_i)≥v_i(A_j) (i<j) | 母文证明两基例充分推出共同4-colorable laminar全类；连续估值全域覆盖尚缺。OPEN；fair_goods/candidate_report.md FG01 |
| TS-NASH-SPARSE-SQUARING-v2 | 构造binary cubic局部势博弈，n≥2块时degree≤6、treewidth=pathwidth=3；对ε≥2^(−2^n)且≤1/2存在扰动NE与任意原NE距离≥1/2，故不保证落入δ=1/4闭球 | 完整内部证明/图证与独立审查；原shared-t已有常数pathwidth，价值仅有限加强，新颖性未认证；TOOL_DRAFT_DEMOTED。nash_equilibria/candidate_report.md、fair_goods/nash_sparse_potential_review.md。不是求任意NE的时间下界 |

论文事实与本组推导的逐条定位在子线报告/JSON；域或结论变化必须新version。有限计算只算Evidence，不能把OPEN更新为定理。

## BMKP候选的三个独立模块

- **GA-03-L1**：固定有限联合标签、每个long所有expensive都计critical且≤K、每个short≤2件、同类型上舍入重量不变且利润在同一宽δ桶。按每类型的总critical需求全局取最重物品，可同时保long全部舍入容量/利润不等式，short重量不增、利润损失<2δ。完整假设与配对证明见候选正文。内部完整推导及独立重构，尚不认证新颖性；不是输入到这些标签的免费生成器。
- **GA-03-L2**：两容量B1≤B2、共同阈值Q>0、short数量m1,m2，每件至多一次且每包≤2物。带m1+m2个零dummy的图存在固定基数m1+m2且至少m1条small-eligible边的matching，当且仅当short可全部满足。多项式最大权matching实现该接口；此为嵌套资格的标准组合模块，不声称一般Exact Matching已解。
- **GA-03-L3**：任意有限共同非负重量/利润向量、非负容量B_j和目标t_j，若允许每物品列和≤1的分数LP可行，则存在可在总位多项式时间构造的互不交部分整数sets，逐包重量≤B_j且利润≥t_j−4pmax，其中pmax=max({0}∪{p_e})。使用BFS紧约束计数与逐包结束的自足证明；GA线、跨线和boss4分别重构了计数。保持PROOF_DRAFT_INTERNALLY_CHECKED、无外审/新颖性认证，完整通用实现尚未交付。它允许unused，不能改写成所有物品恰好覆盖。

这些模块支撑TS-BMKP-2CAP-APPROX-v1但不代替源结构引理、共同枚举和算法输出的整稿验证。相关证据与限制均在候选正文、独立审查及VERIFICATION。
