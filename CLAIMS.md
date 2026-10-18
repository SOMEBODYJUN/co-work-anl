# 精确命题入口

新主攻存档 `unrelated-machines`，精确目标 `UM-TARGET-v1` 及经典工具、长链/联合投影、树再耦合、匹配残余/共享逃逸等阶段边界见[不相关并行机精确账本](research/unrelated_machines/CLAIMS.md)。主目标仍OPEN；既有工具重构与限范围方法反例不升级为新近似算法。
另有[共同大边选择与条件块容量](research/current/unrelated_machines/joint_matching_completion_and_block_cuts.md)的条件舍入、限域精确选择NP完全和专用族强化身份，均不关闭主目标。
本页是目录，不以摘要替代量词。每项现行命题的精确范围、依赖和五轴审查状态分别在 [research/current/claims.md](research/current/claims.md) 与 [research/review_status.json](research/review_status.json)。改变对象、假设、量词、成本或结论必须创建新版本。

| 研究线 | Exact Statement 的权威位置 | 当前前沿 |
| --- | --- | --- |
| **当前：不相关并行机 UM-TARGET-v1** | [精确账本](research/unrelated_machines/CLAIMS.md)、[模型与经典地基](research/current/unrelated_machines/model_and_classical_barriers.md) | 一般输入、统一ε、确定性位多项式实际调度仍OPEN；[本题前沿](research/unrelated_machines/RESEARCH_STATE.md) |
| 加权拥塞 WC-TARGET v1 | [MODEL](research/weighted_congestion_frontier/MODEL.md)、[精确账本](research/weighted_congestion_frontier/CLAIMS.md)、[现行证明](research/current/weighted_congestion/README.md) | 每d≥2^20无(d/10)-PNE的全状态族，严格否定Cd/ln d保证；增长阶Θ(d)，最优常数/有限d值未定 |
| 双设施共同/异构目录 | [逐命题登记](research/current/claims.md)、[共同目录](research/current/shared/README.md)、[异构目录](research/current/heterogeneous/README.md) | 共同目录尖锐界、稀疏异构与复杂度结果各有精确输入类；一般异构 2 保留候选 |
| 任意设施数 | [一般因子 2](research/current/multi_facility/uniform_two.md)、[改善过程](research/current/multi_facility/greedy_box_global_progress.md)、[高效构造义务](research/questions/greedy_box_polytime.md) | 存在性/有限构造已内部证明；一般位多项式构造 OPEN |
| 顺序客户吸引 | [分支精确地图](research/current/customer_attraction/README.md)与全仓逐命题登记 | 一般半覆盖 OPEN；子类上界和辅助桥反例分别保存 |


本次四个新精确身份为`WC-HEALTHY-LINEAR-SWEEP-v1`、`WC-HEALTHY-FRONT-COVERAGE-v1`、`WC-LINEAR-DEGREE-ALLSTATE-NONEXISTENCE-v1`、`WC-MATCHING-LOG-UPPER-NEGATIVE-v1`；各自量词、依赖、边界和完整证据链见[主题账本](research/weighted_congestion_frontier/CLAIMS.md)及[自足正文](research/current/weighted_congestion/linear_degree_allstate_lower_bound.md)。WC-TARGET v1原身份保留，其他结构定理/候选不因本题完成升级。

条件证书新增UM-HEAVY-ALTERNATIVE-FILTER-v1、UM-DILUTED-SINK-PROBE-GAP-v1、UM-BIG-CARDINALITY-PROBE-v1，分别是安全接口、准确方法边界及仅对该族的加强效果；见[精确账本](research/unrelated_machines/CLAIMS.md)。


新增UM-DILUTED-ESCAPE-PROBE-GAP-v1精确身份：共享逃逸合并后仍通过所有普通边探针与GHMR；只限该合同，依赖与同行来源见本题账本。

半单位新身份已关闭固定大小分界的共同见证窗口：每个固定δ∈[0,1/2)的(Aδ)存在性NP完全；P≠NP下无总位多项式OPT≤T承诺构造。它仍不是统一低于2算法的困难性，下一步转向实际联合舍入损失。见[共同选择正文§3a](research/current/unrelated_machines/joint_matching_completion_and_block_cuts.md)。

[全局单行基数与紧凑共享逃逸](research/current/unrelated_machines/row_count_escape_gap.md)新增安全位多项式查询及准确反例：完整任务身份/多槽/每机每配置计数延伸仍与GPC₂合用保持gap2；条件块切面仍可识别本族。UM-TARGET-v1继续OPEN；一般共同负载耦合与统一舍入未解。

新身份`UM-SPARSE-CONDITIONED-CONFIG-GAP-v1`为每任务至多三选的全边独立条件配置间隙；[精确账本](research/unrelated_machines/CLAIMS.md)固定不同查询不耦合及未覆盖预处理的范围，不升级主目标。

UM-MACHINE-CONFIG-PROBE-GAP-v1新增“∀机器∀合法完整配置∃各自完整配置LP延伸”的间隙2身份；精确范围、非必要条件警示及共同base边界见[专题账本](research/unrelated_machines/CLAIMS.md)与紧凑族正文§7。

循环批量修复新增UM-ROBUST-CYCLIC-BATCH-OPT-v1、UM-BATCH-SUPPORT-REPAIR-NO-v1、UM-FORK-MINCOST-ROUND-REPAIR-NO-v1；另以UM-COORDINATE-REPAIR-ST-GAP-v1登记与boss7真凸包槽族的守恒直接推论。[准确量词与范围](research/unrelated_machines/CLAIMS.md)区分局部构造和修复反例，未得统一近似。 UM-OPT-HULL-LONG-CHAIN-LOCAL-GAP-v1另登记真凸包mincost初始化后的无界机器严格lex支持；中性预修不被排除。

新增UM-OPT-HULL-ROW-DISCREPANCY-GAP-v1、UM-OPT-HULL-PAIR-NC-GAP-v1、UM-FOREST-BOUNDARY-AUGMENT-v1。前两项仅固定边际输出合同，后一项仅给定单边界森林资源增强恢复接口。[精确专题账本](research/unrelated_machines/CLAIMS.md)保全量词；UM-TARGET-v1保持OPEN。

新增UM-KNAPSACK-MATROID-ENVELOPE-v1、UM-MIN-WORK-FACE-SUPPORT-GAP-v1，精确量词及两项独立冻结审查见[专题账本](research/unrelated_machines/CLAIMS.md)。仅限容量外包与最小工作量支撑合同，不改变UM-TARGET-v1。

新增双边界森林相关菜单与同机槽族单目的地路径修复，精确身份分别为UM-FOREST-TWO-BOUNDARY-MENU-v1、UM-ONE-DESTINATION-SLOT-REPAIR-v1；[专题账本](research/unrelated_machines/CLAIMS.md)登记结构、同步任务身份、近似覆盖及所有未闭合义务，主目标仍OPEN。

新增UM-STAR-CONFIG-TRANSFER-v1与UM-CONTRACTED-SPARSE-CONFIG-GAP-v1，分别固定配置转换的充分条件/方向/支持位复杂度与先消元后探针的准确gap范围。[精确身份](research/unrelated_machines/CLAIMS.md)保全量词，未改变主目标OPEN。

[对称条件矩的运输与重新耦合](research/current/unrelated_machines/symmetric_moment_reset_and_single_machine_threshold.md)把同层重置义务拆清：给定任务聚合可逐列核验；真实最优矩的单机固定后备推前在显式均匀族恰需2T吸收包，但同一个一阶边际在T包时可用真实匹配分解重建矩。它只限制既定矩运输，不是N(P)间隙或一般近似否定；主目标仍OPEN。 后续§9另给独立均匀选择的精确新矩：同族吸收q+2任务即可保全部条件，门槛为(1+2/q)T；这仍非一般输入界或实际调度保证。

新增UM-SHARED-SINK-JOINT-MACRO-v1；[专题精确账本](research/unrelated_machines/CLAIMS.md)固定唯一home、单sink、严格宏边阈值与实际构造量词。它给共同选择的正面接口，不改变一般主目标OPEN。

新增UM-DAG-CONGESTION-FLOW-v1与UM-DAG-ACTIVATION-CORRIDOR-GAP-v1：[专题账本](research/unrelated_machines/CLAIMS.md)固定共同流、整数K、未知W及激活LP的不同合同；条件提取/固定支撑搜索已内部独立核对，主目标仍OPEN。

新增UM-OCCUPATION-MODE-SIDE-CONSTRAINT-v1、UM-FIXED-SINK-PRIVATE-GROUP-THREE-HALVES-v1、UM-FIXED-SINK-MACRO-PROMISE-APPROX-v1；[专题精确账本](research/unrelated_machines/CLAIMS.md)分开支撑界、给定T构造与OPT promise近似。固定K、私有分组及宏阈值不进入一般主目标。

守恒扩区与非单位分叉另立UM-DAG-TRANSIT-CONGESTION-v1、UM-DAG-NONUNIT-PARAMETER-EXACT-v1：[正文](research/current/unrelated_machines/rooted_dag_congestion_flow.md)§7–10和专题账本固定新2K合同及2^h精确树复杂度；未改旧Claim，主目标仍OPEN。

新增UM-SHARED-SINK-MACRO-EXIT-v1与UM-BOUNDED-PROFILE-EXIT-POOL-v1，分别给可退出宏任务的共同匹配、无界机器数但完整有界profile池的实际恢复；[专题账本](research/unrelated_machines/CLAIMS.md)固定限域阈值合同。一般UM-TARGET-v1仍OPEN。

[有限覆盖与反向困难性可靠性缺口](research/current/unrelated_machines/configuration_finite_cover_obstruction.md)已给标准机制的准确调度重构：即使高围长也存在整数OPT坍缩到配置阈值的cover；精选接线与一般困难性仍未排除，UM-TARGET-v1保持OPEN。

新增UM-HALL-GROUP-JOINT-FLOW-v1与UM-HALL-GROUP-PROMISE-APPROX-v1：[共同资格组正文](research/current/unrelated_machines/hall_group_joint_flow.md)给无界sink数量的实际联合流舍入、未知OPT的有限瓶颈恢复；保留组身份/等端体积/负载范围，不改变一般UM-TARGET-v1。

全局矩新增两个分离身份：UM-GLOBAL-MOMENT-NEARFLAT-EXTRACTION-v1给定严格小缺陷C₂证书的实际位多项式提取；UM-GLOBAL-MOMENT-HS-GREEDY-GAP-v1攻击指定全空间HS初始化、顺序和平局。[准确量词](research/unrelated_machines/CLAIMS.md)保留额外证书和所有未覆盖算法；主目标仍OPEN。

[高围长仙人掌的配置锐界与精确块算法](research/current/unrelated_machines/cactus_configuration_gap_and_block_exactness.md)表明simple cactus可同时有CONFIG supgap2和真实精确P；单环分量配置精确、最大顶点块环秩b给2^b poly算法。它们限制反面归约的结构，不证明一般目标不存在。

[反面路线的递归与资源重复边界](research/current/unrelated_machines/private_graft_and_resource_repetition.md)的两个身份UM-PRIVATE-GRAFT-NO-AMPLIFICATION-v1、UM-RESOURCE-REPETITION-SOUNDNESS-NO-v1已入本题精确账本；不改变UM-TARGET-v1的OPEN状态。

固定阶真实矩提取的精确身份 UM-TRUE-MOMENT-VECTOR-GREEDY-LINEAR-GAP-v1 见[专题账本](research/unrelated_machines/CLAIMS.md)及[自足证明](research/current/unrelated_machines/truncated_multiplication_vector_greedy_barrier.md)：一般nT上界、任意固定r的线性下界；不关闭UM-TARGET-v1。

新增UM-PROJECTED-VECTOR-GREEDY-UNBOUNDED-v1、UM-PROJECTED-VECTOR-GREEDY-UNIT-COLLISION-v1；[精确专题账本](research/unrelated_machines/CLAIMS.md)固定真实最优分布/给定任务顺序/特定压缩更新的范围。一般无界证明及单位小证书均不否定UM-TARGET-v1。

## 加权共同组的新增正面接口

[共同资格私有组的加权出口与联合槽](research/current/unrelated_machines/weighted_group_joint_slot_rounding.md)给`UM-WEIGHTED-GROUP-JOINT-SLOT-v1`及未知OPT的`UM-WEIGHTED-GROUP-PROMISE-APPROX-v1`：给定不交home/sink、唯一home私有组、同组共同资格与等端w_j≤δT、W_h≤T及macro端>T/2，在0≤δ<1/2时实际输出≤(3/2+δ)T（sink≤3T/2）；无组负载正下界、sink数不固定。未知OPT承诺版用单调加权LP及有理整数网格搜索。数学算法完整，软件仅实现给定精确LP见证的验证/舍入；独立审查与双路有限Fraction核验已登记，外审/新颖性未认证。一般矩阵如何生成这些分组和处理异端容量仍未解，UM-TARGET-v1保持OPEN。


[低重数标签资源的确定性地板与锐界](research/current/unrelated_machines/bounded_collision_label_resource_floor.md)：所选资源重数Δ给真实b≥1/Δ，二重资源对任意束宽恰保留1/2；全局不同变量组度Δ_G给无需见证的实际(2−1/Δ_G)桥梁调度。只排除该四层有界碰撞接口的近二归约；高重数/跨层一致性与一般UM-TARGET-v1仍OPEN。

进一步的[大需求束碰撞界与平方池锐性](research/current/unrelated_machines/large_bundle_collision_square_root_floor.md)给含根上取整的Λ_c真实树，q=Δ=K=t²时精确maxΛ=b*=1/t；带η→0及ηKmin→∞条件的NO侧必要量为liminfη²Δ≥1。只约束资源束接口，源问题解码和一般困难性仍缺。

[全局四阶负载松弛的锐利二间隙](research/current/unrelated_machines/c2_unit_multislice_gap.md)（`UM-C2-LOAD-UNIT-GAP-v1`）已闭合裸C2-load本身的义务：m≥3,n=m+1单位同机上T_C2=n/m、OPT2，显式有理PSD证书给supgap2。这不同于固定贪心坏例；其三阶同机矩为负、CONFIG阈值2，故不含C2+CONFIG或一般算法困难性。该裸C2命题的范围不变；后续[弱H2合取的新二间隙](research/current/unrelated_machines/weak_h2_configuration_moment_gap.md)另行关闭只共享一阶CONFIG的合同。共享行二阶在该新族上阈值精确，一般强合同与UM-TARGET-v1仍OPEN。

[单任务外接端口的向下投影与锐计数](research/current/unrelated_machines/signed_one_job_port_downset.md)给`UM-SIGNED-ONE-JOB-PORT-DOWNSET-v1`：保留一个外部出现端点且排除外部容量时，两一致态强制至少2^z(2^a+2^b−1)个严格可行状态，固定T>0逐参数锐；不能用该纯内部接口实现等值复制。BG一般signed阈值PCSP的近二困难性不保持调度双出现限制；多任务编码及外部联合容量仍未解，UM-TARGET-v1保持OPEN。

[三外接机器选择器的锐三半界](research/current/unrelated_machines/three_host_selector_sharp_three_halves.md)：给only-a和b+c-free的两份实际C≤T调度，单调二色行权闭包输出only-b或only-c的完整C≤3T/2调度，且两任务锐；内部规模、资格任意，所有预载逐台核。同一机制对一般SC三特殊item给无条件可构造半值，亦锐。两者仅限制明确可用性复制接口；一般主目标和反面仍OPEN，新颖性/外审未认证。

[两状态行列池锐性修复](research/current/unrelated_machines/duplication_state_majority_floor.md)：标签可只选部分资源，s=K=4的真实最优为5/8，反驳旧附属1/2断言；主多数下界仍成立。新精确整数前沿及显式达到构造已独立重构，原K≥2s数例保留；不是一般近二困难性。

[多输出加权状态预算](research/current/unrelated_machines/weighted_fanout_profile_boundary.md)扩展三host接口：给两实际YES，对任意候选输出集K和有理β构造实际C≤(2−β_i)T；真实OPT总和≤(2|K|−1)T，加权星取等。任意两个缺一OPT之和≤3T，至多一个可严格超三半，任意扇出二叉树同时锐；不能用仅单输出近二星代替全局复制soundness。主目标保持OPEN。

[双轨阈值编码边界](research/current/unrelated_machines/dual_rail_threshold_soundness_boundary.md)：归一化scalar整类总有实际3/2（ST半质量直接推论），改unit容量亦总3/2，两种绝对T1界各有完整锐例。非均匀单例外有精确匹配合同；完整signedcube的真实OPT有min_B精确式且趋1。四成本模型分开，未将NO源自动解码为NO调度，主目标正反面仍OPEN。

[单位读出配额森林边界](research/current/unrelated_machines/unit_readout_pruned_forest_boundary.md)：一般arity下实际C<2等价全部变量mandatory r=ceil(k(2−C))森林可注入slots；但arity≤2A时，任意深度和任意wiring均有实际≤1+floor(k/2)/k≤3/2（经典ST半质量推论），14机15job绝对界锐。叶命中精确门槛(k−r+1)^h说明dummy补齐义务；相同64open的两模块真实OPT为1与7/4，叶容量不能代替祖先兼容。一般目标正反面仍OPEN。

[校准计数槽](research/current/unrelated_machines/unit_readout_calibrated_cardinality_slots.md)将单位读出树的半质量推广为有理下传证书：行分数任务数≤整数k−r+1给实际2−r/k。uniform x_h闭式提供所有wiring密度界；任意固定D≥2、arity≤D A的同结构类有确定性位poly统一2−1/(4D)算法，k,h可无界。已扣VW既有2−1/k及经典ST；D无界或一般P仍无统一ε，反面目标保持OPEN。

机器价格的新精确身份 `UM-HEAVY-LIGHT-PRICE-CONVEXIFICATION-v1` 见[专题账本](research/unrelated_machines/CLAIMS.md)：固定原T剪枝与角色，价格LP等价、joint supgap2、无剪枝固定m锐界m及最优价格共同面成功证书；不是一般算法或新困难性，UM-TARGET-v1保持OPEN。

`UM-RESIDUAL-THROUGHPUT-LATTICE-v1` 与 `UM-OCCUPATION-INDUCED-EDGE-DEFICIT-v1` 已入[专题账本](research/unrelated_machines/CLAIMS.md)：固定R的一般异端容量格次模、任务角色变动反例及严格次二占位的任意图缺口表示。原构造显式OPT1，不能当作主目标困难性。

[完整单位树的叶流与选择重组](research/current/unrelated_machines/unit_readout_global_leaf_flow_and_selector_mixing.md)：任意clause密度下固定h有实际(1+2^(−1/h))近似；给p份同一P完整C1见证时，N≥p的任意covered selector坐标重组有锐2−1/(2p−1)实际负载。h、p增长及NO无完整YES均承重，一般主目标及其反面OPEN，外审与新颖性未认证。

新增精确身份：`UM-ST-ENVELOPE-CONFIG-IDENTITY-v1`、`UM-WEAK-H2-CONFIG-MOMENT-GAP-v1`、`UM-STRONG-H2-ROW-PAIR-STAR-EXACT-v1`；[完整账本](research/unrelated_machines/CLAIMS.md)记录一般表示、弱同点合取supgap2及同族强二阶精确校准，均不改变UM-TARGET-v1。

新增限定身份 `UM-UNIT-READOUT-CONFIG-POSITIVE-PART-v1`、`UM-UNIT-READOUT-STRICT-UNIT-GAP-v1`、`UM-UNIT-READOUT-CLOSED-TREES-EXACT-CONFIG-v1`；[专题账本](research/unrelated_machines/CLAIMS.md)给精确量词。仅配置阈值/严格unit promise/经典族精确回算，不升级UM-TARGET-v1。

首步与全程现分离为 [UM-PRUNED-FIRST-MOVE-BOUND-v1 / UM-BOUNDED-BATCH-TRANSIENT-PEAK-SHARP-v1](research/current/unrelated_machines/pruned_first_move_and_transient_peak.md)：一般T剪枝首步上界max(2T,C+T/2)及固定批量环的逐参数锐性；不含一般全程/次二算法。

[逐行均匀相关读出](research/current/unrelated_machines/row_uniform_correlated_guard_rounding.md)新增限定身份 `UM-ROW-UNIFORM-CORRELATED-GUARD-HALF-RETENTION-v2` 与 `UM-ROW-UNIFORM-FLAT-STATE-THREE-HALVES-v1`：共享同一左标签仍有逐点ceil-half共同资源匹配；其显式平层原矩阵可完整输出三二调度。非均匀、重复自查询、多层祖先约束及一般UM正反面不在此结论内；外审和新颖性未认证。

[私有分叉树估值与支持域](research/current/unrelated_machines/private_tree_branching_valuation_and_minorants.md)新增精确signed demand、全叶XOS包络损失k[1−(1−1/k)^h]及single-state紧凑minorant LP；显式叶预算最大损失阶logB/loglogB。一般源计算gap和共同资源分配未由这些oracle解决；generic LP优化未实现，外审与新颖性未认证。

[近单位蕴含PCSP](research/current/unrelated_machines/near_unit_implication_pcsp_and_physical_copy_obligation.md)另给精确minion及所有固定k,r的一般NP-hardness；变量任意出现、无物理编译承诺，不能升级UM-TARGET-v1反面。

新增UM-MULTISMALL-INCIDENCE-FLOW-APPROX-v1、UM-TERNARY-UNIT-SELECTOR-NORMAL-FORM-v1、UM-TARGET-TERNARY-SELECTOR-EQUIVALENCE-v1、UM-TWO-MEASUREMENT-UNIT-PRESENCE-SHARP-GLUING-v1、UM-TWO-MEASUREMENT-TINY-PRESENCE-GLUING-v1；[精确专题账本](research/unrelated_machines/CLAIMS.md)分开双流实际算法、阈值正规形/条件等价与两见证锐界，不升级UM主目标。

新增 UM-LIST-AGREEMENT-DEGREE-BUDGET-v1；[专题账本](research/unrelated_machines/CLAIMS.md)记录实际list构造、全agree逐图锐阈值和source soundness必要度数，不是调度hardness。

新增 UM-PARTIAL-MINREP-SPARSIFICATION-BRIDGE-v2；[专题账本](research/unrelated_machines/CLAIMS.md)明确rare-tail源、Ω(g)必要性及未实现的固定常数物理费，非一般UM hardness。

新增 UM-Q-COORDINATE-SLICE-PARTIAL-MINREP-COUNTEREXAMPLE-v4，只登记整合最终版本；[专题账本](research/unrelated_machines/CLAIMS.md)给完整实际P、精确单位阈值及保source promise反例，不升级一般hardness。


新增 UM-PARTIAL-MINREP-REGULAR-HIGH-GIRTH-SOURCE-v3；[专题账本](research/unrelated_machines/CLAIMS.md)给arbitrary-copylists同时性及正则高围长源，非UM反面。


新增UM-PARTIAL-MINREP-DEGREE-MASS-REGULARIZATION-v5；[账本](research/unrelated_machines/CLAIMS.md)明确非空typed域及任意原degree的质量复制，v4域缺口保留。


新增UM-Q-PRIVATE-INJECTIVE-TREE-CONFIGURATION-FLOOR-v2；[专题账本](research/unrelated_machines/CLAIMS.md)区分私有注入类CONFIGgap≤5/3与原非注入严格promise判定，未给一般σ算法。


新增UM-PRIVATE-TERNARY-RAINBOW-BINARY-SUBTREE-NP-COMPLETE-v1；[专题账本](research/unrelated_machines/CLAIMS.md)严格区分三叉二叉rainbow NP完全与仅5/4比值的实际调度gap。


新增有界重数配置v3、一阶锐渐近与全局叶色2/3复杂性门槛；[专题账本](research/unrelated_machines/CLAIMS.md)明确两种重数域及无一般UM结论。

UM-TWO-SMALL-INCIDENCE-SHARP-APPROXIMATION-v2：共同b>0且finite p≤b、每全行正非unit资格至多2（unit/zero无限、jobs任意共享）；确定性位poly实际3/2近似、OPT<b精确、中阈值one-sided；3DM给同域ρ<3/2除非P=NP不可能。PSM2018框架直接推广，非一般UM反证。 见[正文](research/current/unrelated_machines/joint_slot_prefix_rounding.md)。

UM-SINGLE-PINNED-TREE-MULTIPLICITY-EXACT-CONFIGURATION-GAP-v1：单强制根完整uniform树、整树每色≤µ的普通配置gap sup精确2−1/µ；det bitpoly全部σ≤2−ceil(d/µ)/d，显式底层重色+逐层衰减证书匹配；不改多state固定µ G。 [现行正文](research/current/unrelated_machines/private_injective_tree_configuration_floor.md)。

UM-TERNARY-PALETTE-TENSOR-AMPLIFICATION-OBSTRUCTION-v2：末层两色的对齐Cartesian张量YES精确OPT2−(2/3)^k，gap上包络Gk≤5/4且严格下降趋1；纯k收缩连strong(d−1)也不可，非所有放大不可能。 [现行正文](research/current/unrelated_machines/ternary_rainbow_subtree_exact_hardness.md)。

## 锚点亏缺共同选择与精确保矩的边界

[锚点缺额联合舍入](research/current/unrelated_machines/anchor_deficiency_joint_rounding.md)从同一个LP共同选择anchor位置，并让任意跨分量/异端tiny仅做一次ST；分量缺额≤d0时，实际界为`[2−(1−α)/(d0+1)+β]T`。弱OPT所用边尺度承诺下，仅上截的单调整数二分给同系数OPT保证，无额外网格损失。余秩筛选门槛`1/(d+1)`锐；未声称调度系数最优。固定身份/有界亏缺仍承重。

[强配置匹配矩边界](research/current/unrelated_machines/strong_configuration_matching_moment_obstruction.md)证明任意固定阶、所有短事件非负且本行CONFIG同阶相容，仍可没有保给定二阶的真实共同匹配law；保一阶的锐二阶修复距离为`1/[4N(N−1)]`。实际OPT1且距离趋零，非调度gap。一般输入的混合身份、无界阻塞集和允许改矩后的全机统一余量仍缺；UM-TARGET-v1保持OPEN。

[永久缓冲激活与共同解锁路径](research/current/unrelated_machines/permanent_buffer_activation_and_priority_deadlocks.md)给锐分数窗口[1/3,1/2]和静态/优先级反例；[保留坏环与实际最大件全程锐界](research/current/unrelated_machines/held_cycle_release_and_assigned_max_path.md)用共同保护来流及源补集证明：每个正阈值源有一件eligible时，给定目标的完整路径可构造；并覆盖标准有序槽实际输出。局部promise类峰U逐参数锐，不冒充实际ST输出锐性。具体τ仍是承重输入，未知目标、任意剪枝初态与一般统一次二输出仍OPEN。
