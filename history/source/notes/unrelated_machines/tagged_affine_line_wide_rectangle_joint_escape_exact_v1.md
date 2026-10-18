# Tagged affine LINE：wide rectangles 的 sparse unit 与任意权 half escape

ID：UM-TAGGED-AFFINE-LINE-WIDE-RECTANGLE-JOINT-ESCAPE-v1。

作者 rainbow_gap_source，2026-10-18。仅 scratch。此为首次冻结的 statement-only Exact；作者 Proof 另存、仅交 root hold。此前未将本合同的作者证明或策略发送给 rank、general 或其它独立 reviewer。

## 1. 完整显式几何域

给定素数 R≥2，在 F_R 上运算。有限变量集 X 可含 unused variables；非空 group 集 G，每个 group g 有非空的 distinct-variable 集 X_g⊆X 及非空显式 indexed-state 菜单 S_g。记

q=max_g |X_g|≥1，
d_x=|{g:x∈X_g}|，
D=max_x d_x≥1。

所以 D≤R。每个 incidence (g,x) 给固定 intercept j_x(g)∈F_R，同一变量的不同 groups 的 intercept 互异。这些 intercept 是输入，结论对所有合法输入编号成立，不允许算法修改它们。

每变量资源为带 x 标签的完整 plane U_x={x}×F_R²，不同变量块分离。state s∈S_g 给每个 x∈X_g 一个 slope label a_{g,s}(x)∈F_R；其完整资源集为

T_{g,s}=⊔_{x∈X_g}{(x,z,a_{g,s}(x)z+j_x(g)):z∈F_R}。

同一 state 内资源 distinct。每个完整 state-resource incidence 显式给非负有理 private 权 p_{g,s,u}，总和严格为1。权可依赖整个 indexed state、变量、intercept、点及全部输入；没有 uniform-within-line 或与编号无关的假设。零权 incidences 全部保留。

每个 group 额外给显式非空 slope 集 A_{g,x}⊆F_R（x∈X_g），满足 rectangle containment：

∏_{x∈X_g} A_{g,x} ⊆ {(a_{g,s}(x))_{x∈X_g}:s∈S_g}。

令 L=min_{g,x∈X_g}|A_{g,x}|，因此1≤L≤R。菜单可有多个 indexed states 使用相同 label vector 而不同权；containment 只要求每个 rectangle vector 至少有一个 indexed state。所有这些 states 仍保留。无需菜单正好等于 rectangle，无需给 states 的概率分布、单变量均匀边际或 pairwise independence。

全部资源 planes、state label tables 及完整 line 权表均已显式给出或实际展开。这里的“总位多项式”以此显式输入为准，不是仅给二进制 R、compact CSP 和权 oracle 的 poly(log R) 声称。

## 2. Partial allocation 与完整 ordinary P

partial allocation 每组选择一 indexed state s(g)，领取 B_g⊆T_{g,s(g)}，跨组 B_g 互异。质量为 Σ_{u∈B_g}p_{g,s(g),u}；V 为其最大最小值，V∈[0,1]。

完整 UM 实例 P：每个 indexed state 各一台不同 private root；每个 tagged resource 各一台 resource machine。每个 group 一枚 selector，在该组任意 state root 上用时1。每枚 state-resource incidence 是不同 job，在其 private root 用时 p_{g,s,u}、在该 resource machine 用时1，其余资格∞。全部 indexed states、全部 selector、全部 incidence jobs（包括 private 权0）必须实际调度；无预载、虚拟任务、外部锁定模式或免费导出。

## 3. 合同 A：sparse-positive unit escape

另给整数 b≥1，并假定对每个 state-variable incidence，其完整 line 上的正权点数至多 b；不同 states 的这些点可任意变化，且可依赖完整 state 和 intercept。若

L>b(D−1)，

则存在确定性总位多项式算法输出 partial allocation，每组质量恰1；并输出包含全部原 jobs 的实际 C_max=1 schedule。因此 V=1、OPT(P)=1。

结论对任意固定合法 intercepts 同时适用，不是“存在一种可重编号的 index”。b 是每个 incidence 的 probe/正点预算，D 是变量参加 groups 的数量；二者不可混同。该合同没有排除 compiler 自选参数后不满足上述不等式的实例。

## 4. 合同 B：任意 state 权的 half escape

此合同不加任何 sparse-positive 假设；每条 line 可在全部 R 点具有任意非负权，只要求每个 state 总质量1。若 D>1 且

L>2q(D−1)²，

则存在确定性总位多项式算法输出 partial allocation，每组质量至少1/2；并输出包含全部原 jobs 的实际 C_max≤3/2 schedule。因此 V≥1/2、OPT(P)≤3/2。

这是共同选择 states 与实际资源分配的合同；既不是先固定 states 的断言，也不是由单独的期望、CONFIG 或 FSLP 可行性推出。未声称3/2为该受限类的最佳常数或 NP-hard 近似比。

## 5. D=1、空/零与计算接口

若 D=1，不需合同 A 的 probe 预算或合同 B 的额外不等式：任意选择一 state/group 都可完整领取其全部正权资源，V=1、OPT(P)=1。unused variables 的资源可空置；groups、其变量集及 menus 保持非空以使归一化和 minquality 有定义。

0权 jobs 仍是实际任务。两个合同均保证输出全部未选 states 的实际 jobs，不把其资源外送当作免费、也不预先删除这些 jobs。Partial allocation 中忽略0质量资源与完整 actual P 中保留0权任务是不同操作。

rectangles 作为显式 sets 给定，可在总位多项式内核 containment：从显式 state table 计算落在 rectangle 中的 distinct label vectors 数，与整数 ∏_x|A_{g,x}| 比较，不必枚举一个超过输入大小的 Cartesian product。给定任意 rectangle vector，可在显式菜单中确定性查出一个同 vector 的 indexed state；无需默认权由 label vector 唯一决定，也无需额外 oracle。

所有处理仅扫描显式 groups、变量、states、line points 及有理数表，阈值运算和 field arithmetic 使用二进制精确计算；不按有理分母的数值展开。若用 sparse finite-option 表给 P，每枚 incidence 恰两个有限端（private 为0亦照列）；若给 dense matrix，机器数与 job 数的乘积仍为上述展开输入大小的多项式。

## 6. 条件源应用与明确边界

若一份 source 的 allowed tables 与实际提供的 rectangles 满足上述对象及参数条件，合同直接适用于其 tagged-line 编译，保留这些原 source tables 和固定 intercepts。它不要求 source 为 YES，因此同域内任意 NO 输入也受到该实际 schedule 上界约束。

这不声称所有 LST/Chan hard images 有 wide Cartesian rectangles，不声称原 R-degree-bounded hard family 满足 L>2q(D−1)²，也不从可自行扩大某份 source 的 alphabet 推断排除一切 sparse 编译。Compiler 可选择不满足这些参数条件的 R、D、q、b，或使用无 wide rectangle 的 code-coset tables。真实 source perfect-completeness、PI lifting、硬度及规模还需另行独立核查；不是本纯几何定理的外部前提。

本结果不是一般 SC/UM 常数近似算法，不是一般 arbitrary-weight tagged-line 的常数界，也不是任何新的 hardness。它明确给出 wide-rectangle 与 label slack 子域中的实际 escape；未把局部均匀标签或预期碰撞本身当作联合 minquality 保证。
