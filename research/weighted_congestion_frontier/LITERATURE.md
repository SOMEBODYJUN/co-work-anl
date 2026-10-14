# 文献与协作参考

核对日期：2026-10-14 UTC。下面是 Paper Fact 与设计借鉴；未穷尽后续文献，不能据此认证新颖性。用一手网页检索并阅读准确陈述；成功验收前复查更新。

## 数学基线

1. Christodoulou, Gairing, Giannakopoulos, Poças, Waldmann，*Existence and Complexity of Approximate Equilibria in Weighted Congestion Games*：[arXiv:2002.07466v3](https://arxiv.org/html/2002.07466v3)，[ICALP 2020](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2020.32)。§2 精确模型与成本约定；§3 Theorem 1、式(3)非存在族及 Ω(√d/log d)；§6 Theorem 4 为 n-PNE 存在；§7 公开要求缩小缺口。§7 对势函数方法的讨论是研究动机，不是已证明的工具不可能性。
2. Caragiannis–Fanelli，*On approximate pure Nash equilibria in weighted congestion games with polynomial latencies*：[arXiv:1902.07173](https://arxiv.org/abs/1902.07173)，[JCSS 版本](https://www.sciencedirect.com/science/article/pii/S0022000020301008)。摘要的 (d+δ) 存在保证取 δ=0 得 d。会议与扩展稿社会成本常数有版本差异，本分支不使用其未逐项核对的效率常数。

当前基线保持粗粒度安全陈述；更细 finite-d 上界、后续存在/计算结果的假设由执行天团按相关 idea 核对。精细界优于 d 时，不能把只优于 d 的旧结果叫新突破。

## 开源协作：逐项取舍

| 一手项目 | 实际机制与适配 | 不应冒称 |
| --- | --- | --- |
| [Anthropic / claudes-c-compiler](https://github.com/anthropics/claudes-c-compiler)，[作者机制说明](https://www.anthropic.com/engineering/building-c-compiler) | 作者在 Running Claude in parallel 明确说明不使用 orchestration agent，每个 agent 自行选择下一任务；在 `current_tasks/` 写认领文件，Git 同步使重复认领者换题。仓库同时有 `ideas/`。直接借鉴自主选题、细粒度认领、独立 clone 和 Git 持久化 | 软件项目；作者也使用临时专门任务，不是所有实际动作完全同质。没有原生数学命题账本，也没有我们的 Codex 跨对话公屏，不能保证其代码或证明正确 |
| [jarmstrong158/agentsync](https://github.com/jarmstrong158/agentsync)，[维护者发布说明](https://pypi.org/project/agentsync-mcp/) | agent 自己 survey、claim、build；独立 `agentsync` 分支保存状态，普通 push 作为 compare-and-swap，冲突后重新读取并验证占用；支持多个 agent，无须中心派单。直接对照本工具的冲突认领恢复机制 | 它的原版主要按文件/依赖去重，不能识别数学语义；并未在本项目安装它的 MCP，也不把 Git 冲突合并等同于数学 idea 去重 |
| [LemmaTrail](https://github.com/JanBartos6/LemmaTrail) | 保存精确研究对象、来源、失败机制、继续点；借鉴持久研究状态 | README 要人类决定 canonical 并通过 PR；本项目没有机械移植该治理规则，也不是它的部署 |
| [Joe975/math-lab 的 AGENTS](https://github.com/Joe975/math-lab/blob/main/AGENTS.md) | 自主挑题、按机制检查既有尝试、跨领域传播、独立攻击；借鉴自主选 idea 与真实失败资产 | blind 必须实际隔离已有路线；读过后不能自称干净上下文。其结果身份不替本项目背书 |
| [zhang5lo2/Math](https://github.com/zhang5lo2/Math) | 数学建模流水线、可复现代码与结果 | 固定流水线岗位与本项目的平等开放探索不吻合，不能据其存在说已找到用户要的天团架构 |
| [GitHub refs 文档](https://docs.github.com/en/rest/git/refs#update-a-reference) | 非 force 更新避免覆盖；本工具用普通 Git push 后重新检查状态 | 评论/不同消息文件本身不能提供互斥；租约不保证断网计算绝无重复 |

“无中心派单、成员自主选题和认领、Git 避免重复”已有直接开源先例，上两项就是本轮实际核验的来源。前次把这一组织方式整体说成定制，范围过窄。我们的适配部分是数学精确身份、idea/proof obligation 粒度、Codex 多对话各带子 agent、租约与冻结资产公屏；没有声称任何外部项目完整部署了这些全部细节。此次补充核验只涉及协作来源，不改变数学基线的核验范围。

## 原文归档与写作参考

本轮固定上游 commit 并原样保存选定原文件及许可，逐字节哈希和来源在 SOURCES.md、upstream/manifest.json。包括 MathLab 原始 prompt 与架构、Anthropic 真实认领/idea 样例，以及 mathematical-academic-writing 与 polish_skill 的数学写作、贡献重建、优先权/相关工作和 TeX 保真材料；latex-paper-skills 只选 framing 原文。原文与适配分别标注，不把外部原 Director/CLI 无限loop声称已在 Web 部署。当前尚无团队新数学结果、工具或论文。
