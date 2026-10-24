# 同客户坐标核与非实际密度：独立重构及对稿审查

2026-10-24，independent8。原有限单位客户、任意有限非空共同目录、任意人数、每份完整有序历史纯 SPE；全部平局、重复及空主题均保留。**Q-CAG-HALF 仍 OPEN。**

审查对象为 inventory8 的 [同客户传播全图密度](../inventory/source_preserving_density_envelope.md)。先收到 root 的精确陈述并独立重构；INIT 分情况证明、局部原边容量和最早偏离/反链推导已在读作者正文前发给作者。随后完整读取正文对稿。本次不是完全无公式提示的盲发现，不认领旧客户核的新颖性。**§1—4、§5 的同一全 O 账以及追加核对的 §5.1 I-cashout 接口通过。没有 actual 钱包汇总结论。**

## 1. 加强 INIT 的独立证明

固定 owner i 和 x∈T_i。写 `t=c_T(x)>=1`、`p=1/t`、`d=c_B(x)+1-1_(x∈B_i)>=1`、`w=c_Wi(x)>=1`，原坐标余量 `r=p-P_B∈[0,p]`。令 n 为未来 W-new coverer 数，nMinus 为未来 W-lost coverer 数，所以 `w=d+n-nMinus`。

作者把每条未来边裁成 `min(1/d,p)/w`，合计 `qhat=n min(1/d,p)/w`。下式成立：

    (r-qhat)_+ <=1/w。

我在读作者正文前的证明分两种。若 d≥t，qhat 是原 q_W 总额，原 COORD 直接给 r−qhat≤1/w。若 d<t，r≤p 且 w≤d+n≤t+n，故 `wr≤wp≤1+np`，仍给 r−qhat≤1/w。右侧非负，所以取正部合法。

求和后只用一次完整 IC：`Σ_x(r-qhat)_+≤u_i(W_i)≤u_i`。原 b_i=(Σr−u_i)_+ 不大于 Σmin(r,qhat)，所以原 current/future 总额可保留，按 qhat 分配即可。每个新边 `a_ijx≤p_ix/c_Wi(x)`，而该 owner 对 x 的未来总输出仍不超过 p_ix。作者的 k=d−nB 计数证明与此一致；其 nB 不需另排除 i，因为 x∈T_i 已保证 i 不属于 B\T。

## 2. 局部客户流及完整 IC

正确 reset 为 `A_s=finish_sigma(B_<l,a_s)`，B 是实际叶，a_s 是旧自然节点的规定行动。不是返回实际主题的相反 reset。对正输入 x∈a_s，记 b=c_Vs(x)、a=c_As(x)，均至少1。令 n+、n− 为两叶除当前角色之外新增、丢失 x-coverer 的数目。

逐客户 `a-b=n+−n−`。输入 h 缩放系数 f=bh。每个 positive recipient 得 `h/a`，整束正输出 `n+ h/a`，current 为

    L=h−n+ h/a=h(b−n−)/a=f(1/a−N)。

因为当前覆盖者在两叶中都存在，`b−n−>=1`；又 n+≤a−1。故 L≥0、正出流总额<h（h>0 时），并精确保留客户标签和质量。这个 sub-Markov 性完全不使用 f≤1 或 IC，因而可先定义有限角色 DAG，再证明密度，避免循环。

只要后文已证 f≤1，逐客户 L≤f/a≤1/a。先在同一个 context 中对全部客户求和，再用一条 actual-prefix 完整 IC 得

    L_s<=u_l(A_s)<=u_l。

因此没有把每个客户分别当作一条可重权 IC。作者 EXACT-REFUND 的展开也精确：没有输入的 action 客户取 f=0，`u_l−L_s=e_s+Σ(1−f)D+ΣfN`，各项非负。

过去 positive 边确在 actual 前缀上，支持 x∈B_j；actual-prefix future 目标也是 actual 份额。二者作为物理 (j,x) 终端合法，不调用改枝过去玩家的 IC。其容量汇总不在本局部证明内。

## 3. 非实际目标的全部父亲及反链

令 t=(g,j) 是非实际目标，k 是 g 相对实际有序前缀的最早不同位置。若父 s 的角色为 r，reset 在 r 以前等于 actual。若 a_s=B_r，则 reset 全叶就是 actual，不能到 t；否则 reset 第一次不同恰在 r。故 r=k，且所有父 s 都选择固定行动 g_k，reset 完成叶均等于 V_t。

这是真实有序历史的结论，没有合并同负载历史。父 histories 可以不同，仍必须使用同一个 k、同一个 reset 叶。每条父边除以目标份额 1/c_Vt(x) 后，其密度贡献恰为 h_sx。

所有非终端边严格增加角色。同一 origin i、同一客户 x 的非负质量路径至多访问角色 k 一次，因此同角色 contexts 是 antichain，输入总质量不超过该 origin 的初始未来质量 a_ix。这允许 branching 和真实合流；它不是把每个父亲各领一份原始 p_ix。到达角色 k 的来源必须 i<k。因此全部父边的密度贡献和≤Σ_(i<k)a_ix。

直接 INIT 到非实际 t 的 owner 只能是 k，NEW-CAP 给该部分密度≤p_kx。故

    f_tx<=p_kx+Σ_(i<k)a_ix<=Σ_(i<=k)p_ix<=1。

比较元组的重复、主题重叠均由 Σ_i p_ix=1 保留。没有来源的客户整个图流量为零。由严格角色 DAG 按角色归纳，输入密度及 §2 的完整 IC 支配同时闭合。

## 4. 边界、符号及未证明的聚合

- 只对 x∈当前行动且有正输入使用 a,b 的倒数。空行动无输入，零输入全部输出取零；m=1 没有 future 边。NEW-CAP 只在 x∈T_i 定义 p，不定义 1/0。
- 任意平局和所有离轨历史仍取自原同一完整策略。u_l=0 时不会存在正输入的合法非空 query：完整 IC 与单位客户正收益会矛盾；略去该节点即可，不必除以 u_l。
- actual-prefix 目标没有最早不同 k，父角色可以不同。把它列为终端是必要的；不能把本密度结论延伸给 actual 目标。
- 同一 context 的全部客户合并后才付一次整行利润。不同 contexts 同一角色的 L_s 可以分别受 u_l 控制，本稿没有证明其总和受 u_l 或 2u_l 控制。
- 同一新流的全 O 质量账 `|O|=Σ(d+H)+ΣL+ΣE` 成立。传播没有重采到 O 外客户，current 的 x 是来源标签，不要求 actual 行覆盖 x。过去和 actual-prefix E 则确实有 actual 客户支持。
- 删除 I sources 后 R-only 密度及无 past/actual-prefix sink 的结构继续成立。I-cashout 的追加核对见下一节。

本组件真正接到一般证明的地方是：加强 INIT 后，客户支持能穿过整个原 reset DAG，且每个非实际 context 都可合法使用一次 whole-IC，而无需 whole-profit 重采。它没有付清 `Σ_(s:role=l)L_s+Σ_x E_lx` 的共同实际角色容量。该缺口与一般 half 均保持 OPEN。

## 5. 追加：I-cashout 与加强 INIT 的资金兼容

完成上述审查后，另完整读取 peer 的 [坐标 I 互补付款](../../../R-d3981c0168644971803a9c3380ed687c/next_general/global_credit/coordinate_residual_attack.md)及 [客户核/合成审查](../../../R-d3981c0168644971803a9c3380ed687c/next_general/credible/coordinate_support_attack.md)。这里只核对 inventory8 引用的 I 直接付款，不重新审其旧 fresh-profit 重采流。

加强 NEW-CAP 后仍有同一坐标分割 `p_ix=P_Bix+c_ix+a_ix`，原 H 不变，d_i≤u_i 不变。对 x∈I 求 owner 和：`1=H_x+C_x+A_x`。同一 actual 客户份额 w_lx 的剩额 `w_lx−H_lx` 非负、总和 1−H_x≥A_x。因此当 1−H_x>0 时取

    J_lx=A_x (w_lx−H_lx)/(1−H_x)，

否则 A_x=0 并取 J=0，就得 `Σ_lJ_lx=A_x`、`H_lx+J_lx≤w_lx`。这个构造只需同坐标库存分割和原 H 的同客户列界，完全不依赖旧 a 的比例，所以与新加强 INIT 兼容。若想保留旧 J 的数值则不成立；新初始化必须按新 A_x 重算 J。inventory8 正文没有宣称旧 J 数值不变。

全部 I future 在入图前删除，不能重复传播。同一第一预算支付 d，同一第二预算支付 H+J；R-only 路由再用新剩额 `2u_l−d_l−H_l−J_l`。故 inventory8 §5.1 的资金接口通过，R-STILL-OPEN 依旧未证。

## 6. root 共同 coverer 增边家族的追加审查

另读取作者新增 §4.1。保留每条原 positive edge h/a，向共同 coverer 增加任意 0≤z≤h/a。positive 与共同 recipients 不交，均属于 A 当前以外至多 a−1 个 coverer，所以全部出流≤(a−1)h/a，current 至少 h/a、至多原 L。非负守恒及一次 whole-IC 不变；精确退款再加 Σz。

每条新增 future 边仍进入同一 reset A 的真实规定 context，目标密度贡献≤父 h。最早实际偏离由 reset 决定，与该 recipient 是否共同 coverer 无关，所以全部父角色相同的证明不变。将各 origin 按当前输入占比分摊新边即可保留 origin 标签及同角色 antichain；h=0 时 z=0，不需除零。即使 z 依赖当前合并输入，证明也只使用实现后的非负守恒和边界，不要求 policy 是预先固定的线性映射。

共同 past 边支持 actual 前缀客户，可作为终端，但必须计入同一 E 钱包。共同边全取满时 uniform-reset 角点也正确。增边家族通过；没有新的共同角色容量。

## 7. 独立精确实现 QA

[独立脚本](audit_source_preserving_density.py)只读两个旧 packet 的 raw JSON，不导入作者 kernel、solver 或 verifier，展开为单位客户，逐全部有序历史核验 IC，再从定义构造 NEW-CAP、比例剪枝和原正差同客户 DAG。固定输入为旧52客户/T0145、旧348客户/T524、零客户 m1仅空主题、m2空/单点且全部历史规定单点。

[exclusive-create 冻结输出](source_preserving_density_exact.json)记录源/实现 SHA、全部 IC 数、非零输入/边/终端、每个 context 的前缀密度界及 exact refund、每个 O 单位客户的 H+current-source+路由-current+E=1。四项均通过：全历史 IC 数分别1554、258、1、6。348 输入激活2个非实际 context、12条单位客户正边，均落实际终端；固定 fixture 未激活跨层合流。其 H、current-source、路由-current、E 总额分别38、222、155/17、15/17。52及两个边界输入没有正 future 来源。

本次有限核验只检查实现，不证明一般密度定理或福利/角色容量。

## 8. root 提议的 maximal-future 初始化：新版本实现 QA

为覆盖原最小 future 输入未触及的非实际 interlayer，按 root 指定，只改同一固定52/348输入的已证可选初始化：取 `a_ix=min(r_ix,qhat_ix)`，故 current 为 `Σ(r−qhat)_+<=u_i`。每条边仍按 qhat 比例分配，并保留原边容量、`p_ix/c_Wi` 及客户库存。不扫描新输入、主题排列或实例。

[v2 脚本](audit_source_preserving_density_maxfuture.py)及 [exclusive-create 输出](source_preserving_density_maxfuture_exact.json)保留原 v1 文件不动。52客户输入激活5个非实际 context、40条客户正边，其中7条非实际 interlayer（同一个 context-to-context 转移）、33条实际终端边。348输入有3个非实际 context、12条边，全部实际终端。所有原 IC、NEW-CAP、origin 反链、前缀密度、整行退款和逐客户守恒均通过；两个边界输入也通过。

因为 v2 未激活 merger，再按 root 的可选角点加入全部 common-future 边到上限 h/c_A。[v3 脚本](audit_source_preserving_density_maxfuture_commonfuture.py)及 [exclusive-create 输出](source_preserving_density_maxfuture_commonfuture_exact.json)保留 v1/v2 不动，当前金额扣去共同 future 输出，exact refund 加回同额。52输入变为44条边，其中9条非实际 interlayer、35条实际终端；仍仅一个 context-to-context 转移。348及边界输入计数不变，全部精确检查通过。

三个版本均分别冻结实现 SHA。新输出明确记录 natural-parent merger、INIT+natural merger、同客户 merger 和多 origin context 数；这两个固定 packet 在 v2/v3 的这些计数**仍全部为零**。因此 interlayer QA 已激活，真实 merger 的实现覆盖缺口仍在，不能把本轮称作 merger 已测或一般结论证据。maximal-future 和 common-family 均为 root 提议的已证选择，独立性仅指此处从原始 packet 独立实现及核验。
