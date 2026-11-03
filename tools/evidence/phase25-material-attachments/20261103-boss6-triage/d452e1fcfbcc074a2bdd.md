---
id: "customer-attraction/fifty-two-client-frozen-matching-recovery-chain-and-six-native-records"
kind: "resource"
type_tag: "资源"
title: "五十二客户冻结匹配恢复链与六份原记录"
status: "integer-candidate-identified-with-existing-complete-counterexample; old-success-reused; no-new-run"
summary: "核63维浮点候选、22类52客户整数候选与既有259历史完整证书的身份；保recover_integer重新求LP/受限支撑MILP而非舍入保存权重、14fixture全字段、缺参数键的历史schema和原候选/精确已证反例的不同状态。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/static_matching/recover_integer.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/static_matching/recover_integer.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/static_matching/static_matching_integer_candidate.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/static_matching/static_matching_integer_candidate.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/static_matching/cone_m4p6_seed1022.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/static_matching/existing_examples.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/static_matching/existing_examples.json"
---

# 五十二客户冻结匹配恢复链与六份原记录

## 从哪个候选恢复，哪些对象实际相同

本组只研究单位客户共同标签目录下的**冻结最优匹配桥**，定义和完整程序量词见[精确DP与唯一支持策略锥](<../../../../archives/customer-attraction/state/程序/最优冻结匹配的精确动态规划与唯一支持策略锥--程序.md>)。SPE仍量化全部有序历史、任意平局；冻结匹配成本不是改变后按原策略回复的真实偏离。

34345B正浮点cone报告保存三种不同数据：一个10类、88单位客户的整数种子输入；由该种子取得的完整259历史动作certificate；以及probe返回的63维新浮点客户向量。向量有26个正坐标，其余零，没有负坐标，actual福利被LP归一为一而非总客户质量归一。目标0145、actual3322、gap约0.03434647262788905。这个报告没有给精确有理新输入或独立定义级验证，不把其浮点weights当整数证书。

27757B整数候选保存同一个target、actual、完整certificate及以下22个非零兴趣mask重数：

|mask|人数|mask|人数|
|---|---|---|---|
|2|1|5|4|
|6|2|9|4|
|10|2|16|1|
|20|5|21|1|
|23|1|25|3|
|27|3|29|1|
|32|1|35|1|
|36|3|38|2|
|39|3|40|2|
|51|1|52|2|
|58|4|59|5|

重数总和52，每个复制是不同单位客户。mask第a位表示喜欢标签a。两原件certificate的 `terminal_counts=[0,0,2,2,0,0]`、259个完整动作及原BFS行序逐字段相同；共有certificate的规范JSON SHA为

`1dd1d0da95734ca94d012ce2c40a20e4bc2d9d77f41839a6445092bf4c4bb69a`。

这里没有用计数替代历史：全部根/6个一历史/36个二历史/216个三历史动作在[完整阅读视图](<../../../../archives/customer-attraction/tools/evidence/ra0-static-matching-discovery/full-reading.md>)逐行保留，原两份JSON也均原样保存。

进一步与已正式保存的32574B最终输入逐项比较：22个整数兴趣重数、四人/六标签参数、完整certificate和actual完全相同。该旧最终输入SHA为

`9e7cf1437a7b03fe89d843d4ae20efa3c6a4137373098ed1220d4370656a5245`。

所以本整数候选在当前不是一个未核的新游戏；它对应已完成的[52客户完整反例](<../../../../archives/customer-attraction/state/反例/最优组合冻结匹配的一单位缺口--反例.md>)。原状态字符串 `integer_candidate_requires_definition_audit` 仍保原字节，不把发现时状态倒写成作者当时已有全部审计，也不再造一份相同反例正文。

## 恢复脚本实际重新求什么

2358B `recover_integer.py` 的输入必须含非空candidate、原种子instance、certificate与target；负cone报告的candidate null不属于其正常输入合同。它导入本目录 `cone_attack` 和规范 `Instance/StrategyCertificate`，CLI要求input、`--output`，`--seconds`默认45。两源码有main guard；本次未执行或导入它们。

关键是：恢复器**不消费保存的63个weights，也不把这些坐标直接舍入成整数**。它临时包住 `cone.linprog` 捕获矩阵，再以原种子instance和certificate重新调用 `cone.probe`。这次probe没有传旧报告的query_factor，始终用默认1。它从这次新LP的返回坐标中取大于 \(10^{-9}\) 的支撑，之后只允许这些类型参与整数恢复。故不同求解器版本或退化最优解可能给不同支撑；不能声称历史52结果必由任何当前复跑唯一重现。

令 \(D=\operatorname{lcm}(1,\ldots,m)\)，把captured矩阵A整体乘D，并断言每格距最近整数小于 \(10^{-7}\)。真实单位份额分母均在1..m，因此这个缩放有数学依据；浮点实现仍使用 `np.rint`，不是重新从Fraction系数独立构造原行。把公共gap固定为一，得到

\[
\operatorname{round}(D A_{\rm weights})w
\le-\operatorname{round}(D A_{\rm gap}). \tag{INT}
\]

IC行gap系数为零，OPT/MATCH行为一，所以(INT)要求真实IC非负、指定target对其它支持有至少一单位的严格覆盖差、所有目标排列冻结费超过W至少一单位。整数w非负，目标最小化 \(\sum w\)，仅在新LP选择的固定支撑内搜索；`milp`有给定time_limit。

若返回向量不存在就报错；否则 `np.rint(...).astype(int)` 后回代缩放行，检查最大违反量小于 \(10^{-8}\)。没有独立核回所有真实历史、全部最优元组、完整动作域或唯一最优支持；没有先检查重新求LP的success再读x。这些边界正是输出保留candidate状态、要求定义级审计的原因。

这不是把一个有理向量清公分母的恢复：它新解一个受限支撑整数优化，不能把MILP status0解读为52在所有客户类型、所有策略或所有反例中全局最小。程序也不作公因子缩放；gap一的单位绝对约束已经固定了尺度。输出独占创建、不建父目录，包含status、target、actual、整数weights、完整certificate、unit_customers、milp_status/message；stdout删去weights/certificate大字段。冻结报告这八个顶级字段已全部实读，status0的HiGHS信息仍是历史记录，不是本次新运行。

## 精确52结论实际由什么承担

本页没有再执行52实例。已有origin原程序同输入成功事件的代码SHA为
`23fa930019f22e9e12fd99859e37a250485d7ae740e9946b409527c80ccf2c79`，记录exit0，stdout/生成文件/冻结9173B报告均为
`6488b65a790c2af4bab4f0019a10f6cd4f784d6318fd12517232ba6cfd077cd9`。
旧命令、输入manifest、完整报告及源实现路径逐件绑定在[成功复用清单](<../../../../archives/customer-attraction/tools/evidence/ra0-static-matching-discovery/prior-success-reuse-manifest.json>)。0.368130922秒是旧事件耗时，绝不是本批新计时。

该旧事件覆盖本52输入全部259历史、1554项含自身真实IC比较，即1295项proper比较，及W47、OPT52、target最优。它不读取最终JSON的all_assignments和unique_optimal_supports，因此不能把旧run范围扩大。唯一最优0145与全部24个冻结匹配的结论，由已有自足反例的两项解析穷尽承担：只喜欢1、4、5的三个客户迫使这三标签，再覆盖{0,2}与{0,3}两块迫使0；四个目标各一次，故所有最优元组只有24排列。冻结成本12个48、12个293/6，所以minQ48>W47，严格缺口一。

同时 \(2W-\operatorname{OPT}_4=42>0\)，且 \(48<(5/4)47\)。不能把强冻结桥的失败借给half或5/4弱预算。这个旧origin实现的成功也不能移接给另一个4852B独立审查实现；旧审查页“当时缺blob”只保历史证据范围，root正另行处理其实际来源，本组不预称那些新来源已读或已运行。

## 14个旧fixture报告的全部行

4454B `existing_examples.json` 是14行报告，原文件名均以 `examples/customer_attraction/` 为前缀。每行所有字段如下；counts为标签计数，target保完整索引序列与重复。

|文件末名|m/p|checked|counts|target|value|W|OPT|maximum_gap|
|---|---|---|---|---|---|---|---|---|
|aggregate_theta_failure|3/6|20|110100|102|86/3|34|36|−16/3|
|coverage_opportunity_failure|3/5|8|10011|201|13/2|8|11|−3/2|
|empirical_iid_kernel|3/4|6|1200|100|11/3|7|7|−10/3|
|global_decorrelation_failure|4/6|2|201001|4430|129/2|85|89|−41/2|
|individual_security_failure|3/6|20|110100|205|59/2|32|34|−5/2|
|local_security_increment|3/6|14|110100|205|191/2|105|113|−19/2|
|portfolio_matching_failure|2/5|5|10001|13|44|44|45|0|
|prefix_balance_failure|4/6|2|013000|5034|51/4|14|22|−5/4|
|residual_counterexample|2/5|8|00011|12|8|8|10|0|
|root_stationary_kernel|3/6|28|101100|104|29/2|15|19|−1/2|
|root_tax_failure|4/6|12|300010|1230|69/2|38|61|−7/2|
|tax_bridge_failure|3/4|4|0300|023|9|9|15|0|
|worst_cce_welfare_failure|3/5|7|10002|412|25/3|9|12|−2/3|
|worst_pne_welfare_failure|3/4|2|1002|301|71/6|15|16|−19/6|

每个value−W等于该行maximum_gap。`checked`合计138，3行零gap、11行负gap；不能因为文件名含“failure”就将本诊断当正冻结匹配失败。报告未保存这些输入的完整certificate、生产命令、参数、实现SHA或逐计数结果；现存search CLI也没有一个直接输出这14行schema的模式。本组只保原有限记录，不把未提供的生成事件补成search.py某次成功调用，也不重读/重跑14个既有完整案例来扩充样本。

另外两份400游戏阴性、150游戏5/4阴性与50游戏正浮点记录的完整参数/缺键/状态已在程序对象和[六报告全字段阅读](<../../../../archives/customer-attraction/tools/evidence/ra0-static-matching-discovery/full-reading.md>)保留。六份JSON共2399个原始叶值，数字与字符串原型未丢；两完整certificate共有259个动作按原行序展示，不用摘要替代大JSON尾部。

## 复用、依赖与本次执行边界

`search`/`cone`依赖四个规范模块 `__init__.py`、`model.py`、`exact.py`、`certificate.py`。它们是此前本会话完整实读的同SHA版本，本次核字节/路径复用，不额外导入。`recover_integer`还依赖本批原 `cone_attack`，数值生成依赖numpy/scipy；原报告没有冻结其版本，本次不伪造环境。

全仓比较已读完整52反例、原审查范围、R51另一随机策略锥驱动、52历史重放/后缀合同与origin正式计算。R51 driver有不同随机种子、非PNE筛选和另一个try_cone实现，不能用其已执行420种子/两个锥事件来证明本批150/50游戏输出或复原本批LP。

本次原CLI、import、随机发现、优化器、SPE/匹配重演均为零。只做完整原文/原字段阅读、语义身份比对、代码AST/依赖与旧成功绑定、报告算术和交付结构检查。独有内容、关系与精确逐源回执见[证据入口](<../../../../archives/customer-attraction/tools/evidence/ra0-static-matching-discovery/README.md>)。本组没有新增反例、独立审稿人、外部认证或六人half结论；可复用的是明确的发现链、精确数学/实现边界及已成熟52对象的身份链接。
