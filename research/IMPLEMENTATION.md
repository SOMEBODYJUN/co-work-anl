# 登记、超边与研究的实际命令

用户只需根work.py、仓库外凭据和本阶段[完整提示词](../prompts/README.md)。内部模块由程序调用。2.5第三步登记身份；第三阶段解释数学关系；后续Main/Solver才做研究。设计、任务、数学判断分别交付，不以旧演示或测试次数证明已经接通。

## 同一协作引擎，两套阶段运行

| 阶段 | workflow-run | role | 公屏 | 任务入口 |
| --- | --- | --- | --- | --- |
| 登记 | p25-register-v2 | curator | wcg/board-registration-v2 | registration-task |
| 构图 | map-v2 | mapper | wcg/board-map-v2 | map |

用完整词中的start命令绑定用户指定Boss编号和独立clone，先核Git、remote及实际写端点；继续本人未完任务优先。任务和lead在research/operations/<workflow-run>/，工作区在research/workspaces/<workflow-run>/<Boss>/。旧clean、curation任务与公屏不混入。

```sh
python work.py registration-task lead show
python work.py registration-task list --owner self
python work.py registration-task claim-next
python work.py registration-task done TASK --receipt-file research/registration/receipts/TASK.json
python work.py registration-task handoff --all --reason '实际暂停原因与草稿位置'
```

构图把registration-task换成map。只有唯一lead发布plan和集成总表，lead也做数学；lead claim以远端CAS裁决，不靠公屏口头指定。lead handoff明确交接；必要收回使用reclaim TASK --reason；过期的available/handoff任务由lead用withdraw TASK --reason明确撤下，不碰done成果。claim-next跳过有具体输入问题的候选并报告needs_reframing，继续可执行项，不因计时或静默自动抢任务。任务读最新远端，写入竞争自动重选，响应未知查原request_id。所有资产先checkpoint确认pushed，再done；公屏传实际成果、缺口和依赖，不重复逐动作登记。

## 2.5第三步：实读登记，批次集成

```sh
python work.py research inputs --out research/registration/inputs.json --scope repository --coverage-note "第二步已发布正式材料及必要附件"
python work.py research freeze --inputs-file research/registration/inputs.json
python work.py checkpoint research/registration/inputs.json research/registration/baseline.json -m 'Freeze actual registration inputs'
python work.py registration-task lead claim
python work.py registration-task plan --record-file research/registration/tasks-to-publish.json
```

inputs生成真实path/SHA清单，不猜数学身份。repository以Git快照和当前正式材料为分母，sparse缺页必须恢复，不能用可见文件冒充全仓。局部用--scope partial --paths-file明确JSON路径清单；必要附件可在清单中显式补入。freeze固定实际字节，变化另建baseline，不覆盖旧冻结输入。

登记任务定义：

```json
{
  "task_id": "CA-last-two", "stage": "registration",
  "baseline": {"path": "research/registration/baseline.json", "sha256": "完整SHA256"},
  "materials": [{"path": "实际正文路径", "sha256": "完整SHA256"}],
  "goal": "区分逐人末两人保底和全人数福利结论，保留各自精确Claim身份",
  "write_paths": ["research/registration/batches/CA-last-two.json", "research/registration/receipts/CA-last-two.json"]
}
```

每批schema:2，含objects、materials、edge_files:[]；批次收据含batch_file引用及assets引用数组。共享只读材料不互斥，批次写路径独立；不让所有人改总registry。完成一批立即checkpoint/done并补位，lead持续消解身份和版本冲突。

| 记录 | 实际内容 |
| --- | --- |
| object | object_id、version、title、kind、truth_status、model、statement、quantifiers、assumptions、scope、objections、body、evidence、sources |
| body/evidence引用 | path、完整文件sha256、可选精确唯一Markdown标题section；完整证明可由多个引用共同定位 |
| material | path、sha256、disposition、object_ids、reason；去向为objects/attachment/excluded/needs-decision |

一页可有多个对象，多篇可共同支持一个对象。稳定Claim ID优先；新身份用research new-id一次生成并保存，不取路径或全文hash。一份文件的容器ID不能吞掉不同命题。改同对象登记内容明确增version；不同模型、量词或结论不自动合并。附件须有数学owner；普通代码、日志、数值与PASS不造节点。

truth_status分definition/proved/conditional/conjecture/open/refuted/finite/unassessed。精确有限反例若有完整证明可proved，扫描为finite；原题与失败辅助桥保持独立。open数学正常登记；needs-decision只表示尚不清楚身份、来源或路由。

lead可registration-task collect看已done批次，再compose。manifest示例：

```json
{"baseline":{"path":"research/registration/baseline.json","sha256":"完整SHA256"},"workflow_run":"p25-register-v2"}
```

```sh
python work.py sync
python work.py research compose --manifest research/registration/batches.json
python work.py research register --record-file research/registration/proposed.json
python work.py research registration-check --final
python work.py checkpoint research/registry.json -m 'Integrate accurately registered mathematical objects'
```

也可显式给batches:[{batch_id,record:{path,sha256}}]。compose只生成候选，register由集成Boss更新唯一总表；同ID矛盾必须实质解决。后续定向增量manifest加mode:incremental和base_registry精确引用，保留现有对象、材料和edge_files。登记闭合独立于超边，不因图尚无边而阻塞。

## 第三阶段：由内到外解释，再统一投影

3A对象内部承重链与同子档对象族；3B同档跨批/跨子档；3C真实跨档映射；3D统一投影。核心object_ids负责覆盖且互斥；read_object_ids共享只读；input_pins覆盖两者，写路径独立。不把共同模型锁成串行瓶颈。

```json
{
  "task_id":"CA-last-two-chain", "stage":"3A", "registry":"research/registry.json",
  "object_ids":["CA-LAST-TWO-FLOOR","CA-ALL-N-WELFARE-4N"],
  "read_object_ids":["customer-attraction/last-slot-value-and-catalog-counting"],
  "input_pins":{"CA-LAST-TWO-FLOOR":"对象pin","CA-ALL-N-WELFARE-4N":"对象pin","customer-attraction/last-slot-value-and-catalog-counting":"对象pin"},
  "write_paths":["map/edges/CA-last-two-chain.json","map/receipts/CA-last-two-chain.json"],
  "goal":"解释末两人逐人保底与目录计数界怎样联合推出一般福利界，保所有共同条件"
}
```

```sh
python work.py map plan --record-file map/planned-tasks.json
python work.py map claim-next
python work.py map read-add TASK --object-ids 已登记额外依赖
python work.py research edge-bind map/edges/CA-last-two-chain.json
python work.py checkpoint map/edges/CA-last-two-chain.json map/receipts/CA-last-two-chain.json -m 'Explain actual joint welfare support'
python work.py map done TASK --receipt-file map/receipts/CA-last-two-chain.json
```

一条edge含edge_id、kind、status、source_ids、target_ids、premises_mode:all、relation_mode、conditions、roles、explanation、scope、evidence。逻辑种类implies/refutes/specializes/transfers/equivalent_to；语境种类motivates/cites/sourced_from/implements/checks/corrects/supersedes。语境关系不作证明；反驳精确定位，迁移写清模型映射。

实际例子是末两人保底A与目录计数界B共同推出C：W≥(n−2)K/n+2θ_n，配合两个θ_n下界消去K，得4(n−1)/(n(2n−1))福利保证。n=6仅10/33，不能误写成半覆盖。一条{A,B}⇒C保全部共同前提；不同独立证明另写支持分支。定义可作条件，不机械造模型→所有结论的hub。

accepted由作者实读后填写reviewed_by、review_note及edge-bind计算的endpoint_pins/evidence_pins/review_digest。绑定不代审，也不要求每边再经另一固定审批者。proposed、rejected保准确未付条件和失败机制；不为完成率强行接受。

构图收据为coverage对象表及assets引用数组。每个核心对象有state、object_pin、reason、comparison_scope；linked另列真实accepted incident edge_ids。状态是linked/isolated-after-review/needs-decision；准确open数学或proposed桥可交付，不要求先证明所有未知。done直接核本批已推送独立边资产，无需等待lead先改总表。

```sh
python work.py map collect
python work.py sync
python work.py map assemble
```

collect只读汇集完成批的edge_files和coverage_candidates；assemble仅lead执行，合并research/registry.json的边清单并写map/coverage.json、map/integration.json候选。不自动接受边，不编造跨批/跨档数学判断，保留已有实质整合说明；输入变化时在受影响范围标待复核，lead直接接续修订。lead继续处理重复边、受影响版本及未决身份，实读后填各档/子档archive_reviews和cross_archive_review，再research check --final、research build --final。按build回执projections逐一显式checkpoint准确生成路径，连同总表、覆盖和整合；repository-cleanup默认保存范围不含archives内投影，不能省略这些路径，也不宽泛提交整个archives。图为可重建graph-v2.json三级视图；数学真值仍在正文、登记和边解释。


同一冻结登记输入或同一构图队列中，替换已done批次时在新任务定义加supersedes:[旧任务ID]，覆盖被替换批次的原核心对象（登记按原材料）。新收据的supersession按旧任务ID给reason和assets表；每个旧资产注明retained（新收据保原SHA）、replaced（给新收据中replacement_paths）或retired及实际理由。登记材料字节变化另冻新baseline，用mode:incremental与base_registry接续，不跨baseline替代旧任务。只有新批done后旧批才退出collect，明确替换/退休的旧边退出canonical清单；其他数学保留。例如：

```json
{"supersession":{"old-task":{"reason":"对象版本更新，只重判相关支持","assets":{"map/edges/old.json":{"disposition":"replaced","replacement_paths":["map/edges/new.json"],"reason":"新版本完整承接原关系并修正条件"}}}}}
```

## 后续研究：完整支持与原worker接续

Main读[完整研究词](../prompts/research-runtime.md)，按实际需要启动障碍组或成果组，不默认给所有人塞全仓。程序不会自动创建模型子代理。

```sh
python work.py research search '精确数学关键词' --model '实际模型' --truth-status proved
python work.py research show CA-ALL-N-WELFARE-4N --body
python work.py research context CA-ALL-N-WELFARE-4N --hops 0
python work.py research init RUN --spec research/problem-spec.json
python work.py research save RUN --solver solver1 --profile full --note research/workspaces/RUN/solver1.md --next '继续解决具体未付不等式' --agent-id 实际平台ID
python work.py research save RUN --solver solver1 --profile full --note research/workspaces/RUN/solver1.md --next '回复具体质疑' --state needs-feedback --feedback '具体质疑和已接受部分'
python work.py research resume RUN
```

context可用--edge选择一份替代证明、--edge-status和--relation-kind取研究线索；返回support_options、proof_closure_object_ids、refutations及research_leads。证明支持保完整ALL前提闭包、替代OR分支、条件、证据及未付前提；hops是导航范围，不能截断已选证明。候选、语境和refutes不当正向已证支持。只对相关过期支持提示重读，不让无关旧边挡住正文读取；不把过期解释为结论为假。

spec含problem_id、problem引用、definitions引用数组、obstacles引用数组、seed_ids和导航hops。packet固定本次实际输入；save保不可变笔记、event、continuation_of、agent_id、下一步和反馈。resume恢复事件及未答反馈，登记版本变化、相对原输入新可见的关联边及未答反馈明确显示，不悄改旧packet。Main通过平台真实followup给原worker继续；原进程不可用才由同输入、笔记和断点恢复替代者。

普通云端计算、运行跟踪与结果下载见[GITHUB_RESOURCES](GITHUB_RESOURCES.md)。持续研究从真实数学义务出发，不默认数字搜索、不重复跑旧演示。成熟内容及时保存并只更新相关对象/边，不重做全仓清洗。
