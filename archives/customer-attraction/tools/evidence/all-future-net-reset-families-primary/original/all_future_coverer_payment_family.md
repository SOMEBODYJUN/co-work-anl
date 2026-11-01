# 同客户付款的全部后继覆盖者选择族

2026-10-24，root。精确身份 `B10-ALL-FUTURE-COVERER-PAYMENT-v1`。适用于原模型任意m、任意有限共同目录、每份完整历史纯SPE。本文给比第八轮固定新增边更大的合法付款选择族；不证明共同ROLE可行，不新增half已证范围。取消同客户正负项本身已有旧来源，本文不认领它。

## 1. 固定真实域与局部线性约束

沿用[第八轮固定元组证书](../../round8/residual/linear_joint_payment_certificate.md)。实际叶B、比较叶T（证明合法性不要求最优）、R=union(T) minus union(B)。固定自然context t=(g,i)，原规定动作a_t，原规定叶V_t；actual-prefix重置后强制同一a_t所得真实叶A_t。R客户x∈a_t有

    v_tx=c_Vt(x)≥1,   a_tx=c_At(x)≥1。

actual prefix从不覆盖R，故A_t的覆盖者恰为当前i与q=a_tx−1名未来真实规定玩家。令Q_t(x)为全部这些未来覆盖者（包括原两叶共同覆盖者）。给输入h_tx≥0，每条边目标仍是(A_t,<j,j)。用线性约束

    0≤z_tjx≤h_tx/a_tx  (j∈Q_t(x)),
    L_tx=h_tx−Σ_jz_tjx,
    0≤L_tx≤(v_tx/a_tx)h_tx。                         (ALL-FUTURE)

总出流上界自动给L_tx≥h_tx/a_tx，所以局部范围为

    h_tx/a_tx≤L_tx≤min(h_tx,v_tx h_tx/a_tx)。

所有future边全满时L=h/a，故每个给定输入均存在局部可行点。边仍严格增加角色，客户身份不变，不制造新源或新客户。

## 2. 密度和完整IC合法性

[第八轮反链密度证明](../../round8/inventory/source_preserving_density_envelope.md)仅需：每源客户库存p、source总future≤p、source逐边≤p/c_W，内部每条边≤h/c_A，以及每客户非负守恒。它不需要新增边必须全满。

因此ALL-FUTURE对每个允许选择同时保留全部非实际context的f_tx=v_tx h_tx≤1。证明仍是：目标首次实际差异位置k固定所有父节点角色；每个父边对目标密度贡献≤父h；同源在角色k的父节点构成质量反链。不能把多个父密度上界直接相加，也不能假设唯一父。

局部付款满足L_tx≤f_tx/a_tx。先对x求和，再用一次完整actual-prefix IC：

    Σ_xL_tx≤Σ_(x∈R∩a_t) f_tx/c_At(x)
             ≤Σ_(x∈a_t)1/c_At(x)=D_t≤u_i。

没有重权原IC。若e_t=u_i−D_t，单context退款可明确写为

    u_i−Σ_xL_tx =e_t+Σ_(x∈a_t\R)1/c_At(x)
       +Σ_(x∈R∩a_t)[(1−f_tx)/c_At(x)
                       +f_tx/c_At(x)−L_tx]≥0。

这是每context的一份完整query上界；尚无同角色所有context总和上界。

## 3. 与旧正边、NET取消和uniform角点的关系

记新A覆盖者数n、共同覆盖者数r（含当前）、离开V覆盖者数ell，则a=r+n，v=r+ell。第八轮家族强制每条新增边h/a，共同future边可选；其出流总量≥nh/a≥(a−v)_+h/a，所以全部属于本新族。uniform全部未来全满也是共同角点。

同客户正负价净取消已见[peer核独审§4](../../../R-d3981c0168644971803a9c3380ed687c/next_general/credible/clock_cycle/source_preserving_kernel_review.md)和[round5 NET](../../round5/credible/all_fresh_submarkov_elimination.md)。旧NET允许抵消min(n,ell)，把必要剩余(a−v)_+份保留在原新增覆盖者上。它已经给相同最大current；不把净取消或最大current称作新结论。

ALL-FUTURE额外允许将必要出流改送共同覆盖者；只要求每条真实覆盖者边≤h/a与总量≥(a−v)_+h/a。它包含上述受限接收者家族，且包含关系在局部可行多面体上可以严格；没有证明它使一个原来不可付的完整SPE变得可付。

局部差异示意：a=4,v=3，有当前、一个共同future、两个新增future，V还含一个离开的past覆盖者。价格当前1，共同后继0，两个新增后继各2。按每单位h归一化，旧固定新增边最小价5/4，旧NET取消再加共同边最小价1，新族可只向共同后继送h/4而current留3h/4，价3/4。取h≤1/3符合密度1。这里只比较局部可行多面体，不声称给出完整SPE或target反例；不以局部价格改善代替全树资金。

## 4. 一般价格递推

给非负实际角色价格lambda_i；后继单位成本psi_j按从小到大排序psi_(1)≤…≤psi_(q)。令d=(a−v)_+，β_j=a z_j/h（h=0全零）。条件是0≤β_j≤1、Σβ_j≥d，故线性最优点可取β∈{0,1}，得到

    Psi_t(x)=min_(k=d,...,q)
      [(a−k)lambda_i+Σ_(j=1)^k psi_(j)]/a。

即先取所有比current便宜的后继，再用最便宜边补足d。此为流单位成本，不是允许在任意节点另注入一单位。lambda恒1时每项都为1，仍无总资金增益。payment9从合同独立推导同一式。

## 5. 合并证书与精确剩余

把原R-FLOW换成ALL-FUTURE，保留source、H、I补余、同一ROLE上界2u。可同时采用[可变比较所有权](../payment/roleobstruction/fractional_ownership_extension.md)，但H、source、I补余必须按同一点重算。非ROLE部分仍非空（canonical所有权+uniform流）；质量守恒仍给|O|=Σ_i实际角色总付款。任何ROLE可行点因此推出|O|≤2W。

一般存在性依旧未证；lambda=1仍正好要求|O|≤2W，不能从价格优化或扩大选择空间得出它。代入m=5仍只有同一条件蕴含，没有任意五人的无条件half；本族的局部改善不能承担未付总资金。

menu9与payment9在收到合同后独立重构局部范围、反链适用条件和wholeIC合法性；正文/旧来源核对见各自独审。外审及新颖性均未认证。下一项有效进展须是利用真实off-history IC给跨不同query的总额关系，或直接证明原覆盖不等式。

## 6. 整行退款内取消边：更宽的客户保留选择

menu9独立提出并在其[核查§7](../menu/net_all_reset_kernel_review.md)展开：保留相同边上界、同客户守恒与非负current，但可将逐客户上界换成单一整行限制 Σ_xL_tx≤u_i。

非ROLE部分仍非空：uniform点L_tx=h_tx/a_tx有ΣL≤Σf/a≤D_t≤u_i。从该点取消任意原有边质量，留回它自己的客户current，直到总current达min(Σh,u_i)即可。没有客户重采；取消量至多原整行退款u_i−Σh/a，不会超支此context的一次actual完整行。下游输入减少，按原每客户出流比例重算，质量/边上界及密度继续成立。

这移植的是旧scalarCLIP的整行退款思想，结合已证客户保留边界；不认领新的福利资金。给定当前输入后，可先留β_*u_i（β_*=max_x f_tx≤1）而非u_i作为较窄上界，仍有uniform可行。β_*依赖输入的max，不能在全图联合求变量时当作固定线性系数；本页ROW线性家族用固定u_i，不把β_*窄版混成同一LP。

这个更宽家族允许不同客户共享本context未用退款，故§4逐客户可分价格DP不能原样用于它；应保留客户间共同整行约束解有限LP。多个context仍共享同一个actual role，必须保留原ROLE；不能每个context领完一份u_i再相加。所有常数价格下总额依然|O|。
