---
id: customer-attraction/five-eight-player-BR-credit-constructor-and-complete-count-policy-native-contract
kind: resource
type_tag: 资源
title: 五八人BR信用构造器与完整计数策略的原生合同
status: 原7917两固定mode各一次成功；两完整策略逐字节复现，前NI独审充分成功不重跑
summary: 确定BI输出一份可依count的合法完整策略，真实tie key与结果集合BI不同；证书全部字段/每policy行保，五人自由pivot阳性和八人首债失败是不同route状态。
source_refs:
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-6cf1f30515fe44eeba28d5390d6940e7/coordination_2026_10_23/audit_merge_br_credit.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-6cf1f30515fe44eeba28d5390d6940e7/coordination_2026_10_23/merge_br_credit_certificate.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-6cf1f30515fe44eeba28d5390d6940e7/coordination_2026_10_23/merge_br_credit_m8_certificate.json
---

# 五八人BR信用构造器与完整计数策略的原生合同

7917B原code、27685B五人和481955B八人证书全部原字段及每个210/11440 policy行均已实际读取；[源清单](../../tools/evidence/br-credit-constructor-and-policy-certificates-primary/source-manifest.json)。此前NI是necessary related、NQ是两独审输入/构造者context，均0额外done；当前primary责任逐源承接，不能把旧related读当此前primarydone。NX3真实合批claim 118d18f8eb8e9e4368574eced82afd4aa7f6e0bd pushed，本3 owner/in-progress/sourceSHA已核，原local_sync synced保；不预称正文已推或done。

原一般核/路由数学及NI真独审在[多源信用资源](多源整合核的真实BR信用与五八人路由范围--资源.md)和[原计算](../计算/多源BR信用与五环整数平台的原入口精确复核--计算.md)完整保存，NQ又给[独审输入合同](真实BR债原独审的策略输入与全历史覆盖合同--资源.md)。本页不重新授同一SPE/路由反例，保生成器真正算法、输出schema、数学角色和先验。

## 原单位模型、参数及完整BI为何合法

只标准库Fraction/lru_cache/Path/argparse/json，无原canonical/求解器导入、无外部输入或随机。CLI `--m`只准5或8，默认5；全局M/P/TOPICS在main按参数重新设，P=M+1。Ai={i,M+i}（i0…M−1）、R={0…M−1}，所有2M客户不同单位。主题两两不同；玩家可重复任意题，终局c的占用题a利润为Σ_(x∈topic_a)1/(Σ_(j:x∈topic_j)c_j)。只在a被当前/偏离者加一的终局调用，分母正，代码不承诺任意未占用输入的通用guard。

construct()对计数c递归全部P个孩子。终局sumc=M直接返c；否则每孩子先完成一份已选完整尾策略，再取tuple

`(utility(child_terminal,a), tuple(-q for q in child_terminal), a, child_terminal)`

的最大者，记录policy[c]=a并返该终局。第一目标当前收益最大；收益相同先取终局计数负字典序最大（即原计数字典序更小），再较大action。不能简写成所有收益tie只看最高标签。缓存保存**一份**确定终局/策略，不是canonical所有可实现SPE终局集合，不求最坏福利或枚举全部完整策略。

按余人数归纳，所有所选孩子都是合法纯SPE，当前选对这些真实孩子收益最佳，故拼成一份完整策略SPE。各有序history用policy[count(h)]，对本实例可合法采用这种count-policy；这不限制一般模型只能匿名。普通BI存在性足构造一份例，不声称任意count缓存单selector都代表全部历史依赖均衡。

verify(policy)不再调用construct内部solve，而从导出的map独立replay每计数及每偏离，仍共用同文件utility；它是构造后的分开检查，独立程度不同于不导该py的7883单位定义级独审。expected=count_states(M−1,P)枚举全部sum≤M−1的非负P维计数，域必须相等，故原210/11440 map不是只在轨动作表。

## 导出策略的全部真实字段

两JSON同schema，policy以counts字典序排序：每row仅counts整数数组/action整数。NI已全210/11440原row核长度6/9、每分量非负、总和<M、action合法、无重复/缺/额外；全部非policy字段也逐嵌套标量读，分别73和109个。完整输入byteSHA与每行域覆盖记录在前NI证据，不以只看样本替代全行读取。

| 字段组 | 原内容与责任 |
|---|---|
| status/model/m/topics | 文字说明一份精确count-policy/模型与参数；不替每节点IC |
| policy_count_states/exact_deviation_comparisons | m5 210/1260，m8 11440/102960，均含自身行动 |
| actual_path/actual_terminal_counts/W/OPT | 从给定policy根走到的路径/计数，W7或10，OPT10或16 |
| optimal_source_unique_multiset | [0…M−1]，y_i只Ai覆盖给唯一最优M元组，不借优化oracle |
| initial_A_pivot_slack_per_nonpivot_A | m5 11/5，m8 41/8，根cloneAi唯一回复R的真实行差 |
| R_pivot_reply/R_pivot_payoffs | m5回复4、所有Ai6/5/R1；m8回复7、所有Ai9/8/R1 |
| fixed_pivot_double_write_root_BR_lower_bound | 22/5或41/4；对比available_half_slack_2W_minus_OPT恒4及布尔 |
| expanded_route_BR_slack/updates_at_root/merge层 | m5根4步/总11/5/删重层0,1,2；m8根7步/总41/8/删重层0…5 |
| expanded_route_no_BR_credit_bound_holds | m5 true、m8 false，不因两者都有route就忽略支付差 |
| any_route_initial_BR_lower_bound/all_merge_routes_no_BR_credit_bound_fail/scope | 首债同上、m5 false/m8 true，范围仅已述先压缩框架 |

文件**没有actual_payoffs字段**；各玩家3/2、5/4、9/7、8/7由原独审另算/解析证明，不塞回原JSON。也没有源码SHA/argv/time/seed/完整K/D/M/P/E数值，不能把新事件或总账假造进旧证书。

## 原程序真正检查的route及不检查的部分

verify重放全policy每状态每行动，m5比较210×6=1260含自身，m8 11440×9=102960含自身；前NI7883 --m5另展开1555有序节点/9330含自身，不能混成同一计数。根actual55543或88888876，W=M+2；全部Ai覆盖2M总客户上界，OPT=2M。

任一初pivotAi的clone历史Ai^(M−1)，R唯一BR，非pivotAj收益2，R收益M−1+1/M，slack=M−3+1/M。所有最优源初为全Ai，无重复。fixedpivot两写下界是2slack。

代码另明确构造自由pivot路线：源list全Ai，先old0→R、pivot1；然后old1…M−2各用R作pivot改成最高Ai=M−1。每次assert old/pivot在当前源且不同，按**同原policy**真clone回复求非负slack，列表更新；最终{R,A_(M−1)重复M−1份}，再删M−2次该重复Ai到两源。m5总11/5≤4可付，m8首41/8>4且后slack非负，所有此先压缩框架不能付。后者是首步解析不变量，非此code穷尽了所有路线。

程序没有计算完整多源K/D/M/P/E逐层总账，没验证任意新路由或一般half。删重复后推进actual的合法性/末两人endcap由已完整的一般kernel定理给；原列表删重循环不冒它已在native中逐项输出全账本。保BR或改合同仍不被排。

## 原生写出与当前证据时态

main先report=verify(construct())，m5将全部report含policy pretty输出为邻接merge_br_credit_certificate.json（indent2）；m8用紧凑separators(',',':')为邻接m8文件。两者末尾加换行，再pretty打印**移除policy**的summary。stdout不是完整证书，不能只比summary就称每policy字节同。

此前NI/NQ的7883实际两mode充分成功已绑定这两原输入SHA。当前7917原CLI在两个新空source-root按 `--m 5`、`--m 8` 各实际一次exit0，只有原code和内嵌模型、未预放任何frozen输出；两个生成完整证书与27685/481955B冻结文件逐字节同，stdout只是省去policy的summary且全字段等于保存JSON去policy。source前后SHA不变、断言开、0失败。故完整策略每行身份完全相同，直接复用NI原独审全部IC，不重跑7883。当前真事件/完整原源目录/原生输出和比较均保存，命令不误写成7883的--m5/--m8。

原8376B内部独审的早期BI重构/最高标签叙述只按其原稿保留，当前读完整作者程序与证书是知情比较，非新外审/新颖性。三source之外原7883/报告/一般核稿仅必要related不额外done，不恢复旧工作区私聊或Git操作。

两次原生构造的实际entry见[五人事件](../../tools/evidence/br-credit-constructor-and-policy-certificates-primary/runs/constructor-m5/event.json)和[八人事件](../../tools/evidence/br-credit-constructor-and-policy-certificates-primary/runs/constructor-m8/event.json)，完整文件比较包含所有210/11440 policy行，不以摘要相同冒完整表字节同。
