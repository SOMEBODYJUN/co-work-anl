# 并行线性关系的任意状态重赋权仍可半保留

## 精确身份与读取目的

- **ID/version**：`UM-WEIGHTED-AFFINE-LINE-PARALLEL-RELATIONS-HALF-ESCAPE-v1`。
- **Objects / Domain / Definitions**：prime R≥2、输入整数 k≥2，域 F_R；R个 constraints j 共用相同 k 个不同变量，变量 incidence index 均为 j。每 constraint 的允许表完整列出 A_j={a∈F_R^k:Σ_i a_i=j}。state 的 tagged line 支持及全部非负归一化有理权如下，允许零权与任意 state dependence。
- **Quantifiers / Exact Statement / Conclusion**：对全部上述参数与完整显式权表，存在每组一个允许 state 和全局不交的真实 partial subsets，各取得质量≥1/2；可确定性总位多项式输出这些对象及全部原 UM jobs 的实际≤3/2调度。所选 states 可限为 a(j)=cj+d、Σc=1、Σd=0。
- **Assumptions / Dependencies**：无复杂度假设，不输入源解、OPT、未知 allocation 或分数 oracle。使用有限域与概率平均的自足证明；最终输出确定性整数对象。只沿用仿射线 incidence 的显式定义，不调用 LST 的困难性证明作为前提。
- **Scope**：原 CSP value 恰1/R，但此族易判；不是 NP-hard image。只改原 incidence 权而保这些 groups/states/resources/eligibilities 的接口，不能对包含此族的整个低值 NO 域保证 V<1/2。不排除另一个避开此族的 hard image、额外结构、预处理或改变 gadget 的归约。不同于已有 uniform 任意关系的半保留，本结论允许任意权、需要完整并行线性关系。
- **Evidence / Counterevidence / Objections**：rank 仅 Exact 独立重构，root 实际读后才交作者 Proof；root此前已听口头策略，核对不记盲审。下述 singleton 关系给 V=0/实际OPT2，排除了向任意关系及 k=1 的误推广。精确读取顺序、作者读后与最终正文范围见[审查记录](../../reviews/unrelated_machines/weighted_affine_parallel_relation_reweighting_review.md)。
- **Status**：限定证明完整，独立陈述先行、作者实际读后与最终正文审查分别记录；无软件/有限实验/外审/全球新颖性认证。`UM-TARGET-v1` 仍 OPEN。
- **Related Files**：[uniform source 编译及其范围](line_set_packing_and_take_continue_compilation_obstructions.md)、[另一种 tuple-group 编译](affine_line_tuple_groups_global_dummy_compilation_escape.md)、[审查](../../reviews/unrelated_machines/weighted_affine_parallel_relation_reweighting_review.md)。

## 1. 完整加权菜单与实际矩阵

资源宇宙为不交并 U=⊔_(i=1)^k ({x_i}×F_R²)。constraint j 的每个允许 state a∈A_j 含

\[
S_{j,a}=\biguplus_{i=1}^k\{(x_i,z,a_i z+j):z\in\mathbb F_R\}.
\]

变量 tag 不合并；slope 为 a_i，intercept 为 j；每 state 有 kR 个不同资源。输入对全部 incidences 显式给 w_(j,a,u)≥0，逐 state 和恰1。权可依赖整个 a、j、变量及 cell，不要求共同 item 权、均匀、对称性或最大单项界。V(w) 为每组自由选一 state、领取任意资源子集且组间不交时，最小所领质量的最大值。

普通完整 UM P 的机器为每 state 一个 private M_(j,a)、每 u 一个 resource R_u。每组一件 selector J_j，可在本组任一 private 耗时1。每 incidence 一件不同原 job，仅可在自身 private 耗 w_(j,a,u)，或在 R_u 耗1；其余∞。全部未选 states 与零 private 时间原 jobs 保留。

## 2. 状态相关权下的条件平均

令 C={c:Σc_i=1}、D₀={d:Σd_i=0}，各有 R^(k−1)个向量。先作存在性分析，在两集合上独立均匀取 c,d，选 a(j)=cj+d。每 a(j)∈A_j。

固定 j，映射 (c,d)↦(c,a=cj+d) 是 C×D₀ 到 C×A_j 的双射，逆为 d=a−cj。所以**条件于该组整个已选 state a 后，c 仍在 C 上均匀**。k≥2使每个坐标 c_i 均匀：固定它后有 R^(k−2)种余坐标补和。不要求不同坐标或不同组 states 相互独立。

固定 c,d，tag i 中已选 lines 为

\[
y=d_i z+j(c_i z+1).
\]

c_i=0时不同 j 的 lines 平行不交；c_i≠0时所有 j 的 lines 仅在同一真实点 P_i=(x_i,−1/c_i,−d_i/c_i)相交。故 H(c,d)={P_i:c_i≠0} 之外的已选资源至多属于一组，H 中每点属于所有组。

记删去 H 的第 j 组损失 L_j=Σ_(i:c_i≠0) w_(j,a(j),P_i)。在固定 a(j)=a 条件下，固定非零 z 对应恰一个 c_i=−1/z，概率1/R；此时 P_i 正是固定 line 上的 (x_i,z,a_i z+j)。z=0从不成为共点。因此

\[
\mathbb E[L_j\mid a(j)=a]
=\frac1R\sum_i\sum_{z\ne0}w_{j,a,(x_i,z,a_i z+j)}
\le\frac1R.
\]

先条件于整个 state 才应用均匀性，避免错误地把任意 state-dependent 权当独立权。对 a 再平均、对 R 组相加，E[Σ_j L_j]≤1，故有一个候选 c,d 满足总损失≤1。

## 3. 唯一例外回填、确定性算法及全部原任务

对上述候选，至多一组 L_j>1/2。如果没有，给每组 B_j=S_(j,a(j))\H；它们不交，质量≥1/2。若有唯一例外 h，给它完整 S_(h,a(h))，其余仍删 H。所有共点只交 h，其它点原本各组独占，所以分配仍全局不交；h质量1，其余≥1/2。L_j=1/2不算例外，R=2及零权无例外。资源从未拆分。

确定性算法枚举 c,d 的前 k−1坐标并补最后坐标，候选数 R^(2k−2)=(R^k)²/R²。完整显式输入已有 R^k 个 states，所以这是输入长度多项式，即使 k不是常数。对每候选精确计算 R组、每组至多k个共点权，找到首个总损失≤1者，再按上段输出。平均保证一定找到，不用随机采样、源 witness 或求 OPT。

最后把 selector 放所选 private，只将 B_j 对应的 incidence jobs 导出，所有其它原 incidences 留自身 private。每个 resource 至多一件 unit；未选 private 的全部工作为1；选中 private 的真实负载为

\[
1+\sum_{u\in S_{j,a(j)}\setminus B_j}w_{j,a(j),u}
=2-\sum_{u\in B_j}w_{j,a(j),u}\le3/2.
\]

包含零私时 jobs 及所有未选 states，每原 job 恰执行一次。B_j 内零权 incidence 可以导出或留 private，都不破界。于是实际 OPT(P)≤3/2；selector 给 OPT≥1。

精确规模：groups R，states/private R^k，resource machines kR²，incidence jobs kR^(k+1)，selectors R；finite entries 为2kR^(k+1)+R^k，dense 矩阵为 (R^k+kR²)(kR^(k+1)+R)项。模域运算按 logR 位长，质量用普通精确有理数。每候选至多相加 kR 个输入权，分母积位长不超过相应输入位长之和；候选间不累计分母。全算法按完整显式表总编码长度多项式，不是 succinct poly(k,logR)，也不按1/w或分母数值复制。

## 4. Source value、任意关系反例与准确否定范围

主族任一全局赋值的坐标和恰等于一个 j，因此恰满足一项，source value=1/R。此低值来自容易检查的平行关系，不能称它属于某个未知 hard reduction 的输出像。

若改允许表为 singleton A'_j={(j,0,…,0)}，每组第一变量 line y=jz+j 共含 u*=(x_1,−1,0)。把总权1放 u*、其余0。最多一组可领取该点，R≥2迫 V=0。全部 jobs 留 private 得实际峰2；任意峰<2时每组唯一 private 有 selector1，所以共点 incidence1 都必须导出，同一资源至少R件 unit，矛盾。故实际 OPT=2。k=1时主关系本身就是此反例；k≥2是承重条件，不能删除。

这显示权重确能破坏任意关系的旧 uniform 半保留，但并非仅仅改权就能对所有低值源补上 soundness。若某接口只改原权并声称对包含本族的整个 NO promise域强制 V<1/2，本定理反驳它。另有 hard image避开本族，或允许改关系/资源/资格/预处理，则仍需独立审查，不在否定范围。

若原 source 本来存在完整 supports 不交的 full-set packing，任意逐 state 归一化非负权当然保留完整质量1；这只是 YES 机械保留，不能替代 NO 的全 partial decoder。本结果没有构造 normalized YES1/NO任意小的困难性源，没有推出一般 UM 的反面。
