# 2026 年 9 月以来的原始研究与取用记录

检索窗口为 **2026-09-01 至 2026-11-16**；检索日期 2026-11-16，均按 America/Los_Angeles。只用官方论文、官方代码和作者项目资料支撑技术判断。项目创建时间、论文首发、修订时间和代码版本是不同字段。没有把 9 月之前的 Aletheia、Danus、Station、原 Rethlas 或通用 GraphRAG 当成本次新研究。

## 哪些最适合本仓库

| 项目 | 日期与一手入口 | 实际结构/流程 | 取用与不能据此声称的事 |
| --- | --- | --- | --- |
| Ansatz / Continual Graph Memory | [论文 v1 10-02、v2 11-06](https://arxiv.org/abs/2610.02945v2)，[最新正文](https://arxiv.org/html/2610.02945v2)，[官方代码](https://github.com/uclanlp/continual-graph-memory)；公开代码 commit `23367c6568c344d9c4dbf59be3f39b39f5d54324` 为 09-26 | 已接受事实 DAG、带类型探索图、AND group、独立 verifier、curator 前沿与按需取回；回忆必须本地重新论证才作前提 | 最适合依赖/失败/恢复合同。公开 exploring_graph 是数据结构，很多传播规则在 curator 提示词，不可称完整自动数学推理器。代码版本不能冒作 11-06 论文全部实验的精确部署版本 |
| CoCo-Prover | [论文 10-07](https://arxiv.org/abs/2610.09681)，附录 B、E | 单声明 AND/OR proof hypergraph + 跨声明 lemma DAG；Lean 返回全部子目标；候选 elaborated 与稳定 stable 分开；选择目标后路由 specialist | 真正可核的 AND/OR 超边工程设计；验证对象是 Lean 程序验证基准，没有由此证明其解决了开放数学难题；本次未核实公开工程仓库/代码许可，不导入其源码 |
| OSVerify | [论文 10-13，v2 10-22](https://arxiv.org/abs/2610.18089)，[代码](https://github.com/OSVerify/OSVerify)，[运行合同](https://github.com/OSVerify/OSVerify/blob/main/docs/runtime-reference.md) | whole/segment 错误提出 → 去重 → issue validator → 逐字反馈 auditor → 原作者修复；输入/prompt/schema/backend 指纹与恢复 | 适合作为关键证明和计算的机动审查协议；READY_FOR_HUMAN 或无已确认错误不表示数学成立。开源 runtime 的一层分段和论文的一般算法分别描述 |
| Euler | [论文 10-14](https://arxiv.org/abs/2610.19864)，[代码](https://github.com/canghaimeng/Euler)，[架构](https://github.com/canghaimeng/Euler/blob/main/ARCHITECTURE.md)；论文固定 v0.3.0.dev0 / ea505c7 | route 保 parent、全部 premise obligations 和须有证据的 closing implication，构成逻辑超边；working graph 与 admitted fact graph 分开；全团队里程碑恢复 | 借鉴长线状态、联合闭合桥和恢复；原作/修改为 PolyForm Noncommercial，不拷工程代码。论文案例源自较早工作流，含人工指导和另行形式化，不能归因为当前控制器已自主解题 |
| PACE | [论文 10-24](https://arxiv.org/abs/2610.33690)，[全文及 E/F/G 附录](https://arxiv.org/html/2610.33690v1) | 原题/候选修订 → mechanism → whole prover → independent verifier；候选条件变化后重新核证据适用性；task-specific prompt composer | 借鉴 application-level revalidation，保留原引理。未核实其公开代码、许可证或精确可安装提示词包。`Trace231/ProofLoom` 不能直接当作 PACE 仓库 |
| ProofLoom | [论文 09-28](https://arxiv.org/abs/2609.34960)，[代码](https://github.com/Trace231/ProofLoom)，MIT | proof-obligation-driven theory construction、signature contracts、独立 Judge 防止弱化目标、Planner/Audit 与 Lean 库复用 | 对需形式化的成熟承重步骤有参考价值；重建已发表证明不等于攻克公开问题，本轮不增加 Lean 强制前置条件 |
| Noemesis | [代码](https://github.com/kbr-/math-research)，GitHub public API 记录创建于 09-10；[AGENTS](https://github.com/kbr-/math-research/blob/main/AGENTS.md)，[许可与署名](https://github.com/kbr-/math-research/blob/main/ATTRIBUTION.md) | Git 中长期数学笔记、稳定 claim、依赖 packet、按缺失推导推进、独立审读、指定 Lean 结果 | 很适合 Work/Git 文件持久化；软件 MIT、原研究文字 CC BY 4.0。只借机制并署名，不复制其大量特定研究规章。其一般主目标仍开放 |
| LEVER | [论文 10-08](https://arxiv.org/abs/2610.11862)，附录 A Listings 1–3 | planner/expander 产生完整子义务，AND 按全部子任务算账、OR 比替代路线；最终组装完整 Lean 文件复核 | 借鉴整条路线的未付成本而非只算最容易的一个子任务；PutnamBench 不等于公开难题，未核官方完整代码许可，不导入源码；共享子任务的重复收费另需处理 |

`dongxuelian2/math-research-agent` 创建于 08-18，虽有 11 月更新，未在本轮核出足够明确的 9 月以后新算法版本，故不作“本窗口新项目”的主要依据。早期 HyperGraphRAG 等只保留原历史来源，不用于替代本轮最新检索。

## 别人究竟怎样消费图

Ansatz 的公开流程是：worker 搜陈述和失败 → 取 fact 的前驱与全文 → 自己证明/应用 → 独立 verifier 决定是否接纳 → fact graph 保存依赖 → curator 把探索图的目标、AND 子任务和失败整理成下一前沿 → Main 再派工。其 `agents/contracts/curator.md` 对 `decomposes-into` 同 `and_group` 要全子义务 closed；localization 还需 reassembly fact；reduction 还需桥。传播是合同要求，公开 exploring_graph I/O 本身不证明这些桥。

CoCo-Prover 更接近严格的“超边驱动执行”：一次证明动作对父目标产生完整子目标集合，记录为一个 AND 分支；多个动作形成 OR。路由器选择待做的子义务，Lean 检查接受后才能稳定关闭。跨引理的暂用依赖与最终核验分开；失败只影响依赖该候选的支持，保留无关稳定子图。附录 E 给 system/router/lemma_planner/proof_writer/recovery_reviewer 五类真实 prompt。本仓借其规则，但自然语言引理没有 Lean 的自动真值判据。

Euler 的工程更接近本仓所需的长线研究：ProblemContract 固定原题和 scope，Obligation/Route 表达“全体前提 + closing implication ⇒ 父目标”，context compiler 编译任务输入；reconcile 依据带 claim/scope/kind/checker 的证据更新状态，root 另做完整原题验收。具体公开文件为 `euler/control/contracts.py`、`obligations.py`、`context.py`、`reconcile.py`、`acceptance.py`、`kernel_evidence.py`；真实角色词在 `agents/contracts/`。必要上下文超预算不能静默截前提。我们根据机制自行实现，不复制其非商业工程。

PACE 的可复用增量是：即使旧引理仍成立，改变候选的假设或量词也会使其“对新目标的应用”失效。重新打开应用桥和受影响后继，而不是抹掉旧数学。OSVerify 则给出把一项疑点变成可复核错误、再把精确反馈交还作者的工程合同。

本次未核到同时满足“明确的自动超边推理执行器、公开全部工程/提示词、并以该执行器独立验证解决一般著名公开难题”的统一范例。上面各项覆盖其中不同部分；不能拼接它们各自的成果宣称这种完整成功已经存在。

## 最新版本的必要辨析

Ansatz 11-06 v2 的表述是两批各九个 local-verifier closure，第二批另有 partial 按其准则算 pass；不沿用早期摘要 10/10 作为公认可复现解题率。[作者 10-23 澄清](https://arxiv.org/src/2610.02945v2/anc/SupplementaryData1_records/AUTHOR_CLARIFICATION_20261023.md)修正了早期答案暴露指控；不能把旧 release note 的指控当已证事实。模型内部接受、Lean、专家审查和发表状态分别记录。

[76 页公开 prompt protocol](https://arxiv.org/src/2610.02945v2/anc/SupplementaryData3_prompt_protocol.pdf)含完整 worker/verifier/curator 合同及 skills 等 47 项源记录；它是公开源捕获，不是运行对话，也未证明就是所有实验运行的精确提示词版本。

## 本轮确实拿过来的部分

`upstream/` 保存两种 Apache-2.0 原文合同及各自 LICENSE、适用 NOTICE、commit、源路径、字节数、SHA256 和是否修改。OSVerify 的 NOTICE 保留其 shared policy 对 Rethlas 的改写归属。没有安装整套模型服务，未复制 Euler 非商业源码或无法核许可的 CoCo 工程。新 Main/Solver/审查词是本仓库重新编写的适配，不把原合同里的角色权限、网络端口和工具指令作为本仓指令。

| 上游具体实物 | 本仓落实 |
| --- | --- |
| Ansatz `agents/contracts/curator.md` | ALL 全部义务、reassembly/bridge、未付前沿与循环不自证；`research frontier` 与 HYPEREDGE_WORKFLOW |
| Ansatz `agents/contracts/verifier.md` | 完整前提、引用和原命题的独立检查；research-review-design |
| OSVerify `src/osverifier/skills/policy.md` | 疑点本身须验证；confirmed/not_real/unresolved、保持原题的修复、反馈精确回传 |
| PACE 附录 E/F/G（机制转述） | 每次本题使用写 application；条件/量词改变后定向重审 |
| CoCo-Prover 附录 B/E（机制转述） | 全子义务 AND、替代 OR、provisional 与稳定证据分开；不照搬 Lean 的 closure 判据 |

这些工程选择是本仓设计，不是上游作者对本仓数学或实现的背书。
