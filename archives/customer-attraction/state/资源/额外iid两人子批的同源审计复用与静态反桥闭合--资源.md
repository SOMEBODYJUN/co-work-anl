---
id: customer-attraction/extra-iid-two-player-child-source-closure
kind: resource
type_tag: 资源
title: 额外iid两人子批的同源审计复用与静态反桥闭合
status: seven-sources-fully-read;five-existing-assets-reconciled;one-new-original-entry-run
summary: 七源17845B全部实读；五源与既有原件、三次成功原入口逐字节对齐并复用；新增循环静态PNE稿及其一次原入口证据，另以全k解析说明该族所有完整两人SPE均修复iid差。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-75bfd8f0f91740408bf08f0c9f5e2aa1/iid_extra_slot/child/README.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-75bfd8f0f91740408bf08f0c9f5e2aa1/iid_extra_slot/child/check_family.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-75bfd8f0f91740408bf08f0c9f5e2aa1/iid_extra_slot/child/check_hub.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-75bfd8f0f91740408bf08f0c9f5e2aa1/iid_extra_slot/child/check_two_pne.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-75bfd8f0f91740408bf08f0c9f5e2aa1/iid_extra_slot/child/two_pne_extra_iid_obstruction.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-75bfd8f0f91740408bf08f0c9f5e2aa1/parent/audit_iid_support_hub.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-75bfd8f0f91740408bf08f0c9f5e2aa1/parent/iid_support_hub_independent_audit.json
---

# 额外iid两人子批的同源审计复用与静态反桥闭合

本资源处理R-75bfd8f0f91740408bf08f0c9f5e2aa1中child五源及parent两源，共17845B；七份冻结原件均已完整实读。它们讨论真实两人顺序游戏与静态三人iid值，另有任意背景下等单独收益目录的两人解析子类。所有提供者和客户均单位权，目录有限非空，终局逐客户均分，完整策略包含全部有序决策历史及平局。辅助静态人数、周边主题数、单位客户数没有混为真实玩家数。

本次检索并完整比较了既有正式正文、其原件及真实运行记录。README、check_family、check_hub、父审程序与父审JSON已经具备成熟处置；它们的当前冻结字节与既有保存逐字节相同，故不重新制造正文或重跑同SHA成功入口。真正补闭的是循环静态PNE稿与check_two_pne的原件、准确程序合同及一次执行；新增数学是该族的全部完整两人SPE解析修复。

## 七源的独有内容与落点

|源ID及原文件|本次全部读取的承重内容|实际保留的正式落点|
|---|---|---|
|969e5d50c2ced1120bdd README.md，3587B|等f两人子类、一人边界、262客户θ₂缺口、hub与循环PNE导航、当时一般EI的OPEN|[等f引理](../引理/等单独收益目录的两人首位与任意iid人数比较--引理.md)、[hub解析族](../反例/支持外枢轴修复与静态查询平均的两人分离族--反例.md)、本资源的时态与导航闭合|
|4484bb26c27533158077 check_family.py，1606B|组合计数的八次固定输入、真实两人回复类别、Nash/根/平均缺口不等式、一般族公式回归|既有[child程序对象](../程序/子集枢轴两人族的组合计数与逐客户有理审计--程序.md)，八行stdout及已有成功事件|
|18c7d0a4af3b0e510705 check_hub.py，1933B|262不同单位客户、9题、9²双竞争者×9查询、单背景θ₂、H后八个最佳回应|同一child程序对象中逐客户有限核验，独立stdout及已有成功事件|
|adccbedba7976fe24e3d check_two_pne.py，1792B|1222客户的静态PNE与三人iid KKT、两列全行动比较、75参数公式；顶层输出无文件|[循环静态分离对象](../反例/两人静态纯均衡与三人iid值的循环分离--反例.md)中的精确程序合同及本批原入口证据|
|3d55722d798eb4bff9df two_pne_extra_iid_obstruction.md，3120B|全部k≥26的单位循环构造、两个静态辅助桥反例、最大f和完整SPE边界|同一循环静态分离对象的全族证明，保留原稿谨慎时态并追加明确分开的本次动态证明|
|df0fbb107d5a74f9aca0 audit_iid_support_hub.py，3577B|四例逐单位展开、显式全历史给定策略、全有序对OPT₂、两个多项式平移身份、报告写出|既有[父审程序对象](../程序/两人支持外枢轴的单位展开与静态三人核验--程序.md)，完整四例与494项比较合同|
|a3e9ee1b5f4eab01c439 iid_support_hub_independent_audit.json，2230B|四行客户数、静态α/λ、真实q平均、根收益、W/OPT₂、gap及平移系数|同一父审程序对象的全部四行数据，与既有逐字节重放报告绑定|

双冻结完整commit、原路径、ID、字节数、SHA256、Git blob及真正保留路径逐项保存在[source-manifest.json](../../tools/evidence/iid-extra-slot-child-source-closure/source-manifest.json)。每源都同时定位legacy-cleanup的68fad804ec5946cb296f77dc5b336308a66abf12与main的aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c。五份成熟原件直接引用现有证据位置，仅两份此前未闭合原件在本证据目录新增副本；没有整树复制或覆盖旧正文。

## 成熟资产的同字节及成功事件复用

本次逐项核对当前导出原件与既有原件的大小、SHA256及Git blob，并完整读取相应stdout、父审全部JSON与事件字段。[复用核对记录](../../tools/evidence/iid-extra-slot-child-source-closure/reused-execution-comparison.json)只记录这项同源及事件对齐，不把它写成一次新实验。

|既有原入口|已经保存的实际运行|本次执行次数|不能扩张的范围|
|---|---|---:|---|
|check_family.py|exit0，assert开启，1195B stdout；源SHA e5846d92551e49e2f966686035e8836ee96f6efbe4a7fe53a59cd552a1638f9b|0|八个固定参数的组合计数；大客户行没有逐单位展开，普遍结论靠解析|
|check_hub.py|exit0，assert开启，108B stdout；源SHA b56b5ef32947e8947d675ebd64dff825c7bd3cf2ee8fe2ad2bc0e580970baa18|0|一例262客户的静态iid、θ₂和H后回复；不是全部完整SPE枚举|
|audit_iid_support_hub.py|exit0，输出2230B报告与冻结JSON逐字节相同；报告SHA 7d33ed807a0d5f2486f08b060514003770ca3620fa7b3c1b6ee6ef3a8cfca39b|0|四例给定完整两人策略46个决策历史、494项含self比较；不是全部SPE或一般人数证明|

child两次原入口的[既有事件](../../tools/evidence/extra-iid-two-player-child-primary/replay/execution.json)与父审一次原入口的[既有核对](../../tools/evidence/iid-support-hub-parent-audit-primary/verification.json)分开保存。当前五源一致，不代表以前未执行的check_two_pne也已运行。相反，查得的成熟证据没有它的同SHA成功事件，所以本次只补这一个原入口。

父审四行对应(k,a,P)=(8,1,24)、(8,3,70)、(10,3,252)、(12,3,924)，各例真实根均高于辅助静态λ；第一行 $D=83/2<997/24=\lambda_3<105/2=u_H$。后三行使用P=M/3，第一行P=24不等于70/3，不能把 $D=\alpha_H$ 特例推广到第一行。父审的所有行、福利和多项式身份已经在成熟对象完整保存，本资源只指明其与新循环PNE的区别。

## 新增原入口的实际输入、输出及依赖闭包

本批[原check_two_pne.py](../../tools/evidence/iid-extra-slot-child-source-closure/original/check_two_pne.py)与[原循环稿](../../tools/evidence/iid-extra-slot-child-source-closure/original/two_pne_extra_iid_obstruction.md)保持冻结字节。脚本仅用Python标准库Fraction，全部客户和q在顶层固定构造，无外部文件、求解器、随机种子、CLI参数或本地模块依赖。无main保护，导入即执行；它只打印Python字典，不产生JSON文件。

本次将未修改脚本放在clone外目录执行一次，保持assert开启，exit0、stderr空。固定输入k26，共1222不同单位客户、28题，得到静态PNE双方52、三人静态iid值105529/2028、严格差73/2028、支持外查询601/13、最大裸大小55。它只检查固定竞争者A与B两列的所有行动，没有全28²矩阵或完整回复表；k26到100的75点只是公式断言。全部k的静态反例由解析推导承担。

保存的[147B原stdout](../../tools/evidence/iid-extra-slot-child-source-closure/check-two-pne-stdout.txt)、[空stderr](../../tools/evidence/iid-extra-slot-child-source-closure/check-two-pne-stderr.txt)、[运行记录](../../tools/evidence/iid-extra-slot-child-source-closure/check-two-pne-execution.json)和[stdout解析数据](../../tools/evidence/iid-extra-slot-child-source-closure/check-two-pne-derived-output.json)没有冒充原脚本生成的历史报告。stdout SHA为61edcc792cb45497c69e986e5164958475c5d4f87916b0cf590abb0001a540d9。未重跑另三个成熟入口，也未追加LP、随机发现、全SPE枚举或第二个28²检查。

同一目录程序均无main保护；尤其既有父审在顶层无条件写同目录的iid_support_hub_independent_audit.json。需要复跑时应复制冻结脚本到独立工作目录，保持assert开启；不能通过在原件目录导入它来“只读取函数”。这个说明来自完整源码的实际副作用，不增加模型限制。

## 数学关系、时态和新增范围

README的等f子类在任意合法背景、恰两名真实剩余玩家时，对**任意**静态人数n≥2及任意iid分布q有真实首位支配其单人期望；无需q先为Nash。其公式和完整证明已在等f引理保存。一般不等f目录的末位不能简化为最小交叠；本批hub和循环例都不满足等f，不构成该引理反例。

hub成熟对象与本批循环对象分别反驳不同静态辅助桥。hub用支持外H修复q平均真实偏离和θ₂的不足；循环对象给一个双方都低于λ₃的真正两人静态PNE，但本次从循环窗口不交直接证明：每个首位周边P_i都有与之不交的P_(i+3)，每个末位最佳回应都必须是不交周边，因而每份完整两人SPE均得 $u_1=u_2=2k+3>\lambda_3$、$W=\mathrm{OPT}_2$。这项**本次解析补充**比原稿“可能修复”更强，未声称出自原程序，亦不推出任意不等f两人目录的EI。

README“2026-10-23一般extra-slot仍OPEN”及循环稿“未否定extra-slot本身”保其历史含义：这些源自身没有反驳一般EI。当前一般全背景/全剩余人数的EI已由[七客户三人银行根反例](../反例/额外一人iid收益桥的七客户银行根反例--反例.md)等后续对象否定，不能把旧OPEN延续为当前状态；也不能把那个后续反驳倒归此七源。既有[一般半覆盖根账本](一般半覆盖工作区的直方图与支持外障碍时态--资源.md)记录的是原工作区的入口和时点，补闭本批缺源不抹掉旧时点缺件记录。

本批源数或数据字段通过不是数学全称判断。已完成的是七源语义归属、五源成熟处置复用、循环静态反桥的完整保存和该特殊族的动态修复。一般不等f两人EI是否可证未由这些材料解决；恰六人、任意完整纯SPE的half也未由本批证明或反驳。

供第三阶段使用的[关系证据](../../tools/evidence/iid-extra-slot-child-source-closure/relation-evidence.json)逐边写明支持、区别、假设排除与历史纠错，不把同一工作区导航强造为逻辑蕴含。
