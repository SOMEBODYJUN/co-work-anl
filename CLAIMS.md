# 命题入口与新前沿

本页是根目录的命题导航；[现行逐命题登记](research/current/claims.md)保存完整范围、证明和状态，[规范模型](research/current/model.md)定义两设施客户博弈。凡改变设施数、目录条件、费用函数或客户 NE 量词，均建立新版本，不从旧结果自动推断。

| ID / 问题 | 严格范围与结论 | 状态及详情 |
| --- | --- | --- |
| SC-PHI-E/A/SHARP | 两设施、共同非空目录、正权原子客户、强制服务、独立混合精确客户 NE；存在完整续局下普遍黄金比，编码有理输入有多项式构造，下界族使阈值尖锐 | 现行全文内部审读；外部评审未记录。[共享分支](research/current/shared/README.md) |
| HC-2-UP/LOW | 两设施任意非空异构目录；因子 2 的纯续局上界与逼近 2 的另一下界族 | 内部候选，尚无外部评审。[异构分支](research/current/heterogeneous/README.md) |
| HC-RHO | 每跨对至多一公共客户，**至少一方目录至多两地点**；普遍尖锐 $\rho=2\cos(\pi/7)$ | 现行逐分支内部证明，外部评审未记录。[证明](research/current/heterogeneous/restricted_rho.md) |
| SPARSE-LONG-CYCLE | 对每个 $n\ge2$ 存在两目录各 $n$ 地点、单交叠、正整数权重且各格唯一 NE 的实例，全目录真实极小收益最佳回应构成遍历全部 $2n$ 地点的唯一环 | 本轮新写的显式构造和代数证明，内部算术复核；文献新颖性与外部评审未核。[证明](research/current/heterogeneous/sparse_long_cycles.md) |
| SPARSE-HIGH-ACYCLIC / SPARSE-BALANCED-R | 双方任意长单交叠、任意 `r≥1`；前者在没有 `r` 稳定布局下迫使全目录最佳回应环进入低于本方最大 reach 的 `1/r` 区，后者在两方都无这种低地点时构造完整纯 NE `r` 稳定布局 | 新条件性传播证明与精确边界攻击，内部审读；**不**推出全体 Q-SPARSE 的 `ρ` 上界。[证明](research/current/heterogeneous/sparse_high_reach_barrier.md) |
| SPARSE-RHO-ALL | 双方目录任意有限非空、每跨对至多一共有客户、正实权原子与完整逐布局精确独立混合 NE 存在量词 | 任意固定 reach 优先级纯 NE 规则已有全目录 `ρ` 稳定格；结合 HC-RHO 的 2×2 下界，全类最优普遍因子恰为 `ρ`。新直接证明已作多路线独立内部攻击；外部评审/新颖性未核。[证明](research/current/heterogeneous/sparse_unbounded_rho.md) |
| Q-K-FAC | 任意 $k\ge2$ 共同目录、加权原子客户是否有独立于 $k$ 的普遍近似因子，或有随 $k$ 增长的下界 | 开放；三设施因子 2 是判别关口，**不是**全 $k$ 结论。[任务页](research/questions/three_facilities.md) |
| Q-SPARSE | 两方目录均任意大、每跨对至多一名公共客户，普遍阈值是否仍为 $\rho$ | 本轮由 SPARSE-RHO-ALL 上界与 HC-RHO 下界闭合为 $\rho$；内部证明，外部评审未记录。[任务页](research/questions/sparse_catalogs.md) |
| Q-CUBIC | 双设施共同目录、客户费用 $\mathbb E[L^3]$，最优普遍阈值 | 开放；内部边界 $[\phi,2]$；跨费用类机制才使其成为高优先级。[任务页](research/questions/cubic_costs.md) |

单实例的达到证书、有限搜索与普遍定理的证明是不同证据。精确求解分支及局部困难性另见[现行登记](research/current/claims.md)；下一阶段的投入判断见[研究状态](RESEARCH_STATE.md)。
