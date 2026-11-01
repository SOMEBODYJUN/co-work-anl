---
id: "unrelated-machines/historical-real-source-NO-all-schedule-decoder-route-contract"
kind: "resource"
type_tag: "资源"
title: "真实源NO全调度解码路线卡的历史合同"
status: "historical-route-resource-integrated; no-current-progress-or-hypothesis-upgrade"
summary: "保Boss11反向路线的真实承重量词、审查先验、salvage范围和失败/成功标准，解释两个实际入口及未交decoder；历史授权语句不作当前指令。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/unrelated-machines/R-ca2c8c2f564d4e2fa4b3b0949bb0b66a/ROUTE_CARD.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/unrelated-machines/R-ca2c8c2f564d4e2fa4b3b0949bb0b66a/ROUTE_CARD.md"]
---

# 这份资源是什么

原16行 `BOSS11-R0-R-ACTUAL-NO-DECODER-v1` 为当时Boss11/R-ca2c8c2f564d4e2fa4b3b0949bb0b66a的反向研究路线卡，route R0-R。保其来源身份、研究计划与当时OPEN状态；不是当前Boss4认领指令、人数/审批政策或最新全仓进度。卡中“本会话授权”“没有排他席位”等是历史载体语境，当前执行服从本仓AGENTS和实际owner，不把它当跨会话授权。

核心数学目标O是：从真实源NO出发，排除**完整原矩阵任意低负载实际调度**，需要一个可靠源解码器；局部CONFIG、单端边际、未物理执行的一致性或只测一类规范调度都不够。主目标与CAG六人SPE、纯数值间隙不是同一问题。

# 对近二反面的准确量词

若一般UM目标是存在某固定ε>0、确定性总位多项式(2−ε)实际全任务近似，为在明确复杂度假设下否定这种存在性，需要对**每个固定**足够小δ>0给相应位多项式源归约：已知可计算的正有理标尺T>0，YES有完整OPT≤T，NO有OPT≥(2−δ)T。一个固定较弱比值只排除比它更强的算法，不否定全部统一改善。

例如若假设存在改善ε，选择0<δ<ε，则YES算法输出≤(2−ε)T<(2−δ)T，NO任何合法完整输出≥OPT≥(2−δ)T，可按已知阈值区分。若YES只是≤(1+η)T、NO≥βT，则须明确验证(2−ε)(1+η)<β。不能将未知OPT当decoder输入；随机源归约还须陈述概率/复杂度假设，不能把NP不含BPP与P≠NP混为同一无条件结论。

典型soundness合同是：给任何原矩阵完整调度σ，只要Cmax(σ)<βT，就按总位长多项式输出与源NO相矛盾的见证。此时NO确得OPT≥βT。只对指定selector模式、抽象token、匿名资源或局部延伸证明的命题，若没有映射到任意原σ，尚未履行O。

# 卡所指的两个实际入口

| 入口 | 精确可用合同 | 为什么没有完成O |
|---|---|---|
| bulk OR双实际模式插值 | r≥2、偶k≥2、1/2<ρ<1的固定环/两pool backbone；selector f在正pool代表False、负pool代表True。v3辅助J仅内部I或正C，正C端时间∈(1/2,1]，允许任意异权内部/跨branch。给两份完整实际≤1见证，分别仅u、仅v为True，可构造同一全部原任务的allFalse实际≤3/2。 | 两份完整全局strict见证是输入前提，不能由每子句各自可行免费拼成它们；原不固定selector的OPT本来1。排独立committer抗split只关这个机制，不是源NO矩阵。 |
| weighted parallel relation重赋权障碍 | 素数R≥2、k≥2，R组共用k变量，**完整**关系Aⱼ={a:Σaᵢ=j}；state支持是带变量tag的线(xᵢ,z,aᵢz+j)。每state任意非负有理incidence权总和1。对每份显式完整权表，可选states并领全局不交子集，每组保质量≥1/2，并输出全部原UM任务实际≤3/2。 | CSP value恰1/R只是易判族低值；仅排“保关系/资源/资格只改权”对**包含该族的整个NO域**强制质量<1/2。未知hard image可能避开该族，没有被排除。 |

第一入口的具体backbone：每变量有i∈[2k]循环，正block为1…k、负block为k+1…2k；机器和q/b/f按变量分隔，仅J可跨branches。qᵢ在本Mᵢ耗ρ、后继M耗1、所属block pool耗1/k；正bᵢ在本M耗ρ或C耗1，负bᵢ在后继M耗ρ或自身C耗1；f在两pool各1。所有q/b/f/J必须执行。v3以两见证正C计数的平均gate和内部排序对整数流一起分配J，再完整回填q/b/f；不是只排某branch或忽略未选aux。原卡对应的“salvage”正是这种指定allFalse输出，而非一般OPT下界。

现在实际读到的同SHA current还含独立v4后缀：J可到任意**非pool**机器时直接将所有非f任务共同插值，M/C只保≤3/2，不再继承v3的≤1/一job加强；J可到pool则界为3/2+d/2，d只统计两份见证在两个特殊正pool的实际已用端。它要求的nearunit实际J身份移位是必要条件，非充分decoder。不能把后缀的较大域倒填原路线卡或把一次读whole SHA称旧v3全部又独立复审。

第二入口的实际UM有每state一private机、每tagged资源一resource机，每组selector只能在本组private耗时1，每incidence任务只能在本private耗时w或对应resource耗时1；全部未选states任务保留。用affine候选a(j)=cj+d、Σc=1、Σd=0；条件于完整state后c仍均匀，全部共点损失总平均≤1，至多一组损失>1/2，所有共点交给这个唯一例外，其余删共点即可全组半保留。再让每组selector在所选private、只导出领取incidences，完整原任务峰≤3/2。完整关系及k≥2承重；singleton关系或k=1可权全压同一共点，真实OPT2，故任意关系不在其域。

两入口完整数学与实际审查分别见[一般插值范围链](../审查/一般插值的Exact先验与后缀范围及草稿边界--审查.md)、[任意状态权证明链](../审查/任意状态权仿射并行线的证明与审查链--审查.md)。本批对两个current实际全文比较，既有证明只作相关源，不额外done；无新增外部论文事实认证。

# 原卡诊断族、成功线与kill line

卡列的两树/selector-parking gap测试实际整数选择；全部中间partial quota防止只查完整匹配层；query/return identity要求原任务真实执行；重C与tiny共居检查同机总容量；tagged line/cube严格分域防止资源假同一；给定actual与寻找未知actual区分算法输入义务。本批[奇偶配额稿](../审查/KDM奇偶块的近满配额逃逸与压缩任务身份--审查.md)具体展示近满层可以绕过完整层，而不是验证某hard source包含该族。

成功线要求真实整数YES、任意低全调度NO解码、对每固定改善量的阈值和总位复杂度同时闭合。失败线是出现保全部原任务的低载NO escape或decoder缺口时停止**该具体机制**，保准确salvage，不以堆参数/更多文件代替soundness；它并非停止一般目标或用户授权工作的指令。

oracle/编码检查包括：资格与时间全binary、零/∞、空任务/零OPT、单可用端、同一输出全部机器负载；两已给actual合同不能暗中求未知strict witness，也不能免费枚举指数CONFIG。卡最后提出跨clause/mixed readout、真实共同资格和Chan类额外pairwise-independent关系的partial soundness作为未来方向；它没有提供这些对象的构造、外部文献定理或完成性保证。

# 历史独立性和处置

原计划的builder先冻Exact，未读新Proof的general/rank独立重构并冻结，root实读后才解封作者Proof，最后只对实际canonical指定scope审。root共同推导或先听口头策略时明确不记盲审。卡只是规定这套历史路线，不能证明所有未来稿都实际按它发生；实际读序须各原件/SHA另证。本轮已读所有这里比较材料，不冒称新blind attack。

本源按资源完整整合：保route/actor/ID、唯一O、两salvage入口、首批诊断族、成功/失败标准、oracle位复杂度、当时OPEN及未来动作，而非仅做一个链接索引。卡没有数学程序，本批不为它新增run；相关parity复跑与常数自查不计为路线卡实现。原[16行资源](../../../../tools/evidence/um-weighted-partial-parity-and-route-primary/original/ad465f429de1d94fc30a.md)保持冻结字节，主目标正反面、外审及新颖性不由此升级。
