# RA10 adversarial audit report（独立盲查）

**结论：拒绝当前冻结/发布。** 当前工作区的原件像素和正文字节 hash 可复核，但来源状态、空白页分类、学习稿映射、恢复记录和独立轮次不足以证明零遗漏或已解决。最大风险是 **P001-U01 的假解决**：当前 `source_units[RA10-P001-U01].status` 和所有关联 target 均为 `resolved`，而 `issues[RA10-ISSUE-01]` 仍为 `open`、`resolution` 为空，恢复计划也仍要求恢复。这不是已解决状态。

本报告只依据原件、manifest/ledger/current 状态、恢复计划、历史 draft 和直接打开的页图/分区图；没有采用其他 reviewer 的结论作为证据。报告是新增审计记录，不修改主正文或主账本。

## 1. source 身份和 hash

| 项目 | 观察 |
|---|---|
| task source | `input/pdf/实分析10(1).pdf`，7 页，SHA-256 `946871d69d4fe44aaa7f9c9355ec80da0df5e07d6886f1848ad9d94b20e09757` |
| project copy | `project/source.pdf` 实算同一 hash；与 manifest、RA10 task 登记一致 |
| rendered pages | 7 个页面文件，均 3306×4678；manifest 记录的 7 个 page hash 逐一与实际文件一致 |
| rendered regions | 42 个 2×3 重叠分区，manifest 中记录 hash 逐一与实际文件一致；p0006 的两个底部分区同 hash，p0007 的空白分区出现重复 hash，这与图像内容相容 |
| ledger binding | `ledger.json.manifest_sha256 = 1de9b12fc1c93911c16be77618feca0c24df31a804091abf683a715230558741`，实算 manifest hash 一致 |
| current artifacts | `source-transcript.md` 实算 `1766d35a3c7499c63a926cc54f244748b0b1827c322ea8807eac0be7e1dc8b66`；`study-notes.md` 实算 `32dca0751d06028eccb3877b42ad5b693a21db3cca217f1b1a8cf116535ddacf`；均与当前 ledger 一致 |
| target line hashes | 126 个 transcription target、217 个 study target 的行范围均在文件内，逐行拼接后与 `text_sha256` 全部一致（0 个越界、0 个不匹配） |

**限制：** hash 证明的是当前字节和像素没有被无声替换，不证明转写内容正确，也不证明代理实际完成了视觉阅读。

## 2. source/page/region 发现

直接打开 7 张整页图后，p0001–p0006 有数学笔迹，p0007 整页接近纯白；p0007 六个分区同样没有可读数学正文。manifest 的 `blank_candidate` 标出了 p0002-r3c2、p0004-r1c2、p0006-r3c1/r3c2 及 p0007 六区，但 `blank_status` 对全部 42 区仍是 `unreviewed`。当前 ledger 却把 14 个 page check 和 84 个 region check **全部记为 `assessment: content`**，包括这些候选空白区和 p0007；这使空白页分类与实际图像冲突。

具体风险：

- `RA10-P007-U01` 被记为 `status: resolved`，有 `T-0151`/`T-0153` 两个 `origin: source` target；但其正文仅是“第 7 页”标题和“页面整体接近空白”的来源说明，不是来自空白图的数学内容。该来源单元应被重新判为可审计的空白来源记录，而不应作为数学 source 内容单元。
- `RA10-P007-U01.study_target_ids` 列出 192 个学习 target；p0007 的空白图不可能是这些学习段的证据。这是最强的映射污染信号。
- p0002-r3c2、p0004-r1c2、p0006-r3c1/r3c2 也被 manifest 标作 blank candidate；至少应逐区给出 blank/content 的视觉理由，不能由批量“content”观察代替。
- 当前 source unit 的页级 bbox 覆盖整页，符合物理覆盖，但不能替代逐项内容单元；尤其整页状态 `resolved` 不应掩盖页内 open issue。

## 3. target/mapping 发现

当前 ledger 有 126 个 transcription target（其中 124 个带一个 source ID，2 个编辑性 target 无 source）和 217 个 study target（192 个带 source，25 个编辑性 target 无 source）。内部行 hash 全部自洽，但 study 映射在语义上高度可疑：**192 个带 source 的 study target 每一个都同时绑定 7 个 source page IDs**，包括空白的 `RA10-P007-U01`。每个七页 source unit 也反向列出同一批 192 个 study IDs，因此结构上可互相通过，语义上却无法说明每一学习行实际来自哪一页。

这会造成两类假通过：

1. 任意学习行都有“image:p0001…p0007”证据，导致看似全覆盖，实则失去页级定位；
2. P007 空白页被批量加入每个学习行，掩盖了真实来源遗漏与跨页边界错误。

应按学习段逐行恢复真实 source IDs；不应仅依赖当前双向集合相等来认证语义完整性。

## 4. P001-U01 假解决风险

直接打开 p0001 全页及 `autonomous-recovery/crops/p0001-f9cd5200fee2.png` 可确认顶部命题标题、`Prop.` 行、原像/可测表述和后续有限并公式存在不同清晰度与疑字。数学上下文足以提出候选，但不自动证明笔画读法。当前状态同时出现：

- `ledger.json`：`RA10-P001-U01.status = resolved`；其 19 个 transcription target 和关联 study targets 也均为 `resolved`；
- `ledger.json`：`RA10-ISSUE-01.status = open`，`related_ids = [RA10-P001-U01]`，`resolution = ""`；
- `autonomous-recovery/recovery-plan.json`：`content_resolved = false`、`unresolved_count = 1`、`status = ready`，要求至少两个候选、前向/反向数学检验和回原图；
- `current.json`/`audit-report.json`：`status = NeedsModelRecovery`、`audit_pass = false`、`content_resolved = false`。

因此不能将“target/status resolved”解释成疑点已解决。关闭 P001-U01 前至少需要：候选记录（≥2）、每个候选的局部图像指针、独立前向和反向检验、回原图决定、issue resolution、source/target 状态和两份正文同步更新；任何内容字节变化后 final-round 链从零重启。

## 5. recovery records / issue continuity

当前 `ledger.json` 的 `recoveries` 为空，`final_rounds` 为空；恢复计划只包含 1 个待处理记录 `RA10-ISSUE-01`。项目的 `audit/recovery-log.md` 说候选应位于 recoveries/unresolved，但这些目录/记录在当前 project 中不存在（仅有 recovery-plan 和一张 crop）。这意味着“恢复队列已生成”尚未变成“恢复已执行”。

`ledger-draft.json` 仍显示早期状态：6 个 open issues、4 个 unresolved recoveries、385 个 target，其中 6 个 target unresolved；其 recovery source IDs 使用 `RA10-P0001-U01` 等四位页号，而当前 ledger 使用 `RA10-P001-U01` 等三位页号。当前账本把这 6→1 的问题收缩和 4 条恢复记录消失解释不了：没有逐项关闭/重绑定记录，不能把早期疑点当作已解决。尤其 draft 的 I005/I006 还引用不存在的 `RA10-PP0005-U01`/`RA10-PP0006-U01`，说明历史草稿自身不可直接认证，但它暴露了 ID 清洗未完成的风险。

## 6. old draft / artifact 边界

任务登记明确 `previous_markdowns = []`、`previous_notes_status = not_provided`，所以不能声称完成旧 Markdown 对照。`ledger-draft.json` 的两个正文 artifact 路径是 `../source-transcript.md` 与 `../study-notes.md`，在 draft 所属 project 上一级并不存在；它们的 hash（`4b890fdd989612ffeb8608cb293e279ddb96f4c6ff4c633069b5bbac058ce030`、`80fdf0afa3474564e86bd919838e4ab38cde03810e8309eb94af78201bb0c1ca`）也不是当前 project 正文 hash。因此 draft 只能作为历史草稿/风险线索，不得作为当前冻结证据。

## 7. round/freeze gate

当前 `ledger.json.final_rounds = []`；`audit-report.json` 的唯一结构错误是 `FINAL_THREE_ROUNDS`，`current.json` 仍为 `NeedsModelRecovery`。即便 page/region 共有 pass 1+pass 2 的结构条目，也不能把它们充作冻结后的三轮全量独立复核。特别是 P001-U01 若有任何内容、颜色、来源映射、未决状态或恢复记录变化，第二遍和三轮链都必须重新从新冻结版本计数。

另有两份报告 snapshot 不同：`audit-report.json` 记录 `1fbcbeb00d3a0c663ca30b32e3ada655e31cbd9a99a6b4cf4bdd13ec01e90691`，`audit-reports/current.json` 记录 `5d519006a1d2270d3117bfc8df567595901b2656e589d7d026f4a8dac3a80ddb`。这不是内容错误的证明，但需解释报告版本关系，避免用旧 snapshot 的结论覆盖新正文。

## 8. 必须的恢复动作（给主协调者）

1. 保留 `RA10-ISSUE-01` open；把 P001 标题/命题/原像相关句列成至少两个视觉候选，逐字绑定 p0001 及定向 crop，分别做数学前向、反向检查，再回全页决定。
2. 把 p0007 重新登记为 blank（页面及六区），移除其作为数学内容 source 的泛化 study mappings；复核 p0002/p0004/p0006 的 blank candidate 区。
3. 从 `source-transcript.md` 和 `study-notes.md` 逐段重建真实 page-level source IDs，不接受 192 行×7 页的批量映射作为语义证据。
4. 统一三位/四位页号 ID，逐项对照 draft 的 6 issues/4 recoveries；每条消失的疑点必须有关闭证据或保留为 open。
5. 固定当前正文和 ledger 后，重新跑结构审计；完成第二遍全页/全区检查，再由此前未参与的三个新审阅者连续完成完整三轮。任何正文/映射/未决变化均归零计数。
6. 最终输出必须继续声明没有旧 Markdown 对照，且 `visual_reading_proven`, `zero_omission_proven`, `mathematical_correctness_proven` 在未满足前保持 false。

**本次 adversarial 结论：** 文件 hash 级别完整；语义映射和状态级别不可信；P001-U01 未解决；p0007 空白分类与映射冲突；无 recovery records、无 final rounds；因此当前不能提交或发布。
