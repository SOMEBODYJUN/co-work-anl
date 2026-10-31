# Exact-only：tiny homes、一般 fallback 与额外共享 UD 叶的确定性 19/10

作者：/root/sol_general_repair，2026-10-18。新对象，pending Exact-first 独立攻击；不覆盖或改写先前38c/ce05输入域、证明或canonical。working note中的随机profile存在法不是本结论的确定性证明。本文件不给作者势函数、取整或算法证明。

## 1. 完整 typed 输入域

有任意正整数 k 个 outer groups O_i，k 是输入变量。每个 O_i 恰一个 indexed state，正支持为 homes g_j，j∈J_i，正二进制有理系数 w_j 总和为一。所有 (i,j) 的 homes 全局物理互异，且

    max_j w_j ≤ 1/(4096 k^4).

每 home g_j 恰一个 helper H_j，own indexed state 为该 home 的 unit singleton；所有其余 fallback indexed states 是公共有限资源集 B 上任意显式 normalized 非负二进制有理向量。B 与全部 homes 不交，fallback supports 可任意共享，helper 可无 fallback。没有输入 actual target、good states 或 joint law。

与旧对象不同，本域还允许任意多个额外 leaf groups，**全部正支持只在 B**。每 leaf 的 states 也 normalized，叶数、菜单数和资格度不固定。固定 ε=15/16，令

    H_l={u∈B : max_s p_lsu≥ε},
    b_l=max_s Σ_(u∈B outside H_l)p_lsu.

每 leaf 须满足 b_l<ε，即既有 exact threshold-unit-demand 判别。它不要求每个 state 本身 unit singleton。叶 graph 可能没有全匹配，这种输入仍在域内，算法须真处理。没有其他 groups；没有 homes 上的叶正支持。

所有 indexed state/resource pair 至多一个 listed incidence。允许并保留显式零 incidences、重复 indexed states、unused resources。上述 support 条件只指正系数，零 incidences 可在原资源集任何位置；它们不被从普通矩阵删掉。菜单完整显式，不用succinct编码；结构呈现随输入给出。

## 2. 全部 ordinary UM jobs

每个 indexed state 建不同 private machine，每原资源建 resource machine。每 group 一枚原 unit selector，只能去该组全部 indexed-state private machines；outer selector 因而只有一个有限端点。每 listed incidence 是一枚原不可拆 job，private time 是其原系数、exact resource time 是一，其他单元无穷。没有额外状态约束或guard。

若 groups、states、listed incidences、resources 数为 G,S,I,U，则 P(Q) 有 S+U 台原机器、G+I 原 jobs、S+2I 个 finite endpoints。全部 selectors、未选 state payload、显式零 jobs 都须执行一次，不能只求活跃子问题或另加资格。

## 3. 精确声称

存在一个固定确定性 worst-case 总位多项式算法，仅接收第1节 Q，计算叶判别、显式生成第2节完整 P(Q)，并输出所有原 jobs 在原有限端点上的完整合法 assignment σ，使

    C_max(σ) ≤ (19/10) OPT(P(Q)).

多项式次数是绝对常数，不依赖 k、helpers 数、叶数、indexed states 数、资格度、support宽度或分母数值。没有输入 feasible SA/LP/PSD 点、OPT、实际 allocation、精度参数或调度 oracle；不调用 generic exact SDP finder，不依赖随机采样、Las Vegas/rejection 运行时间或枚举指数 joint state profiles。

允许 standard deterministic matching/mincostflow、精确有理线性优化和 polynomially many rational arithmetic steps；不能把某个指数配置或joint state优化当成oracle。原矩阵的所有job输出与编码长度都属于算法保证。

此域是“single-state outers、全home互异、k^4-tiny、任意helper fallback、额外B-only exact-threshold-UD叶”的指定类。它不推广到多state outers、非tiny home weights、home重叠、homes上的额外leaf正支持、一般nonUD extra groups或任意普通UM。一般 UM-TARGET-v1仍OPEN；无端到端软件、外审或新颖性声称。
