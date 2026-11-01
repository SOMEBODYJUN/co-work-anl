---
id: "customer-attraction/r18-largest-incumbent-individual-bridge-finite-counterexample"
kind: "counterexample"
type_tag: "反例"
title: "R-18 最大 incumbent 个体桥有限反例"
status: "exact-full-SPE-finite-obstruction"
truth_status: "refutes-individual-OPT-over-(2m-1)-bridge-at-one-instance; not a half counterexample"
review_level: "full-5707-byte-read-json-and-related-strategy-comparison"
scope: "3 players, 6 topics, one complete pure SPE certificate; individual incumbent bridge probe"
source_refs:
  - "clean:663827506601922a81a3:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/global_proof/largest_incumbent_n3p6_best.json"
  - "clean:e5885286333aa0d55f8d:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/global_proof/largest_incumbent_n3p6_run.json"
  - "local:archives/customer-attraction/state/计算/R18最大incumbent个体桥策略锥探针--计算.md"
  - "local:archives/customer-attraction/state/反例/父方实际incumbent独立全历史审计报告--反例.md"
  - "local:archives/customer-attraction/state/计算/父方实际incumbent完整历史独立审计--计算.md"
source_identity:
  inventory_blob: "a3c8f557225a319a0f24c750a8ca5b939bf7e35b"
  source_sha256: "7dcd445bdfe275e7b0521945ad4242aea3f3401dc0df848fb01c5bcb2fcfcbbd"
  source_size_bytes: 5707
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R-18-global-proof-incumbent-20261031/original/largest_incumbent_n3p6_best.json"
  - "archives/customer-attraction/tools/evidence/R-18-global-proof-incumbent-20261031/comparisons/663827506601922a81a3.md"

# R-18 最大 incumbent 个体桥有限反例

## 准确被否定的桥

完整读取 5,707 字节 JSON。它给出一份三人六主题的完整有序历史纯 SPE，实际终局计数为 `[1,0,1,1,0,0]`，即 `(0,2,3)`。根福利 `W=750`，三主题最优覆盖 `OPT=963`，根实际动作 `a=0` 的收益 `u=375/2`。因此
\[
 \frac{OPT}{u}=\frac{642}{125}=5.136
e 2m-1=5.
\]
它精确反驳“每份完整 SPE 的某个 incumbent/个体根收益必满足 `u\ge OPT/(2m-1)`”这一加强桥；并不反驳 half，因为 `2W-OPT=537>0`。

## 完整策略和证书身份

JSON 保存全部 `1+6+36=43` 个有序历史动作，包含根、所有一次历史和所有二次历史；顶层 `verified=true`。客户共有 11 个兴趣类型，主题 0–5，整数 multiplicity，总客户质量为 963；这里恰好 `OPT=963`，因为三主题 `(0,2,3)` 覆盖全部客户。`W=750` 是实际终局福利，不能把 `W` 与根收益 `u` 混同。

策略终局计数 `[1,0,1,1,0,0]` 与所有动作表一起构成完整历史证书。JSON 的 `verified` 字段来自搜索器的精确 `verify_canonical` 检查；本次清洗保留原证书，不把有限搜索过程重新描述成一般证明。

## 与已有 incumbent 障碍的关系

既有父方四人/61 客户对象核验的是实际路径上的 incumbent proportional relay；本源是三人/六主题、个体 `OPT/(2m-1)` bridge 的不同量词。二者都保持正的 half 余量，不能互相合并成 Q-CAG-HALF 反例。R-18 最大主题容量/根包络引理同样只提供必要关系，不自动支付本源的个体收益缺口。

本对象处置为 integrated 的精确有限障碍：它否定特定个体 bridge，保留完整 SPE 与客户整数证书；不升级为一般 SPE 反例、hardness、静态 CCE 或 unrelated-machines 结论。
