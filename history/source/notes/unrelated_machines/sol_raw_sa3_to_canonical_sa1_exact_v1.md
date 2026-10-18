# Exact-only：完整 raw degree-four SA lifts 到 canonical plain-SA1

作者：`/root/sol_nsw_independent_attack`，2026-10-18。此文件只有合同与声称，不含作者证明、LDL、程序或运行。Root 已通过对话获知方向与几项代数式；后续重构应披露这些背景，不称全方向盲审。

## 1. 输入与原变量

输入为完整显式 normalized-flat 菜单 Q：非空有限 groups，每组非空有限 indexed states，每个列出的 incidence e=(g,s,u) 有非负二进制有理系数 p_e，每 state 的列出系数总和恰一。所有 listed incidences、显式零 incidences、未选 states、重复 indexed states 及 unused resources 保留。其 ordinary P(Q) 每 state 有独立 private root；每 group 一枚 unit selector 可去该组全部 indexed roots；每 listed incidence 一枚原 job，可去其 private root（时间 p_e）或原 resource u（时间一），其他单元无穷。

对每原 job j 的每个 finite endpoint i 保留独立 raw assignment variable x_{j,i}；总数 N。记 selector 在 state s root 的原端指标为 a_s，incidence e 的 unit resource 端为 E_e。Incidence private 端仍存在，是另一原变量；不先删除或 canonicalize。原 raw 合同不要求 inactive jobs 留 home，也不要求 E_e≤a_s。

阈值为任意二进制有理 1≤T<2，记 epsilon=2−T，故 0<epsilon≤1。

## 2. 共同 raw degree-four LP 合同 S3(P,T)

一个证书为共同线性 functional L，定义在全部原有限端变量的 degree≤4 多项式上，以完整有限 rational moment table 给出，L(1)=1。要求下列等式，对所有相应 monomial multipliers 成立：

1. `L((x²−x)m)=0`，每原变量 x、deg(m)≤2。
2. `L((Σ_{i finite for j} x_{j,i}−1)m)=0`，每原 job j、deg(m)≤3。

Raw literals 是每个原变量 x 及其补 1−x。对以下 **每一条原 affine row h≥0**，以及每个至多三个 raw literals 的乘积 B（包括空乘积 1），共同要求 `L(h B)≥0`：

- 所有原变量的 boxes：`x≥0`、`1−x≥0`。
- 每台实际机器的 raw physical slack：`T−Σ_j p_{i,j}x_{j,i}≥0`，只对该机器 finite endpoints 求和。
- 每个原 unit resource u 的整数有效容量：`1−Σ_{e:resource(e)=u} E_e≥0`，包括该 u 的全部原 incidence heads，亦包括 private 系数为零的原 jobs。这条是 **cap 1**，不是 `T−ΣE_e`。

若重复变量或互补 literals 出现在 B，仍按上述 degree-four 表及 Boolean identities 解释；不赋予额外全局真实 law。这个合同不要求 PSD、CONFIG lists 或其权重的矩，也不免费推断任何未知更高阶条目。

## 3. canonical 输出合同

对每原 indexed state 置 canonical primitive `A_s=a_s`；对每 listed incidence 置 canonical primitive `Z_e=a_s E_e`。定义 canonical degree≤2 functional F 为该 product substitution 的逐字 pullback：`F(f)=L(f(A,Z))`，不改 L 的任何被使用的原 entries；所需物理次数至多四。

这里 `R_epsilon(Q)` 的 plain common primitive-SA1 明确指下述完整合同。Canonical primitives 为所有 A_s、Z_e；F(1)=1，`F(V²−V)=0` 对每 primitive V；每 group 的 `Σ_s A_s=1` 及其乘每 canonical primitive 或其补的等式成立。以下 base affine rows，各自乘 `1`、任意 canonical primitive V 或其补 `1−V` 后，F 值均非负：

- `A_s≥0`、`1−A_s≥0`、`Z_e≥0`、`1−Z_e≥0`、`A_s−Z_e≥0`。
- 每原 resource u 的 `1−Σ_{e:resource(e)=u}Z_e≥0`。
- 每 indexed state s 的 quality row `Σ_{e in s}p_e Z_e−epsilon A_s≥0`。

All listed zero-incidence claims 也保留为 primitives；它们的 coefficient 为零，仍受 gate、boxes 与 resource 行约束。R 不含全局 M1 PSD，除非另行明确加上。

## 4. 精确声称、复杂度和限制

**声称 A（必要性）**：每份实际 makespan≤T 的完整 ordinary P(Q) schedule 的 Dirac moment table 都满足 S3(P,T)，包括其原 zero jobs 与 inactive exports。故 S3 不可行是实际 threshold-T 不可行的 soundFAIL；不声称反向。

**声称 B（充分提取）**：对每个满足 S3(P,T) 的共同有限有理 L，以上指定的、保持所用原矩 entries 不变的 product pullback F 满足完整 `R_epsilon(Q)` plain primitive-SA1。量词是每个给定点，不仅存在某个可能不同的 canonical 点。

**声称 C（可选 PSD）**：若同一个原 L 还满足全局 M2，即全部 raw degree≤2 多项式 p 的 `L(p²)≥0`，则同一个 F 还满足 canonical M1，即全部 canonical affine q 的 `F(q²)≥0`。此为给定证书的附加保持，不宣称存在 exact SDP finder 或任意实可行点的 rational witness。

S3 本身是 rational LP：变量数 O((N+1)^4)，line/identity 数为显式输入规模的固定多项式，所有系数 bitlength 由输入多项式控制。必要时可用普通 rational LP 算法求其有理可行点或判不可行；这里不交付软件实现。给定完整有理 S3 点，F 的全部 degree≤2 entries 可在显式输入和该点总位长的多项式时间/输出位长内直接计算，无未知 CONFIG/SDP oracle、无按概率倒数展开。

S3 是比只给物理 affine-load localizers/M2/CONFIG first-pair 的 raw K2 **另加且不同**的合同；不声称 raw K2 自动含上述 S3 rows，不改名为 native C2。所得 R 点也不是完整真实 schedule law，不给一般 UM 的 constant approximation、actual-gap 上界或全 groups rounding。此是具体同点 repair 接口的数学规格，全球新颖性未认证；一般 UM 主目标仍 OPEN。
