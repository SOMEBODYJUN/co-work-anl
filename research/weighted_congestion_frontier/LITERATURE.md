# 文献与协作参考

核对日期：2026-10-14 UTC。下面是 Paper Fact 与设计借鉴；未穷尽后续文献，不能据此认证新颖性。用一手网页检索并阅读准确陈述；成功验收前复查更新。

## 数学基线

1. Christodoulou, Gairing, Giannakopoulos, Poças, Waldmann，*Existence and Complexity of Approximate Equilibria in Weighted Congestion Games*：[arXiv:2002.07466v3](https://arxiv.org/html/2002.07466v3)，[ICALP 2020](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2020.32)。§2 精确模型与成本约定；§3 Theorem 1、式(3)非存在族及 Ω(√d/log d)；§6 Theorem 4 为 n-PNE 存在；§7 公开要求缩小缺口。§7 对势函数方法的讨论是研究动机，不是已证明的工具不可能性。
2. Caragiannis–Fanelli，*On approximate pure Nash equilibria in weighted congestion games with polynomial latencies*：[arXiv:1902.07173](https://arxiv.org/abs/1902.07173)，[JCSS 版本](https://www.sciencedirect.com/science/article/pii/S0022000020301008)。摘要的 (d+δ) 存在保证取 δ=0 得 d。会议与扩展稿社会成本常数有版本差异，本分支不使用其未逐项核对的效率常数。

当前基线保持粗粒度安全陈述；更细 finite-d 上界、后续存在/计算结果的假设由执行天团按相关 idea 核对。精细界优于 d 时，不能把只优于 d 的旧结果叫新突破。

## 开源协作：逐项取舍

| 一手项目 | 实际机制与适配 | 不应冒称 |
| --- | --- | --- |
| [LemmaTrail](https://github.com/JanBartos6/LemmaTrail) | 保存精确研究对象、来源、失败机制、继续点；借鉴持久研究状态 | README 要人类决定 canonical 并通过 PR；本项目没有机械移植该治理规则，也不是它的部署 |
| [Joe975/math-lab 的 AGENTS](https://github.com/Joe975/math-lab/blob/main/AGENTS.md) | 自主挑题、按机制检查既有尝试、跨领域传播、独立攻击；借鉴自主选 idea 与真实失败资产 | blind 必须实际隔离已有路线；读过后不能自称干净上下文。其结果身份不替本项目背书 |
| [zhang5lo2/Math](https://github.com/zhang5lo2/Math) | 数学建模流水线、可复现代码与结果 | 固定流水线岗位与本项目的平等开放探索不吻合，不能据其存在说已找到用户要的天团架构 |
| [GitHub refs 文档](https://docs.github.com/en/rest/git/refs#update-a-reference) | 非 force 更新避免覆盖；本工具用普通 Git push 后重新检查状态 | 评论/不同消息文件本身不能提供互斥；租约不保证断网计算绝无重复 |

这些来源提供部分可用机制，没有已核实的开源项目完整实现这里的“多个 Codex 对话各带子 agent、平等公屏认领”。本轮是为用户工作方式编写的适配协议和工具，不把借鉴说成开箱即用部署。
