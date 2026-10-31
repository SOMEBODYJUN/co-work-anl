---
id: customer-attraction/retired-topic-selection-artifact-manifest
kind: resource
type_tag: 资料
title: 退役选题独立审查工件清单与版本边界
status: historical-artifact-manifest-integrated-no-math-claim
scope: history/retired_topic_selection/independent_review/evidence/runs/topic_selection/artifact_manifest.json; research/topic-selection snapshot inventory
summary: 完整读取并保全一份退役选题独立审查快照的工件清单。它精确列出 61 个研究文档、测试脚本和有限运行输出的路径、字节数与 SHA-256，并记录 branch、save、peer_base；清单本身不包含数学推导、运行结果或新颖性认证。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/independent_review/evidence/runs/topic_selection/artifact_manifest.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/independent_review/evidence/runs/topic_selection/artifact_manifest.json
related_objects:
  - ../退役选题核验与有限复现合同--资料.md
  - ../两套退役账本的逐命题来源分诊--资料.md
  - ../仓库读取地图与退役双来源恢复--资料.md

# 实读结论

## 来源身份与精确内容

`clean show 0de19177540e33c7aafb` 导出的冻结字节大小为 12,033，源 SHA-256 为 `fa00dd0b9fbf10abef35c010867732d86cdce3f42327239b17482001b4673b3d`。`legacy-cleanup` 提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 和 `main` 提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 均定位到相同内容；inventory 的 blob 为 `4b040ff309d80ef5084b63adba070e921818a5ea`。

JSON 顶层字段为 `branch=research/topic-selection`、`save=topic-selection`、`artifact_count=61`、`peer_base=f07dda4772575a9d0b777199e59206b696c9e2b1`、`boundary`。实际 `items` 也恰为 61 条；路径和 SHA 均唯一。每条只含 `path`、`sha256`、`bytes`，不是对应文件正文、运行日志或证明证书。

按路径前缀统计：`research/topic_selection/` 28 项、`tests/audits/topic_selection/` 16 项、`evidence/runs/topic_selection/` 17 项；总字节数 502,723，三类分别为 348,844、76,760、77,119。研究项混合入口、候选报告、候选 JSON 与少量运行说明；tests 是各子线 toy/审计脚本；evidence 是 toy 输出、选择验证和有限审计 JSON。清单不主张这些 61 个条目已被本清洗批次逐一重读，也不主张“通过”意味着全域定理。

## 与现有对象及已处置来源的比较

现有 `退役选题核验与有限复现合同--资料.md` 已从同一 `artifact_manifest.json` 和 `selection_validation.json` 建立跨子线的有限复现合同，并已把若干脚本/输出分别归入 fair-allocation、local-potential-games、weighted-congestion 等对象。现有 `仓库读取地图与退役双来源恢复--资料.md` 也记录了 `research/topic-selection` 的分支、提交和双来源恢复边界。它们没有保存这一份 61 项清单的逐条路径/哈希表，因此本对象保留清单的唯一 provenance 元数据；清单与已分别处置的子源是索引/来源关系，不是重复数学结果。

本次将原字节副本保存为 `archives/customer-attraction/tools/evidence/retired-topic-selection-20261031/topic-selection-artifact-manifest.json`。它与现有各子线证据副本分开，便于按 `peer_base` 和源 SHA 复核快照，不把历史 branch 名称或 peer 合并提交当作当前运行分支、当前数学状态或外部同行评议。

## 处置与边界

处置为 `integrated`（资料资源）而非数学定理、反例或计算结论：独有内容是快照级工件索引和版本边界，已由本对象与精确证据副本承接。不能把 `artifact_count=61` 当成 61 个互异问题、已完成来源数量或证明覆盖率；不能把 `peer_base` 当作同行认可；不能从 artifact manifest 的存在推断其列出的候选、脚本或 JSON 均已独立验证。每个条目仍以自己的 source ID 和语义回执判断；已完成子源的实际范围沿用各自正文，不由清单扩张。

第三阶段如建关系，只能建立“历史工件清单 → 版本/来源恢复资料”关系，以及清单条目到各自已整合 evidence 的来源关系。清单不提供 `derives`、`refutes` 或跨模型数学边；任何数学复用必须回到相应脚本、输入、输出和自足正文，核对量词、模型和有限范围。
