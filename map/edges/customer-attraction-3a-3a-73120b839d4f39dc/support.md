# 支持账本：对角基础行拆分后的有理必要点

内部标识：`SOLVER-DIAGONAL-SPLIT-FRESH`。

## 精确对象记录

| 项目 | 本批核定值 |
|---|---|
| object | `customer-attraction/diagonal-basic-row-split-exact-necessary-point` |
| truth status | `proved`（固定必要系统点的精确有限证书；正文同时标注 not-SPE/not-exact-optimum） |
| model | 六人共同目录完整历史纯 SPE 的必要行松弛；固定 16 hist 支持、1905 列 |
| quantifiers | 固定有理向量与指定 3945 行；189 个 overlap 反例逐项，而非排除所有重排点 |
| exact point | `O=1`, `W=77122220724026571141557320969163/161324472800190691224726909402699`, `K=244540039145754511523049866718091/1075496485334604608164846062684660` |
| checks | 3945 行、1905 列、165 正列、2232 零 slack、零负 slack；旧 3889/新 56 的零数为 2222/10 |
| literal obstruction | 189 overlap 列低于 `max(0,r1+r2-h)`；列 992/hist 117 给 `r1=r2=h>0,v=0` |
| open obligations | 共同会员测度、全部真实历史 SPE、exact optimum、一般六人 half、重排 `hist/R` 或后继 `Z` 点均未由本证书支付 |

## 56 条拆分的承重关系

在同一完整六人策略及真实尾语义下，`R_ij` 和 `Z_ij` 各自有 source、terminal/query、
reverse-terminal、price、capacity 与强 PAIR 必要式。对 `i!=j` 求和给 30 条，
对 `i=j` 求和给 6 条；每类原始局部式分别非负，故 56 条各自是合法必要和。
四态质量使用

`v00*h + Σ_{s∈{01,10,11}} (v(s)-v00) y_s`，并不假设 R/Z 独立；新增行的
1306 overlap 列系数为 0。28 个逐列加回恒等式及容量 `30K+6K=36K` 由程序
正文和冻结点证据承载，未把“至多 28 个线性方向”误写成秩恰 28。

## 数值回放与限制

`summary.json` 的回放只调用一次原 `build()`，没有再次运行原 CLI、优化器、LP、
随机程序或 SPE 搜索；独立 56 行审计是已有证据而非本批新执行。`all-row-slacks`
完整回代显示当前新点的全部 3945 行非负，所以 `W<1/2` 是 necessary relaxation
的数值现象，不能作为完整博弈的福利反例。189 个 overlap 下界差额只证明字面联合
实现失败；把 overlap 改为 `min` 或重排质量后必须在新点上重核所有行。

## 指定 peer 的关系结论

peer `customer-attraction/diagonal-reply-budget-split-basic-graph-program` 是普遍
真实行拆分引理，核心点是固定有限编码证书。当前没有已发布 3B successor task，
也没有支付“程序引理 ⇒ 当前点整体结论”的方向、反向或等价条件。故本批保持
`isolated-after-review`，不造语境边冒充逻辑边，也不把固定必要点提升为 SPE/half。
