# 当前研究前沿：不相关并行机

当前主攻 `UM-TARGET-v1`，存档 `unrelated-machines`：一般R∥C_max上，统一常数(2−ε)的确定性位多项式实际调度。目标仍 **OPEN**；尚无一般新近似算法。新会话用[完整提示词](research/unrelated_machines/BOSS_START.md)，从[本题地图](research/current/unrelated_machines/README.md)和[专题前沿](research/unrelated_machines/RESEARCH_STATE.md)恢复实际状态。

## 当前承重义务

| 方向 | 已有认识 | 真正尚缺 |
| --- | --- | --- |
| 下界与共同容量 | 经典配置gap、长链、共享逃逸及独立条件配置见证仍有gap2；[准确范围](research/unrelated_machines/FAILED_ROUTES.md)分别记录 | 可计算的共同多机相关性或绕开这些接口的算法，不能把方法障碍当原题困难性 |
| 实际舍入与迁移 | 真最优凸包点的固定槽和固定行包络仍可损失近2；若干显式族可跨槽或沿路径修复 | 一般输入的联合重选、允许接收机增载的共同守容，以及总位多项式进展 |
| 可恢复消元 | 极小星有精确恢复；配置保持须外部互斥；一/双边界森林有实际任务菜单 | 多个菜单共同选择、嵌套/有环核心的可恢复兼容性 |
| 条件矩与需求树 | [矩运输/重新耦合](research/current/unrelated_machines/symmetric_moment_reset_and_single_machine_threshold.md)区分固定推前与同边际重求；[共同流](research/current/unrelated_machines/rooted_dag_congestion_flow.md)给定K证书可提取1/(2K−1)，固定W最小K可求；[固定阶压缩向量贪心](research/current/unrelated_machines/truncated_multiplication_vector_greedy_barrier.md)即使真最优矩也有严格顺序无关线性坏例 | 一般重新耦合、未知支撑W的共同选择；新守恒合同已给2^h精确树（h为非单位点数），一般指数仍在；激活边际不是求解器 |
| 反面归约 | [私有组合/资源重复](research/current/unrelated_machines/private_graft_and_resource_repetition.md)有精确公式和NO变YES反例 | 对每固定ε的近2真实OPT gap、整数一致性soundness及合法输出规模，均尚未完成 |

[开放义务页](research/questions/unrelated_machines/barrier_escape_obligations.md)给共同资格/等端私有组的门槛结构界 `R*=((1+η)(3+δ))/(2+η)<2`。旧前缀恢复异议曾阻止升级，同行撤回记录保留；本次同一覆盖恢复和FPTAS上界修复经独立核查，原结构域的one-sided搜索重新闭合。一般输入如何产生分组及共同容量仍未闭。LST支撑例要求允许零质量边扩张；rank-jump-one在真实有限支持下已有闭合，一般伪矩仍缺共同交换延伸。

完整身份、正文、实际内部审查、代码和冻结证据沿[专题账本](research/unrelated_machines/CLAIMS.md)及数学地图读取。结构性结果、已知工具重构和新颖性判断分别记录，未认证统一算法或外部同行评审。

## 启动与保存状态

当前[work.py](research/weighted_congestion_frontier/tools/work.py)与checkpoint的未绑定默认统一为新题；start回执显示研究入口。已绑定shared的旧clone保留原存档；新题另用独立clone。新题默认保存本题专题目录、原始文献、共同登记与本人桌面，具体命令和显式路径规则见[本题手册](research/unrelated_machines/RUNBOOK.md)。根导航、角色提示词和嵌套规则以[课题路由合同](research/active_research.json)检查，避免旧题再次成为默认任务。


## 同步后的具体接续入口

[单汇点宏退出与完整profile池共同选择](research/current/unrelated_machines/shared_sink_joint_macro_assignment.md)已有结构性实际构造，一般多接收预算及跨home任务仍缺。[严格lex修复长链族](research/current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md)§10说明最小参与机数可增长，链尾中性预修可行，不能把该反例扩成弱C_max单调路径不可能。[条件矩正文](research/current/unrelated_machines/symmetric_moment_reset_and_single_machine_threshold.md)§9给同族独立均匀新矩的精确构造，不是一般调度算法。

[共同容量路线整合审查](research/reviews/unrelated_machines/joint_capacity_route_feasibility_review.md)区分菜单可算与核心可选、真实低秩矩存在与可求，以及实际输出和总进展；新主目标仍OPEN。以上同行正文、账本、审查及证据均随本次安全合并保留，未因重写导航而删除。

[固定数量共享汇点的占位基交换与三半调度](research/current/unrelated_machines/fixed_sink_occupation_rounding.md)给三个分离身份：UM-OCCUPATION-MODE-SIDE-CONSTRAINT-v1允许任意K但仅界定2K个分数组；UM-FIXED-SINK-PRIVATE-GROUP-THREE-HALVES-v1在固定K的给定阈值下输出实际≤3T/2；UM-FIXED-SINK-MACRO-PROMISE-APPROX-v1用含OPT的大宏promise及非单调one-sided整数二分给真正≤3OPT/2。唯一home/给定分组和固定K仍承重，通用LP软件未实现，新颖性未认证。一般主目标下一缺口是不受限的接收容量与跨home/跨尺寸任务身份，UM-TARGET-v1仍OPEN。

## 独立保留的研究线

[加权拥塞](research/current/weighted_congestion/README.md)已有每d≥2^20的无(d/10)-PNE全状态族，严格否定全类Cd/ln d保证；精确常数、有限d及外部评审等按旧账本处理。[设施](research/current/README.md)与[顺序客户吸引](research/current/customer_attraction/README.md)的独立义务见[路线图](research/ROADMAP.md)。这些成果和源文件保留，均不作为本次默认目标。

新增共同退出合同：`UM-SHARED-SINK-MACRO-EXIT-v1`允许宏任务真实退出及宏数超过home数；`UM-BOUNDED-PROFILE-EXIT-POOL-v1`在显式完整pool且`a_zc_j≤p_zj≤ρa_zc_j, p_zj≤βT`时，共同选择全部宏与私有撤离，输出home≤T、pool≤`[ρ(1+η)+β]T`，OPT≤T必成功。sink数不固定。标准cover/匹配/加权总量恢复组合，已独立审查及两路Fraction核验；一般资格、跨home任务与结构提取仍未闭合，UM-TARGET-v1仍OPEN。

[有限覆盖与反向困难性可靠性缺口](research/current/unrelated_machines/configuration_finite_cover_obstruction.md)已给标准机制的准确调度重构：即使高围长也存在整数OPT坍缩到配置阈值的cover；精选接线与一般困难性仍未排除，UM-TARGET-v1保持OPEN。

共同资格私有组现可在**sink数不固定**时共同选择macro/home/receiver：`UM-HALL-GROUP-JOINT-FLOW-v1`用每occupied组出口>T/q的Hall条件、一个整数流和真实前缀输出≤`q(2+δ)/(q+1)T`；`UM-HALL-GROUP-PROMISE-APPROX-v1`在同结构关于OPT的承诺下用有限瓶颈搜索直接输出相同比例OPT调度。q≥2、qδ<2，W_h∈[(1/2+1/q)T,T]、每私有件≤δT、同组共同资格与等端体积承重。q增长时改善可趋零；一般矩阵分组/跨home/异端时间转换仍未解。标准Hall/flow/prefix组合，未认证新颖性，UM-TARGET-v1保持OPEN。

## 全局四阶分配矩的新增义务

[共同C₂矩与近平坦提取](research/current/unrelated_machines/global_assignment_moment_rounding.md)把“有共同相关性”细化为可计算的投影缺陷δ：足够小δ时可位多项式输出实际(1+3δ)T。此证书是额外输入；真实最优均匀矩也能使无小δ保护的固定全空间HS贪心达到2OPT。下一承重义务是一般可生成的共同容量信息与大缺陷舍入，不能免费要求所有OPT≤T实例生成近乎精确证书。

[高围长仙人掌的配置锐界与精确块算法](research/current/unrelated_machines/cactus_configuration_gap_and_block_exactness.md)表明simple cactus可同时有CONFIG supgap2和真实精确P；单环分量配置精确、最大顶点块环秩b给2^b poly算法。它们限制反面归约的结构，不证明一般目标不存在。

## 固定向量提取的真实矩边界

[投影向量正文](research/current/unrelated_machines/projected_vector_greedy_unbounded.md)严格排除一条新的具体充分规则：三机全正时间和真实OPT分布上，固定顺序max-norm左乘的比值仍无界；单位5×5还有严格2倍小证书。它不限制其他矩提取或UM-TARGET-v1。精确身份、一般事件链、审查及实际输入沿专题地图进入；一般可求共同容量/重新耦合仍未解决。

## 加权共同组的新增正面接口

[共同资格私有组的加权出口与联合槽](research/current/unrelated_machines/weighted_group_joint_slot_rounding.md)给`UM-WEIGHTED-GROUP-JOINT-SLOT-v1`及未知OPT的`UM-WEIGHTED-GROUP-PROMISE-APPROX-v1`：给定不交home/sink、唯一home私有组、同组共同资格与等端w_j≤δT、W_h≤T及macro端>T/2，在0≤δ<1/2时实际输出≤(3/2+δ)T（sink≤3T/2）；无组负载正下界、sink数不固定。未知OPT承诺版用单调加权LP及有理整数网格搜索。数学算法完整，软件仅实现给定精确LP见证的验证/舍入；独立审查与双路有限Fraction核验已登记，外审/新颖性未认证。一般矩阵如何生成这些分组和处理异端容量仍未解，UM-TARGET-v1保持OPEN。

新反面障碍 [k-均匀资源束分层地板](research/current/unrelated_machines/k_uniform_bundle_matching_floor.md) 已入账：标准层状需求树满足 (b^*=\max_t\min(\nu_t/q,t/K))，必须同时控制所有 (j)-of-(k) 选择层。它推广三维匹配的单终端地板，并排除仅提高需求、复制资源或压低完整超边匹配的近2归约；主目标仍开放。


[低重数标签资源的确定性地板与锐界](research/current/unrelated_machines/bounded_collision_label_resource_floor.md)：所选资源重数Δ给真实b≥1/Δ，二重资源对任意束宽恰保留1/2；全局不同变量组度Δ_G给无需见证的实际(2−1/Δ_G)桥梁调度。只排除该四层有界碰撞接口的近二归约；高重数/跨层一致性与一般UM-TARGET-v1仍OPEN。

进一步的[大需求束碰撞界与平方池锐性](research/current/unrelated_machines/large_bundle_collision_square_root_floor.md)给含根上取整的Λ_c真实树，q=Δ=K=t²时精确maxΛ=b*=1/t；带η→0及ηKmin→∞条件的NO侧必要量为liminfη²Δ≥1。只约束资源束接口，源问题解码和一般困难性仍缺。

[全局四阶负载松弛的锐利二间隙](research/current/unrelated_machines/c2_unit_multislice_gap.md)（`UM-C2-LOAD-UNIT-GAP-v1`）已闭合裸C2-load本身的义务：m≥3,n=m+1单位同机上T_C2=n/m、OPT2，显式有理PSD证书给supgap2。这不同于固定贪心坏例；其三阶同机矩为负、CONFIG阈值2，故不含C2+CONFIG或一般算法困难性。该裸C2命题的范围不变；后续[弱H2合取的新二间隙](research/current/unrelated_machines/weak_h2_configuration_moment_gap.md)另行关闭只共享一阶CONFIG的合同。共享行二阶在该新族上阈值精确，一般强合同与UM-TARGET-v1仍OPEN。

[闭环容量释放](research/current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md)§11把严格下降障碍推进到弱最大负载单调小步：真实最优凸包的全部最小成本槽输出仍趋2，最小非平凡改件/参与机恰d+1；但单任务到OPT的最小峰值仅为B+1/k²。它不是一般困难性，且该cactus族可精确解。

[异端有界畸变共同组](research/current/unrelated_machines/distorted_group_joint_slot_rounding.md)在给定上下比例包络、唯一home/共同资格结构下联合选宏与接收机，给home≤(1+r+δ)T、sink≤[κ+B̄(1−r)]T，且闭合未知OPT搜索；固定κ+B̄δ<2时只有该结构类具统一改善。 一般UM-TARGET-v1仍OPEN；下一高信息义务是允许可控临时增载的共同容量修复及总位多项式进展，或在一般矩阵中生成保统一余量的相关结构。

[单任务外接端口的向下投影与锐计数](research/current/unrelated_machines/signed_one_job_port_downset.md)给`UM-SIGNED-ONE-JOB-PORT-DOWNSET-v1`：保留一个外部出现端点且排除外部容量时，两一致态强制至少2^z(2^a+2^b−1)个严格可行状态，固定T>0逐参数锐；不能用该纯内部接口实现等值复制。BG一般signed阈值PCSP的近二困难性不保持调度双出现限制；多任务编码及外部联合容量仍未解，UM-TARGET-v1保持OPEN。

[三外接机器选择器的锐三半界](research/current/unrelated_machines/three_host_selector_sharp_three_halves.md)：给only-a和b+c-free的两份实际C≤T调度，单调二色行权闭包输出only-b或only-c的完整C≤3T/2调度，且两任务锐；内部规模、资格任意，所有预载逐台核。同一机制对一般SC三特殊item给无条件可构造半值，亦锐。两者仅限制明确可用性复制接口；一般主目标和反面仍OPEN，新颖性/外审未认证。

本轮反面路线补充两项精确边界：BCG 的 Santa/Max-Min 困难性是 additive forest/all-sources 模型，Bamas 的 MMDA SA gap仍非计算硬度；两份内部无冲突的完整复制在当前需求树中有资源二着色的一半地板。需求 \(k_v>1\) 的 token 桥梁也不保持 restricted Santa 固有值结构。UM-TARGET-v1 仍 OPEN，真正缺口仍是跨层整数一致性与每固定 ε 的实际 OPT gap。

[两状态行列池锐性修复](research/current/unrelated_machines/duplication_state_majority_floor.md)：标签可只选部分资源，s=K=4的真实最优为5/8，反驳旧附属1/2断言；主多数下界仍成立。新精确整数前沿及显式达到构造已独立重构，原K≥2s数例保留；不是一般近二困难性。

[多输出加权状态预算](research/current/unrelated_machines/weighted_fanout_profile_boundary.md)扩展三host接口：给两实际YES，对任意候选输出集K和有理β构造实际C≤(2−β_i)T；真实OPT总和≤(2|K|−1)T，加权星取等。任意两个缺一OPT之和≤3T，至多一个可严格超三半，任意扇出二叉树同时锐；不能用仅单输出近二星代替全局复制soundness。主目标保持OPEN。

[双轨阈值编码边界](research/current/unrelated_machines/dual_rail_threshold_soundness_boundary.md)：归一化scalar整类总有实际3/2（ST半质量直接推论），改unit容量亦总3/2，两种绝对T1界各有完整锐例。非均匀单例外有精确匹配合同；完整signedcube的真实OPT有min_B精确式且趋1。四成本模型分开，未将NO源自动解码为NO调度，主目标正反面仍OPEN。

[单位读出配额森林边界](research/current/unrelated_machines/unit_readout_pruned_forest_boundary.md)：一般arity下实际C<2等价全部变量mandatory r=ceil(k(2−C))森林可注入slots；但arity≤2A时，任意深度和任意wiring均有实际≤1+floor(k/2)/k≤3/2（经典ST半质量推论），14机15job绝对界锐。叶命中精确门槛(k−r+1)^h说明dummy补齐义务；相同64open的两模块真实OPT为1与7/4，叶容量不能代替祖先兼容。一般目标正反面仍OPEN。

[校准计数槽](research/current/unrelated_machines/unit_readout_calibrated_cardinality_slots.md)将单位读出树的半质量推广为有理下传证书：行分数任务数≤整数k−r+1给实际2−r/k。uniform x_h闭式提供所有wiring密度界；任意固定D≥2、arity≤D A的同结构类有确定性位poly统一2−1/(4D)算法，k,h可无界。已扣VW既有2−1/k及经典ST；D无界或一般P仍无统一ε，反面目标保持OPEN。

## 机器价格联合残余：本轮核实的范围

[精确凸化正文](research/current/unrelated_machines/heavy_light_price_convexification.md)证明逐价格重选H恰等价LST+big分数基数，剪枝后相对共同见证仍supgap2；漏剪枝时固定m的锐界m。旧两机候选只演示量词差别，OPT>T；新正文补全部β的参数族、可检验的最优价格共同big面成功分支。这个分支失败没有sound FAIL语义，且一般存在性未证。提高β后再付粗ST加性slack仍受已存半单位promise障碍。主目标继续OPEN；后续只推进非可加共同容量或直接联合舍入，停止仅机器价格/逐机anchor凸化的微调。

## 一般残余容量性质与共同选择的第一缺口

[固定R容量格次模/占位图表示](research/current/unrelated_machines/residual_throughput_and_occupation_projection.md)已自足证明并独立攻击：异端资格无结构要求的F(c)格次模、固定占位缺口D超模；2×2原矩阵证明H改变任务身份后联合目标并不继承。严格次二α下还能精确实现D(I)=诱导边数，原OPT1仍显式可解。这次增加了可复用的状态理论，尚未闭合全输入桥中的共同选择。下一高信息命题必须同时处理R(H)与h(H)并分析实际联合损失；不继续以更多固定R/独立集样本替代它。

[完整单位树的叶流与选择重组](research/current/unrelated_machines/unit_readout_global_leaf_flow_and_selector_mixing.md)：任意clause密度下固定h有实际(1+2^(−1/h))近似；给p份同一P完整C1见证时，N≥p的任意covered selector坐标重组有锐2−1/(2p−1)实际负载。h、p增长及NO无完整YES均承重，一般主目标及其反面OPEN，外审与新颖性未认证。

## 弱H2义务闭合与强行二阶的下一缺口

已证明[弱H2的supgap2](research/current/unrelated_machines/weak_h2_configuration_moment_gap.md)，精确身份UM-WEAK-H2-CONFIG-MOMENT-GAP-v1；它让全局四阶C2与完整配置**共享同一一阶点**，超出旧裸C2或彼此独立探针。通用整数N≥m+1的multislice PSD、条件张量与混合、所有localizer、同x CONFIG1、真实OPT和编码长度均有一般推导。故弱H2不再是尚未排除的统一相对T舍入路线。

同页UM-STRONG-H2-ROW-PAIR-STAR-EXACT-v1证明共享行二阶后该族阈值恰OPT，不只是当前伪矩失效。真正仍缺的是一般强系统的有效求解/误差预算与统一实际舍入；其对偶二次pricing问题不能偷换为旧线性背包，也不能把pricing困难性自动升级为整个系统困难性。全部三阶非负的另一强化同样仍待一般研究。

[槽包络精确身份](research/current/unrelated_machines/slot_envelope_and_configuration_identity.md)又说明：完整实际槽损失的非凸联选本身恰重述原OPT；先固定容量再逐行凸化恰CONFIG，直接凸化函数上图仅LST。此处已关闭表示/退化识别，并未得到一般优化器或近二困难性。下一步只攻新增共同信息或可近似非凸进展机制，不以更多局部包络或样本替代。UM-TARGET-v1仍OPEN。

[配置正部阈值与严格单位五三界](research/current/unrelated_machines/unit_readout_configuration_threshold_polytope.md)：完整私有单位树的CONFIG(T<2)恰由Σ(q−t)+≤floor(k(T−1))q描述；CONFIG1等价整轨LP并有完整C≤5/3输出（偶k≤3/2，k1≤1）。闭合两树精确Tconf=1+s*/k，经典gap族仍为1+1/k，故不外推为一般次二或近二困难性。 主目标及反面仍OPEN，严格1与1+1/k的阈值区别已核清。

首步暂时容量已有[分段锐界](research/current/unrelated_machines/pruned_first_move_and_transient_peak.md)：T剪枝二倍初态可计算地找到≤max(2T,C+T/2)的一步，或在当前值>T且无此步时可靠拒绝T；固定批量环族达到这一首步阈值。剩余关键义务是维持全程共同容量并保证终态改善/位多项式进展；目前既无一般5T/2路径定理，也无从未知目标生成次二输出。

本阶段另有三项可复用边界：关联图反馈边参数的 `2^b·poly(L)` 精确阈值算法、全阶共同矩到真实整数调度的原子提取桥，以及重轻自洽对偶证书并在 `OPT≤T` YES 实例上的纯固定点反例。它们分别关闭低环秩子类、钉死共同矩的全阶承重义务、并否定把逐价最佳响应当作一般共同选择器；`UM-TARGET-v1` 仍 OPEN。

本轮新增两条精确边界：`UM-SUBLINEAR-CC-PROJECTION-GAP-v1` 将长链高围长障碍对角化到任意机器数子线性阶 `r(M)=o(M)`，但明确不宣称总编码位长结论或一般困难性；`UM-HEAVY-LIGHT-FOREST-INTEGRALITY-BARRIER-v1` 给出重轻纯 saddle、森林残余与 `R(H)=T` 仍可产生趋二整数缺口的参数族。后者把“分数角色选择”和“整数容量补全”分成独立承重义务：反馈边森林算法可以可靠 `FAIL`，残余 LP 数值不能替代它。两条均有 Fraction/计数审计，`UM-TARGET-v1` 仍 OPEN。

[逐行均匀相关读出](research/current/unrelated_machines/row_uniform_correlated_guard_rounding.md)新增限定身份 `UM-ROW-UNIFORM-CORRELATED-GUARD-HALF-RETENTION-v2` 与 `UM-ROW-UNIFORM-FLAT-STATE-THREE-HALVES-v1`：共享同一左标签仍有逐点ceil-half共同资源匹配；其显式平层原矩阵可完整输出三二调度。非均匀、重复自查询、多层祖先约束及一般UM正反面不在此结论内；外审和新颖性未认证。

pDM阈值桥的[合入审查](research/reviews/unrelated_machines/pdm_threshold_domain_and_gap_review.md)保留原v1完整源域及gap方向异议：非退化固定参数域的算术内核成立，但尚未写显然NO/空YES合法分支；加一是NO下界。合法编译另由已有槽定理给(1,1+1/d) promise边界。原v1暂记条件性，不以默补假设维持完整归约状态。

[显式树源表示](research/current/unrelated_machines/private_tree_branching_valuation_and_minorants.md)已区分精确需求与共同资源分配，并量化XOS下包络损失；它是反面归约工具，不是主目标正反证明。

[一般近单位promise源](research/current/unrelated_machines/near_unit_implication_pcsp_and_physical_copy_obligation.md)的strong-fixing困难性已闭合，真实任务类型/全机负载/source decoder仍未闭合。两端三型与native多端one-hot/one-cold都是可研究接口；没有把two-occurrence或DAG设为主目标限制。

[实际任务正规形](research/current/unrelated_machines/near_unit_implication_pcsp_and_physical_copy_obligation.md)把全输入统一次二问题等价保在SU两端与三端unit onehot，并给完整<2b解码/零值未知OPT处理；[tiny两见证胶合](research/current/unrelated_machines/unit_presence_two_witness_sharp_gluing.md)使裸unit-presence复制在a<1/3有绝对<2逃逸。前者是表示/工具，后者是接口界，主目标及反面仍OPEN。

[源列表度数预算](research/current/unrelated_machines/list_agreement_degree_budget_and_decoder.md)经独立重构/读后攻击：agr≥L(D−1)/(2d+L(D−1))、all-agree阈值ceil2d/D逐图锐。当前反面仍缺能使每个新增label/component付多incidence费用的真实P；不以O(|B|)总list预算冒充可用source decoder。

[部分MinRep源](research/current/unrelated_machines/partial_minrep_linear_degree_source_and_fee_bridge.md)已核Δ=O(g)及同阶必要性，固定参数随机源采用NP不包含BPP；不把源进展升级为UM反面，继续攻真实常数费用/π接口。

[坐标slice路线](research/current/unrelated_machines/coordinate_slice_source_compilation_counterexample.md)经两阶段独立审查：source NO与actualOPT1+1/D可并存，private-output padding保NO，双射和精确CONFIG1仍不足。下一义务为实际跨test耦合，主反面保持OPEN。


[部分MinRep源](research/current/unrelated_machines/partial_minrep_linear_degree_source_and_fee_bridge.md)已加强为固定高围长、simple、exact regular；任意复制列表NO同时性已核，仍无实际UM弱调度decoder。


[源v5](research/current/unrelated_machines/partial_minrep_linear_degree_source_and_fee_bridge.md)用t_v=deg(v)z补任意源的regularization，并保typed exactfibers；可接FMW新perfect4to1 Paper Fact，未得实际UM编译。


[私有注入树五三界](research/current/unrelated_machines/private_injective_tree_configuration_floor.md)用共同a树分布和Haxell限制任意端口重编号；反面继续在重复叶色/增长height或共享内部等域外机制，主目标OPEN。


[重复叶色三叉锚点](research/current/unrelated_machines/ternary_rainbow_subtree_exact_hardness.md)确有SAT归约与完整P阈值，height随输入增长；放大到near2尚未给出。


[私有树重数界](research/current/unrelated_machines/private_injective_tree_configuration_floor.md)得到G(μ)=2−1/μ+O(μ^−2)；[三叉彩虹](research/current/unrelated_machines/ternary_rainbow_subtree_exact_hardness.md)在全局每色2次总YES、3次NP完全。锐性均在限定对象，主目标正反面OPEN。

[共同b双small行实际sharp3/2](research/current/unrelated_machines/joint_slot_prefix_rounding.md)已双陈述先行/双读后审查并root精确核验；PSM2018框架直接推广，旧row-spread域不改。near2须退出该行结构并有真实低σ解码，一般目标正反面仍OPEN。

[单强制根的µ精确gap](research/current/unrelated_machines/private_injective_tree_configuration_floor.md)已证明sup=2−1/µ；[三叉自然放大限制](research/current/unrelated_machines/ternary_rainbow_subtree_exact_hardness.md)已核YES实际漂移和纯收缩失效。两者均实际陈述先行/读后内审；前者不是多state Gµ，后者不排所有张量，主目标正反面仍OPEN。

## 锚点亏缺共同选择与精确保矩的边界

[锚点缺额联合舍入](research/current/unrelated_machines/anchor_deficiency_joint_rounding.md)从同一个LP共同选择anchor位置，并让任意跨分量/异端tiny仅做一次ST；分量缺额≤d0时，实际界为`[2−(1−α)/(d0+1)+β]T`。弱OPT所用边尺度承诺下，仅上截的单调整数二分给同系数OPT保证，无额外网格损失。余秩筛选门槛`1/(d+1)`锐；未声称调度系数最优。固定身份/有界亏缺仍承重。

[强配置匹配矩边界](research/current/unrelated_machines/strong_configuration_matching_moment_obstruction.md)证明任意固定阶、所有短事件非负且本行CONFIG同阶相容，仍可没有保给定二阶的真实共同匹配law；保一阶的锐二阶修复距离为`1/[4N(N−1)]`。实际OPT1且距离趋零，非调度gap。一般输入的混合身份、无界阻塞集和允许改矩后的全机统一余量仍缺；UM-TARGET-v1保持OPEN。

[永久缓冲激活与共同解锁路径](research/current/unrelated_machines/permanent_buffer_activation_and_priority_deadlocks.md)给锐分数窗口[1/3,1/2]和静态/优先级反例；[保留坏环与实际最大件全程锐界](research/current/unrelated_machines/held_cycle_release_and_assigned_max_path.md)用共同保护来流及源补集证明：每个正阈值源有一件eligible时，给定目标的完整路径可构造；并覆盖标准有序槽实际输出。局部promise类峰U逐参数锐，不冒充实际ST输出锐性。具体τ仍是承重输入，未知目标、任意剪枝初态与一般统一次二输出仍OPEN。

UM-TARGET-v1限定新资产（2026-10-18）：[一般双见证查询分离与锐3/2费用合同](research/current/unrelated_machines/two_witness_query_separation.md)、[单home完整查询模式](research/current/unrelated_machines/single_home_cascade_query_separation.md)、[超立方菜单的Hall与锐3/2](research/current/unrelated_machines/coordinate_slice_source_compilation_counterexample.md)。均已实际独立内审；是给定见证/结构类的边界，不构成主命题正反面证明。精确身份、输入域、实现和未覆盖义务以本题账本为准。


[QUERY-COUNT-FEE-v3](research/current/unrelated_machines/two_witness_query_separation.md)进一步排除单件tiny聚合读取的固定费逃逸：正T两strict模式、β≥3/2，W≤κF迫至少d−2floorκ枚query旧端>(β−1)T。条件性改派费必要界，不是UM困难性；零质量原异议已修复。


[严格重中端占位gap胶合](research/current/unrelated_machines/unit_presence_two_witness_sharp_gluing.md)允许cross-role且两strict见证下给2−gap/2的完整mixed，但不锁job身份。共同尺寸精确重开已修复冻结baseline guard与孤立机遗漏；仅tiny审计，主目标仍OPEN。


[保护环共享子句OR错配](research/current/unrelated_machines/near_unit_implication_pcsp_and_physical_copy_obligation.md)记录一个完整物理接线失败：同一共同匹配让所有SAT/UNSAT公式都strict≤1。只排该接法，重试必须防实际身份交换；主目标未升级。


[有界菜单两组资源联合近似](research/current/unrelated_machines/degree_two_group_bounded_menu_joint_rounding.md)给特定weighted menu类相对OPT的2−1/(2K)；结合旧VW MaxMin算法的直接结构推论，非generalUM。Q2、固定K的加权重试仍不能承载近2严格unit源；重试需真实突破跨组degree/菜单或原矩阵结构，主目标未解。 [有限组交互](research/current/unrelated_machines/weighted_menu_bounded_group_interaction_rounding.md)另给任意K、固定M/Δ的实际改善；[三坐标与三态正规形](research/current/unrelated_machines/degree_three_weighted_menu_cube_embedding.md)精确保OPT/V把任意normalized flat源降K3/资源度3再入zero cube，标准path已核BCG归属。[SC值桥/菜单数锐界](research/current/unrelated_machines/normalized_weighted_menu_santa_value_and_size.md)只排同U逐玩家shortcut。原source无须先限K/Δ，剩余承重仍是norm1与全partial导出的tiny-gap NO decoder，主目标未解。

[笛卡尔菜单的反向放大与一致性差距](research/current/unrelated_machines/cartesian_menu_recoupling_and_coordinate_consistency.md)：一个明确裸product实际OPT=1+2^-t趋1；额外逐坐标语义的配额却为floor((3/2)^t)/2^t趋0。两精确值排同族常数保值事后修复，尚缺真实负载实现的一致性；只否定该放大合同，非一般困难性。

[分块一致性、线性秩与全域缺项标尺](research/current/unrelated_machines/cartesian_menu_block_coherence_rank_and_deficit.md)回收已完成的精确结构：bounded blocks才指数衰减，无环单输入链仍保1/2；q元affine重选与coordinate一致相反极限；并发投影给任意nonlinear缺项必要条件。均未实现物理coherence；主反向承重继续是低负载全局decoder，停止以更多局部tensor数值代替该义务。

[逐机统一内部索引交换](research/current/unrelated_machines/machine_uniform_query_return_index_exchange.md)、[direct共居严格SAT及三半锐逃逸](research/current/unrelated_machines/direct_cohabiting_query_return_strict_sat_and_sharp_escape.md)与[真实直线源/累计路径编译障碍](research/current/unrelated_machines/line_set_packing_and_take_continue_compilation_obstructions.md)关闭各自精确接口；全部原jobs和全机负载已核，未关闭近二源NO的全局decoder。标准matching/Hall扣除新颖性，E曾误标签的proof-aware审查已另冻纠正，并由真正statement-first重构补齐。只有明确改变外部共同容量/partial AND机制时才重试这些具体桥。

[任意异权私有子句的三半上界与共享外端边界](research/current/unrelated_machines/general_weighted_private_clause_exchange_and_shared_outside_boundary.md)：固定辅助内部single-query/single-return接口的3T/2交换可与真实变量环共同匹配，所有局部索引strict可选时整公式实际≤1.5T；不是私有outside免费替ring。标准四任务环与小query返回池允许共享外部身份，但孤立OPT1且未保变量一致性。重试须改变精确模板的共同容量/边界，不能仅在私有Hc增加异权aux；主源NO联合decoder仍未闭合。

[仿射线逐tuple加globaldummy的完整编译](research/current/unrelated_machines/affine_line_tuple_groups_global_dummy_compilation_escape.md)另行关闭一种此前未分析的自然桥：n个tuple groups配n−q个共享dummy、q≤非空relations数，strict unit iff原full-set packing≥q，但无需源解仍actual≤1.5。选择q个不同relations恢复Hall不变量，所有未选state任务保留；不把这个新精确范围倒改成旧D已排，也不外推其它全局守卫/权重/阈值。

[完整归一化菜单的配置证书保持](research/current/unrelated_machines/normalized_menu_configuration_certificate_preservation.md)补足normalform的分数合同：flat machine CONFIG(1) iff positive-support FSLP iff state-dummy SC CONFIG(1)，zero原jobs仍全覆盖；再接SC路径得到rowtotal≤3/item正度≤3而CONFIG1/actual1/D。只排此LP充分性，未排actualOPT≥1的promise常数算法；标准路径/旧gap非新源，主目标OPEN。

[并行sum关系任意状态重赋权的半保留](research/current/unrelated_machines/weighted_affine_parallel_relation_reweighting_obstruction.md)补上不同范围：source value1/R的完整并行sum关系，即使任意state-dependent非负norm1权，仍可实际半保留/全部job≤1.5。条件于整个state保持c均匀，再把共点交唯一例外；singleton关系能V0，故不推广任意关系，不排避开本族的hard image。

[异权内部与重读口的bulk OR实际三半逃逸](research/current/unrelated_machines/bulk_or_commit_two_witness_interpolation.md)给完整block-ring双池下任意异权I/正C时间(.5,1]的committer：两个不同一真全原strict见证经半项配对/共同流，仍有全False全部原job实际≤1.5。内部异权collector与重C都不能单独挡split；缺两全局strict见证的跨子句NO不在范围，不是near2源。

[单标签边际均匀LINE的趋二实际间隙](research/current/unrelated_machines/tagged_affine_line_uniform_marginal_gap.md)给真LINE反例：每incidence label均匀、各state norm1，但V=1/(R−1)/实际OPT=2−1/(R−1)；共同arityR与R-partite可zero padding保值。此非pairwise-independent原hard image，未给源value/CONFIG新结论/计算困难性。

[宽矩形LINE的重细资源共同避冲突](research/current/unrelated_machines/tagged_affine_line_wide_rectangle_joint_escape.md)给出明确额外状态自由度：L>b(D−1)逐组避开旧marks，再以同一B保marks/独占点、每组损失≤Mβ；sparse正点给actual1，L>2q(D−1)²任意权给actual≤1.5。所有固定截距/原jobs保留，不把PI或alphabet可增当rectangle前提。

[两完整actual插值与实际used池端义务](research/current/unrelated_machines/bulk_or_commit_two_witness_interpolation.md)新增同页§6–10 v4：任意P的两actual与指定F原端改派，剩余job双出现配对得逐机件数与负载同τ；bulk J可接全部非pool仍全False≤1.5，任意pool得≤1.5+d/2，真正排near2须已用近unit J_pool身份改变。旧v3前缀/强输出范围保留；未知两witness不免费，不是sourceNO。

[仿射线两两独立的结构边界](research/current/unrelated_machines/tagged_affine_line_pairwise_independence_boundary.md)：单primary/onehot helpers在指定pairwise边际下可按条件化Hall全部actual1；多primary公共4D simplex陪集族则所有local pairs uniform仍V=2/(R+1)/实际OPT=2−2/(R+1)，common q/partite/全部zero jobs保留。后者只删唯一main即unit，不是robust或hard image/主反面。


## 已知目标的任意多件共同释放已闭合

新UM-LOCAL-BUNDLE-SHIELD-PATH-v1/UM-PRUNED-BUNDLE-PEELING-PATH-v1由任务包、内部入流剥离、逆序激活和补集释放闭合全部剪枝初态的给定τ全程U路径。旧all-small activation OPEN已由[新正文](research/current/unrelated_machines/bundle_inflow_peeling_and_pruned_transient_sharpness.md)关闭；下一主目标承重点是未知目标的共同容量与可靠失败语义，不继续增加已知τ样本。U可≥2T，不能误作最终次二算法。

[有界配置任务数的统一槽余量](research/current/unrelated_machines/bounded_configuration_cardinality_slot_margin.md)给固定K的确定性结构承诺算法与自足整数类型证明；[永久消元的支撑丢失](research/current/unrelated_machines/configuration_preserving_elimination_support_loss.md)则把新的共同义务说清：真实OPT凸包初态、完整单机CONFIG路径甚至双符号端点检查，都不自动保证永久删端后仍有好补全。固定K不替代一般统一ε，双符号反例也不排circuit方向；主目标保持OPEN。
当前剩余核心义务：从任意输入可计算地选择共同方向/容量状态，保住或恢复真实整数补全，并给统一余量和总位多项式进展；本轮没有关闭这些义务。
