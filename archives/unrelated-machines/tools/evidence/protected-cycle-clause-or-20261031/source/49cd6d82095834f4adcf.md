# 保护环 clause-OR 失效：规范正文第9节最终组合核验

审查者：boss11 内部 rank_deficiency_fee。本文件只在 clone 外冻结，不修改规范正文或原独立审查。

## 冻结版本与覆盖范围

实际读取规范正文：

`co-work-anl-boss11/research/current/unrelated_machines/near_unit_implication_pcsp_and_physical_copy_obligation.md`

整文件 SHA256：`17b9a0fd3169f7b49bfcd279f17d300c4b2b4cced02be69f1deb05939da97307`。

本次数学覆盖其新增第9节 `UM-PROTECTED-CYCLE-CIRCUIT-CLAUSE-OR-FAILURE-v2`；不以此次读取冒称重新审查第1–8节。组合对照的来源为已读 v2 Exact/Proof：

* Exact SHA256 `535e79f8d7cd30b5db5cc64c4b949a627b9f0b5f675f0a17c7c4b3e6b8922b47`。
* 作者 Proof SHA256 `a1185009ce971afc21eb784ac1b1bead28f30c1602ab847735c5a3fcc8480d02`。
* 原独立 Exact-first 记录 SHA256 `5af034b2d930cfb48c31cde9b4e3a33fce2b6040049b0efc53bd15307fb610ff`。
* v2 读后审查 SHA256 `82b6cdfaccdc105b7c7b8df2ba75d5f2073c01601f23c3bf7ddf4ba553cc243b`。

## 1. 最终 domain 与空退化

第9节限定每 clause 至少两个物理 occurrences，允许重复变量和文字；各 occurrence 的 M_i、C_i 物理身份独立。环至少3个索引，dummy不属于clause、polarity任意；q_i、b_i及u_c的有限端与 v2 原矩阵一致。a∈(0,1)保全部有限时间≤1；可选 a>B/2 仅为其它环合同的连接参数，不参与本匹配结论。

空公式 N=h=0 时明确输出一台 idle 原机器、零 jobs；空调度实际负荷0，合法满足 UM 机器数至少1。非空时没有idle、两侧数量同为2N+h。最终只承诺非idle机器恰一job，正确修复 v1 的对象边界，不在空实例虚构 perfect matching 或 R_c 任务。

## 2. 全部任务和共同实际构造

规范正文的共同证书与本审查者先前独立证书逐项相同：真实 x_i=1/k_c、dummy x_i=0；q_i两环端先各1/2并在pin方向扣x_i，真实q_i在R_c加x_i；b_i的pin/C两项为x_i、1−x_i；u_c向各C_i加x_i。

每个q、b、u的总量均恰1。M_i上被扣的q pin项由同索引b pin项补回，两个相邻环edge各供1/2，总和1。真实C_i的b/u项和1，dummy C_i只有b的1；每R_c有k_c项1/k_c。所有分数非负，k_c=2允许零项。

因此这是一个共同、全任务、全机器的fractional perfect matching，不是逐机换见证。Hall/二部整数匹配在同一原有限资格图上输出完整整数matching；每job恰放一次，每非idle机一job，其实际处理时间≤1，所以所有机器同时负荷≤1。R_c只有其clause真实q邻居，实际q身份读出成立，但q_i@R_c与u_c@C_j的i=j从未被加入矩阵或证明。

## 3. 规范10-job手工解

第9节使用的是本审查者先前提出、root另按原端回算的1-based手工解：

    q1→R+，q3→R−，q2→M3，q4→M4；
    b1→C1，b2→M2，b3→C3，b4→M1；
    u+→C2，u−→C4。

对 (x∨x)∧(¬x∨¬x)、环polarity (0,0,1,1)：q2→M3是合法shifted unit端；q4→M4是合法small home；b2→M2为正pin；b4→M1为负pin的环后继。其余C/R端均为各job原有限unit端。

十机各恰一job，十件原job各恰一次；实际时间均a或1，且有unit任务，峰值恰1。取a=9/10时同样峰1。读出的q索引1、3与返回b索引2、4不同，完整地展示了identity错配。该手工matching与作者Proof的另一份matching不同，二者均合法，不构成版本冲突。

## 4. 稠密矩阵与总位复杂度

按必要的最少padding把不足3次的变量补到3，N≤原occurrence数+2×出现变量数，为显式公式的线性量。若接口另接受显式给出的更长dummy表，则应以该显式N计输入/输出规模，不能隐式指定指数长padding后仍称按未padding公式线性；第9节的必要padding构造不需要这种额外展开。

有限资格数O(N+Σ_c k_c)，每个fractional证书项只含常数和1/k_c，位长多项式。若主模型要求完整稠密P，确实要输出O((2N+h)^2)个矩阵项；正文已明确该二次项，未偷用稀疏线性输出。有限a的重复输出按其原输入有理位长计，仍总位多项式。整数matching、实际owner输出和全机负荷回算皆不按1/a或分母数值展开。

## 5. 失败范围与最终意见

第9节准确证明的是：这个保留私有C_i、增加公共R_c和unit-clause-job u_c的明确实际矩阵，对任意上述公式均已strict feasible，因此这一步OR编译不能保源NO。它没有把fractional证书当实际调度，没有把任务身份读出等同同编号返回，也没有引入源hardness、NP/ETH/UGC或一般近二不可能性。

正文明确保留其它共享资源、medium共居保护、一般nearunit身份机制与UM-TARGET-v1的开放性；实际证明状态、有限10job证书、外审与新颖性也分开记录。规范第9节与冻结 v2 来源组合一致，当前没有standing fatal objection。本次未新增一般hardness或数值样本。
