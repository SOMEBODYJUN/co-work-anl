---
id: unrelated-machines/prefix-atomic-law-decoding-generation-and-later-precision-scope
kind: review
type_tag: 审查
title: 前缀原子law解码的生成义务与精度后续
math_scope: global-prefix-atomic-law-for-ordinary-UM
status: proved-promised-decoder; no-general-generator-or-promise-verifier
summary: 同一个全局前缀law到正完整原子的O(E)解码，生成器NP义务与有限精度polybits后续分开；不把四阶矩或查询器承诺当免费可验证对象。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/composition_decoder_obstruction_review.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/composition_decoder_obstruction_review.md
---

# 前缀原子law解码的生成义务与精度后续

## 精确表示身份与实际来源

本页处理36行composition review中的UM-PREFIX-ATOMIC-DECODING-v1，非私有需求树或unit-presence。另全文读217行canonical a17bde448cd58ab9b637a6050837153006423cf8097b078621bcb302031ff02b；后有限精度是**后续比较**，不倒填旧composition审查范围。现有[宽仿射/前缀双源页](宽仿射矩形与前缀原子解码双源审查--审查.md)、[有限精度/Gram页](前缀原子有限精度与相对Gram审计--审查.md)全文比较；仿射矩形构造与本law是不同输入承诺。

给合法显式P、有理T≥0，每任务有限端集合E_j。对任意相容部分分配S（每任务≤1端）给有理查询器Eval(S)=π(S)，运行时间/输出位长按输入及前缀编码多项式。承诺：π(∅)=1、π≥0，未选j时

$$\pi(S)=\sum_{e\in E_j}\pi(S\cup\{e\}),$$

以及每个**完整**σ、每机i都有

$$(T-L_i(\sigma))\pi(\sigma)\ge0.$$

这些是同一个全局law的全称条件，不是各机器或各前缀另挑见证；本定理没有给一般多项式promise验证器。

## 解码、自约束与全阶关系

从空S按固定任务顺序查询其所有孩子。父权正、子权和等父，至少一子权正，任选确定性正端加入，归纳得完整π(σ)>0。原子局部化即给所有L_i≤T。总查询Σ|E_j|=|E|，按查询承诺和有理正性比较总位多项式，输出全部原任务一次有限端，不枚举完整原子。

空任务直接返回空调度；∞不进E_j，零端/T0同公式覆盖。平方正性不是这一步选择必要条件，带符号孩子总和正仍有正子；正式身份保非负law。若来自degree2n+1 functional，π(S)=L(m_S)，Boolean/one-hot ideal给守恒，平方正性及m_S²=m_S给非负；degree-n负载localizer用q=m_σ（总次数2n+1）给完整原子容量。低阶M2没有这些全阶条件，不能免费替代。

存在该条件当且仅当OPT≤T：正向由解码，反向任一可行σ的Dirac查询器可直接按是否相容输出0/1。这个存在等价不提供未知σ或任意输入的压缩查询器。将阈值改B只解码B调度，不自动继承原T上的失败语义。

## 生成精确阈值的真实复杂度责任

若总确定性位多项式Gen对所有OPT≤T产生合法查询器、对其余可靠FAIL，调用解码并重算σ便精确判T可行。它不能在P≠NP下当免费步骤。实际比较原共同选择稿1–96行：固定T1、端时间{1/2,1}、每任务唯一small端已NP完全；3DM外部NP完全性是既有Paper Fact，本归约自足如下。

给|X|=|Y|=|Z|=q、三元组列表A有s项。每x一源R_x，每a一S_a，每y/z一元素机E，另一闲机。每x三件激活任务，small端R_x时间1/2，unit端为含x的S_a；每a的两件关联任务small端S_a时间1/2，unit端为其y/z元素机。m=s+3q+1，n=3q+2s，有限边3q+7s，全部常数时间。

峰≤1时每R_x最多两件激活，所以至少q台不同S_a被激活且每x至少一次。每已激活S_a不能再留两关联half，须去不同y/z unit端；2r≤2q迫r=q、三元组给完美匹配。反向用完美匹配各x一激活送所选S、两件留R，关联到各互异元素，其余留S，峰≤1。q0为空调度、孤立坐标仍有small端；显式源/稠密输出皆多项式。

NO且q≥1时所有任务留small端给峰3/2，半整数负载排峰≤1，故该源只有1对3/2级真实gap。它足以阻止免费精确T证书生成，**不排一般(2−ε)算法**或另一个增广阈值生成接口。普遍查询器承诺不能仅靠检查被问过的O(E)前缀就认证；已得到σ后验证σ只是输出可行性验证。

## 后有限精度纠偏：数值指数小不等位数指数

当前canonical另有UM-PREFIX-ATOMIC-FINITE-PRECISION-v1，保持同一归一、非负、**精确守恒**law。固定顺序，d_j=|E_j|、D_k=∏_(j≤k)d_j、N=D_n，查询误差≤a，计时须按精度二进制位数而非1/a。每步选近似最大孩子，真质量w满足w≥(q−2a(d−1))/d；乘D_k望远镜得锐界

$$\pi(\sigma)\ge\max\{0,[1-2a(N-1)]/N\}.$$

目标叶权u=[1−2a(N−1)]/N、其它叶v=(1+2a)/N，沿固定平局优先路径给目标估计+a、其它−a即取等，至u0后仍可输出零叶。N1唯一叶权1。不是所有近似器都会取坏枝。

若逐完整原子只有绝对残差(T−L_i)π≥−τ_i，正输出只能给L_i≤T+Nτ_i/[1−2a(N−1)]。两强制任务在A各3/4，另k个零时间B/C任务，N2^k个原子均峰3/2；均匀law的残差−1/(2N)显示N因子不能省。不是漏剪枝，dummy只是拆质量。

Q为全部时间及T分母积，Q(L_i−T)为整数。取a=1/(4N)、τ_i≤1/(4QN)，输出过载≤1/(2Q)<1/Q，故实际精确T可行。logN≤nlogm、logQ多项式，精度数值很小仍仅需多项式位；没有遍历N/Q、也无普遍law生成器或验证器。

相对残差(T−L_i)π≥−Δ_iπ则正叶直接≤T+Δ_i。完整函数评价矩阵F**满行秩**时，K_i=F^Tdiag((T−L_i)w)F、M=F^Tdiag(w)F满足K_i≽−Δ_iM当且仅当全部正权原子容量≤T+Δ_i；单原子指示函数可由列张成，给反向。低阶F不能删满秩前提，绝对−τI也不在任意非正交基下不变。

## 审查先验、旧有限范围与接续

原composition稿无新增实验/外部import；早期精确Fraction例是两机两任务Dirac/均匀、T0零端、两机三unit在T1全部8原子被排及5异质Dirac。后噪声/Gram审计另身份，不在此重跑/复勾。有限数据不替同一law、所有叶局部化和polybit查询三个承诺。仍缺原(P,T)到证书的可构造来源、可靠FAIL及一般source decoder；没有C2+CONFIG或统一次二结论。[本批原件/范围](../../../../tools/evidence/um-foundation-composition-configuration-reviews/README.md)。
