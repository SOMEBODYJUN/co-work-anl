---
id: customer-attraction/security-cce-checkpoint-entry-and-legacy-identity
kind: resource
type_tag: 资源
title: 安全聚合工作区的CCE交付登记与历史身份
status: complete-source-contract-and-current-mathematical-routing
truth_status: eight-customer-static-CCE-bridge-counterexample-reused; no-new-theorem-or-mathematical-run
review_level: 三冻结原件全文读取；与现有完整反例、原始对偶精确资源和后续不同候选逐项比较
scope: 三人八单位客户四标签；指定完整纯SPE与同实例任意静态CCE；旧工作区绑定仅为来源身份
summary: 保留历史README路由、有限命题claim全部关键字段及旧workspace绑定；W6与最低静态CCE544/87分离已有自足证明，44/23是真安全值而非CCE平均值，发现版和旧角色标签不能替当前认证。
source_ids: [5f4f91c3f5cfbbc69670, bb1e45c9e57d20597e69, 598a6c1d6f1153a259ee]
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-6cfe7c79118a41f6bd5659aa5d780852/security_aggregate/README.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-6cfe7c79118a41f6bd5659aa5d780852/security_aggregate/claim.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-6cfe7c79118a41f6bd5659aa5d780852/workspace.json
---

# 这三份来源分别承担什么

[原字节包](../../tools/evidence/security-cce-checkpoint-entry-primary/README.md)保留1225B的安全聚合README、2206B的claim和150B的上层workspace。每份在legacy-cleanup的完整提交`68fad804ec5946cb296f77dc5b336308a66abf12`与main的`aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`内容相同；[清单](../../tools/evidence/security-cce-checkpoint-entry-primary/source-manifest.json)记录全路径、指纹和源ID，不把双位置算作两次独立证明。

README是历史checkpoint的阅读顺序及交付意向；claim是有限数学结论的候选登记；workspace是旧对话身份元数据。它们均非执行程序，status或review_status字段也不会自行证明数学。当前自足论证已在[三人SPE低于全部静态CCE](../反例/三人顺序SPE低于全部静态CCE福利--反例.md)，执行范围、两客户规模和历史内部审查另见[精确核验资源](../计算/三人静态CCE福利原始对偶精确核验--计算.md)。本次是知情源比较，数学运行0次、LP0次，不增造独立审查人。

# claim的准确模型、策略与量词

采用[单位客户共同目录定义](../定义/共同目录完整历史模型--定义.md)。三个单位权提供者观察全部有序历史，各选同一非空有限目录的一个标签；终局每名客户的一单位价值在覆盖它的玩家间均分。重复、离轨和弱最优平局全部保留。该有限实例的四标签兴趣mask及单位客户重数为`{2:4,4:1,8:1,13:2}`，共8名互异客户，四主题覆盖两两不同。

完整策略为根0、次位在四种历史后都选1、末位按下表选择；表不是只列实际路径。

| 首行动 / 次行动 | 0 | 1 | 2 | 3 |
|---|---:|---:|---:|---:|
| 0 | 1 | 1 | 1 | 1 |
| 1 | 1 | 2 | 3 | 2 |
| 2 | 1 | 3 | 1 | 1 |
| 3 | 1 | 2 | 1 | 1 |

这给21个有序决策节点，当前完整证明核其84项含自身的行动比较。根偏离和次位偏离均沿同一策略的真实后继；没有把其它玩家冻结为在轨动作。实际路径`011`，各玩家收益2，福利W=6，最优三主题覆盖OPT=8。claim的count_based=true只描述这份指定策略，不把模型限制成同计数历史必须同回复。

原`proposed_claim_id=CA-WORST-CCE-WELFARE-NO`、`model=CAG-MODEL`是旧标签，正式对象稳定ID见上面反例页。其命题是**存在**一个合法实例和一份完整纯SPE，使同实例**每个**静态CCE都比这份SPE福利高。静态CCE允许任意玩家不对称和相关的有序终局分布；每位玩家只能事前改成固定标签，其它人的终局行动不变。该静态偏离与顺序真实续局不同。

# 锐值、真正安全值与发现版的分工

claim给非负对偶乘子`(0,9/29,20/87,20/87)`。记静态终局z、聚合固定偏离损失G_a(z)=Σ_i[u_i(z)−u_i(a,z_−i)]。全部64个有序终局满足

\[
W(z)-\sum_a\lambda_aG_a(z)\ge544/87.
\]

任意CCE各E G_a≥0，故E W≥544/87。达到分布在排序行动串`011,112,113,222,333`上的总概率依次为`17/87,29/87,29/87,6/87,6/87`，每串均匀展开其不同玩家排列。分布概率和1，期望聚合slack为`(220/87,0,0,0)`，所以逐玩家约束成立，福利恰544/87。对称化用于这个达到分布；下界没有限制原CCE对称。两侧合起来才认证最小值，而不是只从某个高成本可行点推最优。

因此最低CCE与指定SPE的差是22/87>0。该同人数福利替换桥被否定，不能继续仅凭“静态CCE福利有好的PoA”支付任意顺序SPE。claim的proved-finite-counterexample经现有完整反例和精确资源支持；它没有主张尺度最小、全球新颖性或外部同行审查。

真正静态安全值v₃的竞争者在查询抽样前共同选两个合法标签。该例有原始查询p=(0,15,4,4)/23及三个背景11、12、13的对偶概率(3,10,10)/23，匹配给v₃=44/23。W−3v₃=6/23>0且2W−OPT=4>0，所以本例不反真正安全聚合，也不反half；更不能由三人桥反例宣称恰六人的主问题失败。**最低CCE平均值(544/87)/3不等于真正安全值44/23。**

README要求首读eight_client_cce_bridge_failure.md，以八客户锐原始/对偶替代发现材料作为数学入口；这与当前正式路由一致。其余文件分工必须保留：

| 原文件族 | 真实身份与接续方式 |
|---|---|
| search_cce.py / cce_best*.json | 固定完整策略锥后交替优化的浮点发现器及数值候选；候选需分别认证，不能靠文件名授SPE或精确最优值。 |
| cce_integer_candidate.json / verify_cce_counterexample.py / cce_exact.json | 42客户发现链；指定SPE W32，每个CCE≥33。33由所存固定乘子的列最小值保证，README和本claim均未提供达到33的CCE，不能附上精确最小值身份。 |
| cce_small_candidate.json | 整数缩小的发现记录；浮点字段与缩小整数输入分开，完整策略的早期有序版本与最终计数版本亦须分开。 |
| eight_client_cce_exact.json / verify_eight_client_cce.py | 八客户完整有理输出及自含原审计；原始/对偶匹配才给544/87。 |
| ../independent_bottleneck/independent_cce_audit.py --small及对应JSON | claim指向的历史定义级第二实现；不是本次新外审，原审查及后续正式独审的身份以精确资源页为准。 |

此表只解释两入口实际指向和已核正式结论。其它程序/数据的逐源清洗由相应资源对象及独立receipt承担，不以这张表代它们done。README的“下一步正式入库”和“主目标/聚合桥OPEN”为当时checkpoint时态；八客户结果如今已入库，跨人数PC、较弱CCE桥、安全最优无悔SSR又是不同命题，不能从强CCE失败自动推出其失败或成立。其准确量词分别见[跨人数PC](../候选/跨人数静态粗相关均值与顺序福利比较--候选.md)、[安全最优查询面SSR](../候选/安全最优查询面的聚合静态无悔预算--候选.md)。

# 旧workspace只定位来源身份

workspace全部字段是schema=1、save=customer-attraction、actor=`R-6cfe7c79118a41f6bd5659aa5d780852`、instance=`a5bb517bacd142a78704f498800b5b9b`。它没有策略、客户数据、时间、分支、数学完成度或当前Boss7的绑定声明。关联实读旧根README（源183bd96eea2a1aaa8c39）表明原对话自称研究Boss5，同时明确程序生成actor独立；这解释历史别名，不能拿它覆盖本次Boss7身份或冒认旧instance为本次新实例。旧根README还有分数覆盖递推/全历史收益图等其它路线，未因本安全聚合入口被顺带清洗或导入。

# 处置与关系

三主源分别retained为本资源、原字节及现有正式数学去向。独有信息是交付优先级、有限claim逐字段量词和历史身份，它们已完整保留；不新建一个重复反例。数学关系为来源/路由指向既有有限反例，claim参数与完整策略给身份一致性，原始/对偶及执行资源为证据，workspace仅提供来源归属。没有从元数据到定理的推导边，本批未生成第三阶段图。

接续研究可以读对应完整资源重用合法输入和明确证据；不能从W6<544/87外推所有人数、所有SPE的最小福利，不能从该例W≥3v₃证明一般聚合桥，更不能把开放研究本身当作来源未清洗。当前六人half仍需独立全称论证或真实完整六人反例，本页均未提供。
