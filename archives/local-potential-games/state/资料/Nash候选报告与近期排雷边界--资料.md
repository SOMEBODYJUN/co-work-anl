---
id: local-potential-games/nash-candidate-map-and-literature-boundaries
kind: resource
type_tag: 资料
title: Nash候选报告与近期排雷边界
status: retained-candidate-map-literature-checked-not-selected
truth_status: candidate-map-with-finite-audits-and-literature-scope
review_level: full-source-read-cross-archive-comparison
summary: 保留 Nash 子线六类候选、近期文献排雷、三条可核查切口及其取舍；明确 NASH-04 已降为工具引理，NASH-01/02仍为预候选，其他方向为低优先级或远期地图，不把选题报告、有限玩具或文献检索升级为定理。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/independent_review/research/topic_selection/nash_equilibria/candidate_report.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/independent_review/research/topic_selection/nash_equilibria/candidate_report.md
legacy_ids:
  - 9dc1c4b55dd60a4313f9
evidence_paths:
  - archives/local-potential-games/state/资料/局部三次势扰动精度的候选与半球修订--资料.md
  - archives/local-potential-games/state/审查/Nash有限玩具审计v1--审查.md
  - archives/local-potential-games/state/审查/Nash有限玩具审计v2局部重复平方修订--审查.md
  - archives/local-potential-games/tools/evidence/retired-topic-selection-20261031/nash_toy_results_v1.json
  - archives/local-potential-games/tools/evidence/retired-topic-selection-20261031/nash_toy_results_v2.json
---

# 来源身份与总体处置

本对象对应冻结来源 history/retired_topic_selection/independent_review/research/topic_selection/nash_equilibria/candidate_report.md（源 ID 9dc1c4b55dd60a4313f9，blob 3d2a1703aae1f34e0f2256515d09e4a8386102dc，SHA-256 dbe0996ab56ba50cc7ab343a86944bc537d115ad9e8a33cb8cdc4dd05ee1eb9e，27137 字节、227 行）。我完整阅读了六候选报告，并与 local-potential-games 的模型资料、Nash v1/v2 有限玩具审查、nash_toy_results v1/v2 JSON 及现有局部三次势对象比较。

报告是研究选题地图和排雷记录，不是数学定理。它明确拒绝把一般近似 Nash、一般三人精确均衡复杂性或所有势博弈快速算法作为默认主线；六候选中只有 NASH-02 仍列第一顺位预候选，NASH-01 为方法备选，NASH-04 已因论文价值降级为工具引理。NASH-03、NASH-05、NASH-06 只保留为低优先级/远期地图。

## 六候选的精确状态

| ID | 切口 | 当前状态 | 主要边界 |
|---|---|---|---|
| NASH-01 | 零 regret 初始化的同时 RM+，有理多线性势上的统一 best-iterate NE 界 | 方法备选，未闭合 | 大初始化可得的小核不能推出零初始化的统一速率；首激活量可能极小 |
| NASH-02 | 有界无偏随机全信息反馈下交替 RM+ 的高概率 \(\epsilon\)-NE 与样本复杂度 | 第一顺位预候选，仍开放 | 需处理 clipping 与相关噪声；通用随机梯度量级若无 RM+ 优势则价值不足 |
| NASH-03 | bounded-treewidth polymatrix/局部因子博弈的 Minty 可行性识别与证书 | 低优先级基线/子引理 | 可能只是 Minty LP 分离与标准 bounded-treewidth DP 的组合 |
| NASH-04 | 局部三次势的最大度6、pathwidth恰3和双指数扰动精度障碍 | 已降级工具引理 | 共享 \(t\) 原构造本来已有常数 pathwidth，局部化可能只是 remark 级加强 |
| NASH-05 | rank-one 双矩阵且 \(a\) 有限 distinct values 时，全部孤立 NE 或第二 NE 的 output-polynomial 枚举 | 远期备选 | 零和部分仍任意；低秩不自动限制 LP 轨迹或多均衡数量 |
| NASH-06 | 3×3 零和博弈 full-support 非退化类的固定置信度实例依赖采样复杂度 | 有价值但技术体系较远 | 必须区分 \(\operatorname{Gap}(\mathbb E[x])\) 与 \(\mathbb E[\operatorname{Gap}(x)]\)，不能退回 n×2 旧问题 |

这张表是报告的选题判断，不是对候选可解性的证明。每一项都应保留“候选、有限核验、开放义务”的不同状态。

## NASH-01：同时 RM+ 的小核与真实缺口

报告采用 \(X=\prod_i\Delta(m_i)\)、多线性势 \(\Phi\)、同时更新
\[
g_i=u_i-\langle x_i,u_i\rangle\mathbf1,\qquad
r_i'=[r_i+g_i]_+,\qquad x_i'=r_i'/\|r_i'\|_1.
\]
它在假设初始 \(R_i^0\ge4m_iL\) 时重新推导一个可完成但可能不够新颖的 best-iterate 小核：令 \(q=r'-r\)、\(D=\langle x'-x,u\rangle\)，利用正部截断得到
\[
2\|r'\|_1D=R'^2-R^2+\|q\|_2^2,\qquad
R'^2-R^2\ge\|q\|_2^2,\qquad
R'-R\le\sqrt m\,D.
\]
进一步
\[
\|x'-x\|_2^2\le4mD/R',
\]
从而在大初始化区间内势增量可由 \(\sum_iD_i\) 控制，给出显式 \(O(\epsilon^{-2})\) best-iterate 界。

报告明确把这项推导标作内部完整推导、未独立审查、未声称新颖。真正首个义务是从 \(r_i^0=0\) 或任意有理 \(x^0\) 出发，控制低状态 blocks 对同时更新 cross term 的累计负贡献，且不隐藏最小首激活量。若只能保留大初始化，或该结论被一般 gradient 方法直接替代，应降为工具。

## NASH-02：噪声反馈的精确障碍与开放接口

报告限定 binary polymatrix exact potential game、局部 payoff range、有界无偏全动作估计，目标是总样本预算下高概率输出 max best-response gap \(\le\epsilon\) 的真实 profile。它保留 RM+ 而不是把问题改写成一般随机梯度。

报告给出一人二动作精确噪声反例：真实 \(u=(1/2,0)\)、\(r=(1,0)\)、\(x=(1,0)\)，观测以概率 \(1/2\) 为 \((0,1/2)\) 或 \((1,-1/2)\)。观测无偏且有界，但第一分支后 \(r'=(1,1/2)\)、\(x'=(2/3,1/3)\)，真实势变化 \(-1/6\)，另一分支不动；期望真实势变化为 \(-1/12\)，期望新 gap 为 \(1/12\)。这只排除“无偏观测必使真实势期望上升”的错误 Lyapunov 推理，不是 RM+ 不收敛反例。

可继续的证明接口是：在条件估计误差 \(\|\hat u-u\|_\infty\le\eta\) 且当前 gap 至少 \(\epsilon\) 时，建立带显式 noise penalty 的势/状态增量，并把罚项按总样本预算求和。必须处理 positive-part 与噪声相关、误判最佳动作对 regret state 的持久影响，以及 batch 选择；仅证明 batch 逐渐增大而渐近收敛不够。

## NASH-03：Minty 识别的结构化候选

对给定局部收益图和 tree decomposition，报告把 Minty 条件的全称混合约束降到 pure profile 检查：\(q_{x^*}(y)\) 是 block-multiaffine，最小值可在 pure profile 取得，于是约束变成关于 \(x^*\) 的线性系统
\[
\sum_i\sum_{a_i}x_i^*(a_i)u_i(a_i,s_{-i})
\ge\sum_i u_i(s).
\]
候选方向是 bounded-treewidth separation + LP/ellipsoid 输出 anchor 或 infeasibility certificate。报告同时记录二人 common-interest coordination 的 25 个有理 anchor 检查均不支持 Minty anchor；这只是有限玩具，不是连续域识别定理。由于该方向很可能直接组合已知 Minty LP 和图宽 DP，当前不作为主押。

## NASH-04：已整理的工具引理

报告的 NASH-04 内容已经由 local-potential-games 的资料对象与 v2 审查单独整理：局部复制 \(t_i\)、完整梯度、全区间扰动 profile、原 NE 全称分离、闭半径 \(1/2\) 修正、最大度6、pathwidth/treewidth恰3、收益归一化和编码边界均已登记。本候选报告的独有贡献是把它从主课题地图中降级：共享 \(t\) 版本本来就有常数 pathwidth，局部化主要去除高程度 apex，同行可能视为 remark 级推论。它不支持一般 NE 求解时间下界，也不自动给 treewidth \(\le2\) 或 Berge-acyclic 三元势的正向定理。

## NASH-05：rank-one 枚举边界

报告考虑非退化有理双矩阵 \(A+B=ab^\top\)，且 \(a\) 只有 \(k\) 个 distinct values，目标是 output-polynomial 枚举全部孤立 NE 或判定第二个 NE。\(k=1\) 可归入零和最优面；但 \(A\) 的零和部分仍可任意，不能从“找到一个”推出“第二个或全部”容易。首先应精确枚举 3×3、4×4 小输入的 support/path crossings，并研究 \(k=2\) 是否能控制 LP 段数；当前没有足够证据把它列近期开题。

## NASH-06：3×3 零和实例依赖采样

报告限定 full-support、非退化 3×3 零和矩阵和固定置信度 \(\epsilon\)-exploitability 输出，目标是把 support slack、basis conditioning 和 change-of-measure 下界纳入查询复杂度。它明确指出 n×2 已有研究，不能退回 2×2；也明确不把后来 LP-resolving 结果中对 \(\mathbb E[\text{output}]\) 的保证误读成 \(\mathbb E[\text{Gap(output)}]\) 或高概率 \(\epsilon\)-NE。需要先构造相同 entry gap、不同 equilibrium basis condition number 的矩阵对，再做 answer-set 量词下界；否则只能得到 uniform sampling 旧式估计。

## 近期排雷与文献边界

报告记录的排雷改变了若干旧选题直觉：

- Minty 条件 VI 的多项式算法已有新工作；不能把“Minty 下是否有 poly-log 精度算法”作为未核查开放题。
- 同时 RM+ 已有母文覆盖；不能把 alternating 限制当成同时更新的开放性证据。
- 某 alternating RM+ 公开稿后来撤回；撤回不是数学反证，也不能把撤回稿当已接受定理，更不能忽略其公开优先权风险。
- 两队各两人的 team zero-sum/polymatrix NE 复杂性已有 PPAD-complete 结果；不能以旧版 2v2 复杂性问题重提。
- paths、stars、caterpillars 的 graphical/polymatrix exact NE 已有近期正结果；不能把旧 caterpillar 问题原样重提。
- 矩阵博弈实例复杂性已有新 LP-resolving 进展，但其期望与 gap 的量词必须逐字核对。

这些条目来自源报告列出的论文、作者稿和会议材料；本对象保留其核验范围和 URL/ref 线索，不把“检索未发现同定理”写成新颖性认证。特别是撤回稿的作者身份/机构状态与数学正确性是两个独立问题。

## 有限证据和复用边界

local-potential-games 的 v1/v2 JSON 只提供 Fraction 精确的 275/3750 一步恒等式、两分支噪声例、25 Minty anchors、n=1..12 的图和梯度字段，以及 v2 的 pathwidth 3/K4 证书。它们不能证明一般 RM+ 收敛、Minty 识别复杂度、所有扰动 NE 的渐近几何或任何候选的新颖性。

第三阶段若建图，可把本对象连到：

- local cubic potential 资料与 NASH-04 v2 审查：同一工具引理的候选地图与内部证据；
- NASH-02 噪声反例：用于约束未来 Lyapunov 证明的障碍；
- Minty v2 finite toy：用于识别方向的有限反例；
- 退役选题/公平商品目录：仅作来源历史关系，不能把 Nash/local-potential 模型迁移为 fair-goods 或 CAG/SPE 定理。

当前处置是 retained candidate map。没有建立新定理、没有把六候选选定为主课题，也没有把有限玩具、作者稿状态、会议接收或文献排雷升级为外部证明或新颖性结论。
