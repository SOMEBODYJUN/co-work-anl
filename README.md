# 共同研究：数学地图与唯一读取入口

**新主攻：[一般不相关并行机的统一常数2近似壁垒](research/current/unrelated_machines/README.md)。** 精确目标 `UM-TARGET-v1` 仍OPEN；[完整BOSS启动词](research/unrelated_machines/BOSS_START.md)固定存档 `unrelated-machines`，复用现有公屏、私聊和个人桌面。经典舍入与配置gap已重构并配可复现精确证据；[长链扩展](research/current/unrelated_machines/long_path_coalition_gap.md)进一步给任意围长简单图及精确定义的固定机器联合投影gap2，完整多机交叠相容性不被排除；[匹配残余与共享逃逸反例](research/current/unrelated_machines/heavy_matching_residual_and_escape.md)新增安全过滤及准确方法障碍，仍无统一常数改善算法；[残余容量计数传播](research/current/unrelated_machines/bundle_coupling_subdivision_barrier.md)给健全位多项式过滤接口及细分失效；全文下载、证明重构、独立审查和原创进展分别记录。旧题成果与身份保留。
本仓库维护不相关并行机、加权原子拥塞、两阶段设施选址和顺序客户吸引等独立数学模型。数学状态以main正文与精确账本为准；旧会话和公屏用于交流，不能覆盖规范记录。

**[研究总目录](research/README.md) · [全部中文资产名与用途](research/CATALOG.md) · [当前研究路线](research/ROADMAP.md)。**

当前协作沿用原公屏、独立 clone 和统一 main，已加入[个人研究工作区](research/workspaces/README.md)、双方私聊、公屏提及、个人收件与只读访问；实际使用见[操作手册](research/weighted_congestion_frontier/RUNBOOK.md)。测试使用隔离的真实本地 Git 远端，不在实际公屏投放测试身份或开研究分支；数百 Work 同时生成和线上吞吐未认证。[大规模协作构想](design/large_scale_research_collaboration.md)、[原全量总稿](design/AI_Co_Mathematician_master.md)和[前阶段适配](design/work_github_adaptation.md)按收益取用，不是必须整体建设的前提；工具交付不改变数学状态。

## Research Goal / Research Frontier

此前拥塞题已有**严格否定证明**：[线性次数的全状态无均衡族](research/current/weighted_congestion/linear_degree_allstate_lower_bound.md)对每个整数d≥2^20，给出正有理权、正有理纯d次费用、每人两个非空不交动作的有限游戏，全部纯状态都有严格(d/10)改善。任给C≥1,d0≥2，取足够大d≥d0且ln d>10C，即无(Cd/ln d)-PNE。因此不存在原题所问的绝对C,d0。

证明链为健康循环窗口参数 → 全部类前沿出口 → 同类三元时钟修复非法状态 → 原次数预算 → 原题否定量词；每一态而非单个改善环均被覆盖。独立先重构后冻结攻击已覆盖该链；[审查补节](research/reviews/weighted_congestion/ordinal_potentials/linear_degree_allstate_review.md#补充复核整数次数预算与完整多类拼装)另给整数分层次数证明及完整多类拼装核验，精确审计仅核查其实际有限范围。外部同行评审、新颖性与最优常数未认证。精确ID是`WC-LINEAR-DEGREE-ALLSTATE-NONEXISTENCE-v1`及`WC-MATCHING-LOG-UPPER-NEGATIVE-v1`。

面向评审读者的[自足英文主稿PDF](research/current/weighted_congestion/linear_threshold_article.pdf)与[LaTeX源](research/current/weighted_congestion/linear_threshold_article.tex)已完成内部全文审读和十页版面检查；[稿件核查](research/reviews/weighted_congestion/linear_threshold_article_review.md)区分完整主证明、文献推论与尚未认证的外审/新颖性。数学规范正文和Claim身份不变。

WC-TARGET v1的长期身份仍是刻画全类门槛a_*(d)，未改写原陈述。新a_*(d)≥d/10与单列Paper Fact的一般d上界合用给增长阶Θ(d)；精确常数、有限d最优值及复杂度仍未刻画。旧奇环T_d∼d/ln d下界和该拓扑实际阈值恰T_d仍成立，现为独立子类资产。

独立接续先读新全状态证明。既有[Pro自足简报](research/weighted_congestion_frontier/PRO_BRIEF.md)、[来源manifest](research/weighted_congestion_frontier/PRO_BRIEF_SOURCES.json)及[冻结导出器](research/weighted_congestion_frontier/tools/export_pro_packet.py)保留2c49228及其前序快照的模型与工具整理；其旧OPEN状态已由当前新否定证明取代，当前交接应另附新正文与审查。冻结包按指定提交导出，不原位改写。

不相关并行机的新[共同匹配补全接口](research/current/unrelated_machines/joint_matching_completion_and_block_cuts.md)区分条件构造、精确选择NP完全与专用条件块切面；下一步为一般可求解耦合与统一容量余量，主目标仍OPEN。

## Mathematical Objects / Definition Map

| 模型 | 对象与定义链 | 权威定义与研究入口 |
| --- | --- | --- |
| 不相关并行机 | 非负有理处理时间矩阵＋不可用边 → 不可拆分全任务分配 → 最大机器负载 → 统一常数(2−ε)位多项式构造 | [新主攻数学地图](research/current/unrelated_machines/README.md)、[精确身份与边界](research/unrelated_machines/CLAIMS.md) |
| 加权原子拥塞 | 正权玩家＋有限资源子集策略＋非负多项式费用 → 资源负载 → 玩家成本 → α-PNE → 全类阈值 a_*(d) | [MODEL](research/weighted_congestion_frontier/MODEL.md)、[数学资产](research/current/weighted_congestion/README.md) |
| 两阶段设施选址 | 设施布局＋可达关系＋正权原子客户 → 精确独立客户 NE → 完整续局 → 近似 SPE | [模型](research/current/model.md)、[成果地图](research/current/README.md) |
| 顺序客户吸引 | 共同主题目录＋单位客户 → 历史依赖纯策略 → 完整纯 SPE → 覆盖福利 | [独立入口](research/current/customer_attraction/README.md) |

模型间的工具迁移需要明确桥梁；目录相邻不表示定理互相适用。

## Claim Map / Dependency Graph

先读[加权拥塞数学入口](research/current/weighted_congestion/README.md)和[自足否定证明](research/current/weighted_congestion/linear_degree_allstate_lower_bound.md)，再由正文第10节核对独立审查、实际输入、程序与冻结结果。[主题精确账本](research/weighted_congestion_frontier/CLAIMS.md)、[全仓逐命题登记](research/current/claims.md)、[五轴状态](research/review_status.json)和[数学超图](research/index.html)共同给出范围、依赖及证据层级。`derives`列全部共同前提；有限核验用`checks`，方法限制不替代全类结论。

## Known Results

| 成果包 | 精确成果和限制 | 读取入口 |
| --- | --- | --- |
| 不相关机可恢复消元 | 极小超载星保T且输出提升≤max(B,T)；共享容量族/多任务接口仍有准确障碍，主目标OPEN | [自足接口与证据](research/current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md) |
| 加权拥塞全状态线性下界 | 每整数d≥2^20无(d/10)-PNE族，严格否定统一Cd/ln d保证；内部独立已审，未外审 | [完整证明与证据链](research/current/weighted_congestion/linear_degree_allstate_lower_bound.md) |
| 加权拥塞结构工具 | 奇环精确T_d阈值、有限权类/交互高度势、资源支持/密度势、完整择证对偶、规范反例、条件时钟编译及准确方法障碍，各有独立输入合同 | [专题数学地图](research/current/weighted_congestion/README.md) |
| 双设施 | 共同目录尖锐φ、稀疏异构尖锐ρ及复杂度；一般异构2保留候选 | [共同目录](research/current/shared/README.md)、[异构](research/current/heterogeneous/README.md) |
| 任意设施数 | 因子2存在性及有限构造；一般输入位多项式构造仍开放 | [成果与前沿](research/current/multi_facility/README.md) |
| 顺序客户吸引 | 小人数/结构目录福利界与完整策略反例；一般半覆盖仍开放 | [分支数学地图](research/current/customer_attraction/README.md) |
| 正占用核 | 独立的交互秩、锐截断与闭包工具；一般WC签名/均衡桥未建立 | [独立专题](research/current/positive_kernels/README.md) |

## Refuted / Failed / Open Problems / Next Actions

[失败路线](FAILED_ROUTES.md)区分原题的严格反例、具体架构的障碍和可回收接口。当前负例避开全局极差时钟的旧统一预算，使用同类时钟并另证全部错位前沿出口；没有否定旧障碍的准确范围。后续研究可核对/简化线性下界、优化常数、核查文献优先权和外部评审。其他模型的开放问题继续独立维护。

## File Map / 工作程序

| 完整路径 | 内容、作用与读取时机 |
| --- | --- |
| [research/unrelated_machines/README.md](research/unrelated_machines/README.md)、[BOSS_START.md](research/unrelated_machines/BOSS_START.md) | 新存档与完整启动词，绑定unrelated-machines；先恢复精确主目标、文献与真实障碍，再自主选路线；不会把旧TEAM中的拥塞命题带入新题 |
| research/current/unrelated_machines/model_and_classical_barriers.md、research/unrelated_machines/literature_manifest.json | 自足模型、槽匹配和重索引配置gap；manifest连接真实原文版本/哈希/定理位置和缺失项；引用已知工具或攻击新算法前读取 |
| README.md、RESEARCH_STATE.md、CLAIMS.md、FAILED_ROUTES.md | 全仓稳定地图、当前前沿、精确命题入口、失败范围；新对话首先读取 |
| [research/README.md](research/README.md) | 按数学问题分流的研究总目录；先选模型，再沿专题阅读顺序进入具体资产 |
| [research/CATALOG.md](research/CATALOG.md)、research/catalog.json | 全部现行数学正文、问题、审查及已整合拥塞核验资产的具体中文名称、完整路径与阅读用途；JSON 是人工命名源，Markdown 由程序生成 |
| research/GROWTH.md | 原有入库规范：证明、问题、代码、测试、输入、证据和历史材料的归属；写文件前执行 |
| research/REPOSITORY_GUIDE.md | 全仓生产状态、读取顺序、施工与上传、分支收口及交流规则 |
| research/weighted_congestion_frontier/README.md | 当前协作入口；连接数学、启动程序和按需读取路径 |
| research/weighted_congestion_frontier/FILES.md | 本轮逐文件用途、状态和去处；查具体成果、证据或待审项 |
| research/weighted_congestion_frontier/INTEGRATION.json | 各原分支 tip、文件来源/hash、当前路径与退役理由；只在来源审计与恢复时读 |
| research/current/claims.md、research/review_status.json、research/assets.json | 全仓逐命题范围与五轴状态、资产合同；修改或引用结论时查询 |
| research/current/ | 可连续阅读的现行数学稿；审查状态独立记录 |
| research/questions/、research/reviews/ | 开放义务与待审候选；已发生的审查及其覆盖范围 |
| facility_spe/、multi_facility_spe/、customer_attraction/ | 各现有模型的唯一规范程序，运行见 USAGE.md |
| tests/、examples/、evidence/ | 回归及独立审计、输入、冻结证据；运行不得覆盖冻结记录 |
| learning/README.md | 人类研讨学习路线与当前成稿；不替代数学权威稿 |
| history/README.md | 仍有来源价值的原稿及 Git 恢复指针；追溯时按需读 |

日常研究共同保存到 **main**。`wcg/board` 仅承担简短异步研讨；旧工作分支在内容入库并确认原提交可达后删除。程序不再创建随机会话分支。每个对话使用独立本地 clone，一个稳定发布标识，子 agent 无需登记；人数和工作时长不由提示词设限。

需要把当前研究交给 Pro 时，可复用上述自足简报和冻结导出器，但须核对其来源提交及当前否定证明，按[角色与交接顺序](research/weighted_congestion_frontier/README.md#角色与-pro-交接顺序)先由清晰者筛出必要事实与精确障碍、提取者核实按需工具，再提交实际数学材料。论文者独立负责成稿；提示词就绪和材料整理完成分别核验。

不相关并行机新增[条件LP与稀释终端边界](research/current/unrelated_machines/diluted_sink_probe_gap.md)：全部边各有LST强制点仍不足以耦合配置槽；加强基数探针可修复该族，主目标保持OPEN。

半单位新身份已关闭固定大小分界的共同见证窗口：每个固定δ∈[0,1/2)的(Aδ)存在性NP完全；P≠NP下无总位多项式OPT≤T承诺构造。它仍不是统一低于2算法的困难性，下一步转向实际联合舍入损失。见[共同选择正文§3a](research/current/unrelated_machines/joint_matching_completion_and_block_cuts.md)。

[全局单行基数匹配与紧凑共享逃逸](research/current/unrelated_machines/row_count_escape_gap.md)把资源池路线推进到准确边界：一次全局任务权匹配涵盖同一下界的全部子池，但每机/每配置独立守计数仍不等于共同真实负载。新族为多项式规模，GPC₂与所有单行见证仍gap2；现有条件块切面可修复，主目标OPEN。

[直接联合槽的正面衔接](research/current/unrelated_machines/joint_slot_prefix_rounding.md)给UM-ROW-SPREAD-TWO-ROUND-v1：删去零任务后每行正时间跨度≤2（逐机尺度不同）时，显式前缀计数LP加一次全任务槽匹配给3/2位多项式构造。它是VW/ST已知机制的直接推论，绕过过强(Aδ)见证；未消除一般行内跨尺度混合，主目标仍OPEN。

新增[三选稀疏深树的全边条件配置反例](research/current/unrelated_machines/sparse_conditioned_configuration_gap.md)：每条边分别取得完整配置证书仍不能耦合跨查询的共享容量，sup相对阈值间隙仍2。完整四机器交集一致性及可恢复消元不在该障碍范围；主目标仍OPEN。

紧凑共享逃逸正文§6另给UM-COMPACT-MULTIROW-EXTENSION-v1：任意U含至多N−2k个中心时，每个单机配置均可延伸并让U全部机器同时守真实容量；N−2k+1中心加z空pin有明确失败。故“更多独立行见证”仍缺共同相关性，尖锐预算和实际构造不改变主目标OPEN状态。

[完整单机配置探针边界](research/current/unrelated_machines/row_count_escape_gap.md#7-完整单机配置也分别能延伸到完整配置lp)：同一多项式规模族的每个合法单机配置都能分别延伸到完整配置LP，间隙仍趋2；共同条件一阶矩可修复本族，主目标仍OPEN。

[真实最优凸包内的固定槽损失](research/current/unrelated_machines/optimal_convex_fixed_slot_gap.md)进一步把两类障碍分开：即使x来自真实OPT调度凸包，固定有序槽图的所有匹配仍可趋2OPT；本族跨槽迁移可恢复最优。它限制输出空间，不否定一般算法；主目标仍OPEN。

不相关机新增[循环批量局部优化与分流障碍](research/current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md)：已有总位多项式的鲁棒循环修复，但正支撑唯一最小成本槽输出仍可要求真正多目的地分流；不排配置初始化，主目标OPEN。

[需求树与真实调度的直接桥梁](research/current/unrelated_machines/rooted_dag_degree_token_bridge.md)给精确OPT=2−截断需求比例、实际双向构造与二进制大需求压缩。它把一般联合迁移的必要能力写成可复用输入；属于已知MMDA机制重构，主目标仍OPEN。
