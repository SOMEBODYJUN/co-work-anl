---
id: "customer-attraction/dynamic-exchange-assignment-certificate"
kind: "computation"
type_tag: "计算"
title: "Möbius动态交换完整策略与静态排列证书"
status: "complete"
truth_status: "frozen-certificate-read-no-author-audit-rerun"
review_level: "complete-seven-source-read-field-reconciliation"
scope: "7份冻结来源：README、正文、单位客户输入、全策略、witness、exact报告、Fraction审计代码；不含未认领witness生成器"
summary: "逐字段保全1953客户实例、43历史/258比较策略、唯一最优支持及六assignment成本；原审计代码未重跑因其未领取witness依赖缺失，冻结exact报告与正文已完整读取。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/dynamic_exchange/README.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/dynamic_exchange/static_optimal_assignment_counterexample.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/dynamic_exchange/assignment_instance.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/dynamic_exchange/assignment_full_policy.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/dynamic_exchange/assignment_witness.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/dynamic_exchange/audit_assignment_witness.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/dynamic_exchange/assignment_exact_audit.json"
---

# Möbius动态交换完整策略与静态排列证书

## 原件分工和未领取依赖

七源全部已clean show取得并全文实读，原件保存在 [original/](../../tools/evidence/dynamic-exchange/original/)。README指向的 `assignment_witness.json`虽在本批原件中，生成它的发现/简化脚本不在本批；故本轮不声称重跑作者Fraction审计，避免把缺失未认领依赖当成本批已验证程序。冻结 `assignment_exact_audit.json` 作为源报告完整读取，独立父代理单位复核在原正文中被区分为后续材料，不改称本轮外审。

| ID | 内容 | 独有保全 |
|---|---|---|
| 8c89fc3bd9113926f1a4 | README | 研究合同、文件关系、exact失败结论、Möbius依赖、下一步边界 |
| c73db261be5c87159a04 | 主正文 | 公式、全策略表、静态矩阵、机制和半覆盖边界 |
| ff1a437e39e730d230eb | assignment_instance.json | 63类型全部1953单位客户重数 |
| be317a14860bf5650dfe | assignment_full_policy.json | 根、6个第二动作、36个最后动作、实际路径 |
| 850a9b379cc0c33f9ee6 | assignment_witness.json | 13个非零F值和发现策略压缩输入 |
| ec2a4bfedc537bbbee49 | audit_assignment_witness.py | 独立Fraction重放逻辑及其对witness依赖 |
| d2f36e9a1cb98bb0a7e9 | assignment_exact_audit.json | 冻结完整报告全部结果字段 |

## 冻结报告逐字段核对

报告状态是“exact complete-history counterexample to static optimal-tuple assignment bridge only”，包含：

| 字段 | 值 |
|---|---:|
| fresh_histories / fresh_comparisons | 43 / 156（fresh action计数按源报告） |
| full_histories / full_comparisons | 43 / 258 |
| minimum_SPE_slack | 0 |
| M / K_M2_sufficient / K_exact_threshold / K | 456 / 1825 / 31 / 31 |
| customer_count / min_type / max_type | 1953 / 1 / 61 |
| actual / payoffs / W | (0,3,4) / (1733/3,1736/3,1736/3) / 1735 |
| unique_optimal_support / OPT | (1,2,5) / 1740 |
| minimum_assignment / assignment_minus_W | 1736 / 1 |
| half_margin | 1730 |

JSON的 `static_signed_matrix` 恰是正文矩阵M；六种排列成本 `{1736,1737,1736,1736,1737,1736}`全部保留。完整策略文件有43个键，包含空历史、六个长度1历史和36个有序长度2历史；对角重复历史没有删除。

## 原审计代码的真实范围

`audit_assignment_witness.py`只导入标准库Fraction、itertools、ceil、json。它从witness中的13个F值/策略重建fresh三人游戏，核所有不同前缀；再按M1 Möbius公式计算x、K、正类型重数r；为重复历史补最后一动作最佳回应；最后重算全43历史、258动作、覆盖W/OPT和六个assignment。

关键是：该程序在同目录读取 `assignment_witness.json`，并旁写更新后的 `assignment_instance.json`、`assignment_full_policy.json`、`assignment_exact_audit.json`。本批虽完整读取了这些原件，但没有执行这份代码，因为生成/简化脚本不在七源且会覆盖原冻结派生文件；因此本页状态是“原报告和输入全读、作者审计未在本批重跑”，不是伪造的exit0。原文所述的完整定义级审计结论作为来源报告保全，不因未重跑而改写数学对象。

Möbius偏置的关键算术已在正文和JSON相互核对：$\sum|x_B|=456$、K=31保证所有类型重数正；三不同标签终局偏置是 $1736/3$；实际F边际给u和W。OPT三元支持表与唯一支持、assignment矩阵列顺序均逐字段一致。

## 接续边界

本证书可复用作关闭静态assignment接口的原始输入，但不能作为Q-CAG-HALF反例，因为half_margin=1730>0。它还不反驳使用真实改变后缀的ROW或多节点预算；后续若引用，必须链接[静态排列反例](../反例/静态最优主题排列的冻结后缀失败--反例.md)并保留其“只否定(A)”量词。

未领取的发现MILP、witness简化及其他R-105f来源不在本批receipt；不从文件名推测优化器状态或更小客户数。无外审、新颖性认证。
