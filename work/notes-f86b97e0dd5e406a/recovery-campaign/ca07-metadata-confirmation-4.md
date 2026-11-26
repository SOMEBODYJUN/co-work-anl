# CA07 第四遍完整复核之后的精确修改确认

本任务只有 Boss 明确发出开始通知、`audit/second-pass-4-merge/applied-result.json` 已存在后才启动。
只处理 CA07，仍是本篇原三名实际 gpt-6.2-sol/max 线程。不得再启动代理，不得操作 Git。
项目：`work/notes-f86b97e0dd5e406a/notes/CA07/project`。
只在自己的 `proposals/ca07_角色/metadata-confirmation-4/` 写新文件。

## 真实复核范围

先读取当前 ledger、content-plan、merge 的 explicit-edit-receipt 与 applied-result，记录它们的实际 SHA256。
核对两份正文与映射相对于本人第四遍报告完全相同：

- source-transcript.md：`376ba572a25a48a39487bbfb80ce96bdeaf4e405e4fb5c32e04255f6572e3b64`
- study-notes.md：`43c1bce76087b71ca5df2c9032e5fbda3ed8677e7d30ec4a41f615d0bb93e7ce`
- source-target-map.json：`d003ebfed40cfaa6f7dacc42abf1ea15a40b3f3b57b6eef357fe6c95ddc4efbd`

本人已经完成的第四遍 133 来源、160 目标、58 恢复、58 问题，以及真实页区/原生图检查，可以在严格哈希核对后沿用。
清楚区分此前实际打开的图、本次实际再开的图及本次机械验证；不得宣称本轮重新打开了全部图。
不必重复读取未变的正文或再次逐张扫描全部原生图。需确认任何自己尚未检查的实质改动；有必要时再回原图。
不要读取另两人的报告结论。Boss 的合并说明只作为待核对象，不作为通过依据。

本次精确修改为 R004、R011、R013、R022、R030、R045、R049、R050、R054、R055 及其对应问题：
共加 17 条直接来源，明确参数试取、长除求值条件、代数生成条件及伴随矩阵证明中的除法含义。
还将 active pass 1 观察指向视觉员当前的已核准页区记录。
逐条核对实际 after 记录，不只比对预期字段名。原候选、选案、其他证明与局部限定必须保留。
来源133、目标160、恢复58、问题58、正文与映射均不应改变。

## 自己报告的勘误

保留所有已冻结旧报告的字节。在新报告的相应观察里吸收自己的 post-second-pass-4 勘误：

- 视觉员：P4U13 是“使 M 是忠实”，P5U08 是忠实而有限生成在 U09。
- 数学员：P2U13 只写 ∀m≥n，右侧下一单元起 1；P4U22 原文为裸 Ab，另处才有带括 A[b]。
- 对抗员：P1 两支从左接点向右上/右下；P2 末 a0 后为上小点、下短曲及开口0。

每人保留自己的8页48区实查观察与布局，不抄另一个人的整套观察。
沿用的第四遍原图、候选判断与观察分别注明原报告路径和实际哈希。

## 冻结交付

写新的 `second-pass-report.json` 与 `second-pass-report.md`。
使用当前协议中的完整第二遍 JSON 字段，包括真实 reviewer_id/session_id、三文档首尾SHA、
完整 reviewed_scope、8页48区观察、58条逐条恢复判断、实际 findings。
增加 current_context_hashes_start/end，记录本次当前 ledger 与 content-plan。
每条改过的恢复给出本次独立确认理由；其余沿用本人完整第四遍结论时明确注明不变及哈希依据。
只有实际接受了全部58条且没有新发现时才填满 accepted_recovery_ids 并给空 findings。

报告范围是“完整第四遍实查 + 本次真实精确修改确认”，不能伪装成从未参与的新审稿人。
无论结果是否通过，都完成冻结文件并给 Boss 文件名、SHA256、实际检查与发现摘要。
冻结之后不要修改这些文件，后续真实终审由 Boss 另行给出快照通知。
