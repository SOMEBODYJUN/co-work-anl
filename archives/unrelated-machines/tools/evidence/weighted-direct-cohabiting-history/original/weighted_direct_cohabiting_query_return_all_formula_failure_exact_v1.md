# 异权直接共居查询—返回接口的全公式三半逃逸：Exact v1

ID/version：`UM-WEIGHTED-DIRECT-COHABITING-QUERY-RETURN-ALL-FORMULA-FAILURE-v1`。

作者 rainbow，2026-10-18。本文件只冻结明确原矩阵与精确量词结论，不含作者证明，供独立 Exact-first 审查；仅写 clone 外 scratch，不修改 repo / Work / Git。

## 1. 来源扣除与本次改变的对象

本作者已实际读 `medium_cohabiting_pair_sensor_failure_exact_v1.md`（SHA256 `8265815f23cf4bef20ac0f84c3848e1e4e7171596c292d241181c35a94f7ad1b`）及 current `near_unit_implication_pcsp_and_physical_copy_obligation.md` §9。

旧 medium pair-sensor 每索引有 M_i,C_i,D_i 及 q_i,b_i,h_i；q_i@C_i=e、h_i@C_i=1−e、h_i@D_i=1、u_c@D_i=1，证明具体全公式≤1+e。旧 §9 则另有公共 R_c，q_i 的 clause 端为 unit，给全公式 strict matching。二者的原对象与结论不被本文件改写。

本 Claim 是另一套**直接**共居桥：只保 M_i、C_i；没有 h_i、D_i、公共 R_c，clause 原 job u_c 直接在 C_i 执行。q_i 与 u_c 的 C_i 时间可以逐 occurrence 任意不对称，只要求正且和≤1。这改变了真实有限矩阵及量词，不称旧 pair-sensor 同一输入上的加强，也不并入 machine-uniform query/return 交换 v2。

## 2. 源、参数、padding 与全部真实原资格

输入任意显式有限 CNF Φ，每个 clause c 有 k_c≥2 枚实际 literal occurrences；允许同 clause 重复文字、重复变量，亦允许不同 clauses 重复。每枚 occurrence 只属于它所在的一个 clause。空公式允许，但空 clause、unit clause 不在本域。只保实际出现的变量。

每变量将其 occurrences 任意排序成环，若少于3枚则补 dummy 到环长至少3，dummy 不属于任何 clause、polarity 任取。所有 occurrences 含 dummy 总数 N，原 clauses 数 m，真实 occurrences 数 L=Σ_c k_c。用最少必要 padding 时 N≤L+2v，其中 v 是实际出现的变量数；也可把更长 dummy 表显式列入输入并按其实际 N 计规模，不承诺隐式指数 padding 的 source 多项式。

同变量环的后继为 i^+，polarity s_i∈{0,1}（正文字0、负文字1），pin(i)=M_i 当 s_i=0，pin(i)=M_{i^+} 当 s_i=1。给有理 1/2<ρ<1。对每真实 i∈c，给正二进制有理 x_i、y_i，满足

    x_i>0，y_i>0，x_i+y_i≤1。

不要求同一 clause、同一变量或不同 occurrences 的 x_i / y_i 相同。对 dummy 固定 x_i=1，无 y_i。所有有限时间均≤1。若另给希望保护的弱阈值 B∈[1,2)，可额外选 ρ>B/2；结论全公式三半上界本身不需要 B。

若 m=0，则 L=N=0，输出一台 idle 原机器、零 jobs；其实际 OPT=0。若 m>0，机器为每索引两台互异原机器 M_i、C_i（共2N≥1），全部 jobs 为每索引两件不同 q_i,b_i，加每 clause 一件不同 u_c（共2N+m）。下列端且仅这些端有限，其余∞：

| 原 job | 所有真实有限端与时间 |
| --- | --- |
| q_i | M_i:ρ；M_{i^+}:1；C_i:x_i（dummy 时 x_i=1） |
| b_i | pin(i):ρ；C_i:1 |
| u_c | 对每个真实 i∈c，C_i:y_i |

没有预载、免费关系、其它 jobs 或新 state；每件原任务只可整件执行一次。机器 C_i 上不同原任务的时间明确允许不同，不能把它化为 unit 或统一 slot 匹配后忘记真实共居负载。

## 3. 严格身份合同：这确实是一个完整 strict SAT 桥

对每个上述 Φ 与任意合法参数：

1. 从任意 Φ 的满足赋值，可确定性总位多项式构造全部原 jobs 的完整实际峰≤1 调度。每 clause 选一个满足文字 i，使 q_i@C_i、b_i@pin(i)、u_c@C_i；q_i 与 u_c 是两件原任务，实际共居成本 x_i+y_i≤1。
2. 反向任意峰≤1 的完整原调度，均可确定性总位多项式解码 Φ 的满足赋值；特别，非空 Φ 的 strict≤1 可行当且仅当 SAT。允许 dummy 的读出和返回，但不能把它们用作 clause 选择。

反向的承重身份结论也作为本 Exact 的一部分：在任意 strict 调度中，每台 M_i 恰执行一件原 q 或 b；对每个真实或 dummy i，q_i@C_i 当且仅当 b_i@pin(i)。每 clause 的 u_c 只能在这样一个同编号 q_i@C_i 的真实 occurrence 处执行。每变量的有效 cycle edges 因而有同一方向 z∈{0,1}，所有返回 b_i 的 s_i 都等于该 z；可据此给一致变量赋值。没有将同编号返回作为额外物理假设。

这只说明此明确候选在严格端保源，不声称 near-2 soundness。固定 SAT 的严格可行性不被升级为任意接近2的计算困难性。

## 4. 主失败结论：对所有公式都有完整 actual≤3/2

无论 Φ 是否可满足、对所有上述任意异权 x_i,y_i、任意环排序和 dummy polarity，存在且可确定性总位多项式输出全部原 jobs 的完整实际 τ，使

    C_max(τ)≤3/2。

空公式返回第2节的 idle 空调度。非空输出还可以同时满足以下更具体的物理分支合同。

定义 baseline clauses

    C_0={c:存在 i∈c 使 y_i≤1/2}，

其余为 active clauses C_1。每个 c∈C_1 都有全部 y_i>1/2，故全部 x_i<1/2。

- Baseline clause c：可以选一个 y_i≤1/2 的真实 i，放 u_c@C_i；该 clause 全部 b_j 留自身 C_j，全部 q_j 使用环内原端，不导出到 C_j。因此 u_c 是加在原 b_i 的 unit 上，实际合计1+y_i≤3/2；没有删除 baseline 的 q/b/u 原 jobs。
- Active clause c：可以选一枚真实 query 索引 j(c) 与一枚真实 return 索引 r(c)，二者允许不同，使该 clause 恰 q_{j(c)} 导出到自身 C_{j(c)}，恰 b_{r(c)} 返回自身 pin(r(c))，其余 q 用环内原端、其余 b 留自身 C；原 u_c 放 C_{r(c)}。选择的 return pins 在所有 active clauses 间互异，且可同时安排环内全部 jobs，使每台 M_i 恰一件、负载≤1。
- Dummy q_i 全部使用环内原端，dummy b_i 全部留 C_i。

Active 的 j(c)≠r(c) 时，query C_{j(c)} 上可能真实共居 q_{j(c)} 与 b_{j(c)}，成本1+x_{j(c)}<3/2；return C_{r(c)} 只有 u_c，成本 y_{r(c)}≤1。两索引相等时，该 C 上为两件原 q+u，成本≤1。其余 C_i 负载≤1，baseline 已逐机计入 u_c。全部 M_i / C_i / 原 jobs 在一个共同实际分配内受控，不是逐机分别挑见证。

该构造可在辅助的二部匹配图中使用分析性 virtual labels，但它们不是本原 P 的机器或任务，不能作为实际执行端输出。最终每个原 job 的实际目的地必须是第2节列出的原有限资格；全部 baseline q/b/u 也必须恢复。

因此此候选虽然 strict 端确实保同编号与 SAT，却在每个源 NO 都已有≤3/2 的全原任务逃逸。不能借逐 incidence 的权重、同机异权共居或让单个 q_i 变成 small query，把这一具体桥升级为任意小 δ 的 YES1 / NO近2 source。

## 5. 显式总位复杂度与范围

非空原 P 有2N机器、2N+m原 jobs、5N+L有限条目。按完整 dense 矩阵输出时有2N(2N+m)项；不能省略这个成本。ρ、x_i、y_i 均按原输入二进制有理记录，dummy x_i=1 为常数。满足赋值映射、strict 实际解码、baseline / active 分类、共同整数匹配及全部原机负载回算均按这份显式输入总位长多项式，不按 1/x_i、1/y_i、1/ρ 或分母数值展开。

这里借用的普通匹配 / 旧保护环 OR 共同证书是既有技术，不称新的匹配定理或新 source hardness。具体增量是这套改动后的 direct co-location 矩阵、任意 occurrence-dependent 非对称正权、baseline/active 混合分支与完整实际三半失败。没有一般 medium 查询接口不可能性、一般 UM 算法或所有复制机制不可能性；也不以单个有限数例承担全公式证明。

本文件未含作者 Proof、软件或有限优化证据；未认证全球新颖性、外审或独立成文价值。真实 source gap 与 UM-TARGET-v1 保持 OPEN。
