# 强配置矩的共同匹配不可实现与锐二阶修复半径

本文给经典非整数背包伪矩在实际不相关机上的自足编译；不认领该伪矩机制的新颖性。即使所有机器局部配置相容且所有短事件非负，给定共同二阶仍可能没有真实匹配 law。所有实例都有显然最优调度；结论不是调度间隙、计算困难性或 UM-TARGET-v1 的否定。

## 1. 精确系统与要否定的额外接口

每条有限端 `e=(i,j)` 有 Boolean 变量 `x_e`，同任务不同端的乘积为零；所有矩在这个任务商代数中解释。强 H2 在阈值 T 上要求同一 degree≤4 线性泛函 L 满足：归一化、one-hot 乘到 degree≤3、全局 M2 PSD、每台机器的 degree≤1 负载 localizer PSD，并有每台机器的一份 CONFIG(T) 分布，其一阶以及同机二阶与 L 相容。

记 `SH(r)` 为对应 degree≤2r 系统：全局 Mr PSD，one-hot 乘到 degree≤2r−1，负载 localizer 乘到 degree≤r−1。本文反例甚至允许每行 CONFIG 与 L 的**全部本行 degree≤2r 矩**相容，而不仅共享二阶；并且可要求每个 degree≤2r 的 mixed literal cylinder 非负。

本文不否定从证书构造某个实际重匹配的可能性；否定的是额外接口：输出一份真实完整重匹配分布，保留给定 L 的全部一阶和跨机器二阶。这是具体而较强的合同，不能从一阶匹配多面体的积分性直接推出。

## 2. 任意固定阶的共同匹配二阶障碍

精确身份：`UM-FIXED-DEGREE-STRONG-CONFIG-MATCHING-LAW-OBSTRUCTION-v1`。

**命题。** 对每个整数 r≥2，对每个奇整数 N≥4r−1，令 t=N/2。由 N 个不相交 K2,2 单位块组成的实例 P_N（2N 机器、2N 任务，下节定义）有一个 degree≤2r 的有理共同证书，满足 Mr PSD、所有相应 one-hot、所有 degree≤r−1 负载 localizer PSD、每行全部 degree≤2r CONFIG 矩相容，并且每个相容 degree≤2r mixed literal cylinder 非负，代入每块匹配 bit 后相容者严格为正，其余为零；但仍不存在保一阶和二阶的真实完整 heavy matching 分布。对每个固定 r，证书大小和生成时间为 N 的多项式；若 r 本身作为输入，显式矩大小是 N^{O(r)}，不声称关于 r,N 联合多项式。

### 2.1. 全阶 formal slice 的 radical

对 |A|≤2r 定义 `L(b_A)=(t)_(|A|)/(N)_(|A|)`，其中 (z)_a=z(z−1)…(z−a+1)、(z)_0=1，记 S=Σb_i。由 μ_a=(t)_a/(N)_a，aμ_a+(N−a)μ_(a+1)=tμ_a；递推成立到 |A|≤2r−1。因此 `(S−t)P≤r−1` 与全部 degree≤r 多项式正交。

### 2.2. 齐次层的 up/down 分解

令 V_k 为 k-子集的实系数空间，内积为标准系数内积。对 v∈V_k，令 `p_v=Σ_(|A|=k)v_A b_A`。定义 up 与 down：

\[
 (U_kv)_B=\sum_{A\subset B,\ |A|=k}v_A,
 \qquad D_{k+1}=U_k^*.
\]

在 V_k 上直接逐坐标计数得到

\[
 D_{k+1}U_k-U_{k-1}D_k=(N-2k)I.
 \tag{5}
\]

于是 k<N/2 时

\[
 \|U_kv\|^2=\|D_kv\|^2+(N-2k)\|v\|^2,
\]

故 U_k 单射。令 harmonic 空间 `H_k=ker D_k`，则

\[
 V_k=H_k\oplus\operatorname{im}U_{k-1}
\]

是标准系数内积下的正交分解。又由 Boolean 乘法

\[
 p_{U_{k-1}v}=(S-k+1)p_v
 \equiv(t-k+1)p_v\pmod{(S-t)P_{\le r-1}}.
 \tag{6}
\]

从 k=r 向下反复分解并用(6)降阶，degree≤r 空间模 radical 被 H_0,…,H_r 的多项式张成。此处 r<N/2，因为 N≥4r−1。

### 2.3. Harmonic Gram 的全参数计算

若 h∈H_k，则对每个 |C|<k，有

\[
 \sum_{A\supseteq C,\ |A|=k}h_A=0.
 \tag{7}
\]

因为对 D 连续作用 k−|C| 次会给此包含和乘以正整数阶乘。

先取 h∈H_k 和一个 degree ℓ<k 单项式 b_B。其内积为

\[
 \sum_{|A|=k}h_A\mu_{k+\ell-|A\cap B|}.
\]

把交叠数 s=|A∩B| 的函数在 s=0,…,ℓ 上按 `binom(s,c)` 展开；每项是对 C⊆B,|C|=c≤ℓ<k 的包含和，因(7)为零。因此 H_k 与全部较低次数正交，特别地不同阶 harmonic 互相正交。

对 h,g∈H_k，按交叠数分组写

\[
 W_\ell=\sum_{|A|=|B|=k,\ |A\cap B|=\ell}h_Ag_B.
\]

由(7)，对 c<k，

\[
 \sum_{\ell=0}^k\binom\ell c W_\ell
 =\sum_{|C|=c}\left(\sum_{A\supseteq C}h_A\right)
                  \left(\sum_{B\supseteq C}g_B\right)=0.
\]

并且 `W_k=Σ_A h_Ag_A`。三角二项反演给

\[
 W_\ell=(-1)^{k-\ell}\binom k\ell\sum_Ah_Ag_A.
\]

因此

\[
 L(p_hp_g)=c_k\sum_Ah_Ag_A,
 \qquad
 c_k=\sum_{\ell=0}^k(-1)^{k-\ell}\binom k\ell\mu_{2k-\ell}
     =\frac{(t)_k(N-t)_k}{(N)_{2k}}.
 \tag{8}
\]

最后一个恒等式可自足验证：固定不相交的两个 k-子集 A,B，在真实均匀整数 s-slice 上对事件 `b_A=1,b_B=0` 做包含排除，得到左边；直接计数得右边。两边乘 `(N)_(2k)` 后都是关于 t 的次数≤2k 多项式，对 s=0,…,N 的 N+1≥2k+1 个整数取值一致，故对全部实 t 恒等。

取 t=N/2 时，k≤r 的每个下降阶乘因子严格为正，因此 c_k>0。张成、跨阶正交及(8)证明 Mr PSD。

### 2.4. 所有短 mixed literal cylinders

对不交 A,B、|A|=a、|B|=b，a+b≤2r，包含排除或同样的多项式恒等式给

\[
 L\left(\prod_{i\in A}b_i\prod_{j\in B}(1-b_j)\right)
 =\frac{(t)_a(N-t)_b}{(N)_{a+b}}.
 \tag{9}
\]

因 t=N−t≥2r−1/2，a,b≤2r 时所有因子严格为正。任一原端 cylinder 经 K2,2 编译后，若同一 bit 同时出现两种相反 literal 则为零；否则化为(9)。原端的重复变量也不增加 a+b。

### 2.5. 编译及真实二阶 law 的矛盾

使用下节的 K2,2 替换；degree 不增加，故 Mr PSD。所有 row load 恒一使任意所要求阶数的 localizer 恒零。每行的两个 singleton 配置与全部本行矩一致。下节的非整数方差矛盾只用一阶和二阶，因而对所有 r 原样成立。

这说明增加任意固定阶、增加该阶内全部 literal 非负、甚至共享每行全部同阶 CONFIG 矩，都不自动给保留给定跨机器二阶的真实 heavy matching law。它没有排除近似保矩或改动矩的实际舍入。

### 2.6. 失败也可落在 heavy 占用机器的二阶，而非仅块内标签

可以把同一 Boolean formal-slice 证书编译得更小：N 件单位任务，每件 s 只有两台私有机器 a_s、c_s，分别用端 b_s 和 1−b_s。于是 2N 机器、N 任务，每行只有一个原端。所有本行 CONFIG 矩与 singleton/empty 分布相容。负载 localizer 不再恒零，但对 degree≤r−1 的 q，

\[
 L(b_s q^2)=L((b_s q)^2)\ge0,\qquad
 L((1-b_s)q^2)=L(((1-b_s)q)^2)\ge0,
\]

因为 b_s q 和 (1−b_s)q 的次数至多 r。因此仍是 SH(r) 证书，且全部短 cylinders 的结论不变。

现在 b_s 正是机器 a_s 被 heavy 占用的指示变量，而不是始终占用机器中的任务标签。若要保留占用指示的一阶与跨机器二阶，仍由 Var Σ_s b_s=0 和非整数均值矛盾。这个推论进一步说明：把目标从“保重端二阶”放宽到“只保重占用机器的二阶”仍不足以避开该接口障碍。它依旧不妨碍任意实际匹配达到 OPT=1。


## 3. 实际机器编译与非整数二阶分离

### 3.1. 编译成全部负载恒一的 K2,2 块

块 s 含机器 `m_s0,m_s1` 与任务 `j_s0,j_s1`。本块四个有限时间均为 1，跨块不可用。定义端变量

\[
 x_{m_{s0},j_{s0}}=x_{m_{s1},j_{s1}}=b_s,
 \qquad
 x_{m_{s0},j_{s1}}=x_{m_{s1},j_{s0}}=1-b_s.
 \tag{4}
\]

每任务恰一、每行负载恰一都是 Boolean 商代数中的恒等式。同一任务两端乘积和同一行两端乘积都是 `b_s(1−b_s)=0`。对原端单项式按(4)代入定义 L；代入不会增加次数。原端 degree≤r 多项式拉回 Boolean degree≤r，故原全局 M_r PSD。全部 one-hot 等式严格成立，全部 T=1 负载 localizer 恒为零。

每一行使用两个 singleton 配置，各权 1/2。它们的一阶与 L 一致，同机二阶均为零。不仅二阶如此，本行全部次数的矩都由 `b_s+(1−b_s)=1` 和 `b_s(1−b_s)=0` 决定，故与同一 singleton 分布一致。每个任务在任意一个本块完美匹配中都可完成，所以 OPT=1。

### 3.2. 真实共同 heavy pair law 不存在

所有有限端在 T=1 下都是 heavy，每件任务都没有 light 端。任何完整 heavy placement 因而是各 K2,2 块中两种完美匹配的一种。令随机变量 B_s∈{0,1} 指示真实匹配在块 s 采用(4)中的直匹配。

若其一阶和跨块二阶与 L 相同，则

\[
 \mathbb E B_s=1/2,\qquad
 \mathbb E B_sB_u=\frac{N-2}{4(N-1)}\quad(s\ne u).
\]

所以真实整数随机变量 Q=Σ_s B_s 满足

\[
 \mathbb E Q=N/2=t,\qquad
 \mathbb E Q^2=N/2+N(N-1)\frac{N-2}{4(N-1)}=t^2.
\]

即 Var Q=0，故 Q=t 几乎处处。但 N 为奇数，t 非整数，矛盾。即使允许输出部分匹配，只要其边一阶仍与 L 相同，任务覆盖和的期望为一而逐原子至多一，也强制几乎处处完整；不能借部分匹配规避矛盾。


## 4. 保一阶的最优二阶修复半径

本节属于同一 v1 的结论，不声明任何调度近似下界。记跨块目标 pair 为 μ₂=(N−2)/[4(N−1)]。在所有真实 K2,2 完整匹配分布中，约束 E B_s=1/2，定义 Δ 为 max_(s<u)|E B_sB_u−μ₂| 的最小值。则精确有

Δ=1/[4N(N−1)]。

下界：Q=ΣB_s 的均值是半整数 N/2，每个整数 Q 都满足 (Q−N/2)²≥1/4。因此 Var Q≥1/4。伪二阶的方差为零，故

2Σ_(s<u)(E B_sB_u−μ₂)=Var Q≥1/4。

若每项绝对值≤Δ，左侧≤N(N−1)Δ，得到下界。达到：各以概率1/2选择均匀大小 (N−1)/2 与 (N+1)/2 的子集作为直匹配块。全部一阶仍1/2，Var Q=1/4；交换对称性使每个 pair 恰增加 1/[4N(N−1)]。其余跨块端 pair 经 b 或1−b 替换后只改变符号，故全端二阶 sup 误差相同；块内矩完全保持。

这个半径趋于零：精确保二阶接口被否定，允许带误差重耦合的提取未被否定。上述混合还能用两台均匀子集采样器描述；本结果不要求输出其指数多个原子。

## 5. 大小、证据、经典背景和未闭义务

实例有2N机、2N任务、4N有限单位端。一个至多2r次的端单项式经替换要么为零，要么是一个相容 bit cylinder，直接按闭式计算；每条矩的有理位长 O(r log N)。显式证书总大小 N^{O(r)}，可在输出长度的多项式时间内生成。每固定 r 为 N 的多项式；r 作为输入时不声称联合多项式。Boolean M_r 的秩为 binom(N,r)：dim H_k=binom(N,k)−binom(N,k−1)，正 Gram 块求和望远镜；原端矩可拉回且包含所有 bit 单项式，秩相同。

经典背景：Grigoriev 的非整数 knapsack SoS 障碍已存在；Potechin, *Sum of Squares Lower Bounds from Symmetry and a Good Story*, ITCS2019, [正式页面](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITCS.2019.61) 的摘要明确说明恢复 Grigoriev 的 knapsack 下界。本稿不导入其完整定理，PSD 由上文自行证明；已取得[20页正式原文](../../../history/source/literature/unrelated_machines/potechin_2019_symmetric_sos_knapsack.pdf)，SHA256见literature_manifest；实际核摘要及§1.1 Theorem1（PDF3/印61:3），未声称完整内化论文。

有限核验：[Fraction审计](../../../tests/audits/unrelated_machines/strong_configuration_matching_moment_audit.py)精确 Schur 消元三个小矩阵，并独立以 inclusion–exclusion 核对 cylinder、方差与 Gram 系数；[冻结结果](../../../evidence/runs/unrelated_machines/strong_configuration_matching_moment_audit.json)。一般结论来自上述证明，增加测试数量没有证明作用。独立重构及最终稿攻击见[审查](../../reviews/unrelated_machines/strong_configuration_matching_moment_review.md)。

本结果不能推出强 H2 的积分间隙为2，也不排除从同一一阶或改变二阶后输出某个好调度。全输入桥仍须求出可计算共同容量并给所有机器实际统一余量；本节的锐修复半径要求进一步分析“改动二阶”与真实负载之间的累计误差，而非强求原伪矩是真实分布。
