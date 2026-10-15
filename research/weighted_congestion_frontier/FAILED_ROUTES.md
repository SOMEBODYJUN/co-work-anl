# 失败机制与可回收结果

| 尝试与关键机制 | 具体失败或限制 | 排除范围、回收与重试条件 |
| --- | --- | --- |
| 奇环所有 aligned light 强制偏离，再用 odd hub 覆盖 | [精确 T_d 包络](../current/weighted_congestion/odd_ring/cohort_lower_bound_and_envelope.md)限制全部这套正测试，多项式混合不扩大 | 只限制证书；一般 cohort 实际游戏存在界未证明。需改变状态覆盖而非只调次数 |
| 同一重轻两列拓扑靠调参或多项式变强 | [完整拓扑还原](../current/weighted_congestion/source_topology/symmetric_two_column_reduction.md)在精确倍率范围还原到源族 | 异权和非对称资源不在范围；有限 crossover 给分离 |
| 固定小支持 gadget 重复堆叠 | 资源潜在用户数 r 有 r-PNE 的总成本证明；[三玩家例](../current/weighted_congestion/quadratic_triad/three_player_integer_obstruction.md)不可能独自给随 d 无界的下界 | 需增长用户支持或改变机制；有限例仍可复用 |
| 自然 complementary multicolumn 扩展 | [平衡轻玩家状态](../current/weighted_congestion/multicolumn/complement_column_escape.md)提供两倍逃逸 | 只排除此拓扑的放大；非所有多列构造 |
| 仅通过优化有序分组的潜在尾部参数A求统一界 | [两权级锐式](../current/weighted_congestion/weight_bands/ordered_tail_freezing.md)给min A=min{H,(1+K/H)^d}；K=ceil(H²)时固定次数仍随H无界 | 只否定此A包络控制；同一游戏有全空精确PNE，不能推断冻结程序本身选坏状态。可回收阶段Shapley拼接；[双排序混合势](../current/weighted_congestion/weight_bands/two_weight_order_blend.md)已给两权整个子类统一平方根次数界，故参数无界不能外推为该子类存在性障碍；实际占用或重开早组改变合同后可重试 |
| 保留统一固定低漏、只靠更深或更密DAG放大阶跃源 | [精确路径预算](../current/weighted_congestion/polynomial_curvature/dag_low_leakage_budget.md)把检测可行性化为z(z−1)ΣP_kz^(k−1)≤1，原step阈值至多O(√d) | 只限制所列低高端点；不控制过冲或实际多项式β。可回收最小/slack权表示；异质泄漏、改权或直接全状态机制需另证 |
| 固定正权向量，仅把所有正次数提高 | [高次份额势](../current/weighted_congestion/high_degree_share.md)证明，即使拓扑与系数变化，最低正次数趋无穷时近似保证一致趋1 | 排除这一纯高次放大路线；权向量随次数变化或保留低次项不在范围。必要小份额仍非充分反例 |
| 保持 crossover 权和系数只提高次数 | [degree40 与精确极限](../current/weighted_congestion/crossover/README.md)已有较低因子均衡 | 缩权和调幅可重试；固定四玩家仍只能给常数 |
| 稀疏权谱下模拟阶跃坏博弈 | [曲率](../current/weighted_congestion/polynomial_curvature/three_load_curvature_bound.md)与[密度存在界](../current/weighted_congestion/weight_density.md)限制对应保持结构的替换 | 引入稠密 cohort 或改变覆盖结构时另行研究 |
| 同资源密集尺度固定 power 乘子拼接 | [仿射路径](../current/weighted_congestion/power_bridge.md)在固定 p<1 下无统一夹逼，另有 sharp 两类型损失 | 不是博弈无均衡；允许实例相关乘子、跨资源支付等须另证 |
| 窄权带单独归一化 Shapley | [mixed difference/curl 与 selector 线性损失](../current/weighted_congestion/weight_bands/README.md) | 限指定势与归一化规则，不反驳全类次线性存在 |
| 任意固定玩家乘子及依游戏可分序势覆盖全部改善边 | [有限多尺度与固定资源束证明](../current/weighted_congestion/separable_ordinal_obstruction.md)已独立重构攻击；扭曲门槛ρ_d/d→1 | 只否定边际夹逼和全改善边可分序势；全空仍为精确均衡。非可分势、选定改善步或全局极小点接口改变时可重试；普适复制桥其他推论仍各自核对 |

失败本身有价值，但不得悄悄扩大否定量词。程序失败和有限搜索无结果没有数学真值含义。

## 序势障碍不能外推到任意依游戏最小点选择

可能的错误延伸是：既然资源可分目标无法对全部α改善严格下降，就断言任何资源可分目标均不能选出α-PNE。[精确等价](../current/weighted_congestion/separable_ordinal_obstruction.md)第四节否定这种延伸：入射距离唯一选择任意给定合法状态。因此只要求依游戏目标的全部全局最小点为均衡，与该游戏均衡存在本身等价。可回收的是精确量词边界，不是更强无势或无均衡结论；若要求单调、费用局部、跨游戏同规则或非循环有效构造，则需另立并验证这些新增条件。
