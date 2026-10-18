# Binary Cartesian block-fiber 精确配额与无环链逃逸：冻结 Proof v1

对应 Exact：`binary_cartesian_block_fiber_quota_exact_v1.md`。

Exact SHA256：`8d16b510b4064e6ddaaf59edb04549fc5f2eb42c19ed1356d0129efb34e30a98`。

作者/独立发现者：rank_deficiency_fee，2026-10-18。先冻结完整 Exact，再单独冻结本 Proof；未读取新 reviewer 的推导。本证明没有给 ordinary UM 添加逻辑一致性约束。

## 1. 对象与整数分配引理

取 t≥1、n=2^t。Groups 为 g∈F₂^t，resources 为 (a,b)∈F₂^t×F₂^t。State ℓ 的支持为

    S_(g,ℓ)={(a,b): b_i+g_i a_i=ℓ_i 对每i成立}。

每 state 恰 n 枚资源，每项 private 权1/n。所有运算在F₂。

先记录一个共同使用的有限二分图引理。左点为 groups，右点为不可分 resources，边表示允许领取；允许 unused resources。若存在非负分数 x_(g,u)，使每 resource 的总分配≤1、每 group 的总分配恰 H，则可令每 group 领取 q=⌊H⌋ 枚互不冲突的原 resources。

证明：对任意 group 子集 A，

    H|A| = Σ_(g∈A,u) x_(g,u) ≤ |N(A)|，

故 q|A|≤|N(A)|。把每 group 复制为 q 个同邻接 slots。任意 slots 子集若涉及 A 这些 groups，slots 数≤q|A|≤|N(A)|，其邻集正是N(A)。Hall 给覆盖全部 slots 的整数 matching。q=0时空分配也成立。最终物品没有拆分；分数仅证 Hall。亦可用整数容量最大流直接构造。

## 2. 任意 nonlinear block maps 的统一 union 上界

先看一个大小为 b≥1 的 block，写 h=2^b。任取全部 block-groups x∈F₂^b 的标签函数 F(x)∈F₂^b，不要求线性。相应支持

    T_x={(a,b'): b'+x⊙a=F(x)}，

每个大小 h。这里 b' 是 block-resource 的第二个向量，不是 block-size b。

将 block-groups 配成 h/2 对互补组 {x,x+1^b}。这两个组任意已选支持恰交一枚资源：两组方程相减唯一解

    a=F(x)+F(x+1^b)，  b'=F(x)+x⊙a。

对每 resource u，记 m(u)=#{x:u∈T_x}，c(u) 为其同时落入两端的互补组对数。互补配对在 group 集上是一个 matching，所以 c(u)≤⌊m(u)/2⌋。当 m(u)≥1 时，⌊m(u)/2⌋≤m(u)−1；m=0时c=0。每互补组对恰交一枚，因此

    Σ_u c(u)=h/2。

总 incidences 为 h²，故重复损失满足

    h²−|⋃_x T_x|
      =Σ_(u:m(u)>0)(m(u)−1)
      ≥Σ_u c(u)=h/2。

于是对任意 nonlinear F，

    |⋃_x T_x|≤h²−h/2。

现在取固定 partition I₁,…,I_k，b_j=|I_j|，h_j=2^{b_j}，∏h_j=n。对任意 admissible maps F_j，令 U_j 为第j个block的全部 selected supports 并集。完整 g 遍历所有 block-group 元组，且每完整支持是对应block支持的 Cartesian 积。因此精确有

    ⋃_g S_(g,ℓ(g)) = ∏_j U_j。

这一步使用同一F_j不随外部block坐标改变；没有对 partial B_g施加 Cartesian 条件。由单block上界，

    |⋃_g S_(g,ℓ(g))|
      ≤∏_j(h_j²−h_j/2)
      =n ∏_j(h_j−1/2)=nH。

任意共同不交 partial B_g，令 s=min_g|B_g|，则s为整数，且

    ns≤Σ_g|B_g|≤|⋃_g S_(g,ℓ(g))|≤nH。

因此s≤⌊H⌋=q，给Q≤q/n。这覆盖所有nonlinear maps及所有任意partial subsets。

## 3. 每个 block 内循环标签达到上界并给所有 groups 相同分数配额

对每 block 固定一个循环顺序，在该block令

    ℓ_i(g)=g_(next(i))。

这属于admissible block-fiber choice；singleton block的next(i)=i也允许。固定资源的a向量。两个groups g,h给出同一(a,b)当且仅当其差δ=g+h在每block满足

    δ_(next(i))=a_iδ_i。

若该block的a不全1，某a_i=0，沿block循环推出δ全部0；若a全1，δ必须是block内常数0或1，恰两个可能。因此令

    z(a)=#{j:a|_(I_j)=1^{b_j}}，

对这个固定a，每个被覆盖resource恰有2^{z(a)}个兼容groups。这里是一个线性映射的affine fiber：任意一个解加上上述kernel即为全部解，所以所有非空fiber大小一致。

将每个被覆盖resource按1/2^{z(a)}分给所有兼容groups。每resource总分配恰1。每group的selected support对每a恰有一枚resource，故它得到的总量为

    Σ_(a∈F₂^t) 2^{−z(a)}
      =∏_j[(h_j−1)·1+1·(1/2)]
      =∏_j(h_j−1/2)=H。

同时，全部resources总分配为selected union大小，全部groups总分配为nH，所以这个choice的union恰nH，达到第2节的统一上界。

由第1节整数分配引理，每group能领取恰q=⌊H⌋枚共同不交原resources。所得partial B_g不必是Cartesian积，也无需具有显式代数函数形式。结合上界得到

    Q(I₁,…,I_k)=⌊∏_j(2^{b_j}−1/2)⌋/2^t。

## 4. 校准、舍入与有界 block 衰减

单block：H=n−1/2，故q=n−1，Q=1−1/n。

全singleton：H=(3/2)^t，故Q=⌊(3/2)^t⌋/2^t。

一般有H/n=∏_j(1−2^{−b_j−1})，且0≤H−q<1，直接给

    0≤∏_j(1−2^{−b_j−1})−Q<2^{−t}。

若b_j≤L，则每因子≤c=1−2^{−L−1}，0<c<1。又k≥⌈t/L⌉，故

    Q≤∏_j(1−2^{−b_j−1})≤c^k≤c^{⌈t/L⌉}。

固定L时指数衰减。t=1时唯一partition给q=1、Q=1/2；不使用t=0退化对象。

## 5. 固定 acyclic-chain family 的精确值

固定ℓ₁(g)=0、ℓ_i(g)=g_(i−1)（2≤i≤t），只优化partial B_g。对固定a，资源方程写作

    b=(L+diag(a))g，

其中L只在(i,i−1)、i=2,…,t处为1。矩阵是下三角，det=∏a_i，所以a=1^t时可逆、rank=t；其它a不满秩。

对t≥2，取rows2,…,t和columns1,…,t−1，得到一个对角全1、只有可能上对角非零的(t−1)阶矩阵，故rank≥t−1。于是a≠1^t时rank恰t−1。t=1直接检查：a=1 rank1，a=0 rank0，与同一结论一致。

所以a=1^t时覆盖n个b、每resource恰一owner；其余n−1种a各覆盖n/2个b、每resource恰二owner。Selected union大小精确为

    n+(n−1)n/2=n(n+1)/2。

任何disjoint partial allocation的最小整数基数s满足

    ns≤n(n+1)/2，  s≤⌊(n+1)/2⌋=n/2，

因t≥1保证n为偶数。

反过来，把每resource均分给其一或两个owners。每group对每a恰有一枚resource，得到总量

    1+(n−1)/2=(n+1)/2。

第1节整数分配引理给每group恰n/2枚不可分原resources。故Q_chain(t)=1/2，含t=1。

此family的cross-coordinate依赖图就是1→2→…→t，不含自依赖、无环、每输出至多看一个其它输入。因此仅无环或仅单输入依赖，允许的选择集合已包含恒值1/2的实例，不能推出该二元族的最大值趋零。没有在此计算优化所有acyclic maps后的最大值，也没有断言所有稀疏依赖约束失败。

## 6. 实际完整任务调度与准确语义边界

完整ordinary P_t的private机器、resource机器、selectors和全部indexed-state incidences均如Exact。对任意所选state family和disjoint B_g，执行如下完整调度：selector J_g在M_(g,ℓ(g))；仅该state中B_g对应的原jobs外送各自真实R_u；其余selected incidences以及全部未选state incidences留自己的原private机器。

全部原jobs恰一次。每resource至多一件unit；unselected private负载1；selected private负载

    1+(n−|B_g|)/n=2−|B_g|/n。

因此实际峰≤2−min_g|B_g|/n。配额达界时每组恰q，峰恰2−q/n；chain整数配额给峰3/2。这些只是同一原矩阵上的合法调度。

矩阵没有读取或强制block-fiber/chain规则。它仍允许全局循环选择，实际不受限OPT=1+1/n；证明也可在此自足给出：全局循环对所有a≠1^t领取，给完整峰1+1/n。任意C<2调度中，补groups实际selector所选支持恰交一resource，那两件原incidences至少一件留在自己的selected private，与selector合计1+1/n；C≥2时下界平凡。因此不能把2−Q称为不受限原P_t的OPT，也不能从受限Q衰减推出普通UM的NO gap。

对于另一个base菜单，若它已有每base group选一个full state、且这些full supports跨groups不交的YES见证，则逐坐标使用这份见证，标签只看本坐标group。其Cartesian full supports对不同group tuples仍不交：两个不同tuples在某坐标的base groups不同，那一坐标的supports不交。逐坐标choice自动属于任意block partition的admissible class。故逻辑条件不排除该份YES提升，但这里的binary base本身并没有V=1见证，也没有给任意base的NO soundness或实际coherence gadget。

## 7. 显式构造与位复杂度

完整P_t有n groups、n² private机、n² resource机、n³ incidences和n selectors；时间1/n编码O(t)。选取block循环标签并生成每个group的n个原resource邻居，只有n²条selected support edges。

精确计算

    H=∏_j(2^{b_j+1}−1)/2^k，  q=⌊∏_j(2^{b_j+1}−1)/2^k⌋。

分子二进制长O(t+k)，q≤n，算术位数O(t+k)。无需浮点取整。用每group q个slots的普通matching，slots≤n²、边≤n³；或者直接整数容量flow。不枚举所有nonlinear F_j，也不输出2^{函数表长}个families。Hall分数分母最多2^k，亦只有O(k)位；可不把它们实际输出到构造算法。

Chain按相同有限图构造整数配额；若欲核rank，可直接使用上述结构公式，不需枚举全部assignments。所有见证与全jobs调度按完整显式P_t总位长多项式输出/核验，未承诺poly(t)输出n³ jobs。资源跨group degree仍n，不声称degree3。

这统一lemma只量化明确的block-fiber逻辑约束及固定chain反例；不把它升级为所有products不可能、一般UM算法或实际hardness。
