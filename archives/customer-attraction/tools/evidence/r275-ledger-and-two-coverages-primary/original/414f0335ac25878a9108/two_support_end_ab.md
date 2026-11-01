# 两覆盖终局以不同主题收尾时的任意人数半覆盖

## 精确身份与状态

**B10-TWO-SUPPORT-END-AB-v1。** 采用 CAG-MODEL。对每个有限单位客户集、每个有限非空共同目录、每个整数 m≥2，以及每个完整有序历史依赖纯 SPE，假定实际终局仅使用两个不同的客户覆盖集合 A、B，且最后两位依次选择 A、B。设 A、B 的实际频次为 k,l≥1，m=k+l。此前的顺序任意，目录中其他主题的数量、包含关系和交叠均不受限制。则存在下文显式的 β_(k,l)<2，使

\[
\operatorname{OPT}_m\le \beta_{k,l}W.
\]

空主题、重复选择、零客户和全部离轨历史依赖平局均保留。若 W=0，结论直接是 OPT=0。不同标签覆盖相同客户时，假设仅涉及覆盖集合，**不要求策略按计数或覆盖匿名化**。一个覆盖集合的情况沿既有结果处理，本命题不需要把它重命名为两个不同集合。

状态：root 自足推导；background_exchange 研究员从末两人原始比较独立重建全部系数与正性条件，未发现致命异议；独立逐客户 Fraction 审计见同目录 `audit.py`、`audit.json`。没有外审或新颖性认证。一般 Q-CAG-HALF 仍 OPEN。该命题没有解决以 BB 收尾的所有两覆盖终局，更没有处理无界实际支持数。

## 真实末两人闭包

记

\[
a=|A\setminus B|,\quad b=|B\setminus A|,\quad c=|A\cap B|,
\qquad W=a+b+c.
\]

在实际末两人之前固定原有序前缀 h，其客户负载为

\[
p_x=(k-1)\mathbf1_A(x)+(l-1)\mathbf1_B(x).
\]

对任意目录主题 X,Y 定义

\[
f(X)=\sum_{x\in X}\frac1{p_x+1},\qquad
g(X,Y)=\sum_{x\in X\cap Y}\frac1{(p_x+1)(p_x+2)},
\quad U(X,Y)=f(X)-g(X,Y).
\]

实际末两人收益是 u=U(A,B)=a/k+c/m，v=U(B,A)=b/l+c/m。固定任意合法主题 T，令 R 为**给定完整 SPE**在历史 (h,T) 的真实末位回复。三个比较

\[
s_1=u-U(T,R)\ge0,\quad
s_2=U(R,T)-U(B,T)\ge0,\quad
s_3=v-U(R,A)\ge0
\]

分别来自实际倒数第二位、离轨末位、实际末位。共同目录保证 R 可作为实际末位的偏离。直接展开得

\[
u+v+g(A,A)-f(B)-U(T,B)
=s_1+s_2+s_3+g(A,A)-g(A,R)\ge0.\tag{1}
\]

这就是既有末两人税恒等式在第二比较主题取 B 时保留重叠项的形式；没有冻结真实回复。

令 t_o,t_A,t_B,t_C 分别为 T 在 N\(A∪B)、A\B、B\A、A∩B 四块中的客户量。(1) 精确给出

\[
\boxed{
t_o+\frac{t_A}{k}+\frac{t_B}{l+1}+\frac{t_C}{m}
\le\frac{k+2}{k(k+1)}a+\frac cm.}\tag{2}
\]

该式对每个目录主题成立，包括离轨回复本身；前缀内 A、B 的具体有序排列不进入逐客户分母。

## 支付最优并集的两条不同预算

取恰 m 个最优主题，允许重复。对 (2) 求和，将每个最优并集客户至少出现一次，并以实际各块大小支付剩余权重，得到

\[
\operatorname{OPT}_m\le
P=\left(2+\frac{l(k+2)-1}{k(k+1)}\right)a
+\frac l{l+1}b+\left(2-\frac1m\right)c.\tag{3}
\]

另一方面，实际末位 B 的最优性给任意 T：

\[
\frac{t_A}{k+1}+\frac{t_B}{l}+\frac{t_C}{m}+t_o
\le \frac bl+\frac cm.
\]

同样求和、支付并集余量，得到

\[
\operatorname{OPT}_m\le
L=\frac k{k+1}a+
\left(2+\frac{k-1}{l}\right)b+
\left(2-\frac1m\right)c.\tag{4}
\]

所有丢弃的项均逐客户非负，不把最优主题的重复覆盖当成新增福利。

## 显式凸合及全部整数参数的正性

设

\[
X=\frac{l(k+2)-1}{k(k+1)}>0,\quad
Y=\frac{k-1}{l}\ge0,\quad
Z=\frac{k+2}{k+1}>0,\quad
V=\frac{l+2}{l+1}>0.
\]

取 λ=(Y+Z)/(X+Y+Z+V)，故 0<λ<1。两块 a、b 在 λP+(1−λ)L 中的系数相等，均为

\[
\gamma=2-\delta,\qquad
\delta=\frac{ZV-XY}{X+Y+Z+V}.
\]

关键正性是恒等式

\[
ZV-XY=
\frac{l(k+2)(k+l+1)+(k-1)(l+1)}
{kl(k+1)(l+1)}>0.\tag{5}
\]

分子首项严格正，第二项非负，覆盖 k=1 或 l=1 的边界。因此

\[
\boxed{
\operatorname{OPT}_m\le
\min(P,L)\le
(2-\delta)(a+b)+\left(2-\frac1m\right)c
\le \left[2-\min\left(\delta,\frac1m\right)\right]W.}\tag{6}
\]

取 β_(k,l)=2−min(δ,1/m)<2 即得命题。没有借有限参数检验外推 (5) 的正性。

当 l=1 时，因最后两位为 A,B，实际路径必是 A^(m−1)B；(3)、(4) 恰退回旧 R-31 工作区的两条预算。本稿的新增范围是任意 k,l 和此前任意排列，只要求实际末两位不同。它不宣称旧结果或末两人税恒等式是本轮首次发现。

## 依赖、反对意见和剩余义务

依赖：CAG-MODEL 的完整 SPE 节点最优性，以及 `research/current/customer_attraction/two_remaining_tax.md` §2 的同一三比较恒等式。旧资产 `research/workspaces/customer-attraction/R-31bbb6cfd6594bc8bb076db7b2950993/credible_search/two_theme_terminal.md` 的 l=1 情形包含在本稿中。

独立攻击检查了：背景确是 k−1、l−1；真实回复 R 可以回到实际末位比较；比较主题和回复可重复；k=1 的 Y=0 不使凸合退化；最优组合可能覆盖不到实际某块；W=0 时不能写效率比。未发现仍成立的致命异议。

仍缺：一般两覆盖终局可能以 BB 收尾，且 B 频次不足以使用旧频次筛选。不能无证明地把另一个 A 移到倒数第二位；完整 SPE 的可实现顺序会受影响。更一般的无界实际支持数仍需新的跨分支预算。该结构结果只是可接续资产，不能作为停止一般研究的理由。
