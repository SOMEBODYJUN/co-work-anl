---
id: customer-attraction/free-fractional-saddle-true-menu-mean-kkt-remainder
kind: lemma
type_tag: 引理
title: 自由分数鞍点的真实菜单均值KKT余量
status: exact-static-lower-bound-and-ledger-proved; actual-common-payment-unproved
summary: 真正free-fractional鞍点给H_q≥H_(q_i)，位置均值查询F_i−δ为非负KKT项加倒数曲率；明确q_i来自同σ删当前菜单，SC不自带防御KKT，真实IC只付相关对角，负κ仍须共同付款。
source_refs:
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round4_general/security/README.md
---

# 真正自由背景鞍点，不是自洽点或任取查询

有限单位客户N、有限非空共同标签目录S、m≥2单位提供者；保空/同覆盖标签、重复行动、零客户和所有有序历史平局。令k=m−1，p和q均为目录上的概率分布，p_x和q_x分别为覆盖客户x的边际。定义
\[
\Phi(p,q)=\sum_x\frac{p_x}{1+kq_x},\qquad
\delta_m=\min_q\max_{A\in S}\sum_{x\in A}\frac1{1+kq_x}.
\]
固定一个真正鞍点(p*,q*)：p*在q*下为最佳查询，q*全局最小化固定p*的凸目标；共同值δ_m。有限单纯形紧、对p线性对q凸连续保证这种分析鞍点存在。它不是原游戏随机SPE，q*也不要求由真实后继实施。

这里比池化自洽p所需的“p支持为q(p)下最佳查询”多了背景最优条件。SC不规定q(p)是p下最优防御，故不能给任一SC自动套下文KKT；任取已知坏p也未必是此p*。3885B入口的这条数学现完整重推，不重授固定点/KKT理论或一般福利结论。

# 同一原策略的实际位置均值

固定完整有序历史纯SPE σ，actual叶B、利润u_i与W=Σu_i。actual位置i强制A后仍沿同σ真完成Z_i(A)，删当前i槽得m−1竞争行动V_i(A)，其负载L_i(A)_x。A~p*；定义真实竞争行动的平均概率
\[
(q_i)_T=\frac1k\,\mathbb E_A\#\{j\ne i:Z_i(A)_j=T\},
\quad \mu_{ix}=\mathbb E_A L_i(A)_x=k(q_i)_x.
\]
q_i是合法目录概率分布，所有旧前缀和真实后继都计入，只删当前一次。不同同覆盖标签仍保真实历史及后继，不能合并成同一动作。定义位置均值分数查询
\[
F_i(p^*)=\sum_x\frac{p_x^*}{1+\mu_{ix}}.
\]
这先对A平均负载再倒数，并让查询覆盖用独立p*边际；不是原相关对角收益，也不是倒数后取期望。

# 精确KKT/曲率分解及符号

令 \(D_x=1+kq_x^*\ge1\)、\(H_T=\sum_{x\in T}p_x^*/D_x^2\)、\(H_q=\sum_Tq_T^*H_T\)。沿任意目录分布s，固定p*的方向导数为
\[
\left.\frac d{d\varepsilon}\Phi(p^*,(1-\varepsilon)q^*+\varepsilon s)
\right|_{0+}
=k(H_q-H_s)\ge0.
\]
这是q*最小化固定p*凸目标的一阶条件。因此H_q≥H_s对所有s，特别H_q≥H_(q_i)；q*的正支持都落在H_T最大主题上。不是“p*的最佳查询”那条KKT方向。

逐客户精确倒数展开
\[
\frac1{1+\mu_i}-\frac1D
=-\frac{\mu_i-kq^*}{D^2}
+\frac{(\mu_i-kq^*)^2}{(1+\mu_i)D^2}
\]
乘p_x*求和，用Φ(p*,q*)=δ_m，得
\[
\boxed{F_i(p^*)-\delta_m
=k[H_q-H_{q_i}]
+\sum_x\frac{p_x^*(\mu_{ix}-kq_x^*)^2}
{(1+\mu_{ix})D_x^2}\ge0.}\tag{KKT-MEAN}
\]
两个非负项分别来自背景最优方向及倒数曲率，不使用SPE。全目录空或零客户时全0；分母恒正，不除W/δ。m1另直接最优，无需构造1/k的q_i。

# 真IC仍只付相关对角

为自足定位未付项，令A,T独立同分布p*：
\[
D_i^{\rm true}=\mathbb E_A\sum_{x\in A}\frac1{1+L_i(A)_x}\le u_i,
\quad
C_i=\mathbb E_{A,T}\sum_{x\in T}\frac1{1+L_i(A)_x}.
\]
设e_i=u_i−D_i^true≥0、κ_i=D_i^true−C_i（符号自由）、J_i=C_i−F_i≥0，末个符号是倒数Jensen。则
\[
\boxed{W-\sum_iF_i=\sum_i(e_i+\kappa_i+J_i).}\tag{TRUE-LEDGER}
\]
再加KKT-MEAN各位置余量，
\[
W-m\delta_m=\sum_i(e_i+\kappa_i+J_i)
+\sum_i(F_i-\delta_m).
\]
KKT给的是每F_i≥δ的**静态下界**，不是u_i≥F_i。真实后继观察已实现A使κ可能负；列出所有非负余项不自动共同支付它们。不可将e_i、J_i、KKT曲率在同一余额中再重复领取。

该域是完整自由背景k conv(S)。[共享菜单Gram/KKT页](共享真实菜单的等价格Gram核与KKT协方差分解--引理.md)使用更小的真实菜单共享K，虽有同类精确分解，值γ/背景/信用不必等于此δ/q*；不能只继承其中有利项。[真实query运输账](真实查询运输的完整收益对偶与切线误差合同--引理.md)也说明固定p/背景的完整余额不会因改主题—角色运输免费改善。

# 静态常数只给条件桥

任意固定q、M=max_AΣ_(x∈A)1/(1+kq_x)，对最优m元组覆盖重数d_x，用1_(d_x>0)≤(d_x+kq_x)/(1+kq_x)，求和得OPT_m≤mM+kM=(2m−1)M；取最优q给
\[
\mathrm{OPT}_m\le(2m-1)\delta_m.
\]
所以若另证W≥mδ_m，得OPT≤(2−1/m)W；较弱W≥(m−1/2)δ_m便足half。KKT-MEAN没有证明这两付款。m5强桥给条件9/5，弱桥需9δ_5/2；当前五人half别证不回填这些更强接口，m6弱桥需11δ_6/2，同样不由本恒等式解决。

已有[PB标准平台](../反例/PB标准分数鞍点的真实前三步平台--反例.md)在任意合法高背景下连续三个真实节点δ不变且u<δ，否任意背景逐人/局部链助手；不是原根聚合反例。后银行零根逐人反族又是另一证据。旧635的all-p全角色池化反例，也不能因KKT存在就删掉其负去相关或将它当此最优p*失败。

一般证明来自上述导数及精确倒数式，0原程序/新checker。原入口全部历史/发现器/证据与PB/SC分流见[资源](../资源/池化背景发现器与安全分支入口的证据层--资源.md)；没有新普遍福利、反例或新颖性认证。
