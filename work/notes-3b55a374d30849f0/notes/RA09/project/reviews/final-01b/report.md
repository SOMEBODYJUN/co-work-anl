# RA09 Final-01b 独立最终复核报告

## 结论

本轮从当前新快照重新开始，未读取或依赖上一轮 RA09-final-01 的结论。按 source-first 顺序先完成 12/12 张整页和 72/72 个六区区域的视觉检查，再核验正文、ledger、mapping、issues、第二阶段证据和数学补证。

**findings empty：本轮没有发现新的内容、数学、图形、页面裁切或哈希/映射问题。** 当前快照中已有的五个 open issue（Q001、Q002、Q003、Q004、Q005）、六个 unresolved source unit，以及 VS2-R002 的一个未决恢复提案，均仍由现有记录明确标注；本轮不把它们冒作新发现，也不修改其状态。

## 快照与哈希

| 对象 | SHA256 |
|---|---|
| 原始 PDF `source.pdf`（manifest 原名 `实分析9(1).pdf`） | `436163228383e9c54919d41a4f2468a4923ac5712a2b4e8aa89761236a604883` |
| `manifest.json` | `79fe8e43472f1e7d5bff5786408c8ba795782cba051dfe2012d5bdc5c06400c9` |
| `proposals/integration-v2/source-transcript.md` | `2294913e155df421144c5e539107dd021a41cdfe56cbb469d84adddac1897ade` |
| `proposals/integration-v2/study-notes.md` | `1ae50ce2b146366409e31c2121a0fcb6a8f746928e46f65f458c55a9b9ba03ba` |
| `ledger-integration-v2.json` | `eb6de6b967c842690528f0600cb4888bb5fc3b90fd02372816678c074c50a905` |
| `ledger-config-integration-v2.json` | `1d456666d5376a2544215907dc45e861bd5d981f43d28742d3b4ab3e23a42b34` |
| `proposals/integration-v2/mapping.json` | `e16aff61fa9984a5a8267d2b8c94eeb689a2950e31fc4f37abdb1c1efd7b51d9` |
| `proposals/integration-v2/issues.json` | `1b7670e6f98ef9ac0d5f0948aba28e23a6a65ca461ad161352b603d42f882431` |

另核对了 ledger 中 44 个 artifact：每个文件均存在且实际 SHA256 与 ledger 一致；manifest 中的源 PDF、12 个 page image 和 72 个 region image 也全部一致，0 个哈希不匹配。`pdfinfo` 报告源 PDF 为 12 页 A4，和 manifest/assignment 一致。

## 覆盖与结构完整性

| 检查项 | 结果 |
|---|---|
| 原始 PDF 整页视觉检查 | 12/12 |
| 六区重叠区域视觉检查 | 72/72（每页 6 区） |
| 页面/区域图像哈希 | 12 + 72，0 个不匹配 |
| source units | 136（130 resolved，6 unresolved） |
| target units | 344（148 transcription，196 study；330 resolved，14 unresolved） |
| target marker hash | 344/344 通过 |
| target text hash | 344/344 通过 |
| mapping target IDs | 344/344 一致；无 missing/extra |
| source ↔ target 双向关联 | 全部通过 |
| source bbox 与 page/region | 136/136 在页界内且与列出区域相交 |
| ledger `page_checks` / `region_checks` | 24/24、144/144（两轮记录均 pass） |
| 有限模型 QA | inverse-image 1728 cases、indicator 40 cases、端点生成族、binary-to-ternary 256 points 均 pass |
| ledger `final_rounds` | 0；本文件是独立 Final-01b 记录 |

视觉上 p0011 只有页顶两行，p0012 整页空白；这两种稀疏/空白状态均在整页与六区中实际确认，未把普通留白当成遗漏。

## 黑/蓝/红边界与数学核验

源 PDF 的蓝色笔迹出现在 p0003（问号圈）和 p0008（示意图蓝箭头），未见源 PDF 红色笔迹。学习稿有 45 个蓝色 `[!info]` 信息块；转写稿和学习稿各保留 5 个 `<span style="color:red">` 原稿待答/待填标记。普通黑色转写、蓝色补充/订正、红色原稿未决位置的边界清晰，没有把蓝色标准化答案伪装为黑色原字。

独立数学核验覆盖以下主线：

- $G_\delta/F_\sigma$ 的定义、度量空间距离函数表示、Borel 基数与 Cantor 非 Borel 子集；
- 开集外逼近、闭集内逼近、无限测度的局部分解和取补；
- $F_\sigma$ 内核订正与内外正则性；
- Carathéodory 可测族不能恰等于 Borel 代数的补证；
- 逆像族的交并补封闭、生成族判别、扩展实数端点和四种半直线；
- 四种可测性组合的包含关系及正负无穷反例；
- 常函数、示性函数端点纠正、孤立点相对拓扑连续性和连续函数可测性。

上述补证与黑色原稿的边界均有明确说明。p0009 的修复字面式在两份正文中均为
`$G(E)=B\cup\{+\infty,-\infty\}$`；完整有限区间生成族及端点区分说明位于蓝色补证，不覆盖原黑字。

## 现有未决状态（不是本轮新发现）

- `issues.json` 中 5 个 issue 仍为 `open`：Q001、Q002、Q003、Q004、Q005；其对应 source units `RA09-P001-U008`、`RA09-P002-U012`、`RA09-P006-U006`、`RA09-P006-U012`、`RA09-P008-U010` 均保守保留疑字。
- `RA09-P008-U011` 也保持 unresolved，和 VS2-R002（p0008 生成族的圆括号端点/参数尾）相连；3 个 recovery 中 2 个 resolved、1 个 unresolved。
- target 中 14 个 unresolved（六个原始疑字的转写/学习目标及其两处补证继承标记）均保留，未被本轮改写。

这些状态与当前 ledger、issues、mapping 和 visual-second 证据一致；本轮仅复核并记录，不向 ledger 写回。

## 判定

`verdict: pass_no_new_findings`。这表示当前新快照通过本轮独立复核且没有新发现；是否因既有 open/unresolved 项而延迟最终冻结，由总协调者按冻结规则决定。

## 操作记录

只读取并核验当前快照，写入本目录的 `blind-reading.md`、`report.md` 和 `review-record.json`。未改动正文、ledger、配置、第二阶段证据或 Git。
