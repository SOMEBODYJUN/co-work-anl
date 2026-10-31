# 共享外端 small-query／return-pool：Exact-only 全模式审查

对象：`shared_outside_small_query_return_pool_exact_v1.md`。2026-10-18，独立 Exact-first 审查；未读同名 Proof、作者策略、其它 agent 记录或后续交换推导。仅新建 scratch 文件。

## 实际源与结论

实际读取：`/workspace/scratch/038d9dcc4cac/shared_outside_small_query_return_pool_exact_v1.md`。

字节数 4,987；实际核 SHA256：

`37304837169ba1e11595c9681528dfe21efe2ccf8a04e6bafc73b7c2b8cf2e4e`。

**PASS；未发现 fatal。** 对全部 k>=2、显式 positive rational a_i 且总和至多1、所有 S,T 子集，精确 pattern optimum 确为1 iff `empty != T subseteq S`，否则为2。独立证明处理全部原 jobs、任意 pool 分配、多query、多return、空集、阈值等号及总位复杂度，不把 pool 容量1当作输入硬约束。

本例只认证标准 unit pool 与共享外端得到的 small-query containment 接口。没有认证新的 source、变量一致性、一般外接、near-2 hardness 或 matching 新颖性。

## 1. 任意完整 assignment 的精确负载公式

每 q_i 的实际目的地决定 S：i在S则 q_i 在 H，否则在 E_i。每 b_i 的实际目的地决定 T：i在T则 b_i 在 E_i，否则在某个 P_r。对 pool 内的 indices `i notin T`，令其实际 pool 选择为 `rho(i) in {1,...,k-1}`。于是

\[
\begin{aligned}
L_H&=\sum_{i\in S}a_i\le1,\\
L_{E_i}&=\mathbf1_{i\notin S}+\mathbf1_{i\in T},\\
L_{P_r}&=|\{i\notin T:\rho(i)=r\}|.
\end{aligned}
\tag{1}
\]

这覆盖每一合法完整 assignment：S、T 任意，rho 任意，不预设匹配或一机一件。每个原 job 恰执行一次、资格及时间精确来自原矩阵。所有外端 E_i 的 q_i/b_i 真实共机负载完整计入。

每份完整 assignment 均有 C>=1，因为 k枚 b jobs 中至少一枚实际执行且所有 eligible 时间都是1。H 峰至多1，所以 C 实际是一个至少1的整数，由外端1/2和 pool 的整数负载决定；它不必只为1或2，差的 pool 分配可给3乃至k。

## 2. 所有 C<2 调度必满足非空 containment，并且已峰1

先取任意实际完整 assignment，不以 S,T 的关系为前提，假设其 C<2。

每 P_r 上都是 unit b jobs，所以每台至多一件。这是低峰推出来的结论，而非模型免费容量。pool 返回数因此满足

\[
k-|T|\le k-1,
\]

即 `T!=empty`。其次，若某 i 同时属于 T 且不在 S，则 q_i、b_i 都实际在 E_i，两件 unit jobs 给负载2，矛盾。所以 `T subseteq S`。

在这个实际 assignment 中，每 E_i 至多1、每 P_r 至多1，而 H 本来总量至多1。因此 C<=1，配合 b-job 下界得 **C=1**。没有未覆盖的中间负载或非指定 partial pattern。

因此任意 `1<=B<2` 的实际弱调度必满足关系且已经峰1。若 B<1，没有完整实际调度。这里“实际”限定不可删：只有知道这份 rho 的实际峰低于2，才可以断言它的 pool 分配没有碰撞。

## 3. 关系成立时的确定性峰1 witness

给任意 S,T，满足 `empty != T subseteq S`。先按定义放所有 queries 和 outside returns。剩余 `k-|T|<=k-1` 枚 b jobs，按输入索引递增顺序逐个放到不同的 `P_1,...,P_{k-|T|}`。

所有2k件原 jobs 均被安排。H 总量<=1；T subseteq S 保证每 E_i 至多一件 unit job；每 pool machine 至多一件。故峰<=1；b-job 下界使精确峰1。得到 `OPT(S,T)=1`。

**量词区别：** 好的 S,T 只保证存在这个最佳 pool 分配，不保证相同 pattern 的每份 rho 都弱。例 k=3、`S=T={1}`，若把 b_2,b_3 同放 P_1，这份合法完整 assignment 的峰为2，虽然该 pattern 的 optimum 是1。这不反驳 Exact；Exact 正确区分了 pattern 最优值和实际弱调度。

## 4. 所有坏 patterns 的精确下界2和共同上界2

若 `T not subseteq S`，某 E_i 的两件 unit jobs 被 pattern 强制同时执行，任意 rho 都给 C>=2。

若 T为空，则全部 k 枚 unit returns 必在 k-1 台 pool machines。普通 UM 允许它们共居，但 pigeonhole 保证至少一台有两件，任意 rho 都有 C>=2。这包含 S为空的 inactive，也包含任意非空 S：把 queries 移进 H 不增加 pool 台数。

这两种情形恰是关系失败的全部情况。

对任意 S,T，均可构造 peak<=2：按模式放 q_i 和 outside b_i；枚举 m=k-|T| 枚 pool returns，前 min(m,k-1) 枚分别放不同 pool machines；若还有最后一枚（只可能 m=k），把它放 P_1。此时所有 P_r 至多2；每 E_i 最多两件；H<=1。k>=2 保证 P_1 存在，全部2k jobs都有有限合法目的地。因此每坏 pattern 的 exact optimum 是2，不是仅一个下界。

以上证明无需列举 `2^(2k)` 个 S,T，也没有遗漏非singleton queries/returns。

## 5. 空集、singleton 和阈值等号

- `S=T={i}` 是好的 aligned_i，精确峰1，构造包含所有其它 k-1 枚 queries 的 outside 负载和全部 k-1 枚 returns 的 pool 负载。
- `S=T=empty` 是 inactive，k枚 returns 挤 pool，精确峰2。
- `S={j},T={i},i!=j` 在 E_i 有 q_i+b_i 双 unit，精确峰2。
- `S=empty,T!=empty` 总违反 containment，峰最小2；T为空而 S 任意也最小2。所以零query或零return均已覆盖。
- `S=T=[k]` 有全部 small queries 真正共居 H、全部 returns 在不同 E_i，峰1。这说明孤立模块的无约束真实 OPT恒为1，没有 source NO。
- `1<=B<2` 只接纳实际峰1调度。等号 `B=2` 时，每一 S,T 都至少有一个合法 witness；坏 patterns 全部不再被排除。此时并不是所有 rho 均可接受：k>=3 时仍可把三枚以上 returns 塞入同一个 pool，给峰>2。
- 当 `0<delta<1` 取 `B=2-delta`，所有坏 pattern 的最小峰2严格大于 B，差值 delta，无需改变 a_i 或增删对象。普通 positive a_i 输入允许取 `a_i=1/k`，k件 queries 一起到 H 时质量恰1。

k=1 不在正式域且不能纳入：没有 pool machine，T为空会使 b_1无内部 eligible 目的地，pattern 并非总有有限调度。a_i 的正式正值域已保留；证明不借其数值下界或倒数进行复制。

## 6. 显式位复杂度和任务覆盖

机器数 `1+(k-1)+k=2k`；jobs 数2k。每 q_i 两个有限端共2k项，每 b_i 的 k-1 个 pool端加其 E_i 共k项，所以 finite entries 总数 `k^2+2k`；dense matrix有 `4k^2` 项。input列出 k个有理 a_i，故其长度至少Omega(k)，quadratic eligibility 构造仍是显式输入长度多项式。

正/坏模式 witnesses 只作一次索引扫描，给每一原 job 一个具体机器。实际 load 解码扫描给定 destinations，按(1)计算所有2k台原机负载；也可同时验证没有漏 job、重复 job或非法资格。pool 分配不需要求未知 matching 或输入 optimum witness。

有理总和的 numerator/denominator 编码增长至多为输入分子分母位长之和加多项式log项，精确检查 `sum_i a_i<=1` 及所有负载比较为总位多项式。没有按分母、`1/a_i`、`1/delta` 或隐式指数展开。给出或检查单一 S,T 时无需枚举所有 patterns。

## 7. 规范 scope

合同只给至少一件具体 b_i 返回 outside，且每件返回保证同索引 q_i 在 H。它不强制 S=T、singleton S/T，也不保证每件内部 q 都返回其 b。H 的多query共居已在真实 total load 中，而 E_i 不可私有化。

不能把这个恒OPT1的孤立接口升级成 source soundness、多个 occurrences 的全局 truth/label 一致性、任意 E_i 同一化、额外 query outside资格或任意实际 clause 任务的读取保证。任何此类新矩阵都要重证全任务 YES 与任意低峰调度的解码。本文没有反驳一个仅保证内部替换的 machine-uniform localA 理论，也不提供一般 UM 算法或 near-2 hardness。

有限辅助检查只可验证小参数；PASS 依据为上述任意k的完整负载与case proof。未读作者 Proof/策略、未给其它 agent 发送证明、未写 repo/Git/Work，源 Exact 保持原字节。
