# 单 context 密度不能只由流结构相加：精确 policy 诊断

2026-10-24，inventory8。只攻击下列**纯流结构候选**：加强初始化的每条原客户边容量、客户库存≤1、严格角色 DAG 与客户保持 raw 正边核，是否已经推出同一实际角色全部 context 的客户密度和≤1？答案是否定的。

这不是真 SPE 辅助命题反例，也不是 Q-CAG-HALF 反例。下面完整确定性 policy 明确不是 SPE，只否定把 [单 context 密度界](source_preserving_density_envelope.md)不加新激励理由便相加的步骤。

## 精确 policy 与流

角色0至3，目录 a={x}、b=空集。所有历史默认规定 b，仅 history a、ba、aab、bba 规定 a。这完全指定深度4策略，actual为bbbb。源角色0强制a的真实叶为aaba；role1 context a 的actual-reset为baab，role2 context ba 的actual-reset为bbaa。role3两个a-prescribed contexts aab、bba 的reset均为bbba。

给x一单位，在初始aaba的三个coverer之间均分：初始current=1/3，role1、role3各得1/3，每条future边恰满足p/cW=1/3。raw客户保持核的精确流为：

| context | incoming h | leaf x-load | density f | current | positive future |
|---|---:|---:|---:|---:|---|
| a | 1/3 | 3 | 1 | 1/6 | role2: 1/6 |
| ba | 1/6 | 2 | 1/3 | 1/12 | role3: 1/12 |
| aab | 1/3 | 3 | 1 | 1/3 | 无 |
| bba | 1/12 | 2 | 1/6 | 1/12 | 无 |

同一role3、同一prescribed action a的密度和为7/6>1；每个非实际context单独仍有f≤1，全部源质量含初始current精确守恒为1。机制是初始leaf已在role3覆盖x，第一次reset移除该coverer，第二次又加回。raw正边没有用第一次reset的负项取消初始role3请求。

## 准确限制

actual bbbb所有利润为0，a偏离有正利润，所以该policy非SPE。本例不否定结合全部SPE激励也许成立的聚合界，只表明聚合不是库存、正边支持与严格DAG的推论。

role3 current合计5/12≤actual-prefix a查询利润1，故本例没有否定更弱的“同角色同query action的全部current由一条wholeIC共同支付”。负项退款可能支付密度重入的额外部分。NET/CLIP可能删除本例传播；没有声称对所有允许路由失败。

[精确脚本](attack_role_density.py)完全补全该policy，以Fraction重算4个非零context、源总守恒、单节点f≤1及7/6聚合；[输出](role_density_counter.json)。没有搜索新SPE，没有固定人数正面扩展。
