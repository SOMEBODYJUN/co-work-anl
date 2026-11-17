# 从原题到研究、入库和恢复的执行流程

用户只下载 [完整 Main 启动词](../../prompts/research-runtime.md)。Main 恢复当前 clone 后自动读本页和内部角色词。本页是应用记录、版本复核及回流的共同合同；不把同一套字段复制到每份提示词。没有用户指定的原题，本次只交程序和流程，不创建数学实战 RUN。

## 1. 先理解各实物的真实用途

| 实物 | 用途 | 不能据此声称什么 |
| --- | --- | --- |
| archives/.../state 与必要证据 | 完整命题、定义、证明、构造和边界 | 文件存在不证明其中数学成立 |
| research/registry.json | 稳定对象 ID、版本、状态和完整正文定位 | 登记或 proved 标签不是程序认证 |
| map/edges | 有解释的联合支持、替代证明、反驳和迁移 | 可达、accepted、current pin 不支付本题条件 |
| graph-v2 及各档投影 | 从当前登记与边重建导航 | 投影不是另一套真值或永久编辑入口 |
| 本 RUN 四人工作室、notes/events | 保全研究中的每项有用进展、失败、反馈和接续 | 保存不等于正式准入，旧 working 不等于在线 |
| studio.json 与 studio/ 记录 | 索引承重成果、真实采用、冻结复核和回流计划 | 不另建数学真值、调度队列或模型服务 |

先按[完整启动词](../../prompts/research-runtime.md)恢复 clone 并读当前入口，再读实际 spec、packet、工作区和所需正文。旧 RUN 用于恢复数学，不按旧 roster 或日志重启退役协作。

## 2. 固定原题并建立四人工作室

先核 clone、origin、分支、HEAD 和未提交成果，保全后同步；使用用户明确的 Boss，凭据留仓库外。原题合同保模型、域、量词顺序、全部约束、退化/平局、成功目标和反例标准。原题尚未登记可直接研究，无相关旧成果就 seed_ids:[]。

统一路径如下。RUN 是实际运行 ID，不是默认要启动的题目；新工作室不得覆盖旧 RUN。

```text
research/workspaces/<RUN>/spec.json
research/workspaces/<RUN>/problem.md、definitions.md
research/workspaces/<RUN>/main/journal.md
research/workspaces/<RUN>/independent/journal.md
research/workspaces/<RUN>/informed-a/journal.md
research/workspaces/<RUN>/informed-b/journal.md
research/workspaces/<RUN>/<slot>/... 实际证明、代码、输入、输出
research/workspaces/<RUN>/records/... 本次命令的 JSON 输入
research/runs/<RUN>/run.json、packet-full.json、packet-obstacle.json
research/runs/<RUN>/notes/、events/、studio.json、studio/
```

直接复制 [开题合同](spec-template.json) 到本 RUN 的 spec.json，填实际 problem_id、problem、definitions、obstacles、seed_ids 与目标约束，移除 template_only 后直接传 --spec；没有另一层 math_spec 需要抽取，不手填 registry 指纹。所有 path 都相对当前 clone，引用是实际文件完整字节的 SHA256，可带原文精确且唯一的 section 标题。init 捕获实际 branch/remote/HEAD，后续 studio 操作核原仓库路由。

以下命令中的 RUN、路径、ID、数学文字和 SHA 必须换成本次实值；示例不是已经运行的研究或回执。用户没有原题时不执行 init。

```sh
python work.py research studio init RUN --spec research/workspaces/RUN/spec.json --expect-branch rebuild/research-v2 --expect-remote https://github.com/SOMEBODYJUN/co-work-anl.git
```

init 复用现有 packet/init_run，保存 full 与 obstacle 两种不可变输入和四人目录；它返回 agents_launched:0。Main 必须通过 Work 实际派出 independent、informed-a、informed-b，自己同时研究。默认子代理 gpt-6.1-sol / ultra / fork_turns:none，遵守用户实际配置并记录平台真值。

| 槽位 | profile | 初始输入及数学责任 |
| --- | --- | --- |
| main | full | 自己推导、构造、做关键合成；串行发布 |
| independent | obstacle | 同一原题、定义、预先允许障碍；独立研究，不当盲审席 |
| informed-a | full | 当前承重缺口与有用的完整支持，自主换方法 |
| informed-b | full | 互补路线或合成义务，不重复同一冻结计算 |

长线沿原研究者接续，不凑一轮才反馈；局部成熟即接回，其余人继续。承重复核临时借未参与论证的现有研究者，不加常驻汇报或审批席。Main 自己的推导和失败同样要留在 main/journal。

## 3. 每项有用结果即时保全，不逐步填多表

每条线连续写 journal：准确陈述、域/量词/条件、完整推导或见证、证据、真实状态、对原题的作用、尚欠步骤和下一动作。候选、未核草稿、失败机制与未答反馈也及时保存；失败只说明准确尝试范围，不自动证明反例或不可能。

先真实派工再用 studio line 登记四人的本次 agent/session；Main 未被平台报告的 model/effort/fork 可以省略，不套用子代理默认冒充自报。子代理首次或换会话必须给实际派工配置。line 是同一 update_run 的包装，另记 session_tag 与可选实读账，不产生第二条状态链。

```sh
python work.py research studio line RUN --line main --note research/workspaces/RUN/main/journal.md --next '自己的当前推导与下一步' --agent-id ACTUAL-MAIN-ID --session-tag ACTUAL-SESSION-TAG
python work.py research studio line RUN --line independent --note research/workspaces/RUN/independent/journal.md --next '从原题接续本线数学' --agent-id ACTUAL-INDEPENDENT-ID --session-tag ACTUAL-SESSION-TAG --model gpt-6.1-sol --reasoning-effort ultra --fork-turns none
python work.py checkpoint research/workspaces/RUN research/runs/RUN -m 'Save substantive research and its exact continuation'
```

另两条成果线按其实际槽位和 ID 各记录一次，不复填同一派工。首次登记后，普通有用进展用原 save 或 studio line 二选一，不对同一变化存两遍；原 save 沿同一 agent 的已记配置和 session_tag 接续。首次真实派出、换 agent 或换会话时记录实际配置；未知项不猜填。session_tag 由 Main 为本次真实 Work 会话显式创建，仅标记记录来自哪次会话，不是平台认证或活跃凭证。每个有用结果先落盘/save，checkpoint 由 Main 按实际变化串行做；只有命令确认 pushed 才报远端已保存。

实读账可在本人目录写成下式，再给 line 加 --read-ledger 路径。可选账只保最后声明的已读范围及未读段，不支付数学前提；普通保存无需另造账。

```json
{"reads":[{"path":"本次实际已读文件","sha256":"实际完整文件SHA256","section":"可选精确唯一标题"}],"note":"实际读过的范围、用途和仍未读部分"}
```

independent 的账只能列原 obstacle packet 的 problem/definitions/obstacles 精确引用及本线自身文件，不能列图或其它线。Work 的共享文件系统不能证明未越读。发生污染必须写时刻和实际输入，后续不称独立；本版不在原槽静默换 profile，需新 spec/RUN 显式约定新输入，保旧 packet/事件。独立线初始探索与其后知情复核分别报告。

## 4. 超边消费：反向找路线，正向核完整联合推导

```sh
python work.py research search '本次缺失结论及同义词' --model '本题实际模型'
python work.py research show OBJECT-ID --body
python work.py research context TARGET-ID --edge EDGE-ID --hops 0
python work.py research frontier TARGET-ID --edge EDGE-ID --expect-branch rebuild/research-v2
```

show --body 只展开 body，必要 evidence 仍须按 path/SHA/section 实读。context 的一条支持内部 ALL，替代完整证明之间 OR；--edge 选择当前目标的支持，必要源前提继续完整展开。hops=0 只限额外导航，不截断选定支持。大对象按同一义务分 pass，保已读/未读范围，不能静默丢前提。

逐项核：目标原句与本题用途、每个前提的实际作用、变量/模型/量词对应、同一见证/策略/概率空间/参数、全部附加条件、联合 closing implication 和剩余。A 与 B 分别成立不能默认合成桥成立；开放前提只能支持准确条件路线。

| 关系语义 | 本题必须保留的限制 |
| --- | --- |
| ALL / OR | 全部共同前提缺一仍欠；一路失败保有效独立替代，不自动判目标假 |
| equivalent_to | 反向需全部 targets；open 等价环无外部起点不能自证 |
| conditional | 推导成立不等于前提已付，全部未付条件向下传 |
| contribution | 只用 result，完整目标的 remaining 仍开放，不升级 whole |
| transfers | 原结果与桥共同用，保模型、参数代价、复杂度、编码和解码保证 |
| refutes / finite / context | 反例只否精确目标；有限扫描、引用、实现或相似不形成一般证明 |

frontier 给的是假设边条件成立的结构闭包和研究线索；不分析自由文本条件、不执行证明助手、不改 truth_status，也不启动或接续代理。Main 据报告选择有用欠项，通过 Work 真实 followup 原线或派出临时研究者。实际采用仍须写本题论证。

## 5. 只有真实采用才写 adopt

adopt 的 record-file 放在本 RUN workspace。它绑定当前 spec、edge 和全部端点，逐项记录付款、联合桥、条件及上游欠账；程序能拒绝显式记录的漏项、过期 pin 和应用循环，不能识别证明文本中未声明的隐藏依赖，也不能判断所填 proof_ref 是否真的证明了文字。

指纹有不同含义，不能混填：path/sha256 绑定完整文件原始字节；problem_spec_pin 取 run.json 的 spec_pin；edge_declaration_pin/object_pins 取当前 context/show 的 declaration_pin/registration_pin；应用 revision_pin 取 adopt 返回值。承重 proof_ref 使用 save 事件中 note 指向的现有不可变快照，或已固定字节的独立证明文件；journal 继续写并链接该论证。直接引用持续编辑的 journal 会随下一次更新失效，不必为此每步另建 artifact。

下面是全部必需字段的模板。premise_bindings 按实际正向 sources 或等价反向 targets 逐一列全；paid 状态必须给 proof_ref，开放状态必须给稳定 obligation_id。condition_discharge 至少保整段 conditions_text，其 argument 对每个实际条件逐项论证；可另列各子句。即使无额外假设也说明模型适用性。remaining 非空文字准确说明仍欠什么；没有就明确写无，本次结论范围已付。

```json
{
  "application_id":"APP-ID",
  "line":"informed-a",
  "problem_spec_pin":"run.json中的实际spec_pin",
  "edge_id":"EDGE-ID",
  "edge_declaration_pin":"当前实际declaration_pin",
  "direction":"forward",
  "object_pins":{"全部源及目标ID":"各自实际registration_pin"},
  "source_to_target_mapping":"完整变量、模型、量词与共同见证对应",
  "applicability":{"model":"实际模型吻合论证","quantifiers":"量词顺序和见证选择","scope":"本次适用域"},
  "premise_bindings":[{
    "source_id":"SOURCE-ID","source_pin":"实际pin",
    "local_statement":"本题中的精确前提","applicability":"该源结论如何适用于本题",
    "state":"established-here","proof_ref":{"path":"实际证明","sha256":"实际SHA256"}
  }],
  "bridge_obligation":{
    "state":"global-whole-argument-applies",
    "statement":"全部本题前提共同推出本次实际结论",
    "proof_ref":{"path":"实际联合论证与本题映射","sha256":"实际SHA256"}
  },
  "conditions_text":"逐字保留当前edge.conditions",
  "condition_discharge":[{
    "condition":"逐字保留完整edge.conditions","argument":"逐条件付款及适用性论证",
    "state":"established","proof_ref":{"path":"实际条件证明","sha256":"实际SHA256"}
  }],
  "result_scope":"whole",
  "actual_result":"本题实际得到的结论，不超过whole或contribution.result",
  "remaining":"本次精确剩余；全部已付时明确写无",
  "evidence_refs":[{"path":"完整本题应用论证","sha256":"实际SHA256"}],
  "depends_on_applications":[],
  "inherited_unpaid_obligation_ids":[],
  "discharged_obligations":[],
  "unpaid_obligation_ids":[]
}
```

开放前提用 state:open-obligation 或 explicit-assumption，开放桥/条件用 open/gap，并给 obligation_id 替代 proof_ref。新证桥用 new-bridge-established。contribution 使用 result_scope:contribution，并增 target_remaining:{statement:原边remaining原文,obligation_id:稳定目标剩余ID}，不能照抄 whole。

上游应用在 depends_on_applications 列 application_id/revision_pin；若某 premise 直接来自它，同时写 from_application:{application_id,revision_pin} 指回同一依赖。inherited_unpaid_obligation_ids 列全部上游未付假设债，明确 discharge 才能移除；discharged_obligations 每项 obligation_id/proof_ref。unpaid_obligation_ids 汇总仍未付的前提、桥、条件和继承假设债，程序沿显式依赖重算。proposed 论证自身缺口仍欠，不能冒作已证。

contribution 的 target_remaining 与局部结论本身的假设债分开：已成立的局部引理可以独立发布，不因原题尚未完成被降成条件引理；目标剩余仍沿显式应用递归传给下游，whole-target 发布必须用已审 target_discharges 逐项支付。不能换一层 application 就丢掉完整目标的剩余。

```sh
python work.py research studio adopt RUN --record-file research/workspaces/RUN/records/application.json
```

应用间精确引用供改版定位真实消费者，不是全图失效传播。一个旧证明错了先核有效 OR，缺支持待证而非假；新用法错不等于原引理本身假。

## 6. 成熟承重成果才索引、冻结和复核

普通 journal/save 已足以保全。只有需要独立定位、采用、承重复核或回流的结果才用 artifact。数学状态可 draft/candidate/established/conditional/finite/refuted/failed/open；完整推导仍在 note_ref，附准确证据。authors 列实际作者 agent ID，applications 列实际采用的应用及 revision_pin；未用图可空。

```json
{
  "artifact_id":"RESULT-ID","line":"informed-a","state":"conditional","kind":"本次实际类型",
  "statement":"精确陈述、条件、量词及对原题的作用",
  "note_ref":{"path":"research/workspaces/RUN/informed-a/lemma.md","sha256":"实际SHA256"},
  "authors":["ACTUAL-AUTHOR-AGENT-ID"],
  "applications":[{"application_id":"实际APP-ID","revision_pin":"实际revision_pin"}],
  "unpaid_obligation_ids":["实际未付义务ID"],
  "evidence_refs":[{"path":"实际必要证据","sha256":"实际SHA256"}],
  "publication_refs":[]
}
```

需正式回流时先准备准确 state 正文、登记 batch 和必要边的最终字节。在 publication_refs 列 batch、边及尚未由这些声明覆盖的待发布材料；freeze 自动展开其中 body/evidence/materials，不重复抄证据清单，再 artifact/freeze/review。这仅针对成熟交付，不每轮复制草稿。可以先写独立 lemma.md，journal 链接它；正式正文保持已审字节，不从长 journal 摘一句代替完整数学。

```sh
python work.py research studio artifact RUN --record-file research/workspaces/RUN/records/artifact.json
python work.py research studio freeze RUN --artifact RESULT-ID --freeze-id RESULT-REV1
```

artifact 自动保不可变 note 快照；freeze 绑定当前成果、原题/定义/允许障碍的实际字节、应用 revision 和全部 content_refs；自动展开显式应用的递归上游、边、端点 body/evidence、付款 proof_ref，以及 publication_refs 内对象/边的必要证据。证明内隐藏依赖仍须研究者如实列全。证据及拟发布字节不得在审读中悄改；修复另给成果版本和 freeze ID。freeze 本身不是复核、发布或数学通过。

Main 真实派未参与生成的研究者，用 [挑战词](../../prompts/research-review-design.md) 实读 freeze 的全部内容，按证明顺序核推导，也尝试推翻错误指控。给 confirmed/not-real/unresolved、成立部分、缺口、影响和最小修复；未找到反例不等于核完。独立输入污染在报告单列。已登记 independent 不得用原身份接成果线复核输入；需要时先保其断点、让出实际槽位，再派 fresh 挑战者，或显式新 spec/RUN 约定新输入，不能冒称原 obstacle 代理仍独立。

```json
{
  "review_id":"REVIEW-REV1","freeze_id":"RESULT-REV1",
  "freeze_revision_pin":"freeze返回的实际revision_pin",
  "reviewer_agent_id":"ACTUAL-NONAUTHOR-ID","independent":true,
  "scope":"本次确实核完的陈述、推导、计算与适用范围",
  "verdict":"approve","evidence_level":"internal-independent",
  "report_ref":{"path":"research/workspaces/RUN/records/review.md","sha256":"实际SHA256"},
  "reviewed_content_refs":[{"path":"逐项照freeze.content_refs列全","sha256":"对应实际SHA256"}]
}
```

```sh
python work.py research studio review RUN --record-file research/workspaces/RUN/records/review.json
```

verdict 可 approve/changes-required/inconclusive，evidence_level 可 internal-independent/formal/external，均为真实执行者声明，不是程序认证。同一 freeze 已有 changes-required/inconclusive 时，后续 approve 要用 resolves_review_ids 列对应旧报告，并写 resolution_argument 实质解决疑点；另找一份赞同不能盖掉未解反馈。重大争议按需定向复核准确反馈，不固定每步三重审。报告实际 followup 回原作者，修后新字节定向再核；答复落盘后才 ack-feedback。

## 7. 成熟数学定向回流：准备与实际发布分开

可复用结果不必等原题全解。Main 对入库负责，可委派正文/证据/登记实质准备，自己核接口并串行发布。state 保存完整陈述与证明，registry 用稳定 ID/version 与精确 body/evidence，真实数学关系才入 edges；普通算式/代码/log/数值点不造对象，已认真比较没有边也不凑边。

本次 registry batch 沿用 IMPLEMENTATION 的 schema:2、objects、materials、edge_files:[]，放本 RUN workspace。每对象完整填 title/kind/truth_status/model/statement/quantifiers/assumptions/scope/objections/body/evidence/sources；每材料列实际 path/SHA/disposition/object_ids/reason。成熟状态与数学范围必须吻合：局部证明可 proved，未付假设 conditional，有限观察 finite，准确开放义务 open。失败尝试本身不自动成为反例或已证障碍；需要提炼独立精确结论。

需要新增边时，按 IMPLEMENTATION 的完整边格式写到 map/edges 的本次目录，保 ALL/OR、whole_result 或 contribution、条件、角色、解释、scope、证据和实际审读。新对象尚未入 canonical 时，现有 edge-bind/edge-check 的 --batch-file 在内存中校验本次 batch 并叠加新/更新对象；只做草稿绑定，不写正式总表。

```sh
python work.py research edge-bind map/edges/本次目录/真实边.json --batch-file research/workspaces/RUN/records/registration-batch.json --write
python work.py research edge-check map/edges/本次目录/真实边.json --batch-file research/workspaces/RUN/records/registration-batch.json
```

先定准确 status、reviewed_by/review_note 和最终数学文字，再绑定；之后改变承重字段须重核重绑。在 publication_refs 列本次 batch 与边，已声明的正文、材料、端点和必要证据由 freeze 自动展开，按第 6 节 artifact→freeze→真实复核→review。已审旧字节不能包办新增元数据。无需另造 preflight registry 或先把未审对象正式登记。

promote 的完整输入如下。它检查本次受审字节并生成候选 registry 和回流计划，不修改正式总表，不运行模型，不确认 push。

```json
{
  "plan_id":"BACKFLOW-ID","freeze_id":"RESULT-REV1","review_id":"REVIEW-REV1",
  "claim_scope":"local-result",
  "scope_argument":"本次可发布结论怎样由已审推导支持，原题仍欠什么",
  "registration_batch_ref":{"path":"research/workspaces/RUN/records/registration-batch.json","sha256":"已审实际SHA256"},
  "object_ids":["本batch全部实际对象ID"],
  "edge_refs":[{"path":"map/edges/本次目录/真实边.json","sha256":"已审最终边SHA256"}],
  "candidate_registry_path":"research/workspaces/RUN/backflow/BACKFLOW-ID/proposed.json"
}
```

```sh
python work.py research studio promote RUN --record-file research/workspaces/RUN/records/backflow.json
```

edge_refs 可空，不能伪造关系。whole-target 只可用于完整原题证明且无未付假设债，scope_argument 仍由人核；conditional 不得冒作闭合。存在直接或继承的 contribution.target_remaining 时，在 promote 输入加 target_discharges:[{obligation_id,argument,proof_ref}] 逐项支付，proof_ref 必须已列入本次受审 content_refs；local-result 不因原题剩余而受阻。promote 只合本次明确增量，保旧登记 baseline 和无关数学，返回 backflow-plan-ready-local-not-published、candidate_registry_ref 与真实后续 commands。

Main 先检查候选及 base_registry_ref 仍匹配当前正式总表；候选自带 backflow_guard，register 拒绝基表变化后的覆盖。若他人已推进，重读相关对象并重新生成本次候选，不覆盖其有效增量。然后执行返回的现有命令：

```sh
python work.py research register --record-file research/workspaces/RUN/backflow/BACKFLOW-ID/proposed.json
python work.py research edge-check map/edges/本次目录/真实边.json
python work.py research check
python work.py research build
```

非空边逐条 check；没有新增边省略该行。build 返回实际 projections。Main 将本次正式正文/证据、registry、边、RUN 记录和实际投影路径一并发布；承重交付用 promote 返回的计划 path：

```sh
python work.py checkpoint ACTUAL-PUBLICATION-PATHS --review-plan ACTUAL-PLAN-RECORD-PATH -m 'Publish reviewed research increment'
```

ACTUAL-PUBLICATION-PATHS 是本次全部实际路径；promote 返回的 checkpoint_review_args 已给 --review-plan 及不可变 plan JSON 路径，可直接复用。需要一次发布多项时可重复 --review-plan。checkpoint 在最后 push 前（包括远端推进后的合并重试）核计划、冻结、审查、正式对象/边及投影的实际 commit 字节，变化就停下定向修复/复核；只有返回 pushed 才称已审增量已发布。promote 本身仍未登记或发布。此检查仅由显式 --review-plan 触发；普通 journal、未完候选和计划随时沿原 checkpoint 保全。

每项增量发布或同步发现相关新边/改版后，Main 重新读取受影响目标的 context/frontier、正文和必要 evidence，核新增支持能支付什么、旧采用是否仍有效、还有哪些义务。把具体结论和下一缺口通过真实 followup 送回相关线，或按空位派工，保存其实际接续。只写新边或 backflow plan 不会触发调度，也不等整题结束才使用新增数学。

日常研究增量不带 --final。该参数还核第三阶段 baseline、全量 coverage/integration 和旧任务队列；不为一个新引理重开全仓构图，也不把新对象伪装成已纳入旧 680 批。保历史构图交付快照，本次新增量按实际对象/材料/边及准确版本单独说明。

改旧对象要保稳定身份并提高实质版本，更新命中引用、受影响边/应用及真正消费者；重绑 pin 之前必须重新核承重论证，不能以新 hash 替代审读。不可变旧证据保原字节，当前入口给准确勘误，有效 OR 保留。无关研究和普通草稿继续。

## 8. 恢复、持续和完成

```sh
python work.py research studio status RUN --session-tag ACTUAL-CURRENT-SESSION-TAG
```

status 已包含原 resume 的 recovery，不必再对同一状态重复运行 resume。先读原 packet 与有效 notes/events，未答反馈、真实计算 job ID、应用/边版本变化及未付义务。status 的 application_version_issues 也检查尚未 freeze 的采用是否在同步后改版，不能只盯已冻结结果。status 的 session_match 只比较标签，platform_liveness 始终未验证；同标签也先查 Work 平台实际 agent 状态。能调用才 followup，不可恢复就用相同数学输入和原线路实物新派，记新 ID 与 continuation，不假装跨会话恢复旧模型。旧 RUN 无 studio 仍用 resume/save 保全，不用 init 覆盖旧记录。

未闭合就继续有价值路线，成熟异步接回；不因一次提交、一轮代理、队列暂空或自设预算结束。重复同一机制失败时，综合最强近成功、精确排除范围和未探索部分，提出不同表示/构造/合成，并说明何种证据改变判断。暂停前保存四人完整实物与准确下一动作，不声称离线后台执行。

完整原题证明或满足原模型所有条件的真实反例才报闭合。局部 closed、条件结果、有限观测、内部独立复核、形式化、外审与发表分开。程序只执行已实现的结构、显式依赖与字节一致性检查；自由文本证明、未声明依赖、实际阅读/作者独立性、Work 活跃和 Git 远端成功仍须按真实证据报告，不能据此保证数学真理或解决公开难题。

## 9. 消费者的现有回归边界

这三项是已有图的消费验收，不是擅自启动下一原题：

1. SUMmin/uniform 等价边 boss3-uniform-summin-full-budget-equivalence-3313f41b4a46c9dc：两个 open 端点、全部 m、完整 σ/槽及同一 p，环不能生成已证预算。
2. 全 SPE 贡献边 boss5-all-spe-summin-budget-7383c8bf44f753cc：保全部共同前提和固定 K=6M+4 输入族，只支付局部 result，remaining 不得丢失，不能关闭一般 SUMmin 或无条件六人 half。
3. 两条 OR 路线仅一条过期：定向刷新该支，保另一路；无支持待证不等于判假。

可重放的完整工程实例在 [studio 集成测试](../../tools/test_research_studio.py)：test_backflow_builds_complete_candidate_then_existing_register_and_context_use_new_edge 实际写临时正文、batch、边、冻结与复核记录，生成 guarded 候选，经既有 register/check/build 后再用 context 取到新关系。[真实对象消费测试](../../tools/test_research_studio_real.py) 使用上述 SUMmin 端点及原始证据，核完整 ALL 与局部范围。

```sh
python -m unittest discover -s tools -p 'test_research_studio*.py' -v
```

测试在隔离临时仓库使用明确的测试身份与占位数学，不派 Work 模型、不向当前正式总表或远端发布。它验证文件流和拒绝边界，不认证合成数学。真实对象测试也只验证输入结构；这些演练、单测和文档不是新版长线实战或自然语言证明验真。
