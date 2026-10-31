# UM-TWO-WITNESS-QUERY-COUNT-FEE-v3：独立审查与 read-after

审查者：general_query_response_review。2026-10-18。

读取次序：先只读 v3 Exact，独立验证 heavy/no-heavy 分组及整数费用推论并向 parent 冻结判断；之后首次读 v3 Proof。旧 v1 零错误审查、v2 Exact/Proof 及各 read-after 记录均保持不改。

冻结输入 SHA-256：

- Exact：`fda4d7ef5f6534b020bd3461d66d135406dad46ce8b178566397495d7c8fe362`
- Proof：`497b3ca00e9df3091552cd24c6942f8f891712d2df64d04baac19e9c2a036ac8`

**结论：v3 新增 heavy 必要条件与作者证明均通过，未发现 fatal。v2 既有部分的范围未变。**

## 独立推导

令 `c=β−1≥1/2`。heavy 查询定义为初态单件时间严格大于 cT；数量 H，其余 nonheavy 查询数量 `S=d−H`，包括等于 cT 以及零时间的查询。

把 Rβ 台查询旧端总量严格大于 cT 的机器划分为：

1. 含至少一枚 heavy 查询的机器。这些机器的源 query 集互不相交，每机可选一枚 heavy 作为见证，故机器数≤H。这里甚至不需要额外使用 c≥1/2；不会重复计算同一 heavy。
2. 不含 heavy 的机器。每枚源查询旧端≤cT，单枚不可能形成严格总量>cT，故每机至少拥有两枚 nonheavy queries。不同机器的源组互不相交，因此此类机器数≤floor(S/2)。含 heavy 机器可能另外消耗若干 nonheavy，只会使此上界更松，不会导致重计漏洞。

所以

\[
R_\beta\le H+\lfloor S/2\rfloor.
\]

结合 v2 同族的坏查询→重机单射，

\[
|G|\ge d-R_\beta\ge S-\lfloor S/2\rfloor=\lceil S/2\rceil.
\]

在既定条件“每个合法 singleton 在峰≤βT 时的非查询改派费至少 F>0”下，每个 q∈G 的实际输出都适用该条件。支持不交给费用总和≤W，因此

\[
W\ge |G|F\ge\lceil S/2\rceil F.
\]

若另有 `W≤κF`、有理 `κ≥0`，则非负整数 `ceil(S/2)≤κ`，所以 `ceil(S/2)≤floorκ`，继而 `S≤2floorκ`、`H≥d−2floorκ`。

## 边界与作者 proof 对照

- `p_old=cT` 属于 nonheavy。单件恰等于阈值仍不能使机器查询总量严格超阈值，故至少两枚的计数正确。
- `S=0` 时只保证零枚合格，费用下界 W≥0；不会从中凭空保证某 singleton 可行。
- κ=0 或 0<κ<1 时 floorκ=0，必要结论为 S=0、H=d。该必要形状不声称构造存在，也不推出所有 singletons 可行。若根本不存在峰≤βT 的某查询 singleton，其物理费用下界可以是空真；作者明确允许这种情形。
- κ 非整数时必须向下取整，作者证明正确使用 floorκ。例如 κ∈[1,2) 时最多允许 S=2，不会把 κ=1.9 松成 S≤3。
- W=0 与 F>0 时公式仍成立，只迫使 G 为空及 S=0；未错误使用严格负费用。
- W≤F 给 H≥d−2；d≤2 时结论可能平凡。β=2−ε 仅在既定 β 域中解释，即 `0<ε≤1/2`，其 heavy 阈值正是严格 `>(1−ε)T`。
- 所有费用推论都保留已有 F 下界假设；单凭 good 数目与任意权不能无条件推出 W≥ceil(S/2)F。作者的新增段落承接前文该费用条件，未引入无条件的收费结论。
- heavy 识别只需有理数比较，H、S 及所有 floor/ceil 只需多项式位长整数算术，不引入数值迭代或新调度求解。

作者 v3 proof 与上述独立推导逐项一致。既有 v2 的 η=0、正 η 严格整数界、分组 s 界及 W=0 修复均保留。

**冻结判断：v3 全部结论通过；后续 canonical 组合审查另行记录。**
