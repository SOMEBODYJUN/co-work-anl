# 加权拥塞既有成果的恢复范围与方法用途

本次从 `origin/main` 恢复，基准提交 `240eae24ff7f19bb52e4e2d307780067145d9a0d`。既有数学正文、证明与冻结审计没有改写。用户本轮要求研究这些结构如何帮助稳定决策及优化；本文件明确可用地基与缺失来源，防止把前次聊天里的结论当作已恢复的证明。

## 可恢复的研究地基

| 仓库路径 | 本轮用途 |
| --- | --- |
| [research/current/weighted_congestion/linear_degree_allstate_lower_bound.md](../linear_degree_allstate_lower_bound.md) | 全状态线性下界：界定统一稳定保证的极限，不提供收敛或福利算法 |
| [research/current/weighted_congestion/linear_threshold_article.tex](../linear_threshold_article.tex) | 既有自足英文主稿源文件 |
| [research/current/weighted_congestion/linear_threshold_article.pdf](../linear_threshold_article.pdf) | 既有英文主稿PDF，正文与此前审查保持原样 |
| [research/current/weighted_congestion/power_bridge.md](../power_bridge.md) | 局部边际与共同玩家尺度：本轮校准方法的接口 |
| [research/current/weighted_congestion/weight_bands/finite_weight_class_potentials.md](../weight_bands/finite_weight_class_potentials.md) | 有限权类与共占高度：可供方法选择的结构保证 |
| [research/current/weighted_congestion/class_front_phase_quotient.md](../class_front_phase_quotient.md) | 前沿压缩与出口条件：区分压缩核与全状态保证 |
| [research/current/weighted_congestion/incidence_forest_private_reduction.md](../incidence_forest_private_reduction.md) | 森林及单核心挂树：原游戏的固定lift接口 |

逐文件 SHA-256 和最后修改提交记录在 [source_recovery.json](source_recovery.json)。其中旧英文主稿继续承担线性下界的完整证明；本轮方法稿以引用和用途地图组织它，不另复制整套证明。

## 无法从当前历史恢复的材料

旧个人桌面 `research/workspaces/shared/R-fc01bf7f59834de89c83796491d55ef7/README.md` 提及 near-unit 稿、森林权类稿、机制综述及短提交 `db2e428`、`6c728f0`、`8bf2901`。本次对恢复的 main 历史执行 `git cat-file`，这些提交对象均不可用；桌面没有对应正文。

这只说明本次没有恢复到相应文件，不说明其中数学命题为真或为假，也不声称这些对象在所有远端或备份中均不存在。本轮新增方法从可读正文及独立重构出发，另立精确身份；不借用缺失稿的证明或审查状态。

## 本轮方法问题

决策使用者需要输入与输出合同：允许多大单方改善、选哪一种社会成本、运行规模、状态变化费用以及失败时能得到什么证据。承重任务是共同玩家尺度的可核验校准、原游戏的修复与核心压缩、稳定性约束下的成本选择，及相同模型下的基线比较。

全状态线性下界继续是已有独立结果；方法改进必须明确结构假设，不能由局部势或修复器推成任意游戏的更小统一保证。

## 用户补充的旧工作参考与范围纠正

用户随后提供了 [STRUCTURAL_VIEW_AND_POSITIVE_RESULTS.md 的原字节存档](../../../../history/source/notes/weighted_congestion/structural_view_and_positive_results_reference.md)，其 SHA-256 为 `c026cc8bf14bfcb5c669b3141ac5858dbca5ae4b0d9a24a701579ea6ea3e5e46`。这是此前缺失工作的研究总结，原文记载了比本次 main 地基更强、更完整的结构主线；文件本身不是其链接所指的完整证明。

**需要纠正：上一轮只恢复了远端 main 中的文件，并基于这些文件新增了决策方法专题；没有完整恢复旧稿，没有取得不可见的完整历史对话，也没有按旧工作原有证明逐步复原。** “恢复”只适用于列明的仓库文件，不能解释为旧数学成果已全部重建。

参考记载的近一主结果、全局类型尺度兼容与森林推论、最小全局权深度的正反匹配，以及稳定集合的一般实现，都未在上一轮的方法成稿中完整恢复。新校准/优化方法可独立保留，但不能代替这些旧主线，也不能据此宣布新稿已达到旧稿水平。

旧参考中指向证明和审查的链接原样保留，以便今后按原身份恢复；不以新方法稿的审查状态覆盖这些未恢复证明。

旧主线与新专题的逐项差别、两种森林定义及成文定位，见[范围比较](previous_structure_scope_comparison.md)。
