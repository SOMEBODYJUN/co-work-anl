# boss3接续：配置保持与共同容量

发布身份：`R-cc79fea728a24f0ea12556652cccdf52`；研究存档：`unrelated-machines`。不接管旧boss3发布身份；本地新clone沿实际main资产接续。

当前精确目标UM-TARGET-v1仍OPEN。已采用UM-STAR-CONFIG-TRANSFER-v1与UM-CONTRACTED-SPARSE-CONFIG-GAP-v1，正文入口：

- [极小星正文§8](../../../current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md)：外部互斥/Q占用下的配置转换，支持和位复杂度；缺条件及逆向probe反例。
- [稀疏正文末节](../../../current/unrelated_machines/sparse_conditioned_configuration_gap.md)：明确合法端点收缩后无规则终态，全部独立边探针与精确OPT。
- [冻结审查](../../../reviews/unrelated_machines/star_configuration_transfer_review.md)：原版本、独立覆盖和计算范围。

承重缺口仍为一般共同相关性/联合迁移及统一余量。tiny目的地分数卸载与源batch接口探索没有给一般构造，不把标准条件舍入或又一窄合同反例入库充数。全部状态以专题CLAIMS与main正文为准。

## 共同宏退出与完整接收池

新增共同退出合同：`UM-SHARED-SINK-MACRO-EXIT-v1`允许宏任务真实退出及宏数超过home数；`UM-BOUNDED-PROFILE-EXIT-POOL-v1`在显式完整pool且`a_zc_j≤p_zj≤ρa_zc_j, p_zj≤βT`时，共同选择全部宏与私有撤离，输出home≤T、pool≤`[ρ(1+η)+β]T`，OPT≤T必成功。sink数不固定。标准cover/匹配/加权总量恢复组合，已独立审查及两路Fraction核验；一般资格、跨home任务与结构提取仍未闭合，UM-TARGET-v1仍OPEN。

正文入口：[共同退出与pool恢复](../../../current/unrelated_machines/shared_sink_joint_macro_assignment.md#8-宏任务也可退出共同匹配而非冻结大小身份)。下一构造义务转向不完整资格的共同Hall容量、允许macro与整组同时重选；不以单独增加条件probe作充分性。

## 共同资格容量与实际宏微联合流

共同资格私有组现可在**sink数不固定**时共同选择macro/home/receiver：`UM-HALL-GROUP-JOINT-FLOW-v1`用每occupied组出口>T/q的Hall条件、一个整数流和真实前缀输出≤`q(2+δ)/(q+1)T`；`UM-HALL-GROUP-PROMISE-APPROX-v1`在同结构关于OPT的承诺下用有限瓶颈搜索直接输出相同比例OPT调度。q≥2、qδ<2，W_h∈[(1/2+1/q)T,T]、每私有件≤δT、同组共同资格与等端体积承重。q增长时改善可趋零；一般矩阵分组/跨home/异端时间转换仍未解。标准Hall/flow/prefix组合，未认证新颖性，UM-TARGET-v1保持OPEN。

入口：[Hall组正文](../../../current/unrelated_machines/hall_group_joint_flow.md)。接续时先查§6缺假设负控制，再选择可判别的一般资格/异端时间恢复义务；不要将无OPT promise算法误写为general。
