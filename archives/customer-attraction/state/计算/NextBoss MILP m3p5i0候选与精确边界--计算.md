---
id: "customer-attraction/next-boss-milp-m3p5i0"
kind: "computation"
type_tag: "计算"
title: "NextBoss MILP m3p5i0 候选与精确边界"
status: "mixed-optimal-and-time-limit-proposals-with-related-exact-records"
truth_status: "finite numerical candidates; no universal theorem"
review_level: "full-8762-byte-read-and-related-full-tree-audit-comparison"
scope: "players=3, topics=5, player=0, gap objective; two portfolios"
source_refs:
  - "clean:88b4beda4151fde746e7:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_boss/milp_m3p5i0.json"
  - "local:archives/customer-attraction/state/计算/自由终局逐人归一模型的候选与对偶复核--计算.md"
  - "local:archives/customer-attraction/tools/evidence/full-tree-milp-candidate-audits-primary/full-report-compact-read.json"
source_identity:
  inventory_blob: "4c478db21dcd53bfffa1dff930c60ce42a9b2a22"
  source_sha256: "af9bb15e97c365089909f9ff98b79ae06337ea894f1d244e1a1435cc822edead"
  source_size_bytes: 8762
evidence_paths:
  - "archives/customer-attraction/tools/evidence/next-boss-milp-five-20261031/original/milp_m3p5i0.json"
  - "archives/customer-attraction/tools/evidence/next-boss-milp-five-20261031/comparisons/88b4beda4151fde746e7.md"

# m3p5i0

JSON 完整读取 8,762 B。第一 portfolio `[0,1,2]` 返回 status 0/Optimal，variables 654、constraints 1497、objective 2、mip nodes 6990；第二 `[1,2,3]` 返回 status 1/Time limit reached，`mip_gap=0.625`、dual bound `-3.25`，但 incumbent objective proposal 仍为 2。两条结果的源 limitation 都是 numerical MILP proposal。

关联 full-tree exact audit 对两条固定策略记录都给出 exact objective 2、完整 SPE、`W=3`、`OPT=5`、`gap_bridge_slack=1`；这只是 fixed-cone exact reconstruction，不能抹除原第二 proposal 的 time-limit 状态，也不能把数值 MIP dual bound 当精确全局界。两条相关记录均有 `2W-OPT=1`，不构成 half 反例。

对象处置为 integrated 混合状态记录，明确区分 solver status、incumbent proposal 和后续固定锥 exact audit。
