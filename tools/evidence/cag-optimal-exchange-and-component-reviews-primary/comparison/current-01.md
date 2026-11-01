---
id: same-actual-welfare-harmonic-terminal-wallet-payment
kind: lemma
type_tag: 引理
title: 同一实际福利对末对钱包的调和复制付款
status: proved-general-component-with-unpaid-early-frozen-taxes
summary: 各较早实际节点复制同一倒二主题的真实IC和逐客户调和分母界，在同一份W内支付(2Hm+1)倍末对reduced-wallet，并保留精确非负退款；它不支付早期冻结税。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round9/exchange/harmonic_terminal_wallet.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round9/credible/review_harmonic_terminal_wallet.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round9/exchange/README.md
---

采用[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)：有限单位客户、有限非空共同目录、任意 $m\ge2$ 名单位提供者及任意一份完整有序历史纯 SPE。目录允许空主题、同覆盖不同标签，选择允许重复，所有离轨平局仍按同一原策略执行。令实际叶为 $S_1,\ldots,S_m$，实际利润 $u_i$，$W=\sum_i u_i$ 为根实际覆盖数。结论是
\[
\boxed{(2H_m+1)C'\le W,\qquad H_m=\sum_{r=1}^m\frac1r.}\tag{HW}
\]
$C'$ 是下面同一实际末对的钱包；本引理不取决于任何比较最优元组。HW 是已证的全输入组件，弱最优冻结指派及其早期税仍开放，六人半覆盖未由它解决。五人半覆盖当前有另一路[独立定理](../定理/五人半覆盖--定理.md)，不能倒推本页更强接口成立。

## 同一实际末对的静态资金

写 $A=S_{m-1}$、$B=S_m$，$a=u_{m-1}$、$v=u_m$；$k_x$ 是实际前 $m-2$ 位在 $x$ 上的覆盖次数。定义
\[
L=\sum_{x\in A}\frac1{k_x+2},\quad
C=a-L=\sum_{x\in A\setminus B}\frac1{(k_x+1)(k_x+2)},\quad
t=\min(a,v),\quad C'=t-L.
\]
实际末位可以复制合法主题 $A$，故 $v\ge L$；逐客户 $a\ge L$。因此
\[
0\le C'\le C,\qquad C-C'=(a-v)_+.
\tag{TAIL}
\]
这与[选择性冻结钱包](实际末对冻结查询的选择性钱包--引理.md)的 $C,C'$ 是同一对象。该前件还证明每个合法查询的点态静态行
$f_{m-1}(T)=a+C'-h_T$、$h_T\ge0$，以及 $f_m(T)\le v$。本引理新增的原来源内容是用所有更早真实复制行支付同一份 $C'$，不是再造一份可叠加的实际钱包。

## 各较早角色的一条完整真实复制行

对 $i\le m-2$，令 $r_i=m-i+1$，$b_i(x)$ 是实际前 $i-1$ 位负载，并定义
\[
q_i=\sum_{x\in A}\frac1{b_i(x)+r_i},\qquad
F=\sum_{i\le m-2}q_i.
\]
角色 $i$ 在其完整实际有序前缀改选 $A$ 后继续原策略。对每个 $x\in A$，当前人已覆盖它，而后继至多再给 $r_i-1$ 个覆盖者；无论后继如何依历史改变，该角色最终收益至少 $q_i$。原 SPE 的完整偏离 IC 因而给
\[
u_i\ge d_i(A)\ge q_i.\tag{COPY}
\]
这里对完整主题 $A$ 使用一次原利润行，没有客户重权 IC，不冻结后继，也不拿离轨后继利润替换实际后继利润。对不同 $i$ 各用自身的一次预算，得到
\[
W\ge F+a+v\ge F+2t=F+2L+2C'.\tag{ONE-W}
\]
$F$ 是复制安全下界的和，不是实际前 $m-2$ 位的利润和；两者差额在退款中显式保留。

## 完整逐客户调和计费

对 $x\in A$ 令
$F_x=\sum_{i\le m-2}1/(b_i(x)+r_i)$，所以 $F=\sum_{x\in A}F_x$。
由 $b_i(x)\le k_x$ 和 $k_x+r_i\le(k_x+1)r_i$，有
\[
F_x\ge\frac{H_m-3/2}{k_x+1}.
\]
因为早期角色对应 $r_i=m,m-1,\ldots,3$，其倒数和正是 $H_m-3/2\ge0$。于是，置 $k=k_x$，
\[
\begin{aligned}
F_x+\frac2{k+2}-\frac{2H_m-1}{(k+1)(k+2)}
&\ge\frac{(H_m-3/2)(k+2)+2(k+1)-(2H_m-1)}{(k+1)(k+2)}\\
&=\frac{k(H_m+1/2)}{(k+1)(k+2)}\ge0.
\end{aligned}\tag{CLIENT}
\]
对 $A\setminus B$ 求和；$A\cap B$ 上保留 $F_x+2/(k_x+2)$ 的非负贡献，得到
\[
F+2L\ge(2H_m-1)C\ge(2H_m-1)C'.\tag{HARM}
\]
与 ONE-W 合并即得 HW。这里所有分母严格正；无需在不同客户上同时实现最坏历史，也没有预设偏离后叶满足半覆盖。

## 退款的精确来源

定义
\[
R=\sum_{i\le m-2}(u_i-q_i)\ge0,\qquad
J=F+2L-(2H_m-1)C\ge0.
\]
$J$ 逐客户等于 CLIENT 在 $A\setminus B$ 上的完整余量，加上 $A\cap B$ 的 $F_x+2/(k_x+2)$。由于
$a+v=2t+|a-v|$、$C-C'=(a-v)_+$，有准确恒等式
\[
\boxed{W-(2H_m+1)C'
=R+|a-v|+J+(2H_m-1)(a-v)_+.}\tag{REFUND}
\]
每个右端非负项都有来源：$R$ 是较早实际利润对其复制下界的余量，$|a-v|$ 是末对利润失衡，$J$ 是逐客户调和余量，最后一项是从 $C$ 改成 $C'$ 的信用。它们不是再加进同一 $W$ 的独立收入。本账已经使用早期 COPY 行和两份实际末对利润；若别的初始化或角色银行也使用这些资金，合并前必须证明未重用余额。

$m=2$ 时早期和为空、$H_2=3/2$，上述乘法式与空和仍成立。$A$ 为空、$W=0$、$C'=0$、重复或空主题都无需除 $W$。$m=1$ 无末对，本引理不适用。在非零外部背景中不能把活跃玩家利润和直接改称新增覆盖数；本页的 $W$ 始终是整个根实际叶的原利润和。

## 五人与六人的准确接入位置

直接代入同一一般推导，
\[
m=5:\ H_5=137/60,\quad C'\le30W/167<W/5,\quad
W/5-C'\ge17W/835;\qquad
m=6:\ C'\le10W/59.
\]
六人系数 $10/59$ 大于 $1/6$；仅由 HW 得 $W/6-C'\ge-W/354$，不能确保这块非负。这不是六人 half 反例。五人的正余额也尚未支付三条早期冻结税。

具体而言，任取覆盖最优 $m$ 元组及排列，重标主题 $T_i$ 分给角色 $i$。冻结其他实际动作的利润为 $f_i(T_i)$，在真实实际前缀强制 $T_i$ 的收益为 $d_i(T_i)$。令 $e_i=u_i-d_i(T_i)\ge0$、$E_i=f_i(T_i)-d_i(T_i)$，且 $Q=\sum_i f_i(T_i)$。选择性钱包前件给
\[
Q-W=C'+\sum_{i\le m-2}(E_i-e_i)-e_m-h_{T_{m-1}}.\tag{QTAIL}
\]
所以弱桥 $Q\le(1+1/m)W$ 仍需共同选择最优元组和排列，使
\[
\sum_{i\le m-2}(E_i-e_i)\le W/m-C'+e_m+h_{T_{m-1}}.
\]
HW 只确定右边 $W/5-C'$ 的一块已付资金；左边缺一般共同上界。强 $Q\le W$ 已失败，弱桥仍是充分候选；不得以此局部调和付款升级为全位置共同容量、跨互斥context银行或半覆盖证明。

## 后续静态吸收对接口的修订

全仓后续 `round10/exchange/direct_terminal_surplus_and_early_gap.md` 保留同一 QTAIL，但不再要求较强弱指派桥来证明half。为说明这个变化，令 $O=\cup_iT_i$、$X=A\setminus B$，并保留静态松弛
$\mathcal S=Q+(1-1/m)W-|O|\ge0$。对客户，记实际次数 $c$、比较次数 $d$、同角色同时实际/比较覆盖次数 $z$；$c,d>0$ 时其松弛系数是
$s_x=d/(c+1)+z/[c(c+1)]-1/m$。其余非零情况为 $c=0,d>0$ 时 $d-1$，及 $c>0,d=0$ 时 $1-1/m$。均非负；在 $c=m$ 时需保留 $z=d$ 才得 $(d-1)/m\ge0$。

该后续逐客户证明
\[
Z_{\rm sur}:=\mathcal S+|X|/m-C\ge0.
\]
$X$ 外保 $s_x\ge0$；$X$ 内 $c\ge1$，若 $d=0$，新系数为 $1-1/[c(c+1)]$，若 $d>0$ 则为 $(cd+z-1)/[c(c+1)]$，都非负。此吸收不需SPE或最优性，不是新增实际收入。

写 $\Delta=(a-v)_+$、$\mathrm{EARLY}=\sum_{i\le m-2}(E_i-e_i)$，则 QTAIL 和上式给准确直接接口
\[
|O|-2W=\mathrm{EARLY}-e_m-h_{T_{m-1}}
-(W-|X|)/m-\Delta-Z_{\rm sur}.\tag{DIRECT}
\]
所以直接half证明可让静态松弛与 $|X|/m$ 吸收尾钱包，无需另用HW；但 EARLY 仍未有全历史共同上界。HW依旧是正确组件，不能把它的同一资金再加到DIRECT的信用上。该后续原件本批全文比较并保存，不额外done，也不把其接口重排说成一般付款已闭合。

## 内部审查与来源身份

主源 exchange9 写出全 $m$ 证明和 REFUND。正式主源 credible9 的 `review_harmonic_terminal_wallet.md` 明确**读作者全文后**依定义独立重构，不是盲审；它核 COPY、CLIENT 分子 $k(H_m+1/2)$、交集退款、利润失衡、$m=2$ 及五人剩余，并明确当时未重跑作者数值审计。

README 另引 menu9 的 `terminal_wallet_independent_review.md`，是不同文件：先收到候选消息、在读作者稿前重构证明，再对作者稿检查 REFUND。该审查用 `F_actual` 表示早期实际利润和、`Q` 表示本页 $F$，二者不能混成一个量。它不认证外审或新颖性。两个审查的先验与执行身份分别保留，不把本批读后重构改称新增盲审。

另全文核了原root的 `harmonic_wallet_independent_reconstruction.md`：先收到定理陈述、读作者稿前重构，收到menu9确认后再对稿，并独立Fraction核五人代入。它与credible9读后检查也是不同先验，不能合并为同一“全盲审”记录。

本批一次原审计入口在两个固定完整策略上重核全部IC及公式，实现证据见[审计与审查资源](../计算/调和末对钱包的原审计与审查身份--计算.md)。原件、逐源SHA、真实执行和后续比较见[证据目录](../../tools/evidence/harmonic-terminal-wallet-primary/README.md)。普遍性由本页解析证明承担；有限实现、内部审查与未付一般接口分别保持。
