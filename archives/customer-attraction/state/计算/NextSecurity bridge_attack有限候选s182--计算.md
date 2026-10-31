---
id: "customer-attraction/next-security-bridge-best-s182"
kind: "computation"
type_tag: "计算"
title: "NextSecurity bridge_attack 有限候选 s182"
status: "finite-floating-near-equality"
truth_status: "roundoff-level equality; no BR failure"
review_level: "full-1190-byte-read"
scope: "k=7,m=5, seed182 stored candidate"
source_refs:
  - "clean:8aca340221a9b57475dc:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_security/bridge_attack/best-k7-m5-s182.json"
  - "local:archives/customer-attraction/state/审查/NextSecurity bridge_attack范围与BR开放边界--审查.md"
source_identity:
  inventory_blob: "92abc3f444e7c2ec192d4ac9fa324797859c2d82"
  source_sha256: "bf79440df2672bdee771bdda2c5af1a6b87dc5c1eb47bd94a57e6fe005bb5c7a"
  source_size_bytes: 1190
evidence_paths:
  - "archives/customer-attraction/tools/evidence/next-security-bridge-attack-20261031/original/best-k7-m5-s182.json"
  - "archives/customer-attraction/tools/evidence/next-security-bridge-attack-20261031/comparisons/8aca340221a9b57475dc.md"

# s182

完整读取 JSON：`k=7,m=5,iteration=0`，`W=23`、`v=4.6000000000000005`，`ratio=1.0000000000000002`，terminal 五次主题3。该正差仅为浮点舍入量级，不能当作严格 `m v>W` 或 BR 反例。对象处置为 integrated 有限数值记录。
