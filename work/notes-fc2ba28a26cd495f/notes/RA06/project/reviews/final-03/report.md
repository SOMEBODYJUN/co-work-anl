# RA06 final-03 独立最终候选复核报告

## 结论

**本轮没有新发现。** `new_findings=[]`、`new_issue_ids=[]`。结论只表示相对于本次从源件逐项重读所发现的新增问题为空；当前快照已有的未决项不被关闭，也不据此声称整体无遗留问题。

推荐继续**条件保留**当前 integration-v2 候选，保留以下未决集合，交由 root 决定 `final_rounds` 与最终 seal：

- recoveries：19 条中 10 条 resolved、9 条 unresolved；未决 IDs 为 `VS-REC-Q002`、`VS-REC-Q003`、`VS-REC-Q004`、`VS-REC-Q006-FINITE`、`VS-REC-Q007-ENDPOINT`、`VS-REC-Q014-SUPER`、`VS-REC-Q016-TITLE`、`VS-REC-Q017-DELTA`、`VS-REC-Q018-PREFIX`。
- target units：199 条中 174 条 resolved、25 条 unresolved。
- issues：10 条中 2 条 resolved、8 条 open；当前 open issues 均对应已保留的字形/题意不确定性。

## 复核范围

### 源 PDF 与视觉证据

- 原始输入：`input/pdf/实分析6.pdf`；项目源副本：`source.pdf`；SHA-256：`c089cd714af04d97bfbf17a031881acd508ebd70b2f5221aa745bc5253b6db89`，二者字节一致。
- 读取 `manifest.json`（SHA-256 `51bc0d36d72b940cefa5645e38ebdd52327c4dc40f4183816b93e856423c642a`）并按其 6 页、2×3 分区方案逐一查看：6 页整页、36 个分区全部覆盖；第 6 页及其 6 个分区确认空白。
- 额外查看登记的 13 个 crops：`p0001-margin, p0002-cube, p0002-reduce, p0002-top, p0003-closed, p0003-derived, p0003-sequence, p0003-side, p0004-basis, p0004-claim, p0004-ex1, p0005-proof, p0005-rn`。
- 页图哈希均按 manifest 与当前快照复核；没有出现渲染替换或证据路径漂移。

### 正文与映射

- `source-transcript.md` 70 个原稿 marker units（298 行）；`study-notes.md` 129 个学习 marker units（756 行）；ledger target units 199。
- `source-units.json` 78 个 source units，全部有目标映射；mapping 199 个 target IDs 与 ledger 完全相同，正向和反向 source↔target 引用均一致；`remaining-mapping-ids.json` 为空。
- 按 ledger 的 marker-span 规则（`start_line..end_line`，单 LF 连接、不加尾 LF）重算，199/199 个 target text hashes 匹配。

### Recoveries、issues 与其他证据

- 全量读取 ledger 中 19 条 recoveries、10 条 issues，并与 `unresolved.md`、`source-split-adoption.json`（32 条拆分采用）、`new-crop-register.json`（9 条新增裁图）、`observations.json`/`observations-author.json`（各 6 页+36 区）、`integration-progress.json`、`two-point-enumeration.json`、`terminology.md`、`editorial-record.md` 交叉核对。
- ledger 当前 page checks 12 条、region checks 72 条，`final_rounds` 仍为空。mapping、source units、ledger、ledger-config、正文及 29 个 ledger artifacts 的哈希全部与冻结快照一致。

## 源件逐页要点

| 页 | 从源件直接确认的内容 | 整合版处理是否出现新增缺陷 |
| --- | --- | --- |
| p0001 | 紧性/Lindeloff；第二可数蕴含 Lindeloff、末字“逆不真”；T₁/T₂；紧集闭且有界的有限子覆盖路线；交式球心原笔漏下标；两点非 Hausdorff 紧开集反例。 | 未见新增缺陷；原笔漏下标与 T₁/T₂ 分层被保留/说明。 |
| p0002 | “有限[Q006]”提要；闭子集引理；Hine Borel；Q002a/b 右端点与指数未决；半开括号原形；二分嵌套方块和直径式。 | 未见新增缺陷；数学闭方块修复和原笔形状分开。 |
| p0003 | 方块差集选点、收敛子列、开球矛盾；自密/闭集/导集；Q007、Q008、Q009。 | 未见新增缺陷；下标修复、普通并号与严谨说明分层。 |
| p0004 | 完全集；Q003 的 `2^c` 题意歧义；原 `∅=U`；Q₁/Q₂、基计数、`G_x` 与 Q004；最大区间证明未完。 | 未见新增缺陷；非空纠错和数学候选都标为补充。 |
| p0005 | 构成区间及不相交/唯一表示；高维表示不唯一；第二可数局部连通分解；Q010 与未完 p 进制提示。 | 未见新增缺陷；“至多”与未完状态均保留。 |
| p0006 | 全页和六区均为空白。 | 空白页未被正文或映射虚构为知识单元。 |

## 数学与层级复核

本轮逐段检查学习稿中的条件和补证边界：

- Lindelöf/第二可数、度量空间紧集闭且有界、闭子集紧、Heine–Borel 的补证均带有相应的空间/开集条件。
- `Q_002` 的数学规范 `[-a,a]^n` 与原稿 `[Q002a]^[Q002b]` 分开；半开方块为何不能直接用于紧性有明示纠错。
- `Q006` 不把一个集合的“闭且有界”偷换成整个赋范空间“有限维”；有限维候选另列完整量词和 Riesz 引理证明。
- 导集、孤立点、自密、闭集分解中，原稿普通并号/集合与元素混用均以蓝色说明纠正，原黑色式保留。
- `Q003` 的通常开集数、通常拓扑基数、底集上全部拓扑数三者明确区分，`2^c` 不被强行归题。
- 最大开区间、构成区间、不相交分解和局部连通空间的开集分支定理都标明了“开集”条件；原稿未完段落仍用红色保留。
- 以上检查未产生新的数学错误、source-target 错配或黑/蓝/红层缺陷。

## 哈希和完整性

- PDF 源哈希、manifest、source transcript、study notes、mapping、source units、ledger-config、ledger 均记录在 `review-record.json`；项目 ledger 登记的 29 个 artifacts 全部匹配（0 mismatch）。
- 199 个 target text spans 全部匹配（0 mismatch）。
- 本轮未修改冻结正文、映射、ledger 或任何既有证据文件；未使用 Git。

## 最终状态

- `new_findings: []`
- `new_issue_ids: []`
- `mutated_frozen_artifacts: false`
- `mutated_ledger: false`
- `git_used: false`
- `pass_claim: false`：因为仍有 9 个 unresolved recoveries 和 25 个 unresolved targets；“无新增发现”不等于“所有遗留已解决”。
