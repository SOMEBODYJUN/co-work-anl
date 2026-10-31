---
id: local-potential-games/nash-finite-toy-audit-v1
kind: review
type_tag: 审查
title: Nash有限玩具审计v1
status: finite-exact-audit; superseded-by-v2-for-localized-graph-certificate; no-asymptotic-theorem
summary: "v1 有理数精确核对 RM+ 一步恒等式、噪声势下降、Minty 协调玩具与局部重复平方样本；其 pathwidth 记录为较粗的上界6，不能当渐近收敛或几何分离定理。"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/independent_review/evidence/runs/topic_selection/nash_equilibria/toy_results.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/independent_review/evidence/runs/topic_selection/nash_equilibria/toy_results.json
---

# Nash 有限玩具审计 v1

## 来源和实际读取

本审查实读稳定源 ID `d406d5ce806cac7e1c9f` 的 6,251 字节 JSON，原路径为 `history/retired_topic_selection/independent_review/evidence/runs/topic_selection/nash_equilibria/toy_results.json`。两个历史版本（`legacy-cleanup` 提交 `68fad804ec5946cb296f77dc5b336308a66abf12`、`main` 提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`）一致，源 SHA-256 为 `de596c41b04878990b835e9b344c714bcd448db8b38be8f327ad2bedc6667c8a`。副本见 [`nash_toy_results_v1.json`](../../tools/evidence/retired-topic-selection-20261031/nash_toy_results_v1.json)。

Nash 候选报告把这些记录拆成 RM+、Minty 识别、随机反馈和局部势候选；本审查保留 v1 的历史位置，特别注明 v2 后来修正了局部重复平方的路径宽证书。两版本不是字节重复：v1 的图证书较粗，v2 记录了新的袋分解和 K4 minor。

## 算术与一步恒等式

JSON 声明 `Fraction exact; deterministic enumeration; no seed`。`one_step_identity` 在二元（标记为 `2`）上核对 275 个状态，在三元（标记为 `3`）上核对 3,750 个状态。它们是 RM+ 一步更新相关代数恒等式的有限检查；文件没有给出所有玩家动作集合、全局势的完整量词或长期轨迹，因此不能从计数推出收敛率、最佳迭代复杂度或一般 \(\epsilon\)-Nash 结论。

## 无偏噪声不保证期望势上升

单步噪声例的两个分支为：

| 观测 \(u\) | 下一状态 \(r'\) | \(x'\) | 真实势增量 | 下一真实 gap |
|---|---|---|---:|---:|
| `(0,1/2)` | `(1,1/2)` | `(2/3,1/3)` | `-1/6` | `1/6` |
| `(1,-1/2)` | `(1,0)` | `(1,0)` | `0` | `0` |

两分支等概率且观测均值无偏，但 `expected_true_gain` 为 `-1/12`，`expected_true_gap` 为 `1/12`。这是一条精确反例：无偏观测、正部截断和状态归一化共同作用时，不能直接声称真实势的期望单调上升。它不证明 RM+ 不收敛，只排除一个过强的 Lyapunov 推理；要得出随机算法界仍需显式控制噪声、clipping 与 regret-state。

## Minty 二人协调玩具

`minty_two_player_coordination` 穷举了 25 个有理 anchors（坐标网格为 0、1/4、1/2、3/4、1）。记录的 `universal_symbolic_average` 是 `-1`；25 行分别给出每个 anchor 的两坐标和对应平均偏离值，最有利的边界也没有使该符号变为正。该记录支持固定二人协调玩具不存在所测试的 Minty anchor，但它不是对所有 anchor 连续域的独立证明，除非另有符号恒等式；更不能外推到任意图宽或任意 payoff 因子。

## 局部重复平方 v1 记录

对 \(n=1,\ldots,12\) 的构造，JSON 记录每个 n 有 \(5n\) 个玩家、3 次扰动测试。n=1 时最大度 3、pathwidth certificate upper bound 4、最大单项式次数 2；n≥2 时最大度 6、pathwidth 上界 6、最大单项式次数 3。每个固定 n 的有限 KKT/符号检查通过，但 v1 没有记录完整袋序列、K4 minor 或“距离所有原 NE 至少 1/2”的全称证明。

因此 v1 最多支持：显示的 profile 在有限精度下满足该构造的局部梯度符号，且重复平方样本的邻接度/次数没有超出记录上界。它不能单独支持路径宽恰为 3、双指数扰动位障碍或几何分离定理；这些需要读取 v2 及其独立报告。

## 结论等级与后续

**有限证书：** 275+3,750 个一步恒等式、两分支噪声下降数值、25 个 Minty 网格 anchor、n=1..12 三次扰动的梯度/图字段。

**障碍：** 无偏噪声破坏期望势单调；二人协调的 25 点 Minty 检查给出统一负平均；一阶局部构造的 v1 图宽只给粗上界。

**未完成：** 没有一般 RM+ 随机收敛算法、没有 Minty 识别复杂度定理、没有全称扰动 NE 几何分离，也没有外部新颖性认证。v2 的更精确图证将作为独立来源保存，不能改写为 v1 已含。
