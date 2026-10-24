# 只在 fresh 利润内归一化：无正 C 迁移的合法消元

2026-10-24，relay。一般全输入表示组件；credible收到精确陈述后独立重构通过。**未证明总费用下降或Q-CAG-HALF。** 分母与新流均重新定义，不能把其好处和round5旧流的SOURCE/DIAGONAL混合领取。

## 1. 对象与分母

沿用 `../../round5/credible/all_fresh_submarkov_elimination.md` 的原完整SPE sigma、实际叶Z/覆盖C/收益u，以及natural context t=(g,i)。令a=sigma_i(g)，规定叶B_t=finish(g)，actual-reset叶A_t=finish(Z_<i,a)。完整actual IC给

    D_t=u_i(A_t)<=u_i，    e_t=u_i-D_t>=0。

只对x in a outside C定义U、V、c_A、c_B及全fresh正边q_tj、P_t、负项N_t、diagonal J_t、common L_t，与round5定义相同。记

    nu_t=u_i(B_t;N outside C)， d_t=u_i(A_t;N outside C)，
    Y_t=u_i(A_t;C)， X_t=u_i(B_t;C)。

新分母用nu_t，不用完整v_t=X_t+nu_t。逐客户FRESH及LOSS立即给

    nu_t-d_t=P_t-N_t，
    nu_t-P_t=J_t+L_t=d_t-N_t>0。                 (F-LOSS)

严格号只在nu>0时用。每个正q_tj都有fresh x见证，它被A_t中j的规定动作覆盖，所以后继natural context r(t,j)的fresh利润也严格正。nu=0时全部fresh q/P/N/J/L都0；只接受fresh利润注入时不会从正边进入它。

## 2. fresh闭合的sub-Markov DAG

对nu_t>0的context给非负fresh利润注入b_t，按严格角色顺序定义

    h_t=b_t+sum_(s,j:r(s,j)=t) beta_s q_sj，
    beta_t=h_t/nu_t。

对任意未来角色集合K、k=|K|，同一逐客证明给

    sum_(j in K)q_tj/nu_t<=k/(k+1)。

这次fresh权重[1/c_B]/nu的和恰为1。无需tracked、b>=1或outside客户owner；所有fresh客户共同使用现有利润质量，不新造客户源。

全DAG求和有

    sum_t b_t=sum_t beta_t(nu_t-P_t)
               =sum_t beta_t(J_t+L_t)。         (F-MASS)

nu=0节点不能正接收的域证明已在上一节给出，有限角色DAG保证递推唯一与所有系数有限。

## 3. 无正X迁移的整条IC账与安全退券

由d_t=u_i-Y_t-e_t及F-LOSS，

    nu_t-P_t=u_i-Y_t-N_t-e_t。

所以

    sum_t b_t=sum_t beta_t[u_i-Y_t-N_t-e_t]。   (F-LEDGER)

每个beta是一个context的非负标量；上述只把同一个完整actual IC乘beta，没有对客户另加权。X_t不出现，因为未把off-history的C利润纳入归一化或传播。

credible另独立指出，逐节点有

    0<=Y_t+N_t+e_t<=u_i，
    u_i-Y_t-N_t-e_t=J_t+L_t>0。

因此可以把Y+N+e在同一整行账内安全退券，余量作为actual整行非负coupon；正余量蕴含u_i>0，其整行系数为

    kappa_t=beta_t(J_t+L_t)/u_i。

传播始终fresh，所以没有past-C出口，也无需给互斥叶X另造库存。但同一actual角色可收到多个context的kappa，**尚无其和<=1**；把所有这些净券求和仍只是原注入质量，不是已付W。

若暂不使用有利的-e项，合法上界为

    sum b_t<=sum beta_t(u_i-Y_t-N_t)
            =sum b_t+sum beta_t e_t。

没有因此自动<=sum u_i。也没有把反事实查询C收益Y_t改称可重复花的actual I/G库存。

## 4. 初始化与真实域

OPT-owner查询不一定是natural prescribed动作；必须用round5合法INIT。保留初始owned-R当前吸收A_i^src；每个未来规定角色j得到该真实叶上所注入R客户的利润b_(i→j)。这些都是fresh利润，正注入使后继nu>0。于是同一rho总量有

    M=sum_R rho_x=sum_i A_i^src+sum_t b_t。

加F-LEDGER即给全fresh消元。不同来源在同一真实context相加，不能仅按相同主题识别有序历史。

初始source也可利用完整IC的fresh部分。令D_i^F为source查询fresh利润、Y_i^src为其C利润，alpha_i=A_i^src/D_i^F，则

    A_i^src<=alpha_i(u_i-Y_i^src)， 0<=alpha_i<=1。

零D^F对应零A，取alpha=0。这仍是同一整条IC乘一个标量后减去其query C部分。不能同时领取旧source付款而不核同一费用。

## 5. 改变了什么，仍缺什么

本核避免正X(C)跨叶迁移、past-C coupon与C内重采。代价是nu<=v，转移q/nu比旧q/v大；同一输入的beta与后续流可能上升，不能宣称总成本不增。SOURCE、NET、M−H、HIT、priority界若依旧核，均须按新流另证。

一个未证充分接口是同一初始化与fresh流共同满足

    sum_i alpha_i(u_i-Y_i^src)
       +sum_t beta_t(u_i-Y_t-N_t)<=W。          (F-BUDGET?)

则完整actual IC与F-LEDGER给M<=W；取M=OPT-W便闭合half。**没有证明F-BUDGET，也未证明它弱于旧TOTAL。** 加费的beta可能抵消不重采C的结构收益。

本页未实质使用ell_t>=0的off-history IC。下一步必须把真孩子比较或其它全局约束接到同一净actual行费用，而不是把新分母、更短ledger或更安全退券认作half进展。
