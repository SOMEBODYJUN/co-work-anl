# RA06 对抗审计报告（独立盲审）

审计对象为当前 `integration-v2` 快照、原稿页图/区域图、旧稿与交接、`final-03` 审计记录及自主恢复队列。本报告只写入本目录；未修改主 ledger、正文或主 audit report。清单先于本报告建立在同目录的 `blind-checklist.md`，并在第一阶段未读取 `recovery-team/visual` 或 `recovery-team/math` 结论。

## 结论

当前正文目标片段的 199/199 个 `text_sha256` 与 `integration-v2` 两份正文一致，manifest、PDF、页图和区域图哈希也一致；已明确保留的 25 个未决 target、9 个未决 recovery、8 个 open issue 仍被中性编号/红色未完标记保留。结构上没有发现“正文已经改了而该 target 的 text hash 未改”的直接漏同步。

但冻结链已经被后续台账写入破坏，且自主恢复队列不是按当前 ledger 建成：当前恢复队列对 34/66 条记录没有任何 crop/evidence/source 定位，其中许多定位在当前 ledger 中实际存在。这会把可恢复的图像任务错误标为 `tool_blocked`，并使下一轮恢复无法覆盖真实未决内容。以下两项是阻断发布的硬问题；旧稿追踪是需要明确口径的中风险问题。

---

## ADV-001（硬阻断）：final-round 写入后 ledger 与 final-03 冻结哈希不一致

**证据与路径**

- `reviews/final-03/review-record.json` 的 `frozen_artifacts.ledger.sha256` 与 `core_snapshot_hashes.ledger.sha256` 均为 `8d2105e98acc4e19a99785fa65d8512f251d6fe359f12963e340fe42319e22e7`。
- 同一记录写明 `final_rounds_before_root_seal: 0`、`mutated_ledger: false`，且 `audit-reports/final-03.json` 的 `snapshot_sha256` 仍为 `09675aff3dcf9e74358e4bfa0bde0045f91dcf53232bbe0c737f5c9212c0250d`。
- 当前 `ledger-integration-v2.json` 实际 SHA-256 为 `d1e47edd4e33ffe74a50b1d9478ce95dddb613f55efd57faa2c12d518d48587e7`，不是冻结值；当前 `ledger.final_rounds` 已有 3 条（`RA06-final-01/02/03`）。
- `final-rounds.json`（实际 SHA-256 `221d10039016595b0cb77f221ec88188944c131cd35d37a03189876ba488e004`）与当前 ledger 内嵌的三条记录相等，证明这不是哈希计算偶发误差，而是审计后确实追加了 ledger 内容。
- `reviews/final-03/report.md` 第 31 行仍称 `final_rounds` 为空、ledger 与冻结快照全部一致；该陈述与当前文件冲突。

**影响**

最新审计报告、review-record、final-rounds 和当前 ledger 不再描述同一个可验证快照。任何依赖 8d2105… 或 `final_rounds_before_root_seal=0` 的 seal/发布判断都无法证明当前 ledger 未被修改；三轮记录也没有在写入后得到新的官方 audit/hash 绑定。

**修复建议**

1. 由 root 决定保留这三轮还是回退到 pre-seal ledger；不得静默覆盖历史。
2. 若保留三轮：以当前 `ledger-integration-v2.json` 重新计算并记录 ledger SHA，重跑结构 audit，更新 `audit-reports/final-03.json`（或新版本报告）、`reviews/final-03/review-record.json` 的 frozen/core hash、`mutated_ledger`、`final_rounds_before_root_seal` 和 snapshot 绑定；同时把 `final-rounds.json` 纳入明确的 hash 清单。
3. 若回退三轮：恢复 ledger 使其实际 SHA 回到 8d2105…，并把三轮记录另存为待 seal 证据，不能继续在报告中宣称当前 ledger 为空 final_rounds。

---

## ADV-002（硬阻断）：autonomous-recovery/recovery-plan.json 是旧 ledger 的派生物，34 条记录丢失当前证据定位

**证据与路径**

- `autonomous-recovery/recovery-plan.json` 的 `input_report` 指向 `audit-reports/final-03.json`，但计划没有记录生成时使用的 ledger SHA，因此无法证明它对应当前 ledger。
- 当前计划的 66 条记录中只有 32 条有 crop，34 条的 `source_ids`、`evidence_ids`、`page_ids`/`bbox_px` 和 `crop_paths` 为空。缺 crop 的 ID 为：
  - source：`RA06-P002-U01-B`、`RA06-P004-U12-B`；
  - target：`N-p3-radius-convention`、`T-p4-12-b`、`N-p4-12-b`；
  - page：`VS-PASS2-V2-p0002` 至 `VS-PASS2-V2-p0005`；
  - region：`VS-PASS2-V2-p0002-r1c1/r1c2/r2c1/r2c2`、`VS-PASS2-V2-p0003-r2c1/r3c1/r3c2`、`VS-PASS2-V2-p0004-r1c1/r3c1/r3c2`、`VS-PASS2-V2-p0005-r3c1`；
  - recovery：`VS-REC-Q002`、`VS-REC-Q003`、`VS-REC-Q004`、`VS-REC-Q006-FINITE`、`VS-REC-Q007-ENDPOINT`、`VS-REC-Q014-SUPER`、`VS-REC-Q016-TITLE`、`VS-REC-Q017-DELTA`、`VS-REC-Q018-PREFIX`；
  - issue：`Q006`、`Q007`、`Q008`、`Q009`、`Q010`。
- 这些空字段并非当前 ledger 的真实状态。例如：
  - 当前 `ledger.source_units[RA06-P002-U01-B]` 有 `page_id=p0002`、bbox `[130,475,1140,600]`、证据 `image:p0002`, `image:p0002-r1c1`；计划该记录三者均为空。
  - 当前 `ledger.source_units[RA06-P004-U12-B]` 有 `page_id=p0004`、bbox `[1010,2410,1720,2640]`、证据 `image:p0004`, `image:p0004-r3c1`, `image:p0004-r3c2`；计划均为空。
  - 当前 `ledger.target_units[N-p3-radius-convention]` 指向 `RA06-P003-U06`、证据 `image:p0003`；计划 `source_ids=[]`, `evidence_ids=[]`。
  - 当前 `ledger.target_units[T-p4-12-b]` 与 `N-p4-12-b` 各指向 `RA06-P004-U12-B`、证据 `image:p0004`；计划均为空。
  - 当前 `ledger.recoveries[VS-REC-Q002]` 指向 `RA06-P002-U04`，有五个页/区证据；计划完全为空。`VS-REC-Q003/004/006-FINITE/007-ENDPOINT/014-SUPER/016-TITLE/017-DELTA/018-PREFIX` 同样如此。
  - 当前 `ledger.issues[Q006–Q010]` 各有 `image:p0002/p0003/p0005` 与 `artifact:uncertainties` 证据；计划这些 issue 的 `evidence_ids` 全部为空。
  - 计划 `T-p2-01` 只有 source `RA06-P002-U01`，而当前 ledger 已按拆分把它映射到 `RA06-P002-U01` 和 `RA06-P002-U01-B`；这是可见的双向映射漂移。

**影响**

恢复代理按旧计划无法为上述未决字形/页区生成定向 crop，也无法把候选与正确 source/target/recovery/issue 绑定。部分记录虽在当前正文中保持 `[Q...]` 或红色未完标记，但恢复队列会漏掉它们，形成“正文看似保留、恢复证据实际不可达”的假解决/假阻塞。

**修复建议**

1. 以当前 `ledger-integration-v2.json`（先解决 ADV-001 的 seal 口径）重新运行 autonomous recovery，给计划加入 `ledger_sha256`、manifest SHA、audit-report SHA 和每条 crop 的文件 SHA。
2. 重新派生全部 66 条记录的 `source_ids/evidence_ids/page_ids/bbox_px`；对有页/区证据的 34 条必须生成 600–1200 dpi crop，并逐条验证路径存在、哈希与 manifest 区域证据相符。
3. 特别复核 split IDs `RA06-P002-U01-B`、`RA06-P004-U12-B` 以及 targets `N-p3-radius-convention`, `T-p4-12-b`, `N-p4-12-b` 的正向/反向映射；计划中的空 source 不能继续作为恢复输入。
4. 重新生成后把旧计划保留为历史文件并明确标注旧 ledger SHA，避免覆盖造成不可追溯。

---

## ADV-003（硬阻断/状态误报）：`status: tool_blocked` 是派生缺证造成的，不是视觉工具不可用

**证据与路径**

- `autonomous-recovery/recovery-plan.json` 将状态写成 `tool_blocked`；`tools/autonomous_recovery.py` 的实现只要任一记录 `crop_paths` 为空就设置该状态。
- 当前 PDF `source.pdf` SHA-256 `c089cd714af04d97bfbf17a031881acd508ebd70b2f5221aa745bc5253b6db89`、manifest SHA-256 `51bc0d36d72b940cefa5645e38ebdd52327c4dc40f4183816b93e856423c642a`、6 页和 36 个区域图全部可读且哈希匹配；现有计划也已经生成了 32 条记录的 800 dpi crops。
- 因而 `tool_blocked` 的触发原因是 ADV-002 的旧 ledger 关系/证据为空，而不是 `missing_pdf`、`corrupt_pdf` 或视觉工具不可用。

**影响**

状态名会把可继续自主恢复的任务误报成工具故障，容易错误走人工阻塞路径；这与 assignment 的 `manual_intervention=false` 和恢复策略相矛盾。当前合同要求保持 claimed 并继续模型恢复，状态应能区分“有工具但队列缺证”与真实工具阻塞。

**修复建议**

- 在重新生成计划后，若所有有证据的记录均有 crop，将状态改为 `ready`；仍无 source/page 的记录应单列为 `missing_evidence`，列出其 ledger ID，不得笼统标 `tool_blocked`。
- 在计划中记录 `missing` 列表、原因分类及对应 ledger SHA；禁止仅用 `not crop_paths` 把数据关系错误归因于工具不可用。

---

## ADV-004（中风险）：旧稿存在但 old_units/old_ids 为空，旧稿去向只有 prose 声明而无台账闭合

**证据与路径**

- `proposals/rebuild/source-transcript.md` SHA-256 `c3f771d36dd91c28598cec889df0de51d689a14c40aa87f91b1632bb7e8435ad`、`proposals/rebuild/study-notes.md` SHA-256 `73d08b25b72a08ceab706a402f0de809e1958834530f24457c53d1c15bb04aed` 均存在；`proposals/rebuild/handoff-first-pass.md` 与 `proposals/integration-v2/handoff-first-pass.md` 明确说“原 compared rebuild 两稿及 ledger-first-pass.json 保留不改”。
- 当前 `ledger-integration-v2.json.old_units` 长度为 0，199 个 target 的 `old_ids` 全为空，`ledger-config-v2.json` 的 artifacts 也没有 `kind: old` 条目。
- assignment 的 `previous_markdowns=[]` 表明这些 rebuild 文件可能只是本运行的候选首稿，而非用户提供的旧稿；但当前记录没有明确写出这一排除口径。

**影响**

若 rebuild 被视为待审旧稿，则任何删除、拆分、改写（例如 62 source units → 78、124 targets → 199、Q005/Q010 等改写）都无法通过 old↔current 映射追踪；若它不属于旧稿范围，现有审计也没有把这一点写成机器可核验的排除声明，容易把候选历史误读为已完成旧稿迁移。

**修复建议**

- 明确二选一并写入 ledger/config/audit：
  1. 将 rebuild 两稿作为候选历史而非输入旧稿，记录其路径、SHA 和 `old_scope_excluded_reason`；或
  2. 将两稿注册为 `kind: old` artifacts，建立 old_units 与 target `old_ids`，至少覆盖拆分、删除、合并、改写和未决项。
- 在最终报告中列出该口径，避免仅凭 `old_units=[]` 推断“没有旧稿”。

---

## 已核实但未列为问题的项目

- `manifest.json`、`source.pdf`、6 页图和 36 个区域图的实际哈希均与 manifest 一致；第 6 页 6 个区域均为空白且有两轮 blank 检查。
- 当前 ledger 78 个 source IDs、199 个 target IDs、72 个 region checks 的 ID 唯一；source→target 与 target→source 引用在当前 ledger 内闭合。
- 199 个 target 的 marker 行段按 ledger 规则（包含 marker 行、单 LF 连接、不加尾 LF）重算全部匹配 `text_sha256`；正文中的未决项仍以 `[Q...]`、中性定位或红色未完说明保留。
- 当前 ledger artifacts 列出的 29 个正文/证据文件哈希均匹配；上述问题集中在审计后 ledger 追加、恢复计划派生快照和旧稿范围声明，不是简单的正文 text-hash 漏记。

## 建议的修复顺序

1. 先决定并修复 ADV-001 的 ledger/final-round seal 口径，重新生成当前官方审计快照。
2. 用该快照重建 ADV-002 的恢复计划、证据定位与 crops，并把状态从误报的 `tool_blocked` 细化为 `ready`/`missing_evidence`。
3. 明确 ADV-004 的旧稿范围；若纳入则补 old artifacts/units/mappings，若排除则写入可核验排除声明。
4. 对新的当前快照再执行第二遍和三轮终审；任何正文、台账、恢复状态或映射变化都应使旧 final-round chain 失效。
