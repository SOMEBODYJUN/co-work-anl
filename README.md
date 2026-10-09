# 两阶段设施选址博弈：研究与人类学习入口

本轮另启动独立的[顺序客户吸引博弈分支](research/current/customer_attraction/README.md)：
研究 Deng 等共同目录、单位均分模型的[任意纯 SPE 半覆盖目标](research/questions/customer_attraction_half_coverage.md)。
已建立保留全部历史依赖平局的有限精确工具，**任意人数上界仍未证明**。
[三人锐界](research/current/customer_attraction/three_player_sharp.md)已完整内部独立审查：
每个完整纯 SPE 满足 `OPT_3≤(5/3)W`，且下界达到。
真实离轨回复和跨节点比较闭合上界，不依赖已失败的税归纳。
[先前142/81推导](research/current/customer_attraction/three_player_bound.md)作为两人税机制的独立回收保留。
[固定背景两人税界](research/current/customer_attraction/two_remaining_tax.md)仍成立，
但[首步机会成本桥](research/current/customer_attraction/tax_bridge_counterexample.md)在空背景三人即失败，
[一般背景总税界](research/current/customer_attraction/general_tax_counterexample.md)也有完整根 SPE 内的反例。
[完整策略重数锥](research/current/customer_attraction/strategy_cone.md)给固定人数与主题标签数的有理精确优化接口，
没有将有限策略样本升级为一般上界。
该模型的客户不主动优化，与下述既有设施研究没有直接定理迁移。

本项目研究正权原子客户的两阶段设施选址：设施先选位置，客户随后选择设施并形成精确独立 Nash 均衡。我们寻找一个纯设施布局和覆盖全部布局的客户均衡续局，使设施单边搬迁的收益受统一倍率控制。

**人类团队从 [learning/README.md](learning/README.md) 开始。** 顺读入口是 [从一个搬迁问题开始](learning/00_guide.md)，模型与技术课之后由 [两条主证明的接口](learning/01b_proof_map.md)进入长证明；[精确证书课](learning/10_certificates.md)把概率策略与定义级核验连起来。已有预备课、手算、[分析式证明技术](learning/01a_proof_techniques.md)、核心证明讲义、有限必要障碍与 [两周研讨安排](learning/07_seminar.md)。先掌握主线，不按提交时间通读所有研究分支。

## 当前目标与主要成果

当前主要算法目标是：对任意设施数、共同目录、显式可达集合和正二进制有理原子权，在联合输入位长多项式时间内构造完整因子 2 近似 SPE。**一般因子 2 存在性已有完整内部证明，高效构造仍开放。** 最佳统一常数是否小于 2 是另一项研究问题。

| 成果 | 精确范围与结论 | 现行入口 |
| --- | --- | --- |
| 四共同地点无 FPTAS | 两设施、正整数原子权；在全部纯布局与完整精确独立混合续局之间优化实例稳定倍率，P≠NP 下不存在加性/乘性 FPTAS；不排除 PTAS 或一般任意盒 NE 搜索 | [全局间隙证明](research/current/shared/four_site_no_fptas.md)、[审查、实际核验及文献差异](research/FOUR_SITE_FPTAS_AUDIT_2026-10-09.md) |
| 共同目录双设施 φ | 任意覆盖和正原子权；尖锐普遍因子 φ，显式有理输入有位多项式构造 | [分支](research/current/shared/README.md)、[完整证明](research/current/shared/proof.md)、[锐性下界](research/current/shared/sharp_phi_lower.md) |
| 一般异构双设施 2 | 不同目录；四种子/全环上界及匹配下界；当前账本仍为内部候选 | [分支](research/current/heterogeneous/README.md)、[全环](research/current/heterogeneous/full_catalog_cycle.md) |
| 任意长单交叠异构目录 ρ | 每个合法跨目录对至多一个共有客户；固定完整纯规则给出尖锐 ρ；双侧目录长度不受限 | [全长直接证明](research/current/heterogeneous/sparse_unbounded_rho.md) |
| 共同目录实例复杂度 | 每个事先固定的有理 1≤a<φ，判定实例最优倍率≤a 弱 NP 完全；三地点处理 a=1，五地点覆盖全部 1<a<φ | [结构与算法边界](research/current/shared/instance_complexity_barriers.md)、[五地点全归约](research/current/shared/five_site_exact_hardness.md) |
| 任意设施数共同目录 2 | 存在纯选址、站内均匀在轨客户 NE 和完整精确纯离轨续局；不声称 2 尖锐或一般位多项式 | [主定理](research/current/multi_facility/uniform_two.md)、[逆审](research/current/multi_facility/reverse_review.md) |
| 任意规模贪心完整盒 NE | 固定规范贪心布局；阈值截断负载与离乡人数的交错字典序势证明任意严格改善加归位修复有限终止，构造完整盒内精确客户 NE；无一般多项式总步数界 | [全局进展证明](research/current/multi_facility/greedy_box_global_progress.md)、[运行](USAGE.md) |
| 等权可移动客户的无约束流选择器 | 任意覆盖图与二进制重数；无约束目标的每个全局最小者自动在完整盒内并满足 `(H)`。等权原模型子类此前已可多项式求解；本轮删除冗余下界、强化最优解性质并补规范实现 | [完整新证明与旧结果比较](research/current/multi_facility/equal_light_flow.md)、[实现](multi_facility_spe/equal_light_flow.py) |

以上成果审查状态不同，均无外部同行评审记录。精确作用域、来源证明、现行重构、内部审查与实现分别登记在 [命题账本](research/current/claims.md) 和 [五轴状态表](research/review_status.json)。内部证明、有限实例证书及学术发表是不同层次。

## 算法前沿在哪里

双设施另有一个可集中完成的[实例最优倍率 EPTAS 候选](research/questions/shared_alpha_eptas.md)：
[固定重支持的近带精确补全](research/current/shared/near_band_completion.md)已内部证明，
外带少量重客户枚举及全局 C² 误差有明确路线；规范一般算法、完整位复杂度和实现仍待交付。
[团队价值辩驳与实际初探](research/NEXT_DIRECTION_DEBATE_2026-10-09.md)记录选择理由。
这一方向与一般盒内任意 NE 的多项式目标独立，不把候选升级为已完成 EPTAS。

2026-10-08 的[共单例搜索接口](research/current/multi_facility/complement_search_reduction.md)
将另一类负载均衡搜索精确实现为真实贪心实例：全状态保盒且严格保 `(H)`，没有归位修复，仍保留全部客户选择关系。两速度 `1,2` 的归约为通常位多项式；一般带区间表述不展开重数。它是结构定位成果，编译器不求均衡，不证明一般高效构造或困难性。证明、实现、独立精确核验及近期解释/自由选路目标已汇入[复合审查记录](research/COMPLEMENT_REDUCTION_AUDIT_2026-10-08.md)。

[完整盒内存在性与改善—归位全局终止](research/current/multi_facility/greedy_box_global_progress.md) 已闭合：规范贪心布局总有精确站纯、站内独立均匀客户 NE，有限精确构造可接完整因子 2 续局。一般输入剩余的是**总运行时间的位多项式界**，精确下一目标见[交接页](research/questions/greedy_box_polytime.md)。[计算前沿](research/current/multi_facility/polytime_frontier.md) 的离轨多项式定理仍成立；当前可执行完整构造使用有限的帽容量纯改善过程，未实现该文献调度算法。

普遍盒可行性还与既有两个精确 DP 相接：固定逐名关联图树宽及双侧度，或固定地点 primal 树宽及每站不同轻权种类数，均有完整位多项式因子 2 数学构造，无需旧浅层有向图条件。这一新版推论不改变旧命题的假设；一般参数下仍开放。

本轮[审查汇总](research/EQUAL_LIGHT_FLOW_AUDIT_2026-10-07.md)区分旧结果、新增性质和实际复现范围。等权可移动轻客户现在另有[规范无约束流实现](research/current/multi_facility/equal_light_flow.md)。它允许冻结客户异权，恰有逐客户单位增广；`--method equal-light-flow` 已接完整证书。该方法的在轨阶段为位多项式，当前软件的离轨及默认阶段仍是有限纯改善。它不扩大旧 `SC-K-UNIFORM-LIGHT-FLOW-2` 的原模型输入类，也未解决一般异权总时间。

[盒内完成](research/current/multi_facility/polytime_frontier.md)、[自适应原池重置](research/current/multi_facility/adaptive_reset_floor.md) 和 [冻结安全超载](research/current/multi_facility/frozen_overload_completion.md) 是三类可复用接口。最后一类只给偏离者设收益帽，允许其他设施安全超载。它们不提供任意输入的成功证书生成器。特殊可算类按讲义 [工具](learning/05_tools.md) 分类阅读；必要障碍集中在 [前沿](learning/06_frontier.md)，不必逐个记住优先规则反例。

实时进展放在 [RESEARCH_STATE.md](RESEARCH_STATE.md)，准确失败量词见 [FAILED_ROUTES.md](FAILED_ROUTES.md)。[路线图](research/ROADMAP.md) 与 [问题库](research/questions) 用于选题，不替代现行证明。[2026-10-05 发表对标](research/PUBLICATION_BENCHMARK_2026-10-05.md)比较实际期刊论文、各成果包的贡献力度及投稿判断，并记录对 2025 博士论文相关章节的优先权核查；不提升数学审查状态。2026-10-01 的 [出版评估](research/PUBLICATION_REVIEW.md) 保留为历史快照。

最新的 [全仓投稿层级评估](research/PUBLICATION_ASSESSMENT_2026-10-06.md) 按问题意义、可复用机制与用户期刊目录定位成果，重估两设施共同目录五地点困难性的贡献，并澄清广义 φ 猜想的目录边界；不提升数学命题或外审状态。

## 仓库结构

| 区域 | 用途 |
| --- | --- |
| [learning](learning) | 人类团队的分层课程、练习、核心证明路线与两周研讨会 |
| [research/current](research/current) | 现行模型、命题、完整数学证明与算法解释；定义与结论的权威入口 |
| [facility_spe](facility_spe) | 双设施规范算法、局部/实例精确求解和验证器 |
| [multi_facility_spe](multi_facility_spe) | 任意设施数的有限精确构造器；支持全局枚举与贪心盒内构造，尚无一般多项式总时间保证 |
| [customer_attraction](customer_attraction) | 独立的顺序主题选择、单位客户均分模型；全部纯 SPE 终局及完整历史证书，服务半覆盖猜想 |
| [tests](tests) | 回归、独立定义级比较和有限精确攻击，分别标明验证范围 |
| [examples](examples) / [evidence](evidence) | 输入、证书、冻结实验；不以有限成功替代全称证明 |
| [history](history) | 来源手稿与旧推导，保留追溯；不是新人入口 |

[ASSETS.md](ASSETS.md) 将命题连到证明、代码和证据；[数学超图](research/index.html) 的推导边列出全部共同前提。GitHub 显示 HTML 源码，下载后可交互查看。[来源对照](research/source_crosswalk.md) 和 [迁移记录](research/path_migration.json) 保留原资产的当前解释。

## 怎样参与与复现

新人先按课程完成模型与主定理的过关任务。研究贡献遵守 [AGENTS.md](AGENTS.md) 和 [新增研究规则](research/GROWTH.md)：候选、现行证明、实现、有限证据分开登记；改变模型、量词或适用域要明确版本；教学整理不提升数学状态。

程序入口和限制见 [USAGE.md](USAGE.md)。从仓库根运行维护检查：

```sh
python3 research/build_map.py --check
python3 research/build_crosswalk.py --check
python3 research/check_assets.py
```

本次人类交接的范围、发现及验证见 [learning/AUDIT.md](learning/AUDIT.md)。
