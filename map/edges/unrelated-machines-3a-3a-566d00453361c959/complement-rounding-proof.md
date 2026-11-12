# 资源下界与作业上界的补基舍入等价

## 对象、输入和所用原文

本比较的两个完整算法接口是：

- `M-737cbc9ea3b54c03b847026018cf5b19`：restricted resource-matroid Santa Claus 的给定可行 assignment LP 点、共同下界 T，可多项式舍入为整数分配，最小值至少 T−max_j v_j。
- `M-0a576e4d0f4647d18173160e6cbaad70`：restricted job-matroid makespan 的给定可行 assignment LP 点、共同上界 T，可多项式舍入为整数调度，最大负载至多 T+max_j p_j，并由此得到2近似。

两端均采用 BLMRS arXiv:2307.08453v1 的 Definition 7/8。非空有限玩家/机器集上的每个资源或作业 j 选给定整数 polymatroid P_j 的一个 basis，值或尺寸 s_j 是各玩家/机器共同的有限非负有理数。整数 rank function 以 value oracle 给出，数值和有理输入使用二进制编码。分数 basis 指整数基凸包中的点。任意有限种公共值均适用，空项集约定最大项值为零。

已对照 `research/registration/batches/register-ab98f323ad-0104.json` 的 v1 合同与当前 v2 登记，并实读冻结 PDF 的 polymatroid/dual 定义、Definition 7/8、Proposition 9、assignment LP、Theorems 21/23 和 Lemma 22，以及当前 §5 与新增必要证据 `archives/unrelated-machines/tools/evidence/boss2-6405-blmrs-proof/rounding-slots-and-dual.md`。冻结 v1 的 floor/ceil 两相邻索引图在十玩家四项均匀拟阵实例上缺少所声称的分数见证。当前结论由新增证据中的压缩单位槽、两秩交整数性、原资源补基及常向量对偶证明。下文先给一对一的常向量变换，再保留旧任务逐玩家单点上界和私有补偿的构造。

## 补基恒等式

令共同玩家/机器底集为 E。P_j 的非负、单调、规范化整数 rank function 为 f_j。取任一满足 z_j(i)≥f_j({i}) 的整数向量 z_j，定义

    g_j(S)=z_j(S)+f_j(E\S)−f_j(E),
    Q_j=P(g_j).

z_j 支配 P_j 全部独立向量。g_j 规范化、整数且子模。增加 i 时的边际为 z_j(i)−[f_j(A)−f_j(A\{i})]≥0，其中 A 为增加 i 前的补集，故 g_j 单调且非负。这是原 PDF 的 polymatroid dual。

有严格的基集合恒等式

    B(Q_j)={z_j−b:b∈B(P_j)}.

证明：若 b 为 P_j 的基，则 z_j−b≥0，总和为 g_j(E)，并且对任意 S，

    (z_j−b)(S)=z_j(S)+b(E\S)−f_j(E)≤g_j(S).

反之，若 a∈B(Q_j)，由 a(i)≤g_j({i})≤z_j(i) 得 z_j−a≥0；用 a(E)=g_j(E) 和 a(E\S)≤g_j(E\S) 得 (z_j−a)(S)≤f_j(S)，总和为 f_j(E)。故 z_j−a∈B(P_j)。同一仿射恒等式也对两个基凸包成立。因此给定分数 x_j，可以在不改变原项身份的情况下取分数补基 y_j=z_j−x_j，整数舍入后再取补基解码回原项。

## 常向量给出一对一的双向舍入

按新增必要证据 §3，逐项取 K_j=f_j(E) 与 z_j=K_j·1_E。由 f_j 单调性知 z_j(i)≥f_j({i})，故上一节恒等式适用。令 C=Σ_j s_j K_j，s=max_j s_j。每个原项 j 与一个公共值或尺寸相同的对偶项配对。任一分数或整数基配置 x 与其补基 y 都满足

    Σ_j s_j y_j(i)=C−Σ_j s_j x_j(i)   (i∈E).

**资源减最大舍入推出作业加最大舍入。** 对给定作业分数基 x，令 L_i=Σ_j p_j x_j(i)≤T。对偶资源的分数价值 C−L_i 同时非负且至少 C−T，所以可在共同阈值 τ=max(0,C−T) 调用资源舍入。获得对偶整数基 a 后取原作业整数基 b_j=z_j−a_j，各机负载至多 C−τ+s≤T+s。

**作业加最大舍入推出资源减最大舍入。** 对给定资源分数基 x，令 V_i=Σ_j v_j x_j(i)≥T。因为 V_i≤C，对偶分数基在共同作业阈值 C−T≥0 下可行。获得对偶整数基 a 后取原资源整数基 b_j=z_j−a_j，每人价值至少 C−(C−T+s)=T−s。

每个对偶秩 oracle 用一次原秩 oracle 和二进制整数运算。C、阈值及各基坐标的编码长度均为原输入与原秩输出位长的多项式。两方向保持每个原项及其完整基，最大项值不变。空项或所有值为零时可直接输出各原基。上述推导适用于任意给定可行分数基见证，包含 T≥C 的作业输入。

## 单点上界和私有补偿的原构造

旧任务取较紧的坐标上界 z_j(i)=f_j({i})。此时各坐标的补基常数可以不同，需把它们统一成一个阈值。

记

    s=max_j s_j,
    C_i=Σ_j s_j z_j(i),
    C=max_i C_i,
    D_i=C−C_i≥0.

若 s=0，任取各原 polymatroid 的整数基，两种接口均立即成立。以下假设 s>0。把 D_i 写成

    D_i=q_i s+r_i,
    q_i=floor(D_i/s),  0≤r_i<s.

为每个 i 加至多两个确定性私有辅助项：值/尺寸 s、rank function q_i·1_{i∈S} 的项；以及值/尺寸 r_i、rank function 1_{i∈S} 的项。零项可略去。这两个基分别被强制为 q_i e_i 和 e_i，因此无论舍入算法如何选择，玩家/机器 i 从辅助项得到的值/负载恰好是 D_i，其他玩家/机器得到零。所有辅助项值≤s。

这里 q_i 用一个 polymatroid 的二进制 rank 表示，不把它展开为 q_i 个独立资源。每个原 rank oracle 增加多项式次查询即得 z_j 和 g_j 的 oracle；D_i、q_i、r_i 的位长均为原有理输入及 rank 输出位长的多项式。辅助项总数≤2|E|，所以这不是伪多项式展开。

### 资源减最大舍入推出作业加最大舍入

给定原 job-matroid LP 可行点 x，设 L_i=Σ_j p_j x_j(i)≤T，取上节 s_j=p_j。若 T≥C，则任取各 P_j 的整数基 b_j，都有 Σ_j p_j b_j(i)≤C_i≤C≤T，已完成目标。否则 C−T>0。

以 Q_j 为资源 polymatroid，以 p_j 为资源值，取分数 y_j=z_j−x_j，再加入上述确定性私有辅助资源。每个玩家 i 的总分数值为

    Σ_j p_j y_j(i)+D_i=C_i−L_i+C−C_i=C−L_i≥C−T.

故这是资源端共同阈值 T'=C−T 的合法给定分数见证，且最大资源值≤s。调用资源减最大舍入，得到每个玩家总整数值≥C−T−s。移除确定性辅助资源后，原 Q_j 资源的整数值≥C_i−T−s。令 b_j=z_j−a_j，其中 a_j 是原 Q_j 资源舍入后的基。补基恒等式保证每个 b_j 恰为原 P_j 的整数基；其机器负载满足

    Σ_j p_j b_j(i)=C_i−Σ_j p_j a_j(i)≤T+s.

辅助项只在归约内部出现，最终输出逐个保留原作业及其原 basis 合同；没有丢弃或拆分原任务。于是得到整个作业加最大舍入目标，而不是某一步的局部贡献。

### 作业加最大舍入推出资源减最大舍入

给定原 resource-matroid LP 可行点 x，设 V_i=Σ_j v_j x_j(i)≥T，取 s_j=v_j。由于 x_j(i)≤z_j(i)，有 T≤V_i≤C_i≤C，故共同作业阈值 T'=C−T 非负。

以 Q_j 为作业 polymatroid，以 v_j 为作业尺寸，分数 y_j=z_j−x_j，并加入同样的确定性私有辅助作业。机器 i 的总分数负载为

    Σ_j v_j y_j(i)+D_i=C−V_i≤C−T.

调用作业加最大舍入，得到各机器总负载≤C−T+s。扣除固定辅助负载 D_i 后，原 Q_j 作业负载≤C_i−T+s。取整数补基 b_j=z_j−a_j∈B(P_j)，原资源分配的每个玩家值为

    Σ_j v_j b_j(i)=C_i−Σ_j v_j a_j(i)≥T−s.

这支付整个资源减最大舍入接口。负的 T−s 仅表示下界弱，不影响非负合法分配或算法合同。

## 2近似的独立边界核对

对作业端，先暂时删除 f_j(E)=0 的惰性项，最后以唯一零基接回；所有项均惰性或所有活跃尺寸为零时，OPT=0，直接输出即可。其余令 s 是活跃作业的最大尺寸。每个活跃整数基的总重数至少1，故对每个活跃 j，任何整数调度都至少有一台机器收到该作业的一份，从而 OPT≥p_j，故 s≤OPT。

求 assignment LP 最优阈值 F≤OPT，然后对其可行分数点用上述舍入，得到 Cmax≤F+s≤2OPT。LP 的各作业子集秩约束可用次模最小化分离，基等式、非负性和负载约束可直接检查，故可在有理编码与秩 oracle 合同下多项式求解。这里 s≤OPT 来自整数基非零性。一个 rank-one 作业可在多台机器间分数分摊，给定阈值 T 可以小于其尺寸。删除 rank 零项后得到的 s 不大于原题 max_j p_j，故也保留原始给定点的 T+max_j p_j 保证。

所以两个当前登记接口在原整数 polymatroid value-oracle 域上多项式等价；两个方向均覆盖完整目标。没有对一般 unrelated-times、配置LP、SPE 或静态拟阵外包作额外结论。
