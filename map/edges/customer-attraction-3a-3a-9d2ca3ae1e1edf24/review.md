# 审阅记录：M-94fb 5251 行点

## 完整读取

本轮完整读取任务定义（含 read-add 后的 `M-c213464ff5db45bcb0625547ae7f20a1`）、`AGENTS.md`、`research/IMPLEMENTATION.md`、`prompts/03-map-worker.md`、登记总表中两个 endpoint 的完整记录，以及任务声明的 8 份材料。两份 81 万字节级 JSON 和 43 万字节级 replay JSON 以原始字节读取并解析全部顶层字段、1905 列、所有保存质量和 4 个 point summaries；未把截断的终端输出当作读取范围。全部声明 SHA 匹配。

## 数学判断

核心对象是有限必要行系统的 `finite` 有理点：5251 行（旧 4927 + 新 324）全部精确非负，但同一 1905 列质量在追加的 36 条实际安全 floor 上有 5 个严格负值。最负值及五个精确键已在 `support.md` 和两个 checks 边中给出。新增 324 行的真实源/查询/`min`-投影恒等式和源码对字面隐藏状态的 617220 个系数比较均已核对；这只支付固定有限行的必要性和审计身份。

read-add 对端 5287 行点全部通过 36 floor，但其 207 个质量列与核心点不同（`K=1`、`hist=10`、`joint=106`、`overlap=90` 改变），且 `W` 改变。故只能记录同族点态 checks/context overlap，不能作 implies、refutes、specializes 或 half 迁移。共同定义只固定模型语义，不能生成 hub 边。deferred 候选未读、未作为证据。

## 边界

没有重跑旧全图、LP、优化器或完整 SPE 树；原文件已记录的两次 CLI Fraction 验证仅作为来源证据。`W<1/2`、负 floor、辅助质量或有限点态差异都不能升级成完整 SPE/half 结论。开放义务是寻找真实目录/完整策略实现，或给出满足全部历史 IC 的精确完整 SPE 反例。

## 交付

本任务只交两条 `checks`/`context` 边：一条 self-context 记录核心有限审计与完整模型的语义断点；一条记录核心 5251 点与 read-add 的 5287 点之间的精确点态差异。两条边均不含 `whole_result` 或 `contribution`，不改变任何数学对象状态，不写 registry、Boss、board 或 Git。
