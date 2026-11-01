# 第三轮：可信策略构造与一般反例机制

主目标 Q-CAG-HALF 仍 OPEN。没有一般反例。

- `regret_replication.md`：每个 k≥1 的完整 SPE 可信副本构造；m=2k，W=OPT=4k，R=k/2，否定所有固定系数的 R≤C W/m。完整策略包括关键离轨分支与任意 BI 接管子树，不能仅凭在轨路径理解。
- `regret_replication_audit.py` / `regret_replication_audit.json`：Fraction 符号状态审计及小副本完整有序树回归。一般 k 的结论依赖正文归纳证明。

下一步继续研究一般目标：把“即时收益安全 + 少数异常分支递归 + BI 接管”的完整策略协议用于存在未覆盖客户的实例。直接给原 gadget 的 Z 加客户不能保持证明。
