---
id: "customer-attraction/pb-background-on-path-prefix-obstruction"
kind: "obstruction"
type_tag: "障碍"
title: "PB大背景作为实际前缀的最后D单例偏离障碍"
status: "proved-specific-on-path-obstruction"
summary: "原PB参数和目录下，任何精确实现指定背景后再接2475个regular行动的完整路径，都有最后D-singleton玩家的真实严格偏离，故不能成为根SPE实际路径。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/security_continue/direct_PB_prefix_obstruction.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/security_continue/direct_PB_prefix_obstruction.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/security_continue/README.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round5/menu/pair_attack.md"
---

# PB大背景作为实际前缀的最后D单例偏离障碍

## 精确排除范围

使用[任意合法背景PB反例](../反例/任意合法背景的前两人额外槽安全值--反例.md)的**原目录、原参数和原指定背景b**。考虑任意有限行动前缀，它可任意交错regular、R-singleton、D-singleton，只要逐客户负载最终恰为b；再接r=2475个实际regular行动。

**结论：任何这样的一条完整有序路径都不能是根纯SPE的实际路径。** 无论怎样补齐所有离轨子树，其中最后一位D-singleton玩家总有一个regular主题的真实严格偏离。它不要求前缀采用最初示意的“全singleton”实现，也不冻结该偏离后的任何玩家。

这只是指定PB构造的实际前缀迁移障碍，不反驳合法背景子SPE的存在，不证明实际前缀版本PB、LAST或一般half，也不排除改目录、参数、背景或其他根构造。

## 所需输入性质与实际路径计数

参数为d=20、k=3、q=12、Q=2063、H=100000、M=10^9、r=2475。R为全部R块客户，D为全部D块客户；二者都是单位客户。

原目录只含regular和所有客户的singleton。每个regular至少覆盖dq=240位R客户，至多覆盖dkq=720位R客户；R-singleton覆盖一位R客户，D-singleton不覆盖R。指定b在每个R块的q−1名客户上为M、另一名上为M+1，在每位D客户上为HM。

因此指定背景的R类覆盖份数总和为

\[
 L_0=\sum_{x\in R}b_x=dQ(qM+1)=495120000041260.
\]

这里按客户累计覆盖**次数**，不是R客户人数。其后r个regular实际行动使整个实际终局的R总负载至多

\[
 L=L_0+r\,dkq=495120001823260.                         \tag{1}
\]

## 任何精确背景实现都需要D-singleton

反设前缀没有D-singleton。任取一位D客户，只有regular可能覆盖它；它需要HM份背景覆盖，所以前缀regular行动数N_reg≥HM。

另一方面，每个regular给R总负载至少dq份，因此

\[
 N_{\rm reg}\le\frac{L_0}{dq}
 =\frac{Q(qM+1)}q
 =\frac{24756000002063}{12}<HM=100000000000000.         \tag{2}
\]

矛盾。这一计数允许前缀中任意多R-singleton，它们只会进一步消耗L_0，不会改变N_reg的上界。

于是完整被考察路径中存在最后一个D-singleton玩家i，规定行动为{y}，y∈D。由于后r个行动都是regular，i发生在指定背景完成之前。该背景最终给y负载HM，后来负载只增不减，故i的实际终局收益满足

\[
 u_i=\frac1{c_y}\le\frac1{HM}.                        \tag{3}
\]

## 对真实后继完全不作冻结的偏离

i之后的**实际路径**已没有D-singleton。原目录的其余行动都至少覆盖一位R客户，因此i之后的人数n_i不超过这些实际行动给R的总覆盖份数，进而n_i≤L。

这个实际路径计数只用来确定同一节点之后的玩家总人数。i偏离后，行动内容可以全部改变，但后继人数n_i不变。

i尚处于指定背景完成之前，故其节点每位R客户的旧负载≤M+1。让i改选任意regular主题T，再执行原完整策略在这一偏离后的真实后继。无论这些后继如何行动，T中至少dq位R客户的最终负载逐个至多

\[
 (M+1)+1+n_i\le M+L+2.
\]

因此这个真正可选动作保证

\[
 D_i(T)\ge\frac{dq}{M+L+2}.
\tag{4}
\]

精确交叉乘法为

\[
 dq\,HM-(M+L+2)=23504878998176738>0.
\]

结合式(3)–(4)，D_i(T)>1/(HM)≥u_i。这是原完整有序历史游戏的一次严格获利偏离，违反SPE，证明结论。它甚至不依赖偏离后继本身的均衡性，只使用每位后继最多给某个客户增加一份覆盖。

## 可复用的路径排除原则

上述论证抽出一个具体工具：若目录分成不触R的单客户动作和每个至少触一位R客户的其他动作，考虑实际最后一位前者。终局R总负载可上界它之后的人数；若当时R前缀负载另有上界，一个大R主题便给对所有真实续局有效的分母保底。当这个保底严格超过该单客户行动的实际收益上界，路径就不可能在轨。

这个工具没有给互斥分支一份共同福利预算，也不把任意合法背景变成实际根前缀。对当前PB原参数，阻碍已存在于规定路径自身，补写离轨SPE无法消除它；若要继续构造，需实质改变使最后D-singleton有利的计数冲突。

## 来源、算术与关系证据

源5b753273b2fb8219b7bc原标个人解析记录、待独立复核；本轮全文实读并重建式(1)–(4)，同时核对完整PB原稿及四份子SPE审查的合法背景边界。后者没有声称证明实际前缀可到达，因此此障碍是补充，不是推翻其子博弈反例。

本轮用Python Fraction和整数从给定参数直接重算L_0、L、regular次数上界及正交叉乘积，详见[算术记录](../../tools/evidence/pb-background/replay/prefix_obstruction_arithmetic.json)与[复现说明](../../tools/evidence/pb-background/README.md)。这次标量核算没有枚举巨大前缀或策略树；所有排列和真实回复的范围由以上通用论证承担。

接续README源e05edfe94ae06a486565把此问题与[查询税余量](../引理/实际末两人的查询税余量--引理.md)并列为两条尚未闭合的方向。本页准确保留其停点：税池方向仍缺早期总亏损共同支付；PB方向必须改变实际前缀冲突。第三阶段应将本对象连为“指定背景的在轨迁移障碍”，不能连成PB子SPE反例失效或half已证。
