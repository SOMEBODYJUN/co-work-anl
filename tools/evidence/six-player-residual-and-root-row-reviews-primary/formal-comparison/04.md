---
id: "customer-attraction/two-remaining-tax"
kind: "lemma"
type_tag: "引理"
title: "固定背景下恰两名剩余玩家的税界"
status: "complete"
truth_status: "proved"
review_level: "internal-reconstruction-and-exact-replay"
scope: "任意合法有序前缀；恰两名剩余提供者；每份完整纯SPE；任意两个比较主题"
legacy_ids:
  - "CA-TWO-REMAINING-TAX"
summary: "三个真实节点的最优性加两个非负交叠余项，控制两个比较主题的剩余总利润；不依赖一般税归纳。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/customer_attraction/two_remaining_tax.md#1-固定背景与精确命题"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/customer_attraction/two_remaining_tax.md"
---

# 固定背景下恰两名剩余玩家的税界

## 对象与精确命题

采用[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)。固定任意合法有序前缀，在客户 $x$ 上留下整数负载 $b_x\ge0$，之后恰有两人依次行动。
令所给完整纯SPE的实际续局为 $(A,B)$。所有实际、比较主题允许重复或为空，所有离轨历史和平局保留。

定义

$$
U_b(X,Y)=\sum_{x\in X}\frac1{b_x+1+\mathbf1_{x\in Y}},\qquad
R_b(X,Y)=U_b(X,Y)+U_b(Y,X).
$$

对任意 $T,S\in\mathcal S$，

$$
\boxed{R_b(T,S)\le R_b(A,B)+
\sum_{x\in A}\frac1{(b_x+1)(b_x+2)}.}
\tag{T2}
$$

右边同时界住所有比较二元组的最大值。若 $b\ne0$，这里比较的是剩余两人总利润，不是完整终局覆盖。

## 完整证明：必须使用同一策略的真实离轨回复

令

$$
f_b(X)=\sum_{x\in X}\frac1{b_x+1},\qquad
g_b(X,Y)=\sum_{x\in X\cap Y}\frac1{(b_x+1)(b_x+2)}.
$$

逐客户有

$$
U_b(X,Y)=f_b(X)-g_b(X,Y),\qquad
R_b(X,Y)=f_b(X)+f_b(Y)-2g_b(X,Y).
\tag{1}
$$

写实际收益为 $u_1=U_b(A,B),u_2=U_b(B,A)$，令 $Q$ 是所给完整策略在首人改选 $T$ 后的真实末位回复。
三个合法SPE比较分别是

$$
u_1-U_b(T,Q)\ge0,
\quad U_b(Q,T)-U_b(S,T)\ge0,
\quad u_2-U_b(Q,A)\ge0.
\tag{2}
$$

第一个在固定前缀的首节点，第二个在偏离前缀 $T$ 后的末节点，第三个在实际前缀 $A$ 后的末节点。
共同目录保证 $Q$ 在实际末节点也是合法比较主题。它不是重新选的均衡或冻结的 $B$。

将(1)展开，精确抵消得到

$$
\begin{aligned}
R_b(A,B)+g_b(A,A)-R_b(T,S)
={}&[u_1-U_b(T,Q)]\\
&+[U_b(Q,T)-U_b(S,T)]\\
&+[u_2-U_b(Q,A)]\\
&+[g_b(A,A)-g_b(A,Q)]+g_b(T,S).
\end{aligned}
\tag{3}
$$

前三项由(2)非负；另外

$$
g_b(A,A)-g_b(A,Q)
=\sum_{x\in A\setminus Q}\frac1{(b_x+1)(b_x+2)}\ge0,
\quad g_b(T,S)\ge0.
$$

故(3)证明(T2)。任意有限客户数通过求和覆盖；不要求SPE终局是静态PNE，不要求同计数历史使用相同回复。

## 空背景推论、用途和不能外推的部分

空前缀时 $R_0(X,Y)=|X\cup Y|$，且 $g_0(A,A)=|A|/2$，所以

$$
\operatorname{OPT}_2\le W(A,B)+\tfrac12|A|\le\tfrac32W(A,B).
$$

例如两个不交主题分别有二名、一名单位客户，两人所有历史都选大主题构成完整SPE：选大主题最终收益至少一，偏离单例至多一。
实际 $W=2,\operatorname{OPT}_2=3$，说明两人范围的 $3/2$ 可达到。
该特例也来自三人锐界正文所述大主题家族的同一直接论证，不依赖文献导入。

此引理是[三人两人税组合界](../定理/三人两人税组合界--定理.md)的承重依赖；仓库四人证明也直接使用它，而不使用三人福利界。
更长后缀的首动作偏离会产生一组真实后继，不能把本证明单一回复 $Q$ 直接替换为共同最优回复组。
税的望远镜式、一般归纳的条件逻辑和已失败接口已由另一批正式整理，见[固定背景剩余收益与税](../定义/固定背景剩余收益与税--定义.md)。

本引理的审计只检查其逐客户恒等式；原来源后半部的末位诊断、顺序重排家族已分别拆入[末位收益税诊断](末位收益税诊断--引理.md)和[终局重排税差](../构造/终局重排税差--构造.md)。

原税页§4中“若每个子局首步桥成立，则根有$\operatorname{OPT}_m\le(2-1/m)W$”只是一项前提已被否定的条件推导；正确的税预算不能补回该前提。
该节的分母例$b=c=10$及三类失败范围也已完整吸收到上述税定义/接口对象，本批不再另造重复正文。

## 证据与出处

来源是 `two_remaining_tax.md` §§1–3、§5；源ID `3248e8da0ea722454971`。两冻结版本内容相同。
独立的 `Fraction` 审计在背景 $0,1,2,10,1000,10^{40}$ 上各检查全部32个 $A,B,T,S,Q$ membership，共192项；没有调用均衡求解器。
这些有限背景用于查实现错误，任意合法背景结论来自(1)–(3)的符号抵消与正分母。
脚本、冻结报告和本轮复跑见[审计资源](../计算/三人和两人税精确审计--计算.md)。

原稿记录内部独立复核，未记录外部同行评审；原稿将空背景两人界归于 Deng 等 §5 Theorem 5.2。本轮给出自足证明，未核验外部版本或新颖性。
