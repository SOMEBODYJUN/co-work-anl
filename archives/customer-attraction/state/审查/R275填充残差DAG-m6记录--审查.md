---
id: "customer-attraction/R275-padded-residual-m6-dag"
kind: "review"
type_tag: "审查"
title: "R275 填充残差 DAG-m6 记录"
status: "complete-count-DAG-read"
truth_status: "finite-exact-instance; scoped-counterexample-only"
summary: "冻结 complete-SPE-count-target-DAG-v1 JSON 给出一个六人九主题实例的完整计数 DAG，专门反驳 common-query regret ≤ minimum provider payoff；它明确排除 Q-CAG-HALF，路径福利 W=25、OPT=26、最小收益4、bridge_slack=-1。"
source_refs:
  - "clean:ee53fbf96073c13bf5c0:research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/direct_global/padded_residual_m6_dag.json"
  - "local:archives/customer-attraction/tools/evidence/R275-padded-best-agent/manifest.json"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R275-padded-best-agent/padded_residual_m6_dag.json"
  - "archives/customer-attraction/tools/evidence/R275-padded-best-agent/manifest.json"
---

冻结源的 blob 是 `1801f189cd58799af9f5a0746ae9e42f77f9fa7e`，大小 490722 字节，SHA-256 为 `555d309040dc76222624776a71c6d49b54804880cf38da12d2597abed2129efc`。schema 为 `complete-SPE-count-target-DAG-v1`，scope 明确写成“只反驳 common-query regret ≤ minimum provider payoff；不是 Q-CAG-HALF”。

实例有 9 个主题、6 名提供者和 10 类带重数客户。完整 JSON 含 5440 个计数节点，其中 2437 个带行动和子节点、3003 个叶节点；每个非叶节点记录当前 counts、目标 counts、遵循 action 及九个后继索引。根节点为全零计数，根 target 为 `[1,1,0,0,0,1,1,1,1]`，因此这是一份显式的完整计数 DAG 数据，而不是单条实际路径摘要。

记录的预期路径是 `[5,6,7,8,0,1]`，六个提供者效用为 `[4,4,4,4,4,5]`，终局福利 `W=25`，实例最优 `OPT=26`，查询主题为 2，未覆盖查询数为 5，`F=30`，最小提供者收益为 4，`bridge_slack=-1`。这些字段只支持该有限实例对指定 common-query regret 桥的反例；它们不说明六人完整历史纯 SPE 的半覆盖结论，也不改变主问题的客户覆盖量词。

可复用的是“完整计数目标 DAG + 目标路径 + 终局收益/最优值/桥松弛”的证据接口：后续可以逐节点核对行动最优性、离轨子树和客户分摊，再把反例与其他 common-query 或残差势对象比较。当前 JSON 没有独立程序证明其所有节点合同，需结合生成器或逐节点审计；因此本记录保留为有限精确数据对象，不升级为一般定理。
