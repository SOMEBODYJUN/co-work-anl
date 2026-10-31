# 逐机统一内部辅助的 bulk OR-commit：完整 backbone 分摊候选，仅陈述 v1

作者：fee_cascade_review，2026-10-18。此陈述沿 root 提出的共同容量 flow 方向整理，用于内部 Exact-first 重构；不声称 blind 原创路线。文件只含完整原对象、输入见证与精确输出合同，不含 Proof、推导或实验。仅 scratch，不写 repo/Work/Git，不登记成熟资产。

## 1. 参数与原 backbone

给整数 r≥2、偶数 k≥2、二进制有理 1/2<ρ<1。变量 a∈[r]；每变量环索引 i∈[2k]，后继 i⁺按本变量模 2k 循环。前 k 个索引为正 block s_i=0，后 k 个为负 block s_i=1。每环长 2k≥4，无其它 padding。

每变量有不同原机器 M_(a,i)、C_(a,i)（i∈[2k]）及两台原 pool A_(a,0)、A_(a,1)。每索引有不同原 jobs q_(a,i)、b_(a,i)，每变量有原 selector f_a。所有列出的不同变量、索引、类型的机器/jobs 均物理互异。

Backbone 的全部有限资格如下，其余为∞：

| 原 job | 全部有限原端与真实时间 |
| --- | --- |
| q_(a,i) | M_(a,i):ρ；M_(a,i⁺):1；A_(a,s_i):1/k |
| b_(a,i)，正 block i≤k | M_(a,i):ρ；C_(a,i):1 |
| b_(a,i)，负 block i>k | M_(a,i⁺):ρ；C_(a,i):1 |
| f_a | A_(a,0):1；A_(a,1):1 |

q 没有 C 端。Backbone jobs 没有下节内部 I 端或其它端。没有预载、隐含 jobs、拒绝任务、分拆或额外物理关系。

由 f_a 的实际原目的地读取 x_a：f_a→A_(a,1) 表示 True；f_a→A_(a,0) 表示 False。所测关系是 x_1∨⋯∨x_r。

## 2. 任意资格的 commit/aux 内部网络

另给有限内部原机器集 I，与全部 backbone machines 不交，以及有限原 job 集 J，与全部 backbone jobs 不交。J 包含该 committer 的**所有** guards、aux、需求任务；没有可在证明中另删的辅助任务。

每个 I 机器 h 给二进制有理 c_h≥0。J 的资格可任意、跨 branches 布线可任意，但有限端只允许以下两类：

- h∈I：若 j∈J 对 h 有限，则 p_(h,j)=c_h。即在同一内部机器上的全部有限处理时间统一，允许 c_h=0，也允许 c_h>1 的未用端；不同内部机器的 c_h 可以不同。
- 正 readout C_(a,i)，a∈[r],i∈[k]：若 j∈J 对其有限，则真实处理时间恰为 1。

每 job j∈J 至少一个有限端。J 没有负 block C、M、pool 或其它端；I 上除了 J 没有其它原 job 的资格。不同 J jobs 在同一 C 或内部机器上是否均有资格由显式矩阵决定，没有默认全连接。没有要求某 guard 在不同模式下执行在相同位置，也没有给定 guard 集中于某 branch 的免费关系。

下节 c_(a,j) 将统计**所有 J 原 jobs**在正 block C 的实际占用，包括 aux；不只统计被称为 guard 的部分。

全 P 的实际原机器数为 m=r(4k+2)+|I|，原 job 数为 n=r(4k+1)+|J|。设 E_J 为 J 在 I∪正 C 的实际 finite 条目数，则全部 finite 数为 r(10k+2)+E_J，dense 项 mn。内部零端按真实零处理，不改变 job 不可拆分和恰执行一次的要求。

## 3. 给定的 r 份完整实际 strict mode witnesses

算法输入除同一原 P 外，给 r 份实际完整合法 assignments σ^(1),…,σ^(r)，每份覆盖原全部 n jobs 恰一次，所有原 machines 的真实负载同时≤1。对每 j∈[r]，其 selector 目的地满足：

- f_j 在原 A_(j,1)，即 x_j=True；
- 所有 a≠j 的 f_a 在原 A_(a,0)，即 x_a=False。

不对这些完整实际 witnesses 的 q exports、b returns、各 job 原目的地或 J 的内部安排另作模式假设。它们不是删去 backbone 或某 aux 后的部分调度，也不是分数点/占用示意图。它们可以把 J 中不同 jobs 放在不同 branch，或在未选 branch 放 aux；这些负载全部属于前提并实际计入。

记

c_(a,j) = |{z∈J : σ^(j)(z) 是某 C_(a,i), 1≤i≤k}|，

K_a = ceil((1/r)·Σ_(j=1)^r c_(a,j))。

所有这些数都从所给完整实际 witness 原目的地读取。它们不规定新物理任务或新容量。

## 4. 精确候选结论

对上列全部 P 和所给合法完整 witnesses，可确定性总位多项式构造一份同一原 P 全部 n jobs 的实际完整分配 τ，使：

1. 全部 f_a 在其原 A_(a,0)，即实际 selector 读出全 False。
2. 全部 J jobs 仍各执行一次，使用原有限端；每台 h∈I 同时负载≤1。每正 readout C 至多一枚 J job，且每变量正 block 接 J 的数目至多 K_a；没有输出任何虚拟 job 或 machine。
3. 每原 M_(a,i) 恰执行一枚原 q 或 b，真实负载≤1；每原 C_(a,i) 恰执行一枚 unit 原 J job 或 b，负载1。每个负 pool 负载≤1/k；每个正 pool 除自身 f_a 外，执行的原 q 数量至多 max(0,K_a−1)。全部原 q/b/f/J 按身份完整覆盖，且每个只执行一次。
4. 因而所有原 machines 同时满足

   C_max(τ) ≤ B_data
     := 1 + (1/k)·max_(a∈[r]) max(0,K_a−1)
     ≤ 1 + ceil((k−1)/r)/k
     ≤ 3/2。

   r=2 且 k 偶时最后统一上界为3/2。这里不声称 B_data 或统一上界是任意输入 P 的精确条件化最优值。

同一陈述若不提供这些 witnesses、只假设 r 份完整 strict modes 存在，则只给相应 all-False 完整分配存在、conditional OPT(P|all False)≤1+ceil((k−1)/r)/k；不承诺计算未知 strict witnesses。

给定前提下原 P 的不固定 selector 的 OPT(P)=1（由 f 的全 unit 资格及至少一份完整 strict witness）。本结论的内容是全 False **指定实际 selector 读出**在弱阈值内也可出现，不能把该条件化输出界写成源 NO 或原 P 的大 OPT。

## 5. 范围、复杂度与未覆盖出口

这是对 “unit 正 C readout + 逐内部机器统一时间 aux 网络 + 上述完整共享 pool/ring backbone” 的 OR-commit 候选测试。r 份完整一真模式可以作为 OR gadget 必须保留的真实 YES 选择，但不要求原 P 已经实现 strict OR soundness；若另有 strict OR soundness，本结论仍给其弱读出失败。

所有 K_a 都计入 guards 与 aux 在 C 的占用；不能忽略未选 branch 的 aux，也不假定其免费搬走。有限原矩阵、内部 c_h、ρ、r 份完整 assignments 均按总二进制编码长度收费。r、k 为显式展开对象的计数。算法不按 c_h 的倒数、分母数值或隐式巨大 k 展开；c_h=0 和空 I/J 不导致除零。输入的所有 unused finite 条目仍属于原矩阵规模。

本候选不覆盖同一内部机器对不同 J jobs 具有不同有限时间的网络，不覆盖 J 可以执行于 ring/pool/负 C 的修改，不覆盖不同 backbone 或不足 r 个完整一真 strict 模式的实例。真实非uniform tiny/medium aux、跨多层共同容量等离开此域的路线须另立完整矩阵和全 job 见证/decoder，不能据本陈述否定其全部可能性。

没有 source NO、NP-hardness、一般 UM 求解器、软件运行、外审或全球新颖性认证。它用于决定上述准确 unit-aux commit 线路是否能挡 split，不把标准容量 flow 技术当新的主目标进展。
