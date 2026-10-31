---
id: "customer-attraction/single-query-convexification-cost-and-v-pay-candidate"
kind: "candidate"
type_tag: "候选"
title: "单查询凸化代价与共同付款条件"
status: "variance-and-fixed-background-identities-proved; v-pay-unresolved"
summary: "Vp/2是一次查询的准确固定背景二次凸化代价；存在合法共享鞍点满足V-PAY为更强的充分候选，真实适应性缺陷尚未被它控制。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round12/geometry/one_query_convexification_candidate.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round12/geometry/conditional_demand_and_information_budget.md#3"
---

# 固定模型与同域记号

模型为有限单位客户、有限非空共同目录和m≥1名单位提供者，完整历史纯SPE σ任取，保空主题、重复和所有平局。实际收益u_i、福利W=Σ_i u_i，最优m主题覆盖为OPT_m。

为让候选自足，本页用[可信端点全行均值cap](../引理/可信端点均值cap的三域与松弛信用--引理.md)的同一共享鞍点合同：原实际行动端点固定，其他行动可用完整孩子SPE见证，逐行彩票q_i只需E_qd_i≤u_i。令删除进入槽后的平均背景为L*，t_x=(1+L_x*)^{-1}，p为该鞍点真正的查询分布，ρ_x=Pr_p[x∈A]。γ=max_TΣ_{x∈T}t_x，p的正支持主题取等号。它不是任取方便p的公式，也不把端点分析彩票视为原博弈的新SPE。

原source仍是同一σ在实际前缀强制A的真实叶。其删除槽负载为ℓ_i⁰(A)，进入收益d_i⁰(A)，I_i=u_i−E_pd_i⁰≥0，IC=Σ_iI_i。定义
\[
 C=\sum_iE_p\sum_{x\in A}t_x^2(\ell_i^0(A)_x-L_x^*),
\]
\[
 D=\sum_iE_p\sum_{x\in A}
 \frac{t_x^2(\ell_i^0(A)_x-L_x^*)^2}{1+\ell_i^0(A)_x}\ge0.
\]
逐客户倒数恒等式给
\[
 \boxed{W-m\gamma=IC+D-C}.                        \tag{BAL}
\]
有限shadow对偶亦给C=Cov−G，G=Σ_iμ_iI_i+Σ_iE_pR_i≥0。G只是一份原source信用；用Cov写候选时必须把同一G加回，不能同时把它当新钱。

因为L*是总行动质量m−1的合法分数目录负载，已有静态账为
\[
 Q_{\rm stat}=(m-1)\gamma-\sum_xL_x^*t_x\ge0,
 \quad OPT_m\le(2m-1)\gamma-Q_{\rm stat}.          \tag{STATIC}
\]
其逐客户证明是1_{c_x^*>0}≤(c_x^*+L_x*)/(1+L_x*)，对最优m主题价格用γ上界。Q_stat不是额外实际利润。

# 一次查询的准确凸化代价

置v_A=t⊙1_A、v=E_pv_A，令
\[
 V_p=E\|v_A-v\|^2=\sum_x\rho_x(1-\rho_x)t_x^2.
\]
由于0<t_x≤1，0≤ρ_x≤1，且p支持主题的t价格为γ，
\[
 \boxed{0\le V_p\le\sum_x\rho_xt_x^2
                  \le\sum_x\rho_xt_x=\gamma.}     \tag{VAR}
\]
对任意**固定**向量w及Φ(z)=‖z‖²/2，展开平方并用E(v_A−v)=0得
\[
 \boxed{E\Phi(w+v_A)-\Phi(w+v)=V_p/2\le\gamma/2.}\tag{CONV}
\]
若w也依赖A，展开会额外保留E〈w,v_A−v〉，不可照用(CONV)。这正是实际适应性后继不能被固定背景Jensen代替的一个明确位置。

# 未证明的加强候选及其充分性

原稿提出
\[
 \boxed{C\le D+IC+\tfrac12(V_p+Q_{\rm stat}).}     \tag{V-PAY?}
\]
最弱有用量词为：每个输入及每份完整σ，**存在**一个合法共享minimax鞍点及其允许的端点实现满足(V-PAY?)；没有要求所有非唯一鞍点均成立。若换成raw/floor、完整槽或行动边际对齐域，须重建其L、γ、C及信用，不能混取别域较好系数。

将(V-PAY?)代入(BAL)，再用(VAR)，得到
\[
 2W\ge2m\gamma-V_p-Q_{\rm stat}
 \ge(2m-1)\gamma-Q_{\rm stat}\ge OPT_m.
\]
所以它比把V_p换成γ的原充分付款界更强，**不是**half的等价重述，也未证明half必推出它。m=5的路线压力为W≥(9γ−Q_stat)/2；m=6为W≥(11γ−Q_stat)/2。这些路线压力不覆盖已由另一证书解决的五人half。

当p为单点时V_p=0，且Cov=0，C=−G≤0，因而该端点满足候选。它只核验零方差端点；并不保证一般输入有单点鞍点。零客户时γ=V_p=C=D=IC=Q_stat=0，全式保持，无除零。

# 从凸化恒等式到候选还缺的内容

(CONV)只描述固定w的一个查询样本。原游戏中后继观察已经实现的A，行动和后续历史都可依赖它；每个位置共用A也不删除这种响应。欲得(V-PAY?)，仍须把所有真实响应、交叉历史重置及其累计前缀乘子的净成本由**同一**D、IC、Q_stat及可用G支付，只剩一份V_p/2。

隐藏查询、改成事先承诺、以分数平均行动替代原子行动，都会改变观察结构或原游戏；一般匿名势/PSD/纯SPE存在性没有给所需付款。E‖v_A‖²和‖Ev_A‖²的差恰是V_p，也不能当它们相等。[条件末位需求与信息预算](../引理/固定中间动作的末位需求运输与单查询信息预算--引理.md)保留三个待证连接；[真实重放协方差](../问题/真实重放协方差的定量付款--问题.md)进一步显示每个信息增量前的累计prefix，未给单位系数界。

原稿随后记录tree内部核过VAR、CONV及单点端点，亦说明既有正C保险例有D+IC>C，不能直接反驳V-PAY。这里保留原稿所记的内部核查范围；本批没有拿到新盲审、重算保险例或跑扫描，不把该文字记录提升为未证候选的认证。

# 来源和可接续状态

主源3350字节及条件信息稿4146字节均全文读，与全行mean-cap原source账及后续raw逆鞅表达全文比较。原件、指纹和逐源去向见[证据](../../tools/evidence/conditional-demand-information-primary/README.md)。已证部分是(VAR)/(CONV)、原同域(BAL)/(STATIC)及零方差端点；(V-PAY?)仍开放，未证明失败，清洗保留候选不等于解完它。
