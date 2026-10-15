# 加权拥塞：现行数学资产与未解义务

精确对象采用 [MODEL](../../weighted_congestion_frontier/MODEL.md)：任意有限正权玩家、有限资源子集策略、非负系数次数至多 d 的多项式费用，玩家成本为资源费用之和，α-PNE 取弱不等式。命题身份在[主题账本](../../weighted_congestion_frontier/CLAIMS.md)，逐命题审查在[全仓五轴表](../../review_status.json)。此页整合各分支的共同数学认识，原稿中的时点状态不覆盖这份账本。

## 主目标已经推进到哪里

令
T_d=max_(R>1)[R(1+R)^d+1]/[(1+R)^d+R^(d+1)]，d≥2。
团队的完整构造证明 a_*(d)≥T_d∼d/ln d；已核实文献普遍上界为 d。**WC-TARGET 仍开放，尚缺对数因子的匹配。**一般证明和内部独立攻击已收录；外部评审、全球优先权未认证。

核心机制依次是：

1. 定义真实 hub/cohort 资源策略，直接重算每种偏离后的负载。
2. 任一 light 同 hub 时由严格 light 测试提供偏离；否则所有 light 反位，奇数 parity 提供一个可偏离的 hub。两类覆盖全部纯状态。
3. 正系数可行性化为闭环乘积严格大于一，同时满足真实权重闭环。
4. 用有限 reset/amplifier 实现给定倍率；人数可以很大，但始终是有限合法游戏。
5. 归一化两端因子并利用闭环，证明 T_d 是这套正局部测试的精确 envelope。它限制证书，不是 a_*(d) 的上界。

R1 的[线性重置完整稿](odd_ring_linear.md)给出显式 E_d=d/[(d+1)d^(1/(d+1))−d]，每个 d≥2 可在 E_d 本身排除均衡。R3 的[同次数完整稿](odd_ring/PROOF.md)给出每个 α<T_d 的全有理、全部资源次数恰 d 的构造，并扩展到混合非负多项式测试。R=1/t 将两边的标量包络逐项相同；二者是共同机制的独立实现，保留各自作者和审查，不能重复计算为两个独立突破。

奇环 singleton-cohort 的实际存在界 min{2,T_d} 是另一个有严格输入限制的定理。一般多 light cohort 的实际均衡阈值仍缺证明；不能从局部测试失败推导真实均衡存在。

## 按当前义务选择资产

| 数学问题 | 现行正文与实际用途 | 审查边界 |
| --- | --- | --- |
| 奇环下界、精确包络与 singleton | [同次数总证明](odd_ring/PROOF.md)、[线性实现](odd_ring_linear.md) | [独立资源/状态攻击](../../reviews/weighted_congestion/odd_ring_independent/REVIEW.md)、[包络审查](../../reviews/weighted_congestion/odd_ring_independent/EXACT_ENVELOPE_REVIEW.md)、[多项式审查](../../reviews/weighted_congestion/odd_ring_parameters/polynomial_envelope_review.md) |
| 文献源族究竟能做到多强 | [锐渐近](source_envelope/proof.md)、[全部对称拓扑还原](source_topology/proof.md)、[有限次数签名证书](source_degree32/PROOF.md) | 源族或受限拓扑的上界，不能变成全类上界 |
| 稀疏权谱与稠密权带如何共存 | [权密度与 sharp moment](weight_density.md)、[资源拼接与仿射两类型](power_bridge.md)、[局部窄权带](weight_bands/README.md) | 结构上界；参数在全类没有统一控制 |
| 参数“潜在用户密度”是否有约束力 | [padding](density_padding/proof.md) | 最小 potential 密度可任意填充，不否定最大稀疏密度上界 |
| 用固定小 gadget 放大 | [三玩家整数例](quadratic_triad/proof.md)、[补列多列逃逸](multicolumn/RESULT.md) | 有限例与资源支持上界分开；三玩家稿所引独立 review 未找到 |
| 非对称有限机制与次数外推 | [degree32 非对称例](crossover/README.md)、[缩权极限与有限运输](crossover/limit_family.md) | 固定四玩家只给常数下界，不能替代无限增长族 |
| 阶跃模拟与异权端点 | [三负载曲率](polynomial_curvature/proof.md)、[精确三点包络](polynomial_curvature/extension.md)、[异权还原](heterogeneous_endpoint/endpoint_reduction.md) | 严格局部条件，不是对所有构造的排除 |
| 辅助阶跃依赖模型 | [DAG 阈值](step_dag/proof.md) | step 费用不是当前多项式全类；迁移必须证明 |
| 固定乘子、ordinal 势和保守端点 | [待审候选目录](../../questions/weighted_congestion/README.md) | 有完整候选稿或有限证据，未统一升级为已审定理 |

全部文件、程序、冻结证据、来源和退役决定见 [FILES](../../weighted_congestion_frontier/FILES.md) 与 INTEGRATION；无需先通读它们才开始数学工作。

## 继续研究

首要义务是全类 O(d/ln d) 存在界；另一条是越过 light-forcing 的更强全状态下界。一般 cohort 的实际状态结构可作为判别接口。源族调参、固定人数增长和纯局部势的各个失败必须按其准确量词使用，不构成方法白名单。

审计统一运行 `python3 tests/audits/weighted_congestion/replay.py --list`，选择一个代码路径传入同一程序。它在临时目录重建旧相对布局，原冻结证据不会被覆盖。运行结果只验证实际计算范围；无限族和任意实参数依赖上面的数学证明。
