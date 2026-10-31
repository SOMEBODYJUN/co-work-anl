# 14-machine / 13-job raw K2 点：独立 Exact-first 重构

审查者：`/root/sol_nsw_independent_attack`。本记录在尚未读取本 candidate 的 Author Proof、LDL、代码或 run output 时冻结。新的实例和 moment specification 仅来自 parent 释放的 Exact。本审不是对所有背景全盲：此前已独立审过 raw K2 resource-path Exact、读过随后释放的 Author Proof 和 canonical §12，也研究过 primitive-SA1、资源 empty、M1/M2 与有限 slice 的 conditioning 边界。

## 1. 实际读取的唯一新输入

`/workspace/scratch/038d9dcc4cac/sol_general_repair_k2_canonical_pullback_exact_v1.md`

- 实核 SHA-256：`a79fd77dc17c87a8729bc3c4b47088a434f24db98e37f95b0ec9e01ec604323a`。
- 实核 3,594 bytes、49 行、mode `0644`。
- 真正显示并逐行读完 **1–49**，无截断。
- 未读本 candidate 任何 author proof、LDL、代码、run、其他 review，也未向作者索取推导；没有读新 literal candidates 或修改 repo/Git/Work。

以下从该 Exact 独立生成：所有机器 raw load、全局 M2 的表示分解、唯一非恒定 root 的 affine-localizer 矩阵、每机 legal CONFIG、完整真实 schedule 与 canonical 负矩。

## 2. 全部 ordinary jobs 与原端变量

四组各两 indexed states，故有 8 个不同 private roots；六资源 `u,v,r,w_u,w_v,w_r` 互异，共 **14 machines**。四枚 selector 各两 finite endpoints。Incidences 是 M/0 两枚、M/1 一枚、每 helper 两枚，共九枚，各两 finite endpoints。总数 **13 jobs、26 finite endpoints**。没有隐含零 incidence jobs；“未列系数零”不增添未列 job。

原 selectors 的两端均为 unit；每 incidence private 端系数是列出的 1/2 或 1，resource 端为 unit，其他无穷。没有采用 canonical `export≤activation` 作为本物理实例侧条件。

记 `a=b_1,b=b_2,c=b_3`，位均形式 Boolean。原 selector/incidence-head 的 Exact 替换都只是 `a,b,c` 的单个 literal；同 job 另一端是其补。因此所有原 job one-hot 是仿射恒等式，在任意 degree≤3 multiplier 后仍零；全部 Boolean identities 乘至 degree 4 由三位 Boolean 商直接成立。

三位 square-free moments 为

\[
\ell(1)=1,\qquad p=\ell(a)=\ell(b)=\ell(c)=\frac3{10},
\quad q=\ell(ab)=\ell(ac)=\ell(bc)=\frac3{80},
\quad r=\ell(abc)=-\frac1{160}.
\]

原变量的 degree≤4 monomials 先按所有 finite-endpoint 替换，再 Boolean reduction；所得 L 是一份共同完整 rational functional。不是逐机器另取互不一致的矩。

## 3. 全局 M2：独立表示分解为正定小块

任意原 degree≤2 多项式代换后，均在

\[
\mathcal B=(1,a,b,c,ab,ac,bc)
\]

的七维空间。只需证明此 basis 的 bit M2 正定。它对三位置换不变；以下直接正交分解，不使用作者 LDL。

令 `S=a+b+c`、`U=ab+ac+bc`。对称子空间 basis `(1,S,U)` 的 Gram 为

\[
\frac1{160}
\begin{pmatrix}
160&144&18\\144&180&33\\18&33&12
\end{pmatrix}.
\]

整数矩阵的 leading principal minors 依次是 `160,8064,35280`，全正。

另将 pair basis 按遗漏位排序，即 `(bc,ac,ab)`。对 `x,y∈R³` 且 `Σx_i=Σy_i=0`，多项式 `Σx_i b_i+Σy_i∏_{j≠i}b_j` 的 Gram form 为

\[
(p-q)\|x\|^2+2(r-q)\langle x,y\rangle+(q-r)\|y\|^2
=\frac1{160}\bigl(42\|x\|^2-14\langle x,y\rangle+7\|y\|^2\bigr).
\]

它是二维 standard representation 上的两份相同 positive block；对应 `[[42,−7],[−7,7]]` 的 leading minors 为 `42,245`。该四维部分与 `(1,S,U)` 在本 Gram 下正交。两部分合计七维，因此 bit M2 正定。直接七维 determinant 为 `117649/1342177280000>0`，也核对一致。

任意物理全局 quadratic 都 pull back 到这个空间，所以完整 26-endpoint M2 是其 PSD pullback。这里仅要求 quadratic squares 非负；`abc` 的负期望没有被当成 degree≤2 square，也没有额外假设全局 triple/quartic literal 非负。

## 4. 逐机 raw loads 与所有全局 affine localizers

按原 finite endpoints 逐项相加，可得：

| 物理机 | 实际 job load 的仿射代换 |
|---|---|
| M/0 private root | `1/2+a−b/2+c/2` |
| 其余七个 private roots | `1` |
| 资源 u | `b+(1−b)=1` |
| 资源 v | `(1−c)+c=1` |
| 资源 r | `(1−a)+a=1` |
| 资源 w_u | `b` |
| 资源 w_v | `1−c` |
| 资源 w_r | `1−a` |

令 `T=7/4`。Load 恒 1 的机器对任意全局 affine `q_0` 的 localizer 是 `(3/4)L(q_0²)≥0`。对于 load 为 Boolean literal `z` 的三个资源，Boolean degree-four reduction 给

\[
L((T-z)q_0^2)=(T-1)L(q_0^2)+L(((1-z)q_0)^2)\ge0.
\]

`(1−z)q_0` 是物理全局 quadratic，故第二项确属 M2 允许的平方。

唯一剩余 root 为 M/0，其 slack 是

\[
h=T-\mathrm{load}_{M/0}=\frac54-a+\frac b2-\frac c2.
\]

每个物理全局 affine `q_0` 代换后是 `α_0+α_1 a+α_2 b+α_3 c`。相应完整 affine-localizer Gram，在 basis `(1,a,b,c)` 上为

\[
\bigl[\ell(h B_iB_j)\bigr]_{i,j}
=\frac1{320}
\begin{pmatrix}
304&24&150&66\\
24&24&10&-4\\
150&10&150&17\\
66&-4&17&66
\end{pmatrix}.
\]

整数矩阵的 leading principal minors 依次为 **304、6720、509600、22583120**，均严格正。因此 M/0 的 localizer 也对全部原全局 affine `q_0` 成立，远多于只核每个单变量/补条件。矩阵的一个 cross entry 为负不影响 PSD。

这完整覆盖全部 14 台机器的 physical raw-load localizers。没有将 physical load 换成 canonical activation quality。

## 5. 独立构造逐机 CONFIG，匹配 first 与 pair

全部 eligible jobs 为 unit 的机器，在 `T<2` 时只需 singleton/empty。七个非 M/0 的 private roots 各有 selector 与一个 private incidence，其指标互补，所以配置为两 singleton，权是相应 literal 的 `L` 和其补；两者非负且 sum 1，唯一 distinct pair 矩为零。

资源 u、v、r 也各有两互补 unit-head 指标，按上述方式给两 singleton。资源 `w_u,w_v,w_r` 各只有一个 unit job，按其一阶矩给 singleton，以补量给 empty。这些配置均真实合法，且确实共用同一个 L 的 first/pair。

M/0 root 有三枚 job：selector `A=a`，private u incidence `B=1−b`，private v incidence `C=c`，尺寸分别 `1,1/2,1/2`。其 first 为 `(48,112,48)/160`，pairs `(AB,AC,BC)=(42,6,42)/160`。给以下显式有理 list：

| 配置 | 权 |
|---|---|
| `{A,B}` | `42/160` |
| `{A,C}` | `6/160` |
| `{B,C}` | `42/160` |
| `{B}` | `28/160` |
| empty | `42/160` |

权之和为 1；所有负载≤3/2<T。其 first/pair 正好是上列值。唯一非法全集 `{A,B,C}` 负载为 2，该 list 不含它。

Global L 对其三阶原同机矩却给 `L(ABC)=ell(a(1−b)c)=q−r=7/160`。这与 list 的三阶不相等，但合同只共享 first 和 pair，故不是违反当前 K2。若把该原三阶也要求共享，立即得到反证；没有在此借这个更强合同偷补当前合同。

因此完整 physical K2(P,7/4) 的数学证书已经构造完毕。所有全局表 entries 都是分母整除 160 的有理数；新配置只用上述小分母，不需 oracle 或未知 SDP finder。

## 6. 执行全部原 jobs 的实际 makespan 1

取四个 selectors 分别去 `M/1,Hu/0,Hv/0,Hr/1`。这些被选 roots 仅留 selector。各 incidences 按如下安排：

- M/0 的 u、v 两 jobs 都留其共同 private root，总负载 `1/2+1/2=1`。
- M/1 的 r job 去资源 r。
- Hu/0 的 u job 去 u；Hu/1 的 w_u job 留 Hu/1 private root。
- Hv/0 的 v job 去 v；Hv/1 的 w_v job 留 Hv/1 private root。
- Hr/0 的 r job 留 Hr/0 private root；Hr/1 的 w_r job 去 w_r。

全部 13 原 jobs 均被执行，每台机负载≤1。任意实际 schedule 必执行原 unit selectors，故 makespan 至少 1。因此 **actual OPT(P)=1**。没有 actual-OPT integrality gap，也没有实例不可行结论。

## 7. 直接 canonical product pullback 的两个明确失败

按 Exact 的文字 map：每 canonical `A` 是物理 selector 端，每 canonical incidence claim `Z=A·export`；canonical degree≤2 entries 直接用 physical degree≤4 的 L。具体地

\[
Z_{M0,u}=ab,\qquad Z_{M0,v}=a(1-c),\qquad A_{Hv0}=c.
\]

于是

\[
L(Z_{M0,u}A_{Hv0})=\ell(abc)=-\frac1{160}<0.
\]

`Z≥0` 的 primitive-SA1 lift 乘原 canonical primitive `A_Hv0` 必非负，所以直接不属于 plain common primitive-SA1 R。其二阶非负失败不能被 global canonical M1 PSD 修复：M1 的确由 physical M2 pullback 保留，但 M1 PSD 不强制这个 cross entry 非负。

Outer state 0 的 canonical quality 行是

\[
g=\frac{Z_{M0,u}+Z_{M0,v}}2-\frac{A_{M0}}4
=\frac{ab}2+\frac a4-\frac{ac}2.
\]

乘 `A_Hv0=c` 并 Boolean reduction 后给

\[
L(gc)=\frac r2-\frac q4=-\frac1{80}<0.
\]

它也等于 `L(g c²)`，所以 canonical activation quality 的相应 affine localizer 失败。代数上 `g=a h`，而物理合同只给 `L(h q_0²)≥0` 对 affine `q_0`；并不强制交叉矩 `L(hac)` 非负。这解释为何本反例与 §4 已证 physical localizer PSD 完全相容。

## 8. 结论、算术核验与范围

**未发现 fatal；Exact 的三个声称均已独立重构。PASS 仅限这份给定 raw K2 点的直接 canonical product pullback 失败。** 该 P 的实际 OPT 为 1；另有正常 integral/canonical feasible point。不排除改点、另求 R、其他提取或主算法，也不否定单 outer 给定 R 点的算法。

本审为独立数学证明，未读任何作者程序/LDL/run。为避免手算 determinant 错误，我在本 turn 自行运行了一个仅用 Python `fractions.Fraction` 的 inline 精确算术计算：重建 7×7 bit M2、3×3 symmetry block、2×2 standard block、4×4 physical localizer，计算上述 principal minors，并核对 M/0 CONFIG first/pairs 及两负值。它不是通用 26-endpoint K2 checker，没有模拟调度算法，没有把有限算术检查升级为算法软件实现。

冻结前本 candidate 的新来源只有上述 49 行 Exact；原先 K2/SA1/形式 slice 背景已在开头披露。全球新颖性未认证；一般 UM 主目标仍 OPEN。
