# Normalized flat Cartesian tensor 反向放大：作者 Proof v1

对应冻结 Exact `UM-NORMALIZED-FLAT-CARTESIAN-TENSOR-REVERSE-AMPLIFICATION-v1`。Exact 文件 SHA256 为60299e46c9677b6fbfc94ac866bfe317151c83154c1fe7c14510eedc84050bac。root 已仅据陈述独立闭合上界与GF2 cyclic下界；本作者 Proof 另冻仅发root，不主动发送给尚在 Exact-only 阶段的新 reviewer。

全部对象、符号、P与范围以 Exact 为准，t≥1。这里只给自足证明，不称所有tensor操作无效。

## 1. 任意 states 的互补 group 交一格：上界

固定任意 g∈GF(2)^t，令 h=g+1^t，二者是不同的真实groups。给它们任意实际选择的 indexed states ℓ(g)、ℓ(h)，不是假设坐标state只依赖g_i。

每坐标的共同resource必须且只须满足

b_i+g_i a_i=ℓ_i(g)，
b_i+(g_i+1)a_i=ℓ_i(h)。

唯一解是 a_i=ℓ_i(g)+ℓ_i(h)，b_i=ℓ_i(g)+g_i a_i。因此 S_(g,ℓ(g)) 与 S_(h,ℓ(h)) 恰交一枚真实 resource tuple。任何 pairwise-disjoint partial allocation 不能让这两个groups都领取各自全部2^t项；至少一个只领取≤2^t−1项，其质量≤1−2^(−t)。这对全部 states 及部分子集成立，故V_t≤1−2^(−t)。

## 2. Cyclic labels 与完整 partial allocation：下界

下标按t循环，g_(t+1)=g_1。对每 g 选择完整state向量

ℓ_i(g)=g_(i+1)。

其支持可按 a∈GF(2)^t 一一参数化：第i坐标是(a_i,b_i)，其中 b_i=g_(i+1)+g_i a_i。把所有 a≠1^t 对应的resources都分给g。每组领取恰2^t−1项。

证明这些B_g跨组不交。若g与h领取同一resource，其a向量必须相同，因为a正是resource各坐标的一部分。令δ_i=g_i+h_i，比较两式b_i，得

δ_(i+1)=a_i δ_i 对每i成立。

领取时a≠1^t，故某i有a_i=0，推出δ_(i+1)=0。沿整个循环递推得全部δ_j=0，因而g=h。不同groups不会领取同一resource，各B_g合法；故V_t≥(2^t−1)/2^t。

结合第1节，V_t=1−2^(−t)。t1时循环就是自己，a=0是唯一保留向量，仍给每组1项，全部推导有效。

## 3. 全部原jobs的 actual 上界

使用第2节state与B_g：每selector J_g放M_(g,ℓ(g))，该selected state中对应B_g的2^t−1件 incidence jobs真正导出到相应R_u。该state剩余一件incidence留private；全部未选 states 的每一件 incidence也留自己的private machine。没有省略未选state jobs。

selected private load恰1+2^(−t)，未选private load恰1。resource接收的unit jobs按第2节全局不交，故每resource负载≤1。全部selectors与全部8^t incidence jobs各执行一次，所有时间均是Exact原有限端，得到actual峰恰1+2^(−t)。

## 4. 任意完整actual调度下界

若实际峰C≥2，则C≥1+2^(−t)显然（t≥1）。否则C<2，每resource只能执行至多一件unit incidence job。

任取互补groups g,h，其selectors实际所在states为ℓ(g),ℓ(h)。第1节给这两个state支持中唯一共同resource u。两件不同真实jobs I_(g,ℓ(g),u) 与 I_(h,ℓ(h),u) 不能同时在R_u上unit执行。因此至少一件留在它自己selected private机，该机还实际执行本group的unit selector，负载至少1+2^(−t)。这给所有完整actual调度同一下界；其它未选state jobs占资源只会增加障碍。

于是OPT(P_t)=1+2^(−t)=2−V_t。这个下界也可从任意actual C<2提取selected-state实际exports质量≥2−C得到，但不需要先规范化未选state jobs。

## 5. 规模与位复杂度

group、每组state、每state支持的三个计数均为2^t，故incidence数8^t；indexed state/private总数4^t，resource总数4^t。selector数2^t，每selector有2^t条finite资格，合4^t条；incidence每件两finite资格，合2·8^t条。机器总数2·4^t、jobs总数8^t+2^t。

显式t-bit标签、state资格与上界完整actual assignment均可逐项生成；各权2^(−t)位长O(t)，有理加法与负载精确回算按显式总长度polynomial。dense矩阵若要求也按Exact给出的条目数输出。不声称8^t输出能在poly(t)时间完成。

本族仅是所定义裸Cartesian菜单操作的NO反向放大，不提供任何复杂性源；额外一致性/不同group结构/别的产品不在这个证明的量词内。
