---
id: customer-attraction/monotone-shapley-complementarity-anchor-dominance-unbounded-root-ratio
kind: counterexample
type_tag: 反例
title: 共同单调Shapley模型的锚弱占优与无界根比
status: proved-auxiliary-model-half-separation;not-nonnegative-client-CAG-or-submodular-counterexample
truth_status: proved-all-m-ge2
review_level: full-primary-source-read-and-direct-Shapley-reconstruction;no-new-runtime
model: auxiliary-monotone-set-function-with-slot-Shapley-sharing
scope: m≥2单位行动者、m+1标签；共同全域单调集合函数，重复标签作为不同有标号槽；丢弃非负客户表示
summary: 单调互补C由锚单项/锚卫星AND/全卫星unanimity组成，锚对任意固定对手弱占优，完整常锚SPE有W1而OPT3m/2；只反弱Shapley放松，二标签次模已失败。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-977d3dbff13346b3b7c0f5a4caa6168e/coupling/monotone_complementarity_root_boundary.md
---

# 共同单调Shapley模型的锚弱占优与无界根比

2420B原稿全文实读。它记录普通互补性的一个精确辅助模型边界，原文即不声明新颖性。本页补全槽Shapley及共同signed覆盖表示的直接解释；不将其命名为原非负单位客户问题的新反例，也不引入当前源码/实验成功身份。

## 修改了哪一个模型前提

固定整数m≥2，标签目录P={a}∪D，其中D有m个卫星。令

\[
\beta=1/(m-1),\quad K=3m/2,\qquad
C(S)=1_{a\in S}(1+\beta|S\cap D|)+K1_{D\subseteq S}.
\tag{1}
\]

C定义在全部标签子集，C(∅)=0。它是锚单标签unanimity、m个AND(a,b)及全卫星unanimity的非负和，所以在**标签集合**上单调且超模。

终局有m个有标号行动槽，每槽选择一个目录标签。对任意槽子集R，以其已选标签集合A(R)定义coalition值v(R)=C(A(R))；重复标签仍是不同槽，不能先合并后平分。每位收益为随机排列中其加入前后v增量的均值，即Shapley值。福利由效率等于C(最终已用标签)。策略仍在全部有序历史指定动作，但已经丢弃共同非负单位客户表示；这与[原CAG模型](../定义/共同目录完整历史模型--定义.md)的客户均分不是同一收益假设。

C单调使任意槽的每个排列边际都非负，故全部终局收益非负。标签C超模不表示重复槽提升后的v仍超模，本构造也不需要后一断言。

## 为什么共同线性身份仍然成立

令k_B(S)=1_(B∩S≠∅)。在共同覆盖基上，AND(a,b)=k_a+k_b−k_ab，且全卫星unanimity满足

\[
1_{D\subseteq S}=\sum_{\varnothing\ne B\subseteq D}(-1)^{|B|+1}k_B(S).
\]

因此(1)有一张固定signed客户表：w_{\{a\}}=1+mβ，每个w_{\{a,b\}}=−β；对非空B⊆D取w_B=K(−1)^(|B|+1)+β1_(|B|=1)，其余0。这张表共同解释全部coalition、终局和偏离，没有逐终局另配客户。

对一个覆盖原子k_B，若最终有d个槽选到B中的标签，这些槽各得1/d，其他得0；这是“谁先覆盖该原子”的排列概率。Shapley线性所以该signed表恰给同一均分收益行。效率逐原子成立；删除另一有标号槽后重算Shapley，若i,j同覆盖该原子，两边balanced-contribution差均为−1/[d(d−1)]，否则均0。因此E与BC及共同signed客户线性身份都保留，删除槽时C/β/K保持固定。这不把signed系数变成非负客户数。

非负客户要求已经在二标签被违反：对任意卫星b，

\[
C(a)=1,\quad C(b)=0,\quad C(ab)=1+\beta,
\qquad C(a)+C(b)-C(ab)=-\beta<0.
\]

等价地，该对的交集质量负。任何共同非负客户覆盖都次模，所以此辅助数组不可能由原单位客户实现；统一清分母也不能修复负号。它更没有反驳共同**次模**Shapley模型的较强half候选。例如同一C的全人口层表示中U_a(e_a+e_b)=1+β/2>1=U_a(e_a)，已有正外部性；不满足[共同单调次模删除势提升](../定理/共同删除势的全域效率与单调次模提升--定理.md)的DR前提，该表示定理本身也没有一般福利结论。

## 锚对任意固定m−1对手的弱占优证明

固定任意其余m−1个槽行动。当前先选a时，终局锚数c≥1、卫星计数v_j，c+Σv_j=m。对AND(a,j)原子，一名锚槽的pivotal概率是

\[
1/c-1/(c+v_j),
\]

因为它须是第一个锚而之前已有j；一名j槽则为1/v_j−1/(c+v_j)。v_j0时该AND原子未被满足、全部贡献0。

**c≥2。** 当前改卫星b后仍有锚，m槽不可能同时容纳全部m个不同卫星，所以K项在两侧恒0。当前锚与偏离b的准确利润为

\[
U_a=1/c+\beta\sum_{v_j>0}(1/c-1/(c+v_j)),\qquad
U_b^{dev}=\beta(1/(v_b+1)-1/(c+v_b)).
\]

若c≤m−1，U_a≥1/c≥β≥U_b^{dev}。若c=m，则所有v_j0，当前a利润1/m，改卫星利润β(1−1/m)=1/m，仍为弱比较，不能删掉这份平局。

**c=1。** 偏离后没有锚，除非m槽恰是全部m个不同卫星，否则C及所有偏离收益为0；原锚至少得1。唯一例外中，其余m−1槽是不同卫星、当前改补缺卫星，此时原锚从每个AND得β/2，故U_a=1+β(m−1)/2=3/2；偏离后m槽全为unanimity必要槽，每位得K/m=3/2。该边界也是弱比较。

于是a在每一个固定对手配置都不差于任何卫星，包含m2与任意重复标签配置。

## 完整常锚SPE及根目标的真实失败

取策略σ：在每个有序历史都选a。当前偏离不会改变σ规定的未来全锚，所面临的对手恰是“真实过去+未来固定锚”的一份配置。上一节的弱占优直接比较该真实偏离；所有有序节点都成立，所以这是完整纯SPE。这里没有从静态弱占优推出**任意**历史依赖SPE的性质，只构造这份明确常策略；一般动态续局仍可能随当前动作改变。

σ根终局全锚，W=C(a)=1。至多m标签若不含锚，只在选齐D时取K，其余为0；若含锚，至多再有m−1卫星，值≤1+β(m−1)=2<K。因此

\[
\boxed{OPT_m=K=3m/2,\quad 2W-OPT_m=2-3m/2<0,\quad OPT_m/W=3m/2\to\infty.}
\]

全P有m+1标签，不能拿C(P)当m槽OPT。K在奇数m时可为有理值；这是辅助集合函数系数，不伪装成真实单位客户数。

因此，仅用“同一共同signed Shapley表示、全域C单调、全部终局收益非负、全部真实定义的Γ非负”不能支付根half行：此处所有这些前提成立、目标却严格负。反驳的是这个弱放松。非负客户/二阶局部客户正性/次模性都已经排除此点，所以它没有触及原共同非负客户加真实分支的主问题。

它也不同于[分数基数条件平方族](../障碍/任意人数条件平方与二阶整数正行的共同客户缺口--障碍.md)：后者保很强局部正性却W=OPT1，本例有负half目标却连二阶次模都不过。不能把两个不同输入的优点合并成一份强松弛half分离。

[静态弱占优与动态势的边界](../引理/单色真实后缀的饱和查询与剩余税--引理.md)中的原CAG例也未反half；本文只在明确常锚策略下使用静态比较。原稿无附属程序或数值报告，本次解析重构新增程序运行0，无外审/新颖性或原六人half反例声明。原件与入口的逐项去向见[本批资源](../资源/背景剪枝与共同客户根支付入口的逐项范围--资源.md)。
