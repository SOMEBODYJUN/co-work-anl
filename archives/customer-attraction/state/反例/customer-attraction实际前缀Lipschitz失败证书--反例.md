---
id: "customer-attraction/direct-cover-incumbent-lipschitz-failure"
kind: counterexample
type_tag: "反例"
title: "customer-attraction 实际前缀 incumbent Lipschitz 失败证书"
status: "finite-obstruction-retained"
truth_status: "machine-readable-finite-obstruction"
review_level: "full-source-read"
scope: "one finite failure record for a proposed actual-prefix incumbent-value inequality"
source_refs:
  - "clean:0ac1ca48b9d17ab806e9:research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/direct_cover/incumbent_actual_lipschitz_failure.json"
  - "local:archives/customer-attraction/tools/evidence/customer-attraction-lipschitz-failure-20261031/original/incumbent_actual_lipschitz_failure.json"
  - "local:archives/unrelated-machines/state/审查/customer-attraction直接覆盖分支README、义务分层与前缀障碍路由--审查.md"
source_identity:
  inventory_blob: "3dff8e3939b61ce231d63436585dbd7ae4922a12"
  source_sha256: "ba4f8e246d61cc6e4d5537c332f17da0fa9ab62138f17ef9c536f06915e47943"
  source_size_bytes: 1460
  frozen_commits:
    - "68fad804ec5946cb296f77dc5b336308a66abf12"
    - "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/customer-attraction-lipschitz-failure-20261031/original/incumbent_actual_lipschitz_failure.json"
  - "archives/customer-attraction/tools/evidence/customer-attraction-lipschitz-failure-20261031/comparisons/comparison-notes.md"
related_objects:
  - "archives/unrelated-machines/state/审查/customer-attraction直接覆盖分支README、义务分层与前缀障碍路由--审查.md"
---

# customer-attraction 实际前缀 incumbent Lipschitz 失败证书

## 身份与准确结论

完整实读 clean source `0ac1ca48b9d17ab806e9` 的 JSON 文件 `incumbent_actual_lipschitz_failure.json`：1460 字节，SHA-256 `ba4f8e246d61cc6e4d5537c332f17da0fa9ab62138f17ef9c536f06915e47943`，inventory blob `3dff8e3939b61ce231d63436585dbd7ae4922a12`。原始 JSON 和比较记录分别保存在 [原文 evidence](../../tools/evidence/customer-attraction-lipschitz-failure-20261031/original/incumbent_actual_lipschitz_failure.json) 与 [comparison notes](../../tools/evidence/customer-attraction-lipschitz-failure-20261031/comparisons/comparison-notes.md)。

证书记录空前缀 `prefix=[]`、`T=0`、`A=1`、`r=4`，以及比较值 `left=9`、`right=39/4`。因此该记录承载的有限结论是：在其指向的 customer-attraction 具体实例和定义下，候选实际前缀桥 `f_r(b,T) ≥ ((r−1)/r) f_{r−1}(b+A,T)` 在该点失败，因为 `9 < 39/4`。这里的“失败”是一个有限障碍，不是对所有背景、所有人数或所有主题的全称反例。

## 实例数据

实例有六个主题 `A,B,C,D,E,F` 和四个玩家；JSON 列出十二种客户主题子集及重数：单主题 `{A},{B},{C},{D}` 的重数分别为 12、8、4、8；双主题 `{A,E},{A,F},{C,E},{C,F}` 的重数为 6、6、3、3；三主题 `{A,E,F},{B,E,F},{C,E,F},{D,E,F}` 的重数为 6、2、1、2。JSON 的 `source` 字段为 `root_tax_failure.json`，说明该记录依赖外部/兄弟来源解释其量词和计算过程；本页不把该未认领文件当已读。

## 证据层级和用途

该文件是 machine-readable finite obstruction，适合作为后续脚本、独立重算和正式障碍证明的输入。要把 `left/right` 解释成 incumbent 入场者收益或具体前缀函数值，必须共同读取 direct-cover README、`incumbent_lipschitz_obstruction.md` 和验证脚本，核对客户计数、策略路径、收益定义以及 `r`、`A` 的角色。当前 JSON 单独不能证明 README 中的 61 客户实际路径 `(B,A,A,F)` 或完整 SPE，也不能替代精确分数推导。

证书不否定弱匹配、弱平均、旧强平均、真正聚合安全值或 Q-CAG-HALF 目标；它只阻断一种按人数比例传递单一 incumbent 标量值的桥。后续可尝试保留替代主题信用、构造真实跨分支中继或证明更弱的条件桥，但必须另建对象和验证证据。
