---
id: "customer-attraction/actual-load-tangent-bank-and-common-error-payment"
kind: "candidate"
type_tag: "候选"
title: "实际负载切线银行与共同误差付款"
status: "static-and-kkt-identities-proved; t-pay-unresolved"
summary: "原策略共享菜单的实际平均删除负载由KKT给出一份至多gamma/2的具体银行；T-PAY仍缺全历史平方误差转移，完整最优余量只是原half的等价账。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round12/direct/GENERAL_PROOF_WORKING.md#2-4"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round12/direct/README.md"
---

# 原共享菜单合同

有限单位客户、有限非空共同目录，任意m≥1名单位提供者，任意完整有序历史纯SPE σ；保空主题、重复标签、零客户及所有离轨平局。实际主题为S_i，终局客户负载c=Σ_i1_{S_i}、收益u_i，福利W=Σ_i u_i。

原源第i行是实际前缀强制A后仍沿同一σ的真实叶，删除**同一i槽**的负载为ℓ_i(A)，其进入收益为d_i(A)。本页使用原策略菜单共享域
\[
 K=\frac1m\sum_i\operatorname{conv}\{\ell_i(A):A\in\mathcal S\}.
\]
该有限紧凸域的每个负载都是m−1份目录行动的分数负载。取真正共享鞍点(p,L*)，即有限查询分布p与K中背景的max_p min_L Σ_xρ_x/(1+L_x)，ρ_x=Pr_p[x∈A]。令
\[
 t_x=(1+L_x^*)^{-1},\quad w_x=\rho_xt_x^2,
 \quad g_t(A)=\sum_{x\in A}t_x,
 \quad\gamma=\max_Ag_t(A)=\sum_x\rho_xt_x.
\]
p的正支持主题取最大t价。原稿是这个K的候选，不自动沿用后来扩大cap、raw floor或aligned域较好的γ；若换域，所有背景、源与信用必须一起重建。

# 原源主账和完整静态余量

令I=Σ_i[u_i−E_pd_i(A)]≥0，并置
\[
 C_{\rm corr}=\sum_iE_p\sum_{x\in A}t_x^2(\ell_i(A)_x-L_x^*),
 \quad D=\sum_iE_p\sum_{x\in A}
 \frac{t_x^2(\ell_i(A)_x-L_x^*)^2}{1+\ell_i(A)_x}\ge0.
\]
由原IC和逐客户倒数展开，有
\[
 \boxed{W-m\gamma=I+D-C_{\rm corr}.}              \tag{BAL}
\]
这里C_corr是中心化切线债，不是客户集合或净cap成本。

取任意覆盖最优m主题元组T，客户并集O、覆盖次数a_x。定义
\[
 Q_{\rm stat}=(m-1)\gamma-\sum_xL_x^*t_x\ge0,
 \quad P_{\rm opt}=m\gamma-\sum_jg_t(T_j)\ge0,
\]
\[
 Rep=\sum_{x\in O}(a_x-1)t_x\ge0,
 \quad Out=\sum_{x\notin O}L_x^*t_x\ge0.
\]
逐客户在O上用1=t_x+L_x*t_x，并将重复比较主题贡献单列，得到**精确**等式
\[
 \boxed{OPT_m=(2m-1)\gamma-Q_{\rm stat}
                       -P_{\rm opt}-Rep-Out.}     \tag{STATIC}
\]
所以若保全部余量，
\[
 C_{\rm corr}\le I+D+\tfrac12(\gamma+Q_{\rm stat}+P_{\rm opt}+Rep+Out)
\]
恰与2W≥OPT_m等价。把所有余量重命名没有产生新付款；有用的新证明仍须将具体跨历史债映到其中**特定**信用，且只用一次。Popt与Rep+Out的总和固定，见[最优组合影价松弛](../引理/最优组合影价松弛与正损失替换停界--引理.md)。

# 实际负载的KKT银行

原actual主题S_i是第i行菜单中的合法查询，其真实叶就是原实际叶，所以ℓ_i(S_i)=c−1_{S_i}。因此
\[
 L^{\rm act}=\frac1m\sum_i\ell_i(S_i)=\frac{m-1}{m}c\in K.
\]
在L*最小化F_p(L)=Σ_xρ_x/(1+L_x)的一阶条件为
\[
 \langle-w,L-L^*\rangle\ge0\quad(L\in K).
\]
代入L_act，结合w·L*=Σ_xρ_xt_x(1−t_x)=γ−Σ_xρ_xt_x²，得m≥2时
\[
 \boxed{\sum_x\rho_xt_x^2c_x
 \le\frac m{m-1}\left(\gamma-\sum_x\rho_xt_x^2\right).}\tag{ACTUAL}
\]
这不是原σ的额外IC，而是同一共享背景域已有的KKT约束。

令一份具体非负银行
\[
 B_{\rm act}=\frac{m-1}{2m}\sum_x\rho_xt_x^2c_x.
\]
则
\[
 0\le B_{\rm act}\le\tfrac12\left(\gamma-\sum_x\rho_xt_x^2\right)
                         \le\gamma/2.             \tag{BANK}
\]
原稿提出更强的充分付款候选
\[
 \boxed{C_{\rm corr}\le D+I+B_{\rm act}.}          \tag{T-PAY?}
\]
若成立，(BAL)/(BANK)给W≥(m−1/2)γ，而(STATIC)给OPT_m≤(2m−1)γ，遂得half。它未使用完整静态余量，因而只是较强充分条件，不是half等价式。m=5时银行为(2/5)Σρt²c，m=6时为(5/12)Σρt²c；系数的代入不是付款证明。

m=1时不要除以m−1：K={0}、t=1，单人SPE已直接最大化主题覆盖，W=γ=OPT₁；定义B_act=0仍有意义。零客户或全空主题时所有金额为零，不作γ或W归一化。

# 原IC到切线游戏只给带误差的不等式

固定t，在任意完整终局Z上令v_A=t⊙1_A，并定义
\[
 u_i^{\rm tan}(Z)=2g_t(Z_i)-v_{Z_i}\cdot(t\odot c(Z)),
\]
\[
 E_i^t(Z)=\sum_{x\in Z_i}\frac{(1-t_xc_x(Z))^2}{c_x(Z)}\ge0.
\]
Z_i中的客户保证c_x≥1，逐项展开即
\[
 \boxed{u_i(Z)=u_i^{\rm tan}(Z)+E_i^t(Z).}         \tag{TANGENT}
\]
在任意**原σ的**历史h，obey与dev都执行同一原σ在各自改变后历史的真实后继。原整主题IC只推出
\[
 u_i^{\rm tan}(dev)-u_i^{\rm tan}(obey)
 \le E_i^t(obey)-E_i^t(dev).                       \tag{T-IC}
\]
故该节点正切线regret至多其本身规定叶的平方误差；它一般并非零。不能假定σ是切线二次游戏的SPE，也不能用实际路径节点的误差支付其他离轨历史的全部规定误差。

尚缺的是：把r_beta差、所有改变前缀的重置误差和相关全主题IC，合法转入**同一**B_act，或映到明确的静态余量。BANK只界定若存在付款可花多少钱，没有建立债到该银行的映射。普通PSD、对称交互、SPE存在或给银行命名均未证明T-PAY。[切线与动态首利诊断](../障碍/切线策略与动态首利摊派的真实边界--障碍.md)给实际失效方向。

# 来源、比较与状态

主工作稿9382B和README811B全文读，核冻结SHA；与原source均值cap账、单查询V-PAY、真实重放累计前缀、最优组合松弛及两项旧反例全文比较。本页未将原策略K与cap扩大域混拼。完整原件、相关阅读范围及无新程序记录见[证据](../../tools/evidence/direct-tangent-payment-primary/README.md)。

已证的是STATIC、ACTUAL、TANGENT和T-IC，不是T-PAY。原窗口明确没有程序或有限probe；本批亦无新增数学运行、盲审或外审。原稿“五人仍OPEN”是历史方法状态，不能覆盖现行另证的[五人half](../定理/五人半覆盖--定理.md)。当前恰六人全称目标没有因银行界而解决；下一步是保完整IC的共同误差付款或另一个净覆盖论证。
