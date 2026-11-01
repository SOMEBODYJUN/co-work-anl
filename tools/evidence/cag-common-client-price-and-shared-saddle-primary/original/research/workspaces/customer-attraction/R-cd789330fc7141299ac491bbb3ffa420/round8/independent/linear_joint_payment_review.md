# 固定 T 共同付款 LP 与广义 source 引理的独立审查

2026-10-24，independent8。完整读取 [primal handoff](../residual/linear_joint_payment_certificate.md)及其 [common-edge 价格递推](../residual/common_edge_price_potential.md)，并按原单位客户公式重构。审查范围为这些明示的有限线性充分接口及广义 source 密度；**所述接口通过，未发现代数、历史域或符号错误。一般可行性及 Q-CAG-HALF 仍 OPEN。** 不作外审或新颖性认证，没有新扫描。

## 1. 非最大 current 的 INIT 与重算 I-PAY

对固定 T，p、P_B、r、H、qhat 及所有 completion 都是固定原策略数据。任意 INIT 点的 a>=0、c>=0、c+Σa=r，给 a_ix<=r_ix<=p_ix，逐边 qhat 又给 `c_Wi a_ijx<=p_ix`。这些正是密度定理需要的合同；不需要把 d 固定为原 maximal current。

任意这样的点仍逐坐标保留 `p=P_B+c+a`。固定 x∈I 求 owner 和，`1=H_x+C_x+A_x`。同一 actual 客户份额 w 的未花总额为 1−H_x>=A_x，且 H_lx<=w_lx。因此 I-PAY 必有非负补余分配；零总容量时 A_x=0。J 必须由这个点的新 A_x 共同选择，不能继承另一初始化的数值。原文没有混用这些选择。

I 支付只花同一第二 actual 客户钱包的余量，current d 只花第一整行预算。J 可以送到较早实际角色，因为没有调用该角色的 IC。付清的 I 不再进入 R 图，未重复领取库存。

## 2. 固定有序 DAG、optional-common 与自动密度

图从全部可能初始 R 边作闭包。它们、V_t、a_t、A_t、Q/N/M 都由原完整 σ 和固定 T 决定，不受 a,z 的金额改变。每条 future 边都严格增大角色，且 recipient 选择同一 x，所以有限有序 DAG 保留合法规定叶；同负载不同历史没有合并。

R 无 actual coverer，因此 reset A 的 x-coverer 正好是当前与 Q。N、M 不交，且 `1+|N|+|M|=c_A`。故 raw mandatory 输出、optional-common 上界给

    h/c_A<=L=h−Σz<=h(1+|M|)/c_A。

所有输入为零时 DAG 递推强迫所有后续为零；不可能由任选 z 创造无源流。来源可按各节点当前输入占比事后拆分到每条边，h=0 时无需作比例。因此每个 origin/client 在同一角色层的质量反链上界仍成立，尽管 z 是合并后才选择的变量。

固定非实际 target，首个实际有序差异 k 强迫所有 natural parents 都在角色 k，reset 叶等于该 target 的规定叶。mandatory 单边目标密度贡献为父 h，common 不超过父 h。到这些父节点的 source owner<k；直接 INIT owner 只能为 k。所以原文 `f_t<=p_k+Σ_(i<k)a_i<=1` 对每个非最大 INIT 点和每个 optional-common 点都成立。它不是新增 LP 约束，也没有先假设密度再证明非负流。

`1+|M|<=c_V`，所以对同一 context，L_x<=h_x c_V/c_A<=1/c_A。先求和到完整 query 利润，再只用一条 actual-prefix 原 IC，得 Σ_xL_x<=u_k。没有按客户重权 IC。这个结论仍不能将同角色的多个 context 费用免费相加；ROLE 是另外的真正共同约束。

## 3. MASS+ROLE、有限性与一般性状态

INIT 的所有 O 客户库存和恰为 |O|。I-PAY 清掉同一点的全部 I-future。R 图有限守恒且没有 past/actual-prefix R sink，故全部 R 输入最后恰成为 ΣL。原 MASS 与 ROLE 的相加即给 |O|<=2W，固定 T 充分接口正确。

除 ROLE 外的系统非空：加强初始化的正部关系给一个 INIT 点；任意 INIT 点有上述 I 补余；然后 common 全零依角色递推给 R-FLOW。所有变量受有限客户库存及有限 DAG 的路径守恒控制，因此 P0 非空、闭、有界，固定实例下为有理系数有限 LP。m1 无 future；空行动无客户变量；全零点合法；各倒数都只在相应覆盖客户上使用。

一般性结论严格止于“若 LP 可行，则该 T 的 |O| 被支付”。每个完整 SPE 是否存在某个最优 T 使 ROLE 同时可行仍未证；本审查不把它改称 HALF 的等价定理。

## 4. 不需 SPE 的多 query / 同 owner source 引理

§4 的 source 合同也通过。只需要有限原纯 policy、每 source 严格未来的真实 prescribed 目标、总库存 Σ_αp_αx<=1、总注入 A_αx<=p_αx 以及逐边 `b_αjx c_Wα(x)<=p_αx`。正输入目标本身覆盖 x，故 c_W>0；source 查询当前是否覆盖 x 并非密度证明所必需。

同 owner 有多个 query 不破坏首偏离论证。直接到达非实际 t 的 source 都必须 owner=k，且其 W_α 正是 V_t，所以直接密度合计≤Σ_(owner=k)p_αx。经父节点到达的同一客户质量，按 origin 反链合计≤Σ_(owner<k)A_αx。相加得到 GENERAL-DENSITY。actual-prefix targets 按正文作物理 actual 客户 sink，不套用不存在的首偏离 k。

此段没有使用 SPE、最优 T、SD 或当前 query 上界。也没有为任意 source 附送 initial current/H/J 钱包。只有把 current 转为 actual 利润支付时才需另用完整 IC，原文界线正确。

## 5. PRICE-CUT 与 R 价格消元

F(P0) 是紧凸支付集合，和向下闭盒 z<=2u 不相交时，分离法向量可取非负：任何负坐标都会使向下无界盒的线性上确界无限。因此原 PRICE-CUT 的 min、方向及 λ>=0 域正确。

暂去 ROLE 后，内部各客户的 common 选择没有共享容量约束。固定 λ，有限 DAG 的每个 common 份额选择 current 价格 λ_i 或 child 价格，恰给 PRICE-DP 的 min；端点选择可同时采用。density 对整个选择族自动成立，所以消元没有丢掉一个隐藏的跨节点可行性条件。ψ 的“一单位”是同质流的单位价格系数，不是声称可向任意 context 单独注入一个违反 source 合同的合法 IC 单位。

保留 INIT 和 I-PAY 后，原较小 LP 的目标确为 λ(d+H)+λJ+Σa_Rψ。λ全1时 ψ全1，MASS 使价格条件正是 |O|<=2W；原文明确说此条未证明，没有把目标藏入分离等价。

结论：primal、source 引理与价格 handoff 的明示关系均通过；尚无一般 ROLE 可行性或新的 actual 总预算。
