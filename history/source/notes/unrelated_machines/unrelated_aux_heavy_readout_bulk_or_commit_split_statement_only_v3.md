# 任意异权内部与非均匀重 readout 的 bulk OR-commit：仅陈述 v3

作者 fee_cascade_review，2026-10-18。沿 root 与作者共同推进的方向整理；不是 blind 原创性声明。此 v3 保留 v2 的任意异权内部、两实际一真见证与内部三半目标，另将全部正 C 有限端从 unit 放开为 (1/2,1] 内异权。v1/v2 原字节均不覆盖，最终只考虑成熟一个 v3 合同。本文件不含 Proof、构造策略或实验，只供内部 Exact-first 重构。仅 scratch，不改 repo/Work/Git，不预登记成熟资产。

## 1. 原 backbone 与实际 selector 读出

参数为整数 r≥2、偶数 k≥2、二进制有理 1/2<ρ<1。变量 a∈[r]；每变量有环索引 i∈[2k]，后继 i⁺按本变量模 2k 循环。正 block i∈[k]、负 block i∈{k+1,…,2k}，记相应 s_i=0、1。无其它 padding。

每变量有原机器 M_(a,i)、C_(a,i)（i∈[2k]）及 A_(a,0)、A_(a,1)；每索引有原 jobs q_(a,i)、b_(a,i)，每变量还有原 selector f_a。所有不同类型/索引/变量的上述对象物理互异。

Backbone 的全部有限原资格为：

| 原 job | 全部有限原端与真实时间 |
| --- | --- |
| q_(a,i) | M_(a,i):ρ；M_(a,i⁺):1；A_(a,s_i):1/k |
| b_(a,i)，i≤k | M_(a,i):ρ；C_(a,i):1 |
| b_(a,i)，i>k | M_(a,i⁺):ρ；C_(a,i):1 |
| f_a | A_(a,0):1；A_(a,1):1 |

q 没有 C 端。其它 backbone 端均∞，尤其不接下节 I。由 f 的**实际原目的地**读取 x_a：f_a→A_(a,1) 为 True；f_a→A_(a,0) 为 False。所测 OR 为 x_1∨⋯∨x_r。没有其它原 jobs/预载/免费标签关系。

## 2. 任意 unrelated 内部 committer

另给有限原内部机器 I，与所有 backbone machines 不交，以及有限原 jobs J，与全部 backbone jobs 不交。J 包含该 committer 的全部 guards、aux、需求任务；每 job 至少一有限端。

J 只能有以下原端：

- I 上任意显式 unrelated 时间 p_(h,z)∈有理非负数∪{∞}，可同机异权、可有零、可有未用有限值>1；**不要求**逐机统一时间或 tiny/medium 上界。
- 正 readout C_(a,i)，a∈[r],i∈[k]：每个有限端的真实时间是 (1/2,1] 内的二进制有理数，允许同机对不同 J jobs 异权，资格可逐 job 任意不同、跨 variables/branches 任意。这个范围约束全部 J 在正 C 的有限原端，不只某个输出。

J 不接负 C、ring M、pool A 或其它端。I 上除 J 外没有其它原 job 的资格。全部其它未列端为∞。不存在未计入 J 的辅助执行或隐形状态。

P 的实际 machines m=r(4k+2)+|I|、jobs n=r(4k+1)+|J|；若 J 的显式 finite 数为 E_J，则全 finite 数为 r(10k+2)+E_J、dense 项为 mn。所有 finite 为二进制有理。内部 zero 仍是不可拆分原 job 的真实端，不是可省略 job 的许可。

## 3. 只给两份不同一真完整 strict witnesses

算法输入除原 P 外，给两个不同 u,v∈[r] 及同一 P 的两份**完整实际**分配 σ^u、σ^v，均覆盖全部 n 原 jobs 恰一次、使用原资格、全部原 machines 同时真实峰≤1。

σ^u 的 selector 模式为仅 x_u=True、其余全 False；σ^v 为仅 x_v=True、其余全 False。也即相应唯一一 f 在原负 pool，其余在各自原正 pool。不需要其它 r−2 个一真模式的 witnesses。

不再对输入中 q exports、b returns、环方向、J 的 readout guard/aux 归属作任何模式约束。两 witness 可含部分 exports/returns，也可在未选 branch 的 C 上执行 aux；该占用全部计入实际负载与下列 c。

从实际原目的地定义

c_a^t = |{z∈J : σ^t(z) 是某 C_(a,i), 1≤i≤k}|，t∈{u,v}，

K_a = ceil((c_a^u+c_a^v)/2)。

所有统计包括全部 J jobs；不是只统计 guards 或额外承诺分数占用。

## 4. 精确候选输出

对全部上述合法输入，可确定性总位多项式构造同一原 P 的一份实际完整分配 τ，使：

1. 全部原 selector f_a 在其原正 pool A_(a,0)，实际读出全 False。
2. 每个 J job 恰执行一次，且其输出原目的地可限制在 {σ^u(z),σ^v(z)}。每原 I machine 同时真实负载≤3/2；每正 readout C 至多一枚 J job，每 branch 的正 C 接 J 的总数≤K_a。这里的 I 目标是3/2，**不是 v1 的≤1**；正 C 上选中的 J 使用其原真实异权时间，不改成 unit。
3. 每原 M 恰执行一枚原 q/b、真实负载≤1；每原 C（正或负）恰执行一枚原 J job 或 unit b，真实负载≤1；负 C 仍恰为自身 unit b、负载1。每原负 pool≤1/k；每原正 pool除自身 f_a 外，执行的 q 数≤max(0,K_a−1)。全部 q/b/f/J 原 jobs 各恰一次，全部原资格合法，没有实际 slot/gate/虚拟执行。
4. 输入统计必满足

   K_u,K_v≤k/2+1，且对 a∉{u,v} 有 K_a≤1。

   从而实际所有 pool 同时≤1+max_a max(0,K_a−1)/k≤3/2；连同内部 I 与 C/ring 的同时界，完整实际 C_max(τ)≤3/2。

原 P 不固定 selectors 时，OPT(P)=1；完整 strict witnesses 与 f 的 unit 资格均已提供这个事实。本结论的内容是原全部 jobs 在全 False **指定实际读出**上仍可共同负载≤3/2，不是原 P 存在较大 OPT 或源 NO hardness。

若只假设两份不同一真完整 strict modes 存在、不给 witnesses，则只给相应全 False 完整分配存在、conditional OPT(P|all False)≤3/2，不承诺计算未知 strict witnesses。

## 5. 精确范围、复杂度与未覆盖出口

本 v3 保持 v2 的任意非负 unrelated 内部 I、只需两个不同一真完整实际 modes、内部 I 目标3/2；正 C 的全部 J 有限时间改为 (1/2,1] 内任意异权，输出在每 C 至多一 J，C 的实际目标改为≤1而非恰1。J 只接 I/正 C、原 backbone 表、全部真实 witnesses 的义务保持。不能偷写任意 unrelated 内部≤1，不能把 witness 存在性当免费调度求解器。

有限矩阵、两份完整实际 assignments、所有有理时间按总二进制编码长收费。r/k 是显式展开对象计数，输出逐原 job 给实际原 machine。没有按 tiny 时间倒数、参数分母数值、ρ 的精度倒数或隐式 padding 进行伪多项式展开；空 I/J、内部零、I 上 unused finite>1 均属于域。

本候选不覆盖正 C 上时间≤1/2的 tiny 有限端或时间>1的有限端，不覆盖 J 可以到负 C、ring 或 pool，不覆盖不同 backbone 或不足两份不同一真完整实际 strict modes 的上下文。离开这些条件的真实共同容量与 source decoder 须另立完整原矩阵，不能由本结论排除其全部可能性。

无软件、有限枚举、一般 UM 新算法、source NO 或近二困难性、外审/全球新颖性认证。此结论只用于判断上述 committer 网络能否阻止真实 split/all-False 逃逸；无提前成熟资产登记。
