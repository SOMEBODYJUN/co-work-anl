---
id: "customer-attraction/r18-maximum-cardinality-forced-root-obstruction"
kind: "obstruction"
type_tag: "障碍"
title: "R-18 最大主题强制根的非完整 SPE 障碍"
status: "exact-suffix-obstruction-only"
truth_status: "refutes-maximum-cardinality-as-guaranteed-root-action; not a full-SPE or half counterexample"
review_level: "full-5740-byte-read-and-related-MILP-comparison"
scope: "3 players, 6 topics; all positive-depth histories SPE; root forced to maximum-cardinality topic"
source_refs:
  - "clean:ac0a7249b93d1961cb92:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/global_proof/largest_incumbent_small_counterexample.json"
  - "clean:14375a4d622e69252e13:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/global_proof/simplify_largest_incumbent.py"
  - "local:archives/customer-attraction/state/反例/R18最大incumbent个体桥有限反例--反例.md"
  - "local:archives/customer-attraction/state/引理/五人最大主题根界--引理.md"
source_identity:
  inventory_blob: "1793c0eeebe5655dd6d359ebc16f389530f139d3"
  source_sha256: "44ae1a0ecec9659c75eee622ed9990e216815ff17a150375dc19bd1b1cfd0986"
  source_size_bytes: 5740
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R-18-global-proof-incumbent-20261031/original/largest_incumbent_small_counterexample.json"
  - "archives/customer-attraction/tools/evidence/R-18-global-proof-incumbent-20261031/comparisons/ac0a7249b93d1961cb92.md"

# R-18 最大主题强制根的非完整 SPE 障碍

## 障碍的准确量词

完整读取 5,740 字节 JSON。它明确声明：这是“最大基数主题作为保证动作”的反例，根被强制且不必最优；每个正深度历史满足 SPE，**不是**完整 SPE，也不是 half-coverage counterexample。

实例有 3 名玩家、6 个主题。完整策略对所有正深度历史保存动作；实际终局为 `(0,2,3)`，各主题裸大小为 `[13,12,13,13,13,13]`，所以根主题 0 是最大基数主题之一。强制根 incumbent 的实际收益为 `13/2`，三主题最优覆盖 `OPT=33`，实际福利 `W=26`，个体比值 `OPT/u=66/13≈5.077`，但 `2W-OPT=19>0`。

`all_suffix_comparisons=252` 核对的是固定根之后的正深度历史和动作偏离；根偏离收益为 `[13/2,21/2,21/2,12,13/2,21/2]`，主题 3 的根偏离明显高于强制动作。因此把根动作固定为最大主题破坏了完整 SPE 量词。

## 与简化 MILP 和完整证书的关系

同批 `simplify_largest_incumbent.py` 从三人六主题完整 incumbent 证书的所有正深度 SPE 行出发，以整数客户重数 MILP 搜索：保持主题 0 的最大裸大小、满足全部 suffix IC，并要求根收益严格低于 `OPT/(2m-1)`。生成的 JSON 与本源 SHA 同为 `44ae1a...`；它是可复现的有限障碍输入。

该障碍与三人完整 incumbent 个体桥反例不同：完整反例的根也通过完整 SPE，但本源只保持正深度 SPE，根被外力固定；二者都不构成 Q-CAG-HALF 反例。与五人最大主题根界的关系也仅是“最大主题是必要分析对象”，不能推出最大主题自动为根最优动作。

对象处置为 integrated 障碍记录。它否定“根可无条件强制任一最大基数主题”这一路线，不否定完整 SPE 的 half、静态 CCE、一般策略锥或 unrelated-machines。
