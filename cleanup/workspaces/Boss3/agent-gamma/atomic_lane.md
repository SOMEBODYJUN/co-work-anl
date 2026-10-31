> 这是第一轮原文卡与推导记录；后续裁决以 [BATTLE](../BATTLE.md) 和 [候选池](../candidate_pool.json) 为准。全库来源统一为 A=作者明确原题、B=作者明确建议方向、C=团队派生；本稿局部使用的分级符号不得当作统一来源标签。

> 第二轮已发现允许类型缩放的全人数 64/59 证书，故 37/33 不能作为新最好上界出售；固定 {1,3} 的 curl 条件也由 Harks–Klimm–Möhring 2011 Prop.3.4 直接覆盖。严密说明随后并入同一工具资产，未宣称新颖。

# boss37 重新选题：原子拥塞博弈线（2026-10-20）

## 0. 结论与诚信边界

已按新指导重新选题，不再围绕一般 R||Cmax 的统一 2−ε 不可能性。这里给出 **14 个有不同数学对象/核心工具的候选**，其中 4 个应淘汰或仅当背景，3 个值得根部投入查重/证明。8 篇以上一手论文已实际打开；部分论文只有原文摘要可读，下面明确区分。所有“自己的延伸”均不是已经核实的新开放问题。网页检索覆盖至 2026-10-20，但“没有搜到”绝不等于“未被解决”。

最值得先攻的是：**在有限权重类型下自动合成离散资源势，并把数值最优解转成有理证书和解析定理**。已完成一个可独立检查的小定理：权重只有 1/2、每种至多两名玩家、任意策略集合、任意非负二次多项式延迟，存在 **37/33-近似势**，因此任意严格 37/33 改善序列终止。这个因子仅在“真实权重作为玩家缩放系数”的边际夹逼模板中证明最优；不是此类博弈最好的 NE 存在阈值，不是所有近似势最优。尚未完成针对有限类型文献的完整查重。

最危险的误判：

1. 二次延迟的一般存在界早已是 **4/3**，不是只知道 d=2；Hansknecht–Klimm–Skopalik 2014 Thm14，Caragiannis–Fanelli 2021 Thm2 都有。
2. 两玩家二次延迟的存在阈值早有 tight 数值约 **1.054**（2014 Thm16）；不能把37/33叫做两玩家突破。
3. 不同 Lp 聚合在 matroid 中存在 NE，强单调/共同局部排序的框架早在 FLS2017 Thm9、Cor13；2024 Takazawa 又覆盖 weighted/set-functional aggregation。简单“把Lp加权”不够新。
4. 有限优先级延迟老开放题已被 Takazawa arXiv:2407.12300/TCS2026 解决。
5. CGGPW MOR2023 的搜索摘要常丢掉 √ 符号。原始 arXiv:2002.07466 Thm1 下界是 Ω(√d/ln d)，不是 Ω(d/ln d)。

## 1. 一手阅读证据：先给文章定性，再提想法

以下每篇的定位、工具和玩具模型均是研究者归纳；定理事实对应列出的 section/theorem。

|代号|一手论文、定位与URL|文章类型|工具本质与应先练的玩具模型|
|---|---|---|---|
|P1|Harks–Klimm–Möhring, **Characterizing the Existence of Potential Functions in Weighted Congestion Games**, TCSys2011。原始作者机构预印本摘要及文件入口：https://depositonce.tu-berlin.de/items/e9ae5bcd-e85d-42f2-a01f-3e9bd874a645；DOI https://doi.org/10.1007/s00224-011-9315-x 。正文PDF工具访问失败；只核实原文摘要“全体权重下 exact potentials iff affine；weighted potentials还允许共同指数”。|分类驱动|从二人矩形的混合差分/curl为0推出函数方程。玩具：单资源、两个玩家各选用/不用资源的4个格点。**不能将全体权重分类直接套到固定{1,3}。**|
|P2|Harks–Klimm, **On the Existence of Pure Nash Equilibria in Weighted Congestion Games**, MOR2012，§主结果/原文abstract：https://pubsonline.informs.org/doi/abs/10.1287/moor.1120.0543?journalCode=moor 。原文摘要已打开，正文未读全。|分类驱动|从“每个实例都存在NE”反推成本族只能仿射或共指数；两玩家分类更宽。玩具：同一个四格博弈上比较不同资源的成本形状。|
|P3|Ackermann–Röglin–Vöcking, **Pure Nash equilibria in player-specific and weighted congestion games**, TCS2009：https://doi.org/10.1016/j.tcs.2008.12.035 。作者机构原文摘要：https://cris.maastrichtuniversity.nl/en/publications/pure-nash-equilibria-in-player-specific-and-weighted-congestion-g/ 。matroid存在定理亦由P10 Thm2.3/2.6逐字陈述；原论文全文未成功取到。|结构分类驱动|matroid交换把全球改善压成单元素交换；策略结构的最大性需允许对手策略任意交织。玩具：uniform rank2交换；再删一个base制造交换缺口。weighted BRD已有超多项式且非伪多项式下界，不能贸然宣称收敛快。|
|P4|Caragiannis–Fanelli–Gravin–Skopalik, **Approximate Pure Nash Equilibria in Weighted Congestion Games: Existence, Efficient Computation, and Structure**, TEAC2015。作者全文：https://ngravin.github.io/assets/pdf/TEAC/teac_weighted-full_15.pdf ，§3 Ψ-games、§4/5算法、§6 Open problems。|工具驱动|用可积的对称多项式代理真实载荷幂，恢复potential；另用cost分层控制后续扰动。玩具：两权重a,b的二次幂与完全齐次对称多项式比较。§6明确尝试其他potential代理，以及仅依据原游戏成本的动态。|
|P5|Hansknecht–Klimm–Skopalik, **Approximate Pure Nash Equilibria in Weighted Congestion Games**, APPROX2014，全文：https://drops.dagstuhl.de/storage/00lipics/lipics-vol028-approx-random2014/LIPIcs.APPROX-RANDOM.2014.242/LIPIcs.APPROX-RANDOM.2014.242.pdf 。Thm3/4与12为通用工具，Thm14低次多项式，Thm16两玩家tight表达式。|工具驱动|按不同玩家顺序积累资源边际费用，选极小/极大排列；局部边际误差控制整体改善。玩具：权重1,2一个资源，顺序费用19和17。一般二次4/3、三次约1.785；二人二次tight约1.054。|
|P6|Caragiannis–Fanelli, **On approximate pure Nash equilibria in weighted congestion games with polynomial latencies**, JCSS2021；作者最终版本：https://arxiv.org/pdf/1902.07173 （v5 2020）。Lemma1、Thm2、Cor5、Thm7、§4。|视角+工具驱动|将资源潜能写成总载荷幂与单个权重幂之和；用边际区间把全局动态问题化成单资源不等式。玩具：x²的两项potential。Cor5已有高拥塞 exp(1/τ)近似，§4明确猜测其Lemma1模板一般无法优于d，并提出低于d的PoS等方向。|
|P7|Christodoulou–Gairing–Giannakopoulos–Poças–Waldmann, **Existence and Complexity of Approximate Equilibria in Weighted Congestion Games**, MOR2023。全文：https://arxiv.org/pdf/2002.07466 ，Thm1，Thm3/Cor1，Thm4/5，§7。|问题+组合驱动|先做无均衡小工具，再与电路gadget黑箱拼接，迁移非存在性到复杂性。玩具：一个重玩家和若干等轻玩家诱发环；区分“有向环”与“每个profile均可改善”。一般d存在上界d，下界Ω(√d/ln d)；一般单调成本n上界n，下界Θ(n/ln n)。|
|P8|Giannakopoulos–Poças, **A Unifying Approximate Potential for Weighted Congestion Games**, TCSys2023。作者全文：https://arxiv.org/pdf/2005.10101 （v3 2022）。§2.1 Equivalent Cost Functions、Lemma1、Thm1、Thm2–5。|工具驱动|积分potential加按玩家单重费用的校正；接口输出(均衡近似α,PoS β)。玩具：在有限可达载荷之间改变插值，游戏不变但potential分析改变。§2.1明确说不同等价表示会影响界，正文大多未利用。|
|P9|Feldotto–Leder–Skopalik, **Congestion Games with Mixed Objectives**, JCO2018；作者全文：https://arxiv.org/pdf/1607.05143 。Thm1/3/4、Thm8、§4。|模型+结构分类驱动|sum/max混合把延迟与带宽并列；用matroid greedy共同最优性解释何时存在NE。玩具：两玩家rank2但latency/bottleneck资源排序相反。Thm3已有α统一、线性cost、matroid无NE反例；Thm8共同单调依赖的lazy BRD多项式。|
|P10|Feldotto–Leder–Skopalik, **Congestion Games with Complementarities**, CIAC2017；全文：https://arxiv.org/pdf/1701.07304 。Thm4/5/6，Thm9、11、12、Cor13，§6。|视角+分类驱动|把sum/max换成一般聚合，抓住“一次交换的排序是否依赖上下文”。玩具：长度r向量只换一个坐标；不同Lp的全策略偏好可能冲突而局部排序一致。Thm4/5给 r^[½(1/p−1/q)] 的tight存在阈值；§6仍提出针对结构改进算法/效率分析，但不是允许突破这个一般存在阈值。|
|P11|Takazawa, **Pure Nash Equilibria in Weighted Congestion Games with Complementarities and Beyond**, AAMAS2024；期刊2025题名改为weighted matroid/non-additive aggregation。全文：https://arxiv.org/html/2401.03861v1 。Def3.1/3.2、Thm3.3、Cor3.4/3.5、Thm4.1/4.2。|组合+分类驱动|共同total preorder + matroid simultaneous exchange + lexicographic资源势。玩具：聚合对一个坐标的偏好不随其余r−1坐标而反转。这个工具已吃掉很多看起来新的Lp/weighted推广。|
|P12|Giannakopoulos, **A Smoothed FPTAS for Equilibria in Congestion Games**, EC2024。全文：https://arxiv.org/html/2306.10600v3 。Thm1、Lemma1、§3.2/3.3。|视角驱动|把指数最坏实例放进随机扰动模型；潜能下降时间≤“成本最大/最小比”，再与指数状态数截断结合积分。玩具：E[min(A/min X_i,B)]。定理涵盖unweighted general/polynomial/step/costsharing；不直接覆盖没有exact potential的weighted或heterogeneous聚合。|
|P13|Takazawa, **A unified model of congestion games with priorities: Two-sided markets with ties, finite and non-affine delay functions, and pure Nash equilibria**, TCS2026；全文：https://arxiv.org/pdf/2407.12300 。Table2、Thm4.1/4.4/4.5、Thm6.2–6.7。|组合+模型驱动|把priority旧模型与有限delay模型统一，lexicographic势/优先级分阶段。玩具：三玩家不同资源上优先级形成一个有向环。老“高优先级对低优先级产生有限delay”问题已解决。|

## 2. 候选池：14题battle

标记：O=原文公开方向；E=本次延伸。状态P=支撑旧结果已直接核实；N?=本延伸的新颖性未完整核实。价值采用不同标准：分类题看新类是否严格且自然/必要充分；工具题看是否给可复用证书和新界；算法题看是否真正poly且不偷换oracle；反例题看是否排除自然猜想并有最小性。

|ID/类型|精确问题、量词和来源属性|已知界/状态核查|20天价值与最可能致死障碍|裁决|
|---|---|---|---|---|
|A01 工具|E（由P4§6、P5、P8§2.1启发）：固定有限权重字母表T={1,2}，任意人数、任意strategy systems、非负二次延迟。找最小资源分离势的边际夹逼因子；先证明某个α<4/3对**所有人数**成立，再转有理证书/简洁公式。|P：一般4/3。固定真实w缩放，人口各≤2已精确证37/33；各≤20浮点LP相同。N?：未发现直接写37/33的文献，但不能据此认新。|数值→有理→解析的证据链清楚，OR/优化理论贴合；可以有自足小定理。致死：换type scaling后37/33被轻松支配；或2014特定排列/后续finite-type理论已直接覆盖。|**第一优先查重+全n证明**|
|A02 分类|E（P1/P2）：对允许权重仅{1,q}、任意有限人数与策略，分类哪些整数载荷延迟c使所有游戏存在以真实w缩放的exact potential。先q=3，再任意整数q和一般有限T。|P：全权重仅affine。自行curl推出{1,3}差分式2c(t+3)−3c(t+2)+c(t)=0；通解a+bt+d(−1/2)^t。该非仿射项在b足够大时仍单调。N?未完成查重。|分类题价值在“允许权重的算术结构改变potential谱”，不是改参数数值。致死：已有restricted-weight/semigroup分类；或者只得到一眼可见差分式、推广没有实质。|**第二优先，24h novelty gate**|
|A03 算法|O→E：P10§6提出更贴合Lp结构的算法。对异质Lp聚合、max策略大小r、p_i∈[p,q]，在自然随机成本扰动下，能否在expected poly时间输出β(1+ε)-PNE，β=r^[½(1/p−1/q)]？仅要求达到已知tight存在阈值。|P：β存在且一般tight；P10已有算法但其因子带普通拥塞算法的损失；P12 unweighted普通聚合有smoothed FPTAS。N?最新专门Lp算法未完整查重。|有明确组合工具，且不需突破一般存在屏障；先r2,p1/q2。致死：c→c^z后密度在0附近退化，原smoothed逆最小成本积分不再poly；或已有论文直接组合。|**第三优先，先跑最小模型**|
|A04 视角|E（P12）：把independent扰动改为任意相关、只要求每个成本参数边际density≤φ；保持单调/资源共同因素；是否保留approx BRD smoothed poly？|P：原文独立Lemma1。自行union-bound可去独立，见§5。N?这种extension是否已知未核实。|可作工具附录，可解释“相关噪声保持单调”的模型。致死：核心lemma一页直接推论，独立成文价值低；exact NE的结论不能跟着推。|**仅作A01/A03附属**|
|A05 稳定性/结构|E（P9 Thm1/8）：rank-r matroid混合sum/max，b_e在共同非降d(ℓ_e)的[1,κ]倍内。最小保证α(κ,r)，并给tight rank2反例；进一步只允许k个逆序对。|P：κ1存在；完全错序matroid可无NE。简单近似转移有α≤κ；此上界本身太容易。N? sharpness/逆序数版本未查完。|价值要求“必要充分或tight”的量化共序理论。致死：少量逆序已能编码无界反例；上界只是成本扰动transfer。|备选，须先构造tight模型|
|A06 表示优化|E（P8§2.1）：给定有限reachable loads和成本值，优化所有等价插值/积分校正，以最优(α,β)-PoS曲线输出证书；先3个load值。|P：P8明确等价表示会改变界，正文多数未用；通用框架已有。N?最优表示算法未核实。|优化理论方向自然，有LP/duality落点。致死：与A01高度工具重叠；若只是重写通用marginal LP，缺少新理论。|与A01合并，不另立主项目|
|A07 拓扑|E（P3“忽略策略交织”的最大性启发）：每个资源最多被两玩家使用，定义玩家交互图；对tree/单cycle图、非matroid strategies分类weighted或player-specific游戏何时必有PNE。|P：matroid一般最大性不排除固定交织正结果；player-specific singleton已有NE。N?树图结论尚未文献核实/证明。|价值要求真正打破matroid边界并给图论必要充分。致死：仅一条edge的任意两玩家resource组合就能编码匹配便士；需要严格约束“双方共享资源/动作”的形状。|高风险，先2玩家穷举判死|
|A08 组合结构|E（P3）：每个策略族是两个matroid的共同bases（或由matroid删一个base），是否存在仅依赖exchange defect的常数近似PNE？|P：matroid exact存在；非matroid普遍最大性已知。N?不存在统一近似界的反例未核实。|分类扩展有价值，需要以exchange obstruction刻画界。致死：一个缺失base便可复制任意大改善cycle，尺度放大后无有用界。|不宜先选；先最小反例|
|A09 动态|E（P3/P11）：weighted matroid+monotone aggregation，固定t种weights、rank2、相同cost族时是否有**指定pivot rule**的poly-time/local-exchange算法？|P：一般weighted BRD超多项式且非pseudo-poly；P11只保证有限终止；unweighted P10 Thm12 polynomial。N?下界是否已用2types需优先核实。|若两类型排除硬构造，可出算法。致死：2009下界可能已经2types；lex potential的成本等级有限并不意味着下降长度poly。|有条件备选，严禁数等级即poly|
|A10 效率|O→E（P6§4）：对α低于d的weighted polynomial games的approx PoS，先固定{1,2}二次与A01势结合，推α/PoS tradeoff并给lower examples。|P：一般α≥d的(d+1)/α已知；P8处理若干其他族。N?finite-type sharp曲线未知。|价值看是否有新的实质Pareto点；能给A01另一个卖点。致死：A01边际势的socialcost夹逼很差，不能凭α改善便宣称PoS改善。|A01的第二阶段|
|A11 机制|E（P4 Ψ与costsharing经典）：真实weighted quadratic resource cost不变，允许每个资源给不同weight types加固定budget-balanced转移；最小转移幅度恢复potential/NE，分类可行性。|P：Shapley costsharing等恢复NE已有强大理论，见Gkatzelis/Kollias/Roughgarden：https://www.cs.drexel.edu/~gkatz/cost-sharing.pdf 。N?“最小偏离原收费”的精确优化版本未查完。|价值是最小干预的LP、对偶和具体tight界。致死：既有costsharing characterization直接覆盖；固定type转移不够修复load-dependent curl。|中风险，先读costsharing原文|
|A12 优先级结构|E（P13）：priority-based matroid games允许不同资源排序，限制不一致性为一个feedback vertex/player；求PNE/approx PNE复杂性或FPT算法。|P：P13 Table2已给许多consistent/inconsistent存在结果，且某些player-specific inconsistent也已有NE。N?残余复杂性需对照精确定理。|价值在参数化算法而非再证存在。致死：核心对象已经落在Thm4.5/6.4，或者参数1已NP-hard。|低优先、必须精读再定义|
|A13 开放大题|O：P6§4所猜其Lemma1局部range模板无法一般优于d；证明“模板能力下界”，先只分析某个窄多项式/校正势族。|P：公开conjectural direction；一般二次已4/3不能误读成任何d都不能<d。N?全模板下界未确认。|工具能力下界可能有价值，toy问题可20天。致死：量词含糊、d小例外；证明窄模板不足发表，全模板可能与原大题一样难。|只保留窄模型，不主攻普遍猜想|
|A14 大题淘汰|O：P7§7缩小 Ω(√d/ln d)到d 的一般存在gap，或一般n/ln n到n gap。|P：本次原文核实，未发现近期直接解决；这不是确认最新最好界的完整survey。|问题重要，但需要新工具，20天无法以可解性下注。|**淘汰主目标；只当远景**|

## 3. 最优三个题的可检验陈述与止损门

### S1（A01）：有限权重类型的离散势合成

**具体陈述。** 令n_1,n_2任意，所有玩家权重在{1,2}，每个资源延迟c_e(x)=a_e x²+b_e x+d_e，a_e,b_e,d_e≥0，各玩家strategy set为任意非空有限资源子集族。问：是否有定义在(k,l)∈Z_+²上的资源势F，使所有加入边满足

w(k+2l+w)² ≤ F(k+1_{w=1},l+1_{w=2})−F(k,l) ≤ (37/33)w(k+2l+w)²？

若是，则所有此类游戏均有37/33-approximate potential。若否，最小失败(k,l)及其有理Farkas/负cycle证书是什么？这就是可以由程序自动证伪的目标。不要偷换成只有任意小于4/3的因子；37/33来自真正实验，可作为最先检验的强猜想。

**当前已证范围。** n_1,n_2≤2，任意资源数、策略数；见§4。浮点测试n_1=n_2∈{1,2,5,10,20}，q∈{1.01,1.1,1.5,2,3,10}，d∈{2,3}，共120组合。q2,d2,n≥2均37/33，q2,d3,n≥2均137/107。后者未做有理全约束证明。

**尚欠的跨n义务。** (i)构造全Z_+²统一F或证明任意population LP可行；(ii)验证所有加入边，无边界/无穷遗漏；(iii)说明nonnegative polynomial linear组合；(iv)计算/表示F的bit complexity；(v)终止不等于polynomial运行；(vi)证明37/33只模板最优后，另行测试允许type scaling λ_1,λ_2的更强模板；(vii)查HKS2014顺序potential、CF2021校正势和后续finite-type工作是否已有更好界。

**止损。** 48h内若能从HKS/其他文献直接算出≤37/33，则不宣传“新上界”；可继续问最优模板/自动证书是否有新意义。若全n LP在较小处失败，转最小障碍分类，勿继续扫大量浮点实例。

### S2（A02）：固定权重字母表下的exact-potential谱分类

**可检验陈述。** 对所有有限玩家集，w_i∈{1,3}；对所有有限strategy systems；成本C_i=Σ_e w_i c_e(load)。所有这样的游戏存在exact potential，当且仅当每个资源在正整数点上满足

c_e(t)=a_e+b_e t+d_e(−1/2)^t，t=1,2,…。

0处成本不被占用玩家观察，可以自由定义。这里要求资源所有整数点取非负并单调，可通过足够大a_e,b_e实现。若原始cost不含w_i，它就是weighted potential（玩家缩放w_i），不改变NE。

**当前小证明。** 矩形curl对一个light与一个heavy、背景总载荷x≥0给出
c(x+4)−c(x+1)=3[c(x+4)−c(x+3)]，即2c(t+3)−3c(t+2)+c(t)=0，t=x+1≥1。因可任意加入weight1背景玩家，所有整数x都实现。特征多项式2r³−3r²+1=(r−1)²(2r+1)，故通解如上。同weight两人curl自动为0；若把这些矩形条件正式放入finite Boolean occupancy lattice的path-independence引理，就得到充分性。**该充分性是标准离散可积性推论，但尚未单独写成严密可引用定理；新颖性未核实。**

**扩展不只是换q。** 一般整数q有(q−1)c(t+q)−q c(t+q−1)+c(t)=0。多个允许weights意味着差分算子的公因式/semigroup兼容性，可能产生“权重集合一扩充就坍缩为仿射”的分类；这才是值得包装的本质。不要把若干q数值小例子当多篇结果。

**止损。** 24h原文查重若已有完全finite-weight分类则放弃。若只给单一q、没有可复用算术刻画，应降为短note，不当20天主项目。

### S3（A03）：异质Lp近似均衡的smoothed算法

**可检验陈述。** 无权原子拥塞博弈，各strategy大小≤r，玩家p_i∈[p,q]，c_r(k)为非负非降成本。扰动模型先采用“各resource/load的z次幂成本有独立bounded-density noise”，z=2/(1/p+1/q)。证明β(1+ε)-improvement中指定的代理BRD，在expected poly(n,m,1/ε,φ)步终止，β=r^[½(1/p−1/q)]，最好能改到对原c的自然单调性保持扰动。

第一模型可能只是P10+P12直接推论，**不能作为最终新贡献**；必须至少攻下原cost扰动时的密度变换/近0 tail，或给更自然的相关扰动模型以及matching obstruction。原cost uniform noise经z次幂变换后出现density~t^(1/z−1)，逆最小成本的截断期望可能非常差。这是一个明确、可快速判死的数学障碍。

## 4. 已完成的有理证书：37/33四玩家小定理

设F(k,l)表如下，行k=light数，列l=heavy数，k,l∈{0,1,2}：

|F(k,l)|l0|l1|l2|
|---|---:|---:|---:|
|k0|0|296/33|1354/33|
|k1|1|629/33|2279/33|
|k2|5|37|109|

`exact_certificate.py` 对12条加入边逐一使用Python Fraction精确验证
wL_new² ≤ ΔF ≤(37/33)wL_new²；没有容忍误差、没有随机seed。

定义Φ(profile)=Σ_e a_e F(k_e,l_e)，先考虑pure quadratic。玩家i旧策略到新策略，保留资源成本不变。删去资源的potential decrease至少w_i乘其旧成本，加入资源的potential increase至多(37/33)w_i乘其新成本。故若C_old>(37/33)C_new，整体ΔΦ<0。有限profile集保证动态终止。常数延迟用F_const(k,l)=k+2l，仿射x用F_aff(k,l)=½[(k+2l)²+(k+4l)]，其边际恰为wL_new。把这两个exact potentials和二次F按非负系数相加即得一般非负二次多项式结论。

**模板最优性。** 从(0,0)到(2,1)两条路径：light/light/heavy的边际下界和为1+4+32=37；heavy/light/light的边际上界和为α(8+9+16)=33α。同一终点F必须同时≥37和≤33α，因此α≥37/33。

**边界再次强调。** 该最优性只针对统一真实w缩放的marginal interval模板。允许玩家类型另选缩放λ_1,λ_2可以变强；所有ordinal potentials又更宽。这个四玩家例并没有证明存在一个必须需要37/33近似的博弈。

## 5. 一个附属小证明：相关噪声的截断倒数引理

若X_1,…,X_μ∈[0,1]可以任意相关，而每个X_i的边际density≤φ，令Y=min_iX_i，则仅由union bound，P(Y≤t)≤min{1,μφt}。对a>0、B≥a，利用tail积分：
E[min{a/Y,B}]=a+∫_a^B P(Y<a/u)du ≤ a+∫_a^B min{1,μφa/u}du。
这给O(aμφ[1+ln(B/a)])上界，不需要独立性。取B=μ^β仍为poly(μ,β,φ,a)。因此P12仅依赖这一截断倒数lemma的approx BRD分析可以去独立；但这一观察太短，单独论文价值有限。它有助于构造保持成本非降性的共同噪声，或把A01证书加入smoothed算法。

## 6. 可复现实验与文件

- `research/topic_selection/probes/finite_weight/type_count_potential_lp.py`
- `research/topic_selection/probes/finite_weight/type_count_results.json`
- `research/topic_selection/probes/finite_weight/exact_certificate.py`
- `research/topic_selection/probes/finite_weight/exact_certificate.json`
- 本报告 `research/topic_selection/probes/finite_weight/ATOMIC_RESELECTION_2026-10-20.md`

Python3/scipy1.17.0，HiGHS；type_count为120个确定性组合；无seed。各≤20的q2,d2最大浮点constraint violation约3.64e−12，不能代替全n证明；四玩家exact_certificate的12条约束则已用有理数严格检查。原子研究者交稿时未改共享仓库；现由主研究者汇集保存。
