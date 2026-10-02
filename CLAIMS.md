# 命题入口与新前沿

本页是根目录的命题导航；[现行逐命题登记](research/current/claims.md)保存完整范围、证明和状态，[规范模型](research/current/model.md)定义两设施客户博弈。凡改变设施数、目录条件、费用函数或客户 NE 量词，均建立新版本，不从旧结果自动推断。

| ID / 问题 | 严格范围与结论 | 状态及详情 |
| --- | --- | --- |
| SC-PHI-E/A/SHARP | 两设施、共同非空目录、正权原子客户、强制服务、独立混合精确客户 NE；存在完整续局下普遍黄金比，编码有理输入有多项式构造，下界族使阈值尖锐 | 现行全文内部审读；外部评审未记录。[共享分支](research/current/shared/README.md) |
| SC-DIAG-NORMAL / SC-OFFDIAG-FPT | 双设施共同目录；同址收益可对半，实例最优的精确值与完整证书只需异址真实坐标极小值；正有理输入指数参数为异址最大交叠人数 $\kappa_{\ne}$ | 新严格推导、实现和独立对照；不转移到异构目录。[证明](research/current/shared/instance_complexity_barriers.md) |
| SC-TWO-SITE-EXACT / SC-EQUAL-REACH-EXACT / SC-TWO-REACH-SPARSE | 前两项分别为共同目录至多两地点、全体地点 reach 相等；第三项再要求每对异址至多一公共客户且 reach 至多两种 | 各存在精确 SPE；第三项不可删除单交叠假设。[证明](research/current/shared/instance_complexity_barriers.md) |
| SC-TWO-REACH-MULTI-NO | 共同目录三地点、两种 reach、五名正整数客户；允许某异址对两名共有客户 | 完整 NE 枚举给 $\alpha^*=14/13$，严格反驳删除上述单交叠条件。[构造](research/current/shared/instance_complexity_barriers.md) |
| SC-THREE-DEC1-HARD / SC-THREE-DECa-HARD | 共同目录恰三地点、显式正整数权、完整逐布局精确混合 NE；固定有理 $a=1$ 或 $1<a<(1+\sqrt3)/2$ | 全局 $\alpha^*\le a$ 弱 NP 完全；不是从局部难性直接推出，须靠覆盖六类布局的守卫。**恰三地点**在 $a\ge(1+\sqrt3)/2$ 的细分类仍开放。[归约](research/current/shared/three_site_exact_hardness.md) |
| SC-FIVE-DECa-HARD | 共同目录恰五地点、显式正整数权、完整逐布局精确混合 NE；**每个事先固定的有理 $1<a<\phi$** | 全局 $\alpha^*\le a$ 弱 NP 完全；YES 归约实例 $\alpha^*=a$，NO 严格大于 $a$。新证明不扩大旧三地点定理作用域；三、四地点的高倍率细分类仍开放。[证明](research/current/shared/five_site_exact_hardness.md)、[独立内部审查](research/FIVE_SITE_AUDIT_2026-10-02.md) |
| SC-GRANULAR-APPROX / LOCAL-ATOM-WARDROP-k | 前者为两设施共同目录、异址最大共有客户单体权重 $\theta<R_{\max}$；后者为固定 $k$ 设施局部布局、任意原子与 Wardrop 客户 NE | 前者构造倍率至多 $(R_{\max}+\theta)/(R_{\max}-\theta)$ 的完整续局；后者给尖锐的每坐标误差 $(k-1)\theta/2$，**不**推出全 $k$ SPE。[两设施](research/current/shared/atomic_granularity.md)、[局部一般化](research/current/local_and_exact/atomic_wardrop_gap.md) |
| SC-SPARSE-3 / SC-SPARSE-4 / SC-SPARSE-5 | 同一共同目录、每对**不同**地点至多共享一名客户；地点数分别至多 3/4/5 | 尖锐普遍上确界依次 $\sqrt2,\sqrt[3]4,\phi$；三、四地点新上界与正有理下界，五地点下界沿用原六地点族剪枝。[证明](research/current/shared/small_sparse_catalogs.md) |
| HC-2-UP/LOW | 两设施任意非空异构目录；因子 2 的纯续局上界与逼近 2 的另一下界族 | 内部候选，尚无外部评审。[异构分支](research/current/heterogeneous/README.md) |
| HC-RHO | 每跨对至多一公共客户，**至少一方目录至多两地点**；普遍尖锐 $\rho=2\cos(\pi/7)$ | 现行逐分支内部证明，外部评审未记录。[证明](research/current/heterogeneous/restricted_rho.md) |
| SPARSE-LONG-CYCLE | 对每个 $n\ge2$ 存在两目录各 $n$ 地点、单交叠、正整数权重且各格唯一 NE 的实例，全目录真实极小收益最佳回应构成遍历全部 $2n$ 地点的唯一环 | 本轮新写的显式构造和代数证明，内部算术复核；文献新颖性与外部评审未核。[证明](research/current/heterogeneous/sparse_long_cycles.md) |
| SPARSE-HIGH-ACYCLIC / SPARSE-BALANCED-R | 双方任意长单交叠、任意 `r≥1`；前者在没有 `r` 稳定布局下迫使全目录最佳回应环进入低于本方最大 reach 的 `1/r` 区，后者在两方都无这种低地点时构造完整纯 NE `r` 稳定布局 | 新条件性传播证明与精确边界攻击，内部审读；**不**推出全体 Q-SPARSE 的 `ρ` 上界。[证明](research/current/heterogeneous/sparse_high_reach_barrier.md) |
| SPARSE-RHO-ALL | 双方目录任意有限非空、每跨对至多一共有客户、正实权原子与完整逐布局精确独立混合 NE 存在量词 | 任意固定 reach 优先级纯 NE 规则已有全目录 `ρ` 稳定格；结合 HC-RHO 的 2×2 下界，全类最优普遍因子恰为 `ρ`。新直接证明已作多路线独立内部攻击；外部评审/新颖性未核。[证明](research/current/heterogeneous/sparse_unbounded_rho.md) |
| SPARSE-BAD-LONG | 对每个 `3/2<r<ρ` 与任意 `n≥1`，正有理单交叠 `(n+1)×(n+1)`、每格唯一客户 NE | 全布局无 `r` 稳定格，但唯一全目录精确回应环遍历全部行动；否定阈值以下“坏倍率自动短精确核心”，**不是** `>ρ` 反例。[证明](research/current/heterogeneous/sparse_bad_long_cycles.md) |
| SPARSE-BAD-LONG-ALL | 新版本将前行的 `r` 量词扩为**每个 `1≤r<ρ`**，并保留任意 `n≥1`、正有理权、唯一 NE 与全目录唯一长环 | 原版本为子命题；新范围由明确开参数余量及 `r=1` 转移证明，不把较小 `r` 下的所有 `A_i` 误称为高行。[证明](research/current/heterogeneous/sparse_bad_long_cycles.md) |
| Q-K-FAC | 任意 $k\ge2$ 共同目录、加权原子客户是否有独立于 $k$ 的普遍近似因子，或有随 $k$ 增长的下界 | 开放；三设施因子 2 是判别关口，**不是**全 $k$ 结论。[任务页](research/questions/three_facilities.md) |
| Q-SPARSE | 两方目录均任意大、每跨对至多一名公共客户，普遍阈值是否仍为 $\rho$ | 本轮由 SPARSE-RHO-ALL 上界与 HC-RHO 下界闭合为 $\rho$；内部证明，外部评审未记录。[任务页](research/questions/sparse_catalogs.md) |
| Q-CUBIC | 双设施共同目录、客户费用 $\mathbb E[L^3]$，最优普遍阈值 | 开放；内部边界 $[\phi,2]$；跨费用类机制才使其成为高优先级。[任务页](research/questions/cubic_costs.md) |

单实例的达到证书、有限搜索与普遍定理的证明是不同证据。精确求解分支及局部困难性另见[现行登记](research/current/claims.md)；下一阶段的投入判断见[研究状态](RESEARCH_STATE.md)。
