# 同菜单 token-label lift：独立 Exact-first 冻结

2026-10-18，sol_true_hardness（6.1sol max）。本次唯一实际全文读取的作者材料是
`sol_token_label_lift_exact_v1.md`，SHA256
`5a953ed6365e2be029ef31d3ee0184447d626971ad8af7369ee5190eac69a86d`。
未读作者 Proof、code/audit 或相关证明私聊，未向作者询问。本稿从 statement 自行重构，独立程序亦未 import 或读取作者程序。

结论：Exact 的 (A)–(D) 均通过本次独立攻击。以下给一般 M1 的自足证明、所给 aggregate M2 的显式 Schur 正性和 rank、formal lift 负平方，以及排除任何 aggregate-preserving 原 token M2 extension 的必要条件。本稿不是 scheduling native gap 或一般压缩算法。

## 1. 一般 M1：按 token 标签平均与 contrast 分块

先看一组 k≥2，r∈{0,…,k}，h=k−r。记

`a=L(A)`，`p_i=L(X_i)`，`M_ij=L(X_i X_j)`。

Boolean ideal 与 M2 PSD 给 `p_i≥0`、`M_ij≥0`：例如 `L(X_iX_j)=L((X_iX_j)²)≥0`。Exact 的两个 aggregate 等式给

`Σ_i p_i=r a`，`Σ_j M_ij=r p_i`，`M_ii=p_i`。

取任意 lifted linear polynomial，由常数、untouched context variables 以及各组全部 t_a,x_a,i 组成。在每组把系数按 token a 分为平均值与和为零的 contrasts。组内独立 token-permutation 对称性使：

* 该组 contrast 与 context、其它组、该组平均项的二阶交叉均为零；
* 平均项的全部一、二阶矩等于原 aggregate functional 中的线性代换 `Σ_a t_a=k−rA`、`Σ_a x_a,i=X_i`。

第二条可直接由 Exact 显示的系数求和核验：`Σ_a,b L'(t_a x_b,i)=h p_i=L((k−rA)X_i)`；`Σ_a,b L'(x_a,i x_b,j)=M_ij`；`Σ_a,b L'(t_a t_b)=L((k−rA)²)`。不同组和 context 的交叉由其 replacement factors 直接乘开，亦相同。因此所有平均项合起来的平方值为 L 对某个 aggregate/context linear polynomial 平方的值，非负。

还需每组的 contrast block。令 D 为 same-token 的 home/head 二阶矩阵，O 为两个不同 token 的同类矩阵。对每个 token 的 contrast 系数向量 `(u,v_i)`，所需矩阵为 D−O。由 Exact 系数逐项相减：

`k(k−1)(D−O) = [[h r a, −h pᵀ], [−h p, k diag(p)−M]]`。   (1)

其二次型恰为

`h Σ_i p_i (u−v_i)² + Σ_{i<j} M_ij (v_i−v_j)² ≥0`。   (2)

核算使用 `Σp=ra` 和 M 的行和 r p；第二项是 `r diag(p)−M` 的 weighted Laplacian。所有权非负，h≥0，分母 k(k−1)>0。因此每组 contrast block PSD。相加得到完整 lifted M1 PSD，允许任意多组及与共同 context 的相关性，没有假定不同组独立或把 L 解释成 true law。

k=1 没有 contrast。r 只能 0 或 1，M1 正好是原 L 的线性代换 `t=1−rA, x_i=X_i`。当 r=0 时，ΣX=0 与 Boolean/M2 令全部 X 的相关 M1 矩为零；当 r=1 时，XA=X、ΣX=A 令不同 heads 的 M1 交叉为零，故与“不兼容请求取零”的约定一致。没有 (k)_2 分母。

r=0 时 h=k，Σp=0，式 (1) 的整个 contrast 块为零，全部 homes 恒为 1；r=k 时 h=0，home contrasts 为零，head contrast 仅剩 Laplacian。故两端、空 head 菜单、inactive/active 混合均在证明内。一般 (A) 得证；没有从此推断 M2 PSD。

## 2. 所给 signed functional 的基础数据与矩约束

共有 C(10,4)=210 个 four-subsets。beta 的非零权是：10 个纯半集各 1/8，100 个 2+2 半集各 −1/400，故总权 `10/8−100/400=1`。nu 与 beta 都逐点满足 ΣXi=4；所以定义的 L 满足该等式乘任何总度≤3 单项式，包括带 Y 的乘子。Boolean reduction 则直接满足全部 degree≤4 Boolean ideal。

记半集内外的 beta 矩。直接计数得到：

| beta moment | 值 |
|---|---:|
| Xi | `2/5` |
| XiXj，i≠j 同半 | `7/20` |
| XiXj，跨半 | `−1/25` |
| 三个不同 Xi 全同半 | `1/4` |
| 三个不同 Xi 为 2+1 | `−1/100` |

Xi²=Xi。L 的 pure-X 矩来自真 uniform nu，Y 的一阶与二阶均为 delta，因为 beta 总权 1。这分别给 Exact 所说的两个 abstract full-row laws；跨半 `L(YXiXj)=−delta/25` 已明确排除 true joint X,Y law，但不自动排除 degree-four M2 PSD。

## 3. 完整 67 维 aggregate M2 的精确 PSD 与 rank 55

Boolean degree≤2 monomials 共 `1+11+C(11,2)=67` 个。pure-X 部分有 56 个，four-slice 上可用 45 个 pair monomials `P_e=XiXj`（e={i,j}）作基底，因为

`Xi=(1/3)Σ_{j≠i}XiXj`，`1=(1/6)Σ_{i<j}XiXj`。

这些等式对 nu 和 beta 均逐点成立，所以与任何 Gram 索引相乘的 L 矩也一致。Y 部分用十个 YXi 作基底，因为 `Y=(1/4)Σ_i YXi`。上述给 12 条线性独立 Gram-null relations，故完整 rank 至多 55。

在 45+10 基底上，Gram 为

`G=[[A, delta C], [delta Cᵀ, delta D]]`，

其中 `A_ef=E_nu(P_eP_f)`、`C_ei=E_beta(P_eXi)`、`D_ij=E_beta(XiXj)`。令 R 为 10×45 的 vertex/pair incidence 矩阵，J 为全一矩阵。由于 A 的三个 entry 值分别是相同 pair 的 2/15、交一元的 1/30、互异的 1/210，

`A=(1/14)I+(1/35)RᵀR+(1/210)J`，

`A⁻¹=14I−(4/3)RᵀR+(1/4)J`。   (3)

`RRᵀ=8I+J_10`，故 A 的 eigenvalues 是 `4/5`（常数，1维）、`3/10`（vertex standard，9维）、`1/14`（ker R，35维），全正。

设 E=CᵀA⁻¹C。beta 的同半置换与两半互换对称性使 D、E 在 R^10 上分成三类不变正交子空间：常数向量（1维）、半符号 s=(1^5,−1^5)（1维）、两个半集内各自和为零的 contrasts（8维）。精确数值为：

| 子空间 | D eigenvalue | E eigenvalue | D−delta E（delta=1/100） |
|---|---:|---:|---:|
| constant | `8/5` | `4932/125` | `3767/3125` |
| half-sign | `2` | `15` | `37/20` |
| within-half contrasts | `1/20` | `453/1000` | `4547/100000` |

为使这些数值不依赖黑箱计算，可用以下短算重构：`RC=3D`，`1_45ᵀC=(12/5)1_10ᵀ`，因而

`E=14 CᵀC−12D²+(36/25)J_10`。

CᵀC 的三类 eigenvalues 分别是 `498/125, 9/2, 69/2000`。例如 `C1` 在 20 个同半 pair 上为 7/5，在 25 个跨半 pair 上为 −4/25，平方范数除以 10 为 498/125；`Cs` 在 20 个同半 pair 上为 ±3/2，其余零，平方范数除以 10 为 9/2；对 v=e1−e2，Cv 有六个 ±1/10 和十个 ±3/100，其余零，平方范数除以 2 为 69/2000。置换对称性将这三个方向推广为整个 1+1+8 分解。

因此 Schur complement `delta(D−delta E)` 为 10 维正定；A 为 45 维正定，G 为 55 维正定。连同前述 12 null relations，完整 67 维 M2 为 PSD，rank 恰 55。没有 numerical tolerance、未知 moment 或 degree-six test。

## 4. uniform formal lift 的负平方

按 Exact 取 k=r=4、h=0、A=1，保留 untouched Y。记 S=Σ_i s_i Xi。由第 2 节，`E_beta S²=sᵀDs=20`，而 ΣXi=4。formal lift 使不同 token 不同 head 的矩为原矩除以 12，相同 head 不同 token 及同 token 不同 heads 为零。

对 `Q=Y Σ_i s_i(x_1,i−x_2,i)`，Y²=Y，直接展开：

`L'(Q²) = (2/4)L(YΣXi) − (2/12)L(Y(S²−ΣXi))`

`=2delta − (8/3)delta = −(2/3)delta = −1/150`。

Q 是 degree two，所以这是 lifted M2 的真实负 Gram 范数，不是一个仅有负 entry 但仍可能 PSD 的指控。(B) 的两面均得到独立证明。

## 5. 排除任何 aggregate-preserving original-token M2 extension

此节不使用 uniform kernel。假设存在 Exact (C) 所说的原 token extension，记其 functional 为 Lhat。原 token 一热等式及 Boolean/M2 已足够令同 token 不同 head 的 quadratic product null：固定 x_a,i，将一热方程乘它，所有 `Lhat(x_a,i x_a,j)` 非负且总和为零，故各项为零；其 degree-two norm 为零，所以再乘 Y 或 Y² 仍为零。这也与原 head full rows 的要求相容。

对任意 real v_i，令 degree-two polynomials

`P_a=Y Σ_i v_i x_a,i`，a=1,…,k。

共同 M2 PSD 给

`k Σ_a Lhat(P_a²) − Lhat((Σ_a P_a)²) = Σ_{a<b} Lhat((P_a−P_b)²) ≥0`。   (4)

用同 token exclusive null、Boolean Y、X_i=Σ_a x_a,i，以及全部 aggregate≤4 矩的保真，(4) 左侧变成

`vᵀ [k diag_i L(YXi) − (L(YXiXj))_ij] v`。

因此 Exact (D) 的 block PSD 是任何这类 extension 的必要条件。它不依赖 token-label 对称性，不依赖给出的 formal kernel，也不需要把 Y 解释成条件概率事件。

对本点，L(YXi)=delta·2/5，`(L(YXiXj))=delta D`。第 3 节已算 Ds=2s，故该必要 block 在半符号方向的 eigenvalue 为

`delta(4·2/5−2)=−2delta/5`。

其 quadratic value 为 `(−2delta/5)||s||²=−4delta=−1/25<0`，与 (4) 矛盾。因此不存在任何保持这个完整 aggregate functional 的原 token M2 extension。(C)、(D) 得证；没有将“uniform lift 不 PSD”偷换成“所有 extension 不存在”。

## 6. 自写独立 Fraction 审计

`sol_true_hardness_token_label_lift_exact_first_audit.py` 从 210 个 subsets 和 statement 权重直接重建 functional，全过程精确 Fraction：

* 直接构造全 67×67 Boolean monomial Gram，做带零对角检查的 rational symmetric Schur elimination，得到 PSD、rank55；
* 对全部 232 个 Boolean degree≤3 monomials 核 ΣXi=4 的 multiplied 等式；
* 直接核 45 维 A 的 inverse 公式、RC=3D，以及三类 D/E eigenvectors/eigenvalues；
* 直接逐项展开 20 项 Q 的 400 项平方，得 −1/150；
* 核必要 block 的半符号 eigenvalue −1/250 和 quadratic −1/25。

结果保存在 `sol_true_hardness_token_label_lift_exact_first_audit_output.json`。一般 (A) 的量词由第 1 节的显式 PSD 分解负责，未以本固定点的 finite audit 代替。没有运行作者任何 audit、没有使用浮点 SDP 可行性器。

## 7. 准确结论范围

本点是一个 aggregate M2+两 abstract full-row laws 的压缩失真实例。它不是 native scheduling 的 CONFIG 或 moment gap，不证明 Bamas 的 witness 满足/违反任何系统，不排除换另一个 aggregate feasible point、增加必要 block 或更强 lift。D 只给必要条件，未证明它充分。

本稿保持 Exact-first 来源冻结；待 root 真正实际全文读后，才可另读作者 Proof 并写新的 read-after。repo 未改，Work/Git/凭据未使用。
