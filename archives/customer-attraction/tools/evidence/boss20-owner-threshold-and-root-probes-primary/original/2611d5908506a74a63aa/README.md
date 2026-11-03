# boss20 的个人研究工作区

研究存档：`customer-attraction`；发布身份：`boss20`。

## 当前研究

目标固定为 Q-CAG-HALF：任意有限共同主题目录、任意人数、全部有序历史依赖纯 SPE，证明 `OPT_m <= 2W`。当前仍 OPEN；本工作区只推进一般输入类，不启动固定人数、固定目录或逐规模专项。

本轮沿三条相互检验的全范围接口工作：

- `clean_audit/owner_theta_audit.md`：独立内审确认 owner-hybrid 的同叶容量与动态 Theta 的局部子博弈语义；真实未付是 incoming-reset 与跨叶 whole-IC 传播。
- `route_flow/dual_owner_budget.md`：把 mixed-owner 充分条件化为分支成本 LP 的精确对偶 `D <= |G|`；这隔离了跨树共同定价义务。
- `route_mpath/dynamic_query_debt_identity.md`：完整路径菜单的 Fraction 恒等式。自由菜单唯一可能的正债来自条件倒数协方差；`route_mpath/README.md` 记录残余负载单调时可闭合，但一般 SPE 尚未给出该单调性。
- `independent_attack/threshold_multiplicity_audit.md`：三主题六玩家、单位重数 0/1/2 的完整 SPE 穷举只作有限候选筛查；最小 `W + ΣTheta - OPT = 1`，不提升一般结论。

## 根方向与下一步

根方向是把真实后继动作造成的正协方差或 incoming-reset 成本，绑定到同一历史标签下的真实 IC 行，避免跨互斥叶重复使用 `u_i`、`eta_i` 或尾部返还。优先判别两种情况：

1. 能否从后继玩家的最优性证明全路径残余负载单调，或以真实 whole-IC 给协方差逐客户定价；
2. 若不能，能否构造满足全部离轨历史的完整 SPE，使 LP 对偶 `D>|G|` 或动态 Theta 同序矩阵失败。单个静态叶、静态 max-flow、有限无反例均不足。

`root_explorations/` 仅保留本轮临时 Fraction 探针，范围和非证明性质见其中说明。

## 当前状态

一般主目标没有证明或真正反例。已推送资产均准确标为候选、接口、内审或有限观察；不把保存、审查或同行消息升级为数学真值。
