---
id: "customer-attraction/shared-menu-equal-price-gram-and-kkt-covariance"
kind: "lemma"
type_tag: "引理"
title: "共享真实菜单的等价格Gram核与KKT协方差分解"
status: "exact-geometric-identities-proved; common-half-slot-payment-unproved"
summary: "同一原策略共享菜单鞍点给共同Gram核、非负KKT信用及C=Vcorr−G；half只需余gamma/2，但等价几何不是已付金额，未把原SPE移植到切线游戏。"
source_refs:
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round11/geometry/shared_saddle_geometry_checkpoint.md"
---

# 只在同一原策略共享菜单域取鞍点

原稿f628126751d47bbb0ff3为4753B全文。有限单位客户N、有限非空共同目录S、m≥1名单位提供者、任意全部有序历史完整纯SPE σ；容许空主题、重复行动、零客户及任意离轨平局。固定actual主题B_i、利润u_i与福利W=Σu_i。位置i在actual有序前缀强制A、后继沿同一σ，删掉该当前i槽后其他m−1槽的客户负载记L_i(A)，原当前真收益
\[
 d_i(A)=\sum_{x\in A}\frac1{1+L_i(A)_x}\le u_i.
\]
绝不冻结实际尾或改变当前query后仍取旧后继。

取有限紧凸共享背景域
\[
 K=\frac1m\sum_{i=1}^m\operatorname{conv}\{L_i(A):A\in S\}.
\]
每个L都是m−1份目录行动的合法分数负载。定义
\[
 F_p(L)=\sum_x\frac{\rho_x}{1+L_x},\qquad
 \rho_x=\Pr_{A\sim p}(x\in A).
\]
p在有限目录单纯形，F对p线性、对L凸连续，故有限维凸minimax给一个真正鞍点(p*,L*)，其值γ。此为分析对象，不是原策略中隐藏的随机化。p*的支持并非任取喜欢的主题：令t_x=(1+L*_x)^{-1}，则
\[
 g_t(A):=\sum_{x\in A}t_x\le\gamma\quad(A\in S),
 \qquad g_t(A)=\gamma\quad(p^*(A)>0).
\]
这些等价格事实来自p*在固定L*上的最大化。与后来扩大mean-cap端点域、raw/floor域或行动对齐域比较时，必须同时重建L*、γ和所有信用，不能只继承较好系数。

# 真实收益的共同Gram表示

在同一个有限客户欧氏空间，定义
\[
 v_A=t\odot\mathbf1_A,\quad v=\mathbb E v_A=t\odot\rho,
 \quad w_i(A)=t\odot L_i(A),\quad h=t\odot L^*=\mathbf1-t.
\]
只在x∈A上用c_i(A)_x=1+L_i(A)_x≥1。逐客户恒等式
\[
 \frac1c=2t-t^2c+\frac{(1-tc)^2}{c}
\]
相加给
\[
 d_i(A)=2g_t(A)-\|v_A\|^2-\langle v_A,w_i(A)\rangle+D_i(A),
\]
\[
 D_i(A)=\sum_{x\in A}\frac{(1-t_xc_i(A)_x)^2}{c_i(A)_x}\ge0.
\tag{TAN}
\]
所以主题间有一个共同PSD Gram核G(A,B)=〈v_A,v_B〉。然而正支持只固定||v_A||_1=γ，不固定||v_A||²；不能从等L1价格推出相同self交互。令
\[
 s=\mathbb E\|v_A\|^2=\sum_x\rho_xt_x^2.
\]
由t_xL*_x=1−t_x，精确得〈v,h〉=γ−s。这是同一个真实收益的分解，不声称σ在切线二次游戏中也是SPE；若跨原离轨history用原IC，必须带上相应两真实叶的误差差。

# KKT付了去相关方向，未付query相关部分

固定p*，L*最小化F_p。负梯度为−t²⊙ρ=−t⊙v。把L*按K定义写为各行凸组合的平均；线性一阶条件迫这些行凸组合只支持最大化〈v,w_i(B)〉的列。若
\[
 M_i=\max_{B\in S}\langle v,w_i(B)\rangle,
\]
则Σ_iM_i=m〈v,h〉。因此对query分布p*有明确的非负余量
\[
 G_{KKT}=m\langle v,h\rangle
       -\sum_i\mathbb E_A\langle v,w_i(A)\rangle\ge0.
\tag{KKT}
\]
这份KKT在同一共享域里真实成立；没有加入新的博弈IC。

中心化切线债与query-response协方差为
\[
 C=\sum_i\mathbb E_A\langle v_A,w_i(A)\rangle-m\langle v,h\rangle,
\]
\[
 V_{corr}=\sum_i\mathbb E_A\langle v_A-v,w_i(A)\rangle.
\]
直接加减同一个Σ_iE〈v,w_i(A)〉即得
\[
 \boxed{C=V_{corr}-G_{KKT}.}\tag{GEO}
\]
KKT控制去相关的平均方向，尚未控制后继看见已实现A之后的相关响应。因此PSD或等价格不推出Vcorr≤0、C≤0。原稿提到已有C>0的保险例，本批未读它的原始数据/程序或重跑；本结论也不依该例，更不由一句旧实例报告证明任何路线不可能。

# half-slot的准确充分目标

令I=Σ_i[u_i−E_A d_i(A)]≥0、D=Σ_iE_A D_i(A)≥0。对(TAN)求和，使用支持上g=γ、〈v,h〉=γ−s，得到
\[
 \boxed{W-m\gamma=I-C+D.}\tag{BAL}
\]
由此W≥mγ需要C≤D+I，但half的充分要求更弱：
\[
 C\le D+I+\gamma/2,
\quad\text{等价地}\quad
 V_{corr}\le D+I+G_{KKT}+\gamma/2.
\tag{HALF-SLOT?}
\]
**这条未被证明。** 足够的量词是每份输入及完整σ存在一个上述合法共享鞍点，使同次定义满足付款；并非已证所有非唯一鞍点都满足。γ/2是允许的误差金额，不是已发现可领取的实际钱包。

为自足说明其充分性，取任意最优m主题元组T、客户覆盖次数a_x与并集O。每个x∈O有a_x≥1，故
\[
 1\le(a_x+L_x^*)t_x.
\]
求和、对m个比较主题各用g≤γ，再对L*的m−1份合法分数行动也用同一价格上界，得到
\[
 OPT_m\le\sum_jg_t(T_j)+\sum_xL_x^*t_x
          \le m\gamma+(m-1)\gamma=(2m-1)\gamma,
\]
于是若(HALF-SLOT?)成立，(BAL)给2W≥(2m−1)γ≥OPT_m。只得到较强充分路线，不说half必反推这条付款。

m5代入需W≥9γ/2；后来五人half已另证，不替本共享域付款补证。m6需W≥11γ/2，本稿未解决。m1时K={0}、t=1，原单人IC给W=γ=OPT1；没有m−1倒数。零客户/全部空主题所有量0，以上不除γ或W，退化域保留。

# 方差不匹配及下一真实义务

因E(v_A−v)=0，把w_i(A)换为w_i(A)−h不改变Vcorr。普通Cauchy/Young只能先得query向量方差与**完整响应向量**方差的乘积/和；而
\[
 D_i(A)=\sum_{x\in A}
 \frac{t_x^2(L_i(A)_x-L_x^*)^2}{1+L_i(A)_x}
\]
只在被当前query覆盖的坐标计误差，并带各自真分母。query未覆盖坐标的后继响应变化不进这条D，却仍可进中心化协方差。因此不能将完整欧氏响应方差无证明地由D替代。这是对象不匹配的定位，不是PSD/几何方法不可能定理。

[实际切线银行](../候选/实际负载切线银行与共同误差付款--候选.md)后来在**同一原菜单K**提供了明确B_act≤γ/2，但T-PAY仍要求把真实跨历史债映到那一份银行；本页γ/2许可额本身没有完成映射。[单查询凸化候选](../候选/单查询凸化代价与共同付款条件--候选.md)的固定w恒等式也不能删除w_i(A)的适应性。各页的端点域、KKT信用和付款金额须保持同次定义，不能混用有利项。

原稿六节全部保，已证的是(TAN)/(KKT)/(GEO)/(BAL)及静态价格界；未证的是共同HALF-SLOT。无新有限扫描、原程序run、外审/盲审/新颖性声明或half反例。精确原件及比较范围见[本批证据](../../../../tools/evidence/cag-common-client-price-and-shared-saddle-primary/README.md)。
