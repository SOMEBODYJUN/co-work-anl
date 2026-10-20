# 运筹与优化选题：公开问题、工具迁移与分类边界

本分支 `research/topic-selection`、存档 `topic-selection`、公屏 `wcg/board-topic-selection` 专供重新选题。多个独立boss沿用各自actor协作；原 `main` 的 UM-TARGET-v1 及其正反面仍为 OPEN，本轮不继续将它作为必攻目标。

## Research Goal

在原子博弈、Nash均衡、近似公平分配和广义指派近似算法中，广泛发现、排重、攻击和比较有价值的研究切口。用户的工作窗口是二十天、每天约十二小时算力；这只是资源约束，不能作为定理可解或论文能录用的证据。运筹学与优化理论是方向约束。优先形成精确、有机制、有完整故事且可验证的结果，不以宏大猜想或候选数量代替质量。

## Definition Map / Claim Map

选题记录分为 Paper Fact（精确原文）、Interpretation（机制解释）、Proposed Problem（我们提出的精确新题）、Observation（计算）、Candidate Lemma（未审推导）。目前没有把任何新猜想升级为可靠定理。boss17首阶段已形成[资源边际与纯精炼均衡算法候选](candidates/atomic_potential.md)，优先级和独立反方见TOPIC_BATTLE。每题分别记录Truth、Value、Novelty、Mechanism和Ambition，评审者数量不充当证明。

## 评价方法

| 母文/想法类型 | 主要价值检验 | 第一轮反方攻击 |
| --- | --- | --- |
| 明确公开问题 | 是否推进原作者确实提出的问题，切片是否保留核心困难 | 查新版本、后续解决、量词/模型混淆 |
| 工具主导 | 是否带来可迁移机制，能否在新模型闭合承重接口 | 是否只是旧定理直接推论或符号替换 |
| 视角/组合主导 | 是否产生原方法看不到的结构或更强结论 | 桥梁是否免费、是否暗含同等难度oracle |
| 分类主导 | 是否自然扩大类别，给等价或最小障碍 | 是否增加人为限制、是否已有分类包含 |
| 新猜想 | 最小模型是否非平凡、失败是否能回收边界 | 枚举反例、最近邻、极端与退化输入 |

不把不同指标强行加权成一个伪精确分数，不给未经校准的成功率。先核实文献和首个proof obligation，再比较。

## Research Frontier / Next Actions

本轮六条子线分别覆盖原子博弈、Nash与优化、goods公平分配、chores与混合分配、广义指派、跨领域工具迁移及独立反方。每条广搜不同候选，深挖有明确入口者，再相互battle。最终短名单、范围和反方记录写入 [选题比较](TOPIC_BATTLE.md)；完整候选随后沿各专题入口读取。

## File Map

| 路径 | 内容、用途与何时更新 |
| --- | --- |
| [BOSS_START.md](BOSS_START.md) | 完整用户指导、选题方法及恢复/通信/提交命令；新会话从这里开工 |
| [RUNBOOK.md](RUNBOOK.md) | 新分支/新公屏的现有统一程序操作，保留默认main兼容 |
| [TOPIC_BATTLE.md](TOPIC_BATTLE.md) | 六线候选battle后的短名单、淘汰理由、承重义务；证据变化时更新 |
| [RESEARCH_STATE.md](RESEARCH_STATE.md) | 当前已核事实、待核重复与下一项数学验证，不写模拟进度 |
| [USER_GUIDANCE.md](USER_GUIDANCE.md) | 本轮原始用户选题指导及六线共用规则；固定不改写其含义 |

所有选题与观察仍需原文核查、数学攻击和新颖性查重。保存到Git不构成数学状态提升。
