# R-18 终局数值 MILP 候选：m=3,p=4 双玩家记录

- **稳定对象 ID**：`R-18-TERMINAL-MILP-PROPOSALS-20261031`
- **来源**：`803f20f0f54fc58a267c`（player 0）和 `cf0af9e399949ffdbb1a`（player 1）。原 JSON 与完整 action table 在 evidence 目录。
- **状态**：有限数值候选；源文件自己声明不构成精确或一般定理。

## 两条记录

两条记录的参数均为 `players=3, topics=4, objective=terminal, seconds=30`，portfolio 为 `[0,1,2]`，MILP 有 354 个变量和 806 个约束，HiGHS 返回 optimal (`status=0`, `mip_gap=0`)。

- `803f20f0f54fc58a267c`（player 0）：objective proposal (7/3\approx2.3333333333)，root utilities ((1,4/3,7/3))，mip node count 6226，elapsed 8.70 秒。
- `cf0af9e399949ffdbb1a`（player 1）：objective proposal (2)，root utilities ((1,1,2))，mip node count 194，elapsed 0.608 秒。

两份 `types` 都含浮点 (2/3) 或 2 的权重，并列出完整 21 个历史节点 action。因为这是数值 MILP 的放松/候选输出，不能从 `status=0` 推出动作表在精确分数模型中满足全部 SPE 不等式，也不能把 objective proposal 解释为 (W)、(OPT) 或半界违反量。

## 处置边界

该批来源的独有信息是“对不同指定玩家的终局目标，m=3,p=4 数值 MILP 可以找到 proposal 7/3 或 2 的候选策略表及求解规模”。它可用于下一步精确化（把浮点类型乘 LCM 变成整数，逐完整历史重验，并计算真正 W/OPT），但目前没有 exact certificate、客户目录语义或 half 反例。归档为候选对象，保留数值与局限，不升格为证明。
