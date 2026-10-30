---
id: "unrelated-machines/rooted-dag-congestion-audit-evidence"
kind: "evidence"
type_tag: "证据"
title: "有向需求树共同拥塞双路冻结审计证据"
status: "current-rerun-matches-frozen-audit"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/rooted_dag_congestion_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/rooted_dag_congestion_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/rooted_dag_congestion_flow.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/rooted_dag_congestion_independent.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:examples/unrelated_machines/rooted_dag_congestion_cases.json"
---

# 证据范围

本目录保存 `84ebead8a3eb35b9ec3d` 组合审计的原始 JSON、关联审查、规范实现、独立实现、输入 fixture，以及本轮在 Python 3.12.14 上的重跑输出。原始审计是双路冻结记录：规范共同拥塞流程序、独立根树/边流 oracle 和经典基线结果同时存在；本轮只重跑前两路并做字段级精确比较，没有把重跑误写成新的一般证明。

## 冻结内容与哈希

原始审计的 source SHA、命令和限制完整保存在 `rooted_dag_congestion_audit.json`。规范代码 SHA 为 `64895990f782290aab59bedd7600422bc046cfd818d2f648c8142c5e06a056bd`，独立代码 SHA 为 `bafee6f27f3c10268c5fdf98f9ad9d6c13597e60637493550b2103178396ca2a`；关联审查副本 SHA 为 `a62c5ac1450b73c2b8a0a4a6a6fd733109eaa7a90da4968aef99f4c470d5e0fd`。每个保存文件的字节数和 SHA 另列在 `manifest.json`。

## 实际重跑

直接执行保存下来的规范程序得到 `current_original_rerun.json`；把其旁置为模块后，以 `PYTHONPATH` 执行独立程序得到 `current_independent_rerun.json`。两者均使用整数/`Fraction` 精确算术，不使用浮点容差。比较结果如下：

- 规范路：14,076 个枚举证书赋值、497 个提取证书、4,548 个固定支撑搜索实例（434 可行）、1,516 个最小拥塞支撑对象（262 可行）、K=1,2,3 单调性、低走廊深度 1,000、19 个非法输入拒绝，均与冻结 JSON 的 `canonical` 字段逐项一致；特殊案例和 K=2..16 尖锐族列表也逐项一致。
- 独立路：1,566 个证书案例、596 个不同对象、240 个分数案例、60 个巨大 K 案例、10,001 个锐宽案例、5,350 个固定支撑 finder 案例、1,516 个对象的最小 K oracle、5,279 个实际树到证书案例、396 个 κ* 交叉对象、2,071 个提取交叉检查，及 q=2..25 激活走廊列表均与冻结 `independent` 字段一致；seed 为 792148。
- 规范程序首次直接启动时，独立程序因其原始导入名需要模块目录而出现 `ModuleNotFoundError`；将同一保存的规范文件放入 scratch 模块路径后重跑通过。该启动约束属于复现包装边界，不改数学结果，也没有修改源程序。

## 数学边界

这些运行只核对固定支撑、整数流提取、K 单调/最小 K、尖锐族和激活走廊反例的有限实现合同。它们不搜索一般输入的好支撑 W，不给统一常数 K，不消除 `2^h` 参数，也不提供 `UM-TARGET-v1` 或一般 unrelated-machines 近二算法。规范审查另外指出：给定 W 的失败只否定该 W/K 证书；激活边际 LP 的可行不替共同整数流；经典 Bamas 基线仍是独立有限记录。
