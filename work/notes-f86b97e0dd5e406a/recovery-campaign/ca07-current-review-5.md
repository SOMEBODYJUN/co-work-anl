# CA07 当前候选第五次完整复核（终审发现合并后）

仅继续当前 CA07 固定三人组。不是下一篇，也尚未开始新的终审。三份 e5ab9b2ae651 实际终审已全部冻结，其有发现链作废。正式输入只由 Boss 修改，代理只写自己的新目录 `post-final-current-review-5/`；不得 Git、不得改既有哈希文件、不得启动其他代理。

## 当前具体修订

1. T037/S016 将下标比较的“同前一行”改成“同上文 D 式右侧”；原第3页中间隔有列式。T037 新增 P003-U06。
2. T060 明引黑弯箭两端等式，新加 P005-U04/U05；T068 明引上行 t 的贯横，新加 P005-U18。现有源目标边总数 756（转写385、学习371）。
3. R026/I026 补 P004-U11 与其800图，并明写由(2)的有限性和 C=A[b] 得到(3)的包含及有限性。
4. R056/I056 明列 f(b)=0、非零系数环及正次数首一式，先做长除再求值消商项；以 f=g=T、b=1 检验去掉零值条件不成立。
5. 当前 pass1 改为视觉员自己冻结的 corrected-observations-2.json，只精确更正 P5r2c1 上斜下圆分隔。其 native crop bbox 与 source-unit bbox 现已分开登记。
6. 旧 pass2 从生效的 plan.observations 中明确撤下并归档。对抗员已另存旧观察的真实勘误：P1集合下一行根句、下一物理行是题头；P5r3c1 多、项、式三字后另有由形末团。当前候选需要新的实际第二遍报告，不能拿旧接受结论绑定新两稿。
7. R019/R032/R037 的问题描述附本轮相关改动，候选原文和选案不变。全部 source/target/recovery/issue 重新标为等待当前复核；issues 使用 schema 的 open 状态，不代表发现新的58个内容问题。

## 本轮真实工作

独立重新完整读当前两稿、133S/160T的语义对应和全部58R/58I（正向、反向、候选、来源、局部保形）。核每个直接引用的真实源边，不能仅验证已有边互逆。核当前全部8页48区的pass1观察，以及拟绑定pass2的8页48区，尤其三个物理观察更正。

可以延用本人刚完成的 e5ab 终审原图全量实读，以及本人此前已实际看的133张原生800来源单元；但必须核对同一原件和字节并准确注明复用，不声称本轮未开的图是重新看过。对所有本次改动所据原生图实际重开：P1U09/U10、P2U10/U11/U18、P3U06/U10、P4U10/U11、P5U04/U05/U06/U12/U18/U19。必要时追加1200或整页/分区，全部如实记 path、真实裁图框/源单元框区别、SHA与所见。

把全部实际新发现返回。没有发现才逐项实际接受，不能预填通过。两稿正文/映射起止SHA必须是下列当前值；另记实际开始/结束 ledger 与plan SHA，不能冒充报告绑定后才生成的哈希。

## 交付

目录：`project/proposals/ca07_ROLE/post-final-current-review-5/`。
每人保存 `second-pass-report.json`、`second-pass-report.md`、实际开图日志。JSON沿用通用协议第二遍字段：reviewer_id/session_id、document_hashes_start/end、reviewed_scope的完整source/target/recovery/issue清单、完整pages/regions、accepted_recovery_ids、逐条58 recovery_reviews、findings。

对抗员为真实非作者；其无发现完整当前报告才可由Boss通过 accept_note_second_pass.py 绑定。页区观察可采用本人 corrected-observations.json 中已经实核的准确文字，须标明本轮对当前两稿与所有台账的独立复核，图像相同字节复用的来源。视觉员和数学员各自独立确认当前完整范围及8处合并，不借其他人的新通过结论。

旧报告/源先/勘误已冻结，均不得改字节。三份当前确认完成后，Boss才会接受第二遍并给出新终审快照；之后三人各自重新源图先读及全量终审。

## 当前实际版本

```json
{
  "candidate_snapshot_sha256": "840ef895e825e4e5abb554db179747ec727623518e73f9b7eca7c954ed3111ef",
  "document_hashes": {
    "source-transcript.md": "bd99e4b49247d96aad42efb7178c0bf00bab9afd75ee5327d7fd4b694be49905",
    "study-notes.md": "90102801c76a6c5e39c9b2d3e7e9b79b1b6fe026373e66b64ebdf8fb6c916e21",
    "source-target-map.json": "4698a4d731b9cfd0141f2adc9f4bd58e6bd464b7be406dbe1214af45e9fbf974"
  },
  "ledger_sha256": "8bede780c43d40f73e5c58fd118ecd00e99624f9a633ed16d85dd3d8e88c0d0d",
  "content_plan_sha256": "1b25d84a5dab43e815ae2aa429f1736c11fe4eaef85459e0474b7fca636896ae",
  "project": "work/notes-f86b97e0dd5e406a/notes/CA07/project",
  "protocol": "work/notes-f86b97e0dd5e406a/recovery-campaign/current-note-agent-protocol.md",
  "decisions": "work/notes-f86b97e0dd5e406a/notes/CA07/project/audit/final-e5ab9b2ae651-merge/boss-decisions.json",
  "applied_result": "work/notes-f86b97e0dd5e406a/notes/CA07/project/audit/final-e5ab9b2ae651-merge/applied-result.json"
}
```
