---
id: customer-attraction/owner-complete-hall-b-zero-flow-and-same-leaf-reservation
kind: lemma
type_tag: 引理
title: 归属完备角色的Hall-B零流与同叶预留
status: same-leaf-zero-flow-reservation-and-prefix-isolation-proved; cross-leaf-payment-open
summary: 任意可行Hall-B流必避开owner完备角色；将调和源裁为真实外部利润后预留全部O势边际，同叶与全最优前缀隔离不提供跨叶共同IC付款。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round3/relay/hall_owner_anchor_connection.md
---

# 归属完备角色的Hall-B零流与同叶预留

## 固定叶及Hall-B存在性的承重

有限单位客户、有限非空共同目录、任意m≥1；固定最优合法T、O及分割$Q_i\subseteq T_i$。固定任意合法完整叶B，不先要求为SPE。令$C_x=\{i:x\in B_i\}$、$c_x=|C_x|$，$E=\{x\in O:x\notin B_{o(x)}\}$。Hall-B仅为$x\in E$建owner到每个coverer及终点t的边，各容量$1/(c_x+1)$。$c_x=0$仅有单位终点；owner不在coverer中，无自环。source为
\[
 b_i^H=\sum_{y\in B_i\setminus O}H_{c_y}/c_y.
\]
终点是missing-owner价格，已覆盖O客户也可有终点，不能叫真实遗漏客户。

为自足说明全部割：对任意角色集J，在J内独立以p把Q替成B，其余保持Q，逐实现扩回合法T后最优性给
\[
 \sum_{y\notin O}[1-(1-p)^{c_y(J)}]
 \le\sum_{x\in E:o(x)\in J}p(1-p)^{c_x(J)}.
\]
除p并在(0,1)积分得到$\sum_{y\notin O}H_{c_y(J)}\le\sum_{x\in E:o(x)\in J}1/(1+c_x(J))$。因$H_c/c$随c递减，$b^H(J)\le\sum H_{c_y(J)}$。对右侧一客户写$d=c_x(J)$，出割容量是
\[
 \frac{1+c_x-d}{1+c_x}\ge\frac1{1+d},\quad
 \text{差}=\frac{d(c_x-d)}{(1+c_x)(1+d)}\ge0.
\]
所有割足够，有限最大流最小割给同时运输全部source的有理流，角色净流出$b_i^H$，可去循环为有限终点路径。角色边可逆时间，不是游戏行动链。这是既有[全子集调和运输](../定理/最优归属的全子集调和运输与锚定隔离--定理.md)的静态证明，未按客户重权原IC。

## owner完备强迫任意可行流零入零出

若$Q_i\subseteq B_i$，替换单槽i时没有O库存损失。其余Q扩回T仍合法，故$B_i\setminus O=\varnothing$；亦即HYB单点割左侧至多$|Q_i\setminus B_i|=0$。即使Q_i为空也成立。于是$b_i^H=0$；i的owner客户全不在E，故i没有角色出边或终点边。非负守恒强迫
\[
 out_i=0,\qquad in_i=0.
\]
结论对**任何**Hall-B可行流成立，不只是选得到一份好流；别的owner指向i的正容量也只能用零流。强制查询配对T_i时$B_i=T_i$，该角色可有覆盖其他owner的e信用，但其Hall-B入边仍必不用。

不能将任意流结论照搬到Hall-A：A也用owner在场客户，锚角色仍可能有出边。已有[普通利润联合资金](../定理/锚定最优主题的普通利润联合资金--定理.md)在锚并集A外另构残余A图，能**选择**避开A客户资源；这是不同的构图结论，不与本引理矛盾。

## 同叶捕获与预留预算

在查询叶$B_i=T_i$，每个$x\in Q_i$的当前查询份额1/c与其他coverer合计$(c-1)/c$，属于owner在场的非owner插入信用。Hall-B仅用owner不在场E，故这些客户标签的容量不重叠；更一般全部owner在场边与E图不重叠。这只是一叶的容量相容，不能把同一客户在不同互斥叶各花一次。

将source降为真实外部利润$b_i^G=\sum_{y\in B_i\setminus O}1/c_y$。因$H_c\ge1$，把B流去循环、分解为源到终点路径并裁去多余源流，得到运输$b_i^G$的新流。用[owner势分解](../定理/共用指数角色钟的归属势表示与合法激励范围--定理.md)记$\ell_i^Q(B;O)$为只在O上modified边际，$e_i^E$为owner不在场客户给i的误差份额。incoming用这些客户各$1/(c+1)$容量，因此
\[
 \boxed{role\!out_i+sink_i=b_i^G+in_i
 \le b_i^G+e_i^E\le u_i(B)-\ell_i^Q(B;O).}
\]
保留了O上全部modified边际，且owner在场的e也未消费。若B是actual叶，定义$\kappa=\sum_i\ell_i^Q(B;O)$，这份预留正是κ，不是额外一份I福利。原调和$b_i^H$一般大于单位利润，未经裁源不能直接代入IC钱包。

对已覆盖$x\in E$，终点容量$1/(c+1)$等于coverer的modified边际合计$c\cdot1/[c(c+1)]$。可把终点分接到各coverer、每边$1/[c(c+1)]$；加上原误差边$1/(c+1)$恰为$1/c$真实份额。$c=0$仍为单位终点。要成为完整Hall-A还须加入原本不用的owner在场非owner边；A/B不能当两套独立货币。

## 最优全前缀与历史边界

在同一原完整策略$\sigma$强制完整最优前缀$(T_1,\ldots,T_k)$后立即沿原策略的真实rollout中，所有$j\le k$完备，故Hall-B全部source、已用角色边和终点均支撑于未来角色$k+1,\ldots,m$，k=m时皆空。没有删祖先、匿名计数或要求后继避开背景。未来内部仍可从较晚角色流到较早未来角色。

只有当前i查询T_i、此前仍走actual前缀时，其他祖先可能不完备，不能自动套整个前缀隔离。任意合法B的静态利润也不自动等于某过去节点规定完成叶的IC左端。跨不同真实rollout还需共同选择流，使missing-owner价格、严格递增捕获和完整原IC系数相容，实际I/G只花一次。主源ROLL中的$\sum_i(e_i^-+D_i)$仍未支付；本引理没有控制其总量。

## 历史身份与本批证据

5599B完整原文在[原件清单](../../tools/evidence/relay-following-actual-primary/source-manifest.json)。原文记relay提出零流陈述及证明，credible收到二者后独立重构；明确不是严格盲审。A/B全割已由root/shared重构，本批核其数学与现有两份正式定理，没有重跑先前A/B程序，也没有把旧有限图报告冒作新证据。空客户、空Q、重复主题、零覆盖及r=0剩余前缀均按上述零式处理。六人half和一般跨叶incoming尚未由这些同叶正组件闭合。
