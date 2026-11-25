# RA11 对抗审计盲审清单（第一轮）

- 审计者：`/root/ra11_adversarial_audit`
- 轮次：独立第一轮；未读取视觉恢复者或数学上下文恢复者的结论。
- 审计范围：`ledger.json`、`manifest.json`、`current.json`、`audit-report.json`、`autonomous-recovery/recovery-plan.json`、`source-transcript.md`、`study-notes.md`、`audit/` 下现有证据、14 页原图/页区索引、`reviews/` 中已有第二遍记录。
- 目标：发现 RA11-P001-U01、RA11-P005-U01 的假解决和遗漏，并检查 source/target/old/recovery/issue/page_checks/region_checks、正文与哈希是否同步。

## 独立检查项目

1. **现存未决项**：逐项核对 issue 状态、related_ids、evidence_ids、resolution；确认是否存在 recoveries 候选、正反向验证、未完成记录。
2. **source→target 双向链**：核对 14 个 `source_units` 的页号、六分区、bbox、`transcription_target_ids` 与 `study_target_ids`；对照每个 target 的 `source_ids`，检查孤立、反向多挂、状态冲突和未覆盖。
3. **old_units/旧稿去向**：确认 `old_units` 是否为空且与 manifest/current/notes assignment 的 previous_markdowns 一致；若为空，确认没有旧稿 ID 被正文或映射引用。
4. **页面/分区覆盖**：检查 28 个 page checks 与 168 个 region checks 是否每页两遍、每区两遍、均有原图证据；注意页面边缘、空白/内容分类、跨区接续及页边符号。
5. **正文同步**：逐查 source transcript、study notes、映射字段、颜色标签、红色疑点和 ledger 的 unresolved/open 状态是否一致；数学顺畅不能替代原图证据。
6. **证据链与哈希**：核对 `manifest_sha256`、artifact SHA-256、正文 artifact 记录、审计 report 的快照；发现任何正文改动而无重新哈希、crop 未登记或登记路径不实即记为失败。
7. **冻结门槛**：检查 recoveries 数量/候选数、final_rounds、审计锁定正文哈希、`audit_pass`/`content_resolved`/`unresolved_count`。当前任何一项缺失均不能提交或切换下一篇。
8. **原图复核计划**：对 p0001 与 p0005 先看整页，再查所有六区和页边；对候选符号至少保留两个候选、前向/反向检验、作者记号比对及 800 dpi（必要时 1200 dpi）裁图。该项在本盲审记录写入后继续执行。
