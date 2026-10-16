# 研究总目录：先选问题，再读具体资产

**新主攻入口：[一般不相关并行机的统一常数2近似壁垒](current/unrelated_machines/README.md)**。先读模型/精确账本与本题前沿，使用[新BOSS启动词](unrelated_machines/BOSS_START.md)；旧题地图按需读取，不能把旧拥塞目标带入新save。
本题新增[大边匹配残余及共享容量方法反例](current/unrelated_machines/heavy_matching_residual_and_escape.md)：安全过滤能识别原间隙族，但共享逃逸族仍保持gap趋2；统一常数突破仍OPEN。
当前主要成果是**加权原子拥塞博弈的线性全状态非存在下界及Cd/ln d保证的严格否定**。设施选址和顺序客户吸引是独立保留的研究线；它们有不同模型、量词和未解问题。完整的[中文资产名、文件位置、具体用途与状态依据](CATALOG.md)覆盖当前数学正文、问题、审查和已整合的拥塞核验资产。

面向审稿式连续阅读，可直接读[线性非存在界英文主稿PDF](current/weighted_congestion/linear_threshold_article.pdf)和[成稿核查](reviews/weighted_congestion/linear_threshold_article_review.md)；含完整证明，未认证优先权或期刊录用。

交给未读仓库的研究者：先读[当前线性全状态否定证明](current/weighted_congestion/linear_degree_allstate_lower_bound.md)及其独立审查；解题前冻结整理可复用[自足接题材料与精确方法障碍](weighted_congestion_frontier/PRO_BRIEF.md)和[完整任务正文](weighted_congestion_frontier/prompts/PRO_ATTACK.md)；旧整理稿的OPEN状态由新否定结论取代，其余数学、审查与证据仍可按冻结短指针追溯，不要求默认通读历史。

本题后续从[共同匹配选择与条件块容量](current/unrelated_machines/joint_matching_completion_and_block_cuts.md)进入：条件舍入、低余量精确选择障碍、专用共享容量切面与仍OPEN的统一构造分开登记。

## 我应该从哪里开始

| 你要研究什么 | 首读与主要资产 | 当前真正缺口 |
| --- | --- | --- |
| 一般不相关并行机的统一常数突破 | [本题地图](current/unrelated_machines/README.md) → [精确账本](unrelated_machines/CLAIMS.md) → [长链联合投影边界](current/unrelated_machines/long_path_coalition_gap.md) | UM-TARGET-v1仍OPEN；固定机器见证只共享单机边际仍gap2，完整多机交叠相容性与一般图构造复杂度是当前缺口。 |
| 一般不相关机统一常数近似 | [本题地图](current/unrelated_machines/README.md)→[精确星消去与容量接口](current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md) | 已有可恢复消元、安全下界及准确障碍；一般统一ε与位多项式调度输出仍未证明。 |
| 加权原子拥塞的普遍存在门槛 | [数学总述](current/weighted_congestion/README.md) → [精确模型](weighted_congestion_frontier/MODEL.md) → [线性次数全状态下界与原题否定](current/weighted_congestion/linear_degree_allstate_lower_bound.md) → 正文所链两份独立审查及代码/冻结证据 | 本次Cd/ln d判定已严格否定：每d≥2^20无(d/10)-PNE族；全类门槛增长阶Θ(d)，精确常数/有限d值、外部评审和新颖性另待核查。 |
| 非负共享负载响应的低阶表示 | [正占用核接口](current/positive_kernels/README.md) → 交互秩面 → 锐截断 → 非闭锥补全 | 固定正质量、完整Boolean表与正混合；一般动作签名及selector桥未建立，独立传感器实例已给 |
| 共同目录双设施的尖锐稳定性 | [黄金比成果与阅读顺序](current/shared/README.md) → 主定理、完整证明、尖锐下界、算法 → 小目录复杂度 | 已有内部成果的外部审查与优先权；实例最优倍率 EPTAS 仍是候选义务 |
| 异构目录双设施及单交叠边界 | [异构成果与阅读顺序](current/heterogeneous/README.md) → 一般目录候选、单交叠全长锐界、长回应环 | 一般异构上界的候选状态不能被单交叠定理覆盖 |
| 固定双设施布局的客户均衡 | [局部均衡与精确算法](current/local_and_exact/README.md) → 支持几何、局部强弦、精确求解及成本扩展 | 精确续局、有限证书与普遍全局保证分别核对 |
| 任意设施数的统一因子与构造 | [多设施成果与阅读顺序](current/multi_facility/README.md) → 因子二 → 完整盒有限构造 → 结构类算法与障碍 | 一般输入位多项式构造、最佳统一常数 |
| 顺序客户吸引的一般半覆盖 | [福利界、工具和反例地图](current/customer_attraction/README.md) → 模型、小人数/结构类结果 → 完整策略和全局桥 | 一般半覆盖仍开放；辅助桥的反例不是主问题反例 |

第一次进入仓库先读根 [README](../README.md)、[当前前沿](../RESEARCH_STATE.md)、[命题入口](../CLAIMS.md)、[失败入口](../FAILED_ROUTES.md)。随后只读所选专题；不用先通读全部旧稿、工具或协作提示词。

给未读仓库的独立研究者，使用[加权拥塞全类判定交接简报](weighted_congestion_frontier/PRO_BRIEF.md)及[独立攻题任务](weighted_congestion_frontier/prompts/PRO_ATTACK.md)。简报合并必要定义、可靠边界、准确方法限制和未闭合义务，详细数学正文按需读；冻结导出及源映射从专题入口进入。

一般群组奇环的actual缺口已由[单缺陷双取向消去](current/weighted_congestion/odd_ring/cohort_lower_bound_and_envelope.md#10-一般群组奇环实际阈值与正测试包络一致)闭合：不要求UF、允许部分aligned light和混合多项式，全部该拓扑均有T_d-PNE，实际最坏阈值恰T_d。先读精确拓扑和[独立攻击](reviews/weighted_congestion/odd_ring_parameters/general_cohort_actual_upper_review.md)，再调用两路Fraction证据；不能把这个拓扑当全类规范形。


本题新增[计数传播与成束相容性](current/unrelated_machines/bundle_coupling_subdivision_barrier.md)：可位多项式计算下界、旧gap族上的修复及其细分失败。只排除相应下界合同，目标仍OPEN；先读本题精确账本再使用。

## 文件按什么用途存放

| 位置 | 里面是什么 | 如何用 |
| --- | --- | --- |
| [current/](current/README.md) | 当前数学定义、自足证明、反例和可复用方法 | 按各专题 README 的证明链阅读；目录位置不代表统一审查等级 |
| [questions/](questions/README.md) | 仍未闭合的问题、候选稿及保留的已闭合问题合同 | 先看现在缺哪一步；旧探索计划不当成新任务 |
| [reviews/](reviews/README.md) | 已实际发生的数学审查与独立攻击 | 核对冻结版本、覆盖 claim 与仍成立的异议 |
| [weighted_congestion_frontier/](weighted_congestion_frontier/README.md) | 拥塞模型、账本、文献与协作程序 | 做数学先读模型/账本；需要协作操作时再读运行说明 |
| [../tests/audits/](../tests/audits) 与 [../evidence/](../evidence) | 独立核验代码、输入、证书和冻结结果 | 从对应正文或资产目录进入；计算不替代一般证明 |
| [../history/](../history/README.md) | 必要原稿、来源和已退出当前优先序的投稿判断 | 只在追溯时读；旧路线快照不覆盖现行研究状态 |

加权拥塞的跨尺度新接口见[有序权组冻结](current/weighted_congestion/weight_bands/ordered_tail_freezing.md)：阶段局部势可拼接密集权群，但最优潜在尾部参数固定次数仍可无界。[DAG端点低泄漏预算](current/weighted_congestion/polynomial_curvature/dag_low_leakage_budget.md)则精确限制指定阶跃模拟测试；二者均未闭合全类匹配上界。

[阶跃DAG极值幅度的真实全入状态](current/weighted_congestion/step_dag/polynomial_extremal_all_in.md)另在精确幅度锚定下给多项式实际状态的统一平方根界，无低泄漏假设；任意幅度和全类拓扑尚未归约。

## 名称、命题与审查怎样对应

每份文件的**中文数学名称与阅读目的**在 [CATALOG.md](CATALOG.md)，人工维护源为 `catalog.json`。同一文件可以包含多个命题，各自精确身份见 [current/claims.md](current/claims.md)；拥塞另有[主题账本](weighted_congestion_frontier/CLAIMS.md)。

| 登记 | 它回答的问题 |
| --- | --- |
| [assets.json](assets.json) | 某个命题适用于什么输入，正文、实现、测试、证据和来源在哪里？ |
| [review_status.json](review_status.json) | 来源证明、当前重构、内部审查、外部审查和实现分别到什么状态？ |
| [graph.json](graph.json) / [交互图](index.html) | 哪些定义与全部共同前提推出结论，哪些边仅是有限检验、反例或未解限制？ |
| [source_crosswalk.md](source_crosswalk.md) | 原始稿件怎样被当前数学解释、保留或取代？ |
| [拥塞资产链](weighted_congestion_frontier/FILES.md) / [来源迁移记录](weighted_congestion_frontier/INTEGRATION.json) | 一个拥塞成果包怎样连接正文、审查、核验和冻结证据，原分支原件怎样恢复？ |

关系图提供搜索种子。未出现在图上的方法仍可探索；状态、量词和真值以精确陈述及证明为准。

## 下一步与新资产入库

[当前全仓路线](ROADMAP.md)列现在值得推进的义务；[入库规范](GROWTH.md)和[生产、读取、保存规则](REPOSITORY_GUIDE.md)决定新文件的位置。给新资产写具体名称、用途、精确范围和证据层级；完成相应核验后及时保存到 `main`。

从仓库根运行 `python3 research/build_catalog.py --check`、`python3 research/build_map.py --check`、`python3 research/build_crosswalk.py --check` 和 `python3 research/check_assets.py`。这些检查负责目录和登记一致，不能充当数学证明。

不相关并行机的[稀释终端与条件探针比较](current/unrelated_machines/diluted_sink_probe_gap.md)解释独立配置/逐边LST为何仍gap2，并给出条件内保留大任务基数的可算修复；全局统一近似仍OPEN。

半单位新身份已关闭固定大小分界的共同见证窗口：每个固定δ∈[0,1/2)的(Aδ)存在性NP完全；P≠NP下无总位多项式OPT≤T承诺构造。它仍不是统一低于2算法的困难性，下一步转向实际联合舍入损失。见[共同选择正文§3a](current/unrelated_machines/joint_matching_completion_and_block_cuts.md)。

[全局单行基数匹配与紧凑共享逃逸](current/unrelated_machines/row_count_escape_gap.md)把资源池路线推进到准确边界：一次全局任务权匹配涵盖同一下界的全部子池，但每机/每配置独立守计数仍不等于共同真实负载。新族为多项式规模，GPC₂与所有单行见证仍gap2；现有条件块切面可修复，主目标OPEN。

[直接联合槽的正面衔接](current/unrelated_machines/joint_slot_prefix_rounding.md)给UM-ROW-SPREAD-TWO-ROUND-v1：删去零任务后每行正时间跨度≤2（逐机尺度不同）时，显式前缀计数LP加一次全任务槽匹配给3/2位多项式构造。它是VW/ST已知机制的直接推论，绕过过强(Aδ)见证；未消除一般行内跨尺度混合，主目标仍OPEN。

[三选稀疏深树的独立条件配置边界](current/unrelated_machines/sparse_conditioned_configuration_gap.md)区分“每条边都可单独强制”和“这些条件点有共同多机相关性”。前者仍gap2，完整四机器bag交集联合一致性在本族精确；沿正文进入独立审查、双路代码和实际输入/证书。

紧凑共享逃逸正文§6另给UM-COMPACT-MULTIROW-EXTENSION-v1：任意U含至多N−2k个中心时，每个单机配置均可延伸并让U全部机器同时守真实容量；N−2k+1中心加z空pin有明确失败。故“更多独立行见证”仍缺共同相关性，尖锐预算和实际构造不改变主目标OPEN状态。

[完整单机配置的独立全LP延伸](current/unrelated_machines/row_count_escape_gap.md#7-完整单机配置也分别能延伸到完整配置lp)给出比逐边条件LST更强的准确边界：所有本地配置各自有完整证书仍gap2，下一缺口是共同条件矩与可构造舍入。

[真实最优调度凸包与固定槽输出空间](current/unrelated_machines/optimal_convex_fixed_slot_gap.md)是本题联合舍入的新压力测试：分数点已在真实最优凸包内，所有固定槽matching仍趋2；跨槽修复可恢复最优。由正文进入精确身份、冻结审查、双路审计及输入/证书；无主目标算法突破。

[循环批量修复与分流合流](current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md)连接可终止局部优化、无界撤离及唯一成本LST分流边界；新增与boss7真最优凸包槽族的守恒桥梁，证明逐坐标修复也会近2停滞。一般多源共同容量仍OPEN。

[有向需求树与不相关机负载的精确桥梁](current/unrelated_machines/rooted_dag_degree_token_bridge.md)把MMDA已知必要方向重构为无需配置枚举的实际任务输入，含最优值恒等、大需求填充、有限阈值及总位复杂度；用于检验联合迁移的资源相容性。

[真实最优边际的舍入断点](current/unrelated_machines/optimal_hull_marginal_rounding_barrier.md)给固定row/count包络sup2及同sink pair负相关的尖锐期望/尾界；x本可为真实OPT调度的显式平均。[单边界森林批量恢复](current/unrelated_machines/forest_boundary_contraction.md)给实际根负载支配、内部(1+η)T和max恢复，无深度累计。后者是已知结构DP机制的接口化；一般多边界/有环核心与统一ε仍OPEN。

[原任务拟阵容量外包](current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md#7-原任务地集上多拟阵容量外包的精确损失)与[整个最小总处理量面的支撑边界](current/unrelated_machines/optimal_convex_fixed_slot_gap.md#6-最小总处理量的整个最优面也可能丢掉修复边)给联合迁移接口的两个锐限制。一般构造仍须重开原零质量边、允许接收机增载并共同守容；两项均未给新近似比或新颖性认证。

大小任务共同修复进一步分清两条事实：[冻结宏任务的全微任务重开](current/unrelated_machines/optimal_hull_marginal_rounding_barrier.md#10-冻结宏任务后的微任务全局重开间隙与尖锐迁移前沿)即使精确联合优化仍趋2，并有尖锐宏任务迁移前沿；[两层异质需求贪心](current/unrelated_machines/rooted_dag_degree_token_bridge.md#7-两层需求树的半比例贪心与任务桥梁的二分之三负载界)给无宽度限制的浅层半比例树和对应3/2实际调度。一般多层/多边界联合选择仍OPEN，二者不是主目标突破。

[双边界森林的相关菜单](current/unrelated_machines/forest_boundary_contraction.md)：`UM-FOREST-TWO-BOUNDARY-MENU-v1`给a精确支配、b乘性保零和实际任务见证，任务不交挂件共享边界可求和；菜单共同选择与串行嵌套仍需新机制。

[同机槽族的单目的地修复](current/unrelated_machines/optimal_convex_fixed_slot_gap.md)：`UM-ONE-DESTINATION-SLOT-REPAIR-v1`给最小迁移m(m−1)/2，并可整批沿路径严格下降至OPT；仅此显式族，接收机允许增载。

两项均已自足证明、独立内部攻击和有限精确核验；都是限结构正面接口/修复，未认证全球新颖性，不形成一般输入的统一ε。UM-TARGET-v1保持OPEN。

[外部互斥星的配置保持](current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md#8-外部配置互斥下的配置点双向保持)补精确正面证书接口；[收缩后稀疏终态](current/unrelated_machines/sparse_conditioned_configuration_gap.md)又补先极小星消元后独立CONFIG探针的gap2范围。证明→star_configuration_transfer_review.md→双路代码/实际终态/冻结证据可接续；一般共同选择与统一ε仍OPEN。

[单共享汇点的宏任务共同匹配与私有任务整组撤离](current/unrelated_machines/shared_sink_joint_macro_assignment.md)：UM-SHARED-SINK-JOINT-MACRO-v1以保零覆盖背包成本+dummy全局匹配给home≤T、z≤(1+η)T的位多项式实际构造；宏图任意，私有任务无尺寸限制。一般多预算/跨home任务仍OPEN。

[对称条件矩的运输与重新耦合](current/unrelated_machines/symmetric_moment_reset_and_single_machine_threshold.md)把同层重置义务拆清：给定任务聚合可逐列核验；真实最优矩的单机固定后备推前在显式均匀族恰需2T吸收包，但同一个一阶边际在T包时可用真实匹配分解重建矩。它只限制既定矩运输，不是N(P)间隙或一般近似否定；主目标仍OPEN。

[共同拥塞需求树的正面流接口](current/unrelated_machines/rooted_dag_congestion_flow.md)允许任意深度的低需求走廊与汇流；给证书提取、固定W最小K均位多项式，保证1/(2K−1)精确尖锐。下一缺口是未知W的共同选择，不能用已被反驳的激活边际LP替代。

[共同容量路线整合审查](reviews/unrelated_machines/joint_capacity_route_feasibility_review.md)连接菜单、条件矩、需求树与宏任务修复：核准局部范围、一般核心残留及新候选的精确提取/进展义务；不是另一个模型或新统一算法。
