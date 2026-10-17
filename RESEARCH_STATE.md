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

[全局四阶负载松弛的锐利二间隙](research/current/unrelated_machines/c2_unit_multislice_gap.md)（`UM-C2-LOAD-UNIT-GAP-v1`）已闭合裸C2-load本身的义务：m≥3,n=m+1单位同机上T_C2=n/m、OPT2，显式有理PSD证书给supgap2。这不同于固定贪心坏例；其三阶同机矩为负、CONFIG阈值2，故不含C2+CONFIG或一般算法困难性。一般主目标仍OPEN，下一可判别义务是含完整本地配置信息的共同矩/实际联合舍入。

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
