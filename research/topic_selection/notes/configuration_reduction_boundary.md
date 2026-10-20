# GBAP/SAP配置次模归约：可审查初稿与复杂度边界

状态：归约本身已在CGST2011 §4.2中出现，不是新idea。非均匀全局knapsack与隐式pricing的完整算法边界仍需第二轮独立审查。严禁从此稿直接宣布“一般GBAP新获1−1/e”。

## 1. 定义与精确等价

items为P，bins为L。bin l的局部可行集合族I_l⊆2^P下闭，assignmentprofit v_lp≥0，openingcost c_l≥0，globalbudgetB。GBAP的intervalcapacities只是I_l的一种具体来源。

取配置地集E={(l,S):S∈I_l}。对配置集合A⊆E定义

g(A)=Σ_{p∈P} max({v_lp:(l,S)∈A,p∈S}∪{0})。

限制每个bin至多取一个配置，并满足Σ_{(l,S)∈A}c_l≤B。g是单调次模，因为每个item贡献都是“当前已见最高值”，边际只会下降。一个可行assignment直接映到配置集合，目标不变；反方向，把在多个配置中出现的item只保留到v_lp最大的bin。局部集合下闭，删除冲突copies不破坏可行性，保留利润恰为g(A)。所以两个整数最优值相同。

等cost情况下，globalbudget变成|A|≤k；每bin≤1加总数≤k是partitionmatroid的truncation。更一般，若openbin集合受任意matroidM约束，把同一bin的configurations视为parallelcopies，得到一个matroid。CGST2011 Theorem1.3、§4.2已经明确做了这件事；不能把它作为新近似结果。

## 2. Exponential ground set不是免费

|E|可能为L·2^P。不能把显式地集上的O(|E|poly(P))算法写成对原输入的多项式时间。要说明：

1. 构造/访问I_l：membership不等于optimization；黑箱membership可使最大权可行集合不可近似。
2. pricing：对每个bin和任意非负weights w_p，求max_{S∈I_l}Σ_{p∈S}w_p。若只有αapproximation，算法保证必须保留α。
3. fractionalpoint如何稀疏表示，所需configurations多少，如何得到它。
4. multilinearextension与梯度是否在稀疏support上可计算，采样误差如何影响界。
5. rounding是否可在support上执行；非均匀knapsack不能直接调用matroidpipage并假设budget总成立。

CGST2011 Theorem4.1明确：若每bin有αapproximateweightedpricing，则SAP的continuousgreedy比值为1−e^(−α)−o(1)。其§4.2显示梯度所需weights并非一个难的次模单bin问题，而仍是modularweights的局部packing。

## 3. 梯度的可分解形式

设z在配置地集上，Q~independent(z)，M_p(Q)=max({v_kp:(k,T)∈Q,p∈T}∪{0})。对配置e=(l,S)，在不采样e的背景下

∂_e G(z)=Σ_{p∈S} E[(v_lp−M_p(Q\{e}))_+]。

对于同一bin，背景分布细节必须处理：如果用最标准独立配置multilinearextension，去掉e后背景依赖e，不能无条件把所有该bin配置的coefficients当成相同weights。CGST正文的structuredsparseprocess给了合法实现；简单说“一次pricing就算所有梯度”若未处理此依赖有漏洞。可用binexclusive的抽样extension/对坐标为零的新configuration的directionoracle，也可按正文机制构建实现，但需要写全。

## 4. 给定configurationLP支持时的直接rounding基线

考虑P03 Eq.(1.4)的一个稀疏fractionalsolutionx。满足每bin配置和≤1，每item总marginal≤1，及openingbudget约束。LP目标L(x)=Σ_{l,S}x_lS Σ_{p∈S}v_lp。

若暂且对所有配置独立采样，每个item的“bestcoveredvalue”的期望≥(1−1/e)Σ_{l,S:p∈S}v_lp x_lS。这可用layer-cake证明：对阈值t，令q_t=Σ_{l,S:p∈S,v_lp≥t}x_lS≤1；至少一个qualifiedconfiguration被采样概率=1−Π(1−x_lS)≥1−e^(−q_t)≥(1−1/e)q_t。对t积分并对p求和，得G(x)≥(1−1/e)L(x)。

若openingcost相等，x在上述truncatedpartitionmatroidpolytope中；matroidpipage/swaprounding可给feasibleA且E[g(A)]≥G(x)。这形成从**给定LP支持**到可行解的1−1/erounding，无需重新continuousgreedy。这是旧工具的直接后果，实用baseline有用，理论novelty不足。

如果c_l任意，matroidpipage方向可能改变总openingcost。若只用cost-preserving方向，partition约束可能阻止移动；若最后简单扔掉超预算config，loss可能很大。一般matroid+knapsack次模算法可能通过guessing大贡献元素、enumeration、contentionresolution得到更强保证，但隐式地集的guessing/pricing是否仍可实现要单独证明，不能自动当作免费。

## 5. 交通intervalcapacity的localoracle

P03中每bin的resourcevectors是binaryconsecutiveones，capacity可随位置变化。固定bin、modularprofit，maxweightfeasibleitemset是intervalpacking、整数capacity下可用networkflow/TU实现；若capacity是rational而每itemconsume0/1，integerselection可把capacity取floor。必须核实端点约定、空vector、capacity编码与flow网络规模。这里localoracle有希望是exactpolytime；若再允许item的nonunitdemands、多次占用或非intervalsupports，就不能继续不加证明地用这个oracle。

## 6. 最新去重门槛

Ganz Rozenman–Kulik–Schwartz–Singh 2026, arXiv2605.03071 Theorem1.5：SAP在localαpricing耗时p(n,α)时，(1−ε)(1−e^(−α))approximation，时间Õ((n/ε+p(n,α))m)。因此泛泛提“用Poisson/少抽样让SAP变快”已过期。该theorem是plainSAP；外层非均匀openingbudget、matroidactivation、不确定需求不能擅自并入其statement。

## 7. 第二轮真正该攻击的问题

- 非均匀budget下，能否仅在给定LP的polynomialsupport上完成简单coupling，并把alwaysfeasible与itembestcopyprofit关联起来？
- 相比通用matroid+knapsack方法，速度/结构/运行参数能否明确改善？
- Algorithm1的“先独立configs、再按密度截断、最后bestcopies”损失是否真的达到1/8，最小tightinstance是什么？
- 若允许approximatepricing或样本oracle，哪一层损失应是α(1−1/e)，哪一层能变成1−e^(−α)？不能混用两种分析。

若这些问题都由现成通用定理覆盖，就把C06淘汰；该归约应保留作选题去重案例。

## 第二轮：稀疏支持的确定性预算基线

# C06-v2：给定稀疏配置LP时的简单0.316基线

日期2026-10-20。状态：自足证明草稿，基于旧配置覆盖归约与旧pipage原理的直接组合；不宣称新颖。用于淘汰“把GBAP特定算法1/8提高成某普通常数”这类伪新题。

## 假设、对象、输出

每bin l有下闭配置族 I_l，每物品在bin利润v_li≥0，openingcost 0≤c_l≤B。输入给定有限稀疏配置支持E={(l,S)}及有理数x_e≥0，满足

∑_{e:bin(e)=l}x_e≤1；∑_{e:i∈S_e}x_e≤1；∑_e c_{bin(e)}x_e≤B。

定义LP值L=∑_e x_e ∑_{i∈S_e}v_{li}。目标是每次满足budget和局部packing的可行指派，保证利润≥(1−1/e)L/2。仅用输入配置支持，不需要重新pricing，也不需要假装指数地集已显式列出。若存在c_l>B的bin，必须事前移除；否则LP可给不可打开bin正分数，任何正比例舍入都不成立。

## 配置覆盖与初始值

g(A)=∑_i max({v_li:e=(l,S)∈A,i∈S}∪{0})，是非负归一单调子模函数。记G其标准独立采样multilinear extension。

对item i及阈值t，q_it=∑_{e:i∈S_e,v_li≥t}x_e≤1，覆盖阈值概率1−∏_e(1−x_e)≥1−e^{−q_it}≥(1−1/e)q_it。对t积分并求和即得G(x)≥(1−1/e)L。

## 阶段一：同bin配置交换

若bin有两个正坐标x_e,x_f，则沿d=1_e−1_f保持该bin总和及成本不变。取保持坐标非负的最大可行线段；因该bin总和≤1，坐标上界1自动保持。子模性给∂²_{ef}G≤0，因此G(x+td)沿t为凸函数；至少一个端点不减G。选择该端点。每一步至少一个正坐标归零，O(|E|)步后每bin只剩至多一个配置。

此时可以删除已归零配置，每bin剩一个variable q_l∈[0,1]。不需要继续保持每item LP边际约束：这些约束只用于初始G(x)下界，最终冲突由max-coverage/delete处理。

## 阶段二：保持openingcost交换

先把零成本bin剩余变量提高到1，G不减。若有两个分数变量q_l,q_k，成本均正，沿d=(1/c_l)1_l−(1/c_k)1_k交换。总成本保持，变量区间[0,1]保持，G沿此异号方向仍凸。选不减值的端点，每步至少一个fractional变量变成0或1。

至多O(|E|)步后，有整数配置集A及至多一件fractional配置e，参数q∈(0,1)。A本身budget可行；{e}因c_e≤B也budget可行。此时

G(z)=(1−q)g(A)+qg(A∪{e})≤g(A)+qg({e})≤g(A)+g({e})。

返回A与{e}中g较大者，值≥G(z)/2≥G(x)/2≥(1−1/e)L/2≈0.3160602794L。无fractional配置则直接返回A，无1/2损失。

每个被多个配置覆盖的item只保留在利润最大的bin，其余配置中删除。下闭性保证局部可行；目标恰为g，openingcost不增加，且每bin至多一个配置。

## 可实现性

G可精确有理计算：逐item按正利润阈值排序，积分各层1−∏(1−x_e)，输入支持为K时多项式时间，朴素O(nK logK)每次目标评估足够。O(K)次交换，每次算两端点。没有MonteCarlo误差、exponential pricing或未说明的oracle。

有理数交换端点通过比值及线性运算得到。阶段一端点只是合并/清零；阶段二保持成本后端点为0/1或有理残余成本除c。位长可按有限K次有理运算的多项式上界控制。

## 对候选的影响

这不证明GBAP最优比值是0.316，也不证明新算法无人写过；恰好相反，目标是把现成可推出基线写透。原C06若只是“任意非均匀openingcost上从1/8改进”即不足立题。要留下，必须超越这个基线并比较1−1/e−ε的通用matroid+knapsack方法，或者用明确复杂度/数据访问模型提出新差额。

Primary去重：CGST2011《Maximizing a Monotone Submodular Function Subject to a Matroid Constraint》§4.2已给配置覆盖SAP归约；Sarpatwar–Schieber–Shachnai《Constrained Submodular Maximization via Greedy Local Search》arXiv:1705.06319v3（2018）给matroid+knapsack的(1−e^{-2})/2近似，且引言说明1−1/e−ε通用方法早已存在但有大枚举指数。后者对**显式支持上的整数最优**适用，不能不经额外gap论证冒充对配置LP值L的0.432保证。
