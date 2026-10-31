# 不可分 goods：从固定瓶颈与前缀交换中筛选公平分配题目

日期：2026-10-20。已完整阅读 `USER_GUIDANCE.md` 与现行仓库 `AGENTS.md`；本轮重新选题优先。本报告不沿用旧 unrelated-machines 主目标，不声称任何普遍开放问题已由计算解决。只使用原论文、作者论文页和正式出版物核实状态。

## 推荐排序及本轮实际覆盖

建议进入下一轮 battle 的两个题目是 **FG01 四人 laminar EF1 的固定 key matroid 瓶颈**、**FG02 goods-with-copies 的 SD-EF1**。前者有明确公开问题、有限归约及失败方法；后者有清楚的分类边界、完全序数化的交换结构。若只选一个，优先 FG01，但第一阶段必须允许用反例否定 ordered no-envy 加强命题；加强命题失败不否定普通 EF1。

| ID | 精确切口 | 本轮判断 | 核心理由 |
|---|---|---|---|
| FG01 | 4 人、共同 laminar 约束、完整可行 EF1；先解 8/12 物品 key matroids 的指定 ordered no-envy 加强版 | 第一名，深入 | 明确有限瓶颈；解决两块即可推出整个四人 laminar 类 |
| FG02 | 等值副本、每人每类型至多一件，完整 SD-EF1；先做 3 人 | 第二名，深入 | AAAI25 明确公开问题；可化为前缀约束的整数 b-matching |
| FG03 | 3 人、两类各 3 件、每类 cap=1：EF1 与共同约束下 fPO 能否同时成立 | 保留，次级 | 2026 新价格交错工具仅能逐类删除；最小跨类同步问题 |
| FG04 | 两个任意类别与共同上界，非负 additive；寻找多项式 2/3-MMS | 保留但不建议先攻 | 要打破多类别高值物品重叠与剩余可行性障碍；非单纯套 bag filling |
| FG05 | additive、m=n+2：精确最少 EFX 分配数；先 n=5,m=7 | 储备 | 明确计数问题；比一般 EFX 存在性窄，但价值须靠结构定理 |
| FG06 | 简单图的强 EFX 可定向图分类 | 淘汰，已解 | 2026-09/10 完整多项式分类 |
| FG07 | 多重图 additive/cancelable 的完整 EFX | 淘汰，已解 | 2026-06 已有任意多重图多项式算法 |
| FG08 | 任意共同 matroid、相同 additive 估值的 EF1 | 淘汰，已解 | 2026-08 weighted equitability 已覆盖一般相同估值 |
| FG09 | balanced EF1+fPO 从双值/两估值类型扩大到一般 additive | 淘汰，已解 | 2026-08 已完整解决存在性；算法问题须另立范围 |
| FG10 | simultaneous MMS/EF1 的单纯提速 | 淘汰原版本 | 2026-10 APS+EFL+近似 MXS 已有多项式算法，须重定指标 |

这里的“未发现后续”只是本次检索结论，不是新颖性认证。FG01 母论文为最新预印本；FG02 母论文正式发表于 AAAI25。二者均有 Nisarg Shah 参与，满足从成熟研究群工作的具体边界出发，而非随意拼接题名。

## FG01：四人 laminar EF1 的 8/12 件瓶颈（深入）

**母论文与原文位置。** Benjamin Cookson、Nisarg Shah，2026，*Constrained Fair Allocations via Partition Matroid Reductions*，<https://arxiv.org/html/2608.31121v1>。定位：§3.4 Lemma 8 给三人加强版；Appendix B Definitions 13/14、Lemma 11 给四人两块归约；Lemma 12 给旧工具失败反例；§5 “Resolving the case of four agents” 明说未解决并讨论计算辅助尝试。web refs：`turn16view0`、`turn19view1`、`turn25view1`、`turn47view0`、`turn47view1`。本次另查作者论文页 <https://bcookson.github.io/publications/>（`turn25search9`），未发现四人后续解决。

**Paper Fact（与 idea 分开）。** 论文类型是**结构归约工具 + 小基例分类**：通过保持可行性的 packing、splitting、pruning、extraction，把共同 laminar 约束拆成 uniform 部件与有限 key 部件，再以反向 envy 次序拼接。四人的残余部件只有下面两种。原三人“让第 i 人的 top i goods 分散进不同 bundles”的充分条件不能直接移植，Lemma 12 已给反例。论文还指出，对 graphic/gammoid 的纯 partition-reduction 色数损失界已 tight，不能仅改进该界来获得一般 EF1。

**准确输入、量词与目标。** 对任意四个非负 additive 估值向量及任意指定次序（可固定为 1<2<3<4），寻找完整分配 A，使每人拿独立集，并且

\[
v_i(A_i)\ge v_i(A_j)-\max_{g\in A_j}v_i(g)\quad(\forall i,j),\qquad
v_i(A_i)\ge v_i(A_j)\quad(\forall i<j).
\]

K8：8 件分成大小 (3,3,2) 的三个类别，各类每人 cap=1，总 cap=2。完整性迫使每人恰好两件。K12：12 件分成四个大小为3的类别，各类 cap=1，总 cap=3，每人恰好三件。若两块均有上述加强版，原归约给出任意四人 4-colorable 共同 laminar 约束的完整 EF1；不是一般任意人数 matroid 猜想。

**我们提出的 idea。** 不再强迫 top-i 分散，直接覆盖数值比较形成的多面体区域。K8 全部标号可行分配只有864个，即36个无标号 partition；K12 为31104个，即1296个无标号 partition。先为每个 partition 按指定次序让人选择剩余最优 bundle，自动满足 ordered no-envy，再寻找一小组 partitions 的比较区域覆盖全部估值域。若需机器辅助，直接编码“存在一个非负估值矩阵，使每个可行分配都违反某条公平/次序不等式”；这是有限布尔组合的线性实数可满足性问题。输出可审查的有理反例或不可满足性证书，再抽取人工可读的交换引理。

**首个承重义务。** 必须首先证明/否定 **K8 的 universal ordered-EF1**，包括零值与 ties。不能把 36 个 partitions 的逐次挑选成功于随机数据，误当作区域覆盖证明。一个可独立检查的初步任务是给出 K8 的有限 partition 菜单及完整覆盖证书；只有 K8 成功后再投入 K12。若 K8 失败，精确反例仍有价值：它否定公开建议的加强路线并定位“局部组合条件比普通 EF1 强”的障碍，但需确认反例不被更简单条件解释，不能包装成普通 EF1 不存在。

**玩具计算（已执行）。** `toy_checks.py`、`toy_results.json`。seed=20261020；K8 检查5000个估值矩阵（1667均匀0..10、1667二值、1666随机2幂），每个矩阵枚举全部864个可行分配；均有证人，最少6个。K12 对500个矩阵枚举全部31104分配，均有证人，最少256个。另完整复现 Lemma12 的 top-i 分散要求：可行分配数为0。这说明旧充分条件确实过强，同时数值 EF1 未在这些样本中失败；**没有得到连续估值域的证明**。

**为何值得/危险在哪。** 价值判据是能否以新有限交换/覆盖机制推进公开的四人 laminar 定理，而非仅提高小实例搜索速度。最危险的是作者已尝试计算辅助而失败；连续估值的比较区域可能指数爆炸，K12 尤其如此。只有“K8局部定理+可扩展结构”或“两块全解→四人全类”才足够独立成文；纯5000样本不够。无需承诺20天解决，可以在很早的承重义务上及时止损。

## FG02：goods-with-copies 的 SD-EF1（深入）

**母论文与明确公开问题。** Cookson、Soroush Ebadian、Shah，*Constrained Fair and Efficient Allocations*，AAAI 2025；作者完整版本 <https://www.cs.toronto.edu/~nisarg/papers/constrained-fair-efficient.pdf>，arXiv <https://arxiv.org/abs/2411.00133>。定位：§2.1 定义副本约束；§3.3.2 Theorem 6 排除一般 partition matroid 下 SD-EF1，随后 “Open Question: Does there always exist an SD-EF1 allocation of goods with copies?”；§3.3.1 Theorem5说明 constrained MNW 的1/2-EF1不能直接提高。web refs：`turn28view0`、`turn35view3`、`turn108view0`。本次按完整题名、SD-EF1+copies 与2025/2026组合反查，未检出后续解决；这不排除未索引论文。

**Paper Fact。** 类型是**工具迁移 + 边界分类**：加性约束估值转成 weighted matroid rank，利用 marginal EF1 导出1/2-EF1；complete allocation 与 free disposal 必须分开。副本模型是 partition matroid 的真子类：同类型副本对每个 agent 等值，每人每类型至多一件。一般 partition 的负例依赖类别内不同价值，不能直接当作副本负例。

**精确范围。** n 人、t 个类型，类型 g 有 c_g∈{1,…,n} 件，每人对类型的任一副本取同值 v_ig≥0；完整分配。希望每个 agent i 对所有 j 和自己价值排序的每个前缀 P 满足

\[
|A_i\cap P|\ge |A_j\cap P|-1.
\]

类型计数至多1，因此可把 bundle 视为类型集。此条件等价于删去 j bundle 中对 i 最优的一件后，i 的 bundle 在 i 的序下随机占优，即 SD-EF1；它对所有与该序一致的非负 additive 估值都有效。目标先收缩到 **n=3、任意类型数**；这时 c=3 的全体副本在比较中抵消，非平凡类型仅 c=1/2。

**我们的新视角。** 用矩阵 x_ig∈{0,1} 表示是否拿到类型，列和为 c_g。完全平均的分数解 x_ig=c_g/n 对全部前缀比较恰好无 envy，问题是能否把它舍入成前缀差≤1。普通逐人相对平均值的误差≤1只给两人差≤2，不能推出本题；必须利用成对交换。n=3 时将 c=1 看成选中一人的正颜色，c=2 看成未选中一人的负颜色，问题成为带正负类型的三色前缀平衡。尝试用交替路径/环，在保持列和的同时消除最早违反的前缀；每次修复必须有单调势函数，防止在另一人的排序前缀上反复破坏。

**首个承重义务及最小玩具。** 先证明 n=3 的混合 c=1/2 前缀修复引理，或找最小反例；不要额外加 PO（SD-EF1与PO在其他模型已不相容）。n=2 是简单 warm-up：全体副本抵消，其余为无约束单件，round-robin 给 SD-EF1，不能把它当主结果。真正的第一次困难是三个不同排序与两种 multiplicities 同时出现。候选交换应逐项检查所有已满足的更早前缀，不能只检查当前 pair。

**已执行的可证伪测试。** `copies_exhaustive.py`、`copies_exhaustive_results.json` 对 n=3、4个非全体类型、每类 c∈{1,2}，固定 agent1 顺序以消去统一类型重命名后，穷举 16×24²=9216 个 profile；每个 profile 全枚举81个分配，均有 SD-EF1，最少9证人。ties 可先任意细化再回到原弱序；更少类型可补所有人排最后的虚拟类型后删除。因此该有限检查覆盖≤4非全体类型，但尚无独立形式化证明。另 seed20261021：n3六类型[1,1,2,2,2,1]随机5000组（每组全729分配），n4六类型[1,2,3,1,2,3]随机2000组（每组全9216分配），均无反例。

**价值与反方。** 分类价值必须是利用“同类副本等值”跨越一般partition反例，给三人定理、任意人定理或结构性最小反例；小型有限穷举本身不够。危险是此前缀系统并非显然 TU，逐类 round-robin 的误差可能累积；可行的分数点并不提供整数证书。图/两顺序 discrepancy 的现成界若只给2误差，也不能换符号宣称解决。

## 其余存活候选：范围、工具、承重义务

**FG03 两类约束下 EF1+fPO。** 母论文 Cookson–Shah–Paritosh Verma 2026，<https://arxiv.org/html/2608.06325v1>，§5 Theorem2、§7 Open Question2（`turn81view0`、`turn89view0`）。类型：**新视角/组合工具**，正权 welfare optimal face 保 fPO，KKM挑共同权重，价格 prefix-interlacing 把多个证人合并。Paper Fact：balanced 与 uniform 约束已解决；一般类别仅能每类删一件。我们题目先固定3人、两类各3件、每类cap1，问完整 EF1+fPO。新idea是同步两类的alternating cycles，使总共只需删一件。第一义务：同一正权 optimal face 中，证明可选两个类别交换方向让“最大删除缺口”只落在一类；或者给该6件模型的精确反例。玩具为36个完整可行分配与其正权支持锥，适合有理LP枚举（本轮未运行）。价值是推进原文OpenQ2最小真正跨类情形；危险是单类证人可以不兼容，若只是EF1^cat则重复Theorem2。

**FG04 两类上界的2/3-MMS。** Hummel–Hetland，JAAMAS2026，<https://link.springer.com/article/10.1007/s10458-026-09731-1>，§8讨论高值物品与剩余可行性障碍（`turn33view1`、`turn55view1`）；最新邻居 Kinoshita–Igarashi 2026 <https://arxiv.org/html/2602.08966v1>，单类上下quota2n/(3n−1)、多类n/(2n−1)（`turn77view1`、`turn81view1`）。类型：**约束适配工具**，类内ordered reduction、可行reduction及bag-filling。新idea：只有两类时，将高值goods的overlap压成二分匹配，再让剩余低值袋子交换；目标所有n、两任意类别共同cap、非负additive的polytime2/3-MMS。第一义务：给高值匹配分配后，对每个未满足agent保留其2/3基准与剩余可行性，不能以总剩余价值代替MMS。玩具：n3、两类、每类4-6件，精确枚举MMS partitions检验候选reduction（未运行）。反方：两类并不意味着agent偏好overlap简单；单类2/3已知，有限n的存在界也可能超过2/3，故仅“3人存在2/3”不具新意。

**FG05 m=n+2 的最小EFX计数。** Neoh–Teh AAAI25，<https://arxiv.org/pdf/2504.03951>，§3、§6与Appendix D.1（`turn35view1`、`turn55view2`、`turn56view4`）。类型：**计数视角 + 分类**。Paper Fact：m=n+2时下界n、上界n²；n≤4有恰n的例子，n5作者随机搜索最低14；Conjecture6.1的一般“至少n”不能拿来当小题，因为蕴含一般EFX存在。我们的安全切口仅固定m=n+2，寻找所有n的tight构造/更强下界，先判n5m7是否能有5个。首义务：把EFX0计数在至多两个double bundles的分配形状上精确表示，确认零值/ties与分配标号约定，然后用线性不等式证书优化计数。玩具先复现Appendix D.1的n3/n4整数矩阵，再搜索n5（本轮未运行）。价值须有可推广的构造或极值结构；只把14降成13很可能不足独立成文。

## 已淘汰候选及可保留工具

- **FG06 强EFX可定向图分类。** Zeng–Mehta AAMAS25 <https://arxiv.org/abs/2404.13527>（`turn12academia16`、`turn25view0`）提出χ≤2正、χ>3负与χ=3边界，类型为分类。Jinghan Zeng 2026-09-29/10-01 <https://arxiv.org/abs/2609.36498>（`turn66search0`）已给完整多项式分类：连通图或二分，或仅一个非二分block且该block有内部度2顶点v使G−v二分。原切口已解；工具是block分解与局部障碍。若转多重图，第一义务要先决定“任意端点权重”的定义；两点多平行边已有容易障碍，不能机械扩类。本轮不启动其玩具搜索。
- **FG07 多重图cancelable EFX。** EC23图分配母问题及2025 bipartite/triangle-free工作后，Afshinmehr、Ashuri、Mahmoudkhan、Mehlhorn、Shahrezaei 2026-06 <https://arxiv.org/abs/2606.18665>（`turn68view0`、`turn123view0` §1.2）已解决任意多重图cancelable，包括additive，多项式。类型为突破/组合工具；可迁移单位bundle分割、envy路径rerouting与dumping。原“有三角形的additive多重图”不再新；若改一般monotone必须面对2026 submodular EFX负例而重定支撑域，不能无条件扩类。原问题无待做proof obligation。
- **FG08 相同估值的一般matroid EF1。** Akrami–Liu–Raj–Végh *Matroids are Equitable*（SODA/Combinatorica2026）解决未加权集合平衡；后续 Bérczi–Liu–Reis–Tarnawski 2026-08 <https://arxiv.org/html/2608.13983v1>（`turn19view2`）已用localized exchange、truncation continuation证明一般weighted equitability并给bundle-dependent EF1。类型为强工具突破。旧相同additive题淘汰；值得给指派线的是prefix-constrained matroid/GAP与稀疏discrepancy，而非重复同权EF1。
- **FG09 三估值类型balanced EF1+fPO。** Kawase–Mahara AAAI26 <https://arxiv.org/html/2603.05956v1> §6提出超过两类型（`turn56view2`）。但 <https://arxiv.org/abs/2608.06325>（`turn77view0`）已证明任意additive的balanced存在性，故扩类旧题已解。若改算法，准确新问题是任意n的pseudo-poly算法，原文§7 OpenQ6；固定n naive DP不算突破。新首义务应为价格交错face的可构造定位，而不是再证明两/三类型存在。
- **FG10 simultaneous fairness提速。** Akrami–Rathi AAAI25 <https://arxiv.org/html/2409.01963v2>（`turn33view3`）把2/3-MMS与partial EFX/full EF1结合，类型为工具组合。Akrami–Ashuri–Mehlhorn 2026-10-11 <https://arxiv.org/abs/2610.15437>（`turn68view1`）已经polytime实现exact EFL、(1−ε)-MXS、2n/(3n−1)-APS，exact MXS有pseudo-poly，阈值计算有弱NP难障碍。泛泛“同时MMS/EF1+提速”淘汰；若研究exact RMMS、依赖n或新约束，应另建精确候选。本轮不把更换符号计为创新。

## 对20天资源的使用建议与停止条件

先以 FG01-K8 和 FG02-n3 两个承重引理互相 battle，而非并行攻一般EFX。FG01第一轮需有完整反例公式、独立核查器及原Lemma12复现；FG02第一轮需有真正保持前缀的交换引理，或最小反例及其全分配证书。若只得到更多随机样本，不能升级“可解性”；若算法只给逐类误差、两单位前缀误差或任意次序不受控的EF1，则记录失败并回到精确命题。

已与 chores 线同步2026 chores EFX/EF1+PO新进展，图混合manna交给对方；已与 generalized_assignment 线去重 Santa Claus/knapsack，交付 weighted-matroid-prefix 工具。跨线 battle 已收到前两名模型，待其独立反查。

## 可复现文件

`toy_checks.py` → `toy_results.json`；`copies_exhaustive.py` → `copies_exhaustive_results.json`。均使用整数运算与全枚举分配，没有浮点公平判定。另 `verify_frozen.py` 对五个冻结最小证人实例用独立的纯 Python 标量实现重新枚举，证人数6、256、26、106、9全部一致，结果见 `independent_scalar_verification.json`。第一组是随机估值/偏好样本；第二组是明示有限域的穷举。没有宣称一般定理、独立同行验证或新颖性认证。


## 代码与冻结证据的仓库位置

本报告的脚本位于 `tests/audits/topic_selection/fair_goods/`，输出位于 `evidence/runs/topic_selection/fair_goods/`。复现时复制脚本到新的临时目录运行，勿覆盖冻结输出；完整索引见[本轮复现与核验](../VERIFICATION.md)。
