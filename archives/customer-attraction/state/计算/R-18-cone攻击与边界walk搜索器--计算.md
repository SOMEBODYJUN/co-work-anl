---
id: "customer-attraction/R-18-cone-attack-walk-tools"
kind: computation
type_tag: 计算
title: "R-18 cone 攻击与边界 walk 搜索器"
status: "finite-LP-scouting-tools"
truth_status: "finite-cone-candidate-generators; no-universal-result"
review_level: "full-3077-2784-byte-read"
summary: "cone_attack.py 与 cone_walk.py 在可信策略 cone 上构造 LP rows，要求正 objective 后再做 exact/integer audit；本批保存的 best/cycle JSON 未出现正 gap。它们是有限工具，不是求解器或反例证明。"
source_refs:
  - "clean:08868cd8604deaef5536:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_counterexample/cone_attack.py"
  - "clean:8abd9e3c265173dfb777:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_counterexample/cone_walk.py"
  - "local:archives/customer-attraction/tools/evidence/R-18-cone-cycle-20261031/original/cone_attack.py"
  - "local:archives/customer-attraction/tools/evidence/R-18-cone-cycle-20261031/original/cone_walk.py"
  - "local:archives/customer-attraction/tools/evidence/R-18-cone-cycle-20261031/comparisons/comparison-notes.md"
source_identity:
  records:
    - id: "08868cd8604deaef5536"
      blob: "69fc78866ce465bf0ef6e860aa4be892748bd795"
      sha256: "d01883b0d749b19f90e9b8b260c94aac5cb5b5377faaecbb284515e51074af74"
      size_bytes: 3077
    - id: "8abd9e3c265173dfb777"
      blob: "5891485e864f11b392e988640ea74cfbeded6b2a"
      sha256: "6f8583af9b9fb1c8d52bcf1e5c624c930e96bf03bb6243faa53448294dab2623"
      size_bytes: 2784
  frozen_commits: ["68fad804ec5946cb296f77dc5b336308a66abf12", "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"]
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R-18-cone-cycle-20261031/original/cone_attack.py"
  - "archives/customer-attraction/tools/evidence/R-18-cone-cycle-20261031/original/cone_walk.py"
  - "archives/customer-attraction/tools/evidence/R-18-cone-cycle-20261031/comparisons/comparison-notes.md"
---

完整实读两个脚本。`cone_attack.py` 从 Scout 生成可信 continuation sets、路径和 exact row constraints，再对每个 early index 解 fixed-cone LP；只有正 objective 才写出 cone_best JSON。`cone_walk.py` 在边界 walk 中随机选择 admissible actions/lowest replies，支持 `half` 与其他 mode，仍只记录 LP proposal。

两个工具都依赖缺失的 `search_terminal.py`/Scout 实现，本轮未宣称独立重跑；冻结 JSON 已完整复核。其 docstring 和代码结构都把 LP 当 scouting，后续 exact/integer independent audit 是必要门槛。处置为 integrated 有限工具，不升级算法、hardness 或 Q-CAG-HALF。
