# Round2/tail：分数水位化共同信用

Q-CAG-HALF、GAP-r与聚合安全值桥仍OPEN。核心引理已通过[独立盲重构与解析审查](../shared/review_waterfill.md)；[另一支锐性族定义级独审](../mixed/review_waterfill_sharpness.md)也已通过。

* [自足稿](waterfill_common_credit.md)：任意人数分数水位化，使正质量尾部unit收益≥t，同时全部合法查询返还≤原低尾deficit；精确质量加权利润守恒；真正v4与完整SPE上的常数1锐性族；最小r聚合归约和仍缺的可信桥。
* [作者定义级审计](audit_waterfill.py)与[精确输出](waterfill_exact.json)：53单位客户、400节点、2800偏离、84静态竞争背景；水位权以严格有理区间处理。它不代替别支独审。
* [构造器](build_endogenous_example.py)、[输入](endogenous_53_instance.json)、[完整有序策略](endogenous_53_strategy.json)：构造和最终核验分离。
* [静态匹配证书](endogenous_53_security.json)：真正v4的原始/对偶数据，可独立读取核算。

本轮没有固定锥阴性扩样。下一步应把共同查询信用带入真实孩子内部偏离形成跨根支付，不能把辅助分数profile误称单位玩家SPE，也不能重复花掉原尾利润。
