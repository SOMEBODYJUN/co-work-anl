# 私有双树配置阈值的正部多面体与严格单位阈值的五三界

读取目的：检查以严格负载 1 编译源标签的单位读出路线，是否真的能产生近 2 的困难性。这里给出这个完整结构类的配置 LP 精确描述、(1,5/3) 多项式承诺间隙算法，以及经典两树族的精确配置阈值。它们不是一般 UM 算法或新困难性；尤其不能把严格阈值 1 的结论搬到 1+1/k。

## 1. 共同对象与证据层级

沿用[单位读出双树](unit_readout_pruned_forest_boundary.md)的全部原 P 合同：每变量两棵私有满 k 叉深 h 树，k,h≥1；每变量一枚 selector，只能在两根耗时 1；每内部边任务在父端耗时 1/k、子端耗时 1；每叶任务在父端耗时 1/k，或在所属 clause 的任一 unit 机器耗时 1。不同 clause 的机器互异，容量 A_c 是非负整数；没有其他任务、pins 或资格。所有叶地址和任务显式列出，A_c 可用二进制，外机可截到 min(A_c,d_c)，其余原机器负载为 0。空变量立即返回空分配；需要至少一机时添空闲机。

Objects / Domain / Quantifiers：以下各 Claim 对每个这样的有限显式实例成立，不限制树高、clause 密度或接线。配置采用精确覆盖、每机概率和 1 的通常定义，包含空配置；向下封闭保证与至少覆盖版本等价。非空实例的实际 OPT 与配置阈值均≥1。

Status：限定范围自足证明；独立重构、冻结全文攻击及实现状态见[审查](../../reviews/unrelated_machines/unit_readout_configuration_threshold_review.md)。外审、新颖性和独立成文价值未认证。标准 LP、有序槽、uniform-matroid 分解不是本页发明；有限审计不代替一般证明。

共同 Evidence：第2—5节一般证明、审查页的先陈述重构及全文攻击、[冻结有限输出](../../../evidence/runs/unrelated_machines/unit_readout_configuration_threshold_audit.json)。共同 Counterevidence/Objections：没有尚成立的内部 fatal；经典近单位阈值 gap 明确限制第4节，代码未实现一般 LP，有限输出不证明一般定理。共同 Related Files：本页、审查、§6的两个审计程序及[输入例子](../../../examples/unrelated_machines/unit_readout_configuration_threshold_examples.json)。

## 2. 每个配置阈值的精确正部多面体

**ID/version：UM-UNIT-READOUT-CONFIG-POSITIVE-PART-v1。**

Exact Statement / Assumptions：固定有理 T∈[1,2)，令 s=⌊k(T−1)⌋∈{0,…,k−1}。给每变量两个 selector 边际 y_v0,y_v1，给每个内部边或叶任务下传边际 t_e。根的 incoming 边际 q_u=y_vs，非根 q_u=t_parent。则 CONFIG(T) 可行当且仅当以下多项式规模系统可行：

\[
y_{v0}+y_{v1}=1,\quad y_{vs}\ge0,\quad 0\le t_e\le1,
\]
\[
\sum_{e\in\mathrm{out}(u)}(q_u-t_e)_+\le s q_u
\quad\text{对每内部机器 }u,
\qquad
\sum_{e\in\mathrm{ports}(c)}t_e\le A_c
\quad\text{对每 clause }c.\tag{P_s}
\]

Conclusion / Scope：可在总输入位长的多项式时间精确求 CONFIG 阈值；给定有理可行边际，可多项式构造每机的有理配置分解。此为该结构类的配置描述，不是配置 LP 的一般小规模描述或整数舍入保证。

**必要性。** 在一台内部机上，记 incoming 任务出现事件为 I，某个 outgoing 任务留父事件为 B_e。它们的概率分别为 q 与 1−t_e，故

\[
\Pr(I\cap B_e)\ge(q-t_e)_+.
\]

有 incoming 的配置最多再含 s 枚 small；无 incoming 时全部 k 枚 small 总负载为 1，可同时出现。因此 Σ_e Pr(I∩B_e)≤s q。每外机在 T<2 时至多一枚 unit port，得到 clause 约束。所有原 job 精确覆盖给出同一组边际，不能逐机另选互不相容的边际。

**局部充分性。** 固定一行，令 a_e=1−t_e、c_e=(q−t_e)_+。有 0≤c_e≤q、c_e≤a_e、0≤a_e−c_e≤1−q、Σc_e≤s q。

在长度 q 的概率区间上始终包含 incoming。把长度 c_e 的各段顺次连接到 [0,Σc_e)，再模 q 投到 [0,q)。每段长度≤q，不会重复选同一 job；每点至多被 s 条段覆盖，因为原串接区间长度≤s q。在端点间的每个开区间选其覆盖的 small jobs，给它区间长度的权重。每配置含 incoming 和至多 s 枚 small，边际为 c_e。q=0 时直接省略此部分，不做模 0。

在剩余长度 1−q 的区间上不含 incoming；第 e 枚 small 放在 [0,a_e−c_e)。这些嵌套阈值集合任取至多 k 枚 small，总工作量≤1。q=1 时省略这部分。两部分权重之和恰 1，各 small 的总边际恰 a_e。每行仅 O(k) 个断点，端点有理且位长多项式；可按断点扫描显式给配置，不依赖抽样。

对 clause，把各 port 的质量 t_e 串接切成 unit 长度槽，每槽对应一台不同真实外机；每机用各单任务配置及空配置。只需 ceil(Σt_e)≤min(A_c,d_c) 台。每原 job 在父端质量 1−t_e、子端/外端质量 t_e，selector 两根总质量 1，故所有列精确覆盖。各机配置无需来自一个全局 joint distribution；要求那样的分布将错误地把配置 LP 变成整数调度凸包。

**LP 与位复杂度。** 可引入 z_ue≥0、z_ue≥q_u−t_e、Σz_ue≤s q_u，得到有理线性系统。给定 lift 时使用最小 c_e 而非把任意 z 当作联合概率；存在性无需额外上界。系统规模按显式任务数多项式。调用标准确定性有理 LP 可行性算法，所得基本见证位长多项式；不假定指数配置 oracle 免费。

非空实例的配置可行性只在网格 1+s/k，s=0,…,k 处改变：内部配置的负载为 1 或 1+j/k，外机在 T<2 时单任务。T=2 时已有全父置实际调度。对 s 二分，O(log(k+1)) 次上述 LP 足够，得到精确阈值。k=1 时只须检验 T=1，否则阈值 2。空实例阈值 0，先处理，不按巨大二进制 k,h 展开不存在的树。

Dependencies：本页完整原 P、配置定义、概率交下界、串接区间构造和标准有理 LP 位复杂度；没有整数森林存在性、源 CSP 困难性或有限实验前提。

## 3. 严格单位阈值等价于整轨选择 LP

令 n_cvs 为变量 v 的 sign s 全部叶中接到 clause c 的数量。定义 **整轨选择 LP**

\[
y_{v0}+y_{v1}=1,\quad y_{vs}\ge0,\qquad
\sum_{v,s} n_{cvs}y_{vs}\le A_c\quad(\forall c).\tag{L}
\]

由上一 Claim，CONFIG(1) 可行当且仅当 (L) 可行。因为 s=0 时每个 t_e≥q_u，沿轨归纳得每叶外送边际≥对应根 y_vs，从而得到 (L)。反向给 (L)，在每一轨所有深度令 t_e=y_vs；每内部行取 incoming 单任务配置概率 y_vs、全部 k 枚 small 的配置概率 1−y_vs，外端按上节分配，即得 CONFIG(1)。

这里 **没有比该结构的 CONFIG(1) 多用信息**；它是 CONFIG 在严格单位阈值的精确消元。不能把它描述成对任意配置下界的全局强化。

## 4. 整轨 LP 的确定性完整五三调度

**ID/version：UM-UNIT-READOUT-STRICT-UNIT-GAP-v1。**

Exact Statement：本页结构类中，若 (L) 可行，则确定性总位多项式算法输出全部原 job 的合法 σ，

\[
C_{\max}(\sigma)\le
\begin{cases}
1,&k=1,\\
2-\lfloor k/2\rfloor/k\le5/3,&k\ge2.
\end{cases}
\]

k≥2 偶数时界为 3/2。算法可先求 (L)，也可接受给定精确有理见证；后一运行时间包括见证位长。非空 OPT≤1 必使 (L) 可行，故给出 **YES OPT≤1、NO OPT>5/3 的多项式承诺间隙判定**。它不是整个结构类的任意 OPT 五三近似，也未声称常数 5/3 锐。

**选择轨。** 对每变量选 y_vs≥1/2 的 sign，并把 selector 固定到它的根。令 d_c^* 为所有这些轨接到 c 的叶总数，则

\[
d_c^*\le2\sum_{v,s}n_{cvs}y_{vs}\le2A_c.\tag{1}
\]

这不限制未选轨的叶数；全局 d_c/A_c 可以任意大。未选轨全部任务父置，每台未选机负载恰 1。

**只对选轨建槽。** k≥2 取 r=⌊k/2⌋，L=k−r+1，x_0=1、x_l=(r−1+x_(l−1))/k。由 x_1=r/k≤1/2 且 r/k≤(k−r)/k，归纳 x_l≤r/k≤1/2，l≥1。每选轨深 l 的下传质量 x_l，incoming 在根质量 1、在深 l−1 机质量 x_(l−1)。该行总分数任务数

\[
x_{l-1}+k(1-x_l)=L.
\]

把 incoming 放首位切 unit 槽，再放 small 片；每选轨内部最多 L 槽，incoming 只邻首槽。外部质量为 d_c^* x_h≤A_c，串接成 unit 槽。selector、选轨全部边和叶共同列和 1；一次 Hall 匹配覆盖这些全部原任务。按原机输出，未选轨任务保持父置。

若某内部机接 incoming，至多另接 L−1=k−r 枚 small，实际负载≤1+(k−r)/k；若不接 incoming，其原 k 枚 small 总量≤1。每外 unit 至多一枚 port；所有原机、未选分支和原任务均已计入。此为[校准计数槽](unit_readout_calibrated_cardinality_slots.md)的 **active-only** 使用，不能直接对未选轨强加原 strong LP 行。

奇 k≥3 时 r/k=(k−1)/(2k)≥1/3，偶 k≥2 时 r/k=1/2，得到统一 5/3。分母位长 O(h log k)，由非空显式输入控制。

**k=1。** 每 sign 只有一条链和一个叶。把变量连到其两叶所属 clause，容量 A_c；(L) 给这个二部容量网络分数满流。整数最大流可为每变量选一个真实叶并注入 clause unit。沿所选链全部下传、其他任务父置，完整负载≤1。容量可截到实际叶数，不展开巨大 A。

**承诺间隙与否定范围。** 实际负载 1 迫使 selector 所选轨逐层全部下传，故它的 0/1 sign 本身满足 (L)。因此 LP 不可行可证 OPT>1，可行则输出≤5/3；两种输出覆盖上述 promise。除非 P=NP，该结构不能承载从 NP-hard 源到这个 **严格阈值 1** 的 (1,ρ) gap 归约，ρ>5/3。没有断言该类不存在 OPT≈2 的个别实例，或任意其他阈值也无近 2 gap。

Dependencies：完整单位读出模型、(L) 的共同可行见证、概率取大坐标、仅选轨计数槽及 Hall 匹配、k1 整数流、标准有理 LP；不需要 p 份完整 YES、固定树高、固定总密度或有限测试。

**对 one-hot 源编码的应用。** 若把每个 Label Cover 的 vertex/label 变成一个 Boolean，每个 vertex 的正文字总和至多 1、负文字总和至多其字母数减 1（左端 Q−1、右端 q−1），再加 forward `x_ua+(1−x_vπa)≤1`，以及 s 对一投影 fiber 的 reverse `x_vb+Σ_(π(a)=b)(1−x_ua)≤s`，那么左字母 Q、右字母 q、Q=sq 时，均匀边际 `Pr[x_ua=1]=1/Q`、`Pr[x_vb=1]=1/q` 满足这些源行。按整轨叶出现实现这些行的任何合法本模型实例，只要重复/平衡仍保持这份 (L) 见证，就由本 Claim 输出≤5/3；源整数标签是否一致不影响这个结论。这是给具体编译候选的精确失败机制，不引用或声称一个新 Label Cover 困难性定理。

## 5. 经典闭合两树的精确配置阈值

**ID/version：UM-UNIT-READOUT-CLOSED-TREES-EXACT-CONFIG-v1。**

Objects：单变量两棵满 k 叉深 h 树；每个深 h−1 内部节点的 k 枚叶任务共用其独有的一个 terminal，A=1。各 terminal 互异。这正是[经典间隙族](model_and_classical_barriers.md)的重新索引对象，未改原 P。

Exact Statement：任意 k,h≥1，实际 OPT=2−1/k；其精确配置阈值为

\[
T_{\rm CONF}=1+s_*/k,\qquad
s_* =\min\{s\in\{0,\ldots,k-1\}:(k-s)^h\le2k^{h-1}\}.
\]

**必要性。** 正部行给 Σ_out t_e≥(k−s)q_u。沿某轨全层求和，全部叶外送边际至少 (k−s)^h y_vs。该轨共有 k^(h−1) 个外 unit，故 (k−s)^h y_vs≤k^(h−1)。两根概率和 1，得到所列必要条件。

**充分性。** 两根各 1/2，每层令 x_l=½((k−s)/k)^l。每 row 的正部和 k(x_(l−1)−x_l)=s x_(l−1)，每 terminal 的质量 k x_h≤1 恰是所列条件。第2节给真实 CONFIG 分解。s=k−1 始终可行；整数上/下界沿既有单路径证明，k1 时也成立。

k≥3 时 s=0 永不可行，而既有 gap 族选择的 h 满足 (k−1)^h≤2k^(h−1)，所以该族 **T_CONF 精确等于 1+1/k**，不只存在该阈值的证书。因此逐例间隙恰为 (2k−1)/(k+1)=2−3/(k+1)，趋于 2。

这解释第4节没有触碰已知 gap：仅增加一枚 small 的阈值余量，就允许 incoming 与它同配置，使层边际按 (k−1)/k 衰减；足够深度后配置 LP 已可行，而整轨 LP 仍不可行。将时间整体缩放也会同时改变单位 incoming 合同，不能假装缩放后仍适用第4节。

Dependencies：正部多面体 Claim、同一原 P 的经典实际 OPT 证明；原 gap 为 Verschae–Wiese 的已知结果，本页只给上述显式结构的阈值消元与精确回算。外审及新颖性未认证。

## 6. 有限实现的精确职责

[整轨见证舍入器](../../../tests/audits/unrelated_machines/unit_readout_literal_gap.py)接受精确 (L) 见证，返回每原 job 的具体 σ 并逐机回算；它不集成一般有理 LP 求解器。[单行分解审计](../../../tests/audits/unrelated_machines/unit_readout_configuration_row_decomposition.py)用精确 Fraction 构造配置并核边际、权重及原负载。冻结输出和源码哈希由审查页绑定；全局 CONFIG LP 求解器及其全机配置输出未集成。所有有限网格、小例及经典参数回算仅是 checks，不作为上述一般结论的 derives。
