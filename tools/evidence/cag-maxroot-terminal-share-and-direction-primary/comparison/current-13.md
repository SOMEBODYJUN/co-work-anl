---
id: "customer-attraction/same-prefix-action-balanced-swap-half-reserve"
kind: "lemma"
type_tag: "引理"
title: "同一前缀行动平衡交换的半份约化成本界"
status: "proved-conditional-signed-bound; covariance-flow-balance-and-capacity-unproved"
summary: "完整raw端点域中交换进入者与第一后继，精确消去深尾门槛；同行同前缀行动平衡给μΣθ(d−v)≤半份源约化成本。原源容量、全树平衡与协方差映射仍须另证。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round12/tree/uniform_swap_and_raw_flow_independent_review.md#2"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round12/credible/uniform_copy_swap_component.md#3-5"
---

# 同一前缀行动平衡交换的半份约化成本界

## 模型、固定行及对偶合同

沿用[真实后继重放算法](../算法/固定进入槽的真实后继重放与一次势预算--算法.md)的原共同目录单位客户模型、规范max-min门槛M(h)、固定角色i<m与同一合法前缀h_i。raw叶可选任何进入主题和未来主题，全部实际行动标签已放行；它们不必是原σ续局或SPE。

记
\[
B_i(z)=d_i(z)+\sum_{k>i}[M(z_{<k})-u_k(z)],\qquad
r_i(z)=\eta_i+\mu_iB_i(z)-w\cdot\ell_i(z)\ge0
\]
对所有这些raw叶成立，μ_i≥0、η_i实数、w固定。其来源可为**显式合并**进入收益和未来门槛的单行净cap LP；不能将任意历史乘子λ_h自动改为同一μ_i。

对偶在每个raw变量上的不等式并不要求该raw叶单独满足期望cap。交换后的叶可以不是SPE，也可以不作为单点分布满足cap，仍可用r_i(zswap)≥0；若原对偶域排除了该标签/端点，则下面的引用不合法。

## 第一后继交换的精确恒等式

写z=(h_i,A,B,Y)，zswap=(h_i,B,A,Y)，d=d_i(z)，v=u_{i+1}(z)。最终完整主题计数不变；进入者和第一后继的终局收益交换，其他玩家收益不变。两动作后所有更深前缀的计数也不变，故对应M相等。

理由是M由全部可实现子SPE终局集合定义：同计数历史的后缀博弈同构，映射保收益与全部行动。这里只识别**全集门槛**，没有令固定σ在两个同计数有序历史采用同一续局。

因此
\[
B_i(zswap)-B_i(z)
=2(v-d)+M(h_i,B)-M(h_i,A),
\]
\[
\ell_i(zswap)-\ell_i(z)=\mathbf1_A-\mathbf1_B.
\]
设同一行的主题势
\[
P_i(T)=w\cdot\mathbf1_T+\mu_iM(h_i,T),
\]
则直接减约化成本得
\[
\boxed{r_i(zswap)-r_i(z)=2\mu_i(v-d)+P_i(B)-P_i(A).}
\tag{SWAP}
\]
第二个μ_i(v−d)来自未来总收益中第一后继的反向变化，不可漏掉；这也是下面因子1/2的来源。

## 行动平衡和原源容量是两项条件

取有限个同一行/同一前缀的源叶z_e=(h_i,A_e,B_e,Y_e)及θ_e≥0，要求对**每个合法主题**T
\[
\sum_{e:A_e=T}\theta_e=\sum_{e:B_e=T}\theta_e.
\tag{BAL}
\]
即从进入行动到第一后继行动的有向流在每主题平衡。于是Σ_eθ_e[P_i(B_e)−P_i(A_e)]=0，(SWAP)相加给
\[
\boxed{\mu_i\sum_e\theta_e(d_e-v_e)
=\tfrac12\sum_e\theta_e[r_i(z_e)-r_i(zswap_e)]
\le\tfrac12\sum_e\theta_er_i(z_e).}
\tag{HALF-R}
\]
只用θ非负和交换目标的r_i≥0；没有除以μ_i，μ_i=0同样成立。左侧是**有符号总差**，不允许替换为Σθ(d−v)_+、逐边绝对值或所有祖先损失正部。

若要进一步把右侧支付为原σ源分布P_i(z)=Pr_{A∼p}[z_A=z]的半份库存，还必须有逐端点容量
\[
\sum_{e:z_e=z}\theta_e\le P_i(z)\quad\text{对所有原源叶z},
\]
并且所有计价r_i、μ_i来自同一对偶。由r_i≥0才可推出右侧≤\(\tfrac12E_{P_i}r_i\)。中间重放叶没有自动获得新的P_i质量，不能每遇到一次便再领取同一r库存。

行动平衡和源容量均未由已构造的真实协方差流证明；也尚无将该协方差总功映成左侧有符号短缺的合规映射。只在不同行求和后得到行动平衡仍不足：P_i的M(h_i,T)依赖不同行的实际前缀，统一μ也不会令它们成为同一势。这里保留精确条件引理，不把这些未决义务写成已满足。

## 完整槽和较远角色的版本

若本域另用完整负载分数w⋅c(z)并有自己的
\[
r_i^+(z)=\eta_i+\mu_iB_i(z)-w\cdot c(z)\ge0,
\]
交换保持c完全不变，故
\[
r_i^+(zswap)-r_i^+(z)
=2\mu_i(v-d)+\mu_i[M(h_i,B)-M(h_i,A)].
\]
相应P_i^+(T)=μ_iM(h_i,T)，没有w⋅1_T项。同样的行平衡给(HALF-R)，须用完整槽域**自己的**r_i^+与源容量，不能把它当作删除槽r库存之外又一份钱。

更一般，raw交换进入行动A与未来角色j>i的行动B_j，保其他位置动作不动。令
\[
T_i(z)=\sum_{k>i}M(z_{<k}).
\]
最终计数相同，只交换进入者和j的收益，故
\[
\Delta B_i=2(u_j-d_i)+\Delta T_i,
\]
\[
\Delta r_i=2\mu_i(u_j-d_i)+\mu_i\Delta T_i
 +w\cdot\mathbf1_{B_j}-w\cdot\mathbf1_A.
\]
较深门槛的总差ΔT_i必须保留；这只是固定势恒等式，尚未给一个满足容量与守恒的远距swap流。第一后继的特殊性是所有更深计数已一致，只剩两个第一孩子门槛。

## 总利润守恒与接续边界

固定过去负载，令U_i(z)=Σ_{k≥i}u_k(z)为剩余玩家总利润，则
\[
B_i(z)=2d_i(z)-U_i(z)+T_i(z),\quad
\Delta B_i=2\Delta d_i-\Delta U_i+\Delta T_i.
\]
这解释交换中的双系数，也说明资源总利润守恒没有消去规范门槛重置。U_i已通过未来盈余进入净成本，不能在同一付款中再当独立银行花一次。

本引理对任意人数和目录成立，前提是固定行、明确的raw对偶、行动平衡及所需源容量；m=5或m=6不自动提供这些条件。原内部review核过符号、1/2、μ_i=0及完整槽区别，本次全文实读后重构，未把原内部审查改称本批盲审或外审。两主源及相关定义的原字节与身份在[证据](../../tools/evidence/real-replay-covariance-history/README.md)。与真实流的关系是可尝试的**条件支付工具**，而非已证明该流满足其条件；第三阶段应按此语义登记。
