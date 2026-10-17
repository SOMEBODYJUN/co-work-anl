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

[高围长仙人掌的配置锐界与精确块算法](research/current/unrelated_machines/cactus_configuration_gap_and_block_exactness.md)表明simple cactus可同时有CONFIG supgap2和真实精确P；单环分量配置精确、最大顶点块环秩b给2^b poly算法。它们限制反面归约的结构，不证明一般目标不存在。

## 固定向量提取的真实矩边界

[投影向量正文](research/current/unrelated_machines/projected_vector_greedy_unbounded.md)严格排除一条新的具体充分规则：三机全正时间和真实OPT分布上，固定顺序max-norm左乘的比值仍无界；单位5×5还有严格2倍小证书。它不限制其他矩提取或UM-TARGET-v1。精确身份、一般事件链、审查及实际输入沿专题地图进入；一般可求共同容量/重新耦合仍未解决。
