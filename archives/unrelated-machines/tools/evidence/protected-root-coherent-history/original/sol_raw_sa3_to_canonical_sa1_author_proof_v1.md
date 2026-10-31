# 作者 Proof：raw degree-four S3 的 canonical plain-SA1 同点提取

作者：`/root/sol_nsw_independent_attack`，2026-10-18。对应冻结 Exact `sol_raw_sa3_to_canonical_sa1_exact_v1.md`，SHA `9c2a180330eed2a9b5f5b35b07eb76e2b33ed7ff853bba7376cc06e060595b71`。本文是作者证明，不是独立审查。Root 先实际全文读过 Exact；新 reviewer 只获 Exact 重构并冻结前，不应释放本文。

## 1. 记号与度数约定

保留 Exact 的全部 finite endpoint variables。每个 state s 有原 selector endpoint a_s；每个 listed incidence e∈s 有原 private endpoint D_e 和 unit-resource endpoint E_e。原 job identity 是 `D_e+E_e=1`，不是先删掉一个 job 或强迫 inactive export 为零。阈值 `1≤T<2`，`epsilon=2−T`。

`B` 始终表示至多若干个 **raw** literals 的乘积；raw literal 是原变量 x 或 1−x。允许重复或互补出现。对等式使用 S3 中完整 monomial multiplier identities，并按线性性扩展到同次数任意多项式。所有本证明的总次数都≤4。

Canonical primitives 是 `A_s=a_s`、`Z_e=a_s E_e`。Canonical degree≤2 polynomial 经 substitution 仍 degree≤4，所以 `F(f)=L(f(a,aE))` 定义良好且是同一个共同 functional 的逐字 pullback，没有改点。

## 2. 两个有限次数的正性工具

**Raw cylinder 正性。** 对每个 raw literal product B，若长度≤4，则 `L(B)≥0`。空乘积由 L1=1；非空时取一个 literal 作为原 box row，其余≤3 literals 作为该 row 的 S3 multiplier。因此不需要另给任意 quartic PSD 或全局实际 law。

**Canonical multiplier 分解。** 对每个 canonical primitive V，`1,V,1−V` 的 pullback 都是至多两个、系数为正的 raw cylinders 之和，每个 cylinder 长度≤2：

\[
\begin{array}{c|c|c}
V&V\text{ 的 pullback}&1-V\text{ 的 pullback}\\\hline
A_t&a_t&1-a_t\\
Z_f=a_tE_f&a_tE_f&(1-a_t)+a_t(1-E_f).
\end{array}
\]

以后以 W 表示 `1,V,1−V` 中任一个及其该正展开。每个 W-term 长度≤2，因此乘两个额外 raw literals 的 L 非负；乘一个 raw linear row h 和一个额外 raw literal，则 h 的 multiplier 长度≤3，正是 S3 所提供。

## 3. Canonical normalization、Boolean 与 group equalities

F1=L1=1。对 A_s，Boolean 约束直接来自原 Boolean identity。对 Z_e，明确写为

\[
(a_sE_e)^2-a_sE_e
=(a_s^2-a_s)E_e^2+a_s(E_e^2-E_e).
\]

第一项的 Boolean multiplier 为 `E_e²`，degree 2；第二项 multiplier 为 `a_s`，degree 1，均允许。因此 `F(Z_e²−Z_e)=0`。

Group equality `Σ_s A_s−1` 就是该组原 selector job 的 exact one-hot。乘任何 canonical W 后，W pullback degree≤2，原 one-hot 乘 polynomial degree≤2（事实上≤2<3）合法，故 F 的全部所需 group equality lifts 成立。若另将 canonical 同组 distinct selector pair 排除显式列入，可用 one-hot 乘 A_t、各 A_sA_t cylinder 非负和 Boolean 性逐项推出零。

这一步覆盖全部 indexed states，包括重复 indexed states；没有把一个 group 的不同原 selector endpoints 混成同一变量。

## 4. Canonical boxes 和 gates

每个 `A_s` 或 `1−A_s` 乘 W 后，每个展开项为长度≤3 raw cylinder，故非负。每个 `Z_e=a_sE_e` 乘 W 后，每项长度≤4 raw cylinder，故非负。

`1−Z_e=(1−a_s)+a_s(1−E_e)`，其乘 W 的展开也只有长度≤4 cylinders。Gate `A_s−Z_e=a_s(1−E_e)` 同理。因此 `A≥0,1−A≥0,Z≥0,1−Z≥0,A−Z≥0` 以及它们乘全部 primitive/complement 的 plain-SA1 rows 全部成立。

零系数 incidence 没被删掉；同一个 product formula 和 gate/boxes 对它仍成立。Coefficient 是否为零在本步没有用途。

## 5. Canonical unit-resource capacity

固定任一原 resource u，全部原 incidence heads 均计入，包括 zero-private-time jobs。定义 source 的显式 **cap1** row

\[
r_u=1-\sum_{e:u(e)=u}E_e.
\]

逐项代数恒等式为

\[
1-\sum_{e:u(e)=u}a_{s(e)}E_e
=r_u+\sum_{e:u(e)=u}(1-a_{s(e)})E_e.
\]

乘 canonical W 并取 L。第一项把 W 按 §2 展开，正是原 `r_u≥0` row 乘长度≤2 的 raw cylinders，S3 保证非负。每个和式项是两个 raw literals 乘长度≤2 的 W-term，故为长度≤4 cylinder，其 L 由 §2 非负。总和非负。

这里确实使用 `1−ΣE`，不能将 source 的 unit-resource physical slack `T−ΣE` 免费代替它；后者独自只给一个多余的 T−1。S3 特别列出 cap1 正是付清这一义务。

当 u unused，和式为空，等式与 lifts 仍成立。不同原资源分别处理，不合并 tags。

## 6. Canonical quality：从原 private raw row 付清三 literal 条件

固定 indexed state s。原 private root 的实际 raw load 含 selector endpoint 及其全部 incidence private endpoints：

\[
\mathrm{load}_s=a_s+\sum_{e\in s}p_eD_e.
\]

令原物理 slack `h_s=T−load_s`。用每原 incidence 的 job one-hot、以及 normalized `Σ_{e∈s}p_e=1`，在所有需要的矩上可替换成

\[
h_s=(T-1)-a_s+\sum_{e\in s}p_eE_e.
\]

这仅是 one-hot 等式的合法线性组合，未要求 inactive exports canonical。乘 `a_s` 并用原 Boolean identity，得到 canonical quality polynomial

\[
a_sh_s\equiv (T-2)a_s+\sum_{e\in s}p_ea_sE_e
=\sum_{e\in s}p_eZ_e-\epsilon A_s.
\tag{Q}
\]

精确次数核对：为求 (Q) 乘任一 W 的 L，private-end 替换所需 job identity 的 multiplier 是 `a_s W`，degree≤3；Boolean `a_s²−a_s` 的 multiplier 为 W，degree≤2。故所有差值在 degree 4 内由 S3 等式消去。

于是

\[
F\!\left(\left[\sum_{e\in s}p_eZ_e-\epsilon A_s\right]W\right)
=L(h_s a_s W)\ge0.
\]

最后一个非负性中，W 正展开的每项长度≤2，再乘 a_s 总 raw literal 长度≤3；这正是原 physical `h_s≥0` 的 S3 lifts。包括 W 为任意 **其他** group/state 的 claim 或 complement，仍使用同一共同 L 和全原行，未暗中另选 conditional 点。

零 p_e 在 normalized equality 中保其系数零，不影响身份；原 zero job 的 private/resource endpoints 与一切 identities 仍在完整证书中。T=1 即 epsilon=1 时同一计算有效，没有除 epsilon 或概率。

§3–6 覆盖 R_epsilon(Q) 中所有行及其 primitive/complement lifts，声称 B 得证。

## 7. 必要性与可选 PSD

对任意执行全部 ordinary jobs、makespan≤T 的实际 schedule，所有 finite-endpoint assignments 为 Boolean，job one-hot exact；原 boxes、每机 raw physical slack 均非负。每 resource 的全部 eligible jobs 都是 unit，T<2 迫最多一 job，故 cap1 row 也非负，即使该 job 的 private 系数为零。

每 raw cylinder 在真实 assignment 上为 0 或 1，所以每 linear row 乘任意≤3 literals 仍非负。其 Dirac moments 因而满足 S3 全部约束。这证明声称 A，以及 S3 infeasible 的 threshold-T soundFAIL。未证明任何反向实际可行性或 all-groups rounding。

若同一个 raw L 另有 M2 PSD，对任意 canonical affine q，pullback `q(a,aE)` 的 physical degree≤2，故

\[
F(q^2)=L(q(a,aE)^2)\ge0.
\]

即声称 C 的 canonical M1 PSD。它不从原 PSD 额外提供任何本证明使用的 literal lifts；那些 lifts 已由 S3 显式支付。也不声称 exact SDP finder 或任意实 PSD feasible 自动有 rational certificate。

## 8. 有限 LP、位长与确定性提取

可使用全部 total-degree≤4 moment variables，数量 `binom(N+4,4)=O((N+1)^4)`；或先 Boolean reduction 到 square-free moments，并保一致的等式表示。原 Boolean/job equalities 的 multipliers 分别≤2、≤3，个数为固定多项式。Raw rows 数是 `2N + #machines + #resources`，每 row 的 ≤3-literal multipliers 数为 `O((N+1)^3)`。

每个 literal product 最多展开 8 项，每 source row 至多线性多个 raw terms。所有 rational coefficients 来自输入 p、T 与多项式大小的整数运算，bitlength 多项式。全部构成一个显式 rational LP，不含 unknown CONFIG/SDP oracle。

还可直接控制可行点位长。每个 square-free raw monomial M、degree≤4 由 box lifts 给 `0≤L(M)≤1`：非负用一个 box literal 乘其余≤3；上界用 `(1−x)M'` 逐次比较 `L(xM')≤L(M')`，归至 L1=1。重复幂由 Boolean identities 消去。因此 reduced feasible polytope 有界。若非空，可取一个 vertex；清分母后活跃有理线性系统的整数系数 bitlength 多项式，Cramer/Hadamard 给该 vertex 的 rational bitlength 多项式。普通 rational LP 方法可找可行点或证明不可行；这只是数学算法规格，本文没有实现软件。

给定一份 complete rational L，每 canonical degree≤2 monomial 直接替换到 raw degree≤4 表的固定少量条目，或作固定次数 polynomial expansion；bitlength 与总次数均多项式。All zero/unused/indexed objects 只增加输入中的相应行列数量，不造成任何分母/概率倒数循环。

S3 本身没有要求 M2 或 CONFIG，故不应宣称它在全部约束上包含 raw K2。准确说法是：在 raw K2 之外显式加入本 S3 literal-row family 足以付清该 product interface；只使用 S3 也已足以输出 plain R，若再保同一个 raw M2 则输出 R+M1。不能反向把 raw K2 称为已含 S3。

## 9. 范围

本证明是具体 raw S3→canonical plain-SA1 的 **每给定点** repair 接口；没有 general UM constant approximation、actual-gap bound、全局真实 law、全 groups rounding 或新的 SDP 可计算性结论。算法为数学规格，软件/checker/运行均无。没有以 14m13j 反例或任何旧弱证书代替本页推导。全球新颖性未认证；一般 UM 主目标仍 OPEN。
