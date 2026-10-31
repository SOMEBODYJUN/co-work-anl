# 单位源共同优先级世界：允许事后取消且合法购买整条 IC

2026-10-23，relay 一般候选接口。任意人数、任意有限共同目录、每个完整有序历史纯 SPE。**已证的是下述耦合、守恒和整条 IC 归约；未证明最后总体费用界，也未证明 half。** mixed 收到精确定义后已独立重构源归一、适应取消及 SOURCE-NET 继承；shared另读完整稿核对单位源、适应Gamma及适应路径排序witness无异议。费用界仍未证。

本页接 `predictable_activation_transport.md`，不改旧冻结、不改原 sigma，不将依钟 sampled utility 当原 IC。固定原实际叶 Z、覆盖 C、实际收益 u_i，最优 T 与 owner 分割 Q，O=union T、R=O\C、I=C intersect O、G=C\O。

## 1. 先固定实际 Hall-A 的可行取消多面体

采用 round3 credible 的 `../../round3/credible/owner_hybrid_transport.md` 中实际 equal-share Hall-A。其 role 边只用实际 I，边容量是原真实等分份额；每个 R 终点容量1；source i 是 b_i^G=u_i(Z;G)。令 Gamma 为全部可行取消 gamma 与 role 流 f 的多面体，再附加同时成立的局部总取消下界

    gamma_i=sum_(x in Q_i intersect R)gamma_x
       >=delta_i=min{b_i^G,|Q_i intersect R|}。

由已证的局部指定取消扩充引理，Gamma 非空。它是有界闭有理多面体，且所有元素满足

    0<=gamma_x<=1，    sum_R gamma_x=|G|，
    gamma_i+out_f(i)-in_f(i)=b_i^G。

这里只固定这个**原实际等分预算的同一可行集合**，不换成依优先级的利润定义，不另领取 I/G 份额。

## 2. 一个共用世界里，每个客户始终有一单位源

取所有角色共用的一组独立 Uniform(0,1) 优先级 U_1,...,U_m。每个 x in R 固定自己的阈值 tau_x=U_o(x)。角色 j 对此 x 激活，当且仅当 U_j>=tau_x；owner 本人总激活。

所有 x **无条件各有一单位 token**，从 owner 查询 (o(x),T_o(x)) 开始。在每个合法原实际-prefix查询状态 s=(i,a)，用前页定义的未来 coverer 集 F_s(x)：没有激活 coverer 就吸收，否则跳至索引最小的激活未来 coverer，其查询主题仍是该真实叶所规定的主题。状态 query 在其原实际前缀重置，之后沿原 sigma。

每个 token 的角色严格增加，所以每个世界 U 中恰在一个状态 s_x(U) 吸收一整单位。不同 owner 的阈值可以不同；这不妨碍共享同一个 U，也不要求客户过程相互独立。

条件 U_o=t，令 p=1-t，其它角色的激活独立 Ber(p)，owner 强制激活。对单个 x，这正是前页固定 p 过程条件 owner 激活后的分布。因此

    P_U(s_x(U)=s)=A_s(x)，

即前页积分 dp/p 的吸收量。原初始 owner 状态的概率为1/c_s(x)，非owner状态仍至多1/[c_s(x)(c_s(x)+1)]。

这个构造不是让所有客户强行共享一个 p；它用各自 owner 阈值把相同的逐客户边际放入一个所有源均存在的共同世界。路由只依赖 U 之间的次序。几乎处处优先级严格，因此所有终点可按 m! 个等概率角色排列准确描述。

### 任意适应路径也保留状态上界

在这个单位源世界，可以将“最早激活 coverer”进一步放宽为：只要存在激活未来 coverer，就任选其中一位；可以观察完整 U、全部客户、真实单价后再选择。只禁止在尚有激活未来 coverer 时提前吸收。状态 query 仍限于本页固定的原实际-prefix查询图。

现在不再保证前页最早路由的固定吸收边际或 Markov 递推；但更直接的排序 witness 保留关键上界。若一个非owner状态 s=(i,a) 最终吸收 x，则必有

    U_i>U_o(x)>max_(j in F_s(x))U_j。

这里 owner、i、未来 F 互异。若 k=|F|，上述事件要求 i 在这 k+2 位中最高、owner 次高，概率恰1/[(k+1)(k+2)]。所以即使状态与路径依全世界适应，仍有

    P(s_x(U)=s)<=1/[c_s(x)(c_s(x)+1)]。

初始 owner 状态是否吸收只取决于它有没有激活未来 coverer，故其概率仍恰1/c_s(x)。这不按 U 条件化原 IC，而是对最终非负吸收系数作无条件事件上界。若适应路径还使用独立额外随机数，同一个事件包含证明仍成立。

## 3. 观察完整世界后，从同一 Gamma 中选择取消

任取可测选择 (gamma(U),f(U)) in Gamma，可以依赖全部优先级及全部客户的终点。在该世界把 x 的最终吸收减为 rho_x(U)=1-gamma_x(U)。可以先路由完整一单位，再取消终点质量；这是证明中的非负运输，不是玩家需要提前观察的策略。

每个世界精确有

    sum_x rho_x(U)=|R|-|G|=OPT-W。

因此允许这种事后取消**不会**像共享 p 的随机注入那样改变源归一，也没有把 G 取消多算。对状态定义确定性期望吸收

    A_s^rho=E_U sum_(x in R)rho_x(U) 1_(s_x(U)=s)。

它们非负且总和 OPT-W。由于 0<=rho<=1，每个客户每个状态仍受原 uncancelled BETA2 上界支配；没有要求 rho 与到达事件独立。**不能**把该上界再乘平均残源 E rho_x：适应取消后一般只能保留无缩放的未取消上界。

## 4. 整条 IC 始终只乘确定性常数

令 D_s 为固定查询状态的原完整真实收益。所有带正吸收的状态都覆盖某个 R 客户，所以 D_s>0。定义

    w_s=A_s^rho/D_s，
    K_i=u_i sum_(s at i)w_s。

这些是取完期望后的非负常数。原实际-prefix的完整 SPE IC 给 D_s<=u_i，故

    OPT-W=sum_s A_s^rho<=sum_i K_i。              (LEGAL-COST)

没有按 U 条件化原 IC，也没有在被积式上插入依 U 的权。任意可测取消选择只改变这些合法常数的数值。

设带正吸收状态的真实付款单价为 r_s=u_i/D_s（完整 SPE 时 r_s>=1）。则精确有

    sum_i K_i
       =E_U sum_(x in R)(1-gamma_x(U))r_(s_x(U))。 (COST)

## 5. 原 SOURCE-NET 同时保留

令 bar-gamma=E gamma(U)、bar-f=E f(U)。Gamma 凸且固定，所以均值仍在同一 Gamma；净实际库存为

    eta_i=u_i(I)+bar-gamma_i，    sum_i eta_i=W。

角色 i 的初始 source 当次吸收，不超过所有自有 R 客户的 uncancelled source 吸收之和：

    A_i^src<=sum_(x in Q_i intersect R)1/c_(i,T_i)(x)
             <=D_(i,T_i)，
    K_i^src<=u_i。

若 b_i^G<=|Q_i intersect R|，Gamma 的局部约束给 bar-gamma_i>=b_i^G，故 eta_i>=u_i。否则 Gamma 强迫该 owner 的全部 R 客户逐世界取消，source 吸收恒0。因此仍同时有

    K_i^src<=eta_i，    eta_i-K_i^src>=0。

这一继承不使用 gamma 与优先级独立；只用取消非负、uncancelled 源概率及固定 Gamma 的局部约束。后续 K_i^in 仍未付。

## 6. 新的适应自由度，以及准确的未证终点

先采用最早路由，对每个排列世界选择 Gamma 内最省费用的取消，定义

    V_adapt=E_U min_((gamma,f) in Gamma)
               sum_x(1-gamma_x)r_(s_x(U))。        (ADAPT)

可以预先固定 Gamma 顶点的字典序破平局。只有有限 m! 个排列世界，所以选择和期望不涉及可测性问题；它只是在每个世界求一个有限有理 LP。

由 (LEGAL-COST)，**若能证明对每个原完整 SPE 总可选择最优 matching/owner，使 V_adapt<=W，则闭合 half。** 本页未证明这一全称费用界。

这个接口至少容纳任一固定取消方案：

    V_adapt<=min_((gamma,f) in Gamma)
                  E_U sum_x(1-gamma_x)r_(s_x(U))。

因此将取消放在期望内提供了真实的适应自由度；并不宣称在某个输入必有严格改善。它与逐角色 NET 不同，只要求总费用，不要求每行到达权<=1。它也没有自动解决多客户在同一角色提出不同查询的 collision。

还可使用第2节的适应路径自由度。对每个 x、U，取其固定查询图中所有可由激活 coverer 路径到达的强制终止状态，令

    v_x(U)=min_(这些终止状态 s) r_s。

严格递增的角色保证该集合非空；通过有限图逆序递推可确定最小值及固定破平局路径。定义更弱的充分费用

    V_best=E_U min_((gamma,f) in Gamma)
                sum_x(1-gamma_x)v_x(U)<=V_adapt。

路径与 Gamma 均按同一个世界同时选择，前述 LEGAL-COST、SOURCE-NET 和无缩放 BETA2 仍成立。若 V_best<=W 可闭合 half；**本页同样未证明这条全称费用界**。

这不是说随机化本身优于所有确定性付款：若彻底取消强制终止/rank-cap条件，允许在任意查询状态直接吸收整单位，则会退化成确定性最低查询单价问题，且未必保留这些上界。这里保留 rank-cap 与源预算，避免将表示变化本身当作新增总体付款。

更准确地说，允许适应取消的“单位源world”也可由旧均分流的unit roulette路径实现，本身不是只有本构造才有的能力。这里特有的新增定量控制是：固定owner阈值后，任意依全world选自然后继路径仍保留fixed-state无缩放BETA2，并同时保留源预算。没有因此增加一条总福利付款不等式。

当前解析关系除原实际-prefix的完整比较D_s<=u_i外，没有在费用上界中实质调用所有孩子内部IC；原sigma只固定了真实查询图。OFF-IC等全树关系若要控制同一费用，仍须处理整条比较的跨客户广播与实际C迁移，不能把本页合法系数归约叫作已经完成的IC解耦上界。

下一承重点是证明 V_best 的普遍总费用界（或放弃局部delta后的 V_0，见 `adaptive_cancellation_cut_formula.md`），或者用更强合法全树路由进一步降费。源归一、固定 Gamma、随机终点与常数 whole-IC 系数必须保持同一个合同；不能把它们分别优化后当作同一方案。
