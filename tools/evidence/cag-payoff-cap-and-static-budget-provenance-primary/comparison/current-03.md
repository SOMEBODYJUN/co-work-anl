---
id: "customer-attraction/harmonic-payoff-cap-independent-fraction-audit"
kind: "computation"
type_tag: "计算"
title: "调和福利支付界独立 Fraction 审计"
status: "exact-finite-corroboration-passed"
truth_status: "finite corroboration only; universal proof in companion markdown"
review_level: "full-3302-byte-read-and-exit0-replay"
scope: "m<=11 per-customer algebra; finite exact SPE paths and complete certificates"
source_refs:
  - "clean:9079ae9e54942e1f95bc:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/counterexample/mechanism_scan/harmonic_payoff_cap_audit.py"
  - "clean:b9d80e2f19a93e649701:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/counterexample/mechanism_scan/harmonic_payoff_cap_audit.json"
  - "clean:4e13b559d21301fae696:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/counterexample/mechanism_scan/harmonic_payoff_cap.md"
  - "local:archives/customer-attraction/state/引理/任一实际玩家的调和福利支付界--引理.md"
  - "local:archives/customer-attraction/state/计算/调和末对钱包的原审计与审查身份--计算.md"
source_identity:
  inventory_blob: "b73b416b28b7ee3ad40f4df5fabaa681cd87ebc6"
  source_sha256: "6f197fde4401738214df495cecb56a388dbb6e8e46c2b5cb44af1a53ec9272f3"
  source_size_bytes: 3302
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R-18-harmonic-counterexample-20261031/original/harmonic_payoff_cap_audit.py"
  - "archives/customer-attraction/tools/evidence/R-18-harmonic-counterexample-20261031/replay/harmonic_payoff_cap_audit.stdout"
  - "archives/customer-attraction/tools/evidence/R-18-harmonic-counterexample-20261031/replay/harmonic_payoff_cap_audit.json"
  - "archives/customer-attraction/tools/evidence/R-18-harmonic-counterexample-20261031/related/customer_attraction/"
  - "archives/customer-attraction/tools/evidence/R-18-harmonic-counterexample-20261031/comparisons/9079ae9e54942e1f95bc.md"

# 调和福利支付界独立 Fraction 审计

## 运行和依赖

完整实读 3,302 字节脚本。它只用标准库加既有 `customer_attraction` ExactSPESolver/Instance/verify_certificate 包；将源码和包复制到保留 `ROOT=Path(__file__).parents[6]` 语义的 synthetic source-root 后执行，未改原件。实际 exit 0，输出状态为 `exact finite corroboration; universal proof is in companion markdown`；重放 stdout 和脚本生成 JSON 均保存在 evidence `replay/`。

## 精确计数

`algebra(max_players=11)` 对每个 `m=1..11`、每个非空客户 incidence mask 和每个 `j` 核对调和系数恰为 `H_m`，并检查逐客户分母界；总计 `per_customer_checks=188412`。`true_spe_checks` 用 seed 107131 在 `(players,topics,m)=(2,2,2),(3,4,4),(4,5,5),(7,5,5)` 四组上，每组 3 个随机单位客户实例，枚举规范 solver 的全部有序终局，核对 `W>=H_m payoff` 与逐位置系数，并将一条路径扩成完整策略证书，调用 verify_certificate 检查全部历史和偏离。

输出为 `ordered_paths=84`、`complete_certificates=12`、`complete_ordered_decision_nodes=9555`。冻结 JSON 与复跑 JSON 逐字节一致，证明有限重放稳定。

## 边界

这些数字只证明有限 incidence、有限随机实例和规范证书的实现一致性；一般量词来自 harmonic markdown 中的逐客户偏离证明，不来自枚举。程序没有搜索 half 反例，也没有计算 `OPT/H_m` 之外的全局付款；本对象不把 finite corroboration 升格为 Q-CAG-HALF 或策略锥定理。
