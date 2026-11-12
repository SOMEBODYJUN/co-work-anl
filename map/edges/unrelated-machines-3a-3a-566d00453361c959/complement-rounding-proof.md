# 资源下界与作业上界的补基舍入等价

## 对象、输入和所用原文

本比较的两个完整算法接口是：

- `M-737cbc9ea3b54c03b847026018cf5b19`：restricted resource-matroid Santa Claus 的给定可行 assignment LP 点、共同下界 T，可多项式舍入为整数分配，最小值至少 T−max_j v_j。
- `M-0a576e4d0f4647d18173160e6cbaad70`：restricted job-matroid makespan 的给定可行 assignment LP 点、共同上界 T，可多项式舍入为整数调度，最大负载至多 T+max_j p_j，并由此得到2近似。

两端均采用 BLMRS arXiv:2307.08453v1 的 Definition 7/8：每个资源或作业 j 选给定整数 polymatroid P_j 的一个 basis；值或尺寸 s_j 为非负公共值，而不是依玩家/机器变化。有限整数 rank function 以 value oracle 给出，数值和有理输入使用二进制编码。分数 basis 指整数基凸包中的点。这里不引入一般 unrelated processing-time 矩阵，也不要求只有两种正值。

本次在两个端点的当前 v2 合同上重审。实际实读冻结原 PDF 的 polymatroid/dual 定义、Definition 7/8、Proposition 9、assignment LP、Theorems 21/23 和 Lemma 22，并完整实读新增必要证据 `archives/unrelated-machines/tools/evidence/boss2-6405-blmrs-proof/rounding-slots-and-dual.md`。冻结 v1 的 floor/ceil 两相邻索引图并未给出它们声称的分数见证，不能再把该图当作完整证明。当前端点的舍入结论由新增证据中的压缩单位槽、两秩交整数性、原资源补基及常向量对偶严格证明保留。本页的双向接口变换独立于原错误图；以下原有补基和私有补偿项证明仍逐式成立。因此本次修复的是证据路线和当前绑定，不改变已证明的等价数学身份。

## 补基恒等式与共同阈值的补偿

令共同玩家/机器地面集为 E。P_j 的非负、单调、规范化整数 rank function 为 f_j。定义

    z_j(i)=f_j({i}),
    g_j(S)=z_j(S)+f_j(E\S)−f_j(E),
    Q_j=P(g_j).

z_j 是支配 P_j 全部独立向量的整数上界，不能仅以 ceil(x_j(i)) 代替这个支配条件。g_j 规范化、整数且子模。其单点增量为 z_j(i)−[f_j(A)−f_j(A\{i})]≥0，故单调且非负。这个定义正是原PDF的 polymatroid dual。

有严格的基集合恒等式

    B(Q_j)={z_j−b:b∈B(P_j)}.

证明：若 b 为 P_j 的基，则 z_j−b≥0，总和为 g_j(E)，并且对任意 S，

    (z_j−b)(S)=z_j(S)+b(E\S)−f_j(E)≤g_j(S).

反之，若 a∈B(Q_j)，由 a(i)≤g_j({i})≤z_j(i) 得 z_j−a≥0；用 a(E)=g_j(E) 和 a(E\S)≤g_j(E\S) 得 (z_j−a)(S)≤f_j(S)，总和为 f_j(E)。故 z_j−a∈B(P_j)。同一仿射恒等式也对两个基凸包成立。因此给定分数 x_j，可以在不改变原项身份的情况下取分数补基 y_j=z_j−x_j，整数舍入后再取补基解码回原项。

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

## 资源减最大舍入推出作业加最大舍入

给定原 job-matroid LP 可行点 x，设 L_i=Σ_j p_j x_j(i)≤T，取上节 s_j=p_j。若 T≥C，则任取各 P_j 的整数基 b_j，都有 Σ_j p_j b_j(i)≤C_i≤C≤T，已完成目标。否则 C−T>0。

以 Q_j 为资源 polymatroid，以 p_j 为资源值，取分数 y_j=z_j−x_j，再加入上述确定性私有辅助资源。每个玩家 i 的总分数值为

    Σ_j p_j y_j(i)+D_i=C_i−L_i+C−C_i=C−L_i≥C−T.

故这是资源端共同阈值 T'=C−T 的合法给定分数见证，且最大资源值≤s。调用资源减最大舍入，得到每个玩家总整数值≥C−T−s。移除确定性辅助资源后，原 Q_j 资源的整数值≥C_i−T−s。令 b_j=z_j−a_j，其中 a_j 是原 Q_j 资源舍入后的基。补基恒等式保证每个 b_j 恰为原 P_j 的整数基；其机器负载满足

    Σ_j p_j b_j(i)=C_i−Σ_j p_j a_j(i)≤T+s.

辅助项只在归约内部出现，最终输出逐个保留原作业及其原 basis 合同；没有丢弃或拆分原任务。于是得到整个作业加最大舍入目标，而不是某一步的局部贡献。

## 作业加最大舍入推出资源减最大舍入

给定原 resource-matroid LP 可行点 x，设 V_i=Σ_j v_j x_j(i)≥T，取 s_j=v_j。由于 x_j(i)≤z_j(i)，有 T≤V_i≤C_i≤C，故共同作业阈值 T'=C−T 非负。

以 Q_j 为作业 polymatroid，以 v_j 为作业尺寸，分数 y_j=z_j−x_j，并加入同样的确定性私有辅助作业。机器 i 的总分数负载为

    Σ_j v_j y_j(i)+D_i=C−V_i≤C−T.

调用作业加最大舍入，得到各机器总负载≤C−T+s。扣除固定辅助负载 D_i 后，原 Q_j 作业负载≤C_i−T+s。取整数补基 b_j=z_j−a_j∈B(P_j)，原资源分配的每个玩家值为

    Σ_j v_j b_j(i)=C_i−Σ_j v_j a_j(i)≥T−s.

这支付整个资源减最大舍入接口。负的 T−s 仅表示下界弱，不影响非负合法分配或算法合同。

## 2近似的独立边界核对

对作业端，先暂时删除 f_j(E)=0 的惰性项，最后以唯一零基接回；所有项均惰性或所有活跃尺寸为零时，OPT=0，直接输出即可。其余令 s 是活跃作业的最大尺寸。每个活跃整数基的总重数至少1，故对每个活跃 j，任何整数调度都至少有一台机器收到该作业的一份，从而 OPT≥p_j，故 s≤OPT。

求 assignment LP 最优阈值 F≤OPT，然后对其可行分数点用上述舍入，得到 Cmax≤F+s≤2OPT。这里 s≤OPT 来自整数基非零性；绝不从给定分数阈值 T 推断 s≤T。一个rank-one作业可在多台机器间分数分摊，LP阈值完全可能小于其尺寸。删除rank零项后得到的 s 不大于原题 max_j p_j，故也保留原始给定点的 T+max_j p_j 保证。

所以两个当前登记接口在原整数 polymatroid value-oracle 域上多项式等价；两个方向均覆盖完整目标。没有对一般 unrelated-times、配置LP、SPE 或静态拟阵外包作额外结论。
