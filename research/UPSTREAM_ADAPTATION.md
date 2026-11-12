# 数学超边与研究Agent的一手依据

采用下列论文或官方代码中可核对的具体做法，落实到[构图指令](../prompts/03-map-worker.md)和[研究流程](RESEARCH_WORKFLOW.md)。这些做法支持发现、组织和取用数学材料；边是否成立仍由完整条件与论证决定。

| 一手位置 | 作者实际提示词或机制 | 本仓库采用处 | 数学上不能直接迁移处 |
|---|---|---|---|
| [HyperGraphRAG论文](https://proceedings.neurips.cc/paper_files/paper/2025/file/df55ee6e59f8ac4a625219e11fe9ddba-Paper-Conference.pdf)，附录A.1图8、§4.3；[官方代码](https://github.com/LHRLAB/HyperGraphRAG) | 实际抽取prompt先写完整知识片段，再列片段中的实体；检索从实体或关系双向展开，保留整条关系成员与来源片段 | Mapper先发现候选联系，实读整条陈述；研究context保留命中边的全部前提、结论、条件及出处 | 无向多元事实不等于有向联合蕴涵；完整度、关联分数不证明定理 |
| [Microsoft GraphRAG抽取prompt](https://github.com/microsoft/graphrag/blob/main/packages/graphrag/graphrag/prompts/index/extract_graph.py)，`GRAPH_EXTRACTION_PROMPT`；[官方手调说明](https://github.com/microsoft/graphrag/blob/main/docs/prompt_tuning/manual_prompt_tuning.md)，Entity/Relationship Extraction | 列实体后抽取有明确关系的实体对，并写关系说明；官方支持按领域改prompt及示例 | 给Mapper真实数学联合推导示例，要求说明每项前提提供什么、如何得到结论 | 人名/组织分类、两两相关和强度不能代替数学对象、量词与承重理由 |
| [Stewart–Buehler预印本](https://arxiv.org/html/2601.04878v1)，§§2.1.1—2.1.3、4.2、4.4；[官方代码](https://github.com/lamm-mit/HyperGraphReasoning) | `Event`保留多项source/target及relation；段落溯源、局部到全局整合，按成员索引取完整边；另用语义相似度合并节点 | 由对象内到存档内再到跨存档构图，写完整端点、推理和来源；相似文本用于找候选重复 | 不按相似度或节点度自动合并命题；同名但模型、量词、背景不同者分别保留；图上短路不是证明 |
| [MACE预印本](https://arxiv.org/pdf/2609.21533)，§3、附录D及F.2/F.4；[MAGE预印本](https://arxiv.org/pdf/2608.29678)，附录B.2/B.3、表5及[官方代码](https://github.com/Githubuseryf/MAGE) | MACE按任务提供保有条件、行动、输出的功能单元并收集实际反馈；MAGE整包交付多元证据、成员和出处，按角色与版本取用 | Main给当前目标需要的完整数学包；Solver返回实际使用处、未满足条件或具体失败，Main据此继续原任务或定向修复 | 记忆层不替代Boss分工与Git协调；不把所有消息、角色和旧日志塞进数学图，不把执行分数当真值 |
| Pharos既有固定版本：`aa0b72e4a7211311a3156ef7d993cd3be9f57445`；[query-memory](https://github.com/frenzymath/Pharos/blob/aa0b72e4a7211311a3156ef7d993cd3be9f57445/agents/skills/worker/query-memory/SKILL.md)、[gateway](https://github.com/frenzymath/Pharos/blob/aa0b72e4a7211311a3156ef7d993cd3be9f57445/pharos/gateway/server.py)、[schema](https://github.com/frenzymath/Pharos/blob/aa0b72e4a7211311a3156ef7d993cd3be9f57445/pharos/core/schema.py)、[factgraph](https://github.com/frenzymath/Pharos/blob/aa0b72e4a7211311a3156ef7d993cd3be9f57445/pharos/core/factgraph.py)、[checkpoint](https://github.com/frenzymath/Pharos/blob/aa0b72e4a7211311a3156ef7d993cd3be9f57445/agents/skills/main/operation/checkpoint/SKILL.md) | 先搜陈述，再按需取正文/证明；Fact携带前驱及引用；支持后继查询、撤回与当前研究状态恢复 | search→show/context；稳定object_id与version分开；完整all边；packet、反馈与continuation保存可恢复研究 | 版本检查不等于证明；来源更新要求复核相关边，不自动断言所有后继为假；保留有实质内容的对象，不逐算式原子化 |

构图时直接追问：结论是什么？各项承重前提分别提供什么？它们怎样共同推出结论？哪些条件尚未满足？共同模型、记号和普通定义放入`conditions`与正文入口，不因“用了这个定义”就给整档结果各造一条定义边。候选联系可以保留为`proposed`并写出缺口；研究时须显式辨别其用途。

## 本库实例：末两人保底如何接到一般福利界

1. **发现候选联系。** [末两人定理](../archives/customer-attraction/state/定理/末两人逐人保底与全人数弱福利界--定理.md)§1—2给两个末位玩家各自的收益保底；[目录计数界](../archives/customer-attraction/state/引理/末位最坏背景值与目录计数界--引理.md)§2—3给前缀嵌入和同一$\theta_n$的两个下界。它们可能共同导出前一正文§3的全人数福利界。
2. **读全条件。** 核对[共同模型](../archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md)：有限单位客户、有限非空共同标签目录、$n\ge2$、每份全部有序历史上的纯SPE及任意平局。$K=\max_A|A|$、$O=\mathrm{OPT}_n$；根福利才等于全体收益和。合法前缀嵌入保证末两人保底可降到同一个$\theta_n(0)$。
3. **写定向all边。** 前提A为末两人逐人保底，B为最坏背景值及目录计数接口（$\theta_n\ge O/(2n-1)$及$\theta_n\ge[2O-(n-1)K]/(2n)$），结论C为$W\ge4(n-1)O/[n(2n-1)]$。理由写明：早位玩家各有$K/n$真实偏离保证，所以$W\ge(n-2)K/n+2\theta_n$；代入B的两个下界，按$1/(n-1)$、$(n-2)/(n-1)$加权消去$K$。$n=2$时第二权重为零。A和B共同使用，不能拆成各自单独推出C的两条边。共同模型列`conditions`；准确证明位置为末两人正文§2—3。A与C是同页不同陈述，须由2.5.3分别登记后引用，不能把整页ID接回自身。
4. **研究消费。** Solver要用C时同时读取A、B、共同条件和这段论证；六人代入只得$10/33$。若目标为六人半覆盖，反馈应准确说明此接口还缺提高系数的论证，继续寻找有用桥接，而不能把“相连”报成目标已证。若B改变模型或背景，先复核该all边的适用性。

Boss编号、公屏、共同分支、持续补位与频繁Git保存按本项目约定执行。这里不引入新服务、数据库或依赖。Pharos固定版本的[README](https://github.com/frenzymath/Pharos/blob/aa0b72e4a7211311a3156ef7d993cd3be9f57445/README.md)标注Preview、软件许可为Apache-2.0；本页为机制转述，未复制上游源码或提示词正文，已有vendored依赖的LICENSE/UPSTREAM继续保留。

## 研究运行中实际复用的实现

- **Noemesis。** 在固定版本运行真实引理的定向证据包和分段恢复，并从原入口重跑 ENS-lifting 有限域检查。46 个实例与 26,988 项乘子检查通过。它把当前研究状态、按需打开的原证和计算回执分开保存。我们分别沿用 `research resume/save`、`research context` 和 `research compute`，交接长度由当前数学义务决定。[实跑版本](https://github.com/kbr-/math-research/tree/25239211058ef718402a908b3272f01480c159c4)
- **Ansatz。** 将真实的两人税、PAIR O 加强、原五尾证书和合成结论写入上游 FactGraph。检索找到了加强结论，正向可取合成所需的两个前提，反向可查旧引理的后继。我们的超边保留联合前提和替代证明。发现一条旧证明失效时，定向复核受影响的边，并检查其他仍成立的证明。[FactGraph 固定源码](https://github.com/uclanlp/continual-graph-memory/blob/23367c6568c344d9c4dbf59be3f39b39f5d54324/cgm/core/factgraph.py)
- **Station。** 公开研究轨迹显示构造经共享结果档案被下一位研究者接到新参数族。借这种证据交接组织公屏。数学放在可直接取用的正文和证明，公屏发可复用结果、决定性障碍及影响别人的更正。[真实协作轨迹](https://arxiv.org/html/2608.23691v2)

## 研究运行职责的具体适配

下表来自实际源码及角色词，不把上游成功当本仓已验收。行为已接到现行Main、solver-full与RESEARCH_WORKFLOW；既有ALL/OR语义保留，不增数据库、检索器或常驻审批岗位。

| 固定源码 | 本仓采用的行为 | 适配边界 |
| --- | --- | --- |
| Ansatz [verifier合同](https://github.com/uclanlp/continual-graph-memory/blob/23367c6568c344d9c4dbf59be3f39b39f5d54324/agents/contracts/verifier.md)与[gateway](https://github.com/uclanlp/continual-graph-memory/blob/23367c6568c344d9c4dbf59be3f39b39f5d54324/cgm/gateway/server.py) | 对新的承重命题主动独立检查准确陈述、完整推导、前提及外引适用性；错误与缺口分别给位置、原因和影响，交原研究者修后回查 | 不把作者自审或代理同意当证明；已核且版本/用法一致的支持复用，不每步设审批 |
| Station [coder_manager](https://github.com/dualverse-ai/station/blob/f2603c817694145610b4a1057eeee7fb6f31d516/station/eval_research/coder_manager.py)的_build_audit_prompt、_handle_audit_verdict | 对关键计算合读原义务、脚本、输入、实际输出与报告；查遗漏case、伪穷尽、错误剪枝、超时冒作完成，错误须修代码/证据再核 | 如实未完成可保存，不因未提高数字判失败；Main无需再全量重复独立核验 |
| Ansatz [identify-key-failures](https://github.com/uclanlp/continual-graph-memory/blob/23367c6568c344d9c4dbf59be3f39b39f5d54324/agents/skills/worker/identify-key-failures/SKILL.md)；Station [Exploration/Revival](https://github.com/dualverse-ai/station/blob/f2603c817694145610b4a1057eeee7fb6f31d516/station/constants.py) | 重复同一障碍时综合失败范围、最强近成功与未探索部分，重提数学分解或表示；说明新路线逃出什么旧限制、什么证据会改变判断 | 不照搬按分数tick计时的阈值、固定配比或排行榜；不把加参数与算量冒作新机制 |
| Ansatz [FactGraph撤回](https://github.com/uclanlp/continual-graph-memory/blob/23367c6568c344d9c4dbf59be3f39b39f5d54324/cgm/core/factgraph.py) | 失败支持定向停用，更正送达实际消费者，接收者在原推导撤用或重证 | 上游按DAG全后继撤回不能直接照搬；本仓保独立OR支持，无有效支持恢复待证而非判假 |

本次设计反驳可检验职责、输入和失败处置是否自洽；档内公屏与发现路由可由现有RUN核验。真正跨Pro接用、机动调度收益及新版长线实战仍须留下实际研究证据，不能以文档或代码检查通过代替。
