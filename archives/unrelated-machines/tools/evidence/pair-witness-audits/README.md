---
id: "unrelated-machines/pair-witness-audits-evidence"
kind: "evidence"
type_tag: "证据"
title: "双件见证与两选择块秩审计证据"
status: "semantic-reruns-match-frozen-records"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/top_two_pair_witness_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/two_choice_block_rank_audit.json"
---

# 证据范围

本目录保留两条相邻但身份不同的审计链：top-two 审计枚举 2 机 4 job、3 机 3 job 的全部半单位矩阵及 256 个两变量 unit/binary-clause 公式；two-choice block-rank 审计使用精确块秩 solver、cactus high-girth fixture 和全部固定阈值检查。

规范正文已把 top-two 目标与普通 makespan 分开：B₂≤3O₂/2 属于不同目标，3SAT 编译只给固定小于 3/2 的受限困难性；它没有给主目标的趋二 gap。block-rank 记录的 gap target 也不自动等于配置阈值，不能从有限 cactus 样例升级为一般 hardness。

## 本轮重跑

`current_top_two_rerun.json` 与冻结 JSON 的 `matrix_audits`、`sharpness_audit`、`degeneracies`、`errors` 字段逐项相同；差异只在运行环境的 base commit、platform 和 scratch source path。`current_block_rerun.json` 的全部有限字段（1000 个随机实例、4096 个 two-triangle cut-vertex 实例、6 个独立 cactus 交叉案例、11 个非法案例和所有 boundary 列表）与冻结 JSON 完全一致。两条程序均使用整数/Fraction 精确算术。

证据目录同时保存 boundary/review 正文副本、四份源程序、冻结 JSON、当前重跑 JSON 和 manifest；这些文件证明的是具体有限运行和目标分层，不是新的全称算法或外部新颖性。
