# 研究总目录：新题入口与独立模型

**当前主攻 `UM-TARGET-v1`，研究存档 `unrelated-machines`：一般不相关并行机R∥C_max的统一常数(2−ε)确定性位多项式构造。目标仍OPEN。** 新对话使用[完整BOSS提示词](unrelated_machines/BOSS_START.md)、[最新版work.py](weighted_congestion_frontier/tools/work.py)和[本题手册](unrelated_machines/RUNBOOK.md)。程序所在旧目录承载共享工具，当前题目按save和精确目标确定。

## 新题的阅读与研究链

[本题数学地图](current/unrelated_machines/README.md) → [精确账本](unrelated_machines/CLAIMS.md) → 当前义务的正文 → 已发生的独立审查 → 实际代码、输入、证书与冻结证据。[模型与经典地基](current/unrelated_machines/model_and_classical_barriers.md)固定全量词、零值边界、槽舍入和配置gap；[专题前沿](unrelated_machines/RESEARCH_STATE.md)与[失败及回收](unrelated_machines/FAILED_ROUTES.md)定位真正未解接口。[原始文献](unrelated_machines/LITERATURE.md)另列取得、阅读与重构状态。

方法障碍、条件正面结果与特殊情形不升级成主目标突破。共同多机容量、实际联合迁移、可恢复菜单、条件矩重耦合与需求树支撑选择等路线均可探索；[路线图](ROADMAP.md)是搜索种子。


本题最新结构接口还包括[单汇点宏退出与完整profile池共同选择](current/unrelated_machines/shared_sink_joint_macro_assignment.md)，及[循环修复正文](current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md)§10的严格lex长链边界。按[共同容量路线整合审查](reviews/unrelated_machines/joint_capacity_route_feasibility_review.md)区分局部构造、核心共同选择与总进展；特定族[条件矩新构造](current/unrelated_machines/symmetric_moment_reset_and_single_machine_threshold.md)§9不能直接提升为一般算法。

[固定数量共享汇点的占位基交换与三半调度](current/unrelated_machines/fixed_sink_occupation_rounding.md)给三个分离身份：UM-OCCUPATION-MODE-SIDE-CONSTRAINT-v1允许任意K但仅界定2K个分数组；UM-FIXED-SINK-PRIVATE-GROUP-THREE-HALVES-v1在固定K的给定阈值下输出实际≤3T/2；UM-FIXED-SINK-MACRO-PROMISE-APPROX-v1用含OPT的大宏promise及非单调one-sided整数二分给真正≤3OPT/2。唯一home/给定分组和固定K仍承重，通用LP软件未实现，新颖性未认证。一般主目标下一缺口是不受限的接收容量与跨home/跨尺寸任务身份，UM-TARGET-v1仍OPEN。

## 各模型分别读取

| 模型 | 权威入口 | 状态与范围 |
| --- | --- | --- |
| **当前：不相关并行机** | [当前数学](current/unrelated_machines/README.md)、[协作入口](unrelated_machines/README.md) | 统一ε主目标OPEN；精确阶段成果逐项查账本 |
| 加权原子拥塞 | [数学地图](current/weighted_congestion/README.md)、[旧题入口](weighted_congestion_frontier/README.md) | 线性全状态族否定Cd/ln d保证；长期精确门槛及其他义务独立保留 |
| 正占用核 | [表示与闭包](current/positive_kernels/README.md) | 工具输入与均衡桥分别处理 |
| 两阶段设施 | [模型与专题分流](current/README.md) | 共同/异构目录、设施数、精确续局量词各有身份 |
| 顺序客户吸引 | [当前地图](current/customer_attraction/README.md) | 一般半覆盖仍有缺口；结构结论不能直接替代 |

## 查文件、状态与来源

[CATALOG](CATALOG.md)给具体中文名和用途；[current/claims](current/claims.md)与各专题CLAIMS固定身份；[review_status](review_status.json)分列来源证明、当前重构、内审、外审、实现；[assets](assets.json)绑定文件合同；[图](index.html)区分推导、有限核验、攻击和限制；[来源解释](source_crosswalk.md)保留原件与现行重写关系。旧模型的全文、证据和历史通过这些入口保留，不作为新题必读清单。

入库按[GROWTH](GROWTH.md)及[生产、读取和保存规则](REPOSITORY_GUIDE.md)。根地图保持稳定，阶段状态写专题前沿。每次相关更新运行build_catalog、build_map、build_crosswalk和check_assets；后者包含[当前课题路由检查](check_active_research.py)，防止默认入口退回旧题。

[共同流正文](current/unrelated_machines/rooted_dag_congestion_flow.md)§7–10新增守恒扩区及非单位分叉参数算法：单位走廊与汇流全部交给一次共同流，只有h个非单位点的支撑选择仍付2^h。精确实际根树与主目标的一般多项式量词分开；按新ID/冻结审查读取，不改旧合同。

[共同资格私有组的无界sink联合流](current/unrelated_machines/hall_group_joint_flow.md)：实际输出比例`q(2+δ)/(q+1)`，并有未知OPT的结构承诺版本；同组资格/等端体积及组总量范围仍承重，q增长时无统一ε。一般主目标保持OPEN，下一义务是可恢复的一般分组或异资格/异端容量转换。

## 全局四阶矩与实际提取接口

[全局分配矩正文](current/unrelated_machines/global_assignment_moment_rounding.md)连到显式证书合同、近平坦有理提取、真实最优分布HS反例、冻结审查和双路精确代码。经典平坦来源与新定量推导分开；一般生成/大缺陷舍入未解决，UM-TARGET-v1仍OPEN。
