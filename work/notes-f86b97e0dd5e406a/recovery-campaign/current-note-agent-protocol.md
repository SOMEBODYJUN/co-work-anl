# 当前篇独立读图与复核交接格式

本文件仅说明机械交接格式，不提供任何课次的正文、候选或审阅者身份。
每篇重新从自己的原 PDF 开始，由 Boss 指定的三个真实新线程处理；同篇完成全部阶段后退出。
模型为 gpt-6.2-sol，推理强度 max。不得再启动子代理、不得操作 Git、不得处理其他篇。
只写本线程自己的 project/proposals/角色目录。正式正文、台账与发布由 Boss 整合。
新文本记录在上报或登记哈希前以单个换行结尾；哈希已经声明或冻结的原始记录不得再改字节。

## 初读

在查看他人正文、候选或报告前，按物理页顺序实际打开每张整页图及每页全部重叠分区。
保存 source-first-reading.md，逐页写内容顺序、跨区衔接、页边、重复、删改、原留空、普通空白。
分区观察只写该张分区图中实际可见的字句或片段。整页读到的内容不能直接搬成每区观察；
只露尾字就标明尾字，跨区单元要分别说明各区所见部分。版面中的物理行数以原页为准，
不能把数学推导的步骤数、Markdown换行或目标块数当作原纸的行数。
实际打开每个分区后及时记下该区观察，最终汇总前再逐条对照区域边界；
复核页区记录时要核其文字陈述的位置和版式，不能只检查记录条数、关联ID与文件哈希。
程序生成图片不等于模型已看图；记录真实 view_image 次数及路径。
普通空白不当作红色待填；原明示待证与其后留空合为一个待填位置。
每个不清楚的字、上下标、商环/理想记号、箭头及证明缺步都列候选，回原 PDF 做 800 dpi 定向图；
必要时 1200 dpi。不得把 400 dpi 图片放大后声称是 800 dpi 原 PDF 渲染。
裁图 bbox_px 使用 manifest 基准 DPI 坐标，换算点坐标后 get_pixmap(dpi=800/1200, clip=...)。
每条裁图登记 page_id、bbox_px、dpi、path、sha256，并实际打开。
裁图索引使用 JSON 数组，或含 `crops` 数组的对象；`path` 始终相对当前 project 根目录。
候选记录中的 `evidence_paths` 同样使用 project 相对路径，便于 Boss 登记真实文件而不猜测图号。

所有三人的独立初读记录完成后才由 Boss 合并。原文错误保真照录，学习稿就地蓝色订正。
“直接可读”“上下文恢复”“原稿错误”“未能裁决”必须区别。
在有效依据下可以选择上下文恢复，但不能把仍无决定依据的内容设为已完成。
正文中不跳过词间的单独墨团；若能读而有删改，记录原字及删改性质。
对指标、上下标和短笔，先逐笔判断，再作数学规范化；例如纸面只有点迹或短横时，
不能把由索引范围恢复的完整数字说成直接看见，必须就地说明原笔迹与恢复理由。

## 视觉员交接

保存 sources.json，数组每项：

    {"id":"当前篇-P001-U01","page_id":"p0001","bbox_px":[x0,y0,x1,y1],
     "label":"具体内容位置及所见信息","status":"resolved 或 unresolved"}

每个定义、条件、公式、实质证明行、例题、旁注、可读删改、原待填各有来源单元。
空白页不制造来源内容单元，但必须有页区观察。
保存 transcription-blocks.json，数组每项：

    {"text":"实际 Markdown 段落","source_ids":["对应来源ID"],
     "origin":"source/supplement/editorial","status":"resolved/unresolved",
     "explanation":"原稿、编辑说明或补充的真实来源"}

source 保持原序与原错误；supplement 明示蓝色说明；editorial 的 source_ids 必须为空。
几行相关公式可以共用一目标块，但来源仍保持细分。
每一来源必须在转写中出现。正文用 Obsidian 的 $...$、$$...$$；callout 每行含 >。
同一来源在索引、总结表、跨页原文提示中重复使用时，每个实际目标都要登记源边，
不能因它已经指向别处而省略新目标。机械互逆只能确认已有边，不能发现语义缺边。
字形比较与内容来源要区分：跨页比较的蓝注同时给实际比较图的 `evidence_paths`，
由 Boss 换成已登记 evidence_ids；明确引用另一页原句/原式时，将对应来源单元也列入 source_ids。
人名、术语、缩写不能只凭定理指称默默排成标准拼法；逐处看实际字母或笔形，
若采用规范名而原写法有可辨区别，局部蓝注说明。普通草写与漏写不能判清时，
记录可见形状及合理的连笔候选，不强判作者拼错，也不声称标准字母均逐一可见。
蓝注若直接复述另一位置的原字母串、原式或原句，该位置就是此蓝注的内容来源；
即使已附比较图、已给别的目标登记来源边，也仍须为这个目标单独登记真实来源边。
来源框的墨迹覆盖检查不能证明逐字转写完整。首遍建立来源单元后，第二遍还须实际逐张看
由原 PDF 直接渲染的全部来源单元 800 dpi 图（Boss 可用 tools/render_note_units.py 准备），
逐 ID 记录独立词组、连接字、重复、原错误、上下标、括弧和边字是否全部落入转写。
裁图存在及哈希相符都不能代替实际看图；必要时另作 1200 dpi 和同手字形对照。
模型补证用蓝色 note/info callout，原明确留空用红色标记并紧接蓝色解答。
callout 标题后放一行单独的 `>`，正文与表格才正常分开。展示公式的 `$$`
只在外侧加空行，两个定界符之间不能插空行。表格内数学竖线用 `\vert{}`
等 TeX 命令，不写会切开单元格的裸竖线，也不在闭合 `$` 前留下空格。
目录、编辑标题与来源解释不要伪装成原稿。

观察文件 observations.json 的格式：

    {"pages":[{"page_id":"p0001","assessment":"content/blank/unresolved",
               "observation":"整页实际核对点","layout_observation":"版式及跨区情况"}],
     "regions":[{"region_id":"p0001-r1c1","assessment":"content/blank/unresolved",
                 "observation":"该区首末、公式、边注、衔接与空白的具体观察"}]}

## 数学员交接

独立看完所有原页区并保存首读后，按原数学结构给完整学习稿提议。
保留所有 A/B 路线、例题及原证明细节；先放工具，再放其应用；题目与解答相邻。
已有文字不能从别篇复制，不能把数学上合理的内容冒充读到的字。
每个模糊处至少两个实质候选，正向推导、逆向验证或反例、前后引用与记号对照。
记录条件、定义域、同态方向、下标和理想/商环运算的类型是否相容。
study-blocks.json 可用 source_ids（Boss 合并后提供）或先用 page_ids/source_labels 定位。
蓝色补证必须写实际论证，不能只说“标准可得”“容易证明”。
需要调用的外部标准结果应明确说明；不把其证明假装为原稿内容。

## 对抗员交接

保持非正文作者身份。独立初读后对照初稿，记录所有遗漏、错字、错误数学和不当归属。
recoveries-proposal.json 每项应有：problem、至少两个 candidates、选取结果或未决、
forward_validation、backward_validation、return_to_image、具体裁图路径及页区范围。
两方向需不同的检验方法。有限样例只能反驳某候选或检查一致性，不能证明普遍命题。
完成初稿后，正式第二遍须再次核对全部原页区、两稿、所有来源/目标、恢复与问题记录。
second-pass-report.json 写实际 reviewer_id、开始与结束的两份正文/mapping SHA，
每个已复核 recovery_id 的结论，以及完整 pages/regions 实查观察。
没有完整复核或仍有实质发现，就明确返回 findings，不能预先填空发现。

恢复提议可统一使用以下字段；不确定处保留实际未决，不能为了适配格式编造结论：

恢复提议也可用完整 Markdown 交付，由 Boss 机械转入台账。候选、正反检验、实际回图与证据路径必须齐全。
全篇公共文件哈希和实际打开的图清单集中记录一次，各条引用相关图即可；不要在每条重复整篇历史或全部工件。

    {"local_id":"本线程自己的记录号","page_id":"p0001",
     "source_labels":["精确到原行的定位"],"source_ids":[],
     "problem":"需要判定的具体字、公式、条件或证明省略",
     "candidates":[{"id":"c1","text":"候选读法及含义","evidence_paths":["真实图或报告路径"]},
                   {"id":"c2","text":"另一实质候选","evidence_paths":["真实图或报告路径"]}],
     "selected_candidate_id":"已有决定依据时的候选ID，否则null",
     "confidence":"实际置信度及仍需保留的限定",
     "forward_validation":{"method":"具体正向方法","inputs":"实际前提","result":"实际推导"},
     "backward_validation":{"method":"不同的逆向方法","inputs":"候选后果","result":"类型/反例/后文引用检验"},
     "return_to_image":{"observation":"实际字形、位置和作者记号的检验","evidence_paths":["实际800/1200dpi图"]},
     "evidence_paths":["支撑整个记录的真实文件"]}

非作者第二遍完整 JSON 使用以下字段，观察格式与初读相同；完整 ID 清单从实际当前 ledger 核对后登记：

    {"reviewer_id":"实际线程ID","session_id":"实际线程ID",
     "document_hashes_start":{"source-transcript.md":"实际SHA","study-notes.md":"实际SHA","source-target-map.json":"实际SHA"},
     "document_hashes_end":{"source-transcript.md":"实际SHA","study-notes.md":"实际SHA","source-target-map.json":"实际SHA"},
     "reviewed_scope":{"source_unit_ids":[],"target_unit_ids":[],"recovery_ids":[],"issue_ids":[]},
     "pages":[],"regions":[],"accepted_recovery_ids":[],
     "recovery_reviews":[{"recovery_id":"真实ID","decision":"接受或实际发现","reason":"独立核验依据"}],
     "findings":[]}

示意里的空数组不能代替实查清单。第二遍需同时保存详细叙述报告，记录正文与映射核对、
每条恢复的独立判断及真实新增发现。首遍完成后 Boss 会明确通知第二遍的当前版本。

## 最新快照的终审

只有 Boss 明确给出冻结 snapshot、scope 和两份正文 SHA 后才开始。
本战役按用户指定的固定三人跨阶段独立复核，不声称终审者从未参与该篇。
每人先重新看全部原页区并写 source-first-reread.md，再对冻结两稿与完整 scope 逐项核对。
不能借用他人的通过结论。不得编辑正式文件或他人报告。
报告包括 snapshot_sha256、document_hashes、scope、page_notes、findings 和实际 evidence_ids。
有新发现必须报告；Boss 修订后旧终审链失效。只有最新内容的三份无新发现独立记录才可封链。
正文以外的审计结构检查不能替代视觉/数学检查。

终审记录写在自己目录的新子目录 `final-快照前12位/`，不覆写前阶段记录。
先实际逐张重看原整页与全部重叠区（不以低清缩略接触表代替），再保存
`source-first-reread.md`，最后核对两稿和完整范围并保存 `final-report.json`。
终审 JSON 格式：

    {"reviewer_id":"实际代理ID","session_id":"实际代理ID",
     "snapshot_sha256":"Boss给出的冻结快照",
     "document_hashes_start":{"source-transcript.md":"实际哈希","study-notes.md":"实际哈希","source-target-map.json":"实际哈希"},
     "document_hashes_end":{"source-transcript.md":"实际哈希","study-notes.md":"实际哈希","source-target-map.json":"实际哈希"},
     "scope": "将实际完整核过的冻结scope对象放在这里，不是字符串",
     "findings": "真实发现ID数组；只有实查没有新发现才为空数组",
     "evidence_ids":["全部实际重看的image:页/区ID及实际使用的artifact:裁图ID"],
     "page_notes":[{"page_id":"p0001","observation":"该物理页实查的具体内容及数学/来源核对"}],
     "notes":"本轮实际复查范围、证明检验、结论及此前参与此篇的披露",
     "blind_reading":{"path":"自己source-first-reread.md的项目相对路径","sha256":"真实文件字节哈希"}}

上述示意中的说明字符串不可原样当数据填写。实际发现须有具体说明，不能为了封链预填通过。
不把其他人的终审报告或“已通过”当证据，不更改正文、ledger、既有证据、冻结文件或其他人的记录。
三份实际报告由 Boss 按顺序登记与封链；任何实质修订后，以新快照重新完成三份独立终审。
