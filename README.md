# 共同研究：数学地图与唯一读取入口

本仓库保留三个数学模型，分别维护定义和量词。当前主要研究方向是**加权原子拥塞博弈的普遍近似纯均衡门槛**。新对话以本仓库为准，旧对话、公屏和交接副本不再作为研究状态来源。

**从这里查研究资产：[按问题进入研究总目录](research/README.md) · [全部中文资产名、路径与用途](research/CATALOG.md) · [当前未解义务](research/ROADMAP.md)。** 各专题入口给出证明链与阅读顺序；具体文件区分数学正文、候选、反例、独立审查、程序和冻结证据。

## Research Goal / Research Frontier

当前天团的具体题目是：**全类 O(d/ln d) 近似纯均衡存在命题成立还是不成立**。量词与唯一完成标准见[本题验收](research/weighted_congestion_frontier/ACCEPTANCE.md)，下述长期前沿和其他资产不另作本次完成目标。

加权拥塞的目标是刻画非负系数、次数至多 d 的多项式费用下的普遍存在阈值 a_*(d)。已收录的团队一般证明给出奇数环下界 T_d∼d/ln d；已核对文献给出普遍上界 d。**主目标仍开放：缺少匹配的全类存在上界，或超出现有强制偏离证书的新下界机制。**全球优先权与外部同行评审尚未认证。

研究详情从[加权拥塞数学入口](research/current/weighted_congestion/README.md)进入。[当前状态](RESEARCH_STATE.md)只列当前前沿；[精确命题目录](CLAIMS.md)连接真正的命题身份；[失败路线](FAILED_ROUTES.md)区分命题反例与方法限制。

## Mathematical Objects / Definition Map

| 模型 | 对象与定义链 | 权威定义与研究入口 |
| --- | --- | --- |
| 加权原子拥塞 | 正权玩家＋有限资源子集策略＋非负多项式费用 → 资源负载 → 玩家成本 → α-PNE → 全类阈值 a_*(d) | [MODEL](research/weighted_congestion_frontier/MODEL.md)、[数学资产](research/current/weighted_congestion/README.md) |
| 两阶段设施选址 | 设施布局＋可达关系＋正权原子客户 → 精确独立客户 NE → 完整续局 → 近似 SPE | [模型](research/current/model.md)、[成果地图](research/current/README.md) |
| 顺序客户吸引 | 共同主题目录＋单位客户 → 历史依赖纯策略 → 完整纯 SPE → 覆盖福利 | [独立入口](research/current/customer_attraction/README.md) |

模型间的工具迁移需要明确桥梁；目录相邻不表示定理互相适用。

## Claim Map / Dependency Graph

加权拥塞的核心链为：资源策略与真实偏离成本 → 奇环全状态证书 → 正系数闭环 → 有限有理构造 → T_d 下界。局部证书包络本身只限制该方法；新增[一般群组奇环实际阈值证明](research/current/weighted_congestion/odd_ring/cohort_lower_bound_and_envelope.md#10-一般群组奇环实际阈值与正测试包络一致)以稳定计数和双取向消去独立证明该完整拓扑阈值恰T_d，含强迫失败，但不是全类存在上界。固定权重和动作数的[签名压缩与全状态择证对偶](research/current/weighted_congestion/template_certificates/finite_action_duality.md)另给任意资源数的精确有限表示；仍缺统一于所有模板的估计。[严格反例整数规范形与端点](research/current/weighted_congestion/template_certificates/integer_counterexample_normal_form.md)消去逐固定实倍率反例的实参数，并证明a_*(d)端点可行；没有全类搜索规模界。[任意乘子与依游戏可分序势障碍](research/current/weighted_congestion/separable_ordinal_obstruction.md)已作完整重构及独立攻击，只否定所写全改善边证书；全局选态仍开放。 [空交反链核心](research/current/weighted_congestion/template_certificates/integer_counterexample_normal_form.md#7-去包含支配与必选背景的空交反链核心)进一步把反例限制为人人至少两非空、无包含、空交策略，并给所有α≥1同时有效的单向lift；允许删玩家，不给规模界。

其他模型的定义、引理、反例和算法关系以及加权拥塞已登记结果统一放在[数学超图](research/index.html)及[结构化图](research/graph.json)。`derives` 列全体共同前提；实验只用 `checks`，失败与限制分别登记。图是导航，真值以精确陈述及证明为准。

## Known Results

| 成果包 | 精确成果和剩余限制 | 何时读取 |
| --- | --- | --- |
| 加权拥塞奇环 | 无限下界及正局部证书的精确包络；线性重置与同次数两种实现，内部独立审查，未外审 | 当前研究必读[整合说明](research/current/weighted_congestion/README.md) |
| 加权拥塞工具 | 文献源族锐包络、完整对称拓扑限制、密度势、高次份额近精确势、[有序权组冻结与参数锐式](research/current/weighted_congestion/weight_bands/ordered_tail_freezing.md)、[DAG低泄漏预算](research/current/weighted_congestion/polynomial_curvature/dag_low_leakage_budget.md)与[极值幅度实际状态界](research/current/weighted_congestion/step_dag/polynomial_extremal_all_in.md)、资源局部势拼接、有限非对称分离与方法障碍；逐条审查等级不同 | 按具体义务选择[文件与状态表](research/weighted_congestion_frontier/FILES.md) |
| 双设施 | 共同目录尖锐 φ 及构造、稀疏异构尖锐 ρ、实例复杂度和四地点无 FPTAS；一般异构 2 保留候选状态 | [共同目录](research/current/shared/README.md)、[异构](research/current/heterogeneous/README.md) |
| 任意设施数 | 一般因子 2 存在性及有限构造；一般输入位多项式算法仍开放 | [主定理及算法前沿](research/current/multi_facility/README.md) |
| 顺序客户吸引 | 小人数和结构目录的福利上界、真实完整策略反例及安全值桥障碍；一般半覆盖仍开放 | [分支地图](research/current/customer_attraction/README.md) |

[两权类别双排序混合势](research/current/weighted_congestion/weight_bands/two_weight_order_blend.md)给全局两权、任意人数与权比的(1+√(4d−3))/2-PNE。它以互补精确边际绕过两权尾部参数无界，任意多权的全类桥仍开放。

[循环窗口复制的真实近d改善环](research/current/weighted_congestion/cyclic_clone_improvement_cycles.md)将旧可分势障碍提升为任意全局全边下降势障碍，仍有全空精确PNE。[共同幂混合最小点障碍](research/current/weighted_congestion/common_power_mixture_obstruction.md)另直接排除指定连续目标族的全部最小点。全类存在性仍OPEN；环本身不能当无均衡；[锚定三元全状态锁定](research/current/weighted_congestion/anchored_cycle_lock.md)已将严格双轮环编译成无α-PNE，但新增次数依实例。[统一低泄漏锚定时钟预算的普适次数障碍](research/current/weighted_congestion/uniform_clock_budget_barrier.md)已证明满足现行统一预算的全部输入均有α ln q/q<α/(α+1)<1；负向前沿须改用实际时钟差、非统一预算或其他全状态机制；[三次锚定架构证书](research/current/weighted_congestion/anchored_clock_degree_barrier.md)已排除在指定基体上保持原degree的方案，未排常数倍degree。正向仍需选步或超出这些目标族的选态。

[有限可动权类的三角排序势](research/current/weighted_congestion/weight_bands/finite_weight_class_potentials.md)已给A_(d,k)隐式界，固定k为d^(1−1/k)，任意固定背景精确吸收、k个R窄簇损失R^d。d≥16且k≤ln d/lnln d的明确子类达到2d/ln d；无界可动类别时A趋d，唯一全类题仍OPEN。真正前沿已收缩为无界可动权类的选态桥或全状态增长反例，不再把固定背景或仅两类稠密cohort当未解接口。

## Refuted / Failed / Open Problems / Next Actions

由拥塞局部成本正展开提取的独立主题是[正占用核](research/current/positive_kernels/README.md)：固定正质量的非负共享负载响应中，低交互秩给出次数/用户支持的联合过滤、顶背景差分的锐质量预算和准确闭包。正文含独立传感器实例、原作者及冻结来源；低次数大支持仍允许，一般签名与均衡桥另列，主目标保持开放。

[失败路线入口](FAILED_ROUTES.md)记录失败的具体断言、反例范围和回收工具。下一步从当前 proof obligation 出发选方法；已有路线是搜索种子，不是方法白名单。有启发的未完成 idea、卡点、类比和合作问题可自由在公屏研讨，注明不确定性即可；整理入库和重要 claim 升级仍分别执行原有规范。

## File Map / 工作程序

| 完整路径 | 内容、作用与读取时机 |
| --- | --- |
| README.md、RESEARCH_STATE.md、CLAIMS.md、FAILED_ROUTES.md | 全仓稳定地图、当前前沿、精确命题入口、失败范围；新对话首先读取 |
| [research/README.md](research/README.md) | 按数学问题分流的研究总目录；先选模型，再沿专题阅读顺序进入具体资产 |
| [research/CATALOG.md](research/CATALOG.md)、research/catalog.json | 全部现行数学正文、问题、审查及已整合拥塞核验资产的具体中文名称、完整路径与阅读用途；JSON 是人工命名源，Markdown 由程序生成 |
| research/GROWTH.md | 原有入库规范：证明、问题、代码、测试、输入、证据和历史材料的归属；写文件前执行 |
| research/REPOSITORY_GUIDE.md | 全仓生产状态、读取顺序、施工与上传、分支收口及交流规则 |
| research/weighted_congestion_frontier/README.md | 当前协作入口；连接数学、启动程序和按需读取路径 |
| research/weighted_congestion_frontier/FILES.md | 本轮逐文件用途、状态和去处；查具体成果、证据或待审项 |
| research/weighted_congestion_frontier/INTEGRATION.json | 各原分支 tip、文件来源/hash、当前路径与退役理由；只在来源审计与恢复时读 |
| research/current/claims.md、research/review_status.json、research/assets.json | 全仓逐命题范围与五轴状态、资产合同；修改或引用结论时查询 |
| research/current/ | 可连续阅读的现行数学稿；审查状态独立记录 |
| research/questions/、research/reviews/ | 开放义务与待审候选；已发生的审查及其覆盖范围 |
| facility_spe/、multi_facility_spe/、customer_attraction/ | 各现有模型的唯一规范程序，运行见 USAGE.md |
| tests/、examples/、evidence/ | 回归及独立审计、输入、冻结证据；运行不得覆盖冻结记录 |
| learning/README.md | 人类研讨学习路线与当前成稿；不替代数学权威稿 |
| history/README.md | 仍有来源价值的原稿及 Git 恢复指针；追溯时按需读 |

日常研究共同保存到 **main**。`wcg/board` 仅承担简短异步研讨；旧工作分支在内容入库并确认原提交可达后删除。程序不再创建随机会话分支。每个对话使用独立本地 clone，一个稳定发布标识，子 agent 无需登记；人数和工作时长不由提示词设限。

需要把当前研究交给 Pro 时，按[角色与交接顺序](research/weighted_congestion_frontier/README.md#角色与-pro-交接顺序)先由清晰者筛出必要事实与精确障碍、提取者核实按需工具，再提交实际数学材料。论文者独立负责成稿；提示词就绪和材料整理完成分别核验。

全类非势接口的两个准确边界：[择证平稳与循环支撑](research/current/weighted_congestion/template_certificates/stationary_selector_obstruction.md)区分概率dual与全改善终止；[有向分叉强迫割均衡](research/current/weighted_congestion/directed_fanout_forcing_cut.md)排除唯一源、私有双人侧资源在UF下越过T_d的放大。二者均未完成全类判定。

[有限次局部矩与全成本压缩](research/current/weighted_congestion/template_certificates/selector_local_moments.md)将签名接口细化为D维完整成本空间、≤D正单项式资源保真表示和≤D+1支撑dual；其仿射全签名刚性另表明：非全等权下，低degree成本不能保真拆成全小用户支持资源，即使提高次数。完整proper锥另可同时实现近d真实唯一坏环和完全暂态dual，任何dual暂态质量必须为正；这是已知两机制的同时化，不给任意selector方法。奇环缺陷择证另迫使任意α<2^d的dual同时覆盖全部移动者，两方向均有正质量，最小状态支撑恰2n；等权可行例已排除固定人数的局部补偿截断。真正未解仍是每个selector的moment hull与resource polar是否在统一倍率相交。[循环窗口前沿商与不同步反例](research/current/weighted_congestion/class_front_phase_quotient.md)提供相对phase表示，但类内clock不能自动给错位front出口，故负向仍需新同步/离front覆盖机制。两包均未完成唯一全类题。

[共享侧资源截断势](research/current/weighted_congestion/shared_side_truncated_potential.md)把同权hub、unique-light/source、最坏负载UF子类扩到任意共享hub子集，给A_d≤2d/ln d；独立AS+B判据覆盖部分非UF实例。[实际时钟差分与预算](research/current/weighted_congestion/anchored_clock_actual_margins.md)给非统一clock的O(n²)充分LP、必要总预算和κ稳定条件，固定四玩家43次证书优于原uniform91选值但不称最优。原全三元、统一M架构另有80次全状态证书却不满足(U)，故(U)对原架构也非必要；这仍不是增长族。实际接口另证：固定人数/权谱/α/纯三次亦可用private成本压低环余量，阻止任意预给degree cap的保环三元clock；健康余量增长输入仍未排除。真正缺口仍是无界可动权类的全类选态、跨source/预算外反馈或次数效率可增长的全状态族。

[共占图高度与实际改善环必要链](research/current/weighted_congestion/weight_bands/finite_weight_class_potentials.md)把三角势参数从全局权类数放宽为同一降权共占图的路径高度；全局权种数可无界。实际严格改善闭词也必须跨越相应高度门槛，各弧可来自不同端点。仍无全类高度控制；动态换秩改变势，缺少高链SCC出口或瞬态dual。

[跨源共享侧资源平方根界](research/current/weighted_congestion/shared_side_truncated_potential.md)在同权hub、唯一source、二元同费副本和UFmulti下，以真实Rosenthal势给1+√d-PNE，允许同一side含多个source的light；异权hub或强迫失败仍缺桥。[近似支持失真障碍](research/current/weighted_congestion/template_certificates/selector_local_moments.md)把完整成本小支持归约的限制扩到允许改权与有限乘性失真；[类内时钟编译障碍](research/current/weighted_congestion/class_front_phase_quotient.md)另有strict sweep却保留严格精确PNE的固定基体，任意次数有序三元同类clock不能消除此状态。后二者仅限方法合同，不是全类非存在；三项新身份、冻结审查及双路有理证据均由专题入口接入。

[跨源共享侧资源的重置增量预算](research/current/weighted_congestion/shared_side_truncated_potential.md)第九节的`WC-MULTISOURCE-FORCING-TARGET-TRADEOFF-v3`在同权hub、唯一main source、二元同费副本及原UFτ下给ατ≥d的α-PNE，允许τ≥1；d≥16取τ=ln d即得d/ln d。独立`WC-SHARED-SIDE-EXACT-FORCING-THRESHOLD-v1`又证明：该结构类保证精确PNE的强迫边界恰τ=d，任1≤τ<d均有2玩家全部4态反例。sharp只限α1，不称整个乘积域必要。v1/v2精确身份及原冻结证据保留，新RI经独立重构/冻结攻击和双路Fraction核验。全类仍缺低于对数级强迫或强迫失败时的稳定light/反馈控制、异权hub桥及无界高度非势选态，WC-TARGET保持OPEN。


[局部异权hub排序侧势](research/current/weighted_congestion/shared_side_truncated_potential.md)在UFhet下把跨source共享侧资源扩到任意多hub权类：侧内权比R与source到侧最小hub权比K满足α≥R、(α−1)²≥Kd时给全antiα-PNE。允许无界全局跨度，仍依局部比与强迫假设；没有全类C,d0。正文第十节接独立重构、凸性加强、精确边界与双路有理证据。

[异权重置增量与全局最小点边界](research/current/weighted_congestion/shared_side_truncated_potential.md)第十一节在UFhetτ下将条件加强为α≥R、ατ≥Kd；新版本保留旧身份。线性无light反例又证明同一排序势全部全局最小点均可有趋近R的真实改善，不能仅改取global min消R。独立审查及两路Fraction证据从正文11.5进入。

[潜在使用森林与单玩家挂树私人成本归约](research/current/weighted_congestion/incidence_forest_private_reduction.md)给任意正权、任意有限资源子集策略和非负非减费用的exactPNE；只在单核心玩家处附着的树可换私有常数，保多项式次数并将所有α≥1的reduced PNE用同一lift提升。单环二玩家例的最佳因子72/71说明森林不能无证扩域。先读两个精确合同，再读冻结审查/代码/证据。全类仍缺无界局部权比、非强迫反馈或有环核心的统一选态。
