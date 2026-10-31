# 直接静态吸收与十客户相邻钱包反例的证据

本目录支撑[直接缺额引理](../../../state/引理/静态覆盖松弛吸收末对钱包的直接缺额式--引理.md)、[十客户反例](../../../state/反例/十客户重复实际行的相邻钱包失败--反例.md)和[原审计资源](../../../state/计算/十客户相邻钱包的原审计与失败层级--计算.md)。

## 五个正式来源

Boss4已确认claim pushed `776eb54ad832ed0a91f8b12fd1bfe1b09680ea38`、synced。开工时确认本stage不存在，未覆盖既有交付。正式五源24960B均全文读取并核inventory SHA，两个冻结来源逐字节一致，原件保完整仓库相对路径。

|源ID|文件|字节|
|---|---|---:|
|23058322be690f0f6cc0|direct_terminal_surplus_and_early_gap.md|3694|
|5aa36b9a875a25bc107b|compact_adjacent_wallet_counterexample.md|7258|
|4f9bddd16812ef8b7605|audit_compact_adjacent_counterexample.py|4722|
|c056b152c687bc4468ec|compact_adjacent_counterexample_exact.json|5868|
|8ed477b1d30e8bca1bb1|tree/exchange_terminal_refinement_review.md|3418|

共同前缀 `research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round10/`；前四份在exchange，最后一份在tree。完整定位、blob、SHA、双commit和角色见[source-manifest.json](source-manifest.json)。比较源不额外done。

## 一次无外部输入的原main

原4722B程序只用标准库；十个单位客户、三名玩家、四标签、根/SECOND/LAST完整21节点策略均内置。没有外部运行输入或库/模型依赖，不能凭原报告列表虚构JSON输入。运行器把原码置于新 `replay-tree/` 原路径，代码未改。

唯一一次原main：Python3.12.14、exit0、0.047476768493652344秒、stderr空，源码前后SHA不变。新5868B JSON逐字节等冻结报告，SHA `4249c114f4ae5abb8994bc604a5834610e70829100a5dd139d7a0b778e51afe3`。原码/旧报告、新JSON、stdout、stderr与执行记录分开保留：[execution](replay/execution.json)、[新输出](replay/compact_adjacent_counterexample_exact.json)、[stdout](replay/stdout.txt)、[stderr](replay/stderr.txt)、[内置输入清单](runtime-input-manifest.json)。

真实执行穷尽21有序决策历史/84含自身IC，重算3×4冻结矩阵、C_adj、全部64比较元组、四种最优多重集的18个不同指派。反例正文保原报告全部21行强制动作真实收益。没有运行tree/root独立审计、后续一般族程序或任何旧13人程序，没有新实例/策略搜索。

## 完整数学边界与后修正

直接引理保S的所有客户格、c=m时t=k、X内两格ABSORB及QTAIL两个DIRECT等式。静态部分无需SPE/最优性；真实末对部分独立使用原IC。尾钱包与静态松弛相消，无需额外HW，但EARLY仍未付；没有新增可叠加actual收入。

十客户W9/OPT10、冻结regret2/C_adj1反驳ROWMAX、OPT-ALL、COMMON-ALL；其最有利最优指派minQ6，故本例不反驳存在性。原JSON的not_refuted保持局部/历史含义。后续root全m族的完整正文已读，C_adj1、minQ−W=(m−4)/2，从m≥7否定全人数存在性和任意固定倍数桥；本族仍满足half，m5/m6单族不严格违例。没有把旧OPEN、后修正或机制反例混成half结论。

## 十二份全文比较与审查先验

12份comparison-only原件45812B：后续root一般族；tree compact审查/独立源码/JSON；root字面源码/JSON；旧两query删除势边界；自洽查询候选；旧13人基本税算术；exchange10 README；前轮点态钱包与调和钱包。均保存原字节并核两定位，不额外done。

tree的direct审查是已知精确公式、未先读证明的内部重构；tree compact是作者明确构造陈述后的独立手算/实现，无作者导入，历史63非自身IC但未做弱式完整优化；root字面实现历史84含自身IC并枚举minQ6。它们与本次作者代码复现分别记录，本批不冒称新盲审、外审、最小性或全球新颖性。

全仓冻结Markdown按direct/compact/相邻存在性源名检索后追到后修正原族；当前末对/HW/强冻结指派/fresh候选全文比较，五人定理与六人问题只核模型状态。旧suffix两稿的未付删除势/联合势遗憾不能由固定点或child IC消去，不据旧历史OPEN恢复新结论。旧13人37/66只反驳全部query/base加强，不当minfresh-OPT或half反例。

全部必要本地blob读取成功，设置GIT_NO_LAZY_FETCH=1；未重试任何先前非必要远端/认证操作。三正式对象/5receipt/自查关系/下一候选齐；[verification](verification.json)只验证字节、链接、报告行和已有执行，不再次运行数学程序。
