# RA10 adversarial blind checklist

**审计角色：** RA10 adversarial / independent blind check
**审计对象：** `project/` 当前工作区；只新增本目录文件，不改正文、ledger、manifest、审计报告或恢复队列。
**输入边界：** 原件 `source.pdf`、`manifest.json`、当前 `ledger.json`/`current.json`/`audit-report.json`、`ledger-draft.json`、`autonomous-recovery/recovery-plan.json`、当前两份正文及实际页图/分区图。未把其他 reviewer 的结论作为证据。

## 必查项目

- [ ] **source identity**：任务来源、上传名称、页数、字节和 SHA-256；`source.pdf` 与任务登记及 `input/pdf/实分析10(1).pdf` 三方一致。
- [ ] **manifest/render**：7 页、400 dpi、3306×4678、2×3 区、重叠 0.12；页面图与区域图逐一核 hash；检查 blank_candidate/blank_status 与实际图像是否一致。
- [ ] **source units**：每页是否恰有一个来源单元；来源单元状态是否能与疑点/空白状态相容；特别检查 P001-U01 的“resolved”是否掩盖开放 issue，以及 P007 空白页是否被当作有内容页。
- [ ] **transcription targets**：每个 target 的行号、字节哈希、source_ids、origin、evidence_ids；从正文行反向核到 target，再从 source unit 正向核回 target。
- [ ] **study targets**：检查是否存在不加区分地把同一学习行绑定到全部物理页的泛化映射；空白页不得成为数学内容的来源。
- [ ] **recovery records**：恢复记录是否存在、是否与当前 source/issue IDs 相同、是否含至少两个候选、前向/反向数学检验、回原图证据和最终状态；不能仅凭 recovery-plan “ready” 计作完成。
- [ ] **issues**：每个未决是否有合法 related_id、证据、候选和 resolution；open issue 不得与 source/target `resolved` 状态冲突；旧疑点不得无审计地消失。
- [ ] **page checks**：每页是否有 pass 1+pass 2，空白页是否按 blank 评估；检查者、session、evidence、观察范围是否完整。
- [ ] **region checks**：每个 manifest region 是否有 pass 1+pass 2；blank_candidate 区不得仅凭“content”文本通过；重叠区和页边必须有回看证据。
- [ ] **old draft / prior state**：`ledger-draft.json` 的 artifact 路径、哈希、旧 source IDs、open issues/recoveries 与当前版本逐项对照；路径越界、失效 hash、ID 改名均需标明，不能混作当前证据。
- [ ] **hash/version gate**：实际文件 hash 与 ledger/manifest 完全一致；audit report 的 snapshot 与当前报告/正文版本关系可解释；正文修改后 final-round 计数必须归零。
- [ ] **rounds**：作者初读、第二遍全区检查、冻结后连续三轮全量独立复核分别计数；当前 ledger 的 `final_rounds` 不能空而报告“通过”。
- [ ] **P001-U01 adversarial trap**：即使候选在数学上通顺，也必须逐笔画与回原图核验；命题标题、`Prop.` 行和“原像/值域”表述保留候选/未决，不能把蓝色补全或标准定理当黑色原文。只有 issue resolution、target status、source status、正文红色疑点和恢复证据同步后，才允许关闭。

## 判定原则

1. 结构脚本的通过只能证明文件结构和引用可计算，不能证明真的看清了字或证明数学无误。
2. “source/target resolved” 与“issue open”同时出现时，按未决处理，并追问状态是否是伪解决。
3. 任何疑点数量、ID、正文、颜色、来源映射或哈希发生实质变化，都使既有 final-round 链失效。
4. 空白页必须成为可验证的空白观察；不应被批量映射成所有学习段的来源。
5. 没有旧稿时不得捏造 old-note 对照；若存在早期 draft，只能作为历史草稿，必须明确不具当前冻结资格。
