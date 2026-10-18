# Binary Cartesian 菜单的 block-fiber 精确配额与无环链逃逸：冻结 Exact v1

候选 ID：UM-BINARY-CARTESIAN-BLOCK-FIBER-QUOTA-v1。

状态：自足精确陈述，供新的 Exact-first 独立重构；本文件不含作者 Proof。下面的 block-fiber 条件是明确的逻辑选择限制，没有声称由 ordinary UM 机器/任务实现。它与先前裸 Cartesian 反向放大使用同一完整实际 P，但优化的 admissible state 选择族不同。

## 1. 完整 binary Cartesian 对象

整数 t≥1，n=2^t。groups 为 g∈F_2^t，resources 为 (a,b)∈F_2^t×F_2^t。每 group 有全部 indexed states ℓ∈F_2^t，state 支持

    S_(g,ℓ)={(a,b): b_i+g_i a_i=ℓ_i，i=1,…,t}。

加法与乘法均在F_2。每state恰有n枚不同resources，每项private权1/n，总量严格1。资源各坐标也可按(a_i,b_i)↔2a_i+b_i识别为{0,1,2,3}，不把同一resource按不同incidences复制成私有物品。

对应完整 ordinary UM 矩阵P_t：每resource一台R_(a,b)，每indexed state一台M_(g,ℓ)，每group一件selector J_g，在自己全部state机器时间1；每原incidence (g,ℓ,u)、u∈S_(g,ℓ) 一件独立job，只能在M_(g,ℓ)时间1/n或R_u时间1。其它资格∞。全部states的全部incidence jobs均保留，没有新增逻辑守卫或其它实际任务。

## 2. 固定 partition 与 block-fiber admissibility

固定坐标集合[t]的非空blocks partition I_1,…,I_k，b_j=|I_j|≥1，Σ_j b_j=t。各block内坐标顺序固定。

一个state选择族 ℓ(g)、g∈F_2^t，称为 block-fiber admissible，当存在函数

    F_j:F_2^{b_j}→F_2^{b_j}，j=1,…,k，

使所有g均有 ℓ(g)|_(I_j)=F_j(g|_(I_j))。每F_j允许任意非线性、常数值和重复输出；只有跨block输入依赖被禁止。F_j是全family共享的函数，不能为不同外部block坐标另选不同F_j。

对每个admissible family，每group可领取任意B_g⊆S_(g,ℓ(g))，跨groups两两不交。B_g不要求是Cartesian积或具有任何函数形式。定义

    Q(I_1,…,I_k)
      =max_(admissible ℓ, pairwise-disjoint B) min_g |B_g|/n。

优化同时遍历全部admissible nonlinear functions和任意partial subsets。

## 3. 精确配额结论

令

    H=∏_(j=1)^k (2^{b_j}−1/2)，   q=⌊H⌋。

则精确有

    Q(I_1,…,I_k)=q/2^t。

存在admissible family及共同不交B_g，使每group恰领取q枚资源。可在完整显式P_t与partition的总位长多项式时间内构造这些state选择和全部B_g；不需枚举全部nonlinear F_j或指数多份state选择族。

同时，全部admissible families的selected-support union满足统一且可达到的上界

    |⋃_g S_(g,ℓ(g))|
      ≤∏_(j=1)^k (4^{b_j}−2^{b_j−1})
      =2^t H。

此union上界与每group资源数的整数约束共同给精确floor，不能将H的分数值当作实际整数领取数。

### 参数校准

* 一个block：k=1、b_1=t，Q=1−2^(−t)，恢复裸binary family的反向放大值。
* 全singleton blocks：k=t、b_j=1，Q=⌊(3/2)^t⌋/2^t，不等于基例值的简单t次幂。
* 若所有b_j≤L，其中整数L≥1，则

      Q ≤∏_j(1−2^(−b_j−1))
        ≤(1−2^(−L−1))^k
        ≤(1−2^(−L−1))^⌈t/L⌉。

  所以固定L的此逻辑约束使Q随t指数衰减。
* 精确floor的舍入损失小于2^(−t)：

      0≤∏_j(1−2^(−b_j−1))−Q<2^(−t)。

t=1属于所有相应边界，Q=1/2；t=0不在域中。

## 4. 同一 binary family 的 acyclic-chain failure

另外固定一个特定state选择族，不再优化其labels：

    ℓ_1(g)=0，
    ℓ_i(g)=g_(i−1)， 2≤i≤t。

定义Q_chain(t)为只在这份固定family下，优化所有共同不交、任意partial B_g的最大最小|B_g|/n。则对全部t≥1，精确有

    Q_chain(t)=1/2。

其selected-support union大小精确为n(n+1)/2，并可用共同整数资源分配给每group恰n/2枚资源。t=1时该family是两个groups均选择label0，公式仍成立。

按坐标索引定义 cross-coordinate dependency digraph：j→i 表示输出label ℓ_i实际依赖输入g_j、j≠i。上述固定family只有1→2→…→t的一条无环链，每个坐标至多依赖一个其它坐标，且不含自依赖。

因此“仅要求cross-coordinate依赖无环”或“每label依赖至多一个其它坐标”，都不能保证本binary family的最优partial保留值趋零：允许的选择族已经包含这个恒为1/2的例子。这里没有声称优化全部acyclic state函数时的最大值也恰1/2；只声明这份合法固定链的精确值及其反例含义。

## 5. 完整任务、YES preservation 与准确范围

给本页任何admissible state选择和不交B_g，把selectors放所选state机器，仅导出该state中B_g对应的原incidence jobs，所有其它原incidence jobs留自己的private机。全部原jobs恰一次，实际峰至多2−min_g|B_g|/n。此是ordinary P_t上的合法调度构造，但不意味着P_t会强迫selector选择族admissible。

原P_t并未增加任何block-fiber物理约束，因而其不受限ordinary OPT仍是1+2^(−t)，不能把逻辑限制后的2−Q称为原P_t的OPT。尤其block条件下Q衰减，不自动给ordinary UM的NO实例。

该逻辑条件保留通常的逐坐标full-support YES提升：对任意另一个具有完整不交state见证的base菜单，逐坐标使用该base见证的选择函数，是每个partition都允许的block-fiber choice，其Cartesian支持仍不交。这里仅说选择条件不排除这份YES见证；没有给base归约、degree保持、实际coherence gadget或源NO decoder。

完整P_t有2^t groups、4^t private机、4^t resource机、8^t incidence jobs及2^t selectors。时间1/n位长O(t)。上界见证和整数分配均按显式实例总长度多项式构造/核验，不声称poly(t)输出。资源跨全部group menus的degree为2^t，不保持degree3。

本候选只量化一族明确的逻辑functional restrictions及一个acyclic-chain逃逸；不证明所有tensor失败，不提供实际UM一致性机制、一般算法或任何hardness。
