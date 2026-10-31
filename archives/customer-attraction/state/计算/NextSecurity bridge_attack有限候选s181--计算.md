---
id: "customer-attraction/next-security-bridge-best-s181"
kind: "computation"
type_tag: "计算"
title: "NextSecurity bridge_attack 有限候选 s181"
status: "finite-zero-margin-candidate"
truth_status: "near-equality numerical candidate; no BR failure"
review_level: "full-1250-byte-read"
scope: "k=7,m=5, seed181 stored candidate"
source_refs:
  - "clean:0ebec0f26015db374a38:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_security/bridge_attack/best-k7-m5-s181.json"
  - "local:archives/customer-attraction/state/审查/NextSecurity bridge_attack范围与BR开放边界--审查.md"
source_identity:
  inventory_blob: "7ae6709a67016d160c5bad65ad6238c479f69c0a"
  source_sha256: "2627cadd3a72c95724822d00dac96c8ba7dc29f6fe0d2d3c8966a845ab3dc8b7"
  source_size_bytes: 1250
evidence_paths:
  - "archives/customer-attraction/tools/evidence/next-security-bridge-attack-20261031/original/best-k7-m5-s181.json"
  - "archives/customer-attraction/tools/evidence/next-security-bridge-attack-20261031/comparisons/0ebec0f26015db374a38.md"

# s181

JSON 完整读取。`k=7,m=5,iteration=20`，`W=101`、`v=20.19999999999998`、`ratio=0.9999999999999991`，即 `m v/W` 数值上贴近 1；terminal 为五次主题0。它是等号面候选，未给出正 margin、BR 失败或 CAG 反例。对象处置为 integrated 有限数值记录。
