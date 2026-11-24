# RA09 Final-01c 独立最终复核报告

## 结论

本轮按 source-first 顺序独立完成：先查看当前 `source.pdf` 的 12/12 张整页和 72/72 个六区重叠区域，之后才读取当前正文、映射、issues、ledger、恢复记录及审计快照。针对所有来源单元、目标单元、哈希、双向映射、黑/蓝/红边界、有限模型数学核验和既有未决项均完成检查。

**findings：`[]`。** 本轮没有发现新的内容遗漏、错读、数学错误、图形/版面问题或哈希/映射问题。Q001–Q005、六个既有 unresolved source units 以及 VS2-R002 的未决状态均由当前记录明确保留，本轮没有将它们冒作新发现，也没有改变其状态。

本轮结论是 `pass_no_new_findings`，仅表示对当前快照没有新增发现；当前 ledger 的 `final_rounds` 仍为 0，审计快照仍含既有未决记录，不能据此称三轮终审或内容已完全解决。

## 当前快照与文件哈希

本轮运行项目审计工具得到的内容快照为：

`102fd608c5dc326ee62e4a2c697ec11e3567d44c5b293c7169263c13c7117dc5`

本轮实际核对的哈希如下：

| 对象 | SHA256 |
|---|---|
| 原始 PDF `source.pdf`（manifest 原名 `实分析9(1).pdf`） | `436163228383e9c54919d41a4f2468a4923ac5712a2b4e8aa89761236a604883` |
| `manifest.json` | `79fe8e43472f1e7d5bff5786408c8ba795782cba051dfe2012d5bdc5c06400c9` |
| `proposals/integration-v2/source-transcript.md` | `2294913e155df421144c5e539107dd021a41cdfe56cbb469d84adddac1897ade` |
| `proposals/integration-v2/study-notes.md` | `1ae50ce2b146366409e31c2121a0fcb6a8f746928e46f65f458c55a9b9ba03ba` |
| `ledger-integration-v2.json` | `1c415c69387be8ebfb1ee1ef8c85b93bf4feee48bc093104d50c4c9b80cfffc2` |
| `ledger-config-integration-v2.json` | `1d456666d5376a2544215907dc45e861bd5d981f43d28742d3b4ab3e23a42b34` |
| `proposals/integration-v2/mapping.json` | `e16aff61fa9984a5a8267d2b8c94eeb689a2950e31fc4f37abdb1c1efd7b51d9` |
| `proposals/integration-v2/issues.json` | `1b7670e6f98ef9ac0d5f0948aba28e23a6a65ca461ad161352b603d42f882431` |
| `reviews/visual-second/integration-v2-confirmation.md` | `57f9f744483e2ed3a75d32c1f42ee95c2095e64c18b9b61d528d4b74adfc6cf7` |

原始 PDF 为 12 页 A4；manifest 与实际页/区图像哈希全部一致。当前 ledger 的 manifest hash 与 manifest 实际 hash 相同。

## 清单、哈希与双向覆盖

| 检查项 | 本轮结果 |
|---|---:|
| source units | 136（130 resolved，6 unresolved） |
| target units | 344（transcription 148，study 196；330 resolved，14 unresolved） |
| artifact 文件哈希 | 44/44 通过 |
| target 行范围和 text hash | 344/344 通过；无越界、空区间或空目标 |
| target marker hash | 344/344 通过 |
| mapping target IDs | 344/344 一致；missing 0，extra 0，duplicate 0 |
| source ↔ target 双向关联 | 344/344 通过，无断链 |
| source bbox 与页/区域相交 | 136/136 通过 |
| manifest page image hashes | 12/12 通过 |
| manifest region image hashes | 72/72 通过 |
| ledger page checks | 24/24（每页 pass 1、pass 2 各一条） |
| ledger region checks | 144/144（每区 pass 1、pass 2 各一条） |
| ledger `final_rounds` | 0（本轮文件不写回 ledger） |

当前 6 个 unresolved source units 为 `RA09-P001-U008`、`RA09-P002-U012`、`RA09-P006-U006`、`RA09-P006-U012`、`RA09-P008-U010`、`RA09-P008-U011`；对应的转写/学习稿目标仍以 `unresolved` 标记，未被哈希或映射检查掩盖。

## 黑、蓝、红边界

- 源 PDF 可见蓝色笔迹只在 p0003 问号圈和 p0008 集合族蓝色斜箭头；源 PDF 未见红色笔迹。
- `source-transcript.md` 的 5 个红色 span 与原稿待答/待填/待证位置逐一对应，普通黑色转写没有被标成蓝色或红色。
- `study-notes.md` 保留同样 5 个红色原稿位置，并有 45 个以 `> [!info]` 开始、每行均以 `>` 延续的蓝色补充/订正块；未发现 callout 边界泄漏到相邻黑色原文的情况。
- p0004 的原稿 `F_\delta` 和重复差集、p0008 生成族的圆括号原写法、p0010 示性函数端点缺漏、p0011 原待证空白均保持黑色原稿；相应标准数学内容仅以蓝色纠错/补证给出。
- 蓝色集合族图示说明与黑色原图文字分开，未把蓝箭头或蓝色标准答案冒充黑色原字。

## 数学核验

本轮重新阅读黑色原稿与蓝色补证的主要数学链条，并复核有限模型检查结果：

- $G_\delta/F_\sigma$ 定义、度量空间距离函数、Borel 性、Cantor 零测集中的非 Borel 子集及严格包含；
- 可测集开集外逼近、闭集内逼近、无限测度的局部分解、取补、$G_\delta$ 外壳和 $F_\sigma$ 内核；
- 外正则、闭集内正则、有界集内外测度判据和边界零测充分条件；
- 逆像族的任意并/交/补恒等式、生成族判别、最大目标拓扑；
- 扩展实数序拓扑、端点单点、四种半直线、Borel 代数以及与 $[0,1]$ 的同胚；
- 迹 $\sigma$ 代数、扩展实值可测函数的上水平集判别；
- 四种源/目标 $\sigma$ 代数组合的包含关系、$C_{BB}$ 与 $C_{MM}$ 的互不蕴含反例、有限区间无法分离两个无穷端点；
- 常函数、示性函数端点校正、相对拓扑连续性和沿 $\tau_f\subset\Sigma_f$ 的第二条连续函数可测证明。

复算/有限检查结果与当前 QA 记录一致：逆像恒等式 1728 cases 通过；示性函数水平集 40 cases 通过；有限端点区间生成族大小 16 且两个无穷端点不可分，上射线生成族大小 32 通过；二进制到三进制有限抽样 256 点重构和单射性通过。有限检查只支持这些有限模型，不替代一般证明；本轮未发现蓝色一般证明与黑色原稿路线之间的新矛盾。

## 既有未决项复核

- **Q001**：p0001 编号 5 旁注中“会有〔疑字 001〕有反例”的连笔仍无法唯一恢复；保留中性疑字。
- **Q002**：p0002 底部两处过渡旁注仍分别为 002-A、002-B；可读首尾和位置明确，字形不能唯一确定。
- **Q003**：p0006 “$\Sigma_f$ 是〔疑字 003〕$\sigma$ 代数”中间字形仍不唯一；所需封闭性质的蓝色证明不冒充原字。
- **Q004**：p0006 末行“只要邻域，〔疑字 004〕（1）（2）线序拓扑”连接语仍不唯一；保留原句和疑点。
- **Q005**：p0008 “$\Longrightarrow$ 用生成〔疑字 005〕”末字连写仍不唯一；生成族补证单独标为蓝色。
- **VS2-R002**：p0008 的原稿生成族实际可辨为圆括号 `$\mathcal D=\{(a,+\infty)\}$`，右端闭括号和 `a\in\mathbb R` 参数尾没有足够笔迹证据。正确的 `$\{(a,+\infty]:a\in\mathbb R\}$` 只保留在蓝色补证，recovery 继续 `unresolved`。

上述项目均是当前快照中已有的未决状态，不是本轮 findings。当前审计 JSON 的未决计数仍为 39（含这些 source/target units、已有第二阶段页区判断、VS2-R002 和 Q001–Q005），并有 `FINAL_THREE_ROUNDS` 结构提示；本轮不改写这些记录。

## 本轮操作边界

只新建：

- `reviews/final-01c/blind-reading.md`
- `reviews/final-01c/report.md`
- `reviews/final-01c/review-record.json`

没有修改正文、ledger、ledger-config、mapping、issues、第二阶段证据或 Git。
