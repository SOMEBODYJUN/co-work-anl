# 同客户传播的全图密度上界：加强初始化与同角色父节点反链

2026-10-24，inventory8。任意有限共同目录、任意人数及每份完整历史依赖纯 SPE。**Q-CAG-HALF 仍 OPEN。** 本文给一般输入上的来源保持组件，不给共同实际钱包上界。空主题、重复主题及任意历史平局均保留。

Natural reset 始终是 `A_t=finish_sigma(B_<i,sigma_i(g))`，其中 B 是原实际叶；绝不是 `finish_sigma(g,B_i)`。许多不同 off-history 父节点可以合并到同一 reset 叶，本文允许合并。关键是同一**非实际目标 context**的全部父节点处在同一角色，因此在固定客户质量流中构成反链。

本地客户保持核已经见于 [peer 最大客户密度核 §2](../../../R-d3981c0168644971803a9c3380ed687c/next_general/credible/coordinate_support_attack.md)，本文不重新认作新核。新增候选组件是：加强 round7 全 O 初始化边界后，该核在全部实际生成的非实际 context 都满足逐客户利润密度不超过1。因此各 context 的 whole-IC 系数可以统一取1。**不同 context 同一角色的系数之和仍未控制。**

## 1. 更强初始化子容量保留原 current/future 总额

固定原完整策略 sigma、实际叶 B、实际利润 u_i，以及任意比较元组 T、并集 O；取最优时才使用 |O|=OPT。沿用 [round7 坐标初始化](../../round7/parent/optimal_coordinate_initialization.md)：对 x∈T_i，

    p_ix=1/c_T(x), d_ix=c_B(x)+1−1_(x∈B_i),
    W_i=finish_sigma(B_<i,T_i),
    r_ix=p_ix−P^B_ix≥0.

保留原全部 P^B 支付，记其 actual 列为 H_l。每条原 future 正边 j>i、x∈(W_i)_j\B_j 的子容量可进一步收紧为

    qhat_ijx=min(p_ix,1/d_ix)/c_Wi(x)
             ≤1/[d_ix c_Wi(x)].                    (NEW-CAP)

这特别要求每条初始化输出满足

    c_Wi(x) a_ijx≤p_ix.                            (INIT-DENSITY)

证明这仍允许原 current 总额。固定 (i,x)，缩写

    t=c_T(x), d=d_ix, w=c_Wi(x),
    nB=|{l:x∈B_l\T_l}|,
    n=|{j>i:x∈(W_i)_j\B_j}|,
    nMinus=|{j>i:x∈B_j\(W_i)_j}|.

因为 W_i 在 i 以前与 B 相同，w=d+n−nMinus。置 k=d−nB。若 x∈B_i，k=|B_x∩T_x|；否则 k=1+|B_x∩T_x|，共同 coverer 不含 i。故

    1≤k≤min(d,t),    r_ix=k/(td),
    qhat_ix=n min(d,t)/(tdw).

于是

    k w−n min(d,t)
      =kd−k nMinus+n[k−min(d,t)]≤kd≤td,

即 `(r_ix−qhat_ix)_+≤1/w`。先求和，之后只用实际节点 i 的一次完整合法偏离：

    Σ_x(r_ix−qhat_ix)_+≤u_i(W_i)≤u_i.             (INIT-WHOLE-IC)

故 b_i=(r_i−u_i)_+、r_i=Σ_xr_ix 仍不超过 `S_i=Σ_x min(r_ix,qhat_ix)`。若 S_i>0，取

    a_ix=(b_i/S_i) min(r_ix,qhat_ix),

否则全零；再按 qhat_ijx 比例分到各 j。则

    p_ix=P^B_ix+c_ix+Σ_j>i a_ijx,
    c_ix=r_ix−a_ix≥0,
    d_i=Σ_xc_ix=min(r_i,u_i)≤u_i,
    Σ_j>i a_ijx=a_ix≤p_ix.

H、d_i、b_i 与原初始化相同；只改变逐客户剪枝。每条边仍为原正边子容量。这里没有逐客户使用 IC。

若共同容量需要保留初始current余量，也可不固定最大current角点：任取 `0≤a_ix≤min(r_ix,qhat_ix)` 且 `Σ_x(r_ix−a_ix)≤u_i`，再在NEW-CAP边容量内分配。其future总额可从b_i到S_i选择，d_i相应降低。下面全图证明只用a_ix≤p_ix与INIT-DENSITY，故同样适用；若d或I/R分配改变，全部剩余预算及J必须重算。

## 2. 先定义同客户流，不预设密度界或调用 IC

将 a_ijx 注入真实 context `(W_i,<j,j)`，保留客户 x 与 origin i 两个标签。对每个 x∈O，其全部原始份额 Σ_i p_ix=1，未来初始总质量 Σ_i a_ix≤1。

在 natural context s=(g,l)，令

    V_s=finish_sigma(g), a_s=sigma_l(g),
    A_s=finish_sigma(B_<l,a_s),
    v_sx=1/c_Vs(x), D_sx=1/c_As(x)  (x∈a_s).

使用原 full-customer 正负原价：

    q^+_sjx=1_(j≠l,x∈(A_s)_j\(V_s)_j)/[c_As(x)c_Vs(x)],
    P_sx=Σ_jq^+_sjx,
    N_sx=Σ_j 1_(j≠l,x∈(V_s)_j\(A_s)_j)/[c_As(x)c_Vs(x)].

逐客户恒等式为

    v_sx−P_sx=D_sx−N_sx>0.                      (CLIENT-LOSS)

严格正性用于非空 action 的客户；空动作没有正输入。合并同 context、同客户全部输入 h_sx，再定义

    f_sx=h_sx/v_sx=c_Vs(x)h_sx.

每条 positive edge 发出

    f_sx q^+_sjx=h_sx/c_As(x),                  (X-FLOW)

并保留当前金额

    L_sx=f_sx(v_sx−P_sx)≥0.                    (CURRENT-X)

j>l 时进入真实 prescribed context `(A_s,<j,j)`；若该 history 是 actual prefix，直接作为 actual (j,x) 终端券吸收，不再使用 IC。j<l 时原边支持保证 x∈B_j，亦作为 actual (j,x) 券终止。当前 L_sx 是来源 x 标签的实际整行支付，并不声称 x∈B_l。

CLIENT-LOSS 给每个客户的精确质量守恒。future 角色严格增加；past 与 actual-prefix 均为终端。因此有限 DAG 唯一定义全部流，不用 IC 或 f≤1 假设。每客户行和 P_sx/v_sx<1。

固定一个 origin i 和客户 x，任意固定角色 k 上全部 natural contexts 的 h_sx 总和≤该 origin 的初始 future 质量 a_ix。理由是角色严格增加，每条分拆的质量路径至多访问该层一次；也可按逐层 sub-Markov 守恒归纳。这是同角色质量反链，不是把不同父历史合并成一个 context。

## 3. 所有非实际 context 的全图密度界

**GLOBAL-CLIENT-DENSITY。** 对上述同一份流、每个非 actual-prefix context t=(g,j) 和每个输入客户 x，

    0≤f_tx=c_Vt(x)h_tx≤1.                      (DENSITY-ONE)

证明。令 k<j 是 g 与 actual prefix 首次不同的位置。任意 natural positive future edge 若进入 t，其父节点 s 的 reset 叶为 `finish_sigma(B_<r,a_s)` 且在 j 前等于 g。若 a_s=B_r，reset 叶就是 actual B，不可能进入非 actual t；否则该叶第一次偏离 actual 恰在 r。因此所有父节点均有角色 r=k。

父节点可以很多、history 可以不同，但 action 都为 g_k，其 reset 完成叶均为同一 V_t。由 X-FLOW，每个父节点 s 对目标密度 c_Vt(x)h_tx 的贡献恰为 h_sx。

初始 owner i 只向角色>i 注入，而后续角色继续增加。所以到达这些角色 k 父节点的来源必有 i<k。用第2节同角色反链，

    Σ_(s→t)h_sx≤Σ_(i<k)a_ix.                   (PARENT-ANTICHAIN)

直接初始化注入若到达 t，其 owner 亦必须是 k（其 W_i 第一次偏离 actual 恰在 i）。INIT-DENSITY 保证直接注入对目标密度贡献≤p_kx；没有对应 source/边时该项为0。合计得到更强的前缀界

    f_tx≤p_kx+Σ_(i<k)a_ix
        ≤Σ_(i≤k)p_ix≤1.                        (PREFIX-DENSITY)

这允许多个 off-history 父节点的真实合流，由同角色反链共同支付。证毕。

**实际 history 边界。** actual-prefix 目标可以接收由许多不同角色 reset 的流，没有首偏离 k；本文不声称它的 h_tx≤v_tx。这些目标已定义为 actual 同客户终端，其容量单独进入共同账。

## 4. 一次完整 IC 与精确非负退款

对非 actual s=(g,l)，actual-prefix 完整 IC 给

    D_s=Σ_(x∈a_s)D_sx≤u_l,   e_s=u_l−D_s≥0.

将 action 中没有输入的客户取 f_sx=0。DENSITY-ONE 与 CLIENT-LOSS 给

    L_s=Σ_xL_sx
       =Σ_x f_sx(D_sx−N_sx)
       ≤Σ_xD_sx=D_s≤u_l.                      (ONE-WHOLE-IC)

只调用同一条完整 IC 一次。可从该整行利润安全退还

    u_l−L_s=e_s+Σ_(x∈a_s)(1−f_sx)D_sx
                      +Σ_(x∈a_s)f_sx N_sx≥0. (EXACT-REFUND)

故净 current 可按实际 l 原利润份额统一支付，净系数 κ_s=L_s/u_l∈[0,1]。这没有让每个 singleton 客户各领一次 u_l。正输入使 a_s 非空，actual-prefix IC 因而保证 u_l>0；零输入节点略去。

## 4.1 root 补充：共同 coverer 增边家族

root 从上述核指出：保留每条原 positive edge 的 h_sx/c_As(x)，还可对任意共同 future coverer `j>l, x∈(A_s)_j∩(V_s)_j` 加入任意

    0≤z_sjx≤h_sx/c_As(x).

令新current为 `L'_sx=L_sx−Σ_jz_sjx`。原positive与共同coverer共占A_s当前以外至多c_As(x)−1人，故

    h_sx/c_As(x)≤L'_sx≤L_sx.

逐客户质量仍守恒，current非负，ONE-WHOLE-IC与EXACT-REFUND继续成立（退款再加Σz）。每条新增future边进入真实A_s prescribed context，目标密度贡献≤h_sx；§3的同角色父节点/质量反链证明逐字适用，整个增边家族仍有f≤1。

R-only时A_s没有past x-coverer。把所有共同future边取满，全部A_s future coverer各得h_sx/c_As(x)，当前亦恰得h_sx/c_As(x)。这是旧按query coverer均分的uniform-reset角点，不认领为新核。raw正差核是共同边全取0的另一角点。

全O还可给共同past coverer加入≤h_sx/c_As(x)的actual(j,x)终端券；支持合法且current只减。共同past与future全取满时，正差加共同边恰为全部A_s其他coverer，得到同客户uniform-reset（包括actual past券）。新增past出口必须与原H、d及其他终端共用实际预算。

此为保留客户、允许向后移动当前付款的选择家族，一般不是旧SAFE/CLIP子核。只证明局部合法性与全图密度，未证明存在满足共同剩余容量的一点。有限DAG中原正差边固定为h/c_A，共同边在[0,h/c_A]内，current等于输入减出流；这是线性流条件，同角色实际容量仍是额外未证的可行性约束。

## 5. 同两份钱包的联合账仍有未付项

记 E_lx 为全部 past/actual-prefix actual 客户终端。固定同一初始化及本次客户保持流，

    |O|=Σ_l(d_l+H_l)+Σ_(s非actual)L_s+Σ_lx E_lx. (JOINT-LEDGER)

每个原 O 客户始终恰一单位，传播不会重采到 O 外客户。E_lx 只支持 x∈B_l。current L_s 的 x 标签仍不要求 x∈B_l。

同一实际角色 l 可出现多个 s。ONE-WHOLE-IC 只给各 L_s≤u_l；真正还需

    Σ_(s:i(s)=l)L_s+Σ_xE_lx≤2u_l−d_l−H_l       (STILL-OPEN)

对所有 l 同时成立，或足以推出总和≤2W的更弱共同关系。本文没有证明它。单节点 κ_s≤1 不推出同角色 Σ_sκ_s≤1。

### 5.1 全 I / 仅 R 两个合法接口

也可先用 [peer I-future 互补付款](../../../R-d3981c0168644971803a9c3380ed687c/next_general/global_credit/coordinate_residual_attack.md)清除全部 I=O∩C 的 future 来源，保留同一次初始化的 d、H，并由本次新 a_ix 的 I-future 质量重新计算补余实际券 J；不能继承旧剪枝的 J 数值。仅将 R=O\C 的原 a_ijx 送入本核。DENSITY-ONE 继续成立，因为删除来源不增加 h；source 标签与传播客户始终同为 R。

R 客户不被任何 actual action 覆盖，所以没有 past 正券，也不可能进入 actual-prefix sink。这时全部未付质量仅为各 natural s 的 L_s^R。原完整 IC 的退款额可写为

    u_l−L_s^R=e_s+Σ_(x∈a_s\R)D_sx
              +Σ_(x∈a_s∩R)(1−f_sx)D_sx
              +Σ_(x∈a_s∩R)f_sx N_sx≥0.

尤其没有把 actual C 或 O 外 fresh 的查询收入另领为额外库存。联合两钱包剩余仍然要求

    Σ_(s:i(s)=l)L_s^R≤2u_l−d_l−H_l−J_l.         (R-STILL-OPEN)

本稿未证明这个角色汇总界。

### 5.2 与原 SAFE/CLIP 的关系

客户保持核用各自 f_sx=h_sx/v_sx 缩放客户，原 full-profit SAFE 用同一个 h_s/v_s；有的边可比旧 SAFE 边更大。因此一般不是旧核的删正边/CLIP 版本，未证明相对旧核费用单调，也不证明原限定 full-SAFE 的 RESIDUAL-CAP。

## 6. 状态及接点

解析新增关系是 NEW-CAP 与 DENSITY-ONE：它们把原 OPT 客户库存接到全部未来 whole-IC，保留客户身份，并把每个非实际 context 的最大客户密度控制为1。无需误用相反 reset 的唯一父节点结构。

这回答同客户库存能否合法存活于未来 whole-IC，并给出明确非负退款；没有解决这些局部付款共享同一实际角色两份钱包的问题。一般 half 仍 OPEN，未扩大已证输入范围。[independent8 独立合同重构并对稿](../independent/coordinate_density_review.md)通过 NEW-CAP、raw 同客户核、全图密度、one-wholeIC 及 full-O 联合账；其后亦读取 peer 接口，确认 §5.1 的 I-cashout 合成（重算 J）合法。审查不含同角色汇总 cap，未作外部新颖性认证。

[精确 policy 诊断](role_density_aggregation_boundary.md)表明同一角色全部 f 可达7/6，不能从单 context 密度界直接相加得到角色密度界。该诊断明确非 SPE，仅攻击纯流结构推论；current 聚合及原一般目标未被反驳。
