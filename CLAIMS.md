# 精确命题入口

本页是目录，不以摘要替代量词。每项现行命题的精确范围、依赖和五轴审查状态分别在 [research/current/claims.md](research/current/claims.md) 与 [research/review_status.json](research/review_status.json)。改变对象、假设、量词、成本或结论必须创建新版本。

| 研究线 | Exact Statement 的权威位置 | 当前前沿 |
| --- | --- | --- |
| 加权拥塞 WC-TARGET v1 | [MODEL](research/weighted_congestion_frontier/MODEL.md)、[精确账本](research/weighted_congestion_frontier/CLAIMS.md)、[现行证明](research/current/weighted_congestion/README.md) | 奇环下界 T_d∼d/ln d；全类普遍上界仍为已核实文献 d。目标 OPEN |
| 双设施共同/异构目录 | [逐命题登记](research/current/claims.md)、[共同目录](research/current/shared/README.md)、[异构目录](research/current/heterogeneous/README.md) | 共同目录尖锐界、稀疏异构与复杂度结果各有精确输入类；一般异构 2 保留候选 |
| 任意设施数 | [一般因子 2](research/current/multi_facility/uniform_two.md)、[改善过程](research/current/multi_facility/greedy_box_global_progress.md)、[高效构造义务](research/questions/greedy_box_polytime.md) | 存在性/有限构造已内部证明；一般位多项式构造 OPEN |
| 顺序客户吸引 | [分支精确地图](research/current/customer_attraction/README.md)与全仓逐命题登记 | 一般半覆盖 OPEN；子类上界和辅助桥反例分别保存 |

Paper Fact、解释、猜想、观察、计算证据和内部可用记录必须分开。完整证明、独立审查、软件状态、外部审查和新颖性各自记录。尚成立的致命 objection 阻止升级。

跨主题的 `PK-INTERACTION-RANK-FACE-v1`、`PK-SHARP-FORBIDDEN-MASS-v1` 与 `PK-OCCUPANCY-CONE-CLOSURE-v1` 见[正占用核接口](research/current/positive_kernels/occupancy_rank_faces.md)和全仓精确账本。三项分别为表示过滤、锐单核预算与闭包定理，不是WC全类存在界。

[统一低泄漏锚定时钟预算的普适次数障碍](research/current/weighted_congestion/uniform_clock_budget_barrier.md)为新增限定方法命题；精确ID与全部量词在主题账本，不改变WC-TARGET身份。

[有限次局部成本与择证矩接口](research/current/weighted_congestion/template_certificates/selector_local_moments.md)登记保全部成本的D维压缩、小支撑dual及完全暂态parity机制；[循环窗口前沿商](research/current/weighted_congestion/class_front_phase_quotient.md)另登记精确表示与不同步出口反例。具体量词及假设修复只由主题账本和审查给出，均不升级WC-TARGET。

共享侧资源与真实时钟另有三个精确ID：`WC-SHARED-SIDE-TRUNCATED-ROSENTHAL-v1`、`WC-SHARED-SIDE-BUDGET-POTENTIAL-v1`和`WC-ANCHORED-ACTUAL-MARGIN-INTERFACE-v1`，见[主题精确账本](research/weighted_congestion_frontier/CLAIMS.md)。前两者区分UF子类与直接AS+B判据；后者区分充分LP、必要预算和有限43次证书。均未升级WC-TARGET。

共占高度扩展另有 `WC-WEIGHT-INTERACTION-HEIGHT-POTENTIAL-v1` 与 `WC-REALIZED-INTERACTION-CHAIN-CYCLE-v1`，见[主题账本](research/weighted_congestion_frontier/CLAIMS.md)及原三角势正文第11–13节。两个新ID分别为潜在图结构存在界和实际严格闭词必要链；未改旧权类ID。

[异权仿射全签名成本射线刚性](research/current/weighted_congestion/template_certificates/selector_local_moments.md)新增独立Claim：非全等权时全成本保真不能缩小全部资源的潜在用户支持，任意提高有限次数仍不行。原例有精确PNE；不升级全类存在/非存在状态。

另首登三个独立ID：`WC-MULTISOURCE-SHARED-SIDE-ROSENTHAL-v1`（同权hub跨源UF平方根存在界）、`WC-APPROXIMATE-SUPPORT-DISTORTION-v1`（允许改权的完整成本近似小支持失真）、`WC-CLASS-INTERNAL-CLOCK-COMPILER-OBSTRUCTION-v1`（固定有理strict sweep及任意次数类内三元compiler反例）。精确对象、全部假设和证据见[主题账本](research/weighted_congestion_frontier/CLAIMS.md)，不改旧Claim或WC-TARGET。

实际时钟余量依赖与完整proper锥必要暂态质量另有独立精确身份，见[主题账本](research/weighted_congestion_frontier/CLAIMS.md)；不改变WC-TARGET。
