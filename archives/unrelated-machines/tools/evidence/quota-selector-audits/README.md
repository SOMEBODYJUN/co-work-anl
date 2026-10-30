---
id: "unrelated-machines/quota-selector-audits-evidence"
kind: "evidence"
type_tag: "证据"
title: "配额与选择器三源有限审计证据"
status: "current-reruns-match-frozen-json"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/selector_tiny_root_three_values_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/single_layer_quota_sqrt_multiplicity_floor_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/two_state_quota_hall_audit.json"
---

# 证据范围

本目录保存三份小规模 exact audit 的原始 JSON、对应脚本、相关平方根配额正文/审查、当前重跑输出和 manifest。三源属于不同数学接口：三值 selector 的完整 ordinary-UM 矩阵分类、单层配额超图的平方根重数计数、两状态固定方向支付的 Hall 等价。它们可以相互比较，但不能合成一个一般调度器或一个统一 hardness 结论。

## 当前重跑

- `selector_tiny_root_three_values_audit.py` 输出与冻结 JSON 字节级 JSON 解析后完全一致：6 个完整矩阵，所有原 jobs 保留；perfect 两例 OPT=1，parity_middle 两例分别为 3/2、4/3，nonisolated_h_deficiency 两例分别为 2、5/3。
- `single_layer_quota_sqrt_multiplicity_floor.py` 原样输出 `ok: 23192 exhaustive systems; group formulas checked`；其 Fraction 穷举范围为 q=3、资源宇宙 U=3,4,5、K=2,3，另检查 Δ,K=1..8 的分组公式网格。
- `two_state_quota_hall.py` 原样输出固定方向 Hall 判据：1,296 个资源关联模式、279,936 个固定方向实例，全部与显式匹配枚举一致，并保留 `finite_check_only=true`。

所有程序使用整数或 Fraction，不使用浮点容差。三份 JSON 的 source hash、命令、范围和限制保存在各自原始副本中；文件字节哈希见 `manifest.json`。

## 数学范围

平方根正文证明的是：若每个变量的给定邻域至少 K、每个资源全局关联度至多 Δ，则最大不交 t-束比例满足

`b ≥ max_t min{t/K, (K−t+1)/(K−t+1+tΔ)}`。

当 K≥√Δ+1 时给出 `1/(√Δ+1)−1/K` 的整数化地板；这是单层给定标签的自足计数引理。selector audit 只检验有限普通 UM 矩阵的三种来源分类与实际 OPT；Hall audit 只检验已固定方向的配额支付，不负责选择 rail 或变量子集。任何失败或通过都不能被解释成一般输入的 FAIL 证书、近二算法或硬度证明。
