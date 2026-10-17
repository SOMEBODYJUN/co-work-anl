# 共同研究：一般不相关并行机的统一常数2壁垒

**当前唯一主攻是 `UM-TARGET-v1`，存档为 `unrelated-machines`。** 给定一般不相关机器处理时间矩阵，寻找一个确定性算法和统一常数 ε∈(0,1)，在输入总二进制位长的多项式时间内输出完整任务分配，并对所有合法输入保证 C_max≤(2−ε)OPT。机器数、任务数均可增长；有限处理时间为非负有理数，允许不可用边，每个任务至少有一台可用机器。零最优值和空任务也须覆盖。目标仍 **OPEN**。

新对话使用[完整BOSS提示词](research/unrelated_machines/BOSS_START.md)和[最新版work.py](research/weighted_congestion_frontier/tools/work.py)，附仓库外凭据。提示词直接写明主目标、启动、通信、地图和提交操作。[操作手册](research/unrelated_machines/RUNBOOK.md)给全部命令；新建且未绑定的clone默认进入新题，已绑定旧存档的clone保持原绑定，新题另用独立clone。

团队协作改用[门控研究协议](research/unrelated_machines/TEAM_OPERATING_MODEL.md)：Claim Card→架构→盲审→red-team→复杂度审计→route gate。样本数量、随机成功率和提交数量不再作为研究进度指标。

## 研究目标与当前前沿

从[本题数学地图](research/current/unrelated_machines/README.md)进入[精确账本](research/unrelated_machines/CLAIMS.md)、[当前前沿](research/unrelated_machines/RESEARCH_STATE.md)和[失败与回收](research/unrelated_machines/FAILED_ROUTES.md)。经典LST/ST舍入、配置LP间隙是已知工具重构；现有方法障碍和结构性正面接口均未给出一般输入的统一常数改善。证明、内审、外审、实现及新颖性分别记录。

| 研究义务 | 当前可用资产与准确入口 |
| --- | --- |
| 精确模型与经典地基 | [模型、槽舍入及两树配置间隙](research/current/unrelated_machines/model_and_classical_barriers.md)；[文献与取得状态](research/unrelated_machines/LITERATURE.md) |
| 跨机器共同容量与相关性 | [长链联合投影](research/current/unrelated_machines/long_path_coalition_gap.md)、[共享逃逸与完整单机配置延伸](research/current/unrelated_machines/row_count_escape_gap.md)、[稀疏条件配置边界](research/current/unrelated_machines/sparse_conditioned_configuration_gap.md)；各自反例只限制其精确定义的接口 |
| 可恢复结构与实际联合迁移 | [极小星及配置保持](research/current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md)、[森林边界菜单](research/current/unrelated_machines/forest_boundary_contraction.md)、[真实最优边际与固定槽](research/current/unrelated_machines/optimal_convex_fixed_slot_gap.md)；一般共同选择及进展仍未闭合 |
| 新表示与可构造性 | [条件矩运输和重新耦合](research/current/unrelated_machines/symmetric_moment_reset_and_single_machine_threshold.md)、[固定向量提取的真实矩边界](research/current/unrelated_machines/projected_vector_greedy_unbounded.md)、[需求树精确桥梁](research/current/unrelated_machines/rooted_dag_degree_token_bridge.md)、[共同拥塞流接口](research/current/unrelated_machines/rooted_dag_congestion_flow.md)、[固定阶真实矩贪心的线性最坏界](research/current/unrelated_machines/truncated_multiplication_vector_greedy_barrier.md)；按正文核对给定证书、未知支撑及总位复杂度；共同流§7–10给非单位分叉参数2^h精确树，尚非一般多项式 |
| 条件困难性与gap放大 | [私有组合与资源重复边界](research/current/unrelated_machines/private_graft_and_resource_repetition.md)：精确max/min无放大、完全pool分数整数化；真正近2整数OPT soundness仍缺，不是主目标反证 |

路线是搜索种子，可以改变方法。仅有配置间隙、固定槽损失、某个见证选择困难性或特殊情形算法，均不关闭主目标。所有精确身份与新增成果沿本题地图和账本维护，根入口保持稳定，不逐轮追加摘要。

本阶段的路线复盘和下一道硬门槛见[专题前沿的全输入桥合同](research/unrelated_machines/RESEARCH_STATE.md#路线复盘从局部合同转向全输入桥)：已有成果主要诊断局部证书不足并建立受限联合构造；只有从任意输入产生可验证共同容量、实际全机整数输出及可靠阈值失败语义，才算直接推进 `UM-TARGET-v1`。

本轮的[团队资产清点矩阵](research/unrelated_machines/RESEARCH_STATE.md#团队阶段清点去重后的路线矩阵-2026-10-17)把 boss3 的条件块选择、boss6 的多目的地修复、boss7/9 的联合迁移、boss10 的反面归约和受限正面接口放回同一依赖图；工作桌面只保留入口与卡点，canonical 正文和证据不重复复制。

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

[全局四阶负载松弛的锐利二间隙](research/current/unrelated_machines/c2_unit_multislice_gap.md)（`UM-C2-LOAD-UNIT-GAP-v1`）已闭合裸C2-load本身的义务：m≥3,n=m+1单位同机上T_C2=n/m、OPT2，显式有理PSD证书给supgap2。这不同于固定贪心坏例；其三阶同机矩为负、CONFIG阈值2，故不含C2+CONFIG或一般算法困难性。一般主目标仍OPEN，下一可判别义务是含完整本地配置信息的共同矩/实际联合舍入。

[闭环容量释放](research/current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md)§11把严格下降障碍推进到弱最大负载单调小步：真实最优凸包的全部最小成本槽输出仍趋2，最小非平凡改件/参与机恰d+1；但单任务到OPT的最小峰值仅为B+1/k²。它不是一般困难性，且该cactus族可精确解。

[异端有界畸变共同组](research/current/unrelated_machines/distorted_group_joint_slot_rounding.md)在给定上下比例包络、唯一home/共同资格结构下联合选宏与接收机，给home≤(1+r+δ)T、sink≤[κ+B̄(1−r)]T，且闭合未知OPT搜索；固定κ+B̄δ<2时只有该结构类具统一改善。 一般UM-TARGET-v1仍OPEN；下一高信息义务是允许可控临时增载的共同容量修复及总位多项式进展，或在一般矩阵中生成保统一余量的相关结构。

本阶段不相关并行机新增两项可复用边界：[异质大宏统一残余容量与 ST 舍入](research/current/unrelated_machines/heterogeneous_macro_uniform_residual_st_rounding.md) 在 `|B|=|H|` 与大宏承诺下允许宏身份异质、tiny 资格任意并得到 `(3/2+δ)` 结构类界；[严格次二批量能垒](research/current/unrelated_machines/strict_sub2_batch_barrier.md) 说明常数批量且中间严格低于二倍时的局部修复会遇到 `OPT=1` 孤立坏态。两者均保持 `UM-TARGET-v1` OPEN。

[单任务外接端口的向下投影与锐计数](research/current/unrelated_machines/signed_one_job_port_downset.md)给`UM-SIGNED-ONE-JOB-PORT-DOWNSET-v1`：保留一个外部出现端点且排除外部容量时，两一致态强制至少2^z(2^a+2^b−1)个严格可行状态，固定T>0逐参数锐；不能用该纯内部接口实现等值复制。BG一般signed阈值PCSP的近二困难性不保持调度双出现限制；多任务编码及外部联合容量仍未解，UM-TARGET-v1保持OPEN。

[单层配额超图平方根重数地板](research/current/unrelated_machines/single_layer_quota_sqrt_multiplicity_floor.md)进一步证明全局资源重数 Δ 下的中间层地板为 1/(√Δ+1)−1/K（同阶上界由资源总量给出）；它把共享标签反面归约的必要碰撞规模收紧到平方级，但不是一般困难性。

[三外接机器选择器的锐三半界](research/current/unrelated_machines/three_host_selector_sharp_three_halves.md)：给only-a和b+c-free的两份实际C≤T调度，单调二色行权闭包输出only-b或only-c的完整C≤3T/2调度，且两任务锐；内部规模、资格任意，所有预载逐台核。同一机制对一般SC三特殊item给无条件可构造半值，亦锐。两者仅限制明确可用性复制接口；一般主目标和反面仍OPEN，新颖性/外审未认证。

[两状态行列池锐性修复](research/current/unrelated_machines/duplication_state_majority_floor.md)：标签可只选部分资源，s=K=4的真实最优为5/8，反驳旧附属1/2断言；主多数下界仍成立。新精确整数前沿及显式达到构造已独立重构，原K≥2s数例保留；不是一般近二困难性。

[多输出加权状态预算](research/current/unrelated_machines/weighted_fanout_profile_boundary.md)扩展三host接口：给两实际YES，对任意候选输出集K和有理β构造实际C≤(2−β_i)T；真实OPT总和≤(2|K|−1)T，加权星取等。任意两个缺一OPT之和≤3T，至多一个可严格超三半，任意扇出二叉树同时锐；不能用仅单输出近二星代替全局复制soundness。主目标保持OPEN。

[双轨阈值编码边界](research/current/unrelated_machines/dual_rail_threshold_soundness_boundary.md)：归一化scalar整类总有实际3/2（ST半质量直接推论），改unit容量亦总3/2，两种绝对T1界各有完整锐例。非均匀单例外有精确匹配合同；完整signedcube的真实OPT有min_B精确式且趋1。四成本模型分开，未将NO源自动解码为NO调度，主目标正反面仍OPEN。

[单位读出配额森林边界](research/current/unrelated_machines/unit_readout_pruned_forest_boundary.md)：一般arity下实际C<2等价全部变量mandatory r=ceil(k(2−C))森林可注入slots；但arity≤2A时，任意深度和任意wiring均有实际≤1+floor(k/2)/k≤3/2（经典ST半质量推论），14机15job绝对界锐。叶命中精确门槛(k−r+1)^h说明dummy补齐义务；相同64open的两模块真实OPT为1与7/4，叶容量不能代替祖先兼容。一般目标正反面仍OPEN。

[校准计数槽](research/current/unrelated_machines/unit_readout_calibrated_cardinality_slots.md)将单位读出树的半质量推广为有理下传证书：行分数任务数≤整数k−r+1给实际2−r/k。uniform x_h闭式提供所有wiring密度界；任意固定D≥2、arity≤D A的同结构类有确定性位poly统一2−1/(4D)算法，k,h可无界。已扣VW既有2−1/k及经典ST；D无界或一般P仍无统一ε，反面目标保持OPEN。
