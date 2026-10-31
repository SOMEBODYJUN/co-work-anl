# 多见证互斥查询的共享任务收费与实际容量精确合同

这是给独立攻击者的 Exact-only 冻结陈述。这里不含证明，不声称源 decoder、标签复制、一般 UM 近似或困难性。

候选身份：`UM-MULTIWITNESS-SHARED-JOB-FEE-CAPACITY-v2`。

v1第7项遗漏K非空，空集令严格和式0<0错误；本v2只修复该量词，保留v1原冻结文件。

## 完整原矩阵与模式

给整数 p≥1，正有理数 0<a_r≤1、0<b_r≤1（r∈[p]）、0<c≤1，并要求

\[
c+\sum_{r=1}^p b_r\ge1.
\]

原机器为全部互异的 H_1,…,H_p、A_1,…,A_p、R、S，共 2p+2 台。原任务为全部互异的 q_1,…,q_p、x_1,…,x_p、f，共 2p+1 件。全部且仅下表端有限，未述端为∞：

| 原任务 | 初始端与时间 | 另一原端与时间 |
| --- | --- | --- |
| q_r | H_r:a_r | A_r:1 |
| x_r | A_r:1 | R:b_r |
| f | R:c | S:1 |

全部任务必须恰执行一次，没有预载、额外任务、状态相关资格或隐含容量。初态 σ₀ 为表中全部初始端。

对任意 K⊆[p]，pattern K 只规定：q_r 在 A_r iff r∈K；其余 q_r 固定于自己的 H_r。所有 x_r、f 可任意选各自合法端。记 B_K=Σ_(r∈K)b_r，pattern OPT_K 为所有此类完整实际调度的最小峰。

只给非查询任务收费：w_f=1，全部 w_(x_r)=0。费用是相对 σ₀ 的指定 owner 改派费，即 fee(τ)=1 当且仅当原 f 真正在 S 上执行，否则为0。它不是物理负载总量；c=1 时不是“新增 unit”费用，c<1 时是非unit→unit的指定改派费。

对有理阈值 1≤β<2，记 F_β(K) 为满足 pattern K 且 C_max≤β 的实际调度的最小费用；不存在这种调度时记为∞。所有阈值均为闭阈值 ≤β。

## 精确结论

对全部上述输入、所有 K 及 β：

1. 完整无约束原实例 OPT(P)=1，σ₀ 峰≤1。对每个 r，还有一份完整 actual σ_r，query 恰 q_r 改 owner，且峰≤1。
2. 每个子集模式的准确最优值为

\[
\boxed{\operatorname{OPT}_K
=\min\{2,\max\{1,B_K\}\}.}
\]

3. 每个子集模式在 β<2 的准确最小费用为

\[
\boxed{F_\beta(K)=
\begin{cases}
\infty,&B_K>\beta,\\
0,&c+B_K\le\beta,\\
1,&B_K\le\beta<c+B_K.
\end{cases}}
\]

特别地，K 在 strict1 可行 iff B_K≤1。

4. 单位共享汇流特例 b_r=c=1，p≥2：全部 p 个单查询各自有 strict1 actual；任意满足一个单查询模式且 C_max<2 的完整 actual，都必须真正改派同一原 f。因此各单查询费用均1、合计p，而非查询费用宇宙 W=Σ_(非query)w=1。任意 |K|≥2 的 pattern 精确 OPT_K=2；不存在把全部 p 查询移到指定新端的 strict1 actual。C_max≤2 时所有 pattern 都有 fee0 的完整 actual。a_r 可同时任意接近0。
5. 任意有理 1≤β<2，可取 b_r=1、β−1<c<1，使上述每个单查询在阈值β仍必费1；此时同一收费原 f 真正从一个非unit原端 c 迁往 unit 原端1。原P仍 OPT1。
6. 均匀容量 s 特例：给整数 1≤s≤p，令 b_r=1/s。则 pattern K strict1 可行 iff |K|≤s；在 β∈[1,2) 时

\[
F_\beta(K)=
\begin{cases}
\infty,&|K|>s\beta,\\
0,&|K|\le s(\beta-c),\\
1,&s(\beta-c)<|K|\le s\beta.
\end{cases}
\]

这是不取整实阈值与整数 |K| 的精确比较，不隐藏等号。s≥2 时任何单查询在 β≥3/2 均有 fee0 actual；s=1,c=1 时阈值精确2。
7. 更一般地，若一个非空 K strict1 可行，而其中每个单查询 r 在同一闭阈值β∈[1,2) 都必收费，则

\[
\boxed{|K|(\beta-c)<B_K\le1.}
\]

因而 β≥3/2、c≤1 时这样的 K 至多一个元素。该结论只约束本精确共享汇流构件；不声称一般网络的必要形式。

## 对象、算法、范围与旧资产区别

所有参数二进制有理，全部原资格显式。全部结论要求实际完整 σ，而非独立资源期望或匿名 unit presence。每个 finite 端和全部原任务已列出；允许 p 随输入增长。各达界 σ、pattern最优 σ 与费用最优 σ 都有确定性总位多项式输出，输出不展开分母数值。给定β及K时，“∞”仅是该明确pattern下的实际不可行性。

本构件有 p+1 份完整 strict actual；p≥2 的单位汇流特例缺少共同全开 strict actual。不能将双见证查询分离定理输入中免费的 σ₁ 换成“每个 query 各有一份 σ_r”。这正是本项区别；没有反驳该双见证定理。

旧 `weighted_fanout_profile_boundary.md` 的多输出星读取不同矩阵状态中的独立零/满预载，并给两份完整全端模式；本项在同一固定 P 中读取每枚 q_r 的实际 owner、同一 f 的实际改派及共享 R 上互斥的 unit x_r。没有开关预载，也不要求或提供全部 queries 同时全开 strict 模式。两类合同的读出和量词不同。

每个查询模式的源标签解释、查询可跨源测试复用、跨部件外接、源 NO 的任意低负载 actual 解码、无重复计算的费用预算，均未构造。这个 OPT1 的参数族不是 OPT gap、不是 SAT/Label-Cover reduction，也不是 `UM-TARGET-v1` 正面或反面。数学新颖性及独立论文价值未认证。
