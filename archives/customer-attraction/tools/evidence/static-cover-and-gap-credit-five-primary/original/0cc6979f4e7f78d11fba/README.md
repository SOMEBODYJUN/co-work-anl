# 第七轮独立攻击：静态最优覆盖与单角色信用

2026-10-24。研究备份；Q-CAG-HALF 仍 **OPEN**。未改共享状态或 git/work.py。

- `static_cover_and_gap_credit.md`：从原模型独立尝试静态最优覆盖选择与单角色 gap 路线。均匀静态最优排列桥被现有八客户完整 SPE 精确否定；不是运输研究员的最优匹配桥反例。给出全范围单角色覆盖恒等式、其逐客户非负静态余项，以及一个真正的点态关系：实际其他角色覆盖客户上的静态→动态损失已由该客户自己的余项支付。另给最深低阈值节点的逐真实后继 EXCLUSIVE 关系。剩余债务集中于实际当前主题及实际遗漏客户；没有将剩余债务支付完。
- `audit_static_cover_and_credit.py`：只读现有输入/策略，从单位客户公式检查全部有序历史的 SPE、最优覆盖、均匀静态反例及信用分解，不调用规范 SPE solver/verifier。
- `exact_audit.json`：上述定义级精确审计输出；不是一般证明。
- `review_prefix_pushback.md`：独立通过同前缀单孩子 pushback，给出精确 H complement 及可选共同客户耦合；明确已有 future claim/多孩子不能免费叠加。
- `review_fixed_parent_first_positive.md`：独立通过 fixed-parent SD 第一正税整束 COLUMN，另证明精确列余量与 actual 行利润容量；不审 full SD 整体容量。

单角色根 sharp-gap 候选 `OPT_m-W <= (m-1) min_i u_i` 仍未证明。这与已有 `tail_credit/gap_and_deletion_obligations.md` 的 GAP-r 路线直接相关，本文不认领 gap 方向为新发现，不重复其 fixed-cone probes。标量孩子摘要不足的已有可变人数伪菜单障碍仍适用。本文分解只是把真实后继仍须提供的取消关系写清，并未把有符号余项或条件性推论称作新福利定理。

下一步：对 `static_cover_and_gap_credit.md` §4 中实际当前主题上的负债使用真实后继 IC；若不能支付，不能由点态非当前信用升级 sharp-gap 或 half。等待 owner 分派成熟结果的独立攻击。
