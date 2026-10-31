# 动态全续局L的产品转移：一般组件与精确反例

2026-10-24。研究目标仍为任意m、任意有限共同目录、每份完整有序历史纯SPE的Q-CAG-HALF，状态OPEN。这里不修改共享稿或git，不发公屏。跨组件可信平局补偿及SPE投影非SPE的机制已有[旧产品福利非可加稿](../../R-44b24f3962bd4f68a4b6913610c0d417/global_security/cartesian_efficiency_failure.md)；这里重构其一般闭包接口，不认领机制首次。

- [一般产品转移闭包及SM放大接口](product_transfer_lemma.md)：适用于任意m和任意产品组件；证明全续局L只能保证次可加，以及跨组件下一角色IC盈余可转移。给出攻击SM-opt-exists的精确放大充分条件，尚未找到满足条件的组件。
- [完整策略构造与直接审计](product_transfer_certificate.py)：十名展开单位客户、九主题、三玩家；完整91有序决策历史、819含自行动比较。不是只核强制节点。
- [完整证书](product_transfer_certificate.json)与[有理审计](product_transfer_audit.json)：严格证明L_product(BB)=5/2<3=2L_component(B)。实际根叶W=OPT=10；仅否定L可加，不反驳SM、TB或half。
- [定向产品凸化攻击代码](product_transfer_attack.py)：精确计算单步转移正则化barL。确定性检查2186个三主题三角色、各类型重数0..2的组件，没有找到所写放大充分条件；仅阴性诊断，不继续扩此规模或样本。

当前边界：产品非可加是可信续局量词的真实增量，不是一条已支付一般福利下界。下一步须用跨组件IC转移真正压低所有最优排列的L总和，或找到与产品无关的一般新预算；不能从本例推断SM失败。

独立审查：同轮`../source_reset/product_independent_review.md`、`../independent_attack/product_transfer_independent_review.md`及`../harmonic_debt/review_product_transfer.py`均从客户份额/有序历史重构通过。审查不升级为外审或福利结论。最新解析边界：同质all-big锐族的Cartesian产品、实际全Big，始终有对角最优排列的sumL=qm>q(m−1)；见正文§7，停止沿该同质产品扩样。

本轮交接：正文、完整证书、直接审计与候选攻击代码均已写完；未改共享文件或git。异质组件与更深耦合仅列为未开始的可能方向，没有对应新候选或运行。研究到此停止扫描，留给父方checkpoint和清洗。
