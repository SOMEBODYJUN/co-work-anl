# 加权拥塞独立旧题与共享协作程序

**当前主攻为UM-TARGET-v1，save=unrelated-machines。** 新对话从[本题数学地图](../current/unrelated_machines/README.md)、[完整BOSS提示词](../unrelated_machines/BOSS_START.md)和[操作手册](../unrelated_machines/RUNBOOK.md)开始。本目录tools继续承载全仓共享程序，历史路径不改变数学目标；当前角色prompts也已切换新题。

## 独立保留的拥塞数学

旧Cd/ln d全类存在命题已有[完整线性全状态否定证明](../current/weighted_congestion/linear_degree_allstate_lower_bound.md)：每整数d≥2^20有全部状态严格(d/10)改善的有限正有理两动作游戏。精确身份与量词见[CLAIMS](CLAIMS.md)，从[现行拥塞地图](../current/weighted_congestion/README.md)沿正文进入独立审查、代码和冻结证据。WC-TARGET v1长期精确门槛身份保留；常数、有限d与外部评审等按旧题账本处理。

[英文主稿PDF](../current/weighted_congestion/linear_threshold_article.pdf)、[LaTeX源](../current/weighted_congestion/linear_threshold_article.tex)和[成稿审读](../reviews/weighted_congestion/linear_threshold_article_review.md)保留。外部同行评审、优先权和期刊录用均不由内部重构保证。

本目录MODEL、CLAIMS、ACCEPTANCE、RESEARCH_STATE和FAILED_ROUTES只属于此独立模型。旧[PRO_BRIEF](PRO_BRIEF.md)、[来源快照](PRO_BRIEF_SOURCES.json)及[冻结导出器](tools/export_pro_packet.py)用于恢复旧解题前材料，包内OPEN是当时状态，不能当现行答案或新调度接题包。原旧提示词可从[切换前快照](https://github.com/SOMEBODYJUN/co-work-anl/tree/799393621d09ea1aeb702434a053ed77aa141587/research/weighted_congestion_frontier/prompts)恢复。

## 共享工具和当前角色

统一入口[work.py](tools/work.py)提供start、sync、公屏、私聊、提及、收件箱、已读、访问桌面和checkpoint。使用[当前手册](../unrelated_machines/RUNBOOK.md)，协议见[PROTOCOL](PROTOCOL.md)。新clone默认新题，旧shared绑定继续兼容；独立Work各用一个clone的main，不创建研究分支。

| 当前角色 | 新题任务入口 |
| --- | --- |
| boss共同研究 | [完整BOSS](../unrelated_machines/BOSS_START.md)；[TEAM兼容副本](prompts/TEAM.md) |
| 材料清晰者 | [CLEANER](prompts/CLEANER.md) |
| 工具提取者 | [EXTRACTOR](prompts/EXTRACTOR.md) |
| 论文者 | [PAPER_WRITER](prompts/PAPER_WRITER.md) |
| 内部研究者 / 外部Pro | [PEER](prompts/PEER.md) / [PRO_ATTACK](prompts/PRO_ATTACK.md) |
| 共同操作 | [OPERATIONS](prompts/OPERATIONS.md) |

旧题文件用途查[FILES](FILES.md)和[CATALOG](../CATALOG.md)；原件处置查[INTEGRATION](INTEGRATION.json)与[SOURCES](SOURCES.md)。数学身份、冻结原件及证据保持原范围；新题不默认读取这些旧题文件。
