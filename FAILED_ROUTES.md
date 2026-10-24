# 失败路线入口：一般顺序半覆盖

当前目标 **Q-CAG-HALF**，存档 **customer-attraction**，仍OPEN。失败记录要说明尝试的机制、具体失效步骤、反例覆盖范围及留下的可复用信息，不能只写“此路不通”。

| 机制 | 为什么失败、留下什么 | 自足入口 |
| --- | --- | --- |
| 即使重选最优并集，也要求全部遗漏≤W | 已有71单位客户二人完整SPE：W35，唯一最优OPT38，遗漏36>35。净差OPT−W仅3；必须保留实际在最优外的覆盖信用 | [原反例及完整策略](research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/exchange/unique_optimum_omission_obstruction.md)、[独立审查](research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/coupling/optimal_omission_independent_review.md)；是旧辅助桥失败，不是half反例 |
| 只按实际客户负载校正并要求Σf(c)≥OPT、f0=0/f1=1 | 完整无拥挤SPE已有W<OPT；任意人数族迫使统一支付f1≥3/2，高负载系数无助于这些路径 | [无拥挤全人数族](research/current/customer_attraction/collision_free_three_halves_family.md)，不反驳half |
| 进一步换成同实例最低静态CCE福利：十三客户完整SPE覆盖9，所有静态CCE期望福利≥137/15 | [完整反例](research/current/customer_attraction/worst_cce_welfare_counterexample.md)证明这种更弱静态福利支配也失败；精确最低2785/297 | 保留真正不观察查询的安全值或直接跨真实分支预算；本例不反驳半覆盖 |
| 八客户简化的静态CCE福利比较 | 四主题计数依赖完整SPE福利6，而最低静态CCE福利544/87；此失败不要求历史非匿名平局 | [较小独立见证](research/current/customer_attraction/eight_customer_cce_welfare_gap.md)，保留十三客户原版本及聚合安全值开放 |
| 把SPE终局当作静态Nash | 后继会响应早期偏离；终局可以有静态改善。保留真实全历史偏离比较 | [续局失败桥](research/current/customer_attraction/continuation_lemmas.md) |
| 比较到同实例的另一最差静态PNE | 完整SPE覆盖十五，全部静态PNE覆盖十六，替换静态均衡仍不能支付 | [静态福利比较反例](research/current/customer_attraction/worst_pne_welfare_counterexample.md) |
| 逐人安全值/末位保底推广到所有人 | 有完整SPE违反逐人保证；聚合桥须单独证明 | [逐人安全值反例](research/current/customer_attraction/individual_security_counterexample.md)、[末位聚合反例](research/current/customer_attraction/aggregate_theta_counterexample.md) |
| 每一步或每个前缀余额非负 | 合法SPE可以先亏后补；局部失败不否定全局补偿 | [全局债务与局部反例](research/current/customer_attraction/security_chain_and_local_boundary.md) |
| 根总税、最优主题匹配收费 | 真实完整策略已经击穿具体收费；更弱全局覆盖未被反驳 | [根总税反例](research/current/customer_attraction/root_tax_counterexample.md)、[匹配收费反例](research/current/customer_attraction/portfolio_matching_counterexample.md) |
| 固定必要条件LP的坏点 | 点可能没有真实可补全SPE；只能否定该证书模板 | [五人索引模板边界](research/current/customer_attraction/five_player_indexed_bound.md) |

完整分类、触发重试条件与原始证据见[本题失败地图](research/customer_attraction/FAILED_ROUTES.md)和[全部资产索引](research/current/customer_attraction/README.md)。数学路线可以自由改变；已有失败不是方法白名单。

其他模型保留其独立失败账本：[调度](research/unrelated_machines/FAILED_ROUTES.md)、[拥塞](research/weighted_congestion_frontier/FAILED_ROUTES.md)。旧角色与旧主攻入口的历史字节见[本次清理记录](research/customer_attraction/CURATION.md)，不作为当前指令。

加权拥塞结构应用的背景成本遗漏、校准NO误用、最小势福利误推和原游戏修复混淆，已分别记录失效机制与修补条件，见[专题失败账本](research/weighted_congestion_frontier/FAILED_ROUTES.md)及[独立审查](research/reviews/weighted_congestion/decision_methods_review.md)。
