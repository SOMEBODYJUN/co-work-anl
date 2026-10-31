# Exact-only：可变多个单state outer、极小home权重的19/10算法

作者：`/root/sol_general_repair`，2026-10-18。scratch 待独立后置攻击的限定算法候选，不是一般 UM-TARGET-v1，不声称新颖性。本文件只给输入模型和量词结论，不给作者证明、权重更新、随机实验、方差或去随机化算法。

## 1. 显式 typed 输入域

输入有任意正整数k个outer groups O_1,...,O_k；k是显式输入的一部分，**不是固定常数**。每个O_i恰好只有一个indexed state，其正支持为homes g_(i,j)、j∈J_i，系数是正二进制编码有理数w_(i,j)，满足

    sum_(j in J_i) w_(i,j)=1,
    max_(i,j) w_(i,j) <= 1/(4096 k^4).

所有homes在不同(i,j)间物理互异。每个home有且只有一个对应helper H_(i,j)。它的own indexed state为该home的unit singleton；它的其他indexed states是有限资源集B上的任意显式normalized非负二进制编码有理向量。B与全部homes不交；不同helpers、不同outers的fallback支持可任意重叠。helper可以没有fallback state，总保留own state。没有其他groups。

每个indexed state/resource pair至多列出一个incidence。给定的零incidences、重复fallback state索引、unused resources均保留。零incidences不改变上述正home支持或归属假设。输入是完整显式typed菜单Q；没有隐式或succinct状态编码。profile条件是该输入域的实质限制，未声称可将任意菜单免费归一化到该条件。

## 2. 完整普通 UM 矩阵

为每个indexed state建立不同private machine，为每个资源建立resource machine。每group一个原unit selector，只能在该group全部state-private machines执行；outer的selector因此只有一个有限机器端。每个listed incidence为一个原不可拆job，在自己的state-private machine时间原系数、在exact resource machine时间1，其他单元无穷。没有额外guard、容量或状态逻辑约束。

所有helpers的未选fallback states payload、给定零incidence jobs、全部selectors均必须执行。若groups、states、listed incidences、resources数为G,S,I,U，则P(Q)有S+U台原机器、G+I原jobs、S+2I个有限资格单元。结构呈现随输入提供，不要求从任意unrelated矩阵识别它。

## 3. 精确声称

存在一个固定确定性总位多项式算法，对每个第1–2节域内的typed Q，**仅接收Q本身**，显式生成完整普通矩阵P(Q)并输出所有原jobs在原有限端点上的完整assignment sigma，满足

    C_max(sigma) <= (19/10) OPT(P(Q)).

多项式次数为绝对常数，不依赖k、home数、fallback支持宽度、indexed states数或输入分母的数值。不给feasible relaxation点、actual allocation、真实OPT、精度参数或实际调度oracle；不提供精确SDP oracle。

允许使用标准确定性有理LP可行性算法。若候选算法采用plain common primitive-SA1，其精确系统是：每原indexed state一个binary A，每listed incidence一个binary Z；state partitions、所有boxes、gates Z<=A、resource capacities sum Z<=1、每state perspective quality sum pZ>=epsilon A；每个原线性row均保留并乘每个同一原A/Z primitive及其补，全部使用一个共同对称二阶数组、binary diagonal。这些均需从Q显式生成并求解，不是免费给定的点。无需PSD、unit-FSLP或真实joint state distribution假设。

此结论没有推广到outer含多个states、home支持重合、缺少own-home helper、额外auxiliary core、未满足tiny-home条件或任意普通UM矩阵。它不解决一般主目标，不排除这些更广域的困难性，也没有端到端实现、外审或新颖性声明。
