---
id: "customer-attraction/four-player-static-assignment-independent-review-evidence-contract"
kind: "review"
type_tag: "审查"
title: "四人冻结匹配独审的报告与复用边界"
status: "full-original-review-preserved; claimed-independent-code-and-output-absent; different-old-success-reused-with-scope"
summary: "保2026-10-21独审对象、全部有序策略/终局量词、1554含self计数及静态矩阵；作者独立实现报告与已实际成功的另一origin程序分开，不增加新审查者或运行。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/direct_global/static_matching_counterexample_independent_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/direct_global/static_matching_counterexample_independent_review.md"
---

# 四人冻结匹配独审的报告与复用边界

[2869B原独审](../../../../tools/evidence/monochromatic-tax-and-full-menu-contracts-primary/original/a78d96dc6f303010aea7/research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/direct_global/static_matching_counterexample_independent_review.md)日期2026-10-21，direct_global，审查同个人区static_matching/static_matching_counterexample.json。FJ已全文实读并核SHA；本批正式primary诚实复用，不把再次归档当新增盲审者。

它反驳的精确辅助桥是：对每个有限单位客户共同目录完整纯SPE实际终局z，存在达到OPT_m的最优m主题元组及到实际角色的匹配，使Σ_i u_i(T_i,z_−i)≤W。z_−i冻结其他实际行动；该诊断不沿改变后历史继续，不能用SPE直接限制。原稿结论“独立定义级审计通过、无fatal objection”是原内部报告身份，不是外审或新颖性认证。

## 作者报告的方法和计数

原稿指static_matching_independent_audit.py及同名JSON，称只用Python标准库，不导规范model/solver/verify或作者搜索器；先把重数展开52名编号不同单位客户，按每终局覆盖者数直接算Fraction利润。完整策略字典需无重复覆盖1+6+6²+6³=259有序决策历史；每历史h与每行动a都分别沿原策略真完成h和h+a，比当前玩家真实利润，不能合并同负载不同顺序，也没有冻结这些SPE比较的后继。

报告1554项含自身比较，285平局、1269严格。259项规定动作自身必是平局，故按作者数字换算为1295项非自身，其中26平局、1269严格；这是计数换算，**不是新执行**或新增IC样本。它又称枚举6⁴=1296有序终局，包含重复/少主题补重复，恰24个最优叶为(0,1,4,5)各排列。六主题覆盖集合两两不同；actual=(3,3,2,2)、四人各47/4、W47、OPT4=52，所以2W−OPT42>0而非half失败。

## 全部静态矩阵及存在量词

同一actual的四行冻结查询为：

| 原角色位置 | T0 | T1 | T4 | T5 |
| --- | ---: | ---: | ---: | ---: |
| 1 | 51/4 | 38/3 | 51/4 | 71/6 |
| 2 | 51/4 | 38/3 | 51/4 | 71/6 |
| 3 | 47/4 | 35/3 | 47/4 | 35/3 |
| 4 | 47/4 | 35/3 | 47/4 | 35/3 |

两组相同行源于actual同主题角色冻结身份对称，不是假设完整策略匿名或平局规则对称。全部24匹配12个为48、12个为293/6，最小比W多1；(0,5,1,4)给51/4+71/6+35/3+47/4=48。最优支持与全部匹配都被量化，强于只否定某固定最优匹配。允许更大预算、真正离轨回复、查询安全值、跨节点运输等并未因此反驳。

[52客户自足反例](../反例/最优组合冻结匹配的一单位缺口--反例.md)已完整保52客户和259个有序决策节点，并从三个私有块及{0,2}/{0,3}直接证唯一0145；再从基线281/6及目标0、1、4、5对应增量(1,1,1,1/6)解析穷尽24Q，不只信JSON字段。该对象还证无条件OPT≤Q+(1−1/m)W，弱预算Q≤(1+1/m)W足推half；本例48<235/4，故不反这条弱化。分区一次收费R和真实偏离V各有自己的量词及反例，不能凭“匹配”同名合并。

## 原缺件和实际可复用证据

实际原独审代码ID1894bab391f4c921d293、4852B/SHA6b4caa4542594092ed639ae28f1a7486d2a1fab50c282f3169df0bc7745fa65d；同名报告4638f7b82684049fdae6、3789B/SHAdbab286597b6f62916a1bc3f9c46bfa5d4ad881b6432131893afea82d9478188，先前纯本地读取均缺blob。本批复用缺失回执，不重试网络，不说已读代码/JSON、原CLI已复现或285等字段获得新认证。

另一份[origin来源回撤程序的旧实际重放](../计算/来源回撤原程序与有序策略的精确重放--计算.md)确已在同SHA52输入上核259节点1554含自身比较，输入SHA9e7cf1437a7b03fe89d843d4ae20efa3c6a4137373098ed1220d4370656a5245。FJ已完整读其10829B代码、命令/exit/报告/输入绑定；本批核FJ证据SHA复用，0重跑。它是不同实现和研究用途，不冒充缺失4852B原独审，不把另外五fixture或旧0.368秒说成本批新样本/时长；不读取all_assignments/unique_optimal_supports也不报告285平局。实际SPE成功、作者独立审查报告、原文概率/搜索声明分别标明。

本页保存的是完整审查资源及其可复用证据合同，没有增加审稿人数、原程序执行或一般数学结论；原对象之外无需发消息找审查人或凭据。阶段二关系见[本批完整证据](../../../../tools/evidence/monochromatic-tax-and-full-menu-contracts-primary/README.md)，不把review PASS写成六人half证明、外审或全局最小性。
