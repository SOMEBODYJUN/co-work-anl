# 共同研究：顺序客户吸引的一般半覆盖

当前唯一主攻 **Q-CAG-HALF**，存档 **customer-attraction**：一般共同目录、任意人数、每个完整历史依赖纯子博弈精炼均衡的福利是否至少达到最优的一半。主目标仍 **OPEN**。新对话从本文和[本题短地图](research/customer_attraction/README.md)恢复；不相关机、拥塞和两阶段设施是分别保留的研究线。

## 研究目标与数学对象

有限单位客户集 N，有限非空共同主题目录 S⊆2^N，m≥1名单位权提供者依次观察全部有序历史并选择一个主题。终局 a=(S₁,…,Sₘ) 中，客户 x 的覆盖者数为 cₓ(a)，提供者 i 的收益为 uᵢ(a)=Σₓ∈Sᵢ 1/cₓ(a)，福利 W(a)=|∪ᵢSᵢ|=Σᵢuᵢ(a)。OPTₘ 是 m 个目录主题的最大并集大小。

**精确目标：对每个上述实例、每个 m、每个在全部有序历史最优的纯 SPE σ，证明 2W(a(σ))≥OPTₘ。** 允许重复主题、空主题、零客户和任意历史依赖平局。零福利用乘法不等式，不定义0/0。客户不再作第二阶段负载优化。完整定义和原文范围见[模型](research/current/customer_attraction/model.md)及[文献边界](research/current/customer_attraction/literature.md)。

## 定义、命题与依赖

模型 → 全历史 SPE 的真实偏离不等式 → 小人数福利定理 / 目录结构定理 → 一般目标。安全值、策略锥、运输和分支支付只是可选择的表示或充分接口，不是方法白名单，也不是已解决的一般桥。

| 数学身份 | 当前认识 | 证明、限制与证据入口 |
| --- | --- | --- |
| Q-CAG-HALF | 任意目录与人数仍OPEN；没有完整证明或真正反例 | [精确目标](research/questions/customer_attraction_half_coverage.md)、[本题账本](research/customer_attraction/CLAIMS.md) |
| 三人、四人一般目录 | 三人锐5/3；四人1499/750<2；内部证明与审查 | [三人证明](research/current/customer_attraction/three_player_sharp.md)、[四人证明](research/current/customer_attraction/four_player_bound.md) |
| 五人一般目录 | 当前上界约2.061695>2，未达半覆盖 | [精确有理界](research/current/customer_attraction/five_player_indexed_bound.md)；模板最优点不是SPE反例 |
| 有限极大覆盖 / 层级结构 | 至多六极大任意人数已证；七极大仅有明确部分范围；另有向日葵与层级关联定理 | [按范围的完整结果表](research/current/customer_attraction/README.md) |
| 完整策略计算与证书 | 集合值逆向归纳、客户重数锥、有限精确核验 | [终局全集](research/current/customer_attraction/exact_solver.md)、[策略锥](research/current/customer_attraction/strategy_cone.md)；不构成一般证明 |

## 真正前沿与失败机制

早期偏离会改变全部后继行动。缺口是跨真实分支的全局福利控制；当前没有可直接归纳的一般支付机制。[研究前沿](research/customer_attraction/RESEARCH_STATE.md)固定剩余义务，[失败地图](research/customer_attraction/FAILED_ROUTES.md)解释逐人保底、逐步非负、根总税和冻结后继为何失败。新方法可以完全绕开这些接口。

下一步直接攻一般全称命题，或寻找排除全部真实续局歧义的合法反例。新增局部常数、有限样本、辅助桥反例可有独立价值，但各按真实范围保存。计算、内部审查、外审和新颖性保持不同状态。

## 三个角色与一个程序

| 当前角色 | 工作 | 可直接复制的提示词 |
| --- | --- | --- |
| Boss | 自主带团队研究；自由选路、证明、反例、计算和交流，探索不设前置审核 | [BOSS_START](research/customer_attraction/BOSS_START.md) |
| 清洗者 | 检查对象、证明和证据，处理真实异议；整理自足资产并入库 | [CLEANER](research/customer_attraction/CLEANER.md) |
| 整理者 | 判断独立成稿、拆合与定位；准确突出新增机制、意义和优势 | [EDITOR](research/customer_attraction/EDITOR.md) |

统一程序是根目录 [work.py](work.py)，附件单文件也能恢复独立clone。身份自动使用R-UUID并复用本clone绑定；新会话默认customer-attraction，旧存档不会自动改绑。全部研究提交main，公屏、提及、私聊和个人桌面继续使用同一工具。命令见[RUNBOOK](research/customer_attraction/RUNBOOK.md)。

## 研究文件地图

| 完整路径 | 内容、作用与读取时机 |
| --- | --- |
| research/customer_attraction/README.md | 当前主攻的短入口与最短阅读链；新boss首先进入 |
| research/customer_attraction/RETAINED_QUESTIONS.md | 保留问题的开放、已闭合、失效接口及暂停旧题，避免重复立项 |
| research/current/customer_attraction/README.md | 每份自足正文、范围、代码和证据的完整索引，按当前义务查阅 |
| research/current/claims.md、research/review_status.json | 全仓精确身份及证明/内审/外审/实现的权威账本，引用和状态提升时读取 |
| research/assets.json、research/graph.json、research/catalog.json | 命题文件合同、真实数学依赖、中文名称与用途；有实质变化时同步 |
| research/questions/customer_attraction_general_handoff.md | 未闭合的数学义务及已失败桥的范围；不再重复存放长角色提示词 |
| research/reviews/customer_attraction/、customer_attraction/、tests/ | 已发生的审查、规范实现及独立验证；以每条合同为准 |
| examples/customer_attraction/、evidence/ | 实际输入、完整策略证书及冻结运行；冻结记录不原位覆盖 |
| research/workspaces/customer-attraction/ | 每位研究者持续备份的个人桌面，含未核验与失败尝试；整理后进入按数学对象组织的共享资产 |

[研究总目录](research/README.md)、[中文资产目录](research/CATALOG.md)、[全仓资产](ASSETS.md)与[生产规则](research/REPOSITORY_GUIDE.md)补充导航。历史来源从[历史入口](history/README.md)进入；本次实际清理与原字节追踪见[整理记录](research/customer_attraction/CURATION.md)。
