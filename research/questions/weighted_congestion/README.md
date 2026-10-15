# 加权原子拥塞博弈：开放义务与候选成果目录

这里保存可继续工作的候选、未闭合义务和证据缺口。**在 main 保存不表示数学状态升级。** 精确模型查 [MODEL](../../weighted_congestion_frontier/MODEL.md)，已整合成果查[现行数学入口](../../current/weighted_congestion/README.md)，引用前查[主题账本](../../weighted_congestion_frontier/CLAIMS.md)及[实际审查记录](../../reviews/weighted_congestion)的覆盖范围。

## 先分清三个仍开放的问题

| 开放义务 | 已有可调用入口 | 当前缺口 |
| --- | --- | --- |
| 全类 O(d/ln d) 纯近似均衡存在性 | [权密度](../../current/weighted_congestion/weight_density.md)、[资源局部势拼接](../../current/weighted_congestion/power_bridge.md)、[局部窄权带](../../current/weighted_congestion/weight_bands/README.md) | 结构参数没有全类控制，稠密尺度与共同乘子接口尚未普遍闭合 |
| 超过现有正局部测试的增长下界 | [奇环精确包络](../../current/weighted_congestion/odd_ring/cohort_lower_bound_and_envelope.md)、[非对称缩权族](../../current/weighted_congestion/crossover/limit_family.md) | 需要新的全状态覆盖或更强机制；固定玩家数与改证书系数不足以自动得到增长族 |
| 一般多成员奇环的实际阈值 | [单成员实际存在证明](../../reviews/weighted_congestion/odd_ring_parameters/SINGLETON_NOTE.md) | 单冲突图表示不直接覆盖多成员群组；证书不可行不能替代真实均衡构造 |

## 按候选名称进入

| 候选成果名称 | 主稿与具体内容 | 尚需核查的义务与使用边界 |
| --- | --- | --- |
| 权重校准边际势的线性障碍 | [完整候选稿](marginal_potentials/fixed_marginal_potential_obstruction.md) | 单资源全部子集、固定权重校准夹逼；原稿保留 parent review pending，不能当全游戏非存在 |
| 任意玩家乘子的有限多尺度障碍 | [推广候选](marginal_potentials/arbitrary_multipliers.md) | 允许乘子依赖整个权向量；精确有限证书不代替一般证明的独立攻击 |
| 普适资源可加序势的局部夹逼桥 | [复制规则推导](ordinal_potentials/universal_additive_ordinal_bridge.md) | 规则不能依赖策略族、其他资源和游戏规模；需保持这些量词才能调用 |
| 依游戏选择的资源可分序势障碍 | [候选证明](ordinal_potentials/game_specific_separable_ordinal_barrier.md) | 游戏自身有精确均衡，否定的是资源可分势证书；对照[内部审查记录](../../reviews/weighted_congestion/ordinal_potentials/REVIEW.md)逐项核范围 |
| 玩家成本幂和的坏全局最小点 | [完整有限族推导](ordinal_potentials/power_of_total_cost_obstruction.md) | 特定目标的选择失败，不是无均衡；程序使用真实成本与精确根式比较 |
| 保守两攻击的多项式端点还原 | [整体候选](polynomial_endpoint/conservative_endpoint_candidate.md)、[副资源端点子命题](polynomial_endpoint/side_polynomial/Q_ENDPOINT_REDUCTION.md) | 子命题的本地复核与整体候选状态分别保留；只比较所写两条充分证书 |
| 完整对称两列状态商与证书损失 | [轨道公式及有限比较](two_column_orbits/two_column_orbit_candidate.md) | 一般直接推导已保存，但所引独立 review 原件未找到；有限优化不证明全参数最优 |
| 互补符号列与增长支持扩展 | [机制、有限证书及开放族](signed_columns/TRIAD_AND_EXTENSION.md) | 四玩家有有限精确证书；浮点筛选只是发现工具，增长族还缺一般全状态证明 |
| 源两攻击锐渐近的另一份推导 | [独立候选稿](source_envelope_candidate/sharp_envelope.md) | 自身审查没有完成；[现行已审同结论证明](../../current/weighted_congestion/source_envelope/sharp_asymptotic_envelope.md)不反向补造本稿审查 |

[非可分选择目标审查](../../reviews/weighted_congestion/multicolumn_review/NONSEPARABLE_REVIEW.md)保存幂和、乘积及对数目标的反例信息，但所引原 frontier 证明/程序缺失。可以读已在审查正文明确写出的推导，不能把缺失原资产假定为可调用证明或实现。

## 怎么复验与继续写

先按义务选候选，再读精确陈述、攻击边界和实际证据。代码与冻结输出的中文名称、用途和来源集中在 [FILES](../../weighted_congestion_frontier/FILES.md)；用 `python3 tests/audits/weighted_congestion/replay.py --list` 找程序，并在临时目录重放。候选成功通过有限计算、没有找到反例或被提交到 main 都不改变全称命题的真值。

形成一般证明、反例或可复用中间结果后，按 [GROWTH](../../GROWTH.md)更新精确身份、实际审查与研究图，再 checkpoint。保留尚未解决的致命 objection；不要用另一个命题的审查覆盖当前缺口。
