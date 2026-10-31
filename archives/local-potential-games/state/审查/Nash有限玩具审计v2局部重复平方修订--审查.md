---
id: local-potential-games/nash-finite-toy-audit-v2-localized-squaring
kind: review
type_tag: 审查
title: Nash有限玩具审计v2局部重复平方修订
status: finite-exact-audit; corrected-pathwidth-certificate; universal-geometric-claim-still-conditional
summary: "v2 保留 RM+、噪声和 Minty 有理核验，并把局部重复平方构造的 n≥2 路径宽上界修订为3且给出K4 minor；KKT只核对显示profile，几何分离仍依赖单独全称论证。"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/independent_review/evidence/runs/topic_selection/nash_equilibria/toy_results_v2.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/independent_review/evidence/runs/topic_selection/nash_equilibria/toy_results_v2.json
---

# Nash 有限玩具审计 v2：局部重复平方修订

## 来源、SHA 和与 v1 的关系

本审查实读稳定源 ID `1d1e2617403c3b28cf64` 的完整 30,259 字节 JSON，原路径为 `history/retired_topic_selection/independent_review/evidence/runs/topic_selection/nash_equilibria/toy_results_v2.json`。`legacy-cleanup` 提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 和 `main` 提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 均有该版本，源 SHA-256 为 `2a08aba541bf1cc78052f99042a191d56b6552381b936eb2b2335be4ddbee3f5`。副本见 [`nash_toy_results_v2.json`](../../tools/evidence/retired-topic-selection-20261031/nash_toy_results_v2.json)。

v2 不是 v1 的简单重命名：RM+ 一步恒等式、噪声反例、Minty 25 anchors 等数值相同，但局部重复平方段给出完整 path-bag 顺序、n≥2 的 K4 minor 以及 pathwidth 恰为 3 的记录；v1 仅保留较粗的上界 6。两源都保存，以便第三阶段追踪修订而不把新证书伪装成旧版本内容。

## 共享的 exact 核验

算术为 Fraction、确定性枚举、无 seed。二元一步恒等式检查 275 个状态，三元检查 3,750 个状态。噪声分支仍为

\[
(0,1/2)\to r'=(1,1/2),\ x'=(2/3,1/3),\ \Delta\Phi=-1/6;
\qquad
(1,-1/2)\to r'=(1,0),\ x'=(1,0),\ \Delta\Phi=0.
\]

等概率平均真实势增量为 `-1/12`，下一真实 gap 平均为 `1/12`。Minty 二人协调仍检查 25 个 rational anchors，symbolic average 为 `-1`。这些有限 identity/反例保持 v1 的范围：它们排除“无偏噪声必使期望势上升”，并对所列 25 个网格点给出统一负值，但不建立随机 RM+ 收敛或连续域 Minty 不可行性定理。

## 局部重复平方的 v2 图证

### n=1 与 n≥2 的结构

对 n=1，玩家数为 5，最大度 3，最大单项式次数 2，路径宽上界为 2；源列出三个长度很短的 bags。对每个 n=2,…,12：

- 玩家数为 \(5n\)；
- 最大度为 6；
- 最大单项式次数为 3；
- `pathwidth_certificate_upper_bound` 为 3；
- 每个 n 测试 3 个扰动 profile；
- `k4_minor_branch_sets` 固定给出四个 branch sets `[x1]`, `[z1]`, `[c2]`, `[t2,x2]`；
- `pathwidth_exact_if_n_ge_2` 为 3。

源还保存从 n=2 到 n=12 的完整 path-bag 顺序：每个阶段依次经过 `t_i`、`c_i`、`d_i` bags，变量只在相邻阶段连续出现；因此该审计的图字段比 v1 的“上界 6”更精确。K4 minor 给出 treewidth 至少 3，而 bag 分解给出 pathwidth 至多 3，故在 JSON 声明的图定义和构造变量下得到 pathwidth/treewidth=3 的有限结构证书。

### 梯度范围和收益规范化

v2 记录的符号范围为：

| 坐标 | 全域梯度范围 |
|---|---|
| `t_i` | `[-3,-1]`（`t_1` 为 `[-9/4,-5/4]`） |
| `c_i` | `[-1,1]`（`c_1` 为 `[-3/4,1/4]`） |
| `d_i` | `[-1,1]` |
| 非末端 `x_i` | `[-5/2,5/2]` |
| 非末端 `x'_i` | `[-3/2,3/2]` |
| 末端 `x_n` | `[-7/2,-1/2]`；原 NE 且 `t_n=0` 后为 `[-7/2,-3/2]` |
| 末端 `x'_n` | `[-5/2,-3/2]` |

局部收益定义为

\[
u_v(a)=a_v\,\partial_v\Psi(a_{-v})/4,
\]

全局绝对值不超过 7/8。这个定义和图证对应的是稀疏局部收益；不能把全局势 \(\Psi\) 误当作每个玩家都直接观察的完整 utility。v2 警告 KKT 只在显示的 profile 上逐坐标精确检查。

### 扰动与分离边界

`precision_statement` 记录显示 profile 到原 NE 集合的分离下界为 1/2，并标记“排除闭半径 1/4 球”；同时明确提醒：距离 \(\ge1/2\) 本身不足以排除闭半径 1/2 球。这个边界修正很关键：正文可以声称在给定构造与全称分离论证成立时，固定 \(\delta=1/4\) 的闭球性质失败；不能把它夸大为排除所有半径 \(1/2\) 或更大保证。

## 证据分层和未闭合部分

**有限证书。** v2 给出 275/3,750 个一步恒等式、两个噪声分支、25 个 Minty 网格 anchor、n=1..12 的 3 次扰动记录、梯度区间、path-bag 分解和 K4 minor。所有数值为 Fraction 或整数，未使用随机 seed。

**条件结构结论。** 在采用源中局部收益、图定义和变量命名的前提下，v2 的 path-bag 与 K4 branch-set 记录支持 n≥2 的 pathwidth/treewidth=3 组合证书。它不自动说明同一图宽约束下所有势博弈都具有该几何性质。

**仍未完成。** JSON 明确写出：KKT 只在显示 profile 检查，几何分离到所有 exact NE 需要 `REPORT.md` 的独立全称论证；有限样本不证明一般定理或渐近收敛。因此本源不证明双指数扰动位下界、不证明随机 RM+ 收敛复杂度、不证明 Minty 识别 coNP/多项式边界，也不认证新颖性。v2 的独有去向是本审查正文、证据副本及与 v1 的版本关系；不要把 v1 的粗路径宽字段覆盖掉。
