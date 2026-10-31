---
id: "unrelated-machines/weak-h2-weighted-fanout-boundary-review"
kind: "review"
type_tag: "审查"
title: "弱H2强行矩与加权扇出边界双源审查"
status: "integrated-with-strong-contract-calibration"
truth_status: "scoped-general-proofs-plus-exact-finite-audits; no-general-UM-algorithm"
review_level: "full-source-read-and-cross-archive-comparison"
scope: "weak H2 configuration/moment gap, strong same-row pair calibration, and weighted fanout preloaded-witness boundary"
source_refs:
  - "source:6a55a2b4d6d9bbb39e0f:research/current/unrelated_machines/weak_h2_configuration_moment_gap.md"
  - "source:9b272a005d864cfa241d:research/current/unrelated_machines/weighted_fanout_profile_boundary.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/weak_h2_configuration_moment_gap_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/weighted_fanout_profile_boundary_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/unrelated_machines/weak_h2_configuration_moment_gap.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/weak_h2_configuration_moment_gap_audit.json"
legacy_ids:
  - "UM-WEAK-H2-CONFIG-MOMENT-GAP-v1"
  - "UM-STRONG-H2-ROW-PAIR-STAR-EXACT-v1"
  - "UM-WEIGHTED-FANOUT-PROFILE-BOUNDARY-v1"
  - "UM-FANOUT-MISSING-ONE-THREE-HALVES-v1"
---

# 1. 实读范围、身份和双源关系

本批完整读取 `clean show` 的两个 canonical 正文、inventory 元数据、正文所链接的两份既有审查、弱 H2 的最小精确验证器和冻结 JSON，并回读相关稀释星、配置矩、扇出选择器与预载模型文稿。当前源指纹为：`6a55a2b4d6d9bbb39e0f`，路径 `research/current/unrelated_machines/weak_h2_configuration_moment_gap.md`，SHA-256 `2e6aa07ed9e6cd3401eaa2560429e71af4932cdbb7633ff7a54a9ad973cb5dec`，23401 bytes；`9b272a005d864cfa241d`，路径 `research/current/unrelated_machines/weighted_fanout_profile_boundary.md`，SHA-256 `7bb7e967d492751f0f92fb547608af56e5aaffff387dca559b54d20ef283d78`，10051 bytes。两源均是冻结提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 的当前正文。

两个对象有共同主题“用局部接口边界校准近二余量”，但数学量词不同，不能合并成一个定理。弱 H2 源给出一个显式实例族：共享一阶端边际、全局 degree-four 矩和每机 degree-one 负载 localizer 都可行，而配置行不共享二阶时 gap 趋近 2；同一稀释星族一旦要求配置共享同机二阶，阈值又精确回到真实 OPT。加权扇出源从两份已知完整 YES 调度出发，给出预载关闭/开放接口的确定性实际舍入预算和三半锐界。前者是松弛证书的相容性障碍，后者是有两个实际见证时的构造性正面边界；不能把任何一项扩大成一般 unrelated-machines 算法或困难性结论。

本页将两个当前 source ID 处置为 `integrated`。与已有同名审查重复的部分作为版本复读和量词核对，不制造重复资产；本页保留当前 canonical 的精确参数、强合同校准、预载算法、加权等号族和缺一三半反例，供后续关系图使用。

# 2. 弱 H2：同一一阶 CONFIG 加全局四阶矩仍可趋二

## 2.1 合同与参数族

稳定身份为 `UM-WEAK-H2-CONFIG-MOMENT-GAP-v1`。每个有限端 `e=(i,j)` 有 Boolean `x_e`，任务 one-hot 在相容商代数中成立。弱 H2(T) 的共同泛函 `L` 要求：全局 degree-four 矩对应的 `M_2` PSD；每台机器 degree-one 负载 localizer PSD；到次数三的 one-hot 守恒；同一一阶边际 `x_e=L(x_e)` 有完整 `CONFIG(T)` 行。CONFIG 行只与一阶相容，**不要求其同机二阶或更高矩等于 `L`**。

固定 `k>=3`，令
\[
b=k^2,\qquad r=b+1,\qquad N=b+k,\qquad T=t=N/r=1+(k-1)/(k^2+1).
\]
实例有 `k^3+3k-1` 台机器、`k^3+k^2+k` 项任务：中心 `V_a`、全局 `G_g` 和局部 `R_{a,l}`。每块有单位 `X_a`（在 `V_a` 或所有 `G_g`）、`b` 件 `Y`（只在本块 `R` 上为 1）和 `k` 件 `Z`（在 `V_a` 上为 `1/k`、本块 `R` 上为 1）。

真实整数下界利用 `C<2` 时每台单位机器至多接一个单位任务：`k` 件 X 只有 `k-1` 台 G，某件 X 必须去中心；该块 `b` 件 Y 占据 `b` 台 R，唯一剩余 R 至多接一件 Z，所以中心还承担至少 `k-1` 件 Z，得
\[
\operatorname{OPT}=2-1/k.
\]
同一构造给出上界，故
\[
\operatorname{OPT}/T=(2-1/k)/(1+(k-1)/(k^2+1))\to2.
\]
这是一族松弛 gap 的一般证明，非有限猜测；它不声称任何算法在该族上失败。

## 2.2 fractional multislice 与 PSD

通用引理取任意 `m>=3,N>=m+1`、`t=N/m`，N 个任务各有 m 个单位端。对至多四个不同任务的相容单项式，用各机器计数 `c_a(S)` 定义
\[
\mu_S=\frac{\prod_{a=1}^m(t)_{c_a(S)}}{(N)_{|S|}},
\]
同任务异端置零。下降阶乘递推给出 one-hot 及 `(Q_a-t)` 对 degree-three 测试的 radical；二次空间按任务对数组分成常数、一次、对称 harmonic 与反对称 harmonic 四块。对称块的机器核为
\[
\mathcal K_S(B,C)=\frac{t^2}{N(N-3)}\left(F-\frac{mH}{N-2}+\frac{d}{(N-1)(N-2)}\right),
\]
其中 `B,C` 对称且行和为零；由行和零的 Cauchy 不等式 PSD。反对称块为
\[
\mathcal K_A(C,D)=\frac{t^2}{(N-1)(N-2)}\langle C,D\rangle,
\]
也 PSD。故 `M_2` 自足地 PSD，且允许负三阶矩；这不是概率分布。

全局 L 先以权 `1/k` 选择激活块。条件于激活块，X 采用真实双射，非激活块的 Y 使用真实注入且 Z 留中心，激活块的 N 件 Y/Z 在 R 上使用上述四阶伪矩；再对激活块平均。张量积和线性拉回保持全局 `M_2` PSD，组件守恒给 one-hot，激活 R 的 localizer 恰为零，其他机器由真实组件的非负负载 Gram 得到 localizer PSD。

同一一阶端边际由配置行实现：中心 `V_a` 用 `{X_a}` 权 `1/k` 与全体 Z 权 `(k-1)/k`；全局 `G_g` 按 X 均匀配置；每台 R 把各 Y 以 `1/r`、各 Z 以 `1/(kr)` 配置，合计 `(b+1)/r=1`。每个正配置的负载为一，故是 CONFIG(1)，也必是 CONFIG(T)。这里恰恰利用了弱合同不共享同机二阶。

## 2.3 强化合同的精确校准

正文的 `UM-STRONG-H2-ROW-PAIR-STAR-EXACT-v1` 只研究同一稀释星族：要求每台机器 CONFIG 行对不同端的二阶条目与共同 `L` 匹配。因为 `1<T<2` 且行端均为单位，合法配置至多含一个任务，故共享二阶给每行不同端 `L(x_e x_h)=0`。`M_2` PSD 进一步推出条件容量
\[
\sum_{e\in E_i}L(x_f x_e)\le L(x_f)
\]
对任意原端 f；证明用 `x_ex_h` 的零范数和多项式 `x_f(1-Q_i)` 的平方。

取任一中心端 `f=(V_a,X_a)`，令 `q=floor(k(T-1))<=k-2`。中心配置至多容纳 q 件 Z，给出 `sum_j L(x_f x_{V_a,Z_j})<=q alpha`。X/Z one-hot 把剩余 Z 端质量推到本块 R；本块 `r=b+1` 台 R 的条件容量上界再与 b 件 Y 的质量合并，得到
\[
(b+k-q)\alpha\le(b+1)\alpha,
\]
从而 alpha=0。对每个中心均如此，X 的总一阶覆盖只能落在 `k-1` 台 G，矛盾。所有 `T<2-1/k` 的强合同证书均不可行；真实最优调度在 `T=2-1/k` 达到，所以该族的强 H2 阈值精确等于 OPT。

这个校准只说明同机二阶共享切掉上述伪矩族；不能推出一般强 H2 的 gap 小于 2、强合同可多项式求解，或存在统一舍入。它应作为第三阶段中“弱 CONFIG 投影—同机二阶相容性—条件容量”的条件边。

## 2.4 有限证据和限制

规范验证器使用 Fraction/整数 Bareiss 做通用 `m,N=(4,3),(5,3)` 的 PSD 与 one-hot 小检查；全局 `k=2,b=2,T=4/3` fixture 检查 M1、全部机器 localizer、有限端 CONFIG 边际和负同机 pair/负三阶。一般 PSD 由 multislice 分解承担，有限 fixture 不承担任意 `k` 量词；没有枚举全局混合的全部矩，也没有通用精确 SDP/CONFIG 求解器。

强化反对意见是实质性的：弱证书在 R 行的同机二阶为正（约为 `t(t-1)/(N)_2`），而 singleton CONFIG 的同机二阶为零；同机三阶还可为负。故它不满足共享二阶或全三阶非负的强化合同。不能把弱 gap 直接转写成强合同 gap，也不能用有限程序通过替代一般证明。

# 3. 加权扇出预载接口：有两个实际 YES 才有正面预算

## 3.1 定义和两个稳定身份

稳定身份为 `UM-WEIGHTED-FANOUT-PROFILE-BOUNDARY-v1` 与 `UM-FANOUT-MISSING-ONE-THREE-HALVES-v1`。基础机器包括输入 `a`、互异输出集合 `B={b_1,...,b_q}`、任意内部机器；有两个逐任务完整实际调度：`S_1` 中只开放 `a`、所有 B 关闭且 makespan≤T，`S_2` 中关闭 `a`、全部 B 开放且 makespan≤T。关闭仅加不可迁移预载 T，不删除原任务边。对 `K` 和 `i in K`，状态 `P_(K,i)` 关闭 `a` 与 `K\{i}`，其余输出开放，真实最优值为 `mu_(K,i)`。

对任意显式有理 `beta_i>=0`, `sum beta_i=1`，确定性算法输出某 i 和该状态完整调度，使
\[
C_{max}\le(2-\beta_i)T.
\]
并且
\[
\sum_{i\in K}\mu_{K,i}\le(2k-1)T.
\]
均匀 beta 给 `2-1/k`；加权星族达到等号面 `mu_i=(2-omega_i)T`，因此预算常数对这个接口精确锐。算法输入只含两份 YES、beta 和显式矩阵，不调用未知 `mu`。

第二身份定义 `nu_i` 为关闭 `a,b_i`、其余输出开放的最优值。任意不同 `u,v` 有
\[
\nu_u+\nu_v\le3T,
\]
从而至少一个缺一状态可构造到 `3T/2`，至多一个 `nu_i` 超过三半，且 `sum_i nu_i<=3qT/2`。满二叉树边任务（父端 `T/2`、子端 T）使每个缺一状态恰为 `3T/2`，且每项任务只有两台可用机器，说明系数锐。

## 3.2 加权闭包与逐件拼接证明

给两个见证定义源端权
\[
w_{uv}=\sum_{j:S_1(j)=u,S_2(j)=v}p_{uj},\quad L_u=\sum_{S_1(j)=u}p_{uj}\le T.
\]
先给每个输出终端自己的颜色，再依次把仍未着色的点永久吸入满足 `w(u,C_i)>=beta_i L_u` 的颜色闭包，剩余点归最后一色。零行和 `beta=0` 都被显式处理，扫描和有理比较为总位多项式。

每个颜色类含一个输出和输入 a。对类 `W` 的每件任务采用 `S_2` 端当两个见证端都在 W，否则采用 `S_1` 端；该拼接不复制、不丢弃任务。类内机器负载是
\[
\sum_{S_1(u)\to outside W}p_{uj}+sum_{S_2(j)\to u,,S_1(j)\in W}p_{uj},
\]
第一项由闭包保证至多 `(1-beta_i)L_u`，第二项由 S2 至多 T，故全局至多 `(2-beta_i)T`。关闭输出加预载 T 后仍只接到相应界；一般 K 通过撤掉 B\K 的预载并视作内部机器得到同一结论。该证明使用两份**实际** schedule，而不是一个分数点或未知 optimum。

加权预算的反证只用算法界和真实 `mu` 的定义：若总和小于 `2k-1`，设 `d_i=2-mu_i/T`，归一化后取 `beta_i=d_i+(1-D)/k`，算法便输出小于某个真实 `mu_i` 的调度，矛盾。这里 `mu` 只在存在性证明中出现，程序不需计算它。

## 3.3 锐例、零边界和不能外推之处

加权星任务 `j_i` 在 a 上耗时 `omega_i T`、在 b_i 上耗时 T，展示整个预算等号面；零任务、空集合、额外有限端、单可用任务和 T=0 均在声明域内单列。满二叉树缺一实例展示每个 `nu_i=3T/2`，而“每个缺一都接近二”在该接口不可能，因为两两预算和限制最多一个超过三半。

正文还给出三个输出上的控制反例：两个任务分别 `(a:1/4,b_1:1)`、`(a:3/4,b_2:1)`、第三输出无基础任务时，三个缺一最优值为 `5/4,7/4,1`，说明不能把三半界改成所有缺一状态都不大于三半或都接近二。该障碍不是一般近二困难性；改变外部容量、状态资格或读出合同可能绕开它。

# 4. 两源比较、既有结果关系与第三阶段用途

1. **弱 H2 与强行矩：** 弱源的伪矩在同一一阶 CONFIG 投影下接近二，缺口来自 CONFIG 未共享同机二阶；同源强校准证明在该族把二阶共享变成条件容量，阈值正好为真实 OPT。这是同一实例族的合同边界，不是两个独立 gap 可相加。
2. **扇出与弱 H2：** 扇出源需要两份真实 YES 调度和显式预载，输出为实际 schedule；弱 H2 源只有共同形式证书，且其配置行没有二阶相容性。不能用扇出闭包算法修复弱 H2，也不能用弱 H2 证书冒充两份实际见证。
3. **与稀释星/配置对象：** 弱源实例来自中心—全局—资源的稀释星，强同机二阶正面阈值是对该对象的精确校准；需保留其“只在该族”的量词。与三选深树和固定阶强矩文稿的关系是条件接口关系，不应把不同的任务域和矩阶混合。
4. **与已有扇出/三外接审查：** 当前 `9b272` 的加权 `beta` 闭包和缺一三半是对三外接选择器/单输出预载边界的扩展；旧三外接正文保留 sharp `3/2`，本页新增的是加权预算面、任意 K 的总和不等式和“最多一个超三半”反例。与两份 YES 的结构域一致，但不提供从任意 UM 输入产生 YES 见证的算法。

第三阶段关系图可记录：

- `弱一阶 CONFIG + 全局四阶矩` → `同机二阶未共享` → `趋二伪证书`；
- `同机二阶共享` → `M2 PSD 条件容量` → `该稀释星族阈值=OPT`；
- `两份实际 YES + 加权闭包` → `某一缺一状态的实际 (2-beta)T` → `总和/三半预算边界`。

这些边必须标明“特定合同/特定实例族/有两个见证”的限定，不能从旧图摘要直接导入为全局关系。

# 5. 证据层级、开放义务与逐源处置

**一般证明：** 弱 H2 稀释星族 `OPT=2-1/k`、fractional multislice PSD、同一一阶 CONFIG、趋二比值；强同机二阶共享在该族的条件容量引理和阈值精确性；加权闭包算法、`sum mu <=(2k-1)T`、缺一两两预算和满二叉树 `3T/2` 锐例。上述量词不依赖有限枚举。

**有限精确证据：** 弱 H2 验证器的小 `m,N` Bareiss PSD、`k=2,b=2` fixture、有限端 CONFIG/负 pair/负 triple 检查，以及扇出来源列出的确定性 Fraction 代码和控制实例。有限审计不能扩大任意 `k`、任意扇出、一般强 H2 或复杂度结论。

**保留的障碍：** 弱证书不满足共享同机二阶，强合同不能由弱点免费升级；扇出算法不生成未知 YES，且单外层预载结构不能把每个缺一状态都做成近二。保留 T=0、空任务、零时间、额外资格、单可用任务等边界，避免把它们误删为“非典型”。

**未闭义务：** 没有一般强 H2 的 gap/舍入算法、没有从一阶或弱矩证书构造两份实际 YES、没有改变二阶后统一舍入的误差定理，也没有 UM-TARGET-v1 或 NP-hardness 结论。后续若研究，先明确需要真实 schedule 见证还是允许只改动全局二阶，并写出同机容量和任务覆盖量词。

逐源处置：

- `6a55a2b4d6d9bbb39e0f`：`integrated`。弱 H2 参数族、multislice PSD、CONFIG 一阶相容、强同机二阶精确校准和有限证据边界写入第 2、4、5 节。
- `9b272a005d864cfa241d`：`integrated`。加权闭包算法、加权总预算、缺一三半、加权星等号族、满二叉树锐例和控制反例写入第 3、4、5 节。

两源均为全文件实读、相关正文/审查/程序/证据已比较；独有内容去向和不能合并的理由已在第 4 节明确。
