# 逐行动阈值停止：合法自由度与仍未支付的全局量

2026-10-23，general_direct。此稿是给tree_credit首次满行停止构造的一个一般可用局部自由度，不是half证明，也不声称局部背包优化自动改善最终全树费用。所有查询仍是原实际前缀下原完整策略的真实完成叶。

## 1. 一个role内可以逐行动选择接纳率

沿用`../tree_credit/first_saturation_frontier.md`的同一owner、取消库存γ、残源ρ、钱包η及已付初始source费用。固定处理到某role i时的captured incoming `q_a(x)`。记

\[
M_a=\sum_xq_a(x),\quad A_a=\sum_x\frac{q_a(x)}{c_{i,a}(x)},\quad
D_a=D_i(a),\quad f_a=u_i A_a/D_a.
\]

零量项按原稿约定取零；有正incoming时`A_a,D_a,u_i>0`。`f_a`是接受该行动所有incoming时的完整原IC费用，不是对客户单独加权的IC。

可任选`θ_a∈[0,1]`满足

\[
\sum_a\theta_af_a\le e_i:=\eta_i-K_i^{src},\tag{FEE}
\]

将该query所有incoming客户共同乘`θ_a`接纳，其余首次停止。最后该行动的唯一whole-IC系数仍为

\[
w_{i,a}=\frac{A_{i,a}^{src}+\theta_aA_a}{D_a}.
\]

因此source钱包、费用≤η、客户守恒和HIT耦合都保留。不同action使用不同接纳率不会变成客户级IC重加权：每条真实IC依然只乘一个非负常数。

若`sum_a f_a≤e_i`全收；否则可令费用恰用尽，构造仍按role顺序无循环。原统一`θ_i`只是这个可行集合中的一个选择。

## 2. 给定当前incoming时，局部停止总质量是连续背包

当前role立即停止的总质量为

\[
B_i=\sum_a(1-\theta_a)M_a.
\]

在固定(FEE)预算下，最小化这个**当行**的`B_i`等价最大化`sum θ_aM_a`。以

\[
v_a=\frac{M_aD_a}{A_a},\qquad \frac{M_a}{f_a}=\frac{v_a}{u_i}
\]

排序，优先接纳`v_a`大的action即可；至多一个不同阈值层被部分接纳，同阈值action可任意分配。有限目录保证最大元存在。

一个交换证明：若`v_a>v_b`而`θ_a<1, θ_b>0`，将费用ε从b移给a，接纳质量增加`ε(v_a−v_b)/u_i>0`。故最优解不允许此逆序。

于是存在阈值τ_i，使所有仍被拒绝的action满足`v_a≤τ_i`，所有被正量接纳的action满足`v_a≥τ_i`（等值层可同时接纳/拒绝）。这在质量law与费用law之间给出有限范围：若`λ_a^{stop}=(1−θ_a)A_a/D_a`，则

\[
B_i=\sum_a\lambda_a^{stop}v_a\le\tau_i\sum_a\lambda_a^{stop}.\tag{THRESHOLD}
\]

它并未将`B_i`免费换成费用总和；τ_i尚未被1或实际利润控制。

## 3. 不可省略的限制

局部最优只最小化**此role马上停止的质量**。被接纳质量随后可在更晚role吸收或停止，所以不同接纳action还会改变未来incoming、未来满行集合和钱包使用；本稿没有证明贪心阈值最小化全局B。若要以一个最终全局固定frontier为目标，需要给未来存活/吸收再计价值，不能先假定该价值相同。

同样，THRESHOLD没有支付`B≤E+U`，没有证明每owner的停止whole-IC系数总和≤1，也没有允许改变owner后沿用旧γ/η。它只提供一个合法的逐action接纳自由度及可审查的精确局部最优性。

下一实质义务仍是把阈值、实际I份额运输、SPE slack或可合法的交替槽操作接成共同付款。没有该关系时，阈值化只是更宽的构造空间，不是一般福利新下界。
