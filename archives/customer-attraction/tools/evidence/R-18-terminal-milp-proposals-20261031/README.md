# R-18 next_boss terminal numerical MILP proposals

来源：`803f20f0f54fc58a267c`（m=3,p=4, player=0，SHA-256 `468436cb9d87a407bb22a5f4f68a80c537f25817013ac47d6e23df5ccbb78912`）与 `cf0af9e399949ffdbb1a`（m=3,p=4, player=1，SHA-256 `c4e68cd7b6e24d5fab4e6d22ab056788d827a25a97a6bc2beb3a90608fb7a1d7`）。

两个 JSON 都由 HiGHS 数值 MILP 返回 `status=0`、`mip_gap=0`，但源字段明确写 `limitation: numerical MILP proposal, not an exact or general theorem`。每个实例有 354 variables、806 constraints、portfolio `[0,1,2]`，并保存完整 21 节点 action table 与浮点类型权重。它们是候选发现记录，不是已验证的共同目录 SPE 或 half 反例。
