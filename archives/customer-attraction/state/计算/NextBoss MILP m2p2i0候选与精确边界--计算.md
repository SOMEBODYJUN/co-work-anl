---
id: "customer-attraction/next-boss-milp-m2p2i0"
kind: "computation"
type_tag: "计算"
title: "NextBoss MILP m2p2i0 候选与精确边界"
status: "numerical-milp-proposal-with-fixed-cone-exact-record"
truth_status: "finite candidate; no universal bridge or half theorem"
review_level: "full-1136-byte-read-and-related-full-tree-audit-comparison"
scope: "players=2, topics=2, player=0, gap objective"
source_refs:
  - "clean:f5b29355e7782b55ad74:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_boss/milp_m2p2i0.json"
  - "local:archives/customer-attraction/state/计算/自由终局逐人归一模型的候选与对偶复核--计算.md"
  - "local:archives/customer-attraction/tools/evidence/full-tree-milp-candidate-audits-primary/full-report-compact-read.json"
source_identity:
  inventory_blob: "0d74743a9ac83e6dbb91f0d1b2f76df470168333"
  source_sha256: "c430e8cbda4217984675d744e2b39d78dcc195fefd9407a4d431ddd522529d82"
  source_size_bytes: 1136
evidence_paths:
  - "archives/customer-attraction/tools/evidence/next-boss-milp-five-20261031/original/milp_m2p2i0.json"
  - "archives/customer-attraction/tools/evidence/next-boss-milp-five-20261031/comparisons/f5b29355e7782b55ad74.md"

# m2p2i0

JSON 完整读取 1,136 B。HiGHS status 0/Optimal，portfolio `[0,1]`，`variables=23`、`constraints=44`、`mip_node_count=1`、`objective_proposal=1`，types `[2,1,0]`，动作表 3 行，root utilities `[1,1]`。

关联 exact audit 将该记录重构为 fixed-cone exact objective 1 的完整二人 SPE，实际路径 `[0,0]`，`W=2`、`OPT=3`、`gap_bridge_slack=1`。因此 `2W-OPT=1`，half 仍成立；数值 MILP proposal 不是一般 gap 定理或反例。处置为 integrated 有限候选/精确固定锥记录。
