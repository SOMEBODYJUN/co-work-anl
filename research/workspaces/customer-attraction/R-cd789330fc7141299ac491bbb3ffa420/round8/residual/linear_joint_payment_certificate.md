# 固定比较元组的共同付款线性证书

2026-10-24，residual8，按 root 的合成陈述独立展开。范围为任意有限单位客户、有限非空共同目录、任意人数及每份完整有序历史纯 SPE，含任意平局、重复、空主题和全零输入。**Q-CAG-HALF 仍 OPEN。** 本页给有限线性可行性充分接口，不证明一般可行性，不作新颖性认领。

依赖：[坐标初始化](../../round7/parent/optimal_coordinate_initialization.md)、[加强边界与全图密度](../inventory/source_preserving_density_envelope.md)、[peer I-future 实际补余](../../../R-d3981c0168644971803a9c3380ed687c/next_general/global_credit/coordinate_residual_attack.md)、root 的 optional-common 家族（[价格势重构](common_edge_price_potential.md)）。

## 1. 固定数据与有限有序图

固定原实例、完整 SPE σ、实际叶 B、实际利润 u，C=union(B)。固定比较元组 T，置 O=union(T)、I=O∩C、R=O\C。只有取 T 最优时才将 |O| 识别为 OPT_m。下面的完成叶、客户分母、边集合和 H 均是数据，不随流变量改变。

对 x∈T_i 定义

    p_ix=1/c_T(x),
    delta_ix=c_B(x)+1−1_(x∈B_i),
    W_i=finish_sigma(B_<i,T_i),
    P_ix^B=Σ_(l≠i:x∈B_l\T_l) p_ix/delta_ix,
    r_ix=p_ix−P_ix^B>=0.

第一实际正价列为

    H_lx=Σ_(i:x∈T_i,l≠i,x∈B_l\T_l)p_ix/delta_ix,
    H_l=Σ_xH_lx.

H 只支持 I；对 x∈I，已有列界给

    0<=H_lx<=w_lx:=1_(x∈B_l)/c_B(x).

初始边集合和加强容量为

    E0(i,x)={j>i:x∈(W_i)_j\B_j},
    qhat_ijx=min(p_ix,1/delta_ix)/c_Wi(x).

只在 E0 中定义初始边变量；其它边固定为0。上述分母都只在相应客户确被覆盖时使用，故正。

自然 R 图从全部可能初始 R 边的目标 t=(W_i,<j,j) 出发，按如下固定 reset 边取闭包。自然 context t=(g,k) 的数据为

    a_t=σ_k(g), V_t=finish_sigma(g),
    A_t=finish_sigma(B_<k,a_t).

对 x∈R∩a_t，定义

    Q_t(x)={j>k:x∈(A_t)_j},
    N_t(x)={j∈Q_t(x):x∉(V_t)_j},
    M_t(x)={j∈Q_t(x):x∈(V_t)_j},
    tau(t,j)=(A_t,<j,j).

加入全部 j∈Q_t(x) 的真实 prescribed target。R 不被任何 actual 主题覆盖，故 A_t 中 x 的 coverer 只有当前 k 和这些未来角色：c_At(x)=1+|N|+|M|。所有 R target 都非 actual-prefix，也没有 R 的 past actual 出口。

每条边严格增加角色，全部合法有序历史有限，故闭包有限。也可使用全部自然有序历史作有限状态集、将不可能状态固定为0；不能按主题计数合并不同有序历史。

## 2. 原始线性可行性系统

所有变量均非负。

**初始坐标 INIT。** 对每个 x∈T_i、j∈E0(i,x)，引入 a_ijx、c_ix、d_i：

    0<=a_ijx<=qhat_ijx,
    c_ix+Σ_j a_ijx=r_ix,
    d_i=Σ_(x∈T_i)c_ix,
    d_i<=u_i.                                      (INIT)

记 a_ix=Σ_j a_ijx。c>=0 已包含 a_ix<=r_ix。**不固定** d_i=min(Σr_ix,u_i)：可以在原加强边容量内多送 future、少占 current，给共同预算保留空间。每个坐标仍精确满足 p_ix=P_ix^B+c_ix+a_ix。c_ix 的 x 仅是来源库存标签，不要求 x∈B_i；d_i 是完整 actual i 利润行上的金额，不是 actual(i,x) 同客户券。

**I 实际补余 I-PAY。** 对 x∈I、实际角色 l，引入 J_lx：

    0<=J_lx<=w_lx−H_lx,
    Σ_lJ_lx=Σ_(i:x∈T_i)a_ix.                       (I-PAY)

令 J_l=Σ_(x∈I)J_lx。右端是本可行点的全部 I-future；直接付清后不再进入 R 图。B_l 不覆盖 x 时 J_lx 自动为0。付款角色可早于 owner；没有调用过去角色 IC。

**R 流 R-FLOW。** 对每个自然 t=(g,k)、x∈R∩a_t，引入 h_tx、L_tx；对 j∈Q_t(x) 引入 z_tjx。初始入口是 INIT 变量的线性和

    b_tx=Σ_(i:t=(W_i,<k,k))a_ikx.

仅合法初始边参加此和。要求

    h_tx=b_tx+Σ_(s,j:tau(s,j)=t)z_sjx,
    z_tjx=h_tx/c_At(x)                             (j∈N_t(x)),
    0<=z_tjx<=h_tx/c_At(x)                         (j∈M_t(x)),
    L_tx=h_tx−Σ_(j∈Q_t(x))z_tjx.                  (R-FLOW)

L>=0 也由边界自动推出，且

    h_tx/c_At(x)<=L_tx
       <=h_tx[1+|M_t(x)|]/c_At(x).

用边流 z 而非 α 与 h 的乘积，系统才是线性的。若需要比例，可在求得 h>0 后事后定义 α=c_A z/h。旧完成叶 V、reset A 和分母均不因 z 改变。 L_tx 的 x 也只是来源库存标签；R 时 actual B_k 必不覆盖 x，L 仍通过完整 query IC 付到实际 k 的整行钱包，不能称 actual(k,x) 券。

**共同角色行 ROLE。** 对每个实际角色 l 要求

    d_l+H_l+J_l+Σ_(t:role(t)=l)Σ_(x∈R∩a_t)L_tx
       <=2u_l.                                    (ROLE)

这是真正尚未证明总可满足的共同预算。不能每个 context 先独占一份 u_l，再把它们免费相加。

## 3. 对任意可行点的合法性与充分性

**密度对任意变量选择自动成立。** INIT 给 a_ix<=r_ix<=p_ix，以及逐边 c_Wi(x)a_ijx<=p_ix。给定仅按客户合并的可行流，可在每个节点按各 origin 的输入比例拆分全部 future 输出及 current（h=0 时全零），得到逐 origin 的守恒流。因此，对每个 origin i、客户 x，严格 future 质量路径在同一角色层至多经过一次，该层全部 context 输入不超过 a_ix；不需父节点唯一。

固定非 actual target t，令 k 为其历史与 actual 首次不同的位置。所有 reset 父节点均在角色 k，可有许多不同旧历史，但 reset 叶相同。每条 mandatory 父边乘目标负载后的贡献恰为父 h_sx，common 父边贡献不超过 h_sx。到这些父节点的 origin 只能小于 k；直接入口的 owner 只能是 k。因此

    c_Vt(x)h_tx<=p_kx+Σ_(i<k)a_ix<=Σ_(i<=k)p_ix<=1.   (DENSITY)

它对所有 R-FLOW common 选择同时成立；无需额外写进 LP，也没有将多个父密度上界直接相加。

**每 context 一次完整 IC。** 令 f_tx=c_Vt(x)h_tx。共同 coverer 数 r_t(x)=1+|M_t(x)|<=c_Vt(x)。由 R-FLOW 和 DENSITY，

    Σ_xL_tx<=Σ_(x∈R∩a_t)h_tx r_t(x)/c_At(x)
             <=Σ_(x∈R∩a_t)f_tx/c_At(x)
             <=Σ_(x∈a_t)1/c_At(x)
             =u_k(A_t)<=u_k.

最后一步是 actual-prefix 强制 a_t 的一条原完整 IC。客户权先用于证明金额不超过完整 query，再调用一次 whole IC；没有按客户重权原 IC。遗漏的非 R query 收益及 1−f 缺额均属于同一整行退款，不能另花一次。common 边只降低 current。

**质量守恒给充分证书。** 每个 x∈O 的初始份额和为1，故 INIT 精确给

    |O|=Σ_l(H_l+d_l)+Σ_(i,x∈I)a_ix+Σ_(i,x∈R)a_ix.

I-PAY 将 I 源改写为 Σ_lJ_l。R-FLOW 是有限守恒严格 future DAG，所以全部 R 源最终恰变为 Σ_(t,x)L_tx。因此

    |O|=Σ_l[d_l+H_l+J_l+Σ_(t:role l,x)L_tx].          (MASS)

全部金额非负、来自同一份每客户单位库存，J 付清的 I 没有再传播，也不重采到 O 外客户。结合 ROLE 得 |O|<=2Σ_lu_l=2W。

**结论：固定 T 的 LP 若可行，就有 2W>=|O|；T 最优时得到该实例、该完整 SPE 的 HALF。** 这是充分接口，不是一般可行性定理。

忽略 ROLE 后其余系统确有可行点：加强初始化正部论证给 INIT 点；对任意 INIT 点，I 库存给

    Σ_i a_ix=1−Σ_lH_lx−Σ_i c_ix<=Σ_l(w_lx−H_lx),

所以 I-PAY 可按未花实际份额比例分配；零总容量时源量亦零。随后 common 全取0、按角色递推即得 R-FLOW。真正未知的只是能否共同满足 ROLE。

## 4. 无需 T 或 SPE 的一般 source 密度引理

以下是 root 提出的广义 source 合同，本分支独立核对通过；它只证明流/密度，不证明初始付款预算。

固定任意完整纯 policy σ（本段不要求 SPE）及 actual B=finish_sigma()。有限 query-source 集合中的 α 有 owner i(α)、合法动作 a_α 及真实 actual-prefix query 叶

    W_α=finish_sigma(B_<i(α),a_α).

给每个客户 x 非负库存 p_αx，要求 Σ_αp_αx<=1。每条初始边必须进入 W_α 中一个确实覆盖 x 的严格未来 prescribed context，且其质量 b_αjx 满足

    A_αx:=Σ_jb_αjx<=p_αx,
    b_αjx<=p_αx/c_Wα(x).

同 owner 可以有多个不同 query，也可有相同 query 的多个标签；各自库存仍参加同一总和。实际前缀目标若出现，直接作 actual 客户 sink。若 x 并非 R，reset 新增的 past coverer 也可出现：其 mandatory h/c_A 正边只作 actual 客户 sink；future 新增边仍为 h/c_A，共同 future 边仍在[0,h/c_A]内。current 留下其余质量，故每客户总出流不超过输入。只在接收者动作覆盖 x 时定义输入，故所有使用的分母均正。R 情形正好退化为本页 R-FLOW。

对非 actual target t，设首次实际差异位置为 k。所有 reset 父节点角色都为 k：否则其 actual-prefix reset 叶的首次差异位置不会是 k。每条父边对目标密度的贡献<=父 h_sx。到这些父节点的 origin owner 都小于 k，且同一 origin/client 在角色 k 的全部输入构成质量反链，所以间接贡献至多 Σ_(α:owner<k)A_αx。

可直接注入 t 的 source owner 只能为 k；该 source 的 W_α 就是 t 的规定完成叶，逐边上界因而使其直接密度贡献<=p_αx。多 query 只需将它们一起求和。因此

    c_Vt(x)h_tx
       <=Σ_(α:owner=k)p_αx+Σ_(α:owner<k)A_αx
       <=Σ_(α:owner<=k)p_αx<=1.                    (GENERAL-DENSITY)

没有使用最优 T、坐标 SD 身份、SPE 或 query 当前利润上界。optional-common 边只把父贡献从 h 降为至多 h，故整个家族同时适用。只有要把 current 金额解释为实际利润付款时，才需另用对应的完整 IC。source initial current/H/J 等资金不在此引理结论内。

本页 INIT 是该引理的特例 α=i、p_αx=p_ix、A_αx=a_ix。更一般 source 合同不能倒推本 LP 的初始预算或一般 ROLE 可行性。

## 5. 角色价格分离：精确但仍未付的对偶 cut

令 P0 为 INIT、I-PAY、R-FLOW 的多面体，暂不加 ROLE。§3 已证其非空。每客户初始质量至多1，严格 future 流无环，所有变量有有限上界；P0 是有限维紧凸多面体。对 v∈P0 定义

    F_l(v)=d_l+H_l+J_l+Σ_(t:role l,x)L_tx.

有限凸分离给精确条件：ROLE 有共同可行点，当且仅当对所有 λ∈R_+^m，

    min_(v∈P0)Σ_lλ_lF_l(v)<=2Σ_lλ_lu_l.            (PRICE-CUT)

必要性取同一可行点。充分性来自紧凸付款集合 F(P0) 与向下闭盒 {z:z<=2u} 的分离；若不相交，分离法向量可取 λ>=0，给严格反向不等式。这只是有限 LP/分离合同，不是新的实际资金上界。

R 内部流可按 [价格递推](common_edge_price_potential.md) 消元。给定 λ，若 ψ_t(x) 是该 optional-common 家族的最小终端价格，PRICE-CUT 左边等于较小 LP

    min  Σ_iλ_i(d_i+H_i)+Σ_(l,x∈I)λ_lJ_lx
          +Σ_(initial i,j,x∈R)a_ijx ψ_(W_i,<j,j)(x)
    subject to INIT and I-PAY.

ψ 只依赖固定图、客户与 λ，不依赖初始 a；同一客户各 common 边可同时取最便宜端点，GENERAL-DENSITY 对这些选择仍成立。I 的 J 容量与初始 d<=u 不能在消元时删除，它们保留了 source/current 与实际客户钱包的共同选择关系。

当 λ恒为1时，ψ恒为1，MASS 对所有 P0 点都给 Σ_lF_l=|O|。PRICE-CUT 的这一条正是 |O|<=2W。它未被证明，不能隐藏在对偶等价中。真实 off-history IC 怎样限制一般价格最优值仍是缺口。

## 6. 精确量词与交接

固定实例、完整 σ、固定 T 后，这是有限有理系数 LP；若可行，有有理证书，可用精确算术逐行核验。变量只分配金额，不修改 σ、query 完成叶或平局。选择另一个 T 必须重算分区、r/H/qhat 与入口；不能混合不同 T 的好部分。

为证明原目标，需要证明：每个原实例及每份完整纯 SPE，存在一个最优 T，使该共同 LP 可行。**该一般可行性命题仍 OPEN**，不声称它与 HALF 等价。构造阶段的局部 IC 只使用 actual-prefix 完整查询；证明一般可行性仍可能需要全部 off-history 可信约束，不可把任意满足部分行的 policy 当 SPE。

optional-common 家族一般不是旧 full-profit SAFE/CLIP 子核；本 LP 可行不自动证明旧限制路由 RESIDUAL-CAP。非最大初始 current 也意味着 d、I/R 源量、J 和 R 终端必须共同求取，不能先固定其中某一旧方案的数值。

m=1 时没有 future 图；空主题无正客户行。全零输入所有量与变量为0，不定义效率比。其它分母仅在相应动作确实覆盖该客户时使用。本页未运行新扫描，没有把线性化、密度或价格等价提升为新的共同容量 theorem。

[库存分支的合同重构及全文审查](../inventory/payment_primal_review.md)通过固定线性数据、任意初始分割、多 query 密度、一次 whole-IC、MASS/ROLE 充分性及价格分离；未覆盖一般可行性，不是外审或新颖性认证。

[独立分支的完整审查](../independent/linear_joint_payment_review.md)亦通过上述固定-T primal、任意 source/optional-common 密度、条件充分性及价格消元；特别说明 ψ 是同质流的单位成本系数，不声称可向任意 context 独立注入一单位而保持 IC 密度。一般可行性仍未证明。
