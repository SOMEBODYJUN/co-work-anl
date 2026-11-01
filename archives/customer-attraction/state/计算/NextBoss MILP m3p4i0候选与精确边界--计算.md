---
id: "customer-attraction/next-boss-milp-m3p4i0"
kind: "computation"
type_tag: "计算"
title: "NextBoss MILP m3p4i0 候选与精确边界"
status: "numerical-milp-proposals-with-fixed-cone-exact-records"
truth_status: "finite candidates; half holds at related exact records"
review_level: "full-6275-byte-read-and-related-full-tree-audit-comparison"
scope: "players=3, topics=4, player=0, gap objective; two portfolios"
source_refs:
  - "clean:c56d65e673ba2a13bc6b:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_boss/milp_m3p4i0.json"
  - "local:archives/customer-attraction/state/计算/自由终局逐人归一模型的候选与对偶复核--计算.md"
  - "local:archives/customer-attraction/tools/evidence/full-tree-milp-candidate-audits-primary/full-report-compact-read.json"
source_identity:
  inventory_blob: "b71bb42f467e462e496f221bafeacd1bcb9b1d63"
  source_sha256: "f2371caeee5917453f1dcd3103840215168c07b2e4f7d35bb28d3107edd94de7"
  source_size_bytes: 6275
evidence_paths:
  - "archives/customer-attraction/tools/evidence/next-boss-milp-five-20261031/original/milp_m3p4i0.json"
  - "archives/customer-attraction/tools/evidence/next-boss-milp-five-20261031/comparisons/c56d65e673ba2a13bc6b.md"

# m3p4i0

JSON 完整读取 6,275 B。两个 HiGHS 结果均 status 0/Optimal，portfolio 分别 `[0,1,2]` 与 `[1,2,3]`，变量 354、约束 806，objective proposals `2` 与 `2.0000000000000004`；每条动作表有 21 个节点，root utilities 约为 1。

关联 full-tree exact audit 将两条候选都核为 fixed-cone exact objective 2 的完整三人 SPE：各自 `W=3`、`OPT=5`、`gap_bridge_slack=1`，half 余量 `2W-OPT=1`。这说明数值 MILP 候选并不是 half 反例，也不证明所有三人策略满足同一 bound；处置为 integrated 有限候选/精确固定锥记录。
