# 失败机制与可回收结果

| 尝试与关键机制 | 具体失败或限制 | 排除范围、回收与重试条件 |
| --- | --- | --- |
| 奇环所有 aligned light 强制偏离，再用 odd hub 覆盖 | [精确 T_d 包络](../current/weighted_congestion/odd_ring/cohort_lower_bound_and_envelope.md)限制全部这套正测试，多项式混合不扩大 | 只限制证书；一般 cohort 实际游戏存在界未证明。需改变状态覆盖而非只调次数 |
| 同一重轻两列拓扑靠调参或多项式变强 | [完整拓扑还原](../current/weighted_congestion/source_topology/symmetric_two_column_reduction.md)在精确倍率范围还原到源族 | 异权和非对称资源不在范围；有限 crossover 给分离 |
| 固定小支持 gadget 重复堆叠 | 资源潜在用户数 r 有 r-PNE 的总成本证明；[三玩家例](../current/weighted_congestion/quadratic_triad/three_player_integer_obstruction.md)不可能独自给随 d 无界的下界 | 需增长用户支持或改变机制；有限例仍可复用 |
| 自然 complementary multicolumn 扩展 | [平衡轻玩家状态](../current/weighted_congestion/multicolumn/complement_column_escape.md)提供两倍逃逸 | 只排除此拓扑的放大；非所有多列构造 |
| 保持 crossover 权和系数只提高次数 | [degree40 与精确极限](../current/weighted_congestion/crossover/README.md)已有较低因子均衡 | 缩权和调幅可重试；固定四玩家仍只能给常数 |
| 稀疏权谱下模拟阶跃坏博弈 | [曲率](../current/weighted_congestion/polynomial_curvature/three_load_curvature_bound.md)与[密度存在界](../current/weighted_congestion/weight_density.md)限制对应保持结构的替换 | 引入稠密 cohort 或改变覆盖结构时另行研究 |
| 同资源密集尺度固定 power 乘子拼接 | [仿射路径](../current/weighted_congestion/power_bridge.md)在固定 p<1 下无统一夹逼，另有 sharp 两类型损失 | 不是博弈无均衡；允许实例相关乘子、跨资源支付等须另证 |
| 窄权带单独归一化 Shapley | [mixed difference/curl 与 selector 线性损失](../current/weighted_congestion/weight_bands/README.md) | 限指定势与归一化规则，不反驳全类次线性存在 |
| 任意固定玩家乘子、universal ordinal、game-specific separable 的更广障碍 | 原稿保留在[候选区](../questions/weighted_congestion/README.md)，其中部分仍待父对话审查 | 未完成独立审查的强结论不作为已审 barrier；先核对原证明与缺失依赖 |

失败本身有价值，但不得悄悄扩大否定量词。程序失败和有限搜索无结果没有数学真值含义。
