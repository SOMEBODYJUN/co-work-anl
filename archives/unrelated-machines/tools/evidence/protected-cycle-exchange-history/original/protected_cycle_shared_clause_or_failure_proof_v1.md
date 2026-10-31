# Ci/Rc/unit-clause OR 变体的全公式严格可行：作者证明 v1

对应 `UM-PROTECTED-CYCLE-CIRCUIT-CLAUSE-OR-FAILURE-v1`，完整对象见 `protected_cycle_shared_clause_or_failure_exact_v1.md`。本证明在 Exact 已交由另一审查者仅读独立攻击后冻结；不主动发送给该审查者。

## 1. 显式共同 fractional perfect matching

只看原 P 的 job–machine 有限资格二部图，先构造单位容量的分数匹配。真实 occurrence i 属于 clause c 时令 x_i=1/k_c；dummy 令 x_i=0。因为 k_c≥2，所有 x_i∈[0,1/2]。

按如下原有限端赋质量，未列边质量全0：

- q_i 在自己的原 C_i 上质量0，在所属 R_c 上质量 x_i（dummy没有 R端）；内部两端质量为：
  - s_i=0 时，q_i→M_i 为1/2−x_i，q_i→M_{i^+} 为1/2；
  - s_i=1 时，q_i→M_i 为1/2，q_i→M_{i^+} 为1/2−x_i。
- b_i→pin(i) 质量 x_i，b_i→C_i 质量1−x_i。
- u_c→C_i（i∈c）质量 x_i=1/k_c。

这些都是原矩阵实际允许端，全部非负。下面逐原 job、逐原机器核总量。

**job列。** 每 q_i 的内部质量为1−x_i，加 R质量 x_i，恰1；dummy内部恰1。每 b_i 为 x_i+(1−x_i)=1。每 u_c 在 k_c 个原 C端各1/k_c，总量1。故每原 job 精确覆盖一次质量。

**内部机器。** 对每条 cycle-edge i（内部端 M_i,M_{i^+}），q_i 与 b_i 在 M_i 合计质量恰1/2，在 M_{i^+} 合计也恰1/2：pin方向由 b_i 补上 q_i 被扣的 x_i。每 M_i 恰邻本edge的左端及前一edge的右端，因此收到1/2+1/2=1。此处 n_v≥3，后继/前驱为原不同内部端，没有把同一 job 在一台机器重复计成不同资格。

**私有 C_i。** 真实 occurrence 的 C_i 收 b_i 质量1−x_i 及唯一所属 clause 的 u_c 质量x_i，恰1；dummy C_i 只收 b_i 质量1，也恰1。q_i→C_i 资格不使用。

**公共 R_c。** 恰收该 clause 全部 q_i 的1/k_c，共k_c项，质量恰1。

所以所有2N+m个原 jobs与全部2N+m台原机器组成共同 fractional perfect matching；不是分别对每台机器选择不同见证。

## 2. 恢复全部实际任务而非分数执行

建立原 job→机器的二部单位容量网络：source→每job容量1，每原有限资格边容量1，每机器→sink容量1。上节是流量2N+m的分数可行点，故最大流值至少2N+m；总 source 容量也恰该值。整数容量的最大流可取整数，因此给一份覆盖全部原 jobs的实际 perfect matching。

按该 matching 把每 job 完整放到一个原有限端。每机器恰一原 job，而本实例每有限处理时间为a或1、均≤1，故实际全机负载同时≤1。没有把上节分数处理时间当实际调度，也没有拆分原任务。

R_c 的原邻接 jobs只有该 clause 的 q_i，所以整数 matching 中每 R_c 确实收到一枚属于该 clause 的原 q_i，并走原 unit 端。这保留了任务身份读取本身，而没有保住它与被返回 b_i 的编号关联。

构造显式规模O(N+Σ_c k_c)，x_i 只需分母 k_c 的O(log N)位。可直接运行任意确定性二部整数最大流/匹配算法，不必按分数分母展开复制，更不按1/a枚举。全部原矩阵输出、actual matching与逐机负载回算均为总位多项式。

## 3. 一个10-job/10-machine的真实 UNSAT→strict YES

取 Φ=(x∨x)∧(¬x∨¬x)，两 clause 均arity2、显然 UNSAT。单变量环按 occurrence i=0,1,2,3 排列，s=(0,0,1,1)，i=0,1属clause0，i=2,3属clause1，无dummy。任意 a∈(0,1) 都可，若同时指定 B<2 则可选 a>B/2。

以下完整实际分配逐 job 只用一次：

|机器|实际job|处理时间|
|---|---|---:|
|M0|b0|a|
|M1|q0|1|
|M2|q2|a|
|M3|b2|a|
|C0|u0|1|
|C1|b1|1|
|C2|u1|1|
|C3|b3|1|
|R0|q1|1|
|R1|q3|1|

全部端合法，十件原任务均恰出现一次，十台机器各恰一件，峰值1。正 clause 的实际读取是 q1@R0，触发返回的却是 b0@M0；负 clause 的实际读取是 q3@R1，返回的却是 b2@M3。内部未导出的 q0 取 shifted 端，而 q2 取 home 端，形成两个 phase。正负读数共存，保护环原来的同编号 swap与全局bit decoder不再适用。

这与 root 的6-occurrence/D-pool反例是不同的原 P；本变体保留每个 C_i，并另加 R_c 与 u_c。二者不能混同为一个矩阵证书。

## 4. 准确失败范围

私有 protected component 中，q_i@C_i 当且仅当同编号 b_i 返回pin，是靠私有 C_i 的恰一占位维系的。外接本变体后，q_i 可直接去 R_c，而 u_c 可占另一个 C_j；计数仍给每机一 job，却只守住总量，允许 q_i 被取走、b_j 被送回。分数证书表明该松动不只是少数例外：所有 clauses arity≥2 时任意公式都 strict feasible。

本定理只否定这一明确 clause OR 编译步骤；它不否定原私有身份组件、不否定加入 medium/跨尺度共享保护后的不同矩阵，也没有证明一般 copy 不可能。所有处理时间≤1且源 NO直接变strict YES，所以该变体尤其不能提供近2 soundness。
