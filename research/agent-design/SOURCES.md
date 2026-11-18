# 设计来源、实际借入字节与运行边界

核查日期：2026-11-16（America/Los_Angeles）；研究窗口：2026-09-01 至 2026-11-16。仓库审计基线为 `rebuild/research-v2@3e8402cabac61aadc5575d797671bfa0d183324e`。[架构审计](ARCHITECTURE_AUDIT.md)说明来源怎样接到已有仓库。

实际借入的是 **3 份参考合同，共 36,587 字节**，另有 LICENSE/NOTICE 共 23,467 字节。没有安装 Ansatz、CoCo-Prover、PACE、Euler 或 OSVerify 的研究运行时。保存在 `upstream/` 的合同不是活动指令；本库程序不读取它们来调度、接纳证明或写图。

## 2026-09-01 以后的一手核查

| 来源与版本 | 可核的机制 | 本库取用 | 证据边界 |
| --- | --- | --- | --- |
| Ansatz / Continual Graph Memory：[arXiv v2](https://arxiv.org/abs/2610.02945v2)，首发 10-02、修订 11-06；[官方仓库](https://github.com/uclanlp/continual-graph-memory)；参考合同固定 `23367c6568c344d9c4dbf59be3f39b39f5d54324` | 已接纳事实与探索状态分开，按依赖取证；curator 合同要求 AND 全部闭合、localization 的 reassembly 与 reduction 的 bridge | 取完整前提、失败和未付前沿；按需实读由 worker 完成，Work 的 idea 子代理承担策略咨询。原文 curator/verifier 作为参考 | v2 报两批各九项 local-verifier closure，第二批另有 partial 按研究准则计 pass；模型评定与专家确认不同。不能沿用 v1 的 10/10 解题宣传；09-26 的合同快照不等于 11-06 全部实验的精确部署版本 |
| CoCo-Prover：[论文 v1 / 附录 B、E](https://arxiv.org/html/2610.09681v1)，10-07 | 声明内 AND/OR proof hypergraph、声明间 lemma DAG；Lean 返回完整子目标；provisional 可探索，stable 要求 kernel 接受和依赖 stable；失效只回滚相关依赖 | 用完整联合义务与独立替代分支解释本库已有 ALL/OR；临时探索与可采用结果分开 | soundness 相对于明确 Lean 环境和禁止占位公理等前提；本库自然语言审查没有这一保证。五项程序验证基准不等于一般开放数学；未核实公开完整代码/许可证，不复制其工程或附录提示词 |
| PACE：[官方 arXiv 记录](https://arxiv.org/abs/2610.33690)，10-24 | 摘要可核：机制构造、whole prover、独立 verifier；候选或条件改变时重审证据，区分已核前提、探索材料和未付义务 | 本题应用范围/条件变化触发定向重审，保留旧引理本体；不允许改弱用户原题来闭合 | 本次官方摘要检索可得，abs/html/pdf 直接读取均返回 DisabledError，故不声称本次重读附录 E/F/G。未核到可安装代码和许可；不把 Trace231/ProofLoom 当 PACE 仓库，不借其基准分数保证本库增益 |
| Euler：[论文 v1](https://arxiv.org/html/2610.19864v1)，10-14；[官方架构](https://github.com/canghaimeng/Euler/blob/main/ARCHITECTURE.md)、[许可](https://github.com/canghaimeng/Euler/blob/main/LICENSE) | 原题合同、Obligation/Route、范围化证据、依赖上下文和长期恢复；路线除全部 premises 还保 closing implication | 用现有 spec/RUN 保存原题与研究线；联合应用另写本题合成桥，不由前提分别成立默认合成 | 工程为 PolyForm Noncommercial 1.0.0，本轮未复制代码。论文案例与当前 main 不是同一精确版本；不能把案例、人工参与、形式化和当前控制器的贡献混为自主解题证明。main 架构链接只作阅读入口 |
| OSVerify：[论文 v2](https://arxiv.org/abs/2610.18089)，首发 10-13、修订 10-22；[官方 README](https://github.com/OSVerify/OSVerify)；policy 固定 `c43385bcbedec943cabe0d7e95df5b50404d9acb` | 错误提出与验证分开；反馈逐字审计；保原始输入和范围；部分进展不因未解全题被判错 | 承重交付按需独立挑战，具体问题回原作者；confirmed/not_real/unresolved 分开，审查绑定准确字节 | READY_FOR_HUMAN 交人确认；partial PASS 允许继续，均不认证正确。本库未运行上游 OSVerify engine；本轮自行实现冻结字节与 review 版本绑定，仍不验证证明语义 |

### 实际读图与派工

Ansatz 先查找简短声明、事实 ID 和图路径，按需取所选事实的先决依赖，再单独打开完整证明和证据。Main 的原合同把数学证明交给 worker，并在真正的新进展或阻塞触发独立策略咨询。新 worker 会话按任务和持久记录恢复。这三项分别见 [论文 §2.1、§2.3、§9.6](https://arxiv.org/html/2610.02945v2)、[固定版本 Main 合同](https://github.com/uclanlp/continual-graph-memory/blob/23367c6568c344d9c4dbf59be3f39b39f5d54324/CLAUDE.md) 和 [consult 合同](https://github.com/uclanlp/continual-graph-memory/blob/23367c6568c344d9c4dbf59be3f39b39f5d54324/.claude/skills/consult/SKILL.md)。

当前流程用本仓的 search/context/show 和 Git 版本实现按需读取及接续。Main 按用户要求只取超边和短回执。Work idea 子代理承担策略咨询，另一个子代理执行与取证，原独立障碍槽保原输入。见 [HYPEREDGE_WORKFLOW](HYPEREDGE_WORKFLOW.md)。

## 原样保留的实物

以下 6 项逐文件重算原始字节数与 SHA256，全部匹配相邻 `provenance.json`。两份 manifest 均声明 `modified=false`，给出固定 commit 的原始 URL。本次这些固定 URL 被检索器拒绝，**结果是本地字节与既存 provenance 一致，不是再次远端下载比对**。

| 本地文件（相对于 `research/agent-design/upstream/`） | 上游路径 | 字节 | SHA256 |
| --- | --- | ---: | --- |
| `ansatz-23367c6/curator.md` | `agents/contracts/curator.md` | 6,857 | `d87a48ea715d0ba3e19618692fa6d5562993f2ec7e2e176550b53b54cf2d7783` |
| `ansatz-23367c6/verifier.md` | `agents/contracts/verifier.md` | 13,180 | `b677d7fba8f8528cfdd6e9d36e817ca972831aed50093973e56948c21ebc1a3e` |
| `ansatz-23367c6/LICENSE` | `LICENSE`，Apache-2.0 | 11,340 | `d51dbb6676bff13e23abd800608ec96bd6e637fd5b5194ef9ea8d848416d8ef3` |
| `osverify-c43385b/policy.md` | `src/osverifier/skills/policy.md` | 16,550 | `fe3080890a6ae335e91adc43a1951189647d33a25cb8d8cced90a47f43136ecc` |
| `osverify-c43385b/LICENSE` | `LICENSE`，Apache-2.0 | 11,357 | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` |
| `osverify-c43385b/NOTICE.md` | `NOTICE.md` | 770 | `bb0e58607b31d03cd1d29aa77b5f0966716ce23a58543e9c81980c530bfe0a19` |

总计 60,054 字节。准确来源 URL 和 commit 见 [Ansatz provenance](upstream/ansatz-23367c6/provenance.json)、[OSVerify provenance](upstream/osverify-c43385b/provenance.json)。OSVerify NOTICE 保留 shared policy 对 Rethlas `887cc46427636bbdd235160a112f9a30ae81d040` 的改写归属；本库未把那些 skills 注册为活动工具。

本库使用自身的 Git 与 RUN 权限，实际活动词见 [research-runtime](../../prompts/research-runtime.md)。上游 curator、fact_submit 服务和 OSVerify release gate 属于各自运行时。

## 思想适配与本库实现

| 类别 | 实物 | 准确归属 |
| --- | --- | --- |
| 原样参考数据 | 上表合同和许可/NOTICE | 外部原文；不是被 import 的组件或已启动代理 |
| 机制适配 | 本库 Main/Solver/review 词，HYPEREDGE_WORKFLOW 的原题映射、bridge、复核、回流 | 本库编写，借鉴上表局部机制；不是安装上游提示词包 |
| 已有本库实现 | `research_runtime.py` 的 registry/context/packet/init/save/resume；`registration.py`、`map_tasks.py` | 本轮之前已有；不把稳定 ID、完整 ALL/OR、SHA 绑定和 RUN 续接记成本轮新增 |
| 本轮本库实现 | `research_frontier.py` 的条件结构闭包、循环与贡献报告；studio 薄接口 | 复用现有 JSON/Markdown 独立编写，未复制上述项目 Python 运行时。“本库实现”是工程归属，不宣称通用思想具有研究新颖性 |

引用检查没有发现从 `agent-design/upstream/` 读合同、调用 `cgm`、`euler` 或 `osverify` 的运行路径。`work.py → research_runtime.py → research_frontier.py` 使用标准库及本库模块；模型由 Work 实际工具启动。

## 历史适配仍须如实说明

[tools/vendor/UPSTREAM.md](../../tools/vendor/UPSTREAM.md) 是历史来源记录，不属于本次窗口的新证据。“本轮没装外部运行时”不等于仓库没有第三方代码。

| 历史实物 | 固定来源与许可 | 当前关系 |
| --- | --- | --- |
| `tools/vendor/matek/frontmatter.py`，4,312 字节，SHA256 `bbe2434384171146e50be431d0915c8f6d6f9b05190ec4e21d16d05c590907db` | [MATEK](https://github.com/PhillipKerger/matek-theorem-agent) `1de478c12f34fc1adea32bbc3f0c5aadadfd6ca5`，MIT；本库提取/修改 flat frontmatter，非整文件原样复制 | `research_runtime → curation → vendor.matek.frontmatter` 为实际间接依赖；未引入 MATEK Agent/Pydantic runtime |
| `tools/vendor/mathagent/model.py`，8,607 字节，SHA256 `e72a5f7ce23622b50155af8d83f26166a5779f651fd972ba165b8acc213d8ae7` | 目录有 Apache-2.0 LICENSE；历史记录指 [math-agent](https://github.com/Ephemeral6/math-agent) `3a161e1f6ced822c340b9e23c0ada2a4b82dbdbe`，缺逐文件 provenance | 全树 Python 引用检查未发现 import/调用；仍在树内的闲置模型。缺凭据时不能称其为该 commit 原样源码。`compute.py` 的 `tools/vendor/**` 和 tools 整包导出仍可能携带它；本次不擅自删除历史归属 |

早期 HyperGraphRAG、GraphRAG、Pharos 的来源在 [UPSTREAM_ADAPTATION](../UPSTREAM_ADAPTATION.md)，不充当本窗口新证据。此前列出的 ProofLoom、Noemesis、LEVER 等仅保补充阅读地位；本次核心适配限于上表可核五项，不把未重核创建日期、许可或成果数写成已完成审计。

可检查的工程性质是版本可定位、ALL 不丢成员、open 环不自付、贡献保 remaining、反馈绑定准确字节、远端保存有实际 pushed 证据。数学正确性、研究线的实质独立性、最优派工、吞吐增益和最终突破，要由真实研究记录分别判断；单测、提示词和模型同意均不能代替。
