---
id: "customer-attraction/next-security-cone-search-tool"
kind: "resource"
type_tag: "资源"
title: "NextSecurity cone_search 有限搜索入口"
status: "source-read-dependency-bound"
truth_status: "finite numerical search tool; dependency boundary retained"
review_level: "full-3469-byte-read"
scope: "k=7,m=5 corrected cone-search implementation"
source_refs:
  - "clean:83cac7213a311617ef54:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_security/bridge_attack/cone_search.py"
  - "local:archives/customer-attraction/state/计算/NextSecurity cone有限候选s184--计算.md"
source_identity:
  inventory_blob: "0b4dff26a5ef950f1da52a6d411f3f2ea19e8298"
  source_sha256: "799568e518d6ad23f0083facd9ff25cc8248a30abaa97f46e8a5f605eba2a012"
  source_size_bytes: 3469
evidence_paths:
  - "archives/customer-attraction/tools/evidence/next-security-bridge-attack-20261031/original/cone_search.py"
  - "archives/customer-attraction/tools/evidence/next-security-bridge-attack-20261031/comparisons/83cac7213a311617ef54.md"

# cone_search.py

完整读取 3,469 B。程序依赖同目录 `search.py` 的 Oracle；本批没有该依赖原件，因此未伪造运行结果。代码保留完整 count-Markov policy、真实偏离 Gamma 行、固定 query LP、w≥0/Gamma w≥0 约束，以及 k=7,m=5 的 seed 变体。它自己把 margin 当浮点 discovery，不提供 exact cone 对偶或一般 BR 证明。

对象处置为 integrated 资源，依赖缺失边界已记录，不迁移到 unrelated-machines。
