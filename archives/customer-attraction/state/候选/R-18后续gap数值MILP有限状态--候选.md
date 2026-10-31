# R-18 后续 gap 数值 MILP 有限状态

- **稳定对象 ID**：`R-18-GAP-MILP-NEXT-20261031`
- **来源**：`0f058ff99f06d6dd1009`、`0a4e32f3f28fd7849789`、`45d455cbe472e843691a`。完整 JSON 保存在 `archives/customer-attraction/tools/evidence/R-18-gap-milp-next-20261031/`。
- **状态**：有限数值候选，保留求解器状态和误差，不构成证明。

## m=3,p=5, player=1

`0f058ff99f06d6dd1009` 有两条结果，均 `status=0`、`mip_gap=0`，654 variables、1497 constraints，根 utilities 为 ((1,1,1))，objective proposal 均为 2；node count 为 677 和 844，耗时约 15.65 秒和 11.92 秒。即使数值求解达到自身的 optimal 状态，源仍明确这是 proposal 而非精确或一般定理；类型权重与完整策略表尚未经过 Fraction/ExactSPESolver 重建。

## m=4,p=5, player=0/1

`0a4e32f3f28fd7849789`（player 0）两次均在 40 秒限制内返回 `status=1`，proposal 约 (8.96\times10^{-13}) 和 (6.49\times10^{-13})，mip gap 约 (1.67\times10^{13}) 和 (2.27\times10^{13})。`45d455cbe472e843691a`（player 1）两次也为 `status=1`，proposal=1、mip gap 约 14。两者都有 3935 variables、9682 constraints，root utilities 近似全 1，但未达到 optimal，不能从 proposal 值推导真实 gap。

## 处置

这三源的独有内容是 next_boss 变体在不同 (m,p) 和指定玩家上的求解器边界：m=3,p=5 有两次数值最优 proposal=2；m=4,p=5 两个玩家均在 40 秒截断。它们应作为下一步精确化的候选输入，需把浮点类型离散化后重建完整历史 SPE，再计算真实 W/OPT；当前不归入反例、定理或 half 结论。
