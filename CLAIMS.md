# 精确命题入口

新主攻 `UM-TARGET-v1` 、阶段边界 `UM-LONG-PATH-GAP-v1`、`UM-COALITION-PROJECTION-GAP-v1`、`UM-TREE-MARKOV-COMPLETION-NO-v1` 及经典工具 `UM-ST-ROUND-v1`、`UM-CONF-GAP-v1` 见[不相关并行机精确账本](research/unrelated_machines/CLAIMS.md)。主目标仍OPEN；另有`UM-HEAVY-MATCH-FILTER-v1`、`UM-SIMPLE-SUPPORT-GAP-v1`与`UM-ESCAPE-MATCH-GAP-v1`的限范围安全过滤和方法反例，均非主目标近似算法；既有结果重构不升级为新算法。
本页是目录，不以摘要替代量词。每项现行命题的精确范围、依赖和五轴审查状态分别在 [research/current/claims.md](research/current/claims.md) 与 [research/review_status.json](research/review_status.json)。改变对象、假设、量词、成本或结论必须创建新版本。

| 研究线 | Exact Statement 的权威位置 | 当前前沿 |
| --- | --- | --- |
| 加权拥塞 WC-TARGET v1 | [MODEL](research/weighted_congestion_frontier/MODEL.md)、[精确账本](research/weighted_congestion_frontier/CLAIMS.md)、[现行证明](research/current/weighted_congestion/README.md) | 每d≥2^20无(d/10)-PNE的全状态族，严格否定Cd/ln d保证；增长阶Θ(d)，最优常数/有限d值未定 |
| 双设施共同/异构目录 | [逐命题登记](research/current/claims.md)、[共同目录](research/current/shared/README.md)、[异构目录](research/current/heterogeneous/README.md) | 共同目录尖锐界、稀疏异构与复杂度结果各有精确输入类；一般异构 2 保留候选 |
| 任意设施数 | [一般因子 2](research/current/multi_facility/uniform_two.md)、[改善过程](research/current/multi_facility/greedy_box_global_progress.md)、[高效构造义务](research/questions/greedy_box_polytime.md) | 存在性/有限构造已内部证明；一般位多项式构造 OPEN |
| 顺序客户吸引 | [分支精确地图](research/current/customer_attraction/README.md)与全仓逐命题登记 | 一般半覆盖 OPEN；子类上界和辅助桥反例分别保存 |


本次四个新精确身份为`WC-HEALTHY-LINEAR-SWEEP-v1`、`WC-HEALTHY-FRONT-COVERAGE-v1`、`WC-LINEAR-DEGREE-ALLSTATE-NONEXISTENCE-v1`、`WC-MATCHING-LOG-UPPER-NEGATIVE-v1`；各自量词、依赖、边界和完整证据链见[主题账本](research/weighted_congestion_frontier/CLAIMS.md)及[自足正文](research/current/weighted_congestion/linear_degree_allstate_lower_bound.md)。WC-TARGET v1原身份保留，其他结构定理/候选不因本题完成升级。
