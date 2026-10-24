# 第八轮独立攻击与密度审查

2026-10-24，independent8。一般 Q-CAG-HALF **OPEN**。未修改 git/work.py 或旧资产。

- [同客户坐标核与非实际密度审查](coordinate_density_review.md)：从 root 陈述独立重构后完整对稿。通过加强 INIT 容量、局部非负同客户流、最早有序偏离及同角色 antichain 密度上界、一次 whole-IC 和全 O 守恒；没有 actual 钱包共同容量。追加实读 peer 原文后，I-cashout 与新 INIT 兼容也通过，J 必须按新 A_x 重算。无需有限计算承担一般性。
- [独立精确脚本](audit_source_preserving_density.py)与 [exclusive-create 冻结输出](source_preserving_density_exact.json)：只读旧52/348原始JSON，另加 m1零客户空主题和 m2空/单点全历史单点策略。完整 IC、NEW-CAP、同客户 DAG、密度前缀界、退款、逐客户库存均通过。348激活2个正context、12条正边且均实际终端；固定输入未覆盖跨层合流。仅实现 QA。
- 密度审查 §6 追加通过 root 共同 coverer 增边家族，origin 按输入占比分摊即可维持反链。
- [tree8 方程审查](tree_equations_review.md)：Hessian、对称耦合、RESET 符号、passive-query ROBUST、同叶税、期望式及新增边际势 Ξ/SAT 均通过；不含跨叶或实际共同钱包支付。
- root 指定 maximal-future 初始化的 [v2 独立脚本](audit_source_preserving_density_maxfuture.py)/[冻结输出](source_preserving_density_maxfuture_exact.json)，以及全部 common-future 角点的 [v3 脚本](audit_source_preserving_density_maxfuture_commonfuture.py)/[冻结输出](source_preserving_density_maxfuture_commonfuture_exact.json)，全部通过原检查并保留旧冻结实现。固定52输入分别激活7/9条客户 interlayer 边；两 packet 仍未激活任何 merger，明确保留实现覆盖缺口。详见审查 §8；无新实例扫描。

最初提出的 NE-descent 与 fluid benchmark 想法均已有失败或已有归属；核对后停止，未另存 rediscovery 数学资产。下一步是把支持保持能力接向仍 OPEN 的同角色全部 contexts 共同付款；不得把各 L_s≤u_l 相加成一份钱包。
