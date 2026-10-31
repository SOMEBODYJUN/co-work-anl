# 加权Leontief均衡与线性Fisher市场：已知接口的精确重构

日期2026-10-20；任务仅为审核根部给出的一个完整框架，不新开候选池。读取2509.08767v3 §§5,8，以及证明/排覆盖必需的既有文献。没有追加随机实验。

## 判断先行

根部的“weighted-log弱优化 → 强凹坐标精度 → 有理恢复 → critical flow”路线可以补成二进制多项式算法；未发现致命数学反例。本文给出明确分母界、内球、梯度/函数值oracle、误差常数与边界条件。

但**更直接的覆盖机制已经出现**：weighted public Leontief NE的贡献矩阵，恰好满足同一估值与预算的**标准linear Fisher市场的money/spending equilibrium**条件。因此可直接调用Orlin2010的精确linear Fisher算法，不必采用弱优化有理恢复。该对应也落在Tao–Zheng2025《Fisher Meets Lindahl》的既有一般对偶定理与Brandt等2025 Proposition1的组合内。

因此NA02作为新算法主目标淘汰。正确处置是：保留为已重构的完整接口与文献覆盖资产；**不要把weighted exact NE标为本轮新解原问题或直接锁为独立论文**。2509.08767v3 §8仍写open不能抵消这条覆盖链。

## 1. 精确模型和可去掉的退化输入

给n个agent、m个project，输入是二进制编码非负有理数v_ix和budgets b_i，sum_i b_i=1。每个正budget agent至少有一项v_ix>0；其Leontief效用为

    U_i(δ)=min_{x:v_ix>0} δ_x/v_ix.

策略X_ix>=0，sum_x X_ix=b_i，总量δ_x=sum_i X_ix。每个agent只改变自己一行，效用看所有行的总和。

b_i=0的agent没有可选偏离，可先删掉并最终补零行。之后删掉所有正budget agent都估值0的project，最终补δ_x=0和零贡献列；这一步不会遗失一个需要输出的NE。对余下instance所有b_i>0，每行/列至少一个正v。m=1和n=1均允许。

如原budget C_i总和B不是1，可先置b_i=C_i/B，最后把所有δ和X乘B；也可全程用总money B的Fisher模型。以下规范化总budget为1。

## 2. 自足critical-support lemma（适用于任意正budgets）

设T_i(δ)=argmin_{v_ix>0} δ_x/v_ix。一个策略矩阵X是NE iff每行正贡献只落在T_i(δ)。

**充分性**：若X_i全在T_i，严格提升效用必须增加每个critical project的总量，因此必须同时增加agent在T_i上的总贡献；但她已经把全部budget放在T_i上，无从做到。

**必要性**：若她在非critical z上有正贡献，从z挪出足够小ε，按v_ix比例分给全部critical x。每个critical ratio严格提高；有限多个非critical正估值项有严格slack，可取ε小到这些项不先跌到旧效用。若v_iz=0，减少z也不损她效用。这样构成严格有利偏离。

此外任一NE中U_i(δ)>=b_i/sum_x v_ix>0：agent可用自己budget按v_i比例分配，其他agent非负贡献不会损害保证。若每行v归一化为sum_xv_ix=1，则U_i>=b_i。

该lemma是2509.08767v3 Lemma5.2所引的Brandt等结构结论；这里重证以排除“克隆才适用于weighted”的疑虑。

## 3. 完整两向归约：public Leontief ↔ private linear Fisher spending

构造linear Fisher市场：相同buyers i、goods x；每个good供给1；buyer i有budget b_i，private utility为sum_x v_ix y_ix。**这个private线性效用不是public Leontief效用**。令p_x是Fisher price，X_ix=p_x y_ix是money spending。

Fisher equilibrium的spending合同为

    X_ix>=0,
    sum_x X_ix=b_i,          (每buyer花完budget)
    sum_i X_ix=p_x,          (每good恰好卖完一单位)
    X_ix>0 => x∈argmax_y v_iy/p_y.    (MBB)

余下每列至少一个正v、每budget正，因此均衡price p_x>0。正估值项上

    argmax_x v_ix/p_x = argmin_{x:v_ix>0} p_x/v_ix.

### Fisher → public NE

直接输出public贡献矩阵X和总分布δ=p。两项money守恒给每行budget和每列总量；MBB条件恰好是critical-support条件。因此X是weighted Leontief NE。又sum_xδ_x=sum_i b_i=1。

如需区分两套utility，设private Fisher utility A_i=sum_xv_ix y_ix；MBB时A_i=b_i*max_x(v_ix/p_x)，所以

    public U_i(p)=1/max_x(v_ix/p_x)=b_i/A_i.

这里出现b_i/A_i，而不是把A_i误当public U_i。

### public NE → Fisher

由第2节每个正budget agent的public U_i>0。若某project x有正v_ix，则δ_x>=v_ix U_i>0，所以保留project的price p_x:=δ_x均正。定义private allocations y_ix=X_ix/δ_x。

列和sum_i y_ix=1，buyer支出sum_x p_xy_ix=b_i；public critical-support正好给MBB，因此每buyer的private线性bundle最优，市场清算。故(y,p)是linear Fisher equilibrium。

**Theorem NE-FISHER-TRANSFER-v1**：上述映射是spending-matrix层面的双向等价，完全保留agent数、project数、非零估值pattern和原budgets；其计算是有理数乘除，没有agent cloning，没有扩大budget分母。

### 最小加权2×2 exact example

取b=(1/3,2/3)，v_1=(1,0)，v_2=(1,1)。linear Fisher有prices p=(1/2,1/2)，goods allocations λ_1=(2/3,0)、λ_2=(1/3,1)。两列各卖1单位，buyer1只买其唯一正价值good，buyer2对两good的bang-per-buck相同。

映射后的实际public策略为

    X_1=(1/3,0),  X_2=(1/6,1/2),  δ=(1/2,1/2).

每行恰好花完原budget；第一人只有project1 critical，第二人两项都critical，因此是NE。private utilities是A=(2/3,4/3)，public Leontief utilities是U=(1/2,1/2)，逐项满足U_i=b_i/A_i。这不是把private allocation λ直接误当public策略；正确策略是p⊙λ。

## 4. Orlin2010 的实际模型合同及有理输入转换

Primary：[Improved Algorithms for Computing Fisher’s Market Clearing Prices, Dagstuhl2010作者PDF](https://drops.dagstuhl.de/storage/16dagstuhl-seminar-proceedings/dsp-vol10171/DagSemProc.10171.2/DagSemProc.10171.2.pdf)。其§1.1直接把x_ij定义成**money spending**，不是goods fractions；列backorder为-p_j+sum_i x_ij。四项optimality条件正是第3节四条，且只要求每行、列至少一项正utility，允许其余utility为0。其强多项式版本返回精确market equilibrium；算法的optimality test/BasicSolution是有理线性系统，非只输出ε近似。

原文用整数budgets e_i和整数utilities U_ix。对本任务有理输入：

1. 令Q_b为所有b_i分母的乘积，e_i=Q_b b_i为正整数。
2. 令Q_v为所有v_ix分母的乘积，U_ix=Q_v v_ix为非负整数。
3. 调用Orlin的**强多项式版本**，取得(P,Z)；输出δ=P/Q_b，X=Z/Q_b。

全局utility倍乘Q_v不改变MBB；budget全局倍乘Q_b只把prices与money spending倍乘，故恢复后精确满足原输入。也可逐行清utility分母，因为buyer内正倍乘不改变偏好。

logQ_b、logQ_v至多为输入各分母位长之和；所有整数化数据总位长仍是输入多项式，不展开成Q_b个agent。Orlin的强多项式arithmetical-operation保证及有理运算位长保证给二进制多项式算法。不得误用其早期依赖e_max数值的弱版本来声称本结论。

**输出合同**：算法返回每个X_ix的精确有理数实际策略，不只是δ、效用值、limit point或ε-NE。原输入若含被删零budget agent/全零列，补零行列即可。

**结果身份**：该Theorem的algorithmic conclusion是已知linear-Fisher算法的直接转移；即使公开母论文§8仍列open，也不构成我们独占的新算法技术。

## 5. 原weak-optimization框架：只保留四项已核义务

该route没有发现致命问题，但第3–4节直接转移已不需要它；因此不继续实现ellipsoid或写成第二份算法稿。已核的四项是：

1. **weighted-log等价与范围**。把每行v归一化为和1后，max sum_i b_i logu_i、δ simplex、δ_x>=v_ixu_i与weighted NE等价。KKT中λ>=0、sum_iλ_ix=1，sum_xλ_ixv_ix=b_i/u_i，得到b_i<=u_i<=1。原文2305.10286v3 §4.3/B.2已经覆盖weighted等价。

2. **显式polybit分母界**。固定正确critical sets，仅用于存在性证明；变量(u,δ,X)的有界LP加入critical等式、support、row b、column δ和0..1 bounds。所有可行点给NE，严格凹目标使u一致，故任意BFS的u都是u*。令d0=n+m+nm、Q为归一化后所有v,b分母乘积，则D=(d0 Q)^d0是Hadamard/Cramer给出的统一分母上界；logD是输入多项式。无需枚举critical sets来计算D。

3. **弱优化oracle与几何合同**。a=b_min/(2m)，限制a<=u<=1不排除最优；消去δ_m后的K有显式内点u_i=3/(4m)、δ_x=1/m，可取r=1/[16m(n+m)]、R=n+m。f=-sum b_i logu_i在K上gradient精确有理、norm<=1/a，函数值可用argument reduction+log级数近似到任意η，时间poly(input bits,log1/η)。有限精度有理ellipsoid可用exact线性separation与精确gradient cuts，近似函数值只用于挑选最好可行query；复杂度依赖log1/a、log1/ε。必须调用其polybit截断实现，不能只写real arithmetic。尤其不需要精确比较大分母加权product。

4. **坐标精确恢复**。f在u坐标的Hessian至少b_min I；取ε=b_min/(100D^4)，objective-gap ε给||û-u*||₂<=sqrt(1/50)/D²<1/(3D²)。因此continued fractions唯一恢复分母<=D的每个u_i*。随后δ_x=max_i v_ixu_i*且sumδ=1（否则全体u可同比放大）；critical pair精确比较后做row-b/column-δ的有理flow给actual profile。log1/ε为polybit，不能使用运行时间poly(1/ε)的算法。

这四项可作一般“有理最优坐标+曲率+弱优化→精确恢复”的教材接口，但在此实例上已被直接Fisher转移替代，没有独立新算法差额。

## 6. 覆盖审计与原文叙述中不能直接继承的一步

- **2509.08767v3** §§5,8：已完整读本任务相关内容。§8 Thm8.3只给cloning伪多项式，随后确实把weighted Leontief polynomial列作open；§5有固定critical LP的rationality地基，但没有把本任务weighted算法明写出来。
- **2305.10286v3** §4.3：原文已经明确positive rational contributions/valuations下有理性与weighted-log等价；§4.4 Proposition1对非均匀budgets给public Leontief NE iff Lindahl。该部分没有把我们的spending矩阵等价直接表述成linear Fisher算法。
- **2511.04572v1/v2** Tao–Zheng2025（v2 2025-12-04），已核§3 Theorem2及其前dual-utility例子：Leontief的dual utility是(1/B_i)sum_j a_ij x_ij（linear），并交换public allocations与Fisher prices。其Assumption1为continuous、non-decreasing、locally nonsatiated、quasi-concave；本文非空support的Leontief效用满足全部条件，预算按正值预处理；§5.1 Thm5后还直接指出Leontief Lindahl PRD等于linear Fisher PRD。因此“public Leontief↔linear Fisher”的跨模型接口已有更一般primary定理覆盖；结合上一条Prop1与Orlin2010，精确weighted算法是直接推论。2026 STOC官方目录列有该文。
- **Orlin2010** §1.1的spending合同与第3节完全逐式相同；这是更短的algorithmic coverage证据。

根部weak框架不应照抄2509.08767v3 Thm5.3证明末段“由u/δ的有限有理位长，几何平均objective也具有该有理编码长度，故binary search有限命中”的论证。例如两agent各budget1/2，v1=(1,0)、v2=(2,2)，NE为δ=(1/2,1/2)，真实utilities=(1/2,1/4)，几何平均是1/(2sqrt2)，无有理二进制编码。这个例子只指出该末段表述不支持所声称的终止推理，不否定其结果；结果可以由第3–4节既有Fisher算法直接得到。本文的坐标强凹恢复完全避开该问题。

## 7. 来源（全为primary）

1. Becker–Fries–Greger–Segal-Halevi, [Efficiently Computing Equilibria in Budget-Aggregation Games, 2509.08767v3](https://arxiv.org/html/2509.08767v3), §§5,8。
2. Brandt–Greger–Segal-Halevi–Suksompong, [Coordinating Charitable Donations with Leontief Preferences, 2305.10286v3](https://arxiv.org/html/2305.10286v3), §4.3、Theorem1/B.2、§4.4 Proposition1。
3. Orlin, [Improved Algorithms for Computing Fisher’s Market Clearing Prices](https://drops.dagstuhl.de/storage/16dagstuhl-seminar-proceedings/dsp-vol10171/DagSemProc.10171.2/DagSemProc.10171.2.pdf), 2010，§1.1、§2 BasicSolution与强多项式版本。
4. Tao–Zheng, [Fisher Meets Lindahl: A Unified Duality Framework for Market Equilibrium, 2511.04572v2](https://arxiv.org/html/2511.04572v2), §3 Theorem2及前文Leontief dual例子、§5.1 Theorem5后；[STOC26官方目录](https://acm-stoc.org/stoc2026/toc.html)。
5. Vazirani, [Rational Convex Programs, Their Feasibility, and the Arrow-Debreu Nash Bargaining Game, 1010.4280](https://arxiv.org/pdf/1010.4280), §§1,2（仅作弱优化/rational convex program标准背景）。
6. Grötschel–Lovász–Schrijver, [Geometric Algorithms and Combinatorial Optimization](https://link.springer.com/book/10.1007/978-3-642-97881-4)；Dadush–Hojny–Huiberts–Weltge, [A simple method for convex optimization in the oracle model](https://link.springer.com/article/10.1007/s10107-023-02005-8), 2024 §1（引用的是ellipsoid标准界的回顾，不是该文新算法）。


## 独立来源核查：完整覆盖链与阅读边界


日期：2026-10-20。任务限于primary来源、版本和覆盖核查；不在这里另证明算法或新开候选。根部已决定：**NA02“加权Leontief预算聚合博弈exact bit-polynomial NE新算法”主目标淘汰，回收为已有Fisher/Lindahl理论的直接应用与查重案例。**

## 1. 结论与精确身份

Becker–Fries–Greger–Segal-Halevi arXiv2509.08767v3 §8确实把weighted Leontief的普通polynomial computation列为开放问题；其2026年AAMAS正式版也仍保留同一问题。因此来源A身份没有误读。

但仅凭该文仍称open不足以作为新颖性证据。Tao–Zheng2025的统一Fisher/Lindahl对偶框架已经直接包含**public Leontief ↔ private linear Fisher**，允许任意正预算。结合Brandt等2025的“public Leontief NE distribution iff Lindahl equilibrium”，再调用Orlin2010的linear Fisher exact/strongly-polynomial算法，即覆盖当前候选的目标。

本轮独立发现的same-matrix Fisher归约是这条既有框架的特例。不要把“根部与fair组重新推导出来”“2026作者仍列open”包装成2026新突破。下文把每个source接口与阅读边界列全。

## 2. Source P1：原A问题没有误读，但版本内没有weighted bit-poly定理

**论文。** Patrick Becker, Alexander Fries, Matthias Greger, Erel Segal-Halevi, *Efficiently Computing Equilibria in Budget-Aggregation Games*。

- arXiv: https://arxiv.org/abs/2509.08767 ；最早2025-09-10，最新v3为2026-02-24。
- 精确全文： https://arxiv.org/html/2509.08767v3 。
- 正式版：AAMAS2026，2026-05-25至29，10页，DOI10.65109/CCMB1463；官方PDF https://www.ifaamas.org/Proceedings/aamas2026/pdfs/CCMB1463.pdf 。

**已核原文。** §8 Definition8.1把rational agent weights w_i=q_i/D克隆为D个equal-share agents；Lemma8.2传回NE；Theorem8.3的运行时间poly(m,D)，明确仅pseudo-polynomial。§8末段随后问weighted游戏是否可在polynomial而非pseudo-polynomial时间计算NE，特别点名Leontief。

正式AAMAS版§8亦如此：printed p1311 / PDF第8页，Theorem8.3与最后一段仍是pseudo-poly和weighted poly开放问题。不是仅arXiv过期、正式版已更正。

**普通poly与strongly-poly的措辞边界。** 该问题原句使用polynomial in n,m并对照cloning的D，没有“strongly polynomial”一词。该文§5的equal-share多项式定理依赖输入binary encoding/valuation大小，不是先给一般weighted bit-poly后再追strong-poly。因此把其理解为“消除对数值D的伪多项式依赖”有上下文依据。正式写目标时仍应自行明确复杂度poly(n,m,L)，L是全部rational input位长；不能把原文略写n,m冒充其已完整规定所有bit-model细节。

**已存在的工具。** §5 Lemma5.4给equal-share下rational/polybit equilibrium表示，Lemma5.5引用Kamal Jain2007 Theorem13的exact convex oracle工具；其运用场景和幂乘积oracle是unweighted。没有在v3中找到一般weighted exact bit-poly theorem。

## 3. Source P2：Brandt2025提供NE↔Lindahl和weighted NSW，不提供一般weighted exact-poly算法

**论文。** Felix Brandt, Matthias Greger, Erel Segal-Halevi, Warut Suksompong, *Coordinating Charitable Donations with Leontief Preferences*，JET230:106096(2025)，DOI10.1016/j.jet.2025.106096。

- arXiv首次2023-05-17，v4为2025-10-10： https://arxiv.org/html/2305.10286v4 。
- 作者55页journal PDF： https://pub.dss.in.tum.de/brandt-research/balanced_journal.pdf 。

**对象完全对齐。** §3每agent有任意贡献C_i≥0，public utility u_i(δ)=min_{j:v_ij>0}δ_j/v_ij；profile逐agent行和C_i、总分配δ为列和，和当前weighted budget aggregation模型相同（总预算可归一）。

**三个已知接口。**

1. §4.3 Theorem1：唯一equilibrium distribution等于weighted Nash welfare ∑_i C_i logu_i的最大化分配。因此“用weighted log convex program刻画NE/唯一δ”本身已经已知。
2. §4.3紧接定理的计算讨论：rational valuations/contributions给rational optimal distribution；给定critical sets可用LP求它。该段把Becker2025后续描述为pseudo-polynomial，只有identical contributions时binary-input polynomial。作者PDF printed p12亦同。不要把摘要“efficient”理解为exact bit-poly。
3. §4.4 Proposition1：对于Leontief utility，collective equilibrium distribution iff Lindahl equilibrium；允许non-uniform budgets。此为接入P3的关键已知桥梁。

**名词防混。** §7的“binary weights”指utility coefficients v_ij∈{0,1}，不是“agent预算用二进制编码”或一般rational预算；其LP算法已覆盖该受限偏好类，不能当作新的weighted-bit结果。

**近期slides的误导风险。** 作者slides https://pub.dss.in.tum.de/brandt-research/donor_slides.pdf ，PDF第33页笼统写Becker2026的rational/poly computation，没有在该页加equal-contribution限定。该页没有新算法证明或新的exactweighted theorem，且P1正式2026论文仍写weighted pseudo-poly。故不能凭slides的宽泛一句认定generalweighted被单篇P1直接解了；最终coverage来自下述P3链。

## 4. Source P3：决定性的2025已有public Leontief / private linear Fisher对偶

**论文。** Yixin Tao, Weiqiang Zheng, *Fisher Meets Lindahl: A Unified Duality Framework for Market Equilibrium*。

- arXiv2511.04572，首次2025-11-06，v2为2025-12-04，均早于本次2026-10-20截止日。
- 精确全文： https://arxiv.org/html/2511.04572v2 （无版本URL https://arxiv.org/html/2511.04572 当前亦为v2）。
- 摘要与版本： https://arxiv.org/abs/2511.04572 。

### 4.1 模型和假设

§2.1定义private Fisher每good unit supply，各agent任意B_i>0；public Lindahl也任意B_i>0、unit production costs。Assumption1为utility continuous、non-decreasing、locally nonsatiated、quasi-concave。每行至少一个正v_ij的Leontief满足这组条件；零预算agent可移除，零val所有good可移除（退化处理由根部主稿详述）。

### 4.2 确切utility变换，系数不是倒数

§3“Indirect Utility Function”中，Theorem1后、Example1前，原文明确同时写两方向：

- 线性utility Σ_j a_ij x_j的dual utility为(1/B_i)min_j{x_j/a_ij}；
- 反方向，Leontief utility min_j{x_j/a_ij}的dual utility为(1/B_i)Σ_j a_ij x_j。

并明确指出按agent正比例缩放utility不影响private/public equilibrium。因此当前public Leontief系数v_ij对应**同矩阵v_ij**的private LINEAR Fisher偏好；(1/B_i)只是可忽略的agent-wise正比例。不能误接到private Leontief Fisher（后者可能irrational）。

### 4.3 Theorem2直接给预算保留、allocation/price交换

§3 Theorem2 “Duality between Lindahl Equilibrium and Fisher Market Equilibrium”对同一agents、goods、budgets的dual market建立iff：public allocation x变成private Fisher equilibrium price向量；public personalized Lindahl prices变成private Fisher personalized allocations。§3 Remark1还给反方向。

这与fair组/root的独立映射一致：设private Fisher quantity allocation为λ_ij、price为p_j，则public collective distribution δ_j=p_j，public individual spending X_ij=p_j λ_ij。private MBB条件v_ij/p_j最大，正对应public critical p_j/v_ij最小。此处只是把已知定理和当前记号对接，不以该公式主张新归约。

**阅读范围。** 已读§2假设、§3两方向utility公式、Theorem2完整statement和主证明、§4.1例子的CES接口，以及对应Brandt引用。本轮没有审完全51页所有dynamics/chores应用；本coverage不依赖那些部分。§1.1 warmup主要写public LINEAR↔private LEONTIEF，若只读warmup容易看反；真正覆盖当前题的是§3明确反方向公式+Theorem2。

## 5. Source P4：linear Fisher的exact/strongly-polynomial算法早已存在

James B. Orlin, *Improved Algorithms for Computing Fisher's Market Clearing Prices*, STOC2010,pp291–300,DOI10.1145/1806689.1806731。

- MIT作者final manuscript入口： https://dspace.mit.edu/entities/publication/aeca65f4-08b6-4649-8a19-e123eda7614c 。
- 可读19页primary全文： https://drops.dagstuhl.de/storage/16dagstuhl-seminar-proceedings/dsp-vol10171/DagSemProc.10171.2/DagSemProc.10171.2.pdf （2010-04-27版本）。

§1.1直接用money-spending变量x_ij定义solution；cash约束逐buyer行和e_i，allocation约束逐good列和p_j，正spending只走U_ij/p_j最大的equality edges。这三个条件本身就与当前public Leontief NE的row-budget/column-total/critical-edge描述相同。算法求actual market equilibrium，不是只求近似价格。

其abstract/§1给linear Fisher第一个strongly-polynomial算法；复杂度O(N^4 logN)（N=buyers+goods，文中另有稀疏改进）。文中模型先用integral budgets/utilities。当前rational输入可通过公共预算缩放及逐agent正比例utility缩放清分母，输入位长增长为多项式；具体strongly-poly算术模型表述及恢复profile的bit细节由根部归约稿负责，不在本来源核查中重复证明。至少exact ordinary bit-polynomial覆盖已经足以淘汰当前“新算法”主目标。

## 6. 三篇决定性source的拼接，不是凭摘要宣布覆盖

| 当前目标步骤 | 已知primary接口 | 是否需本轮新工具 |
|---|---|---|
| weighted public Leontief NE的collective distribution | Brandt2025 §4.4 Proposition1等于Lindahl equilibrium | 否 |
| same budgets、same v变到private LINEAR Fisher | Tao–Zheng2025 §3utility公式+Theorem2 | 否 |
| exact求Fisher prices和spending/allocation | Orlin2010 §1.1与strongly-poly algorithm | 否 |
| 从Fisher回到public profile | Tao–Zheng的price/allocation交换；P2 critical/decomposition接口 | 记号/退化核验需要写清，但不构成新算法设计 |

因此，P1的weighted问题虽然文字上仍被称作open，具体Leontief情形已落入2025公开对偶框架和2010算法的直接组合。**不能用“2026论文仍写open”压过另一篇已公开primary定理的覆盖。** 是否作者之间存在引用遗漏或问题措辞未同步，不在本任务中推断；只陈述source内容与数学接口。

## 7. Jiang / Jain / Vazirani备线：只保留机制去重，不继续长查

按照root最新指令，Fisher覆盖已足够，以下只记录已读证据，不另开候选、不继续长查。

- Haotian Jiang, *Minimizing Convex Functions with Rational Minimizers*, arXiv2007.01445v5（2022-09-20，初稿2020；SODA2021后journal版），https://arxiv.org/pdf/2007.01445 。已读Definition1.1、Theorem1.6及Definitions2.6–2.7：oracle必须对任意查询返回最优“YES”或严格分离所有minimizers的非零向量；minimizer集合需为bounded rational polyhedron且LCM vertex complexity有界。可用它或其追溯的GLS理论做exact-convex优化，**不是新工具**；domain扩展、total oracle、bit复杂度仍需核验，不应只凭“unique rational optimum”五字调用。
- Vijay V. Vazirani2012, *The Notion of a Rational Convex Program, and an Algorithm for the Arrow-Debreu Nash Bargaining Game*, JACM59(2):7，https://ics.uci.edu/~vazirani/NBalg.pdf 。已读§1、§2：RCP定义就要求rational最优解有polybit表示；logarithmic线性约束convex program并不自动rational，必须逐模型建立。其主算法对象ADNB不是当前public donor游戏。故weighted NSW+exactconvex恢复属于既有范式，不能宣称发明了新的理性恢复方法。
- Kamal Jain2007, *A Polynomial Time Algorithm for Computing an Arrow–Debreu Market Equilibrium for Linear Utilities*, SICOMP37(1):303–318，DOI10.1137/S0097539705447384。publisher只读到摘要，原Theorem13通过P1的Lemma5.5精确转述核查；不要说本轮已审其原Theorem13完整证明。

## 8. 搜索边界与最终处置

本轮使用两套搜索引擎，对weighted Leontief / weighted budget-aggregation / donor coordination exact polynomial / Nash welfare rational convex / public-private Fisher Lindahl duality做定向检索。初步仅看到P1/P2的pseudo-poly描述，**随后因改变接口关键词找到P3决定性覆盖并修正结论**；保留这个历程是为了避免把早期“没搜到”当成仍open。

最终：NA02作为“首次weighted Leontief exact bit-poly NE算法”淘汰。可以保留一份清楚的Fisher归约、独立审查和原cloning补齐记录，作为学习资产和防重复成果；不把它重新包装成新工具、新公开问题解决或强多项式突破。具体新的研究主目标不在本来源义务范围内。
