---
id: "customer-attraction/R-18-gap-floor-probe"
kind: computation
type_tag: 计算
title: "R-18 gap-floor probe 有限检查"
status: "reduced-replay-no-floor-violation"
truth_status: "finite-random-experiment; no-universal-floor-result"
review_level: "full-1066-byte-read-and-reduced-replay"
scope: "R-18 literature_mechanism/gap_floor_probe.py; reduced rounds (10,5,2) for (m,p)=(3,4),(4,5),(5,7)"
summary: "脚本寻找 m*min_pay < OPT-W 的完整 SPE 候选；浮点/整数 ExactSPESolver 依赖下的缩短回放完成 10、5、2 轮均无候选。严格 violation 需要 factor=(OPT-W)/min_pay>m；本批 sparse JSON 的 factor 2/3/4 均未满足各自 m=3/4/5。"
source_refs:
  - "clean:25a41ee07de97123bfb6:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/literature_mechanism/gap_floor_probe.py"
  - "local:archives/customer-attraction/tools/evidence/R-18-gap-probes-20261031/original/gap_floor_probe.py"
  - "local:archives/customer-attraction/tools/evidence/R-18-gap-probes-20261031/replay/reduced/gap_floor_reduced.stdout.txt"
  - "local:archives/customer-attraction/state/计算/R-18gap-sparse三组最佳记录--计算.md"
  - "local:archives/customer-attraction/tools/evidence/R-18-gap-probes-20261031/comparisons/comparison-notes.md"
source_identity:
  inventory_blob: "ce5a9a7504032010bab3c5d35d4de95767e939df"
  source_sha256: "957f93496d1b0509b119b048bc10d3e058c3f0bebaa04df6bfb8de581161ff7a"
  source_size_bytes: 1066
  frozen_commits:
    - "68fad804ec5946cb296f77dc5b336308a66abf12"
    - "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R-18-gap-probes-20261031/original/gap_floor_probe.py"
  - "archives/customer-attraction/tools/evidence/R-18-gap-probes-20261031/replay/reduced/gap_floor_reduced.stdout.txt"
  - "archives/customer-attraction/tools/evidence/R-18-gap-probes-20261031/comparisons/comparison-notes.md"
---

# R-18 gap-floor probe 有限检查

脚本完整读取 1,066 B，SHA-256 `957f93496d1b0509b119b048bc10d3e058c3f0bebaa04df6bfb8de581161ff7a`，稳定 ID `25a41ee07de97123bfb6`，blob `ce5a9a7504032010bab3c5d35d4de95767e939df`。它对随机客户重数构造 `Instance`，用 `ExactSPESolver` 枚举完整历史终局；若某终局满足

[
m\,\min_{a\in q}u_a < \operatorname{OPT}-W,
]

才写出 `gap_floor_counterexample.json`。等价地，输出里的 `factor=(OPT-W)/min_pay` 必须严格大于 m 才是该 floor 条件的 violation。

我用归档 strategy-cones 的 `customer_attraction` 依赖做缩短回放：((m,p,    ext{rounds})=(3,4,10),(4,5,5),(5,7,2))。stdout 为 `completed 3 4 10`、`completed 4 5 5`、`completed 5 7 2`，无 counterexample JSON。此回放验证的是依赖和逻辑可执行性，不是原脚本声明的 20,000/10,000/1,000 轮完整搜索。

三份 companion sparse JSON 的 factor 分别为 2、3、4，而对应 m 为 3、4、5，均小于严格 floor violation 所需的 m。因此这些 JSON 不能被误标成 gap-floor 反例；它们属于另一脚本的稀疏 best 记录。本对象处置为 integrated 的有限实验检查，不升级 floor 定理、Q-CAG-HALF 或完整反例。
