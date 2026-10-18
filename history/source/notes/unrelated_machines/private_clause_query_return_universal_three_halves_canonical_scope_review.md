# 私有 clause 全公式三半上界：canonical 实读范围审查

日期：2026-10-18。审查者：fee_cascade_review。仅 scratch；未修改 repo、Work、Git、canonical 或旧记录。

## 1. 实读对象与认证范围

本次实际全文读取：

`/workspace/scratch/038d9dcc4cac/co-work-anl-boss11/research/current/unrelated_machines/general_weighted_private_clause_exchange_and_shared_outside_boundary.md`

实际 SHA256：`6074c7ee16c63404e09ad5fb11ed927c1594f91d58c79abd37469a0c58d92fd4`，匹配 root 解封给定值。

**本记录的正式 final/canonical 认证范围仅 §2–3，ID `UM-PRIVATE-CLAUSE-QUERY-RETURN-UNIVERSAL-THREE-HALVES-v1`。** §1 作为本结论局部依赖和背景已经实际读取，其对应 Exact 与作者 Proof 先前已审；不把本记录扩大为另一次 §1 主 scope。§4–5 随文件全文实际读取，但没有在本记录中独立认证其数学、例子或审查状态，也不借其正确性支撑 §2–3。

审查次序保留如下：

- 先仅据全局 Exact、局部交换 Exact 与旧 query-separation，独立重构 direct-coloring 局部路线及 N+h 全局匹配，形成 `private_clause_query_return_universal_three_halves_independent_review.md`，SHA256 `b114fc2e82b5d633bc971c6562a41d234a73ac1ae216364cde58743896246742`。
- root 解封后才实际全文读局部/全局两作者 Proof，形成 `private_clause_query_return_two_proofs_actual_read_after_review.md`，SHA256 `9d7fca1aed5b5dc31217fb4b627dc82cb3996103009fbb44f3d53da4acf1836b`。
- 现在才读取上述 canonical，并另冻本 scope 记录。两份旧记录本次再次实际核 hash，原字节未改。

## 2. §2 的对象与量词保持在已审域

canonical 保留了已冻结 Exact 的承重条件：T>0 有理、显式 CNF、每 clause 至少两枚物理 occurrence、每 occurrence 只属一 clause、重复变量/文字允许；各出现变量的 occurrence 环显式 padding 至至少三索引。N 含 padding，L 为真实 occurrence，d=N−L；额外 padding 按实际表计入输入，不按二进制数值免费展开。

原 jobs 是每索引的 q_i,b_i 及各 clause 的 A_c；原 machines 是各 ring M_i、各 H_c 和各 dummy 私有 D_i。H_c 两两私有，且与 ring/D 分离；A_c 两两不同，只在自身 H_c。每个真实 q/b 的内部资格均限自身 clause，时间可为任意非负有理、零或∞；大于 T 的有限未用端不影响见证或构造。实际所有 clause 需求 jobs 必须列入 A_c，没有隐形删去的需求。

q 的原外部资格恰两 ring 端，时长各在 [0,T]；真实 b 仅有按正负 polarity 指定的一个原 pin，时长在 [0,T]。Dummy q 只有两 ring 端，dummy b 仅其原 D_i:T，不能被误用于填 ring。其它资格为∞。这些条件足够且未被 canonical 放宽。

给定的 λ_(c,i) 是完整覆盖 A_c+q_i+(R_c\{b_i}) 的实际局部内部 assignment，不是全局 strict 源调度或共同 SAT 赋值。算法前提明确提供每个索引的合法见证。仅假设这些见证存在时，canonical 仅给实际 OPT≤3T/2 的存在结论，没有承诺搜索未知 strict 证书。空公式独立输出一 idle 原机和零 jobs，OPT=0；非空公式的计数不硬套于该分支。

因此 §2 的“任意源 SAT/UNSAT”量词只在这个完整模板和全部局部可选前提内，并未泛化为一般 UM 或一般 source 编译器。

## 3. §3 局部模式库不隐藏 inactive 判定

对各 λ 补上独占时间 T 的测试 outside，只是获得 §1 局部交换所需的两完整实际测试调度；测试机并非原 P 的 ring。遍历 ordered pairs 时观察算法实际返回的二选一结果：有一次 inactive 就保存 baseline；否则保存全部 cross，并以 λ 补对角项。这一定义不需要证明 active 的 inactive 不可行，也不调用一般异权可行性 oracle。k_c≥2 确保有序不同对非空。

保存的每个 H_c 模式都是一份同时控制所有 H_c machines 的实际 assignment，始终覆盖全部 A_c，边界 job 清单也精确符合其 query/return 模式。它们只使用原有限内部端。

§1 所用分析零端已经在先前 read-after 中正式核清：δ=0 是修改后的辅助实例事实，不是原时间 T wrapper 的 δ。恢复原局部 outside 时所有原 jobs 已补回。canonical §2–3 不再把这个私有 outside 的≤T负载免费当成真实 ring 的负载界，而另做共同匹配。

## 4. 真实 ring 容量由同一个匹配控制

§3 分析二部图两侧各 2N+h：左为全部原 q_i,b_i 与 active w_c；右为原 M_i、每索引 K_i 与 active V_c。q 无 K 边，dummy b 无 ring 边，w 只连本 clause 的 K；w/K/V 均不实际执行。

取 active θ_i=1/k_c≤1/2，其余零。q 在两个 ring 端的半份质量中，从 pin 扣 θ 再加到 V；真实 b 把 θ 补回同一原 pin，其余至 K；w 补各 K 的 θ。故所有左行恰一，各 ring 列仍为一，每 K 列为一，每 V 列为一；非负性来自 k_c≥2。这是同一个全局 fractional perfect matching，因而对任意左子集都有 Hall 容量不等式，确定性整数匹配即可得到共同选择。没有把这些分数质量当作处理时间或输出拆分 job。

整数匹配强制：baseline/dummy 的 K 只邻自身 b，故那些 b 留 K，相关 q 取 ring；active V 恰吸一 q_j；active w 恰占一个 K_r，其 b_r 被迫取 pin，其余 b 取 K。反向若另有 b 不取 K，就需要同 clause 第二个 w 补其 K，故不可能。各 active 恰一 query/return，j,r 可以相同也可以不同。

每个原 ring M 因完美匹配恰接一个原 q 或真实 b；所有 clauses 的返回 pin 与其它 q 的 ring destinations 已共同排好，没有按 clause 分别选看似空闲的 pin。重复 occurrence 使 pin 可以重合，但都在同一图中竞争容量，未被遗漏。该图与原独立记录 N+h 图的匹配保持消元/展开已于前一记录证明；canonical 采用 2N+h 不构成 scope 改动或原记录勘误。

## 5. 全部原 jobs、负载与计数

实际回填 baseline 的 A_c+R_c，active 的 A_c+q_j+(R_c\{b_r})，都采用各自完整保存的 H_c 模式。匹配 ring 的 q/b 在其原有限端执行；dummy b 回自身 D_i。逐 job 可核每 A 恰在自身 H，每真实 q/b 恰内部或 ring 二选一，dummy 两 jobs 各一次，覆盖原全部 2N+a（a=Σ|A_c|），没有测试 outside 或 w/K/V 留在输出。

所有 H_c 私有，故各已保存峰≤3T/2 同时成立。每个 ring 恰一件原 job，真实时长≤T，即使时长为零也不丢其 job 身份。每 D_i 恰自身 dummy b，时长 T。因此全部原机器的实际共同峰≤3T/2。内部时间零、实际外端时间零均无需除零或改变这个计数。

原 machine 数 N+H+d（H=Σ|H_c|）、job 数 2N+a、finite 条目 3N+E_int 正确：q 的两 ring 端计 2N，真实 b 单 pin 与 dummy b 单 D 合计 N，内部 finite 计 E_int。Dense 为 (N+H+d)(2N+a)，必须按完整显式输入收费。分析图和测试 wrapper 不计入原对象，却各为多项式额外构造。

局部调用至多 Σ k_c(k_c−1)≤L²，模式库与 2N+h 图规模多项式；θ 分母 k_c 的位长为 O(log k_c)。有理负载和、比较、匹配、最终原身份输出均按输入与给定证书总位长多项式，不按分母值、时间倒数或隐式 padding 展开。canonical 未承诺一般调度 solver，且本记录没有运行软件或枚举。

## 6. 结论与边界

**正式结论：上述实际 hash 的 canonical §2–3 在已审 Exact 域内正确闭合，未发现 fatal、原资格/job 遗漏、局部 outside 免费外接或隐藏 inactive oracle。** 实际上界确实涉及所有原 jobs 与所有原 machines，不只是内部投影或测试实例。

辅助跨网络、共享 H/jobs、非全索引 strict 可选、不同外部资格及多 query/return bundle 不在本次认证域。单纯加资格保留旧可行分配；新 guard 若完整纳入 clause 模式并维持所有前提，仍在其上界内。不能由此声称任何退出模板的修改已经足够，或一般 near-2 主目标已关闭。

此范围记录不认证 canonical §4–5，不读取其链接 reviewer 文件来冒称代审，不声称外审、全球新颖性或一般软件实现认证。旧独立与 read-after 记录保持原字节。
