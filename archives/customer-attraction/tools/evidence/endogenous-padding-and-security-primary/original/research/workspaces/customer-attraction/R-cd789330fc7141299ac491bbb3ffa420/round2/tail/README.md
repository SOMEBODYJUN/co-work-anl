# Round2/tail：分数水位化共同信用

Q-CAG-HALF、GAP-r与聚合安全值桥仍OPEN。核心引理已通过[独立盲重构与解析审查](../shared/review_waterfill.md)；[另一支锐性族定义级独审](../mixed/review_waterfill_sharpness.md)也已通过。

* [自足稿](waterfill_common_credit.md)：任意人数分数水位化，使正质量尾部unit收益≥t，同时全部合法查询返还≤原低尾deficit；精确质量加权利润守恒；真正v4与完整SPE上的常数1锐性族；最小r聚合归约和仍缺的可信桥。
* [作者定义级审计](audit_waterfill.py)与[精确输出](waterfill_exact.json)：53单位客户、400节点、2800偏离、84静态竞争背景；水位权以严格有理区间处理。它不代替别支独审。
* [构造器](build_endogenous_example.py)、[输入](endogenous_53_instance.json)、[完整有序策略](endogenous_53_strategy.json)：构造和最终核验分离。
* [静态匹配证书](endogenous_53_security.json)：真正v4的原始/对偶数据，可独立读取核算。
* [统一缩尾全树税账](uniform_shrink_full_tree_tax.md)：全历史局部regret沿原规定续局之和由一次背景返还支付；[global独审通过](../global/uniform_tax_independent_review.md)。[作者精确回归](uniform_tree_tax_exact.json)保留实际翻转；不能跨多次偏离边望远镜。
* [VAR最终独审](review_variational_final.md)：先保存[盲重构](review_variational_blind.md)，再对作者正文；核心KKT、CC、FE/JOINT、唯一性/连续性、同多重集交换和Debt恒等式均在明示范围内通过。[独立精确输出](variational_blind_exact.json)含14份KKT证书及根信用非单调导数。
* [κ0的H-only债务停界](zero_pool_switch_debt.md)：复用已有34客户真实完整SPE；所有真实分支H=0仍有严格正的虚拟交换Debt。只阻止H独自支付该接口，不反驳聚合安全值桥或half。

本轮没有固定锥阴性扩样。当前一般缺口是跨真实孩子的共同支付：统一缩尾税仅在规定边共享终局，VAR的严格上升仅在同一单位多重集成立；换到真实子树时税表、单位基线和支撑都可能重置。H独自支付已在κ0失败，尚需把真实高尾剩余利润/激励松弛与静态minimax按一次预算耦合。没有闭合这个接口，不把辅助分数profile误称单位玩家SPE，也不重复花掉原尾利润。本轮到此收束。
