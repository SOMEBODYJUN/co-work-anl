---
id: customer-attraction/natural-capture-routing-bellman-prices-and-hall-cancellation
kind: algorithm
type_tag: 算法
title: 自然捕获路由的Bellman价格与Hall取消
status: exact-fixed-instance-routing-and-cancellation-optimization; universal-price-budget-open
truth_status: Bellman-and-correct-Hall-layer-representations-proved; no-total-cost-at-most-W-theorem
review_level: full-author-and-supplement-reading; exact-bare-versus-fixed-delta-comparison; analytic-reconstruction-no-new-execution
scope: 固定完整SPE、最优元组及owner；actual-prefix query、当前吸收固定的自然captured-mass路由；裸Hall或指定逐客户delta残余网络分别计算
summary: 单客户最小整行采购费满足严格角色Bellman，全部来源共享同一最优规则且价≥1。裸Hall取消用r_H层积分；保局部delta时必须改用a−r_delta残余层积分，不能将裸最优取消与SOURCE-NET预付拼接。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round5/rank/incoming_density_diagonal_ledger.md#6
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round5/rank/incoming_density_diagonal_ledger.md#6
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round5/dynamic/review_density_ledger_supplement.md#2-4
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round4/shared/net_dynamic_rank.md#2-4
---

# 自然捕获路由的Bellman价格与Hall取消

## 固定同一游戏、真实query与允许的选择

固定[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)的一份完整纯SPE $\sigma$、实际叶$Z$、覆盖$C$、实际收益$u_i$、福利$W$。客户单位且有限，目录有限非空，人数$m\ge1$，空主题/重复/零客户及全部离轨平局保留。固定最优$m$主题元组$T$与owner分块$O=\bigsqcup_iQ_i$、$Q_i\subseteq T_i$；$R=O\setminus C,I=O\cap C,G=C\setminus O$。

query $s=(i,a)$的实际前缀真实完成为$B_s=\operatorname{finish}_\sigma(Z_{<i},a)$，$D_s=u_i(B_s)$。对$x\in R\cap a$，$c_s(x)=1+|F_s(x)|$，$F_s(x)=\{j>i:x\in B_{s,j}\}$。只允许[自然重分配定理](../定理/自然重分配的入密度共同对角账--定理.md)的路由：每单位到达当前固定吸收$1/c_s(x)$，其余比例$(c_s-1)/c_s$在这些真实future coverer间任意分配，进入规定动作状态$(j,B_{s,j})$，保持真父历史。不能改当前吸收、原策略或输入客户价值。

所有query的单位吸收统一乘完整IC系数$w_s=A_s/D_s$，费用是$u_iw_s$。正输入的$a$含$x$，所以$D_s>0$且完整SPE给$u_i\ge D_s$。不被触达的零收益状态可以省略，不定义零分母价格。多个来源和客户合并后仍只有同一query的一条完整IC系数。

## Bellman既给下界又可同时达到

令$V_s(x)$为单位$x$到达$s$后，此自然重分配族中的最小**实际整行采购总费**。其当前费是$u_i/[D_sc_s(x)]$；固定当前query以后只需选择captured部分去哪个真实child。严格角色增加给有限逆推：

\[
\boxed{V_s(x)=\frac{u_i}{D_sc_s(x)}
+\frac{c_s(x)-1}{c_s(x)}\min_{j\in F_s(x)}V_{(j,B_{s,j})}(x).}
\tag{BELLMAN}
\]

$c_s=1$时第二项为0，不取空集最小值。任意分配都至少支付这些child价的最小值；将全部captured质量送到一个最小child便达到。固定每个$(s,x)$的一项argmin，在任何父来源、任何非负源量下都使用该同一规则，因而不是给不同来源挑不可兼容的各自最优解。

承重条件是这里没有跨客户或跨来源的共享容量限制，且成本对输入密度线性。每个客户规则可同时固定，合流费用是各分量费用和；最后的IC仍是合并后的唯一$A_s/D_s$，不是逐客户重权IC。若后来附加逐角色共同钱包或源间容量，必须另证优化的可兼容性，不能直接沿用此分离最小化。

由$u_i/D_s\ge1$严格逆角色归纳，$c_s=1$时$V_s\ge1$，否则

\[
V_s(x)\ge1/c_s+(c_s-1)/c_s=1.
\]

初始化价$v_x=V_{(o(x),T_{o(x)})}(x)$，于是对任意残源$\rho_x$，同一最优自然规则的成本恰为$\sum_x\rho_xv_x$。原等份路由是可选规则之一，故这一固定元组/owner/来源下最小价不增；不声称每个$H,T,\mathrm{COV},L$分别单调或总费已经$\le W$。

## 裸actual Hall取消的精确网络

本节的$\Gamma$**不含额外指定的局部delta下界**。令$g_i=u_i(G)$、$g=|G|=\sum g_i$。在角色图上，source到$i$容量$g_i$；每个$x\in I$从owner $o(x)$向其每个非owner实际coverer$j$加容量$1/c_Z(x)$。每个$x\in R$在其owner处有一个容量1的独立终端。记跨角色割容量为$c_I(U,U^c)$，$Q(U)=\bigcup_{i\in U}Q_i$。

所有G源可同时送满。理由是最优$T$的合法替换：用actual主题替换角色集U的比较槽，新增的G客户不多于丢失的O客户。丢失客户的owner在U且未被actual U覆盖；R贡献至多$|R\cap Q(U)|$，I中每个这种客户的全部实际coverer在$U^c$，恰供一单位出割。又$g(U)$不超过actual U覆盖的G客户数，所以

\[
g(U)\le |R\cap Q(U)|+c_I(U,U^c).
\]

这是全部source割条件。对$S\subseteq R$只开放S终端，最大流/最小割的rank为

\[
r_H(S)=\min_{U\subseteq[m]}
\{g(U^c)+c_I(U,U^c)+|S\cap Q(U)|\}.
\tag{RANK}
\]

$r_H(\varnothing)=0$、单调、$r_H(R)=g$、$r_H(S)\le\min(g,|S|)$。这是可分数容量的多态体rank，不将分数客户取消误叫整数matroid基。

其子模性可直接验：令$f(U)=g(U^c)+c_I(U,U^c)$，有向cut加模函数满足子模式。取S、T的最小割$U_S,U_T$，逐客户有

\[
|S\cap Q(U_S)|+|T\cap Q(U_T)|
\ge |(S\cup T)\cap Q(U_S\cap U_T)|
+|(S\cap T)\cap Q(U_S\cup U_T)|.
\]

加$f$的子模式，再用交/并割作为两个rank的候选，即得$r_H(S)+r_H(T)\ge r_H(S\cup T)+r_H(S\cap T)$。

给定非负终端需求$\gamma$可实现当且仅当$\gamma(S)\le r_H(S)$对所有S成立。必要性取流向S的子流；充分性把终端容量改成$\gamma_x$，对每个角色割U取$S=R\setminus Q(U)$，由$\gamma(S)\le r_H(S)\le f(U)$得全部sink可饱和。单点rank自动给$\gamma_x\le1$。因此完整裸取消集合是

\[
\Gamma=\{\gamma\ge0:\gamma(S)\le r_H(S)\ \forall S,\ \gamma(R)=g\}.
\tag{BASE}
\]

## 同一套价格上的共同最优取消

把$v_x$降序排为$v_1\ge\cdots\ge v_d\ge0$，$S_k=\{x_1,\ldots,x_k\}$。取

\[
\gamma_{x_k}=r_H(S_k)-r_H(S_{k-1}).
\]

单调性给非负，总和g；对子集A，子模边际递减使上述增量对$x_k\in A$不超过$r_H(A\cap S_k)-r_H(A\cap S_{k-1})$，故$\gamma(A)\le r_H(A)$。因此同一个greedy取消同时饱和全部价格前缀。其它可行取消的每个前缀不超过rank，分层相加即得

\[
\boxed{\min_{\gamma\in\Gamma}\sum_x(1-\gamma_x)v_x
=\int_0^\infty\bigl(|S_t|-r_H(S_t)\bigr)\,dt,\quad
S_t=\{x:v_x\ge t\}.}
\tag{HALL-TOTAL}
\]

这是同一元组/owner、同一Bellman规则和同一个取消向量的共同最优，不是每个价格层各领一份G。$v_x\ge1$时最低单位层恰$|R|-g=\mathrm{OPT}-W$；额外层仍需支付。上式没有证明积分$\le W$。

## 保SOURCE-NET局部delta须换残余rank

若预先固定逐客户$0\le\delta_x\le1$，每owner $\delta_i=\sum_{x\in R\cap Q_i}\delta_x\le g_i$，可先直接把$\delta_x$从owner source预送其终端。残余源$g'_i=g_i-\delta_i$、终端库存$a_x=1-\delta_x$，I边不变。其rank为

\[
r_\delta(S)=\min_U\{g'(U^c)+c_I(U,U^c)+a(S\cap Q(U))\},
\quad r_\delta(R)=g-\delta(R).
\]

最后等式因每个完整割的source/库存总计恰同减$\delta(R)$。加权的同一子模/greedy证明适用，完整取消为$\gamma=\delta+z$，最小残费正确是

\[
\boxed{\min_{\gamma\in\Gamma,\ \gamma\ge\delta}
\sum_x(1-\gamma_x)v_x
=\int_0^\infty\bigl(a(S_t)-r_\delta(S_t)\bigr)dt.}
\tag{DELTA-TOTAL}
\]

不能保局部delta预付却继续套裸HALL-TOTAL的最优值。固定逐客户delta是这里的精确版本；未将所有可能的owner总下界或重新选择delta混作同一个可行集。

特别当$\delta_i=\min(g_i,|R\cap Q_i|)$时，SOURCE-NET原预付可保留：若$g_i$较小，$\gamma_i\ge g_i$使$\eta_i=u_i(I)+\gamma_i\ge u_i$，而source采购费至多$u_i$；若$g_i$较大，本owner R全取消、source费用0。自然recipient重分配不改source当前吸收，所以这个**同一delta/同一取消**的论证不受影响。裸最优$\gamma$则未必满足delta，不能拼接两者的好处。

## 证据身份、边界与仍需新关系

主长稿第6节和6038B补审都完整实读；后者特别指出裸$\Gamma$与保delta残余版本的区别。为使本页自足，旁读并保全10812B`net_dynamic_rank.md`的rank/cut/greedy证明，其完整定位在[related清单](../../tools/evidence/density-ledger-reviews-primary/related-source-manifest.json)，本批不替该源提交done。

算法在已给定真实query菜单上有限逆推并做有限最大流/greedy；本批五主源均Markdown，没有实现此优化的新程序，不声称此次运行了Bellman、任意recipient家族或Hall最优取消。前批实际程序只核固定等份/固定rho=1，其[有限边界](../计算/自然入流密度协方差与共同对角账的精确回归--计算.md)不随本解析扩张。

零源略去，空主题无正状态，$c=1$不取空min，价格相等任意greedy平局不影响最优值；R空时g=0、费用0。尚未证明任一最优元组/owner的上述最小总费总不超过W；增加逐角色cap也不由本分离优化免费满足。[自由trim候选](../候选/自由删源总价与半覆盖的充分接口--候选.md)是更宽、须放弃旧逐行钱包的充分接口，不是这里Hall网络已经支付的结论。
