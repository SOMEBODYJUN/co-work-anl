# 登记、超边与研究的实际接口

使用根 `work.py` 和 [当前启动词](../prompts/research-runtime.md)。程序负责文件、版本与结构，Work 负责实际派工。

## 后续研究的当前入口

第三阶段完成后使用[完整 Main 词](../prompts/research-runtime.md)和[超边/保存/入库实操](agent-design/HYPEREDGE_WORKFLOW.md)。原有 `init/save/resume`、登记及构图命令继续兼容；新 `studio` 将它们接成 Main 与三研究线的工作室，普通数学不套登记/构图任务队列。

```sh
python work.py research studio init RUN --spec PATH --expect-branch rebuild/research-v2 --expect-remote https://github.com/SOMEBODYJUN/co-work-anl.git
python work.py research studio status RUN --session-tag CURRENT_SESSION
python work.py research studio --help
```

`studio line` 调同一套 save 记录真实派工、笔记和反馈。普通中间结果用 journal/save 即时保全；`adopt` 仅用于真正采用超边；`artifact/freeze/review/promote` 用于承重采用或成熟回流，字段及完整实例集中在上述实操，不由用户手填。

新对象还没进当前总表时，可先 `research edge-bind EDGE --batch-file BATCH --write` 和 `research edge-check EDGE --batch-file BATCH` 绑定检查审前关系；只在内存组合明确批次，不改现役 registry。冻结并实际复核后，promote 从已审 batch/edge 生成保留同行内容的完整候选；现有 `research register --record-file CANDIDATE` 才正式写唯一总表。候选绑定当前 registry 字节，基线变化会拒绝覆盖，须同步并重建。随后正式 edge-check、check/build，用 promote 返回的 checkpoint_review_args 调同一个 checkpoint，在最终 push 前核已审文件、正式登记与图投影；确认 pushed。普通未完笔记、候选和计划仍可直接 checkpoint。

研究增量使用 `research check/build`。已退役的整阶段 `--final` 参数会被拒绝。Python 只核结构与字节，真实 Work 派工、独立数学复核及原题闭合判断由研究者完成。

2026-11 新版设计及完整角色词见 [agent-design](agent-design/README.md)。新增只读前沿：

```sh
python work.py research frontier OBJECT-ID --edge EDGE-ID --expect-branch rebuild/research-v2
```

它复用 context 的完整 ALL/OR 支持，列开放前提、适用条件、局部贡献 remaining、绑定刷新与不自证的循环。`structural_assuming_conditions_closure` 假设所有条件成立，仅用于规划；不验证条件、不更新数学真值、不启动模型。`--expect-branch` 在读取数学前拒绝其它本地分支；输出 local snapshot 的 commit/remote/dirty 与 registry pin，不冒称远端确认。本题实际使用必须另留 spec+edge+object pins、模型/量词对应、条件付款和准确证据，详见 [完整流程](agent-design/HYPEREDGE_WORKFLOW.md)。

以下 init/packet/save/resume 接口可作文件工具复用；调度由 Work 的真实子代理工具执行。JSON 生成不是模型派工。

Main按[完整研究词](../prompts/research-runtime.md)操作；新Project明确Boss号与精确研究题目，独立clone用start --role boss --save <实际研究存档>，不复用登记/构图角色或套旧题。同一对话沿原clone/RUN恢复数学与原输入，普通派工按当前设计判断；明确对照才保原输入隔离。四人研究用studio init生成原题/障碍与full两份packet，经平台真实spawn/followup，以line或save记实际ID。下列init --mode open保留为低层兼容接口，不另开第二套四线状态；初始化只写本地计划和包，不启动模型。

spec含problem_id、problem引用、definitions引用数组、obstacles引用数组、seed_ids；可加hops、edge_ids、edge_statuses、relation_kinds。原题和定义完整保模型、域、量词和约束。Main先核本对话/RUN中的实际原题；已有自主选题授权可从该范围的真实开放义务选题，只有会改变题意的关键条件不明才询问。没有相关既有成果时写`seed_ids:[]`，full packet以空objects/edges启动，原题、定义和障碍仍完整；不强塞无关旧对象，也不要求先登记原题才准研究。选择了具体edge_ids则须给真实相关seed，防止丢掉明确选择的证明分支。obstacle只接原题/定义/障碍，full另给按需登记成果；用户明确要求继承时照办并准确说明实际输入。packet不代表权限隔离。对照运行沿各槽的原 profile 派工和反馈。明确改变实验输入时建立新 spec/RUN。

```sh
python work.py research search '精确数学关键词' --model '实际模型' --truth-status proved
python work.py research show OBJECT-C --body
python work.py research context OBJECT-C --hops 0
python work.py research init RUN --spec research/problem-spec.json --mode open
python work.py research peers RUN
python work.py research save RUN --solver next-lemma --profile full --note research/workspaces/RUN/next-lemma.md --next '继续具体未付不等式' --agent-id 实际平台ID --model gpt-6.1-sol --reasoning-effort ultra --fork-turns none
python work.py research save RUN --solver next-lemma --profile full --note research/workspaces/RUN/next-lemma.md --next '回应具体推导缺口' --state needs-feedback --feedback '具体疑点及已成立部分'
python work.py research save RUN --solver next-lemma --profile full --note research/workspaces/RUN/next-lemma.md --next '接续答复后的推导' --state working --ack-feedback
python work.py research resume RUN
```

普通 open 运行返回明确 worker 默认配置（gpt-6.1-sol / ultra / none），实际派工服从用户本轮配置。save 的 --model、--reasoning-effort、--fork-turns 可记录实际配置，后续事件沿用已记录值；旧记录不猜填。配置与 agent_id 是执行者对实际平台派工的记录。

新版设计见 agent-design。开题固定用户原题，Main 实际安排 idea 和执行子代理。新成果发布后，Main 把新增边和义务交给工作者，工作者重读受影响的 context/frontier、正文与必要证据，再回报下一项缺口。research peers 从保存且 pin 匹配的 packet/input_refs 定位同行 RUN、工作区和主笔记，保留不同版本和定义。普通 resume 保原 packet、工作文件和未答反馈。

先实际答复并写note，再ack-feedback。新feedback与ack互斥；普通save保未答反馈，ack关闭pending但保事件历史，后续needs-feedback不复活已答问题。resume保同agent、不可变笔记、continuation、原packet、未答反馈和相关版本变化，并显示相对原输入新可见的关联关系，不悄改原输入。

context默认hops0仅导航，已选逻辑支持完整ALL闭包不截断；support_options之间OR、内部ALL。--edge选择替代分支，--edge-status/--relation-kind仅筛额外研究线索。等价反向支持标direction:reverse，all_premises保全部target_ids。refutations、research_leads与正向支持分开。绑定当前不代表未付前提已证；数学使用必须看全部条件、量词、状态、objections和证据。相关stale定向复核，缺附件仍可读有效正文，不让无关旧边阻断本题。

计算从具体数学义务出发。普通云端用compute request→checkpoint pushed SHA→github runs/run/artifacts/download；已有实验可research compute --manifest --out即时保存。Codespaces留给真实交互/特殊环境，不默认开机或跑旧审计。参数和云端实际状态见[GITHUB_RESOURCES](GITHUB_RESOURCES.md)。有价值成果先完整保存，成熟后定向回写state、登记和有关边，不重做全仓清洗。

明确需要固定分工时，可用research assignments-draft --baseline <已发布baseline> --owners <用户明确的Boss逗号清单>生成可选安排草稿；检查后再发布。manifest显式给assignments精确引用时，compose核相同baseline、批次和材料/路径，不用它代替实际队列归属；默认workflow_run路径从已done任务收拢。freeze只接受已提交HEAD中的材料字节，未提交的数学修改先checkpoint再冻结。
