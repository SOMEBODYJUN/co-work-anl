# RA06 final-02 独立终审复核报告

- `reviewer_id`: `RA06-final-02-source-first`
- `session_id`: `/root/ra06_review_02`
- `review_mode`: source-first；先独立查看原 PDF 的全页与 36 个重叠区，再读取 integration-v2 正文、mapping、ledger、视觉第二遍证据与数学补证
- `scope`: 冻结候选 `proposals/integration-v2/`、`ledger-integration-v2.json`、`ledger-config-v2.json`、`proposals/integration-v2/mapping.json`、视觉第二遍证据以及源图像/裁图
- `结论性质`: 条件性终审意见。本报告不写入 `ledger.final_rounds`，不执行 seal，也不修改冻结正文、ledger 或已有审查记录。

## 1. 盲读顺序与视觉范围

本轮先打开 `source.pdf`（manifest 中原名 `实分析6.pdf`）的六张全页渲染图，再逐一查看 2×3、8% 重叠的 36 个区域，观察记录写入 [blind-reading.md](blind-reading.md)。在这一阶段没有读取当前正文、mapping、ledger、issues 或视觉第二遍结论，也没有用数学标准式替换源图字形。随后才读取冻结候选、mapping、ledger-config、ledger、`unresolved.md`、visual-second JSON/Markdown 与研究补证。

六页和六区盲读要点如下：

- p0001 是黑色主线与蓝色闭性、有限覆盖补充交错的紧性/拓扑页；T1/T2、球交和有限覆盖段跨区，右侧和底部有浅蓝笔。
- p0002 是列紧、Heine–Borel 与嵌套方块的续页；下边界附近的蓝色不等式逐区复核，初始方块端点、指数和“有限”后字均保留字形风险。
- p0003 以蓝色嵌套方块/导集补注为主，黑色闭包段在下半部；δ 的附笔、闭性前缀和 `E` 上标均不能仅凭数学路线定字。
- p0004 交错记录完全集、拓扑计数、基与最大开区间；Ex1 计数对象和 `G_x` 右半串是独立未决区域。
- p0005 是构成区间、连通分支与进制展开提示；标题词形与进制证明的红色未完边界均可见。
- p0006 六区均为空白，未在正文、学习版或映射中虚构该页内容。

第二遍证据的 13 个裁图也已逐一打开：`p0001-margin`；`p0002-cube`、`p0002-reduce`、`p0002-top`；`p0003-closed`、`p0003-derived`、`p0003-sequence`、`p0003-side`；`p0004-basis`、`p0004-claim`、`p0004-ex1`；`p0005-proof`、`p0005-rn`。裁图支持局部回看，但没有授权把蓝色补证写成黑色原笔。

## 2. 输入快照、覆盖和哈希

### 2.1 源与渲染快照

- `source.pdf` SHA256：`c089cd714af04d97bfbf17a031881acd508ebd70b2f5221aa745bc5253b6db89`。
- `manifest.json` SHA256：`51bc0d36d72b940cefa5645e38ebdd52327c4dc40f4183816b93e856423c642a`；ledger 的 `manifest_sha256` 与之相同。
- 六张全页渲染图哈希：

| 页 | SHA256 |
|---|---|
| p0001 | `2953eae100c8e5ec3183e0442c21e48d59b0d98b4ed9e731b6cbfc4d859b1714` |
| p0002 | `31b262460e36df3b980c4c9c3bef2063e9d5bb063b1093322f7b5ef8c3ca3e80` |
| p0003 | `43aa288c5ab9b287d1181f3e763571c2d3f7d063f9bc39d923e614fab1e1f398` |
| p0004 | `7f06b65de54b1b737db7647cf7b65533165b75ba814cc663ee8d2c5f0ce21c78` |
| p0005 | `850659b19def05dedabdf2732f5041e5ccc2300a6185cd86289f804b8aaa4c14` |
| p0006 | `fcd191ffdfd24d771bcb32a9004529cf3f7caba40da865aa3ba6a52ab187dfd3` |

### 2.2 正文与台账哈希

| 文件 | SHA256 |
|---|---|
| `proposals/integration-v2/source-transcript.md` | `9614f4e85e08f08d459fd7ad2c9efb3649b8b1e583c3099e5deff9beb87f822e` |
| `proposals/integration-v2/study-notes.md` | `147aa7565b23aa6c8e67482626f21e624010917c9e454d568c347aa7c1bb7c9e` |
| `proposals/integration-v2/mapping.json` | `306239caf9f93c19bac0eb40f3459fa510750b1d74a1f21818af04b97235ac82` |
| `proposals/integration-v2/unresolved.md` | `4be52b793061b94d841254318494c5ef6bc556b584d0ddb009a8a3ad4db4e239` |
| `ledger-config-v2.json` | `f0477d606dc4048bf0669994f9d7a83744d8d87a3579ac9eeac89c312bd491fa` |
| `ledger-integration-v2.json` | `8d2105e98acc4e19a99785fa65d8512f251d6fe359f12963e340fe42319e22e7` |
| `reviews/final-02/blind-reading.md` | `a4e4a266e9818a7d20881c44ad4ffe6663aae4696faded1ae2b06b7b079181d2` |

The mapping hash above was recomputed from the current file; it is recorded here as a review snapshot and was not written back to the ledger.

按 `tools/build_ledger.py` 的 `marker_spans` 规则重算每个 target 的 `text_sha256`：`start_line` 到 `end_line` 均包含 unit marker 行，行间使用单个 LF。199/199 个 target hash 全部匹配（0 mismatch）。ledger 列出的 29 个 artifacts 逐一重算也全部匹配（29/29，0 missing、0 mismatch）；`manifest_sha256` 与 manifest 实体哈希一致。此前若以不含 marker 行的切片重算会得到不同值，但那不是本项目的哈希规则，本轮不把该算法差异报告为问题。

### 2.3 source–target 覆盖

- source units：78；其中 69 `resolved`、9 `unresolved`。页分布为 p0001 15、p0002 14、p0003 19、p0004 18、p0005 12，p0006 为 0。
- target units：199；其中 174 `resolved`、25 `unresolved`（转写与学习版合计）。
- `mapping.json` 的 199 个 target 对 78 个 source id 的引用重新核对：78/78 source id 均有 target 映射，缺失 0，未知 source id 0。
- ledger 中第二遍 page checks 为 6/6，assessment 分别是 p0001 `content`、p0002–p0005 `unresolved`、p0006 `blank`。
- 第二遍 region checks 为 36/36：`content` 19、`unresolved` 11、`blank` 6；p0006 六区全部 `blank`。区域数、页区对应关系和源单位证据指针相符。
- ledger 初始已有 `recoveries` 19、`issues` 10，`final_rounds` 在本轮开始时为 0；本 reviewer 没有写入 final round。

## 3. 黑/蓝/红层与逐页数学复核

### p0001：紧性、T1/T2 与有限覆盖

黑色转写保留 Lindeloff 拼写、第二可数关系、T1/T2 的原顺序、球交空式和有限子覆盖括注。蓝色层将度量球分离、`δ_y=d(x,y)/3`、有限球并推出有界、闭性收尾和空集边界单独写成补证；这使 T1 与真正需要的 Hausdorff/度量分离没有被混为一谈。`B(y,δ_{y_i})` 的球心下标属于记号订正，黑色原笔不被伪装为已经写出下标。`有界` 与 `有限` 也保持区分。独立推演后，这些蓝色结论成立，没有新数学缺陷。

### p0002：列紧、Heine–Borel 与嵌套方块

`T-p2-01` 两处“有限[Q006]”保持中性；`T-p2-04` 的初始方块右端点/指数保持 Q002a/Q002b 占位。黑色 `[-a,a)^n` 的半开形状保留，蓝色另给规范闭方块 `[-a,a]^n`，并明确这不是字形恢复。有限维赋范空间中闭有界与列紧/紧的条件化证明、一般度量空间紧与列紧的等价、Heine–Borel 方块二分、`2^n` 子块计数和直径趋零均复核通过。初始选择与后续下标的差异没有被黑色静默修正。

### p0003：嵌套方块、导集与闭包链

黑色保留 `x_{m+1}∈Q_m\Q_{m+1}`、子列/极限点及原始 `δ` 记号；蓝色明确指出该选点与末行直径之间的下标错位，并给出改下标或重选点的补法。`Q007` 的 δ 后小笔、`Q008` 的闭性补记前缀、`Q009` 的 `E` 上标均保持 unresolved。E′ 闭性、孤立点分解和高阶导集的范围经独立检查成立；离散单点反例说明不能从蓝色公式反推原上标。红色 proof/下降关系仍标示原稿未完成，蓝色补证没有抹掉该事实。

### p0004：完全集、拓扑计数、基与最大开区间

`T-p4-02` 的 Ex1 中间词/计数对象保持 Q003。学习版将通常实轴开集数 `c`、通常基的种数 `2^c`、幂集大小 `2^c` 和同一底集上全部拓扑数 `2^{2^c}` 分开，以条件化方式给出补证；没有用原笔 `2^c` 单独决定题目。`∅=U` 的黑色等号保留，蓝色说明后文取 `x∈U` 需要非空开集。Q004 的 `G_x` 右半串只保留为未决，不用端点证明反推变量和下标。最大开区间的 `inf/sup`、有限端点不在开集内以及无穷端点分支均成立。

### p0005：构成区间、连通分支与进制展开

构成区间的合并/唯一性路线、第二可数局部连通空间至多可数个连通分支均与原图对应。`T-p5-04`、`T-p4-13`、`T-p4-14`、`T-p5-11` 的红色未完证明标记仍在，学习版蓝色补证被明确当作后加内容。`T-p5-10` 题头保持 Q010，不在“实区间均连/构造”之间替字；p 进制展开的存在性、至多两种展开以及闭区间逐次分割路线均检查通过，两条数学路线都不足以唯一恢复题头。

### p0006：空白页

六区均为空白；正文、学习版和 mapping 未生成第六页内容。

## 4. 九项未决恢复与 25 个未决 target

本轮确认以下 9 项 recovery 继续为 `status: unresolved`、`selected_candidate_id: null`；蓝色证明的成立不改变原笔字形的不确定性：

| recovery | 原始范围 | 复核结论 |
|---|---|---|
| `VS-REC-Q002` | p0002 `RA06-P002-U04` | 初始方块右端点与指数不能由规范 `[-a,a]^n` 反推；保留 Q002a/Q002b。 |
| `VS-REC-Q003` | p0004 `RA06-P004-U02` | Ex1 中间词和计数对象仍有多个数学解释；继续条件化。 |
| `VS-REC-Q004` | p0004 `RA06-P004-U12-B` | `G_x` 右半变量、关系符、下标未唯一；不以端点证明补字。 |
| `VS-REC-Q006-FINITE` | p0002 `RA06-P002-U01/U01-B` | “有限性/有限维”未唯一；补证只在明确条件下成立。 |
| `VS-REC-Q007-ENDPOINT` | p0002 `RA06-P002-U04` | 初始方块右端单拱可能为 `a` 或 `n`；保留。 |
| `VS-REC-Q014-SUPER` | p0003 `RA06-P003-U16` | `E` 上标内部圆圈/导号不能唯一判读。 |
| `VS-REC-Q016-TITLE` | p0005 `RA06-P005-U10` | “实区间均连/构造”两条可行数学路线均存在。 |
| `VS-REC-Q017-DELTA` | p0003 `RA06-P003-U06` | `δ` 后小笔可能是下标 0 或收笔。 |
| `VS-REC-Q018-PREFIX` | p0003 `RA06-P003-U15` | 导集闭性旁注前缀未定，不能假称此前已有完整证明。 |

对应的 25 个 unresolved target 为：

`T-p2-01`, `N-p2-01`, `N-p2-scope`, `N-sequential-equivalence-proof`, `T-p2-04`, `N-p2-04`, `N-p2-cube-exponent`, `T-p3-06`, `N-p3-06`, `N-p3-radius-convention`, `T-p3-15`, `N-p3-15`, `N-derived-closed-proof`, `T-p3-16`, `N-p3-16`, `N-p3-closure-scope`, `T-p4-02`, `N-p4-02`, `N-topology-count-candidate`, `T-p4-12-b`, `N-p4-12-b`, `T-p5-10`, `N-p5-10`, `N-interval-connected-proof`, `N-connected-subset-interval`。

这些 target 与 ledger 的 source status、recoveries 和 open issues 一一对应；本轮未新增 issue/task ID，也未把任何既有 unresolved 改成 resolved。

## 5. 复核意见

独立 source-first 复核没有发现新的数学错误、源目标漏映射、黑蓝红层越界、区域缺失或哈希不一致。当前候选的安全边界是：黑色尽量保留源笔，蓝色显式表示订正/补证/条件化解释，红色保留原稿未完证明；9 个未决 recovery 与 25 个未决 target 仍可追溯并未被数学可行性偷换为字形确定。

这不是“通过”声明。最终 seal 前仍应由 root 确认上述 9 项 recovery、25 个 target 的未决状态是否符合项目合同，并按合同决定是否写入 `ledger.final_rounds`；本 reviewer 不代写该台账字段。冻结正文、ledger、mapping、已有 reviews 均未修改，也未执行 Git。
