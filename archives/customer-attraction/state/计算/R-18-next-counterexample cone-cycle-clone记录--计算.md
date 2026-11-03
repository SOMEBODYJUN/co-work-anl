---
id: "customer-attraction/R-18-next-counterexample-cone-cycle-clone"
kind: computation
type_tag: 计算
title: "R-18 next-counterexample cone/cycle/clone 记录"
status: "finite-scouting-no-positive-violation"
truth_status: "finite-cone-cycle-clone-proposals; no-real-counterexample"
review_level: "full-json-read-and-search-output-reconciliation"
summary: "pair_cone_best_5_5 objective≈1.39e−17、cycle_best_5 C2 ratio=1、terminal_best m5p5/m7p5 bridge ratio分别1/1和0.81399/half1.00595；均未形成正 gap 或 half 反例。"
source_refs:
  - "local:archives/customer-attraction/tools/evidence/R-18-next-counterexample-20261031/comparisons/comparison-notes.md"
  - "local:archives/customer-attraction/state/计算/R-18-cone候选与cycle记录--计算.md"
  - "local:archives/customer-attraction/state/计算/R-18完整策略锥搜索与clone半桥--计算.md"
source_identity:
  note: "本页聚合解释本批 JSON；各 source IDs 与哈希见对应 receipts。"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R-18-next-counterexample-20261031/original/pair_cone_best_5_5.json"
  - "archives/customer-attraction/tools/evidence/R-18-next-counterexample-20261031/original/cycle_best_5.json"
  - "archives/customer-attraction/tools/evidence/R-18-next-counterexample-20261031/original/terminal_best_5_5.json"
  - "archives/customer-attraction/tools/evidence/R-18-next-counterexample-20261031/original/terminal_best_7_5.json"
  - "archives/customer-attraction/tools/evidence/R-18-next-counterexample-20261031/original/terminal_clone_equality_audit.json"
  - "archives/customer-attraction/tools/evidence/R-18-next-counterexample-20261031/comparisons/comparison-notes.md"
---

完整读取四份候选 JSON 和 clone audit：pair cone objective 约 (1.39\times10^{-17})（数值零）、cycle C2 violation ratio=1、m5p5 terminal bridge ratio=1/half=1、m7p5 bridge ratio=0.813988/half=1.005952。clone equality audit 的 9 条报告全部 `valid=true`，覆盖 m=2…10 的 finite exact regression，但 scope 明确 general proof 由 README analytic argument 承担。

这些记录没有正 cone gap、没有 `bridge_violation_ratio>1`、没有 half ratio 超过 2，也没有生成完整福利反例。它们是有限 scouting/回归数据，需与策略锥 exact verifier 分开。
