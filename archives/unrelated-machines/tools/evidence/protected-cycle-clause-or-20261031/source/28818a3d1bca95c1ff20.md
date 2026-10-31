# 保护环与共享 clause-OR 的 v2 证明读后核验

审查者：boss11 内部 rank_deficiency_fee。角色：先完成 Exact-first 独立攻击，再读冻结 v2 Exact 和作者 Proof。本读后记录另立文件，不修改原独立记录。

## 1. 冻结对象与读取顺序

首次只读 v1 Exact 后的独立重构已经冻结于：

* `protected_cycle_shared_clause_or_independent_exact_first_review.md`
* SHA256 `5af034b2d930cfb48c31cde9b4e3a33fce2b6040049b0efc53bd15307fb610ff`。

本次按次序读取：

1. v2 Exact `protected_cycle_shared_clause_or_failure_exact_v2.md`，SHA256 `535e79f8d7cd30b5db5cc64c4b949a627b9f0b5f675f0a17c7c4b3e6b8922b47`。
2. v2 作者 Proof `protected_cycle_shared_clause_or_failure_proof_v2.md`，SHA256 `a1185009ce971afc21eb784ac1b1bead28f30c1602ab847735c5a3fcc8480d02`。

上述三个 hash 已实际回算。未读取 v1 作者 Proof，未把未列明的其它证明文件算作本次覆盖。

## 2. v2 对象修补

v1 的空公式导致0机器，不是本项目 m_machine≥1 的合法 UM 对象。v2 在且仅在 N=m=0 时添一台 idle 机器、没有 jobs，实际机器数 max{1,2N+m}；空调度负荷0。

“每台非idle机器恰一原job”在空退化时真且没有伪造 matching；非空公式时没有idle，原两侧大小均2N+m，原匹配证明不变。此修补同时出现在 Exact 和 Proof §0 中，覆盖了原独立意见的唯一对象边界问题。没有standing objection。

## 3. 一般匹配证明与独立重构一致

作者的 x_i 与独立重构的 r_i 完全相同：真实 occurrence 为1/k_c，dummy为0。作者全部 q_i→C_i 质量0，b_i 的 pin/C 分配为 x_i和1−x_i，q_i 从 polarity 对应内部端扣x_i且在R_c放x_i，u_c向各C_i放1/k_c。所有这些均为原有限端。

独立证书已逐job和逐machine列式；作者对每个环edge把 q_i与b_i合起来看作两端各1/2，与独立行式中 pin 项逐项抵消是同一个等式。该恒等式不要求环上polarity一致，不要求各clause arity相同，不要求变量/文字在clause中不重复。

k_c=2 时1/2−x_i=0，不产生负数，不要求此边必须在整数输出中使用。dummy的 x_i=0 给 b_i→C_i 质量1、q_i两内部端各1/2，不产生R资格。n_v≥3确保两内部端不同且每个物理 occurrence 索引独立。

作者用整数最大流恢复matching，独立记录用Hall和逐次交替BFS恢复；二者在同一共同fractional perfect matching证书上等价。分数只作存在证书，最终每job完整选择一个原端，每machine恰一job，实际全机负荷≤1。R_c只邻该clause的真实q_i，故任务身份读出本身保留，但不保与u_c释放C_j的索引相同。

## 4. 两份10-job UNSAT手工匹配均合法

令 Φ=(x∨x)∧(¬x∨¬x)，环索引0,1,2,3，polarity为(0,0,1,1)，clause0含0,1，clause1含2,3。下面把作者Proof的匹配与本审查者先前独立给出的匹配放在同一0-based记号下核对：

|原机器|作者匹配|独立手工匹配|
|---|---|---|
|M0|b0（a）|b3（a）|
|M1|q0（1）|b1（a）|
|M2|q2（a）|q1（1）|
|M3|b2（a）|q3（a）|
|C0|u0（1）|b0（1）|
|C1|b1（1）|u0（1）|
|C2|u1（1）|b2（1）|
|C3|b3（1）|u1（1）|
|R0|q1（1）|q0（1）|
|R1|q3（1）|q2（1）|

作者匹配中 b2 的负pin为M3；独立匹配中 b3 的负pin为M0。其余small边均是各自合法home或正pin；两个shifted q分别为作者q0→M1和独立q1→M2。所有unit C/R端逐条属于原矩阵。

两列各将十件原job恰用一次、十台machine恰一件，所有实际时间为a或1，且各有unit，故对任意a∈(0,1)峰值均恰1。它们不是相同matching，也不需要相同；都是同一个显式P的完整合法证书。

作者读出的正/负q索引为1、3，对应返回blocker索引0、2；独立匹配读出的q为0、2，对应返回blocker1、3。两者均显示真实q@R与返回b的身份错配，无需把旧同编号交换decoder当额外约束。

## 5. 位复杂度与输出

稀疏有限资格图边数O(N+Σ_c k_c)。certificate项分母为k_c或2k_c，位长O(log(k_c+1))，不依a的数值大小；整数matching可完全在原资格图上运行，不复制分母份数。

若要求完整稠密P，填入其余∞所需O((2N+m)^2)项，是显式公式规模的多项式；每个有限时间a的重复输出只按其输入位长线性计，仍总位多项式。空公式只有一台idle/零job，单独常数时间输出。作者新增说明与实际矩阵大小一致。

## 6. 结论与未覆盖范围

v2 Exact 与 Proof 的限定全公式严格可行结论成立；原空公式对象问题已修复，当前没有standing fatal objection。数学上新增公共R_c和u_c后的实际P，对任意SAT或UNSAT公式都已具有C≤1实际调度，因此这一明确clause-OR编译不保源NO。

本读后核验不升级到一般nearunit identity-copy不可能性，不认证其它D-pool变体、medium共享保护或一般UM近似困难性；没有外审或全局新颖性声明。没有把有限测试代替一般证明，本次未新增数值枚举。
