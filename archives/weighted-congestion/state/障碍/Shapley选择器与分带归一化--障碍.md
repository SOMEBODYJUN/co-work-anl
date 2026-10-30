---
id: "weighted-congestion/shapley-selector-band-obstructions"
kind: "obstruction"
type_tag: "障碍"
title: "Shapley选择器与分带归一化"
status: "proved"
summary: "局部权比R的标准Shapley最小点选择可趋近R损失；分别按带缩放不必有普通精确势，跨单点带的标准选择器可损失线性于次数。见证均有精确PNE。"
review_status: "algebra checked in cleanup; external review and priority unverified"
legacy_ids:
  - "WC-R3-DENSE-POT-SHARP v1"
  - "WC-R3-BAND-CURL v1"
  - "WC-R3-BAND-LINEAR v1"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/weighted_congestion/weight_bands/README.md#sharpness-for-this-particular-potential-selector"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/weighted_congestion/weight_bands/README.md#fatal-mixed-difference-obstruction-to-separate-band-normalization"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/weighted_congestion/weight_bands/README.md#linear-loss-of-the-standard-shapley-selector-across-singleton-bands"
---

# Shapley选择器与分带归一化

使用[局部窄权带定理](../定理/局部窄权带的Shapley份额势--定理.md)定义：F(x)=xc(x)，H的插入边际是普通Shapley份额φ，资源固定尺度a_e为潜在用户最小权，所研究选择器为Φ=Σ_eH_e/a_e的全局最小点。玩家原成本始终是费用和，不乘权。以下三项有不同对象和否定量词，保留独立稳定子身份。它们没有证明任何游戏缺少近似均衡。

## 局部R界对该选择器的渐近锐性

稳定子对象`weighted-congestion/shapley-local-selector-sharpness`；原身份`WC-R3-DENSE-POT-SHARP v1`。

对每个固定实R>1，存在局部潜在用户权比≤R的游戏序列，使上述Φ的唯一最小点的最佳近似倍率趋于R，而游戏都有精确PNE。

取m名权R固定玩家，唯一策略{A}；一名权1可动玩家选择{A}或{B}。设d=m²、W=mR+1、c_A(x)=x^d/W^d、c_B(x)=ρ_m常数。移动玩家A上的原成本恰1；其标准Shapley增量为

\[
 \delta_m=\frac1{(m+1)W^d}
 \sum_{k=0}^{m}[(kR+1)^{d+1}-(kR)^{d+1}].\tag{1}
\]

因为它在随机排列中之前有k名固定玩家的概率均为1/(m+1)。仅取最后位置给下界；移动者权最小，普通份额序及效率给其份额不超过平均份额W/(m+1)。因此

\[
 \frac W{m+1}\left[1-(1-1/W)^{d+1}\right]
 \le\delta_m\le\frac W{m+1}.\tag{2}
\]

(d+1)/W→∞，故括号趋1，两界趋R。充分大m取ρ_m=δ_m−1/m>1。两资源的潜在最小权尺度都是1，势的两个可选增量分别δ_m和ρ_m，故唯一最小点选B。其最佳近似倍率为ρ_m→R；选A的状态原成本1<ρ_m，为精确PNE。这个锐性只属于指定势的选择器，不给全类阈值下界。

## 单点权带分别归一化的混合差障碍

稳定子对象`weighted-congestion/band-normalization-curl`；原身份`WC-R3-BAND-CURL v1`。

单资源两用户权1和M>1、F(x)=x³，对应合法费用c(x)=x²。两权带各只有一个权值。H的混合差为

\[
 \kappa=H(\{i,j\})-H(\{i\})-H(\{j\})
 =\tfrac12[(M+1)^3-M^3-1]=\tfrac32M(M+1)>0.
\]

若分别按玩家带权归一化ψ_i=φ_i、ψ_j=φ_j/M，并要求存在普通精确集势Q具有这些插入边际，则Q的同一个混合差必须同时等于ψ_i({i,j})−ψ_i({i})=κ与ψ_j({i,j})−ψ_j({j})=κ/M，矛盾。

该结论只排除普通精确势。H本身仍可作为ψ的加权势，玩家乘子分别为1与M；不能省略这条例外，也未排除其他势或非势存在证明。

## 标准选择器跨两单点权带的线性损失

稳定子对象`weighted-congestion/shapley-singleton-band-linear-loss`；原身份`WC-R3-BAND-LINEAR v1`。

对每个整数d≥7，取M=d²。一名权M固定玩家只用A，一名权1玩家选A或B。设

\[
 c_A(x)=\frac{x^d}{(M+1)^d},\qquad
 \delta_d=\frac{1+(M+1)^{d+1}-M^{d+1}}{2(M+1)^d},
 \qquad c_B(x)=\rho_d=\delta_d/2.\tag{3}
\]

δ_d恰为可动玩家加入A的两人Shapley边际，其A原成本恰1，B边际和原成本均ρ_d。两资源潜在最小权都是1，故标准H与按a_e缩放的Φ都唯一选择B。由幂差积分、Bernoulli不等式，

\[
 \delta_d\ge\frac{d+1}{2}\left(\frac M{M+1}\right)^d
 \ge\frac{d+1}{2}(1-1/d)
 =\frac{d^2-1}{2d}\ge d/3.
\]

中间用d/(d²+1)≤1/d。于是ρ_d≥d/6>1，所选状态的最佳倍率至少d/6，而选择A精确PNE。每个带内都等权，却有资源混合两带；按带权恢复加权势不改变唯一可动玩家的势选择。

还可使同一资源上的两个潜在权带任意密集：对任意整数L≥1，分别增添L名权1和L名权M玩家，各自可选∅或{A}。所有新用户在任何Φ最小点都选∅，因为在A者离开会以严格正Shapley边际降低势。于是原唯一所选状态与ρ_d损失不变，两带各有至少L+1名A的潜在用户。全体新增者选空且原可动者选A仍为精确PNE。

这不否定“被选择状态及偏离后都有大量实际活跃用户”的其他假设，因为新增潜在用户在势最小点实际不活跃。也不证明冻结选择器实际输出很差：[尾部冻结的参数障碍](潜在尾部参数的锐界--障碍.md)与这里的真实最小点损失是不同证据类型。

## 审查和关系边界

三条独有构造和关键极限均从原README逐式重算保留。独立份额审查主要证明包络和R-PNE，不将其审查范围扩大为对本文件三种障碍的独立冻结攻击。未外审、全球新颖性未认证。

[双排序势](../定理/两权类别双排序混合势--定理.md)给全局两权类O(√d)保证，正因使用不同资源函数而不受这里标准Shapley选择器的线性损失否定。固定背景吸收后这些只剩一名可动者的例子当然有精确均衡；这再次显示选择器损失与真实存在界必须分开。后续全状态线性下界是独立的真反例构造，不能用本文件有精确PNE的见证替代它。
