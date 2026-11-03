---
id: customer-attraction/parent-exchange-moments-independent-audit
kind: computation
type_tag: 计算
status: exact-fraction-audit-passed
truth_status: exact-combinatorial-identities; no-SPE-or-half-claim
review_level: full-992-byte-read-and-execution
source_refs:
  - clean:eb9d6f8881d931c75b45:research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/parent/audit_exchange_moments_independent.py
---

# 最优交换矩独立 Fraction 审计

脚本仅使用 `math.comb`、`Fraction` 和谐和数，核验玩家数 `1..20`、背景覆盖数 `c=0..m`、交换数 `d=1..m` 的 harmonic coefficient 与两种 Vandermonde kernel，共 3080 个 exact parameter triples。实际执行一次 exit 0，stdout 为 `status=PASS`、`exact_parameter_triples=3080`、players_range `[1,20]`、`Fraction only`。

这只证明列出的组合恒等式回归通过。它不验证客户目录、完整策略、SPE、incumbent bridge、matching payment 或 Q-CAG-HALF，也不迁移到 unrelated-machines。与 archived exchange-moments/weak-matching 对象的关系是独立算术支撑，不能将交换矩直接当作真实跨枝激励。
