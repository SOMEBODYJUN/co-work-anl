# 坐标剩余的客户支持：合法保留核与尚未支付的共同费用

2026-10-24，credible。对象始终为任意有限共同目录、任意人数及每份完整历史依赖纯 SPE。**Q-CAG-HALF 与 RESIDUAL-CAP 均未解决。** 本稿独立读取 [坐标初始化](../../../R-cd789330fc7141299ac491bbb3ffa420/round7/parent/optimal_coordinate_initialization.md)、round5 全客户核及 round6 SAFE/CLIP 后推导；没有做小人数扫描或重数锥扫描。

**主要审查结论：I-future 的互补实际客户券付款，与从头重算的旧 fresh-profit ν 核，可以合法合成。** 下面 §0 给出资金、初始支配及零分母域的独立重构。它仍只给非负表示，未证明净券共同 cap。

§2 另保留一种客户不重采的合法替代表示，供准确恢复本轮推导。它没有更好的全局预算，**不作为一般 half 的新增推进**；不能把另一种表示当作已支付的剩余容量。

## 0. I 互补付款 + 从头重算 ν 流：独立核对通过

本节只根据 `global_credit` 发来的合成陈述重构，之后读取旧 [fresh-profit 正文](../../../R-cd789330fc7141299ac491bbb3ffa420/round6/relay/fresh_profit_normalization.md)逐式对稿。来源归 global_credit；本分支仅独立核查。固定同一原实例、同一完整 σ、同一 actual B、同一比较 T、同一合法坐标剪枝。令 C=∪B_i，I=O∩C，R=O\C。

### 0.1 同一 H 之后的实际 I 份额够付全部 I-future

令 H_lx 为初始 P^B 最终送到 actual l 的 x 金额。固定客户 x、a=c_T(x)>0、b=c_B(x)>0、q=|{i:x∈T_i∩B_i}|。若 x∈B_l\T_l，则直接求和得到

\[
H_{lx}=\frac1a\left[\frac q b+\frac{a-q}{b+1}\right]\le\frac1b;
\]

其余 l 的 H_lx=0。这是同一张 H 的逐客户列界，不是另外选择一张运输矩阵。令 H_x=Σ_lH_lx，c_x=Σ_i c_ix，a_x=Σ_i a_ix。初始化精确守恒给

\[
H_x+c_x+a_x=1\quad(x\in O).
\]

对 x∈I 置 w_lx=1_(x∈B_l)/b−H_lx≥0，Σ_lw_lx=1−H_x。若 1−H_x>0，取

\[
J_{lx}=\frac{a_x}{1-H_x}\,w_{lx};
\]

否则因 a_x≤1−H_x=0 取 J_lx=0。于是 Σ_lJ_lx=a_x，且 H_lx+J_lx≤1_(x∈B_l)/b。这个付款只占**同一份第二实际 I 客户钱包的剩额**，不调用任何历史 IC。付款角色早于源 owner 也不影响合法性。

原 d_l=Σ_xc_lx 保持不变，仍只占第一份完整 u_l 钱包。没有既用 H 的旧钱包、又重新分配完整 I 一单位的重复领取。

### 0.2 剩余初始 a_R 真的是后继 fresh 利润子量

删除全部 x∈I 的 future injections，只保留原子边 a_ijx、x∈R。其目标仍为 W_i 的真实 prescribed context t=(W_i,<j,j)，且当前动作覆盖 x。原子边界给

\[
0\le a_{ijx}\le q^W_{ij}(x)
=\frac1{d_{ix}c_{W_i}(x)}\le\frac1{c_{W_i}(x)}.
\tag{INIT-F}
\]

因为 x∈R，它不被任何 actual 主题覆盖。故该项确在接收者的 fresh 利润里，不是实际 I 来源误入 fresh 图。

同一个**非零初始 context** 不会由两个不同 owner 直接生成：正源要求 T_i≠B_i（否则 W_i=B，q^W 全为零），且 W_i 在 i 前等于 actual，在 i 处首次不同。若 i<k，则 k-owner 的初始历史在位置 i 仍等于 actual，与 i-owner 的首次不同矛盾。因而每个初始 context 只有一个 owner；将该 owner 的全部 R 客户相加，由 INIT-F 得

\[
0\le b_t^R\le\nu_t:=u_j(W_i;N\setminus C).
\tag{INIT-NU}
\]

这是**初始输入**支配，不声称后续合流后的 h_t≤ν_t 或 β_t≤1。新的 reset 可能把多个 owner 的后续流合到同一 context，必须先合计再重算。

### 0.3 ν 核必须整体从头重算，且没有正 C 债

在每个 natural context t=(g,l)，令 V=finish(g)，A=finish(B_<l,σ_l(g))。只在当前动作的 fresh 客户 N\C 上计算原 q_tj、P_t、N_t、J_t^diag、L_t^common，分母取

\[
\nu_t=u_l(V;N\setminus C),\qquad
f_t=u_l(A;N\setminus C),\qquad
Y_t=u_l(A;C).
\]

完整 actual-prefix IC 的 e_t=u_l−u_l(A)≥0 给

\[
\nu_t-P_t=f_t-N_t
=u_l-Y_t-N_t-e_t
=J_t^{diag}+L_t^{common}>0\quad(\nu_t>0).
\tag{NU-SAFE}
\]

所以可从同 context 的 β_tu_l 第一整行费用安全退掉 β_t(Y_t+N_t+e_t)，净支付 β_t(ν_t−P_t)≥0。这里没有 round5 完整 v 核的正 X 迁移项；不能把两套分母或旧 β 混用。

从新的 b_t^R 开始，严格按角色重算

\[
h_t=b_t^R+\sum_{s\to t}\beta_sq_{st},\qquad
\beta_t=h_t/\nu_t.
\]

初始正输入由 INIT-F 蕴含 ν>0。每条正 future 边由一个 fresh 客户 x 见证，接收者真实 prescribed 动作覆盖 x，因此其 ν>0。ν=0 节点不会收到正质量；零节点全取零。fresh 客户没有 past actual coverer，故没有 past-C 出口。有限严格角色 DAG 给有限系数和质量守恒，无需另假设 β≤1。

ν 使用**全部** N\C 客户，不只 R；流中仍可能重采成 outside-O 的 fresh 客户。此合成只保留来源库存标签，不声称每个传播客户始终是原 R 的同一个客户。

### 0.4 财务合成与真正未付 cap

令

\[
K_l=\sum_{t:i(t)=l}\beta_t(\nu_t-P_t)\ge0.
\]

NU-SAFE 与 DAG 守恒给 Σ_lK_l=Σ_(i,x∈R)a_ix。与坐标初始化和 I 付款合并，恰为

\[
|O|=\sum_l(d_l+H_l+J_l+K_l).
\tag{COMPOSITE}
\]

已证明 d_l≤u_l，H_l+J_l≤u_l(B;I∩B_l)≤u_l。因此两份实际钱包留下的金额

\[
Q_l=2u_l-d_l-H_l-J_l\ge0
\]

是合法、同资金的余量。但 **K_l≤Q_l 尚未证明**，较弱的联合总资金不等式也未证明。把非负终端 K 写成 actual coupon，不等于已经证明这些 coupon 的共同系数 cap。

所有式子只读取同一 σ 的真实完成叶，未改 tie、未冻结后继。重复比较主题通过 c_T 保留；空主题/零源不产生正流；全零输入所有量为零。没有从一次固定输入通过推断一般 cap。

## 1. 先区分三种“保留支持”

1. **来源标签。** 对固定非负核，可以将合并流线性拆回 origin 标签。这不要求输出边客户等于 origin，原 full-customer SAFE 已能做到。
2. **传播客户身份。** 原客户 x 只走由同一 x 产生的 coverer 正边，不在下一 context 重采成另一个客户。本稿 §2 给一个合法替代核。
3. **实际同客户券。** origin x 最终只能占用 actual (j,x) 客户份额。这通常不可能：坐标初始化第一接收角色 j 的 actual B_j 不覆盖源 x，而任何原 SAFE/合法 CLIP 行都有严格正的 current 吸收。current 仍须由 j 的完整利润钱包支付，不能伪装成 actual (j,x) 券。

第一种不能推出第二种，第二种也不能推出第三种。下面保留第二种；current 终点仍是完整利润行。

## 2. 最大客户密度核：一次 whole-IC 足够

固定一个真实 natural context t=(g,i)。其规定动作 a=σ_i(g)，规定完成叶 V，actual-prefix 重置完成叶 A=finish(B_<i,a)。对 x∈a，记

\[
v_x=1/c_V(x),\qquad D_x=1/c_A(x).
\]

逐客户沿用原全客户正负原价 P_x,N_x（可先作同 context、同客户 NET-CANCEL）：

\[
v_x-D_x=P_x-N_x,\qquad
v_x-P_x=D_x-N_x>0.
\tag{1}
\]

原价支持与原文相同：future 正边是 A 的真实后继 prescribed context；past 正边只能到 actual (j,x) 券。使用 NET-CANCEL 时把 P,N 换成其合法删边后的 P',N'，式(1)仍成立。

现在让这个 context 的输入**已按原客户合并**为 h_x≥0，且 h_x>0 只允许 x∈a。置

\[
\beta_x=h_x/v_x,\qquad \beta_* =\max_x\beta_x.
\]

对每个客户 x，沿其原正边送出 \(\beta_xq^+_{tj}(x)\)，不重采客户；保留当前金额

\[
L_t=\sum_x\beta_x(v_x-P_x)
   =\sum_x\beta_x(D_x-N_x)\ge0.
\tag{2}
\]

质量严格守恒：

\[
\sum_xh_x=L_t+\sum_{x,j}\beta_xq^+_{tj}(x).
\tag{3}
\]

令 D=Σ_(x∈a)D_x，原 actual-prefix IC 为 D≤u_i，写 e=u_i−D≥0。因为 β_x≤β_*，

\[
L_t\le\sum_x\beta_xD_x\le\beta_*D\le\beta_*u_i.
\tag{4}
\]

**这不是逐客户重权 IC。** 只调用一次系数 β_* 的完整 IC，再从同一实际整行退还

\[
F_t=\beta_*u_i-L_t
=\beta_*e+\sum_x(\beta_*-\beta_x)D_x+\sum_x\beta_xN_x
\in[0,\beta_*u_i].
\tag{5}
\]

退款逐项非负，故可以按 actual i 的原利润份额统一退券；净 current 系数为 κ_t=L_t/u_i≤β_*。若输入为空，所有量取零；正输入蕴含该动作非空，原 actual-prefix IC 保证 u_i>0。未使用 off-history slack 的额外信用。

等价地，可以对层集 X_s={x:β_x≥s} 作 layer-cake：在每个层上使用同一完整 IC 的 ds 份，积分的总系数恰为 β_*，而不是 Σ_xβ_x。不能将各 singleton 核各自领一份 u_i 后相加。

### 全树合法性与准确限度

同 context、同客户的全部输入必须先合并，再计算 β_x、β_*。future 角色严格增加，past 边只终止，故有限 DAG 守恒；每条传播边保留同一 x。NET-CANCEL 后，正 future 边要求 c_A(x)>c_V(x)，故同客户沿非终端谱系的负载严格上升。

如果仅接 R=O\C 客户源，则这些客户在全部 actual 主题上均不存在，所有 past 正出口为零。此时所有传播始终保留 R 客户身份，current 金额仍由 actual 完整行支付。

**尚未支付的是**同一角色全部 context 的 \(\sum_t\kappa_tu_i\)，连同初始化 d、H 及其他已付款项的共同容量。逐节点 κ_t≤β_*，或每个来源单位库存守恒，都不推出同一角色的 β_* 累计≤1。没有证明剩余角色界，也没有证明费用比原 full-profit 核下降。

本节合同已由 `clock_cycle` 子分支从陈述独立重构，尤其独立给出式(5)的退款分解；见 [独立记录](clock_cycle/source_preserving_kernel_review.md)。这是内部数学核查，不是主目标或外部新颖性认证。

## 3. 为什么它不能偷偷当作原 RESIDUAL-CAP 的 CLIP 选择

原 full-profit 核用同一 β=h/v 乘所有客户正边。§2 则用各自 β_x；某条边可能比 βq^+ 更大，所以通常不是原核的合法删边。没有证明两种图的角色费用有单调关系。原 RESIDUAL-CAP 中“存在最优 T、坐标剪枝和 full SAFE/CLIP 选择”的量词没有被本节替代或反驳。

原核在一个 context 保留固定客户集合 X 的正传播支持，有一个精确局部条件。设

\[
P_X=\sum_{x\in X,j}q^+_{tj}(x),\quad
P=\sum_{x,j}q^+_{tj}(x),\quad
F=u_i-(v-P)=N+e.
\]

合法 SAFE/CLIP 至多删去 min(P,F) 的正原价，且必须至少保留 (v−u_i)_+。因此

\[
\boxed{\text{可仅保留 X 客户正边}
\iff (v-u_i)_+\le P_X.}
\tag{6}
\]

若不成立，至少 \(((v-u_i)_+-P_X)_+\) 的原价必须走 X 外客户。这只判断同一个 context 的支持剪枝，不是共同钱包界。

### 一个既有完整 SPE 上的精确代入

只重放原 348 单位客户证书与不变全历史策略，没有搜索新输入。重新以 Fraction 检查全部 43 历史、258 项含自身行动比较；这次回放重用源坐标审计的读取、完成叶及收益函数，再另算本节局部支持量，**不是第二套互不导入的 SPE 审计实现**。actual B=(0,3,4)，最优 T=(5,2,4)，OPT=270；使用原坐标文中明确给出的比例剪枝。

在初始 context g=(5,0)、当前角色为第三人时，

\[
h=35/9,\quad v=163/2,\quad u_3=71,\quad
P=63/4,\quad P_O=39/4,\quad F=21/4.
\]

故 (v−u_3)_+=21/2>39/4=P_O。任意该行合法 CLIP 至少保留 3/4 的 O 外客户正原价；仅以其固定初始输入归一化，流量下界为

\[
\frac{h}{v}\frac34=\frac{35}{978}>0.
\]

这精确排除“原 full-profit 图总能免费保留 O 传播支持”的局部步骤。**不是 RESIDUAL-CAP 反例：**没有排除更换最优 T、改变坐标分配；原文件已经记录该固定例的角色剩余容量通过。也没有将固定路由失败换成存在性失败。

## 4. 与本轮 I-future 直接付款的接合

`global_credit` 另提出实际已覆盖 I=O∩C 的 future 库存直接付款。本分支从陈述独立核对：令 H_lx 为已付第一类正价，

\[
w_{lx}=\mathbf1_{x\in B_l}/c_B(x)-H_{lx}\ge0,
\quad a_x=\sum_i a_{ix}\le1-\sum_lH_{lx}.
\]

按 \(w_{lx}\) 的剩余比例分配 J_lx，就有 Σ_lJ_lx=a_x 且 H_lx+J_lx≤actual(l,x) 份额；零端点取零。它不调用过去或未来 IC。d 仍占第一份完整钱包，H+J 共同占第二份实际 I 客户钱包。来源与正式正文归 `global_credit`；本分支仅作独立资金核查，不认领新颖性。

此直接付款可以先清掉 I future，剩下 R 源再考虑 §2 的客户保留核，或使用原 full-customer SAFE。若改成只保留 fresh 正边、却仍用完整利润 v 作分母，round5 的 current 吸收含 X+J+L，**不能**直接说已被 u_i 支配；必须保留原 C 迁移账，或使用已另证的 fresh-profit/§2 最大密度合法退款。

无论采用哪种图，真正还缺的是同一批 R 来源在同一份实际剩余钱包中的联合付款；没有从库存、支持或有限 DAG 守恒自动推出这一点。
