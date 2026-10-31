---
id: customer-attraction/random-rank-joint-query-inventory-and-worldwise-hall-cancellation
kind: theorem
type_tag: 定理
title: 随机排序的联合查询库存与逐世界Hall取消
status: worldwise-integer-cancellation-and-mean-capacities-proved; whole-IC-budget-open
truth_status: all-cut-token-compatibility-and-random-net-inventory-proved; no-general-source-net-inheritance
review_level: full-main-and-readme-reading; historical-statement-first-internal-cut-reconstruction; one-finite-prefer-I-run
scope: 任意有限单位客户共同目录、任意m≥1及完整有序历史纯SPE；固定最优T/owner/actual叶；共同无并列随机priority
summary: 每个实际G客户给其赢家整单位source，owner缺失客户给赢家error边或真实query-token sink，全部HYB割保证逐world整数取消G枚R/I-query token。均值是Hall-B容量，随机赢家收入仍不能替原IC固定u。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round4/mixed/rankwise_joint_hall.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round4/mixed/rankwise_joint_hall.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round4/mixed/README.md
---

# 随机排序的联合查询库存与逐世界Hall取消

## 固定原模型和同一个排序世界

采用[完整历史共同目录模型](../定义/共同目录完整历史模型--定义.md)：有限单位客户、非空有限目录、任意$m\ge1$，保空主题、重复动作、零客户和所有有序历史任意平局。固定原纯SPE $\sigma$、actual叶Z、覆盖C、利润$u_i$、福利W；固定最优合法T、并集O及全局owner分块$Q_i\subseteq T_i$。令$R=O\setminus C,I=O\cap C,G=C\setminus O$，$J_x=\{i:x\in Z_i\}$、$I^-=\{x\in I:o(x)\notin J_x\}$。

全角色共用无并列priority U，可取iid连续均匀变量或等概率的$m!$个角色排列。priority无并列不限制原SPE动作平局。actual覆盖客户的winner $w_U(x)$是其actual coverer中U最高者。

query始终为原actual前缀强制合法主题a后沿同一$\sigma$完成，利润$D_i(a)$。owner-threshold token只沿active真实future coverer严格增加**时间角色**，没有active future时整单位吸收；在每个新state重置actual前缀。这里的金融coupon图按priority定向，不能与该时间有向查询图认作同一条路径。

## 每个world中实际存在的单位库存

对每个owner实际未覆盖的O客户x（即$R\cup I^-$）：

- 若$J_x\ne\varnothing$且$U_{w_U(x)}>U_{o(x)}$，放owner到winner的容量1角色边；
- 否则放owner到客户独立query终端的容量1边。

第二种恰是该客户query token存在的事件：R恒有token；I^-只有owner高于全部actual coverer时有token。owner已实际覆盖的I不建B边或sink。B角色边严格升U，故无角色环。

每个$y\in G$的整单位source给其winner，记角色source为$g_i(U)$。每world $\sum_ig_i(U)=|G|$，但$g_i(U)$一般不等actual等分利润$g_i=u_i(G)$；均值才满足$E g_i(U)=g_i$。

## 全部角色割保证逐world整数取消

固定world和任意角色集L，定义

\[
M(L)=\{x\in O:o(x)\in L,\ J_x\cap L=\varnothing\}.
\]

[owner hybrid](最优归属的全子集调和运输与锚定隔离--定理.md)给actual G被L覆盖的客户数$\le|M(L)|$，而$g_U(L)$只数winner在L的G客户，至多该覆盖数。每个M客户owner在L、actual coverer全在外，且owner实际未覆盖；若它有高于owner的winner，coupon是出L的unit边，否则有query终端unit边。每客户恰给1出割，故

\[
cap_U(L)\ge |M(L)|\ge |G\cap\bigcup_{i\in L}Z_i|\ge g_U(L).
\]

超级源到角色容量$g_i(U)$，有限最大流最小割使全部G source同时饱和。容量整数，可取整数流；恰取消G枚**这个world真正存在**的R/I-query token。可以观察整个world、查询终点和价格后选任意可行流，不需要固定$\lambda/\kappa$均值换算。

这是每world cut证明，不把平均容量冒充点态容量；静态cut本身不需SPE。随后购买query的价格下界和资金比较才使用原完整SPE。

## 均值恰回到actual Hall-B

对$x\in I^-$，令$c=|J_x|$，owner不在J。每个actual coverer成为B出口的事件是它在$\{o\}\cup J$中最高，概率$1/(c+1)$，恰为actual owner-error份额。sink事件是owner最高，概率$\kappa_x=1/(c+1)$；R的sink恒1。source均值为actual G原等分利润。

因此期望B图正是[联合库存Hall-B](联合查询库存的Hall取消与初始化付款--定理.md)的source/角色error容量和missing-owner query库存。区别在于此处先用unit coupon证明点态可行，再取均值；不是在均值网络选一个随机$\lambda(U)$后仍套固定条件删除。

## 随机净库存与原IC的分界

将每个actual覆盖客户整1收入也给其winner，记$\widehat u_i(U)$，均值$u_i$、总和W，G source正是其G部分。若终端取消角色总量为$\lambda_i(U)$、角色流f，则

\[
\lambda_i+out_f(i)-in_f(i)=g_i(U),
\quad in_f(i)\le\widehat u_i(I;U),
\]

因为每条incoming边的目标正是该I客户的winner。随机净库存

\[
\widehat\eta_i(U)=\widehat u_i(I;U)+\lambda_i(U)\ge0,
\quad\sum_i\widehat\eta_i=W,
\quad E\widehat\eta_i=u_i(I)+E\lambda_i.
\]

它定位了同一个world的一份钱，未产生第二份I/G。原actual-prefix完整IC却是$D_i(a)\le u_i$，采购单价仍为固定$u_i/D_i(a)$；不能将$\widehat u_i(U)$替进原IC。它与query/取消事件相关，均值正确不足以恢复SOURCE-NET或row预算。[实际数值障碍](../障碍/随机赢家收入的逐世界激励替换--障碍.md)给$D=91>\widehat u_0=45$的同一证书world。

## 合法付款接口及尚未支付的费用

world剩余query token数为$|R|+N_I(U)-|G|$，其中$E N_I=\kappa^-:=\sum_{x\in I^-}1/(c_x^0+1)$。取消后先取期望吸收A，再给每个query唯一常数$w=A/D$；正A保证D正。完整SPE给

\[
|R|+\kappa^--|G|\le K:=\sum_{i,a}u_iA_{i,a}/D_i(a).
\]

若同一个owner、路线和取消选择能使$K\le W+\kappa^-$，减同一I-query新增源才得half。这个共同费用界未证。取消只给$0\le$保留$\le1$，故固定state吸收受未取消Beta/owner势边际控制；不能再乘平均残比例，不能将每state$w\le1$相加为row cap。

旧R-only自适应方案在**固定actual等分**Gamma上附局部owner总取消下界，因而另证SOURCE-NET；本unit赢家图没有该同一约束，不搬用它的预付。固定Hall-B的激活前lambda删除又是第三份合同，三者不各领一次G。精确比较与历史先验见[审查](../审查/排序联合取消的三种合同与两版证据--审查.md)。

R-only[单调投影](../算法/联合查询取消向遗漏客户取消的单调投影--算法.md)能在同世界将联合费减至少$N_I$，但仍以本未证费用界为前提，不额外产生预算。原5040B主稿及2514B README本批全文重新实读、核SHA；relay/credible全cut重构是源述内部身份，相关relay报告明确先从精确陈述重构，非无提示盲审、外审或新颖性认证。六人half未闭合，五人已有[独立定理](五人半覆盖--定理.md)。
