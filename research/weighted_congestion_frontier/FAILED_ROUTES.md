# 失败机制与回收

## WC-R1-PREFIX-SMOOTHING v1：保持原阶跃平台的直接多项式搬运

- 尝试：保留原文 Theorem 5 的 binary 权重与 prefix 策略，以提高次数的非负多项式近似每个 step，控制阈值前泄漏与阈值后平台。
- 关键依赖：卫星 a_1 的三个可达负载 L=3/2−2^(−m)、H=3/2、U=2−2^(−m) 上，要求 p(L)≤εp(H)、p(U)≤Kp(H)，固定 ε<1 与 K。
- 具体失败：log-load 凸性迫使 K≥ε^(−2^(m−2))（m≥3），与次数无关。故提高次数不能修复有界平台失真；只检查 L,H 的次数代价遗漏了 U 的过冲。
- 否定范围：仅否定这种 faithful-simulation 接口；没有否定 prefix 拓扑、费用重配或全状态非存在机制。
- 回收：一般三负载约束 p(U)/p(H)≥[p(H)/p(L)]^[log(U/H)/log(H/L)]，可直接加入新的成本预算，而无需再做盲目阶跃拟合。
- 重试条件：改变负载几何，或给出能利用过冲且覆盖所有状态的新证明。
- 证据： [一般证明与边界](assets/R1/prefix_curvature/proof.md)、同目录有理精确回归及独立攻击。主目标仍开放。

公屏与保存程序的运行说明见 [RUNBOOK.md](RUNBOOK.md) 和 [CHECKPOINT.md](CHECKPOINT.md)。

## WC-R1-HET-ENDPOINT-REDUCTION v1：只在原端点证书内混合轻权

- 尝试：给每名轻玩家不同正权和不同卫星多项式，保留“全 opposite 攻击 heavy、每个 singleton-aligned 攻击该 light”的严格证书。
- 失败机制：重玩家的总 margin 按轻权平均后有一个密度见证，给出实数 n=W/w_i 的同权代数证书；凸性支持 n 向下取整，倍率损失小于 1/(α−1)。
- 否定范围：仅此 endpoint-forcing 证书，且输出仍允许同权非负多项式。没有自动证明所有 full-state 异权 star 都满足它，也未认证文献精确包络的额外比较。
- 回收：精确整数还原和全状态端点充分性；真实未解方向是不同玩家负责 singleton、中间状态覆盖或非对称列。
- 重试条件：明确构造一个不通过这些端点测试但全状态均有大倍率偏离的新族。
- 证据与边界：[一般证明](assets/R1/cohort_growth/endpoint_reduction.md)、同目录独立审查及精确回归。
