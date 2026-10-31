# 广义指派与结构化瓶颈分配：八题广筛及两条深入路线

日期：2026-10-20。已完整阅读 USER_GUIDANCE.md 与仓库 AGENTS.md；用户重新选题优先，不延续 general R||Cmax 破2。只使用原论文、正式会议信息、作者或作者机构材料。搜索覆盖2025/2026；搜索未命中不构成新颖性认证。与 fair_goods / fair_chores 已去重：它们做EFX/EF1/MMS，本线做容量严格的指派优化及舍入工具。

**首推 GA-03 两种容量的瓶颈多背包。** 它有2026顶会明确开放入口，且本轮找到可审算法草稿。GA-01虽深入，但本轮末发现2026通用cost-reduction框架很可能直接给出目标，已降为LIKELY_STANDARD_COROLLARY_PENDING_CHECK，不为凑数当第二主押。GA-02预算Santa Claus保留作备选，不把预算放宽当真近似。没有任何候选被承诺20天解决。

## 八题比较

| ID | 精确候选及目标 | 论文类型/想法来源 | 本轮判断 |
|---|---|---|---|
| GA-01 | 显式transversal matroid，任意分数basis x、单一线性cost c、k个[0,1]行a；输出basis，cost≤c·x，各行误差O(log(2k)+sqrt((a·x)log(2k)))，随机多项式 | 工具迁移；ICALP25作者明确点名SBO matroids | 已深入后降级：很可能为SOSA26标准推论；不作第二主押 |
| GA-02 | identical-valuations Budgeted Santa Claus，只有两种正资源值{1,R}，任意非负指派cost，预算B严格；目标真4-近似、随机多项式 | 公开log n改进问题的结构切片 | 备选；常数cost / 常数value bicriteria不算达标 |
| GA-03 | BMKP，公共item weight/profit、容量仅{B1,B2}、任意数量各类bin；目标每固定ε的多项式(2/3−ε)，容量不增 | 分类扩展；ICALP26 §7明确问常数种容量 | 第一名；联合类型恢复+双容量matching+独立4pmax舍入构成未审算法候选 |
| GA-04 | 任意顺序、weighted laminar matroid prefix basis rounding，单cost保留、所有prefix误差≤C·wmax，C为绝对常数 | 2026新prefix conjecture的结构类 | 暂缓；包含partition硬核，可能不比原prefix Beck–Fiala容易 |
| GA-05 | restricted Santa Claus，找到多项式(4−δ)-近似 | 将拓扑integrality-gap转constructive | 淘汰旧表述；2026作者机构已有3.534+ε算法公告，尚未核到完整可审定理 |
| GA-06 | max-GAP，每item至多两个eligible bins、bin数不固定，任意size/profit；目标0.76-近似，硬容量 | Fair contention resolution工具迁移 | 暂缓查重；3/4只是朴素独立抽样基准，不是已知最优界 |
| GA-07 | Group GAP，unit bins、公共sizes、group总size≤m/2、仅完整group计利润；目标1/5、硬容量 | reserved-capacity submodular组合工具 | 备选较低；母文1/6，需证明不是现成参数优化 |
| GA-08 | random-order online max-GAP；随机到达，决策不可撤销；目标competitive ratio0.16，硬容量 | 2025/26重轻两阶段工具 | 暂缓；当前(1−ln2)/2≈0.1534，改进不确定且偏online |

GA-01/04是加性舍入工具问题，不能直接包装成某个容量严格的乘法近似。GA-08是在线competitive ratio，不能与offline approximation混写。全general Santa Claus常数近似、global max-GAP常数大幅改进、general R||Cmax破2均不作为本轮短期主目标。

## GA-03：最值得继续的公开分类扩展

**Paper Fact。** Chen–Hu–Mao–Chen–Mei–Zhang–Chen–Zhang，ICALP2026，*Near-Tight Approximation Algorithms for Bottleneck Multiple Knapsack Problems*：同容量得到2/3−ε；任意容量得到1/2−ε，并有超过1/2的困难性，连unit profits也成立。§7最后一段明确问：常数种不同容量是否能2/3−ε。完整版本§4、Appendix A给profile、critical-item与舍入机制。正式版 https://doi.org/10.4230/LIPIcs.ICALP.2026.60 ；全文 https://arxiv.org/html/2605.05233v1 。web：turn86view1、turn118view0、turn120view0、turn122view0。

**文章定性。** 分类/组合工具型：同容量靠重物品profile、留slack、昂贵/便宜分工，避免max-sum中可牺牲某些bins的做法。价值判断应问是否自然扩大“容量类型数”这一分类轴，同时保留紧的2/3界，而非仅在任意容量1/2上改符号。最近邻硬度§6的容量B_j=t−u_j可有Θ(n)个不同值，不覆盖两种容量；独立battle也核实了这一点。

**我们的新idea。** 对每个容量分别计算profile产生的标签，但把每件物品的两个标签组成全局joint type。critical定义为所有long（至少3件）背包中的昂贵物品并集，每joint type只按**总需求**取最重物品。重物品替换critical槽时，本容量的舍入重量不变；较轻旧物品放回short槽，重量下降，short每槽只损一个利润桶宽。如此避免两个容量类独立取“最重”而重复用同一原物品。short允许singleton/pair，用zero dummy变为配对；小容量可行边嵌套于大容量可行边，只需指定匹配基数并最大化小边数。

**已写出的数学进展。** TWO_CAPACITY_LEMMA.md 中有三个独立可审引理：GA-03-L1固定联合标签的canonical恢复；GA-03-L2两个容量的nested pair匹配；GA-03-L3允许丢弃的4pmax加性舍入（极点秩计数，硬容量）。第三个引理独立证明，避免母文Lemma22若被字面解读为“全部物品必须整数覆盖”带来的合同歧义。母文的2pmax陈述不能不经审查直接导入。

**首个proof obligation。** 给定两个已猜profile、每joint type critical总数和各容量的long配置数量，证明全局最重critical集合可恢复为互不交原物品，且每long的舍入容量证书保持；准确条件、配对交换证明已在GA-03-L1写出。接下来总算法义务是：把母文Lemma8的前置利润上界与heavy-cheap预处理严格记账；保证joint标签对所有item全局可计算且类型数只依ε；保持singleton/pair与all-cheap long区分；gap oracle用几何网格而非假单调二分。独立review目前未找到联合恢复或本地slack舍入的不等式反例，仍不等于总定理获证。

**当前风险。** 最危险的是从同容量母引理导入时藏在“rescale ε”中的常数，以及是否把按未知OPT抽出的容量子实例误当成算法可直接知道。我们的算法只枚举常数维profile/配置数量；未知OPT仅用于存在性证明。未使用的昂贵物品必须允许丢弃，便宜LP只含全局cheap池，列约束为≤1。不得把所有余物强塞真实背包。

**玩具与可证伪测试。** 独立canonical选择已被最小2物品/2槽冲突矩阵否定；联合规则通过3000个Fraction实例、seed=20261020，共4927次交换。配对引理在6物品、weights∈{1,2,3,4}、capacities{2,4}、unit profits、1或2个小包的8192实例上穷举通过。未加小边quota的匹配在weights(2,2,1,1)上会选两个重量3的pair，尽管(2,2)+(1,1)可行。计算只核toy合同，不验证完整近似算法。

## GA-01：深入后被降级的工具开放问题

**Paper Fact。** Rohwedder–Rouhani–Wennmann，ICALP2025，*Cost Preserving Dependent Rounding for Allocation Problems*，Theorem2保单cost、保bipartite degree，且对star支持的行有Chernoff量级误差；§4末段问matroid bases版本，明确建议strongly base-orderable（SBO）类。https://doi.org/10.4230/LIPIcs.ICALP.2025.127 ，https://arxiv.org/abs/2502.08267 。web：turn26view0、turn37view2、turn97view1。

**新切片。** 显式transversal graph表示的matroid，而非任意SBO oracle。输入有理x∈P(M)、有理c、a_1…a_k∈[0,1]^E；目标输出basis B，使每个输出cost≤c·x，且以常数成功概率所有行同时满足误差O(log(2k)+sqrt((a_r·x)log(2k)))。不保精确边际。若同时要求边际不变，rank1、cost(0,1)、x=(1/2,1/2)已不可能。

**机制与首义务。** 两bases的strong ordering允许对匹配元素对独立翻硬币，形成互补bases；对任意a，单次merge方差Σ(a_e−a_f)^2/4≤(a·(B+D)/2)/2。学习母文“整个level选互补标签中总cost较低的一侧”，而非每节点单独贪心选cost；后者会丢掉所需level集中性。第一义务是polytime构造transversal strong bijection，并将dyadic TreeMerge各层的集中递推转到arbitrary rows。SBO仅给存在bijection不自动给算法。

**最近邻与致命风险。** 2026-08 Bérczi等给matroid成本保留稀疏discrepancy；SOSA26 Swamy–Traub–Vargas Koch–Zenklusen给face-preserving error-body→cost error-body差的通用转化；2026-10-12 Cherniavskii等给partition/block-TU hard constraints成本保留discrepancy。这些不字面写出目标均值依赖Chernoff合同，但可能使本题成为直接推论，须先审再投入。固定error body框架与依μ=a·x的半径能否无损兼容是第一条查重门。URLs：https://arxiv.org/html/2608.13983v1 ，https://arxiv.org/abs/2510.21287 ，https://arxiv.org/html/2610.16079v1 。web：turn104view0、turn104search0、turn52view1。

**本轮末的降级依据。** 已写COST_CHERNOFF_COROLLARY_CHECK.md：取L=ceil(log2(2k))、r_r=K(L+sqrt(μ_rL))，先在P(M)∩(x−R)内最小化cost。新均值ν_r≤μ_r+r_r；足够大K使标准SwapRounding的C(L+sqrt(ν_rL))≤r_r自洽。SOSA26 §2的cost证明只需最优点这一处的face-preserving与误差包含，遂得到cost保留及2R误差，甚至对任意matroid。技术门为面保持实现、rational半径、原open是否要求更强分布合同；尚未认证，但足以不再推荐GA-01独立开题。新增web：turn152view0。

**价值/反方。** 若真得到可用的成本保留集中工具，可迁移到硬预算公平优化，价值比单个常数调参高；如果只是既有SOSA26框架直接实例化，则应淘汰或只作学习。Toy：3×6 transversal有17个bases、136对全部存在strong bijection；单对8个outcomes成本均≤23/2，但cost选取改变行均值（第一行从3/2变1），说明绝不能继续声称边际保留。K4有一对spanning trees，对6个bijections均不strong，故不能把工具无条件推广到全部graphic matroids。

## 其余六题的完整卡片

**GA-02 两值预算Santa Claus。** 精确模型如表，所有人价值相同且每资源只有一个v_j∈{1,R}，资源可弃、单全局cost预算严格。母文ICALP25 Theorem3为O(log n)，§4第一问改进该因子；窄化为two values是我们的新idea。最近邻STOC26 Bamas–Li–Rohwedder *Randomized Rounding over Dynamic Programs* Theorem1.8针对unrelated values给双准则 n^ε polylog n（预算也放大），未解决此合同：https://arxiv.org/html/2511.03490v1 ，web turn82view2。首义务：构造成本不增且每small-resource重用至多常数的big/small选择，不可把Θ(log n)的拥塞硬写常数。玩具应从两player、1big+若干unit small、cost{0,1,2}枚举，审计min-cost Pareto frontier。风险：两值并未消除共享small的cover选择，依旧可能有非局部局部搜索障碍；本轮不以缺少反例当可解性依据。价值看是否推进母文真预算开放问题；全一般常数版不推荐。

**GA-04 prefix laminar。** Bérczi–Liu–Reis–Tarnawski 2026，§6 Conj5/6：给有序matroid ground set、非负weights、fractional basis，求basis令所有weighted prefix差≤Cwmax；cost版本另需c(B)≤c·x。一般只给O(log n)，binary weights已有C=1；uniform weighted Thm16正文无cost，不能仅凭Intro就报“cost版C=1已解”。我们的候选是height2 laminar、任意item order、单cost的常数C多项式构造。https://arxiv.org/html/2608.13983v1 ，web turn32view6。首义务：找跨laminar子树的前缀交换，不让误差随活跃子树数累加。反方：包含partition；cactus graphic只是partition的换写，已由battle淘汰，不另立题。连续不交的partition blocks、bounded active-width给的简单求和界也不是好论文。Oct12 hard-constraint paper已提供partition误差oracle框架；新结果须真正证明更强discrepancy，而非换输入名。

**GA-05 restricted Santa Claus构造化。** Haxell–Szabó，Combinatorica2025（预印2022），Theorem1.1给CLP gap3.534、§7处理(1,ε)two values，核心为拓扑连通性代替组合增广。https://arxiv.org/abs/2202.01143 ，https://doi.org/10.1007/s00493-025-00141-7 ，web turn82academia16。原拟目标polytime(4−δ)并非本轮可安全选题：IIT Madras 2026-01/02 Anil Kumar thesis-defense作者机构公告明确声称3.534+ε polynomial算法；https://cse.iitm.ac.in/spotlight.php?highlight=140 ，web turn86view0。尚未取得完整公开算法审查，故不把公告当获验证定理，但已有强重复风险，淘汰旧目标。若重定题需精读其geometric-programming构造与topological gap适用范围。Toy CLP gap不代表多项式算法，不把gap证书当解决。

**GA-06 degree2 max-GAP。** 母文Feige–Vondrák FOCS2006 *Approximation algorithms for allocation problems: Improving the factor of1−1/e*，§2.2 fair contention，§4 GAP rounding：https://theory.stanford.edu/~jvondrak/data/alloc-focs.pdf ，web turn65view1、turn97view4。新想法是arbitrary #bins但每item至多2可选bins，目标期望profit≥0.76OPT、硬容量，复杂度polyinput。不是“仅2bins”（固定bin数有不同算法结构）。首义务：利用eligible-bin graph的edge结构协调config抽样，证明超3/4的项级收益并同时保bin packing。Toy2bins2unititems独立抽样期望3/2，对OPT2仅3/4；相关matching直接得2，所以3/4是工具损失而非hardness。最近邻two-player SMW已有13/17，不能误当GAP或degree2结论；当前最近邻覆盖不足，不推荐直接开工。价值看graph结构是否扩大既有rounding能力，单个小toy不是新算法。

**GA-07 Group GAP改进1/6。** Kulik–Sarpatwar–Schieber–Shachnai ESA2019，main theorem给group总size≤m/2时1/6；核心把分数GAP利润变成submodular set function并预留一半总容量。https://arxiv.org/html/1907.01745v2 ，https://doi.org/10.4230/LIPIcs.ESA.2019.69 ，web turn82view4、turn104view2。精确目标1/5算法、sizes bin-independent但profits可bin-dependent、仅全部items成功放入的group计收益、容量严格。首义务：证明reserved-capacity subproblem在相同输入条件下达到2/5，并核总算法的另一半损失仍≤1/2；不能简单把两阶段保留率相乘后当已有定理。最小toy为m=2/3、groups≤m/2，枚举group完整性与LP选择；重物品使仅按总weight选groups未必可pack。近期检索未见完全同目标，但文献较旧、参数优化撞车风险高；工具型判断应看是否可迁移到别的all-or-nothing assignment。

**GA-08 random-order GAP。** Klimm–Knaack IPCO2025 / Mathematical Programming2026，*Generalized assignment and knapsack problems in the random-order model*，main result竞争比(1−ln2)/2。https://doi.org/10.1007/s10107-026-02405-6 ，web turn23search27、turn67search22。输入items随机排列到来、每次揭示全部bins上的size/profit、不可撤销选择或拒绝；目标ratio0.16（取期望、对offlineOPT），运行时间多项式。学习重/轻分阶段但试让中型items多一次保留机会。首义务是精确写停止时间下剩余容量概率，避免把random-order依赖当独立。Toy2bins≤6items枚举全部n!排列；目前尚未做这项audit。该题并非本轮最优，目标微改进可能依赖大篇概率分析，且偏online。

## 证据、复核与交付状态

代码：toy_audit.py；输出：evidence/toy_audit.json。运行 `python topic-selection-drafts/generalized_assignment/toy_audit.py` 可复现。核心判断均以整数或Fraction核查；joint-canonical使用seed=20261020，其他已执行toy为穷举；参数部分另审计901个ζ=1/d（d=100…1000）的显式预处理与几何grid差式。

独立battle提出并已纳入：cactus≡partition；cost-preservation不兼容精确marginals；BMKP hardness多容量不覆盖两种；joint labels需全局可计算；profits先cap；K须在重组之后规范化；heavy-cheap删除须另付利润预算；cheap池允许discard；gap oracle不可伪二分；母文Lemma22字面覆盖合同不能盲调；GA-01很可能是2026直接推论，应降级。GA-03完整算法仍处候选态，详见独立证明笔记和cross-field review；没有把计算升级为证明，也没有新颖性认证。


代码与冻结输出：`tests/audits/topic_selection/generalized_assignment/`、`evidence/runs/topic_selection/generalized_assignment/`；见[复现说明](../VERIFICATION.md)。
