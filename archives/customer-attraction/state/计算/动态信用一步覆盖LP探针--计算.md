---
id: "customer-attraction/dynamic-credit-coverage-one-step-probe"
kind: computation
type_tag: 计算
title: "动态信用一步覆盖 LP 探针"
status: "finite-floating-probe-found-witness"
truth_status: "finite-exploratory-LP-witness; no-SPE-or-universal-claim"
review_level: "full-1498-byte-read-and-execution"
scope: "R-12bf dynamic_credit/coverage_one_step_probe.py; r=3,k=4,3000 random response maps"
summary: "随机探针在 trial 9 找到 gap=1/5 的一步投影 LP witness，minrow=0；这是有限浮点诊断，不是完整 SPE、精确反例或半覆盖结论。"
source_refs:
  - "clean:469334e1729f6e2a0365:research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/dynamic_credit/coverage_one_step_probe.py"
  - "local:archives/customer-attraction/state/引理/背景新增覆盖余额与首步分解--引理.md"
  - "local:archives/customer-attraction/state/审查/两步安全归纳与策略锥精确边界--审查.md"
source_identity:
  inventory_blob: "0a9d932a36589a4508857f5727d8e50b6d997d5e"
  source_sha256: "71410303ae040502d47b226ec3124e7d089619871f9647d54e236379202e350c"
  source_size_bytes: 1498
  frozen_commits:
    - "68fad804ec5946cb296f77dc5b336308a66abf12"
    - "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/dynamic-credit-coverage-one-step-20261031/original/coverage_one_step_probe.py"
  - "archives/customer-attraction/tools/evidence/dynamic-credit-coverage-one-step-20261031/replay/probe.stdout.txt"
  - "archives/customer-attraction/tools/evidence/dynamic-credit-coverage-one-step-20261031/comparisons/comparison-notes.md"
---

# 动态信用一步覆盖 LP 探针

脚本固定 `r=3,k=4`，在四 topic 的非空 mask 上随机生成 3000 个 response map，构造 Fraction utility/profit 与 coverage 等式，再用 `scipy.optimize.linprog` 搜索一步安全/覆盖投影的负 gap。实际执行在 trial 9 找到：`gap=1/5`，权重支持 `{2:3/5,3:1/5,4:3/5,8:3/5,9:1/5}`，`minrow=0`。

这是有限浮点 LP witness。脚本没有构造完整策略树、没有验证 SPE、没有给出 exact rational certificate，也没有证明所有背景或所有目录的投影规则失败。它只能说明被抽样的局部线性约束存在分离候选。与 `背景新增覆盖余额与首步分解--引理` 对照，探针反驳的是把一步余额强制非负的充分模板；全局望远镜可能由后续正余额支付，故不能把该 gap 写成 Q-CAG-HALF 反例。

与 `两步安全归纳与策略锥精确边界--审查` 的 113 客户精确负差相比，本源是更小的随机浮点 probe，证据层级更弱；本批保留 stdout 和 source SHA，未迁移到 unrelated-machines。
