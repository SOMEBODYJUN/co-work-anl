---
id: "customer-attraction/R-18-walk-m5p7-best"
kind: computation
type_tag: 计算
title: "R-18 walk m5p7 最佳完整 SPE"
status: "finite-exact-walk-candidate"
truth_status: "one-verified-full-history-SPE; ratio-below-half"
review_level: "full-331160-byte-read-and-instance-recalculation"
scope: "counterexample_search/walk_m5p7_best.json; 5 players, 7 topics"
summary: "canonical_full_history_verified=true；重算 W=5、OPT=9、ratio=9/5，portfolio [0,1,2,3,4]。有限完整 SPE 候选但不是 half 反例。"
source_refs:
  - "clean:daf1b2e40a5c83fa5223:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/counterexample_search/walk_m5p7_best.json"
  - "local:archives/customer-attraction/tools/evidence/R-18-counterexample-search-walks-20261031/original/walk_m5p7_best.json"
  - "local:archives/customer-attraction/tools/evidence/R-18-counterexample-search-walks-20261031/comparisons/comparison-notes.md"
source_identity:
  inventory_blob: "2fa6f71c208d206509edbc80dfd9d7a727b356a3"
  source_sha256: "f5800bde7c51f12db89d9eefbf1aa3a0981b0acfcc638f18f4701ba4084419e2"
  source_size_bytes: 331160
  frozen_commits: ["68fad804ec5946cb296f77dc5b336308a66abf12", "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"]
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R-18-counterexample-search-walks-20261031/original/walk_m5p7_best.json"
  - "archives/customer-attraction/tools/evidence/R-18-counterexample-search-walks-20261031/comparisons/comparison-notes.md"
---

完整读取 331,160 B。实例有 5 人、7 主题、5 客户类型：单例 1/2/4 各 1、[0,5] 重数 5、[3,6] 重数 1；终局五次主题 0。canonical Instance 重算 (W=5,OPT=9,OPT/W=9/5)。JSON 标记完整历史验证通过，portfolio 为 [0,1,2,3,4]，因此这是一个已验证端点而非全局反例。
