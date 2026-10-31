# 研究运行层

这里包含两个轻量层：第二阶段半的登记/读取索引，以及第二阶段完成、第三阶段超图可用后给 Work 数学 Agent 使用的研究运行提示词。

当前仓库的数学正文继续放在 `archives/**/state/`，超图继续表示已经确认的对象关系。本目录增加一个轻量桥接层：2.5 只登记对象、来源、证据、边界和两跳读取索引；研究运行层再把这些内容分发给数学 Agent。

## 三种状态

```text
source records → object Markdown → Research Packet → research result → object / evidence / hyperedge proposal
```

对象 Markdown 不因 packet 生成而合并。一个 packet 可以引用多个对象，一个对象也可以进入多个 packet；登记层保存它们的关系和用途。2.5 不证明关系边，第三阶段才决定正式超边。

## 选定的开源参考

- [Danus](https://github.com/frenzymath/Danus)：Apache-2.0。主 Agent 调度只处理一个 claim 的 Worker，已验证事实进入 content-addressed fact graph；借鉴“小 claim、局部上下文、事实图和角色权限”，不照搬 CLI。
- [Noemesis](https://github.com/kbr-/math-research)：软件 MIT，研究文字 CC BY 4.0。借鉴 claim registry、append-only 记录、fresh-context review、失败路线和长期恢复。
- [Math Research Agent](https://github.com/dongxuelian2/math-research-agent)：MIT。借鉴 planner 返回 typed actions、依赖 DAG、ready frontier、continuation、证据回执和持久化研究状态。
- [OpenTorus](https://github.com/maximilianbehr/OpenTorus)：Apache-2.0。借鉴 typed dossier、prove-or-refute、显式 gap、攻击路线和可恢复 campaign。
- [OpenProof](https://github.com/mxthematic/openproof)：MIT。借鉴 planner/prover/retriever/repairer 的子目标分解和 proof-node graph；它的 Lean 核验属于按需工具，不是本项目的默认常驻角色。

这些项目的 CLI、模型提供商和执行后端都不直接成为 Work 的运行时。我们只移植可观察的数据契约、提示词结构、局部上下文和分支/恢复规则，并保留各自许可证与出处。

## Work 中的最小运行

Research Boss 作为唯一整合者，六个 subagent 采用两种配比：

- `continuation`：4 boundary + 2 blind；
- `hard-open`：2 boundary + 4 blind。

Verifier、adversary、形式化工具只在一个具体结果需要它时临时占位。常态输出是：新路线、对象关系、证据需求、失败边界和下一动作。两跳是默认上下文窗口，遇到边界再按路径扩展。

JSON 是路由和登记规范，数学正文仍用 Markdown。见 `schemas/`、`templates/`、`prompts/02.5-research.md` 和 `prompts/research-runtime.md`。
