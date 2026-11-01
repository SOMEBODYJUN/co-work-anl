---
id: "customer-attraction/next-security-first-deviation-known-games"
kind: "computation"
type_tag: "计算"
title: "NextSecurity 已知游戏首偏离菜单"
status: "finite-known-game-menu-record"
truth_status: "all stored ratios below one; no BR failure"
review_level: "full-3690-byte-read"
scope: "Known CAG records and first-deviation menu cap ratios"
source_refs:
  - "clean:d6fb97872270eabaf31c:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_security/bridge_attack/first_deviation_menu_known_games.json"
  - "local:archives/customer-attraction/state/审查/NextSecurity bridge_attack范围与BR开放边界--审查.md"
source_identity:
  inventory_blob: "860a843f7ef50fd93ca8be6f210551b66538d97f"
  source_sha256: "2ad0f47a7e681d3814f7409afd2a4f895c954f78c630fbd581d8612abc218d2e"
  source_size_bytes: 3690
evidence_paths:
  - "archives/customer-attraction/tools/evidence/next-security-bridge-attack-20261031/original/first_deviation_menu_known_games.json"
  - "archives/customer-attraction/tools/evidence/next-security-bridge-attack-20261031/comparisons/d6fb97872270eabaf31c.md"

# 已知游戏菜单记录

完整读取 JSON。记录 optimal-last-query、global-decorrelation、local-security、root-stationary、individual、five-individual、root-tax、aggregate-theta、empirical-iid 等已知游戏；每条 `ratio_mcap_W` 均小于或等于 1，最高约 `0.9980756895`。这些是已知实例的菜单 cap 与 W 比值，不是新的全树证明。

对象处置为 integrated 有限资料/计算记录；不把这些非正差值升级为 BR 或 Q-CAG-HALF 证明。
