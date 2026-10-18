# Normalized flat Cartesian tensor 反向放大：冻结 Exact v1

ID: UM-NORMALIZED-FLAT-CARTESIAN-TENSOR-REVERSE-AMPLIFICATION-v1。
作者 boss11 内部 typed_edge_gap，2026-10-18。先发完整 Exact，不附作者 Proof，供新 reviewer 独立攻击。本页是一个明确 tensor 操作的精确反候选，不是近二 hardness 源。

## 1. 基例与符号

U={0,1,2,3}，严格按下表识别为 GF(2)^2；加法均模2。

| u | (a,b) |
|---|---|
| 0 | (0,0) |
| 1 | (0,1) |
| 2 | (1,0) |
| 3 | (1,1) |

基例有两个 groups g∈{0,1}；每 group 有两个 indexed states ℓ∈{0,1}。state 支持为

S_(g,ℓ)={(a,b):b+ga=ℓ}，每项权1/2。

即 g0 的 states 是 {0,2} 与 {1,3}，g1 的 states 是 {0,3} 与 {1,2}。没有其它资源、states 或权。每 state 的两项总质量1。

## 2. 唯一讨论的 t-fold Cartesian 操作

整数 t≥1。groups 是全部 t-bit 向量 g=(g_1,...,g_t)∈{0,1}^t，resources 是全部 u=(u_1,...,u_t)∈U^t。每 group 有全部 t-bit indexed states ℓ=(ℓ_1,...,ℓ_t)∈{0,1}^t。

state (g,ℓ) 的支持精确为逐坐标 Cartesian 积

S_(g,ℓ)=∏_(i=1)^t S_(g_i,ℓ_i)
       ={((a_i,b_i))_(i=1)^t: b_i+g_i a_i=ℓ_i 对每i成立}。

它有恰2^t个 distinct resources，各项 private 权2^(−t)，总质量严格1。不同 indexed states、groups、resource tuples 都按上述显式标签区分；没有把一个资源复制成独立的 incidence-only 私有物品。

## 3. 完整 ordinary unrelated P_t

每 resource u∈U^t 一台 resource machine R_u；每 indexed state (g,ℓ) 一台 private machine M_(g,ℓ)。每 group g 恰一件 unit selector J_g，只在本 group 全部 M_(g,ℓ) 上耗时1。

每 (g,ℓ,u) 且 u∈S_(g,ℓ) 恰一件独立 incidence job I_(g,ℓ,u)，只有两个有限端：M_(g,ℓ) 上时间2^(−t)，R_u 上时间1。所有未述时间∞，无其它jobs、机器或预载。所有 indexed states 的 jobs 都必须实际执行，不只生成后来被选的 states。

V_t 定义为：给每 g 选一个 indexed state ℓ(g) 及其任意资源子集 B_g⊆S_(g,ℓ(g))，要求 B_g 跨 groups 两两不交；最大化 min_g |B_g|/2^t。允许资源不分配，不允许物品拆分或多个 owners。

## 4. 待独立攻击的 Exact Statements

(A) 对每整数 t≥1，精确有

V_t=1−2^(−t)。

特别基例 V_1=1/2，而不是把基例取幂后得到 V_1^t=2^(−t)。t=0 不在对象域：既不采用空tuple的退化group约定，也不把上式错误延伸到t0。

(B) 对第3节全部原jobs的普通实际 makespan，精确有

OPT(P_t)=2−V_t=1+2^(−t)。

Claim 包含一份全 jobs actual 上界调度及任意完整 actual 调度的下界，不把 V 的部分资源分配当作已执行完全部未选 state jobs。actual 映射不需要 t-fold 产品中的 state 选择逐坐标独立于其它 group 坐标；相反 V_t 的优化允许每 g 单独选择任意完整 ℓ(g)，这是所定义操作的实际自由度。

(C) 规模精确为2^t groups、4^t indexed states/private machines、4^t resource machines、8^t incidence jobs及2^t selectors。每 state 的支持列表恰2^t项；全部 sparse finite processing-time 条目恰2·8^t+4^t。private 权2^(−t)的位长O(t)。对象构造、见证及检验按显式实例总位长 polynomial；**不是声称输出或运行时间 polynomial in t**。若必须输出 dense P，则其矩阵有(8^t+2^t)·(2·4^t)条目，依该显式长度计费。

## 5. 准确否定范围

该族否定对第2节此裸 Cartesian-menu 操作的一般性命题“base NO V≤η 自动推出 product NO V≤η^t”：固定基例η=1/2已反向趋近1。它不同于旧 ternary-tree aligned product 因终端 palette 使 YES 完备性失真的障碍；本页只研究这里明示的 normalized flat 菜单与全部 state choices。

本页不证明任何任意 tensor、带额外一致性约束的产品、其它 group/资源定义或 particular source-compiler image 都失败。不把单纯 resource-pool 维数计数当作所有产品反例；不提供源 hardness 或对一般 UM 的算法。
