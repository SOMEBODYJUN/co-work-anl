# RA06 独立盲审清单（对抗审计）

本清单在读取 `recovery-team/visual` 与 `recovery-team/math` 结论之前建立；审计只以当前 manifest、integrated ledger、正文/旧稿、交接、recovery-plan、PDF/页区哈希和独立脚本核验为依据。

## A. 输入与版本

- [ ] assignment 的 source PDF 路径、页数、SHA-256 与 `project/source.pdf`、manifest 一致。
- [ ] manifest 的页/区域计数、bbox、区域 SHA-256 与实际文件一致；普通空白页/区状态可解释。
- [ ] integrated ledger 的 `manifest_sha256` 与 manifest 实际 SHA-256 一致。
- [ ] latest audit report 的 `snapshot_sha256` 可由 ledger/正文/证据快照重现；若不能，记录冻结链断裂。
- [ ] recovery-plan 的输入报告、source_pdf、unresolved_count、状态与最新 ledger/audit 一致。

## B. 台账结构与映射

- [ ] source_units、target_units、old_units、recoveries、issues、page_checks、region_checks 的 ID 唯一；状态与字段完整。
- [ ] 每个 source_unit 至少有页、bbox、证据、region、transcription/study 目标；每个 target_unit 反向指向存在的 source；孤立/虚构 ID 标记。
- [ ] source↔target 双向映射一致；`mapping.json`、`source-units.json` 与 integrated ledger 一致。
- [ ] old_units/old_ids 准确描述 rebuild 旧稿去向；不得以空数组掩盖旧稿中已存在且被改写/删除的单元。
- [ ] unresolved source/target/recovery/issue 的数量、状态和相关文本/证据能互相闭合；resolved 不能仍留未决内容。

## C. 正文与证据同步

- [ ] transcription/study 正文中每个 target 的行号有效且文本哈希等于 ledger `text_sha256`。
- [ ] 正文的黑/蓝/红标记符合工作合同；未完成原稿证明和补证边界没有互换。
- [ ] 现正文与旧稿、handoff、editorial-record 的变更有可追踪记录；旧稿没有被误当作当前稿。
- [ ] recovery/issue 的 selected candidate、resolution 与正文实际字串一致；候选仍 unresolved 时正文不得伪装确定。
- [ ] page_checks/region_checks 覆盖全部非空页区、source IDs 与实际单位一致，未把空白区当内容或漏记跨区内容。

## D. 数学与内容完整性（独立检查）

- [ ] 每页的源单元与正文按页序覆盖；关键定义、公式、证明、例题、旁注和原待填位置没有漏项。
- [ ] 补证/纠错明确标为新增；原稿原意、符号和未完成处保持可区分。
- [ ] unresolved 条目有至少两个候选、原图回查和正反数学检查记录；若 recovery-plan 要求而记录缺失，标为失败。
- [ ] 颜色标记、内容状态、问题状态和审计声明（audit_pass/content_resolved）相容。

## E. 证据/哈希与发布门禁

- [ ] ledger artifacts 的记录哈希与当前文件逐一相等；文件改动后未更新哈希要报错。
- [ ] source/target `text_sha256` 与正文实际目标片段相等；行号漂移或重复 ID 要报错。
- [ ] final-round 快照哈希在内容/ledger 改变后应失效；同一快照重复三轮需解释并在内容变更后重开。
- [ ] audit report 不得宣称零遗漏/数学正确/视觉已读，除非证据字段和审计状态支持。
- [ ] recovery-plan 的 tool_blocked/manual_intervention 标志与实际是否具备 crops/图像工具相容；有图像证据却仍停在阻塞要报错。

## F. 对抗性“假解决”扫描

- [ ] 已写蓝色补证但 source/target 仍 unresolved，或反之。
- [ ] issue 已 resolved 但对应正文/哈希/候选仍未同步。
- [ ] old draft 被替换/改写但 old_units=0 或 mapping 没有追踪。
- [ ] ledger 与正文真实文本、颜色、行号、路径不一致。
- [ ] 恢复候选只在证据/研究文件中出现，未进入正文或进入正文却未留证据链。
- [ ] 未决行被数学补证“合理解释”而冒写为已确定原文。

## G. 报告要求

- [ ] 每个发现给出文件路径、ID、证据哈希关系、影响和具体修复建议。
- [ ] 明确区分阻断发布的硬问题与可接受的历史/审计说明。
- [ ] 本审计不修改主 ledger、正文或主 audit report；只写本目录的 checklist 与 adversarial report。
