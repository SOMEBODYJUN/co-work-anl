---
id: customer-attraction/source-preserving-client-flow-initialization-and-context-density
kind: theorem
type_tag: 定理
title: 同客户来源保持流的加强初始化与节点密度
status: proved-local-flow-density-and-whole-ic-role-aggregation-open
summary: 加强每条初始边至min(p,1/δ)/cW仍可初始化；同源同角色质量反链给每个非实际context的客户密度≤1，允许多query/合流/可选共同边；不是同角色总密度或共同付款上界。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round8/inventory/source_preserving_density_envelope.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round8/inventory/source_preserving_density_envelope.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round8/residual/linear_joint_payment_certificate.md
---

# 同客户来源保持流的加强初始化与节点密度

## 模型、真实reset及结论层次

在[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)中，有限单位客户、有限非空共同目录、$m\ge1$名单位提供者顺序选主题，客户终局由覆盖者均分。固定全部有序历史上的纯策略$\sigma$与其实际叶$B$；涉及IC的结论再要求$\sigma$是完整纯SPE。空主题、重复行动、零客户和任意历史平局均保留。

natural context为原策略具体有序历史$t=(g,k)$，规定动作$a_t=\sigma_k(g)$、规定叶$V_t=\operatorname{finish}_\sigma(g)$。**actual-prefix reset**为

\[
A_t=\operatorname{finish}_\sigma(B_{<k},a_t).
\]

它与在原off-history $g$改选实际行动$B_k$后的return叶不同，不能交换。下文证明每个非实际context的逐客户密度至多1、因而单context金额可由一次完整query IC付款；**不证明同一角色多个contexts的总金额可付**。

## 加强初始边，保留一次坐标库存

固定任意合法比较元组$T$（此节不需覆盖最优），$O=\bigcup_iT_i$，$W_i=\operatorname{finish}_\sigma(B_{<i},T_i)$。对$x\in T_i$写

\[
p_{ix}=1/c_T(x),\quad \delta_{ix}=c_B(x)+1-\mathbf1_{x\in B_i},\quad
P^B_{ix}=\sum_{\ell\ne i:\ x\in B_\ell\setminus T_\ell}p_{ix}/\delta_{ix},\quad
r_{ix}=p_{ix}-P^B_{ix}.
\]

actual角色$\ell$的正付款$H_{\ell x}$由这些$P^B$按recipient收集，只支持$I=O\cap C$，$C=\bigcup_iB_i$。若$x\in I$，$\delta_{ix}\ge c_B(x)$且$\sum_i p_{ix}=1$，故

\[
0\le H_{\ell x}\le w_{\ell x}:=\mathbf1_{x\in B_\ell}/c_B(x).
\]

初始future边仅指向$j>i$且$x\in(W_i)_j\setminus B_j$的真实prescribed context，加强为

\[
\widehat q_{ijx}=\frac{\min\{p_{ix},1/\delta_{ix}\}}{c_{W_i}(x)}.
\tag{NEW-CAP}
\]

它特别给$c_{W_i}(x)a_{ijx}\le p_{ix}$。每分母仅在相应客户被覆盖时使用。

**加强后仍可初始化。** 固定$(i,x)$，缩写$t=c_T(x)$、$d=\delta_{ix}$、$w=c_{W_i}(x)$。令$n_B=\#\{\ell:x\in B_\ell\setminus T_\ell\}$、$n=\#\{j>i:x\in(W_i)_j\setminus B_j\}$，$n_-$为相反方向消失的future coverer数，$k=d-n_B$。集合计数给

\[
w=d+n-n_-,\quad 1\le k\le\min(d,t),\quad
r_{ix}=k/(td),\quad \widehat q_{ix}:=\sum_j\widehat q_{ijx}=n\min(d,t)/(tdw).
\]

于是

\[
kw-n\min(d,t)=kd-kn_-+n[k-\min(d,t)]\le kd\le td,
\]

从而$(r_{ix}-\widehat q_{ix})_+\le1/w$。先对$x\in T_i$求和，再使用实际前缀处对整个主题$T_i$的一次完整IC，得到

\[
\sum_x(r_{ix}-\widehat q_{ix})_+\le u_i(W_i)\le u_i(B).
\tag{INIT-IC}
\]

设$r_i=\sum_xr_{ix}$、$b_i=(r_i-u_i)_+$、$S_i=\sum_x\min(r_{ix},\widehat q_{ix})$，则$b_i\le S_i$。若$S_i>0$取$a_{ix}=b_i\min(r_{ix},\widehat q_{ix})/S_i$，按$\widehat q_{ijx}$比例拆边；否则取0。令$c_{ix}=r_{ix}-a_{ix}$，得到

\[
p_{ix}=P^B_{ix}+c_{ix}+\sum_j a_{ijx},\qquad
\sum_xc_{ix}=\min(r_i,u_i)\le u_i.
\]

这只证明一个可行初始化，不必固定该极大current角点。任取加强边界内$a$，只要$c+\sum a=r,c\ge0,\sum c\le u_i$，下述密度证明仍成立；改变初始$I/R$拆分时，实际补余付款$J$必须随同重算，不能继承旧数值。

## 同客户核先由非负守恒定义，不预设密度或IC

对输入客户$x\in a_t$，记$v_{tx}=1/c_{V_t}(x)$、$D_{tx}=1/c_{A_t}(x)$。正recipient为$j\ne k$、$x\in(A_t)_j\setminus(V_t)_j$，原价

\[
q^+_{tjx}=\frac1{c_{A_t}(x)c_{V_t}(x)}.
\]

相反消失coverer给负项$N_{tx}$，正价和为$P_{tx}$。逐客户精确有

\[
v_{tx}-P_{tx}=D_{tx}-N_{tx}>0.
\tag{LOSS}
\]

合并同context、同客户输入$h_{tx}$，先定义$f_{tx}=c_{V_t}(x)h_{tx}$，不假定其至多1。每条正边发出$fq^+=h_{tx}/c_{A_t}(x)$，当前留

\[
L_{tx}=f_{tx}(v_{tx}-P_{tx})\ge0.
\]

future recipient进入$A_t$的真实prescribed context；过去recipient必有$x\in B_j$，只能作actual同客户终点，不能购买过去玩家的IC。若future目标history恰为actual-prefix，同样直接作actual同客户终点。所有非终端边严格增加角色，有限DAG及LOSS定义唯一非负守恒流，无需预先调用SPE或密度。

可以给共同future coverer$j>k,x\in(A_t)_j\cap(V_t)_j$加入$0\le z_{tjx}\le h_{tx}/c_{A_t}(x)$，从current扣掉同量；完整$O$版本也可加入同范围的共同past actual终点。原正边加共同边至多占$A_t$中当前之外的coverer，因此新current仍至少$h_{tx}/c_{A_t}(x)$，至多原$L_{tx}$。raw差核为共同边全0；全取满为同客户uniform-reset角点。一般不是完整利润SAFE/CLIP的删边版本，未证明费用相对旧核单调。

## 来源反链与广义密度定理

更一般地，仅固定任意完整纯policy（此段不需SPE、比较最优或$T$）。每个query-source $\alpha$有角色$i(\alpha)$、合法动作、真实actual-prefix query叶$W_\alpha$及客户库存$p_{\alpha x}\ge0$，满足

\[
\sum_\alpha p_{\alpha x}\le1,\quad
A_{\alpha x}:=\sum_j b_{\alpha jx}\le p_{\alpha x},\quad
b_{\alpha jx}\le p_{\alpha x}/c_{W_\alpha}(x).
\tag{SOURCE}
\]

每条初始边仅进入$W_\alpha$中确实覆盖$x$的严格future prescribed context。同角色可有多query，甚至相同query的多标签，但都共用同一客户库存和。SOURCE本身不附送initial current、$H/J$或任何利润预算；密度证明也不需假设source当前行动覆盖$x$，只需其正输入目标覆盖$x$。

合流后每个输出可按各source输入比例拆回标签，零输入不作比例。由于角色严格递增，同一source/client的每条质量路径在同一角色层最多访问一次，所以该层**所有contexts**的输入和至多$A_{\alpha x}$。这是来源质量反链，不是将不同有序历史合并。

固定非actual目标$t=(g,j)$，令$k<j$为$g$与actual-prefix的首次差异位置。任何reset父节点的角色必须正是$k$，否则其actual-prefix reset叶首差异位置与目标不符；所有这些父的reset叶等于目标规定叶$V_t$。mandatory父边对目标密度$c_{V_t}(x)h_{tx}$的贡献恰为父$h_{sx}$，共同边贡献不超过它。

到这些角色$k$父节点的source角色都小于$k$，因此反链给间接贡献至多$\sum_{i(\alpha)<k}A_{\alpha x}$。直接注入$t$的source角色只能为$k$，其$W_\alpha=V_t$，逐边SOURCE使直接密度总额至多$\sum_{i(\alpha)=k}p_{\alpha x}$。故

\[
\boxed{c_{V_t}(x)h_{tx}
\le\sum_{i(\alpha)=k}p_{\alpha x}
+\sum_{i(\alpha)<k}A_{\alpha x}
\le1.}
\tag{GENERAL-DENSITY}
\]

canonical初始化是source $\alpha=i,p_{ix}=1/c_T(x)$的特例，给更强前缀式$f_{tx}\le p_{kx}+\sum_{i<k}a_{ix}\le\sum_{i\le k}p_{ix}\le1$。父节点可以有多个、来源可以重合；证明不假设唯一父。actual-prefix目标没有首差异$k$，只作为实际终点，**不声称它也满足该密度界**。全部optional-common选择同时适用，故不是另加到LP的密度约束。

## 单节点whole-IC与精确退款

再要求原$\sigma$为完整SPE。对一个非actual context，actual-prefix完整query IC给$D_t:=\sum_{x\in a_t}D_{tx}\le u_k$，$e_t=u_k-D_t\ge0$。没有输入的客户取$f=0$。密度与LOSS给

\[
L_t=\sum_xf_{tx}(D_{tx}-N_{tx})\le\sum_xD_{tx}=D_t\le u_k,
\]

及精确非负退款

\[
u_k-L_t=e_t+\sum_{x\in a_t}(1-f_{tx})D_{tx}+\sum_{x\in a_t}f_{tx}N_{tx}\ge0.
\tag{REFUND}
\]

先证明金额不超过**整个**query利润，再调用一次完整IC；不是逐客户重权IC。加入共同边只减current，退款再增加同量。正输入使query动作非空，所以$u_k>0$；可按actual角色$k$的真实利润份额统一分摊金额，来源$x$不必属于$B_k$。

$I$来源可以先用[共同付款系统](../候选/固定比较元组的线性共同付款证书--候选.md)的实际补余$J$直接清掉，剩余仅$R=O\setminus C$进入同一客户保持核：此时无past实际coverer或actual-prefix $R$终点，全部$R$ source严格future最终成为current。删除来源不增加密度；但须按本次$a$重算$J$。若换为仅fresh-profit重采核，必须重新按其分母计算，不能继承本客户保持流的费用或把两核付款相加。

## 全部比较客户与仅遗漏客户的两种共同账

canonical比较库存的完整$O$流始终保留原客户身份。记$E_{\ell x}$为下游全部past或actual-prefix同客户终端，支持于$x\in B_\ell$。由初始$p=P^B+c+a$及有限DAG守恒，精确有

\[
|O|=\sum_\ell(d_\ell+H_\ell)+\sum_{t\text{ 非actual},x}L_{tx}+\sum_{\ell,x}E_{\ell x}.
\tag{JOINT-LEDGER}
\]

同一角色的真正未付条件是

\[
\sum_{t:\operatorname{role}(t)=\ell,x}L_{tx}+\sum_xE_{\ell x}
\le2u_\ell-d_\ell-H_\ell,
\]

并非每个context单独可付便能相加。先付清$I$来源后，$R$无实际终端，联合账变为$|O|=\sum_\ell(d_\ell+H_\ell+J_\ell)+\sum_{t,x\in R}L_{tx}$，待证余量变为$2u_\ell-d_\ell-H_\ell-J_\ell$。两种账本是不同选择，不能对同一$I$来源既领$J$又保留其旧传播；也不能把退款中的actual $C$查询收入另记一份库存。

## 不得跨越的同角色边界

每个context有$L_t\le u_k$或$f_{tx}\le1$，不推出同一角色多个context和也由一次$u_k$支付。旁读的明确非SPE policy诊断对此给纯流反例：四角色0–3，目录$a=\{x\},b=\varnothing$，所有history默认$b$，仅$a,ba,aab,bba$规定$a$，actual为$bbbb$。角色0强制$a$后为$aaba$，一单位源在三个coverer间均分。

| context | 输入$h$ | 规定叶负载 | 密度$f$ | current | 正future输出 |
| --- | --- | ---: | --- | --- | --- |
| $a$ | $1/3$ | 3 | 1 | $1/6$ | 角色2：$1/6$ |
| $ba$ | $1/6$ | 2 | $1/3$ | $1/12$ | 角色3：$1/12$ |
| $aab$ | $1/3$ | 3 | 1 | $1/3$ | 无 |
| $bba$ | $1/12$ | 2 | $1/6$ | $1/12$ | 无 |

同角色3同动作的密度和为$7/6>1$，单节点仍均不超过1，全部源质量守恒。actual全零利润但$a$偏离有正收益，故它**不是SPE**；只排除从纯库存/支持/DAG推出聚合密度。角色3 current和$5/12\le1$，也没有反驳更弱的同query current共同付款、所有路由选择或六人half。

本定理可复用的是NEW-CAP、来源保持反链、非实际节点密度及一次whole-IC退款；最终仍须对同一角色全部current和actual终点施加一份共同预算。源/旁读原件、两个历史内部合同审查及其准确未证域见[本批核读说明](../../tools/evidence/origin-payment-density-primary/REVIEW.md)。本批解析重推，不重复运行前批正确origin审计，不将未领取的密度诊断脚本称已复跑。
