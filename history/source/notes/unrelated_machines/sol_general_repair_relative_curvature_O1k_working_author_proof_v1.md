# Working作者证明：reciprocal-gradient profile势的 O(1/k)付款

2026-10-18，/root/sol_general_repair。对应另冻的`sol_general_repair_relative_curvature_O1k_working_exact_v1.md`。只给root实读；不发正在v4 Exact-first的审者，不修改v4及更早原件。未独立审查的候选，不另立成熟Claim或借旧审票。

## 1. 固定输入、实际桥及baseline

严格沿新working Exact：single-state outers、全部homes互异、unit-own helpers、任意shared-B fallback、B-only exact-threshold-UD leaves；k≥2时ν≤1/(1024k)，k1无额外上界。H为helpers数，H≥1。令V为全部原group的最佳最小菜单值。normalized state总量一及resource-unit独占给实际OPT(P)=2−V，1≤OPT≤2：正向选择attaining states输出所领正incidences；反向C<2使输出resources disjoint，selector所在state输出值至少2−C。全部未选payload和零jobs仍留各自private。

固定ε=15/16，leaf判别E_l和b_l<ε给原菜单值≥ε iff bundle交E_l。若该图无完整matching，actualV<ε，输出所有payload留private、selector任放的baseline C≤2，ratio<32/17<19/10。以下叶full matching存在；空叶、空B、rank0均允许。

## 2. Profile oracle、次模性与actual benchmark

令M为B的vacancy matroid：X独立 iff全部叶可匹配到B\X，即满rank transversal matroid的dual。固定helper profile A每helper选一个fallback indexed state或empty；B分给这些helper candidates，并完整匹配全部叶，每资源至多一个owner。helper chosen-state值Q_j≤1，outer welfare W_i=Σ_(j∈J_i)w_jQ_j∈[0,1]。

fractional region是普通integral ownership/leaf-matching network。给λ>0，最大值f_λ(A)=max λ·W可用普通matching精确计算：令t_u=max_(active j)λ_i(j)w_jp_j,s_j,u（空max为零），则f_λ=Σ_u t_u减去完整叶matching的最小Σmatched t_u。未匹配资源给argmax helper或dummy，得到integral最大者。

同资源candidates是M的parallel copies，另加所有零dummy；weighted matroid rank在全部fallback options的candidate-copy unions上单调次模。此数学延拓在非profile集合可含一helper多个options；Q_j≤1、W_i≤1只在合法单option profiles用。

actualV≥ε时，取真实allocation中被outer拿走home的helpers，保留它们达到ε的B fallback states/bundles，其他helper设empty。每outer所取home质量≥ε，故有一个共同profile O满足对所有λ

    f_λ(O)≥ε²Σ_iλ_i.                                (2.1)

叶从其真实bundle保留一枚E_l资源，仍与这些helper bundles disjoint。O只在证明中存在，不是输入或调用oracle。

次模交换给任意合法A和这个O，若A_j只替换helper j成O的option，

    Σ_j[f_λ(A_j)−f_λ(A)]≥f_λ(O)−2f_λ(A).             (2.2)

证明：加全部O的marginal上界f(O)−f(A)，每个addition marginal≤单替换gain加该旧option的deletion loss；这些deletion losses之和≤f(A)。empty或相同indexed option同样有效。

## 3. k1分支：标准greedy，无tiny

λ_1=1，按固定helper顺序，每步在其全部fallback options加empty中选当前marginal最大者；f(∅)=0。对任意O_j，final marginal≤当该helper轮到时的marginal≤当步gain，故f(O)≤f(G)+Σgain=2f(G)。每query是§2 matching，最后求integral最优B allocation，W=f(G)。

W<1/4则f_opt≤2W<1/2<ε²，(2.1)反证actualV<ε，baseline完成。W≥1/4则Good={Q_j≥q=1/10}，home质量z满足W≤z+q(1−z)，所以z≥1/6>q；按§10直接回填。叶阈值始终15/16，无prefix/ν损失。这是标准次模工具直接应用，不认领新机制。

以下全部新势分析仅用于k≥2。

## 4. 先测真实fixed-profile LP，再用reciprocal梯度

令

    a=1/4, K=32k, ξ=1/(4096H), τ=1/(64H), q=1/10.

在当前profile的ownership/leaf-flow network上，先用普通精确有理LP检查能否同时W_i≥a。若可行，返回一个poly-bit rational flow并转§10；只这是固定profile的线性可行性，不是joint profile或actual OPT oracle。

若LP不可行，定义实分析势

    φ(x)=x,                                      0≤x≤a;
    φ(x)=a+log(1+K(x−a))/K,                       a<x≤1;
    Φ(W)=Σ_i φ(W_i),   P(A)=max_(fixed A flow) Φ(W).

φ是C1、凹、递增，gradient λ(x)=1（x≤a），否则1/(1+K(x−a))。0≤Φ≤k，1/(1+24k)≤λ≤1；λ Lipschitz K，a以外φ''=0或−Kλ²。P在compact flow polytope上达到最大，即使精确optimizer可能irrational，算法不求它。

在任一exact optimum W*，first-order optimality给f_λ(A)=λ·W*，λ_i=φ'(W_i*)。LP infeasible保证某W_i*<a，所以某λ_i=1、Σλ≥1。逐坐标有

    λ_i W_i*≤aλ_i+1/K,
    λ·W*≤aΣλ+k/K.                                (4.1)

这里无需从近似objective gap推单坐标稳定性；fixed-profile LP分支正是消除此义务，不能删掉。

## 5. stable weighted matroid coupling

固定λ、任意λ-optimal fractional W及一helper option替换j，存在新profile λ-optimal W'，令Δ_j=f_λ(A_j)−f_λ(A)，有

    λ·(W'−W)=Δ_j,
    max_i |λ_i(W_i'−W_i)|≤λ_i(j)w_j,
    Σ_i |λ_i(W_i'−W_i)|≤2λ_i(j)w_j.                 (5.1)

在integral maximal-weight basis上删旧j copies、再加新copies。每删一basis元素，只换一最佳replacement便有全局最优新basis；插入只需fundamental-circuit最小权交换。这由symmetric basis exchange证明，所有zero dummies使ground rank不变。

删阶段其他helpers的总weighted gains G≤旧j贡献A_0；加阶段总weighted losses L≤新j贡献B_0；A_0,B_0≤λ_owner w_j。聚到owner outer的变化B_0−A_0+g_owner−l_owner在[−A_0,B_0]，其他坐标在[−B_0,A_0]，L1≤A_0+B_0+|A_0−B_0|。因此包括same-outer其他helpers和整条leaf匹配级联后，仍有(5.1)。

fractional optimum分解成同一linear-optimal face的integral network vertices，再补零dummy成bases；逐分量执行后平均。分解只作存在证明，算法不求它。

## 6. 沿整条交换线段支付relative curvature

不能把current λ当作沿segment常数。对任何x,x+h∈[0,1]，若Kλ(x)|h|<1，则

    λ(x+sh)≤λ(x)/(1−Kλ(x)|h|),       0≤s≤1.        (6.1)

x≤a时λ=1，右边≥1。x>a且向上走时λ只减；向下但未过a时由reciprocal公式相等；过a时Kλ|h|≥1−λ，右边至少一，故仍成立。

由(5.1)以及λ_owner≤1，

    Kλ_i|W_i'−W_i|≤K w_j≤Kν≤1/32.

因此整段gradient坐标至多(32/31)λ_i<2λ_i，二阶绝对值≤4Kλ_i²；φ在a处虽不C2，C1且gradient Lipschitz，积分Taylor仍给

    Φ(W')≥Φ(W)+λ·(W'−W)−2KΣ_i λ_i²(W_i'−W_i)².

再用(5.1)的L∞×L1，Σ_iλ_i²ΔW_i²≤2λ_owner²w_j²。于是当W=W*为exactΦ-optimum，

    P(A_j)−P(A)≥Δ_j−4Kλ_owner²w_j².               (6.2)

Σ_(j∈J_i)w_j²≤ν且0<λ_i≤1，故全部替换的curvature总额

    Σ_j4Kλ_owner²w_j²≤4KνΣ_iλ_i²
                          ≤(1/8)Σ_iλ_i.           (6.3)

用了新ν≤1/(1024k)，K=32k。没有λ_min^(-2)或hidden k²付款。

## 7. actual target强制poly大进展

当前fixed-profile LP不可行时Σλ≥1。假设actualV≥ε，合(2.1)、(2.2)、(4.1)，

    Σ_jΔ_j≥(ε²−2a)Σλ−2k/K
           =(97/256)Σλ−1/16
           ≥(81/256)Σλ.

减去(6.3)，

    Σ_j[P(A_j)−P(A)]≥(49/256)Σλ≥49/256=:ρ.         (7.1)

所以某个单helper target option替换使P增≥ρ/H。它在算法枚举的原fallback options加empty中；不知道O或exact λ*不影响此存在式。

## 8. 无exact-log oracle的有理P近似

### 8.1 fixed-profile rational-gradient Frank–Wolfe

初始W=0加任意full leaf matching。每步取当前rational λ_i=φ'(W_i)，用§2 matching求integral payoff R_t，γ_t=2/(t+2)，同时将完整flow及W更新为其凸组合。只调用rational gradient，不调用真实log值。

gradient Lipschitz K，域diameter²≤k，故gap_(t+1)≤(1−γ_t)gap_t+(Kk/2)γ_t²，初始gap≤k，标准归纳给gap_t≤2Kk/(t+2)。固定N=ceil(4Kk/ξ)步后，P−Φ(W_hat)≤ξ/2。

每integral payoff的坐标是原w_jp_jsu的和，共同分母D_1的log长度为输入多项式。t≥1后vertices权重恰为2(r+1)/(t(t+1))，所以W分母可取D_1t(t+1)、flow分母t(t+1)。gradient分母再由1+K(W−a)一次有理式产生，不跨iterations递归相乘；所有matching比较都poly-bit。N=O(k²H)。

### 8.2 统一有理log截断与误差

每个W_hat_i>a令x=1+K(W_hat_i−a)，则1≤x≤1+24k，z=(x−1)/(x+1)∈[0,z_max]，z_max=12k/(12k+1)。设R=12k+1、δ_log=Kξ/(2k)。用整数倍增求J≥1满足2^J≥4R/δ_log，令L=RJ；二者只依k,H，不依原系数的倒数。

用有理式

    log_L(x)=2Σ_(n=0,…,L−1) z^(2n+1)/(2n+1)

代替log。所有项非负且是原实数log的下界；tail满足

    0≤log x−log_L(x)
      ≤2z_max^(2L+1)/((2L+1)(1−z_max²))
      ≤2R·2^(−2J)≤δ_log.

这里1/(1−z_max²)≤R，且((R−1)/R)^R≤1/2（直接Bernoulli不等式），不依赖数值exp/log oracle。对W≤a用exact linear值，其他用a+log_L/K；返回E(A)。总截断误差≤kδ_log/K=ξ/2，故

    P(A)−ξ≤E(A)≤P(A),       0≤E(A)≤k.             (8.1)

L=O(k log(kH))，可用精确有理算术。若z=A/B，共同分母可取B^(2L−1)乘全部odd denominators的积，bit长度O(L(logB+logL))；B来自poly-bit endpoint W。没有exact transcendental求值、分母数值循环或指数series。给所有初始matching、排序与ties固定输入索引，使E是profile的确定函数。

## 9. 全算法、soundFAIL、总位次数

叶无fullmatching先按§1 baseline；k1先按§3；余下k≥2初始化全empty profile，循环：

1. 用普通有理LP测当前profile能否同时W_i≥a。若可行，转§10。
2. 若不可行，按§8求E(current)，枚举每helper每个原fallback option加empty，重算各neighbor的E。
3. 存在E增至少τ则选最大者，固定索引打破平局，继续；否则输出baseline全部原jobs。

若第3步FAIL但actualV≥ε，LP infeasible使§7适用，某neighbor的true P增≥ρ/H；由one-sided(8.1)，其E增≥ρ/H−ξ=(783/4096)/H>τ=1/(64H)，矛盾。因此FAIL确actualV<ε，不是单个profile LP失败单独推出actual不可行。k1 FAIL及无leafmatching也有同一实际结论，baseline ratio<32/17。

每次E至少增τ、range[0,k]，所以至多64kH+1次moves。每轮一个poly-bit rational LP、polynomially many profile evaluations，每evaluation固定O(k²H) matching和poly(k,H,inputbits)有理log项。input menu只显式枚举单helper options，不展开joint profiles。所有LP基本点、FW flows、梯度、cost、log截断与E comparisons均poly-bit；次数为绝对多项式。

## 10. LP成功的共同prefix-flow及全部原jobs

k≥2 LP成功给固定helper states与fractional W_i≥1/4。令a_iu=max_(j∈J_i)w_jp_j,s_j,u≤ν，Σ_ua_iu≤1。聚合同outer claims到argmax helper只增utility。按a_iu降序，对每prefix count F_l加integer lower floorF_l；与全部叶rows恰一、资源列≤一放同一整数lower-bound circulation。原fractional flow见证可行，整数性给完整叶matching和整数outer claims。分部求和每outerweighted损失≤max a_iu≤ν，所以

    W_i≥1/4−ν≥1/4−1/2048=511/2048>19/100.

这只用于k≥2；k1从§3直接有integral W≥1/4，ν可一，绝不套此loss界。对两分支同取Good={Q_j≥q=1/10}，home质量z_i满足W_i≤z_i+q(1−z_i)，因W_i>19/100有z_i>q。保留Good B bundle，outer给其homes，其他helpers各own；leaf给matching资源并选一个提供≥ε incidence的原state。全homes互异且与B不交，所以所有groups质量≥q。

按原编译把selectors放所选原private、只输出所取正incidence jobs，其余全部原jobs留private，含unselected payload、全部zero incidences及重复indexed states。每job恰一次、原finite endpoint合法，C≤2−q=19/10；unit selectors使OPT≥1。全部矩阵和输出规模仍S+U、G+I、S+2I，稠密展开多项式。baseline分支也完成同一全部jobs。

## 11. 身份及未付范围

本稿是未独立审查working proof，root已知先行概要不算fresh票。没有读或取代truehardness正在做的v4 Exact-first；v4正文、Exact、作者字节及审查完全不改。此候选没有端到端代码、完整tiny实例实验或软件认证；上述log误差和总位界由本稿直接付款。

相对v4它增加一个固定profile有理LP分支与reciprocal-log势，以relative curvature代替Euclidean λ_min界；没有解决multi-state outers、homes重叠或nonUD extras。也不声称一般UM算法或任何新的NP-hardness。一般UM-TARGET-v1继续OPEN。
