---
id: customer-attraction/fixed-capture-prices-hall-deficits-and-joint-payment-dual
kind: theorem
type_tag: 定理
title: 固定捕获价格的Hall缺额与共同付款对偶
status: exact-fixed-choice-representations-proved; universal-net-budget-open
truth_status: rank-base-greedy-total-deficit-dual-margin-proved; no-half-theorem
review_level: historical-nonblind-analytic-review-and-current-full-source-reconstruction
scope: 任意有限单位客户共同目录、任意人数和完整有序历史纯SPE；同一最优元组、归属、原查询菜单及固定线性捕获规则
summary: 实际取消量是Hall终端rank的base；固定whole-IC采购价格的最小总费是缺额层积分，逐角色共同付款是全非负价格支持函数判别。固定局部预取消时须使用残余rank与平移后的行差。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round4/shared/net_dynamic_rank.md#1-6
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round4/shared/net_dynamic_rank.md#1-6
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round4/credible/review_net_dynamic_rank.md#1-3
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-b6d636d360e14c11aeb4b76415ed422b/direction_review/continuation_general_scope/incoming_payment.md#五
---

# 固定捕获价格的Hall缺额与共同付款对偶

## 同一固定选择及真实采购价

采用[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)：有限单位客户、有限非空共同目录、任意$m\ge1$，每名单位权玩家观察全部有序历史选主题，终局客户在覆盖者间均分。固定原完整纯SPE $\sigma$、actual叶$Z$、覆盖$C$、利润$u_i$、福利$W=|C|$。固定一个最优有序$m$主题元组$T$及分析分割$O=\bigsqcup_iQ_i$、$Q_i\subseteq T_i$。空主题、重复动作、零客户及任意离轨平局保留；$Q_i$自身不必是合法行动。

记$R=O\setminus C,I=O\cap C,G=C\setminus O$，$I_i=u_i(I),g_i=u_i(G)$，$g=|G|$。从每个$x\in R$的owner $o(x)$合法查询$T_{o(x)}$注入单位源，采用一份预先固定、按源量非负线性的严格递增角色捕获规则。query $s=(i,a)$总是读取同一原策略的actual-prefix完成叶

\[
B_s=\operatorname{finish}_\sigma(Z_{<i},a),\quad D_s=u_i(B_s).
\]

总current吸收$A_s$只购买一次完整IC，系数$w_s=A_s/D_s$。正吸收保证$D_s>0$；$D_s=0$时没有正吸收，费用置零。将分子按来源拆分，定义$p_{ix}\ge0$为单位$x$源最终在角色$i$的实际采购费。于是

\[
K_i(\rho)=\sum_{x\in R}p_{ix}\rho_x,\quad
p_{ix}=0\ (i<o(x)),\quad v_x=\sum_ip_{ix}\ge1. \tag{PRICE}
\]

最后不等式由单位源全吸收及$u_i\ge D_s$得出。$p$是整行IC的来源线性分拆，**不是**逐客户另加的IC权重。它也不是[固定净券钱包](../候选/分数归属与实际净券的共同钱包--候选.md)列和为1的净需求$P$；本页列和$v_x$可以大于1。

## 实际Hall网络、rank及base

source到角色$i$容量$g_i$。每个$x\in I$从$o(x)$到其每个非owner actual覆盖者$j$有容量$1/c_Z(x)$；记角色割容量$c_I(J,J^c)$。每个$x\in R$在owner处有独立容量1的终端。令$Q(J)=\bigcup_{i\in J}Q_i$，交$R$的限制在公式中由$S\subseteq R$自动给出。

最优$T$的合法替换给$g(J)\le c_I(J,J^c)+|R\cap Q(J)|$，所以全部source能同时送满$g$；完整证明见[同时源付款](实际取消的同时源付款与入流余额--定理.md)。只开放$S\subseteq R$终端时，最大流最小割给

\[
r(S)=\min_{J\subseteq[m]}\{g(J^c)+c_I(J,J^c)+|S\cap Q(J)|\}. \tag{RANK}
\]

$r(\varnothing)=0$、单调、$r(R)=g$且$r(S)\le\min(g,|S|)$。令$f(J)=g(J^c)+c_I(J,J^c)$；有向cut加模函数$f$子模。取$S,T$的最小割$J_S,J_T$，逐客户验证

\[
|S\cap Q(J_S)|+|T\cap Q(J_T)|\ge
|(S\cup T)\cap Q(J_S\cap J_T)|+
|(S\cap T)\cap Q(J_S\cup J_T)|.
\]

与$f$的子模式相加，用两个交叉割分别上界$r(S\cup T),r(S\cap T)$，得$r$子模。

非负终端需求$\gamma$可实现，当且仅当$\gamma(S)\le r(S)$对所有$S$成立。必要性取流向$S$的子流；充分性把终端容量改为$\gamma_x$，任意角色割$J$所需条件是$\gamma(R\setminus Q(J))\le f(J)$，由$S=R\setminus Q(J)$及$r(S)\le f(J)$给出。单点rank自动给$\gamma_x\le1$。完整取消集合恰为紧凸base

\[
\Gamma=\{\gamma\ge0:\gamma(S)\le r(S)\ (S\subseteq R),\quad\gamma(R)=g\}. \tag{BASE}
\]

容量可以为分数，不能将其称为整数matroid基。原博弈客户仍为单位客户。

## 支持函数、总费及真正缺额

任取非负价格$z_x$，降序排列$z_1\ge\cdots\ge z_d\ge0$，$S_k=\{x_1,\ldots,x_k\}$、$z_{d+1}=0$。同一个向量

\[
\gamma_{x_k}=r(S_k)-r(S_{k-1})
\]

属于$\Gamma$：单调性给非负/总和$g$，子模边际递减对任意子集逐项相加给$\gamma(U)\le r(U)$。每个可行取消的价格前缀量都至多$r(S_k)$，故

\[
h_\Gamma(z):=\max_{\gamma\in\Gamma}z\cdot\gamma
=\sum_k(z_k-z_{k+1})r(S_k). \tag{GREEDY}
\]

取$z=v$，取消后$K_i=\sum_xp_{ix}(1-\gamma_x)$，得

\[
\min_{\gamma\in\Gamma}\sum_iK_i
=\int_0^\infty d_H(S_t)\,dt,\quad
d_H(S)=|S|-r(S),\quad S_t=\{x:v_x\ge t\}. \tag{TOTAL}
\]

将RANK中的$J$换成$L^c$，并使用$Q$分割$R$，得到全部方向均确定的缺额式

\[
d_H(S)=\max_{L\subseteq[m]}
\{|S\cap Q(L)|-g(L)-c_I(L^c,L)\}. \tag{DEFICIT}
\]

同一个greedy同时优化全部嵌套价格层；没有每层另领$G$。由于$v_x\ge1$，最低单位层给$d_H(R)=|R|-g=\mathrm{OPT}_m-W$，所以

\[
\min_\Gamma\sum_iK_i=\mathrm{OPT}_m-W+
\int_1^\infty d_H(S_t)\,dt.
\]

未证的总价桥是额外层积分$\le2W-\mathrm{OPT}_m$，等价于这份固定系统的最小采购费$\le W$。它可以强于half，因还支付本捕获规则的正IC税；本页没有证明该上界。

## 逐角色NET的共同对偶与精确margin

同一Hall取消的钱包为$\eta_i=I_i+\gamma_i$，其中$\gamma_i=\sum_{x:o(x)=i}\gamma_x$，总和$W$。置

\[
d_i=\sum_xp_{ix}-I_i,\qquad M_{ix}=p_{ix}+\mathbf1_{o(x)=i}.
\]

逐角色要求$K_i\le\eta_i$等价于$M\gamma\ge d$。紧凸$\Gamma$的线性像与上正交要求分离，给精确判别

\[
\exists\gamma\in\Gamma:\ M\gamma\ge d
\quad\Longleftrightarrow\quad
h_\Gamma(M^T\lambda)\ge\lambda\cdot d
\quad\text{对所有 }\lambda\ge0. \tag{NET-DUAL}
\]

必要性逐行非负加权；反向若不相交，向下闭的可满足行差域给一个非负分离法向量，违反右式。每个支持函数由GREEDY精确计算。不同$\lambda$的最大化器可以不同；所有方向通过后，凸分离才推出**一份**共同$\gamma$。

令$\Delta_m=\{\lambda\ge0:\sum\lambda_i=1\}$。两个紧凸集的双线性极小极大给

\[
\min_{\gamma\in\Gamma}\max_i(K_i-\eta_i)
=\max_{\lambda\in\Delta_m}
\{\lambda\cdot d-h_\Gamma(M^T\lambda)\}. \tag{MARGIN}
\]

$\lambda=\mathbf1$方向恰为TOTAL$\le W$，因为owner项总和为$g$且$\sum I_i+g=W$；逐角色NET需要全部非负方向，因此更强。外层还可共同选择最优$T$/owner，但不能交换外层与$\lambda$，把每个方向各自有利的owner拼成同一个见证。一个固定选择的严格margin仅否定该选择。

## 保指定局部预取消时，rank和行差都要平移

固定$0\le\delta_x\le1$，$\delta_i=\sum_{x:o(x)=i}\delta_x\le g_i$。先直送$\delta$，残余source $g'_i=g_i-\delta_i$、终端库存$a_x=1-\delta_x$，I边保持。每个完整割总容量同减$\delta(R)$，所以残余仍送满；其rank

\[
r_\delta(S)=\min_J\{g'(J^c)+c_I(J,J^c)+a(S\cap Q(J))\},\quad
r_\delta(R)=g-\delta(R).
\]

同一加权子模证明适用。写$\gamma=\delta+z$，$z$属于残余base$\Gamma_\delta^{res}$，则

\[
\min_{\gamma\in\Gamma,\gamma\ge\delta}\sum_xv_x(1-\gamma_x)
=\int_0^\infty[a(S_t)-r_\delta(S_t)]\,dt. \tag{DELTA-TOTAL}
\]

逐角色行差也必须改为

\[
d_i^\delta=\sum_xp_{ix}(1-\delta_x)-I_i-\delta_i,
\quad K_i-\eta_i=d_i^\delta-(Mz)_i.
\]

NET-DUAL/MARGIN用$\Gamma_\delta^{res},d^\delta$，$M$不变。等价地可在未平移的$\Gamma\cap\{\gamma\ge\delta\}$上使用原$d$。不能把残余base与原$d$混搭；也不能将裸$\Gamma$最低价附上另一局部$\delta$的SOURCE-NET预付。

## 证据、后续与边界

10812B作者稿和5141B审查全文取回核SHA。历史审查首次读取已含作者证明，是非盲解析核查；它核对RANK/BASE/GREEDY/TOTAL/DEFICIT/NET-DUAL/MARGIN和残余修正，不声称审了作者程序或动态预算。当前12142B一般审查的支持函数式以$\Gamma\cap\{\gamma\ge\delta\}$表述，与本页平移版本一致。精确先验及后续差别见[内部核读](../审查/固定价格取消与入流付款的内部核读--审查.md)。

[自然recipient Bellman](../算法/自然捕获路由的Bellman价格与Hall取消--算法.md)已保存同一rank/greedy的一个应用；本页保存原始整列采购价格、DEFICIT、全部角色价格、精确margin及残余行差，不把重复rank说成新的预算进展。[分数归属接口](../候选/分数归属捕获与共同激活付款接口--候选.md)进一步保留原稿§7—8。

空$R$时$g=0$、全部向量为空；$G=0$时base只有零取消；价格并列任意greedy平局，零价格不产生分母。有限表示没有紧凑输入多项式时间声明。本页未求解一般NET或六人half；五人half已有[独立定理](五人半覆盖--定理.md)。
