---
id: "customer-attraction/next-security-menu-cone-best-s185"
kind: "computation"
type_tag: "计算"
title: "NextSecurity on-path menu cone 候选 s185"
status: "finite-on-path-menu-candidate"
truth_status: "not-full-BR; no bridge failure"
review_level: "full-5992-byte-read"
scope: "k=7,m=5 on-path first-deviation menu only"
source_refs:
  - "clean:40e744a6ff551c2e0121:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_security/bridge_attack/menu-cone-best-185.json"
  - "local:archives/customer-attraction/state/审查/NextSecurity bridge_attack范围与BR开放边界--审查.md"
source_identity:
  inventory_blob: "2ee2a2f9c85c3aa6d7c4bbc41009295b2317f953"
  source_sha256: "536323a220515920c6c82bb335c81f8f9f94ddcb98b58278f9badae03a209dec"
  source_size_bytes: 5992
evidence_paths:
  - "archives/customer-attraction/tools/evidence/next-security-bridge-attack-20261031/original/menu-cone-best-185.json"
  - "archives/customer-attraction/tools/evidence/next-security-bridge-attack-20261031/comparisons/40e744a6ff551c2e0121.md"

# s185

完整读取 JSON。scope 明确是 `only on-path first-deviation menu, not full BR`；k=7,m=5，gap=`-0.0`，uniform query，root `[0,0,0,0,1]`，menu 只有两行。该对象没有涵盖全部在轨节点或全树偏离，故不能用来证明或反驳 BR。处置为 integrated 有限 on-path 候选。
