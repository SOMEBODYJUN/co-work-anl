---
id: customer-attraction/r18-largest-incumbent-individual-bridge-search-record
kind: computation
type_tag: 计算
title: R-18 最大 incumbent 个体桥有限搜索记录
status: finite-search-record-read
truth_status: finite-root-relaxed-search-only; linked-step25-claim-is-not-SPE
review_level: old-8004-byte-read-retained;later-generator-root-omission-qualified
scope: n=3,p=6 incumbent search run JSON; configured 500 steps, 21 stored steps
source_refs:
- clean:e5885286333aa0d55f8d:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/global_proof/largest_incumbent_n3p6_run.json
- clean:663827506601922a81a3:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/global_proof/largest_incumbent_n3p6_best.json
- local:archives/customer-attraction/state/计算/R18最大incumbent个体桥策略锥探针--计算.md
- local:archives/customer-attraction/state/反例/R18最大incumbent个体桥有限反例--反例.md
- local:archives/customer-attraction/state/审查/最大incumbent候选的根激励遗漏与错误认证--审查.md
source_identity:
  inventory_blob: 45138056ff5746303d2ff202e6c8c32893c3062a
  source_sha256: c20fef2198c5c1436fef8a1f47d680e0ea44c7e4c2836b68e77634d0c97562a5
  source_size_bytes: 8004
evidence_paths:
- archives/customer-attraction/tools/evidence/R-18-global-proof-incumbent-20261031/original/largest_incumbent_n3p6_run.json
- archives/customer-attraction/tools/evidence/R-18-global-proof-incumbent-20261031/comparisons/e5885286333aa0d55f8d.md
---

# R-18 最大 incumbent 个体桥有限搜索记录

完整读取 8,004 字节 run JSON。配置参数为 `players=3`、`topics=6`、`steps=500`、`seed=731`；记录中实际有 `steps=21` 个已处理 step，顶层 `best="5"`。每条 record 保存当前终局目标、浮点 `value`、portfolio `J` 和 所建松弛锥行数 `rows`；记录没有将浮点 proposal 自动当作 exact bridge 证书。

`best=5` 恰等 `2m-1` 阈值，只表示该有限策略锥队列没有在已保存记录中产生严格个体桥违反；它与 step25 的 exact best JSON（`OPT/u=642/125`）必须分开读取。该 run 的配置写了 500 上限，但输出只列 21 个已执行 step，因此本页不把它描述为 500-step 穷尽。

对象处置为 integrated 有限搜索记录。它用于说明候选生成范围和有限 proposal 行数，不证明个体 `OPT/(2m-1)` bridge，也不反驳 Q-CAG-HALF；不迁移到 unrelated-machines。

后续已确认同生成器显式删除根IC且verified:true硬编码，三人step25 best并非完整SPE；其OPT/u=642/125只是真实形式策略上的精确算术，不是个体桥反例。此run的21条/数值best5仍保历史，不倒称其每个锥有完整根认证；见[后续根审查](../审查/最大incumbent候选的根激励遗漏与错误认证--审查.md)。
