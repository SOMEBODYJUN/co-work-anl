# 研究总目录：先选问题，再读具体资产

当前主攻是**加权原子拥塞博弈的普遍近似纯均衡门槛**。设施选址和顺序客户吸引是独立保留的研究线；它们有不同模型、量词和未解问题。完整的[中文资产名、文件位置、具体用途与状态依据](CATALOG.md)覆盖当前数学正文、问题、审查和已整合的拥塞核验资产。

## 我应该从哪里开始

| 你要研究什么 | 首读与主要资产 | 当前真正缺口 |
| --- | --- | --- |
| 加权原子拥塞的普遍存在门槛 | [数学总述](current/weighted_congestion/README.md) → [精确模型](weighted_congestion_frontier/MODEL.md) → 奇环全状态下界、正局部证书包络、结构势和[依游戏可分序势障碍](current/weighted_congestion/separable_ordinal_obstruction.md) | 下界与全类上界仍有对数缺口；需要全类存在机制或更强非存在机制；[整数规范反例与闭端点](current/weighted_congestion/template_certificates/integer_counterexample_normal_form.md)只提供精确搜索接口 |
| 共同目录双设施的尖锐稳定性 | [黄金比成果与阅读顺序](current/shared/README.md) → 主定理、完整证明、尖锐下界、算法 → 小目录复杂度 | 已有内部成果的外部审查与优先权；实例最优倍率 EPTAS 仍是候选义务 |
| 异构目录双设施及单交叠边界 | [异构成果与阅读顺序](current/heterogeneous/README.md) → 一般目录候选、单交叠全长锐界、长回应环 | 一般异构上界的候选状态不能被单交叠定理覆盖 |
| 固定双设施布局的客户均衡 | [局部均衡与精确算法](current/local_and_exact/README.md) → 支持几何、局部强弦、精确求解及成本扩展 | 精确续局、有限证书与普遍全局保证分别核对 |
| 任意设施数的统一因子与构造 | [多设施成果与阅读顺序](current/multi_facility/README.md) → 因子二 → 完整盒有限构造 → 结构类算法与障碍 | 一般输入位多项式构造、最佳统一常数 |
| 顺序客户吸引的一般半覆盖 | [福利界、工具和反例地图](current/customer_attraction/README.md) → 模型、小人数/结构类结果 → 完整策略和全局桥 | 一般半覆盖仍开放；辅助桥的反例不是主问题反例 |

第一次进入仓库先读根 [README](../README.md)、[当前前沿](../RESEARCH_STATE.md)、[命题入口](../CLAIMS.md)、[失败入口](../FAILED_ROUTES.md)。随后只读所选专题；不用先通读全部旧稿、工具或协作提示词。

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

加权拥塞新增[两权类别双排序混合势](current/weighted_congestion/weight_bands/two_weight_order_blend.md)：不限制两类人数或权比的平方根次数存在界，附独立攻击与两份精确审计；全类多权问题仍开放。

全类非势接口的两个准确边界：[择证平稳与循环支撑](current/weighted_congestion/template_certificates/stationary_selector_obstruction.md)区分概率dual与全改善终止；[有向分叉强迫割均衡](current/weighted_congestion/directed_fanout_forcing_cut.md)排除唯一源、私有双人侧资源在UF下越过T_d的放大。二者均未完成全类判定。
