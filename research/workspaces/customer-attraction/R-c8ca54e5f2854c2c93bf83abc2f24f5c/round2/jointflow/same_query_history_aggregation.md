# 同角色全 query 的未来覆盖密度与 normalized current 库存

2026-10-25。**身份：全输入流聚合引理 v1；Q-CAG-HALF 及不同 query 的共同角色预算仍 OPEN。**
适用于原单位客户、任意共同有限非空目录、任意人数和全部有序历史纯 SPE；流不等式本身对任意完整纯 policy 成立，SPE 只在完整 query 的最后付款时使用。重复、空主题、任意平局和零客户均保留。无外审或新颖性认证。

## 1. 固定合同及结论

采用既有 [R-only optional-common 流](../../../R-cd789330fc7141299ac491bbb3ffa420/round8/residual/linear_joint_payment_certificate.md) §1–2。固定完整 policy sigma、实际叶 B；R 为实际并集外客户的任意子集。自然 context s=(g,j) 定义

    a_s=sigma_j(g), V_s=finish_sigma(g),
    A_s=finish_sigma(B_<j,a_s).

对 x∈R∩a_s，令 E_s(x) 为 A_s 中覆盖 x 的角色集合、e_s=|E_s|。由于 x∈R，min E_s=j。输入 h_sx 沿严格 future 边 tau(s,l)=(A_s,<l,l) 分流：

    z_slx=h_sx/e_s           (l∈E_s, x不被(V_s)_l覆盖),
    0≤z_slx≤h_sx/e_s         (l∈E_s, x也被(V_s)_l覆盖),
    L_sx=h_sx−Σ_(l>j)z_slx.

源 alpha 的 owner 为 i(alpha)，真实 actual-prefix query 叶为 W_alpha，库存 p_alphax≥0 满足 Σ_alpha p_alphax≤1。初始边仅注入 W_alpha 中覆盖 x 的严格未来角色，且

    0≤b_alphalx≤p_alphax/c_Walpha(x).

原 INIT 还要求初始总 future≤p；本引理仅用逐边容量。图从初始 query 叶的真实 future prescribed contexts 出发按 reset 边闭包；允许真实节点合流，不合并不同有序 histories。

**未来覆盖密度结论。** 记 c_alphax=c_Walpha(x)，q_alphax 为 W_alpha 中 owner 严格未来的 x-coverer 数；c=0 时这一源项按零计算，因为没有合法 x 初始边。令

    B_kx=Σ_(alpha:i(alpha)<k)p_alphax q_alphax/c_alphax.

对任意角色 k、任意 x∈R，任意同一份可行 optional-common 流均有

    Σ_(s:role(s)=k)h_sx |C_x(V_s)∩{k,...,m}|≤B_kx≤1.   (TAIL-DENSITY)

这是父方另一研究员 curvature 独立重构时给出的精化；同角色全 action normalized current 为其推论：

    Σ_(s:role(s)=k)c_As(x)L_sx≤B_kx
       ≤Σ_(alpha:i(alpha)<k)p_alphax≤1.             (LAYER)

无正输入的坐标贡献为零。R 的 source 实际前缀不覆盖x，所以 c=q+eta，其中eta为source query本身是否覆盖x的0/1指标。每个非零分母项 p q/c=p(1−eta/c)。原 INIT 的 source query 都覆盖 x，eta=1，故

    Σ_(s:role(s)=k)c_As(x)L_sx
       ≤Σ_(alpha:i(alpha)<k)p_alphax[1−1/c_Walpha(x)].  (LAYER-SOURCE)

若广义 source query 不覆盖x、仅真实尾部覆盖x，则eta=0，该项是p，不能误用1−1/c；例如c=1时后者为零而真实 future 源可非零。左端是 reset-normalized current **c_A L**，不是旧 prescribed density **c_V h**。

**同 query 完整 IC 推论。** 固定合法 query a，令 A=finish_sigma(B_<k,a)。所有 role=k、prescribed action=a 的 histories 共用 A。由非负性和 (LAYER)，

    Σ_(s:role k,a_s=a)Σ_x L_sx
      ≤Σ_(x∈R∩a)1/c_A(x)
      ≤u_k(A)≤u_k(B).                              (HQ-IC)

这是在调用 IC 之前聚合全部同 query histories，再调用这一条 actual-prefix 完整 IC 一次。最后一步才需 SPE。不同 query 的完整行系数仍不能免费相加。

## 2. 目标层的真实 current 报酬

固定 k,x。对每个 role(s)=k 目标节点，写 D_s=E_s(x)，min D_s=k。mandatory 出口恰是 D_s 中原 V_s 未覆盖 x 的角色；全部在 k 之后。其余 common 出口只降低 current。因此

    c_As(x)L_sx
      ≤h_sx[|D_s|−|D_s\C_x(V_s)|]
      =h_sx|D_s∩C_x(V_s)|
      ≤h_sx|C_x(V_s)∩{k,...,m}|.                   (TERM)

C_x(V) 表示 V 中覆盖 x 的角色集合，包含过去和未来。raw（common 全零）时到共同coverer交集的第一界为等式；这里不能删掉共同 coverer 因子。

## 3. 目标层之前每单位输入的全部报酬至多一

固定这份流，正输入节点定义 rho_sl=z_slx/h_sx；零输入节点任取不超过1/e_s的非负比例。每条比例≤1/e_s，角色严格增加。角色 k 目标的每单位终端报酬取更强的未来覆盖数

    P_s=|C_x(V_s)∩{k,...,m}|.

超过 k 的节点报酬为零；没有 x 输入/覆盖的节点也为零。对 j<k 的节点按逆角色定义

    P_s=Σ_(l≤k)rho_sl P_tau(s,l).

这是同一固定流的线性终端报酬，不是重新选择策略或查询。逆向归纳给全部 role(s)=j<k 的 P_s≤1：设 E=E_s(x)，e=|E|，
每个 l<k 孩子按归纳至多一；至多有一个 l=k 孩子 t，其规定叶 V_t=A_s。
故该孩子的报酬恰为

    P_t=|E∩{k,...,m}|.

从而

    P_s≤[|E∩{j+1,...,k−1}|+|E∩{k,...,m}|]/e
       ≤(e−1)/e≤1.                                (BACK)

两类角色不交，且不含当前 coverer j∈E。若 E 不含 k，根本没有 k 孩子，保留全部≥k coverer 的上界仍合法。证明不依赖目标query或其reset集合，故得全 action 的 (TAIL-DENSITY)。

## 4. 初始来源只付一次

对 owner i<k 的源 alpha，令 C=C_x(W_alpha)，c=|C|。初始注入 l<k 的未来报酬≤1；若注入 l=k，其 V=W_alpha，报酬≤|C∩{k,...,m}|；l>k 不再到达目标。逐边初始容量因此给总报酬上界

    (p_alphax/c)
      [|C∩{i+1,...,k−1}|+|C∩{k,...,m}|]
      =p_alphax q_alphax/c_alphax≤p_alphax.        (SOURCE)

两个集合是互不相交的 C 子集，联合恰为C中owner严格未来的q个coverers。若 source query 自身覆盖 x，则 i∈C 没计入括号，右端为 p_alphax(1−1/c)。若c=0没有边，贡献为零，不计算0/0。owner i≥k 的源不能通过严格 future 边到达 k。

逐源求和，在线性合流图上每个初始质量的总报酬等于目标层终端报酬之和，得到 (TAIL-DENSITY)；结合 (TERM) 得 (LAYER)，原INIT的eta=1给 (LAYER-SOURCE)。
所有初始分母仅在存在相应 x-coverer 边时使用，无覆盖便无边。零库存、空动作、零输入不产生项。

## 5. 与旧 uniform 角点及仍未付的标量质量的区别

旧 [同 action uniform-reset 去重](../../../R-cd789330fc7141299ac491bbb3ffa420/round8/residual/common_action_reset_deduplication.md) 使用 common 全满、L=h/c_A，(LAYER) 退化为旧同层输入反链 Σh≤1。旧 [捕获命中界](../../../R-cd789330fc7141299ac491bbb3ffa420/round3/mixed/capture_hitting_capacity.md) 也针对这一全 coverer 均分核。
本稿对任意 optional-common、特别 raw common 全零保留 |D_s∩C_x(V_s)| 因子，旧 Σh≤1 不直接控制这个 current 报酬。
旧 [7/6 prescribed-density 诊断](../../../R-cd789330fc7141299ac491bbb3ffa420/round8/inventory/role_density_aggregation_boundary.md) 不反驳本式：其 role3 的 c_A L 总和为5/12，7/6是另一量 c_V h。

具体地，设

    theta_(k,a,x)=c_A(k,a)(x)Σ_(s:role k,a_s=a)L_sx,
    lambda_(k,a)=max_(x∈R∩a)theta_(k,a,x)  （空集合取0）。

本文证明 Σ_a theta_(k,a,x)≤1，且每个 query 的 current 可由 lambda_(k,a)u_k 付款。
但 **Σ_a max_x theta_(k,a,x)** 不能由 **max_x Σ_a theta_(k,a,x)** 控制，故未证明 Σ_a lambda_(k,a)≤1。
也未证明它们与原 d,H,J 共用实际角色2u容量总能足够。不同 query 的完整行总质量/真实 IC 耦合仍未付；不能把 (LAYER) 当 ROLE 或 half。

原 INIT 的初始 current c_kx 不能免费加入左端：旧合同仅要求 Σ_xc_kx≤u_k，没有逐客户 c_kx≤p_kx/c_Wk(x)。owner=k 的 future 边不会返回k，但初始 current 乘 c_Wk 后仍不受其 p_kx 券控制。
若另加此逐客初始 current 容量，可将 owner=k 的这一初始金额与同源p一次计入；尚未证明附加限制不损 INIT 可行性，本稿不作该扩张。

同一证明代入 m=5 仍只给 (LAYER) 和逐 query 的 (HQ-IC)，没有无条件推出 OPT_5≤2W。无人数专项、无新目录限制、无策略修改。

## 6. 来源与实际审查

source/reset/optional-common 合同来自§1链接的旧 joint certificate；逐 context 密度来源为 [旧正文](../../../R-cd789330fc7141299ac491bbb3ffa420/round8/inventory/source_preserving_density_envelope.md)。
本次推导是任意 optional-common 的终端系数 (TERM)、前层报酬界 (BACK) 及其全 action 合成 (LAYER)。父方先收到精确合同，未读本稿独立重构 fixed-query 与 all-action 两版通过。父方另一研究员curvature只收合同独立重构主式通过，并指出广义source的eta/c=0边界、给出更简未来coverer数phi。由此加强为 (TAIL-DENSITY)，属本分支与该独立重构的共同推导，不独认。两次检查均保留 R-only、strict future、初始 current 和不同 query 标量总量的限制。无外审或新颖性认证。

作者的 [定义级 Fraction 审计](audit_layer_current.py) / [输出](layer_current_audit.json) 重建两份固定完整 arbitrary policies：旧7/6 prescribed-density重入诊断，以及一份含a、c两个覆盖同客户标签的固定policy。另用两个最小policy核广义source query不cover但tailcover（eta=0,c=1）及c=0无边边界。各检查common比例0、1/2、1，逐节点核 (TERM)、逐层核 (TAIL-DENSITY)/(LAYER)、全部初始注入质量吸收；两query policy的分数/full common角点在同一角色确有不同query正current。十二项均精确通过。它们明确非SPE，检验的是不需要SPE的流引理，不是一般half的有限证据，也没有新增参数搜索。
