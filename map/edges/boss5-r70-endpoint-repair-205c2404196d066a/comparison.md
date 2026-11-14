# R70 同一完整策略的两个精确输入

## 登记与逐历史核对

`M-c5e460641b3e47729159aa9e7cb6a175` 的主陈述是一个 58 客户输入的全部完整纯 SPE。`cag-r70-six-player-seven-topic-fixed-complete-strategy-lp` 的主陈述量化指定完整策略 σ 的全部非负、非零客户类型向量中满足完整纯 SPE 约束者，并用独立的 11 客户点取得下界。两点审计文件的 `points.random` 和 `points.lp_integer` 分别核验这两组输入。正文的“随机58点”和“LP十一点”小节分别归前者主陈述和后者证据。

| 输入 | 非零掩码及重数 | 同覆盖标签 | σ 的根福利 $W$ | 六槽最优 $\mathrm{OPT}_6$ | 比值 |
| --- | --- | --- | ---: | ---: | ---: |
| 58 客户 `random` | 1:9, 2:2, 8:2, 20:34, 32:5, 64:6 | 2、4 | 43 | 58 | 43/58 |
| 11 客户 `lp_integer` | 2:1, 5:6, 8:1, 16:1, 32:1, 64:1 | 0、2 | 6 | 11 | 6/11 |

两行都绑定 SHA-256 为 `d2924549f6ea10bd9a732434bef8145694e2bcbbec471abdef60d8d609687141` 的有序动作表。它在两输入都走 $(0,2,2,2,2,2)$。58 客户点沿路径覆盖标签 0 的 9 客户及标签 2 的 34 客户，六槽选择 $(0,1,2,3,5,6)$ 覆盖全部。11 客户点沿路径只覆盖兴趣为 $\{0,2\}$ 的 6 人，六槽选择 $(0,1,3,4,5,6)$ 覆盖全部。两点的正支撑不同，因此不能用同一比例缩放得到另一点。

从保存的动作表，在每个有序历史 $h$ 用 σ 完成规定终局，再对每个标签 $b$ 强制首步并用同一 σ 完成改变后历史。两点各回算 19,608 个历史的全部七个选择、共 137,256 项含自身比较，与保存的支付尺度 60 的整数余量逐项相同。两点各有 924 个终局计数，覆盖与均分收益也逐项回算。最小动态 IC 余量均为 0，紧项分别为 37,357 和 39,531。静态诊断各有 6 和 37 个 PNE 计数。

58 客户点的全 SPE 断言另用不交极大块的结构定理及同覆盖标签商。若 34 客户块终局有至多四人，四个小块上的任一玩家可改至该块取得至少 $34/5>6$，故 PNE 中这些小块全空。余下至少两人挤在 9 客户块，各得至多 $9/2<34/5$，也可改进。若 34 客户块有六人，则改至空的 9 客户块有利。故 34 客户块恰五人，且另一人必须占 9 客户块，否则有人可从 34 客户块改到空着的 9 客户块。完整 σ 给至少一份 SPE。同覆盖类的代表可按有序历史选取，保持逐客户收益与真实后继，故商策略可分别提升为 $(1,0,j,0,5-j,0,0)$，$j=0,\ldots,5$。

11 客户点的所有真实 IC 非负，给指定 σ 锥的取等证据。七个遗漏标签分支的证书合计使用 21 条真实 IC。定向回算从 σ 重建了 3,048 个去重键，并逐类型重算七组有理余量共 889 项，每组最小值为 0。遗漏 0、2 给 $6/11$，其余分支给 $3/5$ 下界。对任意锥内非零向量，取实现真实 $\mathrm{OPT}_6$ 的遗漏标签，得 $W\ge(6/11)\mathrm{OPT}_6$。11 客户点给等号，58 客户点给同锥内严格较大的比值 $43/58>6/11$。这些结论仍限于相应的一个输入或一个固定 σ。

## 旧推导处置

`map/edges/customer-attraction-3a-3a-a8bf604bd9813bf3/r70-point-attains-fixed-cone-six-eleven.json` 的 `roles` 和 `contribution.result` 把 11 客户取等向量及其审计归给 M-c5e，由此提出 `implies`。M-c5e 的已登记向量有掩码 20、无掩码 5，福利比为 $43/58$，所以该前提不能支付这项取等。退休旧边，保留 `cag-r70-same-sigma-two-input-check` 的语境比较。现行登记只有固定 σ 锥定理的陈述及证据收录该确切 11 客户点。同样为 11 客户、$W=6,\ \mathrm{OPT}_6=11$ 的八标签 mask134 对象使用不同目录及策略。

## 固定锥证明包的归属文字

`map/edges/customer-attraction-3a-3a-4b2f43276f388bc1/fixed-sigma-cone-six-eleven.json` 的 `explanation` 写有“read-add 后的 M-c5e 精确点在同一 σ 上逐历史核验 137256 条比较”，`review_note` 写有“因下界依赖另一个登记对象，先通过 map read-add 加入 M-c5e...”。该边的真实输入是 `CAG-MODEL` 和 `CA-STRATEGY-CONE`，取等证据是所引 `point-audit.json` 的 `points.lp_integer` 和固定锥定理登记证据。数学证明已足；将归属改为独立 11 客户点即可。

同目录 `support.md` 的“Exact lower bound and attainment”首段写有“The added dependency `M-c5e460641b3e47729159aa9e7cb6a175` was read through `map read-add` because its paired exact audit supplies the lower endpoint. Its 11-customer point has multiplicities”。`review.md` 的“读取与对象边界”首段写有“把下界达到性所需的 deferred candidate `M-c5e460641b3e47729159aa9e7cb6a175` 通过 `map read-add` 正式加入后读取其 README、point-audit 和整数点文件”，`readledger.json` 的 `read_add[0].reason` 将 11 客户点的需要与对象 read-add 直接相连。这些处可以保留历史操作，并把证据来源写成共用审计中的独立 `lp_integer` 输入。

`map/receipts/customer-attraction-3a-3a-4b2f43276f388bc1.json` 的固定锥 `coverage.reason` 写有“M-c5e read-add 的独立 point-audit 在同一 σ 上核验 11 客户点”，`comparison_note` 写有“M-c5e point-audit, CAG-MODEL, and CA-STRATEGY-CONE are declared read dependencies used to establish the fixed-cone lower bound”。改为从固定锥对偶得下界，从独立审计 `points.lp_integer` 得取等。此任务的写入范围只覆盖 a8bf 替代批。
