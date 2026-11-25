# RA07 Final-01 独立最终复核报告

## 结论

本次复核按 source-first 顺序完成：13/13 张整页和 78/78 个六区重叠区域均已查看，随后完成正文、映射、ledger、配置、证据和 recovery 的独立核验。快照的文件完整性、源/目标映射、marker/text hash 和证据引用均通过；正文也保留了源稿的黑色笔迹、蓝色补充/纠错和红色未决边界。

结论为 **conditional_hold（有条件暂缓冻结）**：没有发现新的致命数学或版面问题，但仍有四个命名语义问题、九个 source unit 的保守未决状态，以及三个 recovery proposal 未选定候选。若冻结要求所有原始字形唯一恢复，应先处理这些未决项；若冻结允许保留原始不确定性，则当前正文的标注策略是可审计的。

本报告只报告问题和验证结果，不修改正文、ledger、其他审查记录或 Git。

## 快照和哈希

| 对象 | SHA256 |
|---|---|
| 原始 PDF `input/pdf/source.pdf`（原名 `实分析7.pdf`） | `c053b24757b997ab489d1c18371df9ba44137919d53596b7158856ac1e8746c8` |
| `manifest.json` | `7cd8b8c47a2e6ee020eb41097fe85c4812e483989cf535ebe0a19a9c490b5b03` |
| `proposals/integration-v2/source-transcript.md` | `72954031a008ad305e8630a826fb7e2ae774f7dd56878178c7377f6d19ec715f` |
| `proposals/integration-v2/study-notes.md` | `3cbfca7725ab6b77a8b9fa91fc350aa28b39779c3864b025a004b45c18772ac0` |
| `ledger-integration-v2.json` | `3c805322435b7ae18ac662693a0ed1d54dbcc3ccfc283c3fbe3964ef20dac215` |
| `ledger-config-integration-v2.json` | `012f59fecdc3ce43e3acdfcc03e38023c2c56bcb9725301f3c781055a4c60ce3` |

另核对了 ledger 中的 33 个 artifact：每个文件均存在且实际 SHA256 与 ledger 一致；manifest 中的源 PDF 哈希也与实际文件一致。integration-v2 确认文件的哈希为 `1c6592348f36cf28693f1ae3bc1cf3be021d4d3ddb27ecd8e0440cf9d0144564`。

## 覆盖和结构完整性

| 检查项 | 结果 |
|---|---|
| 原始 PDF 整页视觉检查 | 13/13 通过查看 |
| 六区重叠区域视觉检查 | 78/78 通过查看；每页六区 |
| 区域/页面图像 hash | 13 页图 + 78 区图，0 个不匹配 |
| 非空/空区域 | 68 个含笔迹或正文区域；10 个空白区域；p0013 整页空白，p0012 部分空白 |
| source units | 149 |
| target units | 420（transcription 162；study 258） |
| target marker hash | 420/420 通过 |
| target text hash | 420/420 通过 |
| mapping target ID 与 ledger | 420/420 一致；source ID 双向关联通过 |
| source bbox 与 region/page | 149/149 在页界内且与列出的区域相交 |
| ledger `final_rounds` | 0；本文件为独立 Final-01 记录 |

marker/text hash 按 target 的 1-indexed `start_line:end_line` 读取正文片段，并核对首行 `<!-- unit: TARGET-ID -->`；没有发现脱离 marker、错行或正文片段漂移。

## 正文与源图边界

黑色原稿、蓝色补充/纠错和红色未决边界是可见且一致的。源 PDF 的蓝色痕迹主要位于 p0001（问号圈）和 p0004（补证明/更正），未发现源 PDF 红色笔迹。study-notes 中有 93 个蓝色信息块，5 个红色标记；红色标记集中在原稿未回答或证明未完的位置，没有被用来掩盖不确定字形。

正文准确保留或显式说明了下列源稿风险：

- p0002 原始 Darboux 行的 `sup U = inf L` 与正确的 `inf U = sup L` 方向差异；
- p0004 黑色原始分母的 `ε/2^k`/视觉上接近 `ε/(2k)` 差异，蓝色版本使用几何级数并保留源稿差异；
- p0005 孤立 `I/G` 笔形没有被静默规范为 `|G|`；
- p0006 Carathéodory 条件中 `T`、页顶截断和左边缘残弧；
- p0007 原稿的 I/T 与适用范围混用；
- p0008 原始严格不等号并非一般事实，蓝色补充标明“不保证”；
- p0010 原稿 `A∪V=A∪(A\V)` 的方向错误，蓝色给出差集方向修正；
- p0011 原稿 `T∩A∪B^c` 的括号风险，蓝色补足 `(A∪B)^c` 的解释。

我独立检查了蓝色补充中的 Carathéodory、正距离/可加性、可测族闭性、内测度、Vitali 和无限维测度论证，没有发现新的致命逻辑错误。黑色原稿中的错误或不完整证明均有边界标示，不能当作已经证明的黑色结论。

## 题目、证明和图

- **题目**：p0001 的无限维/平移正规性/非平凡测度问题、p0003 Remark(2) 的覆盖对象、p0010 Vitali 行、p0011 公式前连接字仍按不确定度保留；正文没有把候选答案伪装成原稿唯一读法。
- **证明**：p0002 的 Darboux 条件、p0004 的次可加估计、p0006–p0008 的 Carathéodory 分割、p0009 的零测集、p0010 的 Vitali 处理和 p0011 的有限可加链均能在正文找到对应源单元或蓝色补证。p0008 空证明标题和 p0012 稀疏结尾被保留为不完整，而不是补写为源稿证明。
- **图**：p0006 两圆图（小圆 E 与未命名大圆）和 p0011 A/B/T 三圆图及编号 1–4 的拓扑关系保留；没有发现新增箭头、阴影、标签或深度关系错误。

## 实质未决与风险

### 四个命名语义 issue（ledger 中仍为 open）

| Issue | 源位置 | 独立判断 |
|---|---|---|
| RA07-Q001 | RA07-P001-U013 / T-P001-013 | 句首接近“无穷维”；后续量词样符号无法唯一恢复；蓝圈问号应保留 |
| RA07-Q002 | RA07-P003-U009 / T-P003-009 | Remark(2) 的对象候选为闭矩形/闭长方体，但字形不足以唯一确定 |
| RA07-Q003 | RA07-P010-U008 / T-P010-008 | Vitali 行起首动词、名字后的连接字和原稿拼写保留不确定性；`Vatelli`、`[2,3]^c` 等片段清楚 |
| RA07-Q004 | RA07-P011-U008 / T-P011-008 | `m*(T∩A)+m*(T∩A^c)=m*(T)` 前三个连接字无法唯一辨认，公式本体清楚 |

### 九个未决 source units / 26 个未决 target units

`RA07-P001-U013`、`RA07-P003-U007`、`RA07-P003-U009`、`RA07-P005-U007`、`RA07-P006-U009`、`RA07-P010-U008`、`RA07-P011-U008`、`RA07-P011-U010`、`RA07-P006-U014` 仍为 ledger 的 `unresolved`。对应 target 未决计数为 26（含 transcription 和 study 的原位转写/补证目标）；这与保守策略一致，没有把不确定笔画升级为确定文本。

### Recovery

11 个 recovery proposal 中 8 个已解决，`VS-REC-004`（p0005 I/G）、`VS-REC-006`（p0006 左页缘残弧）和 `VS-REC-010`（p0011 双重补集小注第二字）仍未选定候选。三项均已实际回看整页/重叠区，但前向笔形和反向数学语境都不足以唯一选字；本报告不替其选择候选。

### 冻结判定

若“冻结”允许源稿字形和未完成处以红色/中性标记显式保留，则当前稿具备可追溯性：source unit、target marker/text hash、证据和恢复候选均可回链，且未见新的致命内容错误。若冻结要求上述九个 source unit 及三个 recovery 全部确定，则状态应保持 conditional_hold，直至完成独立确认。

## 操作记录

只读取并核验了当前快照，写入本目录的 `blind-reading.md`、`report.md` 和 `review-record.json`。没有改动正文、ledger、配置、第二阶段证据或其他审查记录；没有执行 Git 操作。
