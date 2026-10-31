---
id: "customer-attraction/r29-direct-prefix-extra-slot-historical-status-resource"
kind: "resource"
type_tag: "资源"
title: "DIRECT与前缀门槛的历史量词和后来反驳"
status: "complete"
review_level: "full-primary-reading-self-contained-reconstruction-and-new-exact-check"
summary: "原DIRECT/PREFIX/extra-slot/Mfull未闭合是历史；已证银行完整族分别否定逐人桥，三窗口和54尾例自身仍不是这些根反例，half与安全聚合保边界。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-29b83efed6b045678e3b7ee11dffb7b3/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-29b83efed6b045678e3b7ee11dffb7b3/README.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-29b83efed6b045678e3b7ee11dffb7b3/general_proof/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-29b83efed6b045678e3b7ee11dffb7b3/general_proof/README.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-29b83efed6b045678e3b7ee11dffb7b3/general_proof/potential_attack/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-29b83efed6b045678e3b7ee11dffb7b3/general_proof/potential_attack/README.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-29b83efed6b045678e3b7ee11dffb7b3/new_representation/opt_threshold_cycle.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-29b83efed6b045678e3b7ee11dffb7b3/new_representation/opt_threshold_cycle.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-29b83efed6b045678e3b7ee11dffb7b3/security_bridge/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-29b83efed6b045678e3b7ee11dffb7b3/security_bridge/README.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-29b83efed6b045678e3b7ee11dffb7b3/GENERAL_WORKING.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-29b83efed6b045678e3b7ee11dffb7b3/GENERAL_WORKING.md"
---

# DIRECT与前缀门槛的历史量词和后来反驳

## 原候选层级和root/PREFIX量词

共同目录单位客户、任意m、全部有序历史纯SPE，实际收益u_i、福利W、m主题最优覆盖OPT_m。原DIRECT要求每份空背景完整根SPE的每个实际玩家2m u_i≥OPT_m；求和可推出half，只是充分加强，不是half等价。它也不同于较弱净缺口mu_i≥OPT_m−W。

原EXTRA-SLOT-INDIVIDUAL要求u_i≥v_(m+1)(0)，对手m个整数静态槽、不观察查询；静态OPT_m≤2m v_(m+1)使extra-slot蕴含DIRECT。保完整m槽真实根菜单的Mfull若能自由混列cap≤u，也蕴含extra-slot，因为真实完整列只是全部合法静态m元组的子集。各方向不能倒用，不把tail m−1槽菜单偷换成保根m槽。

PREFIX固定原实例总人数m及OPT_m，量化每个不超过m−1个合法主题前缀后的每份子SPE，门槛仍OPT_m/(2m)。它允许非最优祖先，所以足以进行最小坏剩余人数归约；DIRECT本身不允许悄然扩大此背景量词。PREFIX⇒DIRECT，未证明等价；目前两者一般全称版本都已由下面同一个零前缀真反例否定，不能继续列OPEN。

## 后来银行族是真正完整根反例，不是本环或固定尾例

已完整比较[银行一般族](../反例/笛卡尔银行目录的逐人分数门槛反族--反例.md)：每m≥2，用m个经济客户、m−1个两客户银行块、全部m(m−1)个共同主题(一个经济+一个银行)。完整有序历史BASE/PUNISH/EXIT控制器已经证明所有再次联合偏离和固定过去处罚目标，给
\[
 u_1=1+1/(m-1),\quad W=2m,\quad OPT_m=3m-2.
\]
原定理的全历史可信性在已读正式对象，本批仅复用，不新跑银行控制器。于是
\[
 {OPT_m\over2m}-u_1={m^2-5m+2\over2m(m-1)}>0\quad(m\ge5).
\]
分子为2+m(m−5)，直接全人数严格；m5为13/10−5/4=1/20，m6为4/3−6/5=2/15。它否定DIRECT，并因空前缀包含在PREFIX中而同时否定更强PREFIX。不能说54固定旧玩家子局或未理性的三窗口菜单完成了这个反驳。

同一族自由分数m槽值δ_(m+1)=3/2−1/(2m−1)，Jensen使真正整数v_(m+1)≥δ_(m+1)；m≥4时δ_(m+1)>u1，m4差1/42，故extra-slot一般逐人桥亦已否。保根Mfull当前[完整银行菜单](../反例/笛卡尔银行完整根菜单的低值自洽分布失败--反例.md)另给m4精确cap59/36>根4/3，否定存在低cap列混合；不是拿一个坏对称NE去否定存在量词。

但这些输入half余量2W−OPT=m+2>0。其真正整数v_m≤2：固定m−1个竞争主题，让银行各出现一次、经济互异，每查询经济份额≤1、银行份额=1；这个不观察查询的对偶给上界2。因此W=2m≥m v_m，本族**不反驳真正安全聚合**。根完整菜单值、自由分数门槛和整数静态值并未被宣称相等。

## 原阴性实验和正确不适用性判断仍保留

| 原记录 | 本批证据等级与现在用途 |
|---|---|
| GENERAL_WORKING/boss攻击15旧完整策略锥 | 仅相关工作稿的历史报告：LP点需Fraction核非负/IC/归一化，未有精确负点；无完整对偶或锥最优认证。不重跑，不据此证明全部策略。 |
| potential_attack两锥 | 原报告四人259历史root-tax锥O/u1=7未过8；三人43历史X/Y锥浮点约4.20562390158未过6。没有完整有理最优对偶，不能称精确全域最优；它们没覆盖后来银行m5真例。 |
| 34客户逐人v3反例 | u1=29/3>OPT3/6=17/3，确不否定DIRECT。这个适用范围核对正确，却不能当DIRECT正面证据。 |
| 三窗口环 | 精确击穿根低/尾高松弛，但末位可获3，非完整SPE；其当时“本页未反驳DIRECT”仍对该例成立。 |
| 54客户静态尾PNE支配反例 | 固定合法旧主题后的完整两尾SPE，原根未认证；它反驳的是观察者静态替换桥。 |

原source的“尚未证明/未闭合”标签是2026-10-24阶段历史，不能被后来整理沿用成当前OPEN，也不改写当时原字节。WP2在security README只是旧名称导航，本批未取得其完整精确合同，**不凭名字认证其当前真值或与FM同义**。一般背景半利润、安全聚合及half不能随逐人加强失败而一并判假。

新检查只按已证银行公式代入m2…12，核准确门槛符号与显示分数，未重审原银行全树。一般严格域m≥5/m≥4来自解析分子。source-state-updates另保准确旧段/SHA与当前已读证明接口；本批没有外审/新颖性声明，也不把新状态归功给旧有限扫描。
