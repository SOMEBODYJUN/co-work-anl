---
id: "customer-attraction/next-security-cone-best-s184"
kind: "computation"
type_tag: "计算"
title: "NextSecurity cone 有限候选 s184"
status: "finite-cone-roundoff-margin"
truth_status: "roundoff-level positive; no exact bridge failure"
review_level: "full-5807-byte-read"
scope: "k=7,m=5, seed184 corrected cone candidate"
source_refs:
  - "clean:2648475511709fc9736c:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_security/bridge_attack/cone-best-k7-m5-s184.json"
  - "local:archives/customer-attraction/state/审查/NextSecurity bridge_attack范围与BR开放边界--审查.md"
source_identity:
  inventory_blob: "6d9679bbbd40cb328402840368b93258dc9f9fa4"
  source_sha256: "96b244d09171c70ceae5329e6cf48b3d353de2d3d24372c05451a5aeff9552b6"
  source_size_bytes: 5807
evidence_paths:
  - "archives/customer-attraction/tools/evidence/next-security-bridge-attack-20261031/original/cone-best-k7-m5-s184.json"
  - "archives/customer-attraction/tools/evidence/next-security-bridge-attack-20261031/comparisons/2648475511709fc9736c.md"

# s184

完整读取 JSON：`margin=1.1102230246251565e-16`，uniform query，k=7,m=5。该数值是 double roundoff 量级，不是 exact positive bridge failure；w、policy layers 也只是浮点 cone proposal。对象处置为 integrated 有限诊断。
