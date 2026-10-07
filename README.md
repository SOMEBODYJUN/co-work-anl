# 两阶段设施选址博弈：研究与人类学习入口

本项目研究正权原子客户的两阶段设施选址：设施先选位置，客户随后选择设施并形成精确独立 Nash 均衡。我们寻找一个纯设施布局和覆盖全部布局的客户均衡续局，使设施单边搬迁的收益受统一倍率控制。

**人类团队从 [learning/README.md](learning/README.md) 开始。** 顺读入口是 [从一个搬迁问题开始](learning/00_guide.md)，模型与技术课之后由 [两条主证明的接口](learning/01b_proof_map.md)进入长证明；[精确证书课](learning/10_certificates.md)把概率策略与定义级核验连起来。已有预备课、手算、[分析式证明技术](learning/01a_proof_techniques.md)、核心证明讲义、有限必要障碍与 [两周研讨安排](learning/07_seminar.md)。先掌握主线，不按提交时间通读所有研究分支。

讲义现以逐章重写的 Markdown 为源：主证明在正文连续展开，下界、归约、异构与非线性材料在 [十三份教学附录](learning/appendices/) 完整展开。每份附录都有自身的模型、结论和证明；非线性教学重构的来源状态独立标明，不视为已存在的规范研究分支或软件。全部教学文件、数学身份和规范阅读依据登记在 [learning/manifest.json](learning/manifest.json)，本轮审读范围及修改见 [learning/AUDIT.md](learning/AUDIT.md)。

## 当前目标与主要成果

当前主要算法目标是：对任意设施数、共同目录、显式可达集合和正二进制有理原子权，在联合输入位长多项式时间内构造完整因子 2 近似 SPE。**一般因子 2 存在性已有完整内部证明，高效构造仍开放。** 最佳统一常数是否小于 2 是另一项研究问题。

| 成果 | 精确范围与结论 | 现行入口 |
| --- | --- | --- |
| 共同目录双设施 φ | 任意覆盖和正原子权；尖锐普遍因子 φ，显式有理输入有位多项式构造 | [分支](research/current/shared/README.md)、[完整证明](research/current/shared/proof.md)、[锐性下界](research/current/shared/sharp_phi_lower.md) |
| 一般异构双设施 2 | 不同目录；四种子/全环上界及匹配下界；当前账本仍为内部候选 | [分支](research/current/heterogeneous/README.md)、[全环](research/current/heterogeneous/full_catalog_cycle.md) |
| 任意长单交叠异构目录 ρ | 每个合法跨目录对至多一个共有客户；固定完整纯规则给出尖锐 ρ；双侧目录长度不受限 | [全长直接证明](research/current/heterogeneous/sparse_unbounded_rho.md) |
| 共同目录实例复杂度 | 每个事先固定的有理 1≤a<φ，判定实例最优倍率≤a 弱 NP 完全；三地点处理 a=1，五地点覆盖全部 1<a<φ | [结构与算法边界](research/current/shared/instance_complexity_barriers.md)、[五地点全归约](research/current/shared/five_site_exact_hardness.md) |
| 任意设施数共同目录 2 | 存在纯选址、站内均匀在轨客户 NE 和完整精确纯离轨续局；不声称 2 尖锐或一般位多项式 | [主定理](research/current/multi_facility/uniform_two.md)、[逆审](research/current/multi_facility/reverse_review.md) |

以上成果审查状态不同，均无外部同行评审记录。精确作用域、来源证明、现行重构、内部审查与实现分别登记在 [命题账本](research/current/claims.md) 和 [五轴状态表](research/review_status.json)。内部证明、有限实例证书及学术发表是不同层次。

## 算法前沿在哪里

[计算前沿](research/current/multi_facility/polytime_frontier.md) 已把离轨完成分成可检查的条件接口。逐席贪心可造预算，但一般客户修复未必与预算兼容；全输入还缺合适的在轨布局/精确客户均衡选择及多项式复杂度证明。

[盒内完成](research/current/multi_facility/polytime_frontier.md)、[自适应原池重置](research/current/multi_facility/adaptive_reset_floor.md) 和 [冻结安全超载](research/current/multi_facility/frozen_overload_completion.md) 是三类可复用接口。最后一类只给偏离者设收益帽，允许其他设施安全超载。它们不提供任意输入的成功证书生成器。特殊可算类按讲义 [工具](learning/05_tools.md) 分类阅读；必要障碍集中在 [前沿](learning/06_frontier.md)，不必逐个记住优先规则反例。

实时进展放在 [RESEARCH_STATE.md](RESEARCH_STATE.md)，准确失败量词见 [FAILED_ROUTES.md](FAILED_ROUTES.md)。[路线图](research/ROADMAP.md) 与 [问题库](research/questions) 用于选题，不替代现行证明。[2026-10-05 发表对标](research/PUBLICATION_BENCHMARK_2026-10-05.md)比较实际期刊论文、各成果包的贡献力度及投稿判断，并记录对 2025 博士论文相关章节的优先权核查；不提升数学审查状态。2026-10-01 的 [出版评估](research/PUBLICATION_REVIEW.md) 保留为历史快照。

## 仓库结构

| 区域 | 用途 |
| --- | --- |
| [learning](learning) | 人类团队的分层课程、练习、核心证明路线与两周研讨会 |
| [research/current](research/current) | 现行模型、命题、完整数学证明与算法解释；定义与结论的权威入口 |
| [facility_spe](facility_spe) | 双设施规范算法、局部/实例精确求解和验证器 |
| [multi_facility_spe](multi_facility_spe) | 任意设施数的有限精确构造器；指数搜索，不能作为一般多项式算法 |
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
