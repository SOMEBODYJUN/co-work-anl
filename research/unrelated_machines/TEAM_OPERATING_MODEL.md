# UM-TARGET-v1 团队研究协议（门控版）

本文件把团队的评价单位从“运行了多少实例”改成“关闭了哪条承重 proof obligation”。它是协作协议，不改变 `UM-TARGET-v1` 的数学身份，也不把有限实验升级为证明。

## 当前判断

主目标仍是：存在统一 `ε>0` 和确定性位多项式算法，对所有一般 `R||C_max` 输入输出实际分配并满足 `C_max≤(2−ε)OPT`。当前最小共同义务是：对任意输入和阈值 `T`，由输入本身生成可计算的共同多机容量状态并一次性输出全机整数分配，或者输出可独立验证的 `FAIL⇒OPT>T`。给定分组、真实矩、支撑、home/sink、固定槽或逐机证书都不满足这个输入合同。

现有大规模枚举只能验证有限接口。它们的用途限于寻找最小反例、核查有限引理边界或审计实现；不能用样本数、随机成功率、提交数或同行赞同替代全称证明。以后不再扩大简化树、完整分配、随机实例、加权构造和预算检查的数量，除非运行前已经写出一个会被结果区分的参数化假设。

## 三条活动轨道

1. **正向算法轨道（主力）**：固定 `T>0` 和常数 `δ<1`，寻找比 LST/ST 与未强化配置 LP 多出的全局不变量。一个合格的候选必须联合选择大任务整数放置 `h` 与短任务分数 `x`，证明所有机器的共同容量不变量，并由槽舍入输出实际调度；若失败，必须给出可验证的 `FAIL⇒OPT>T`。它还要处理阈值搜索、零值、空任务、不可用边、极大分母和总位复杂度。
2. **反向困难性轨道（压力测试）**：只接受明确假设下的真实整数 gap。对每个固定 `δ>0`，必须有多项式归约使 YES 的 `OPT≤1`、NO 的每个合法调度 `OPT≥2−δ`，并给出对任意低负载调度的解码、规模和位长证明。配置/SA 间隙、单个固定 `ρ<2`、局部 3DM 选择困难或条件 Santa 假设均不能终结主目标。
3. **结构障碍轨道**：把两树、长链、宏/tiny、共享容量、投影遗忘和 occupied-home 等失败压缩为可复用的统一 obstruction 或判别条件。它的交付物是参数化引理或失败机制，不是继续制造同族样本。

每两个研究周期做一次 route gate。正向若没有新全局不变量，反向若没有任意 `δ` 的整数 soundness，结构若只是同一障碍的换名，均转为 `Salvage` 或 `Kill`，不再开同类 worker。

## 角色与隔离

角色是职责，不要求一角色一 agent。常驻最多四到五个职责，其他角色按 checkpoint 触发：

- **Theory Director / Integrator**：每周期最多选择一个正向和一个反向承重义务，维护 Claim、状态、失败路线和 go/no-go；不按投票升级。
- **Positive Algorithm PI**：只交全局算法、不变量或严格的算法边界；必须说明额外信息、实际输出和位复杂度。
- **Hardness PI**：只交完整 gap 归约或明确条件命题；必须说明 `δ` 量词、YES/NO、decoder 和复杂性假设。
- **Skeptic / Red-team**：优先寻找参数化逃逸；构造者未读审查前不得自审。
- **Proof / Complexity Auditor**：先盲读 statement，重构量词、外部定理条件、边界、oracle、终止和位长。
- **Literature Referee**：只核原始定理的精确假设、阈值、版本和定位，防止把邻近模型或已知工具误报为突破。

## Claim Card 与任务生命周期

任何推导或代码前，owner 先写一张卡：

```text
Claim ID/version；route=F/R/B；Exact Statement；Objects/Domain/Quantifiers/Assumptions/Scope
它关闭的唯一 proof obligation；相比 LST/ST/configuration-LP 新增的信息
一个核心 lemma 或构造；复杂度/位长账本；边界情形；攻击族
事前预算；停止条件；预期交付路径；owner；independent auditor
```

计算只允许服务于卡片中的一个可证伪问题，且必须在运行前写明预期分叉。结果只按以下状态处理：`Advance`（独立复核后的新全局引理/归约/障碍）、`Salvage`（主合同失败但保留独立资产）、`Blocked`（唯一义务未解且有下一检验）、`Kill`（重复、只增样本或不改 Claim）。构造者、盲审者、red-team 和复杂度审计者必须分离；存在一条未处理的 fatal objection 时，Claim 不能升级。

## 三轮 gate

**R1 架构轮**：正向交一页定理、伪代码和新不变量；反向交一页源 gap、归约骨架和 YES/NO 公式；结构轨道交一页统一 obstruction。禁止先跑大搜索。

**R2 盲审轮**：审查者只看精确 statement，攻击两树/长链、共享小端、多行容量、全 tiny 3-partition、零边、空任务和高分母；复杂度审计单独检查 oracle、阈值搜索、复制数和输出位长。

**R3 分流轮**：闭合主合同才进入 `current`；有独立边界或失败机制进入 `questions`/`FAILED_ROUTES`；否则冻结候选并停止同类微调。每次 gate 后只保留最多两个正向候选、一个反向候选和一个结构障碍。

## 公屏与 checkpoint

公屏消息统一以 `[TYPE][CLAIM-ID][STATUS]` 开头，随后只写精确结果、证据或 objection、一个下一问题、owner/auditor。每个有长期价值的引理、参数化反例、严格障碍、文献事实或审计结论立即 checkpoint；普通日志、重复摘要和样本计数不提交。checkpoint 前同步并重读受影响的 Claim、正文和 objection，保持 Truth、Value、Novelty、Mechanism、Ambition 分轴记录。

