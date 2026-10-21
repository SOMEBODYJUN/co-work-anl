# 失败路线入口：一般顺序半覆盖

当前目标 **Q-CAG-HALF**，存档 **customer-attraction**，仍OPEN。失败记录要说明尝试的机制、具体失效步骤、反例覆盖范围及留下的可复用信息，不能只写“此路不通”。

| 机制 | 为什么失败、留下什么 | 自足入口 |
| --- | --- | --- |
| 把SPE终局当作静态Nash | 后继会响应早期偏离；终局可以有静态改善。保留真实全历史偏离比较 | [续局失败桥](research/current/customer_attraction/continuation_lemmas.md) |
| 逐人安全值/末位保底推广到所有人 | 有完整SPE违反逐人保证；聚合桥须单独证明 | [逐人安全值反例](research/current/customer_attraction/individual_security_counterexample.md)、[末位聚合反例](research/current/customer_attraction/aggregate_theta_counterexample.md) |
| 每一步或每个前缀余额非负 | 合法SPE可以先亏后补；局部失败不否定全局补偿 | [全局债务与局部反例](research/current/customer_attraction/security_chain_and_local_boundary.md) |
| 根总税、最优主题匹配收费 | 真实完整策略已经击穿具体收费；更弱全局覆盖未被反驳 | [根总税反例](research/current/customer_attraction/root_tax_counterexample.md)、[匹配收费反例](research/current/customer_attraction/portfolio_matching_counterexample.md) |
| 固定必要条件LP的坏点 | 点可能没有真实可补全SPE；只能否定该证书模板 | [五人索引模板边界](research/current/customer_attraction/five_player_indexed_bound.md) |

完整分类、触发重试条件与原始证据见[本题失败地图](research/customer_attraction/FAILED_ROUTES.md)和[全部资产索引](research/current/customer_attraction/README.md)。数学路线可以自由改变；已有失败不是方法白名单。

其他模型保留其独立失败账本：[调度](research/unrelated_machines/FAILED_ROUTES.md)、[拥塞](research/weighted_congestion_frontier/FAILED_ROUTES.md)。旧角色与旧主攻入口的历史字节见[本次清理记录](research/customer_attraction/CURATION.md)，不作为当前指令。
