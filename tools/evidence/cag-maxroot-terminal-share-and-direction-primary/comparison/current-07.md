---
id: "customer-attraction/fixed-past-and-global-mean-cap-frontier-internal-review"
kind: "review"
type_tag: "审查"
title: "固定过去负载与全行均值cap组件的内部复核"
status: "internal-identities-and-coarse-bound-checked; covariance-payment-unresolved"
summary: "保原matching已读两主稿后的检查身份，自足重构P/F两质量、前缀下界、端点保底B_m与无需鞍点的静态折扣，再核global mean-cap原source正信用及未证PAY。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round12/matching/frontier_components_independent_review.md"
---

# 原内部检查的范围

本源3192字节全文明确已读aggregate的`fixed_prefix_shadow_component.md`及tree的`mean_cap_credible_shadow_working.md`，随后作域/代数检查。它不是读主稿前的盲重构，未使用有限计算或策略扫描，也没有声称外审或新颖性。结论是两份全输入组件在所写范围无致命问题，**没有**得到half或有用新福利界。以下保其完整承重推导及每种银行的适用域。

采用[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)，任意m≥1、有限单位客户、有限非空目录，保空主题、重复、零客户和离轨平局。固定完整纯SPE \(\sigma\)、实际主题\(B_j\)、收益\(u_i\)、\(W=\sum_i u_i\)。原actual-prefix行i强制A后沿同一原策略的真实叶为\(Z_i(A)\)，删除固定i槽负载\(\ell_i(A)\)。

# 原固定策略菜单的两份行动质量

各行任选原真实菜单分布\(q_i\)，令\(L=m^{-1}\sum_iE_{q_i}\ell_i(A)\)、\(t=(1+L)^{-1}\)、\(g_t(T)=\sum_{x\in T}t_x\)、\(\gamma=\max_Tg_t(T)\)。逐行拆过去/未来，
\[
L=P+F,\quad
P_x=\frac1m\sum_j(m-j)\mathbf1_{x\in B_j},\quad
F_x=\frac1m\sum_iE_{q_i}\sum_{j>i}\mathbf1_{x\in Z_i(A)_j}.
\]
P、F各有行动质量\((m-1)/2\)，不是各占一份\(m-1\)。对\(b_i(x)=\sum_{j<i}\mathbf1_{x\in B_j}\)、\(r_i=m-i+1\)，因\(j<i\)时\(m-j\ge r_i\)，有
\[
L_x\ge P_x\ge\frac{r_i}{m}b_i(x).
\tag{PREFIX}
\]
这使用固定actual前缀，不能无条件迁移为任意离轨背景的下界。

定义静态信用
\[
Q_{\rm stat}=(m-1)\gamma-\sum_xL_xt_x.
\]
其准确拆分为
\[
Q_{\rm past}=\frac1m\sum_j(m-j)[\gamma-g_t(B_j)],\quad
Q_{\rm future}=\frac1m\sum_iE_{q_i}\sum_{j>i}
[\gamma-g_t(Z_i(A)_j)].
\]
两项非负且相加等于Qstat，仅使用主题价格最大值定义，**不需鞍点KKT**。这是原检查确认的范围修正；它们不是两份额外Qstat。未来折扣来自这些所选q_i分支，不自动等于另一个查询p的未来折扣。

# 一阶段安全保底及端点计算

原完整IC给\(u_i\ge\max_T\sum_{x\in T}(b_i(x)+r_i)^{-1}\)。结合(PREFIX)，对\(0\le b\le m-r\)，
\[
t_x(b_i(x)+r_i)\le
\max_{0\le b\le m-r_i}\frac{b+r_i}{1+r_ib/m}.
\]
分式导数符号为\(1-r_i^2/m\)，所以端点最大值是
\[
\max\left\{r_i,\frac{m^2}{m+mr_i-r_i^2}\right\}.
\]
取最大价格主题，得到
\[
u_i\ge\gamma a_m(r_i),\quad
a_m(r)=\min\left\{\frac1r,\frac{m+mr-r^2}{m^2}\right\},
\quad W\ge\gamma B_m,\ B_m=\sum_{r=1}^ma_m(r).
\]
r≥√m时取1/r，r≤√m时取二次式。直接求和给
\[
B_5=\frac15+\frac14+\frac13+\frac{11}{25}+\frac9{25}
=\frac{19}{12},\qquad
B_m=\frac12\log m+\frac12+o(1).
\]
渐近中的小r二次和趋于1/2，大r调和差为\((\log m)/2+o(1)\)。没有除\(\gamma\)，所以全零客户和m=1边界保留。该粗界远不足以支付m=5在Qstat=0时所需\(9\gamma/2\)；原检查并未把数值正确误作half付款。

# 全行mean-cap：原source正信用及精确符号

另一个组件改变背景域：固定actual行动端点，允许在每个真实完整孩子SPE端点\((A,e)\)上混合，进入收益只需全行\(E_qd_i\le u_i\)。逐叶cap凸包、逐行动mean-cap、全行mean-cap依次包含；所有删除槽负载仍有合法目录质量m−1，彩票不叫原游戏新SPE。

在该共享域的鞍点\((p,L^*)\)令\(\rho_x=\Pr_p[x\in A]\)、\(t=(1+L^*)^{-1}\)、\(w=\rho t^2\)、\(\gamma=\sum_x\rho_xt_x\)。每行shadow最优值\(H_i\)有有限LP对偶
\[
H_i=\eta_i+\mu_iu_i,\quad
\eta_i+\mu_id_i(A,e)\ge w\cdot\ell_i(A,e),
\quad\mu_i\ge0,\ \eta_i\in\mathbb R.
\]
查询源保原\(\sigma\)，记\(I_i=u_i-E_pd_i^0(A)\ge0\)、\(R_i(A)=\eta_i+\mu_id_i^0(A)-w\cdot\ell_i^0(A)\ge0\)。于是
\[
\boxed{G=\sum_i[H_i-E_pw\cdot\ell_i^0]
=\sum_i\mu_iI_i+\sum_iE_pR_i\ge0.}\tag{CAP-SLACK}
\]
用同一\(L^*\)定义原源的
\[
D=\sum_iE_p\sum_{x\in A}\frac{t_x^2(\ell_i^0(A)_x-L_x^*)^2}{1+\ell_i^0(A)_x},\quad
\operatorname{Cov}=\sum_{i,x}t_x^2\operatorname{Cov}_p(\mathbf1_{x\in A},\ell_i^0(A)_x).
\]
中心化线性项为\(C=\operatorname{Cov}-G\)，倒数展开给
\[
\boxed{W-m\gamma=D-\operatorname{Cov}
+\sum_i(1+\mu_i)I_i+\sum_iE_pR_i.}\tag{BAL}
\]
原检查特别保留正\(\mu_iI_i\)、因子m及η无符号；无需把\(\mu_i u_i\)另行从W支付，也不得将已拆的G再花一次。逐行动源变体的\(I_i\ge0\)来自条件均值cap，非每个超cap端点的纯进入IC；全行版则始终用原source。

目录静态比较给\(\operatorname{OPT}_m\le(2m-1)\gamma-Q_{\rm stat}\)，所以仍待证明
\[
\operatorname{Cov}\le D+\sum_i(1+\mu_i)I_i+\sum_iE_pR_i
+(\gamma+Q_{\rm stat})/2.
\]
源/背景分开、有限对偶与非负银行均未给此金额。原稿末句明确不认证外审或新颖性，原样保留其范围。

# 与现有正文、后续修订及当前状态

对应完整主对象为[固定过去负载与静态折扣](../引理/原策略菜单的固定过去负载与静态折扣分解--引理.md)及[可信端点三域与松弛信用](../引理/可信端点均值cap的三域与松弛信用--引理.md)。本源独有信息是实际内部对稿核查、无需鞍点的折扣范围及对源/彩票条件的检查；未伪装成第二次独立发现。后续[aligned固定点](../定理/行动边际对齐的可信菜单固定点--定理.md)将源/背景行动边际对齐，却令G=0，不能与本页好项并领。完整槽又有不同静态系数及同源范数，不免费拼接。

主稿、两受核原稿及相关floor/full/真实流正文均全文比较，原字节和指纹见[证据](../../tools/evidence/credible-transposition-reset-primary/README.md)。本批无程序源或新增有限运行；结构核验不能充当数学自动认证。原稿五人方法未闭合不覆盖现行五人定理，六人目标也未由本内部核查关闭。关系是原主稿→审查的来源/验证范围和上述直接代数，不新增福利边；正式超图留第三阶段。
