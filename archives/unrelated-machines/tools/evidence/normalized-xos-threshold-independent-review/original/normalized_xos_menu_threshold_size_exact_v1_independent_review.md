# 归一化显式 XOS 阈值菜单：Exact-only 独立计数审查

审查候选：`UM-NORMALIZED-XOS-THRESHOLD-MENU-SIZE-OBSTRUCTION-v1`。

日期：2026-10-18。此次只实际读取指定 Exact，没有读取作者 Proof、其它 agent 的推导或 repo 文件。以下覆盖证明独立重构。本记录只在 scratch 新建，不修改源 Exact、repo、Git 或 Work。

## 实际读取对象

`/workspace/scratch/038d9dcc4cac/normalized_xos_menu_threshold_size_exact_v1.md`

字节数：`2,992`。

实际核对 SHA256：

`f10774625ddc30e09db98088a8c4cee579da027c8ae2512f6baba3ed5203bb44`

## 结论

**PASS；未发现 fatal。** 在相同 `2t` 个资源的宇宙上，用非负、有理、总系数恰为 1 的显式 additive clauses 表示 XOS，同时使所有 t-subsets 的值恰为 1、所有至多 `d=floor(eta t)` 项的集合值至多 eta，确有

\[
K\ \ge\frac{\binom{2t}{t}}{\binom{2t-r}{t-r}}\ \ge\ 2^r,
\qquad r=d+1\in\{1,\ldots,t\}.
\]

这里没有声称比值本身在所有参数下达到，没有把资源数上的指数写成输入 bitlength 上的线性指数，也没有把显式逐玩家、同宇宙、全子集阈值保真界面扩大成所有 normalization 或所有归约的不可能性。

## 独立证明

### 1. 一个 unit t-set 必含某个 clause 的全部正 support

对每个 clause s 定义严格正 support

\[
A_s=\{u:w_{s,u}>0\},\qquad m_s=|A_s|.
\]

因为系数非负且总和等于 1，每个 clause 在任何子集上的值都至多 1。若一个 t-set T 满足 `f(T)=1`，则有限个 clauses 的最大值由某个 s 取得，其在 T 上的系数和等于 1。因此 T 外的非负系数总和为 0，逐个系数为 0，得到 `A_s subseteq T`。

反之，若 `A_s subseteq T`，该 clause 在 T 上的值就是 1，于是 `f(T)=1`。所以待覆盖的 unit t-sets，恰是至少包含某个 clause 正 support 的那些 t-sets。有限 K、非负性和总量恰为 1 均已在此使用。

### 2. low 条件强制 support 至少 r 项

归一化保证每个 support 非空。若某 clause 的 `m_s<=d`，则令 `B=A_s`。它是 low 条件管辖的集合，却有 `f(B)>=sum_{u in A_s}w_{s,u}=1>eta`，矛盾。因此

\[
m_s\ge d+1=r.
\]

当 `d=0` 时这一结论仍成立：归一化已直接保证 `m_s>=1=r`，不需要捏造一个非空、大小至多零的 low 集合。

### 3. 每个 clause 的 unit-set 覆盖数

如果 `m_s>t`，没有 t-set 能包含其 support，该 clause 覆盖零个 unit t-sets。如果 `r<=m_s<=t`，恰有

\[
\binom{2t-m_s}{t-m_s}
\]

个 t-sets 包含 `A_s`。这至多是

\[
B_r:=\binom{2t-r}{t-r}.
\]

一种不依赖公式单调性记忆的论证是：先取 `A_s` 的任意 r 元子集，包含整个 `A_s` 的 t-sets 只是包含该 r 元子集的 t-sets 的子族。

全部 `binom(2t,t)` 个 t-sets 都要被至少一个 clause 覆盖。对覆盖族取并集上界即可得

\[
\binom{2t}{t}\le\sum_{s=1}^K
|\{T:|T|=t,A_s\subseteq T\}|\le K B_r.
\]

支持集相同、indexed clauses 重复或覆盖彼此重叠，只会使这条并集上界更松，不会破坏下界。零系数已经正确地从严格正 support 中排除。

### 4. 组合数比至少 2^r

由于 `1<=r<=t`，下面每个分母均为正，且

\[
\frac{\binom{2t}{t}}{\binom{2t-r}{t-r}}
=\prod_{j=0}^{r-1}\frac{2t-j}{t-j}
\ge\prod_{j=0}^{r-1}2=2^r.
\]

逐因子不等式等价于 `2t-j>=2(t-j)`，即 `j>=0`。j=0 时等号成立；如果 r>=2，至少 j=1 的因子严格大于 2。无需 Stirling 近似、概率独立性或对所有 T 的显式枚举。

## r 与 t 的端点、非空性和额外零 clauses

- `t=1` 时必有 `d=0,r=1`。两个 singleton 都要达到 unit，两个 delta clauses 即可，界给 `K>=2`，正确且可达。
- `d=0,r=1` 时 low 条件只管空集合，其值确为零。声明的比值为 2，虽可能很松，但仍正确。事实上这时最小 K 是 `t+1`：取 t+1 个不同资源的 delta clauses 可命中每个 t-set；反过来若 K<=t，每个非空 support 中任取一点，取一个避开这些点的 t-set 即得到未覆盖集合。该更精确边界不与 Exact 的非锐性声明冲突。
- `r=t` 时覆盖分母是 `binom(t,0)=1`，所以每个能覆盖 unit t-set 的 support 必恰为该 t-set，`K>=binom(2t,t)`。没有负参数组合数或零分母。
- 整个条件族不是 vacuous。对每个 t-set T 列一个在 T 上均匀取 `1/t`、T 外为零的 clause。共有 `binom(2t,t)` 个，每个总量为 1；所有 unit t-sets 被覆盖，任意至多 d 元 B 的每个 clause 值至多 `d/t<=eta`。所有系数均为非负有理数。
- 一个额外全零 clause 不会提高非负 XOS 值；删掉它不影响 f，且上述 K 下界已由非零归一化 clauses 承担。不能通过给零 clause 计数来减少必要的有效 clauses 数。

## bitlength 和显式输出规模

固定任意正有理常数 eta 后，`r=floor(eta t)+1>eta t`，故必要状态数至少 `2^{eta t}`。原加性玩家的显式表示是 `2t` 个资源及每资源价值 `1/t`，资源编号和有理数各用 `O(log(t+1))` 位；总源长度为 `O(t log(t+1))`。因此对任何固定多项式次数 c，必要 K 最终大于源长度的 c 次方。仅列出 K 个 indexed clauses 就需要至少 Omega(K) 输出量；dense 列系数更大，允许省略零系数也不能消掉 K 个有效 clauses。

这严格给出显式输出超多项式障碍。应把“指数”理解为资源数 N=2t 上的 `2^{Omega(N)}`；此论证不直接宣称 `2^{Omega(L)}`，其中 L 是逐项编码后的源 bitlength。全体 t-sets 和 small sets 是数学保真量词，不是源输入中必须逐个列出的指数表。

固定 eta 与变化 eta 的量词不能交换。如果 eta 随 t 变小，例如 `eta=1/(2t)`，则 d=0，而上面的 t+1 个 delta clauses 已给多项式规模的合法菜单。因此原 Exact 不声称 eta 趋零时仍存在统一指数常数，是实质正确的范围限制。

计算 `d=floor(eta t)`、组合数或它们的有理比并非下界证明所要求的转换算法。若作精确核验，这些整数的编码长度为 O(t) 加上参数编码，标准整数算术为多项式；不能把组合数的数值大小误认为其二进制存储长度。原始显式菜单条目的系数长度可以任意大，但更高数值精度不会改变 positive-support 覆盖论证。

## 必须保留的范围限制

该结论否定的是：一个普适逐玩家接口，在不改变这 `2t` 个资源、无辅助玩家/一致性结构的条件下，将这一原加性玩家转换成**显式、非负、逐 clause 总量恰为 1**的 XOS，同时保存所有 t-subsets 的 exact-unit YES 和所有 small subsets 的 low 阈值，并要求输出规模对上述源输入为多项式。

它不否定全局归约、辅助资源/玩家、仅对可达分配保真、损失部分 unit 值、隐式且另证可计算的表示、特定源直接构造等其它接口。归一化限制尤其不能删除：原来的单个 additive clause `w_u=1/t` 总量为 2，已用 K=1 同时满足所有所述 unit/low 阈值。该例不在 norm-1 域，正好说明结论不能扩大为所有非归一化菜单的下界。

这不是 normalized unit/tiny gap hardness 源，不是对普通 Santa Claus 或 UM 近似的下界，也不把任何 degree reduction 自动升级成这里的逐玩家保真接口。沒有读入作者 Proof 或其它 agent 的新推导。

## Reviewer-derived optional strengthening，非本次 PASS 所必需

这是此次独立重构额外得到的简单支持集观察，不改变被审查 Exact，也不在本记录中升级为另一个已独立审查的候选。

令

\[
r_*:=\max\{1,\lceil d/\eta\rceil\}.
\]

当 d>0，取某 clause 的 d 个最大正权系数。其和至少 `d/m_s`，而 low 条件使该和至多 eta，故 `m_s>=ceil(d/eta)`；m_s<d 已被前面的矛盾排除。d=0 时用非空 support。因此 `r_*<=m_s`，且 `r_*<=t`，同一计数证明给更强的候选下界

\[
K\ge\frac{\binom{2t}{t}}{\binom{2t-r_*}{t-r_*}}.
\]

对固定 eta，`t-r_*<=ceil(1/eta)-1` 为常数，所以该可选强化甚至给 `4^t/poly_eta(t)` 量级下界。其证明仍只在相同 restricted interface 内，不能扩大 scope。若要提升该强化为正式新 Exact，仍应单独冻结并安排相应审查。

## 审查状态

有限整数核验仅为辅助；PASS 依据是上面的独立覆盖证明。没有实现、外审、新颖性或普适归约不可能性认证。源 Exact 原字节不变。
