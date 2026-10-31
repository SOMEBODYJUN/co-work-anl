---
id: "customer-attraction/seven-client-three-topic-tail-two-cycle-witness"
kind: "counterexample"
type_tag: "反例"
title: "七客户三主题尾响应二循环的透明完整SPE"
status: "complete"
review_level: "full-primary-reading-self-contained-derivation-and-new-unit-client-check"
summary: "13节点策略使对角25/6小于交叉26/6，半半去相关差−1/24；纯BB尾列cap2，不能反驳自由菜单，half成立。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-28e8b1905f3b4a1f934d87d8071ccd67/CLAIMS.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-28e8b1905f3b4a1f934d87d8071ccd67/CLAIMS.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-28e8b1905f3b4a1f934d87d8071ccd67/independent_audit/blind_tail_cycle_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-28e8b1905f3b4a1f934d87d8071ccd67/independent_audit/blind_tail_cycle_review.md"
---

# 七客户三主题尾响应二循环的透明完整SPE

## 准确失败命题与模型

采用[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)：有限单位客户及提供者、有限非空共同主题目录、全部有序历史纯SPE、客户价值均分，保重复、离轨与任意平局。这里三主题三玩家七客户，只否定“根真实尾响应租金矩阵的每个循环，对角和不少于循环交叉和”这个明确方向；不把不同符号习惯的“反单调”名称作定义。

该接口已由[真实后继去相关障碍](../障碍/自适应后继与真实菜单安全值--障碍.md)的较早实例否定。本例价值是更小透明的独立内部核对见证，不是新桥首次被否定，不声称客户/主题最小性、外审或全球新颖性。源内LOCAL-TAIL-CYCLE-7-WITNESS-v1是此有限见证身份，不是新一般定理。

## 七客户和全部13节点

客户兴趣类型为A一名、AB一名、BC三名、ABC两名，各人为不同单位客户。根C；第二人在首A/B/C后分别B/B/C；末位除CC后A外一律B。下表每格为当前选A/B/C后沿同一完整策略真实完成的收益，故包含全部离轨节点：

| 历史 | 选A | 选B | 选C | 规定 |
|---|---:|---:|---:|---|
| 根 | 2 | 2 | 13/6 | C |
| A | 3/2 | 5/2 | 13/6 | B |
| B | 2 | 2 | 5/3 | B |
| C | 13/6 | 13/6 | 13/6 | C |
| AA | 4/3 | 4 | 11/3 | B |
| AB | 3/2 | 5/2 | 13/6 | B |
| AC | 5/3 | 8/3 | 13/6 | B |
| BA | 3/2 | 5/2 | 13/6 | B |
| BB | 2 | 2 | 5/3 | B |
| BC | 13/6 | 13/6 | 5/3 | B |
| CA | 5/3 | 8/3 | 13/6 | B |
| CB | 13/6 | 13/6 | 5/3 | B |
| CC | 8/3 | 8/3 | 5/3 | A |

规定逐行最大，所以有限完美信息博弈的一步偏离原理认证完整纯SPE。根C严格最优；C后第二人为三方平局、CC末位A/B平局，不能将“根严格”扩称整树无平局。实际CCA收益(13/6,13/6,8/3)，覆盖全部七客户，W=OPT3=7。

## 租金矩阵、指定分布失败与自由菜单救援

根强制s后两个真实尾动作为q^A=BB、q^B=BB、q^C=CA。对独立查询t，定义R(t;q)=Σ_(x∈t)1/(1+c_x(q))。它是对同一实际尾的静态查询求值，不是把真实偏离的后继冻结。矩阵为

| 查询/触发信号 | A | B | C |
|---|---:|---:|---:|
| A | 2 | 2 | 5/3 |
| B | 2 | 2 | 8/3 |
| C | 5/3 | 5/3 | 13/6 |

因此R(B;q^B)+R(C;q^C)=25/6<26/6=R(B;q^C)+R(C;q^B)，差−1/6。p在B/C各半时，适应查询的对角均值减独立自身推送尾的全四项均值=(25/6−26/6)/4=−1/24，否定这份p的去相关。

但自由选择尾菜单分布时，纯BB列的全部查询cap=max(2,2,5/3)=2<根收益13/6；其余列CA对B查询为8/3，任何加入CA都令B值≥2，故这个尾菜单零和值恰为2。它没有否定自由菜单桥，不能迁移旧36客户例更强的“全部菜单混合均不足”性质。

源独审还明确指出旧36客户同为三玩家：X2/Y2二循环对角20、交叉24；若须包含实际根X0，取X0/Y2也有对角20<交叉21。较早四人例交叉差−11亦是同类接口。这些历史算术已有正式对象，本批只比较其完整正文，不再认证其原程序或额外done。

## 独立性和本次实际检查

原blind review声明先收陈述独立计算、未读作者证明，脚本不导入规范solver/verifier/作者代码；这是原审查的读序。本批已读全部五主文后再写检查，**不称新增盲审**。两原审计程序本地blob缺失且未懒取，未执行原入口。

新标准库Fraction核查将四类型展开为七名单位客户，按上述完整策略一次重算13节点39个含自身行动值（26非自身）、全部矩阵、循环差、纯BBcap和最优覆盖；PASS。有限给定策略认证由完整表成立，不由搜索无反例外推一般命题。原half主目标没有被此例反驳。
