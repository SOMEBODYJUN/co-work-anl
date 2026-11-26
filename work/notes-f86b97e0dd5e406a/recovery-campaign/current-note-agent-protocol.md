# 当前篇独立读图与复核交接格式

本文件仅说明机械交接格式，不提供任何课次的正文、候选或审阅者身份。
每篇重新从自己的原 PDF 开始，由 Boss 指定的三个真实新线程处理；同篇完成全部阶段后退出。
模型为 gpt-6.2-sol，推理强度 max。不得再启动子代理、不得操作 Git、不得处理其他篇。
只写本线程自己的 project/proposals/角色目录。正式正文、台账与发布由 Boss 整合。

## 初读

在查看他人正文、候选或报告前，按物理页顺序实际打开每张整页图及每页全部重叠分区。
保存 source-first-reading.md，逐页写内容顺序、跨区衔接、页边、重复、删改、原留空、普通空白。
程序生成图片不等于模型已看图；记录真实 view_image 次数及路径。
普通空白不当作红色待填；原明示待证与其后留空合为一个待填位置。
每个不清楚的字、上下标、商环/理想记号、箭头及证明缺步都列候选，回原 PDF 做 800 dpi 定向图；
必要时 1200 dpi。不得把 400 dpi 图片放大后声称是 800 dpi 原 PDF 渲染。
裁图 bbox_px 使用 manifest 基准 DPI 坐标，换算点坐标后 get_pixmap(dpi=800/1200, clip=...)。
每条裁图登记 page_id、bbox_px、dpi、path、sha256，并实际打开。

所有三人的独立初读记录完成后才由 Boss 合并。原文错误保真照录，学习稿就地蓝色订正。
“直接可读”“上下文恢复”“原稿错误”“未能裁决”必须区别。
在有效依据下可以选择上下文恢复，但不能把仍无决定依据的内容设为已完成。

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
模型补证用蓝色 note/info callout，原明确留空用红色标记并紧接蓝色解答。
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

## 最新快照的终审

只有 Boss 明确给出冻结 snapshot、scope 和两份正文 SHA 后才开始。
本战役按用户指定的固定三人跨阶段独立复核，不声称终审者从未参与该篇。
每人先重新看全部原页区并写 source-first-reread.md，再对冻结两稿与完整 scope 逐项核对。
不能借用他人的通过结论。不得编辑正式文件或他人报告。
报告包括 snapshot_sha256、document_hashes、scope、page_notes、findings 和实际 evidence_ids。
有新发现必须报告；Boss 修订后旧终审链失效。只有最新内容的三份无新发现独立记录才可封链。
正文以外的审计结构检查不能替代视觉/数学检查。
