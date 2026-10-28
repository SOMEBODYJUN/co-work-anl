# 本轮清洗：先建立地基，再整理数学

当前任务 `repository-cleanup`。文件分支 `cleanup/research-foundation-20261028`，初建于 `8ca370ad`，发布前已吸收远端 `1caf781a`；新公屏 `wcg/board-cleanup-20261028`，线程 `repository-cleanup-20261028`。数学研究当前主目标 **Q-CAG-HALF-6**，原存档 `customer-attraction`；状态仍 **OPEN**。用户另行让 Pro 做两次求解，本轮不规定其方法。

## 已做与待做

- 地基已checkpoint推送，首个提交 `6dd9897c0dc37c778db771e23fb614ff24cb693c`；新版根work.py已从全新独立clone实际start成功，返回正确文件分支、新公屏和清洗入口。原clone未提交工作保留；未知临时文件未清掉。
- 地基改动：根 work.py 支持明确文件分支、公屏分支、全仓清洗存档；checkpoint 回执与资产描述使用实际分支，首次发布需显式授权参数；main、其他存档和旧身份仍隔离。
- 协作结构：Boss 带内部 Solver；所有 Solver 可访问全部材料和工具，自由研究同一完整目标。撤回此前协调者擅加的“结构优先/暂停LP”要求；不强制拓扑、LP、形式化或任何数学路线。
- 后续清洗：读懂并合并数学正文，删重复与无用过程，重写旧启动词，退役冗余索引及其强制检查，清理各主题入口。以下范围是可并行清洗的工作面，不是数学研究路线。

## 清洗分工如何加入

地基由本对话协调者负责。其余对话按下面互不重叠的范围在公屏认领；有多少人就开多少个实际有工作的范围，无需凑十个。每人仍可访问全仓，认领只限定写入范围，避免互相覆盖。

| 可认领范围 | 主要文件 | 应交付内容 |
| --- | --- | --- |
| 客户吸引正式数学 | research/current/customer_attraction/、本题问题与审查 | 准确定义、已证范围、开放缺口与自足正文；吸收独有结果后删除重复 |
| 客户吸引未成熟研究 | research/workspaces/customer-attraction/ | 按数学对象抽取有接续价值的猜想、片段、反证和证据；没有独有信息的旧流水删除 |
| 其他研究模型 | unrelated_machines、weighted_congestion、设施与positive_kernels的各自目录 | 每个模型独立入口与正文，明确暂停/开放/已证，不被六人目标覆盖 |
| 代码与证据 | customer_attraction/、facility_spe/、multi_facility_spe/、tests/、examples/、evidence/ | 保留确有数学作用的实现、真实输入和复现实例，去掉冗余输出和失效测试 |
| 旧规则与派生登记 | 旧提示词、catalog/assets/graph/crosswalk及生成检查脚本、design/ | 提出并实施可删除的整套冗余依赖；根入口统一交协调者整合 |
| 学习与写作材料 | learning/、稿件、相应history来源 | 保留独有解释、来源与稿件，修正范围混淆和断链 |

大范围可按数学对象进一步拆开。不要同时改根 README、AGENTS 或同一主题启动页；把相应修改点交协调者一次整合。公屏交流新的判断、具体冲突和可接续的想法，个人局部工作自行完成。

## 留、合、删的准则

**留下的是内容。** 精确结论、证明关键步、严格反例、有效条件、真实失败机制、有价值但未完成的 idea、必要代码/输入/证据都可保留。未入库的内容允许继续研究和保存；不能因未证或未登记而删掉。

**合并必须吸收独有信息。** 同一个命题的独立证明、纠错、关键假设或不同反例可能各有价值。不能只留下短摘要丢掉承重数学；也不再保存几十份相同摘要。正式入库意味着有自足、可接续的正文和准确状态，不意味着每项都必须是已证定理。

**删除已无用途的工作树文件。** 重复扫描、完整吸收后的旧副本、失效提示词、无信息状态播报和不再使用的派生JSON可以删；先检查真实引用和生产/消费代码，再一起删依赖。Git提供旧版本恢复，避免另建一套臃肿归档。未知的未跟踪文件先确认来源与内容。

**一个主题一个启动入口。** README含题目、准确现况和有用内容的直接链接，按发生的实质变化替换对应段落。长证明、证据和未成熟研究仍有各自文件；“只更新一个入口”不等于把全仓压成一个长文件。底层程序所需JSON可留，冗余导航JSON不再强制维护。

**检查与改动相称。** 改程序跑相关真实行为测试；改证明检查相应推导；迁移文件检查实际引用和复现依赖。没有数学变化就不升级Claim，没有必要就不跑全仓数值枚举。清洗过程中不能用“检查通过”代替数学理解。

## 已实际下载并读代码的开源项目

这些是可复用来源，不是“本题效率最高”的已测排名，也没有把仓库宣传分数当作独立证据。

| 项目与固定版本 | 实际读过的实现 | 本轮判断 |
| --- | --- | --- |
| [QED](https://github.com/proofQED/QED/tree/bf91aaf8daa763281bdf0dafb46457fc794c11a5)，MIT | code/model_runner.py、code/decomposition_prover.py、single_prover/regulator提示词、config.yaml | 自然语言全题prover、工具CLI和证明修改/改计划的分支可借鉴；其多阶段持续验证、固定重试、情绪施压和默认绕过沙箱不照搬。不是原样部署。 |
| [OpenProver](https://github.com/Kripner/openprover/tree/e200251b34349ab6c34548d30319abde86cb6bc6)，MIT | openprover/prover.py的Repo/WHITEBOARD/worker调度、prompts.py、pyproject.toml | 精简白板、内容增改删和续接有参考价值；worker被限制只看任务上下文、单问题拆分和默认验证不符合用户所需的完整自由Solver，不能声称只适配接口就满足要求。 |
| [ResearchMathAgent](https://github.com/sjtuytc/ResearchMathAgent/tree/d1fe055ea6f32a5b7e9efddc288e6bfbd25bb86a) | rma/store.py、rma/ops/solver.py、pyproject.toml | 可参考局部修改保留已正确内容；此版本未发现许可证文件，暂不复制代码。其复杂共享状态不作为当前目录重构目标。 |

三个项目均已在仓库外独立clone，不自动执行其脚本或注入其默认提示词。当前执行环境未安装codex/claude/gemini CLI，也没有lean/lake；因此没有声称外部框架已能在当前对话中实跑。现有对话与subagent通道继续使用；外部CLI/API适配应在实际有该接口的宿主做一次端到端验证后才采用。用户指定模型与推理强度不随上游默认值改变。

清洗原则另参考：[ACE论文](https://arxiv.org/abs/2510.04618)的局部增量更新，避免反复摘要抹掉细节；[SimpleMem论文](https://proceedings.mlr.press/v306/liu26dx.html)的合并冗余、按需取上下文；[ReasoningBank](https://github.com/google-research/reasoning-bank)同时从成功与失败提取经验。它们没有提供数学仓库清洗的通用标准，也没有证明对本题有效。本轮只借用适用原则，不另装记忆数据库，不机械复制它们的角色编制。

## 地基验收与后续边界

验收需包含真实本地Git远端测试：新clone加入清洗分支、两clone互相同步、脏文件保留、checkpoint不触main、实际分支资产引用、旧存档隔离、新旧公屏隔离与远端确认。通过后发布新版work.py及加入方式，再让清洗者接入。

地基程序测试已完成：`test_work.py` 32项、`test_checkpoint.py` 45项、`test_board.py` 22项，共99项通过；旧入口导航检查通过。它们验证程序行为，不证明任何新的数学命题。程序仍从旧tools路径兼容调用，移动此路径与退役旧索引留到依赖清洗时一起处理。

Pro新增结果从main或实际交付位置导入，逐条核数学而非自动并入本轮现况。清洗分支的最终合入main在所有实际冲突和证据依赖处理后进行；本轮基础设施发布不代表全仓数学清洗已完成。
