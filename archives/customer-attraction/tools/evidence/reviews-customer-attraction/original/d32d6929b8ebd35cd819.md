# 冻结真实前缀联合席位预算：内部解析及独立数值审查

对象：**CA-PREFIX-COUPLED-SEAT-BUDGET-v1**，[现行陈述与证明](../../current/customer_attraction/general_half_proof.md#31-冻结真实前缀的联合客户席位一般付款的精细加强)。原 Q-CAG-HALF 仍 OPEN；本页不认证外审或数学新颖性。

## 解析审查的实际顺序与范围

提出者的一般[原推导](../../workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/continuation_general/omission/prefix_coupled_seat_budget.md)先给 G_j(k)=a_j/k+Σ_(B_j\Q_j)1/(b_x+r)。另一内部研究员仅收到该精确陈述，未读作者证明，独立用动作归属与同叶包含支配重构了全历史阈值归纳。随后才读作者完整 F 稿并检查其更强极小化，不能把后者也称为盲重构。[原审查记录](../../workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/continuation_general/induction/private_offset_spectrum_independent_review.md)保留完整先后与证明。

root 另按定义核对了承重步骤：

- 起始 b、r、F/G 及全部 Q_j 在当前子树内保持固定，不能在离轨后重选实际遗漏。
- 一项合法动作最多触及一个 Q_j；触及 Q_j 的主题必包含于合法极大 B_j。
- 有后继触块时，当前完整 B_j 在同一真实终局支配那个后继，后者的收益来自同一给定 SPE 的离轨历史归纳。
- 无后继触块时，当前以外的 r−1 个真实主题包含子树中已行动者与真实未来者，触块数恰为 q_j，故可代入 F_j(q_j+1)。索引 q_j+1≤d_j≤r。
- 约束集非空由避开 Q_j 的实际主题重复得到；r=1 使用空元组。阈值为零直接用收益非负；全部并列、空主题、重复和零客户均保留。

在这些定义下未发现解析漏洞。每个实际位置仅由其 u_i 支付一次，得到 W≥ΣΛ_i≥Σλ_i。若 Q_j 全空，则让静态竞争者重复 B_j 达到所有根客户的最大负载，故 F=G，退回原分母界。

## 另一研究员的独立有限证据

[独立数值审查原记录](../../workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/continuation_general/menu/refined_spectrum_numerical_review.md)只读作者的单位客户输入和指定路径，未读或导入作者脚本、规范模型或 SPE 求解器。原输入没有完整动作表，审查员从完整有序树独立补全一个实现该路径的 SPE，再逐节点重放全部比较；不是声称检查输入中不存在的原动作表。

移入标准位置的[审计脚本](../../../tests/audits/customer_attraction_prefix_coupled_seats.py)保留该定义级实现。它展开124个单位客户，确认31个有序决策节点的155项含自身比较（124个真正偏离），路径收益为(37,30,28)，W=95，OPT=100。显式 G 谱总和为127/2，旧两界逐位置最大值之和为184/3，严格差为13/6。root 已重跑此脚本并核对反算。

输入：[严格区分实例](../../../examples/customer_attraction/prefix_coupled_seats_strict.json)；冻结结果及独立补全动作表：[精确记录](../../../evidence/runs/2026-10-23/customer_attraction_prefix_coupled_seats.json)。默认执行脚本只核验和打印摘要，不改冻结记录；显式 `--output` 可写新的运行报告。

有限审计证明的是指定例的完整可实现性、精确数值和严格区分，不证明任意人数引理。一般性由解析阈值归纳承担；本次没有独立计算该例的精确 F 极小值或 Λ_i。

## 结论等级

本一般预算内部解析与所列有限证据检查完成。它严格加强既有两个保底的逐位置最大值，沿用已有超集席位归纳；不认证全球新颖性。尚未证明 ΣΛ_i≥OPT_m/2 或 OPT_m−W≤ΣΛ_i，未扩大原目标已证范围，全部共享遗漏的全树支付仍 OPEN。
