---
id: "customer-attraction/real-replay-covariance-amount-and-prefix-payment-gap"
kind: "problem"
type_tag: "问题"
title: "真实重放协方差的切线余项、累计前缀与定量付款"
status: "identities-proved; stated-uniform-payment-interface-unresolved"
summary: "保真重放的加权门槛重置、切线EDGE和不同主题同叶残差，并将raw逆鞅累计前缀表达与真流总功相等；非负守恒流和一次净cap望远镜未支付协方差金额。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round12/tree/real_replay_covariance_flow.md#5"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round12/tree/uniform_swap_and_raw_flow_independent_review.md#1-4"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round12/geometry/conservative_raw_tail_replay.md#5-7"
---

# 真实重放协方差的切线余项、累计前缀与定量付款

## 已闭合的构造与仍未闭合的金额

在[真实后继重放算法](../算法/固定进入槽的真实后继重放与一次势预算--算法.md)的精确模型和记号下，固定实际行i、原完整纯SPE σ、其原实际前缀h_i及原源z_A。给定所选raw目标Q_i，已证明非负路径质量p_AQ_i(y)、正确终点Q_i、每条未来边的原整名玩家IC，以及同一固定F_i/B_i/r_i的一次有符号望远镜。

未证明的是这些合法流上的
\[
\mathrm{Cov}=\sum_iE_p[(w_A-w)\cdot\ell_i(z_A)]
\]
能由同一原源的收益/曲率/约化成本以及允许的静态半槽余量支付。以下保留可用的全输入恒等式和准确剩余项；没有把“流存在”当作金额界。

## 真实未来边的规范门槛重置

取真重放的未来j边z→z′，两叶在j以前的前缀和进入行动A一致。Γ_j=u_j(z)−u_j(z′)≥0。这里u_j(z)是该真实分支的值，不能替换成原实际路径固定的u_j。令
\[
S_{\rm desc}(z)=\sum_{k>j}[u_k(z)-M(z_{<k})].
\]
z、z′的严格后继都沿同一原σ，故两端S_desc≥0。前于j的M不变，当前j的门槛也相同，因此直接从净成本定义得
\[
\boxed{\Delta B_i=\Delta d_i+\Gamma_j
 +\sum_{i<k<j}[u_k(z)-u_k(z')]
 +S_{\rm desc}(z)-S_{\rm desc}(z').}
\tag{RESET}
\]
中间祖先的收益损失可正可负。它们不能由当前一个Γ_j自动支付。重放到中途时，这些更早未来角色可能已被强制成目标动作；不能把它们都再称为“从原源发出的最佳回复”或领取新的原源规范盈余。

原内部审查还核过较早非均匀mean-floor对偶。若
\[
r_i=\eta_i+\mu_i d_i+F_i-w\cdot\ell_i\ge0,
\quad F_i=\sum_h\lambda_{ih}\mathbf1_{z\text{延伸}h}(M(h)-u_{|h|+1}),
\]
其中μ_i、λ_ih均非负，\(S_{\rm desc}^{\lambda}(y)=\sum_{k>j}\lambda_{i,y_{<k}}[u_k(y)-M(y_{<k})]\)。则同样有
\[
\Delta F_i=\lambda_{i,z_{<j}}\Gamma_j
 +\sum_{i<k<j}\lambda_{i,z_{<k}}[u_k(z)-u_k(z')]
 +S_{\rm desc}^{\lambda}(z)-S_{\rm desc}^{\lambda}(z'),
\]
\[
w\cdot\Delta\ell_i=\mu_i\Delta d_i+\Delta F_i+r_i(z)-r_i(z').
\]
两个S_desc^λ≥0。j=i+1时祖先和为空，丢弃目标的非负r_i(z′)、S_desc^λ(z′)给正确方向的上界；后于第一人的干预仍保祖先损失。

相对于H_i=η_i+μ_i u_i，若z本身是原完整child-SPE源，令s_k(z)=u_k(z)−M(z_{<k})≥0，则
\[
w\cdot\ell_i(z')-H_i\le\mu_i[d_i(z')-u_i]
 +\sum_{i<k<j}\lambda_{i,z_{<k}}[u_k(z)-u_k(z')-s_k(z)]
 +\lambda_{i,z_{<j}}[\Gamma_j-s_j(z)]-S_{\rm desc}^{\lambda}(z').
\tag{EXCESS}
\]
规范源松弛在这里是**减去**，进入收益超过cap的部分仍是有符号、带价格的μ_i[d_i(z′)−u_i]。不能假定它非正。原源的s≥0银行也不能无条件复制到已强制过多个动作的中间叶。这些加权式只在同一个给定对偶和允许raw域内使用，不将旧μ_i/λ_h混入新的全局单μ库存。

## 切线EDGE与不同主题同叶残差

对未来边使用统一净cap对偶
\[
r_i(z)=\eta_i+\mu B_i(z)-w\cdot\ell_i(z)\ge0,
\]
则
\[
w\cdot\Delta\ell_i=\mu\Delta B_i+r_i(z)-r_i(z').
\]
固定原进入主题A，定义其倒数切线误差
\[
E_{i,A}^t(z)=\sum_{x\in A}\frac{(1-t_xc_x(z))^2}{c_x(z)}\ge0.
\]
未来边上进入者一直选A，因此x∈A保证c_x≥1，并且Δc=Δell_i。展开误差为
\(d_i(z)-2\sum_{x\in A}t_x+w_A\cdot c(z)\)，得
\[
-w_A\cdot\Delta\ell_i=\Delta d_i-\Delta E_{i,A}^t.
\]
合并得到精确边量
\[
\boxed{-(w_A-w)\cdot\Delta\ell_i
=\Delta d_i-\Delta E_{i,A}^t
 +\mu\Delta B_i+r_i(z)-r_i(z').}
\tag{EDGE}
\]
固定B_i与r_i的差在同一保守流上望远镜；剩下的进入者切线收益工作不能从NET-TELE自动消失。逐边取祖先损失或后继盈余的正部会破坏原本可用的相消。

若本次角色j复制原进入主题，即y_j=A，则在新叶z′中进入者和j选同主题，单位提供者分得相同收益，故
\[
\Delta d_i+\Gamma_j=u_j(z)-d_i(z).
\]
一般目标y_j却给
\[
\boxed{\Delta d_i+\Gamma_j=u_j(z)-d_i(z)
 +[d_i(z')-u_j(z')].}
\tag{PAIR}
\]
方括号是**同一叶中两个不同完整主题**的收益差，没有已证的固定符号。仅有鞍点输入价格相同或价格支持条件不提供这个实际终局收益差的符号。将所有y_j换成A虽恢复copy相消，却改变已选Q_i及其端点势银行，不能继续引用原Q_i的NET-TELE。

最后静态进入改写A→y_i的删除负载功为零，对偶只给
\[
0=\mu\Delta B_i+r_i(z^{\rm pre})-r_i(y).
\]
把此零项加到总和才能使净势/约化成本到达真实Q_i。此最后边不能使用上面的固定A切线恒等式或进入者IC；改写后当前主题已不是A，甚至A中的某些客户可能全不被覆盖。

## raw坐标流的逆鞅式与累计前缀

在所有实际行共享同一个A∼p，源未来动作均为原σ在各自h_i,A后的真实动作。独立抽联合目标Y，其每行边际就是给定Q_i。选固定次序逐一替换所有未来动作单元，同一行依时间顺序，最后各行换进入标签。未来单元总数N=m(m−1)/2。

置v_A=t⊙1_A、v=E v_A。第k个单元的源/目标动作加权向量为b_k=t⊙1_source、c_k=t⊙1_target。令
\[
\mathcal G_k=\sigma(Y,\text{第k步后仍未擦除的源动作单元}),
\quad M_k=E[v_A\mid\mathcal G_k],\quad
\delta_k=M_{k-1}-M_k.
\]
这里M_k是条件期望过程，与规范门槛函数M(h)区分。这是递减信息集，目标独立性给M_N=v。有限条件期望投影和增量正交给
\[
\sum_kE\|\delta_k\|^2=E\|M_0-v\|^2
\le V_p:=E\|v_A-v\|^2.
\tag{ENERGY}
\]
b_k−c_k是\(\mathcal G_{k-1}\)可测；总删除负载在第k层是\(\mathcal G_k\)可测。逐边条件期望和有限换序因此准确给
\[
\mathrm{Cov}=\sum_kE\langle M_{k-1}-v,b_k-c_k\rangle
=\boxed{\sum_lE\left\langle\delta_l,
                  \sum_{k\le l}(b_k-c_k)\right\rangle}.
\tag{PREFIX}
\]
后一式用M_{k−1}−v=Σ_{l≥k}δ_l。每个信息增量乘的是**全部已替换前缀**的向量；(ENERGY)没有给这个前缀乘子的范数或其与δ_l的有符号配对界。不能删除乘子，也不能为同一增量的多次出现反复领取V_p/2。

raw与真重放逐(A,y)起终点相同，固定A的线性自适应shadow是终局状态函数，故(PREFIX)等于真流总有符号功。它不使raw边拥有原IC，也不让两条流逐边有相同银行。

另一个逐行raw变体可在该行每次替换后按原条件律law(A｜剩余旧源后缀)刷新进入标签；目标独立且此前替换只擦除源单元，条件塔保证**当前标签与raw尾的完整联合分布**刷新前后相同，任意raw统计期望不变。尾全部替换后仍须最后改成目标标签以到达Q_i。刷新后的标签已不一定是原固定源A，不能无代价将EDGE/PREFIX的原源权w_A改为刷新权；这种刷新没有证明减少原协方差总额。

## 一个自足的half充分金额接口

为准确保留源中的未证目标，另加以下明确接口条件：Q_i是统一净cap域在共同shadow w的最优解，L=(1/m)Σ_iE_Q ell_i；取t_x=1/(1+L_x)，p支持在最大主题t价格上，\(\gamma=\max_T\sum_{x\in T}t_x\)。这些是这一付款接口的附加条件，流构造本身不需要它们。

定义原源曲率余量
\[
D=\sum_iE_A\sum_{x\in A}
\frac{t_x^2(\ell_i(z_A)_x-L_x)^2}{1+\ell_i(z_A)_x}\ge0,
\]
并用算法对象中的I=I_total及同一对偶差G≥0。倒数的精确二次展开给
\[
\boxed{W-m\gamma=I+G+D-\mathrm{Cov}.}
\tag{LEDGER}
\]
例如逐客户用\(1/(1+\ell)=t-t^2(\ell-L)+t^2(\ell-L)^2/(1+\ell)\)，求原源期望；平均权ρ产生G，中心化权产生Cov。G=μI+μS_total+R是同一G的细分，不能再额外相加为新钱。

L是质量m−1的合法分数主题负载，故
\[
Q_{\rm stat}=(m-1)\gamma-\sum_xL_xt_x\ge0,
\qquad\mathrm{OPT}_m\le(2m-1)\gamma-Q_{\rm stat}.
\]
后一式逐客户用\(1_{c_x^*>0}\le(c_x^*+L_x)/(1+L_x)\)，再对最优m主题的价格各用γ即可。因此足以证明但本批**尚未证明**
\[
\boxed{\mathrm{Cov}\le I+G+D+\tfrac12(\gamma+Q_{\rm stat}).}
\tag{PAY?}
\]
一旦(PAY?)对这一接口成立，(LEDGER)给2W≥(2m−1)γ−Q_stat≥OPT_m；目前没有由已证流、Γ、半库存条件或(ENERGY)得到该金额界。source/arrival容量、跨行前缀势兼容和任意目标同叶残差均须在同一预算内处理。

m=5时N=10，所需是W≥(9γ−Q_stat)/2；m=6时是W≥(11γ−Q_stat)/2。这是本接口未闭合的条件，不表示五人half仍开放：现行[五人半覆盖定理](../定理/五人半覆盖--定理.md)已由另一份精确证书证明，不能由旧探索稿的历史OPEN标签覆盖它。当前任意目录恰六人的完整历史目标亦未由这些流公式解决。

## 完整槽边界、审查与下一步

若改用完整分数w⋅c，最后进入改写的功是\(w\cdot(1_{y_i}-1_A)\)，必须保留；零功结论只对删除同一i槽成立。给完整槽约化成本r_i^+=η_i+μB_i−w⋅c，转换成删除槽成本为r_i^−=r_i^++w⋅1_{z_i}。各原源共用A∼p时转换的原源储备总差为
\[
\sum_iE_p(r_i^--r_i^+)=m\sum_x\rho_x^2t_x^2.
\]
这是既有完整槽自交叠范数银行的同一项，不能漏掉最后边或作为第二份独立信用。完整槽自己的静态系数与银行仍须按其自身域使用。

两主源已全文实读；比较均匀copy/swap、raw-tail、mean-floor、固定前缀、完整槽范数、跨历史净cap以及两份后续内部审查，确认这些符号/范围修订均被原文明确限制。当前新正文保留原内部审查的已读来源身份，不称本批盲审；未运行随机搜索、固定规模证书或别的已成功原程序。证据与逐语义去向见[资源合同](../../tools/evidence/real-replay-covariance-history/README.md)。相关五人正式定理只读取模型范围与闭合恒等式作状态比较，未假称本批重审其整个证书。

已证真实流、固定势相消和条件[行动平衡半库存界](../引理/同前缀行动平衡交换的半份约化成本界--引理.md)可继续使用；开放的是它们能否在原所选端点律与原源容量下支付(PAY?)。本对象保未完成数学及其确切缺口，没有将尚未证明的式子退休，也没有用新银行替换所选Q_i。关系已解释，正式超图留第三阶段。
