---
id: "customer-attraction/R-18-cone-cycle-records"
kind: computation
type_tag: 计算
title: "R-18 cone 候选与 cycle 记录"
status: "finite-cone-and-cycle-no-positive-violation"
truth_status: "finite-LP-scouting; no-real-counterexample"
review_level: "full-912-2938-345-byte-read"
summary: "cone_best_5_5 objective=-0.0625、cone_best_7_5 objective=-0.01886，均无正 gap；cycle_best_5 C2_violation_ratio=1、half_ratio=1。它们是有限 cone/cycle 候选记录，不是真实 half 反例。"
source_refs:
  - "clean:b11182f2a1d2dd4b5597:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_counterexample/cone_best_5_5.json"
  - "clean:1f622e0805b6cea2e66f:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_counterexample/cone_best_7_5.json"
  - "clean:60c6ec5af123aa5f5ab3:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_counterexample/cycle_best_5.json"
  - "local:archives/customer-attraction/tools/evidence/R-18-cone-cycle-20261031/comparisons/comparison-notes.md"
source_identity:
  records:
    - id: "b11182f2a1d2dd4b5597"
      blob: "5c9e504a96057a11424c080cadd804afc3641e97"
      sha256: "6812b7ee258478ea2c65ab364ec5133fc010de01c21b9625eecebc91c317d391"
      size_bytes: 912
    - id: "1f622e0805b6cea2e66f"
      blob: "9217d9280817d662d2471e7e269f175f21dd3d63"
      sha256: "ffd191cb28397835a744361944b5e5e2a8e6436fea309651277386b00b44ee5e"
      size_bytes: 2938
    - id: "60c6ec5af123aa5f5ab3"
      blob: "ba3d84c838661a686d53e7ef70380766972a8436"
      sha256: "b7a92543f63fba46733028b892448c248b9e0a72054354ba4dfb8b255cbb65e5"
      size_bytes: 345
  frozen_commits: ["68fad804ec5946cb296f77dc5b336308a66abf12", "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"]
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R-18-cone-cycle-20261031/original/cone_best_5_5.json"
  - "archives/customer-attraction/tools/evidence/R-18-cone-cycle-20261031/original/cone_best_7_5.json"
  - "archives/customer-attraction/tools/evidence/R-18-cone-cycle-20261031/original/cycle_best_5.json"
  - "archives/customer-attraction/tools/evidence/R-18-cone-cycle-20261031/comparisons/comparison-notes.md"
---

# R-18 cone 候选与 cycle 记录

三个 JSON 完整读取：

| JSON | 参数/记录 | 结果 |
|---|---|---|
| cone_best_5_5 | n=5,m=5，iteration 0，path [2,0,0,0,0]，early_index 3，408 rows | objective `-0.06249999999999999` |
| cone_best_7_5 | n=7,m=5，iteration 416，path [5,0,0,0,4]，early_index 2，1706 rows | objective `-0.018860612513786672` |
| cycle_best_5 | m=5，iteration 27，path [2,0,0,0,0] | C2_violation_ratio=1，half_ratio=1 |

两个 cone objective 都为负，说明保存的 fixed cone LP 没有找到正的早期/末位 gap 方向；cycle 记录也没有超出 1 的 violation ratio。seed weights 与 LP weights 均保存在原 JSON，可用于后续复核，但这些记录没有形成 exact integer customer certificate 或完整 SPE 反例。

与已有 strategy-cone/full-tree 结果一致：浮点 LP 只是候选生成器，正 objective 还必须经过整数恢复、完整有序历史验证和 welfare/OPT 重算。本批没有正 objective 或 ratio>1 的 cycle。
