---
id: "customer-attraction/R-18-terminal-clone-equality-audit"
kind: computation
type_tag: 计算
title: "R-18 terminal clone equality 审计"
status: "finite-exact-regression-passed"
truth_status: "finite-exact-regression; analytic general proof external"
review_level: "full-2368-byte-read"
source_refs:
  - "clean:fb8540bc2e41ff59f186:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_counterexample/terminal_clone_equality_audit.json"
  - "local:archives/customer-attraction/tools/evidence/R-18-next-counterexample-20261031/original/terminal_clone_equality_audit.json"
  - "local:archives/customer-attraction/tools/evidence/R-18-next-counterexample-20261031/comparisons/comparison-notes.md"
source_identity:
  inventory_blob: "0e8e655a44eb392c4bc1e4418684dd9ed46aeccb"
  source_sha256: "ffda09f1b7df455f91caf208968e0f80aa558dcaf606377f524fc58cf0f7810"
  source_size_bytes: 2368
  frozen_commits: ["68fad804ec5946cb296f77dc5b336308a66abf12", "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"]
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R-18-next-counterexample-20261031/original/terminal_clone_equality_audit.json"
  - "archives/customer-attraction/tools/evidence/R-18-next-counterexample-20261031/comparisons/comparison-notes.md"
---

JSON scope 是 `finite exact regression; general proof is analytic in README`。9 条报告覆盖 m=2…10，每条 `valid=true`；客户数 m+1，welfare=OPT=m+1，histories/deviations 分别达到 (2^m-1) 规模。它是 clone equality 的有限审计输出，未提供全局 analytic proof 本身，不能冒充 Q-CAG-HALF 或完整反例。
