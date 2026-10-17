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
