---
id: "customer-attraction/credible-endpoint-mean-cap-domains-and-slack-credit"
kind: "lemma"
type_tag: "引理"
title: "可信端点的逐叶、逐行动及全行均值cap与松弛信用"
status: "proved-domain-duality-and-balance; covariance-payment-unresolved"
summary: "实际行动端点固定下区分逐叶纯威胁重选与两种分析彩票；全行均值cap对原σ源给G=ΣμI+R≥0，未支付剩余协方差。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round12/tree/mean_cap_credible_shadow_working.md"
---

# 固定原均衡及三个不同的cap域

采用[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)：有限单位客户、有限非空共同目录\(\mathcal S\)、任意\(m\ge1\)名单位提供者，保空主题、重复、零客户和任意离轨平局。固定一份完整有序历史纯SPE \(\sigma\)，实际路径\(B\)、实际收益\(u_i\)及\(W=\sum_i u_i\)。行\(i\)的实际前缀为\(h_i=B_{<i}\)，实际行动为\(a_i=B_i\)。

对\(A\ne a_i\)，令\(E_i(A)\)为在精确历史\((h_i,A)\)后的所有完整纯孩子SPE见证及其终局。见证\(e\)给进入者收益\(d_i(A,e)\)及删除**同一角色\(i\)**后的负载\(\ell_i(A,e)\)。相同终局可保留不同策略见证标签；后续使用某见证的IC时必须沿该见证自己的真实偏离叶。对\(A=a_i\)，仅允许原实际终局，其\(d_i=u_i\)、\(\ell_i=c(B)-\mathbf1_{a_i}\)。游戏有限，故见证标签集合可取为有限集合。

逐叶cap先删掉\(d_i>u_i\)的见证，再凸化其负载。逐点选择这些剩余见证时，所有\((i,A\ne a_i)\)都是原实际路径的不同**首次偏离**孩子，子树互不相交；将各见证独立拼回并保留实际路径，仍得同一\(B,u,W\)的完整纯SPE。这是[可信续局菜单](../../tools/evidence/credible-cap-fixedpoint-primary/original/research/current/customer_attraction/credible_continuations.md)的既有拼接机制。凸组合本身不因此成为可执行的SPE。

两个更大的分析域为
\[
D_i^{\rm action}(A)=\{E_q\ell_i(A,e):q\in\Delta(E_i(A)),\ E_qd_i(A,e)\le u_i\},
\]
\[
K_{\rm action}=\frac1m\sum_i\operatorname{conv}
                    \bigcup_A D_i^{\rm action}(A),
\]
\[
D_i^{\rm global}=\{E_q\ell_i(A,e):q\in\Delta(\{(A,e)\}),\ E_qd_i(A,e)\le u_i\},
\qquad K_{\rm global}=\frac1m\sum_iD_i^{\rm global}.
\]
每行彩票归一。实际行动端点在两域均保持单点。原\(\sigma\)在每个强制主题后的真实孩子SPE都有\(d_i^0(A)\le u_i\)，故所有条件域非空。它们是紧凸多面体；若\(K_{\rm original}\)表示仅用原\(\sigma\)各强制菜单的共享域，则
\[
K_{\rm original}\subseteq K_{\rm leafwise}\subseteq
K_{\rm action}\subseteq K_{\rm global}.
\tag{DOM}
\]
每个负载均可表示为总提供者质量\(m-1\)的合法目录分数负载；空主题允许其客户坐标总和为零，质量并非客户负载坐标之和。

均值cap可在同一彩票内用低收益叶抵消高收益叶，因此不保证每个端点满足进入IC，也不声称产生原游戏新的纯SPE或无附加机制的混合SPE。全行cap还可跨不同\(A\)抵消，不推出任何逐行动条件cap。独立背景彩票与原查询源的量词必须分别保留。

# 逐行动价格与条件查询源

固定非负客户shadow \(w\)。有限LP的强对偶给
\[
\max_{q:E_qd\le u_i}E_q(w\cdot\ell)
=\min_{\lambda\ge0}\{\lambda u_i+
                \max_e(w\cdot\ell_e-\lambda d_e)\}.
\tag{APRICE}
\]
对最优\(q,\lambda\)，互补性和所有列的对偶约束给
\[
\lambda(u_i-E_qd)=0,\qquad
w\cdot(\ell_e-E_q\ell)\le\lambda(d_e-E_qd)
\quad\text{对每个可信见证 }e.
\]
此结论适用于先均值约束后优化的域；把\(d>u_i\)的列预先删除，不自动得到能支持所有未删前端点的同一个标量价格。式子没有界定\(\lambda\)，也没有从\(W\)另行支付\(\lambda u_i\)。

在\(K_{\rm action}\)的共享鞍点令\(t=(1+L^*)^{-1}\)、\(\rho_x=\Pr_p[x\in A]\)、\(w=\rho t^2\)。分解\(L^*\)时，每个正权行动内的彩票必最大化对应条件域的\(w\cdot\ell\)：否则替换它会违反整体一阶最优性。保留这些彩票，对未用行动另选条件shadow最大化彩票，就得到每个\(A\)都有明确\(q_{iA}\)、\(E_{q_{iA}}d_i\le u_i\)的查询源。此时\(I_i=u_i-E_{A\sim p,e\sim q_{iA}}d_i\ge0\)来自条件均值cap，并非每个可能超cap的端点都满足原进入IC。倒数展开必须在每个端点上计算后取期望；用平均负载的倒数替代平均倒数会丢失曲率余量。

# 全行域保留原查询源的精确正信用

以下仅用\(K_{\rm global}\)，查询源始终为原\(\sigma\)的\(\ell_i^0(A),d_i^0(A)\)，不改用所选背景彩票。连续凸负载域和有限查询单纯形给共享minimax鞍点\((p,L^*)\)。置
\[
F_p(L)=\sum_x\frac{\rho_x}{1+L_x},\quad
t_x=(1+L_x^*)^{-1},\quad w_x=\rho_xt_x^2,\quad
\gamma=F_p(L^*).
\]
所有合法主题\(T\)满足\(g_t(T)=\sum_{x\in T}t_x\le\gamma\)，\(p\)支持上的主题取等号。负载最小化的梯度是\(-w\)，因此\(L^*\)最大化\(w\cdot L\)。在任意实现\(L^*=m^{-1}\sum_i\bar\ell_i\)中，每行\(\bar\ell_i\)最大化自己的\(D_i^{\rm global}\)，值记\(H_i\)，于是
\[
\sum_iH_i=mw\cdot L^*
=m\left(\gamma-\sum_x\rho_xt_x^2\right).
\]
每行有限LP对偶有\(\mu_i\ge0\)、\(\eta_i\in\mathbb R\)：
\[
H_i=\eta_i+\mu_i u_i,\qquad
\eta_i+\mu_i d_i(A,e)\ge w\cdot\ell_i(A,e)
\quad\text{对每个允许的可信端点。}
\tag{GDUAL}
\]
不要求\(\eta_i\ge0\)或\(\mu_i\le1\)。列可以逐叶超过cap，因cap只约束彩票均值。

原查询列均在该域内，故
\[
R_i(A)=\eta_i+\mu_i d_i^0(A)-w\cdot\ell_i^0(A)\ge0,
\qquad I_i=u_i-E_pd_i^0(A)\ge0.
\]
将它代入唯一的共享KKT差额，得到
\[
\boxed{G:=\sum_i[H_i-E_p(w\cdot\ell_i^0(A))]
=\sum_i\mu_i I_i+\sum_iE_pR_i(A)\ge0.}
\tag{CAP-SLACK}
\]
高\(\mu_i\)在这里乘的是原完整查询IC松弛，符号为正；无需另外证明\(\sum_i\mu_i u_i\le W\)。右端是同一\(G\)的分拆，不能与未拆的\(G\)重复相加。

# 倒数主账及尚未证明的付款

定义
\[
C=\sum_iE_p\sum_{x\in A}t_x^2(\ell_i^0(A)_x-L_x^*),
\quad
D=\sum_iE_p\sum_{x\in A}
\frac{t_x^2(\ell_i^0(A)_x-L_x^*)^2}{1+\ell_i^0(A)_x},
\]
\[
\operatorname{Cov}=\sum_{i,x}t_x^2
\operatorname{Cov}_{A\sim p}(\mathbf1_{x\in A},\ell_i^0(A)_x).
\]
逐客户恒等式
\[
\frac1{1+\ell}=t-t^2(\ell-L^*)+
                    \frac{t^2(\ell-L^*)^2}{1+\ell}
\]
给\(W-m\gamma=\sum_iI_i-C+D\)。中心化源指示给\(C=\operatorname{Cov}-G\)，故
\[
\boxed{W-m\gamma=\sum_i(1+\mu_i)I_i
                 +\sum_iE_pR_i(A)+D-\operatorname{Cov}.}
\tag{GBAL}
\]
分母始终是原删除槽源\(1+\ell_i^0\)，没有把独立背景见证当成该原源。

目录合法性与主题价格上界给
\[
Q_{\rm stat}=(m-1)\gamma-\sum_xL_x^*t_x\ge0,
\qquad\operatorname{OPT}_m\le(2m-1)\gamma-Q_{\rm stat}.
\]
后式逐客户用\(\mathbf1_{c_x^{\rm opt}>0}\le(c_x^{\rm opt}+L_x^*)/(1+L_x^*)\)，再将最优\(m\)主题各自价格以\(\gamma\)上界。因此仍待证明的足够金额为
\[
\operatorname{Cov}\le\sum_i(1+\mu_i)I_i+\sum_iE_pR_i+D
                      +\frac{\gamma+Q_{\rm stat}}2.
\tag{PAY?}
\]
CAP-SLACK未证明(PAY?)。在某可信见证内让未来一人偏离后所得叶，其偏离者可能并非最佳回复，因而该叶未必是同一进入历史后的完整孩子SPE端点；不能直接套用(GDUAL)。需另证可信闭包，或显式改变为[raw均值门槛域](逐历史均值门槛的受限实际标签域--引理.md)，并承担新增门槛成本。

# 比较、审查和可接续范围

本源7695字节全文读取；与原可信菜单、全槽对偶、真实重放、规范门槛和后续weighted-credit/组件审查逐项比较。原稿记载credible分支平行独立推导均值cap，随后内部核对第1及3–5节；matching内部核第1–5节。这些历史内部检查未认证协方差付款，也不构成本批盲审、外审或新颖性声明。本批按公式重构，不运行别的有限搜索来代替全输入证明。原件、比较稿与逐语义去向见[资源说明](../../tools/evidence/credible-cap-fixedpoint-primary/README.md)。

与[完整槽原源范数账](完整槽均值cap的原源范数账与付款接口--引理.md)相比，本页背景质量为\(m-1\)、静态系数为\(2m-1\)，无完整槽自交叠项；不能混取两个域的较好\(\gamma\)和银行。与[行动边际对齐固定点](../定理/行动边际对齐的可信菜单固定点--定理.md)相比，本页背景行动边际可以不同于\(p\)，所以有正\(G\)，但源未来折扣不因此与所选背景自动一致。

当\(m=5\)时本接口尚需\(W\ge(9\gamma-Q_{\rm stat})/2\)；这不覆盖现行另证的[五人半覆盖定理](../定理/五人半覆盖--定理.md)。当\(m=6\)时本接口尚需\(W\ge(11\gamma-Q_{\rm stat})/2\)，当前每份完整纯SPE目标未由本对偶闭合。\(m=1\)、零客户、空主题和零\(\rho\)坐标均直接满足所写有限恒等式；没有除零。关系为域包含、直接对偶推导和有条件付款接口，正式超图留第三阶段。
