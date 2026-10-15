# 失败机制与可回收结果

| 尝试与关键机制 | 具体失败或限制 | 排除范围、回收与重试条件 |
| --- | --- | --- |
| 奇环所有 aligned light 强制偏离，再用 odd hub 覆盖 | [精确 T_d 包络](../current/weighted_congestion/odd_ring/cohort_lower_bound_and_envelope.md)限制全部这套正测试，多项式混合不扩大 | 证书上限本身仍非存在证明；但新增[第10节](../current/weighted_congestion/odd_ring/cohort_lower_bound_and_envelope.md#10-一般群组奇环实际阈值与正测试包络一致)用稳定区间/双取向/平移消去独立证明一般cohort实际阈值恰T_d。该同权同费奇环内即使放弃UF也不能放大；需改变承重拓扑/权/费用合同 |
| 同一重轻两列拓扑靠调参或多项式变强 | [完整拓扑还原](../current/weighted_congestion/source_topology/symmetric_two_column_reduction.md)在精确倍率范围还原到源族 | 异权和非对称资源不在范围；有限 crossover 给分离 |
| 固定小支持 gadget 重复堆叠 | 资源潜在用户数 r 有 r-PNE 的总成本证明；[三玩家例](../current/weighted_congestion/quadratic_triad/three_player_integer_obstruction.md)不可能独自给随 d 无界的下界 | 需增长用户支持或改变机制；有限例仍可复用 |
| 自然 complementary multicolumn 扩展 | [平衡轻玩家状态](../current/weighted_congestion/multicolumn/complement_column_escape.md)提供两倍逃逸 | 只排除此拓扑的放大；非所有多列构造 |
| 仅通过优化有序分组的潜在尾部参数A求统一界 | [两权级锐式](../current/weighted_congestion/weight_bands/ordered_tail_freezing.md)给min A=min{H,(1+K/H)^d}；K=ceil(H²)时固定次数仍随H无界 | 只否定此A包络控制；同一游戏有全空精确PNE，不能推断冻结程序本身选坏状态。可回收阶段Shapley拼接；[双排序混合势](../current/weighted_congestion/weight_bands/two_weight_order_blend.md)已给两权整个子类统一平方根次数界，故参数无界不能外推为该子类存在性障碍；实际占用或重开早组改变合同后可重试 |
| 保留统一固定低漏、只靠更深或更密DAG放大阶跃源 | [精确路径预算](../current/weighted_congestion/polynomial_curvature/dag_low_leakage_budget.md)把检测可行性化为z(z−1)ΣP_kz^(k−1)≤1，原step阈值至多O(√d) | 只限制所列低高端点；不控制过冲或实际多项式β。可回收最小/slack权表示；异质泄漏、改权或直接全状态机制需另证 |
| 固定step-DAG极值幅度，只改多项式曲线以利用过冲或漏费 | [实际全入状态界](../current/weighted_congestion/step_dag/polynomial_extremal_all_in.md)在p0(1)=A,pv(1+wv)=A h_v(q_D)下给d≥16的4√(d/ln d)-PNE | 直接处理所有玩家真实偏离，但仅限该锚定幅度；任意幅度未被排除。回收缺口矩Σh_v(w_v−outsum)<1/q与Jensen；改幅度/选其他light集合时需新证明 |
| 固定正权向量，仅把所有正次数提高 | [高次份额势](../current/weighted_congestion/high_degree_share.md)证明，即使拓扑与系数变化，最低正次数趋无穷时近似保证一致趋1 | 排除这一纯高次放大路线；权向量随次数变化或保留低次项不在范围。必要小份额仍非充分反例 |
| 保持 crossover 权和系数只提高次数 | [degree40 与精确极限](../current/weighted_congestion/crossover/README.md)已有较低因子均衡 | 缩权和调幅可重试；固定四玩家仍只能给常数 |
| 稀疏权谱下模拟阶跃坏博弈 | [曲率](../current/weighted_congestion/polynomial_curvature/three_load_curvature_bound.md)与[密度存在界](../current/weighted_congestion/weight_density.md)限制对应保持结构的替换 | 引入稠密 cohort 或改变覆盖结构时另行研究 |
| 同资源密集尺度固定 power 乘子拼接 | [仿射路径](../current/weighted_congestion/power_bridge.md)在固定 p<1 下无统一夹逼，另有 sharp 两类型损失 | 不是博弈无均衡；允许实例相关乘子、跨资源支付等须另证 |
| 窄权带单独归一化 Shapley | [mixed difference/curl 与 selector 线性损失](../current/weighted_congestion/weight_bands/README.md) | 限指定势与归一化规则，不反驳全类次线性存在 |
| 任意固定玩家乘子及依游戏可分序势覆盖全部改善边 | [有限多尺度与固定资源束证明](../current/weighted_congestion/separable_ordinal_obstruction.md)已独立重构攻击；扭曲门槛ρ_d/d→1 | 只否定边际夹逼和全改善边可分序势；全空仍为精确均衡。非可分势、选定改善步或全局极小点接口改变时可重试；普适复制桥其他推论仍各自核对 |

失败本身有价值，但不得悄悄扩大否定量词。程序失败和有限搜索无结果没有数学真值含义。

## 正展开提取中只取底背景的稳定预算失败

[正占用核](../current/positive_kernels/occupancy_rank_faces.md)中，底背景q差分虽在有限正锥精确判秩，但n≥q+2的full-support归一化k次核使全部这些差分趋0，极限unanimity仍秩n−1。失败是遗漏高背景，不是数值精度；因此该测试没有无界次数统一gap，且不能交换闭包截面。改取顶背景可回收显式锐gamma与稳定删除；不排低次数的大支持线性资源，更不改变全类均衡状态。零质量反边界必须计算所有active坐标，不能漏掉零质量观察者。

## 序势障碍不能外推到任意依游戏最小点选择

可能的错误延伸是：既然资源可分目标无法对全部α改善严格下降，就断言任何资源可分目标均不能选出α-PNE。[精确等价](../current/weighted_congestion/separable_ordinal_obstruction.md)第四节否定这种延伸：入射距离唯一选择任意给定合法状态。因此只要求依游戏目标的全部全局最小点为均衡，与该游戏均衡存在本身等价。可回收的是精确量词边界，不是更强无势或无均衡结论；若要求单调、费用局部、跨游戏同规则或非循环有效构造，则需另立并验证这些新增条件。

## 全状态dual的平稳或回返支撑限制

尝试把原dual概率取成selector单位速度链的平稳概率，会引入原替代不要求的流量方程。[明确增长反障碍](../current/weighted_congestion/template_certificates/stationary_selector_obstruction.md)在仿射费用已让该条件的必要倍率无界，尽管原dual和exactPNE存在；具体失败是轻重移动访问频率不匹配。放宽为任意回返状态支撑也恰好要求全模板αFIP，强于只找PNE。可回收的是仿射循环按移动者权重重加权，以及回返支撑的准确量词。允许暂态质量或另选持留率时应重新研究，不受单位速度否定直接覆盖。

## 有向分叉的统一强迫放大

把一个light复制出多条私有双人side以影响多个hub，仍共同占用其唯一main强迫预算。[割均衡定理](../current/weighted_congestion/directed_fanout_forcing_cut.md)在弱UF及α≥T_d用加权割平衡入反馈，给全anti真实PNE，所以此准确拓扑和假设内无法放大非存在。失败是结构上已有均衡，不是浮点搜索失败；异权、异形side、并行和selfloop均被覆盖。可回收工具是预算不等式与正部割；UF失败、同一side含多hub、action-asymmetric副本或多主源改变承重条件时才值得重试。它不排除这些类外机制，更不证明全类上界。

## 全部改善终止与共同幂混合选态的两种真实失败

[循环窗口复制](../current/weighted_congestion/cyclic_clone_improvement_cycles.md)先补连接测试、重新求有限gain锥，再以逐人圆周秩实现真实近d环，故旧局部循环实现义务已闭合：任意全局函数也不能对全部严格α改善下降（α<ρ_d）。这是方法失败而非无均衡，因为全空精确PNE保留。可回收循环lift与连接guard；只选部分改善步、非循环地选全局最小点仍可重试。

[共同幂混合](../current/weighted_congestion/common_power_mixture_obstruction.md)在一个四玩家游戏中用同一严格正分离击败全部非负μ，而非把逐单幂坏例交换量词。失败精确限于保留原a_e、资源共同μ的目标族；固定背景消去后的新规则、资源分别归一化或集合型目标尚未排除。回收点态分离再积分的全局最小点攻击工具。

## 用已有近d环直接否定全类：缺失的是次数预算

原先直接把改善环当无均衡的推断仍无效，因为全空精确PNE存在。[锚定三元锁定](../current/weighted_congestion/anchored_cycle_lock.md)现在通过限制回两个动作并新增资源，解决指定双轮环的全状态出口，但输出次数q=max(p,D)，D依δ、B/η、n。具体失败步骤是把原环倍率α≈p直接当作输出次数q上的倍率；尚未证明α ln q/q无界。可回收的是完整全状态编译与确定first-opposite修复。可重试条件是改善次数预算、另造更均衡且余量可控的输入环，或另用不受当前统一δ估计约束的锁定机制；这里没有证明所有时钟不可能。

## 在原次数内仅调锚定三元费用

尝试为每个anchor0三元自由选择同pair同费非负多项式而保持p。失败不只是统一δ估计松：[显式三次基体](../current/weighted_congestion/anchored_clock_degree_barrier.md)的12列非负锥有精确整数dual，只需两条sweep弱margin≥0就强制0101/1010所有偏离margin<0。准确范围是该基体、anchor、phase、同费pair、degree≤3；不否定O(p)常数倍degree。可回收有限列分离及允许非均匀幅度的攻击接口；重试须改次数预算、拓扑、相位/两侧费用或基体。

## 用固定者、必选资源或包含动作承担全类难点

[空交反链核心](../current/weighted_congestion/template_certificates/integer_counterexample_normal_form.md)给alpha-independent lifting，严格反例可剥掉上述部分；不能把它们当作无界可动类别桥本身。具体易错步骤是把原成本中的共同非负K直接当成core成本，反向投影对α>1会失败。可回收单向提升及整数展开；若路线要求保人数、所有原均衡投影或精确最佳因子，须重立并证明新增合同。

## 在统一低泄漏clock预算内继续优化输入环

尝试用近p倍率双轮环、换anchor或优化B/η/n，再沿δ^D≤η/(4α²BL)得到超q/lnq全状态反例。失败机制现在有[普适证明](../current/weighted_congestion/uniform_clock_budget_barrier.md)：完整MODEL的strict R-FIP迫使R>α，任意anchor含全局极大极小三元给δ≥(R+1)/(R+2)，因此所有满足该预算的D都超2(α+1)ln(2α)，实际次数q≥D有αlnq/q<α/(α+1)<1。无需重复极值，也不要求α趋无穷。可回收R-FIP/极端三元/一元单调性接口；只封闭该充分预算的输入调参，重试须使用actual新旧clock差、逐三元不同预算或新全状态机制。没有证明该预算必要或游戏本身有q/lnq-PNE。

## 类内同权锁定后假设不同步前沿自动有出口

尝试仅在同权clone类内加clock避免global极差，再把每类prefix/suffix合法性当全局sweep。[12player反例](../current/weighted_congestion/class_front_phase_quotient.md)有strict24步环却在phase(0,4,0)六端点全稳定；任意递增同权010/101 clock在留front边old=new，不能新造出口。失败步骤正是未证的全front base出口，不是一般clock不可能；内部clone仍有改善。可回收扭转phase商、2N费用表和literal反例；重试须明确处理错位同步或保留/控制离front出口。

## 用低阶局部一致矩替代完整selector支撑多面体

[局部矩精确接口](../current/weighted_congestion/template_certificates/selector_local_moments.md)说明资源测试只看≤d对手，但可行feature必须来自conv{Ψ_h(s)}。擅自删掉全局selector-support兼容性会扩大可行集；D维或小支撑只改表示，未证明每selector可行。可回收张量基、正锥消元、dual小支撑和parity暂态例；重试须对真正凸包与资源极锥给统一相交证明，不可把parity例当暂态必要。

## 共享侧强迫与真实时钟预算的新边界

- 仅把私有side改成共享多个同权hub、仍保留unique-light/source和最坏负载UF，不能自动突破现有量级：[截断Rosenthal势](../current/weighted_congestion/shared_side_truncated_potential.md)给A_d≤2d/ln d的全antiPNE。原私有割不能直接迁移，但α倍纯hub底势与正部补偿支付source重置；可回收AS+B判据，不排异权hub、跨source多light或预算失败的真实游戏。
- 直接替代uniformδ时，不可把[保环S总预算](../current/weighted_congestion/anchored_clock_actual_margins.md)当充分可行性，也不可把firstopp出口失败升级为稳定态。新κ条件才同时控制全部玩家，且仅为充分稳定条件；固定三次基体上较旧dual弱。43次稀疏实际证书及同稿所接原全三元统一M的80次证书对照uniform91，后者另证明(U)对原架构本身也非必要；只说明保守预算有损，不能否定已证uniform预算障碍，也未给一般常数倍degree或最优43。

## 动态层秩不能直接拼成同一全局势

[共占高度接口](../current/weighted_congestion/weight_bands/finite_weight_class_potentials.md)沿全局固定相容秩或整闭词端点图给三角边际。逐步把当前活跃层重排会改变势本身，势降不能望远镜；没有证明每次能选到不扩张累计height的改善边。两相同资源已有精确PNE但全部状态实际height随人数增长，故“找低单点height态”也不是一般必要步骤。回收的是固定图/端点图相容性；可重试条件为证明高链SCC有出口、累计移动者图可控制或直接构造瞬态dual，不能从长链推无PNE。

## 从低阶成本空间直接推出小用户支持资源表示

尝试先用degree≤d的低阶张量空间，再把每个cost interaction项当成只依赖少数玩家的合法正资源，从而降到有限interaction结构。[异权仿射全签名刚性](../current/weighted_congestion/template_certificates/selector_local_moments.md)给精确失败：V_i=s_iΣ_jw_js_j仅degree1、任意n≥2且权不全等，但一对异权的零contrast排掉共享高次，solo成本饱和迫全部正资源全用户且费用a_e x。任意提高有限degree仍不能全保真缩支持；正锥约束不是线性cost-space维界。等权pair高次表示说明不能删权假设。可回收≤D资源数量压缩、局部矩极锥和一般完整成本张量界；本障碍不排改权、加辅助玩家、仅保均衡/单向lift或近似成本归约。重试这些路线须重新写清并证明较弱保真合同，不能把本例有精确PNE误作全类反例。

## 允许有限近似和改权后的小用户支持全成本归约

尝试把degree低的完整cost table近似拆成统一有限支持r，再调用r-PNE。新[定量收费下界](../current/weighted_congestion/template_certificates/selector_local_moments.md)允许表示方改正权、提高任意有限degree，仍有β≥m(1+ε)/[(r−1)(1+mε)+mε]；固定r,β取m和正有理ε即失败。失败步骤是每个light在singleton到heavy-pair的成本跃升都需共享资源支付，而每条heavy小支持资源至多覆盖r−1名light，预算由heavy全入成本控制。回收pair收费与对称A²缩放；只限制相同玩家/标签的完整成本夹逼。原例全0 exactPNE，辅助玩家、只保均衡/单向lift及选择性成本保持仍可重试，不能把这一障碍说成无均衡。

## 同类有序三元时钟不能通用锁定全部严格环输入

旧不同步反例只缺front端点出口；新[64资源actual系数基体](../current/weighted_congestion/class_front_phase_quotient.md)本身就在phase(0,0,1)具有全部玩家严格exactPNE，同时保有strict21/20双轮环。所有类front在任意递增三元上非010/101，所以所有玩家翻位时clock负载只为2w→2w或w→3w，任意fresh同费非负非减三元clock叠加仍保留PNE。具体失败是时钟完全无法新增该front的任何真实出口，而非次数选择不足。回收front精确PNE局部引理和显式有理基体；跨类、其他arity、非对称副本、辅助玩家或更高倍率专用输入类尚未排除。仅加次数/幅度不能修复本输入；不把固定反例外推为全部近线性环都有稳定front。

## 跨source共享侧资源也须超出准确强迫合同

[新真实Rosenthal势](../current/weighted_congestion/shared_side_truncated_potential.md)以κ_d(t)=min(dt,t+1)控制已有外场上的重置增量，闭合此前TR仅从零外场出发的缺口。在同权hub及按side全部light总权的UFmulti下，任意跨source共享仍有1+√d-PNE。 同稿第九节进一步分离UF强迫τ与目标α，(τ−1)(α−1)≥d即足够；因此达到目标量级也不需把强迫倍率提高到目标倍率，τ=1+ln d已给α=1+d/ln d。 v2进一步给α=d/ln d，且τ≥d+1可取精确PNE；均仍是同权/UF子类充分条件。 v3再用side增量把条件降为ατ≥d并纳τ1，τ=ln d即可给目标量级；独立2玩家四状态证明τ=d是保证exactPNE的sharp强迫边界，不能据此声称α>1乘积域必要或全类下界。可回收reset预算和源超可加估计；不覆盖异权hub、非UF或多个main source，负向若只保全部该合同便不能放大。此为结构存在定理，不是全类上界。


## 仅依结构参数给actual保环时钟统一次数

尝试摆脱uniformδ预算后，直接要求次数cap只依p/n/权谱/α。失败发生在真实环余量：[actual接口第九节](../current/weighted_congestion/anchored_clock_actual_margins.md)对每cap构造同4玩家/同权/同α/p3的空交反链基体，以动作专属private三次成本压低全部环margin而保持0101/1010稳定gap；必要ΣS预算趋零，固定cap逐列效率有界，任意允许非统一clock只要保全环仍保这些均衡。系数幅度和资源数保持有界，不是无限幅度问题。可回收actual预算和padding压力测试；重试须控制特选输入的余量/稳定gap或改变架构/放弃保环，不排健康余量增长族或全类目标。

## 把完整proper锥的dual自动限于recurrent或点质量

旧子锥反例不能单独排除“完整锥会强制recurrent解”的希望。[local-moment第11节](../current/weighted_congestion/template_certificates/selector_local_moments.md)把低阶parity暂态dual与唯一真实strict坏环同时植入完整proper锥：任何dual必须有正暂态质量；singleton常数列又排除所有点质量。新增范围是无删列/无共同sink，不是任意selector可行法；实例质量下界依η/M，没有统一d估计。可回收同时化路由和概率质量分离，重试仍须处理任意selector的真正feature hull，而非交换singleton例的量词。


## 将全状态择证对偶截断为固定数量移动者

尝试用少量玩家的方向矩匹配或局部transfer覆盖每个selector，再拼成全类证书。[奇环缺陷择证](../current/weighted_congestion/template_certificates/selector_local_moments.md)给出具体失败：等权奇n、任意d≥1与1≤α<2^d，两个proper邻边degree-d列迫相邻移动者质量互相为正，私人常数列再迫每个方向正质量；最小状态支撑恰2n而n任意大。原selector有显式α1 dual，故失败是人数截断而非全类dual不可行或无均衡。回收的是完整补偿链、定量质量界及min-index的2^d锐边界。重试必须允许无界数量玩家、证明可控全局transfer或使用依模板/D的支撑界；不能把本例当作主目标否定。

## 把异权hub直接当同权Rosenthal边际

[局部异权排序侧势](../current/weighted_congestion/shared_side_truncated_potential.md)第十节用降序前缀取代真实同权计数；凸性给边际[G,(a/A_j)G]，源重置另付K。原exact marginal不能原样使用：配套审查有三hub整数二次side-only游戏，八态均有strict改善。即使只分析新排序势，其单副本R损失在线性例的比值(n+1)R/(R+n)→R，故不能从该夹逼直接消R。这不是全类存在障碍；单side锐式例由最小绝对负载差给exactPNE，pair-only仍受既有2-PNE界覆盖。可回收排序边际/κ重置和局部R/K充分界；重试需利用副本差额或新选态，并重新证明全部真实偏离。

## 只改取降序侧势的全局最小点来删除局部R

第十节原边际锐性只限制逐副本夹逼；现在[第十一节完整线性游戏](../current/weighted_congestion/shared_side_truncated_potential.md)证明更强失败：n重n轻分离时，全部全局最小点精确由非负恒等式覆盖，且均有趋近R的真实改善，也均为严格局部最小点。因此global-min间tie-breaking不能修复删除α≥R的论证。该游戏仍有exactPNE，失败只限这个势的最小化；回收GlobalR恒等式和完整方法反例，换势或选择非最小状态时可重试。

## 将森林的递归稳定延续直接扩大到单环或多根

[森林归约](../current/weighted_congestion/incidence_forest_private_reduction.md)靠互不相交子树的固定报价闭合任意耦合策略。单环二玩家四资源已无exactPNE；循环共享会破坏独立报价，不能仅按某个根的响应重置后费用替代真实冻结偏离。保次数lift只覆盖每附属分量至多一个核心玩家；核心资源挂树或多核心接触需新合同。回收当前价相等/进入价下界接口，不外推全类失败。

全前沿条件编译没有修复strict sweep自动覆盖的失败：它另要求全部front保front严格出口，增长输入与B/η控制仍缺。

## 把固定hub的精确轻响应当成整个游戏的提升

[阈值响应接口](../current/weighted_congestion/fixed_hub_light_threshold_response.md)给unique-light、无UF的真实稳定light选态，但其势随hub向量改变，不能累计为同一全局势。原共享侧正文9.17两玩家例在每个固定hub都有精确light响应，重选后hub成本由补位对称相同，仍有真实冻结light的hub改善。因此失败是偏离合同和响应预算缺失，不是light响应不存在。多light共享side另由旧三玩家例直接阻止该exact响应推广；回收显式阈值势/单遍选择，下一步须支付冻结与重置成本差。存在/FIP为已知Milchtaich特例，新颖性不因重构升级。
