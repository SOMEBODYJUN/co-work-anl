---
id: bottleneck-knapsack/two-capacity-profile-label-enumeration-candidate
kind: candidate
type_tag: 候选
title: 双容量瓶颈背包的profile标签与完整枚举
status: explicit-candidate-pipeline; imported-profile-and-joint-global-proof-pending
summary: 保存源稿全部归一化参数、profile提取/标签公式、slack吸收、long/short池分离、全局数量枚举及几何网格预算；三局部模块可独立证明，总候选仍未认证。
legacy_ids: [TS-BMKP-2CAP-APPROX-v1]
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/independent_review/research/topic_selection/generalized_assignment/TWO_CAPACITY_LEMMA.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/independent_review/research/topic_selection/generalized_assignment/TWO_CAPACITY_LEMMA.md
---

# 双容量瓶颈背包的profile标签与完整枚举

## 模型、目标和真正状态

物品公共正有理重$w_e$、非负有理利$p_e$，背包容量属于$\{B_1,B_2\}$、$0<B_1\le B_2$，每件至多一次、可unused，不能弃置背包，容量不得增广。目标最大化全部背包最小利润。求每个固定$\varepsilon>0$、关于显式二进制输入长度多项式的$(2/3-\varepsilon)$近似。两个容量值不是两个背包，容量比无上界；这是中央优化，不是NE。

原112行13399B全文逐项读；[三条件模块](../引理/联合类型交换与允许弃置的背包恢复--引理.md)有完整本地证明，但从母文profile提取到一轮全局成功的联合论证仍须核，规范通用算法未交付。下面明确记哪些式可直接推出、哪些是候选的导入合同；不因旧反方“未找到fatal”把总算法升为定理。

## 一、单向阈值与最终参数

阈值$T$采用单向gap-oracle：若$OPT\ge T$则至少一个枚举轮成功；成功只承诺输出每包利润≥$qT$，不承诺$T\le OPT$。不能把成功谓词直接用作精确二分的比较器。

归一为$T=1$，先cap利润$p_e\leftarrow\min(p_e,1)$。若一个原可行包含利润至少一的物品，cap后仍有利润≥一；否则该包利润不变，故阈值一见证保持。定义

$$\zeta=\frac1{\lceil\max(100,20/\varepsilon)\rceil},\quad U=1-\zeta,\quad\gamma=U\zeta,\quad\delta=U\zeta^2,\quad K=1/\zeta\in\mathbb Z,$$
$$q_{pre}=2/3-8\zeta,\qquad Q=q_{pre}-3\zeta=2/3-11\zeta.$$

昂贵统一指$p_e\ge\gamma$，便宜严格$p_e<\gamma$，不随容量、profile或critical身份改变。原最终预算预留heavy-cheap损失、下舍入、short交换、$4p_{max}$舍入及网格，不能只写“rescale $\varepsilon$”掩盖。

## 二、候选导入的profile接口

从未知阈值一见证出发，含$p_e\ge q_{pre}$物品的包保该单件为初始short singleton。其余包所有原物品$p_e<q_{pre}$、原利润≥一。在每个其余容量$B_t$包删heavy-cheap：$w_e\ge(1-\zeta^2)B_t$且$p_e<\gamma$。因$\zeta\le1/100$且正重量，至多一件，损失$<\gamma<\zeta$，余利润≥$U$。

分别对两个容量，仅取这些剩余包和其原用物品构成互不交子实例，容量除$B_t$、利润除$U$。直接代数给

$$p_e/U<q_{pre}/U<2/3-6\zeta,$$

因为$U(2/3-6\zeta)-q_{pre}=(4/3)\zeta+6\zeta^2>0$；剩余heavy物品归一利润≥$\gamma/U=\zeta$。这些是候选拟对齐母Lemma8的individual-profit与no-heavy-cheap前提，不能改用未经说明的同容量greedy。

**导入义务仍在。** 源拟调用母文Lemma8，在各自子实例内得到大小$O(\zeta^{-2})$的profile $T_t$、若干≤二件short及具有slack的long：raw利润≥$U(2/3-\zeta)\ge2/3-2\zeta$。调用所需完整profile符号、剩余物品的适用性及重组范围必须和母文§4.2–4.6、定义11/15、相关附录逐式核；本页没有新读母论文全证明，故不把这个导入当免费已证引理。

源随后规范long昂贵数：若超过$K$，保任意$K$昂贵件、弃其他物品，其利润≥$K\gamma=U$。保heavy时rest上界只会减；若去heavy，原rest≤$\zeta^2B_t$，足以留all-light的$\zeta^3B_t$ slack。这个局部删除计算解释cardinality预算，但仍需和实际profile见证类别一致，不能只从输入昂贵数断言结构变换后仍受限。

## 三、两容量的全局联合标签：原公式和边界

每容量$t$给昂贵物品计算$u_t(e)$，其定义是候选的一部分：

- 不适用于该容量者标$\perp$。
- heavy指$w_e\ge(1-\zeta^2)B_t$。在相同$\lfloor p_e/(U\zeta)\rfloor$利润桶内，从$T_t$中找不轻于$e$的最轻代表，以其重作$u_t(e)$；无代表标$\infty$。
- light按$T_t$选尺度：若有profile heavy $h$满足$w_e\le B_t-w_h$，选其中最重者，令$W_t(e)=\zeta(B_t-u_t(h))$；否则$W_t(e)=\zeta^3B_t$。再令

$$u_t(e)=\left\lceil\frac{w_e}{\zeta W_t(e)}\right\rceil\zeta W_t(e).$$

联合类型同时记录两个容量的状态/$u_t$、$g(e)=\delta\lfloor p_e/\delta\rfloor$及高利润标志。同类型才可做L1全局最重恢复；不能先在两容量各选一套原物品再拼。$\perp,\infty$不能作为有限重量使用；$W_t(e)=0$不能照除。profile代表的自代表性质$u_t(h)=w_h$、零残量及无适用代表仍是源明确列出的实现/导入核查点，本页不补一个未证明的默认规则来假装完成。

源估计每容量有效light重量数$O(\zeta^{-4})+O(|T_t|\zeta^{-2})$，加利润桶/状态、两容量乘积，保守联合类型数$O(\zeta^{-12})$，不依$B_2/B_1$或背包数。**此计数须从正确的母profile定义导出**；仅有一个有限$T_t$的名字或数值样例不足以独立证明所有输入都被这些类型覆盖。

## 四、slack怎样吸收上舍入

对真正满足profile合同的long，源需要以下逐包不等式。all-light时原slack$\zeta^3B_t$，每昂贵轻物增重≤$\zeta^4B_t$，至多$K=1/\zeta$件，合计≤slack。

含heavy $h$时，profile应保证原rest≤$(1-\zeta)(B_t-u_t(h))$。该包任意light $e$能与对应profile代表同包，因此所选最重可配代表使$W_t(e)\le\zeta(B_t-u_t(h))$；每项增重≤$\zeta^2(B_t-u_t(h))$，至多$K$项，合计≤$\zeta(B_t-u_t(h))$。加上重物上舍入，仍总重≤$B_t$。不要求同包所有$e$的尺度相同。

这些代数吸收在**确有上述profile/尺度合同**时成立；证明这些合同对源的所有结构变换都适用，是联合证明剩余部分。下舍入利润损失≤$K\delta=U\zeta\le\zeta$，long下舍入值≥$2/3-3\zeta\ge Q$。L1交换后short原利润≥$q_{pre}$减$<2\delta$，故仍≥$q_{pre}-2\delta$。

## 五、枚举、物品池与完整成功轮

候选枚举两profile（各大小$O(\zeta^{-2})$）、每联合类型critical总数$N_\tau$、每容量各long配置的multiplicity；每配置至多$K$昂贵件。若类型和配置数确只依$\zeta$，数量枚举轮数是$n^{f(1/\zeta)}$，每固定精度为输入多项式；不是EPTAS的$f(1/\varepsilon)\operatorname{poly}(n)$承诺。相同容量背包可重新编号，不为每一包独立猜原物品身份。

每轮执行：

1. 每类型取全局最重$N_\tau$，按所猜long标签槽任放；$u_t$无效或上舍入残容量负则拒绝。
2. 便宜池严格$p<\gamma$，对每long解列和≤一的LP，重量上限$B_t-\sum_{critical}u_t(e)$、利润下限$Q-\sum_{critical}g(e)$。只接受合法非负残容量。
3. noncritical昂贵池用L2恢复全部short。这与cheap LP物品池不交；unused昂贵物不能临时叫cheap塞进LP。
4. 用L3把cheap LP舍入；每long损失≤$4p_{max,cheap}<4\gamma<4\zeta$，硬容量不增。

正确结构见证中，short经交换利润≥$q_{pre}-2\delta$。若含利润≥$Q$物品可缩singleton，且$\zeta\le1/100$给$Q>\gamma$；否则两件中任一件均≥$q_{pre}-2\delta-Q=3\zeta-2U\zeta^2>\gamma$，因此能完全放入昂贵matching池。canonical long的cheap集合在L1中不变，给cheap LP见证，两池不抢物。于是**若某枚举轮确命中全部合法profile/类型/数量见证**，long输出≥$Q-4\zeta=2/3-15\zeta$，short≥$Q$，得到阈值保证。最后加粗前提是总算法不能省掉的联合覆盖义务。

## 六、正OPT几何网格与最终误差

$OPT>0$时，它位于最小正原利润和全部原利润之和之间。用有理公比$1+\zeta$网格逐点调用单向oracle，取成功输出中实际最小利润最高者。有一个$T\le OPT$且$T\ge OPT/(1+\zeta)$，它应成功。则

$$\frac{2/3-15\zeta}{1+\zeta}\,OPT\ge(2/3-16\zeta)OPT,$$

差恰$(\zeta/3+16\zeta^2)/(1+\zeta)\ge0$。$\zeta\le\varepsilon/20$给$16\zeta\le\varepsilon$。正有理利润范围的对数由输入位长控制，网格长度关于位长和$1/\zeta$多项式；$OPT=0$应单独给合法零保证分配，不能除零或把成功$T$当精确OPT下界。

## 七、版本比较、未决义务和证据

后续反方冻结末节已对齐本参数$U,\gamma,\delta,K$及$8\zeta/11\zeta/16\zeta$，撤回其正文旧$6\zeta/13\zeta$等数值。profit cap、unused、昂贵数规范化、heavy-cheap删除和池分离旧异议不应复活；“已读修复、未找到fatal”也不证明总定理。真正仍须完成：母Lemma8和profile/short输入逐式导入；自代表、零尺度和无效标签；所有数量配置轮覆盖；容量相等、空long/short类、零利润及位长/输出合同；通用实现和中间不变量核验。

源3000个L1 Fraction例和8192个单位利润pair穷举只核局部模块，本批没有重跑，更没有把它们说成总BMKP实现。原母文ICALP2026 §7常数容量种类问题是来源记录；两容量切片不解一般固定$K$，本页不重新认证全球开放性或新颖性。完整原稿、实际比较和逐节去向见[证据](../../../../tools/evidence/retired-five-primary/README.md)。与[前批资料](../资料/双容量BMKP候选的三模块与完整目标--资料.md)互补：本页保全具体标签、slack和枚举，主张仍为候选，第三阶段只能建带全部导入条件的关系。
