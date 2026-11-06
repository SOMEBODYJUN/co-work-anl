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
python work.py registration-task claim-next --count 6
python work.py registration-task done --record-file research/registration/ready.json
python work.py registration-task handoff --all --reason '实际暂停原因、草稿位置与下一步'
```

构图换成map。lead claim以远端CAS确定唯一集成人；lead也做数学。lead用plan --record-file直接发布任务，成功即pushed，程序接回本地状态，不另手填占用日志。本人未完优先，claim-next --count N一次取得实际空位可做的N个任务；N是任务/worker数，不是材料数，不预占以后工作。单任务可含几十/几百份materials，只一次claim和一次done。本批反馈仍交原worker，整批交付后立即补fresh worker接下一批；Boss身份不变，明确复用旧worker才扣其已用历史，不等全轮。

核心对象和写范围互斥，共同只读材料不占锁。状态读最新远端；普通竞争自动重选，响应未知用原request_id确认。claimed不证明进程还活着，公屏静默不等于可抢。暂停handoff，lead另lead handoff；必要reclaim TASK --reason由lead明确收回。过期available/handoff用withdraw TASK --reason，claim-next跳过并报告needs_reframing而继续合法项，不自动吞任务。正文/批次/边/收据先checkpoint确认pushed，再done。

## 批次和上下文预算

登记是批量提取成熟数学身份：核精确陈述、模型量词、条件、来源/owner并定位完整证明，没有新疑点不重新逐句审全部已整理证明，实际已读范围如实记录；不重做清洗/证明。构图按数学关联比较，不按固定几篇机械循环。两阶段都默认gpt-6.1-sol/ultra、fresh fork_turns:none；本批修订找原worker，交付后下一批用新fresh worker。用户明确继承时按其要求，并在规划中扣除已继承上下文；未知时标未知并保留空间，不能当0。

所选Sol在Work/Codex的[官方默认窗口](https://learn.chatgpt.com/docs/models)为500K；这不是本次会话的实报剩余额度。draft前sync保本地正文/registry一致；绑定阶段另读最新轻量远端任务metadata排重，未绑定的独立规划才使用本地tracking快照。候选同名刷新，不覆盖已发布任务。两个draft共用--model、--context-tokens、--context-source、--used-tokens、--reserve-tokens、--output-tokens、--context-mode。容量来源为official-default/platform-reported/user-specified；省略容量时仅采用所声明Sol官方默认，不能假称平台实报。未显式指定--reserve-tokens时默认按窗口40%预留，正文预算为窗口减预留再减已用历史；--output-tokens默认预留的一半且最多100K，已包含在预留中不双扣。500K时正文/元数据初值300K、总预留200K、输出100K；显式256K时相应为153600/102400/51200，而非继续固定扣200K。可按明确平台/用户容量调节。字符、UTF-8字节和估计token分别列出，并注明计量方法；其它模型不套500K。完整对象含所有必要证明refs作为阅读单位，重复文件/重叠section按实际区间去重；同页独立Claim可以分批共享读取，不为去重合并命题。单对象超预算保同一task，用reading_passes/章节给有序完整读取方案，不为每pass另认领，不截断、隐去或冒称已读完。

只给当前owner仍为本Boss且确认pushed的任务派worker，历史请求已成功不证明当前仍归本人。领取默认给短摘要和任务路径，worker按路径读本批完整定义，不把全仓任务表注入Boss上下文。成熟批次先合并checkpoint确认pushed，再把当次可交的条目写入ready.json：

```json
[{"task_id":"实际完成批次ID","receipt_file":"该批实际收据路径"}]
```

`done --record-file ready.json`先核本次全部条目，再一次CAS交付；任一条目有错整次不部分发布。ready是当次命令输入，不是第二队列；确认pushed后可删临时ready，失败保原输入。成熟几个交几个，不等凑齐6个或一整轮。单项`done TASK --receipt-file PATH`仍可用；未知回执沿原request恢复，不重领。

## 2.5第三步：真实输入、稳定身份与分批集成

仅lead在本run尚无已发布baseline时初始化；已有输入先恢复，不让所有Boss重复生成和冻结。

```sh
python work.py research prepare-inputs --scope repository --coverage-note '第二步当前已发布正式材料及必要附件' --output research/registration/inputs.json
python work.py checkpoint research/registration/inputs.json -m 'Publish actual registration inputs'
python work.py research freeze --inputs-file research/registration/inputs.json
python work.py checkpoint research/registration/baseline.json -m 'Publish registration baseline'
```

prepare-inputs --output为现行便捷入口，--path可重复指定局部材料/必要附件；canonical inputs --out使用同一真实分母，可配--paths-file的JSON路径清单。局部明确--scope partial，不能把局部或稀疏可见文件当全仓。repository以Git快照和当前正式材料闭合，缺页先恢复；输入只绑定path/SHA，不自动判断数学准入。freeze固定字节，不覆盖既有baseline；材料变化另冻新版本。

真实输入冻结后，lead自动生成一份可执行任务数组：

```sh
python work.py sync
python work.py research batches-draft --baseline research/registration/baseline.json --output research/registration/tasks.json
python work.py registration-task plan --record-file research/registration/tasks.json
```

默认跳过当前canonical同SHA且准确处置材料，新版本/needs-decision才入批；显式重审用--include-registered。默认单批最多200份材料，按同档/子档、正文读取线索及实际token预算装包；当前正文实测常见约35–45份/包，短材料可100以上，以实际草稿为准，不凑数截断。一次claim-next --count 6批领6个包，可合计约200份分给已有6个worker，不是每个worker再spawn6个。草稿每task包含task_id、stage:registration、baseline引用、materials精确引用数组、goal、独立write_paths及context_plan；worker读取本批后写`research/registration/batches/<task-id>.json`与对应receipts。lead按实际数学关联修订这份草稿，不另填一套全仓工单。同名候选草稿直接更新，不产历史版本；tasks=0不交空表plan，转恢复/整合后按真实状态判断。

plan成功即发布，无需先给草稿做一次独立远端登记。每批schema:2，含objects、materials、edge_files:[]；收据含batch_file精确引用及assets引用数组。一页可供不同批次共享阅读，但独立文件由各自worker写。若有用户明确固定owner安排则遵守；assignments-check可验证可选固定分配表，不取代队列的实时归属或迫使每轮手工排全仓。

| 记录 | 必需内容 |
| --- | --- |
| object | object_id、version、title、kind、truth_status、model、statement、quantifiers、assumptions、scope、objections、body、evidence、sources |
| body/evidence引用 | path、完整文件sha256、可选精确且唯一Markdown标题section；完整证明可由多个引用定位 |
| material | path、sha256、disposition、object_ids、reason；去向为objects/attachment/excluded/needs-decision |

精确Claim稳定ID优先，包含既有namespace和冒号ID；新对象才new-id一次生成并保存。容器页ID不吞不同命题。一页可多对象，多篇可支持同一对象；不同模型、量词、域或结论不因同名自动合并。同对象实质变更增version，换命题另立身份。附件必须有数学owner，普通算术、单次数值、代码、日志和PASS不造节点。

truth_status为definition/proved/conditional/conjecture/open/refuted/finite/unassessed。精确有限反例存在性有完整证明可proved；扫描为finite。被否的辅助桥与原题独立。清楚的open义务正常登记，needs-decision只表示身份、来源或路由尚不清楚。完整知识留正文，statement用于定位，不把证明压成一行或为编号切碎原文。

### 一份正文登记两个对象的完整格式

数学全文继续留在Markdown；worker写`research/registration/batches/<task-id>.json`，lead集成到唯一`research/registry.json`。下面演示一份正文中有两个独立对象，假定原文已有“命题A与证明”“命题B与证明”两个唯一标题，各章包含对应完整陈述与证明。示例不是实际登记；ID、路径、标题、状态、来源和所有`<...>`必须换成实读值。`unassessed`仅演示状态字段，不能不作数学判断就照抄。

```json
{
  "schema": 2,
  "objects": [
    {
      "object_id": "EXAMPLE-A",
      "version": 1,
      "title": "<对象A准确名称>",
      "kind": "<对象A实际数学类型>",
      "truth_status": "unassessed",
      "model": "<实际模型和定义域>",
      "statement": "<对象A精确陈述>",
      "quantifiers": "<对象A完整量词>",
      "assumptions": ["<对象A实际前提>"],
      "scope": "<对象A适用范围>",
      "objections": "<实际异议、缺口或已核对范围>",
      "body": {
        "path": "<本批真实正文路径.md>",
        "sha256": "<完整文件原始字节的实际64位SHA256>",
        "section": "命题A与证明"
      },
      "evidence": [],
      "sources": ["<实际可追溯来源标识>"]
    },
    {
      "object_id": "EXAMPLE-B",
      "version": 1,
      "title": "<对象B准确名称>",
      "kind": "<对象B实际数学类型>",
      "truth_status": "unassessed",
      "model": "<实际模型和定义域>",
      "statement": "<对象B精确陈述>",
      "quantifiers": "<对象B完整量词>",
      "assumptions": ["<对象B实际前提>"],
      "scope": "<对象B适用范围>",
      "objections": "<实际异议、缺口或已核对范围>",
      "body": {
        "path": "<本批真实正文路径.md>",
        "sha256": "<完整文件原始字节的实际64位SHA256>",
        "section": "命题B与证明"
      },
      "evidence": [],
      "sources": ["<实际可追溯来源标识>"]
    }
  ],
  "materials": [
    {
      "path": "<本批真实正文路径.md>",
      "sha256": "<完整文件原始字节的实际64位SHA256>",
      "disposition": "objects",
      "object_ids": ["EXAMPLE-A", "EXAMPLE-B"],
      "reason": "<说明本文件怎样承载两个对象及实际读取比较范围>"
    }
  ],
  "edge_files": []
}
```

逐对象的`object_id`是数学身份，`version`是该对象记录版本；同一文件的两个对象使用同一个文件SHA256，不以hash合并身份。引用只支持`path`、`sha256`和可选`section`；`section`是原文精确且唯一的ATX标题文字，不是URL锚点、行号或任意文本片段，读取到下一个同级或更高级标题前。无合适唯一标题可省略该字段绑定全文，仍须以准确陈述辨别对象并如实交待定位疑点。正文改动会使全文SHA256变化，相关引用须按真实新字节及既有版本/冻结规则定向更新。

上例只有在各`body`已完整承载对应论证且无另外必要证据时才可用空`evidence`。证明、必要定义、输入、程序或证书在其它章节/文件时，逐条加到`evidence`，每项仍是`path/sha256/section`引用；完整证明可以跨多个引用。`sources`是来源追溯字符串，不能代替字节定位。`materials`按文件版本反向列全数学owner：正文用`objects`，必要附件用`attachment`并归相应对象；一份附件可服务多个对象。代码、数值和日志不因此自动成为数学对象。

实际识别命题、区分同义/独立内容、判断量词条件与状态并填写JSON的是Boss/worker。`tools/research_runtime.py`的`load/ref_bytes/section`和`tools/registration.py`的`validate_batch`会检查必填结构、ID/版本、SHA、标题存在且唯一，以及材料与owner的引用闭合；这些检查不替代上述数学判断。第三阶段按`object_id`引用超边端点，不把整篇文件当一个默认节点。

lead持续collect已done批次，保全后sync再compose，不等全部人结束。registration-task collect --baseline <本轮已发布baseline路径>默认只给短摘要；加--full的JSON可直接作为compose manifest；也可用以下短manifest自动选本baseline已done批次：

```json
{"baseline":{"path":"research/registration/baseline.json","sha256":"完整SHA256"},"workflow_run":"p25-register-v2"}
```

```sh
python work.py registration-task collect --baseline research/registration/baseline.json --full > research/registration/batches.json
python work.py sync
python work.py research compose --manifest research/registration/batches.json
python work.py research register --record-file research/registration/proposed.json
python work.py research registration-check --final
python work.py checkpoint research/registry.json -m 'Integrate accurately registered mathematics'
```

也可显式batches:[{batch_id,record:{path,sha256}}]。compose生成候选，register只由lead更新唯一总表；冲突实质解决，不静默覆盖。登记闭合独立于图，不因尚无超边而停工。

后续小增量manifest用mode:incremental和base_registry当前精确引用，保现有对象、材料和edge_files，只接必要新批。新baseline不重收旧baseline；collect用--baseline选本轮版本，增量manifest再补mode/base_registry。只是同一baseline内改正已done批次才用下面的supersedes机制；材料字节变化另冻新baseline并增量，不跨baseline替代旧任务。

### 缺对象、语义冲突与研究成果怎样接回

`compose`只合记录，不判断数学同义。确认为同一精确命题时，登记lead先比较模型、变量对应、量词顺序、前提、结论和域，选一个主身份、主正文并合齐独立证明和必要证据；主记录由实际分配到主body材料的批次作者维护，必要时先调整批次范围，其他作者把来源归该owner，不各自写不同的同ID记录。主owner未发布时，同Boss的已推批可成组交付；跨Boss由lead先集成主owner，相关作者再续交，同时做其它独立材料。已经done的资产按现有定向替代/增量处理，不直接覆盖旧回执。

map lead发现漏对象，或研究Main有新成果时，由发起人负责把精确陈述、条件、正文/证据出处和需要新增/改版的理由送到现有p25登记lead并跟进；不能发完消息就当完成。只有独立可复用的数学对象需要补登记，普通证明步骤留在现有正文和边解释。原lead已交接或明确空缺，发起Boss可用本对话合适绑定clone或独立阶段clone显式`lead claim`接任；已有归属未解时先保存具体数学与待整合项、继续其它独立工作，不凭静默抢占。

字节不变的既有正文可复用对应baseline，发布只含必要来源的局部批次；同SHA材料的owner列表由增量合并。新正文或改字节先明确checkpoint确认pushed，再发布新的inputs/baseline路径；全仓完成须新baseline仍覆盖当前全仓字节，但只派新增/改动部分的数学工作。用`mode:incremental`和当前`base_registry`精确引用收必要新批。需要清理重复身份时，manifest的`retired_objects`给准确去向与理由，保留独有数学和来源。涉及总表时串行安排：登记lead先完成并推送对象/材料增量，map lead再同步、重判受影响pin与关系；其余数学不等全仓重建。

旧核心未变而只增加已登记依赖，用`map read-add`续原批；核心版本/pin已变，作者保草稿并handoff，map lead按新版本重派交原worker接续；已done批按定向替代处理。正常完成本轮登记/构图后，准确出口已pushed并交清接续位置，lead也须`lead handoff --reason`释放集成位，后续增量才有合法接任入口；不是每包结束就重换lead。

## 第三阶段：从内到外建边与整合

3A先对象内部承重链，再同子档对象族；3B同档跨批/跨子档；3C真实跨档映射；3D统一投影。lead先按关联与同一预算形成草稿再发布：

```sh
python work.py sync
python work.py research map-draft --stage 3A --output map/planned-tasks.json
python work.py map plan --record-file map/planned-tasks.json
```

已有任务先恢复，不重复plan已发布草稿；0任务不plan空表，转恢复或整合。3B/3C需重复--object-id或--objects-file明确实际比较frontier；没有明确前沿就不重新全量draft。3D是lead整合，不使用map-draft。同页和正文明确链接只是优先合读线索，不自动变成数学关系。数量可能几篇、十几篇或更多，不固定3–5、9篇或对象配额。完整对象是原子阅读单位；同页不同独立sections可以分包，共同定义/证据共享读并去重。核心object_ids负责覆盖且互斥，read_object_ids共享只读，input_pins覆盖两者。pin是完整对象记录指纹，不是文件SHA；research show给registration_pin。以下三对象仅示例一条真实ALL关系，不是默认批量上限。

```json
{
  "task_id":"joint-proof", "stage":"3A", "registry":"research/registry.json",
  "object_ids":["OBJECT-C"],
  "read_object_ids":["OBJECT-A","OBJECT-B"],
  "input_pins":{"OBJECT-A":"<对象A的registration_pin>","OBJECT-B":"<对象B的registration_pin>","OBJECT-C":"<对象C的registration_pin>"},
  "write_paths":["map/edges/joint-proof","map/receipts/joint-proof.json"],
  "goal":"核清A和B是否共同支持C，保留完整模型、量词、条件与证据"
}
```

```sh
python work.py map plan --record-file map/planned-tasks.json
python work.py map claim-next --count 6
python work.py map read-add TASK --object-ids 已登记的额外共享依赖
python work.py research edge-bind map/edges/joint-proof/support.json
python work.py research edge-check map/edges/joint-proof/support.json
python work.py checkpoint map/edges/joint-proof/support.json map/receipts/joint-proof.json -m 'Publish explained joint support'
python work.py map done --record-file map/ready.json
```

edge含edge_id、kind、status、source_ids、target_ids、premises_mode:all、relation_mode、conditions、roles、explanation、scope、evidence。逻辑种类implies/refutes/specializes/transfers/equivalent_to；语境种类motivates/cites/sourced_from/implements/checks/corrects/supersedes。定义通常作条件和正文引用，不机械造模型hub。引用、相似度、目录从属不冒作推导。

{A,B}⇒C写一条ALL边，不能拆成A单独、B单独足够的两边；不同独立证明另写OR支持。equivalent_to表示ALL(source)⇔ALL(target)，反向要同时保全部targets。refutes多目标须逐项有否定证据，只否定合取不能宣称每项都假；迁移必须写模型映射与保留/丢失条件。各对象代表本次实际数学，示例ID不能直接写进真实任务。

作者完整实读后可accepted，无固定二次审批流水。先定最终status、reviewed_by及具体review_note，再edge-bind填endpoint_pins/evidence_pins/review_digest三个字段，最后edge-check。绑定覆盖语义文字，之后改文字、状态、端点或证据要重核。edge-check校本边而不要求已在canonical清单，程序检查不代替数学判断。前提尚未证明但“若A且B则C”的论证完整时，可以是`accepted`且`relation_mode:conditional`，不会把C提升为已证；关系论证本身还有缺步才用`proposed`。所有前提与额外条件均已付清才可作为无条件支持，`rejected`保精确失败理由。

map收据含coverage对象表和assets引用数组。coverage覆盖所有核心对象，每项有state、object_pin、reason、comparison_scope；linked另列真实accepted incident edge_ids。状态为linked/isolated-after-review/needs-decision。清楚open问题和proposed联系可准确完成比较；没有accepted联系时如实记录范围和未付义务，不为完成率强造边。已发布canonical边可用精确SHA共享复用，不占原样边写范围；新文件仍保独立write_paths。

### 一条ALL边与对应收据

以下是尚未绑定的关系草稿，所有ID、文字和引用都须替换为实际数学。`status`取决于推导有没有完成，不取决于前提命题是否已经证明；草稿先列为`proposed`，确认推导后按上文确定状态及relation_mode，填写审读说明并运行edge-bind/edge-check。

```json
{
  "edge_id": "joint-support",
  "kind": "implies",
  "status": "proposed",
  "source_ids": ["OBJECT-A", "OBJECT-B"],
  "target_ids": ["OBJECT-C"],
  "premises_mode": "all",
  "relation_mode": "conditional",
  "conditions": "<共同模型、量词及全部附加条件>",
  "roles": {"OBJECT-A": "<A提供哪一步>", "OBJECT-B": "<B提供哪一步>", "OBJECT-C": "<所得结论>"},
  "explanation": "<完整推导及变量对应；若未完成则指出具体缺步>",
  "scope": "<关系实际适用范围>",
  "evidence": [{"path": "<实际论证路径.md>", "sha256": "<文件实际64位SHA256>", "section": "<原文唯一标题>"}]
}
```

对于上例核心只有C的任务，确认有成立关系后的收据如下。`object_pin`用`research show`返回的registration_pin，assets的SHA在边文件最终写好/绑定后计算；收据不把自己列为asset。

```json
{
  "coverage": {
    "OBJECT-C": {
      "state": "linked",
      "object_pin": "<对象C当前registration_pin>",
      "comparison_scope": "<实际比较的A、B、C版本与必要论证范围>",
      "reason": "<为何这条关系准确支持本对象，条件还有哪些未付>",
      "edge_ids": ["joint-support"]
    }
  },
  "assets": [{"path": "map/edges/joint-proof/support.json", "sha256": "<最终边JSON实际64位SHA256>"}]
}
```

一批可多边，也可认真比较后零边。零边时，把已比较哪些候选、为何不能成立或尚缺哪一步，直接写入现有coverage的comparison_scope/reason，交`assets:[]`，无需另造说明文件。以下同样只演示核心C；实际每个core都要有条目，不能把有限比较说成不存在任何潜在关系。

```json
{
  "coverage": {
    "OBJECT-C": {
      "state": "isolated-after-review",
      "object_pin": "<对象C当前registration_pin>",
      "comparison_scope": "<实际读过的对象版本、候选关系和证据范围>",
      "reason": "<逐项说明本范围没有成立关系的数学理由及有价值的未付条件>"
    }
  },
  "assets": []
}
```

零边仍须真实完成本范围工作。已读对象本体与必要论证，按模型、陈述和条件主动检索后确无合理候选，可记录实际检索范围及理由据实isolated-after-review，不凑无关比较或自环；未读/未检索不能当完成。身份/输入或比较尚未弄清写needs-decision，由lead定向续办。空assets只适用于图阶段，登记仍须已推batch_file资产。需要保留有价值的候选关系时，写proposed边并把其文件列入assets，不能因不accepted就删除线索。

```sh
python work.py map collect
python work.py sync
python work.py map assemble
```

collect默认给只读短摘要，--full才返回完整独立边和coverage候选；assemble仅lead合入registry.edge_files、map/coverage.json与map/integration.json候选。它不自动接受关系或编造数学整合。保留旧实质说明，输入变化只在受影响范围标待复核，lead接着修订。

lead实读并填每个当前档/子档archive_reviews及cross_archive_review，核重复、模型/版本、真实跨批联系和疑点；准确开放数学可以留图，最终清零的是未辨认身份/来源/交付疑点。research check --final及research build --final后，按回执projections显式checkpoint每个准确生成路径，连同registry、coverage、integration确认pushed。repository-cleanup默认范围不含archives内投影，不能漏交，也不宽泛提交整个archives。graph-v2是可重建三级视图，完整知识仍在正文/登记/边解释。

## 定向替代，不重做全仓

同队列改版定义加supersedes:[旧done任务ID]，新任务覆盖旧核心（登记按原材料）。新收据supersession按旧任务给reason与旧assets去向：retained须新收据保原SHA，replaced给新收据内replacement_paths，retired给实际理由。只有新批done才排除旧批；明确替换/退休的旧边退出清单，其它数学保留。例如：

```json
{"supersession":{"old-task":{"reason":"对象改版，仅重判相关支持","assets":{"map/edges/old.json":{"disposition":"replaced","replacement_paths":["map/edges/new.json"],"reason":"新边保完整旧关系并修正条件"}}}}}
```

## 后续Main与Solver消费

Main按[完整研究词](../prompts/research-runtime.md)操作；新Project明确Boss号与精确研究题目，独立clone用start --role boss --save <实际研究存档>，不复用登记/构图角色或默认套旧问题。同一研究对话沿原clone/RUN恢复。每个新RUN固定obstacle-1、full-1、full-2，均gpt-6.1-sol/ultra/fork_turns:none；init生成实际packet和槽位，不自动创建模型。平台真实spawn/followup，记录真实agent_id。此三槽配置不限制登记/构图的可用并发。

spec含problem_id、problem引用、definitions引用数组、obstacles引用数组、seed_ids；可加hops、edge_ids、edge_statuses、relation_kinds。原题和定义完整保模型、域、量词和约束。Main先核本对话/RUN中的实际原题；已有自主选题授权可从该范围的真实开放义务选题，只有会改变题意的关键条件不明才询问。没有相关既有成果时写`seed_ids:[]`，full packet以空objects/edges启动，原题、定义和障碍仍完整；不强塞无关旧对象，也不要求先登记原题才准研究。选择了具体edge_ids则须给真实相关seed，防止丢掉明确选择的证明分支。obstacle只接原题/定义/障碍，full另给按需登记成果；用户明确要求继承时照办并准确说明实际输入。packet不代表权限隔离。固定槽位不直接换profile；需要成果交现有full槽，用户明确改变输入实验则用明确新spec/RUN，保原packet。

```sh
python work.py research search '精确数学关键词' --model '实际模型' --truth-status proved
python work.py research show OBJECT-C --body
python work.py research context OBJECT-C --hops 0
python work.py research init RUN --spec research/problem-spec.json
python work.py research save RUN --solver full-1 --profile full --note research/workspaces/RUN/full-1.md --next '继续具体未付不等式' --agent-id 实际平台ID
python work.py research save RUN --solver full-1 --profile full --note research/workspaces/RUN/full-1.md --next '回应具体推导缺口' --state needs-feedback --feedback '具体疑点及已成立部分'
python work.py research save RUN --solver full-1 --profile full --note research/workspaces/RUN/full-1.md --next '接续答复后的推导' --state working --ack-feedback
python work.py research resume RUN
```

先实际答复并写note，再ack-feedback。新feedback与ack互斥；普通save保未答反馈，ack关闭pending但保事件历史，后续needs-feedback不复活已答问题。resume保同agent、不可变笔记、continuation、原packet、未答反馈和相关版本变化，并显示相对原输入新可见的关联关系，不悄改原输入。

context默认hops0仅导航，已选逻辑支持完整ALL闭包不截断；support_options之间OR、内部ALL。--edge选择替代分支，--edge-status/--relation-kind仅筛额外研究线索。等价反向支持标direction:reverse，all_premises保全部target_ids。refutations、research_leads与正向支持分开。绑定当前不代表未付前提已证；数学使用必须看全部条件、量词、状态、objections和证据。相关stale定向复核，缺附件仍可读有效正文，不让无关旧边阻断本题。

计算从具体数学义务出发。普通云端用compute request→checkpoint pushed SHA→github runs/run/artifacts/download；已有实验可research compute --manifest --out即时保存。Codespaces留给真实交互/特殊环境，不默认开机或跑旧审计。参数和云端实际状态见[GITHUB_RESOURCES](GITHUB_RESOURCES.md)。有价值成果先完整保存，成熟后定向回写state、登记和有关边，不重做全仓清洗。

明确需要固定分工时，可用research assignments-draft --baseline <已发布baseline> --owners <用户明确的Boss逗号清单>生成可选安排草稿；检查后再发布。manifest显式给assignments精确引用时，compose核相同baseline、批次和材料/路径，不用它代替实际队列归属；默认workflow_run路径从已done任务收拢。freeze只接受已提交HEAD中的材料字节，未提交的数学修改先checkpoint再冻结。
