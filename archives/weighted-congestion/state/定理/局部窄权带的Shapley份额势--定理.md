---
id: "weighted-congestion/local-band-shapley-envelope"
kind: "theorem"
type_tag: "定理"
title: "局部窄权带的Shapley份额势"
status: "proved"
summary: "Shapley普通份额随权增加、每权份额随权减少，给资源局部潜在用户权比R的R-PNE及严格R改善下降。"
review_status: "independent algebraic reconstruction and finite exact audit; unrefereed"
legacy_ids:
  - "WC-R3-DENSE-SHARE v1"
  - "WC-R3-DENSE-LOCAL v1"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/weighted_congestion/weight_bands/README.md#the-resource-set-potential-and-its-exact-marginal"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/weighted_congestion/weight_bands/README.md#exact-positive-coefficient-proof-of-the-share-ordering"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/weighted_congestion/weight_bands/README.md#resource-local-r-pne-lemma"
---

# 局部窄权带的Shapley份额势

## 集函数、精确边际和效率

给有限非空正实权用户集S、非负系数多项式c，写W(T)=Σ_{i∈T}w_i、F(x)=xc(x)，故即使c有常数项也有F(0)=0。n=|S|时定义H(∅)=0及

\[
 H(S)=\sum_{\varnothing\ne T\subseteq S}
 \frac{(|T|-1)!(n-|T|)!}{n!}F(W(T)).\tag{1}
\]

普通均匀排列Shapley份额为

\[
 \phi_i(S)=\sum_{T\subseteq S\setminus\{i\}}
 \frac{|T|!(n-|T|-1)!}{n!}
 [F(W(T)+w_i)-F(W(T))].\tag{2}
\]

直接相减H(S)−H(S\{i})：对不含i的非空T，t=|T|的系数差为−t!(n−t−1)!/n!；对含i的T，系数为(t−1)!(n−t)!/n!，恰是式(2)正负两项。故

\[
 H(S)-H(S\setminus\{i\})=\phi_i(S).\tag{3}
\]

在每个排列中边际总和望远镜成F(W(S))，平均后得到效率

\[
 \sum_{i\in S}\phi_i(S)=W(S)c(W(S)).\tag{4}
\]

## 两种权序与局部包络

原身份`WC-R3-DENSE-SHARE v1`。任意i,j满足w_i≤w_j时，

\[
 \phi_i\le\phi_j,\qquad\phi_i/w_i\ge\phi_j/w_j.\tag{5}
\]

从而对全部i∈S，

\[
 \min_{j\in S}w_j\,c(W(S))\le\phi_i(S)
 \le\max_{j\in S}w_j\,c(W(S)).\tag{6}
\]

完整代数证明如下。线性性使只需F(x)=x^q、整数q≥1。多项式展开的一个指数向量γ项只在包含其非空支持的联盟出现；排列中支持每个成员等概率最后出现，所以

\[
 \phi_i(S)=\sum_{|\gamma|=q,\gamma_i>0}
 \frac{q!}{\prod_j\gamma_j!}
 \frac{\prod_jw_j^{\gamma_j}}{|\operatorname{supp}\gamma|}.\tag{7}
\]

固定i,j权a≤b及其余用户指数β，令m为β支持数、h=q−Σβ，并取非负公共因子

\[
 B=\frac{q!}{h!\prod_{\ell\ne i,j}\beta_\ell!}
       \prod_{\ell\ne i,j}w_\ell^{\beta_\ell}.
\]

h=0时对差无贡献。h≥1时，共含i,j的项在φ_i−φ_j中消失，余项为B(a^h−b^h)/(m+1)≤0。对归一化差φ_i/a−φ_j/b，h=1时为零；h≥2时该β块恰为

\[
 B(b-a)\sum_{r=0}^{h-2}
 \left[\frac{\binom h{r+1}}{m+2}-\frac1{m+1}\right]a^rb^{h-2-r}.\tag{8}
\]

这是把仅含i或j的B(a^{h−1}−b^{h−1})/(m+1)和共含二者的交叉项合并、再分解幂差得到。每个括号非负，因为binom(h,r+1)≥2，且2/(m+2)−1/(m+1)=m/((m+1)(m+2))≥0。求和及对c的非负线性组合给式(5)。

取最小权用户u、最大权用户v。式(4)说c(W)是各φ_i/w_i以w_i为权的平均；式(5)给φ_u/w_u≥c(W)≥φ_v/w_v。再用普通份额序，得w_uc(W)≤φ_u≤φ_i≤φ_v≤w_vc(W)，即式(6)。没有除c(W)，零费用不例外；单用户等号。仿射c只涉及q=1,2，归一化序等号，故φ_i=w_ic(W)。

## 潜在用户局部权比的存在界

稳定子对象`weighted-congestion/local-band-shapley-pne`；原身份`WC-R3-DENSE-LOCAL v1`。

游戏有限非空玩家/资源，正实权，非空有限资源子集策略族允许空策略；每资源c_e为任意非负系数多项式。成本C_i(s)=Σ_{e∈s_i}c_e(x_e(s))，不乘玩家权，偏离重算负载。设潜在用户U_e={i:某合法策略含e}。对非空U_e置a_e=min_{i∈U_e}w_i、b_e=max_{i∈U_e}w_i，假设b_e/a_e≤R，R≥1。没有次数、人数或策略长度限制。

令S_e(s)为实际用户集，定义

\[
 \Phi(s)=\sum_{e:U_e\ne\varnothing}H_e(S_e(s))/a_e,
 \qquad D_i(s)=\sum_{e\in s_i}\phi_{i,e}(S_e(s))/a_e.
\]

式(3)在任意单方偏离给精确ΔΦ=D_i(s′)−D_i(s)：删除和加入用对应端点的边际，保留资源完全相同而取消。实际用户包含于潜在用户，所以式(6)在每个状态和偏离后状态给

\[
 C_i(s)\le D_i(s)\le R C_i(s).
\]

Φ的每个单方局部最小点满足D_i(s)≤D_i(s′)，于是C_i(s)≤RC_i(s′)。有限非空状态空间存在全局最小点；若C_i(s)>RC_i(s′)，则D_i(s)>D_i(s′)，故全部严格R改善下降并终止。式(1)可能有指数多个子集，没有多项式时间保证。

无人资源取零势且不定义a_e；全部策略为空时全部成本零，精确PNE。零费用、零偏离成本、空策略、保留资源及次数零均直接包含。R=1时资源缩放使每个份额等于原费用，给精确势；d≤1还可用未缩放H和玩家乘子w_i，在无权比限制时给精确PNE。

“潜在”不可换成“当前”：偏离者可能此前未在资源上出现，按当前最小权重新缩放会改变函数并破坏精确边际式。允许全局有任意多相距极大的权带，只要每资源潜在用户全在某一宽度≤R的带中即可。某资源跨带时，单看各带内部窄不保证本条件。

## 独立检查、来源与关系

本轮全文比较实际审查`source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/weighted_congestion/weight_bands_review/independent_review.md#shapley-bound-independently-proved`。它在未读候选时以独立同分布标签采样、支持内均分及条件计数比较证明包络，继而重建势；该审查原记录的candidate-proof comparison栏仍为当时pending，不能擅改为已执行全面逐稿攻击。源README末段指向不存在的旧`dense_band_review`路径，本对象改用实际存在并已读的上述文件。

[本批有限精确核验](../计算/权类别与局部权带的精确核验--计算.md)从原始子集式重新算份额、效率和上下界，不是重复计算式(8)两端；一般实参数定理仍靠上述证明。

[有序权组尾部冻结](有序权组尾部冻结--定理.md)在每阶段平移费用后用本包络，以资源固定比例β/a缩放，得到不同的顺序存在机制。[Shapley选择器与分带归一化障碍](../障碍/Shapley选择器与分带归一化--障碍.md)给R选择器锐性、普通势混合差障碍及跨单点权带的线性损失；这些例有精确PNE，不能当真实非存在。两权[双排序势](两权类别双排序混合势--定理.md)使用另一势，故不受标准Shapley选择器障碍否定。

原稿文献记录包括Kollias–Roughgarden的Shapley总费用势、Feldotto等的份额费用比较、Ren等的有界权结果；这里不导入那些外部定理。本轮未重新核查论文或穷尽优先权，不把既有机制称新颖。旧全类OPEN说法已由后续全状态线性下界替换；本地权比定理仍成立，全球新颖性、外审与最优存在倍率未认证。
