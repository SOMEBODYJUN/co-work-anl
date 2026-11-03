---
id: "customer-attraction/r18-complete-spe-cone-walk-finite-candidates"
kind: "computation"
type_tag: "计算"
title: "R-18 完整 SPE 策略锥 walk 有限候选"
status: "finite-float-proposals-with-exact-certificate-recovery"
truth_status: "finite search only; no universal half conclusion"
review_level: "full-11291-byte-read-and-30-step-replay"
scope: "m=5,p=7 targeted complete-history SPE cone walk; 30 steps, seed 182026"
source_refs:
  - "clean:08605c4591bbe42073f4:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/counterexample_search/cone_walk.py"
  - "local:archives/customer-attraction/state/资源/完整终局税候选的策略锥浮点反例搜索合同--资源.md"
  - "local:archives/customer-attraction/state/计算/调和福利支付界独立Fraction审计--计算.md"
  - "local:archives/customer-attraction/state/计算/signed-harmonic策略锥LP诊断入口--计算.md"
source_identity:
  inventory_blob: "eaa9cd42f85002d82fc7dd4960960399498d1ea9"
  source_sha256: "766ae31b8049acb3483ae1a0939a3a7030b62236bcff8a74bb6ab36c8177c6d6"
  source_size_bytes: 11291
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R-18-harmonic-counterexample-20261031/original/cone_walk.py"
  - "archives/customer-attraction/tools/evidence/R-18-harmonic-counterexample-20261031/replay/cone_walk.stdout"
  - "archives/customer-attraction/tools/evidence/R-18-harmonic-counterexample-20261031/replay/cone_walk_r30_run.json"
  - "archives/customer-attraction/tools/evidence/R-18-harmonic-counterexample-20261031/replay/cone_walk_r30_best.json"
  - "archives/customer-attraction/tools/evidence/R-18-harmonic-counterexample-20261031/related/customer_attraction/"
  - "archives/customer-attraction/tools/evidence/R-18-harmonic-counterexample-20261031/comparisons/08605c4591bbe42073f4.md"

# R-18 完整 SPE 策略锥 walk 有限候选

## 搜索机制和精确恢复

完整实读 11,291 字节程序。`Engine` 枚举完整有序历史的计数状态、终局 incidence 和客户收益，向后递归保留全部最佳回复终局集合；`strategy` 在不合并有序历史的情况下恢复一份完整纯 SPE，并把每个真实偏离行写成整数收益差。`linprog` 只用于浮点 proposal；`exact_recover` 随后用 Fraction 线性消元恢复整数客户重数，`verify_canonical` 调用完整 `verify_certificate` 检查所有有序历史。

本次以 `--players 5 --topics 7 --steps 30 --seed 182026` 运行，使用既有 `customer_attraction` 包的 exact model。stdout、有限 run JSON 和 exact best JSON 保存在 evidence `replay/`；程序原件未修改。

## 复跑结果

第 0 步先恢复一个 exact ratio `9/5` 的候选，30 个 distinct cone 中最终 `best_exact_ratio=9/5`；run JSON 的 `records` 同时保存每步行数、浮点 input/optimized ratio、portfolio 和 cone SHA。这个 ratio 是 `OPT/W` 的有限候选比值，超过 1 但小于 2；它没有形成 half 反例。

程序在 exact recovery 后保存 `canonical_full_history_verified=true` 的候选实例/策略，说明该候选在其固定 CAG 实例中确为完整历史纯 SPE。它并未对所有实例、所有完整策略或任意客户重数进行穷举，也没有将浮点未恢复 proposal 计入精确证书。

## 处置边界

这是有针对性的有限 cone walk：种子、层化重叠输入和 `m=5,p=7` 均固定。程序自己写明有限搜索不能证明普遍 half；浮点 proposal 与 exact certificate recovery 必须分开。对象处置为 integrated 计算/候选记录，不将 `9/5` 当作目标反例、不把 LP proposal 当精确下界，也不迁移到 unrelated-machines。
