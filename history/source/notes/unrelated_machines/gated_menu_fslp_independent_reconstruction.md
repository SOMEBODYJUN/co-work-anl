# 独立重构：正支撑 FSLP 的资源最大值舍入与完整四层负载

2026-10-18。读取顺序：先收到 root 的口头 Exact（独立 state 抽样、福利至少 (1−1/e)n、b<1−e^(-1/2) 时四层 C≤2−b）；本稿独立重构后才读取其正式 Exact 文件，尚未接触作者 Proof。此前读过旧 normalized-NSW 页，但本证明不依赖旧 NSW 机制或其证明。

## 1. 输入与输出合同

n≥1 个 groups，有限资源 U，组 g 有非空显式 indexed states S_g。给非负二进制有理系数 p_gsu；未列资源的系数为 0；每 state 满足 sum_u p_gsu=1。于是 U 非空。允许显式零、unused resources、重复 indexed states。给定或通过显式 rational LP 求得

lambda_gs≥0，sum_s lambda_gs=1，sum_{g,s:p_gsu>0}lambda_gs≤1 （每资源 u）。

结论：确定性 total-bit-polynomial 算法输出每组一个原 state s_g 和两两不交资源 B_g⊆{u:p_g,s_g,u>0}，r_g=sum_{u∈B_g}p_g,s_g,u，满足 0≤r_g≤1 与 sum_g r_g≥a n，a=1−1/e。算法不计算 e，也不作随机采样。

## 2. 独立 state 分布的福利下界

分析中各组独立按 lambda_gs 取 state，令 Y_gu=p_g,s_g,u，M_u=max_g Y_gu。资源 u 交给达到最大正系数的某组（固定 index 破并列），故福利 W=sum_u M_u。

对每 t>0，令 q_gu(t)=Pr[Y_gu≥t]。因 {Y_gu≥t}⊆{Y_gu>0}，正支撑 FSLP 给 Q_u(t)=sum_g q_gu(t)≤1。组间独立给

Pr[M_u≥t]=1−product_g(1−q_gu(t))≥1−exp(−Q_u(t))≥(1−1/e)Q_u(t)。

最后一步是凹函数 1−e^(−x) 在 [0,1] 上的弦界。所有权重在 [0,1]，尾积分因此给

E M_u≥a*sum_g E Y_gu。

对资源求和，E W≥a*sum_g sum_s lambda_gs sum_u p_gsu=a n。该证明仅用跨组 state 独立，不要求同组不同资源独立，也不把零 incidence 计进正支撑容量。

## 3. 精确有理 conditional expectation 与位复杂度

对每资源 u，列出它所有原 state 中不同的正系数 0=w_u0<w_u1<...<w_uL。在一个固定 state-prefix 下，已经固定的组改成其点质量分布，其他组仍使用原 lambda。令 q_gu,l 为当前分布下 Y_gu≥w_ul 的概率；它是 lambda 子集之和或 0/1。精确条件期望为

E[M_u | prefix]=sum_{l=1}^{L}(w_ul−w_u,l−1)*(1−product_g(1−q_gu,l))。

所有量都是明确有限有理数。下一组的当前条件期望等于各 lambda_gs>0 的 state 子期望加权平均；选择子期望最大的正概率 state，条件期望不下降。依次固定 n 组，最终 W≥a n。

若总 state 数 S、显式 incidence 数 I，则 sum_u L_u≤I（零项不产生新正 threshold），正概率 candidate 总数至多 S；每个 candidate 可以朴素地重算所有 q 和全部乘积。该过程仅多项式次扫描、加法、乘法和有理比较。lambda 位长若为 B_lambda，n 项概率乘积的分母位长至多各因子分母位长之和；系数差与有限求和的位长也由全部显式输入位数之和的多项式控制。没有以 1/min positive p、分母数值、1/lambda 或概率倒数作循环。若先求 LP，0/1 约束矩阵与显式规模保证可输出多项式位长 rational basic feasible witness。

最后每资源交给所选 state 中最大正 p 的最小 indexed group；无正项则闲置。各 B_g 不交，sum r_g=W，r_g≤1。全部操作位多项式。

## 4. 严格计数与精确门槛

对任意 b∈[0,1)，令 h_b=#{g:r_g≥b}。若 h_b≤bn，因为 n−h_b>0 且其它组 r_g<b，

sum r_g < h_b+(n−h_b)b ≤(2b−b²)n。

因此对所有 b 满足 2b−b²≤a，即 b≤b0:=1−e^(−1/2)，必有 h_b>bn。口头 Exact 的 b<b0 是安全范围；数学上 equality b=b0 也成立，但 b0 非有理，算法无需将其作为输入。

更一般，b<a 时 h_b>((a−b)/(1−b))*n。因此 unit-FSLP 可行不可能有 robust NO “每个实际 allocation 都少于 gamma_hi*n 个质量≥delta 的 groups”，只要 gamma_hi≤(a−delta)/(1−delta)。等号也排除。特别 gamma_hi≤delta≤b0 的整个典型近二参数区间已被这个新机制排除。

还可去掉输入 b：将所得 r_g 从大到小排序，计算每个 k=1,...,n 的 beta_k=min{k/n,r_(k)}，取 beta=max_k beta_k。以上计数蕴含 beta≥b0。全过程只比较原有理数；由此直接输出下面 C≤2−beta≤1+e^(−1/2) 的调度，不计算任何超越常数。这里不宣称此结构类的最佳近似比或新颖性。

## 5. 完整 ordinary UM 矩阵与全部任务

机器：一 root R；每组一个 G_g；每 indexed state 一个 M_gs；每资源一个 U_u。

原任务：

1. root pin：仅 R 耗时 1。
2. n 件不同 root jobs a_1,...,a_n：在 R 各耗时 1/n，在每个 G_g 各耗时 1。
3. 每组一件原 home job h_g：在 G_g 耗时 1，在该组每个 M_gs 耗时 1。
4. 每个显式 state-resource incidence 一件不同原 job j_gsu：在 M_gs 耗时原 p_gsu，在 U_u 耗时 1；其它端无限。显式零项在私有端以 0 执行，允许未列为零的资源不建 incidence。

选上节一个 k 及其 top-k 组 H。取 k 件不同 root jobs，逐一放到 H 的不同 G_g；剩余 n−k 件留 R。每个 g∈H 的 h_g 送到所选 M_g,s_g；其它 h_g 留 G_g。只对 H 的所选 states 把 B_g 对应 positive incidences 送 U_u，其余所有 incidence 留各自 M_gs，包括所有未选 states、所有不在 H 的组以及所有零 jobs。

逐机负载：

- R：1+(n−k)/n=2−k/n。
- G_g：H 内仅接一件 root unit；H 外只留自身 h_g；两者均为 1。
- H 内 selected M_g,s_g：收到 h_g 的 unit，加本地 remaining weight 1−r_g，负载 2−r_g。
- 所有其它 state machines：全体 incidence 总和恰 1。
- 每 U_u：B_g 全局不交，至多一件 unit incidence，负载≤1。

每个原任务在合法原端执行恰一次，全部机器同时满足 C≤max{2−k/n,2−min_{g∈H}r_g}=2−beta_k（beta_k≤1）。选择最大 beta_k 即得 C≤1+e^(−1/2)。若按口头 Exact 固定 rational 0<b<b0，取 H={r_g≥b}，则 k/n>b、selected r_g≥b，给 C≤2−b。root pin 保证 OPT≥1；给 unit 支撑 packing 时可外送全部 n 件 root jobs和全体所选正 incidences，达到 C=1。

## 6. 不覆盖的输入

如果只给 weighted load LP sum p_gsu*lambda≤1 而非 positive-support capacity，则第 2 节 Q≤1 失效；不能导入本结论。若 state 总量不同于 1，或 group home 有额外 compulsory weight、额外共同 coherence/AND jobs，或 root/group资格受限，则所有负载需重证。该证明没有把一般 UM 归约到此结构类，也不解决主 UM-TARGET-v1。

## 7. 审查状态

本稿的推导先于正式 Exact 实读和作者 Proof；尚无软件实施或有限实验。独立一般证明涵盖 n=1、重复 states、显式零、unused resources、zero lambda、r_g=0、全体 r_g=1、非整 bn、state 权重极小和大分母。下一步实际读取作者正式 Exact，对其额外量词/输入差异逐项攻击。
