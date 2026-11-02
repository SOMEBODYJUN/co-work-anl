---
id: "customer-attraction/full-client-coordinate-inventory-two-budget-initialization"
kind: "lemma"
type_tag: "引理"
title: "全客户坐标库存的双预算初始化"
status: "original-raw-cap-initialization-proved; residual-full-SAFE-payment-unproved"
summary: "任意比较T的四价身份给同一逐客户库存/原正边容量可行点，current与actual正列各由一份u支付；保原RAW-cap及full-profit SAFE接法，后加强密度守卫不能倒填原实现。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round7/parent/optimal_coordinate_initialization.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round7/parent/optimal_coordinate_initialization.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round7/coupling/optimal_coordinate_inventory_blind_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round7/coupling/optimal_coordinate_inventory_blind_review.md"
---

# 全客户坐标库存的双预算初始化

## 模型与结论范围

有限单位客户、有限非空共同主题目录、任意m≥1名单位提供者，客户最终在覆盖者间均分。固定每个有序历史上的纯SPE σ，actual终局B=(B₁,…,Bₘ)、客户负载c_B、覆盖C及各利润uᵢ。保空主题、重复、零客户和任意离轨平局。任取合法比较m元组T（可重复），并集O、负载c_T；T不要求是SPE，初始化不需最优性，只有最后取最优时才将|O|识别为OPTₘ。

[5680B提出稿](../../tools/evidence/optimal-coordinate-initialization-five-primary/original/c2f441d2e775cb90335d/optimal_coordinate_initialization.md)及[6472B合同重构](../../tools/evidence/optimal-coordinate-initialization-five-primary/original/2b23e55ba6420a0ce7c7/optimal_coordinate_inventory_blind_review.md)全读。本页保原RAW-cap下明确比例分割、两已付预算与full-customer SAFE接续；一般初始化存在性后来已由[更强边界定理](../定理/同客户来源保持流的加强初始化与节点密度--定理.md)覆盖，不重授为新结果。原选择的每条边较弱，不能反向视为后者的密度输入合同。

## 四价坐标身份：reference是T，actual是B

对x∈Tᵢ定义

\[
p_{ix}=1/c_T(x),\quad \delta_{ix}=c_B(x)+1-\mathbf1_{x\in B_i},\quad
W_i=\operatorname{finish}_\sigma(B_{<i},T_i),\quad z_{ix}=1/c_{W_i}(x).
\]

c_T、δ、c_W均≥1；x不在Tᵢ时所有来源项取0，不定义无关零分母。下标δ是客户分母，与整行current dᵢ不同。四类非负价格为

\[
\begin{aligned}
P^B_{ix}&=\sum_{\ell\ne i:\ x\in B_\ell\setminus T_\ell}\frac1{c_T(x)\delta_{ix}},&
N^B_{ix}&=\sum_{\ell\ne i:\ x\in T_\ell\setminus B_\ell}\frac1{c_T(x)\delta_{ix}},\\
q_{ix}:=P^W_{ix}&=\sum_{j>i:\ x\in(W_i)_j\setminus B_j}\frac1{\delta_{ix}c_{W_i}(x)},&
N^W_{ix}&=\sum_{j>i:\ x\in B_j\setminus(W_i)_j}\frac1{\delta_{ix}c_{W_i}(x)}.
\end{aligned}
\]

去掉当前i后reference T到静态B-other，负载差给1/c_T−1/δ=Pᴮ−Nᴮ；静态B-other到真实Wᵢ，因过去actual前缀相同，只剩future差，给1/δ−z=q−Nᵂ。两式相加：

\[
\boxed{p_{ix}=z_{ix}+P^B_{ix}-N^B_{ix}+q_{ix}-N^W_{ix}.}\tag{COORD}
\]

这里无逐客户IC，无off-history松弛重权，也没假设比较T本身理性。固定x∈Tᵢ，令n_B=# {ℓ:x∈Bℓ\Tℓ}；因为i是T-coverer，n_B≤c_B−1_(x∈Bᵢ)=δ−1，故Pᴮ=n_B/(c_Tδ)≤p，定义rᵢₓ=p−Pᴮ≥0。

## 同一库存与边容量的显式分割

由COORD，r−q=z−Nᴮ−Nᵂ≤z且z≥0，故(r−q)₊≤z。**先对x求和**，再仅用actual i节点对完整合法Tᵢ的一条真实IC：

\[
\sum_x(r_{ix}-q_{ix})_+\le\sum_{x\in T_i}z_{ix}
=u_i(W_i)\le u_i.
\tag{DEFICIT}
\]

设rᵢ=Σrᵢₓ，Sᵢ=Σmin(rᵢₓ,qᵢₓ)=rᵢ−Σ(r−q)₊，bᵢ=(rᵢ−uᵢ)₊。则0≤bᵢ≤Sᵢ。Sᵢ>0时取

\[
a_{ix}=\frac{b_i}{S_i}\min(r_{ix},q_{ix});
\]

Sᵢ0时全取0。每条原future边

\[
q^W_{ijx}=\frac{\mathbf1_{j>i,\ x\in(W_i)_j\setminus B_j}}
{\delta_{ix}c_{W_i}(x)}
\]

在qᵢₓ>0时取aᵢⱼₓ=aᵢₓqᵂᵢⱼₓ/qᵢₓ，否则全0。于是同一个点同时有aᵢₓ≤min(r,q)、0≤aᵢⱼₓ≤qᵂᵢⱼₓ、Σⱼaᵢⱼₓ=aᵢₓ。current cᵢₓ=rᵢₓ−aᵢₓ非负，且

\[
\boxed{p_{ix}=P^B_{ix}+c_{ix}+\sum_{j>i}a_{ijx},\qquad
 d_i:=\sum_xc_{ix}=\min(r_i,u_i)\le u_i.}\tag{INIT}
\]

cᵢₓ的x是来源库存标签，不要求x∈Bᵢ；dᵢ由actual i的一次整行利润付款，不能把它变成actual(i,x)物理客户券。uᵢ0时dᵢ0，整行系数定义0；空Tᵢ全为0，m1无recipient且比较收益≤u₁，所以b₁0；所有比例仅在正S/q使用。有限输入均有理，选择可事先固定，不按随机后续轨迹事后挑源。

future进入严格j>i的真实prescribed context (Wᵢ,<j,j)，该context规定叶确为Wᵢ。源客户满足x∈(Wᵢ)ⱼ且x∉Bⱼ，只是**对接收角色的新客户**，可能已被别的actual角色覆盖；不能称全局fresh R。

## 第二预算列界与精确未付余量

将Pᴮ按各recipient收成Hℓₓ。若x∈Bℓ\Tℓ且x∈O，则Hℓₓ=Σ_(i:x∈Tᵢ)pᵢₓ/δᵢₓ，δᵢₓ≥c_B(x)>0且Σp=1，所以Hℓₓ≤1/c_B(x)；其余x处H0。于是

\[
H_\ell\le u_\ell\big(B;(O\cap B_\ell)\setminus T_\ell\big)\le u_\ell.
\tag{COLUMN}
\]

每个O客户在全部T-coverer上的p和为1，全部INIT求和给

\[
\boxed{|O|=\sum_\ell(d_\ell+H_\ell)+\sum_i b_i.}\tag{TWO}
\]

current占第一份actual预算，H占第二份的一部分；future总b仍未付款。将**这同一份**a注入原full-customer SAFE或合法CLIP严格future DAG，重新合并同context输入、计算actual终端A^out，非负守恒给ΣA^out=Σb。它没有保持origin客户标签的承诺。充分目标仍是同一次选择上

\[
A_\ell^{out}\le R_\ell:=2u_\ell-d_\ell-H_\ell\quad\forall\ell.
\tag{RESIDUAL?}
\]

Rℓ≥0，且由COLUMN

\[
R_\ell\ge(u_\ell-d_\ell)+
u_\ell\big(B;(B_\ell\setminus O)\cup(B_\ell\cap T_\ell)\big).
\]

未证的是对每个原实例/每份完整SPE，存在一个**最优T及同一合法分割/路由**满足全部余量；不是声称每T或每路由成立。原source标签i在初始history前i−1等actual，full-SAFE正past出口不早于i；这个时间支持只给[来源后缀必要割](来源因果资金的后缀必要割与定向锥边界--引理.md)，不自动给PRICE/HIT或共同角色cap。

## 与更强守卫、交集直接付款的精确区别

原RAW-cap是1/(δc_W)。后加强定理用qhat=min(p,1/δ)/c_W，并以c_Waᵢⱼₓ≤p作为GENERAL-DENSITY输入。旧比例点只知aᵢₓ≤p及aᵢⱼₓ≤1/(δc_W)，**不能无证继承**这个更强逐边条件。加强后仍可做极大current、d=min(r,u)，但a/I-R拆分可以改变，必须重算后续J/流，不能只因d相同就说两个点相同。

本页full-SAFE重采全部客户，与后来的同客户流、R-only自然图不是同一kernel。进一步用[同actual客户I互补券](最优交集客户的互补付款与新鲜余量接口--引理.md)直接支付I-future是合法的新出口，但须从续流删除同一a，且不自动满足原限定full-SAFE RESIDUAL或恢复它的源时间合同。不能对一份I未来质量既领J又保旧传播。

普遍初始化/ROW/COLUMN/客户总库存是已证组件；Σ已付+未付=|O|不是新的福利界。当前[五人half](../定理/五人半覆盖--定理.md)已独立成立，不说明本特定余量接口已付；六人/一般共同付款仍未由本引理解决。原审查/348有限实现的准确层次在[来源资源](../资源/坐标初始化原实现与合同审查的范围--资源.md)。
