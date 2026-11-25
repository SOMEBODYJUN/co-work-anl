# RA07 对抗审计报告（独立盲审）

本审计对象为 RA07 当前项目目录中的源 PDF、manifest、页图/区域图、`proposals/rebuild` 与 `proposals/integration-v2` 两套稿件、主账本及整合账本、审计报告、恢复计划、页面/区域复核和交接文件。先建立了同目录的 `blind-checklist.md`，再读取 reviewer 结论；没有修改主 ledger、正文、主 audit、mapping 或 recovery 文件。

## 结论

源文件的基础完整性是可复核的：项目 `source.pdf` 的 SHA-256 为 `c053b24757b997ab489d1c18371df9ba44137919d53596b7158856ac1e8746c8`，与 assignment/manifest 一致；manifest 的 13 页图和 78 个区域图均存在且哈希匹配。以 `ledger-integration-v2.json` 为输入重算时，33/33 artifact hashes、420/420 target marker/text hashes、149/149 source bbox/region 约束和双向 mapping 均通过，26 个页面检查和 156 个区域检查也覆盖了 13 页和每页六区。

当前状态仍不能作为一个单一、可冻结的快照。`ledger.json` 仍是首遍旧账本，而 `ledger-integration-v2.json` 才包含第二遍证据、恢复记录和三轮 final-round；`audit-reports/current.json` 实际按旧账本报告了 92 个缺失第二遍结构错误，恢复计划却按 `final-03`/整合账本生成了 42 个未决项。三轮之后的文件哈希又没有回写到最终报告的“当前账本”声明。恢复队列中 6 条有现存页/区/证据定位的记录没有 crop 或定位字段，因而被笼统标为 `tool_blocked`。此外，两套首遍 handoff 都携带与当前文件不相符的正文哈希，且 rebuild 是否是需迁移的 old draft 没有机器可核验的口径。

以下 ADV 项为阻断发布或冻结的实质问题。

## ADV-001（硬阻断）：canonical ledger 分裂，current audit 读取了旧账本

**证据**

- `project/ledger.json` 实际 SHA-256 为 `215cb0a0c864846d45d80ad63963c55b2e41441782b68a75ccb9bed33039ff50`；它有 148 source units、418 target units、21 artifacts、13 page checks、78 region checks、0 recoveries、0 final rounds。
- `project/ledger-integration-v2.json` 实际 SHA-256 为 `541911c0fe4b3e64290b81a37566e6aefc795e4943dfc102e7c0f85228795237`；它有 149 source units、420 target units、33 artifacts、26 page checks、156 region checks、11 recoveries、3 final rounds。它新增了 `RA07-P006-U014`、`T-P006-014`、`N-P006-014`，并纳入 visual-second 和 root revisit evidence。
- `ledger-config-integration-v2.json` 的 output 指向 `ledger-integration-v2.json`；`final-rounds.json` 与该账本的 `final_rounds` 数组完全相等（3 条）。这说明整合账本和 final-round 文件是一个后来阶段，而 `ledger.json` 不是其别名或同步副本。
- 最新名字为 `audit-reports/current.json` 的报告写的是 snapshot `633ddc199043c285287a84b636639e2c5aceac3a99c1a842d8ff1ac4c61e0b4b`、`unresolved_count: 21`、`structural_error_count: 92`，92 条错误全部是旧账本缺少第二遍 page/region pass 和 final-three-round。相反，`audit-reports/final-03.json` 写的是 snapshot `8b1293d44865ec783926bad7fd054080ed1ec61fc424340e9af6ead8ce74cb77`、42 个未决、0 个结构错误；其 scope 正是 149/420/33/26/156/11/3 的整合账本。
- `autonomous-recovery/recovery-plan.json` 的 `input_report` 为 `audit-reports/final-03.json`，`unresolved_count` 为 42；因此 current audit 与 recovery plan 不是同一输入快照。

**影响**

“当前审计”无法回答到底哪一本 ledger 是权威输入。若以 `ledger.json` 发布，第二遍证据、恢复记录和三轮复核被丢失；若以 `ledger-integration-v2.json` 发布，`audit-reports/current.json` 的 92 个结构错误和 21 个未决数就是过时结果。任何依赖 current audit 的 claimed/recovery/freeze 判断都会得到错误状态。

**修复建议**

1. 由 root 明确选择 `ledger-integration-v2.json` 为唯一 canonical ledger（或明确回退旧账本），并在配置中记录 canonical path、实际 SHA 和生成时间。
2. 从选定账本重新运行结构审计，生成新的 current audit；旧的 `current.json` 应改名为带输入 hash 的历史报告，不能继续占用“当前”名称。
3. 重新生成 recovery plan 和 final-round chain，使 input report、ledger SHA、manifest SHA、正文 SHA 全部绑定到同一快照。

## ADV-002（硬阻断）：恢复计划缺少现有证据定位，却将状态归因为 tool_blocked

**证据**

- `autonomous-recovery/recovery-plan.json` 在 `2026-11-25T11:59:11.372377+00:00` 生成，记录 42 条（9 source、26 target、4 issue、3 recovery），状态为 `tool_blocked`。
- 计划共引用 127 个 crop path，已检查这些路径全部存在；但下列 6 条记录完全没有 `crop_paths`，且其 `source_ids`/`page_ids`/`bbox_px`/`evidence_ids` 为空或未填：`RA07-P006-U014`、`T-P006-014`、`N-P006-014`、`VS-REC-004`、`VS-REC-006`、`VS-REC-010`。
- 这些不是缺少源材料的记录。整合账本中：
  - `RA07-P006-U014` 有 `page_id=p0006`、bbox `[0,2410,120,2630]`、`image:p0006` 和 `image:p0006-r3c1`；
  - `T-P006-014`、`N-P006-014` 各有 `RA07-P006-U014` 反向映射，并有 `artifact:visual-second-p0006-left-margin`；
  - `VS-REC-004` 有 `RA07-P005-U007`、p0005 evidence；`VS-REC-006` 有 `RA07-P006-U009`、p0006 evidence；`VS-REC-010` 有 `RA07-P011-U010`、p0011 evidence。
- 赋予 `tool_blocked` 的计划没有记录生成时的 ledger SHA，只有 source PDF SHA；因此即使有 42 条输入，也不能证明这些空定位是从当前整合账本派生。
- assignment 的 `recovery_policy.real_block_reasons` 仅列 `missing_pdf`、`corrupt_pdf`、`visual_tool_unavailable`。当前 PDF、页图、区域图和已有 crops 均可读且哈希匹配，未见工具不可用证据。

**影响**

恢复代理拿到的不是完整的可回图队列：至少 6 条现有 evidence-backed 任务无法得到 crop，计划生成器因空 crop 统一输出 `tool_blocked`，会把“队列派生不完整”误报成“视觉工具故障”。这与 `manual_intervention: false` 和保持 claimed、继续模型恢复的 assignment 策略冲突。

**修复建议**

- 先固定 canonical ledger，再以其 source/target/recovery/issue 的 evidence 和 bbox 重新生成 42 条计划；对上述 6 条至少补写 source/page/bbox/evidence，并生成或明确记录无法裁图的原因。
- 在计划顶层加入 `ledger_sha256`、`manifest_sha256`、`input_report_sha256`；每个 crop 记录文件 SHA、来源页 bbox 和证据 ID。
- 将状态拆为 `ready`、`missing_evidence` 和真实 `tool_blocked`；只有 assignment 列出的三种真实阻塞才可使用 `tool_blocked`。

## ADV-003（硬阻断）：final-03/审计/三轮文件的冻结声明互相过期

**证据**

- `reviews/final-03/report.md` 声明“当前 `ledger-integration-v2.json` file SHA-256”为 `77ef788e5033b0b6fc608836b9479e40b7cfdd916236f4a250cd02b389f93944`，并称其 `final_rounds` “remains the two sealed rounds supplied for this task”。当前文件实际 SHA 为 `541911c0fe4b3e64290b81a37566e6aefc795e4943dfc102e7c0f85228795237`，`final_rounds` 长度为 3。
- `final-rounds.json` 实际含 `RA07-final-01/02/03` 三条，且与整合 ledger 内嵌的三条完全相等；因此不是报告中“仍为两轮”的同一文件状态。
- `reviews/final-01/report.md` 记录的 ledger SHA `3c805322...`、`reviews/final-02/report.md` 记录的 ledger SHA `65ad9034...` 也都不是当前整合 ledger SHA。这些可作为历史报告，但 final-03 使用“Current”措辞且未给出后续追加三轮的 seal 说明。
- `reviews/visual-second/integration-v2-confirmation.md` 是更早的整合确认，明确写“最终独立终审轮次尚为 0”。它没有时间/输入 hash 标注把自己限定为历史记录，若被当作当前冻结确认会再次产生状态冲突。

**影响**

第三轮记录被追加后，没有产生一个与三轮之后账本相绑定的新官方审计/封存证明。`final-03` 的 report、外部 final-rounds、账本 final_rounds 和 current audit 描述了至少三个不同阶段；审阅者无法仅凭文件判断哪些 review 仍有效、哪些输入已被修改。

**修复建议**

1. 将 Final-01/02/03 report 明确标注为其输入 hash 的历史报告；新建一个指向当前 ledger SHA 的 seal/current report，或回退 ledger 到 report 所声称的快照。
2. 新 current audit 必须在三轮数据写入后运行，并把 `ledger.json`、`ledger-integration-v2.json`、`final-rounds.json` 的关系写入结果。
3. 保留历史文件但禁止再把 `integration-v2-confirmation.md` 或 final-03 的旧“current ledger”数字作为当前状态引用。

## ADV-004（中高风险）：两套首遍 handoff 的正文哈希错误，rebuild 的 old-draft 口径未闭合

**证据**

- `proposals/rebuild/first-pass-handoff.md` 与 `proposals/integration-v2/first-pass-handoff.md` 内容和 SHA 完全相同，均宣称 `source-transcript.md` 为 `df0e9e45491ef2345a5de8d2585e9bed5785b25f029cb66d9e5bc92215edf594`、`study-notes.md` 为 `c80abe60b72787b9701fdd1a52c67dfec254216e9a182721955d935b13a7aba6`，并宣称 148 source / 422 target。
- 实际文件哈希分别为：rebuild source `a8111e9c0e2a5fb072da43051c600c4fff5bb504e5a66b7234e6a80703bf7d2c`、rebuild study `4beee8a4e18cb311970fa748679de47ad744330d0eabfe1ff2e0bdaafdb8f661`；integration-v2 source `72954031a008ad305e8630a826fb7e2ae774f7dd56878178c7377f6d19ec715f`、integration-v2 study `3cbfca7725ab6b77a8b9fa91fc350aa28b39779c3864b025a004b45c18772ac0`。
- `ledger-integration-v2` 是 149 source / 420 target；`ledger.json`/rebuild first-pass ledger 是 148 source / 418 target；没有任何 ledger/config artifact 被标记为 `kind: old`。
- `assignment.previous_markdowns` 是空数组，说明 rebuild 可能只是同一运行中的候选首稿；但当前记录没有写出“rebuild 明确不是用户旧稿”的可核验排除声明。

**影响**

首遍 handoff 不能证明它描述的是哪一套正文；审阅者可能按错误 hash 审核错误稿。若 rebuild 被视为旧稿，`old_units=[]` 又无法追踪两稿之间的新增页边残弧、target 拆分和多项字形修订；若它只是候选稿，当前 ledger/config 仍缺少排除口径。

**修复建议**

- 为每套稿件分别生成带实际 hash、line count、source/target count 的 handoff，并在文件名中标明 first-pass/integration-v2。
- 明确 rebuild 是“同一运行的候选首稿”还是需纳入 old scope；若纳入，注册 old artifacts/old_units 和 old↔current mapping；若排除，写入 `old_scope_excluded_reason` 和实际 hash。
- 任何新 final review 都必须引用明确的 integration-v2 hash，不得再引用这两个过期首遍 handoff 的 hash。

## ADV-005（中风险，需显式保留黑/蓝边界）：p0004 误差分母的源字形与数学预算不同

`VS-REC-003` 选择的原笔候选是同基线的 `ε/(2k)`（C1），其 backward validation 明确指出 `Σ ε/(2k)` 发散而数学预算意图支持 `ε/2^k`（C2）。integration-v2 的转写和学习稿原位保留 `2k`，蓝色补证随后使用几何级数 `Σ2^{-k}=1`。这是可接受的保真/纠错分层，当前没有把它判为静默数学错误；但任何新整合必须继续把“原笔记录”和“可用的几何预算”分开，不能把 source line 当作已证明的次可加性估计，也不能把 C1 标成数学正确候选。

## 已独立核实的通过项

- source PDF 实际 hash 与 manifest/source assignment 一致；13 页、13 页图、78 个区域图的存在性与 hash 均通过。
- integration-v2 ledger 的 33 个 artifacts 均存在且实际 hash 匹配；source/target ID 唯一，双向 mapping 无断链。
- 420 个 target 按各自 `start_line:end_line` 重算 text hash 全部匹配，marker 行也全部匹配；149 个 source bbox 均在页界内且与列出的 region 相交。
- integration-v2 的 13 个 pass-1 page checks + 13 个 pass-2 page checks、78 + 78 region checks，覆盖所有页和每页六区；p0013 被记录为空白页，p0012 被记录为稀疏页。
- 三轮 scope 均列出 13 page IDs、78 region IDs、149 source IDs、420 target IDs、11 recoveries、4 issues、26 page checks 和 156 region checks，且 findings 为空；这些 scope 数字本身与整合账本一致，但不消除 ADV-001–004 的冻结链问题。

## 建议的修复顺序

1. 先确定唯一 canonical ledger，重新生成 current audit，并把旧 audit 按输入 hash 标为历史。
2. 用同一 canonical ledger 重建 autonomous recovery plan，补全 6 条现有证据记录的定位/crop，加入 ledger/manifest/report hashes，消除错误的 `tool_blocked`。
3. 将三轮 final-round 记录、review record、final report 和当前 ledger 绑定到同一新 snapshot；不满足这一点时不得宣称已冻结。
4. 重写两套 handoff 的实际 hashes，并明确 rebuild 的 old-draft 口径；需要迁移则建立 old mapping。
5. 新快照再做一次结构审计和必要的三轮复核；保留 p0004 的 `2k`/`2^k` 黑蓝边界。
