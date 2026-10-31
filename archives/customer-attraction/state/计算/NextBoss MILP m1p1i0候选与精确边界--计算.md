---
id: "customer-attraction/next-boss-milp-m1p1i0"
kind: "computation"
type_tag: "计算"
title: "NextBoss MILP m1p1i0 候选与精确边界"
status: "numerical-milp-read-related-exact-certificate"
truth_status: "trivial finite instance; no universal theorem"
review_level: "full-898-byte-read-and-related-full-tree-audit-comparison"
scope: "players=1, topics=1, player=0, gap objective"
source_refs:
  - "clean:227366498f86ecfdd4b2:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_boss/milp_m1p1i0.json"
  - "local:archives/customer-attraction/state/计算/自由终局逐人归一模型的候选与对偶复核--计算.md"
  - "local:archives/customer-attraction/tools/evidence/full-tree-milp-candidate-audits-primary/full-report-compact-read.json"
source_identity:
  inventory_blob: "d71c49abb333d082684045c9c2f1dc15a8d1bc18"
  source_sha256: "bea526f2d72918b4ad5073491ac83698f9f85534343e6d6970f2b80e8e7ff2e4"
  source_size_bytes: 898
evidence_paths:
  - "archives/customer-attraction/tools/evidence/next-boss-milp-five-20261031/original/milp_m1p1i0.json"
  - "archives/customer-attraction/tools/evidence/next-boss-milp-five-20261031/comparisons/227366498f86ecfdd4b2.md"

# m1p1i0

JSON 完整读取 898 B。HiGHS 返回 status 0/Optimal，`variables=4`、`constraints=7`、portfolio `[0]`、`fun=0`、`objective_proposal=-0.0`、root utility `[1]`。源文件自己声明这是 numerical MILP proposal，不是 exact/general theorem。

关联 full-tree exact audit 将该记录重构为一客户一主题完整 SPE：固定策略锥目标为 0，`W=1`、`OPT=1`、`gap_bridge_slack=1`，完整历史 SPE 为真。它是平凡基线，既不产生 gap，也不触碰 half 障碍；不把 MILP status 当成一般证明。对象处置为 integrated 计算记录。
