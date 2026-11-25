# 数学手记复核工具

这些工具检查 PDF 页数、图像像素、内容清单、双向对应和审核记录的完整性。**结构/记录通过 ≠ 图像确已被阅读 ≠ 数学内容零错或零遗漏。** 内容单元是否真实穷尽原稿、恢复推理是否正确，仍由实际看图与数学复核负责；声明的身份和 session 也不是身份认证。

所有运算在本地完成，无 OCR 模型、API 或网络请求。需要 Python 3.10 或更新版本。

## 文件

| 文件 | 用途 |
| --- | --- |
| `prepare_pdf.py` | 真实页数、原件副本、全页图和重叠区域、SHA-256 与像素坐标 |
| `audit.py` | JSON Schema、文件完整性、内容和旧稿对应、恢复记录、审核门槛 |
| `schema/manifest.schema.json` | 图像准备结果的严格 Schema |
| `schema/ledger.schema.json` | 内容清单及审核台账的严格 Schema |
| `schema/example.template.json` | **未完成且不能通过**的台账起点；占位哈希必须替换 |
| `selftest.py` | 小型合成 PDF 的正常及失败边界回归 |

## 准备与首次检查

在本包项目根目录运行：

```bash
python -m pip install -r .agents/skills/math-notes-evidence-audit/scripts/requirements.txt
python .agents/skills/math-notes-evidence-audit/scripts/prepare_pdf.py input.pdf --out review-project
cp .agents/skills/math-notes-evidence-audit/scripts/schema/example.template.json review-project/ledger.json
python .agents/skills/math-notes-evidence-audit/scripts/audit.py hash review-project/manifest.json
python .agents/skills/math-notes-evidence-audit/scripts/audit.py check --manifest review-project/manifest.json --ledger review-project/ledger.json --report review-project/audit-reports/structure.json
```

最后一条命令在模板尚未填写时应失败，这是预期行为。`--out` 必须为新目录或空目录，避免覆盖已有复核证据。

`prepare_pdf.py` 默认以 220 dpi 将每个物理页渲染成 RGB PNG。每页固定两列三行，各相邻基础单元按默认 `--overlap 0.08` 扩展后有重叠；边缘裁到整页边界。可显式设置 `--dpi 300 --overlap 0.12`。坐标是整页 PNG 的整数像素，顺序 `[x0,y0,x1,y1]`，右、下边界不包含在内。原件复制为 `source.pdf`；它、整页图和每张裁图都记录 SHA-256。

`blank_candidate` 只提示接近白色的裁图，`blank_status` 始终为 `unreviewed`。淡笔迹、压缩、扫描背景都可能误导提示。空白页及其全部区域仍须两遍明确观察记录。

`audit.py` 还会重渲染 PDF 并比对全页像素，再比对裁图与整页对应像素，检查真实页数与网格覆盖。不同 PyMuPDF 渲染版本可能产生像素差异；应在同一锁定的运行环境完成准备和审计，版本见 manifest。版本更新后如不一致，应重新准备并重新复核，不能修改记录来掩盖差异。

## 台账填写规则

Schema 严格拒绝未知字段，不能用 `done: true`、总页数声明或 `pass: true` 替代内容记录。页码从一开始；manifest 的页标识如 `p0001`，区域如 `p0001-r1c1`。台账所有标识应在本类清单中唯一，原稿、目标和旧稿单元须用不同命名空间。

文件路径相对所属 JSON 所在目录：manifest 内路径相对 manifest，ledger 内路径相对 ledger。只能引用项目内文件，禁止绝对路径、`..` 及越界符号链接。建议 ledger 与 manifest 放在同一项目目录。

### 工件与逐行清单

`artifacts` 至少有一份 `kind: transcription` 原稿转写和一份 `kind: study` 复习稿。`kind: old` 是需要迁移或解释的旧稿；没有旧稿时可以没有该类。`kind: evidence` 用于演算记录或额外裁图。所有正文和旧稿均须为 `format: text` 的 UTF-8 纯文本（可用 Markdown 或 LaTeX），并记录整个文件真实哈希。

```bash
python .agents/skills/math-notes-evidence-audit/scripts/audit.py hash review-project/transcription.md
python .agents/skills/math-notes-evidence-audit/scripts/audit.py text-hash review-project/transcription.md --start 1 --end 3
```

`target_units` 记录转写与复习稿的 `artifact_id`、起止行和 `text_sha256`。行区间两端均包含；区间文本以 `splitlines()` 分行，再用单个 LF 连接，**不含末尾换行**后计算 SHA-256。每个非空行必须恰好属于一个单元，不能有漏行或重叠。标题、注记、编者解释也需对应相关原稿单元；空白行可以不分配。工具不把文本哈希当作语义正确性证明。

`source_units` 是逐图建立的原稿内容单元，包含页、准确像素 bbox、所有与 bbox 相交的区域、短标签、状态、转写目标、复习稿目标与证据。原稿每个单元同时对应转写与复习稿；目标凡实际填写 `source_ids`，都必须反向对应原稿目标表。两侧都核验，正文新增行也不能绕过清单。

每个 `target_units` 还须填写 `origin`、`old_ids`、`evidence_ids` 和 `explanation`。旧稿独有内容、新增补充和编排标题可以合法没有 `source_ids`，不能为了填满清单虚构原图来源。

| `origin` | 来源约束 |
| --- | --- |
| `source` | 至少一个真实 `source_ids`，证据包含对应整页；有旧稿对应时也填 `old_ids` |
| `old` | 旧稿独有内容：`source_ids` 为空，`old_ids` 非空，证据含相应旧稿工件 |
| `supplement` | 明确说明新增补充；关联实际 source/old 单元，或提供独立演算/参考的文本证据工件 |
| `editorial` | 新增编排说明/标题：不伪托 source/old 来源，给出具体编辑说明及其文本证据 |

`old_ids` 必须与旧稿单元的 `target_ids` 双向对应。`supplement` 与 `editorial` 的说明不能为空；它们的来源声明不等于数学正确性证明。正文应按交付规则向读者清楚标明旧稿独有内容与补充内容。

证据标识无需重复登记已有图：

| 引用 | 绑定的真实文件 |
| --- | --- |
| `image:p0001` | 经哈希与 PDF 像素核验的整页图 |
| `image:p0001-r1c1` | 经哈希与整页 bbox 像素核验的区域图 |
| `artifact:calculation-01` | `artifacts` 中该标识的真实哈希文件 |

每个原稿单元的 `evidence_ids` 必须同时包含整页和全部相关区域。跨栏公式、跨区推导、边注与接续关系应先回整页；六区网格不替代整体版式判断。必要时生成额外放大裁图，登记为图像证据工件，并提供 `source_crop: {page_id, bbox_px}`。程序验证额外裁图像素确实来自该页 bbox。

`old_units` 也逐行覆盖旧稿所有非空行。**所有 disposition 都必须有具体 study 目标单元**，并由目标的 `old_ids` 反向对应；目标本身有实际行号和精确文本哈希。`migrated` 表示在复习稿中保留整理；`explained` 表示在复习稿中保留原说法的可读辨析/订正；`unresolved` 表示复习稿仍保留待定说法和原因，对应目标也须未决。每条 `explanation` 都须说明在哪个目标保留、纠正或辨析原义。证据必须包含旧稿自身的 `artifact:<id>`。不允许只在台账写一句解释就让旧稿内容从正文消失。

程序核验具体正文去向及双向对应，**不能检验原义是否完整保留、订正是否正确**。它不要求原始 OCR/转义/Markdown 与新版逐字相同，允许规范 LaTeX 和清理 OCR；逐义保真及可读辨析须由独立复核者实际检查。

### 两遍全页与区域检查

每个物理页须有两条 `page_checks`，每个区域须有两条 `region_checks`，`pass` 分别为 `1` 和 `2`。首遍可由作者完成；第二遍必须非作者；两遍 reviewer 与 session 均不同。同一遍可在同一实际 session 检查多个页区。

每条记录必须有实际观察文本、图像证据以及精确的原稿单元清单。全页检查还须有 `layout_observation` 和 `cross_region_unit_ids`（bbox 涉及多个区域的全部单元）。`assessment` 只能是 `content`、`blank` 或 `unresolved`。空白判断与已有内容单元冲突会失败；标为有内容却无单元清单也会失败。

### 推理恢复与未决项

每条 `recoveries` 须记录问题、至少两个不同候选、候选证据、选中候选或 null、前向与反向验证的方法/输入/结果/证据、返回整页与区域的观察，以及复核者/session。`resolved` 要求选中真实存在的候选且两种验证均为 `pass`；两种方法应描述不同检验。程序不执行台账里的任意代码，也不自动证明恢复数学正确。

不能排除歧义时保留 `status: unresolved`，并让关联原稿和目标单元保留未决状态。`issues` 保存其他待定问题或修复解释。历史问题解决后保留记录，`resolution` 写明如何解决。提交前由模型自动生成高分辨率裁图、候选表和正反向检验清单；这一步不转交人工。

`unresolved_count` 统计未决**记录数**（单元、页区判断、旧稿、恢复和开放问题），不代表互不重复的数学问题个数。同一个歧义可能影响多条记录。结构合法但有未决项时，报告可为 `audit_pass: true`，同时一定是 `content_resolved: false`、`status: NeedsModelRecovery`。这表示模型恢复循环尚未收敛，不是人工门禁；任务必须保持认领状态，只有缺页、损坏原件或视觉工具不可用才允许 `notes block`。

## 最后三轮及完整快照

`authors` 要列出参与正文编写或修改的人/代理。最终每轮 reviewer 必须是未参与该笔记编写、页区检查、恢复复核或此前终审的新身份，session 也不能复用。身份真实独立与是否真的看过图仍需流程保证，哈希不提供这一证明。

开始每轮前，先取得该轮实际要读的完整内容快照与全量范围：

```bash
python .agents/skills/math-notes-evidence-audit/scripts/audit.py snapshot --manifest review-project/manifest.json --ledger review-project/ledger.json
python .agents/skills/math-notes-evidence-audit/scripts/audit.py scope --manifest review-project/manifest.json --ledger review-project/ledger.json
```

快照包含 manifest 原始文件哈希、原 PDF/所有页图/区域图/全部正文和证据工件的**实际内容哈希**，以及除 `final_rounds` 外整个 ledger（清单、双向映射、页区检查、恢复决策、issues 等）。它同时锁定转写和复习稿，不只是主 Markdown。

每轮记录须包含：

- `id`、连续的 `round`、新 `reviewer_id`/`session_id`；
- 开始阅读时实际取得的 `snapshot_sha256`，不得事后替换；
- `scope` 的每项全量标识（由 `scope` 命令给出），以及每页具体 `page_notes`；
- 显式 `findings` 数组：新发现的问题标识必须存在于 `issues`；没有新发现也必须明确写 `[]`；
- 全部整页图和区域图的 `evidence_ids`、实际说明 `notes`；
- 独立的 `blind_reading` 与 `report`，各为 `{path, sha256}`，分别是先看原图写的盲读清单、之后对照产物的报告；
- `previous_round_sha256` 和 `record_sha256` 供记录完整性核验。

盲读和报告必须是项目内非空 UTF-8 文本，每轮每阶段均用独立文件，路径和内容哈希不能跨轮复用。它们直接写在轮记录里，**不要作为内容 artifacts 加入**。这些锁定之后追加的审核证据不改变内容快照，其实际哈希、路径和所有轮字段一起受该轮 hash 及前序 hash 链约束。文件文本、先后顺序和声明不能证明盲读真的发生。

新轮记录先写 `record_sha256: null`（这是待封记录，审计暂时不能通过），写好已经取得的 `snapshot_sha256`、真实观察、范围及两份文件哈希后执行：

```bash
python .agents/skills/math-notes-evidence-audit/scripts/audit.py seal-round --manifest review-project/manifest.json --ledger review-project/ledger.json --round-id final-01
```

`seal-round` 只计算最后一轮的前序链接和记录哈希。它不生成观察、证据、scope、findings 或身份，也**不会覆盖预先声明的 snapshot**。当前内容与开始阅读时快照不一致会拒绝；已封记录拒绝再次封存。正文或内容台账修改后，必须真正重新阅读并追加新身份的新轮；不能给旧报告换快照洗成新复核。

最终门槛要求最后连续三轮都绑定同一个当前完整快照、全量范围、逐页观察、无新增 findings，并且身份/session/证据文件独立。历史发现和旧快照记录可以保留在前面。发现问题并改正文后，需要再完成连续三轮。

最终审计 JSON 使用独立路径。`--report` 不进入内容快照，且拒绝覆盖任何被锁正文、图像、ledger、manifest 或轮证据文件。

```bash
python .agents/skills/math-notes-evidence-audit/scripts/audit.py check --manifest review-project/manifest.json --ledger review-project/ledger.json --report review-project/audit-reports/final.json
```

| 退出码 | 含义 |
| --- | --- |
| `0` | 记录结构门槛满足，已登记未决数为零；仍未证明视觉阅读或数学无错 |
| `1` | Schema、证据、映射、范围、独立性或终审结构有错误 |
| `2` | 结构门槛满足，但仍有明确未决记录，需要人处理 |

报告始终包含 `visual_reading_proven: false`、`zero_omission_proven: false`、`mathematical_correctness_proven: false` 和解释。不能把退出码零包装成“零遗漏证明”。

## 运行回归

```bash
python .agents/skills/math-notes-evidence-audit/scripts/selftest.py
```

测试在临时目录自动生成小型双页 PDF（一页公式、一页空白），不使用真实手记、不需要联网。覆盖漏页、伪造页数、漏区/漏遍、缺失全页检查、双向映射、正文漏行、旧稿去向、恢复假解决、哈希修改、伪造裁图、重复审核者/session、无效证据、未决项、范围不全、记录链篡改，以及旧快照不能重新封成新版本。

如需直接试验 CLI，可生成一份**仅用于测试的合成台账**；其中声明的审核者与文本都是合成测试数据，不能用于真实交付：

```bash
python .agents/skills/math-notes-evidence-audit/scripts/selftest.py --emit-fixture synthetic-demo
python .agents/skills/math-notes-evidence-audit/scripts/audit.py check --manifest synthetic-demo/project/manifest.json --ledger synthetic-demo/project/ledger.json --report synthetic-demo/project/audit-reports/result.json
```

模板本身不预填任何通过记录。测试 fixture 仅用于验证门槛的程序行为，不宣称合成的自报记录代表真实视觉复核。
