---
id: configuration-assignment/equal-opening-cost-natural-lp-truncation-gap
kind: counterexample
type_tag: 反例
title: 等启用成本的自然预算LP与整数截断缺口
status: proved-correction-to-source-scope; arbitrary-cost-half-baseline-unaffected
summary: 两bin精确反例否定原等cost任意给定LP支持的1−1/e保证；floor修复缩小可用x且改变比较目标L。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/notes/configuration_reduction_boundary.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/multi_lane/research/topic_selection/notes/configuration_reduction_boundary.md
---

# 等启用成本的自然预算LP与整数截断缺口

原配置笔记第一轮§4写：“若openingcost相等，x在truncated partition matroid polytope中”，因而从给定自然配置LP点$x$得到相对$L(x)$的$1-1/e$舍入。**该说法缺少整数截断条件**。原$x$只满足每bin和$\le1$、每item marginal$\le1$、成本$\sum_ecx_e\le B$；没有$\sum_ex_e\le\lfloor B/c\rfloor$。

## 两bin、两物品的精确反例

物品$p_1,p_2$；bin1局部族$\{\varnothing,\{p_1\}\}$，bin2为$\{\varnothing,\{p_2\}\}$，均下闭。两正配置各利润一，启用成本$c=1$，预算$B=199/100$。输入给定点

$$x_1=x_2=199/200.$$

每bin与每item marginal均为$199/200<1$，总成本$199/100=B$，故满足原文全部自然LP约束。两配置没有冲突，线性目标和multilinear覆盖值都是

$$L(x)=G(x)=199/100.$$

自然LP最优亦恰$199/100$，因为利润等成本，预算给目标上界，显示点达到。整数解至多开$\lfloor199/100\rfloor=1$个bin，所以$\operatorname{OPT}_{\rm int}=1$。

若要求总是预算可行、期望利润或确定利润$\ge(1-1/e)L(x)$，则均不可能：每次利润至多一，期望也至多一；而$e>5/2$给$1-1/e>3/5$，故

$$(1-1/e)\frac{199}{100}>\frac{597}{500}>1.$$

这是原“**任意给定$x$**、对原$L(x)$比较”合同的反例，不是有限实验、对某舍入实现的失败或对CGST外部定理的反驳。

## 正确修复及不能保留的目标

等正成本$c$的整数可行集对应partition matroid截断到$k=\lfloor B/c\rfloor$，其多面体须有$\sum_ex_e\le k$。因此以下任一条件足以恢复原强界接口：

1. 预算比$B/c$为整数，原预算约束自动给该式。
2. 一般$B/c$，明确把该截断不等式加入分数输入合同/LP，得到**新**可用$x'$和比较值$L(x')$。

本例截断LP最优由$199/100$降为一；原给定$x$被排除。不能加一条约束后仍默认对原$L(x)=1.99$给原保证，也不能把“改LP/重求$x'$”说成原给定点舍入已经成立。[预算舍入页](../算法/给定稀疏配置的确定性预算舍入--算法.md)在修复合同下给完整证明。

自然LP与整数OPT的损失可趋近二：取$B/c\uparrow2$但小于二、两不冲突单位利润bin，总LP值趋二而整数仍一。因此忽略floor不是仅数值取整细节。若$c=0$，预算不起限制，回到普通partition，无此问题。

## 与其它已保存结论的关系

第二轮对任意非均匀成本、$0\le c_l\le B$给$(1-1/e)L(x)/2$的给定支持基线，不需$\sum x$整数截断；其最后比较整数集与一个可负担singleton正是允许这种损失，所以不受本反例影响。前批历史root review重构的是该一般成本基线，没有使用此第一轮等成本强断言；本批新增纠错页，不改旧共享正文。

本源的配置整数覆盖等价、初始layer-cake下界及指数地集复杂度警告也不受影响。受纠正的是“任意自然LP点自动在截断matroid多面体”的推理，绝不据此宣布所有已知次模舍入定理错误。[原件、逐节映射和关系证据](../../../../tools/evidence/retired-config-certificates/README.md)保精确定位。
