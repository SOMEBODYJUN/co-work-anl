---
id: customer-attraction/r2fc-round3-security-support-budget-boundary
kind: obstruction
type_tag: 障碍
title: 较大 support-budget DR 探索与 CAG 迁移边界
status: finite-exploration-retained
truth_status: finite-LP-diagnostics; explicitly-not-CAG
scope: R-2fc8878b4bdd4328bbc1bcf1df8ca831/round3_security 六个报告/脚本；support masks, DR budget recurrence, finite random policies
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/round3_security/rank_seed_n4k6.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/round3_security/support_budget_probe.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/round3_security/support_groups_n3k6.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/round3_security/support_submod_alternating_n4k6.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/round3_security/support_submod_groups_n3k6.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/round3_security/support_submod_n5k6.json

 evidence_packet: ../../tools/evidence/R-2fc-round3-security-20261031/
---

# 实读结果

`support_budget_probe.py` 的约束对象是 (q) 的 support mask 和递归势 (Phi)，并没有 CAG 客户类型、共同主题目录、客户终局均分或六名提供者的完整历史纯 SPE。代码枚举有限有序历史，保留一个固定策略的单步比较，再通过 scipy `linprog` 迭代寻找 (Phi) 与混合 (p) 的下界；所有数值量是浮点值。

四个 no-hit 报告分别覆盖 (n=4,k=6) 的 rank/submod、(n=4,k=6) alternating、(n=3,k=6) groups、(n=5,k=6) submod，记录 `best=0`。`support_groups_n3k6.json` 的唯一 witness 报告记录 `best=-0.006552668982782672`、三人根 `(0,3,4)`、fractional p 与 42 个 masks 的 W；它是该较大 support-budget LP 的候选，不是客户实例或 SPE 证书。

# 处置与迁移边界

六源均保留为有限探索工具/报告。它们可供后续比较“DR 预算递归是否具有类似势支付”的启发，但没有共同前提把 support masks 识别为 CAG 主题或把 LP witness 识别为合法完整 SPE。要迁移到当前六人 CAG，必须重新定义客户归属、覆盖福利、每个离轨历史的真实后继和 exact/Fraction 偏离证书；本批没有完成这些步骤。因此不产生 Q-CAG-HALF 的证明、反例或安全闭包定理。
