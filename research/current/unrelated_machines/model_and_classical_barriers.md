# 不相关并行机的精确目标、经典舍入与配置间隙

本文是已知工具的自足重构，不声称原创突破。文献版本和精确定位见 [来源清单](../../unrelated_machines/literature_manifest.json)；主目标仍 OPEN，见 [精确账本](../../unrelated_machines/CLAIMS.md)。

## 1. 模型与目标身份

机器集 M={1,…,m}，m≥1；任务集 J={1,…,n}，n≥0。输入以二进制编码非负有理数 p_ij，另允许明确的不可用标记 ∞。每个任务至少有一条有限边。合法分配 σ:J→M 只能使用有限边，每台机器的负载为 L_i(σ)=Σ_{σ(j)=i}p_ij，C_max(σ)=max_i L_i(σ)，OPT(P)=min_σ C_max(σ)。任务不可拆分，无抢占、释放时间、先后关系、预测承诺、任务拒绝或通信模型约束。

`UM-TARGET-v1`：是否存在与所有输入无关的常数 ε∈(0,1)，以及一个确定性算法 A，使对所有上述 P，A 在输入总编码长度的多项式时间内输出合法 σ，并有 C_max(σ)≤(2−ε)OPT(P)？m、n 都是输入的一部分。随机算法、估值、准多项式算法和额外输入假设分别立新 Claim，不能替代本身份。

n=0 时空分配的值为0。OPT=0 当且仅当每个任务至少有一条零边：充分性直接逐任务选择零边；必要性来自非负性。算法必须精确处理该情形，不能用0/0比例或依赖正目标归一化。对 OPT>0 才可按目标T缩放。

## 2. 两个松弛的精确身份

给定有理 T≥0，E_T={(i,j):p_ij≤T}。LST 可行性 LP 是

Σ_i x_ij=1（每任务），Σ_j p_ij x_ij≤T（每机器），x_ij≥0，且 E_T 外 x_ij=0。

删除大于T的边是合同的一部分。不能把无剪枝的分数平均目标当本LP。可行性对T单调，但T同时决定边集；选择目标必须处理编码精度和边断点。整数处理时间可在有界整数区间二分；有理数可清分母，公共倍数的二进制长度至多各分母位数之和，不能用遍历所有整数时间的伪多项式实现冒充位多项式。本文程序仅接收已给定的可行x，不提供通用LP求解器。

C_i(T)={S⊆J:∀j∈S,p_ij<∞，Σ_{j∈S}p_ij≤T}，包含空集。Configuration LP 使用 y_iS≥0，Σ_S y_iS=1，Σ_iΣ_{S∋j}y_iS=1。精确覆盖与常见“至少覆盖”版本在向下封闭配置族中等价：删去配置中的任务不会增负载，可拆分权重逐步把过度覆盖降到1。不能在未说明向下封闭时套用此等价。

令 x_ij=Σ_{S∋j}y_iS，可得相同T的LST可行解。因此对正最优值有 T_LST≤T_CONF≤OPT。T_CONF是精确配置可行性阈值；指数列数与近似分离须单独分析，不能把精确配置LP当免费多项式oracle。

## 3. 有序槽匹配舍入的完整主链

`UM-ST-ROUND-v1`（已知结果重构）：给任意剪枝LST的有理可行解x，可确定性位多项式构造整数分配，使每台机器

L_i≤Σ_j p_ij x_ij + max{p_ij:x_ij>0}≤2T，空支撑的max定义为0。

这是Shmoys–Tardos型负载舍入版本；此处未声称实现其保成本最小费用匹配版本。

**构造。** 对每台i，把正x任务按p_ij非增序排列，将长度x_ij的连续区间依次放在数轴上。用单位槽[0,1]、[1,2]等切开。任务j与相交且交长为正的槽相连，边权为交长。机器的槽数为 ceil(Σ_j x_ij)≤n。每任务的全部边权和为1，每槽的全部边权和≤1。

**存在匹配。** 任意任务子集Q的单位需求总量是|Q|，流入其邻槽的总量也是|Q|，各槽容量≤1，故邻槽数≥|Q|。Hall条件给覆盖所有任务的整数匹配；增广路可确定性找到。每个任务分配给所匹配槽的机器，仍是其正x支撑边。

**负载。** 若i的第r≥2个槽选到任务j，因排序，前一完整单位槽内的每个处理时间均≥p_ij。因此本槽所选任务的处理时间≤前一槽的分数处理量。对r≥2求和，各前槽不重叠，合计≤原分数负载；第一个槽最多增加支撑最大处理时间。没有被匹配的槽贡献0，结论仍成立。

**位复杂度。** 槽与边的数量至多多项式；区间端点和交长由输入有理数加减组成，分母乘积的位数至多输入分母位数之和。匹配组合步骤多项式，所有比较可用整数交叉相乘。若再接一个符合位复杂度合同的可行性LP和目标搜索，可得经典通用2近似。只有舍入程序跑通，不能声称整个LP求解流程已实现。

## 4. 配置LP间隙族的独立重索引重构

`UM-CONF-GAP-v1` 是Verschae–Wiese的已知障碍，不是新困难性证明。以下给安全高度约定；原arXiv v1的Lemma5/6与N的记号存在一层索引不一致，不能逐字抄写后省略检查。本文直接由基例推导递推，未宣称核对了期刊版是否修正。

取整数k≥4，q=k/(k−1)，α_h=q^(h−1)/(k−1)。令h≥1最小满足α_h≥1/2。则α_h<q/2≤2/3，递推中全部权重非负。

造两个相同的根树：从根到第h−1层，每个内部点有k个不同孩子；每个第h−1层点再有一个终端点，与之有k条平行边。顶点是机器，每条父子边是任务，在父端耗时1/k、子端耗时1。另有一个任务在两棵树根上都耗时1；其余机器边不可用。因此每任务恰有两条有限边。

**整数下界。** 将根间大任务分给某根。若整个调度负载小于2，则该根不可能再接全部k条小端任务，至少有一条下传到孩子并在那里耗时1。同理一路下传，到平行边的父端时已有一个耗时1的incoming任务。若平行边中≥2条下传，终端负载≥2；否则父端至少承担k−1条小任务，负载≥1+(k−1)/k=2−1/k。故OPT≥2−1/k。

**可达上界。** 沿一棵树选一条根到末层的路径；路径上每个非末节点把一条小端任务下传、其余k−1条留在本节点。末节点同样下传一条平行任务，其余留在父端。路径节点的负载都是2−1/k；其他子树全部边留在父端，负载≤1。另棵树全留父端。故本重构中OPT恰为2−1/k。

**配置可行性。** 目标T=1+1/k。一个末层父端有incoming任务a和k条small任务b_ℓ。终端以各1/k权重选择单任务{b_ℓ}。父端以各1/[k(k−1)]选择{a,b_ℓ}，以1−1/(k−1)选择全部small。每个b_ℓ覆盖恰1，a边际α_1=1/(k−1)。

归纳：若k个子树各把incoming边覆盖α_r，则其父端以各α_r/(k−1)选择{a,b_ℓ}，以1−kα_r/(k−1)选择全部small。每个b_ℓ从父端得到1−α_r，故总覆盖1；a边际α_{r+1}=qα_r。所有配置负载≤1+1/k；选择h保证每一步归一化且权重非负。

两根的incoming都是根间大任务，其当前边际α_h≥1/2。对每个含incoming的配置，以概率1/(2α_h)保留它，否则只删除incoming，保留其中所有small。于是每根incoming边际恰1/2，其他任务边际、归一化与可行负载保持。合并两树得到整个实例在T可行的显式有理配置证书。

故 OPT/T_CONF≥(2−1/k)/(1+1/k)=(2k−1)/(k+1)=2−3/(k+1)→2。第3节和配置投影又给gap≤2。因此supremum gap=2；这里没有声称某个有限实例恰取2，也没有声称本证书T必是最小配置阈值。

**障碍范围。** 不存在对所有配置可行输入与所有T都输出负载≤(2−ε)T的舍入保证（固定ε>0），因为上述族会违反它。这不否定相对OPT的(2−ε)算法：算法仍可引入跨机器约束、额外组合证书、更强下界或其他机制。单机配置已是每机器可行0/1向量凸包；只加对所有这些单机配置均有效的局部不等式不会切掉其投影。

## 5. 代码、证据与尚未内化部分

[Fraction核验程序](../../../tests/audits/unrelated_machines/rounding_and_gap.py)实现有序槽匹配、独立指数枚举、显式配置证书和仅对本对称树族的压缩动态规划。它拒绝浮点、负时间、不可用边上的正质量和不守恒x；含T=0和空任务检查。[冻结结果](../../../evidence/runs/unrelated_machines/classical_baseline_audit.json)明确枚举范围、seed、版本和代码哈希。程序中的三机器示例只验证OPT=3和一个值5的合法调度，不声称已复现教材指定分数解与匹配。

2005的2−1/m、一般问题3/2以下困难性、固定m近似方案及受限指派局部搜索暂以Paper Fact记录，尚未在本专题逐步独立重建它们的完整证明。不得以“下载全文”升级为“所有证明已内化”。后续优先把与新候选承重相关的定理逐条重构，而不是把书目扩张当原创研究进度。

## 6. 全常数否定与稠密小整数正规形

**研究方向与逻辑身份。** 当前主攻转为否定 `UM-TARGET-v1`，该命题的原量词与 OPEN 状态不改。任何实数常数 ε>0 都有某个整数 k≥2 满足 1/k≤ε；同一个算法随即满足较弱的 `(2−1/k)` 保证，无须计算或编码 ε。因此原目标等价于“∃整数 k≥2，∃一个确定性位多项式程序，∀合法输入，输出合法 `(2−1/k)` 调度”。精确否定量化所有这样的 k 和程序；仅排除一个固定比率、一个松弛或一种舍入器都不够。这里的阿基米德化是基础逻辑，不认领其新颖性。

**UM-DENSE-SMALL-INTEGER-EQUIVALENCE-v1。** 定义 D 为所有显式 m×n 矩阵，m,n≥1，全部有限且每项都是 `{1,…,n²}` 中的整数。则原目标成立，当且仅当在 D 上存在统一常数改善的确定性位多项式实际调度算法。具体地，对每个固定整数 k≥2，给定一个在 D 上保证 `α=2−1/k` 的算法 B，可构造覆盖原完整模型、保证 `2−1/(2k)` 的算法。反向直接限制输入域。此为标准缩放、向上取整与大成本替代的自足接口重构；全球新颖性和独立论文价值未认证，不是新的近二困难性定理。

**完整构造。** 空任务直接返回空分配。若每个任务各有零边，就把它分配到任一零边；非负性保证此分支恰覆盖 OPT=0。其余输入满足

\[
0<L:=\max_j\min_i p_{ij}\le\operatorname{OPT}(P)
\le U:=\sum_j\min_i p_{ij}\le nL.
\]

若 n<8k，精确枚举每个任务的有限端组合并保留最小负载；枚举次数至多 m^{8k}，其中指数 8k 固定，不随输入增长。否则令 `g=1+1/(4k)`，实际生成 `T_h=Lg^h`，直到首个 `T_H≥U`，包含首末两项。对每个候选 T 构造**保留同一 n 个任务和 m 台机器**的矩阵

\[
q_{ij}(T)=
\begin{cases}
\max\{1,\lceil 4knp_{ij}/T\rceil\},&p_{ij}\le T,\\
n^2,&p_{ij}>T\text{ 或 }p_{ij}=\infty.
\end{cases} \tag{6.1}
\]

在 B 的实际输出中，若有任务使用原来 `p_ij>T` 或不可用的边，就舍弃这个候选；其他输出按原有理矩阵计算全部机器负载，保留最好者。不把 B 的失败或任何单个候选的舍弃解释为 OPT>T。

**D 域与至少一次成功。** 保留边上 `1≤q_ij≤4kn≤n²`，其他边为 n²，故每份 Q 都在 D 内，包括原来的零边和不可用边。取首个 T≥OPT；它满足 `T≤g OPT`。原最优调度的全部边在该 T 下保留，且在每台机器上取整最多增加其任务件数，故同时有

\[
\operatorname{OPT}(Q)\le (4kn/T)\operatorname{OPT}(P)+n
\le(4k+1)n. \tag{6.2}
\]

因此 B 在这个候选上的 makespan 至多

\[
\alpha(4k+1)n=(8k-2-1/k)n<n^2. \tag{6.3}
\]

任一大成本替代边单件就用时 n²，故此输出不会用到替代边，也一定不会被舍弃。这里必须保留严格不等式；不能只说有限大成本“等同不可用”。

**逐机回译与比率。** 在所有保留边上 `p_ij≤Tq_ij/(4kn)`，包括 p_ij=0。用 (6.2) 的**较强第一项**而非只用粗界 `(4k+1)n`，得到

\[
\begin{aligned}
C_P(B(Q))
&\le \frac{T}{4kn}\alpha\operatorname{OPT}(Q)\\
&\le \alpha\left[\operatorname{OPT}(P)+\frac{T}{4k}\right]\\
&\le \left(2-\frac1k\right)
 \left(1+\frac1{4k}+\frac1{16k^2}\right)\operatorname{OPT}(P)\\
&=\left(2-\frac1{2k}-\frac1{8k^2}-\frac1{16k^3}\right)
 \operatorname{OPT}(P)
\le\left(2-\frac1{2k}\right)\operatorname{OPT}(P).
\end{aligned} \tag{6.4}
\]

逐候选取原负载最小值只会改善此界。输出是原任务的一次合法完整分配，而非一个阈值估计。

**总位复杂度。** `g^{4k}≥2`，所以 H≤4k⌈log₂n⌉；可用有理乘法与比较实际生成候选，不调用实数对数。L,U 的编码长度受原输入总位长的多项式控制，每次乘 g 只增加 O(log k) 位。式 (6.1) 用整数交叉相乘及整除算 ceil，每份 Q 的总位长 O(mn log(n+1))，B 调用次数为固定 k 下 O(log n)。枚举分支的指数依固定 k，不随输入增长。超大有理分母不会引入按其数值或倒数循环。全部判断和逐机负载比较都可精确进行。

**范围与反面义务。** 这是一条**算法存在性的双向等价**，不是从某个 NP 完全源直接产生 gap 的归约。它不声称 D 已经有近二 NP-hardness，也不声称原目标为假；不存在统一改善若获证明，将同时适用于这份常规整数输入类。无条件反证至少蕴含 P≠NP，既有完整说明见[反向合同](private_graft_and_resource_repetition.md)§1。当前仍缺对每个固定 ε 的真实 YES/NO gap 与所有低负载调度的源解码。

**Evidence / Objections / Status / Related Files。** 先对精确陈述独立重构，再对最终正文和精确程序冻结攻击；实际覆盖与哈希见[专门审查](../../reviews/unrelated_machines/dense_small_integer_equivalence_review.md)。[审计程序](../../../tests/audits/unrelated_machines/dense_small_integer_equivalence.py)及[冻结运行](../../../evidence/runs/unrelated_machines/dense_small_integer_equivalence.json)仅验证声明范围内的边界、算术及有限全调度，不能代替本节一般证明。没有实现假设中的未知 B，没有一般新近似算法或困难性状态升级。

## 7. 单一对数平方字母表的稠密整数正规形

**UM-DENSE-GEOMETRIC-ALPHABET-EQUIVALENCE-v1。** 本节进一步限制§6的整数输入域。它是标准缩放/几何取整的自足推论，不认领全球新颖性或新的困难性。对每个实际任务数n≥16定义

\[
h=h_n=\operatorname{bitlength}(n)=\lceil\log_2(n+1)\rceil,
\quad b=b_n=1+1/h,
\quad R_n=\min\{r\in\mathbb Z_{\ge0}:b^r\ge hn\},
\]
\[
\mathcal A_n=\{\lceil b^r\rceil:0\le r\le R_n\}\cup\{n^2\}. \tag{7.1}
\]

重复整数去重。令D_geo为所有m≥1、n≥16、每项均在A_n的显式m×n矩阵；所有边有限、所有处理时间为正整数。字母表只依赖n，不依赖原处理时间、隐藏阈值、分母或所求ε。原UM-TARGET-v1成立，当且仅当D_geo上存在统一改善的确定性位多项式实际调度算法。定量地，任一先固定整数k≥2的D_geo算法B若保证α=2−1/k，则可构造原完整模型上保证2−1/(2k)的算法。固定k下复杂度次数有限；不声明关于可变二进制k的一致多项式。

**字母表与位长。** 二项式定理给b^h≥2，所以

\[
R_n\le h\lceil\log_2(hn)\rceil,\qquad
|\mathcal A_n|\le h\lceil\log_2(hn)\rceil+2=O(\log^2 n). \tag{7.2}
\]

h≥5、n≥2^(h−1)>2(h+2)；最后一个不等式由h=5的16>14起归纳。R_n的最小性给b^(R_n)<(h+1)n，从而ceil(b^(R_n))<(h+1)n+1<n²。因此A_n⊆{1,…,n²}，且保留边的全部数值严格小于哨兵n²。实际按确切有理数b逐次生成幂，分子分母位长O(log²n loglog n)，再用整数整除取ceil；不使用近似实对数。最终每个条目仅O(log n)位。

**全模型转换。** n=0返回空分配；每任务有零边时逐任务选零边，精确处理OPT=0。其余情形沿用§6的0<L≤OPT≤U≤nL。若h=bitlength(n)<8k，枚举原有限端组合求精确最优。此时n<2^(8k)，枚举次数至多m^(2^(8k))，对先固定k是固定多项式次数；这不是实用效率主张。该分支覆盖n<16。

现设h≥8k≥16。实际生成候选T=L b^t，直到首个T_H≥U，包含首末项；由b^h≥2，H≤h ceil(log₂n)=O(log²n)。对每个候选保持原m和n，在p_ij≤T的保留端上定义

\[
z_{ij}=hnp_{ij}/T,\quad
r_{ij}=\min\{r\in\mathbb Z_{\ge0}:b^r\ge\max(1,z_{ij})\},\quad
q_{ij}=\lceil b^{r_{ij}}\rceil. \tag{7.3}
\]

p_ij>T或p_ij=∞时令q_ij=n²。因为0≤z_ij≤hn，r_ij≤R_n，所以每份Q(T)均在同一个D_geo类。零边映成1，p_ij=T仍是保留边。对全部z≥0，取整满足

\[
z\le q(z)\le bz+1. \tag{7.4}
\]

z≤1时q=1；z>1时最小性给b^(r−1)<z≤b^r，故q<bz+1。运行B(Q(T))，检查其真实完整输出。若使用原p_ij>T或∞端，舍弃该候选；否则按原P精确回算全部负载，保留最好者。舍弃候选不提供FAIL⇒OPT>T语义。

**严格哨兵排除与逐机回译。** 取网格中首个T≥OPT，便有T≤b OPT。原最优分配的全部端均保留。逐机相加(7.4)，最多n项，得较强第一式

\[
\operatorname{OPT}(Q(T))
\le b\frac{hn}{T}\operatorname{OPT}(P)+n
\le(h+2)n. \tag{7.5}
\]

B在此候选上有C_Q≤α(h+2)n<2(h+2)n<n²，故不可能使用单件即耗n²的哨兵端，此候选一定保留。对所有保留端p_ij≤Tq_ij/(hn)，结合(7.5)第一式可得

\[
\begin{aligned}
C_P(B(Q(T)))
&\le\alpha\left[b\operatorname{OPT}(P)+T/h\right]
\le\alpha b^2\operatorname{OPT}(P),\\
\alpha b^2
&\le\left(2-\frac1k\right)\left(1+\frac1{8k}\right)^2
=2-\frac1{2k}-\frac7{32k^2}-\frac1{64k^3}
<2-\frac1{2k}. \tag{7.6}
\end{aligned}
\]

取原负载最小的候选仍满足此界，输出原任务的合法完整分配。h、全部候选和幂可精确计算；T位长至多原输入位长加O(log²n loglog n)，逐端比较/查找/ceil、原负载求和均为总位多项式。每份Q有O(mn log(n+1))位，B调用次数多项式。未知B没有被当作已实现求解器。任意正实改善支配某个1/k，无须编码该实数；反向限制输入域直接成立，完成存在性等价。

**反面研究范围。** [固定有限字母表的gcd界](finite_processing_palette_gcd_barrier.md)固定的是实际数值集合或统一g/B余量；A_n随n变化，b_n→1，不与其冲突。即使一个近二困难性族对每个固定ε只用依赖ε的有限字母表，也没有被该固定集合结果统一排除。这里进一步说明，大量独特数值、巨大分母、零边或不可用边都不是否定原目标所必需的：单一O(log²n)种正整数、每项≤n²的全可用域已足够。它没有提供NP源gap或低负载调度decoder，主目标及其反面仍OPEN。

先陈述独立重构与最终正文/代码读后攻击见[专门审查](../../reviews/unrelated_machines/geometric_alphabet_equivalence_review.md)。[Fraction程序](../../../tests/audits/unrelated_machines/geometric_alphabet_equivalence.py)及[冻结运行](../../../evidence/runs/unrelated_machines/geometric_alphabet_equivalence.json)分别标明小h变换测试、大n仅网格测试，以及真正h≥8k分支的完整负载类型枚举；有限核验不代替一般证明。

## 8. 多项式私有填充与单一对数字母表正规形

ID/version: `UM-DENSE-LOGARITHMIC-ALPHABET-PADDED-EQUIVALENCE-v1`.

This is a self-contained sharpening of the existing §7 normal form, with a
different operation: the transformed task count may grow polynomially, with
degree depending on the backend's fixed improvement. It is an approximation
existence equivalence, not a hardness proof, a supplied sub-2 solver, or a claim
of novelty. The existing same-task-count statement is preserved.

### 8.1. Universal family and exact quantifiers

For each integer task count N>=2 let H=bitlength(N) and define

\[
 b_j=1+\frac1{8j},\qquad
 R_{N,j}=\left\lfloor\frac H{2^j}\right\rfloor,
\]
\[
 \mathcal A_N=\{1,N^2\}\ \cup\!
 \bigcup_{\substack{j\in\mathbb Z,\ j\ge2\\2^j\le H}}
 \{\lceil b_j^r\rceil:0\le r\le R_{N,j}\}.       \tag{8.1}
\]

Repeated integers are removed. This alphabet depends only on the actual
transformed task count N. Define D_log as all explicitly encoded m' by N
matrices with m'>=1, N>=2 and entries in A_N. Every edge is finite and positive.

**Claim.** UM-TARGET-v1 holds if and only if D_log admits a deterministic
polynomial-bit-time scheduling algorithm with some universal improvement below
2. Quantitatively, fix an integer k>=2. Given a D_log algorithm B with ratio
alpha=2-1/k, the construction below is a deterministic polynomial-bit-time
algorithm on the full original model with ratio at most 2-1/(2k).

The polynomial's degree can depend on this fixed k; no uniform polynomial in
a binary input k is asserted. Any positive real improvement dominates 1/k for
some fixed integer k, so its numerical encoding is not needed. The reverse
implication simply restricts the full-model algorithm to D_log.

### 8.2. Palette size, values and computability

All r=0 values are the same integer 1, so

\[
 |\mathcal A_N|\le2+\sum_{j\ge2}\left\lfloor H/2^j\right\rfloor
 \le2+\lfloor H/2\rfloor=O(\log N).                \tag{8.2}
\]

For r>=1, b_j<2 and r<=H/4<=H-1; consequently

\[
 \lceil b_j^r\rceil\le2^r\le2^{H-1}\le N.
\]

The r=0 entry is 1. Hence all ordinary palette entries are at most N, and
A_N is contained in {1,...,N^2}; the sentinel N^2 is strictly larger than every
ordinary entry for N>=2. The grids have O(log N) total exponents. Their powers
and ceilings can be generated by exact integer arithmetic; j=O(log H),
r=O(H), and power numerator/denominator lengths are O(H log(H+1)), a sufficient
polynomial bound. No floating logarithm or algebraic-number oracle is used.

### 8.3. Original boundary cases and polynomial padding

Let P have m>=1 machines and n>=0 jobs, nonnegative binary rationals or explicit
infinity, with at least one finite edge per job. For n=0 return the empty
schedule. If each job has a zero edge, choose such edges and return OPT=0
exactly. Otherwise

\[
 0<L=\max_j\min_i p_{ij}\le O=\operatorname{OPT}(P)
 \le U=\sum_j\min_i p_{ij}\le nL.
\]

Let ell be the least nonnegative integer with 2^ell>=8kn. This can be computed
as bitlength(8kn-1). Set

\[
 E=2^k\,8k\,\ell,\qquad N=2^E,
 \qquad H=E+1,\qquad d=N-n.                       \tag{8.3}
\]

Here ell>=4, N>n, and for fixed k,

\[
 N<(16kn)^{8k2^k}.
\]

Create d private dummy jobs and d private machines, in addition to the original
n jobs and m machines. Thus the actual target dimensions are (m+d) by N, which
are polynomial in the original input length for fixed k. Huge constants and
degrees are allowed by this existence statement; this is not an efficiency
claim for implementation.

The k-th grid is present, and its last exponent is

\[
 R_{N,k}=\lfloor (E+1)/2^k\rfloor=8k\ell.
\]

The binomial theorem gives b_k^(8k)>=2, and therefore

\[
 b_k^{R_{N,k}}\ge2^\ell\ge8kn.                   \tag{8.4}
\]

### 8.4. Thresholds and the full target matrix

Let b=b_k and s=8kn. Generate the finite rational grid T_t=L b^t until its
first value at least U, including both endpoints. The grid has at most
8k ceil(log_2 n)+1 values. For every candidate T and every original edge with
p_ij<=T, define z=s p_ij/T and

\[
 r(z)=\min\{r\in\mathbb Z_{\ge0}:b^r\ge\max(1,z)\},
 \qquad q_{ij}=\lceil b^{r(z)}\rceil.             \tag{8.5}
\]

Because 0<=z<=s and (8.4) holds, r(z)<=R_{N,k}. Original edges with p_ij>T or
p_ij=infinity are assigned sentinel N^2. An original job has sentinel on every
dummy machine. Each dummy job has value 1 on its own private machine and
sentinel N^2 on every other machine, original or dummy. This explicitly defines
every entry of the target matrix Q(T); all entries belong to the same A_N.

The scalar rounding inequalities, including z=0 and z=1, are

\[
 z\le q(z)\le bz+1.                              \tag{8.6}
\]

Run B on Q(T). Check that its actual output assigns all N jobs to target
machines. Reject the candidate if any job uses a sentinel edge. This includes
every dummy leaving its own machine and every original job leaving the
retained original edges. For surviving candidates, discard the private dummy
jobs and machines, compute all original loads in exact rational arithmetic,
and return the original schedule of smallest makespan. Rejecting a candidate
does not certify OPT(P)>T.

### 8.5. Every qualifying output decodes at a good threshold

Take the first candidate T>=O. Then O<=T<=bO, and every edge of an optimal
original assignment is retained. Extend that assignment by putting each dummy
on its own machine. Applying (8.6) on each original machine and noting that
each such machine receives at most n jobs gives

\[
 \operatorname{OPT}(Q(T))
 \le b(s/T)O+n\le(8k+2)n.                        \tag{8.7}
\]

The extended dummy loads are 1, already below the right side of the first
inequality since n>=1. From (8.3), N>=16kn, and hence

\[
 \alpha\operatorname{OPT}(Q(T))
 <2(8k+2)n<N^2.                                  \tag{8.8}
\]

Every complete target schedule with makespan at most alpha OPT(Q(T)) therefore
uses no sentinel edge. This statement quantifies over all such outputs, not
over a favored optimal schedule. In particular B's actual output survives,
each dummy is on its own private machine, and all original jobs decode to
retained original edges.

For every retained original edge p_ij<=Tq_ij/s. Use the stronger first bound in
(8.7), rather than just its coarse last bound, to obtain

\[
 \begin{aligned}
 C_P(B(Q(T)))
 &\le (T/s)\alpha\operatorname{OPT}(Q(T))\\
 &\le\alpha\,[bO+T/(8k)]\le\alpha b^2 O\\
 &=\left(2-\frac1{2k}-\frac7{32k^2}-\frac1{64k^3}\right)O
 <\left(2-\frac1{2k}\right)O.                    \tag{8.9}
 \end{aligned}
\]

The least original load among surviving candidates inherits this guarantee.

### 8.6. Bit complexity and limitations

All original rational numbers are only added, multiplied by exact grid powers,
compared by integer cross multiplication, or passed through integer ceil.
For fixed k, the threshold grid has O_k(log(n+1)) terms and bit lengths increase
by O_k(log(n+1)). N is polynomial in n with a fixed k-dependent degree; Q is
written explicitly, including all dummy cross-edges. Its entries have at most
2E+1=O_k(log(n+1)) bits. Thus construction, all B invocations, full output
validation and back-translation are polynomial in the original total encoding
length. No loop is proportional to a rational denominator or its reciprocal.

The alphabet in (8.1) is independent of P, T and k. Polynomial padding is what
allows each fixed k to use enough of its allocated grid while keeping the
total alphabet logarithmic in the actual transformed task count. This does
not establish a logarithmic alphabet with the same original task count, and
does not exclude a still smaller alphabet by a different mechanism.

The result supplies no NP source, no near-2 integer YES/NO gap, and no source
decoder. UM-TARGET-v1 and its negation retain their OPEN status. This is a scoped proof with exact finite audit; external review and global novelty are unverified.

### 8.7. Actual audit contract

[Exact audit](../../../tests/audits/unrelated_machines/logarithmic_palette_padding_equivalence.py) independently enumerates active-job
assignments on small rational matrices, including zeros, infinity and large
denominators, and quantifies over every alpha-qualifying target active load
pattern. The astronomical private block is represented exactly: every
nonprivate dummy assignment has load at least N^2; all low-load dummy assignments
are uniquely private with load 1. This is a complete compressed classification,
not literal construction of an N-column fixture or execution of unknown B.

The [dedicated review](../../reviews/unrelated_machines/logarithmic_palette_padding_equivalence_review.md) separates statement-first reconstruction from actual proof/code reading. The [frozen run](../../../evidence/runs/unrelated_machines/logarithmic_palette_padding_equivalence.json) records the compressed padded-load classification, without claiming to materialize the enormous matrix or execute the unknown backend.
