# exact 4-to-1 的应用与参数边界：本轮关系证明

## 已读对象和原结论核对

核心 M-ab4a576ed0be482b89d4a646ffc102b9 的实际结论是：每个固定 ε>0 都有一个常数字母表上界 r，使有限二部 exact 4-to-1 约束多重图的 val=1 与 val≤ε 承诺区分 NP-hard。左右标签数分别满足 |ΣL|=4|ΣR|；r 只给大小上界，与 Condition3.12 的内部参数 r 不同；定理没有给 ε 与字母表界的近最优函数关系，也没有给最大度界。

实读冻结 Fei–Minzer–Wang Revision2：PDF pp4–6 的 Definitions1.1/1.3、Theorem1.6 和 Corollaries1.7/1.9/1.10；pp21–26 的 sub-game 定义、Theorem3.3、技术输入和 Condition3.12；pp47–48 的 Game2b 完备性/可靠性；pp61–64 的 Game2c/Game3、完备性和最终可靠性；pp74–91 的展开/剪枝、excellent tuple、Lemma6.64 及其证明；pp99–100 的 exact 化。成熟外层/middle 的详细技术引理沿其完整原文入口复用，并非本轮重新逐句复证该119页论文的所有引理。

附录B确实允许保留原顶点后复制边：固定最终 ε∈(0,1)，从 sub-gap ε/2 出发，取 k=ceil(4/ε)，左右标签都乘 Z/kZ，每原边放 k 个 exact4-to-1 约束。YES 同取一个新坐标严格满足全部边；任意失败的旧标签对至多通过其中两个新约束，故新 val≤旧 val+2/k≤ε。标签界成为 kr，边数成为 k|E|；k,r 在归约实例大小之外先固定。不能把“同一顶点图”误读成不增平行边或有界度保证。

旧版正文§2.3把 Minzer–Zheng Lemma6.1 的 q-参数公式误归 Fei；这不否定 Fei Theorem1.6。五个正文owner已随正式源勘误更新至v2；逐段修法及原页证据位于同目录 source-corrections.json 和两张截图。

## 八可着色图：完整目标

要得到的整句目标是 M-922feb7b429f49d4b5f13ca51b34aae7：每个固定 δ>0，区分8-colorable有限图与独立集比例严格小于δ的有限图是 NP-hard。

核心给 GS20 Conjecture3 在 d=4 的全部承诺；其 exact4标签比、完美YES、任意小固定soundness和多重图均吻合。GS20 §2.1将该gap转换到其 d-to-d induced-list satisfiability 版本；Theorem9给 q=2d。其 §3.2–3.3 以支撑在不交d元组上的对称Markov链和长码构图。满足标签 σ 给码字 x 颜色 x_{σ(w)}，所有边两端颜色不同；大独立集则解码出小列表在正比例诱导子图内满足全部约束，违反其源gap。代 d=4 得 q=8。字母表与长码块大小在固定δ之后为常数，所以归约是多项式。该链支付整个目标，不声称图的最大度有常数界。FMW p6 Corollary1.9给同一应用核对。

原始归约证据为本任务下载并实读的 GS20 ICALP2020 正式PDF，原站：
https://drops.dagstuhl.de/storage/00lipics/lipics-vol168-icalp2020/LIPIcs.ICALP.2020.62/LIPIcs.ICALP.2020.62.pdf

具体读取范围：全文 pp62:1–62:12，尤其 Conjectures3–4、Theorems1/7/9、Lemmas6/8/10和§3.3；它只为本文既有端点的实际归约提供证据，不另建理论hub。GS20允许parallel edges见p62:3末段与p62:10。

## 三可着色图：完整目标

整句目标为 M-d007675a9ed240898c90e831af80b092：每个固定整数 k≥3，区分3-colorable与非k-colorable图是 NP-hard。

沿上一节 q=8 的独立集gap，任意固定C可先取 δ<1/C；有C-coloring必有至少1/C比例的独立集，因此NO图非C-colorable。GS20 Lemma8的arc-graph归约将“固定q可着色对任意常数palette”的硬度降到q=3；其一般步骤使用 b(n)=binom(n,floor(n/2))，另有4→3的两次arc步骤。给定目标k，先固定这条有限归约链所需的源palette C，再固定δ及核心的soundness/字母表；故没有让k随输入增长，也不把FMW Remark1.8的稍超多项式版本混进这里。正例始终完整合法着色，非近完整。FMW p6 Corollary1.7与GS20 Theorem1逐句核同。

## 双正规化桥与三一致超图

目标 M-9f8033b6e1a4485b97636171b09f8218 是：每个固定 δ>0，区分2-colorable三一致超图与无比例至少δ独立集的超图是 NP-hard。

KS14 Theorem1.3可调用固定d的任意小soundness、完美YES的exact d-to-1源。其§2.2 Conjecture2.5额外假定源biregular；footnote2明确说作者当时不知道能否WLOG。FMW Theorem1.6的陈述本身没有这个度数性质。以下独立复核正式lemma `PCP-EXACT-PROJECTION-PERFECT-COMPLETE-BIREGULAR-ROUNDING-v1` 的多项式桥，不能用同正文Minzer–Zheng的不完美完备性双正规定理替代。

### 确定性保完备性近似双正规化

令原有限未加权projection constraint multigraph有m>0条约束。去孤点不改val。原点度分别为d_u,d_v。为每个原点建立其度数个clone；两侧各恰有m个clone。每原边e=(u,v)，在两个clone云的每一对之间放同一原投影、权1/(d_ud_v)，保留e的tag。因此每个clone加权度1，新总边权m。

任意clone标签使每个原点独立、均匀抽一个clone，得到原图的随机标签。每条原边的期望满足量恰等于对应clone对的加权总满足量，所以新加权值不超过原值；原最优标签复制到全部clone取得反向不等式。两者val严格相等；原完美标签满足所有复制约束。

设 S=Σ_{e=(u,v)}d_ud_v≤m³，固定有理容许加性损失η∈(0,1)，取整数 D=ceil(S/(ηm))。对每个带原边tag的clone对引入变量 x_{eab}=D/(d_ud_v)。每个clone一侧的变量和都是整数D。对x取floor后，所有行列的剩余需求都是非负整数。分数余量给出了各余量边容量1的二部流的可行分数解；整数最大流给每个变量舍入到floor或ceil，且每行列恰为D。因此得到D-regular二部constraint multigraph、恰Dm个约束。

对任意标签，每个变量的满足指标属于{0,1}，其归一值相对原加权值的差绝对值≤S/(Dm)≤η，同时适用于全部标签。故新val≤旧val+η。YES仍满足全部留下的约束；每条保留投影仍exact4-to-1，标签均不变。x变量数S、多项式位长的有理数、D=O(m²/η)及Dm=O(m³/η)，可由有理运算和二部整数流在输入规模及 1/η 的多项式时间显式完成。固定δ后η为常数，才得到本处确定性多项式hardness归约；没有指数lcm或对二进制η声称显式输出统一bit多项式。该桥由Boss提出，本worker独立复核，随后以正式登记的独立lemma作为超图边的共同前提。

### KS14约束合同与调用

已下载原PDF https://arxiv.org/pdf/1308.3247 ，实读Theorem1.3(pp3–4)、Definition2.4/Conjecture2.5和footnote2(p7)、Theorem2.8(pp8–9)、§5.1–5.3(pp19–25)、AppendixA(p28)。原文以约束数定义正则性，未加simple图限制；其π_{v→u}是简化下标。用于本轮的精确约定是每次选择incident constraint都保留原边tag，邻居按约束出现次数计。附录A的换坐标构造、弱密度计数及§5的投影/期望分别按约束进行；对同端点的不同投影逐条保留，完全相同的平行测试也按重数抽样。这样其证明适用于上述多重图。具体地，AppendixA中一次原约束替换保留所选constraint-ID，若同一对问题产生多个投影就保留多个测试。各层度数、weak-density边数及投影满足率均以带ID约束计数；§5.1的超边生成对每个带ID的π_e各自取测试支撑；§5.3的heavy邻接比例、随机邻居smoothness概率与最后期望满足率同样保留重数。相同问题对上的不同投影会生成超边集合的并；在一个独立集上，每一个测试的乘积指标都为零，因此soundness对任何带ID约束抽样分布都成立。所有原证明的按约束求和及条件期望在此解释下不变，不需要不同邻点，也不把同端点不同映射合成一个关系。不得先去重源约束后再使用原值或正则度数。

原测试的三点确实互异，不能把退化边默删：p18定义 D_{δ,r} 先令 Z=-Y，每个fiber至多改一个坐标；本应用d=4、层差至少1，fiber大小r≥4，故至少另一个坐标的Y,Z仍相反，整个y≠z。x位于另一个层的long-code block，所以与y,z都不同。不同带ID测试若生成相同三点超边，最后可以去重，因为是否含有一条单色边/完整超边只取决于其出现，不取决于重数。

§5.1先给顶点权 w_x=2^{-R_l}/(L|V_l|)，每层总重1/L。转成目标的未加权有限超图还需一个明确步骤：所有非空层令 n_l=|V_l|，取 B=L·(∏_l n_l)·2^{max_l R_l}，把原顶点x替换成 B w_x 个不同clone，并把每条原三点超边替成三个clone云之间的全部三元组。各 Bw_x 为正整数，总clone数恰B。一个clone独立集所占据的原顶点集必是原独立集，否则任选每云一个已占clone便构成超边；反向复制某原独立集的全部clones可行。因此最大独立集比例恰等于原最大加权独立集质量。原2-coloring给每云统一颜色即保2-colorable。δ先固定后L和每个R_l均为常数，B及完整三部超边展开为输入规模多项式；这里没有对随输入增长的R_l声称统一多项式。

先固定目标δ，再取满足KS14归约要求的有理源soundness ζ∈(0,1)。在核心取soundness ζ/2，以上桥取η=ζ/2，即得到biregular、exact4、val=1对val≤ζ的硬度源。KS14 Theorem2.8及§5的长码三查询超图归约，完美标签给x_{σ(v)}二色着色，大独立集的heavy blocks经smoothness/invariance解码成源的正比例满足策略，产生矛盾。因此整个目标成立。这里支付的是承诺可区分硬度，不声称找到某个特定输入的NO证书；FMW p6 Corollary1.10给相同结论。

## 与近最优字母表交易的封闭比较

M-9a7614916cf04cee8915aefce74b502a 的主结论同时要求充分大R、soundness≤R^{-(1−ε)}和YES≥1−τ；MZ Definition1.1取 R=|ΣL|+|ΣR|。已实读其原PDF pp2–3的定义和Theorem1.3、pp8–9的Lemma1.7、p44的Lemma6.1、pp52–55的主定理证明和Theorem7.2，以及§1.3的perfect completeness开放方向。核心只给∀固定η∃常数r的gap，不能控制实际R上的幂次soundness：若仅知道例如r(η)=2^{1/η}这样的允许依赖，η≤R^{−(1−ε)}便不随之成立；这个例子只说明量词信息不足，不是声称论文实际r(η)等于它。反向MZ的YES允许严格小于1，且任意projection不自动有exact4结构。两边没有完整目标的蕴含或等价。本轮不为这个不付清的参数交换造accepted边。MZ的双正规版本也不提供上述完美YES源；本文独立整数流桥才支付超图应用需要的度数步骤。

以上比较仅涉及该正文明确的四个相邻数学对象及其精确归约证据；没有把PCP游戏迁移成unrelated-machines调度实例或六人SPE福利定理。
