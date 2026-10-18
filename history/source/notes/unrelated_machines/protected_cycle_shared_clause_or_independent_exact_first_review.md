# 保护环与共享 clause-OR 的独立 Exact-first 匹配证书

审查身份：boss11 内部 rank_deficiency_fee。对象：`UM-PROTECTED-CYCLE-CIRCUIT-CLAUSE-OR-FAILURE-v1`。只读取冻结 Exact `protected_cycle_shared_clause_or_failure_exact_v1.md`，SHA256 `c5fd305fd172d42980925a2557680b82fabba63970b026a7d9d05259ba2d74c1`；未读取作者 Proof，亦未与作者交换证明。

## 独立结论

对所有非空 Φ，Exact 的全公式 C≤1、逐机恰一原 job、实际 R_c 上原 q_i 身份读出结论成立。下面给与 polarity、occurrence 排序、dummy polarity、a 数值均无关的共同有理匹配证书；再用显式增广路算法转换成全部原 jobs 的整数实际分配。

唯一 statement 边界：空 Φ 给 N=m=0，即0 machine/0 job，违反本研究一般 UM 的 m_machine≥1 输入约定。作为空二部图，其空匹配数学上仍成立，但不能原样称合法目标 UM。可限定 Φ 非空，或为纯空退化另加一台 idle machine 并把“每机恰一job”改为“每非idle机恰一job”。该修改须另冻版本；本文件不改 v1。

## 1. occurrence 权重

对每个真实 occurrence i∈c，定义 r_i=1/k_c；对 dummy 定义 r_i=0。因 k_c≥2，始终有 0≤r_i≤1/2。

以下 x 是任务—机器二部匹配的分数变量，不是分数执行调度。未列出的 x 全为零，包括所有 q_i→C_i 资格。每个 job 的各 x 之和及每个 machine 的各 x 之和都恰为1。

真实 occurrence i∈c：

    x(q_i,R_c)=r_i。

对全部 occurrences（含 dummy）：

    x(b_i,C_i)=1−r_i，
    x(b_i,pin(i))=r_i。

若 s_i=0（正 polarity）：

    x(q_i,M_i)=1/2−r_i，
    x(q_i,M_{i^+})=1/2。

若 s_i=1（负 polarity）：

    x(q_i,M_i)=1/2，
    x(q_i,M_{i^+})=1/2−r_i。

对每 clause c 和每个真实 occurrence i∈c：

    x(u_c,C_i)=1/k_c=r_i。

所有列出的正 x 都在 Exact 的真实有限处理时间资格上；a 只影响执行时间，不影响此证书。n_v≥3 保证两个环端点不同，且每个 occurrence 有唯一环前驱。

## 2. 逐 job 核列和

真实 q_i 的内部两项和为1−r_i，另有 R_c 项r_i，总和1。dummy q_i 的 r_i=0，两环端各1/2，总和1，且没有虚构 R 端。

每 b_i 的两项和为 (1−r_i)+r_i=1。每 u_c 在 k_c 个彼此不同的 occurrence 私有 C_i 上各1/k_c，总和1；即使文字或变量重复，物理 C_i 仍不同。

## 3. 逐 machine 核行和

R_c：只接该 clause 的真实 q_i，各r_i=1/k_c，共k_c枚，合计1。

真实 C_i：接 b_i 的1−r_i和所属 u_c 的r_i，合计1。dummy C_i：只接b_i的1，合计1。q_i 的 C_i 资格全部未使用，不会隐藏重复身份。

令 i^- 为变量环前驱。M_i 恰可能接：q_i 的自身端，q_{i^-} 的后继端，s_i=0时b_i的pin端，s_{i^-}=1时b_{i^-}的pin端。记指示函数 [·]，这些分数和为

    (1/2−[s_i=0]r_i)
      +(1/2−[s_{i^-}=1]r_{i^-})
      +[s_i=0]r_i+[s_{i^-}=1]r_{i^-}=1。

这覆盖任意正负排列、同 clause 重复文字、同 clause 正负同现及 dummy polarity。k_c=2 时某一 q 内部项为零，无负项，也无严格正性假设。

故整个 (2N+m)×(2N+m) 二部图上给出了共同 doubly-stochastic 分数匹配。

## 4. 转成共同整数匹配及完整实际调度

只保留 x>0 的 job—machine 支撑边。对任意任务子集 S，列和给出从 S 发出的总 x 质量为|S|，全部流入其邻机集合 Γ(S)；每机行和1，故

    |S|≤|Γ(S)|。

于是可逐次找增广路构造满匹配，而无需调用未知调度 oracle。具体算法：固定输入给出的 job/machine 顺序，从空匹配开始，为最小未匹配 job 做交替 BFS，若找到空 machine 就沿路翻转，匹配数增1。若失败，BFS 可达任务集 S 与其邻机 Γ(S) 将满足 |Γ(S)|<|S|，与上式矛盾。因此至多2N+m次增广后覆盖全部 jobs。

机器与 jobs 数相等，所以满 job 匹配也恰覆盖全部机器，每机一枚原 job。把原 job 分到其匹配 machine 即为完整实际 σ；所用实际时间仅 a 或1，a∈(0,1)，故所有机器负荷同时≤1。每个 R_c 的匹配邻居只能是其 clause 的某一原 q_i，因而 R_c 的身份读出是真实的，但无条件保证它等于 u_c 所占 C_j 的索引 j；任何源 decoder 都必须另证该相等。

## 5. 位复杂度与证据范围

显式真实 occurrence 数为 Σ_c k_c；每变量最多添两枚 dummy，故 N 为显式公式规模的多项式。所有证书项只含 0、1、1/2、1/k_c、1/2−1/k_c，其分子分母位长 O(log(k_c+1))；证书完全不依赖 a，尤其不存在按1/a或1/(1−a)展开。

正支撑边总数 O(N+Σ_c k_c)。最多2N+m次交替 BFS，每次扫描显式支撑图，故确定性构造总位多项式；可仅以 k_c=2 的整数测试判断 1/2−1/k_c 是否为零，匹配阶段不需要分数运算。

本审查给一般数学证书及构造证明，未运行有限枚举，也未读取作者 Proof。它证明这个明确 P 变体对全部非空公式都有严格实际调度，从而不保源 NO；不证明其它 nearunit 身份构件或一般 UM 归约失败。
