# 候选题源与价值审计：作者原题、母工具与团队子题分别评价

审计日期：2026-10-20。基线为本分支 `90b9991a1f985fe1b4d07b498c8658274ad032c1`，并只读比较 `research/topic-selection` 的 `1b8928d53a6db0b6112a8b8e75360c9053cbd7cc`。不合并两分支的候选数，不覆盖同行排序。本轮用户要求评价现有候选是否来自领域重要学者及其潜在价值；这是题源与选题判断，不是新数学定理或新颖性认证。

## 总判断与审计范围

当前候选池不是全部“大佬明确提出的问题”。Python逐项读取 `candidate_pool.json` 后，59条记录的来源为A=12、B=2、C=45；其中7条exclude。非exclude的52条为A=10、B=2、C=40。ID唯一、来源小计与状态小计已双向相加核对。这里沿用仓库标签，**没有把12条A全部重新认证为当前仍开放**，也没有把exclude全解释为数学错误：其中包含合并及已闭合子题。

A/B/C的意义保持不变：A是作者明确原题，B是作者建议方向，C是团队派生精确问题。对同一卡，母问题为A不使后加的限制题自动变成A。作者地位、母文质量、子题的独立贡献、当前正确性与可完成性是不同判断。

本轮六路只读核验分别覆盖公平参数、公平核心、原子势/交换、Nash精炼/预算、GAP工具、BMKP。深核的是前排来源家族，不声称逐篇完成全部候选的全球查新或证明审查。

## 更符合用户来源要求的前排

| 候选及所在分支 | 可核的来源身份 | 作者/论文分量 | 值得保留的数学差额与当前判断 |
| --- | --- | --- | --- |
| AP-02 非对称拟阵拥塞的纯perfect equilibrium，`research/topic-selection` | Anagnostides–Balcan–Fragkia–Sandholm–Tewolde–Zhang，*The Complexity of Equilibrium Refinements in Potential Games*，v2 §6明确建议去掉对称假设；非对称且affine延迟是团队C | EC2026官网接收名单列文；Sandholm、Balcan的领域资历有官方奖项/主页支持 | 由Nash提升到对扰动稳健的均衡选择，且保留任意非对称拟阵，机制差额自然。已有候选草稿，尚须核最近邻、扰动模型、真实输出与位复杂度。**来源最强的一组，优先查重和承重证明；不能说作者点名了affine子题。** |
| FG01 四人laminar EF1及两个key，`research/topic-selection`；本分支亦存探针 | Cookson–Shah，*Constrained Fair Allocations via Partition Matroid Reductions*，v1 §5及Appendix B；四人、K8/K12、EF1+ordered no-envy均是作者明确缺口A | Nisarg Shah是公平分配核心研究者；此文当前核到2026预印本，未冒称正式会议出版 | 两个key的全估值定理可接到四人laminar全类，成果传承最直接。作者已尝试计算辅助而未完成；固定物品数不使连续估值量词消失。**原题链很强，优先判别，但难度风险高。** |
| FG02 copies SD-EF1，`research/topic-selection` | Cookson–Ebadian–Shah，*Constrained Fair and Efficient Allocations*，AAAI2025，§3.3.2末Open Question。任意人数为A，先三人为C | 正式AAAI论文；与FG01共享Shah的来源实力 | 一般partition已存在反例，copies保留自然结构；完整三人任意类型定理或机制性反例才有独立价值。前缀逐人误差不能偷换成成对误差。**适合作为可证伪的前排对照，有限穷举不够。** |
| GA-03 两容量BMKP，`research/topic-selection` | Chen–Hu–Mao–Chen–Mei–Zhang–Chen–Zhang，*Near-Tight Approximation Algorithms for Bottleneck Multiple Knapsack Problems*，ICALP2026 §7最后一段明确问常数种容量；两容量为C | 张国川为资深运筹/离散算法学者，有中国运筹学会官方会士/奖项记录；不是仅凭ICALP标签 | 从同容量向常数容量种类扩张并保留近紧近似界，直接匹配运筹算法。已有联合类型算法草稿；全局供给、母引理前提、总损失和多项式枚举还须同一证明闭合。**来源、方向和自然差额均强，保留前排。** |

以上是按本轮“具体题源+可形成成果”要求给出的研究判断，不是成功概率排名，也不追溯升级另一分支候选。前排的共同缺口仍是新颖性与完整证明，不因名作者署名而免检。

## 当前主分支前排需要怎样调整评价

| 候选 | 本轮来源核查 | 数学价值与处置 |
| --- | --- | --- |
| FA01/FA02 重边参数与去除shared weight | 直接母文为Kanellopoulos–Nemery–Pergaminelis–Sotiriou–Vasilakis，v5 §5；两题确为A。作者团队以博士生/博士后等职业早期研究者为主，**不能称资深大佬亲提** | FA01一般multigraph FPT若完成仍解决自然公开题，FA02也有真实参数差额。应保留实质价值，**不再以“大佬来源”维持第一名理由**。在用户强调题源后，须与上表重新比较 |
| FA17/FA18 min-charity与cactus残差 | C。母文没有逐字提出删除cost、binary multiplicity或fixed-heavy unit-cactus合同 | FA17已有短算法证明包但有直接组合推论风险；FA18仍缺承重接口。作为FA01配套资产/路线保留，不以子引理已完成代替论文主线 |
| GA01 资源轮廓LP子模分类 | C。Kulik–Sarpatwar–Schieber–Shachnai ESA2019的Theorem1是scalar GAP LP子模工具；作者并未提出此矩阵分类 | Schieber、Shachnai等为成熟近似/资源分配研究者，工具源头扎实。但二维iff与两射线充分性可能落入既有格理论/资源替代性。**工具分类储备；没有GAP新算法后果前不靠母文分量升级。** |
| GA02 Group GAP组尺寸越过m/2 | ESA2019 §6明确A，作者问比m/2更大组是否仍可常数近似 | 比GA01更直接符合原题要求，但跨过保留容量障碍没有现成机制。另加尺寸限制等版本仍是C。保留明确原题，不据年代或题短判断容易 |
| NA03 多面体凹效用cloning | Becker–Fries–Greger–Segal-Halevi，v3 §8末明确建议一般效用分类；min-of-linear识别为C。**Felix Brandt不是此文作者** | 来源正规、方向自然；当前active-cell识别/coNP包含可能是标准凸分析的短应用。需要tight complexity、可读禁形或新均衡算法后果。**暂储备，不与Sandholm来源等量齐观。** |
| AT01 有限权重近似势 | C。HKS2014实际作者为Hansknecht–Klimm–Skopalik；HKM2011为Harks–Klimm–Möhring；另有Caragiannis–Fanelli等成熟工具 | `{1,2}`及仓库具体因子均非作者原题；排列势、正比例缩放、边际夹逼已是旧工具。现有常数结果不足单独主攻；需一般结构、最优性或真正新后果 |
| AT02 有限权重差分势 | C。HKM2011 Proposition3.4、Example3.5已给固定需求curl机制与非仿射例 | 单字母表递推是直接特化，不能因源头作者强就包装新分类。当前不推荐独立主攻 |
| Hao–Michini拟阵PoA及距离引理 | PoA猜想A在作者版§6；距离引理C。作者有正式优化/博弈论文与同行认可，但不自行称最顶级领军组 | 比单个势常数更清楚地接到作者猜想。先核最终TEAC版本、交换图旧引理和真实优于一般界的区间；应用合同未闭合前不称已解/可发表 |
| FA09 个性化双值EFX+PO | 原始直接来源应为Jin–Tao WINE2025 §5；He–Tao2026 §6是后来的转述。一般题A，少人数/少件/两ratio限制C | 本轮更正来源，不改变数学身份。EFX+fPO反例不能否定EFX+普通PO。正式论文与具体工具支持其真实性，但尚不足把子题的价值视作已保证 |

图公平模型更早的作者Christodoulou、Fiat、Koutsoupias、Sgouritsa确有资深研究源头；这不使其成为FA01/02或FA17/18的具体出题人。导师致谢、引用经典工具、与大佬合作过均不等于对当前子题的背书。

## 一手来源与可复查位置

### 原子/Nash精炼

- [母文v2](https://arxiv.org/html/2511.03968v2)：Theorems4.4/4.5、Appendix E.1/E.2、§6去对称建议。另一分支稿中出现的E.4/E.5定位不对应此v2，不应沿用。
- [EC2026官方接收名单](https://ec26.sigecom.org/program/accepted-papers/)：确认六作者及篇名；不声称已经读到正式会议最终全文。
- [Sandholm CMU官方主页](https://www.cs.cmu.edu/~sandholm/)：IJCAI John McCarthy Award、ACM/AAAI/INFORMS Fellow等；[Balcan CMU官方主页](https://www.cs.cmu.edu/~ninamf/)和[CMU Hopper奖新闻](https://www.cs.cmu.edu/news/2020/balcan-receives-acm-grace-murray-hopper-award)。奖项属于作者，不属于本候选。

### 公平分配

- [Cookson–Shah v1](https://arxiv.org/html/2608.31121v1)：§5四人方向、Appendix B Definitions13/14、Lemma11及Lemma12前段。后者仅否定top-i分散旧工具。
- [copies作者全文](https://www.cs.toronto.edu/~nisarg/papers/constrained-fair-efficient.pdf)：§3.3.2 Definition5、Theorem6、末尾Open Question；[AAAI2025正式记录](https://ojs.aaai.org/index.php/AAAI/article/view/33499)。
- [Shah多大官方bio](https://www.cs.toronto.edu/~nisarg/bio.html)与[IJCAI官方奖项](https://www.ijcai.org/awards)：2024 Computers and Thought；bio另列经典MNW论文获2024 Kalai Prize，不能说本次两篇获该奖。
- [重边母文v5](https://arxiv.org/html/2512.25033v5)：Table1、Theorem13、§5；[WINE2026官网](https://wine2026conf.github.io/)列接收，未核到该文独立正式出版条目。
- 作者身份：[Kanellopoulos本人](https://skanellopoulos.github.io/)、[Nemery大学官方CV](https://dauphine.psl.eu/en/research/resume-database/profile/nemery-edouard)、[Sotiriou本人](https://minasmarios.github.io/)、[Vasilakis本人](https://manolisvasilakis.github.io/)。Sotiris不可误认成Panagiotis Kanellopoulos。
- [Jin–Tao原始v2](https://arxiv.org/html/2507.18251v2)：§5直接提出FA09一般问题；[WINE正式记录](https://link.springer.com/chapter/10.1007/978-3-032-18660-7_28)。

### 指派、舍入与优化工具

- [BMKP ICALP2026正式全文](https://drops.dagstuhl.de/storage/00lipics/lipics-vol374-icalp2026/html/LIPIcs.ICALP.2026.60/LIPIcs.ICALP.2026.60.html)：§7最后一段。八作者明确，Guochuan Zhang=张国川。
- [中国运筹学会会士页](https://www.orsc.org.cn/orscFellow/detail?id=68)：张国川的领域、运筹研究奖、学会任职；[浙大官方页](https://person.zju.edu.cn/en/0096209)。
- [Group GAP原文](https://arxiv.org/html/1907.01745v2)，Theorem1及§6；[ESA2019正式记录](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2019.69)。GA02明确原题和GA01派生分类不可混用。
- [成本保持舍入ICALP2025原文](https://drops.dagstuhl.de/storage/00lipics/lipics-vol334-icalp2025/html/LIPIcs.ICALP.2025.127/LIPIcs.ICALP.2025.127.html)：作者Rohwedder–Rouhani–Wennmann，Theorems2/3和§4；Shmoys/Tardos是被引用的经典工具作者，不是本文/后续题的署名作者。硬预算与双准则、星支撑与任意线性量、保成本与保边际须分开。
- [cloning母文v3](https://arxiv.org/html/2509.08767v3)：§8 Lemma8.2后、Theorem8.3后；不把母理论Brandt等的声望转借给本篇署名。
- [HKS2014正式记录](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.APPROX-RANDOM.2014.242)；[HKM2011作者全文](https://www.fim.uni-passau.de/fileadmin/dokumente/fakultaeten/fim/lehrstuhl/harks/TOCS-HKM-2011.pdf)；[Klimm官方](https://www3.math.tu-berlin.de/disco/team/klimm/)；[INFORMS奖项](https://www.informs.org/Recognizing-Excellence/Award-Recipients/Max-Klimm)。
- [Hao–Michini作者版](https://optimization-online.org/wp-content/uploads/2023/11/TEAC_Matroid.pdf)，§6；[ACM期刊入口](https://dl.acm.org/doi/10.1145/3787968)的最终全文本轮未成功读取，保留版本核查义务。

## 下一步与不能推出的结论

本轮建议把AP-02、FG01、FG02、两容量BMKP纳入共同前排再比较；重边题保留其数学价值，GA01/NA03/AT01作为尚需证明独立价值的工具储备。保持各分支原始判断与数学Claim，不因本次题源评价覆盖已保存证明。

对A题要问“我们完成的版本是否真正推进作者问题”；对C题要问“去掉作者名字后，这个定理自身是否仍有自然性、机制和算法后果”。名作者提出能提高问题受到重视的先验依据，不能保证子题新颖、足量、可解或录用。新近全文关键词检索没有找到解决，不等于认证仍开放；本轮没有任何候选升为可靠新一般定理。

本次事实修正：FA09改引直接原始文献；主池59条与非exclude52条的来源统计；各母文作者与子题身份澄清；强来源前排与现有排序的差异。以上值得保存，重复随机实验和新建候选不属于本轮动作。
