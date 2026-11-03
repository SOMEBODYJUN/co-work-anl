---
id: paper-argument-reconstruction-claim-evidence
kind: resource
type_tag: argument-reconstruction
title: 论文论证重构与 Claim-Evidence 对齐
status: integrated
summary: 实读中文 argument reconstruction 参考，保存 problem-driven storyline、模块/公式/实验映射、段落功能和 claim-evidence 对齐规则，明确其不是 UM 数学结论。
source_refs:
  - source:79c05a93fc1b9c04e980:research/weighted_congestion_frontier/upstream/polish_skill/paper-argument-reconstructor/references/argument_reconstruction_zh.md
  - source:local:archives/unrelated-machines/state/资料/数学写作文类剖面与主张责任边界--资料.md
  - source:local:archives/unrelated-machines/state/资料/创新框架候选、缺口与证据反证合同--资料.md
---

# 论文论证重构与 Claim-Evidence 对齐

## 来源身份与处置

Claim `79c05a93fc1b9c04e980` 对应 `research/weighted_congestion_frontier/upstream/polish_skill/paper-argument-reconstructor/references/argument_reconstruction_zh.md`，冻结 blob `342543d1fbe1048b6ef41ac7f706b2e37e64877c`，源 SHA-256 `d0f9a57f868935a697d55611d308c7eaddee2f09dcc9f6b824897d3bdede225b`，大小 5015 B。原文已复制到 [中文参考 evidence](../../tools/evidence/argument-reconstruction-zh-20261031/original/argument_reconstruction_zh.md)，比较记录在 [comparison-notes.md](../../tools/evidence/argument-reconstruction-zh-20261031/comparisons/comparison-notes.md)。

处置为 `integrated` 资料对象：它可直接支撑论文稿件和数学正文的结构审查，但不创建 unrelated-machines 的定义、定理、算法或硬度结论。

## Problem-driven 主线

指南要求论文围绕核心问题而不是模块堆砌展开。默认链条是：真实需求 → 技术瓶颈 → 现有方法限制 → 所需能力 → 提出框架 → 机制解释 → 实验验证 → 实际意义；方法型论文可缩成核心问题 → 具体挑战 → 所需能力 → 模块 → 机制 → 证据 → 含义。每个段落、模块、公式和实验都应回答或支撑核心问题。

诊断顺序是：识别应用场景和核心问题；识别瓶颈或 failure mode；说明现有方法不能做到什么；确定 proposed method 必须提供的能力；把模块/公式/实验/结果映射到具体 claim；找出 unsupported claims、缺失过渡、重复 claim 和模块堆砌；先产出修订后的 storyline，再做句子级改写。

## 段落与贡献责任

段落先标记为应用背景、核心问题、技术 gap、方法动机、模块机制、公式定义、理论分析、实验设置、结果观察、结果解释、限制、实际意义或过渡。没有清晰功能的段落应合并、移动或重写。

每条 contribution 必须对应前文明确提出的 gap 或 challenge。较稳健的写法是“提供解决具体 gap 的 capability formulation”“缓解具体 failure mode 的机制”“在给定条件下验证某项 claim 的 targeted evaluation”。相关工作证据不足时，不写 `first`、`novel`、`unprecedented`，而使用 `we focus on`、`we develop`、`we investigate`、`we introduce a framework for` 或 `under the evaluated conditions` 等有边界表达。

## 各节和实验的承重顺序

摘要从背景/问题到 gap/failure、方法机制、证据和有边界的 implication；引言从真实需求到瓶颈、现有限制、所需能力、方法、贡献和组织；相关工作按方法家族、假设或限制组织，并只在实际文献证据允许时写 claim；方法每个模块都由挑战和所需能力引出，说明输入输出、机制、关系、假设和限制。

实验必须对应一个 claim、模块、指标或部署需求，并写明 claim、数据集/场景、baseline、指标、诊断价值和局限；机制型贡献要有 ablation 或 targeted scenario，不能只报告最终平均性能。结果段落依次给观察、对比、机制解释、与 claim 的关系，并在需要时写条件和限制；不能只复述表格。

## Claim-Evidence 对齐

指南建议用表格逐项记录 Claim、所需证据、现有实验、缺失证据和风险。典型风险包括：声称模块重要却无 ablation；声称 robust 却只测简单场景；声称 real-time/deployment 却无时间和资源分析；声称 safety/reliability 却无 failure-case；声称优于现有方法却无危险 baseline。

在当前第二阶段，这一规则可帮助区分完整证明、有限实验、障碍和候选：代码/重放只能支持其实际运行和输入范围，不能覆盖未读取的量词；反例和 failed converse 必须保留；“无 baseline”是证据缺口，不是新颖性或定理结论。

## 与既有资料的关系

`数学写作文类剖面与主张责任边界--资料` 给出 theorem-proof、计算/实证和视觉文类的依赖；`创新框架候选、缺口与证据反证合同--资料` 给出六字段候选和拒绝规则；`科研想法新颖性风险审计与优先权边界--资料` 给出 direct/adjacent/classic/dangerous baseline 和审稿攻击。本对象新增中文 problem-driven 重构流程、模块—claim—证据映射和实验诊断表，三者不互相替代。

源中指向 problem-driven-literature-review 的详细规则未在本 claim 实读，故不把那个文件的内容冒称为已验证依赖。未来改写论文时仍要保留数学对象的精确量词、来源 hash 和证据层级。
