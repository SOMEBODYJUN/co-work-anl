# CA07 当前内容复核第四版任务

同篇原三名实际 reviewer 继续；模型 gpt-6.2-sol / max 不变。本任务为更新后第二遍的继续，不是终审。只写本人 proposals/ca07_ROLE/second-pass-4/，不改正式稿、台账、plan、其他人记录或 Git。不要阅读其他人的第三遍或第四遍报告。冻结的本人历史记录可读。

## 已冻结当前正文

- source-transcript.md SHA256 376ba572a25a48a39487bbfb80ce96bdeaf4e405e4fb5c32e04255f6572e3b64
- study-notes.md SHA256 43c1bce76087b71ca5df2c9032e5fbda3ed8677e7d30ec4a41f615d0bb93e7ce
- source-target-map.json SHA256 d003ebfed40cfaa6f7dacc42abf1ea15a40b3f3b57b6eef357fe6c95ddc4efbd

133 source / 160 target / 58 recovery / 58 issue / 8 page / 48 region；当前752条双向源目标边。正式状态仍未通过；不得预填通过。

## 实际工作

1. 核当前三SHA，完整重读两稿、所有133来源/160目标的当前落点、58恢复/58问题（包括候选和两向验证），逐项核映射的真实语义；不能只看11处diff。
2. 对改动影响的全部原单元、同手比较与具体前提实际重开800以及必要1200。当前已更新的target：T009,T010,T036,T066,T072,T-V015,T-V016,S016,S030,S035,S037。更新的R/I：006,007,009,020,026,028,029,030,031,032,033,035,039,041,048,058。正文未新增命题；涉及原弧形、两列省写、V内孤弧、右分子T的限定及实际前提来源。
3. 原PDF、8页48区和未变单元没有重渲。可核其SHA不变后沿用本人刚完成第三遍实际打开的原图观察，再对照完整当前内容；必须给出本人原日志路径/SHA、准确区分本轮实际新开和历史同图实读，不能称8/48全为本轮新开。该方式是本次持续第二遍的当前内容完整复核，不是复用旧结论。未改处仍需按当前文句逐ID重核。
4. 若自己第三遍的粗略页区或focused摘要把原字与数学含义混写，本版必须据自己实际图证修正并注明。不要用粗略摘要覆盖已有精细原字。视觉员自己的两条独立勘误应带入；数学员已有Boss指出的7处粗写需实开相应图和单元改准。
5. 写 second-pass-report.json 与 .md：reviewer_id/session_id本人，document_hashes_start/end三文件，reviewed_scope的source_unit_ids/target_unit_ids/recovery_ids/issue_ids全量；8pages/48regions逐条assessment/observation和source-image SHA、阅读方式；58R/58I的当前逐条判断；实际打开清单及SHA/观察、历史复用自己的出处；findings按实际结论填写，accepted_recovery_ids只列真正接受者。非作者报告须兼容 tools/accept_note_second_pass.py，工具只由Boss在三份都完整后调用。
6. 不需无风险重复检验。出现具体新问题则报候选/图证/两向检验，不为赶通过隐藏。不变的已明确原笔不用再添加一层同义保形叙述。完成必要范围后校对自有报告内部一致性，冻结文件并回报SHA。

本轮只有第二遍。随后另发冻结快照，三名各自新开8页48区，按原图优先做三轮独立终审。
