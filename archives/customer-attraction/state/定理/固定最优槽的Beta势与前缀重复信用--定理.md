---
id: customer-attraction/fixed-optimal-slot-beta-potential-and-prefix-repeat-credit
kind: theorem
type_tag: 定理
title: 固定最优槽的Beta势与前缀重复信用
status: fixed-baseline-potential-unit-decomposition-and-prefix-credit-proved; dynamic-budget-open
truth_status: static-global-bound-and-stated-repeat-estimates-valid; no-cross-rollout-payment
review_level: full-11168B-primary-and-4825B-related-reconstruction-reading; current-nonblind-analytic-check
scope: 任意有限单位客户共同目录、m≥1、一次固定最优索引槽配对；形式空槽仅算势；重复信用对应完整最优前缀而非actual-prefix matching
summary: Bernoulli合法替槽积分给固定有限基线F_T与Beta边际，原单位利润分为势边际和O内非负信用。同叶信用只一次；完整最优前缀的Beta查询折扣合≤H_(a−1)，不能跨叶当actual I或逐query改配对。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round3/relay/optimal_exchange_potential_and_query_credit.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round3/shared/review_global_exchange_potential.md
---

# 固定最优槽的Beta势与前缀重复信用

## 同一全局配对及合法静态上界

采用[单位客户共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)，任意$m\ge1$，目录有限非空；保重复主题、空主题、零客户及所有有序历史任意平局。先固定最优合法m槽索引元组$T=(T_1,\ldots,T_m)$，并集O、每客户比较覆盖数$a_x$。重复主题仍有不同槽索引，不能合并。以下静态结论无需均衡。

对合法完整或形式部分profile B，记$c_x(B)$为覆盖槽数，$J(T,B)=\{x\in O:\nexists i,\ x\in T_i\cap B_i\}$，即无同槽保护。令$H_0=0$，正整数Beta为

\[
Beta(a,c)=\int_0^1p^{a-1}(1-p)^{c-1}dp
=\frac{(a-1)!(c-1)!}{(a+c-1)!}.
\]

逐槽独立以概率p把T_i换为B_i。O外新增客户概率$1-(1-p)^{c_x}$；同槽已保护客户永不丢失；其余O客户的比较覆盖槽与B覆盖槽不交，丢失概率$p^{a_x}(1-p)^{c_x}$。每份实现仍是至多m个合法非空主题，形式空槽可补任意目录主题，覆盖≤OPT。因此除p积分得

\[
\boxed{\Phi_T(B)=\sum_{x\notin O}H_{c_x}
-\sum_{x\in J(T,B)}Beta(a_x,c_x+1)\le0.}\tag{P}
\]

没有删除祖先或宣称替槽后策略为SPE。该式只在同一最优T/配对上使用，不能每个真实叶换一份基线再望远镜。

相关shared重构稿补明有限归零基线：

\[
K_T=\sum_{x\in O}1/a_x,\quad F_T=\Phi_T+K_T,
\qquad 0\le F_T(B)\le K_T,
\quad F_T(\varnothing)=0,\quad F_T(T)=K_T.
\]

可由同一Bernoulli覆盖与全空B的期望覆盖差积分得到非负单调槽动作扩展；固定硬币的覆盖增量次模，积分仍次模。最优m槽上界只用于每槽至多一个合法动作或形式空槽的可行profile，不向同槽多动作不可行配置套cap。K_T通常不是OPT；owner薄化会换成另一单位基线势，不制造额外收入。

## 逐客户边际及同一叶的一次信用

把第i槽形式置空，定义$\ell_i(B)=\Phi_T(B)-\Phi_T(B^{-i})$。这不是较少玩家的SPE。只对$x\in B_i$写c≥1：

| 客户条件 | 势边际 |
| --- | --- |
| x不在O | 1/c |
| x在O且另有槽h≠i同槽T_h/B_h保护x | 0 |
| x在O、无其它同槽保护、x在T_i | Beta(a,c) |
| x在O、无其它同槽保护、x不在T_i | Beta(a,c)−Beta(a,c+1)=Beta(a+1,c) |

后一统一积分的被积式为$p^{a-\mathbf1_{x\in T_i}}(1-p)^{c-1}$，在非零情形参数均正；不超过$(1-p)^{c-1}$。因此逐客户$0\le\ell_i\le1/c$，令$e_i=u_i-\ell_i$，有

\[
\boxed{u_i(B)=\ell_i(B)+e_i(B),\quad e_i\ge0,
\quad e_i\text{只由O客户贡献}.}\tag{UNIT}
\]

固定**同一个B**，每O覆盖客户全部真实份额和为1，故

\[
\boxed{\sum_ie_i(B)\le|O\cap cover(B)|.}\tag{LEAF}
\]

actual叶的右端才是I。O外势边际恰是该叶G_B真实收益；不同rollout的G_B/I_B支持可不同，不能各领一次actual I/G，也不能把原完整IC变成逐客加权IC。

## 完整最优前缀的Beta重复查询信用

固定一个最优索引排列，重标成T1,…,Tm。令$Y_i=finish_\sigma(T_1,\ldots,T_i)$，所有Y_i来自**同一原完整策略**，其前i槽确为T；不合并同计数历史、不独立挑续局。当前query收益$d_i=u_i(Y_i)$，信用$r_i=d_i-\ell_i(Y_i)\ge0$。重复界事实上只需保留这些前缀，不需SPE。

对比较覆盖a次的客户，按query出现次序s：首次信用≤1−1/a。若无其它同槽保护，$1/c-Beta(a,c)$随c≥1的整数增大不增，最大在c1为1−1/a（积分形式为$\int_0^1z^{c-1}[1-(1-z)^{a-1}]dz$）；若已有未来同槽保护，则c≥2、信用≤1/2≤1−1/a。a1时不会有其它保护，Beta(1,c)=1/c，信用0。之后s≥2次已有早期同槽保护，边际0且当前分母至少s，所以信用≤1/s。因此

\[
\boxed{\sum_ir_i(x)\le1-1/a+\sum_{s=2}^a1/s=H_{a-1}\le a-1.}\tag{BETA-REPEAT}
\]

O外不在任何T_i，query信用0。这个预算支付比较重复折扣，不支付所有不同规定rollout的e_i；同叶LEAF和跨前缀REPEAT是不同对象。查询折扣进入费用恒等式的符号须保留，不能把上界当可免费扣除的下界。

## owner薄化与后续真实查询账的区别

将O分块$Q_i\subseteq T_i$、每客户唯一owner，只作分析不当合法偏离，得到[单位owner势](../定理/最优归属势的单位分解与同叶联合预算--定理.md)。若owner取本最优顺序首次覆盖槽，首query信用0，后s次≤1/s，合≤H_a−1，是不同更强界。它不使actual-prefix matching查询成为最优前缀链。[插入与两种真实查询账](../引理/归属插入势与两种真实查询重复账--引理.md)自足保存DIRECT-REPEAT、excess E和ROLL的区别。

后来的[固定归属端点引理](../引理/固定最优前缀链的归属端点抵消--引理.md)把owner前缀H_a−1扩到任意固定及分数owner；本11168B主稿的该段证明仍是first-owner版本，不能回填成当时已经证明其它量词。跨排列平均须每个排列连同自己的固定owner/真实叶单独使用，不能逐query切换势。

## 与其它静态交换核的区别

[旧Bernoulli生成表示](../引理/最优索引交换的生成表示与查询税--引理.md)及[最优索引并集预算](../引理/最优索引组合的联合逃逸预算--引理.md)同样来自合法最优替换，但无放回注入/均匀配对将同槽信息平均为组合系数；本页先固定配对，保留J(T,B)的保护事件。积分密度也不同：本页除p给调和H_c及Beta(a,c+1)，旧额外查询税另出现c/(alpha+c)。不能把1/c单位势边际与额外查询分母混成同一收入，或将两份静态上界相减得到免费动态返还。它们保留不同信息，却都不提供跨真实枝的一次付款。

## 历史及有限证据

11168B主源全文重读，保Bernoulli/HARM由shared提出、root重构，固定配对Beta由relay/shared同时得到，同叶预算由shared、前缀查询信用由relay、owner薄化由shared的源述内部身份。4825B相关重构原件全文旁读，称独立得到同势后互核、§3称REPEAT盲重构；原消息精确信息量未附，不能增加“无陈述提示发现”或外审身份。本次读全部证明与程序后非盲核读。

本次两原程序各一次成功，有限mask范围m1…7，不是一般m证明；原pattern程序不测试全局P最优性上界，放松incidence可以不是合法最优profile。一般性由上面的合法替槽证明承担。[精确资源](../计算/最优交换与归属插入的双程序精确回归--计算.md)保实际72818等计数与18项指定IC的范围，不冒称全43节点258 IC复核。

已证固定全局势、单位分解、同叶及前缀重复信用，未证跨rollout联合债或half。五人已有[独立定理](五人半覆盖--定理.md)，六人共同付款未由本组件闭合。主源见[清单](../../tools/evidence/post-root-regret-audit-primary/source-manifest.json)，4825B重构原件见[相关清单](../../tools/evidence/post-root-regret-audit-primary/related-source-manifest.json)。
