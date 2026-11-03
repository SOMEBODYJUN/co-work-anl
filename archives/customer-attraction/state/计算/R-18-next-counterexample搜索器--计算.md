---
id: "customer-attraction/R-18-next-counterexample-searchers"
kind: computation
type_tag: 计算
title: "R-18 next-counterexample 搜索器"
status: "finite-search-tools-read-and-terminal-replay"
truth_status: "finite-scouting-tools; no-universal-result"
review_level: "full-script-read-and-reduced-search_terminal-replay"
summary: "cycle_family_search.py、pair_cone_attack.py、search_clone_half.py 依赖 Scout/search_terminal；本轮不伪造缺失依赖。search_terminal.py 可独立运行，m5p5 20 步与 m7p5 10 步回放均未得到 ratio>1 的 bridge violation，half ratio最高约1.0936/1.0067。"
source_refs:
  - "local:archives/customer-attraction/tools/evidence/R-18-next-counterexample-20261031/original/cycle_family_search.py"
  - "local:archives/customer-attraction/tools/evidence/R-18-next-counterexample-20261031/original/pair_cone_attack.py"
  - "local:archives/customer-attraction/tools/evidence/R-18-next-counterexample-20261031/original/search_clone_half.py"
  - "local:archives/customer-attraction/tools/evidence/R-18-next-counterexample-20261031/original/search_terminal.py"
  - "local:archives/customer-attraction/tools/evidence/R-18-next-counterexample-20261031/replay/search_terminal_5_5.stdout.txt"
  - "local:archives/customer-attraction/tools/evidence/R-18-next-counterexample-20261031/replay/search_terminal_7_5.stdout.txt"
  - "local:archives/customer-attraction/tools/evidence/R-18-next-counterexample-20261031/comparisons/comparison-notes.md"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R-18-next-counterexample-20261031/comparisons/comparison-notes.md"
---

完整实读四个脚本。前三个依赖 `Scout/search_terminal`，本批没有可运行依赖，故不伪造执行；代码只把 LP/cycle/clone 输出作为候选，未形成 exact certificate。`search_terminal.py` 为标准库/numpy self-contained Scout，实际回放 m=5,n=5 20 步和 n=7,m=5 10 步：m5p5 bridge best=0.6、half ratio峰值约1.0936；m7p5 bridge best≈0.58598、half约1.00674。均未触发正 bridge violation 或 half 反例门槛。
