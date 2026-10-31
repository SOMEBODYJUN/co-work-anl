---
id: "unrelated-machines/optimal-hull-closed-cycle-k3d1-input-review"
kind: "review"
type_tag: "审查"
title: "最优凸包闭环 k=3,d=1 输入夹具审查"
status: "integrated-into-existing-finite-review"
truth_status: "input-fixture-only"
review_level: "full-json-read-and-source-hash-check"
scope: "unrelated-machines optimal-hull closed-cycle k=3,d=1 fixture; finite audit linkage only"
source_sha256: "d531ad742ed8b37b4ddd98da8ef187b10d80ddbdd164f5209c3747d1f73cab0a"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:examples/unrelated_machines/optimal_hull_closed_cycle_k3d1.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:examples/unrelated_machines/optimal_hull_closed_cycle_k3d1.json"
---

# 读取与对象边界

该 JSON 是 unrelated-machines 的 `optimal_hull_closed_cycle` 输入夹具，不含策略、调度分配或审计结论。它声明 `k=3,d=1`，7 台机器 `r,h0_0,h1_0,h2_0,h3_0,h3_1,h3_2`，10 个任务 `g0,e0_0,g1,e1_0,g2,e2_0,g3,e3_0,e3_1,e3_2`；未列出的 machine-job 边均 unavailable。

可用边的处理时间全部是有理数：主任务 `g0,g1,g2,g3` 分别在根/局部机器上给出 `1/4,2/9,2/9,2/3` 与局部时间 1；各 `e` 任务给出 `2/3` 局部时间及根/后继时间 `1/18,1/9,1/9`，末组三个 `e3` 在链式机器上分别为 `2/3,1` 和最后回根 `1/9`。这些数值定义闭环局部路径和 slot 成本输入。

# 与已有有限审计的关系

已有《最优凸包长链与闭环逃逸有限审查》承载该输入对应的 `optimal_hull_closed_cycle_audit`：`k=3,d=1` 全枚举 1,024 个合法分配，最优值 1，坏状态为 `7/6`，最小单任务首步峰值为 `23/18`，超出 `1/9`。该审计还覆盖 `k=3,d=2`、`k=4,d=1`，以及 `k=4,d=2`、`k=5,d=1` 的独立 owner/tie-order 检查。

本 JSON 仅提供输入；不能单独推出上述枚举结论，也不能推出一般 rounding、全局配置 LP、近二保证或任何 customer-attraction 六人结论。闭环与长链保持不同对象。

# 处置

来源应标为 `integrated` 到既有闭环审查对象，原始输入复制到 `archives/unrelated-machines/tools/evidence/clean-batch-config-certificates/input-fixtures/optimal_hull_closed_cycle_k3d1.json`，哈希映射见同目录 `manifest.json`。
