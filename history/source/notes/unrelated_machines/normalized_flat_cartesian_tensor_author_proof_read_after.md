# 裸 Cartesian 菜单反向放大：作者证明读后核验

审查者：boss11 内部 rank_deficiency_fee。

## 读取对象、冻结记录与次序

本次实际读取作者 Proof：`normalized_flat_cartesian_tensor_reverse_amplification_proof_v1.md`。

给定并实际回算的 SHA256：`958aba5d1ab5d2aff945df752a80d87bb99a61f64dcfc9cf439db74717338702`。

此前仅根据 Exact 完成并冻结的独立记录是：

* `normalized_flat_cartesian_tensor_independent_exact_first_review.md`
* SHA256 `a04fa4b474fc605ccc32f32728779f02dcec7c0be91e8c01ab031cf99a9f943e`。

Exact 为 `normalized_flat_cartesian_tensor_reverse_amplification_exact_v1.md`，SHA256 `60299e46c9677b6fbfc94ac866bfe317151c83154c1fe7c14510eedc84050bac`。原 Exact-first 记录保持原字节，不用读后结果覆盖其独立次序。

## 证明与独立重构的逐项一致性

1. **V上界。** 作者和独立重构均取互补groups g与g+1^t。任意两state的共同资源逐坐标唯一解为a_i=ℓ_i(g)+ℓ_i(g+1^t)，b_i=ℓ_i(g)+g_i a_i。因此至少一组不能领取其完整2^t项，整数partial cardinality给V_t≤1−2^(−t)。没有限制partial B_g为Cartesian子集，也没有限制state选择只依赖本坐标。

2. **V下界。** 二者独立选出相同循环移位labels ℓ_i(g)=g_(i+1)，并只领取a≠1^t的资源。独立记录通过一个a_j=0的坐标直接确定g后沿环求解；作者比较两个领取者，令δ=g+h，得δ_(i+1)=a_iδ_i，再由零位消去全部δ。这是同一二进制环方程的两种等价验证，均适用于t=1。

3. **完整actual上界。** 作者逐一保留全部未选state的incidence jobs，在自己的private机执行；selected state导出2^t−1件，只留一件small。故selected机恰1+2^(−t)，未选机恰1，resource机至多1。所有8^t incidence jobs及2^t selectors均恰一次，原端合法。

4. **任意actual下界。** 作者直接取互补group所选state的共同资源，对应两件不同incidence jobs。若C<2，二者不能同在其resource机，所以至少一件留自己的selected private机，与本group selector合成1+2^(−t)。若C≥2则下界平凡成立。这比独立记录先反设所有selected jobs全导出的写法更直接，数学结论相同，覆盖全部完整σ。

5. **计数与位长。** 作者的2^t groups、4^t private机、4^t resource机、8^t incidence jobs、2^t selectors与Exact及独立记录一致。有限条目数2·8^t+4^t，dense矩阵(8^t+2^t)·(2·4^t)，时间2^(−t)位长O(t)。复杂度按显式对象长度多项式，不是poly(t)。t=1有10jobs/8machines，峰3/2；t=0明确不在域中。

## 结论、范围与异议

作者 Proof 闭合冻结 Exact 的(A)、(B)、(C)，与已冻结独立重构一致，当前没有standing fatal objection。

结论仅针对明确的normalized flat Cartesian-menu操作及其全部独立group state选择自由度。循环label选择跨group坐标相关，但每个所选state本身始终是原纯Cartesian支持；这正是合法自由度，不是改了乘积定义。

该操作没有保持资源跨group degree3：每资源出现在全部2^t个group的完整menu union。本反例不否定另有一致性条件、degree保持结构、不同资源/分组或特定source image的乘积归约，也不提供一般UM算法或hardness。不记录新实验、外审或全球新颖性认证。
