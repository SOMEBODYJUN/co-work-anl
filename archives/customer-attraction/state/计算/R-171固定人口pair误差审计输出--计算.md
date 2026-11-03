---
id: "customer-attraction/R-171-fixed-population-pair-error-audit-output"
kind: computation
type_tag: 计算
title: "R-171 固定人口 pair 误差审计输出"
status: "replayed-exact-fraction-output"
truth_status: "finite-audit-output; no-general-SPE-transport"
review_level: "full-344-byte-read-and-script-replay"
scope: "R-171 coupling/fixed_population_pair_error_audit.json; direct-payoff and fixed-population path checks"
summary: "冻结 JSON 与独立 Fraction 脚本输出逐字一致：17,280 个局部会员配置和 8,188 个固定人数二值路径检查通过，统一因子为 (r-s)(r-1)，并明确 no SPE transport constructed。"
source_refs:
  - "clean:c89b2700bb93eab9f0f6:research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/coupling/fixed_population_pair_error_audit.json"
  - "local:archives/customer-attraction/tools/evidence/R-171-coupling-pair-20261031/original/fixed_population_pair_error_audit.json"
  - "local:archives/customer-attraction/tools/evidence/R-171-coupling-pair-20261031/original/audit_fixed_population_pair_error.py"
  - "local:archives/customer-attraction/tools/evidence/R-171-coupling-pair-20261031/replay/audit_fixed_population_pair_error.stdout.json"
  - "local:archives/customer-attraction/state/引理/R-171固定人口pair误差与ghost-rent系数--引理.md"
  - "local:archives/customer-attraction/tools/evidence/R-171-coupling-pair-20261031/comparisons/comparison-notes.md"
source_identity:
  inventory_blob: "420001a6051ae91ba767af92da31de9c319b6c47"
  source_sha256: "889b2455633a473395573a7e080e0d136c97e052a9b5b340520f08ba431c3fef"
  source_size_bytes: 344
  frozen_commits:
    - "68fad804ec5946cb296f77dc5b336308a66abf12"
    - "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R-171-coupling-pair-20261031/original/fixed_population_pair_error_audit.json"
  - "archives/customer-attraction/tools/evidence/R-171-coupling-pair-20261031/replay/audit_fixed_population_pair_error.stdout.json"
  - "archives/customer-attraction/tools/evidence/R-171-coupling-pair-20261031/comparisons/comparison-notes.md"
---

# R-171 固定人口 pair 误差审计输出

## 冻结字段与重放

JSON 源完整实读 344 B，SHA-256 `889b2455633a473395573a7e080e0d136c97e052a9b5b340520f08ba431c3fef`，稳定 ID `c89b2700bb93eab9f0f6`，blob `420001a6051ae91ba767af92da31de9c319b6c47`。字段为：

- `status`: `all direct-payoff and fixed-population path checks passed`；
- `scope`: `algebraic errors and arbitrary actual paths; no SPE transport constructed`；
- `local_membership_cases`: `17280`；
- `fixed_population_path_cases`: `8188`；
- `all_primary_pair_profiles_have_exactly_m_players`: `true`；
- `uniform_comparison_factor`: `(r-s)*(r-1)`。

本次执行原脚本得到完全相同的 JSON；replay stdout 的 SHA-256 也是 `889b2455633a473395573a7e080e0d136c97e052a9b5b340520f08ba431c3fef`。因此该文件是脚本有限审计的冻结结果，而不是另一个数学来源或新的计算发现。

## 数学含义和量词边界

`17280` 对应 (h\in\{0,\ldots,32,64,127,1000})、(2\le r\le16)、所有 (1\le s<r) 和四种二值 (A/B) 会员配置。`8188` 对应 (m=1,\ldots,11) 的全部二值实际路径以及两个 (s) 选择模式。统一因子表示该有限审计检查的逐客户支配常数，不表示对所有主题目录、所有人数或所有完整策略的自动量词提升。

JSON 明确写入 `no SPE transport constructed`。这与已归档的连续窗口 ghost-rent 引理、skip-premium 分解和完整 SPE 稀疏槽障碍一致：pair 误差的代数系数可以核对，但仍需真实激励行把局部误差送入根福利；不能把有限路径预算当作完整 Q-CAG-HALF 证明。

本对象处置为 retained 的计算输出；其独有内容是冻结的计数、状态和统一因子，正文公式与有限重放解释位于 `R-171固定人口pair误差与ghost-rent系数--引理`，导航量词与开放义务位于对应审查页。
