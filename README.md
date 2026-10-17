# 共同研究：一般不相关并行机的统一常数2壁垒

**当前唯一主攻是 `UM-TARGET-v1`，存档为 `unrelated-machines`。** 给定一般不相关机器处理时间矩阵，寻找一个确定性算法和统一常数 ε∈(0,1)，在输入总二进制位长的多项式时间内输出完整任务分配，并对所有合法输入保证 C_max≤(2−ε)OPT。机器数、任务数均可增长；有限处理时间为非负有理数，允许不可用边，每个任务至少有一台可用机器。零最优值和空任务也须覆盖。目标仍 **OPEN**。

新对话使用[完整BOSS提示词](research/unrelated_machines/BOSS_START.md)和[最新版work.py](research/weighted_congestion_frontier/tools/work.py)，附仓库外凭据。提示词直接写明主目标、启动、通信、地图和提交操作。[操作手册](research/unrelated_machines/RUNBOOK.md)给全部命令；新建且未绑定的clone默认进入新题，已绑定旧存档的clone保持原绑定，新题另用独立clone。

## 研究目标与当前前沿

从[本题数学地图](research/current/unrelated_machines/README.md)进入[精确账本](research/unrelated_machines/CLAIMS.md)、[当前前沿](research/unrelated_machines/RESEARCH_STATE.md)和[失败与回收](research/unrelated_machines/FAILED_ROUTES.md)。经典LST/ST舍入、配置LP间隙是已知工具重构；现有方法障碍和结构性正面接口均未给出一般输入的统一常数改善。证明、内审、外审、实现及新颖性分别记录。

| 研究义务 | 当前可用资产与准确入口 |
| --- | --- |
| 精确模型与经典地基 | [模型、槽舍入及两树配置间隙](research/current/unrelated_machines/model_and_classical_barriers.md)；[文献与取得状态](research/unrelated_machines/LITERATURE.md) |
| 跨机器共同容量与相关性 | [长链联合投影](research/current/unrelated_machines/long_path_coalition_gap.md)、[共享逃逸与完整单机配置延伸](research/current/unrelated_machines/row_count_escape_gap.md)、[稀疏条件配置边界](research/current/unrelated_machines/sparse_conditioned_configuration_gap.md)；各自反例只限制其精确定义的接口 |
| 可恢复结构与实际联合迁移 | [极小星及配置保持](research/current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md)、[森林边界菜单](research/current/unrelated_machines/forest_boundary_contraction.md)、[真实最优边际与固定槽](research/current/unrelated_machines/optimal_convex_fixed_slot_gap.md)；一般共同选择及进展仍未闭合 |
| 新表示与可构造性 | [条件矩运输和重新耦合](research/current/unrelated_machines/symmetric_moment_reset_and_single_machine_threshold.md)、[需求树精确桥梁](research/current/unrelated_machines/rooted_dag_degree_token_bridge.md)、[共同拥塞流接口](research/current/unrelated_machines/rooted_dag_congestion_flow.md)；按正文核对给定证书、未知支撑及总位复杂度；共同流§7–10给非单位分叉参数2^h精确树，尚非一般多项式 |

路线是搜索种子，可以改变方法。仅有配置间隙、固定槽损失、某个见证选择困难性或特殊情形算法，均不关闭主目标。所有精确身份与新增成果沿本题地图和账本维护，根入口保持稳定，不逐轮追加摘要。

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
