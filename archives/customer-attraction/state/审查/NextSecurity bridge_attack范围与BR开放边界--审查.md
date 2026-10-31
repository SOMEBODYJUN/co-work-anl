---
id: "customer-attraction/next-security-bridge-attack-scope-review"
kind: "review"
type_tag: "审查"
title: "NextSecurity bridge_attack 范围与 BR 开放边界"
status: "finite-search-scope-reviewed"
truth_status: "CAG bridge and Q-CAG-HALF remain open"
review_level: "full-4596-byte-read-and-related-search-comparison"
scope: "CAG-MODEL BR W>=m v_m; reduction/cap observations and finite numerical searches"
source_refs:
  - "clean:6e952aa8354114d160ab:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_security/bridge_attack/README.md"
  - "local:archives/customer-attraction/state/定理/静态独立同分布安全基准--定理.md"
  - "local:archives/customer-attraction/state/计算/R-18占用背景安全有限审计--计算.md"
  - "local:archives/customer-attraction/state/计算/自由终局逐人归一模型的候选与对偶复核--计算.md"
source_identity:
  inventory_blob: "9e66fbb62272459acacd82338b7beefc61605a48"
  source_sha256: "96e1682c3cff3aab1f60321fbc88226edb8547612db3b4d7c7cef65b1dba44c3"
  source_size_bytes: 4596
evidence_paths:
  - "archives/customer-attraction/tools/evidence/next-security-bridge-attack-20261031/original/README.md"
  - "archives/customer-attraction/tools/evidence/next-security-bridge-attack-20261031/comparisons/6e952aa8354114d160ab.md"

# NextSecurity bridge_attack 范围

README 明确模型是 CAG-MODEL，目标辅助桥 `W≥m v_m` 与 Q-CAG-HALF 均未解决。SC-RED-FULL-INTEREST 的全兴趣类型删除保持 `W-mv_m` 不变；SC-CAP-IID 给 `mv_m≤OPT_m` 的基本上界。这两条只是解析观察，不能支付早期安全值或推出 half。

其余内容是有限 numerical discovery：k=7,m=5 随机/局部搜索、随机 count-Markov cone、seed183/184 的 near-zero margin、已知 games 的 first-deviation menu 与有限 MILP。README 自己明确浮点输出、零反例实验和有限候选不构成一般排除定理；本页不把 CAG 与更宽 abstract-potential 对象混同。

对象处置为 integrated 范围审查；后续仍需共同菜单或真实全树支付机制，不迁移到 unrelated-machines。
