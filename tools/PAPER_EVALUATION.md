# 数学论文评价：使用和记录规则

在 Work / Codex 中这样说即可：

> 用本仓库的论文评价流程审查 `paper.tex`。原题在 `target.md`；另读附录 `appendix.tex`。这份稿件尚未公开。先给投稿前最值得修的三个问题，再给完整证据。

Agent 应执行下面的两步，与中间的数学评审一起完成。Python 固定输入、检查记录、生成报告；证明重读、文献检索、判断和复核由实际评审者或 Work Agent 执行。单独在终端运行第一步会生成任务包，不会启动模型或返回编造的结论。

```bash
python work.py research evaluate --paper paper.tex --include appendix.tex --target-file target.md
# 读取命令返回的 task，复制 review-template.json 到 review.json，完成评审。
python work.py research evaluate --run review-<id> --report /path/to/review.json
```

- `--include` 可重复；接受 UTF-8 LaTeX、BibTeX、Markdown、纯文本，以及含文字层的 PDF。PDF 依赖 Poppler 的 `pdftotext`；扫描件需先 OCR。数字、符号、图表仍应对照原文件。程序不会编译或运行稿件。
- 文件路径相对于调用时的目录。LaTeX 依赖请显式列出；静态扫描会提醒常见的缺件，无法枚举所有宏展开路径。缺关键证明时保留疑点。引用独立原题时优先传 `--target-file`。
- 默认稿件未公开。只有稿件已公开且明确允许时用 `--visibility public`。私稿检索只能用既有公开信息（例如经典定理名、公开原题和公开参考文献），不要把稿件、其新主张或未公开措辞送到外部服务。仓库工具本身离线。
- 审查包和输出默认位于已忽略的 `research/paper-evaluations/`。需要恢复时用 `--run review-<id>`，无需重建。不改原稿、不登记数学对象、不自动推送。实质改稿重新建包：不要手改冻结副本。需要公开时单独选择可公开的报告，勿提交快照目录。

## 审查记录

保留模板顶层字段；删除没使用的示例行。JSON 直接采用 UTF-8，LaTeX 反斜线在 JSON 字符串中写成双反斜线。空数组表示该项无可记录内容；不确定的判断须写其原因。所有自述仍要经过实质核查，程序只能检查结构、版本和定位。

- `tracks` 三项分别为 `proof`、`prior_art`、`value`。填写真实评审者标签、核查范围，状态为 `completed`、`partial`、`not_run`。同一人兼任时保留同一标签；未运行也要填标签（可填「无」）和原因。
- `evidence`：给每条证据分配 `E1` 等唯一 ID。稿件证据为 `kind: input`，用冻结包的来源 ID 和 1 起算的含端点行号；文献证据为 `kind: public`，填公开 HTTPS URL、题名、精确定位（页码、定理号、节等）、查阅日期及支持什么。检索记录列实际用过的查询或来源及结果。PDF 的页标记可在编号文本中定位。
- `claims`：只登记承重或贡献性的主张，逐项列出陈述、假设、量词和结论，`source_evidence` 必须指向本稿及其附件。判断原题对应时，引用冻结原题或公开原题。另填 `target.overclaims_target`（布尔值），仅当稿件把已有覆盖写得比实际更广时为真。诚实说明的部分结果可以送专家。目标状态：`exact`、`partial`、`variant`、`not_checked`、`no_external_target`。
- `proof`：`no_gap_found`（在声明范围内未发现缺口）、`gap`（推理断裂）、`refuted`（主张本身有反例）、`not_checked`。缺口和反例要给正文位置和修复／复查义务。有限重放、Lean、专家复核等仅写实际执行的内容，并区分正式语句与原题。正文论证有错误而定理仍真时用 `gap`。
- `prior_art`：可为 `equivalent`、`prior_implies`、`manuscript_implies`、`strict_extension`、`overlap`、`different`、`undetermined`。精确写先例、证据与映射或反向不成立的依据；多条先例可并存。`novelty` 的命题、方法、理论分别填 `supported_increment`、`known`、`uncertain`、`not_applicable`。判断为新增或已有必须引公开证据并做先例比较。
- `importance` 的 `band` 是 `[下限, 上限]` 或 `null`。给分必须有公开历史证据、时间截点、两个以上不同锚点，并给关系 `lower` / `comparable` / `higher`（待评问题相对锚点）及理由。锚点 ID 见 `anchors.json`，11 个固定参照及量尺上限见同文件，已覆盖的区间内用锚点包住评价区间，且关系与区间一致；量尺低端允许单侧比较，须交代依据。未知用 `null`。与稿件结论、发表难度和期刊定位分别判断。
- `quality` 选有证据的数学品质，关联主张 ID 和证据 ID。不求和。看见一个可信贡献即可解释它如何帮助后续研究；无证据可以留空。分歧和未核范围写到单独字段。
- `readiness`：`blocked`、`revise`、`ready_for_expert_review`、`insufficient_evidence`。关键证明缺口或反例必须拦住；受限的检查不能标“可送专家”。`actions` 按优先顺序；推荐具体期刊需要范围与可比文章的证据，不给录用概率。

交付时看 `report.md` 与 `review.json`；输出标识 `review_record_validated` 只表示记录校验通过。完整论证、文献关系与专家审查状态以报告里的证据为准。

## 试跑结果

- 实读 [Furstenberg 1955 年原文](https://www.math.auckland.ac.nz/~gauld/750-05/inftlymanyprimes.pdf)与 [Euclid《几何原本》IX.20](https://mathcs.clarku.edu/~djoyce/java/elements/bookIX/propIX20.html)：结论已有，原文的同余拓扑证明成立，拓扑方法的解释价值单列。没有把两份原文的比较扩张成对历史优先权的确认。
- 对照稿只改拓扑基为模 5 剩余类，但仍声称每个素数的倍数集合闭。偶数集的补集不含任何模 5 陪集：每个模 5 陪集都含奇数与偶数。评审判定证明有阻断项，未误判经典定理为假。
- 运行 `python -m unittest discover -s tools -p 'test_paper_evaluation.py'` 复测附件冻结、私稿默认忽略、改稿后拒绝旧评价以及评分与投稿判断的关键边界。模板导出测试会用新目录实际生成评审包。
