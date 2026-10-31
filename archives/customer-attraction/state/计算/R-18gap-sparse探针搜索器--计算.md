---
id: "customer-attraction/R-18-gap-sparse-probe"
kind: computation
type_tag: 计算
title: "R-18 gap-sparse 探针搜索器"
status: "reduced-replay-exact-sparse-search"
truth_status: "finite-sparse-experiment; no-universal-bound"
review_level: "full-2515-byte-read-and-reduced-replay"
scope: "R-18 literature_mechanism/gap_sparse_probe.py; Fraction SPE max-min recursion and sparse mutation search"
summary: "脚本用 LCM/Fraction 计算可信终局集合与 sparse best factor，原配置每组 5,000 轮；本轮每组缩短为 10 轮，首轮产生 factor 2/3/4、W 9/12/15、OPT 15/21/27。它是有限 sparse search，不是一般 factor 上界或 SPE 定理。"
source_refs:
  - "clean:01be6b7ef76d2362b2db:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/literature_mechanism/gap_sparse_probe.py"
  - "local:archives/customer-attraction/tools/evidence/R-18-gap-probes-20261031/original/gap_sparse_probe.py"
  - "local:archives/customer-attraction/tools/evidence/R-18-gap-probes-20261031/replay/reduced/gap_sparse_reduced.stdout.txt"
  - "local:archives/customer-attraction/tools/evidence/R-18-gap-probes-20261031/replay/reduced/gap_sparse_results.json"
  - "local:archives/customer-attraction/state/计算/R-18gap-sparse三组最佳记录--计算.md"
  - "local:archives/customer-attraction/state/计算/R-18-gap-floor-probe有限检查--计算.md"
  - "local:archives/customer-attraction/tools/evidence/R-18-gap-probes-20261031/comparisons/comparison-notes.md"
source_identity:
  inventory_blob: "eecada283caeae276561c3a9ba53a96ee189f3be"
  source_sha256: "9845ae5847a1a43921e8ee180b36deddbbed4f996a0d37c2df60b9738fa55bf4"
  source_size_bytes: 2515
  frozen_commits:
    - "68fad804ec5946cb296f77dc5b336308a66abf12"
    - "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R-18-gap-probes-20261031/original/gap_sparse_probe.py"
  - "archives/customer-attraction/tools/evidence/R-18-gap-probes-20261031/replay/reduced/gap_sparse_reduced.stdout.txt"
  - "archives/customer-attraction/tools/evidence/R-18-gap-probes-20261031/replay/reduced/gap_sparse_results.json"
  - "archives/customer-attraction/tools/evidence/R-18-gap-probes-20261031/comparisons/comparison-notes.md"
---

# R-18 gap-sparse 探针搜索器

脚本完整实读 2,515 B，SHA-256 `9845ae5847a1a43921e8ee180b36deddbbed4f996a0d37c2df60b9738fa55bf4`，稳定 ID `01be6b7ef76d2362b2db`，blob `eecada283caeae276561c3a9ba53a96ee189f3be`。对每个随机质量向量，`spe(q)` 用 LCM 缩放效用递归构造可信终局集合：每个动作保留达到所有孩子集合的 max-min floor 的终局，再从根的可信集合中最大化

[
\frac{(\operatorname{OPT}-W)\,\mathrm{LCM}(1,\dots,m)}{\min_{a\in q}u_a}.
]

`OPT` 在全部主题计数组合 `comps(m,p)` 上取最大覆盖；搜索先用固定稀疏 singleton 结构，再每 20 轮重置 singleton、每轮随机扰动少量 mask，保留当前 best。达到 `factor>m` 时程序打印 `FAIL` 并退出；否则写出三组 best JSON。

本轮每组执行 10 轮缩短回放，stdout 为 `best 3 4 0 2 9 15 15`、`best 4 5 0 3 12 21 21`、`best 5 7 0 4 15 27 27`；没有 `FAIL`。原脚本声明的每组 5,000 轮并未在本轮重跑，故不能把缩短搜索称为完整阴性结果。

三组记录的 factor 分别是 m−1，且比率 OPT/W 分别 5/3、7/4、9/5，均不构成 `2W<OPT`。与 gap-floor 脚本的严格条件 factor>m 区分后，本对象处置为 integrated 的有限 sparse 搜索工具；不升级一般 factor 上界、Q-CAG-HALF、完整 SPE 反例或 unrelated-machines。
