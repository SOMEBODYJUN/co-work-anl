# 共同研究：一般不相关并行机的统一常数2壁垒

**当前唯一主攻是 `UM-TARGET-v1`，存档为 `unrelated-machines`。** 给定一般不相关机器处理时间矩阵，寻找一个确定性算法和统一常数 ε∈(0,1)，在输入总二进制位长的多项式时间内输出完整任务分配，并对所有合法输入保证 C_max≤(2−ε)OPT。机器数、任务数均可增长；有限处理时间为非负有理数，允许不可用边，每个任务至少有一台可用机器。零最优值和空任务也须覆盖。目标仍 **OPEN**。

新对话使用[完整BOSS提示词](research/unrelated_machines/BOSS_START.md)和[最新版work.py](research/weighted_congestion_frontier/tools/work.py)，附仓库外凭据。提示词直接写明主目标、启动、通信、地图和提交操作；进入研究前先看[BOSS研究总览与路线分诊](research/unrelated_machines/BOSS_RESEARCH_BRIEF.md)和[当前活跃路线](research/unrelated_machines/ACTIVE_ROUTES.md)。[操作手册](research/unrelated_machines/RUNBOOK.md)给全部命令；新建且未绑定的clone默认进入新题，已绑定旧存档的clone保持原绑定，新题另用独立clone。

## 研究目标与当前前沿

从[本题数学地图](research/current/unrelated_machines/README.md)进入[精确账本](research/unrelated_machines/CLAIMS.md)、[当前前沿](research/unrelated_machines/RESEARCH_STATE.md)和[失败与回收](research/unrelated_machines/FAILED_ROUTES.md)。经典LST/ST舍入、配置LP间隙是已知工具重构；现有方法障碍和结构性正面接口均未给出一般输入的统一常数改善。证明、内审、外审、实现及新颖性分别记录。

| 研究义务 | 当前可用资产与准确入口 |
| --- | --- |
| 精确模型与经典地基 | [模型、槽舍入及两树配置间隙](research/current/unrelated_machines/model_and_classical_barriers.md)；[文献与取得状态](research/unrelated_machines/LITERATURE.md) |
| 跨机器共同容量与相关性 | [长链联合投影](research/current/unrelated_machines/long_path_coalition_gap.md)、[共享逃逸与完整单机配置延伸](research/current/unrelated_machines/row_count_escape_gap.md)、[稀疏条件配置边界](research/current/unrelated_machines/sparse_conditioned_configuration_gap.md)；各自反例只限制其精确定义的接口 |
| 可恢复结构与实际联合迁移 | [极小星及配置保持](research/current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md)、[森林边界菜单](research/current/unrelated_machines/forest_boundary_contraction.md)、[真实最优边际与固定槽](research/current/unrelated_machines/optimal_convex_fixed_slot_gap.md)；一般共同选择及进展仍未闭合 |
| 新表示与可构造性 | [条件矩运输和重新耦合](research/current/unrelated_machines/symmetric_moment_reset_and_single_machine_threshold.md)、[固定向量提取的真实矩边界](research/current/unrelated_machines/projected_vector_greedy_unbounded.md)、[需求树精确桥梁](research/current/unrelated_machines/rooted_dag_degree_token_bridge.md)、[共同拥塞流接口](research/current/unrelated_machines/rooted_dag_congestion_flow.md)、[固定阶真实矩贪心的线性最坏界](research/current/unrelated_machines/truncated_multiplication_vector_greedy_barrier.md)；按正文核对给定证书、未知支撑及总位复杂度；共同流§7–10给非单位分叉参数2^h精确树，尚非一般多项式 |
| 条件困难性与gap放大 | [私有组合与资源重复边界](research/current/unrelated_machines/private_graft_and_resource_repetition.md)：精确max/min无放大、完全pool分数整数化；另见[严格单位阈值五三界及近单位阈值分界](research/current/unrelated_machines/unit_readout_configuration_threshold_polytope.md)；真正近2整数OPT soundness仍缺，不是主目标反证 |

路线是搜索种子，可以改变方法。仅有配置间隙、固定槽损失、某个见证选择困难性或特殊情形算法，均不关闭主目标。所有精确身份与新增成果沿本题地图和账本维护，根入口保持稳定，不逐轮追加摘要。

本阶段的路线复盘和下一道硬门槛见[专题前沿的全输入桥合同](research/unrelated_machines/RESEARCH_STATE.md#路线复盘从局部合同转向全输入桥)：已有成果主要诊断局部证书不足并建立受限联合构造；只有从任意输入产生可验证共同容量、实际全机整数输出及可靠阈值失败语义，才算直接推进 `UM-TARGET-v1`。
方向审计与工作模式收口见[team_direction_audit.md](research/reviews/unrelated_machines/team_direction_audit.md)：保留自主并行和直接攻证明，按唯一承重义务配 Builder 与独立 red-team；连续两轮只增样本或同一局部机制就做 honest salvage。

本轮的[团队资产清点矩阵](research/unrelated_machines/RESEARCH_STATE.md#团队阶段清点去重后的路线矩阵-2026-10-17)把 boss3 的条件块选择、boss6 的多目的地修复、boss7/9 的联合迁移、boss10 的反面归约和受限正面接口放回同一依赖图；工作桌面只保留入口与卡点，canonical 正文和证据不重复复制。

[机器价格的精确凸化](research/current/unrelated_machines/heavy_light_price_convexification.md)已核清一条一般接口：全部标量机器价格仍只给带big基数的LST松弛，剪枝后joint gap仍sup2；最优价格共同big面提供可检验成功证书，但无全输入保证。原候选的剪枝/参数语义已修正，下一义务仍是非可加共同容量或实际联合舍入。

[子线性联合投影间隙](research/current/unrelated_machines/sublinear_coalition_projection_high_girth_gap.md)把高围长 `CC_r` 障碍加强到任意机器数子线性阶 `r(M)=o(M)`（仅机器数尺度）；[森林残余整数边界](research/current/unrelated_machines/heavy_light_forest_integrality_boundary.md)则显示重轻纯 saddle 与 `R(H)=T` 即使在森林上也可能有趋二整数缺口。两者都只是方法边界，需与共同容量和实际整数输出义务分开读取。

[一般残余容量结构](research/current/unrelated_machines/residual_throughput_and_occupation_projection.md)进一步给出固定R的容量格次模与精确占位缺口D(I)=诱导边数。任务角色随大边选择变化时，联合目标不继承该性质；这明确了下一共同选择义务，不是一般近似或困难性突破。

本阶段新增[固定工作量与中任务配置分解边界](research/questions/unrelated_machines/fixed_work_and_medium_config_barriers.md)：固定配置加 tiny 槽损失、固定总工作量和固定非减凸势的近二失败范围均已精确记录；它们只收窄方法路线，不改变 UM-TARGET-v1 的 OPEN 状态。

## 定义、命题、依赖与证据

[研究总目录](research/README.md)按模型分流；[中文资产总目录](research/CATALOG.md)说明每个文件用途；[全仓精确命题](research/current/claims.md)、[五轴状态](research/review_status.json)、[文件合同](research/assets.json)和[关系图](research/index.html)分别管理身份、审查、位置和数学依赖。有限核验只作checks，不替代一般证明。原始来源沿[来源解释](research/source_crosswalk.md)追溯。

## 协作、文件与保存

每个Work使用独立clone的main；内部subagents由boss汇集。公屏、@、私聊、收件箱和[个人桌面](research/workspaces/README.md)共用现有程序。main保存共同资产，wcg/board保存异步消息，不创建研究分支。聊天可讨论未完成想法，注明不确定性；有价值阶段完成相应核验后及时checkpoint并核对远端。

| 入口 | 用途 |
| --- | --- |
| [BOSS_START](research/unrelated_machines/BOSS_START.md) / [RUNBOOK](research/unrelated_machines/RUNBOOK.md) | 可复制完整提示词、单文件恢复、当前通信与提交命令 |
| [RESEARCH_STATE](RESEARCH_STATE.md) / [CLAIMS](CLAIMS.md) / [FAILED_ROUTES](FAILED_ROUTES.md) | 全仓前沿、精确身份分流、准确失败范围 |
| [ASSETS](ASSETS.md) / [USAGE](USAGE.md) | 按模型找资产与可运行程序 |
| [生产规则](research/REPOSITORY_GUIDE.md) / [增长规则](research/GROWTH.md) / [路线图](research/ROADMAP.md) | 读取、入库、状态与下一义务 |
| [当前课题路由](research/active_research.json) | 当前目标、save和入口的可检查合同；运行research/check_active_research.py |


当前共同构造另有[单汇点宏退出与完整profile池的共同匹配](research/current/unrelated_machines/shared_sink_joint_macro_assignment.md)；局部修复需核对[严格lex参与机数与中性路径的区别](research/current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md)。[路线整合审查](research/reviews/unrelated_machines/joint_capacity_route_feasibility_review.md)汇集结构接口、真实矩提取和一般进展的剩余义务；[条件矩正文](research/current/unrelated_machines/symmetric_moment_reset_and_single_machine_threshold.md)§9给特定族的新矩构造，仍未给一般调度保证。UM-TARGET-v1保持OPEN。

[固定数量共享汇点的占位基交换与三半调度](research/current/unrelated_machines/fixed_sink_occupation_rounding.md)给三个分离身份：UM-OCCUPATION-MODE-SIDE-CONSTRAINT-v1允许任意K但仅界定2K个分数组；UM-FIXED-SINK-PRIVATE-GROUP-THREE-HALVES-v1在固定K的给定阈值下输出实际≤3T/2；UM-FIXED-SINK-MACRO-PROMISE-APPROX-v1用含OPT的大宏promise及非单调one-sided整数二分给真正≤3OPT/2。唯一home/给定分组和固定K仍承重，通用LP软件未实现，新颖性未认证。一般主目标下一缺口是不受限的接收容量与跨home/跨尺寸任务身份，UM-TARGET-v1仍OPEN。

## 独立保留的旧研究

[加权拥塞](research/current/weighted_congestion/README.md)、[设施选址](research/current/README.md)和[顺序客户吸引](research/current/customer_attraction/README.md)各保留原模型、身份、正文和证据。拥塞的Cd/ln d全类存在命题已有线性全状态反例；其精确门槛等后续义务见旧题地图。旧目录内tools承担共享协作功能，目录名不把新题改成拥塞。旧数学交接包只用于该模型的历史追溯。

[有限覆盖与反向困难性可靠性缺口](research/current/unrelated_machines/configuration_finite_cover_obstruction.md)已给标准机制的准确调度重构：即使高围长也存在整数OPT坍缩到配置阈值的cover；精选接线与一般困难性仍未排除，UM-TARGET-v1保持OPEN。

[共同资格私有组的无界sink联合流](research/current/unrelated_machines/hall_group_joint_flow.md)：实际输出比例`q(2+δ)/(q+1)`，并有未知OPT的结构承诺版本；同组资格/等端体积及组总量范围仍承重，q增长时无统一ε。一般主目标保持OPEN，下一义务是可恢复的一般分组或异资格/异端容量转换。

## 全局分配矩的可提取条件

[全局四阶分配矩](research/current/unrelated_machines/global_assignment_moment_rounding.md)给显式小缺陷证书的确定有理实际提取，同时证明一个来自真实最优分布的全空间HS贪心仍可输出2OPT。给定证书的提取与一般输入如何生成可用证书分开；两项精确身份及经典平坦背景见账本。UM-TARGET-v1保持OPEN。

[高围长仙人掌的配置锐界与精确块算法](research/current/unrelated_machines/cactus_configuration_gap_and_block_exactness.md)表明simple cactus可同时有CONFIG supgap2和真实精确P；单环分量配置精确、最大顶点块环秩b给2^b poly算法。它们限制反面归约的结构，不证明一般目标不存在。

## 加权共同组的新增正面接口

[共同资格私有组的加权出口与联合槽](research/current/unrelated_machines/weighted_group_joint_slot_rounding.md)给`UM-WEIGHTED-GROUP-JOINT-SLOT-v1`及未知OPT的`UM-WEIGHTED-GROUP-PROMISE-APPROX-v1`：给定不交home/sink、唯一home私有组、同组共同资格与等端w_j≤δT、W_h≤T及macro端>T/2，在0≤δ<1/2时实际输出≤(3/2+δ)T（sink≤3T/2）；无组负载正下界、sink数不固定。未知OPT承诺版用单调加权LP及有理整数网格搜索。数学算法完整，软件仅实现给定精确LP见证的验证/舍入；独立审查与双路有限Fraction核验已登记，外审/新颖性未认证。一般矩阵如何生成这些分组和处理异端容量仍未解，UM-TARGET-v1保持OPEN。

[开放义务与本轮边界](research/questions/unrelated_machines/barrier_escape_obligations.md)给门槛/FPTAS结构界 `R*=((1+η)(3+δ))/(2+η)<2`。旧固定前缀恢复存在实质异议，已由同行在 `4300c26` 正确撤回完成状态；本次以同一覆盖实际恢复、修复FPTAS上界与独立冻结审查闭合原声明范围及one-sided搜索，详见[纠错复核](research/reviews/unrelated_machines/threshold_cover_and_support_release_review.md)。同页另有 `OPT=T=1` 的LST支撑反例。一般任务分解仍缺，均非一般算法或困难性证明。

同页还分离了 rank-jump-one 的真实支持引理：有限正权真实矩在 `rank(M2)=rank(M1)+1` 时可恢复 `R+1` 个原子；这不延伸到任意伪矩，也不认证公屏的 `4−2√2` 常数。

反面路线新增的可复用障碍是 [k-均匀资源束分层地板](research/current/unrelated_machines/k_uniform_bundle_matching_floor.md)：标准需求树的 (b^*) 同时由所有 (j)-of-(k) 束匹配层决定；三维匹配的 (1/2) 单终端逃逸只是特例。它把近2反面归约的真正 soundness 义务收窄为：共享标签必须同时压低所有低层束匹配，且保持固定 ε 下位多项式规模。该结果不关闭 UM-TARGET-v1。


[低重数标签资源的确定性地板与锐界](research/current/unrelated_machines/bounded_collision_label_resource_floor.md)：所选资源重数Δ给真实b≥1/Δ，二重资源对任意束宽恰保留1/2；全局不同变量组度Δ_G给无需见证的实际(2−1/Δ_G)桥梁调度。只排除该四层有界碰撞接口的近二归约；高重数/跨层一致性与一般UM-TARGET-v1仍OPEN。

进一步的[大需求束碰撞界与平方池锐性](research/current/unrelated_machines/large_bundle_collision_square_root_floor.md)给含根上取整的Λ_c真实树，q=Δ=K=t²时精确maxΛ=b*=1/t；带η→0及ηKmin→∞条件的NO侧必要量为liminfη²Δ≥1。只约束资源束接口，源问题解码和一般困难性仍缺。

[全局四阶负载松弛的锐利二间隙](research/current/unrelated_machines/c2_unit_multislice_gap.md)（`UM-C2-LOAD-UNIT-GAP-v1`）已闭合裸C2-load本身的义务：m≥3,n=m+1单位同机上T_C2=n/m、OPT2，显式有理PSD证书给supgap2。这不同于固定贪心坏例；其三阶同机矩为负、CONFIG阈值2，故不含C2+CONFIG或一般算法困难性。该裸C2命题的范围不变；后续[弱H2合取的新二间隙](research/current/unrelated_machines/weak_h2_configuration_moment_gap.md)另行关闭只共享一阶CONFIG的合同。共享行二阶在该新族上阈值精确，一般强合同与UM-TARGET-v1仍OPEN。

[闭环容量释放](research/current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md)§11把严格下降障碍推进到弱最大负载单调小步：真实最优凸包的全部最小成本槽输出仍趋2，最小非平凡改件/参与机恰d+1；但单任务到OPT的最小峰值仅为B+1/k²。它不是一般困难性，且该cactus族可精确解。

[异端有界畸变共同组](research/current/unrelated_machines/distorted_group_joint_slot_rounding.md)在给定上下比例包络、唯一home/共同资格结构下联合选宏与接收机，给home≤(1+r+δ)T、sink≤[κ+B̄(1−r)]T，且闭合未知OPT搜索；固定κ+B̄δ<2时只有该结构类具统一改善。 一般UM-TARGET-v1仍OPEN；下一高信息义务是允许可控临时增载的共同容量修复及总位多项式进展，或在一般矩阵中生成保统一余量的相关结构。

本阶段不相关并行机新增两项可复用边界：[异质大宏统一残余容量与 ST 舍入](research/current/unrelated_machines/heterogeneous_macro_uniform_residual_st_rounding.md) 在 `|B|=|H|` 与大宏承诺下允许宏身份异质、tiny 资格任意并得到 `(3/2+δ)` 结构类界；[严格次二批量能垒](research/current/unrelated_machines/strict_sub2_batch_barrier.md) 说明常数批量且中间严格低于二倍时的局部修复会遇到 `OPT=1` 孤立坏态。两者均保持 `UM-TARGET-v1` OPEN。

本轮反面研究新增两项参数化边界：[多小端柔性密度的整数流障碍](research/current/unrelated_machines/mixed_small_endpoint_density_flow_barrier.md) 证明逐机多端 small 密度固定时可由容量流直接得到严格次二调度；[固定轮 assignment Sherali--Adams 的趋二间隙](research/current/unrelated_machines/fixed_sa_assignment_gap.md) 证明固定 literal 层的局部松弛仍保留趋二 gap。它们限制具体编译和固定层舍入方法，不改变一般目标的 OPEN 状态。

[单任务外接端口的向下投影与锐计数](research/current/unrelated_machines/signed_one_job_port_downset.md)给`UM-SIGNED-ONE-JOB-PORT-DOWNSET-v1`：保留一个外部出现端点且排除外部容量时，两一致态强制至少2^z(2^a+2^b−1)个严格可行状态，固定T>0逐参数锐；不能用该纯内部接口实现等值复制。BG一般signed阈值PCSP的近二困难性不保持调度双出现限制；多任务编码及外部联合容量仍未解，UM-TARGET-v1保持OPEN。

[单层配额超图平方根重数地板](research/current/unrelated_machines/single_layer_quota_sqrt_multiplicity_floor.md)进一步证明全局资源重数 Δ 下的中间层地板为 1/(√Δ+1)−1/K（同阶上界由资源总量给出）；它把共享标签反面归约的必要碰撞规模收紧到平方级，但不是一般困难性。

[三外接机器选择器的锐三半界](research/current/unrelated_machines/three_host_selector_sharp_three_halves.md)：给only-a和b+c-free的两份实际C≤T调度，单调二色行权闭包输出only-b或only-c的完整C≤3T/2调度，且两任务锐；内部规模、资格任意，所有预载逐台核。同一机制对一般SC三特殊item给无条件可构造半值，亦锐。两者仅限制明确可用性复制接口；一般主目标和反面仍OPEN，新颖性/外审未认证。

[两状态行列池锐性修复](research/current/unrelated_machines/duplication_state_majority_floor.md)：标签可只选部分资源，s=K=4的真实最优为5/8，反驳旧附属1/2断言；主多数下界仍成立。新精确整数前沿及显式达到构造已独立重构，原K≥2s数例保留；不是一般近二困难性。

[两状态 quota orientation 的 Hall 切分解](research/current/unrelated_machines/two_state_quota_hall_cut_decomposition.md)把固定 rail 方向的部分支付精确写成所有标签子集的 Hall 邻域切，并给出整数流输出与局部缺口；联合方向选择和全方向 `FAIL⇒OPT>T` 仍未闭合。

[多输出加权状态预算](research/current/unrelated_machines/weighted_fanout_profile_boundary.md)扩展三host接口：给两实际YES，对任意候选输出集K和有理β构造实际C≤(2−β_i)T；真实OPT总和≤(2|K|−1)T，加权星取等。任意两个缺一OPT之和≤3T，至多一个可严格超三半，任意扇出二叉树同时锐；不能用仅单输出近二星代替全局复制soundness。主目标保持OPEN。

[双轨阈值编码边界](research/current/unrelated_machines/dual_rail_threshold_soundness_boundary.md)：归一化scalar整类总有实际3/2（ST半质量直接推论），改unit容量亦总3/2，两种绝对T1界各有完整锐例。非均匀单例外有精确匹配合同；完整signedcube的真实OPT有min_B精确式且趋1。四成本模型分开，未将NO源自动解码为NO调度，主目标正反面仍OPEN。

[单位读出配额森林边界](research/current/unrelated_machines/unit_readout_pruned_forest_boundary.md)：一般arity下实际C<2等价全部变量mandatory r=ceil(k(2−C))森林可注入slots；但arity≤2A时，任意深度和任意wiring均有实际≤1+floor(k/2)/k≤3/2（经典ST半质量推论），14机15job绝对界锐。叶命中精确门槛(k−r+1)^h说明dummy补齐义务；相同64open的两模块真实OPT为1与7/4，叶容量不能代替祖先兼容。一般目标正反面仍OPEN。

[校准计数槽](research/current/unrelated_machines/unit_readout_calibrated_cardinality_slots.md)将单位读出树的半质量推广为有理下传证书：行分数任务数≤整数k−r+1给实际2−r/k。uniform x_h闭式提供所有wiring密度界；任意固定D≥2、arity≤D A的同结构类有确定性位poly统一2−1/(4D)算法，k,h可无界。已扣VW既有2−1/k及经典ST；D无界或一般P仍无统一ε，反面目标保持OPEN。

[完整单位树的叶流与选择重组](research/current/unrelated_machines/unit_readout_global_leaf_flow_and_selector_mixing.md)：任意clause密度下固定h有实际(1+2^(−1/h))近似；给p份同一P完整C1见证时，N≥p的任意covered selector坐标重组有锐2−1/(2p−1)实际负载。h、p增长及NO无完整YES均承重，一般主目标及其反面OPEN，外审与新颖性未认证。

## 同点合取的新增理论边界

[弱H2与强二阶配置的分离](research/current/unrelated_machines/weak_h2_configuration_moment_gap.md)给参数化一般证明：全局C2-load与完整CONFIG仅共享同一一阶x时，正值整数间隙上确界仍为2。k≥3的多项式规模稀释星族在T=1+(k−1)/(k²+1)有显式有理共同证书，而真实OPT=2−1/k；关键是条件激活中的伪矩超额在一阶配置投影中被稀释。全局PSD、所有负载localizer、相同x配置及位复杂度均分别证明。共享行二阶的强合同则在**同一族所有T**上阈值恰等于OPT；零pair经PSD传输成全局条件单槽容量。二者是不同Claim，不能外推成一般强H2定理或计算困难性。

[完整槽包络的精确表示](research/current/unrelated_machines/slot_envelope_and_configuration_identity.md)把所有尺度的真实槽上界写成E=ΣΔp·ceil(prefix x)，证明全局min max E=OPT。固定T后逐行凸化子水平集恰CONFIG；先凸化整个上图则只剩线性分数负载。可验证完整损失并未免费解决共同选择。后续要攻共享二阶及更强跨机信息的可计算性/实际提取，或绕过这些松弛的一般构造，停止把上述已排弱合取当充分接口。

本轮研究又固定了三个承重边界：核心—私有资源的全层 matching 近二族、共同 big 选择的独立集阈值障碍、以及固定工作量下二次/排序势的单任务局部极小。它们的精确证明、独立审查和 Fraction 证据已沿本题地图登记；一般统一 (2−ε) 算法仍未得到。

[剪枝首步临时容量锐界](research/current/unrelated_machines/pruned_first_move_and_transient_peak.md)把暂时增载义务精确分成首步与全程：一般首步可确定性守住 U=max(2T,C+T/2)，固定批量环族逐参数达到，C接近2T时可需接近5T/2的常数临时峰。初态不声明ST来源，一步不保证改善；一般全程共同修复仍OPEN。

本阶段另有三项经自足推导与小型有理核验的入口：关联图反馈边参数的 `2^b·poly(L)` 精确阈值算法（`research/current/unrelated_machines/incidence_cycle_rank_exact.md`）、全阶共同矩整数提取桥（`research/current/unrelated_machines/full_degree_moment_localizer_decoding_bridge.md`）以及重轻自洽对偶证书与 YES 固定点边界（`research/current/unrelated_machines/heavy_light_saddle_certificate_and_cycle.md`）。它们均保留准确范围，不升级为一般统一小于2算法。

[逐行均匀相关读出](research/current/unrelated_machines/row_uniform_correlated_guard_rounding.md)新增限定身份 `UM-ROW-UNIFORM-CORRELATED-GUARD-HALF-RETENTION-v2` 与 `UM-ROW-UNIFORM-FLAT-STATE-THREE-HALVES-v1`：共享同一左标签仍有逐点ceil-half共同资源匹配；其显式平层原矩阵可完整输出三二调度。非均匀、重复自查询、多层祖先约束及一般UM正反面不在此结论内；外审和新颖性未认证。

[私有分叉树估值与支持域](research/current/unrelated_machines/private_tree_branching_valuation_and_minorants.md)新增精确signed demand、全叶XOS包络损失k[1−(1−1/k)^h]及single-state紧凑minorant LP；显式叶预算最大损失阶logB/loglogB。一般源计算gap和共同资源分配未由这些oracle解决；generic LP优化未实现，外审与新颖性未认证。

[近单位promise的源困难性与物理复制义务](research/current/unrelated_machines/near_unit_implication_pcsp_and_physical_copy_obligation.md)区分已证明的一般PCSP NP-hardness与仍OPEN的实际UM编译，不将source hard、ordinary non-delta或LPgap当近二反面。

[三端任务正规形](research/current/unrelated_machines/near_unit_implication_pcsp_and_physical_copy_obligation.md)保留UM-TARGET全部算法存在内容；[单位占位两见证胶合](research/current/unrelated_machines/unit_presence_two_witness_sharp_gluing.md)限制tiny裸presence复制。均非已完成主目标正反面。

[列表agreement的精确源预算](research/current/unrelated_machines/list_agreement_degree_budget_and_decoder.md)新增确定性线性地板及逐图锐全agree阈值；约束反面compiler的list accounting，非主目标结论。

[部分MinRep线性度数源](research/current/unrelated_machines/partial_minrep_linear_degree_source_and_fee_bridge.md)把一个充分的源解码费用目标降为固定常数；源的度数阶锐，实际UM收费与一致性仍缺。

[坐标切片编译的完整反例](research/current/unrelated_machines/coordinate_slice_source_compilation_counterexample.md)仍需实际源NO解码；[加权菜单表示与正规形](research/current/unrelated_machines/degree_three_weighted_menu_cube_embedding.md)可把任意normalized flat菜单精确保OPT/partialV变为K3、资源度3再入零权三坐标，标准path明确按BCG归属。[有限交互界](research/current/unrelated_machines/weighted_menu_bounded_group_interaction_rounding.md)给固定M/Δ的实际次二比；[归一化源值与状态数](research/current/unrelated_machines/normalized_weighted_menu_santa_value_and_size.md)精确SC值桥与同U菜单数锐界共同定位仍缺的normalized tiny gap，均非一般UM反面证明。


[前缀原子解码桥](research/current/unrelated_machines/succinct_prefix_atomic_decoding_bridge.md)进一步把全阶矩路线的解码义务压缩为可查询部分分配权：若生成器能保持one-hot守恒与完整逐机局部化，O(|E|)次查询即可得到T可行调度；因此真正未解的是succinct证书生成或sound FAIL，而非终端原子搜索。该接口不改变UM-TARGET-v1的OPEN状态。 同页新增 `UM-PREFIX-ATOMIC-FINITE-PRECISION-v1`：带噪最大质量选择有锐质量界，结合有理负载格点可用poly位精度恢复精确阈值；需指数小数值不等于需指数位数。共同law、真实全叶局部化及一般生成器仍承重。

## 锚点亏缺共同选择与精确保矩的边界

[锚点缺额联合舍入](research/current/unrelated_machines/anchor_deficiency_joint_rounding.md)从同一个LP共同选择anchor位置，并让任意跨分量/异端tiny仅做一次ST；分量缺额≤d0时，实际界为`[2−(1−α)/(d0+1)+β]T`。弱OPT所用边尺度承诺下，仅上截的单调整数二分给同系数OPT保证，无额外网格损失。余秩筛选门槛`1/(d+1)`锐；未声称调度系数最优。固定身份/有界亏缺仍承重。

[强配置匹配矩边界](research/current/unrelated_machines/strong_configuration_matching_moment_obstruction.md)证明任意固定阶、所有短事件非负且本行CONFIG同阶相容，仍可没有保给定二阶的真实共同匹配law；保一阶的锐二阶修复距离为`1/[4N(N−1)]`。实际OPT1且距离趋零，非调度gap。一般输入的混合身份、无界阻塞集和允许改矩后的全机统一余量仍缺；UM-TARGET-v1保持OPEN。

[永久缓冲激活与共同解锁路径](research/current/unrelated_machines/permanent_buffer_activation_and_priority_deadlocks.md)给锐分数窗口[1/3,1/2]和静态/优先级反例；[保留坏环与实际最大件全程锐界](research/current/unrelated_machines/held_cycle_release_and_assigned_max_path.md)用共同保护来流及源补集证明：每个正阈值源有一件eligible时，给定目标的完整路径可构造；并覆盖标准有序槽实际输出。局部promise类峰U逐参数锐，不冒充实际ST输出锐性。具体τ仍是承重输入，未知目标、任意剪枝初态与一般统一次二输出仍OPEN。

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


## 任意剪枝初态的已知目标路径

[任务包共同入流剥离](research/current/unrelated_machines/bundle_inflow_peeling_and_pruned_transient_sharpness.md)现给所有剪枝实际初态到给定实际τ≤T的完整det-bit-poly单件路径，峰U=max(2T,C+T/2)，并沿旧两机族证明全输入类逐参数锐性；不再需要eligible单件、assigned-max或ST来源。逐机二分profile同页。未知τ的共同选择与一般统一次二输出仍缺，UM-TARGET-v1保持OPEN。
[机器固定倍率公共尺寸精确重开](research/current/unrelated_machines/unknown_target_common_multiplier_exact_repair.md)把冻结核心公共尺寸接口扩展到机器固定倍率 `a_i q_C`，但混合尺寸共享机器与一般核心生成仍未解决。

[有界配置任务数的统一槽余量](research/current/unrelated_machines/bounded_configuration_cardinality_slot_margin.md)给固定K的确定性结构承诺算法与自足整数类型证明；[永久消元的支撑丢失](research/current/unrelated_machines/configuration_preserving_elimination_support_loss.md)则把新的共同义务说清：真实OPT凸包初态、完整单机CONFIG路径甚至双符号端点检查，都不自动保证永久删端后仍有好补全。固定K不替代一般统一ε，双符号反例也不排circuit方向；主目标保持OPEN。

## 本阶段的可复用桥梁与仍开放的主目标

[单home消环及有向需求桥](research/current/unrelated_machines/home_unit_cycle_elimination_and_directed_token_bridge.md)去掉环境DAG限制但仍输入实际调度或根树；[SC类型配置与真实匹配后端](research/current/unrelated_machines/type_profile_compression_and_matching_rank_bridge.md)补齐显式多项式列表生成并精确定位全局选择义务；[整比双尺寸中性修复](research/current/unrelated_machines/divisible_two_size_neutral_repair.md)给防循环正面控制组。均不构成一般UM统一次二算法或近二困难性，UM-TARGET-v1保持OPEN。
