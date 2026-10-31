---
id: "customer-attraction/actual-uncovered-private-spectrum-sharp"
kind: "theorem"
type_tag: "定理"
title: "实际遗漏私有块的完整席位谱与条件性锐福利界"
status: "complete"
truth_status: "proved"
review_level: "internal-blind-reconstruction-and-independent-finite-replay"
scope: "任意人数m≥1；任意有限单位客户与有限非空共同目录；每份完整有序历史纯SPE；锐效率界另需某个最优并集的实际遗漏全为极大全局私有"
legacy_ids:
  - "CA-ACTUAL-PRIVATE-SEAT-SPECTRUM-v1"
  - "CA-OPTIMAL-PRIVATE-OMISSIONS-2M1-v1"
summary: "固定实际终局遗漏的全局私有子块，按真实触块次数倒推；实际每个位置均零触及，可求和前m大席位。最优遗漏全私有时得锐OPT_m≤(2−1/m)W。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/customer_attraction/uncovered_private_seat_spectrum.md#1-精确对象与一般残余席位引理"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/customer_attraction/uncovered_private_seat_spectrum.md#3-条件性半覆盖及一般构造必须跨过的边界"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/customer_attraction/uncovered_private_seat_spectrum.md#1-对象和更一般的阈值引理"
---

# 实际遗漏私有块的完整席位谱与条件性锐福利界

## 模型与固定私有子块

客户集有限，每客户价值一；共同目录$\varnothing\ne\mathcal S\subseteq2^N$有限；$m\ge1$名单位提供者依次观察全部先前有序行动，各选一次合法主题；最终每客户在覆盖者间均分。纯SPE定义于**全部有序历史**，包含全部离轨节点，任意历史依赖平局、空主题、重复动作和同覆盖标签均保留。[完整模型](../定义/共同目录完整历史模型--定义.md)固定$W=\sum_i u_i$及最优$m$主题覆盖$\operatorname{OPT}_m$。

取目录中不同包含极大覆盖$B_1,\ldots,B_s$，$s\ge1$，均为合法动作。定义其**极大全局私有块**

$$
P_j=B_j\setminus\bigcup_{\ell\ne j}B_\ell.
$$

私有性对整个共同目录的极大覆盖定义；一个主题相对实际已选动作的独有客户不自动属于$P_j$。先任取固定$Q_j\subseteq P_j$，令

$$
a_j=|Q_j|,\qquad v_j=|B_j\setminus Q_j|.
$$

对任意合法有序前缀$h$，定义真实触块次数

$$
q_j(h)=\#\{\text{此前动作 }A:A\cap Q_j\ne\varnothing\}.
$$

它不要求动作覆盖整个$Q_j$，也不把仅包含于$B_j$却不触及$Q_j$的动作计入。每个$x\in Q_j$的旧客户负载至多$q_j(h)$。

两个承重结构事实如下。任一合法动作$A$可扩入某个极大覆盖；若$A$触及$Q_j$，该极大覆盖含有一个$P_j$客户，只能是$B_j$，故$A\subseteq B_j$。因此一个合法动作至多触及一个非空$Q_j$，每一步最多使一个$q_j$增加一。$Q_j=\varnothing$时$q_j$恒零。

## 任意合法历史的残余阈值引理

固定总人数$m$及阈值$z>0$，定义

$$
f_j(k)=\frac{a_j}{k}+\frac{v_j}{m}\quad(1\le k\le m),
\quad d_j(z)=\max\bigl(\{0\}\cup\{k\le m:f_j(k)\ge z\}\bigr),
\quad R(h,z)=\sum_j(d_j(z)-q_j(h))_+.
$$

$f_j$随$k$不增，所以满足阈值的席位构成初始段；每加入一个动作使$R$至多下降一。

**残余席位引理。** 任意合法有序前缀后剩$r\ge1$人时，若$R(h,z)\ge r$，则该前缀后任一完整纯SPE中每位剩余玩家最终收益都至少$z$。

对$r$同时量化所有合法有序历史和完整纯SPE归纳。$R\ge r>0$保证存在$j$使$q_j(h)<d_j(z)$。当前玩家真实偏离到整个$B_j$，其后严格沿所给策略在该偏离历史的真实续局完成。每步$R$最多降一，所以所有后继子博弈仍有足够残余席位；归纳给其中每位后继收益至少$z$。

若无后继动作触及$Q_j$，当前玩家在$Q_j$每客户的最终负载至多$q_j(h)+1$；此外$B_j\setminus Q_j$每客户被当前真实覆盖，总负载至多$m$。故当前偏离收益至少

$$
\frac{a_j}{q_j(h)+1}+\frac{v_j}{m}
=f_j(q_j(h)+1)\ge z,
$$

其中$q_j(h)+1\le d_j(z)\le m$。$a_j=0$时无需真实增加$q_j$，该式直接是$v_j/m\ge z$，仍合法。

若有后继动作触及$Q_j$，其真实覆盖$A\subseteq B_j$。在同一个最终终局，两名玩家在$A$每客户上获得相同份额，而当前玩家还可能覆盖更多客户。因此当前偏离收益至少该后继收益，后者由归纳至少$z$。$r=1$时没有后继，直接落在第一种情形。

当前SPE最优性把偏离保底转到实际当前收益。实际当前动作也使$R$最多下降一，故归纳还给实际剩余各人同一保底，完成证明。整个论证不冻结回复、不限制匿名平局、不把前缀触及次数等同于每客户实际负载。

## 固定实际遗漏后的完整谱预算

固定一份完整纯SPE及其实际终局，令实际覆盖集合为$C$、$W=|C|$。这里$C$是**实际并集**，不是其他极大覆盖定理中的共同核心。取

$$
Q_j=P_j\setminus C.
$$

这些块由该实际终局事后定义一次；之后在所有离轨历史上保持同一组$Q_j$，不随偏离分支重定义。实际所有动作均不触及任何$Q_j$，因此**每一个实际前缀**都有$q_j=0$。

将带重数席位多重集

$$
\mathcal L=\{a_j/k+v_j/m:1\le j\le s,\ 1\le k\le m\}
$$

降序排列为$\lambda_1\ge\cdots\ge\lambda_{sm}$。第$i$位实际行动时剩$r=m-i+1$人。若$\lambda_r>0$，至少$r$个席位不低于$\lambda_r$，所以$R(h_i,\lambda_r)=\sum_jd_j(\lambda_r)\ge r$。残余引理给当前收益至少$\lambda_r$；$\lambda_r=0$时由非负收益成立。因此

$$
\boxed{u_i\ge\lambda_{m-i+1}\ (1\le i\le m),\qquad
W\ge\sum_{r=1}^m\lambda_r.}\tag{S}
$$

这是每份SPE**实际路径**的后验必要条件，不是任意合法动作路径的收益定理。位置相关的保底随位置加强，不声称实际收益序列本身单调，也不声称给定遗漏量总能实现。

令$a_{(1)}\ge\cdots\ge a_{(s)}$为遗漏块大小排序，$s<m$时补零。全部第一席$f_j(1)=a_j+v_j/m\ge a_j$，故

$$
W\ge\sum_{r=1}^m\lambda_r\ge\sum_{r=1}^ma_{(r)}.\tag{R}
$$

完整谱可严格强于只取每块第一席的rank版本。例如只有一个非零遗漏块$a$时，丢掉所有$v_j/m$仍得到$W\ge aH_m$，而rank版本只给$W\ge a$。保留$v_j/m$的余客户信用是源稿本轮加强的一部分，不能丢成只保留私有量的摘要。

## 最优覆盖中私有遗漏的一般约束

取任意最优$m$主题并集$O$，其实际遗漏的私有部分大小

$$
V_{\mathrm{private}}=|(O\setminus C)\cap\cup_jP_j|
$$

至多涉及$m$个不同私有块：每个比较主题只能触及一个$P_j$。每块遗漏量不超过$a_j$，故

$$
V_{\mathrm{private}}\le\sum_{r=1}^ma_{(r)}\le W.\tag{P}
$$

这一式无须假设最优遗漏全私有。它仅控制最优遗漏中的私有部分；共享遗漏的质量仍未被支付。

## 某个最优并集的遗漏全私有时的锐界

再假设**存在一个**最优$m$主题并集$O$满足

$$
O\setminus C\subseteq\cup_jP_j.\tag{H}
$$

不要求所有可覆盖客户的实际遗漏都私有；只要求某个最优比较并集如此。较强的“全部实际遗漏均私有”和更窄的“遗漏客户只属于一个目录标签”都蕴含(H)。

逐项把构成$O$的合法主题扩成包含它的极大覆盖，所得至多$m$个不同极大覆盖并集包含$O$，又不可能超过$\operatorname{OPT}_m=|O|$，所以并集仍恰为$O$。记其指标集$J$，$|J|\le m$。置$I=|O\cap C|$、$D=|O\setminus C|$。

对$j\in J$，(H)和全局私有性给$B_j\setminus C=Q_j$。所以

$$
D=\sum_{j\in J}a_j,\qquad\sum_{j\in J}v_j\ge I.
$$

后一式是重叠集合大小之和不小于并集，不把$v_j$误写成互不交。前$m$大非负席位之和至少任意至多$m$个指定第一席位之和，代入(S)：

$$
W\ge\sum_{r=1}^m\lambda_r
\ge\sum_{j\in J}(a_j+v_j/m)\ge D+I/m.
$$

利用$I\le W$，得到

$$
\boxed{\operatorname{OPT}_m=D+I
\le W+(1-1/m)I\le(2-1/m)W.}\tag{T}
$$

较弱半覆盖由(P)也可立刻得到，但(T)保留余客户信用后给出锐常数。$m=1$时退化为$\operatorname{OPT}_1\le W$；全零实例全部席位零，用乘法不等式，不定义效率比。

## 每个人数的完整SPE匹配构造

对任意$m\ge1$，取一个含$m$个单位客户的主题$A$，再取$m-1$个与$A$及彼此不交的singleton主题。规定在**每个有序历史**每位玩家均选$A$。

任意当前前缀已有$a$人选$A$，还有$r$人（含当前）。遵循策略的当前收益为$m/(a+r)\ge1$，因为$a+r\le m$。当前改选任一singleton的最终收益至多1，后继仍按该完整策略全选$A$。改选$A$就是原选择。故每个合法节点所有偏离都不优，构成完整纯SPE；这不是仅在轨路径证书。

实际$W=m$，最优选全部$m$个主题覆盖$2m-1$个客户，遗漏全为私有singleton。于是(T)取等，前$m$大谱值也均为1。$m=1$时仅有$A$，同样合法。这是既有all-big家族的整数版本，不认领新构造；它也用于[三人锐界](三人锐福利界--定理.md)和[两人税界](../引理/固定背景两人税界--引理.md)的匹配例。这里新用途是验证条件(H)的全部人数锐界和谱预算。

## 与旧superset、路由席位及一般目标的关系

旧`CA-MAXIMA-SUPERSET-SEATS`取完整$P_j$、固定路由计数$p_j$和共享信用$|B_j\setminus P_j|/m$，在根端以统一第$m$大值$\nu$得所有人保底及$W\ge m\nu$。本对象沿用“当前整极大主题支配同终局后继子主题”的机制，但改用固定子块$Q_j$和**真实触块次数**$q_j$。只有后者才让实际每个位置都从零触及重读第$r$大值。不能在旧路由公式中直接将第$m$大换成第$r$大，也不能因前缀未触块就说前缀未路由到$j$。

对同一目录与终局，本对象单个原始席位甚至不高于旧席位：若$b_j=|P_j|-a_j$，

$$
f_j^{\mathrm{new}}(k)-f_j^{\mathrm{old}}(k)
=-b_j(1/k-1/m)\le0.
$$

增强来自可逐位置重置并求整段谱，而非逐席数值支配。新旧总下界也不必相互支配；若实际已覆盖$m$个等大不交极大主题，各大小$L$，则新$Q$全空只能给$W\ge L$，旧根谱可给$W\ge mL$。

[动态路由席位](../引理/动态超集席位保底--引理.md)保留共享负载$p_I+r$，也使用不同状态；其[四个合法路径收费障碍](../障碍/六极大动态席位合法路径收费--障碍.md)不能作为本实际遗漏谱的反例，反之本条件定理也没有使任意路由路径预算成立。

由(T)可知，若真正存在$W<\operatorname{OPT}_m/2$的完整SPE反例，那么它的每一个最优比较并集都必须遗漏某些同时属于至少两个不同极大覆盖的客户。仅加入互不相交私有奖励、私有储备银行或永不触及这些遗漏块的威胁，不能越过这条必要边界。下一义务是控制最优覆盖的**共享遗漏**，并与私有席位和已覆盖客户信用共同计账；不能把各自支付过的同一份$W$再次相加。一般六人目标仍不由本条件定理解决。

## 实读、核验和出处

主源完整实读并逐式重构：`source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/customer_attraction/uncovered_private_seat_spectrum.md#1-精确对象与一般残余席位引理`、`#2-在实际遗漏上每期重置完整席位谱预算`、`#3-条件性半覆盖及一般构造必须跨过的边界`、`#4-旧席位机制实际新增状态与证据`。两冻结提交内容相同。

内部盲重构来源`source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/customer_attraction/uncovered_private_seat_spectrum.md#1-对象和更一般的阈值引理`、`#4-锐性退化与量词攻击`、`#5-和旧-gs2--gs3-的准确关系`完整复核退化、部分触块、同覆盖标签和不支配关系。旧接口全文实读为`source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/customer_attraction/sunflower_maxima_bound.md#8-任意共同目录可用的-superset-席位接口`。

普遍结论依据上述解析引理与覆盖代数。原有限审计调用仓库SPE枚举器；本轮另写[字面有序历史独立实现](../../tools/evidence/private-seats/replay/private-spectrum-independent.py)，不导入仓库模型或求解器，重现三个具名客户上全部255个非空目录、$m=1,2,3$的765对、1599条可实现有序SPE路径、3660项位置比较，以及$m=1,\ldots,6$的全历史all-big检查。详见[证据对象](../计算/私有席位谱与六极大证据--计算.md)。这些有限检查不代替全称证明；内部审查不等于外部同行评审，也未认证全球新颖性。
