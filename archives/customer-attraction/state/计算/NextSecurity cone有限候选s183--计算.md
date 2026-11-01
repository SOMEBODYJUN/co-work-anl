---
id: "customer-attraction/next-security-cone-best-s183"
kind: "computation"
type_tag: "计算"
title: "NextSecurity cone 有限候选 s183"
status: "finite-cone-near-zero-margin"
truth_status: "floating cone diagnostic; no positive bridge failure"
review_level: "full-5788-byte-read"
scope: "k=7,m=5, seed183 cone candidate"
source_refs:
  - "clean:187b55d8f6d2c314c238:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_security/bridge_attack/cone-best-k7-m5-s183.json"
  - "local:archives/customer-attraction/state/审查/NextSecurity bridge_attack范围与BR开放边界--审查.md"
source_identity:
  inventory_blob: "8fdd20b6840c97c2b55176a9931e13f52fa2ae87"
  source_sha256: "3d5cf17cf166325cbc645863aeb802214fa3353f38207d2d00d0ae139bc968c9"
  source_size_bytes: 5788
evidence_paths:
  - "archives/customer-attraction/tools/evidence/next-security-bridge-attack-20261031/original/cone-best-k7-m5-s183.json"
  - "archives/customer-attraction/tools/evidence/next-security-bridge-attack-20261031/comparisons/187b55d8f6d2c314c238.md"

# s183

完整读取 JSON。`margin=-0.0`、uniform query、root `[4,0,0,0,0,0,1]`，w 向量为浮点 LP 锥解，且 README 说明 seed183 的补集索引括号历史上有误。它不是正候选、不是 exact cone certificate，也不证明 BR。处置为 integrated 有限诊断。
