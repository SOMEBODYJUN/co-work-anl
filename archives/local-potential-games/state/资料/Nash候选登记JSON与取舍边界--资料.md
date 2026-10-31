---
id: local-potential-games/nash-candidate-registry-json-and-selection-boundaries
kind: resource
type_tag: 资料
title: Nash候选登记JSON与取舍边界
status: retained-candidate-registry-update
truth_status: candidate-map-and-literature-scope; no-theorem
review_level: full-json-read-cross-archive-comparison
scope: "Nash计算与优化理论的六条候选及已排雷目标；不延续一般近似Nash或传统加权拥塞主线"
summary: "完整读取 nash_equilibria/candidates.json（2026-10-20），与已有候选报告、NASH-04独立审查和有限 toy 证据对照。NASH-02 是唯一第一顺位预候选，NASH-01 为方法备选，NASH-04 降为工具引理，其余只作低优先级地图；已解决或重复的旧目标单列。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/independent_review/research/topic_selection/nash_equilibria/candidates.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/independent_review/research/topic_selection/nash_equilibria/candidates.json"
---

# Nash候选登记JSON与取舍边界

本文完整读取冻结 nash_equilibria/candidates.json（20,333 bytes，SHA-256 801e10e15f2fd9db599d7fbb8c3a208a975364066ca674d4725556885679041c，研究日期 2026-10-20），并与[候选报告与近期排雷边界](Nash候选报告与近期排雷边界--资料.md)、[Nash-04独立审查](../审查/Nash-04独立审查报告与候选边界--审查.md)、Nash v1/v2 有限 toy 结果和 local-potential-games 现有对象比较。JSON 是候选池登记和优先级更新，不是定理或新颖性认证。

## 1. 总体范围和排序

范围是 Nash 计算与优化理论，明确避开一般近似 Nash 和传统加权拥塞主线。登记的 evidence policy 将 Paper Fact、本组新 idea、exact 计算和全称证明分开；“未检索到同定理”不等于新颖性。

当前唯一第一顺位预候选是 NASH-02；NASH-01 是方法备选；NASH-04 已因价值不足降为工具引理，不强行补第二主押；NASH-03、NASH-05、NASH-06 只保留为低优先级/远期地图。

## 2. 六条候选的精确状态

### NASH-01：零初始化同时 RM+ 的统一 regret 与 NE 速率

模型是 \(n\) 个 simplex 上的有理多线性势 \(\Phi\)，\(\nabla\Phi\) 为 \(L\)-Lipschitz；同时更新

\[
r_i^+=[r_i+u_i-\langle x_i,u_i\rangle\mathbf1]_+,\qquad
x_i=r_i/\|r_i\|_1,
\]

从标准零态 \(r_i^0=0\) 开始，求实际迭代点满足 \(\max_i BRGap_i\le\varepsilon\)，目标参数统一 \(O(\varepsilon^{-2})\) 迭代界，复杂度不得隐藏首激活 regret 的倒数。登记状态 OPEN_RESCOPED_WITH_DUPLICATION_RISK：大初始化 \(R_i^0\ge4m_iL\) 的短推导已有，但零初始化低 state blocks、截断 cross terms 和极小首激活仍未统一控制。4,025 个 Fraction 单步检查是有限证据，不是零初始化全称结论。

### NASH-02：随机全信息反馈下 RM+ 的势与噪声记账

模型是 binary polymatrix exact potential game，最大度 \(\Delta\)、局部 payoff range \(\le1\)，单玩家交替激活，收到条件无偏、\(\sigma^2\)-次高斯的全动作收益向量；目标是显式计费 batch 样本，在概率至少 \(1-\delta\) 下输出实际 profile，满足 \(\max_i BRGap_i\le\varepsilon\)。bandit 反馈另立版本。登记状态 OPEN、priority 1。

首要障碍是 positive-part 截断与无偏噪声相关：一人二动作 \(u=(1/2,0),r=(1,0)\) 的两点噪声观测会给真实势期望下降 \(-1/12\)，因此不能声称“无偏观测使真势期望单调”。真正义务是建立带显式噪声罚项的单步下界，再按总 oracle 预算求和；仅给 generic SGD 或无样本计费的渐近界不满足候选合同。

### NASH-03：有界树宽局部博弈的 Minty 可行性和证书

模型是有理局部因子博弈，每玩家至多 \(m\) 动作，收益因子 primal graph 给定宽 \(w\) tree decomposition。目标是判定是否存在 \(x^*\) 使

\[
\sum_i[u_i(x_i^*,y_{-i})-u_i(y)]\ge0
\]

对所有混合 \(y\) 成立，并输出 anchor 或 strict aggregate-CCE 不可行证书。候选机制是 block-multiaffine 函数的最小值落在 pure profile，将 Minty 条件化为关于 \(x^*\) 的线性约束，再以 bounded-treewidth DP 做 separation。登记状态是低优先级基线：很可能只是既有 Minty LP/Prop1.14 与标准图宽 DP 的组合。二人 common-interest coordination 的25个有理 anchor 检查平均符号为 \(-1\)，只支持有限玩具边界。

### NASH-04：路径宽恰3的有界度三次势精度障碍

模型是 binary graphical exact potential，局部三次有理单项式，最大度 \(\le6\)、\(n\ge2\) 时 pathwidth/treewidth 恰3；扰动变量在 \([\varepsilon,1-\varepsilon]\)，固定闭球半径 \(\delta=1/4\)。候选构造复制 \(x\) 变量和 \(t_i\)，链式重复平方给全原 NE 分离，K4 minor 给宽3下界。状态 DEMOTED_TOOL_LEMMA_NOT_MAIN_TOPIC：共享 \(t\) 的旧构造本来已有常数 pathwidth，局部化主要去掉高阶 apex，同行可能视为 remark 级加强。现有独立审查已修正闭半径 \(1/2\) 边界、收益归一化和编码表述；不支持一般 NE 求解时间下界或 treewidth \(\le2\) 正向定理。

### NASH-05：rank-one 双矩阵的输出敏感枚举

模型是非退化有理 \((A,B)\)，\(A+B=ab^\top\)，且 \(a\) 有 \(k\) 个 distinct values；先固定 \(k=2\)，目标是枚举全部孤立 NE（时间 polynomial in input and output length）或判定第二 NE 存在。低秩不限制零和部分的 LP 轨迹或均衡数量，登记状态 OPEN_HIGH_DIFFICULTY，保留为远期结构问题。首要义务是控制均衡之间的无输出 LP segments，不能只重做“找一个 NE 在 P”的路径算法。

### NASH-06：3×3 零和固定置信度实例依赖采样

模型是未知 \(A\in[-1,1]^{3\times3}\)，可自适应查询独立有界/已知方差样本，promise 唯一 full-support 非退化 NE。目标是以概率至少 \(1-\delta\) 输出 exploitability \(\le\varepsilon\) 的 \((x,y)\)，优化期望查询数和实例依赖。登记状态 OPEN_BUT_DIFFERENT_TECHNICAL_STACK；必须区分 \(Gap(\mathbb E[\text{output}])\)、\(\mathbb E[Gap(\text{output})]\) 和高概率保证，并对所有 \(\varepsilon\)-答案集合量化。它不能退回已有 n×2 结果，技术体系与当前主线较远。

## 3. 已解决、重复或不应重提的目标

登记明确列出以下排雷：

* Minty 下 poly\((\log(1/\varepsilon))\) VI 算法已有最新结果，不能继续作为未核查开放题；
* simultaneous RM+ 收敛已有母文结果，不能把 alternating 限制冒充 simultaneous 开放性；
* alternating RM+ 公开稿的撤回不是数学反证，但其公开优先权和作者状态需单独记录，不能当已接受定理或完全不存在；
* two-team 2v2 polymatrix NE 复杂性已有 PPAD-complete 结果，旧目标不可原样重提；
* caterpillar graphical/polymatrix exact NE 已有近期多项式结果，不能沿用旧 OPEN 标签；
* 新 LP-resolving 工作的期望与 exploitability 量词必须逐字核对，不可把邻近保证升级成 NASH-06 目标。

这些条目改变候选池地图，但不等于对相应近期论文做新的外部验证；JSON 保留 URL/ref 线索而不把检索结论写成优先权认证。

## 4. 有限证据和模型边界

关联 toy 文件只覆盖有限、精确 Fraction 检查：RM+ 一步结构、两点噪声反例、25 个 Minty anchors、NASH-04 的 \(n=1,\ldots,12\) 梯度/路径袋/K4 字段。它们不能证明一般随机 RM+ 收敛、Minty 识别复杂度、所有扰动 NE 几何、rank-one output-polynomial 枚举或 3×3 样本下界。

这些候选属于 local-potential-games 的势/博弈模型，不能自动迁移成 weighted-congestion 的全局近似 PNE 定理、facility-games 的客户续局或 CAG 的顺序 SPE。尤其 NASH-02 的噪声反馈需保留全信息 payoff estimator、交替激活和总样本计费，不能改写成无约束通用 SGD。

## 5. 处置

本源处置为 retained candidate map update。JSON 独有的六条候选精确定义、状态排序、近期排雷、NASH-02 反方障碍和 NASH-04 降级理由已保存；不制造新定理、复杂度结果或新颖性结论。第三阶段若建关系，应将 NASH-02 标为预候选、NASH-01 标为方法备选、NASH-04 标为工具引理、NASH-03/05/06 标为低优先级地图，并把已解决/重复目标作为排除关系，不把候选登记串成一个统一证明链。
