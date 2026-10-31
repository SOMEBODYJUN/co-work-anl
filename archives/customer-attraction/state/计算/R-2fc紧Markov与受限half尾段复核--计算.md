---
id: customer-attraction/r2fc-credible-search-root-tail
kind: computation
type_tag: 计算
title: R-2fc 紧 Markov 与受限 half 尾段复核
status: finite-candidates-and-timeouts
truth_status: finite-evidence-only; no universal half conclusion
review_level: six-source-clean-show-and-independent-field-replay
scope: five-player seven-topic restricted-support probes and count-Markov discovery candidates; one legacy three-player incumbent JSON
source_refs:
  - clean:9dd325f6b652dc4cc0f1:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/m5p7_2210000.json
  - clean:998df8512cbe0c0bbafc:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/m5p7_3200000.json
  - clean:4b182703448445426eaa:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/tight_markov_00011.json
  - clean:3ccd633444ddd50af4b5:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/tight_markov_00112.json
  - clean:0694ab24765066a3e411:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/tight_markov_probe.py
  - clean:7d8c67861a5d1cd5fdf1:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/old_largest_incumbent_audit.json
evidence_paths:
  - archives/customer-attraction/tools/evidence/R-2fc-credible-search-root-20261031/
  - archives/customer-attraction/tools/evidence/R-18-global-proof-incumbent-20261031/original/largest_incumbent_n3p6_best.json
receipt: cleanup/workspaces/Boss2/receipts-R-2fc-credible-search-root-20261031.json
---

# R-2fc 紧 Markov 与受限 half 尾段复核

## 受限 half 探针

两个五人七主题输入分别为根计数 `2,2,1,0,0,0,0` 与 `3,2,0,0,0,0,0`，portfolio 都是 `(2,3,4,5,6)`，floor 为 `1.8`，允许的支持掩码分别为 39 与 23 个。模型各有 42,345 个变量、41,888 个二元变量和 77,065 行；HiGHS 运行约 26.45 秒和 25.88 秒后均为 `status=1` 的 time limit，`floating_value=null`、`floating_bound_not_a_certificate=true`、`exact_candidate=null`。它们只说明这两次有限搜索没有在时限内产出候选或证书，不说明不可行，也不说明所有完整 SPE 低于 half。

## W=1 紧化的 count-Markov 发现

探针源码以任一 root SPE 中每个主题客户量不超过总福利 W、每个玩家可保证其所选主题的 `|T|/m` 为基础，把条件 big-M 从 `m` 替换为 1；该上界只用于 count-Markov 发现阶段。随后脚本把 candidate 展开为完整有序历史证书，故必须同时记作“发现子类”和“候选后验检查”，不能把发现约束当成一般策略空间。两个输入路径为 `(0,0,0,1,1)` 与 `(0,0,1,1,2)`，均为五人七主题、portfolio `(2,3,4,5,6)`。

两次 MILP 各有 4,747 variables、2,310 binary、46,540 rows，约 25.38/25.44 秒时限；`status=1`，`floating_value=1.0` 且 `floating_bound_not_certificate=true`。脚本各输出一个 `exact_candidate`，`objective_value=1`、`ratio=1`、`welfare=1`、`optimum=1`，但 `dual_bound=null`、`dual_support=[]`。这是两个有限候选的精确字段，不是全局最优证明、一般半覆盖构造或六人结论。

## 旧 963 单位客户 incumbent

同批旧 JSON 的 SHA 与已归档 R-18 文件相同。它声明 `verified:true`，但显式写出 43 个决策历史、215 个非自身比较、五条 root `bad_comparisons`，`nonroot_bad_comparisons=0`，`full_history_SPE=false`；实际路径收益 `(375/2,579/2,273)`、福利 750、最优 963。五个根替代严格盈利，故该字段不能认证完整 SPE。现有反例对象已保留这一更正；本批将源作为重复字节 retained，并以独立 validator 复核其根缺口。

## 用途与接续

本批为后续可信搜索提供三种可复用边界：受限 half 搜索的时限结果、count-Markov 候选的 W=1 紧化接口，以及旧 incumbent 的根 IC 缺失诊断。后续若要升格为数学结论，必须提供不依赖 Markov 限制的完整有序历史全称证书、可实现非负客户目录和无时限/有理对偶；本批不改变六人 Q-CAG-HALF 的 OPEN 状态。
