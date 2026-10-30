# 文献两攻击公式：锐渐近成果与阅读入口

本包研究文献原式两攻击倍率的参数上确界，**不研究全类均衡存在上界**。精确整数重数、次数、正轻权和幅度参数域均在[主证明](sharp_asymptotic_envelope.md)中固定。

| 阅读顺序 | 资产名称 | 用途与证据层级 |
| --- | --- | --- |
| 先读 | [参数上确界的锐渐近证明](sharp_asymptotic_envelope.md) | 完整重建上下两侧渐近、整数取整与全部合法参数序列；数学结论由证明承担 |
| 引用前读 | [锐渐近上下两侧独立攻击](../../../reviews/weighted_congestion/source_envelope/review.md) | 核对本稿的参数下界、上界消元及源全状态覆盖；这是内部审查 |
| 比较机制时读 | [统一机制上限](../source_ceiling/README.md)及[独立审查](../../../reviews/weighted_congestion/source_ceiling_review/independent_review.md) | 较早的同机制量级上限，限制源两攻击证书 |
| 复核诊断时读 | [高精度对数诊断程序](../../../../tests/audits/weighted_congestion/source_envelope/verify_logs.py)与[冻结诊断](../../../../evidence/runs/weighted_congestion/source_envelope/verification.json) | 区分真实整数次数行与连续代理行；Decimal 不是区间算术或一般证明 |
| 比较另一份推导时读 | [另一份锐渐近候选](../../../questions/weighted_congestion/source_envelope_candidate/sharp_envelope.md) | 另有自己的源事实核对；本稿已发生的审查不反向认证另一份候选 |

主证明的结论为

\[
F_d\sim\frac{2}{\sqrt e}\frac{\sqrt{d\ln\ln d}}{\ln d}.
\]

它是指定源公式的优化结果；不能把 F_d 替换为全类阈值 a_*(d)，也不能把保守两攻击的最小值当成每个实例的真实最优倍率。完整对称拓扑的实际非存在还原是[另一份有假设和倍率范围的定理](../source_topology/symmetric_two_column_reduction.md)。

详细证明中的 pending 标签保留原撰写时点。现行状态和实际审查范围以[主题账本](../../../weighted_congestion_frontier/CLAIMS.md)、[五轴表](../../../review_status.json)及上表链接的审查正文共同核对。外部同行评审和全球新颖性均未认证。

复验从仓库根调用 `python3 tests/audits/weighted_congestion/replay.py tests/audits/weighted_congestion/source_envelope/verify_logs.py`。程序在临时目录重建原运行布局；冻结诊断不原位覆盖。逐文件中文名称和来源见 [FILES](../../../weighted_congestion_frontier/FILES.md)。
