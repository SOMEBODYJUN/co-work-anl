---
id: local-potential-games/nash-04-independent-review-source
kind: review
type_tag: 审查
title: Nash-04独立审查报告与候选边界
status: internally-reviewed-candidate-scope-corrected
truth_status: finite-evidence-plus-conditional-geometric-lemma-not-general-theorem
review_level: full-source-read-cross-archive-comparison
summary: 实读 NASH-04 局部三次势独立审查报告；确认任意 n 的梯度、扰动 profile、全称原 NE 分离、n≥2 的最大度6与pathwidth恰3推导，并保留闭半径1/2修正、编码和论文价值边界。该报告支持候选工具引理，不支持一般收敛、NE求解时间下界或新颖性结论。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/independent_review/research/topic_selection/fair_goods/nash_sparse_potential_review.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/independent_review/research/topic_selection/fair_goods/nash_sparse_potential_review.md
legacy_ids:
  - b0b8f127a083b2c53cfb
evidence_paths:
  - archives/local-potential-games/tools/evidence/retired-topic-selection-20261031/nash_toy_results_v2.json
---

# 来源与处置

本对象对应冻结来源 history/retired_topic_selection/independent_review/research/topic_selection/fair_goods/nash_sparse_potential_review.md（源 ID b0b8f127a083b2c53cfb，blob aef0cce6c05b6e59500b3b5353975486d8144e9e，SHA-256 16980bd408bf8063fd3ee90a1c788f3cd68c554b75441b7d4412daf61192c70c，11617 字节、170 行）。我完整实读了报告，并与现行[局部三次势扰动精度的候选与半球修订](../资料/局部三次势扰动精度的候选与半球修订--资料.md)、[Nash 有限玩具审计 v2](Nash有限玩具审计v2局部重复平方修订--审查.md)、v1 审计和 nash_toy_results_v2 证据逐项比较。

报告的身份仍是“选题候选、内部数学审查”：它独立重构公式和量词，给出工具引理级的修正，但不声称外部同行验证、新颖性或一篇可直接投稿的主定理。报告特别认为单纯把原共享控制变量 \(t\) 拆成严格递减的 \(t_i\) 并不能自动形成足够新颖的主课题，因为共享 \(t\) 本来就只增加常数 pathwidth。

## 局部势和完整梯度

报告采用 \(y_i=x'_i\)、\(p_i=x_{i-1}y_{i-1}\)、\(x_0=y_0=1/2\)，构造
\[
\Psi=\sum_{i=1}^n[(t_i-c_i)(x_i-p_i)+(d_i-\tfrac12)(x_i-y_i)-2t_i]-2x_n-2y_n.
\]
所有坐标在 \([0,1]\)。关键偏导为
\[
\begin{aligned}
\Psi_{t_i}&=x_i-p_i-2\in[-3,-1],&
\Psi_{c_i}&=p_i-x_i,\\
\Psi_{d_i}&=x_i-y_i,&
\Psi_{x_i}&=t_i-c_i+d_i-\tfrac12
-\mathbf1_{i<n}(t_{i+1}-c_{i+1})y_i-2\mathbf1_{i=n},\\
\Psi_{y_i}&=-d_i+\tfrac12
-\mathbf1_{i<n}(t_{i+1}-c_{i+1})x_i-2\mathbf1_{i=n}.
\end{aligned}
\]
势沿每位玩家坐标为仿射函数，因此边界符号与内部无差异条件给出完整最佳回应，而不是只给一般非凸问题的 KKT 必要条件。报告明确区分局部收益 \(u_v(a)=a_v\partial_v\Psi(a_{-v})\) 与全局势；不能把每个玩家的完整收益都写成 \(\Psi\) 后仍称稀疏。

## 任意 n 和整个扰动区间的候选 profile

令
\[
a_i=2^{-2^i},\qquad q_i=\max\{\epsilon,a_i\}.
\]
对任意 \(n\ge1\) 和 \(\epsilon\in[a_n,1/2]\)，候选 profile 为
\[
t_i=c_i=\epsilon,\qquad d_i=\tfrac12,\qquad x_i=y_i=q_i.
\]
可行性来自 \(q_i\le\max\{\epsilon,1/4\}\le1-\epsilon\)，以及 \(q_i\ge q_{i-1}^2\)。于是 \(t_i\) 在下界且偏导严格负，\(c_i\) 在下界且偏导非正，\(d_i\) 无差异，非末端 \(x_i,y_i\) 偏导为零，末端偏导为负；\(\epsilon=1/2\) 的坐标域退化为单点，最佳回应自动成立。这个结论是全区间代数推导，不是对有限样本 profile 的猜测。

## 到全部原 NE 的分离与半球修正

任取原游戏 NE。因为所有 \(\Psi_{t_i}<0\)，必有 \(t_i=0\)；末端偏导又迫使 \(x_n=y_n=0\)。若所有 \(d_i\in(0,1)\) 且所有 \(c_i<1\)，则 \(d_i\) 无差异给 \(x_i=y_i\)，而 \(c_i\) 的最佳回应给 \(x_i\ge x_{i-1}^2\)，归纳得到 \(x_n\ge2^{-2^n}>0\)，矛盾。因此每个原 NE 至少有一个 \(d_i\in\{0,1\}\) 或 \(c_i=1\)。

候选 profile 的 \(d_i=1/2\)、\(c_i=\epsilon\le1/2\)，所以到任意原 NE 的 \(\ell_\infty\) 距离至少 \(1/2\)。报告纠正了一个容易被夸大的措辞：距离 \(\ge1/2\) 不能排除闭半径 \(1/2\) 球。对 \(n=2\)，它给出一个原 NE 与候选 profile 的距离**恰为** \(1/2\)。安全陈述应固定任意 \(\delta<1/2\)，例如 \(\delta=1/4\)；若要求所有扰动 NE 落入原 NE 的闭 \(\delta\) 球，则必须有 \(\epsilon<a_n\)，从而精度位数满足
\[
\log_2(1/\epsilon)>2^n.
\]
这是必要的几何精度条件，不是充分阈值，也不是任意 NE 求解时间下界。

## interaction graph 的最大度和 pathwidth

报告按“两个玩家坐标共同出现在非零势单项式中”定义 interaction graph，并列出邻居：

- \(t_i,c_i\) 只接触 \(x_i,x_{i-1},y_{i-1}\)；
- \(d_i\) 接触 \(x_i,y_i\)；
- 非末端 \(x_i\) 接触 \(t_i,c_i,d_i,t_{i+1},c_{i+1},y_i\)，度为 6；
- 非末端 \(y_i\) 度为 4；
- 末端 \(x_n,y_n\) 度分别为 3、1。

因此 \(n\ge2\) 时最大度恰为 6，\(n=1\) 时最大度为 3。路径袋为
\[
A_i=\{x_{i-1},y_{i-1},t_i,x_i\},\quad
C_i=\{x_{i-1},y_{i-1},c_i,x_i\},\quad
D_i=\{x_i,d_i,y_i\},
\]
按 \(A_1,C_1,D_1,\ldots,A_n,C_n,D_n\) 排列，首层删去常量 \(x_0,y_0\)。每个单项式支持落入某袋，变量出现连续，故 pathwidth \(\le3\)。

对 \(n\ge2\)，四个连通 branch sets
\[
\{x_1\},\quad\{y_1\},\quad\{c_2\},\quad\{t_2,x_2\}
\]
构成 \(K_4\) minor，给出 treewidth \(\ge3\)。结合袋分解，得到该 interaction graph 的 treewidth/pathwidth 恰为 3。这个“恰为 3”只适用于报告明确定义的战略 interaction graph；若把每位玩家的完整 payoff table scope 变成 clique，得到的是另一张更大的图，不能混用。势因子超图仍有 rank \(\le3\)，且共享两个变量，不能写成 Berge-acyclic。

## 收益归一化和编码边界

全立方体偏导绝对值不超过 \(7/2\)。原报告指出除以 4 只能给 \(|u_v|\le7/8\)，不能保证所有跨 profile 收益落在 \([0,1]\)。若模型必须使用该范围，可用
\[
\widetilde u_v=(u_v+\tfrac72)/7\in[0,1],
\]
并把势除以 7；正仿射变换不改变原游戏或扰动游戏的 NE。

若用绝对顶点编号，结构编码长度为 \(L=O(n\log n)\)，所以不能未经说明地把 \(2^n\) 写成 \(2^{\Omega(L)}\)。用玩家数 \(N=5n\) 表述最稳妥：必要精度位数至少 \(2^{N/5}\)。固定链式 offset 编码可把结构描述压到 \(O(n)\) 位，但正式命题必须说明编码方案。

## 与 v1/v2 证据和现行对象的关系

v2 JSON 的 275/3750 个一步恒等式、两条噪声分支、25 个 Minty anchor、n=1..12 的有限扰动记录、梯度范围、path-bag 和 \(K_4\) 字段，与报告的有限核验部分一致；v2 是有限证据，不替代报告给出的全区间/全原 NE 代数论证。v1 只有粗 pathwidth 上界 6，不能覆盖 v2 的恰 3 证书。

现行资料对象已经保留相同的候选 profile、\(\delta=1/4\) 半球修正、最大度 6/pathwidth 3、收益规范化和编码边界；本报告提供其独立审查来源、完整梯度推导、n=2 闭半径 \(1/2\) 边界例和论文价值评估。没有发现另一个不同数学模型，故不建立重复定理对象。

## 论文状态和后续边界

报告核对作者当前 PDF、arXiv 条目、EC2026 program 和作者主页，记录其论文接收/版本信息，但没有由此认证最终出版全文或新颖性。最新可取作者稿仍显式使用共享 \(t\)，未显式包含 \(t_i\) 局部化或 bounded-degree 结论；“未检索到”不等于最终出版版本绝无该结果。

报告建议把本构造保留为通过内部数学攻击的工具引理，而非单独主课题。真正有区分度的后续问题是 treewidth \(\le2\) 或 Berge-acyclic 三元势是否存在正向多项式精度界；本构造不属于这些类，也不证明它们的正定理。有限代码核验、作者稿件状态和内部审查均不能升级为一般收敛定理、NE 计算复杂度定理或外部新颖性认证。
