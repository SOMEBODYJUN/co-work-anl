---
id: mathlab-blackboard-evidence-ladder
kind: resource
type_tag: upstream-architecture
title: MathLab 黑板架构与证据状态阶梯
status: retained
summary: 实读 MathLab 上游 ARCHITECTURE 文档，保存其持久黑板、并行研究岛、Verifier/扩展协议与证据状态阶梯，并标明它与当前 Boss3 清洗工作流的非部署边界。
source_refs:
  - source:2cebad9493b8dd3a535f:research/weighted_congestion_frontier/upstream/mathlab/docs/ARCHITECTURE.md
  - source:local:archives/weighted-congestion/state/资料/接题来源映射与文献导入的版本边界--资料.md
  - source:local:archives/weighted-congestion/state/资料/冻结上游清单的五组选集与归档边界--资料.md
---

# MathLab 黑板架构与证据状态阶梯

## 来源身份与处置

Claim `2cebad9493b8dd3a535f` 对应 `research/weighted_congestion_frontier/upstream/mathlab/docs/ARCHITECTURE.md`，冻结 blob 为 `d94d2a6ad186b963f33af1d0fa912e6fc8bcbcf7`，源 SHA-256 为 `86caef32120dc9ec8a322f4f6fb917c6131122172d7659b8394f99e9b6906235`，大小 2078 B。原文完整复制到 [MathLab ARCHITECTURE 原文证据](../../tools/evidence/mathlab-architecture-20261031/original/ARCHITECTURE.md)，实际比较记录在 [comparison-notes.md](../../tools/evidence/mathlab-architecture-20261031/comparisons/comparison-notes.md)。

处置为 `retained` 资源对象。它保留上游研究工程的架构和证据分层，供后续理解来源和比较流程；它不创建 unrelated-machines 的定理、算法、硬度或新颖性结论。已有 weighted-congestion 资料曾记录 MathLab 的来源提交和选集，但本 claim 才实际读取 ARCHITECTURE 字节并保存原文 evidence；旧的 manifest 元数据不被倒推为本次逐文件阅读。

## MathLab 的实际数据流

文档把研究项目建模为“交接文件 + 持久黑板 + 并行研究岛”。其步骤是：Cartographer 读取 `HANDOFF.md` 并播种保守 claim/task；Director 把工作分配到不同 research islands；workers 使用本地 shell、web search 和结构化 blackboard；workers 发布持久 claim、计算、反例和证明资产；`PROVISIONAL_PROOF` 自动进入新鲜上下文的 Verifier；Seminars 选择性地把有用想法迁移到其他岛；agents 可以提交 capability request，由 RA framework engineer 热添加项目内扩展工具；SQLite 与项目文件在崩溃和模型上下文重置后保持状态。

这种数据流的承重约束是持久化和隔离：模型上下文可以丢弃，研究状态不能随之消失；独立研究岛用于避免一个吸引人的错误想法锚定所有 worker；跨岛传播通过 promoted findings、targeted messages 和 seminars，而非共享一个大对话。

## RA 扩展协议

RA 将扩展写入 `.mathlab/extensions/manifest.json` 与脚本文件。manifest 的工具项包含 `description` 和 `entrypoint`；每个扩展从标准输入接收 JSON，并在标准输出返回 JSON 或文本。`list_capabilities` 和 `run_extension` 每次调用都会重新读取 manifest，因此扩展可在活动研究过程中热加载。文档明确 RA 默认可以扩展这一层，但不能改写 MathLab core。

这些是上游软件的接口说明，不是当前结果分支已经启用的能力。本题实际使用的 `work.py`、Git checkpoint、board 分支和 `clean` receipt 有自己的身份、权限和远端推送语义；没有证据表明 MathLab 的 SQLite、Verifier 或 RA extension API 已部署到本次 Boss3 clone，因此不把它们写成当前执行依赖。

## 证据状态阶梯

ARCHITECTURE 给出黑板状态阶梯：

`IDEA → CONJECTURED → COMPUTATIONALLY_VERIFIED → PROVISIONAL_PROOF → INDEPENDENTLY_VERIFIED → FORMALLY_VERIFIED`。

另有 `REFUTED` 与 `DISPUTED` 旁路状态。其意图是把“想法”“猜想”“有限计算”“暂定证明”“独立复核”“形式验证”区分开，并在工作流中强制，而不是只靠 prompt 文字提醒。

对当前阶段的接续意义有两点。第一，有限 Fraction/整数重放只能支持有限计算层，不可直接升级为完整定理；第二，即使某一对象在 MathLab 黑板上标为 `PROVISIONAL_PROOF`，也不能替代本仓库正式正文、独立审查、原文 evidence、checkpoint 和 `clean done`。本阶段的 receipt 布尔字段声明实际阅读和独有内容去向，也不等同于数学真值字段。

## 跨存档关系和未覆盖部分

已有 weighted-congestion 来源资料把 MathLab 与 Anthropic、agentsync、写作技能等并列，且特别要求不要把同名 `Joe975/math-lab` 与 `adamisntdead/mathlab` 合并。这个身份区分在本对象中保留：本页只处理 claim 指定的 ARCHITECTURE，不把其他仓库、`prompts.py`、LICENSE 或上游 manifest 的未读内容冒称为本次阅读。

本对象没有验证 MathLab 软件可运行性、SQLite schema、Verifier 实现、RA 权限模型、扩展脚本安全性、并行吞吐或外部论文优先权。若后续要采用某一架构思想，须单独写接入设计和测试证据；不能由这份 2078 B 文档推出当前数学研究的自动复核已经存在。
