---
id: fair-allocation/common-marginal-three-player-nash-audit
kind: review
type_tag: 审查
title: 共同边际三人Nash有限审计
status: finite-exact-audit-only; no-theorem; no-novelty-certification
summary: "三人四资源、每人五基的三组延迟族共同边际精确审计；5625条偏离等式与K4/Hall记录仅支持固定输入观察，不推出一般Nash存在、复杂度或Minty结论。"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/independent_review/evidence/runs/topic_selection/nash_common_marginal_audit_2026-10-20.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/independent_review/evidence/runs/topic_selection/nash_common_marginal_audit_2026-10-20.json
---

# 共同边际三人 Nash 有限审计

## 来源和实际读取

本审查实读稳定源 ID `0b29ccace67e6c390ccd` 的完整 1,588 字节 JSON。原路径为 `history/retired_topic_selection/independent_review/evidence/runs/topic_selection/nash_common_marginal_audit_2026-10-20.json`；`legacy-cleanup` 提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `main` 提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 均有该版本，SHA-256 为 `c21edc9846150fa587f56ab998c8628229281466a0d283643cdc67be589c534e`。精确副本见 [`nash_common_marginal_audit_2026-10-20.json`](../../tools/evidence/retired-topic-selection-20261031/nash_common_marginal_audit_2026-10-20.json)。

相关历史候选报告也已实读。Nash 线报告把它放在有限工具/候选筛选范围，明确区分了随机反馈 RM+、Minty 识别、低秩双矩阵、图宽局部势等不同问题；本 JSON 没有给出这些问题的完整定义或一般证明。因而本审查只复述 JSON 明示字段，并把模型身份、偏离判定和 K4 组合记录限制在可见范围内。

## 固定输入和记录的量词

JSON 明示状态为“finite exact audit only; no theorem or novelty certification”。固定对象包括：

- 玩家数 3；资源数 4；
- 每位玩家有 5 个可行基（`bases_per_player: [5,5,5]`）；
- 共同边际向量
  \[
  (1/5,\,11/20,\,11/20,\,7/10);
  \]
- 三组 delay family，每组列出 4 条四维延迟向量；
- 对偏离关系进行 5,625 条等式检查；
- 每个 delay family 的字典序纯均衡计数为 `[5,11,3]`。

文件没有进一步给出每个基的完整元素列表、收益/成本的统一公式、字典序如何作用于并列或随机选择，也没有给出 5 个基在三名玩家之间的全部对应关系。因此不能从“每人 5 个基”反推一个特定 matroid，更不能把计数当作任意共同边际或任意延迟族的存在定理。

## 三组延迟族的实际字段

第一组四条向量为

\[
(0,1,1,2),\ (0,0,3,4),\ (0,2,2,5),\ (0,1,4,9).
\]

第二组四条向量全部为

\[
(0,1,2,3).
\]

第三组四条向量为

\[
(0,0,0,0),\ (0,2,2,2),\ (0,1,1,8),\ (0,0,5,5).
\]

这些是整数向量；共同边际是有理数。审计字段没有报告浮点运算、随机种子或采样误差，且状态写明 exact audit，因此 5,625 条偏离等式应理解为固定有限表上的精确比较。它仍然只覆盖三组列出的延迟族，不能替代对任意非减延迟、任意共同边际或任意基系统的量词证明。

## Lexicographic pure equilibrium 记录

对三组 delay family，记录的字典序纯均衡数量依次是 5、11、3。该数据可以作为固定输入的枚举结果：在各组列出的延迟向量、共同边际、三人五基配置及其既定字典序下，审计找到这些数量的候选纯均衡。

它不是以下任何结论的证据：

1. 任意三人共同边际基博弈都存在纯 Nash；
2. 精确均衡的个数随资源数或基数有单调公式；
3. 字典序选择器在一般实例上是多项式时间；
4. 共同边际等价于某个统一势函数或 Minty 可行性。

要得到这些结论，至少还需完整给出玩家成本、可行基族、延迟聚合公式及 tie-breaking 量词；当前源只保留审计输出，不包含这些缺失定义。

## K4 边编号与 Hall 障碍

文件附带一个 K4 的六边编号：

\[
(0,1),(0,2),(0,3),(1,2),(1,3),(2,3).
\]

两组基为 `[0,1,4]` 和 `[2,3,5]`；K4 spanning tree 总数记录为 16。Hall 障碍选择第一基中的左子集 `[1,4]`，其邻居子集只有 `[5]`。因此 \(|N(S)|=1<2=|S|\)，该固定二分图不满足将左子集注入右侧的 Hall 条件。

这是一个完整的有限组合证书：给定该边编号、两组基和邻接关系，子集大小不等式直接证明不存在相应的强双射/匹配。它与两容量广义指派审计中的 K4 boundary 使用完全相同的边编号和基对，但两源的目标不同：广义指派源检查联合容量舍入，当前源检查共同边际基博弈的有限组合部分。共享证书可以作为关系边保留，不得据此把“无 strong base-ordering”升级为共同边际 Nash 的一般不可能定理。

## 与 Nash 候选线的比较

历史 Nash 候选报告把有限 toy 检查与几个未决方向分开：随机反馈 RM+ 需要处理无偏噪声和正部截断；Minty 识别需要把混合 profile 的全称条件化为纯 profile 线性约束；低秩双矩阵的第二均衡和输出复杂度仍是另一个问题。当前 JSON 没有包含这些算法或复杂度输入，因而：

- 不能把 5,625 条偏离等式当作 RM+ 收敛证据；
- 不能把 K4 Hall 障碍当作 Minty 不可行性的证书；
- 不能把 5、11、3 三个计数当作低秩均衡枚举下界；
- 不能把共同边际向量的一个实例当作任意正边际或任意非负边际的代表。

源与候选报告共同支持的仅是“这些固定实例适合 exact finite audit，且 K4 组合结构需要单独保留”。它们不构成一份完整的 Nash 定理正文。

## 证据等级、缺口和去向

**有限证书。** 5,625 条偏离等式、三个固定 delay family 的纯均衡计数、K4 16 棵树和一个 Hall 子集均来自原 JSON；证据已按 SHA-256 保全。若历史脚本可恢复，应在临时目录中以有理数重跑并逐字段比较，不能只复述摘要。

**条件结论。** 在完整恢复该固定实例的基族、收益/延迟公式与 tie-breaking 后，可以把上述计数作为该实例的 exact enumeration；其余解释需等待缺失定义补齐。

**障碍。** K4 Hall 子集阻止该特定强匹配；它不阻止一般 Nash，也不证明任意延迟下无纯均衡。源没有记录一个无均衡反例。

**未完成。** 没有一般存在/复杂度定理，没有外部同行审查，没有新颖性认证，也没有把该源并入 CAG 或 unrelated-machines 模型。其独有内容仅为共同边际、三组 delay family、5,625 次精确等式和 K4/Hall 数值；去向为本审查正文与证据副本，第三阶段可用稳定 ID 建立与广义指派 K4 边界的跨线关系。
