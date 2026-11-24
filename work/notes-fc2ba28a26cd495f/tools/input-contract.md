# `build_ledger.py` 输入合同

这是本 RUN 的台账装配工具，不代替项目的 `audit.py`，不生成“看过”、通过、身份、正文解释或数学判断。工具只计算文件/行段哈希、标记行号、bbox 相交区域，以及作者明确映射的反向关系。第二遍与终审尚未进行时，相关数组保持空缺，正式审计应失败。

## 调用

在仓库根目录运行（用真实笔记目录替换 `<NOTE>`）：

```bash
python work/notes-fc2ba28a26cd495f/tools/build_ledger.py \
  --project work/notes-fc2ba28a26cd495f/<NOTE>/project \
  --config ledger-config.json
```

`--project` 指向 `prepare_pdf.py` 创建的项目。`--config` 可以是该项目内部的绝对路径或相对项目路径。所有 JSON 内文件路径均相对项目根目录，禁止绝对路径、`..` 和越界符号链接。manifest 和生成 ledger 均须位于项目根目录，避免改变路径含义。

## 建议布局

```text
project/
  manifest.json                 # 原工具生成；不手改
  source.pdf                    # 原工具复制
  pages/ ...                    # 沿用原工具实际图像目录
  source-transcript.md
  study-notes.md
  ledger-config.json
  source-units.json
  mapping.json
  observations.json
  editorial-evidence.md         # 作者实际编辑/补充依据；按需要创建
  recoveries.json               # 可选，严格原 schema
  issues.json                   # 可选，严格原 schema
  final-rounds.json             # 可选，已封存的真实历史记录
  ledger.json                   # 本工具输出
```

### `ledger-config.json`

以下是**未完成的接口模板**；空作者列表必须由协调者填写实际工具身份。本模板没有任何观察或通过记录。

```json
{
  "authors": [],
  "manifest": "manifest.json",
  "artifacts": [
    {"id": "transcription", "path": "source-transcript.md", "kind": "transcription", "format": "text"},
    {"id": "study", "path": "study-notes.md", "kind": "study", "format": "text"}
  ],
  "source_units": "source-units.json",
  "mapping": "mapping.json",
  "observations": "observations.json",
  "output": "ledger.json"
}
```

`observations` 也可写成文件名数组，例如作者首遍和新代理第二遍各自的真实记录文件；工具只拼接，重复 ID 会报错。可选键 `old_units`、`recoveries`、`issues`、`final_rounds` 各指向 JSON 数组文件；不提供时输出 `[]`。所有身份、状态与发现必须由实际执行者明确输入。

`artifacts` 可增加实际证据工件。其手填字段为 `id/path/kind/format`，图像证据另外填写原 schema 的 `source_crop: {page_id, bbox_px}`。不要填 `sha256`，由工具计算。额外裁图必须保留真实像素；本工具计算文件哈希，像素真实性由原审计工具核对。

### `source-units.json`

顶层为数组；也接受只有 `source_units` 键的对象。每条必须明确提供以下字段，不能省略：

| 字段 | 手填内容 |
| --- | --- |
| `id` | 原稿单元稳定 ID，与正文/旧稿命名空间不同 |
| `page_id` | manifest 中的真实物理页 ID |
| `bbox_px` | 整页 PNG 像素框 `[x0,y0,x1,y1]`，右/下边界不包含 |
| `label` | 作者识读得到的具体内容标签 |
| `status` | `resolved` 或 `unresolved`，由作者判断 |
| `evidence_ids` | 作者实际引用的整页与所有相交区域证据 ID，必要时含额外证据 |

`region_ids`、`transcription_target_ids`、`study_target_ids` 由工具计算，不应放入输入。工具**不会自动补 evidence_ids**。缺少对应整页/相交区域证据会在正式审计失败，作者应根据实际读图情况补齐，不能用脚本代写“已读”。

单元应细到条件、公式、证明实质步骤、旁注及重复路线，不能把整页压成一个不可核对的条目。空白物理页和普通页边通过真实页区观察记录，不凭空造为红色待填。

### 正文标记与 `mapping.json`

两正文所有非空行都必须位于某个显式块内，包括标题、目录、颜色说明。每块以单独一行标记开始：

```markdown
<!-- unit: 唯一的目标单元ID -->
该单元的实际正文。
```

目标 ID 在两个正文之间也须唯一。标记行本身包含于本块；本块终点是下一标记前一行或文件末行。哈希按原合同：`splitlines()` 分行后，以 LF 连接整个含首尾行区间，不追加末尾 LF。首标记前只允许空白行。不能用一个原图单元 ID 同时充当目标 ID。

`mapping.json` 形状为 `{"targets": []}`。数组每条手填：

| 字段 | 手填内容 |
| --- | --- |
| `id` | 与正文标记完全相同的目标 ID |
| `artifact_id` | 所在正文的工件 ID |
| `source_ids` | 真实原稿单元 ID 数组，编排内容可以为空 |
| `status` | 明确的 `resolved` / `unresolved` |
| `origin` | `source` / `old` / `supplement` / `editorial` |
| `old_ids` | 实际旧稿单元 ID 数组；尚无旧稿时为空 |
| `evidence_ids` | 作者明确引用的图像/文本证据 ID |
| `explanation` | 来源、补充或编排依据；新增与编排须具体说明 |

工具补上 `start_line/end_line/text_sha256`，反向生成每个原稿单元在两正文中的目标清单。每个原稿单元必须至少有一个转写目标和一个学习稿目标，否则严格 ledger schema 不通过。来源关系、状态和证据类别不自动推断。

编排标题、目录可用 `origin: editorial`，`source_ids/old_ids` 为空，实际文本证据以 `kind: evidence, format: text` 登记。不要为方便覆盖而伪托原稿来源。原稿正文与蓝色补充建议分别划块，以保持来源类别准确。

### `observations.json`

未读时的准确接口是：

```json
{"page_checks": [], "region_checks": []}
```

作者实际读图后，分别按原 `ledger.schema.json` 的 `page_checks`、`region_checks` 结构完整填写。工具逐字段原样保留，不自动计算 `source_unit_ids`、`cross_region_unit_ids`、`evidence_ids`，也不填 `pass`、身份、assessment 或观察。

每条全页记录需要 `id/page_id/pass/reviewer_id/session_id/assessment/source_unit_ids/evidence_ids/observation/cross_region_unit_ids/layout_observation`。每条区域记录需要 `id/region_id/pass/reviewer_id/session_id/assessment/source_unit_ids/evidence_ids/observation`。首末内容、实际符号、空白与接续关系须来自真正读图。第二遍必须另一位新代理。

### 旧稿、恢复与终审

没有旧稿时无需 `old_units`。有旧稿后，每条输入含原 schema 的 `id/artifact_id/start_line/end_line/disposition/explanation/evidence_ids`；工具计算 `text_sha256`，根据学习稿 `old_ids` 反向生成 `target_ids`。所有旧稿非空行是否完整覆盖仍由原审计核验。

`recoveries`、`issues`、`final_rounds` 原样导入，必须满足原 schema。本工具不编写恢复候选或验证结论，不取得/替换复核开始时的快照，不生成 scope/findings，不封存轮次。待封存的 `record_sha256: null` 应按原工具合同直接追加到 ledger，再用 `audit.py seal-round`；本装配器严格拒绝未封的 schema。

若重建已有 ledger，已有 `final_rounds` 必须作为新输入的原样前缀保留，否则拒绝覆写，防止不小心删除或洗改审阅历史。重新生成内容导致快照变化时，旧轮次只是历史；必须按合同重新累计。封存之后建议直接用原审计工具维护 ledger，避免重复装配。

## 成功与失败的含义

装配成功仅输出 `schema_valid: true, audit_run: false`。必须另行运行：

```bash
python .agents/skills/math-notes-evidence-audit/scripts/audit.py check \
  --manifest <project>/manifest.json --ledger <project>/ledger.json \
  --report <project>/audit-reports/structure.json
```

未完成两遍及三轮时，以上正式审计失败是准确结果。装配器不把 schema 合法解释为内容完整、实际已读或数学正确。未知字段、重复 ID/JSON 键、缺标记、正文漏出标记范围、越界路径、失配 bbox、单元无双正文去向会直接失败，不写部分输出；已有输入、正文、图像和审阅文件不能被输出覆盖。
