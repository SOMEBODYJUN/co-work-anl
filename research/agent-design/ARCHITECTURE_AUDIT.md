# 本库机制、缺口与最小适配审计

本轮复核基线：`rebuild/research-v2@e0ad3a26e5234197ad38e08c8ceafd429fd766f1`；早期审计基线为 `3e8402c`；日期：2026-11-16（America/Los_Angeles）。本页依据实际代码、入口、登记和两项真实超边写成，外部来源与字节核查在 [SOURCES](SOURCES.md)，共同数学合同只在 [HYPEREDGE_WORKFLOW](HYPEREDGE_WORKFLOW.md)维护。

上版的主要问题是**把已具备的机制重新介绍为新设计，文档合同比可执行入口多，且没有把本题应用与普通笔记接成明确操作**。本库已有研究保存、版本绑定、完整 ALL/OR 和回流链；无需另建知识图、数据库、模型服务或每步工单。应补的是现有链上的少量接口和实际验收。

## 读了什么，没读什么

基线 Git 树枚举有 94,715 个 tracked 文件，其中 `archives/` 40,554、`research/workspaces/` 8,333、`research/runs/` 576、`map/edges/` 4,135。`registry.json` 当前列 3,821 个对象、5,137 项材料、2,673 个现役边文件、2,610 个不同 body 路径。物理边文件数不等于现役边数，state 文件数也不等于独立命题数。

这些是树和登记元数据检查，**不是读完全部数学正文**。本次实读范围是仓库规则与研究入口、IMPLEMENTATION/RESEARCH_WORKFLOW、agent-design 全部核心说明及借入合同、runtime/frontier 的读取/保存/检查路径、registration 的准备与校验入口、map_tasks 的阶段边界、vendor 实际引用，以及下面两页数学和两条边的完整声明。其余数学以需要时精确取证；不以“看过目录/registry”冒称全仓证明审查。

直接核对的数学正文：

- `archives/customer-attraction/state/候选/全槽逐行最小价格的共同预算与有限报告--候选.md`
- `archives/customer-attraction/state/引理/完整槽末位最小价格的精确折扣与静态充分桥--引理.md`

直接核对的真实边：

- `map/edges/boss3-uniform-summin-identity-3b-3313f41b4a46c9dc/uniform-summin-equivalence.json`
- `map/edges/boss5-summin-all-spe-3b-7383c8bf44f753cc/all-spe-summin-budget.json`

本审计没有重证这两条边的每份附件，没有重跑 LP、SPE/IC 或原数学计算。源码阅读和运行测试分开记录；旧 validation.json 只证明其列明的旧版本检查。

## 已有机制 → 真实缺口 → 最小补齐

| 本库原有机制与路径 | 真实缺口 | 最小补齐 | 对应外部设计 | 不能保证 |
| --- | --- | --- | --- | --- |
| `research_runtime.packet/init_run/update_run/resume` 已有原题 pin、不可变 packet、笔记快照、事件链、未答反馈、实际 agent_id/config | 上版文档要求固定三线，但普通 init 仍是空 roster 的 open；文件生成与真实 Work 派工容易混称 | 用现有 RUN 增加固定线路入口和当前位置索引；调用实际 spawn/followup，再 save 真实 ID；恢复继续原输入，不复制第二套会话事实 | Ansatz/Euler 的持续状态；本库原来已有大部分 | 文件里有 ID 不证明代理在线；恢复资料不证明平台会话可复活 |
| `context` 已按目标递归保全部支持前提，选项间 OR、每项 ALL；hops 不截承重闭包；等价保双向、反驳/贡献分列 | 获取到图不能说明下一项本题义务；没有把采用桥写成实际本题结果 | `frontier` 做只读结构报告；采用时保存模型/变量/量词对应、逐前提证据、closing implication 和剩余 | Ansatz 的 AND/bridge；CoCo 的完整子目标；Euler 的 closing implication | 结构闭包假设自由文本条件成立；不做自然语言数学判定 |
| `registry` 稳定 object_id/version，body/evidence 的 path/SHA/唯一 section；`edge_bindings` 固定 endpoint/evidence/review digest | 全局对象仍真但对新问题的应用可能失效；只查全文 SHA 不能证明应用可用 | 本 RUN 的采用记录固定 spec、对象/边 pin，保存具体映射、条件付款及上游采用 revision；变更只重开相关使用 | PACE 的适用性重审 | pin 相同只说明字节/记录相同，不说明量词匹配或论证正确 |
| 已有 conditional、whole_result 与 contribution.result/remaining 的明确区分 | 条件结果接续时可能通过摘要、换代理或换名丢未付债务 | 本题沿应用依赖继承全部未付前提/条件/bridge；只有给明确 discharge 才移除 | CoCo provisional/stable 的分离，Ansatz 的联合闭合 | 自然语言的“已付”仍须实质复核；不能照搬 Lean kernel 的 stable 等级 |
| `save` 已冻结笔记字节，反馈可 pending/ack，`checkpoint` 可串行 Git 发布 | 审过旧版、发布新版可能被写成同一次通过；只冻结摘要不足 | 只对承重成果记录准确 body/evidence refs 与 review；冻结覆盖应用及新增证明，发布前比已审字节，变更部分重审；普通草稿仍连续编辑 | OSVerify 的原始输入和精确反馈思想 | 未运行上游 OSVerify engine；本轮自实现冻结与 review 字节绑定仍不能验证证明语义，独立模型也会漏错、误报 |
| `registration.validate_batch/compose/register` 和 `edge-check/edge-bind/build` 已有增量回流链 | 上版只写“成熟后回流”，没有让某项成果明确交出正文/对象/边准备结果 | 用本 RUN 的 backflow plan 指向已有正文、batch、edge 文件，复用校验并明确谁完成 compose/register/检查/推送；不再造第二 registry | 本库已有机制；外部仅启发持久复用 | 合法 JSON、SHA 和登记通过均不认证数学；plan 不等于已入现役总表 |
| `work.py` 已有 Git 锁、checkpoint、远端确认；阶段 CAS 队列仅登记/构图 | 容易把 Main 的 Git 串行扩大成 Main 独占全部证明核验，或把研究每步套批任务 | 研究者直接完成实质正文/证明与定向挑战；Main 核综合接口、串行发布；普通研究不进入 map-v2 claim/done | 本库工作规则；无需外部框架 | Git 串行只避免并发写冲突，不是数学审查或调度最优性 |

表中的最小补齐是将原链可操作化，不是重做登记或构图阶段。机器只适合强制 ID、覆盖成员、依赖引用和版本这些可判断合同；数学条件仍由实读推导负责。

本轮 `tools/research_studio.py` 已将这些合同接到现有 RUN：ALL 绑定逐成员核对，显式应用依赖递归核 revision/未付债务并拒自证环；`target_remaining` 另行继承，不阻止已完成局部结果回流，whole-target 则须给已冻结复核的 `target_discharges`。freeze 自动收纳采用记录、上游采用记录和各新增前提/条件/bridge/discharge 的 proof refs；review 必须列出该批准确字节。非批准意见须由准确绑定的后续审查解释解决，不能挑一份旧 approve 绕过。后续操作复核 opening branch/remote，候选总表只写本 plan 专用目录；现役 registry 基线改变由 register 的 guard 拒绝覆盖。这些都是声明与字节的检查，不能发现证明中未声明的隐含依赖，也不能认证真实代理独立性。

## 工作室、RUN、state、registry 与 hyperedge 的边界

| 层 | 保存什么 | 不承担什么 |
| --- | --- | --- |
| 工作室 / `research/workspaces/<RUN>/` | 当前原题、定义、Main/三线连续笔记、应用和审查；`main/independent/informed-a/informed-b` 是研究线身份 | 不是另一个知识库、队列或平台进程管理器；临时算术不逐句变节点 |
| RUN / `research/runs/<RUN>/` | 不可变输入、真实派工记录、events/笔记快照、当前未答反馈与恢复位置；studio 如有 index，只定位这些实物 | 不以 closed/paused 等运行状态替代数学 truth_status；不复制原有保存链 |
| 正式正文 / `archives/.../state/` | 可复用数学的完整陈述、证明、范围、开放部分或精确失败，必要附件有 owner | “进入 state”不等于已证；这里可以准确保存 conditional/open/finite |
| 登记 / `research/registry.json` | 精确对象身份与 version、状态、条件、完整 body/evidence 字节定位；材料的去向/owner | 不把每页自动当一对象，不用一个摘要代替证明，不从保存成功自动升 proved |
| 超边 / registry 所列 `map/edges/` | 对象之间有数学作用的完整联合关系、条件、各端角色、论证、证据及版本 | 不为连通造边，不把一次普通使用/通信/计算日志都变全局关系 |
| 投影 / `map/graph-v2.json` 等 | 可重建导航和展示 | 不是第二数学真值来源 |

“工作室”是使用现有文件和 RUN 的操作视图。可以为恢复、采用和回流加薄索引，不能让索引另存一份证明状态后反向覆盖 registry。共同定义直接引用正文；只有独立复用的数学陈述才需对象 ID。

## 中间结果什么时候保存，什么时候入库成边

| 时点/成果 | 立即动作 | 何时成为正式对象/边 |
| --- | --- | --- |
| 新推导、候选、失败、计算或下一步已有接续价值 | 更新所属研究线连续笔记；用现有 save 冻结关键接续，Main checkpoint；标真实状态和未付处 | 不要求先审完或先登记才保存 |
| 普通代入、算术、改写或一次有限数值点 | 保在同一论证/证据段，说明实际用途 | 没有独立复用作用时不单造对象、节点、工单 |
| 承重局部引理、完整条件推导、精确反例、决定性计算 | 冻结准确陈述/证明/输入输出；未参与作者论证者按范围挑战；问题回原作者修 | 可复用且范围/状态清楚后写 state；主问题仍 open 也能发布准确局部结果 |
| 要让其它研究可检索使用的独立结果 | 比较既有稳定身份；相同命题增 version，新命题才新 ID；正文及 evidence 进入登记增量 | compose/register 成功且发布后，才称已入当前登记；不以 backflow plan 冒称完成 |
| 新结果与既有对象确有推出、反驳、迁移或独立替代作用 | 实读全部端点、共同模型和量词，写完整关系/条件/解释/evidence | 用现有 edge-check/bind 与现役集成链，实际推送；无可证关系也允许零边 |
| 发现旧支持错误或应用失效 | 当即保存精确疑点/影响，通知真实消费者，暂停该支持；保其它独立 OR | 定向修正文、版本和受影响边；不是把所有后继自动判假或重做全仓 |

候选的新关系可以保存为 proposed 并明确缺步；accepted 只代表作者作了关系接纳声明。conditional 的开放前提仍开放，contribution 的 remaining 仍未付。不能等全题闭合才保存，也不能“每个保存都登记一节点”。

## 为什么必须在本库这几条数学上验收

令原候选
`R_i(p)=min_A E_(T~p) K_i(T,A)`。它用同一个 p、同一完整纯 SPE σ、actual 前缀和恰 m 个真实槽；强制后继续同一 σ。普通图软件无法替研究者检查这些要求。

| 真实输入 | 正确消费 | 常见错误；应挡住什么 |
| --- | --- | --- |
| SUMmin 原页的纯 p 已付和五个保存有理 p 检查 | 纯点按 A=T 有合法论证；五点只认证五点；一般混合共同预算仍 open | 交换 min 与期望；把不同 T 的不同强制列拼成一列；把有限阴性或浮点 LP 当全域证明 |
| `boss3-uniform-summin-full-budget-equivalence-3313f41b4a46c9dc` | 同 m/实例/完整 σ/同 p 上逐列恒等后得两候选预算等价，双向 whole 条件关系完整；两端仍 open | 从“accepted whole 等价”直接产生已证预算；A⇔B 的 open 环无外来付款不能启动 |
| 末位精确折扣与静态桥正文 | 真正已付的是 R_m≤u_m、纯查询和静态 2m 比较；“SUMmin ⇒ half”是完整条件蕴含 | 把固定末位背景公式递推到强制后全部后继改变的早期行；重复花同一末位储备；把 m 槽改成 m−1 槽 |
| `boss5-all-spe-summin-budget-7383c8bf44f753cc` | 两源 ALL：`CA-AGGREGATE-LAST-FLOOR-NO` 与 `CA-MOBIUS-FULL-HISTORY-EMBED`，仅固定 F、原反演及 K=6M+4 输入族；确实覆盖该族全部完整 σ/同 p | 只取一个源；因 unconditional 而支付整个 target；从该输入族跳到所有有限目录或一般六人 half |

因此本次适配的价值是**让本库已有数学的范围和欠账随使用走**。它不是增加一次“查到边→宣布已证”的自动步骤。

## 工程重量与证据限度

必要部分已经在仓：Markdown/JSON、SHA、Git、RUN、登记、超边和真实 Work 调度。新增 studio 模块及 init/status/line/artifact/adopt/freeze/review/promote 八个动作有实际代码、记录维护和学习成本，不能说成零成本接入；也不能因为没有数据库就默认工程够轻。日常路径仅是 init、真实派工、line/save 和 status；adopt 仅用于实际采用超边，artifact/freeze/review/promote 仅用于需要定位、审查或回流的承重交付。这些记录由执行 Agent 按实物生成，不交用户手填。普通数学不能被迫走完整套动作。

薄层是否值得，要看它实际防住的错误是否超过维护开销。至少应确保不存在第二套 worker/真值状态，freeze 覆盖本题新增合成与证据，贡献剩余可明确付款后闭合，分支/remote 与 registry 基线变化能挡误写。显式依赖可以机器校验；证明中未声明的依赖、作者遗漏和假装独立无法仅靠 JSON 发现。重复维护第二套状态、每句建节点、每步三轮审批或安装上游服务，都无当前证据支持。

本轮直接修改现有 checkpoint：承重发布带 promote 返回的 `checkpoint_review_args`，单次提交/推送即可。每次最终 push 前（包括并发 merge 后的重试）从将发布的 Git commit 读取计划、冻结、审查、全部 content_refs、正式登记对象/边及图投影；与已审字节不符就拒发并保本地提交。隔离真实 Git 测试已验证审后改正文不改变远端，peer 推进 registry 后的自动 merge 会因旧投影被拦，重建后正常推送。普通未完 journal、候选与计划 checkpoint 不带此参数，可立即保全；参数表示本次声称发布已审成果，不能把普通保存当成自动数学验收。删除原来 local-only、手工 SHA 脚本、publish-only 的必需三段流程，未增加独立发布命令。

基线确有重复或误导入口：RESEARCH_WORKFLOW 顶部说旧参考，正文又含旧 open 调度；exporter 只复制旧 solver 词而遗漏新内部词；大段应用模板/规则散在多个文档；`tools/vendor/mathagent/model.py` 无运行引用却仍被工具整包带走。本轮已收敛启动词、共同流程和实际 CLI；导出补齐内部词及新项目 AGENTS，原样上游合同/NOTICE 排除模板改写，6 项 provenance 在导出后仍逐项匹配。首次新边的 `--batch-file` 也已覆盖尚无 canonical registry 的项目，且不落正式总表；无 batch 的原命令保原行为。闲置历史文件的清理另按仓库规则及实证处理，不能用本审计擅删数学资产。

可以通过检验约束的是：错误分支在读取前被拒、ALL 成员不丢、open 环不自付、不能单凭 contribution 关闭全目标、旧证据只影响相关分支、准确版本能恢复。贡献的剩余义务若由明确新证明支付并经相应复核，可以进入全目标闭合；不能永久封死这条研究路线。尚无真实长线研究支持吞吐/突破保证；合成单测、真实边消费演练和保存恢复测试也不能证明自然语言数学正确。下一次真实运行应记录一次推导、反馈修复、精确版本复核和局部回流后，再评估接口是否减负。


本轮逐项复现并修复了首次大仓检出超时、普通 save 丢会话/实读记录、line 二次覆写事件、冻结遗漏原题/定义与新边证据，以及未分类旧边绕过 frontier 冒 whole 的问题。freeze 从已声明 batch/edge 自动展开承重引用，避免人工重复列清单；promote 再核正式回流所用范围。两轮根 work.py CLI 演练把新边交给下一轮实际 adopt，并从 fresh clone 接续。完整测试及真实 Work 演练分别记在 validation.json，不以模拟身份测试冒充平台研究。
