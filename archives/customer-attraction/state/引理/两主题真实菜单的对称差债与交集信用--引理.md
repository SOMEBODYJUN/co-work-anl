---
id: two-query-real-menu-symmetric-difference-debt-and-intersection-credit
kind: lemma
type_tag: 引理
title: 两主题真实菜单的对称差债与交集信用
status: proved-local-identity-and-last-two-boundary; full-path-PW-payment-unproved
summary: "精确K对称缺口=E−J−两根IC松弛，PW等价响应债预算并足够FTA；原review只审恒等式。知情比较补一后继E为两末BR松弛负和≤0，71例单向75/2失败但对称余23/2。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/continuation_general/tree/pairwise_gap_identity.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/continuation_general/tree/review_pairwise_identity.md"]
---

# 两主题真实菜单的对称差债与交集信用

3295B主稿与1994B代数独审全文primary处理。它们成立的是局部恒等式和条件归约，未证明问号PW预算；当前清洗还与已证恰一末位BR接口和71客户完整SPE族作知情解析比较，新增的是明确连接，不冒原review已审这些后加推导、盲审或新颖性。

## 同一实际节点的全部真实分枝

有限单位客户、有限非空共同目录、任意m≥1单位提供者、每份完整有序历史纯SPE，保重复、空主题、同覆盖标签、零客户及历史平局。固定actual位置i和其actual有序前缀h_i，背景b_x、actual利润u_i；固定两个合法主题A,T。强制当前X后沿**同一原σ**的真实尾负载记k_X(x)，它可随X改变，绝不识别相同计数但顺序不同的历史。

\[
d_i(X)=\sum_{x\in X}\frac1{b_x+1+k_X(x)},\quad
e_i(X)=u_i-d_i(X)=\Gamma_{h_i,X}\ge0,
\]
\[
K_i(Y,X)=\sum_{x\in Y}\frac1{b_x+1+\mathbf1_{x\in X}+k_X(x)}.
\]

K保强制根X，另加一单位静态query Y；不是删当前槽矩阵或m+1人SPE。

定义有符号的对称差响应债

\[
\begin{aligned}
E_i(A,T)=&\sum_{x\in A\setminus T}
\left[\frac1{b_x+1+k_T(x)}-\frac1{b_x+1+k_A(x)}\right]\\
&+\sum_{x\in T\setminus A}
\left[\frac1{b_x+1+k_A(x)}-\frac1{b_x+1+k_T(x)}\right],
\end{aligned}
\]

及非负的交集额外槽信用

\[
J_i(A,T)=\sum_{x\in A\cap T}\left[
\frac1{(b_x+1+k_A(x))(b_x+2+k_A(x))}
+\frac1{(b_x+1+k_T(x))(b_x+2+k_T(x))}\right]\ge0.
\]

则

\[
\boxed{K_i(T,A)+K_i(A,T)-2u_i
=E_i(A,T)-J_i(A,T)-e_i(A)-e_i(T).}\tag{P}
\]

## 四种会员位证明及空主题

先证明不含actual u的中间式

\[
K_i(T,A)+K_i(A,T)-d_i(A)-d_i(T)=E_i-J_i.\tag{R}
\]

客户不在A∪T时两边零；只在A时系数恰1/(b+1+k_T)−1/(b+1+k_A)，只在T时反向；同时在二者时每枝有1/(q+1)−1/q=−1/[q(q+1)]，得−J。再代d_i(A)+d_i(T)=2u_i−e_i(A)−e_i(T)，得P。**四种会员位只直接核R**；P里的A∪T外客户仍可经u_i和e_i出现，只有这些项代入后精确相消，不能先称全零。

A=T时E0，P给对角2K_i(A,A)≤2u_i；不支付不同主题。A或T为空，相关集合求和为空，但e_i(empty)=u_i必须留；二者都空时P左右皆−2u_i，正是两条空根IC松弛。末位k_X全0，E0；所有分母至少1，零客户时全部0。弱最优与任意平局无须修改。

## 固定对的跨位置未付预算

对同一A,T沿actual路径求和，用Σu_i=W，

\[
\sum_i[K_i(T,A)+K_i(A,T)]\le2W\tag{PW?}
\]

恰等价

\[
\sum_iE_i(A,T)\le\sum_iJ_i(A,T)+\sum_i[e_i(A)+e_i(T)].\tag{B?}
\]

右IC项是系数一的非负真实行组合，交集池逐客非负；尚无左E一般全路径上界。它不是PW证明、新福利下界或全树非负流。J是**这一固定主题对**的一份信用，不能在不同对分别领到后免费相加。

若PW对每对A,T成立，独立A,T~p平均，两项K均值都是pᵀK_i p，故2Σ_i pᵀK_i p≤2W，即FTA。此处因子二不可遗漏；目录大小不受主题对数固定。反向FTA不要求每对cross都≤2W，对角余量可以支付cross，故PW是较强充分式。FTA如何推出静态安全/half、pooled Mpath以及为何个体Mfull反例不传它，见[完整菜单净账](完整真实菜单的逐尾稀释与额外槽信用--引理.md)；本源review并未认证这个尚未付的一般前提。

## 已证末位BR接口给的更强晚位边界

这是本次读全后与[真实末回复PAIR](末位真实回复推送的锐曲率与双分支式--引理.md)的知情解析比较，不倒填原1994B独审范围。恰一名后继时，R=σ末回复(A)、S=σ末回复(T)，均是各自真实节点BR。记
\(U_b(X,Y)=\sum_{x\in X}1/[b_x+1+\mathbf1_Y(x)]\)。binary会员位直接展开得

\[
\boxed{E_i(A,T)=-\{[U_b(R,A)-U_b(S,A)]
+[U_b(S,T)-U_b(R,T)]\}\le0.\tag{LAST-BR}
\]

两方括号分别由A节点的R最佳、T节点的S最佳而非负。证明也可用w_x=1/[(b_x+1)(b_x+2)]：E=Σ_x(1_R−1_S)(1_A−1_T)w_x，括号和为其负值。即使R/S跨history不同，另一个仍是当前目录内合法偏离，不曾把它搬成别枝规定回复。

末位则E=0。因此任意m，最后两个actual位置不产生正E债；m1或m2时全路径PW已由这些边界与P得到。更早位置（至少两个交互后继）仍缺付款，不能把晚位非正性外推。尤其不能删e后试更强总去相关，或单向Σ_iK_i(T,A)≤W；下面同一真实族明确显示反向和IC信用为何不能删。

## 71客户族：单向超W与对称安全同时成立

使用[唯一最优遗漏完整SPE族](../反例/唯一最优组合的全遗漏支付--反例.md)，m2、六主题A,B,T,Q,R,S、整数k≥3，12类单位客户，actualAB，a=|A|=6k−2、b=|B|=|T|=7k−2，W=a+b=13k−4。A与B/T不交，B∩T只有1客，A∩R有2k客；真实首T后末回复R，首A后末回复B。canonical全参数证明已保全部七决策节点，不新跑原证书。

固定row T / forced root A，第一actual位置完整列AB，第二actual位置过去A后强制A的完整列AA；反向row A / forced root T，则列TR和AT。逐客户直接算

| actual位置 | K_i(T,A) | K_i(A,T) |
|---|---:|---:|
| 1 | b−1/2=7k−5/2 | a−k=5k−2 |
| 2 | b=7k−2 | a/2=3k−1 |
| 和 | 14k−9/2 | 8k−3 |

第一行T/B的唯一交客在AB列被B覆盖，query由1降1/2；反向A/R的2k交客在TR列降k。末位强制AA不再要求它最佳，只是原完整策略中的合法单方偏离；其大IC松弛不能删除。

单向和−W=k−1/2>0，故单向cap确失败。对称和为22k−15/2，而

\[
2W-\sum_i[K_i(T,A)+K_i(A,T)]=4k-1/2>0.
\]

k3为71客户，单向75/2>35，反向21，对称和117/2<70，余23/2。更细地，E_1=−1/2是两BR松弛负和、J_1=J_2=0（A∩T空）；根两e均0，末位e_2(A)=b−a/2=4k−1、e_2(T)=0，合P正好给该余量。它没有反PW/FTA/half，反而具体展示相反方向与真实IC信用。

同族唯一最优O=T∪Q，k3时(W,OPT,I,遗漏,actual在O外)=(35,38,2,36,33)，所以gross遗漏36>W却net gap只有3。不能把单向菜单失败、gross遗漏助手失败和对称预算未证混成同一命题。

本五主源均MD，本批原入口/规范solver/LP/新参数扫描0；上表是已证同族的解析代入，非新SPE穷举或旧审计重演。所有已有运行和发现归属不改，原文和新比较的作用见[证据目录](../../tools/evidence/symmetric-query-gap-and-review-primary/README.md)。
