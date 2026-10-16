# 研究总目录：先选问题，再读具体资产

**新主攻入口：[一般不相关并行机的统一常数2近似壁垒](current/unrelated_machines/README.md)**。先读模型/精确账本与本题前沿，使用[新BOSS启动词](unrelated_machines/BOSS_START.md)；旧题地图按需读取，不能把旧拥塞目标带入新save。
本题新增[大边匹配残余及共享容量方法反例](current/unrelated_machines/heavy_matching_residual_and_escape.md)：安全过滤能识别原间隙族，但共享逃逸族仍保持gap趋2；统一常数突破仍OPEN。
当前主要成果是**加权原子拥塞博弈的线性全状态非存在下界及Cd/ln d保证的严格否定**。设施选址和顺序客户吸引是独立保留的研究线；它们有不同模型、量词和未解问题。完整的[中文资产名、文件位置、具体用途与状态依据](CATALOG.md)覆盖当前数学正文、问题、审查和已整合的拥塞核验资产。

面向审稿式连续阅读，可直接读[线性非存在界英文主稿PDF](current/weighted_congestion/linear_threshold_article.pdf)和[成稿核查](reviews/weighted_congestion/linear_threshold_article_review.md)；含完整证明，未认证优先权或期刊录用。

交给未读仓库的研究者：先读[当前线性全状态否定证明](current/weighted_congestion/linear_degree_allstate_lower_bound.md)及其独立审查；解题前冻结整理可复用[自足接题材料与精确方法障碍](weighted_congestion_frontier/PRO_BRIEF.md)和[完整任务正文](weighted_congestion_frontier/prompts/PRO_ATTACK.md)；旧整理稿的OPEN状态由新否定结论取代，其余数学、审查与证据仍可按冻结短指针追溯，不要求默认通读历史。

本题后续从[共同匹配选择与条件块容量](current/unrelated_machines/joint_matching_completion_and_block_cuts.md)进入：条件舍入、低余量精确选择障碍、专用共享容量切面与仍OPEN的统一构造分开登记。

## 我应该从哪里开始

| 你要研究什么 | 首读与主要资产 | 当前真正缺口 |
| --- | --- | --- |
| 一般不相关并行机的统一常数突破 | [本题地图](current/unrelated_machines/README.md) → [精确账本](unrelated_machines/CLAIMS.md) → [长链联合投影边界](current/unrelated_machines/long_path_coalition_gap.md) | UM-TARGET-v1仍OPEN；固定机器见证只共享单机边际仍gap2，完整多机交叠相容性与一般图构造复杂度是当前缺口。 |
| 一般不相关机统一常数近似 | [本题地图](current/unrelated_machines/README.md)→[精确星消去与容量接口](current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md) | 已有可恢复消元、安全下界及准确障碍；一般统一ε与位多项式调度输出仍未证明。 |
| 加权原子拥塞的普遍存在门槛 | [数学总述](current/weighted_congestion/README.md) → [精确模型](weighted_congestion_frontier/MODEL.md) → [线性次数全状态下界与原题否定](current/weighted_congestion/linear_degree_allstate_lower_bound.md) → 正文所链两份独立审查及代码/冻结证据 | 本次Cd/ln d判定已严格否定：每d≥2^20无(d/10)-PNE族；全类门槛增长阶Θ(d)，精确常数/有限d值、外部评审和新颖性另待核查。 |
| 非负共享负载响应的低阶表示 | [正占用核接口](current/positive_kernels/README.md) → 交互秩面 → 锐截断 → 非闭锥补全 | 固定正质量、完整Boolean表与正混合；一般动作签名及selector桥未建立，独立传感器实例已给 |
| 共同目录双设施的尖锐稳定性 | [黄金比成果与阅读顺序](current/shared/README.md) → 主定理、完整证明、尖锐下界、算法 → 小目录复杂度 | 已有内部成果的外部审查与优先权；实例最优倍率 EPTAS 仍是候选义务 |
| 异构目录双设施及单交叠边界 | [异构成果与阅读顺序](current/heterogeneous/README.md) → 一般目录候选、单交叠全长锐界、长回应环 | 一般异构上界的候选状态不能被单交叠定理覆盖 |
| 固定双设施布局的客户均衡 | [局部均衡与精确算法](current/local_and_exact/README.md) → 支持几何、局部强弦、精确求解及成本扩展 | 精确续局、有限证书与普遍全局保证分别核对 |
| 任意设施数的统一因子与构造 | [多设施成果与阅读顺序](current/multi_facility/README.md) → 因子二 → 完整盒有限构造 → 结构类算法与障碍 | 一般输入位多项式构造、最佳统一常数 |
| 顺序客户吸引的一般半覆盖 | [福利界、工具和反例地图](current/customer_attraction/README.md) → 模型、小人数/结构类结果 → 完整策略和全局桥 | 一般半覆盖仍开放；辅助桥的反例不是主问题反例 |

第一次进入仓库先读根 [README](../README.md)、[当前前沿](../RESEARCH_STATE.md)、[命题入口](../CLAIMS.md)、[失败入口](../FAILED_ROUTES.md)。随后只读所选专题；不用先通读全部旧稿、工具或协作提示词。

给未读仓库的独立研究者，使用[加权拥塞全类判定交接简报](weighted_congestion_frontier/PRO_BRIEF.md)及[独立攻题任务](weighted_congestion_frontier/prompts/PRO_ATTACK.md)。简报合并必要定义、可靠边界、准确方法限制和未闭合义务，详细数学正文按需读；冻结导出及源映射从专题入口进入。

一般群组奇环的actual缺口已由[单缺陷双取向消去](current/weighted_congestion/odd_ring/cohort_lower_bound_and_envelope.md#10-一般群组奇环实际阈值与正测试包络一致)闭合：不要求UF、允许部分aligned light和混合多项式，全部该拓扑均有T_d-PNE，实际最坏阈值恰T_d。先读精确拓扑和[独立攻击](reviews/weighted_congestion/odd_ring_parameters/general_cohort_actual_upper_review.md)，再调用两路Fraction证据；不能把这个拓扑当全类规范形。


本题新增[计数传播与成束相容性](current/unrelated_machines/bundle_coupling_subdivision_barrier.md)：可位多项式计算下界、旧gap族上的修复及其细分失败。只排除相应下界合同，目标仍OPEN；先读本题精确账本再使用。

## 文件按什么用途存放

| 位置 | 里面是什么 | 如何用 |
| --- | --- | --- |
| [current/](current/README.md) | 当前数学定义、自足证明、反例和可复用方法 | 按各专题 README 的证明链阅读；目录位置不代表统一审查等级 |
| [questions/](questions/README.md) | 仍未闭合的问题、候选稿及保留的已闭合问题合同 | 先看现在缺哪一步；旧探索计划不当成新任务 |
| [reviews/](reviews/README.md) | 已实际发生的数学审查与独立攻击 | 核对冻结版本、覆盖 claim 与仍成立的异议 |
| [weighted_congestion_frontier/](weighted_congestion_frontier/README.md) | 拥塞模型、账本、文献与协作程序 | 做数学先读模型/账本；需要协作操作时再读运行说明 |
| [../tests/audits/](../tests/audits) 与 [../evidence/](../evidence) | 独立核验代码、输入、证书和冻结结果 | 从对应正文或资产目录进入；计算不替代一般证明 |
| [../history/](../history/README.md) | 必要原稿、来源和已退出当前优先序的投稿判断 | 只在追溯时读；旧路线快照不覆盖现行研究状态 |

加权拥塞的跨尺度新接口见[有序权组冻结](current/weighted_congestion/weight_bands/ordered_tail_freezing.md)：阶段局部势可拼接密集权群，但最优潜在尾部参数固定次数仍可无界。[DAG端点低泄漏预算](current/weighted_congestion/polynomial_curvature/dag_low_leakage_budget.md)则精确限制指定阶跃模拟测试；二者均未闭合全类匹配上界。

[阶跃DAG极值幅度的真实全入状态](current/weighted_congestion/step_dag/polynomial_extremal_all_in.md)另在精确幅度锚定下给多项式实际状态的统一平方根界，无低泄漏假设；任意幅度和全类拓扑尚未归约。

## 名称、命题与审查怎样对应

每份文件的**中文数学名称与阅读目的**在 [CATALOG.md](CATALOG.md)，人工维护源为 `catalog.json`。同一文件可以包含多个命题，各自精确身份见 [current/claims.md](current/claims.md)；拥塞另有[主题账本](weighted_congestion_frontier/CLAIMS.md)。

| 登记 | 它回答的问题 |
| --- | --- |
| [assets.json](assets.json) | 某个命题适用于什么输入，正文、实现、测试、证据和来源在哪里？ |
| [review_status.json](review_status.json) | 来源证明、当前重构、内部审查、外部审查和实现分别到什么状态？ |
| [graph.json](graph.json) / [交互图](index.html) | 哪些定义与全部共同前提推出结论，哪些边仅是有限检验、反例或未解限制？ |
| [source_crosswalk.md](source_crosswalk.md) | 原始稿件怎样被当前数学解释、保留或取代？ |
| [拥塞资产链](weighted_congestion_frontier/FILES.md) / [来源迁移记录](weighted_congestion_frontier/INTEGRATION.json) | 一个拥塞成果包怎样连接正文、审查、核验和冻结证据，原分支原件怎样恢复？ |

关系图提供搜索种子。未出现在图上的方法仍可探索；状态、量词和真值以精确陈述及证明为准。

## 下一步与新资产入库

[当前全仓路线](ROADMAP.md)列现在值得推进的义务；[入库规范](GROWTH.md)和[生产、读取、保存规则](REPOSITORY_GUIDE.md)决定新文件的位置。给新资产写具体名称、用途、精确范围和证据层级；完成相应核验后及时保存到 `main`。

从仓库根运行 `python3 research/build_catalog.py --check`、`python3 research/build_map.py --check`、`python3 research/build_crosswalk.py --check` 和 `python3 research/check_assets.py`。这些检查负责目录和登记一致，不能充当数学证明。
