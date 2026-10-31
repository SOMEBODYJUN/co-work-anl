---
id: "fair-allocation/four-agent-laminar-key-kernels-and-greedy-obstruction"
kind: review
type_tag: 审查
title: "四代理 laminar 核有限枚举与顺序独裁障碍"
status: "finite-exact-observation; naive-greedy-obstruction; general-reduction-open"
truth_status: "review-record"
review_level: "source-read-and-finite-replay-boundary"
scope: "SEL-LAMINAR4-KEY-v1 的八物品/十二物品核、有限枚举和顺序独裁反例；不宣称一般 laminar EF1 约化已证"
summary: "保留四代理 laminar EF1 与 ordered no-envy 约化中两个固定核的精确对象、有限 profile 枚举和顺序独裁失败机制；明确连续无界估值的全域义务仍未闭合。"
source_refs:
  - "clean:3ba6f87d2cd017e87b08:history/retired_topic_selection/multi_lane/research/topic_selection/notes/boss0_laminar_key_probe.md"
  - "workspace:cleanup/workspaces/Boss3/root/value_criteria.md"
related_objects:
  - "../审查/退役公平家务有限证据三源处置--审查.md"
  - "../审查/多线候选池实际比较与去重边界--审查.md"
---

# 对象、量词和来源身份

来源沿用 Cookson–Shah 的 SEL-LAMINAR4-KEY-v1，不是团队新题或新存在定理。模型是四代理、共同 laminar 独立集系统、非负可加估值、完整分配；目标是对任意估值 profile 和预先给定代理顺序同时找到可行分配、EF1 和 ordered no-envy。来源只做两个固定核的有限精确试攻，并明确没有独立审完原文从一般 laminar 实例到这些核的约化。

八物品核有三个类别，大小为 (3,3,2)，每人每类至多一件、总容量二；十二物品核有四个类别，大小为 (3,3,3,3)，每人每类至多一件、总容量三。ordered no-envy 只写作 \(i<j\) 时 \(v_i(A_i)\ge v_i(A_j)\)，EF1 对每个有序对允许从对方包移除一个物品。空包条件按定义为空；有限试验中的指定顺序可由估值 profile 重标号，但不把有限枚举替代所有 profile。

## 有限枚举和证据

代码按每个类别向四代理的所有单射枚举，筛掉容量不符分配后直接计算 ordered no-envy 与 EF1；另以八物品逐件 \(4^8\) 归属枚举和逐件移除 oracle 交叉检查部分完整 profile。算术是非负整数，最大单件值 \(10^6\)，不使用浮点取整。八物品可行分配计数为
\[
4\cdot3\cdot(3!)^2\cdot2!=864,
\]
十二物品为
\[
4!\cdot(3!)^4=31104.
\]
固定 seed 为 20261020；八物品测试 84 个 profile，十二物品测试 16 个 profile，含全零、单位、稀疏零值、共同非均匀和随机整数 profile。所有列出的有限 profile 均找到同时满足两个公平条件的分配，并对维度、负值、浮点、过大数、非法类别和容量边界作拒绝测试。

这些是有限精确 Observation 和可复现程序合同。它们不建立任意连续/无界估值的全称定理，也不能由“没有反例”推出两个核对一般 laminar 问题的充分性。

## 顺序独裁的精确失败机制

取八物品公共估值
\[
(1,2,3,1,2,3,1,2).
\]
在全部可行完整分配上依次最大化代理 1、2、3、4 的自身效用，所有并列选择都得到效用向量
\[
(6,4,3,2).
\]
最后代理观察第一个代理的两件价值 3 物品，删除任意一件后仍有 \(3>2\)，故 EF1 失败；这不是 tie-breaking 偶然。

同一实例存在跨类别目标分配
\[
A_1=\{g_1,g_6\},\quad A_2=\{g_2,g_8\},\quad
A_3=\{g_3,g_4\},\quad A_4=\{g_5,g_7\},
\]
其效用为 \((4,4,4,3)\)，逐项检查同时满足 EF1 和 ordered no-envy。失败机制是早期代理必须牺牲自身最大值，以保留后续跨包公平；这只排除该顺序独裁模板，不排除存在性，也不足以单独构成四人 laminar 结果的完整反例。

## 结论分层和接续

**已证有限观察。** 对列出的固定核、固定 profile 集和精确枚举域，存在满足双目标的分配；顺序独裁在给定八物品 profile 上必然产生 EF1 失败。

**障碍。** 连续无界估值尚未覆盖；十二物品核的全域组合复杂性更高；重复随机样本不会闭合全域锥。下一判别应覆盖保留包间比较的估值锥，或给出带补偿交换的构造，而不是继续堆随机样本。

**未建立。** 本源未证明两个核对所有 profile 可行，未证明原文一般 laminar 约化，未给 EF1/ordered no-envy 全类定理，也未给复杂性下界或外部新颖性结论。第三阶段可把 864/31104 可行计数、(6,4,3,2) 反例和 (4,4,4,3) 见证连接到 fair-allocation 的独立对象，但需保持“有限证据”和“障碍”标签。
