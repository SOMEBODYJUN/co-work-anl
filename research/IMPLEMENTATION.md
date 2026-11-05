# 登记、超边与研究的实际接口

用户每阶段只需根work.py、仓库外凭据和对应[完整Boss词](../prompts/README.md)。启动器恢复独立clone后，进入该clone并只用其根程序；内部模块和说明由执行者自行读取。当前接口保持prepare-inputs、独立edge-check和即时计算保存，同时用同一阶段队列处理登记/构图，不另设每轮人工分配系统。

## 阶段与持续协作

| 阶段 | workflow-run | role | 公屏 | 队列入口 |
| --- | --- | --- | --- | --- |
| 2.5第三步登记 | p25-register-v2 | curator | wcg/board-registration-v2 | registration-task |
| 第三阶段构图 | map-v2 | mapper | wcg/board-map-v2 | map |

任务/lead/身份在research/operations/<run>/，工作区在research/workspaces/<run>/<Boss>/。新对话使用用户给出的唯一Boss号和独立clone；同对话恢复原身份和未完批次。旧clean/curation-run不改绑进新阶段。

```sh
python work.py registration-task lead show
python work.py registration-task list --owner self
python work.py registration-task claim-next
python work.py registration-task done TASK --receipt-file research/registration/receipts/TASK.json
python work.py registration-task handoff --all --reason '实际暂停原因、草稿位置与下一步'
```

构图换成map。lead claim以远端CAS确定唯一集成人；lead也做数学。lead用plan --record-file直接发布任务，成功即pushed，程序接回本地状态，不另手填占用日志。本人未完优先，有实际空位才claim-next。完成一批即保存、done并补位，反馈原worker接续，不等全轮。

核心对象和写范围互斥，共同只读材料不占锁。状态读最新远端；普通竞争自动重选，响应未知用原request_id确认。claimed不证明进程还活着，公屏静默不等于可抢。暂停handoff，lead另lead handoff；必要reclaim TASK --reason由lead明确收回。过期available/handoff用withdraw TASK --reason，claim-next跳过并报告needs_reframing而继续合法项，不自动吞任务。正文/批次/边/收据先checkpoint确认pushed，再done。

## 2.5第三步：真实输入、稳定身份与分批集成

仅lead在本run尚无已发布baseline时初始化；已有输入先恢复，不让所有Boss重复生成和冻结。

```sh
python work.py research prepare-inputs --scope repository --coverage-note '第二步当前已发布正式材料及必要附件' --output research/registration/inputs.json
python work.py checkpoint research/registration/inputs.json -m 'Publish actual registration inputs'
python work.py research freeze --inputs-file research/registration/inputs.json
python work.py checkpoint research/registration/baseline.json -m 'Publish registration baseline'
```

prepare-inputs --output为现行便捷入口，--path可重复指定局部材料/必要附件；canonical inputs --out使用同一真实分母，可配--paths-file的JSON路径清单。局部明确--scope partial，不能把局部或稀疏可见文件当全仓。repository以Git快照和当前正式材料闭合，缺页先恢复；输入只绑定path/SHA，不自动判断数学准入。freeze固定字节，不覆盖既有baseline；材料变化另冻新版本。

登记任务定义：

```json
{
  "task_id":"CA-tail", "stage":"registration",
  "baseline":{"path":"research/registration/baseline.json","sha256":"完整SHA256"},
  "materials":[{"path":"实际正文路径","sha256":"完整SHA256"}],
  "goal":"区分末两人逐人保底和全人数福利的独立Claim身份",
  "write_paths":["research/registration/batches/CA-tail.json","research/registration/receipts/CA-tail.json"]
}
```

lead用registration-task plan --record-file发布。每批schema:2，含objects、materials、edge_files:[]；收据含batch_file精确引用及assets引用数组。一页可供不同批次共享阅读，但独立文件由各自worker写。若有用户明确固定owner安排则遵守；assignments-check可验证可选固定分配表，不取代队列的实时归属或迫使每轮手工排全仓。

| 记录 | 必需内容 |
| --- | --- |
| object | object_id、version、title、kind、truth_status、model、statement、quantifiers、assumptions、scope、objections、body、evidence、sources |
| body/evidence引用 | path、完整文件sha256、可选精确且唯一Markdown标题section；完整证明可由多个引用定位 |
| material | path、sha256、disposition、object_ids、reason；去向为objects/attachment/excluded/needs-decision |

精确Claim稳定ID优先，包含既有namespace和冒号ID；新对象才new-id一次生成并保存。容器页ID不吞不同命题。一页可多对象，多篇可支持同一对象；不同模型、量词、域或结论不因同名自动合并。同对象实质变更增version，换命题另立身份。附件必须有数学owner，普通算术、单次数值、代码、日志和PASS不造节点。

truth_status为definition/proved/conditional/conjecture/open/refuted/finite/unassessed。精确有限反例存在性有完整证明可proved；扫描为finite。被否的辅助桥与原题独立。清楚的open义务正常登记，needs-decision只表示身份、来源或路由尚不清楚。完整知识留正文，statement用于定位，不把证明压成一行或为编号切碎原文。

lead持续collect已done批次，保全后sync再compose，不等全部人结束。registration-task collect --baseline <本轮已发布baseline路径>的JSON可直接作为compose manifest；也可用以下短manifest自动选本baseline已done批次：

```json
{"baseline":{"path":"research/registration/baseline.json","sha256":"完整SHA256"},"workflow_run":"p25-register-v2"}
```

```sh
python work.py registration-task collect --baseline research/registration/baseline.json
python work.py sync
python work.py research compose --manifest research/registration/batches.json
python work.py research register --record-file research/registration/proposed.json
python work.py research registration-check --final
python work.py checkpoint research/registry.json -m 'Integrate accurately registered mathematics'
```

也可显式batches:[{batch_id,record:{path,sha256}}]。compose生成候选，register只由lead更新唯一总表；冲突实质解决，不静默覆盖。登记闭合独立于图，不因尚无超边而停工。

后续小增量manifest用mode:incremental和base_registry当前精确引用，保现有对象、材料和edge_files，只接必要新批。新baseline不重收旧baseline；collect用--baseline选本轮版本，增量manifest再补mode/base_registry。只是同一baseline内改正已done批次才用下面的supersedes机制；材料字节变化另冻新baseline并增量，不跨baseline替代旧任务。

## 第三阶段：从内到外建边与整合

3A先对象内部承重链，再同子档对象族；3B同档跨批/跨子档；3C真实跨档映射；3D统一投影。核心object_ids负责覆盖且互斥，read_object_ids共享只读，input_pins覆盖两者。pin是完整对象记录的指纹，不是文件SHA；research show返回registration_pin供准确引用。

```json
{
  "task_id":"CA-tail-chain", "stage":"3A", "registry":"research/registry.json",
  "object_ids":["CA-LAST-TWO-FLOOR","CA-ALL-N-WELFARE-4N"],
  "read_object_ids":["customer-attraction/last-slot-value-and-catalog-counting"],
  "input_pins":{"CA-LAST-TWO-FLOOR":"对象pin","CA-ALL-N-WELFARE-4N":"对象pin","customer-attraction/last-slot-value-and-catalog-counting":"对象pin"},
  "write_paths":["map/edges/CA-tail-chain.json","map/receipts/CA-tail-chain.json"],
  "goal":"解释末两人保底与目录计数怎样联合推出全人数福利界，保全部共同条件"
}
```

```sh
python work.py map plan --record-file map/planned-tasks.json
python work.py map claim-next
python work.py map read-add TASK --object-ids 已登记的额外共享依赖
python work.py research edge-bind map/edges/CA-tail-chain.json
python work.py research edge-check map/edges/CA-tail-chain.json
python work.py checkpoint map/edges/CA-tail-chain.json map/receipts/CA-tail-chain.json -m 'Publish explained joint support'
python work.py map done TASK --receipt-file map/receipts/CA-tail-chain.json
```

edge含edge_id、kind、status、source_ids、target_ids、premises_mode:all、relation_mode、conditions、roles、explanation、scope、evidence。逻辑种类implies/refutes/specializes/transfers/equivalent_to；语境种类motivates/cites/sourced_from/implements/checks/corrects/supersedes。定义通常作条件和正文引用，不机械造模型hub。引用、相似度、目录从属不冒作推导。

真实例子：末两人保底A与计数界B共同给W≥(n−2)K/n+2θ_n，代入两个θ_n下界消K，得到4(n−1)/(n(2n−1))福利保证。n=6仅10/33。{A,B}⇒C写一条ALL边，不能拆成A单独、B单独足够的两边；不同独立证明另写OR支持。equivalent_to表示ALL(source)⇔ALL(target)，反向要同时保全部targets。refutes多目标须逐项有否定证据，只否定合取不能宣称每项都假；迁移必须写模型映射与保留/丢失条件。

作者完整实读后可accepted，无固定二次审批流水。先定最终status、reviewed_by及具体review_note，再edge-bind填endpoint_pins/evidence_pins/review_digest三个字段，最后edge-check。绑定覆盖语义文字，之后改文字、状态、端点或证据要重核。edge-check校本边而不要求已在canonical清单，程序检查不代替数学判断。proposed保未付条件，rejected保精确失败理由。

map收据含coverage对象表和assets引用数组。coverage覆盖所有核心对象，每项有state、object_pin、reason、comparison_scope；linked另列真实accepted incident edge_ids。状态为linked/isolated-after-review/needs-decision。清楚open问题和proposed联系可准确完成比较；没有accepted联系时如实记录范围和未付义务，不为完成率强造边。已发布canonical边可用精确SHA共享复用，不占原样边写范围；新文件仍保独立write_paths。

```sh
python work.py map collect
python work.py sync
python work.py map assemble
```

collect只读汇集完成批的独立边和coverage候选；assemble仅lead合入registry.edge_files、map/coverage.json与map/integration.json候选。它不自动接受关系或编造数学整合。保留旧实质说明，输入变化只在受影响范围标待复核，lead接着修订。

lead实读并填每个当前档/子档archive_reviews及cross_archive_review，核重复、模型/版本、真实跨批联系和疑点；准确开放数学可以留图，最终清零的是未辨认身份/来源/交付疑点。research check --final及research build --final后，按回执projections显式checkpoint每个准确生成路径，连同registry、coverage、integration确认pushed。repository-cleanup默认范围不含archives内投影，不能漏交，也不宽泛提交整个archives。graph-v2是可重建三级视图，完整知识仍在正文/登记/边解释。

## 定向替代，不重做全仓

同队列改版定义加supersedes:[旧done任务ID]，新任务覆盖旧核心（登记按原材料）。新收据supersession按旧任务给reason与旧assets去向：retained须新收据保原SHA，replaced给新收据内replacement_paths，retired给实际理由。只有新批done才排除旧批；明确替换/退休的旧边退出清单，其它数学保留。例如：

```json
{"supersession":{"old-task":{"reason":"对象改版，仅重判相关支持","assets":{"map/edges/old.json":{"disposition":"replaced","replacement_paths":["map/edges/new.json"],"reason":"新边保完整旧关系并修正条件"}}}}}
```

## 后续Main与Solver消费

Main按[完整研究词](../prompts/research-runtime.md)操作。每个新RUN固定obstacle-1、full-1、full-2，均gpt-6.1-sol/ultra/fork_turns:none；init生成实际packet和槽位，不自动创建模型。平台真实spawn/followup，记录真实agent_id。此三槽配置不限制登记/构图的可用并发。

spec含problem_id、problem引用、definitions引用数组、obstacles引用数组、seed_ids；可加hops、edge_ids、edge_statuses、relation_kinds。原题和定义完整保模型、域、量词和约束。obstacle只接原题/定义/障碍，full另给按需登记成果；用户明确要求继承时照办并准确说明实际输入。packet不代表权限隔离。固定槽位不直接换profile；需要成果交现有full槽，用户明确改变输入实验则用明确新spec/RUN，保原packet。

```sh
python work.py research search '精确数学关键词' --model '实际模型' --truth-status proved
python work.py research show CA-ALL-N-WELFARE-4N --body
python work.py research context CA-ALL-N-WELFARE-4N --hops 0
python work.py research init RUN --spec research/problem-spec.json
python work.py research save RUN --solver full-1 --profile full --note research/workspaces/RUN/full-1.md --next '继续具体未付不等式' --agent-id 实际平台ID
python work.py research save RUN --solver full-1 --profile full --note research/workspaces/RUN/full-1.md --next '回应具体续局质疑' --state needs-feedback --feedback '具体疑点及已成立部分'
python work.py research save RUN --solver full-1 --profile full --note research/workspaces/RUN/full-1.md --next '接续答复后的推导' --state working --ack-feedback
python work.py research resume RUN
```

先实际答复并写note，再ack-feedback。新feedback与ack互斥；普通save保未答反馈，ack关闭pending但保事件历史，后续needs-feedback不复活已答问题。resume保同agent、不可变笔记、continuation、原packet、未答反馈和相关版本变化，并显示相对原输入新可见的关联关系，不悄改原输入。

context默认hops0仅导航，已选逻辑支持完整ALL闭包不截断；support_options之间OR、内部ALL。--edge选择替代分支，--edge-status/--relation-kind仅筛额外研究线索。等价反向支持标direction:reverse，all_premises保全部target_ids。refutations、research_leads与正向支持分开。绑定当前不代表未付前提已证；数学使用必须看全部条件、量词、状态、objections和证据。相关stale定向复核，缺附件仍可读有效正文，不让无关旧边阻断本题。

计算从具体数学义务出发。普通云端用compute request→checkpoint pushed SHA→github runs/run/artifacts/download；已有实验可research compute --manifest --out即时保存。Codespaces留给真实交互/特殊环境，不默认开机或跑旧审计。参数和云端实际状态见[GITHUB_RESOURCES](GITHUB_RESOURCES.md)。有价值成果先完整保存，成熟后定向回写state、登记和有关边，不重做全仓清洗。

明确需要固定分工时，可用research assignments-draft --baseline <已发布baseline> --owners <用户明确的Boss逗号清单>生成可选安排草稿；检查后再发布。manifest显式给assignments精确引用时，compose核相同baseline、批次和材料/路径，不用它代替实际队列归属；默认workflow_run路径从已done任务收拢。freeze只接受已提交HEAD中的材料字节，未提交的数学修改先checkpoint再冻结。
