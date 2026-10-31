---
id: "customer-attraction/next-boss-milp-m1p2i0"
kind: "computation"
type_tag: "计算"
title: "NextBoss MILP m1p2i0 候选与精确边界"
status: "numerical-milp-read-related-exact-certificate"
truth_status: "trivial finite instances; no universal theorem"
review_level: "full-1592-byte-read-and-related-full-tree-audit-comparison"
scope: "players=1, topics=2, player=0, gap objective; two portfolios"
source_refs:
  - "clean:595223804a6485c53444:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_boss/milp_m1p2i0.json"
  - "local:archives/customer-attraction/state/计算/自由终局逐人归一模型的候选与对偶复核--计算.md"
  - "local:archives/customer-attraction/tools/evidence/full-tree-milp-candidate-audits-primary/full-report-compact-read.json"
source_identity:
  inventory_blob: "11df55bcfa427cbf6937f8599e84b526416ac515"
  source_sha256: "9ad13c1be81545723e9c96eeaa79a3b71952b476bc5432a18b42b97286d6d1ba"
  source_size_bytes: 1592
evidence_paths:
  - "archives/customer-attraction/tools/evidence/next-boss-milp-five-20261031/original/milp_m1p2i0.json"
  - "archives/customer-attraction/tools/evidence/next-boss-milp-five-20261031/comparisons/595223804a6485c53444.md"

# m1p2i0

JSON 完整读取 1,592 B。两个 HiGHS status 0 结果均 `objective_proposal=0`：portfolio `[0]` 的 types `[1,0,0]` 与 portfolio `[1]` 的 types `[1,1,0]`，root utility 都为 1；每个结果变量数 8、约束数 12、mip gap 0。

关联 exact audit 将两条记录都核为完整一人 SPE，`W=OPT=1`、`gap_bridge_slack=1`、fixed-cone exact objective 0。两个 portfolio 只是同一平凡 m=1 案的不同覆盖目标，不是半覆盖或个体桥证据。源 limitation 仍保留，处置为 integrated。
