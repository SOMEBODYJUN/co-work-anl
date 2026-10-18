# 坐标切片的精确单位阈值与源编译反例

精确身份：`UM-Q-COORDINATE-SLICE-PARTIAL-MINREP-COUNTEREXAMPLE-v4`。读取目的：检查把投影源变成私有分叉树分配时，一种自然坐标切片表示究竟保存了什么。这里给出完整实际 P、严格阈值等价、精确反例、保源 promise 的 padding，以及双射/配置证书也不能修复的扩展；没有证明一般 q-allocation 或 UM-TARGET 的正反面。

v1 只冻结了显式反例和实际上界；v2 新增精确阈值；v3 新增私有输出 padding；v4 新增双射源与精确 CONFIG 证书。它们是同一候选的结论扩展，旧 Exact 原字节保留，最终仅登记 v4。实际独立重构与读后攻击见 [审查](../../reviews/unrelated_machines/private_tree_branching_valuation_review.md)。

## 对象与坐标切片编译

原游戏是非空、simple、两侧各 n 个顶点的 D-regular 二部全投影游戏，D≥3，共同字母表 Σ 大小 Q≥2。每个右点 b 的不同邻居按 [D] 编号；N=2n、M=DN/2。列表可空，总成本为所有顶点列表大小之和；覆盖指存在兼容标签对。所有对象显式给出。

对每个右点 b 建共享资源块 R_b={b}×[D]^Σ，各块互异。玩家为左顶点。每个玩家 a、每个标签状态 α 各有一棵私有满 D 叉深 Q 树：第一层选择 a 的 D 个不同邻接测试 b；若 a 在 b 的编号为 i，投影为 β=π_ab(α)，下面 Q−1 层按固定全局字母顺序选择 Σ\{β} 各坐标的值。叶映到资源 (b,x)，其中 x_β=i，其余坐标为路径值。因此状态叶像恰是其 D 个完整切片，叶数 D^Q，映射为单射。

用 [已有 q 定义](private_tree_branching_valuation_and_minorants.md) 令 f_a(S)=max_α q_{a,α}(S)。要求各玩家资源两两不交。此处必须保留真正同深 r 叉根子树，不能只数 r^Q 片叶。

完整实际 UM 实例如下。每个状态树内部节点是一台私有机器；每个共享资源是一台资源机器。每个玩家有一枚单位 selector，可在该玩家任意状态根执行。每条树边对应一枚 port 任务：父端用时1/D，孩子内部机器或叶资源端用时1。每个 port 恰有这两个有限选项，此外全部为∞。没有额外任务、容量或外部约束。

每树内部点数 I=(D^Q−1)/(D−1)。机器数 nQI+nD^Q，任务数 n(QDI+1)。数值时间只为1/D和1。所有完整树显式展开；D^Q 不被隐藏成原输入多项式。当 D、Q 先固定时，展开和后述具体分配/调度对原游戏大小为多项式；不声称变参数 binary D、Q 下的统一原输入多项式编译。

## 精确结论及证明

**单位阈值恰等于完美源满足。** P 有实际 C≤1 调度 iff 原游戏有满足全部边的单标签赋值。

若原赋值完美，玩家选其状态全树。固定 b，全部邻居投影为同一 β_b，不同编号 i 的切片 x_β_b=i 两两不交。取各玩家全叶，即得 f_a=D 的分配。selector 放所选根；所选全树全部 port 单位下传，其余状态全部 port 留父端。所有私有及已用资源机器负载均为1，其余资源为0。

反向，实际 C≤1 时 selector 所在根已负载1，所有子 port 均不得留父，必须单位下传。每个收到单位 port 的内部点同样迫全部子 port 下传。逐层归纳，selector 选中的状态全部叶切片都被单位任务占用。固定 b，若两邻居所选状态的投影 β≠β′，完整切片 x_β=i 与 x_β′=i′ 交非空，因为不同坐标可独立指定；对应共享资源承受两枚单位 port，矛盾。因此每个 b 的所有邻居投影相同，selector 所选标签配这些右标签满足全部原边。其余状态即使还有外送也只增加竞争，论证未假设它们为空。

**任意实际 r 叉分配给全部任务的调度。** 若每个玩家在某一状态有深 Q 的满 r 叉根子树，1≤r≤D，且其叶资源全局互斥，则存在实际 C≤2−r/D 调度。selector 放所选根；子树边 port 单位下传；其余所有 port 留父端1/D。每个 active 内部节点有一枚进入单位任务（根为 selector）及 D−r 枚留父 port，负载2−r/D。未选状态和未选分枝内部没有单位入边，所有 D 枚子 port 留父，负载1。资源机器至多一枚单位 port。此计算包含每个状态、每个节点及每枚任务。

## 线性度数部分 Min-Rep NO 的显式反例

固定 g≥2、0<ρ≤1，取整数 D>max(2,2g/ρ) 及 t≥1。源图为 t 份 K_D,D，左右点记 a_c,i、b_c,j，其中 c∈[t]、i,j∈[D]，右邻居编号为 i。公共字母表

\[
\Sigma=\{0,\ell_1,\ldots,\ell_D,p_1,\ldots,p_D\},\qquad Q=2D+1,
\quad
\pi_{ij}(\alpha)=\begin{cases}0,&\alpha=\ell_j,\\p_i,&\alpha\ne\ell_j.\end{cases}
\]

每条被覆盖边若通过0覆盖，充给唯一左 token (a_c,i,ℓ_j)；其余只能通过 p_i，充给唯一右 token (b_c,j,p_i)。每种 token 仅对应一条边，且两类不同侧。故对任何列表族

\[
\#\mathrm{covered}\le\operatorname{cost},\qquad
\operatorname{cost}\le gN\Longrightarrow
\frac{\#\mathrm{covered}}M\le\frac{2g}{D}<\rho.
\]

每右点所有投影像又都包含0。固定ρ并选最小合适 D 时，度数及字母表均 O_ρ(g)；这是真正的部分覆盖 NO promise，不是只检单标签的 NO。

然而所有玩家选择状态 **0**，实际投影为 p_i，不能误作0。根保留 b_c,1,…,b_c,D−1。在每个保留测试内，固定 x_p_i=i；其余坐标 p_s，s≠i，各删值 s；坐标0及ℓ_s 各任删一个值。每层恰保留 D−1 孩子，给满(D−1)叉深 Q 子树。若同一资源属于 i 和 i′，后者要求 x_p_i′=i′，前者已排除此值，矛盾。因此全玩家资源互斥，完整实际 P 可达1+1/D。

源无完美赋值，因为 singleton cost N≤gN 的全覆盖会违反上述 NO。精确单位阈值因此给 OPT(P)>1。所有负载是1/D的整数倍；有限非空调度集合使最优值可达到，故 OPT(P)≥1+1/D。结合实际调度，得到

\[
\boxed{\operatorname{OPT}(P)=1+1/D.}
\]

这是精确小 gap，不能放大成 near2。对固定满足条件的 g、ρ、D 而变化 t，全部对象线性展开；“固定D”本身不决定ρ。该显式 NO 家不被声称是任何特定 PCP 归约的像。

## 保留源 promise 的私有输出 padding

下面不必选择特殊 K_D,D。给任意上述原游戏 Π₀（字母表 Σ₀ 大小 Q₀）、g≥2 及 0<ρ₀<ρ≤1，要求 ρ₀+2g/D≤ρ。构造左冲突图 H：两左点若共享右邻居便相邻。其最大度数≤D(D−1)，贪心给 proper coloring χ:A→[s]，s≤D(D−1)+1。添加不在 Σ₀ 的 α*、p_1,…,p_s 作为共同新符号，令

\[
\pi'_{ab}(\alpha)=
\begin{cases}
\pi_{ab}(\alpha),&\alpha\in\Sigma_0,\\
p_{\chi(a)},&\alpha\notin\Sigma_0.
\end{cases}
\]

**所有新左符号**均用第二行，不仅是α*。图、degree、平衡及全投影保持，Q′≤Q₀+D(D−1)+2，padding 本身是统一确定性位多项式。旧 perfect YES 保留。

若旧源任意 cost≤gN 列表覆盖严格<ρ₀M，则新源同预算列表覆盖严格<ρM。证明：删掉新符号得旧列表，旧方式覆盖<ρ₀M；其余新覆盖边必须用右 token (b,p_χ(a))。同 b 的邻居色互异，且图 simple，所以该 token 至多充一边；新边至多 gN。故总覆盖严格<(ρ₀+2g/D)M≤ρM。公共新字母表内的别名没有产生未计费的旧投影。

但坐标编译对**所有** padded 输入都有 actual C≤1+1/D 调度：玩家均选 α*。在测试 b 下，玩家 a 固定 x_p_χ(a)=i_b(a)；每个其他邻居 a′ 的自由坐标 p_χ(a′) 删去 i_b(a′)，其余自由坐标任删一个值。每个颜色坐标只需删一次，根任取 D−1 邻居，形成满(D−1)叉子树。任意两玩家若同 b 相交，一方固定的坐标正被另一方排除，矛盾。应用上面的完整 port 调度即可。

若旧源是该 NO，则新源也无 perfect，故 padded P 的 OPT 恰1+1/D；若旧源 perfect，则 padded P 的 OPT 恰1。固定 D、Q₀ 后 Q′ 有固定上界，后续树展开对图大小多项式。若这个固定参数域已有 hard 源族，padding 保留相应 promise；此处没有擅自引入未核的 simple hard 源定理，也没有用有限覆盖图免费消除 parallel 约束。

## 双射和均匀纤维仍有反例

再固定 g≥2、0<ρ≤1，取

\[
D=\lceil16g/\rho\rceil,\qquad
Q\ge\max\{2D+1,\lceil(100g^2/\rho)^4\rceil\}.
\]

源为单份 K_D,D，公共字母表大小 Q，含互异0、p_1,…,p_D。各边独立均匀抽取满足 π_ij(0)=p_i 的双射。以至少1/2概率，所有 cost≤gN 的列表均覆盖严格少于ρM。每个种子的全部投影都是双射，公共像为整个字母表。这里是有限概率存在性，不是源困难性归约或高效 NO 检验器。

证明如下。固定廉价列表，左长 A_i、右长 B_j，Σ_iA_i+Σ_jB_j≤2gD。通过0→p_i 的覆盖边数至多2gD≤ρD²/8。其余覆盖指示量在不同边独立，单边概率≤A_iB_j/(Q−1)，总均值≤g²D²/(Q−1)。若总覆盖≥ρD²，普通覆盖 X 必≥ρD²/2。设 z=g²/ρ，Chernoff 给

\[
\Pr[X\ge\rho D^2/2]
\le\left(\frac{2ez}{Q-1}\right)^{\rho D^2/2}
\le Q^{-3\rho D^2/8}\le Q^{-6gD}.
\]

中间一步用 Q≥(100z)^4、Q−1≥Q/2，因此 2ez/(Q−1)≤(e/25)Q^−3/4<Q^−3/4。全部廉价列表数量 K 满足 KQ^−2gD≤(1+1/Q)^2DQ≤e^2D，从而 K≤exp(2gD ln(eQ))。坏事件 union 概率≤exp(2gD−4gD lnQ)≤Q^−3gD<1/2。没有枚举列表来证明概率，也没有依赖有限测试。

每个种子均保留对角 π_ij(0)=p_i，所以前述 state0 删对角值的(D−1)叉分配及完整 C≤1+1/D 调度仍成立。好 NO 种子无 perfect，故其整数 OPT 恰1+1/D。

**每个种子的 T_CONFIG 又恰为1。** CONFIG 使用机器容量1的局部任务集合，机器权和≤1、每 job 覆盖≥1。每棵状态树的每台内部机器取两个配置：其唯一 incoming 单位任务（根处为 selector）权1/Q；自己的全部 D 枚小端 port 权1−1/Q。各配置负载均1。selector 在 Q 个根覆盖恰1，每枚 port 在父端覆盖1−1/Q、子端覆盖1/Q。

固定资源 (b,x)。邻居 i 的双射使其各状态遍历全部投影 β，因此该邻居有 #{β:x_β=i} 枚 eligible 叶 port。对全部 i 求和恰 Q。给这 Q 枚单位 port 各 singleton 配置权1/Q；每个资源机权和恰1，每枚叶 port 子端覆盖1/Q，所有 job 覆盖等式成立。T<1 时 selector 不在任何配置中，所以 T_CONFIG≥1。证书有理、规模为显式 P 的多项式；它不是实际调度。于是好 NO 种子满足精确 OPT/T_CONFIG=1+1/D，未得到 near2 gap。

可选 Q=poly_ρ(g)，D=O_ρ(g)；树展开仍为 D^Q，不能称作变参数原输入多项式。没有把一份好样本任意复制 t 次就宣称保留相同 soundness，global 列表集中预算须另证。有限小例的实际 σ/CONFIG 索引审计见 [代码](../../../tests/audits/unrelated_machines/coordinate_slice_physical_configuration_audit.py) 和 [冻结输出](../../../evidence/runs/unrelated_machines/coordinate_slice_physical_configuration_audit.json)；这些小参数不满足此概率 NO 定理的常数，未被用作 NO 或精确 OPT 的验证。

## 机制、范围与状态

失效步骤是把“所有 test 投影一致”换成“各投影坐标分别可删少量值”：每个对手只需在一个自由坐标删一个值，所有层仍保留 D−1 分叉。源的全局廉价列表 soundness，即使配局部公共像，也不能独自证明此坐标编译的弱调度 soundness。padding 还说明这一问题可在保源 promise 的变换后普遍出现，而非仅某一张玩具图。

可回收的是明确 slice 表示、strict iff 和逐任务精确阈值。重试须改变资源共享/叶排列或补真实的跨测试一致性；单纯增加完整坐标层、要求双射/均匀纤维或 CONFIG1 可行仍不够。结论不排除带额外全局结构的特定 PCP 像、其他表示或一般 q 源困难性。这里的单射叶模型与一般证明已独立攻击；实现只为小例实际 σ/CONFIG 结构审计，未实现随机 NO 检验或一般源编译器。外审和新颖性未认证；UM-TARGET-v1 正反面保持 OPEN。


## 超立方分组菜单的 Hall 保留与锐3/2实际界

本节是不同于前述需求树编译的新对象，另立 `UM-GROUPED-HYPERCUBE-SLICE-SCHEDULING-v2`；不改变 v4 的源反例合同。读取目的：检验 Davies–Guruswami–Ren 的新双标准 Set Packing 困难性是否能直接提供近二调度源。答案限于以下具体菜单桥：不能，整类输入都有实际3/2界，且该归一化界可达。

### 精确对象、算法与量词

取整数 d,Q≥1；变量集 X 与非空组集 G。每组 g 有非空的 distinct-variable 集 X_g、非空显式状态菜单 A_g。每变量 x 参加至多 d 个组，给单射 j_x:{g:x∈X_g}→[d]。状态 s∈A_g 为各 x∈X_g 选一个标签 ℓ_{g,s}(x)∈[Q]。

变量资源是带 x 标签的互不相交立方 U_x={x}×[d]^Q。其状态资源集为

\[
 S_{g,s}=\biguplus_{x\in X_g}
 \{(x,z):z_{\ell_{g,s}(x)}=j_x(g)\},
 \quad L_g=|X_g|d^{Q-1},\quad c_d=1-(1-1/d)^d.               \tag{H1}
\]

每状态每变量恰取一个切片；不同变量不能合并资源名，组的 incidence 索引必须注入；L_g 可随组变化，同组各状态大小相等。没有 CSP 可满足性或源 YES 假设。

**Exact Statement / Quantifiers。** 对每个这样的显式输入、每种任选一状态 s(g)∈A_g、每个组子族 F⊆G，同时有

\[
 \left|\bigcup_{g\in F}S_{g,s(g)}\right|
 \ge c_d\sum_{g\in F}L_g.                                 \tag{H2}
\]

故可在显式输入总位长的确定性多项式时间，分配两两不交 B_g⊆S_{g,s(g)}，|B_g|=⌊c_dL_g⌋。若 d=1 或 Q=1，则可全部分配，|B_g|=L_g；其余情形可以保证 |B_g|≥⌈L_g/2⌉。

**实际 UM 桥。** 每状态一个不同根机器 M_{g,s}；每资源 u 一个不同资源机器 R_u；每组一个 unit selector，只在自己组的各状态根可用。每个 state-resource incidence (g,s,u) 是一枚不同任务，在 M_{g,s} 时间1/L_g，在 R_u 时间1，其他端∞。所有机器、任务标签分离，全部任务必须分配。若完整选定状态集互不相交，OPT=1。对任意上述输入，不依赖 YES/NO，可确定性位多项式输出完整调度，且

\[
 C_{\max}\le3/2;                                         \tag{H3}
\]

d=1 或 Q=1 时 OPT=1。该类所有输入的 OPT/1 的上确界恰为3/2且取得；这不是声称3/2的近似比 NP-hard。

当 d=5,Q=2 时(H2)中的 c_d 可加强为19/25。每组恰三个变量、L_g=15时可每组分配11个资源，实际负载≤19/15。11是对任意固定状态选择的最佳通用整数保留量；不声称优化所有菜单选择之后仍必需要该界。

### 自足证明

固定状态选择及 F。在单个变量 x 上，令 r≤d 为 F 中的 incidence 数，t_ℓ为使用标签 ℓ 的个数，Σt_ℓ=r。注入索引保证同标签所取坐标值不同，因此资源并集恰为

\[
 d^Q-\prod_{\ell=1}^Q(d-t_\ell).
\]

r=0无需证明。d=1时每变量至多一组，所选集合互不相交。d>1，令 z=1−1/d。整数 t∈[0,d] 满足1−t/d≤z^t，故并集≥d^Q(1−z^r)。几何序列的前 r 项平均随 r 下降，r≤d 给

\[
 d(1-z^r)/r\ge1-z^d=c_d.
\]

故该变量并集≥c_d r d^{Q−1}。对带标签分离的变量求和即得(H2)。每个组需求⌊c_d L_g⌋满足全部带需求 Hall 不等式；组到资源二部网络的整数最大流输出实际不交分配。

进一步，d>1时二项式给

\[
 (1+1/(d-1))^{d-1}\ge2,
 \quad (1-1/d)^d\le(d-1)/(2d),
 \quad c_d\ge(d+1)/(2d).
\]

Q≥2时L_g/d为正整数，因此

\[
 c_d L_g\ge L_g/2+L_g/(2d)\ge L_g/2+1/2
 \ge\lceil L_g/2\rceil.
\]

Q=1时同一变量的索引互异，全部所选集合已不交。由此均可得到至少一半的整数分配。

在实际 P 中，把 selector 放在任选根 M_{g,s(g)}，将 B_g 对应的 incidence jobs 移到各自 R_u，其余 incidence jobs 留自己的状态根。资源机各至多一个 unit；未选根的全部小任务负载1；选中根负载

\[
 1+(L_g-|B_g|)/L_g\le3/2.
\]

全部原任务均被恰好分配，证明(H3)。若完整所选集不交，把所选 states 的全部 incidence jobs 外放，未选 states 的全部 incidence jobs 留在各自根，即可达1；至少一个 selector 时间1给 OPT≥1。

**3/2锐例。** d=2,Q=2、一个变量 x、两个组 j_x(g₁)=1,j_x(g₂)=2，各仅一状态，分别取标签1、2。两个大小2切片是 {z₁=1} 与 {z₂=2}，并集大小3。两根均被 selector 占1。若 C<3/2，四枚 incidence jobs（根端1/2）均须外放；但资源机 unit 容量为1，三个可用资源不能接四任务。各组分配一个不同资源则达到3/2，故 OPT=3/2。原 universe 第四格机器仍在，只是没有相应 incidence 可利用。

**19/25与11。** d=5,Q=2，变量上的 a 条行、b 条列满足a+b=r≤5，并集5r−ab≥5r−⌊r²/4⌋≥19r/5，故比率≥19/25。在r=5、(a,b)=(2,3)时等号成立。三变量组的 Hall 需求可取11，因为任意 F 并集≥57|F|/5≥11|F|。五组都使用同三个变量、各变量索引j=g，前两组选标签1、后三组选标签2，总并集57，不能每组分12（需60）。这只证明固定选择下的通用整数界。

### 原论文身份、位复杂度与范围

**Paper Fact。** Davies–Guruswami–Ren, *Scheduling Problems with Constrained Rejections*, arXiv:2511.00184v1，§5用 degree-five 3SAT、二元 alphabet、七个满足局部状态、每 set 大小15。Theorem4 是存在固定常数的**无分组 set selection**双标准困难性，参数 α=1/7、β=(1−ε₀)/7、ε<1/30；并非任意小保留比例困难性。15元素且保留比例1−ε、ε<1/30时，整数上已强制保留全部15。

本文另定义 clause groups，各有七状态，再接(H1)的实际 UM 桥；该桥不是原论文声称的 UM 近二归约。19/15和一般3/2是这里从乘积计数、Hall及全任务负载回算得到的结构推论，不归于原文定理。原PDF字节、SHA、实际读取范围见 literature manifest；root已核§5的18页作者版原PDF（印13–14）与HTML对应段。没有把下载或摘要当新数学。

**Bit complexity。** 资源/状态/incidence显式给出或先实际展开，网络与 P 的规模均为其多项式；时间1/L_g用O(log L_g)位。c_d为O(d log d)位有理数，显式非空cube大小至少d，故精确需求计算也按显式位长多项式。若仅给二进制d,Q及简洁菜单描述，d^Q可指数大，不宣称该隐式编码的位多项式。各参数可增长，不能把固定参数结论冒充一般UM。

**Dependencies / Objections / Status。** 全部(H1)共同前提、精确乘积补集、整数 Hall/max flow、selector/incidence实际任务桥。重复 incidence 索引、合并变量资源、非乘积切片、多尺度负载或第二种接口可离开本定理，但没有由此自动得到 hard source；既有一般私有注入树5/3界仍须另核。证明完成、陈述先行独立审查及读后最终组合见[切片新对象审查](../../reviews/unrelated_machines/grouped_hypercube_slice_scheduling_review.md)。无新生产 LP/flow 实现；证明的可构造性与软件实现状态分开。外审/新颖性未认证，属于经典计数与Hall的结构推论，非主目标完成。
