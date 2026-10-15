# 加权原子拥塞博弈：成果目录与研究入口

当前主目标 **WC-TARGET v1 仍开放**。团队已经保存奇数环的完整全状态下界证明及内部独立审查；全类存在性上界与下界之间仍有对数缺口。本页按数学成果组织阅读，不要求先通读协作工具、原始分支或全部证据文件。

精确对象采用 [MODEL](../../weighted_congestion_frontier/MODEL.md)：有限正权玩家、有限资源子集策略、非负系数次数至多 d 的多项式费用；玩家成本为所用资源费用之和，α-PNE 使用弱不等式。不同玩家数、资源支持、权密度、费用规则和证书量词不能省略。

## 第一次接手：按这个顺序读

1. [模型与全类目标](../../weighted_congestion_frontier/MODEL.md)：固定费用、真实单方偏离和普遍阈值 a_*(d)。
2. [奇数环线性重置总稿](odd_ring_linear.md)：先理解目前最强增长下界的资源机制、显式结果与剩余缺口。
3. [奇数环总证明](odd_ring/cohort_lower_bound_and_envelope.md)：需要调用下界或包络时，读全状态覆盖、系数闭环、有限有理实现及精确适用范围。
4. [逐资源与全状态独立审查](../../reviews/weighted_congestion/odd_ring_independent/REVIEW.md)、[精确包络独立审查](../../reviews/weighted_congestion/odd_ring_independent/EXACT_ENVELOPE_REVIEW.md)：区分已覆盖义务、有限核验与未认证的新颖性。
5. [精确命题账本](../../weighted_congestion_frontier/CLAIMS.md)、[当前前沿](../../weighted_congestion_frontier/RESEARCH_STATE.md)、[失败机制](../../weighted_congestion_frontier/FAILED_ROUTES.md)：选取当前义务后，再从下表进入所需工具。

首屏摘要不能替代上述精确陈述。完整逐文件中文名称、用途、程序和冻结输出见 [研究文件目录](../../weighted_congestion_frontier/FILES.md)。

## 主结果与共同机制

令

\[
T_d=\max_{R>1}\frac{R(1+R)^d+1}{(1+R)^d+R^{d+1}},\qquad d\ge2.
\]

[同次数奇环总证明](odd_ring/cohort_lower_bound_and_envelope.md)给出：每个 α<T_d 都有有限正有理权、正有理系数、全部资源次数恰为 d 的游戏没有 α-PNE。因此 a_*(d)≥T_d∼d/ln d。已核对文献给出的全类存在上界仍为 d；外部同行评审和全球优先权均未认证。

[线性重置总稿](odd_ring_linear.md)给出显式 E_d=d/[(d+1)d^(1/(d+1))−d]，并在该因子本身排除均衡。线性重置与同次数实现属于同一奇环机制；R=1/t 使两份标量包络逐项相同。它们各自保留作者来源和实际审查，不能作为两个独立突破重复计算。

全状态覆盖 → 正系数闭环 → 有限实现 → 下界，是存在的证明链。**正局部测试的精确包络只限制这套证书**；一般多成员群组的实际游戏阈值仍未解决。每组只有一名群组玩家时的 min{2,T_d} 存在界另有严格输入限制。

## 按成果名称查找

| 成果包名称 | 正文入口与内容 | 作用与边界 |
| --- | --- | --- |
| 奇数环下界与精确证书包络 | [总证明](odd_ring/cohort_lower_bound_and_envelope.md)、[线性重置总稿](odd_ring_linear.md)、[可变次数接口](odd_ring_linear/README.md) | 增长下界主线；精确包络是证书界。一般群组实际阈值开放 |
| 文献两攻击公式的锐渐近 | [成果入口](source_envelope/README.md)、[锐渐近证明](source_envelope/sharp_asymptotic_envelope.md)、[统一机制上限](source_ceiling/README.md) | 优化指定源公式，不能作为全类存在上界；另一份推导仍按候选保存 |
| 完整对称两列拓扑还原 | [第三版完整证明](source_topology/symmetric_two_column_reduction.md) | 在所写倍率范围内将实际非存在还原至源公式；不含异权或非对称资源 |
| 三十二次源参数符号上界 | [参数消元与整数符号证明](source_degree32/symmetric_source_interval_certificate.md) | 覆盖指定源公式的全部合法实参数，为有限拓扑分离提供前提 |
| 四玩家十四资源非对称构造 | [固定实例与成本表](crossover/README.md)、[拓扑分离](crossover/separation.md)、[缩权极限族](crossover/limit_family.md) | 有限下界、次数外推失败与极限运输分别记录；固定玩家数不构成增长族 |
| 资源局部权密度与锐矩估计 | [一般证明](weight_density.md) | 稀疏权谱下的结构存在界；密度参数在全类没有统一控制 |
| 资源局部势拼接与两尺度路径 | [共同接口](power_bridge.md)、[路径障碍](power_bridge/path_obstruction.md)、[两权组分片势](power_bridge/affine_two_type.md) | 共享乘子可拼接，但固定次线性幂不能覆盖任意密集权谱；两精确权组有锐跨度界 |
| 局部窄权带与跨带障碍 | [份额、存在界及选择器证明](weight_bands/README.md) | 局部权比存在界；跨带混合差分、标准势线性损失只约束指定方法 |
| 潜在用户密度填充 | [投影与提升证明](density_padding/optional_user_density_padding.md) | 已占权重区间的最小人数可任意填充，有限倍率均衡逐一保持；不否定最大稀疏密度上界 |
| 资源用户支持与双人资源界 | [资源支持存在界](resource_support.md)、[双人资源互补网络](odd_ring_linear/pair_obstruction/PAIR_OBSTRUCTION.md) | 限制有界支持小构件的放大；没有全类常数或多项式时间结论 |
| 三玩家整数二次实例 | [完整成本表与最优倍率](quadratic_triad/three_player_integer_obstruction.md) | 有限精确证明；所引独立审查原件未找到，不补造审查通过 |
| 文献源公式二次包络 | [有理参数上界](quadratic_source/source_family_envelope.md) | 指定源公式的有限次数边界，与三玩家实例分开比较 |
| 阶跃模拟曲率与三负载凸包络 | [前缀模拟障碍](polynomial_curvature/three_load_curvature_bound.md)、[精确三点最优工具](polynomial_curvature/three_point_polynomial_envelope.md) | 排除保持源平台形状的直接模拟；改变权重、拓扑或状态覆盖须另论 |
| 异权端点强制还原 | [单一轻权还原证明](heterogeneous_endpoint/endpoint_reduction.md) | 只作用于所写两类端点强制不等式，不是全部异权拓扑等价 |
| 互补多列拓扑的二倍逃逸 | [存在与三列锐性证明](multicolumn/complement_column_escape.md) | 排除指定共同轻权、多列关联方式的放大；不排除全部多列构造 |
| 任意玩家乘子与依游戏可分序势障碍 | [现行完整重构](separable_ordinal_obstruction.md)、[冻结证明独立攻击](../../reviews/weighted_congestion/ordinal_potentials/game_specific_independent_attack.md) | 线性障碍只针对全部改善边下降的可分证书；所构游戏有全空精确均衡，不排除全局选态 |
| 有向无环阶跃依赖辅助模型 | [路径计数与精确阈值](step_dag/step_dependency_threshold.md) | 费用为阶跃函数，属于辅助模型；迁入当前多项式类需要新证明 |

这些包中的 theorem、obstruction、counterexample、review 和 evidence 是不同类型的资产。同包材料可以互相指向，但来源相同、通过有限计算或位于 current 都不自动提升数学状态。

## 从当前义务继续

- **全类 O(d/ln d) 存在性。** 先读权密度、资源拼接和窄权带三包，核对稠密尺度及共享乘子的未解接口；[边际势和序势候选](../../questions/weighted_congestion/README.md)只按实际审查等级使用。
- **超越现有奇环下界。** 先读奇环精确包络，再看非对称缩权族、曲率和多列逃逸；需要改变全状态覆盖机制，不能把证书失效当实际均衡存在。
- **一般群组奇环的实际阈值。** 从总证明的单成员子类与[单冲突图独立证明](../../reviews/weighted_congestion/odd_ring_parameters/SINGLETON_NOTE.md)起步，明确多成员使哪一步状态表示失效。

已有路线是搜索种子，不限制可尝试的方法。候选、反例和可复用工具可以按真实层级保存；重要状态提升仍须闭合实际证明义务并接受独立攻击。

## 程序、证据与时点状态

程序统一从仓库根运行 `python3 tests/audits/weighted_congestion/replay.py --list` 选择具体核验，再把代码路径传给同一程序。它在临时目录恢复原相对布局，避免覆盖冻结证据。Decimal 诊断、浮点发现、有限有理枚举和整数符号证书在文件目录中分别命名。

部分详细稿保留撰写时的 pending 标签或历史相对路径。现行逐命题审查查[主题账本](../../weighted_congestion_frontier/CLAIMS.md)及[五轴表](../../review_status.json)，实际审查范围查对应审查正文；没有审查记录的结论不能靠入口摘要升级。不可变原件及恢复路径见 [INTEGRATION](../../weighted_congestion_frontier/INTEGRATION.json)。
