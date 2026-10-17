# 三叉树底层调色板下的两种自然放大：仅精确陈述

ID UM-TERNARY-PALETTE-TENSOR-AMPLIFICATION-OBSTRUCTION-v2。Objects/Domain：任意显式完整三叉有根树T，所有叶同深h≥1，叶带可重复binary颜色ID；每个深h−1父节点的三叶至多两种颜色。q(T)为最大整数r，使存在含root的满r叉、全叶深h且全部叶色不同的子树；总有q≥1。

给整数k≥1，定义对齐Cartesian张量T^[k]：深ell节点为原T深ell节点的有序k元组，子关系逐坐标原child关系，叶色为有序k颜色tuple且tuple相等才共色。它是d=3^k叉同高h树，不收缩层。若另给任意高度H≥1的完整d叉同深着色树U，定义普通P(U)：每个internal node一machine，每色一resource；root有单端time1 pin；每树边一不同job，parent端1/d，child为internal时下端为该child machine time1，否则下端为叶色resource time1，其余∞。

Exact Statement/Quantifiers/Conclusions：

1. ∀T,k，q(T^[k])≤2^k。若q(T)≥2，则q(T^[k])=2^k，故P(T^[k])实际OPT恰2−(2/3)^k。
2. ∀完整同深d叉U（d≥2），P(U)实际OPT=2−q(U)/d，且∀U有路径给2−1/d完整调度。特别任何符合本条件的YES树族与任意同域NO树族，经上述张量并重编P后，即使NO最强，乘性gap也至多G_k=(2−3^(−k))/(2−(2/3)^k)≤5/4；G_1=5/4，G_k严格递减且趋1。此处“YES”仅指q(T)≥2；不假设NO张量保持原NP谓词。
3. 若k≥2且k整除h，定义纯k层收缩：深tk的原节点为macro节点，原k步后代为其d=3^k个children，保留原叶颜色。则收缩树q≤2·3^(k−1)<d−1，连YES也不具有满(d−1)叉虹彩子树。
4. 现行ternary_rainbow_subtree_exact_hardness.md中两套v1/v2非退化SAT构件编译输出均满足本底层两色前提；常量分支明确规范选高1(A,B,A)为YES、(A,A,A)为NO后，上述限制适用该整个规范输出族；不声称其它改色/跨副本约束/padding/非对齐乘积也失败。

Assumptions/Dependencies：无复杂度假设；只用上述定义及指定已保存编译器的实际构造。Scope：确定操作的数学限制，非一般UM算法反证、非所有张量不可能。没有按binary k承诺poly输出大小；T^[k]须显式展开，size可约|T|^k，允许更大展开也不改所述等式。Evidence/Status：待仅陈述重构与冻结证明读后审查；未认证新颖性/论文价值，无新通用实现。Related files：既有三叉虹彩正文和审查，rooted_dag_degree_token_bridge.md的一般分叉转译。

版本差异：v1仅陈述草稿第4项把旧v1尚未明确的所有常量分支说满；作者shared指出后v2明确所选常量映射，并钉U高度≥1。原v1字节保留，不倒称已成立。
