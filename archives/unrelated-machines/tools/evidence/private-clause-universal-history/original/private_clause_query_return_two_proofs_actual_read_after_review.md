# 任意异权交换与私有 clause 全公式三半上界：两份作者 Proof actual-read-after

日期：2026-10-18。审查者：fee_cascade_review。仅 scratch 数学审查，不修改 repo、Work、Git 或旧来源；本记录不认证任何尚未解封的 canonical。

## 1. 实读对象、hash 与先后次序

本次已实际全文读取以下两份作者证明，并用 SHA256 核对实际字节：

1. `general_weighted_query_return_three_halves_exchange_proof_v1.md`
   - SHA256 `da8edbfcaaa481e7842947147ea4aa136a775aa1b5a0624ecff5297a57ddbedf`。
2. `private_clause_query_return_universal_three_halves_proof_v1.md`
   - SHA256 `4feceb7cc2bfff412cd3b7bd895838ce25da0727c62633bf9c0b8035362b697e`。

两者均匹配 root 解封消息给定的 hash。其分别对应已经先行实际读取的局部 Exact `bda34c6f0abcbbb3fafad8fbadbec8c2e89f940ddef8e3a8f6d9ab92b04cbd41`、全局 Exact `21b334eec1ca8af9e368604552d93dd5b36eff9b75738e97db07f7097035fd2c`。

原 statement/Exact-first 独立记录为：

`private_clause_query_return_universal_three_halves_independent_review.md`

本次再次核其实际 SHA256 为 `b114fc2e82b5d633bc971c6562a41d234a73ac1ae216364cde58743896246742`，原字节未改。该记录先独立闭合局部 direct coloring 和全局 N+h 图，再由 root 解封本次两 Proof。本记录明确是 proof-aware read-after，不冒充新的 blind review，也不把作者分析零端或 2N+h 图追记为先前已读。

结论：在上述两个冻结 Exact 的完整域与输入见证量词内，两份作者 Proof 均闭合，未发现数学 fatal、资格遗漏、原 job 遗漏或超出对象域的结论。作者局部辅助零端及全局 2N+h 图分别给出原独立证明的有效替代路线；它们不表明 b114 原记录有错。以下逐项说明。

## 2. 局部证明的分析零端确实合法

固定不同索引 i,j，令 A'=A∪(R\{b_i,b_j})。原两 aligned 完整调度在 H 的内部集合分别为 A'+b_j+q_i、A'+b_i+q_j。作者从第一份仅删除 q_i，因处理时间非负，余下 A'+b_j 的内部峰仍≤T。

分析实例 P* 的 job 清单恰为 A'∪{b_i,b_j,q_j}。A' 只保留两个原见证使用的内部端；b_i,q_j 保留第二见证的内部端；b_j 保留第一见证的内部端。所有保留时间均为原真实值。另设互异分析机器 Z_i,Z_j,Z_b，以零时间分别承接 b_i,q_j,b_j。

作者的 ρ0、ρ1 是同一个 P* 上的完整实际调度，而非两份不同子矩阵上的局部负载表：

- ρ0 内部 A'+b_j，b_i,q_j 在各自分析零端；
- ρ1 内部 A'+b_i+q_j，b_j 在其分析零端。

二者覆盖 P* 每个 job 恰一次且同时峰≤T。Q*={b_i,q_j} 的两枚 query 都确实改变 owner（Z 与 H 不交），所以均属于 D；其在 ρ0 的初态处理时间为零。故此 P* 中旧 query-separation 的每个 δ_q 确为 0，可直接得到峰≤3T/2 的两 single-query 输出与不交的非query改变支持。旧定理允许非负时间；这里不需要 strict positive 的 p 条件，也没有除零操作。

这里与 b114 原记录的区别必须保持准确：原记录在原 test wrapper 使用 outside 时间 T，那里两 query 的 δ 是 T，不能写成 0。原记录没有错误地这样调用定理，而是重用其染色论证，证明这两台旧 query outside 机无任何新端入流而永不触发，且 H 无残留 query。作者换为 P* 的零端后，δ=0 是另一个合法辅助实例的事实。两个论证的输出都只采用原内部已见端，并分别完整恢复原 outside，所得原结论一致。

## 3. 不交支持、内部模式与所有原 job 的恢复

b_j 是非query，且在 P* 中从 H 变到 Z_b。两非query支持互不相交，故至少一份输出不改变 b_j。选择该份后，A' 始终在 H，b_j 也在 H；两查询中只有被选择的那枚进入 H。因此内部清单恰为：

- 选 b_i：A'+b_j+b_i=A+R，inactive；
- 选 q_j：A'+b_j+q_j=A+(R\{b_i})+q_j，指定 mismatch(j,i)。

这使用的是具体 job 身份的不交支持，不是平均费用，也不是逐机分别选一份调度。所有 H 上负载来自同一份 τ*，同时≤3T/2。除 b_j 外的非query均属 A'，其两见证端都在 H，故不存在另一个被忽略的非query outside 输出。

最后在原完整 P 中，保留所选内部 assignments，将每个不在内部的原边界 job z 放回其原独占 O_z、真实时间 T。包括被分析性删除的 q_i、未列入 P* 的其它 Q、未内部化 query，均恢复而非遗失。每个原 A 一直在 H；原 R/Q 的清单逐项等于上述两模式。不同 O_z 物理独占且只执行自身 z，故原 outside≤T。无 Z 执行被当作原合法端，原全部 jobs 恰一次，原实际总峰≤3T/2。

若 inactive 在 3T/2 不可行，则构造只能返回所指定 mismatch。反方向需交换 i,j 重新调用，并非从同一输出自动读取。给齐全部 aligned 见证才得到可计算的所有 ordered-pair 模式库；仅假设它们存在时，只得相应存在命题，不据此寻找未知 strict 调度。对 B≥3T/2 的身份同步排除范围与其前提一致，不推出任意 source 的 strict 可选性。

空 A、内部零端、unused machines 均无碍。未用的 >T 端不会进入给定 strict 见证；算法只在两见证实际使用的原端之间选择。空 H 在 k≥2 的合法 aligned 前提下不可能，但不需要额外例外实现。P* 有 |A|+k+1 个 jobs、|H|+3 个 machines，计数正确；原 N=|A|+2k，故 |A|+k+1≤N。新分析端只有零常数，恢复原 outside 才用原 T。其位复杂度为显式原矩阵、T 与见证编码位长的多项式。

## 4. 全局模式库分类没有隐含 oracle

每个 clause 的分析测试 wrapper 仅用于满足局部定理的完整 strict 调度前提。真实局部 λ_ci 加上各边界的独占 T outside 可得到所需完整输入；这不是最终 ring 的负载证明。

按固定顺序运行所有 ordered pairs：一旦某次返回 inactive，就保存它并标 baseline；否则所有 ordered pairs 都实际返回指定 mismatch，连同原 aligned 对角项，得到任意 query j / return r 的全库。active 的定义并不声称其 inactive 不可行，因此没有隐藏的 inactive 可行性 oracle。k_c≥2 使所需有序对非空。

每个存储库条目在自身 H_c 上是同一完整内部 assignment，含所有 A_c，精确含所要求的 q/b 原 jobs。不同 H_c、A_c 私有是后续回填承重条件，不能省略。

## 5. 作者 2N+h 图与原 N+h 图的精确关系

作者图左侧是原 q_i、原 b_i、active w_c；右侧是原 M_i、每索引 K_i、active V_c。两侧均 2N+h。K/V/w 都是分析标签。真实 b 只能到自身 K 或原 pin，dummy b 只能到自身 K；q 只有原两 ring 端及其 active V 端，没有 K 端；w_c 只连本 clause 的 K。

作者的 θ_i=1/k_c≤1/2 使所有分数边非负。q 在 pin 端扣 θ_i，再由同编号 b_i 在该 pin 补回 θ_i，故每个原 ring column 的总质量仍恰为一。active K 收 (1−θ_i)+θ_i=1，baseline/dummy K 收一；V 收 Σ_i θ_i=1；所有左行也恰为一。由同一个完整 fractional perfect matching 对任意左子集求质量，得全部 Hall 不等式，而非只核整图总量。因此确定性整数 perfect matching 存在。

任一整数匹配中，baseline/dummy b_i 被自身孤立邻域 K_i 强制吸收。对一个 active clause，w_c 只能占一个 K_r，迫使 b_r 返回 pin。其余每个 K_i 都必须由自身 b_i 占据；反之若其它 b_i 返回 pin，其 K_i 就还需要第二个同 clause w，矛盾。故每个 active 恰一 return。V_c 只能匹配 q，故也恰一 query。所有 ring 机同时各匹配一枚原 q 或真实 b。

这是原独立记录 N+h 图的匹配保持消元展开，并非相矛盾的图规模声明：

1. 消去所有 baseline/dummy 的强制 b_i—K_i 对。
2. 每 active clause 的 {b_i,K_i,w_c} 子结构恰选择一 occurrence r 返回其 pin，其余 b_i 留 K。将该结构替换为原记录的单一左标签 B_c，允许它到各 occurrence 的 pin；把 V_c 记为原 C_c。
3. 剩下左 q_i+B_c、右 M_i+C_c，各 N+h。原 b/K 不再作为独立标签出现，是有效消元，不是删原调度 job。
4. 反向给定 N+h 图的整数匹配，若 B_c 匹配 pin，选其一条 occurrence 标签 r，扩展为 b_r→pin、w_c→K_r，其余 b_i→K_i；加回 baseline/dummy 强制对，即得到作者图整数匹配。

重复 literal/变量可能使多个 occurrences 同 pin。作者图保留各 b_i/K_i；压缩图可合并 B_c→pin 的同目的边，但须留一个原 occurrence 标签供上述扩展与模式库读取。原独立记录已有这一处理。两种图均不把虚拟标签作为原 P 的机器或 jobs。

## 6. 真 ring、dummy 与完整原对象核验

从作者同一整数匹配回填：baseline 内部 A_c+R_c；active 内部 A_c+q_j+(R_c\{b_r})；所选真实 b_r 在其原 pin，其余原 q 在各自匹配的原 ring 端。dummy q 在原 ring，dummy b 在自身原 D_i 时间 T。

逐原 job 核查：每个 A 在唯一 H；每真实 q 仅在 H 或 ring 二选一；每真实 b 仅在 H 或 pin 二选一；每 dummy 的两 job 各一次。总数恰 2N+a。没有任何分析 outside、Z、K、V 或 w 留在执行清单。每台 ring 恰一原 job，使用的是真实有限端，其真实时长≤T；这一步明确建立全局容量，不引用 wrapper 的免费 outside。各私有 H 同时≤3T/2；每 D_i 只有自身 dummy b，负载 T。因此实际完整峰≤3T/2。

该计数不要求真实外部时长等于 T，可为任意 [0,T]；零端仍被作为一件 indivisible job 匹配，保证了更强的至多一件容量。变量环至少三索引的既定域保证两 q ring 端的原结构；padding dummy 的限制也正确保留。重复 occurrence、内部任意异权/零、源 UNSAT 都不改变推导。

原实际数目仍是 machines N+H+d、jobs 2N+a、finite entries 3N+E_int。后者逐项为 q 的两原 ring 端 2N、真实 b 的单 pin 加 dummy b 的单 D 合计 N，以及内部 E_int；analysis 图和测试 wrapper 不计入原 P。dense 项也须按完整 (N+H+d)(2N+a) 读入。本证明未偷换为仅匹配边数的输入规模。

局部最多 Σ_c k_c(k_c−1)≤L² 次构造，存下的库为多项式规模；作者分析图各侧 2N+h，边数 O(N+L)，θ 的编码 O(log k_c)，最终只运行有限匹配和有理数部分和/比较。不存在按某个 p 的倒数、分母数值、T/p 或隐式 padding 展开。空公式的一台 idle 原机/零 jobs 分支单列，OPT=0，未把非空公式计数硬套于它。

## 7. 最终认证范围及未认证项

本次正式认可的是两份 Proof 在各自已冻结 Exact 域中的论证与显式输入算法/仅存在量词分离。无当前 fatal。原 b114 direct-coloring 与 N+h 路线继续有效，不需要覆盖或勘误。

全局结论依赖所有 real index 的 strict local aligned 可选、H/A 私有、单 q/单 b 模式、指定实际 q 双 ring 端和 b 单 pin。A 外送、跨 clause 共享 H/jobs、多 query/return bundles、缺局部索引或不同外部图均不在此认证域。局部恢复 outside 并未被免费当作真实 ring；全局图为其提供了独立容量证明。

本记录没有运行软件、枚举或认证一般 UM solver；不声称新 query-separation/Hall 技术、外审或全球新颖性，不据此宣布任意 near-2 source 已被排除。只实际读了上列两 Proof；未来 canonical 的正式 §§2–3 尚未读取或认证。
