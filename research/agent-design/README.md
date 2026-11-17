# Work + GitHub 数学研究：程序、提示词与回流

本仓围绕公开难题长期研究，使用 **1 Main + 3 个真实 Work 子代理**：独立原题/障碍线、成果线 A、成果线 B。四人均做数学。GitHub 保存可接续的数学与版本；Python 不启动模型、不判断自然语言证明的真伪。

上一版 `3e8402c` 交付了设计、三份词和只读 frontier，**没有完成工作室、应用采用、审查版本与增量入库的可执行闭环**；根 README、旧流程及模板导出也未统一。上轮 e0ad3a26 接通了基本文件链；本轮重新从真实入口复现保存、冻结、发布与恢复缺陷，直接修改现有函数并做两轮 CLI 回流和真实 Work 平凡数学演练。实际阅读范围和没有读过的范围见[仓库审计](ARCHITECTURE_AUDIT.md)，不以查看登记表冒称读完全部证明。

## 唯一用户入口

用户只需当前分支 [work.py](../../work.py)、仓库外凭据和[研究 Main 完整启动词](../../prompts/research-runtime.md)。执行者自行读取内部 Main、线路和复核词。未指定新数学原题时只完成准备，不擅自启动旧题或把测试称为实战。

| 入口 | 实际作用 |
| --- | --- |
| [Main 完整词](../../prompts/research-runtime.md) | 恢复仓库、固定原题、真实派工、Main 自身数学、持续保存和发布 |
| [内部 Main 细则](../../prompts/research-main-design.md) | 综合、前沿选择、反馈与跨线合作 |
| [线路词](../../prompts/research-line-design.md) / [复核词](../../prompts/research-review-design.md) | 同题三线的输入和交付；对准确版本作定向独立挑战 |
| [完整超边与回流流程](HYPEREDGE_WORKFLOW.md) | 真实命令、record-file、ALL/OR、条件欠账、局部结论、版本复核和入库 |
| [原题 spec 模板](spec-template.json) | 平面 JSON，填真实引用并去模板标志后直接传给 `studio init --spec` |
| [来源及实际复制清单](SOURCES.md) | 原样文件、许可、字节和 SHA；思想借鉴、实际运行依赖分别说明 |
| [本轮验收](validation.json) | 实际运行的测试、真实边消费、源码版本与能力边界 |

## 平时怎样工作

`research studio init` 复用原来的 `init`，固定两份输入 packet，并建立四人的目录：

- `research/workspaces/<RUN>/main/`：Main 自己的推导、综合、构造和证据。
- `independent/`：同一原题、定义和允许障碍下的独立研究。
- `informed-a/`、`informed-b/`：按不同数学缺口使用已有成果。

每人连续写 `journal.md`，有接续价值的推导、候选、失败、计算和反馈及时用原来的 `save` 或便捷的 `studio line` 保存。`research/runs/<RUN>/` 沿用同一套不可变 notes/events、实际 agent ID、未答反馈和恢复链；`studio.json` 仅索引采用、成果冻结与回流材料。普通中间结果不必再填一套表。

真正使用超边时才 `adopt`：逐项给全部联合前提、共同模型和量词、条件、合成桥的证据或未付义务。继承上游欠账，保留局部贡献的目标剩余；明确证明并复核后才可支付。两个开放预算互相等价不能自证，一族输入的全 SPE 贡献不能自动推广成一般 SUMmin。

新承重结果需要采用或回流时，才走 `artifact → freeze → review → promote`。冻结从已声明 batch/edge 自动展开原题、定义、完整证明、端点和关系证据；复核指向准确字节。记录非作者 ID 与独立声明不等于程序验证了平台独立性，Main 仍核真实执行。

## 中间结果怎样进入现有知识

| 内容 | 保存位置与动作 |
| --- | --- |
| 所有有用的中间工作、候选、失败与未付义务 | 各人 journal + RUN 的 save；Main 串行 checkpoint，确认 pushed |
| 可复用的局部引理、条件结论、有限结果、精确反例或开放义务 | 对应 `archives/.../state/` 完整正文及证据；比较稳定身份后生成登记增量 |
| 对象间真实推出、反驳或迁移 | `map/edges/`，完整 ALL 前提/替代 OR、条件、解释和证据；无数学关系可零边 |
| 已审准确增量 | `promote` 合并成 RUN 内 registry 候选，保留同行已有内容；用原 `register` 正式更新唯一总表，再检查、构建投影并用单次 checkpoint --review-plan 发布 |

`promote` 不是已经入库或推送。候选绑定当前 registry 字节；同步后基线变化会被 `register` 拒绝，须在最新快照重新合并。成果发布或同步后 Main 重读受影响 context/frontier，真实 followup 或派工；Python 不自动调用模型。日常使用 `research check/build`，**不把第三阶段 `--final` 的整批构图队列强加给每个研究结果**。第三阶段验收仍是其准确历史快照，新研究增量保自己的范围与证据。

## 为什么借这些，为什么不直接搬整套工程

- Ansatz：借依赖、失败与探索前沿的整理，并原样保存 curator/verifier 两份合同；其外部运行服务没有装入本仓。
- CoCo-Prover：借同一证明的全部子义务与替代证明分开执行；本仓没有 Lean 内核就不沿用其自动正确性等级。
- PACE / Euler：借本题适用性重核、独立的 closing implication 与长线接续；按本仓格式实现。
- OSVerify：原样保存一份 policy，借“先验证具体错误，再准确反馈原作者”；没有把无错误发现当完整证明。

逐文件、许可、来源日期和可核边界见 SOURCES。本仓原有正文—登记—超边、RUN、完整 ALL/OR、Git 发布和计算接口全部继续使用。新增 studio 有维护成本；因此它按需要使用，不增加数据库、模型 API 密钥、驻留调度器、每步工单或常驻审批岗位。它能减少漏前提、丢债、旧审查覆盖新版和过时增量覆写等工程错误；**不能保证数学正确、研究顺畅或攻克公开难题**。这些效果仍要由后续真实研究检验。
