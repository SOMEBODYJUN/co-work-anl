# 文献与协作参考

核对日期：2026-10-14 UTC。下面是 Paper Fact 与设计借鉴；未穷尽后续文献，不能据此认证新颖性。用一手网页检索并阅读准确陈述；成功验收前复查更新。

## 数学基线

1. Christodoulou, Gairing, Giannakopoulos, Poças, Waldmann，*Existence and Complexity of Approximate Equilibria in Weighted Congestion Games*：[arXiv:2002.07466v3](https://arxiv.org/html/2002.07466v3)，[ICALP 2020](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2020.32)。§2 精确模型与成本约定；§3 Theorem 1、式(3)非存在族及 Ω(√d/log d)；§6 Theorem 4 为 n-PNE 存在；§7 公开要求缩小缺口。§7 对势函数方法的讨论是研究动机，不是已证明的工具不可能性。
2. Caragiannis–Fanelli，*On approximate pure Nash equilibria in weighted congestion games with polynomial latencies*：[arXiv:1902.07173](https://arxiv.org/abs/1902.07173)，[JCSS 版本](https://www.sciencedirect.com/science/article/pii/S0022000020301008)。摘要的 (d+δ) 存在保证取 δ=0 得 d。会议与扩展稿社会成本常数有版本差异，本分支不使用其未逐项核对的效率常数。

当前基线保持粗粒度安全陈述；更细 finite-d 上界、后续存在/计算结果的假设由执行天团按相关 idea 核对。精细界优于 d 时，不能把只优于 d 的旧结果叫新突破。

## 开源协作参考

| 一手项目 | 来源事实 | 当前采用的经验 |
| --- | --- | --- |
| [Anthropic / claudes-c-compiler](https://github.com/anthropics/claudes-c-compiler)，[作者说明](https://www.anthropic.com/engineering/building-c-compiler) | 作者采用无中心 orchestrator 的自主选题、独立 clone 和 Git 任务协调；原项目有 `current_tasks/` 与 `ideas/` | 自主选择具体义务、持久资产、失败回收和有效反馈 |
| [agentsync](https://github.com/jarmstrong158/agentsync)，[维护者说明](https://pypi.org/project/agentsync-mcp/) | 以独立分支、普通 push 和冲突后重读协调 agent 状态 | 公屏独立分支与并发更新后重读，消息稳定 ID 支持恢复 |
| [LemmaTrail](https://github.com/JanBartos6/LemmaTrail) | 保存研究对象、来源、失败机制与继续点 | 可恢复的精确研究账本 |
| [Joe975/math-lab 的 AGENTS](https://github.com/Joe975/math-lab/blob/main/AGENTS.md) | 自主挑题、检查尝试机制、跨领域传播与独立攻击 | 干净上下文重构关键瓶颈、具体反例攻击 |
| [zhang5lo2/Math](https://github.com/zhang5lo2/Math) | 数学建模流水线、可复现代码与结果 | 对实际计算保存代码、参数和证据 |
| [GitHub refs 文档](https://docs.github.com/en/rest/git/refs#update-a-reference) | 普通非 force 更新保护远端已有历史 | 推送后确认与并发安全恢复 |

本项目采用一个 Work 对话一个角色号、内部 subagent、异步公屏和阶段 checkpoint。公屏交流像群聊，各对话自主研究、同题可独立并行。当前协议见 PROTOCOL.md；上游具体架构与本项目适配分别记录在 SOURCES.md。

## 原文归档与写作参考

本轮固定上游 commit 并原样保存选定原文件及许可，逐字节哈希和来源在 SOURCES.md、upstream/manifest.json。包括 MathLab 原始 prompt 与架构、Anthropic 原始任务/idea 样例，以及 mathematical-academic-writing 与 polish_skill 的数学写作、贡献重建、优先权/相关工作和 TeX 保真材料；latex-paper-skills 只选 framing 原文。原文与适配分别标注，当前运行按本项目的角色号与异步公屏协议。本轮已形成内部独立审查的 odd-ring 无限下界；外部论文与同行评审尚未完成。

## 2026-10-14：奇数环下界的实际文献审查

一手来源核查与检索限制保存在 [literature_review.md](assets/R1/odd_ring_audit/literature_review.md)。CGGPW 的模型、Theorem 1 equation (3) 和 §7 缺口与 MODEL 一致；CF 的有限次数上界已比粗 d 更细，bounded-weight 后续算法不覆盖本构造的任意权比。抽象 odd-cycle anti-matching 有既有 strategic-game 前例，不能声称该 parity idea 本身新颖。

本轮 mathematical result 为 E_d∼d/ln d 的合法无限非存在族；现行页自足证明原式(3)全域 O(√d) ceiling，故新旧精确下界对大次数严格分离。focused primary search 未发现相同或更强全类非存在结论；这不是全球 absence/priority 证明。Paper Fact、团队一般证明和检索 Observation 保持各自层级。
