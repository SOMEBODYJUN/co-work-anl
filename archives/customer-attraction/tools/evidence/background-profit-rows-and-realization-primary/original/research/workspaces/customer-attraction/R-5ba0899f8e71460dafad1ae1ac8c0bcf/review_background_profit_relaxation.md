# 低阶背景利润松弛的父方精确复跑

2026-10-27；范围仅为 `subagent_3/background_profit_relaxation_note.md` 写明的 439 行，不声称对所有合法 IC 的完备性或六人福利反例。

从仓库根执行 `PYTHONPATH=. python3 research/workspaces/customer-attraction/R-5ba0899f8e71460dafad1ae1ac8c0bcf/subagent_3/background_profit_relaxation.py --audit --solve`。`--audit` 从分数公式为九个有理支持类型逐列重建全部行，输出 `O=1`、`W=28273/72900`、最小松弛零；浮点 LP 最优性不参与该可行性结论。每条行的合法来源分别为真实偏离的最坏分母、已有任意背景的恰三/四人利润定理，以及固定前缀末两人的精确税定理。它们只在原完整 SPE 的同一实际路径上是必要条件，未承载早期强制行动后的回复策略。

`--solve` 用九种支持类型各均分到六个互斥比较主题，按公共分母变成不同单位客户；规范 `ExactSPESolver` 用有理终局收益枚举所有可实现根 SPE 终局，回执为 `REALIZED_CATALOG_COMPLETE_EXACT_SPE_ENUMERATION`。实例客户总数 2187000，精确最差 SPE 覆盖也为 2187000；低福利实际主题计数不在根 SPE 结果集合。因此精确行族坏点不能作为目标反例。求解器的同计数缓存返回全部可实现终局而非单一匿名平局，符合仓库 `exact_solver.md` 的完整历史合同。

本复跑没有另外实现独立求解器。后续若加入更深真实回复行，必须重新核验其合法性；不能把这份松弛点的可行性外推到新增行。
