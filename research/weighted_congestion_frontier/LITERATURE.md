# 文献与协作参考

核对日期：2026-10-15 UTC。下面是 Paper Fact 与设计借鉴；未穷尽后续文献，不能据此认证新颖性。用一手网页检索并阅读准确陈述；成功验收前复查更新。

## 数学基线

1. Christodoulou, Gairing, Giannakopoulos, Poças, Waldmann，*Existence and Complexity of Approximate Equilibria in Weighted Congestion Games*：[arXiv:2002.07466v3](https://arxiv.org/html/2002.07466v3)，[ICALP 2020](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2020.32)。§2 精确模型与成本约定；§3 Theorem 1、式(3)非存在族及 Ω(√d/log d)；§6 Theorem 4 为 n-PNE 存在；§7 公开要求缩小缺口。§7 对势函数方法的讨论是研究动机，不是已证明的工具不可能性。
2. Caragiannis–Fanelli，*On approximate pure Nash equilibria in weighted congestion games with polynomial latencies*：[arXiv:1902.07173](https://arxiv.org/abs/1902.07173)，[JCSS 版本](https://www.sciencedirect.com/science/article/pii/S0022000020301008)。摘要的 (d+δ) 存在保证取 δ=0 得 d。会议与扩展稿社会成本常数有版本差异，本分支不使用其未逐项核对的效率常数。

3. Ren–Wu–Xu–Yang，*$\rho/(1-\varepsilon)$-approximate pure Nash equilibria algorithms for weighted congestion games and their runtimes*：[arXiv:2208.11309](https://arxiv.org/abs/2208.11309)，2025 年期刊版。摘要给出 $\rho=2W(d+1)/(2W+d+1)\le d+1$ 的算法保证，但其定理要求玩家权重归一化在 $[1,W]$（$W$ 为固定常数），并在正文另有正系数/系数比的有界条件。因而当 $W$ 无界、允许零系数和任意正实权重时，它不是 MODEL 的全类上界；这里只记录为受限子类边界，不能替代 WC-TARGET。

当前基线保持粗粒度安全陈述；更细 finite-d 上界、后续存在/计算结果的假设由执行天团按相关 idea 核对。精细界优于 d 时，不能把只优于 d 的旧结果叫新突破。

## 本轮匹配上界核查（2026-10-15）

重新打开 Christodoulou--Gairing--Giannakopoulos--Poças--Waldmann 的 v3 原文。其第 7 节把多项式费用的已知非存在
\(\Omega(\sqrt d/\ln d)\) 与已知存在的 \(d\)-PNE 之间的差距明确列为后续问题，并说明当时的存在上界方法本质上依赖势函数：
<https://arxiv.org/html/2002.07466v3>（§7，尤其 lines 513--519）。这只是 Paper Fact，不是本项目目标的答案。

截至本轮检索，未找到覆盖 MODEL 全部任意正实权、任意有限策略族和非负系数次数至多 \(d\) 多项式的
\(O(d/\ln d)\)-PNE 存在定理。2021--2023 的后续工作仍给出 \(d\) 或受权重上界约束的算法保证；其中出现的
\(\Phi_d\sim d/\ln d\) 主要是 PoA/PoS 根或下界参数，不能替换为近似均衡存在因子。该检索是有限范围的文献证据，不能证明全球不存在遗漏来源；因此 WC-TARGET v1 继续 OPEN。

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

本轮固定上游 commit 并原样保存选定原文件及许可，逐字节哈希和来源在 SOURCES.md、upstream/manifest.json。包括 MathLab 原始 prompt 与架构、Anthropic 原始任务/idea 样例，以及 mathematical-academic-writing 与 polish_skill 的数学写作、贡献重建、优先权/相关工作和 TeX 保真材料；latex-paper-skills 只选 framing 原文。原文与适配分别标注，当前运行按本项目的角色号与异步公屏协议。团队结果已分类入库；现行数学与审查见 ../current/weighted_congestion/README.md。全球优先权与论文发表未认证。
