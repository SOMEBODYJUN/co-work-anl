# Tagged affine LINE：wide rectangles 的 marked/unmarked 联合实际 escape

ID：UM-TAGGED-AFFINE-LINE-WIDE-RECTANGLE-JOINT-ESCAPE-v2。

作者 rainbow_gap_source，2026-10-18。仅 scratch。此为 statement-only Exact，作者 Proof 另存、仅交 root hold。v1 双合同 Exact 已先冻结（SHA256 `379ca688ef9ca69a660549d5f82d176d981adfbdd5cf78a76dd3ee82c6836ef5`）；v2 用一个 marked/unmarked 合同统一并加强，保留 v1 原字节，不把中间来源另作资产。作者此前未向 rank、general、bicriteria 或其它独立 reviewer 发送本合同的证明或策略；root 已读消息中的策略，不具 blind 身份。

## 1. 完整显式几何域

给定素数 R≥2，在 F_R 上运算。有限变量集 X 可含 unused variables；非空 group 集 G，每个 group g 有非空 distinct-variable 集 X_g⊆X 及非空显式 indexed-state 菜单 S_g。记

q=max_g |X_g|≥1，
d_x=|{g:x∈X_g}|，
D=max_x d_x≥1，
M=max_g Σ_{x∈X_g}(d_x−1)。

因此 D≤R，0≤M≤q(D−1)。每个 incidence (g,x) 给固定 intercept j_x(g)∈F_R，同一变量不同 groups 的 intercept 互异。这些 intercept 是输入；结论对所有合法固定编号成立，算法不能修改它们。

每变量资源为完整 tagged plane U_x={x}×F_R²，变量块互异。state s∈S_g 给各 x∈X_g slope label a_{g,s}(x)∈F_R，完整资源集为

T_{g,s}=⊔_{x∈X_g}{(x,z,a_{g,s}(x)z+j_x(g)):z∈F_R}。

每个完整 state-resource incidence 显式给非负有理 private 权 p_{g,s,u}，且 Σ_{u∈T_{g,s}}p_{g,s,u}=1。权可依赖整个 indexed state、变量、intercept、点和全部输入。零权 incidences 全部保留；不要求 uniform-within-line 或权与编号无关。

## 2. 显式 rectangle 接口与 marked 输入

每 incidence (g,x) 给显式非空 slope 集 A_{g,x}⊆F_R，满足

∏_{x∈X_g}A_{g,x} ⊆ {(a_{g,s}(x))_{x∈X_g}:s∈S_g}。

记 L=min_{g,x∈X_g}|A_{g,x}|，故1≤L≤R。菜单可在 rectangle 外有其它 states，且可有多个相同 label vector、不同权的 indexed states；containment 只要求每个 rectangle vector 至少出现一次。不要求任何 state 分布、均匀标签边际或 pairwise independence。

再给有理数 β≥0、二进制整数 b≥0，以及每个 state-variable incidence 的显式 marked point 集 E_{g,s,x}，满足：

- E_{g,s,x} 是该 state 在变量 x 上完整 line 的子集，|E_{g,s,x}|≤b；
- 每个不在 E_{g,s,x} 中的 line cell，其 private 权≤β。

marked 可含0权点；全部集合可依赖完整 state 与编号，不要求先固定 selected states。它们是已给定或可由显式权表计算出的集合；任何处理只扫描实际列表，不按巨大 b、1/β 或有理分母展开。

全部资源 planes、state label tables、完整 line 权表和 marked 列表已显式给出或实际展开。总位多项式以此为准，不是 compact CSP、二进制 R 和权 oracle 的 poly(log R) 声称。

## 3. Partial allocation、完整 ordinary P 与主合同

partial allocation 为每组选择一 indexed state s(g)，领取 B_g⊆T_{g,s(g)}，跨组 B_g 互异；质量为其 p 权和。V 为最大最小质量，V∈[0,1]。

完整 ordinary UM 实例 P：每个 indexed state 各一台不同 private root，每个 tagged resource 各一台 resource machine；每 group 一枚 selector，在其全部 state roots 用时1；每枚 state-resource incidence 是不同 job，在自己的 private root 用时 p_{g,s,u}、在对应 resource machine 用时1，其余资格∞。所有 states、selector、incidence jobs（含 private 权0）必须实际调度；没有预载、额外模式或虚拟任务。

若

L>b(D−1)，

则存在确定性总位多项式算法输出 states s(g) 及 partial allocation B_g，使

E_{g,s(g),x}⊆B_g 对所有 g,x，

min_g Σ_{u∈B_g}p_{g,s(g),u} ≥ v:=max{0,1−Mβ}。

还可要求 B_g 包含 T_{g,s(g)} 中不属于任何其它 selected state 完整资源集的全部点。若某点同时是一个 selected state 的 marked 点与另一个 selected state 的 unmarked 点，则只由其 marked owner 领取；全部 selected marked sets 互异。没有声称 selected states 的完整几何 supports 互不相交。

算法同时输出包含全部原 jobs 的完整实际 schedule，满足

C_max≤2−v。

主合同覆盖 v=0、β=0、b=0 及 M=0 端点。它量化所有合法固定 intercepts 与全部输入 state-dependent 权/marked 选择，不是对期望、局部 CONFIG/FSLP 或任意预选 state tuple 的断言。

## 4. 两个直接应用及 D=1

**Sparse-positive unit escape。** 若每个 state-variable incidence 至多有 b 个正权点，取 marked 为全部正权点、β=0。在 L>b(D−1) 下，V=1，并可输出全部原 jobs 的实际 C_max=1 schedule，因此 OPT(P)=1。b 是每 incidence 正点预算，不是变量 degree D。Probe 可依赖完整 state、intercept 和其它输入。

**Arbitrary-weight half escape。** 不加 sparse 假设。若 D>1 且

L>2q(D−1)²，

则对任意上述 norm1 state 权，存在确定性总位多项式 partial allocation 达每组质量≥1/2，并有完整实际 C_max≤3/2 schedule。可把 β=1/(2q(D−1))、marked 为权严格大于 β 的点、b=floor(1/β) 作为主合同的显式实例；b 仅用于界，不创建 b 或1/β个虚拟对象。

**D=1 / M=0。** 任意 state choices 的不同 groups 的资源块分离，不需阈值除法或 probe 界即可全领取正权资源；V=1、OPT(P)=1。unused variables 的资源可空置。groups、变量集及 menus 非空，保证 minquality 与归一化有定义。

## 5. 全部 jobs、查表与位复杂度

0权 incidence 仍是实际任务。全部未选 states 的 jobs 均在输出中被实际分配；没有预先删除它们或将其外送当作免费。Partial allocation 可忽略零质量资源，不等于删除实际 jobs。

Rectangle containment 可在总位多项式内核查：从显式菜单统计落在 rectangle 内的 distinct label vectors 数，与二进制整数 ∏_x|A_{g,x}| 比较。不必枚举比输入更大的 Cartesian product。给定 rectangle vector，可在显式菜单中查出一个同 vector 的 indexed state；不默认其权由 label vector 唯一决定，也不调用额外 oracle。

阈值比较、Mβ、field arithmetic、选态和完整实际 assignment 均使用精确二进制计算并仅扫描显式对象。对 giant binary b 或极小正 β，不按其数值创建列表。β=0不计算1/β；M=0不进行阈值除法。若输出 sparse finite-option 表，每枚 incidence 恰两有限端（private 为0亦照列）；dense P 的机器数与 job 数乘积仍是上述显式展开输入的多项式。

## 6. 源应用边界

若某份 source 的 tables、实际提供的 rectangles 和参数满足本域，合同保留该 source tables 与固定编号并直接给上述 actual escape；不要求 source 为 YES。同域内任何 NO 输入也受该实际上界约束。

不声称所有 LST/Chan hard images 有 wide Cartesian rectangles，不声称 R-degree-bounded hard family 满足上述 label-slack 不等式。Compiler 可选不满足条件的 R、D、q、b 或无 wide rectangles 的 code-coset tables；不能从可自行扩张一份 source 的 alphabet 推断排除一切 sparse 编译。真实 source perfect-completeness、PI lifting、困难性和规模仍需另行独立核查，不是本纯几何定理的外部前提。

这不是一般 tagged-line、SC 或 UM 的常数近似结论，也不是新 hardness。它仅给 wide-rectangle/label-slack 子域的联合实际 escape；均匀边际或预期碰撞本身没有被当作 minquality 保证。
