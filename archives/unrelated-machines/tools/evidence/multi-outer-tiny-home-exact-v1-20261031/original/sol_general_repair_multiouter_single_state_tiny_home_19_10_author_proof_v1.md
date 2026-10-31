# 作者证明：可变多个单 state outer、极小 home 权重的 19/10 算法

作者：/root/sol_general_repair，2026-10-18。对应冻结 Exact-only：sol_general_repair_multiouter_single_state_tiny_home_19_10_exact_v1.md，SHA256 38c85ffed433edc9742f2e523ae39c820dc315454262a498ff8386b0b6cc001a。此稿在 Exact-first 独立重构之前不给 reviewer；不是一般 UM-TARGET-v1 的解答，不声称新颖性或端到端软件实现。

## 1. 对象、零项与 allocation/普通 UM 恒等式

输入域、全部原 jobs 与端点严格按 Exact §1–2。将 helper 总指标记为 j，i(j) 是它的 outer，home 权重记 w_j。于是对每 i，Σ_{j:i(j)=i}w_j=1；Σ_jw_j=k，且 0<w_j≤δ=1/(4096k⁴)。一个 helper 的 own state 是 home 上的 unit singleton；其 fallback states s 的系数 p_jsu 非负、Σ_{u∈B}p_jsu=1。没有 fallback 的 helper 仍保留 own state。

本证明的辅助随机分配只对正系数 fallback incidences 请求资源。给定的零 incidence jobs 全部保留于原矩阵，最后放回自己的 private machine，处理时间 0；它们不参与随机请求。重复 indexed states 始终视为不同索引。unused resources 可以不分配。

对互不相交的资源 bundles 定义每个 group 的值为它各 indexed states 对自己 bundle 的加性值的最大值，V 为所有 groups 最小值的最大化。有限输入有有限个离散资源分配，最大值达到；0≤V≤1。

严格有 OPT(P(Q))=2−V，且 1≤OPT≤2。证明如下。给定所有 groups 值至少 v 的资源分配，为每组选择达到该值的一个 indexed state；selector 放在该 state 的 private machine，将该 state 在该组 bundle 上的正 incidence jobs 输出到 exact resource machines，其余全部 incidence jobs 留在各自 private machine。每个资源最多一个 unit job；未选 private payload 是 1；选中 private 负载至多 1+(1−v)。这完整执行全部 selectors、未选 state payload、零 jobs，给出 C≤2−v。

反向，若一个完整普通调度 C<2，每台 resource machine 最多一个 unit incidence job。每组 selector 所在 state 的 private machine 剩余 payload 至少为 1 减去该 state 已输出的总系数，故该组从输出资源获得的值至少 2−C。只保留被选 state 的输出，便得到互不相交的资源分配。若 OPT=2，上述正向式迫使 V=0；因此边界也相等。selector 是原 unit job，所以 OPT≥1。

## 2. 真正生成并求解的固定阈值 LP

固定 ε=15/16。显式生成 Exact §3 指定的 common primitive-SA1 系统 R_ε：

- 原 primitives 是每个 indexed state 的 A 与每个 listed incidence 的 Z；
- 全部 base rows 是 state partitions、boxes、gates Z≤A、资源容量 ΣZ≤1，以及每 state 的 ΣpZ≥εA；
- 每个 equality/inequality 及其乘每个同一原 primitive 或其补的 row 全部保留，以共同对称二阶数组表示，使用 X²=X。

等式乘子等式按等式编码，也可拆为两条不等式。没有 PSD、unit CONFIG、额外 U、精确 SDP 或实际分配 oracle。primitives 数为 d 时有 O(d²) moment 变量，rows 数为 O(d·(d+S+U))；全部由输入二进制有理数与固定 ε 构成。boxes 的 lifted rows 给出每个 pair 位于 [0,1]，因此标准确定性有理 LP 可行性算法返回不可行，或一个总编码长度为输入长度多项式的精确有理可行点。

若实际 V≥ε，选择一个达到阈值的 indexed state 和 disjoint bundle 为每组置 A=1、对应正 Z=1，其余置零。所有 base rows 真成立，所有原 primitive/补为 0 或 1，所以它们的所有 lifted rows 也成立。故 R_ε 不可行可正确推出 V<15/16。

在此不可行分支，输出 §1 中所有 selector 任选合法 state、全部 incidence 留 private 的完整 baseline 调度，C≤2。由 OPT=2−V>17/16 得 C/OPT<32/17<19/10。这是 actual OPT 的 sound 结论，不把 LP 不可行误说成 V≤某个更低值。

其余各节假设有精确有理可行点。

## 3. 从共同点提取 packing 数据

记一阶矩为 E。对 helper j 的 own state 及其唯一正 unit incidence，设其 primitives 为 A_j0,Z_j0。quality row (Z_j0−εA_j0) 乘 (1−Z_j0) 得

    E(A_j0 Z_j0) ≥ E A_j0.

gate (A_j0−Z_j0) 乘 A_j0 得反向不等式。box (1−A_j0) 乘 Z_j0 和 gate 乘 Z_j0 再给 E(A_j0 Z_j0)=E Z_j0。因此 E A_j0=E Z_j0；该论证只用共同二阶矩，未用 triple。own state 中给定的额外零 incidences 不进入 quality 式，不改变等式。

每个 outer 恰一个 state，partition 给 E A_i=1。设 x_j 为 outer 在 home j 的正 claim 一阶矩。home 容量（可丢弃其他非负项）给 x_j+E Z_j0≤1。设

    α_js = E A_js,   ζ_jsu = E Z_jsu,   f_j = Σ_{fallback s} α_js.

若该 helper 无 fallback，f_j=0。state partition 和 singleton 等式给 f_j≥x_j。outer 的 quality 给

    Σ_{j:i(j)=i} w_j f_j ≥ Σ_{j:i(j)=i}w_j x_j ≥ ε.       (3.1)

只保留正 fallback incidences 后，base rows 给

    α_js≥0,  Σ_sα_js=f_j≤1,  0≤ζ_jsu≤α_js,
    Σ_u p_jsu ζ_jsu≥ε α_js,  Σ_{j,s}ζ_jsu≤1.             (3.2)

当 α_js=0，gate 强制 ζ_jsu=0，不作 0/0。原零 incidences 可以在 LP 有正 claim，但丢弃它们只减小资源用量，不改变任何 quality 值。

## 4. 固定 helper 概率空间与一个有理 weighted oracle

每个 helper 独立选 fallback s，概率 α_js，或 empty，概率 1−f_j。给定所选 s，每个正 incidence u 独立请求，概率 r_jsu=ζ_jsu/α_js。可等价预先为每个 positive-mass state 的每个正 incidence 生成独立 Bernoulli coin，只读取所选 state 的 coins；总 coins 数为显式 incidence 数，未枚举 helper profile。empty 不请求任何资源。

给任意非负 outer 权重 λ_i、Σλ_i=1，资源 u 将所有实际请求者按分数 λ_{i(j)}w_jp_jsu 降序排列，平局用固定的 helper/state 索引次序，交给第一个请求者。这里只按**实际请求者**选择，永远不把资源改交给未请求但 state 已选中的人。令 helper 获得的 chosen-state 值为 Q_j，令

    W_i = Σ_{j:i(j)=i}w_j Q_j,      0≤W_i≤1.

记此 priority rule 的精确期望向量为 g(λ)。

对一个资源、阈值 z>0，helper j 有一个分数至少 z 的请求的概率是该 helper 对应 states 的 ζ_jsu 之和，记 a_j(z)。states 互斥，所以这个加法合法；不同 helpers 独立。x(z)=Σ_ja_j(z)≤1。故

    Pr(max requesting score≥z)
      =1−Π_j(1−a_j(z))
      ≥1−exp(−x(z))
      ≥(1−exp(−1))x(z) > (5/8)x(z).

最后一个常数只作实数证明使用：e>1+1+1/2+1/6=8/3。算法不计算指数。对有限个 distinct scores 的阶梯函数积分，得期望 maximum 至少 (5/8)Σ_{j,s}λ_{i(j)}w_jp_jsuζ_jsu。对 u 求和，利用 (3.2)、(3.1)：

    λ·g(λ) ≥ (5/8) ε Σ_j λ_{i(j)}w_jf_j
             ≥ (5/8)ε² = a =1125/2048.                 (4.1)

oracle 确实是有理且多项式：排序后，一个 candidate (j,s) 在 u 获胜的概率恰为

    ζ_jsu · Π_{h≠j} (1−Σ_{t:(h,t)先于(j,s)} ζ_htu).      (4.2)

同一 helper 的其他 state 不另乘；这正是共有一个 selected state 的互斥语义。将 (4.2) 乘 w_jp_jsu 并按 outer 求和即得所有 g_i。只含显式个数的加、乘、比较，不列举 state profiles。

## 5. Floored rational MW 同时提高所有 outer 均值

设 θ=1/8，η=1/32，N=1024k。初始 b_i=1。每一轮 t：

1. p_i=b_i/(Σ_hb_h)，λ_i=(7/8)p_i+1/(8k)；
2. 用 §4 的精确 oracle 得到 g_i^t∈[0,1] 和每个资源的 priority order；
3. b_i←b_i(1−ηg_i^t)。

保存 N 轮的所有 priority orders。全部 b_i 始终正，λ_i≥1/(8k)、λ_i≤1。由 (4.1) 以及 Σ_ig_i/k≤1，

    p·g^t ≥ (a−1/8)/(7/8)=869/1792.

对 x∈[0,1/2] 有 log(1−x)≥−x−x²，也有 log(1−x)≤−x。总 b 的上界与每个 b_i 的下界相比较，逐个 i 得到标准且直接可核的 inequality

    (1/N)Σ_t g_i^t
      ≥ (1/N)Σ_t p^t·g^t − η − (log k)/(ηN).

因为 log k≤k（k=1 也成立），最后两项之和≤1/16。因此

    μ_i := (1/N)Σ_tg_i^t ≥757/1792 >2/5.               (5.1)

oracle 每轮的 λ 数值只决定有限个排序；g^t 的概率表达式始终来自同一底层 helper 分布，绝不递归把 b 当新概率。更具体地，令 D_0 为所有 helper categorical probabilities 与所有预抽请求 coins 的分母之积；令 D_1 为所有 w_jp_jsu 的分母之积。两者的 log 均是输入和 LP 点长度的多项式。每个完整 helper outcome 的概率有共同分母 D_0，每个 payoff 有共同分母 D_1，故所有轮次、所有 g_i^t 都可写成分母 D_0D_1 的有理数。N 轮后 b_i 的分母可取 (32D_0D_1)^N，log 长度仍为多项式。实际算法用 (4.2) 计算，不展开指数样本空间。

## 6. 逐资源独立混合与真正的平方势方差

现在每个资源 u **独立**均匀选一个轮次 t_u∈{1,...,N}，按保存的该轮 priority order 选实际请求 winner。不同资源的 t_u 独立，helpers 的全部 state/request randomness 仍按 §4。线性性给 E W_i=μ_i；这里不使用一个全局随机轮次同时控制所有资源。

令 X_j 为 helper j 的整个独立 profile：其 selected state 与所有预抽请求 coins。X_j 的支持可能指数大，但只在以下方差证明中作为独立块使用；算法不会枚举它。给定 X=(X_j)，令

    d_u = max_{actually requesting (j,s) at u} w_jp_jsu,

空集最大值为 0。有 d_u≤δ，并且

    Σ_ud_u ≤Σ_j w_jΣ_{u requested by j}p_jsu≤Σ_jw_j=k.

条件于 X，不同资源 rule 独立，W_i 是独立资源贡献的和，每项位于 [0,d_u]。所以

    Var(W_i | X) ≤Σ_ud_u²≤δk.                         (6.1)

再令 F_i(X)=E_rules W_i。替换一个 helper j 的 profile，固定其他 profiles 和每个资源的 rule。某个资源只有在旧 j 或新 j 是 winner 时能改变 winner；所有其他候选的相对次序不变。若 outer i 的贡献被新 j 抢走，它的分数至多新 j 分数；若由旧 j 释放，它至多旧 j 分数；j 自己属于 i 时也已包含其贡献变化。因此单个资源的 i-value 变化绝对值至多

    (λ_{i(j)}/λ_i) w_j
        (p_old,j,u·1_oldrequest + p_new,j,u·1_newrequest).

资源的 rule 可不同，但每轮 λ 比值均≤8k。对 u 求和，由旧/新 state 各自 normalized（empty 为零），得到

    |W_i(X)−W_i(X with j replaced)|≤16k w_j.

这个界也适用于 F_i 的差，且包含 j 自己所属 outer 的项，不另收漏项。Efron–Stein 给

    Var F_i(X) ≤(1/2)Σ_j(16k w_j)²
                ≤128k²·δΣ_jw_j =128δk³.               (6.2)

全方差公式和 (6.1)–(6.2) 得

    Σ_i Var W_i ≤δk²+128δk⁴
                  ≤129δk⁴≤129/4096<1/25.              (6.3)

这同时控制所有 outer 的平方偏差，没有将单个 weighted objective 的提高误当作每个 W_i 的提高。

## 7. 精确 polynomial conditional expectation backend

定义固定中心平方势 Ψ=Σ_i(W_i−μ_i)²，μ_i 是 §5 的精确有理数，之后不随 CE 更新。由 (6.3)，EΨ<1/25。

依次固定：

1. 每个 helper 的 categorical state/empty；
2. 每个 positive-mass fallback state 的每个正 incidence 请求 coin；
3. 每个资源的独立轮次 t_u。

总待固定变量数、每个 categorical 的选项数及资源轮次数均多项式。每步只在原条件下概率正的选项里，选精确 conditional EΨ 最小者；概率零分支不准选择。state 固定后未选 state 的请求 coins 可照常固定，其选择不影响任何 winner。r=0 或 1 只有一个合法选项。

关键是每次 conditional EΨ 可用只涉及一个/两个资源的 winner events 精确计算。先写 W_i=Σ_u Y_iu，其中 Y_iu 是该资源 winner 对 outer i 的 w_jp_jsu，若 winner 属别的 outer 或没有请求则为零。则 E W_i 是单资源事件和，E W_i² 是单资源平方和加 distinct u,v 的两资源事件和；无需全部资源同时枚举。

单资源未固定 rule 平均至多 N 个 orders；两资源未固定 rules 平均至多 N² 对 orders，因为 t_u,t_v 独立。对给定 one/two-resource rules，枚举该处 winner candidates。每个 helper h 独立贡献一个 probability factor，其计算如下：

- 对它当前仍可能的一个 shared state s 求和，使用原 α_hs 或已经固定 state 的 Dirac probability，另包括 empty；
- 若 h 是 u 的指定 winner，必须选该 winner 的 state，并在 u 请求；同一 helper 在 u,v 都被指定获胜时两个 state 必须相同；
- 在 h 不是指定 winner 的资源上，若其该 state candidate 排在指定 winner 之前，必须不请求；排在后面则无约束；
- 对该 state 内 u,v 的不同请求 coins，使用其原 r_hsu，或已固定的 0/1。它们条件于同一个 state 才独立。

如果 state 或 coin requirements 不相容，该项为零。其他各项是至多两枚请求 coin 概率及一个 state 概率的乘积；对 s 求和后，再将各 helpers 因子相乘。因而即使同一 helper 影响两个资源，也没有把它的 shared state 误当独立重抽。u=v 时只使用单 winner 的 Y_iu²，避免错误地枚举两个 winners。

此公式在 state、coins、rules 的每个 CE 阶段均适用；尚未固定的独立底层变量仍有原先分布，不作隐藏 profile 列举。一次计算包含至多 O(|B|²N²I²) 个显式 winner/order choices，每项作至多多项式个 state 求和、helper 乘法；这个宽松界足够证明绝对次数多项式。

位复杂度同样是 total-bit polynomial。原 helper 概率空间有共同分母 D_0；独立 rule choices 加入 N^{|B|}，payoff 平方可取共同分母 D_1²。任何正概率 partial fixing 的 probability 分母也整除这一底层共同分母，conditional moment 至多再除以其正整数 numerator，其 bit 长度仍多项式。更直接地，以上 factor 公式只使用原 categorical/request probabilities 或 0/1，以及 N 的倒数；每次精确和、积、比较的运算数为多项式。μ_i 的长度也由 §5 控制，未使用指数精度 oracle。

law of total expectation 保证每步选中的正概率分支 conditional EΨ 不增。所有变量固定后得到真正的 actual requesting-winner allocation，满足

    Ψ<1/25,   W_i>μ_i−1/5>1/5 对所有 i.              (7.1)

不能在此后删除请求 coins 并按所有 selected states 的 maximum 重新分配；那可能提高某个 λ 加权值却降低个别 W_i。算法明确保留这里固定的请求 winner。

## 8. 阈值恢复所有 groups 与完整调度

取 q=1/10，称 Q_j≥q 的 helpers 为 Good，设 z_i=Σ_{j∈Good:i(j)=i}w_j。由于所有 Q_j≤1，

    W_i≤z_i+q(1−z_i).

由 (7.1) 得 z_i>(1/5−1/10)/(9/10)=1/9>1/10。保留每个 Good helper 已赢得的 fallback bundle；empty 的值为零，不会 Good。outer i 获得自己所有 Good helpers 的 homes，值为 z_i>q。其余 helpers 获得自己的 home，值为 1。所有 home 物理互异、B 与 homes 不交，fallback winner bundles 原已 disjoint，所以这确实是全部原 groups 的资源分配，每组值至少 1/10。

按 §1 的完整恢复执行所有原 jobs：为每组放置 selector，选 state 的这些 bundle incidence jobs 走 exact resource 端，其余 payload 全部留各自 private。原零 jobs 也留 private；未选 fallback states 从来没有被丢弃。由此 C≤2−1/10=19/10，而 OPT≥1，所以 C≤(19/10)OPT。

连同 §2 的不可行分支，算法对 Exact 域内每个输入都输出一个全 jobs 合法普通 UM assignment。k 是输入变量；δ 条件迫使每个 outer 至少 4096k⁴ 个正 homes，这个巨大但显式的输入规模是本限定域的实际条件，不把它当常数或免费复制归一化。LP、N=1024k 次排序 oracle、MW rational updates、全部 CE choices 以及最后输出均为绝对总位多项式。

## 9. 有限软件证据的准确边界

sol_general_repair_balanced_welfare_pair_backend.py 是独立编写的 Fraction 有限核，测试两个资源、三个 helpers、两个 outer、两个 states/helper、两个 priority rules 的单/双资源 moments 和 state→request→resource-rule CE。它以完整有限枚举校对 moments，并检查每步平方势不增及最终 moments 等于实际 winner values。

该小程序使用统一 request rate，只测试两个固定小实例；它没有实例化 δ 极小输入域，没有生成或求解 R_ε，没有实现 N 轮 MW 或完整普通调度，没有证明一般方差界。第二个小实例可以产生某 outer 的最终值 0，因为它没有 (5.1) 或 tiny-profile 假设；这不升级为目标算法反例或算法证据。一般参数、所有输入和位复杂度仅由上述证明承担。fresh reviewer 应先只读冻结 Exact，独立闭合或攻击，再由 root 决定是否释放本稿和该有限核。
