# 七态 AND endpoint / 二次 localizer：作者 Proof 读后记录

2026-10-18。此为作者 Proof read-after，不是新盲审。旧 Exact-first `/workspace/scratch/038d9dcc4cac/sol_seven_state_and_gate_localizer_obstruction_exact_first_review.md` SHA256 `a492c7a07259e2d2b55d46de257bac4687618f88e420f4567d98652fc080ed2e` 原字节保留。

在 root 实际全文读完旧记录后，按新路由实际完整读 `/workspace/scratch/038d9dcc4cac/sol_seven_state_and_gate_localizer_obstruction_author_proof_v1.md`，SHA256 `6869558f8f155de15bc65f305ce0a3c5d42d76e84a936eb4fdfd5b7c90f29d75`；header 与 §1–4 全部 77 行 / 3766 bytes，工具完整返回 965 tokens、无截断。

结论：PASS/no fatal。作者证明与我的 Exact 独立重构顺序相同：D=Z−CY_i 为 M3 中的 degree-two null vector；先以 degree-three Q=g(H−h)² 支付 Boolean Z²→Z（总次数五），再用 D 与 Q 正交；最后才用 base≤5 转为 P 的真实期望。不存在把 base4 当 base5、将记号多项式当新增 degree-one endpoint、或把 null 关系乘超阶多项式的问题。

七态期望只有 (C,H)=(1,d) 留下负项，精确值 −p(1−eta)(d−h)²；所有合法边界均严格负。新 job 的两个 private unit 端是真实原端点，逐样本完整执行且不改 v 负载；该候选 true law 确满足所有 Gram/Boolean/onehot/moment 条件而失败指定 v localizer。普通 eligibility 本身没有被冒充为逻辑 AND 约束，actual OPT 仍为一。

作者最终 scope 正确：仅禁止忠实 AND 关系与本份基础 fifth moments、原 v 负载、全局 quadratic load 检验同时保留。没有排一般非线性依赖、近似 AND 或改变基础矩的构造；没有 finder、hardness、source decoder 或软件认证。

旧记录冻结后、作者 Proof 未读前，我另曾把一个自行推得的 phase-port 诊断消息发给 root/global：faithful X=C(1−Y_i) 可令 q=(C−X)(H−h) 压缩同一坏项。这不来自本作者 Proof，也不回填旧 Exact-first；本 read-after 不将该未另审消息升级为正式 Claim。

未运行软件，未改 repo/Git/Work 或任一旧冻结文件。
