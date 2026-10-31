# 随机/分布鲁棒优化与凸序：独立选题线（2026-10-20）

状态：研究进行中；本文件即时保存可接续增量，不是已确认新结果。已全文读 BOSS_START、根 AGENTS 与四入口、专题四入口。来源标签 A=作者明确开放题，B=作者明确方向，C=团队派生。未完整核查的历史口头候选不得当作已证或新颖。

## 本轮先行排除检查

**口头旧种子 ROB-CO-W1-v0**：有界区间、固定均值、Wasserstein 球内所有凸损失的共同最坏分布。尚未固定 p，因此未形成数学身份。需要分别检查 p=1、p=∞ 与 p>1；不能把不同距离混同。

1. Gerhold–Gülüm, *Peacocks nearby: approximating sequences of measures*, arXiv:1512.06640，原文 2017-10-02 版本，https://fam.tuwien.ac.at/~sgerhold/pub_files/papers/2018_peacocks.pdf 。原文 Problem 2.5（PDF p.4）正是固定均值的球中最小/最大凸序元素问题；Prop.3.2（PDF p.6）完整解决 W∞，Prop.6.1 解决 stop-loss 距离。因此 **W∞ 版本已被直接覆盖**，不能作为新题。原文 §9 另有耦合到马氏鞅的明确开放问题，待查新。
2. Cai–Liu–Yin, *Worst-case distortion risk measures of transformed losses with uncertain distributions lying in Wasserstein balls*, ASTIN Bulletin 56 (2026), 270–294，在线源 https://www.cambridge.org/core/journals/astin-bulletin-journal-of-the-iaa/article/worstcase-distortion-risk-measures-of-transformed-losses-with-uncertain-distributions-lying-in-wasserstein-balls/38372AA02C3384976985EC50AB05CF19 。搜索显示其 Thm.3.3 后讨论了对风险度量无关的 W1 限损最坏分布，但它是变换后、未必固定均值的不同问题；须逐假设核对，当前不能声称覆盖/不覆盖。

## 正在形成的不同论文族

| 族 | 主问题机制 | 初步候选 | 尚未核查的致命风险 |
| --- | --- | --- | --- |
| 凸序球极值/peacock | call-function 格结构与指标距离的相容性 | W1 有界支撑固定均值下，共同最坏分布何时存在；不存在时的最小凸序上包络 | 可能是已知截尾/格投影定理；W∞ 已解 |
| Wasserstein DRO 对偶与有限支持 | Kantorovich 对偶、增长条件、原子支撑 | 加均值后的精确普适极值/极值支撑界 | 可能只是 Gao–Kleywegt 或 generalized moment LP 的直接推论 |
| 鞅输运稳定性 | 凸序约束把任意 coupling 换成 martingale coupling | 有限支撑、树/格点几何下锐常数或算法 | 2020–2024 sharp inequalities 可能全覆盖 |
| 风险变换与共同最坏法则 | 分位数/isotonic projection、随机序 | 一族分段线性变换的共同最坏分布刻画 | 2024/2026 ASTIN 工作可能已解决；只换损失无价值 |

## 下一实际动作

先对 W1 种子运行独立运输 LP，检查不同 strike 的 call-function 最大值能否由同一分布达到；若不能给精确反例而非继续假设共同极值存在。并行查 §9 公开问题后续、鞅 Wasserstein 锐常数、DRO 有限支持定理覆盖。只把有完整成果包的候选带入 battle。
