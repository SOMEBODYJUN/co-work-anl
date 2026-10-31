---
id: static-covering-surplus-absorbs-terminal-wallet
kind: lemma
type_tag: 引理
title: 静态覆盖松弛吸收末对钱包的直接缺额式
status: proved-static-absorption-and-exact-open-early-interface
summary: 任意实际合法叶和m槽比较元组的静态松弛S与差集份额吸收同一末对C；接真实末对恒等式得精确DIRECT，尾钱包消去而EARLY仍未支付。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round10/exchange/direct_terminal_surplus_and_early_gap.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round10/tree/exchange_terminal_refinement_review.md
---

采用[有限单位客户共同目录模型](../定义/共同目录完整历史模型--定义.md)，任意 $m\ge2$，保留空主题、重复及所有有序历史的平局。前两节只需两个合法长度 $m$ 元组，不需SPE或覆盖最优性；后两节才使用同一原完整策略的真实末对IC。本对象不是新增实际收入或末对常数优化，也未证明早期付款或六人半覆盖。

## 任意角色指派下的静态松弛

固定合法叶 $Z=(S_1,\ldots,S_m)$，$B_Z=\cup_iS_i$、$W=|B_Z|$；任取比较主题 $T_1,\ldots,T_m$ 分给相应角色，令 $O=\cup_iT_i$。客户实际负载为 $c_x$，比较负载为 $k_x$，同槽双覆盖次数为
$t_x=\#\{i:x\in S_i\cap T_i\}$。冻结其他实际动作，定义
\[
f_i(T)=\sum_{x\in T}\frac1{c_x+1-\mathbf1_{x\in S_i}},\quad
Q=\sum_i f_i(T_i),\quad
\mathcal S=Q+(1-1/m)W-|O|.
\]
交集内 $c_x\ge1$，无零分母。对 $c=c_x>0$，有 $t=t_x$ 个查询替换原来已覆盖该客户的角色、另 $k-t$ 个增加覆盖者，故
\[
Q_x=\frac tc+\frac{k-t}{c+1}=\frac{k}{c+1}+\frac{t}{c(c+1)}.
\]
静态松弛的完整逐客户系数为
\[
\mathcal S_x=\begin{cases}
0,&c=k=0,\\
k-1,&c=0,\ k>0,\\
1-1/m,&c>0,\ k=0,\\
k/(c+1)+t/[c(c+1)]-1/m,&c,k>0.
\end{cases}\tag{S}
\]
前三项非负。若 $0<c<m,k>0$，则 $k/(c+1)\ge1/m$；若 $c=m$，每个比较覆盖槽的原角色都覆盖该客户，必须保留约束 $t=k$，所以末项为 $(k-1)/m\ge0$。不能把 $c=m,t=0,k>0$ 当作合法独立参数。因此 $\mathcal S\ge0$，也恢复无条件 $|O|\le Q+(1-1/m)W$。这里 $Q$ 不是顺序SPE的真实偏离利润。

## 收回同一末对差集钱包

令 $A=S_{m-1}$、$B=S_m$、$X=A\setminus B$。同一末对的 unreduced 钱包为
\[
C=\sum_{x\in X}\frac1{c_x(c_x+1)}.
\]
此 $C$ 仅是最后一条实际相邻边的钱包，不是全部相邻边之和 $C_{\rm adj}$。
在 $X$ 内，当前倒二已覆盖而末位未覆盖，故 $1\le c_x\le m-1$。定义
\[
\boxed{Z_{\rm sur}=\mathcal S+|X|/m-C\ge0.}\tag{ABSORB}
\]
证明：$X$ 外仍是式(S)的非负项。$X$ 内，若 $k=0$，则 $t=0$，修正后的系数为 $1-1/[c(c+1)]\ge0$；若 $k>0$，则为
\[
\mathcal S_x+1/m-1/[c(c+1)]
=\frac{ck+t-1}{c(c+1)}\ge0.
\]
这里只用 $c,k\ge1$、$t\ge0$。空差集恢复 $\mathcal S\ge0$，全零客户亦成立。

ABSORB 从原来已保留的静态松弛与 $|X|/m$ 份直接覆盖额度收回 $C$，没有让原策略换续局、没有客户重权IC，也不是另一份actual福利。它不能单独给早期角色的静态/真实差上界。

## 恢复真实末对后得到精确直接接口

现在要求 $Z$ 是同一份完整历史纯SPE的实际叶，$u_i$ 是实际利润，$W=\sum_i u_i$。在实际有序前缀 $Z_{<i}$ 强制 $T_i$ 后仍跟原策略，所得当前收益记 $D_i$。令
\[
e_i=u_i-D_i\ge0,\quad E_i=f_i(T_i)-D_i,\quad
\mathrm{EARLY}=\sum_{i\le m-2}(E_i-e_i).
\]
较早的 $E_i$ 不需非负。由[原点态末对钱包](实际末对冻结查询的选择性钱包--引理.md)，写 $a=u_{m-1}$、$v=u_m$、$\Delta=(a-v)_+$、$C'=C-\Delta\ge0$，并有 $h=h_{T_{m-1}}\ge0$ 和
\[
Q-W=C'+\mathrm{EARLY}-e_m-h.\tag{QTAIL}
\]
$C'\ge0$ 来自实际末位复制IC，不是静态 $\mathcal S\ge0$ 的后果。此处使用原恒等式，不重新多领一次末对利润。

ABSORB 给纯代数
\[
W/m+\mathcal S-C'=(W-|X|)/m+\Delta+Z_{\rm sur}.
\]
将 $|O|=Q+(1-1/m)W-\mathcal S$ 与 QTAIL 合并，得到
\[
\boxed{|O|-2W=\mathrm{EARLY}-e_m-h
-(W-|X|)/m-\Delta-Z_{\rm sur}.}\tag{DIRECT-EARLY}
\]
若用 unreduced 信用 $G=e_{m-1}+g+\ell=\Delta+h$，同式成为
\[
\boxed{|O|-2W=\mathrm{EARLY}-e_m-G-(W-|X|)/m-Z_{\rm sur}.}\tag{DIRECT-G}
\]
所有负号下显示的信用均非负，因 $X\subseteq B_Z$。这没有把未知项的上界误当有利下界；EARLY 本身仍需上界。

## 直接half接口与更强桥的区别

取 $O$ 覆盖最优，DIRECT 给原half的准确剩余接口：
$\mathrm{EARLY}\le e_m+h+(W-|X|)/m+\Delta+Z_{\rm sur}$。
不再需要较强 $Q\le(1+1/m)W$，也不需要另花[调和复制付款](同一实际福利对末对钱包的调和复制付款--引理.md)的 $C'$ 预算。尾项与保留的静态松弛已一起消去；这不表示早期真实续局/冻结差已经付清，更不能再把HW相同来源加作独立钱。

在 $m=5$ 同式为
$\mathrm{OPT}_5-2W=\mathrm{EARLY}-e_5-G_{T_4}-(W-|X|)/5-Z_{\rm sur}$，三条早期项仍未控制。当前[五人half](../定理/五人半覆盖--定理.md)已由另证解决；旧稿只是此路线当时未推出，六人也未由DIRECT关闭。

十客户相邻钱包反例中的坏最优指派 $(A,A,D)$ 是具体一致性例：$W=9,Q=11,|O|=10,|X|=6,C=C'=1$，所以 $\mathcal S=7,Z_{\rm sur}=8$；真实早期和为1、$e_m=h=\Delta=0$，DIRECT两侧均为−8。它反驳的是另一个全行相邻钱包桥，不冲突于本静态吸收或最终末对引理，见[反例](../反例/十客户重复实际行的相邻钱包失败--反例.md)。此处是公式直接代入，原程序不单独输出这些DIRECT字段。

## 审查先验与停止位置

tree10收到精确陈述和逐客户公式后，在尚未读作者证明正文时重推；它是知道候选公式的内部对稿核查，不是对未知结论的盲发现。它完整核 $c=m\Rightarrow t=k$、$X$ 内两格、末位复制IC的独立来源、每个负号、$m=1$域外及五人仍未付EARLY；未运行扫描，也不认证外审或新颖性。

主源末段提及的全后缀调和势尝试，已在旧两查询真实child拼接和自洽查询稿中留下删除势差/联合续局势遗憾。后继各自IC不等于整条suffix联合最优；固定点存在也不提供缺少的金额界。本批全文对读那两稿只解释本尝试未获付款，不恢复它们的历史OPEN为新的背景域结论。原任意背景与根实际前缀量词仍须区分。

本引理的直接前件是静态逐客户恒等式与原真实末对钱包，两类假设分开。原件、内部审查、后续/先有比较和本批程序执行身份见[证据](../../tools/evidence/direct-surplus-compact-wallet-primary/README.md)；本批唯一原审计执行检查十客户构造，不以有限检查代替本页全参数代数。
