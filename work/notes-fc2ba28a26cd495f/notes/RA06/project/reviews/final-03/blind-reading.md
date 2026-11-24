# RA06 final-03：独立 source-first 盲读记录

## 复核身份与冻结边界

- 复核员：`RA06-final-03-source-first`；会话：`/root/ra06_final_03`。
- 本次从原始 PDF 开始，先完成全页和全区源读，再读取整合版正文、映射、ledger、recoveries、issues、证据登记与哈希；没有读取或引用前两轮 final 报告的结论。
- 只在 `reviews/final-03/` 新增本轮三个复核文件；没有改写正文、映射、ledger 或其他冻结快照文件，也没有使用 Git。

## 源件范围与哈希

- 输入 PDF：`input/pdf/实分析6.pdf`；项目副本：`source.pdf`；两者字节一致，SHA-256 均为 `c089cd714af04d97bfbf17a031881acd508ebd70b2f5221aa745bc5253b6db89`。
- `manifest.json` SHA-256：`51bc0d36d72b940cefa5645e38ebdd52327c4dc40f4183816b93e856423c642a`；清单声明 6 页、每页 2480×3509 像素、2 列×3 行、共 36 个分区。
- 实际逐页打开 `p0001`–`p0006`，逐区打开 36 个 `pXXXX-rNcM`；另查看了 13 个登记证据裁图。第 6 页的整页及 6 个分区均为空白，未发现字符、公式、图形、旁注、页码或待填标记。
- 页图哈希按 manifest 逐页锁定：`p0001=2953eae100c8…`、`p0002=31b262460e36…`、`p0003=43aa288c5ab9…`、`p0004=7f06b65de54b…`、`p0005=850659b19def…`、`p0006=fcd191ffdfd2…`。

## 全页盲读结果

1. **p0001：**紧性、Lindeloff 定义及“第二可数蕴含 Lindeloff、逆不真”原句和右上双向旁注；有界闭集/紧集定理的黑蓝混合证明；T₁/T₂ 分离标记、有限子覆盖、最小半径；页末两点拓扑反例。末行有限子覆盖交式中的球心原笔未见下标，保留为原样并由蓝色说明规范为 `y_i`。
2. **p0002：**首部含“有限[Q006]”、列紧与闭集有界提要及闭子集引理；“Hine Borel”原拼写；有界集嵌入方块、Q002a/b 右端点/指数未决、下一行半开括号原形、二分 `2^n` 方块、嵌套链和直径式。蓝笔证明在页末续至 p0003，未在 p0002 结束。
3. **p0003：**从 `x_(m+1) ∈ Q_m \ Q_(m+1)`、点列和收敛子列到开球矛盾；黑笔自密、闭集判别、导集迭代与完全集相关公式；浅色左右方向旁证、导集闭性提示、闭包/内部/边界分解。δ 附笔、浅色前缀和分解式小上标仍按 Q007/Q008/Q009 保留未决。
4. **p0004：**完全集定义；Ex 1 的 `2^c` 计数行和右侧幂集旁注（Q003 题意/字形未决）；`∅=U` 的原等号及蓝色非空纠错；Q₁/Q₂；Ex 2 基的计数和局部条件；`G_x`、`α,β`、最大区间断言与 Q004 未决右半关系式。原证明只写到任取 `y` 和“反证，若不然”。
5. **p0005：**构成区间定义、不同构成区间不相交命题及未完反证；两点对应区间“相等/不相交”推论；唯一表示和高维可数但不唯一旁注；第二可数局部连通空间的连通分支分解；末尾“实区间[Q010]”和 `p` 进制小数“至多有两种展开”提示，证明未续写。
6. **p0006：**全页及六个分区确认为空白，不进入正文或 source-unit。

## 正文、映射和证据复核

- `source-transcript.md`：70 个 marker units；`study-notes.md`：129 个 marker units；ledger 共 199 个 target units。正文 marker 与 ledger 的 artifact、行号范围一一对应；199/199 个 target text hash 全部匹配，未发现缺行、漂移或未映射 marker。
- 78 个 source units 全部有至少一个 target 映射；mapping 的 199 个 target id 与 ledger 完全相等；source↔target 反向引用无断裂。`remaining-mapping-ids.json` 为空。
- 19 条 recovery 全量阅读：10 条已恢复、9 条仍 unresolved。9 条未决为 `VS-REC-Q002`、`VS-REC-Q003`、`VS-REC-Q004`、`VS-REC-Q006-FINITE`、`VS-REC-Q007-ENDPOINT`、`VS-REC-Q014-SUPER`、`VS-REC-Q016-TITLE`、`VS-REC-Q017-DELTA`、`VS-REC-Q018-PREFIX`；它们在正文/`unresolved.md` 中都仍以候选或 Q 标记保留，没有被数学补证静默定字。
- 10 条 issues 全量阅读：当前 2 条 resolved、8 条 open；open 项与上述未决字形/题意相符，没有发现 issue 状态与正文标记相互矛盾。
- 13 个登记证据裁图、6 页图、36 区图的文件哈希均属于当前 manifest/ledger 冻结范围；ledger 登记的 29 个 artifact 哈希全部与磁盘一致。

## 独立结论

在这次独立 source-first 复核中，没有新增 source-target 缺失、字形误定、黑/蓝/红层混淆、数学补证冒充原稿或哈希漂移。`new_findings` 与 `new_issue_ids` 均为空；现有 9 个 unresolved recoveries 和 25 个 unresolved targets 继续保留，不将“无新发现”写成全部无遗留问题。
