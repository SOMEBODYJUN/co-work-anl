# 可变多 outer / 单 state / tiny home：19/10 Exact-first 独立重构

日期：2026-10-18。审查者：`/root/sol_nsw_independent_attack`。状态：先冻结本记录，再允许释放作者 Proof。

## 1. 精确对象、实际阅读与独立性范围

本轮唯一新增实际读取的候选文件是
`/workspace/scratch/038d9dcc4cac/sol_general_repair_multiouter_single_state_tiny_home_19_10_exact_v1.md`。
实际核 SHA256 为 `38c85ffed433edc9742f2e523ae39c820dc315454262a498ff8386b0b6cc001a`，3714 bytes、32 行、当时权限 0644；**实际完整阅读第 1–32 行**，输出未截断，并再次全文复核了同一 32 行。

没有打开本候选的作者 Proof、算法学习记录、代码、运行输出或其他人的新审查，也没有向作者索取算法策略。作者此前另问过旧 SA3 接口，我只给了旧 Exact 的路径和 hash，并明确请其不要发送本候选的 Proof/code/strategy。本轮不读其他新文件，不读或改 repo、Git、Work 或 token。

这不是无背景方向盲审：我已知单 outer 的 primitive-SA1 思路、多 outer 条件点不能免费拼接的障碍、普通 flat 全 jobs 的阈值语义；也参与过 raw-K2 反例和 SA3 接口审查。以下是**只依据本新 Exact 的输入域与结论、独立构造的一套充分算法**，并非对未读作者算法的复述。它不用 raw-K2、PSD、unit-FSLP 或给定实际 joint law。

结论：未发现本 Exact 的数学 fatal；下文给出从 Q 本身出发的确定性总位多项式 19/10 算法。它只支持该 typed 子域，不推出一般 UM 算法。本记录没有端到端实现；唯一软件辅助是独立的几个 Fraction 常数反算，不是作者代码或完整算法测试。

## 2. 记号和第一层显式判定

用 j 表示一个 home/helper，i(j) 是其 outer，权重为 w_j。n 是全部 helpers 数，k>=1，

    sum_{j:i(j)=i} w_j=1,
    w_j<=d:=1/(4096 k^4),
    sum_j w_j^2<=k d=1/(4096 k^3).

固定使用

    epsilon=15/16,  T0=2-epsilon=17/16,  theta=1/10.

从 Q **显式建立并求解 Exact 第 30 行的完整 common primitive-SA1 LP** R_epsilon：原 A/Z 的所有 base rows、每个原 primitive 及其补的乘积、共同对称表和 Boolean diagonal 全保留。不是只解 first-moment LP，不用预给点。变量、行、系数编码总量均为输入的多项式；boxes 的条件行使所有一、二阶变量在 [0,1]。确定性有理 LP 算法可判 infeasible 或返回有理可行点，其位长可取多项式。

所有实际 C<=T0<2 的普通调度都给出 R_epsilon 的一个整数可行点：取 selector 所在 state，所有 inactive-state jobs 放回各自 private，全部 zero jobs 也放 private；inactive private 的 payload 总量是 1，故不增加到 T0 以上。每个 active private 的原负载约束迫使其正 payload 至少 epsilon 被 export。resource 上每个 incidence job 时间 1，T0<2 保证至多一个。因而 canonical gates、quality、cap 和全部 SA1 行都成立。这里是**实际调度的存在性 canonicalization**，不声称任意 raw 分数点可按积映射拉回。

若 LP infeasible，则 OPT(P)>17/16。把所有 payload 放其原 private、每个 selector 放该 group 的任意一个原 private，得到完整原 job 调度 C<=2。因此

    C/OPT < 32/17 < 19/10,
    19/10-32/17=3/170.

以下只考虑 LP feasible 的分支。所有 groups 有 unit selector，故 OPT(P)>=1；这个分支只需构造 C<=19/10。

## 3. 从同一 SA1 点提取一个全局 fallback 分数解

记 outer 在 home j 的正 incidence 的一阶 claim 为 b_j。outer 只有一个 indexed state，partition 及其条件行使其 A=1，故

    sum_{j:i(j)=i} w_j b_j>=epsilon.

helper j 的 own state 记 A^o，own 正 unit incidence 记 Z^o。归一化 own quality 是 Z^o>=epsilon A^o。将它乘 (1-Z^o)，用 Boolean diagonal，得到

    L(A^o Z^o)>=L(A^o).

box A^o 乘 (1-Z^o) 给反向不等式，故这两者相等。box (1-A^o) 乘 Z^o 再结合 gate Z^o<=A^o，得到

    L(Z^o)=L(A^o).

若需要，该 gate 的零一阶 slack 及它乘每个 primitive/补的两条非负行还给出两者的全部二阶行相等；下文只使用一阶等式。这个 singleton 推论确实使用 SA1，不能免费从 first-moment quality 得到。

令 lambda_{js} 为 helper 各 fallback state 的 A 一阶边际，f_j=sum_s lambda_{js}=1-L(A^o)。令 z_{jsu} 为对应正 fallback claim 的边际。home cap 中保留所有 jobs，特别推出 b_j+L(Z^o)<=1，因此

    f_j>=b_j,
    0<=z_{jsu}<=lambda_{js},
    sum_u p_{jsu} z_{jsu}>=epsilon lambda_{js},
    sum_{j,s} z_{jsu}<=1  (u in B).

没有 fallback 的 helper 取 f_j=0。zero incidences 对资源 cap 可能有额外非负贡献，但忽略它们只使以上不等式更弱，最后会把其原 jobs 放 private。所有上述数来自**同一份** LP 点，无不同 outer 条件点的拼接。

## 4. 一个显式构造的独立 state law 与统一 weighted welfare 下界

为每个 helper 独立选一个 fallback state s，概率 lambda_{js}；剩余概率 1-f_j 选 null。null 只表示本阶段不取 fallback，不删除原 own state 或任何 jobs。此人为独立 law 由 LP 边际显式定义，不声称它等于 LP 的二阶相关表。

给定一个 state profile t，令 a_{ju}=w_j p_{j,t_j,u}，null 时全为 0。对 alpha 在全单纯形 Delta_k，定义

    F_t(alpha)=sum_{u in B} max_j { alpha_{i(j)} a_{ju} },
    G(alpha)=E_t F_t(alpha).

F_t 是给定 clauses 后的最大加性 weighted welfare，resource 逐个给最大系数的 helper。每个 outer 的 aggregate welfare 均至多 1，所以 F_t(alpha)<=1；其一个 subgradient 的每个坐标都在 [0,1]。

证明对所有 alpha 同时有 G(alpha)>=1125/2048：在选 state 后，另外以 z_{jsu}/lambda_{js} 的概率请求 u（lambda=0 时 z=0）；不同 helpers 的试验独立，同一 helper 跨资源无须独立。对固定 u 和正阈值 x，各 helper 提供 value>=x 的概率 q_j 满足 sum q_j<=sum_{j,s}z_{jsu}<=1。于是

    Pr(max requested value>=x)=1-prod_j(1-q_j)
        >=1-exp(-sum q_j)>=(5/8)sum q_j.

最后一步用 1-exp(-x)>=(1-exp(-1))x 及 e>=8/3；这是证明中的常数，不需算法计算指数。积分阈值，且 F_t 可以选择所有 requests 的每资源最大者，得到

    G(alpha)>=(5/8)sum_{j,s,u}alpha_{i(j)}w_j p_{jsu}z_{jsu}
        >=(5/8)epsilon sum_j alpha_{i(j)}w_j f_j
        >=(5/8)epsilon^2=1125/2048.

这里没有要求 requests 全局可同时满足：每个 resource 只保留最大请求，而 F_t 正是逐资源最优。各资源间状态相关不妨碍期望求和。

## 5. 条件期望及 subgradient 均可精确有理计算

在任意一部分 helpers 已固定 state 后，余下 helpers 仍按上述独立边际选 state。记相应期望函数 G_D。对固定 u，列出候选值 alpha_i w_j p_{jsu}，null 值 0；对每个 helper，它是有限离散变量，不同 helpers 独立。排序这些有理候选值，用逐阈值的

    Pr(max<x)=prod_j Pr(value_j<x)

即可精确算 E max，继而算 G_D。无需枚举 state profile，单个 resource 的排序与概率乘积次数均为显式输入的多项式。

在 alpha 处对 ties 用固定次序挑 winner。节点 (j,s) 成为该资源 winner 的概率为 lambda_{js} 乘其他 helpers 的“值更小，或相等但 tie 次序靠后”的概率之积。把它乘 w_j p_{jsu}，按 outer 求和，得到精确有理 g_D(alpha)。每个 profile 中选中的 winner 是 alpha 处的最大线性项，因此

    G_D(beta)>=G_D(alpha)+g_D(alpha) dot (beta-alpha)

对全部 beta 成立，且 0<=g_{D,i}<=1。已固定 helpers 的边际改成 0/1；不除以某个可能极小的条件事件概率。zero 或重复 indexed states 不造成困难，ties 以索引打破。

## 6. k>=2 的确定性 state 选择：一个可计算的强凸势

设

    beta=1/(8k),  K={alpha:sum alpha_i=1, alpha_i>=beta},
    lambda=1/4,
    V(D)=min_{alpha in K} [G_D(alpha)+(lambda/2)||alpha||_2^2].

lambda 是这里的正则化常数，不是 state 边际 lambda_{js}。初始 V>=1125/2048。

对下一个未固定 helper j，比较固定到 state s 与把它移除为 null 的函数。固定其余 state profile 时，该差为

    H_s(alpha)=sum_u [alpha_{i(j)}a_{ju}-max_{h!=j}alpha_{i(h)}a_{hu}]_+.

在一个线性片段里，若 j 在 u 上胜出，原最大者的未乘 alpha 系数 c 满足 alpha_l c<=alpha_{i(j)}a_{ju}，而 alpha_l>=beta。因此该片段梯度的 l1 范数至多 sum_u a_{ju}(1+1/beta)。沿线段分片即可推出 H_s 在 K 上对 l2 范数是

    L_j=(1+8k)w_j

Lipschitz。取其余 state 的期望保持同一界，null 也符合该界。

记未固定 j 的平均目标为 J_bar，固定 state s 的目标为 J_s，两者包含相同的二次项。令 alpha_bar 最小化 J_bar。差 delta_s=J_s-J_bar 是 2L_j-Lipschitz，且 E_s delta_s(alpha_bar)=0。lambda-强凸性给

    J_s(alpha)>=V(D)+delta_s(alpha_bar)
                     +(lambda/2)||alpha-alpha_bar||^2-2L_j||alpha-alpha_bar||
              >=V(D)+delta_s(alpha_bar)-2L_j^2/lambda.

对 alpha 取最小再对 s 平均，得到

    E_s V(D | j=s)>=V(D)-2L_j^2/lambda.

这是对同一人为独立 law 的一个可计算势的递推；没有声称条件点仍满足原 SA1，也没有重新求 LP 后免费保住更高阶条件。

下面给出计算 V 所需的确定性有理算法，不把凸优化器或精度参数作为输入 oracle。统一取 tau=1/(1024n)。对 J=G_D+(lambda/2)||alpha||^2 从 uniform alpha 出发做投影 subgradient：

    h=tau/(4k),  H=ceil(8k/tau^2),
    alpha_next=Proj_K(alpha-h(g_D(alpha)+lambda alpha)).

投影到 K 是先减 beta，再投影到总质量 7/8 的非负 simplex；排序并求有理阈值即可精确完成。J 的 subgradient 范数平方<=4k，K 直径平方<=2。标准一步投影不等式求和直接给

    min_{r=0,...,H-1}J(alpha_r)-min_K J
       <= 1/(hH)+2hk <= tau.

所以观察到的最小目标 v_hat 是 [V,V+tau] 内的**可计算有理上估计**，不依赖未给的求解 oracle。每个正概率 state 都做这项计算，取 v_hat 最大的 state；真实新势至少是旧势减 2L_j^2/lambda 再减 tau。顺序处理 n 个 helpers，误差总和 n tau<=1/1024<1/256。

tiny-home 条件支付的总损失是

    sum_j 2L_j^2/lambda
       <= (1+8k)^2/(512 k^3)
       <= 289/4096  (k>=2).

最后一步因 64/k+16/k^2+1/k^3 随 k 递减，最坏 k=2。最终 profile t 因而满足

    min_{alpha in K}F_t(alpha)
       >=1125/2048-289/4096-1/256-1/8
       =1433/4096.

这里最后的 1/8 是 lambda||alpha||^2/2 的统一上界。对任意 alpha in Delta_k，令 alpha'=(7/8)alpha+(1/8)uniform。由 F_t 的凸性和 F_t(uniform)<=1，

    F_t(alpha')<=(7/8)F_t(alpha)+1/8.

所以最终对整个 Delta_k 有

    min F_t >=(8/7)(1433/4096-1/8)=921/3584
             =1/4+25/3584 >1/4.

## 7. k=1、给定 states 的 allocation、以及 threshold repair

k=1 时无需上面的势。alpha=1 唯一，G_D(1) 可精确计算。逐 helper 选条件期望最大的正概率 state，最终 F_t(1)>=1125/2048>1/4，仍为多项式。这不是把 k 视为固定常数的网格枚举；k>=2 的统一算法也完全没有指数 k 的枚举。

现在对所得 fixed fallback states 解一个**显式有理 allocation LP**：每个 u 给 helpers 的分数总和<=1；每个 outer 的 aggregate sum_{j:i(j)=i} w_j sum_u p_{j,t_j,u}x_{ju}>=1/4。它可行：这个 LP 的 max-min 值正是 min_{alpha in Delta_k}F_t(alpha)，由有限 LP 对偶性得到，前节已给严格大于 1/4 的界。

为每资源加未分配 dummy，使其 fractions 和为 1，并取可行 polytope 的一个 vertex。若资源 u 有 d_u 个正分数，则其原产品 simplex 的该 face 维数为 sum_u(d_u-1)；k 条 utility inequalities 在一个 vertex 最多消去 k 维。因此 sum_u(d_u-1)<=k，至多 k 个资源被 split。把所有 split 资源均置为未分配，其余资源完整分给唯一正 helper。这是可直接执行的有理 LP/basic-point 操作，不借未知 integral benchmark。

每丢一个资源，对任意 outer 的 aggregate 损失至多 d，因为 w_j p_{j,t_j,u}<=d 且资源 fractions 总和<=1。记新 integral fallback quality 为 q_j in [0,1]，则

    W_i:=sum_{j:i(j)=i}w_j q_j>=1/4-kd>=1023/4096>19/100.

仅保留 q_j>=theta=1/10 的 helpers 选 fallback，并保留它们被分到的 B 资源；其余 helpers 改选 own home，释放它们的 B 资源。把保留 fallback helpers 的 home 给其 outer。设这批 homes 对 outer i 的总权重为 r_i，因为所有 q_j<=1，

    W_i<=theta+(1-theta)r_i,
    r_i>=(W_i-theta)/(1-theta)>=theta.

最后一步用 W_i>=19/100=theta(2-theta)。因此每个 outer 得质量>=1/10；被保留的 helper fallback 质量>=1/10；其余 helper own 质量 1。全部使用同一份 integral B allocation，homes 两两不同且与 B 不交，所以同一个 item 的全局 disjointness 是逐项成立的。

## 8. 回到全部 ordinary jobs，不丢零与 inactive payload

给每个 group 的 selector 放到刚选的 state-private。对选中 state，恰将上述分配资源对应的正 incidence jobs 放该资源端，其他 jobs 放其自己的 private。所有未选 states 的原 payload jobs 全放各自 private，**所有列出的 zero incidence jobs 也都放原 private**。不存在删除 inactive jobs、删除 duplicate state、压缩状态索引或复用不同 private 的步骤。

每个 active private 负载是 1+1-quality<=19/10；每个 inactive private 负载是 1；zero jobs 的原 private 时间是 0。每个 resource 至多一个原 incidence job，负载<=1。unused resources 留在原矩阵中即可闲置。所有 selectors 与每个 listed incidence 均分配到原有限端点。

矩阵仍恰为 S+U 台机器、G+I 原 jobs、S+2I 个有限资格单元，不把 fallback state 的可能相同向量合并。k>=1 且每 outer 的正权和为 1，所以 n>0，不发生 tau 除零；无 fallback 的 helpers 由 null/own 情形覆盖。所有输入有理分母任意二进制长度，没有额外下界或 numeric-unary 假设。

## 9. 总位多项式与审查判定

源 R_epsilon 和最后 allocation LP 都是显式多项式大小、有理编码 LP，可用通常确定性 LP 算法返回有理点/vertex；固定点位长由基本解 determinant 界给多项式。前者是实际从 Q 求解，后者的可行性由本文对偶界证明。没有精确 SDP、实际 OPT 或 integral feasibility oracle。

中间条件期望每次仅排序显式 state/resource 值、做概率之和与跨 helpers 之积。所有可能 subgradient 系数的分母均可由全部 source 边际和输入 p,w 的分母的一个共同乘积控制，位长为显式输入及源点位长的多项式；状态固定只将部分概率换成 0/1。候选 state 总数至多 S，投影次梯度每候选做 O(k n^2) 次迭代。投影仅排序、加减乘有理常数、除以<=k 的整数。可给全部坐标保留共同分母：每步分母位长仅增加一个多项式界，故全部 O(k n^2) 步后的精确有理位长仍为多项式。目标求值包含平方，但不把平方后的分母递归当下一步坐标分母。全算法次数与位运算次数均为**绝对常数次多项式**，无 k 相关的多项式指数。

在此范围内我有一个完整的独立重构，未发现 fatal。核心新增承重是：同一 global fallback 点；期望 weighted maximum 的 5/8 界；带 floor 的 Lipschitz 差；强凸势的逐 helper 损失；可计算的有理投影次梯度近似；以及至多 k 个 split item 的最终舍弃。各步共同使用原 resource capacity 1，而非分开给不同 outer 重新记容量。

本轮实际软件：仅一段独立 Fraction 常数运算，核 1433/4096、921/3584、超出 1/4 的 25/3584、1023/4096 与 19/100 的差 6119/102400，以及比值差 3/170。未实现或测试完整 LP/状态选择/调度算法；未读作者代码、Proof 或运行结果。因此结论是**数学算法规格被独立重构支持**，不是软件实现认证，也还不是作者未读 Proof 的读后 PASS。

本结果严格限于可变 k、每 outer 单 fixed indexed state、互异 homes、每 home 一个 own-singleton helper、任意显式 normalized B-fallback、无额外 groups、w_max<=1/(4096k^4) 的输入域。一般 normalized Q、multistate outer、重叠 home、一般 UM 等均不在结论中；全球新颖性未认证。算法仅数学规格，无端到端实现。以前其他对象上的反例不因此追认或撤销。
