# 运筹学与优化理论：论文机制、选题比较与直接试攻

本分支当前任务是**重新选题**：以能做成自足数学贡献、清楚讲明机制、匹配运筹学/优化理论训练为优先，从原始论文广搜、精读、比较并实际试攻。用户最新指定优先研究**原子博弈、Nash均衡、近似公平分配、广义指派近似算法**；尚未选定最终主定理，不能沿用旧调度题的唯一目标。

| 当前操作身份 | 固定值 |
| --- | --- |
| 研究分支 | `research/or-topic-battle-20261020` |
| 独立公屏 | `topics/or-optimization-board` |
| 存档 | `or-optimization-selection` |
| 研究地图 | [research/topic_selection/README.md](research/topic_selection/README.md) |
| 完整提示词 | [BOSS_START.md](research/topic_selection/BOSS_START.md) |
| 操作程序 | [work.py](research/weighted_congestion_frontier/tools/work.py)；[RUNBOOK](research/topic_selection/RUNBOOK.md) |

## Research Goal

用户愿意投入20天、每天12小时的gpt-6.1-sol ultra资源。预算用于校准规模，不是成功或后台自动运行保证。先从多个论文族提出候选，再寻找最小但有独立内容的成果包，不以名气、题龄、文件数或模型赞同代替判断。

## Mathematical Objects / Definition Map

目前不是一个统一数学模型。每个候选单独固定对象、定义域、量词、假设、输出和位复杂度。A=作者明确原题；B=作者明确建议方向；C=我们从论文机制派生的精确子题。作者提出大方向，不等于提出我们的特定子题。

论文类型（问题/工具/视角/结合/分类）→精确原定理→承重工具与假设→保留障碍的最小模型→候选命题→证明义务和反例→完整成果包。分类题检查等价刻画、自然扩类、最小禁形或不变量；工具题检查可迁移接口。

## Claim Map / Dependency Graph

从[身份账本](research/topic_selection/CLAIMS.md)进入候选原文、精确问题和实验。文献事实、新猜想、有限观察、完整证明和新颖性分别记录；检索到open字样不代表今天仍开放。比较中的优先级是研究判断，不是成功概率或数学推论。

本轮已保存[59条统一来源候选记录](research/topic_selection/candidate_pool.json)与[实际交叉比较](research/topic_selection/BATTLE.md)；原文机制链分别为[原子博弈](research/topic_selection/lanes/atomic.md)、[公平分配](research/topic_selection/lanes/fair.md)、[广义指派](research/topic_selection/lanes/gap.md)。第二轮已完成，具体反击直接改变候选状态，不按论文数量或投票决定主攻。

## Research Frontier / Known Results / Open Problems

当前承重不确定性是：是否被已有定理覆盖、切口是否只是直接推论、玩具模型能否扩成有内容的定理、一般化后是否重新变成巨大开放问题。具体候选、异议和核验从[本分支前沿](research/topic_selection/RESEARCH_STATE.md)读取。后续已解或覆盖的种子见[排除与回收](research/topic_selection/FAILED_ROUTES.md)。本轮没有把新候选升级为可靠新定理。

## Next Actions

广搜后精读前列论文、重构机制并直接试攻。成熟结果才安排后置独立攻击；探索不需要Route Card、reviewer、路线配额或审批。失败时保留真实边界与可复用机制，避免只有换参数和增加样本。

## File Map

| 完整仓库路径 | 内容、用途与读取时机 |
| --- | --- |
| research/topic_selection/README.md | 选题总地图；连接候选、证据、比较、提示词与下一义务 |
| research/topic_selection/RESEARCH_STATE.md | 当前试攻及剩余不确定性；每次接续先读 |
| research/topic_selection/CLAIMS.md | 精确身份和A/B/C来源；引用或修改候选前读 |
| research/topic_selection/FAILED_ROUTES.md | 已解旧题、直接推论风险、淘汰范围；避免重复 |
| research/topic_selection/BOSS_START.md | 含用户完整指导的完整提示词；新对话启动 |
| research/topic_selection/RUNBOOK.md | 分支、公屏、恢复、私聊、保存和远端确认命令 |
| research/topic_selection/branch_manifest.json | 分支、save、入口和基线SHA合同 |
| research/CATALOG.md | 全仓逐文件名称及用途；按需查旧资产和工具 |

## 独立保留的旧课题

旧[不相关机地图](research/current/unrelated_machines/README.md)、[拥塞地图](research/current/weighted_congestion/README.md)、[设施地图](research/current/README.md)和[客户吸引地图](research/current/customer_attraction/README.md)保留原身份、正文和证据。UM-TARGET-v1及其一般反面仍OPEN；本轮暂退出主攻，不是数学或价值否定。旧main和wcg/board不接收本分支保存。完整旧根地图由branch_manifest.json的base_commit恢复。

旧存档 `unrelated-machines`、旧目标 `UM-TARGET-v1` 仅作历史与按需工具入口，不是本分支启动任务。
