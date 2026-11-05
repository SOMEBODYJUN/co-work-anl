# 可运行的登记、超边与数学研究接口

本规范承接用户要求的2.5第三步、第三阶段和Work研究运行。2.5前两步仍按[原对象群整理规则](CURATION.md)执行；本次不重分类、不移动其正文、不清空认领或公屏。工具已实现不表示全仓已登记、已建图或已有Solver在后台运行。旧`curate`与`map check/build`保留兼容，v2入口是`work.py research`；新建图账本是`work.py map inventory/plan/list/claim/done/handoff/status`。

可直接执行的完整启动词、稳定编号原则、输入冻结/批次集成、独立登记验收和跨批整合验收见[PHASE3_READINESS](PHASE3_READINESS.md)。`--workflow-run`将登记和建图与旧清洗/2.5第二步的身份、工作区、公屏隔开。下列命令的候选总表应由批次compose产生，不让多人直接覆盖总registry。

## 固定设计

数学正文是知识来源；登记与超图是按需读取入口。节点是有精确陈述的数学对象，不是每个文件、日志或程序。一页可以登记多个独立对象，定位到不同标题，无须为了编号切碎原文。代码、输入、输出和复现证书作为owner对象的附件，不自动成为命题节点。对象间的推导、反驳、迁移和启发分开。

`research/registry.json`使用`schema: 2`。不自动把已有frontmatter或旧manifest提升为正式登记。全仓登记应由2.5第二步整理后的实读结果产生；程序提供库存和明确记录的校验。

已同步远端`4eecfe9b3`的只分类目录：材料标号标识一份材料，不等于一个数学命题ID。一份材料可含多个对象，多个材料也可支持同一对象；material记录可附原目录编号供追溯。登记工具不删除、移动或改写原件，不撤销其他Boss的分类与恢复。

| 记录 | 必需内容 | 身份与变更 |
|---|---|---|
| object | `object_id,version,title,kind,truth_status,model,statement,quantifiers,assumptions,scope,objections,body,evidence,sources` | ID不从路径/全文hash生成；改陈述、模型、量词、证明或其他登记字段，明确增version；旧版本留Git历史。不同命题不能以重命名掩盖 |
| body/evidence引用 | `{path,sha256,section?}` | sha256绑定原文件完整字节；section为精确且唯一的Markdown标题，忽略代码块里的伪标题。只返回该标题到下一个同级/上级标题之间正文 |
| material | `{path,sha256,disposition,object_ids,reason}` | `objects/attachment/excluded/needs-decision`；附件必须指向owner。保留/排除须有实读理由，不由文件名、长度或PASS关键词猜测 |
| edge | `edge_id,kind,status,source_ids,target_ids,premises_mode,relation_mode,conditions,roles,explanation,scope,evidence` | `premises_mode: all`保留联合前提；独立证明写不同边。不是两条独立充分的二元边 |
| accepted edge | 再加`reviewed_by,review_note,endpoint_pins,evidence_pins,review_digest` | pins绑定对象完整记录及正文/证据。改条件、角色、解释或端点都会过期；结构检查不证明数学正确 |

`truth_status`：`definition/proved/conditional/conjecture/open/refuted/finite/unassessed`。它与对象类型、关系状态分开。逻辑边种类为`implies/refutes/specializes/transfers/equivalent_to`；语境边为`motivates/cites/sourced_from/implements/checks/corrects/supersedes`。语境边用`relation_mode: context`，不作证明。未证、条件或有限前提只能进入明确`conditional`的逻辑关系；有限检查不能被工具自动当作一般定理。

## 2.5第三步：登记

```sh
python work.py research prepare-inputs --scope repository \
  --coverage-note '第二步已发布材料的当前正式文件快照；只绑定字节，不作数学准入'
python work.py checkpoint research/registration/inputs.json -m 'Freeze 2.5.3 input inventory'
python work.py research freeze --inputs-file research/registration/inputs.json
python work.py checkpoint research/registration/baseline.json -m 'Publish 2.5.3 frozen input baseline'
python work.py research assignments-check --assignment-file research/registration/assignments.json
python work.py research new-id --count N
python work.py research inventory
python work.py research compose --manifest research/registration/batches.json
python work.py research register --record-file research/proposed-registry.json
python work.py research check
python work.py research registration-check --final
python work.py checkpoint research/registry.json -m 'Register reviewed mathematical objects and attachments'
```

由登记Boss实读明确陈述并填写候选registry。`register`拒绝同ID同版本偷偷改内容，拒绝无理由删ID；正式退休放入`retired_objects: {ID: reason}`。正文内容有变时旧引用会失效，需要重新实读后更新绑定。记录中sources保存精确文献/冻结源引用，不能把作者解读写成Paper Fact。

不强制把全部数学压成一行摘要。statement用于定位，完整证明与边界留在body中。`research inventory`只扫描当前正式`archives/.../state/*.md`及问题页，排除evidence里复制的旧树。2.5整理若产生其他正式位置，应先明确扩展扫描边界；不能据有限扫描宣称覆盖任意目录。

## 第三阶段：同一账本分层构图

3A按数学对象族读同组正文；3B补查存档内跨批边；3C核实明确的跨档迁移；3D由一位集成Boss串行生成投影。3–5篇可作为起点，按关系和文本量调整，不是硬配额。每批保留比较范围和跨批疑问，不为连通造边。

任务定义示例使用正式registry对象，可用对象完整记录的`pin`作为`input_pins`：

```json
{"task_id":"sum-local","stage":"3A","registry":"research/registry.json","object_ids":["A","B","C"],"input_pins":{"A":"<object pin>","B":"<object pin>","C":"<object pin>"},"write_paths":["map/edges/sum.json","map/receipts/sum.json"],"goal":"Compare the complete statements and prove the exact joint relation"}
```

```sh
python work.py map plan --record-file map/planned-tasks.json
python work.py checkpoint map/tasks -m 'Publish map construction tasks'
python work.py map list
python work.py map claim sum-local
python work.py research edge-check map/edges/sum.json
python work.py research edge-bind map/edges/sum.json
python work.py checkpoint map/edges/sum.json map/receipts/sum.json -m 'Save explained sum hyperedge and coverage'
python work.py map done sum-local --receipt-file map/receipts/sum.json
python work.py map status
```

`edge-bind`只算并打印绑定，不自动接受关系。作者在实质数学检查后填写accepted字段。任务用正常Git compare-and-push裁决：输入版本或写入范围重叠不能同时领取；同一clone的Git写操作由Main串行组织。done从最新远端快照核对已发布资产字节；本地未推送正文不能登记完成。push回执丢失时读取远端request_id确认，不重复抢任务。失败保留草稿，认证失败不换同一凭据反复试。

receipt格式：`{coverage:{object_id:{state,reason,comparison_scope,object_pin,edge_ids?}},assets:[{path,sha256}]}`。每个对象有`linked/isolated-after-review/needs-decision`之一；linked必须列出真实accepted incident边。done表示该批覆盖处置已交付，needs-decision仍不算最终关系闭合。交接用`map handoff TASK --reason ...`。

最终集成形成`map/coverage.json`，逐对象记录同上，不能有needs-decision；并交`map/integration.json`，绑定当前registry及accepted边，分别记录存档/子档跨批审读和跨档比较，具体字段见PHASE3_READINESS。然后：

```sh
python work.py research check --final
python work.py research build --final
```

最终校验要求当前正式材料有明确处置、每个登记对象有当前版本覆盖结果。草图用不带`--final`的build。输出`map/graph-v2.json`以及存档/子存档对应投影，跨边界节点一并带出。现有`graph.json`原型不覆盖。生成图是派生视图；研究读取直接验证registry和边文件，不会依赖过期投影。

## Work中直接解题

Main使用[研究启动词](../prompts/research-runtime.md)，Solver仅两类：[障碍组](../prompts/solver-obstacle.md)与[成果组](../prompts/solver-full.md)。每次新的RUN固定三个槽位：一个障碍组、两个成果组；三者均使用`gpt-6.1-sol`和`reasoning_effort=ultra`，从空历史启动。Main不算Solver，也不增加常驻审查流水线；容量不足必须记录，不能静默减少数量。

任务spec为`{problem_id,problem:{path,sha256,section?},definitions:[ref],obstacles:[ref],seed_ids:[ID],hops:2}`。problem和definitions必须完整保留题目、域、量词与约束；障碍材料由Main实读挑选，不能塞进全部既有成果。packet生成器不会做语义脱敏，也不是文件访问控制。若Solver仍有全仓工具，必须靠明确读取规则或平台权限维持输入差异，不能声称物理隔离。

```sh
python work.py research init RUN --spec research/problem-spec.json
python work.py research search 'precise mathematical keyword'
python work.py research show OBJECT_ID --body
python work.py research context OBJECT_ID --hops 2
python work.py research save RUN --solver solver1 --profile full --note archives/YOUR_ARCHIVE/workspaces/Boss32/solver1.md --next 'Complete the stated missing inequality' --state working --agent-id PLATFORM_AGENT_ID
python work.py research save RUN --solver solver1 --profile full --note archives/YOUR_ARCHIVE/workspaces/Boss32/solver1.md --next 'Answer the precise objection' --state needs-feedback --feedback 'Specific objection and what is already accepted'
python work.py research resume RUN
python work.py research compute cag-five-local --out research/checks/codespace/cag-five-local.json
```

init只生成输入和恢复状态，**不会自动创建Work子代理**。Main通过平台实际的spawn/followup工具启动固定三槽位，按packet的`fork_turns:none`、模型和effort要求操作。成果组可查全部已登记成果，默认两跳只返回元数据和完整超边；按需show正文、读证据、再扩展，不把全仓塞进上下文。障碍组只接收原题、定义、已知障碍与失败边界；若自主提出需要更完整成果，Main明确记载转换或另开成果组任务，不悄悄污染原输入。

save保存不可变笔记副本、event、continuation_of、平台agent_id和具体下一步。Main把反馈送回原Solver；替代者沿用相同profile、packet、笔记和事件。registry改动不自动改变已保存输入。可恢复的是已保存数学进展和任务状态，不保证平台恢复原进程或隐藏推理。断网保留local-only，恢复凭据后用原checkpoint正常推送。

每形成有价值的Lemma、构造、反例、精确实验、失败机制或关键缺口立即checkpoint；不等目标完全解决。`research compute`会把一次登记实验的回执、版本和输出先提交本地，再尝试推送同一提交。新研究先保存候选正文/证据，更新登记和边需要明确数学判断。Main继续用现有公屏、Boss编号、个人工作区、sync/checkpoint；不为本工具另建每轮远端分支。

## 迁移到其他仓库

```sh
python tools/export_research_template.py --output /absolute/new-workspace --remote https://github.com/OWNER/NEW_REPOSITORY.git --branch main
```

导出工具、提示词和GitHub计算配置，不复制旧数学、凭据、公屏或Git历史；明确改为新仓库URL。导出不创建GitHub仓库、不消费Codespaces、不发布远端。新项目先创建自己的archive、精确定义和登记；第三方vendored代码保留原LICENSE与UPSTREAM。此处资产规范不保证能解决任意开放命题。
