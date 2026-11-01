---
id: "customer-attraction/R-18-symmetric-projection-prefix-obstruction"
kind: review
type_tag: 审查
title: "R-18 对称投影完整 SPE 前缀障碍"
status: "exact-prefix-obstruction-replayed"
truth_status: "exact-obstruction-to-one-desired-root-path; not-global-counterexample"
review_level: "full-2876-byte-read-and-exact-replay"
scope: "counterexample_search/symmetric_projection_audit.py; symmetric 15-topic projection from indexed 64-atom primal"
summary: "Exact audit 在 desired ABCDE 路径上于 prefix ABC 找到不可实现的 SPE continuation：actual payoff 19831685067346891812683589221782153022719200，threshold 24094213092687700447836737606884941913569120，margin negative；V,W,X,Y,T1..T5 九个偏离在每个 SPE reply 下都严格盈利。它否定的是该指定根路径/投影 realization，不是所有 15-topic 实例或 Q-CAG-HALF。"
source_refs:
  - "clean:83b29244c281cae6b652:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/counterexample_search/symmetric_projection_audit.py"
  - "local:archives/customer-attraction/tools/evidence/R-18-counterexample-search-20261031/original/symmetric_projection_audit.py"
  - "local:archives/customer-attraction/tools/evidence/R-18-counterexample-search-20261031/replay/symmetric-audit/stdout.txt"
  - "local:archives/customer-attraction/tools/evidence/R-18-counterexample-search-20261031/replay/symmetric-audit/symmetric_projection_exact_obstruction.json"
  - "local:archives/customer-attraction/state/计算/R-18对称投影m5p15完整证书复核--计算.md"
  - "local:archives/customer-attraction/tools/evidence/R-18-counterexample-search-20261031/comparisons/comparison-notes.md"
source_identity:
  inventory_blob: "3276e4804dce2d2960b21a2be1a7f61ef6830657"
  source_sha256: "765332d082cc21070889df50426f69e23d87d8bf29165ffedf9f5582b13fbaec"
  source_size_bytes: 2876
  frozen_commits:
    - "68fad804ec5946cb296f77dc5b336308a66abf12"
    - "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R-18-counterexample-search-20261031/original/symmetric_projection_audit.py"
  - "archives/customer-attraction/tools/evidence/R-18-counterexample-search-20261031/replay/symmetric-audit/stdout.txt"
  - "archives/customer-attraction/tools/evidence/R-18-counterexample-search-20261031/replay/symmetric-audit/symmetric_projection_exact_obstruction.json"
  - "archives/customer-attraction/tools/evidence/R-18-counterexample-search-20261031/comparisons/comparison-notes.md"
---

# R-18 对称投影完整 SPE 前缀障碍

## 精确重放

脚本完整读取 2,876 B，SHA-256 `765332d082cc21070889df50426f69e23d87d8bf29165ffedf9f5582b13fbaec`，稳定 ID `83b29244c281cae6b652`，blob `3276e4804dce2d2960b21a2be1a7f61ef6830657`。它从冻结 `five_player_indexed_bound.json` 的 64 atom primal 构造 15 主题对称投影，使用 `ExactSPESolver` 和 Fraction 检查 desired root `(1,1,1,1,1)+(0,)*10` 的深层前缀。

重放首先确认 prefix `ABCD` 的 desired continuation SPE feasible，实际 payoff 与 threshold 相等，outcome_count=11。继续到 prefix `ABC` 时 desired continuation 不可行，outcome_count=1；实际选择动作 D 的 payoff 与阈值差为

[
19831685067346891812683589221782153022719200
-24094213092687700447836737606884941913569120
=-4262528025340808635153148385102788890849920.
]

在该 prefix 下，V、W、X、Y、T1、T2、T3、T4、T5 九个偏离都满足“在每个 SPE reply 下的最低收益严格高于 actual”，最小 gain 分别由 replay JSON 完整保存。故指定的 ABCDE 根路径不能由一份完整历史 SPE 实现。

## 边界

这是对一个具体对称 projection 和一个 desired root path 的 exact obstruction。它比浮点 proposal 强，因为使用 Fraction 和 canonical ExactSPESolver；但它没有排除其他根路径、其他客户质量、其他 projection、其他平局或一般 15 主题实例。大 JSON 的 symmetric best 本身 W=OPT=1；本障碍也不是 `2W<OPT` 福利反例。

本对象处置为 integrated 的 exact-prefix obstruction；不升级为 Q-CAG-HALF 反例、一般投影不可能性或 unrelated-machines 结论。
