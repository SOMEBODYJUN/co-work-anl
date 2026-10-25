# 五人半覆盖：根部真实拥挤与共同目录容量

本工作区只研究 Q-CAG-HALF 的 **m=5** 限制：有限单位客户、有限非空共同目录、每一份完整有序历史纯 SPE，允许空主题、重复与任意离轨平局，目标为 `OPT_5≤2W`。**仍 OPEN**。程序身份由本 clone 自动生成；不沿用历史 Boss 编号。

## 最短接续链

1. [当前最强根部组件](five_closure/root_copy_reply_rigidity.md)：真根偏离 T 后，保留倒二复制末主题的真实末回复 C；令 K=max目录主题大小，u 为实际首位最终收益，则每个合法 T,Q 有 `|Q\T|+|Q∩T|/5≤44u/3+13K/5−16|T|/3`。完整证明与独立审查分开；不是 half。
2. [独立重构](five_independent/root_saturation_review.md)：从原始 root / penultimate / terminal IC 合同重建各版；共同上界只有取真最大 K 时才可无条件用 K≤5u。旧11/2、113/21版留作来源，不是并列的新项目。
3. [最大主题容量](five_structure/max_theme_root_capacity.md)：同一真最大主题根枝，整数负载因式给四条 outside 容量界；结合已有二谱四尾定理得到 `1200OPT+2897K≤33482u`、`600OPT+4447K≤28735u` 等。依赖、独审见 [容量审查](five_aggregate/max_capacity_independent_review.md)。
4. [定价实现](root_shared_max_pricing.py)：旧557全类型域加根部新约束，以一个共同 K 标量合账；[输出](root_shared_max_copy_cg.json) **仅浮点证书发现，不是严格上界或 SPE 反例**。所有后续数值必须重新精确认证；当前仓库已独审严格五人界仍约2.042155。

## 精确 Claim 与证据边界

| 身份 | 域、结论及状态 | 正文/证据 |
|---|---|---|
| FIVE-ROOT-COPY-RIGIDITY | 上述原模型每份5人完整纯SPE、每个合法T,Q；共同K版根约束。完整有理非负恒等式，另一路从raw IC独立重构接受；无外审/新颖性认证 | five_closure/root_copy_reply_rigidity.md、audit_copy_reply_rigidity.py/.json；five_independent/root_saturation_review.md |
| FIVE-MAX-ROOT-CAPACITY | 同域，K全目录最大；整数负载与二谱四尾证书推出四条共同K必要行。独立raw审计接受；不推出half | five_structure/max_theme_root_capacity.md；five_aggregate/audit_capacity_independent.py/.json |
| FIVE-JOINT-PAYMENT-NO | 明确否定裸根分支二谱付款及列出的逐级rho补偿加强；原half不受否定 | five_background/joint_payment_counterexample.md、residual_payment_counterexample.md及相邻精确审计；原实例来源均保留 |
| FIVE-INSURANCE-OBSTRUCTION | 完整Cartesian经济/保险结构类中的构造预算障碍；范围承重，仅作者推导待父方审，不当任意目录结果 | five_counterattack/insurance_budget_obstruction.md及相邻审计 |

## 真正未付处

根部几乎完全拥挤会迫使其他主题相近；新IC支付了一部分旧松弛没有表示的容量。现有全类型数值组合仍在二以上。必须增加能与同一实际W共同付款的关系，或构造全部历史可实现的真正反例。互斥根分支的尾利润不能直接相加算作实际预算。

二谱根预算若只保留rho或一份实际matched-G，已有真实SPE反证；应读相应具体合同，不能把它们继续列作未证候选。探索输出不提升为严谨界。个人阶段备份不等于共享canonical入库。
