# 精确命题入口

新主攻 `UM-TARGET-v1` 及经典工具、长链/联合投影、树再耦合、匹配残余/共享逃逸等阶段边界见[不相关并行机精确账本](research/unrelated_machines/CLAIMS.md)。主目标仍OPEN；既有工具重构与限范围方法反例不升级为新近似算法。
另有[共同大边选择与条件块容量](research/current/unrelated_machines/joint_matching_completion_and_block_cuts.md)的条件舍入、限域精确选择NP完全和专用族强化身份，均不关闭主目标。
本页是目录，不以摘要替代量词。每项现行命题的精确范围、依赖和五轴审查状态分别在 [research/current/claims.md](research/current/claims.md) 与 [research/review_status.json](research/review_status.json)。改变对象、假设、量词、成本或结论必须创建新版本。

| 研究线 | Exact Statement 的权威位置 | 当前前沿 |
| --- | --- | --- |
| 加权拥塞 WC-TARGET v1 | [MODEL](research/weighted_congestion_frontier/MODEL.md)、[精确账本](research/weighted_congestion_frontier/CLAIMS.md)、[现行证明](research/current/weighted_congestion/README.md) | 每d≥2^20无(d/10)-PNE的全状态族，严格否定Cd/ln d保证；增长阶Θ(d)，最优常数/有限d值未定 |
| 双设施共同/异构目录 | [逐命题登记](research/current/claims.md)、[共同目录](research/current/shared/README.md)、[异构目录](research/current/heterogeneous/README.md) | 共同目录尖锐界、稀疏异构与复杂度结果各有精确输入类；一般异构 2 保留候选 |
| 任意设施数 | [一般因子 2](research/current/multi_facility/uniform_two.md)、[改善过程](research/current/multi_facility/greedy_box_global_progress.md)、[高效构造义务](research/questions/greedy_box_polytime.md) | 存在性/有限构造已内部证明；一般位多项式构造 OPEN |
| 顺序客户吸引 | [分支精确地图](research/current/customer_attraction/README.md)与全仓逐命题登记 | 一般半覆盖 OPEN；子类上界和辅助桥反例分别保存 |


本次四个新精确身份为`WC-HEALTHY-LINEAR-SWEEP-v1`、`WC-HEALTHY-FRONT-COVERAGE-v1`、`WC-LINEAR-DEGREE-ALLSTATE-NONEXISTENCE-v1`、`WC-MATCHING-LOG-UPPER-NEGATIVE-v1`；各自量词、依赖、边界和完整证据链见[主题账本](research/weighted_congestion_frontier/CLAIMS.md)及[自足正文](research/current/weighted_congestion/linear_degree_allstate_lower_bound.md)。WC-TARGET v1原身份保留，其他结构定理/候选不因本题完成升级。

条件证书新增UM-HEAVY-ALTERNATIVE-FILTER-v1、UM-DILUTED-SINK-PROBE-GAP-v1、UM-BIG-CARDINALITY-PROBE-v1，分别是安全接口、准确方法边界及仅对该族的加强效果；见[精确账本](research/unrelated_machines/CLAIMS.md)。


新增UM-DILUTED-ESCAPE-PROBE-GAP-v1精确身份：共享逃逸合并后仍通过所有普通边探针与GHMR；只限该合同，依赖与同行来源见本题账本。

半单位新身份已关闭固定大小分界的共同见证窗口：每个固定δ∈[0,1/2)的(Aδ)存在性NP完全；P≠NP下无总位多项式OPT≤T承诺构造。它仍不是统一低于2算法的困难性，下一步转向实际联合舍入损失。见[共同选择正文§3a](research/current/unrelated_machines/joint_matching_completion_and_block_cuts.md)。

[全局单行基数与紧凑共享逃逸](research/current/unrelated_machines/row_count_escape_gap.md)新增安全位多项式查询及准确反例：完整任务身份/多槽/每机每配置计数延伸仍与GPC₂合用保持gap2；条件块切面仍可识别本族。UM-TARGET-v1继续OPEN；一般共同负载耦合与统一舍入未解。

新身份`UM-SPARSE-CONDITIONED-CONFIG-GAP-v1`为每任务至多三选的全边独立条件配置间隙；[精确账本](research/unrelated_machines/CLAIMS.md)固定不同查询不耦合及未覆盖预处理的范围，不升级主目标。

UM-MACHINE-CONFIG-PROBE-GAP-v1新增“∀机器∀合法完整配置∃各自完整配置LP延伸”的间隙2身份；精确范围、非必要条件警示及共同base边界见[专题账本](research/unrelated_machines/CLAIMS.md)与紧凑族正文§7。

循环批量修复新增UM-ROBUST-CYCLIC-BATCH-OPT-v1、UM-BATCH-SUPPORT-REPAIR-NO-v1、UM-FORK-MINCOST-ROUND-REPAIR-NO-v1；另以UM-COORDINATE-REPAIR-ST-GAP-v1登记与boss7真凸包槽族的守恒直接推论。[准确量词与范围](research/unrelated_machines/CLAIMS.md)区分局部构造和修复反例，未得统一近似。
