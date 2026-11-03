---
id: customer-attraction/r3b6b-count-markov-outcome-reduction-probe
kind: computation
type_tag: 计算
title: R-3b6b 计数 Markov 终局集合有限降维探针
status: finite-exact-reduction-failure-records
truth_status: count-reduction-not-universal; no-half-conclusion
review_level: exact-source-read-and-output-comparison
scope: abstract fresh-subset marginal-potential games and finite CAG count-dependent policy probes
summary: Exact finite outputs show that a count-dependent Markov selector can lose full ordered-history outcome certificates. The probes concern reduction validity only; they do not restrict the original Q-CAG-HALF model or produce a half counterexample.
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/structural_reduction/fresh_markov_gap.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/structural_reduction/fresh_markov_gap_reduced.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/structural_reduction/fresh_markov_probe.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/structural_reduction/markov_layers.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/structural_reduction/markov_probe.py
---

# R-3b6b 计数 Markov 终局集合有限降维探针

## 抽象 fresh-subset gap

`fresh_markov_probe.py` 在有限势函数 \(F\) 上精确枚举三步策略的完整有序终局集合 `outcomes`，并与要求同一计数状态共享更深层选择的 `markov3` 集合比较。冻结 \(p=5\) 输出含四个完整终局计数
\[
(0,1,4),\ (0,2,3),\ (1,2,3),\ (1,3,4),
\]
而 Markov 子类只保留前三个，差集为 \((0,2,3)\)。势函数取值来自有限随机构造；该对象是抽象计数选择器的降维失败记录，不是客户实例或半覆盖反例。

## CAG 计数层有限程序

`markov_layers.py` 在 CAG `Instance` 上按计数层共享一个子策略映射，逐层合并菜单并设置 cap；`markov_probe.py` 对三主题、三玩家的全部 \(3^7\) 非负重数输入枚举完整 `ExactSPESolver` 终局集与计数 Markov 终局集，遇到首个差异即保存 `markov_gap.json`。它明确把结果标为“count-dependent outcome reduction only”，不把有限未命中或缺失映射升格为一般结论。

本批源码没有把 Markov 约束冒充原模型定义。原模型允许同计数、不同有序历史使用不同动作和平局；因此 Markov 映射只是严格子类。已有[完整历史与计数统一策略的严格分离](../反例/完整历史与计数统一策略的严格分离--反例.md)给出更强的客户实例证据，当前对象只保留这组较小的结构性探针和抽象 gap。

## 证据边界与用途

这些程序支持的结论是：不能把完整历史纯 SPE 的终局集合一般性地压成一个统一计数策略集合，再以此替代全历史验证。它们不说明所有 Markov 策略都不适用，不说明给定根终局没有另一份 Markov SPE，也不说明 Q-CAG-HALF 失败。继续研究必须分别记录完整有序策略、计数子类和是否只比较最差福利；若需要升级为模型反例，需提供单位客户输入、完整 IC 证书和真实 \(W,\operatorname{OPT}\) 计算。
