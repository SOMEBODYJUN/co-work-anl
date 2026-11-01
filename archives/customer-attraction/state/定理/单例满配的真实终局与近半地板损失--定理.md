---
id: customer-attraction/exact-SPE-singleton-terminal-family-near-half-floor-loss
kind: theorem
type_tag: 定理
title: 单例满配的真实终局与近半地板损失
status: proved-all-prefix-all-parameter-family;rules-out-uniform-floor-coefficient-above-half
summary: q=m−1个不交单例与m名单位玩家在每个前缀都使HI恰等真SPE终局，但根累计floor仅m/2、所有SPE福利OPT=m−1；没有假终局也损失近半。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-977d3dbff13346b3b7c0f5a4caa6168e/parent/interval_root_budget_independent_review.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-977d3dbff13346b3b7c0f5a4caa6168e/credible/exact_floor_half_tightness.md
---

# 单例满配的真实终局与近半地板损失

原单位客户共同目录模型，任意q≥1，m=q+1名单位提供者，目录恰q个互不交单例主题，每个主题只覆盖自己的那一名单位客户。重复行动及全部有序历史平局允许。终局z中占用题a的一人收益1/z_a，未占用辅助坐标取0。

H_I/L_I/E_I/G_I采用[完整区间递归](区间终局剪枝的上界比较与全效率目录类--定理.md)。R(b)表示合法有序前缀计数b后，所有完整纯SPE可实现的终局计数集合，不是一份固定Markov策略。真BI在孩子R_a上取l=max_a min_(z∈R_a)U_a(z)，只保各孩子满足U_a(z)≥l的终局；不同有序孩子的完整策略可以独立拼接，因此该逐终局筛选必要且充分。

## 每个合法前缀的完整闭式

设j=|b|，d为已用不同主题数，r=m−j。终局r0时H_I=R={b}、G0，不定义非终局floor。r>0时：

| 前缀种类 | 完整终局集合H_I(b)=R(b) | L_I(b) | G_I(b) |
|---|---|---:|---:|
| 已有重复，j−d≥1 | 保持b，后r人选r个互异fresh主题 | 1 | r |
| 全异，j=d | 全部q主题各出现一次，恰一主题总数2的全部q个终局 | 1/2 | r/2 |

这同时给出纯SPE集合精确性与累计预算，不仅是一个实际路径的计算。

**已有重复。** fresh数q−d≥q−(j−1)=m−j=r。按剩余r归纳，当前fresh后仍有此前重复，孩子只选其它fresh，当前份额1；当前旧题后孩子也全fresh，其份额1/(b_a+1)≤1/2。所以真BI和区间EI都只允许fresh，L1，所有r个互异fresh组合都能逐节点选BR实现，G=1+(r−1)=r。已有任意严重重复也包括，不删除固定背景。

**全异。** fresh数q−j=r−1。当前旧题马上进入重复类，后r−1位填完全部fresh，当前利润恒1/2。r≥2时当前fresh后仍全异，孩子归纳终局仅一题重复，当前利润为1或1/2；1/2确可实现：下一位重复该新题，再填其余fresh。于是每个动作孩子最小值均1/2，所有动作eligible且每个孩子终局当前利润≥1/2，真BI也完全不删，H_I=R。

其并集恰为全部题各一次外加一题重复；任意哪题重复都有合法路径实现。r1时所有题此前都已用一次，末位任题皆1/2，直接同结论。r≥2时fresh孩子G=(r−1)/2，而旧题孩子G=r−1；最小递推选fresh，得到G=1/2+(r−1)/2=r/2。q1/m2边界亦保，那里可实现利润只有1/2而未必两种值都出现。

## 根福利、最低支付路径与严格系数障碍

空根全异，所以
\[
\boxed{H_I(0)=R(0),\quad G_I(0)=m/2,\quad
W(\sigma)=OPT_m=m-1\text{ 对每份完整纯SPE}.}
\]
先各选一个不同主题、最后一人重复任意题，是一条完整可信路径；沿途每个非终局前缀都全异，每期floor1/2、总m/2。实际仅重复题的两位各得1/2，其余m−2位各得1，差为(m−2)/2。

这不是不同客户输入、假终局或不可信前缀造成的损失。各节点能实现其最低当前收益，但不能沿这条同一真实路径让每位同时处于自己的低收益终局。把H_I换成精确R再重新算相同的max-min floor及最小路径和也不改善。
\[
OPT_m/G_I(0)=2-2/m\to2,
\quad G_I(0)/OPT_m=m/[2(m-1)]\to1/2.
\]
因此任何普遍G_I≥c OPT且c>1/2的加强都假：取m使m/[2(m−1)]<c即可。这个家族仍有G_I>OPT/2，不能据它否定精确系数1/2的开放义务，更不能反真实SPE半覆盖（本类始终全效率）。

[共同终局祖先价格](祖先门槛的共同终局根价格与标记流等价--定理.md)取λ0直接给min_HI W=OPT_m，所以该更强价格预算避开本族floor错配；没有因此证明一般最优价格half。

## 来源读序与有限检查范围

4803B父审第三节自记在读稿前重构本全参数证明；4423B作者稿是当时待父审的自足证明。两份全文与当前已成稿对象逐项比较，本轮再按两类前缀重构，保父方先验、不将知情清洗叫新增盲审或外审。

作者audit_exact_floor_tightness.py原记录q1…6全部合法计数前缀、显式HI与真BI/闭式集合/L/G；本批没有读取或执行该原代码/报告，不能把解析归纳称一次新穷举run。原父审关于五环和29客户的独立事件分别属于另外两个来源/输入，不能拿它们替本单例族小参数审计造日志。任意q的结论来自上述归纳，无一般算法位复杂度、新颖性或six-half闭合认证。

原件/指纹、逐源比较与准确复用范围见[本批证据](../../../../tools/evidence/interval-comparison-and-exact-floor-primary/README.md)。
