> 这是第一轮原文卡与推导记录；后续裁决以 [BATTLE](../BATTLE.md) 和 [候选池](../candidate_pool.json) 为准。全库来源统一为 A=作者明确原题、B=作者明确建议方向、C=团队派生；本稿局部使用的分级符号不得当作统一来源标签。

# boss37 重新选题：近似公平分配第一轮独立扫描

核查日期：2026-10-20。此目录只写本轮研究笔记与独立代码；未修改共享仓库，未提交。任务是重新选题，不是继续硬攻一般 scheduling 的 2-epsilon 壁垒。20 天、每天约 12 小时高强度模型辅助是资源上界，不是可解性保证。

## 先给结论

本轮保留 **16 个有实质区别的候选**，涉及 12 篇以上一手论文。主推三条为：

1. **多重图 EF orientation 按 heavy edge 数量参数化**（F01）：最新论文明确提出，已有二值分类与简单图算法可拆解，最符合“读懂工具本质再扩类”。
2. **uniform conflict allocation 在 cactus 图上的 maximal equitable partial coloring**（F03）：以公开的任意图问题为母题，从树扩到每块为边或环的图，结构与可视化包装较好。
3. **预算 chores 的两种 size 情形下多项式 EF1**（F11）：连接 knapsack、density greedy 和公平性；比泛化 EFX 存在性更偏运筹优化，失败也有明确的局部算法障碍可提炼。

F07（三值 chores 最小反例与参数区域）作为高收益计算副线，已经有真实枚举结果，但目前只是有限实验和已知反例复核；不能把它当成已取得新定理。F13（五人七件 EFX 计数极小值）也值得保留为有计算证书路线的备选。

来源标签：**A**=原论文明确提出的 open question；本稿原有 B/C 是内部生成方式标记；统一候选池将所有未被作者明确提出的新 idea 与结构子题归 C，并单独保存母题来源。没有将 B/C 冒充原作者猜想。

## 最新进展清洗：这些旧问题已经不能直接选

| 旧说法 | 截至核查日的一手证据 | 本轮处理 |
|---|---|---|
| additive chores 的 EF1+PO 是否存在 | Mahara, [2507.09544](https://arxiv.org/abs/2507.09544), §§4,6：包括 weighted EF1+fPO 存在；固定人数可多项式计算 | 只保留一般人数多项式计算/受限类算法，不再卖存在性 |
| additive chores 总有 EFX | He–Tao, [2606.08872v2](https://arxiv.org/html/2606.08872v2), Thm1：所有 n>=4 都有三值反例 | 一般存在性已否；三人仍是大问题，不适合直接主攻 |
| bivalued chores EFX 已全部解决 | 同文 Thm3 只证明 n=4；§6 仍问 n>4 | 正确范围 n<=4；五人完整问题仍偏难 |
| bivalued chores EFX 可与 PO 兼容 | 同文 Thm2：每个 n>=4 都存在严格正二值实例使任意 EFX 都非 PO | 已否，不能用作正向主目标 |
| multigraph additive EFX allocation 是否存在 | [2606.18665](https://arxiv.org/html/2606.18665v1), §1.1、结论：cancelable superclass 上已给多项式算法 | 分清 allocation 与 orientation；转 noncancelable 或效率问题 |
| strongly EFX-orientable 简单图完整刻画 | Zeng, [2609.36498](https://arxiv.org/html/2609.36498v1), Thm1.1 已完整刻画 | 不重复树/二分图/三色之间旧空隙；可研究别的约束、近似或多重图 |
| personalized bivalued goods/chores exact MMS | Zhang, [2608.15822](https://arxiv.org/abs/2608.15822)；独立 [2610.19099](https://arxiv.org/html/2610.19099v1) §1.1 也明确承认一般化结果 | 旧15/13、两类型纯 chores MMS 不能再当开放 |
| 小件数三人 chores EFX 从七件开始就开放 | [2609.10585](https://arxiv.org/abs/2609.10585) 已覆盖7、8件；另有 Zenodo 九件候选稿但未完成可靠性评审 | 不能用旧2n门槛给三人题目制造新颖性；九件候选不当已确立事实 |
| 接近二分图的 EFX orientation 应当FPT | [2512.25033v5](https://arxiv.org/html/2512.25033v5) §1.1 回顾：binary symmetric 简单图只需删除两条边变二分图仍NP-hard | 该参数路线直接淘汰，不能只看“接近已解决结构” |

所有未找到后续解决的候选，只能表述为“本次检索未找到”，不是已证明全球仍开放。

## 16 个候选池

| ID、来源 | 精确模型与量词、最小研究目标 | 已知边界与原文位置 | 价值判断策略 | 致死障碍与20天判断 |
|---|---|---|---|---|
| **F01 A** heavy-edge parameter | goods 为多重图边，只能给端点，additive nonnegative integer valuations，可不对称、允许0。heavy 指至少一个端点 valuation>=2 的边，数量k。判定完整 **EF orientation** 是否可用 f(k)poly(n+m,bit length)，进一步2^k poly | P01 Thm5二值multigraph线性分类；Thm13简单图2^k；§5明确问多重图同界 | 先抽象“固定heavy方向后，单位边残差可行性”，不是直接堆参数DP；若得到网络流/整数度约束等价有独立价值 | 平行边使 pairwise envy 与总入度耦合；不能沿用简单图每对最多一件的归约。主推，先争取f(k)再2^k |
| **F02 A** remove shared-weight parameter | 与F01同模型，多重图 EF/EFX 或min-charity；求FPT(tw+Wmax)，Wmax是单边端点最大值，而不是一对端点所有平行边价值之和 | P01 Thms14,23 已FPT(tw+Wshared)；§5明确问替换参数 | 若把大量单位平行边压成奇偶与有限阈值，属于分类工具压缩，有漂亮界面 | 二进制大weights、常数tw弱NP-hard已知；必须Wmax参与。可能需要计数压缩，不宜直接承诺强界；备选 |
| **F03 C** cactus uniform maximalEF1 | 任意cactus冲突图G、任意人数n>=1，v_i(S)=|S|，求n个不交独立集，大小差<=1，且每个未分配顶点邻接每一个颜色类 | P02 §6/AppendixB Thm20树成立，任意图问题明确开放；P03是2026长文后续，应二次精读排重 | 树的root-high-color归纳能否升级到“环块有两个接口”；目标存在+polytime，正负都能用有限坏块解释 | cactus有奇环使单根置换失效；不能用完整equitable coloring文献替代maximal partial模型。主推结构题 |
| **F04 C** cographs / modular classes | uniform valuations同F03；先cograph，再固定modular-width图，研究是否总存在和构造 | P02任意图母问题；本轮已独立证明complete multipartite starter lemma（下文），未核其新颖性 | join/union模块组合是否保存可实现的颜色容量区间；比逐图类凑定理更有价值 | 如果只得到complete multipartite，很可能过浅；需要模块合成定理或明确最小障碍。次级副线 |
| **F05 A+C** three-agent additive conflict | n=3、identical nonnegative additive valuations、任意冲突图；求maximal EF1 allocation，或反例。20天先限outerplanar/小treewidth或给最小反例 | P02 §6显式open；n=2已解，n>=4 identical additive有反例，Lemma15任意负例可自动给NP-hardness | 值得找反例是因为一枚有限负例直接触发一般复杂性结论；正面须有大类和构造 | 三人身份异质时不应默认cut-and-choose推广；完整母题可能很难。48h无结构则降级 |
| **F06 A+C** monotone oracle complexity | 两人、冲突图，identical或heterogeneous monotone valuations；问poly(m,T(m))；先 budget-additive/submodular或固定treewidth图 | P02 Thm10一般monotone指数/伪多项式、additive多项式；§6问强poly；P03后续加入color-switch视角 | 非加性的新势函数，或证明value-oracle query下界；工具/障碍两向都可包装 | 任意monotone表示可能隐藏指数信息；不能把值上界B当输入bit length。备选 |
| **F07 B** smallest ternary chore obstruction | 四人、成本属于{1,r,L}、两种agent type；首阶限定三item type A/B/C，计数(a,b,c)，寻找m<13反例或证明该模板的精确不存在区域 | P04 Thm1已有(3,5,5),(20,1,7)/(20,7,1)13件反例；P05一般m<=2n有EFX | 新价值须是更小反例、参数必要充分条件、或可检验证书；只重现13件不算贡献 | 数值枚举不能证明任意实数成本，更不能证明全模型最小。副线，真实枚举已完成 |
| **F08 C** five-agent bivalued sparse incidence | n=5、c_i(g) in{1,r},r>1；每件chore为large的agent至多2，形成large-incidence图；先该图forest，再cactus，问EFX完整存在+polytime | P04 Thm3解决n=4，§5.4用multigraph deficient-set工具，§6问n>4 | 学习“最亏欠集合+前缀拼接”的真实不变量，检验forest是否去掉五人新障碍 | large-at-most2并不自动是goods graphical model；禁止直接套multigraph EFX theorem。完整五人题不主攻 |
| **F09 A+C** personalized bivalued goods EFX+PO | goods，每人自身两个正数a_i<b_i，任意item pattern；是否存在EFX+PO？先三人、m<=8、两种ratio class寻找不可兼容最小例 | Jin–Tao [原始v2](https://arxiv.org/html/2507.18251v2) §5（WINE2025）明确提出EFX+PO；P04 §6为后续转述。普通公共{a,b}二值已有EFX+fPO | 价值是把“共同价格比例”失效刻画为具体交换cycle；可用精确Pareto前沿枚举 | 排序不同+比例不同会破坏MNW性质；若只在少件数反复没找到例不能当定理。备选 |
| **F10 A+C** noncancelable graphical EFX | multigraph valuation，每物只对至多2agents相关；非additive monotone submodular valuation；先underlying multicactus，允许非端点分配，问完整EFX allocation | P06结论明确问monotone/subadditive扩类；cancelable全部图已解；triangle-free等旧图类成果不可重卖 | 用最小局部补充性/取消律失败实例判断工具真正边界；若submodular不存在，可给极小support反例 | allocation不是orientation，向无价值第三人给物可能修复妒忌；一般submodular EFX已否但不自动落在degree2 support。较高风险 |
| **F11 B** two-size budget chores EF1 | objective additive size s(g) in{s1,s2}、objective additive cost d(g)>=0、异质budget B_i、housekeeper接余下；按P07预算可行子包定义EF1；求polytime | P07 Thm3.1 EFX伪多项式；Thm4.2 EF2多项式；§5仅identical size/cost/density/budget和两人EF1多项式 | 应直接研究两条density序列的交错与knapsack exchange，用exact DP/greedy repair对比；与OR方向连接最强 | 不是普通EF1定义；零成本、housekeeper比较必须保留。两size并不保证DensestFirst已有EF1。主推可计算性题 |
| **F12 B** two-budget budget chores EF1 | objective size/cost任意，B_i in{Bsmall,Blarge}，任意n>=3；先每budget至少2agents，求polytime EF1 | P07 §5.4 identical budgets已解，§5.5两人已解；两budget是两个已解维度的自然组合 | 按budget class做匹配/交换，验证两人cut-and-choose可否块级实现；若有可扩展双层机制有价值 | 同一类内部无妒忌不保证跨类；若只暴力DP有伪多项式改进但未越边界。F11备选 |
| **F13 B/A-gap** EFX count n=5,m=7 | nonnegative additive goods，labelled agents/items；最少完整EFX allocation个数是多少？先寻找<=13的实例或证明>=14，再推广m=n+2 | P08 Thms3.7,3.8给一般n至n²；§6说n<=4可到n，n=5随机最小14；其Conj6.1是更广泛至少n，不可把全general monotone版本继续视为有效 | finite polyhedral-cell/SAT证书+join-graph组合性质，可同时产构造与计数下界；不能只跑随机值 | 5^7=78125分配可算，但valuation space连续无界；只到n=5可能小，需一般机制。很适合计算副线 |
| **F14 B** weighted binary EFX with partition capacities | binary additive goods、positive rational entitlements w_i、每agent各category容量；先公共partition matroid，判定可行完整WEFX并刻画必要充分条件或最小负例 | P08 §4 binary无约束WEFX+PO多项式；约束扩张为本轮新idea | 把weighted envy阈值与b-matching割条件联系；价值判据是cut characterization或明确tight gap | 完整可行性与WEFX可能马上不兼容；需先反例筛，不默认存在。未作充分后续文献清洗，低置信 |
| **F15 B** mixed two types + one exception | objective mixed manna：一type good、一type chore，再加一件cost/value vector任意但符号objective的exception；任意n，问exact MMS存在或参数化tight approximation | P09两types mixed exact MMS几何算法；P10 personalized二值纯good/纯chore已解 | 研究二维整数边界插入一个离群点是否仍有共同支持线；若失败给最小几何孔洞；方法驱动，不是任意加type | 一件exception可能已编码general MMS失败；MMS基准可正/负/零，乘法ratio须分符号。中等风险 |
| **F16 B** online eligibility fairness with recourse | identical-size goods/chores在线到达、eligibility subsets<=2形成forest；采用P11 weak eligibility-aware EFX，问常数/对数recourse每次能否维持，或tight lower bound | P11最新摘要：weakEF1在线可维持，weakEFX offline/online分离；recourse是本轮新idea，需读PDF后固定确切定义 | scheduling restricted-assignment与公平直接交叉；目标tight update tradeoff而不是再证明已知offline existence | 不能用标准envy，也不能把unweighted单位size与一般cost混用；尚未全文核界。低置信候补 |

## 论文定性与工具本质（不按标题猜贡献类型）

| 编号、一手来源、已核位置 | 类型 | 方法本质与玩具模型；如何由此提题 |
|---|---|---|
| **P01** Kanellopoulos et al., [EF(X) Orientations: A Parameterized Complexity Perspective, v5 2026-10-07](https://arxiv.org/html/2512.25033v5), Thms5,13,14,23、§5 | 分类+组合工具驱动 | binary边以偶数平分、奇数由已有“种子”吸收，坏成分可刻画；simple heavy固定后变度约束orientation。玩具：两个顶点p条单位边；加入第三个顶点的一条已入边怎样消除奇数失衡。自然扩类是多重图heavy、去共享weight，不是再追小treewidth |
| **P02** Igarashi–Manurangsi–Yoneda, [Dividing Conflicting Items Fairly](https://arxiv.org/html/2506.14149v1), Thms10,11,14,20，§6 | 视角+分类驱动 | 用maximal partial allocation替代可能不存在的complete/PO；两人靠可行分配链跨越envy方向；uniform转成maximal equitable partial coloring。玩具：星形冲突图可放弃中心，按颜色分叶。自然扩类cactus/cographs、非加性oracle边界 |
| **P03** Equbal et al., [Fair Allocation under Conflict Constraints, 2605.09930](https://arxiv.org/abs/2605.09930), 摘要及引言待二读 | 工具+组合驱动 | color-switch恢复EF1；path上混合符号用cycle-plus-triangles。用途是给P02候选排重；不要假设2025版本就是最新边界 |
| **P04** He–Tao, [EFX for Additive Chores, v2](https://arxiv.org/html/2606.08872v2), Thms1–3、§5.4、§6 | 问题驱动+分类工具 | 三值的计数/容量挤压否存在；四人二值用item-type前缀与deficient-set multigraph拼接。玩具：2+2两agent types，3件共同大活和两组5件交叉偏好。扩类应找计数阻碍或deficient-set条件，不是一口气五人任意 |
| **P05** Kobayashi–Mahara–Sakamoto, [EFX Allocations for Indivisible Chores: Matching-Based Approach](https://arxiv.org/abs/2305.04168), 摘要所列三类结果 | 工具驱动 | 通过matching把partial bundles与agents连接，维护EFX可扩展性；m<=2n、all-but-one同序、三人personalized二值。玩具：每人至多两件。扩类可看matching Hall缺口与例外agent数 |
| **P06** Afshinmehr et al., [EFX Allocations Exist on Multi-Graphs](https://arxiv.org/html/2606.18665v1), §1.1、结论 | 问题+工具驱动 | degree2 item relevance上的cancelable EFX算法；不能据此获得orientation。玩具：两agents共享多件再引第三agent吸收。扩类noncancelable或效率，而不是triangle-free到全图旧推进 |
| **P07** Elkind–Igarashi–Teh, [Fair Division of Chores with Budget Constraints](https://arxiv.org/html/2410.23979v1), Thms3.1,4.2,5.1–5.5，§7 | 视角+组合工具驱动 | objective size/cost与housekeeper使budget比较有意义；manageable sets给EFX伪多项式，density greedy给EF2和若干EF1特例。玩具：两个大小、预算刚过容量临界的三agent。扩类应合并已解特征，并严格用预算可行子包比较 |
| **P08** Neoh–Teh, [Understanding EFX Allocations: Counting and Variants](https://arxiv.org/html/2504.03951v1), Thms3.7,3.8、§4、§6 | 视角+分类驱动 | 从有无解转最低解数；join-graph把可构造分配映到组合图，计数来源有结构。玩具n=5,m=7。新猜想要从join-graph不能实现的形状出发，不盲猜随机最小值就是答案 |
| **P09** Chen et al., [Maximin share allocations for two types of items](https://arxiv.org/html/2610.19099v1), §1.1、§§3–5 | 视角+工具迁移驱动 | 从两job-type scheduling迁入二维整数几何，覆盖goods/chores/objective mixed。玩具是每bundle整数点(a,b)，agent边界为不同斜率直线。natural extension是一exception或sign边界；纯两type已解 |
| **P10** Yuhao Zhang, [Exact MMS Allocations under Personalized Bivalued Valuations: Goods and Chores](https://arxiv.org/abs/2608.15822), 摘要；P09独立工作段交叉核验 | 问题驱动（工具尚未精读，不臆造） | 本轮功能主要是消除旧MMS候选；后续若选此工具链必须全文精读，不能只从结果反推方法 |
| **P11** Biburger–Megow–Shahkarami, [Online Fair Division under Eligibility Constraints](https://arxiv.org/abs/2610.08064), 摘要已核 | 视角+分类驱动 | 可行性改变envy基准，strong/weak的区分决定存在性与在线界；goods/chores的比例性分离。玩具：路径eligibility和单位jobs。衍生recourse前需精确定义和下界量词 |
| **P12** Zeng, [A Polynomial Time Characterization For Strongly EFX Orientable Graphs](https://arxiv.org/html/2609.36498v1), Thm1.1 | 分类驱动 | block decomposition+odd-cycle transversal的局部刻画；非二分只允许一个特定块。玩具：两odd blocks经cutvertex连接。研究扩类应问保留何种证书，而不是重复“染色数<=3” |
| **P13** Mahara, [Existence of Fair and Efficient Allocation of Indivisible Chores](https://arxiv.org/html/2507.09544v1), §§4–7 | 问题驱动+新组合工具 | fixed point保证初始化，离散过程完成fairness；§7指出找到该初始化就得一般poly算法。玩具宜先固定两/三agent看最优LP区域，而非从全局fixed point直接求多项式 |
| **P14** Haviv, [Fair Allocation under Conflict Constraints via Strong Colorability](https://arxiv.org/abs/2607.01059), 摘要已核 | 视角+分类驱动 | common preferences的公平分配与strong chromatic hierarchy联系；完整分配人数条件3Delta-1、算法(3+epsilon)Delta。它研究完整分配，不能直接覆盖P02 maximal partial所有n |

## 已经实际完成的证明：complete multipartite 的 uniform maximal EF1

**命题（本轮独立推导；未声称文献新颖性）**。任意 complete multipartite conflict graph 和任意正整数n，uniform valuations 存在 maximal EF1 allocation，且可多项式构造。

设parts大小 s1>=...>=sk。独立集只能处在一个part中。

* 若总顶点数<n，把每件给不同agent，完整、大小0或1，成立。
* 若s1>=n，只分配第一part，把s1件均匀分成n个非空包；其它parts每件都与每个非空包相邻，故无法补进任意包，maximal。
* 剩下s1<n且总数>=n。取最短前缀s1,...,s_l，其总和S>=n；则l>=2且Sprev=sum_{i<l}s_i<=n-1。令r=s_l。每个part可拆成k_i个大小1或2的非空包，当且仅当ceil(s_i/2)<=k_i<=s_i。只须证明sumceil(s_i/2)<=n<=S。

因为s_i>=r，

    sum_{i=1}^l ceil(s_i/2)
      <= Sprev -(l-1) floor(r/2) + ceil(r/2)
      = Sprev -(l-2) floor(r/2) +(r mod 2)
      <= n.

从各k_i=ceil(s_i/2)开始，逐个增加直至和为n，即得n个大小1或2的包。选中parts全分配；未选中parts每件邻接全部n个非空包，所以maximal。uniform EF1等价大小差<=1，命题得证。

这一命题能作为模块扩类的toy model与正确性测试，但**单独太浅，不能因为有个新证明就立刻选为论文**。价值必须来自cograph组合、cactus全类、一般禁结构或复杂性分界。

## 实验事实与边界

运行 `python reselection_fair/exact_probe.py` 可重现。代码只用int64整数，所有中间数远小于溢出阈值；没有随机步骤，因此seed为null。

1. He–Tao四人三item-type模板：A有3件、B/C各5件，第一类两人的成本(20,1,7)，第二类两人(20,7,1)。按三type件数到四人的分配枚举，准确覆盖 C(6,3)*C(8,3)^2=**62,720** 个type-count allocations（每个labelled分配与一个type-count分配同公平状态）。EFX数为 **0**，复核已知反例。
2. 枚举全部非空坐标子实例 0<=a<=3,0<=b,c<=5，a+b+c<=12，共 **142** 个，成本固定(1,7,20)；**全部存在EFX**。所以该固定成本、固定三type反例在删除item意义下极小。这不证明13是所有四人反例的最少件数。
3. 固定counts(3,5,5)，r=2,...,12且L=r+1,...,50，共 **473** 个整数点，**21** 个无EFX。无解点为r=7时L=20；r=8时22..23；r=9时24..26；r=10时26..29；r=11时28..32；r=12时30..35。它们落在 `2r+6 <= L <= 3r-1`。这是有限样本规律，不是实参数定理；也未对该规律作新颖性核验。
4. 对上面complete multipartite构造，覆盖总顶点数1..30的全部整数parts partition、人数1..12，共 **343,536** 个实例，逐个验证独立性、不重分配、maximal和大小差<=1，失败0。这是证明实现核对，不替代证明。

输出文件：`probe_results.json`、`trivalued_grid.json`、`deletion_subinstances.json`。

## 前三名的20天研究合同与提前止损

### F01：多重图heavy EF orientation

第1–2天逐行重建P01 Thm5/13，固定heavy方向后写清残差变量：p_ij是单位平行边数，x_ij是给i的数量，x_ij+x_ji=p_ij；h_i是heavy已获价值，q_ij是i对j已获heavy的估值。EF要求

    h_i + sum_j x_ij >= q_ij + p_ij - x_ij.

另外单侧0/1边应按Observation3先确定方向，计入h_i常数；上述公式默认剩余单位边在两端价值都1。它显示为什么简单图的度上界归约不能原样搬到多重图。

第3–6天寻找可解残差子类/压缩：heavy端点至多2k，binary坏成分在这些边界外能否收缩成奇偶与容量接口。先输出一个必要充分的interface lemma，再考虑FPT。第7–12天争取f(k)poly的算法或W[1]/paraNP障碍；第13–16天压指数、处理non-symmetric/zero与charity；第17–20天证书、下界、文章。若第4天还不能把binary component与boundary精确分离，降级到仅symmetric或只有一个heavy edge的完整分类，不继续空转2^k。

### F03：cactus maximal equitable partial coloring

第1–2天完整重建root-high-color树归纳，并核P03/P14与graph-coloring文献排重。第3–5天枚举小cactus，尝试root接口状态：root uncolored；root colored且在high类；环上相邻两个boundary的同/异色与high状态。第6–12天证明环block组合，若三角形已经打破不变量，先unicyclic全类或even-cactus。第13–16天给线性/多项式算法及不适用的最小非cactus；第17–20天把公平与图结构等价组织成一条完整叙事。若仅发现“树加一条边也成立”但无机制或无法扩至unicyclic，则价值不够，应换F11。

### F11：两size预算chores多项式EF1

第1–2天固定P07全部比较量词，重建housekeeper的预算可行子包约束。第3–5天准确实现DensestFirst和EF1 verifier，用整数sizes与budgets搜两size失败，并区分“算法失败”与“存在性/复杂性失败”。第6–10天把每size的density序列作为两条链，尝试交换一个大item与若干小item的修复势函数；并行争取固定size ratio的DP或FPTAS。第11–15天从两size推进固定d种size或给强NP-hard计算障碍；第16–20天给tight反例与完整证明。若只得到按B伪多项式，不比原manageable-set路线强，必须降级；若EF1计算一般本就poly的新论文被核到，立即淘汰。

## 本轮诚实的确定性等级

* 已真正做：最新一手检索清洗、候选精确定义、完整multipartite小证明、**62,720**型反例复核、142子实例、473参数点、343,536构造核对。
* 尚未做：前三名完整证明；F14/F16全文与所有后续论文闭包；任何保证20天能发的判断。
* 选择标准：A类看边界是否刚被最新工具打开；B类看工具本质与可推广接口，不靠随机结果“像成立”；C类看扩类是否含自然障碍与统一算法，不按容易加一个graph class就宣称高价值。
