---
id: customer-attraction/joint-query-inventory-hall-cancellation-and-initialization-payment
kind: theorem
type_tag: 定理
title: 联合查询库存的Hall取消与初始化付款
status: fixed-Hall-B-cancellation-and-simultaneous-joint-source-net-proved; incoming-payment-open
truth_status: stated-expected-cancellation-and-source-payment-proved; no-general-total-budget
review_level: full-original-and-shared-activation-contract-reading; analytic-fixed-versus-adaptive-check
scope: 有限单位客户共同目录、固定最优T/owner和原完整计划；actual Hall-B的R/I^-query库存；lambda须激活前固定
summary: actual Hall-B可将调和source逐源降为真实G利润，在R单位与I^-的κ库存中共取消G。固定条件删除保持actual I信用，全部R/I初始化同时在同一eta内付款；后续incoming与W+κ总预算仍未付。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round4/mixed/joint_source_net.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round4/mixed/joint_source_net.md
---

# 联合查询库存的Hall取消与初始化付款

## 同一actual图与query库存

采用[完整历史共同目录模型](../定义/共同目录完整历史模型--定义.md)，有限单位客户、非空有限目录、任意$m\ge1$；固定最优T、owner分割Q、actual叶Z及覆盖C。保空主题、重复、零客户和全部有序历史。记$R=O\setminus C,I=O\cap C,G=C\setminus O$，actual利润$u_i$、$g_i=u_i(G)$；$I^-$是owner实际未覆盖的I客户，$c_x^0$为actual负载。

[共享激活](共享激活的遗漏与归属误差联合边际--定理.md)为R创建单位源，为$x\in I^-$创建单位总源，其中actual信用保留于各coverer，而query分支仅有$\kappa_x=1/(c_x^0+1)$质量。故联合query终点库存恰为

\[
\beta_x=1\ (x\in R),\qquad\beta_x=\kappa_x\ (x\in I^-),
\quad\beta_i=\sum_{x:o(x)=i}\beta_x.
\]

owner已实际覆盖的I不建query终点。$\kappa^-=\sum_{I^-}\kappa_x$不是免费新福利，它同时增加待采购源。

## Hall-B降source，只使用一份actual G

actual[Hall-B](最优归属的全子集调和运输与锚定隔离--定理.md)从owner向每个actual coverer给容量$1/(c_x^0+1)$，向相应客户终点给$\beta_x$。原图可运送调和source

\[
b_i^H=\sum_{y\in Z_i\setminus O}H_{c_y^0}/c_y^0\ge g_i.
\]

去循环后按source路径分解，将每个source自己的路径弱缩小到总量$g_i$，所有边/终端仍不超容量。因此存在$0\le\lambda_x\le\beta_x$、$\sum_x\lambda_x=|G|$及角色流f满足

\[
\lambda_i+out_f(i)-in_f(i)=g_i.
\]

这里仅使用实际G普通利润，**不**将整份调和$b^H$作为可花whole-IC资金。

任取局部$0\le\delta_x\le\beta_x$、$\delta_i\le g_i$可先从本owner source直送其终点，再用残余网络扩充。每个角色割的source需求和本地终端容量同减$\delta(J)$，原割条件保留，故所有owner可同时取$\delta_i=\min(g_i,\beta_i)$。分数库存只用于分析，不改变单位客户模型。

## 激活前固定取消与唯一净收入

在激活/统一U之前固定同一可行$\lambda$。R源保留$1-\lambda_x$；I^-仅将query分支保留比例$1-\lambda_x/\kappa_x$，actual信用分支不动。因query事件质量为$\kappa_x$，期望删除恰$\lambda_x$。总query质量从$|R|+\kappa^-$降为

\[
M=|R|+\kappa^--|G|.
\]

这只要求**期望**取消G，不要求每world恰取消G；I实际信用仍是同一error，不重复加被取消query。由同一角色守恒，唯一净收入

\[
\eta_i=u_i-g_i+\lambda_i=u_i(I)+\lambda_i\ge0,
\quad\sum_i\eta_i=W.
\]

角色error边容量只是实际I利润内的运输容量，不另产生福利。不能同时使用R-only Hall-A的另一份G取消或另一eta。

## 所有R/I初始化source同时付款

同一query的current吸收拆为owner初始源部分$A_i^{src}$与更早角色传入部分；最终只取总吸收的一份$w=A/D$，不是两份IC。每个owner初始query均为完整合法T_i。共享MARG-CAP给$A_i^{src}\le D_i(T_i)$，取消只减它，故

\[
K_i^{src}=u_iA_i^{src}/D_i(T_i)\le u_i,
\]

零D时A零、费置零。若$g_i\le\beta_i$，局部预送使$\lambda_i\ge g_i$，$\eta_i\ge u_i$；若$g_i>\beta_i$，本owner全部query库存满额取消，R和I-query初始源均0。于是

\[
\boxed{K_i^{src}\le\eta_i\quad\forall i,\qquad\sum_iK_i^{src}\le W.} \tag{JOINT-SOURCE-NET}
\]

根无incoming，根联合费用也已付。这个初始化比较不要求IC；用完整SPE购买query时才进一步用$D\le u$。其它角色可能有正incoming，不能将source已付当全行已付。

旧SOURCE-NET只取消R。加入I-query后，无R库存的owner未必由旧二分证明控制；本页Hall-B的missing-owner价格恰好匹配I-query的κ，修复的是全部联合初始化的共享兼容，不是又领一笔G。

## 余下总预算与自适应边界

完整SPE及全吸收给$M\le\sum_i(K_i^{src}+K_i^{in})$。若能共同达到总费$\le W+\kappa^-$，减同一query源$\kappa^-$才得到$|R|-|G|\le W$。这足够预算尚未证明；每state $w\le1$、source预付或各客户分别存在路由，都不支付同role多query碰撞。不能擅自将目标改为另一个系统的费用/净券而保留本页优惠。

I-query条件删除依赖$\lambda$在激活/U前固定。若$\lambda(U)$与query事件相关，$E[(\lambda/\kappa)1_{query}]$不一定等于$E\lambda$。R-only的逐world Hall-A取消另因R token每world始终存在而合法；它不保平均残源乘原MARG-CAP，也不是本页固定Hall-B合同，二者不无证合成。

这不是断言所有world依赖R/I取消不可能。后来`rankwise_joint_hall.md`另以每个G客户的priority赢家为随机source，并只对实际存在的query token设单位sink，逐world全cut保证整数取消；其期望才回到Hall-B容量。它不以平均容量冒充点态容量，也不能用随机赢家收入替原IC的固定$u_i$，旧SOURCE-NET不凭均值恢复。该新合同的全文比较与未复跑边界见[版本审查](../审查/归属势与联合取消的版本及运行范围--审查.md)，原件只作本批旁读，尚未替它done。

3029B源本批重新全文实读核SHA，保credible分别核Hall-B降source、delta、初始分母与联合预付的内部历史身份，无外审或新颖性认证。原审计本批[真实一次运行](../计算/最优归属运输的全割与有理增广回归--计算.md)只测静态A/B，未调用本页激活、条件取消或SOURCE-NET程序；不能用1704个maxflow替一般incoming背书。六人half仍未由本定理解决，五人已有[独立定理](五人半覆盖--定理.md)。
