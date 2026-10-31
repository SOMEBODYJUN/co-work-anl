---
id: customer-attraction/fixed-comparison-linear-joint-payment-certificate
kind: candidate
type_tag: 候选
title: 固定比较元组的线性共同付款证书
status: finite-primal-and-price-equivalence-proved-universal-feasibility-open
summary: 固定原完整策略和比较元组的INIT/I-PAY/R-FLOW/ROLE是有限有理线性充分证书；去ROLE后非空紧，任意common路由自动满足节点密度，价格DP可消元，但普遍共同容量未证。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round8/residual/linear_joint_payment_certificate.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round8/residual/linear_joint_payment_certificate.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round8/inventory/source_preserving_density_envelope.md
---

# 固定比较元组的线性共同付款证书

## 固定策略、数据与尚未证明的存在性

采用[单位客户共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)，任意$m\ge1$，固定全部有序历史上的纯SPE $\sigma$。实际叶$B$、覆盖$C$、利润$u_i$、福利$W=\sum_i u_i$；固定合法比较元组$T$，$O=\bigcup_iT_i$、$I=O\cap C$、$R=O\setminus C$。空主题、重复动作、零客户、同计数历史不同续局及任意离轨平局全部保留。只有$T$最优时$|O|=\mathrm{OPT}_m$。

本文给出有限线性充分证书：其可行点一定支付$|O|\le2W$。**没有证明**每份原SPE都存在某个最优$T$使该系统可行，也不声称这一更强证书与half等价。当前恰六人目标仍开放；五人half已有独立[定理](../定理/五人半覆盖--定理.md)。

所有完成叶、分母和边集先由同一$\sigma,B,T$固定，之后变量只分配金额。重选$T$或移动比较主题到另一个角色，必须按新实际有序前缀重算，不能把旧future叶重命名搬过去。

## 初始坐标及实际正付款

对$x\in T_i$设

\[
p_{ix}=1/c_T(x),\quad\delta_{ix}=c_B(x)+1-\mathbf1_{x\in B_i},\quad
W_i=\operatorname{finish}_\sigma(B_{<i},T_i),
\]

\[
P^B_{ix}=\sum_{\ell\ne i:\ x\in B_\ell\setminus T_\ell}p_{ix}/\delta_{ix},
\quad r_{ix}=p_{ix}-P^B_{ix}\ge0,
\]

\[
H_{\ell x}=\sum_{i:\ x\in T_i,\ \ell\ne i,\ x\in B_\ell\setminus T_\ell}p_{ix}/\delta_{ix},
\quad H_\ell=\sum_xH_{\ell x}.
\]

$H$只支持$I$且$0\le H_{\ell x}\le w_{\ell x}:=\mathbf1_{x\in B_\ell}/c_B(x)$。初始future边仅为

\[
E_0(i,x)=\{j>i:x\in(W_i)_j\setminus B_j\},\qquad
\widehat q_{ijx}=\min(p_{ix},1/\delta_{ix})/c_{W_i}(x).
\]

$\delta$及$c_{W_i}$只在相应覆盖客户上取倒数。$H$与$p,r,\widehat q$均为数据，不随变量变化。

## 全部线性约束

**INIT。** 每个初始边有$a_{ijx}$，每初始坐标有$c_{ix}$，所有变量非负，要求

\[
a_{ijx}\le\widehat q_{ijx},\qquad
c_{ix}+\sum_{j\in E_0(i,x)}a_{ijx}=r_{ix},\qquad
d_i=\sum_xc_{ix}\le u_i.
\tag{INIT}
\]

记$a_{ix}=\sum_ja_{ijx}$。不固定极大current $d_i=\min(\sum r_{ix},u_i)$；可以在原加强边容量内多送future、少占current。库存逐坐标恰为$p=P^B+c+a$。$c_{ix}$是来源客户标签，不要求$x\in B_i$；$d_i$支付于actual $i$的整行钱包，不是同客户实际券。

**I-PAY。** 对$x\in I$与实际角色$\ell$引入

\[
0\le J_{\ell x}\le w_{\ell x}-H_{\ell x},\qquad
\sum_\ell J_{\ell x}=\sum_i a_{ix},\qquad J_\ell=\sum_{x\in I}J_{\ell x}.
\tag{I-PAY}
\]

它一次付清全部$I$ future来源，之后不再进入$R$图。因为同一客户库存给$1=\sum_\ell H_{\ell x}+\sum_i c_{ix}+\sum_i a_{ix}$，未花actual份额总额为$1-\sum H$，足以付$\sum a$。正总余量时按$w-H$比例分配即可；余量0时源量亦0。故每个INIT点都能求这份$J$，但必须按**这个点**重算，不继承另一剪枝的数值。$J$可落在较早实际角色，因为没有调用过去IC；$H_\ell+J_\ell\le u_\ell(B;I)\le u_\ell$。

**固定有序$R$图。** 从全部可能初始$R$边目标$(W_{i,<j},j)$出发，对真实reset未来边取闭包。context $t=(g,k)$有

\[
a_t=\sigma_k(g),\quad V_t=\operatorname{finish}_\sigma(g),\quad
A_t=\operatorname{finish}_\sigma(B_{<k},a_t).
\]

对$x\in R\cap a_t$令

\[
Q_t(x)=\{j>k:x\in(A_t)_j\},\quad
N_t(x)=\{j\in Q_t:x\notin(V_t)_j\},\quad M_t=Q_t\setminus N_t,
\]

目标$\tau(t,j)=(A_{t,<j},j)$。$R$不被actual主题覆盖，所以没有past actual出口、没有正actual-prefix $R$终点，且$c_{A_t}(x)=1+|N_t|+|M_t|$。所有边严格增加角色，有限原树保证闭包有限；不按主题计数合并历史。

**R-FLOW。** 对每个$(t,x)$有$h_{tx},L_{tx}$，每future边有$z_{tjx}$：

\[
\begin{aligned}
b_{tx}&=\sum_{i:\ t=(W_{i,<k},k)}a_{ikx},\\
h_{tx}&=b_{tx}+\sum_{s,j:\tau(s,j)=t}z_{sjx},\\
z_{tjx}&=h_{tx}/c_{A_t}(x)&& (j\in N_t),\\
0\le z_{tjx}&\le h_{tx}/c_{A_t}(x)&& (j\in M_t),\\
L_{tx}&=h_{tx}-\sum_{j\in Q_t}z_{tjx}.
\end{aligned}
\tag{R-FLOW}
\]

仅合法初始边参加$b$。mandatory保全部新增coverer边，common可选；使用边金额$z$而非两个变量的乘积才能保持线性。所得

\[
h_{tx}/c_{A_t}(x)\le L_{tx}\le h_{tx}(1+|M_t|)/c_{A_t}(x),
\]

故$L$自动非负。来源标签$x\in R$不在实际$B_k$，current仍是actual角色整行金额，不能称actual同客户券。

**ROLE。** 最终必须对同一角色的全部费用共同要求

\[
\boxed{d_\ell+H_\ell+J_\ell+
\sum_{t:\operatorname{role}(t)=\ell}\sum_{x\in R\cap a_t}L_{tx}\le2u_\ell.}
\tag{ROLE}
\]

这是尚未证明总可同时满足的共同预算，不能每context另领一次$u_\ell$。

## 自动密度、一次IC与总质量

INIT给$a_{ix}\le r_{ix}\le p_{ix}$及$c_{W_i}(x)a_{ijx}\le p_{ix}$。任意合流后的可行$z$可按来源输入比例分拆，满足[来源保持密度定理](../定理/同客户来源保持流的加强初始化与节点密度--定理.md)；对非实际目标首差异位置$k$，所有reset父节点都在角色$k$，按同源同角色质量反链

\[
f_{tx}:=c_{V_t}(x)h_{tx}\le p_{kx}+\sum_{i<k}a_{ix}\le1.
\]

这对全部optional-common选择成立，不需要另把密度加入LP，也不假设唯一父。由$1+|M_t|\le c_{V_t}(x)$，同一context先对客户求和，再用实际前缀强制整个$a_t$的一次原完整IC，

\[
\sum_xL_{tx}\le\sum_{x\in R\cap a_t}f_{tx}/c_{A_t}(x)
\le u_k(A_t)\le u_k.
\]

它不支付同角色多个$t$之和。

逐客户初始库存和为1，所以

\[
|O|=\sum_\ell(d_\ell+H_\ell)+\sum_{i,x\in I}a_{ix}+\sum_{i,x\in R}a_{ix}.
\]

I-PAY把前一future项精确替为$\sum J$；严格future有限守恒把后一项精确替为$\sum L$，得到

\[
\boxed{|O|=\sum_\ell F_\ell,
\quad F_\ell=d_\ell+H_\ell+J_\ell+\sum_{t:\operatorname{role}(t)=\ell,x}L_{tx}.}
\tag{MASS}
\]

全部金额非负、只计同一单位库存一次，没有重采到$O$外，也没有将$I$付清后再传播。若ROLE存在共同可行点，MASS给$|O|\le2W$，最优$T$时给该SPE的half。

去掉ROLE后系统$P_0$非空：加强初始化正部证明给INIT点，每个该点都有$I$补余，再取common全0按角色递推$R$流。所有变量由有限客户库存和有限DAG守恒界住，故$P_0$是非空紧凸有理多面体。固定显式策略树下它是有限LP，有可行点便有有理证书；没有声称在紧凑游戏输入上规模或求解时间多项式。

## 精确价格分离与内部流消元

$F(P_0)$是紧凸付款集合。与向下闭盒$\{z:z\le2u\}$相交，当且仅当

\[
\boxed{\min_{v\in P_0}\sum_\ell\lambda_\ell F_\ell(v)
\le2\sum_\ell\lambda_\ell u_\ell\quad\text{对所有 }\lambda\ge0.}
\tag{PRICE-CUT}
\]

必要性使用同一ROLE点；不相交时有限凸分离给严格反向，法向量可取非负，因为下闭盒任何负方向的线性上确界无限。这是ROLE可行性的精确表示，尚不是新SPE资金不等式。

固定价格，对每$(t,x)$设同质流的单位费用系数$\psi_t(x)$。反向按角色递推，$k=\operatorname{role}(t)$、$c=c_{A_t}(x)$时

\[
\boxed{\psi_t(x)=\frac{\lambda_k+
\sum_{j\in N_t}\psi_{\tau(t,j)}(x)+
\sum_{j\in M_t}\min\{\lambda_k,\psi_{\tau(t,j)}(x)\}}{c}.}
\tag{PRICE-DP}
\]

mandatory份额固定；每个common份额选择留current价$\lambda_k$或送future价$\psi$，最优端点可同时采用，因为暂去ROLE后这些内部选择没有共享容量约束，而密度对整个选择族自动成立。$\psi$只是齐次金额的单位价格，**不声称可在任意context单独注入违反source密度合同的一单位并调用IC**。

因此PRICE-CUT左边等于更小LP

\[
\min_{\mathrm{INIT,I\!-\!PAY}}
\left[\sum_i\lambda_i(d_i+H_i)+\sum_{\ell,x\in I}\lambda_\ell J_{\ell x}
+\sum_{i,j,x\in R}a_{ijx}\psi_{(W_{i,<j},j)}(x)\right].
\]

必须保留INIT及$I$补余共享容量，不能把每价格各自最优路由叠加为新资金。常数$\lambda=\mathbf1$时PRICE-DP给$\psi\equiv1$，MASS使PRICE-CUT恰为$|O|\le2W$；这条仍未证，目标没有在对偶中消失。

## 回撤审查与前缀cap回收的真实接口

[来源回撤算法](../算法/固定来源路由的最大回撤与价格分离--算法.md)以$P_0$的一份固定点为输入，将每来源整个$R$路由同比例缩小并把撤下质量留当前。它允许$d'_i>u_i$，所以扩张了这里的INIT证书类，必须重新核最终**同一次**ROLE。其精确判定只覆盖固定路由比例族，不是本LP所有初始化/optional-common的可行性判定。主审查源`origin_retraction_application_audit.md`明确确认这些条件，未独立重证全部种子定理、未证实际严格扩张或SPE总成功；已有算法已完整保存回撤证明，本页不再复制新定理。

`origin_retraction_cap_salvage_scope.md`的后续核查保留三项不同对象：

1. 原actual-prefix query已受原$\sigma$当前IC控制，对同一叶再调用cap回收不增加完成。
2. 若另取尾SPE端点$y$，通过较早便宜角色$j<k$回收到同一$y$，控制的是$j$实际行动$B_j$的收益。原来源主题位于$k$，现在只是尾部规定行动；$B_j\cap R=\varnothing$，不能把$j$的cap、source密度或future边当作原$k$入口。若要接流，必须为新$y$重建初始化并取得原owner的whole-IC或明确共同前缀资金，再重算路由。
3. 在incoming history $g$改比较$T_\ell$确实是原完整IC，但新孩子为$\operatorname{finish}_\sigma(g,T_\ell)$，保留旧首偏离，通常不等于actual-prefix source叶$W_\ell$。单孩子过去claim域修复也不能免费合并互斥孩子钱包。本次没有这样的joint-cut组合。

另一合法思路是先由joint-cut生产低插入查询价的真实尾SPE端点，再用cap回收其菜单成员资格；回撤/CUT只输出金额与价格，并不输出这种端点。上述限制没有证明所有初始化或联合分配不可能，只定位缺失的共同资金。原接口源最初收到错误actor路径后已更正，不把旧AMOUNT材料错认为RETRACT，历史定位另保[核读说明](../../tools/evidence/origin-payment-density-primary/REVIEW.md)。

## 资源、关系与未付义务

四主源38093字节此前已完整读取、按相同SHA复用并原bytes保存，[清单](../../tools/evidence/origin-payment-density-primary/source-manifest.json)给原commit/path；没有无故重读或重复已通过的origin程序。六份补充旁读含PRICE-DP、同角色密度反例、两个内部合同审查、实际$I$补余及原cap回收，完整比较见[说明](../../tools/evidence/origin-payment-density-primary/REVIEW.md)。内部审查仅支持明示接口，无外审、新颖性或一般ROLE可行性认证。

本系统与[固定SAFE净券归属钱包](分数归属与实际净券的共同钱包--候选.md)是不同充分证书：前者同客户原库存、optional-common family及$2u$，后者固定净列、实际Hall取消及一份残源钱包；不能从任一局部优点推出另一系统可行。与密度定理是“初始化/局部合法性提供基础，但角色汇总需额外约束”的关系。$m=1$无future，空动作无客户变量，全零输入为零点；均不解决一般共同角色付款。

最终未付命题仍是：每个原实例及每份完整SPE，是否存在一个最优$T$及同一次INIT、$J$、$R$路由选择使ROLE成立，或是否可用更弱总支付直接证明六人half。现有非负流、单节点密度、一次IC、质量守恒和价格等价均不替代这一命题。
