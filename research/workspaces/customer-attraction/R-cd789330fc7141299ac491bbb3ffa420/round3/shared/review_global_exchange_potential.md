# 全局最优交换势：独立重构与同叶信用范围

2026-10-23，shared。本文记录 shared 与 relay 独立得到同一全局势后的互核。原始 Bernoulli/HARM 在[交换正文](optimal_exchange_harmonic_budget.md)；relay 主写全局势与真实最优前缀折扣的合稿。下面是完整解析重构，不依赖有限样本。动态跨 rollout 结论未闭，Q-CAG-HALF 仍 OPEN。

## 1. 同一个固定 OPT 配对、同一个全局基线

固定一个最优 m 槽元组 T，其并集 O、覆盖次数 a_x。对任意 m 槽元组 B 写 c_x，并令 J(T,B) 为无同槽双覆盖的 O 客户。允许分析中的部分槽为虚拟空；所有随机替槽实现至多有 m 个合法非空动作，可补齐，所以最优覆盖上界仍成立。

定义

\[
\Phi_T(B)=\sum_{x\notin O}H_{c_x}
-\sum_{x\in J(T,B)}\operatorname{Beta}(a_x,c_x+1),
\]

\[
F_T(B)=\Phi_T(B)+K_T,\qquad K_T=\sum_{x\in O}\frac1{a_x}.
\]

由 HARM，\(\Phi_T(B)\le0\)。若 B 全空，则 \(\Phi_T(B)=-K_T\)。更直接地，令 Z_p(T,B) 为独立 Bernoulli 替槽元组，则

\[
F_T(B)=\int_0^1\frac{
\mathbb E\,\operatorname{Cov}(Z_p(T,B))
-\mathbb E\,\operatorname{Cov}(Z_p(T,\varnothing))}{p}\,dp.
\]

因此 \(0\le F_T(B)\le K_T\)。该势在所有叶使用同一个最优配对及有限基线，无需对数支撑屏障，也没有随真实叶重置基线。

它有单调次模的槽动作扩展：固定替槽硬币后，所选的带槽动作只增加一个覆盖集合，基线为未替换的 T 槽；积分保持单调次模性。这不声称任何辅助替槽策略为 SPE。

## 2. 单位收益的精确分解

将 B 的第 i 槽置空得 B^{−i}，定义

\[
\ell_i(B)=F_T(B)-F_T(B^{-i})
=\Phi_T(B)-\Phi_T(B^{-i}).
\]

若 x 不在 B_i，则该客户边际为零。若 x 在 B_i，且其它槽中存在同槽 T_h、B_h 双覆盖 x，则边际也为零。其余情况，其它 T 槽和 B 槽的覆盖位置不交；替入 B_i 新覆盖 x 的概率除以 p 为

\[
p^{a_x-1_{x\in T_i}}(1-p)^{c_x-1}.
\]

积分给

\[
\ell_i(B;x)=\operatorname{Beta}
\bigl(a_x+1_{x\notin T_i},c_x\bigr).
\]

在上述零情形以外才使用该公式；Beta 的两个参数均为正整数。对 x∉O，a_x=0 且 x∉T_i，所以边际**恰为** 1/c_x。对 x∈O，被积式不超过 (1−p)^{c_x−1}，故

\[
0\le\ell_i(B;x)\le\frac{1_{x\in B_i}}{c_x}.
\]

定义 \(e_i(B)=u_i(B)-\ell_i(B)\)。于是 e_i≥0，且误差只由 O 内客户贡献。同一个固定叶中，逐客户

\[
\sum_i e_i(B;x)\le
\sum_{i:x\in B_i}\frac1{c_x}=1
\quad(x\in O\cap\operatorname{Cov}(B)).
\]

所以

\[
\boxed{\sum_i e_i(B)\le|O\cap\operatorname{Cov}(B)|.}
\]

若 B 为实际 SPE 终局、C 为实际覆盖，则同叶误差总预算不超过 |I|，其中 I=C∩O；O 外边际总利润精确为 |G|，其中 G=C\\O。这是一次同叶预算，不是给每个真实分支一份 I 或 G。

## 3. relay 前缀查询信用的盲重构

固定 T 的顺序。Y_i 为逐步强制前 i 槽 T_1,…,T_i 后沿原完整策略的真实 rollout。当前查询恰为 T_i，定义

\[
r_i(x)=\frac{1_{x\in T_i}}{c_x(Y_i)}-\ell_i(Y_i;x).
\]

对一个最优覆盖次数 a≥1 的客户 x，按出现于最优主题的先后给这些查询标号 k=1,…,a。

当 k≥2，某个较早槽已经 T_h=B_h 且覆盖 x；它使当前势边际为零。已有 k 个前缀覆盖者，所以 r_i(x)=1/c≤1/k。

第一次出现时，若未来已有同槽双覆盖，则 c≥2，r_i≤1/2≤1−1/a（此情形需 a≥2）。否则

\[
r_i(x)=\frac1c-\operatorname{Beta}(a,c)
=\int_0^1z^{c-1}[1-(1-z)^{a-1}]\,dz
\le1-\frac1a.
\]

最后一步因被积式随整数 c≥1 非增，最大值在 c=1。a=1 时第一次信用精确为零。相加得到

\[
\boxed{\sum_i r_i(x)\le
1-\frac1a+\sum_{k=2}^a\frac1k=H_{a-1}\le a-1.}
\]

因此该查询信用由比较主题的重复覆盖预算支付；没有隐藏客户度数条件。证明只要求已强制的 OPT 前缀；后续动作保持原全部客户 incidence，可以任意改变。shared 独立重构通过，原始发现及主稿归 relay。

## 4. 原 IC 可合法接入什么，仍缺什么

对任意固定配对 T、任意真实比较叶 Z、Y，原 IC 可原样写成

\[
\ell_i(Z)+e_i(Z)\ge\ell_i(Y)+e_i(Y).
\]

这是整条原单位收益比较的精确分解，不给被积式重新加权。在真实 OPT 前缀链上，左边规定 rollout 与右边强制 rollout 的 Φ 差仍包含各自删去当前槽后的真实后继差；没有证明它们由实际叶的 I、G 共同支付。

还须固定一次全局 OPT 槽配对或一次共同分布。即使 K_T 不变，逐条边重选配对会改变 J 及 Φ 本身；不能让每个查询另换配对再沿不同势望远镜。同叶 Σe≤I 与跨前缀 Σr≤ΣH_{a−1} 是不同而精确的对象，前者不自动控制所有规定 rollout 的 e。
