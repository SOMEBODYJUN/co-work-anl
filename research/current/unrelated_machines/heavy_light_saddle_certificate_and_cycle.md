# 重轻角色的自洽对偶证书与二循环边界

本文登记精确身份 `UM-HEAVY-LIGHT-SADDLE-CERTIFICATE-v1`。它不宣称一般算法；它把“先选重任务、再补轻任务”接口中可验证的纯 saddle 条件写成一个严格充分条件，并给出最小的最佳响应二循环，说明逐次重算残余对偶和重任务匹配不能自动停机。与逐价格凸化的 `∀λ∃H` 条件相比，本页增加的是一个可核验的 `∃H,λ` 自洽证书及其精确失败机制。

## 1. 固定阈值与角色

取合法输入 `P`、`T>0` 和 `β∈[1/2,1)`。保留 `E_T={(i,j):p_ij≤T}`，把 `p_ij>βT` 的边称为 heavy，把 `p_ij≤βT` 的边称为 light。一个 heavy placement `H` 是 heavy 边上的部分匹配：每台机器和每个任务至多出现一次；没有任何 light 边的任务必须被 `H` 覆盖。令 `J_H` 为已覆盖任务，`a_i(H)` 为机器 `i` 上被 `H` 选中任务的时间；未覆盖任务 `j` 只允许使用其 light 端集合 `L(j)`。

给定 `H`，定义残余分数值
\[
 R(H)=\min_x\max_i\left(a_i(H)+\sum_{j\notin J_H}p_{ij}x_{ij}\right),
\]
其中 `x` 对每个未覆盖任务守恒、只使用 light 边且非负。若某任务没有可用 light 端且不在 `J_H`，则该 `H` 不 admissible。

令
\[
 \mu_j(λ)=\min_{i\in L(j)}λ_i p_{ij},
\]
并将无 light 端任务的 `μ_j` 视为 `+∞`。对归一化价格单纯形
`Δ={λ≥0:Σ_iλ_i=1}`，定义
\[
 g(H,λ)=\sum_iλ_i a_i(H)+\sum_{j\notin J_H}\mu_j(λ).
\]
残余 LP 的强对偶给出
\[
 R(H)=\max_{λ\inΔ}g(H,λ). \tag{1}
\]

## 2. 自洽 saddle 充分条件

**定理。** 若存在 admissible `H` 和 `λ*∈Δ`，满足

1. `λ*` 是 (1) 的残余 LP 最优对偶，即 `g(H,λ*)=R(H)`；
2. `H` 在 `g(·,λ*)` 上全局最小：对每个 admissible `H'`，
   \[
   g(H,λ*)\le g(H',λ*),
   \]

则 `H` 全局最小化 `R`：对所有 admissible `H'`，`R(H)≤R(H')`。

**证明。** 由 (1)，对任意 `H'` 有
\[
 R(H')=\max_{λ\inΔ}g(H',λ)\ge g(H',λ*)
 \ge g(H,λ*)=R(H).
\]
证毕。条件 2 是一个标准最小费用匹配：把每个 heavy 边 `(i,j)` 的增量代价写成 `λ_i p_{ij}-mu_j(λ)`；若 `j` 没有 light 端，则该任务被强制覆盖。因而给定有理 `λ*`，条件 2 可以用一次整数最小费用流/交替增广在输入位长多项式时间内核验。

特别地，若 `R(H)≤T` 且所有 light 边满足 `p_{ij}≤βT`，对残余最优分数解运行有序槽舍入，机器 `i` 的最终负载至多
\[
 a_i(H)+\sum_jp_{ij}x_{ij}+βT\le R(H)+βT\le(1+β)T. \tag{2}
\]
若 `β≤1-ε`，这就是 `(2-ε)T` 的实际整数调度。式 (2) 是条件输出合同；它没有给出如何从任意 `P,T` 找到自洽 `H`。

## 3. 即使 `OPT≤T` 也可能没有纯自洽 placement

对任意 `β∈[1/2,1)`，令
\[
 δ=(1-β)/4,\quad a=1-δ,\quad b_1=β+δ,\quad b_2=β+2δ,\quad c=δ.
\]
取 `T=1`、两台机器，以及三个任务
\[
 p(A)=(a,a),\qquad p(B)=(b_1,b_2),\qquad p(\ell)=(c,\infty).
\]
所有 `A,B` 的有限边都是 heavy，`\ell` 的唯一边是 light。由于 `A,B` 没有 light 端，它们必须分别进入两台机器；只有两种 heavy placement：
\[
 H_1:A\to1,B\to2,\qquad H_2:A\to2,B\to1.
\]

`H_1` 的残余负载是 `(a+c,b_2)=(1,b_2)`，所以 `R(H_1)=1`，其归一化最优对偶唯一偏向第一台机器，取 `λ_1=(1,0)`。在这个价格下，`g(H_2,λ_1)=b_1+c=b_2<1=g(H_1,λ_1)`。`H_2` 的残余负载是 `(b_1+c,a)=(b_2,a)`，所以 `R(H_2)=a`，其最优对偶唯一偏向第二台机器，取 `λ_2=(0,1)`；此时 `g(H_1,λ_2)=b_2<a=g(H_2,λ_2)`。因此两个 placement 都被自己的最优对偶价格击败，纯自洽 saddle 不存在。

另一方面，`H_2` 本身给出 makespan `a<1=T`，`H_1` 给出 `1`；由于重任务只能分占两机且只有这两个 placement，真实 `OPT=a≤T`。这比 `OPT>T` 的循环例更强：即使在阈值承诺的 YES 实例上，不能假定总能找到纯自洽 pair。它只否定“残余对偶→重匹配→重新求对偶”的必停/必有固定点推断，不否定全局重选、非纯混合信息或其它舍入合同。

以 `β=1/2` 为例，`δ=1/8`，矩阵 `g(H_r,λ_s)` 为
\[
 \begin{pmatrix}1&3/4\\3/4&7/8\end{pmatrix},
\]
其每行的最大值分别由自己的对偶列取得，但每列的最小值由另一行取得；这正是纯策略没有 saddle 而凸化可以有混合 saddle 的最小结构。

## 4. 与现有 min–max 接口的关系

逐价格最小费用流只给
\[
 \forall λ\inΔ\;\exists H:\ g(H,λ)\le T,
\]
而真实共同角色需要某个同一 `H` 通过全部价格；自洽条件把这一量词交换压缩成一个可检查的 saddle 点。若任务角色集合本身也随 `H` 改变，必须把 `\mu_j(λ)` 的基线变化保留在 `g` 中；不能只比较 `Σ_iλ_i a_i(H)`。本页的定义已经允许可选 heavy 任务通过 `\sum_{j\notin J_H}\mu_j` 处理这一变化。

`H_1,H_2` 的二循环并不排除非局部增广、配置相关性、全局整数重选或不同舍入合同；它只关闭“逐次最佳响应必然给出纯 saddle”的推断。若未来要用此路线接近 `UM-TARGET-v1`，最小新义务是：或者证明一般输入存在并可找到某种近似 saddle，并把其残余价格值与实际容量损失统一耦合；或者证明一个不依赖纯 saddle 的全局增广规则。

**Truth / Value / Novelty / Ambition。** saddle 充分性是自足强对偶推导，二循环是精确有理反例；新颖性与外部评审未认证，不能称一般困难性。主目标仍 OPEN。

**Related Files：** `research/current/unrelated_machines/heavy_light_price_convexification.md`、`research/questions/unrelated_machines/heavy_light_joint_residual_minmax_obstruction.md`、`research/current/unrelated_machines/joint_matching_completion_and_block_cuts.md`。
