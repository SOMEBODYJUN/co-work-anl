# 客户密度定理与共同边选择：root 独立核对

2026-10-24，Boss10。一般输入、任意人数、全部有序历史纯SPE；Q-CAG-HALF仍OPEN。root先按精确陈述重构，再读[作者正文](../inventory/source_preserving_density_envelope.md)。[independent审查](../independent/coordinate_density_review.md)另行完成。不是完全盲题发现；客户保持局部核有同行来源，不认领外审或新颖性。

## 1. NEW-CAP

固定x∈T_i，t=cT、d=cB+1−1_Bi、w=cWi均正，n为新未来coverer数，nMinus为失去未来coverer数，nB为B相对T独占coverer数。κ=d−nB是1加共同其它coverer数，故1≤κ≤min(d,t)，w=d+n−nMinus，r=κ/(td)。裁边后qhat=n min(t,d)/(tdw)。

κw−n min(t,d)=κd−κ nMinus+n[κ−min(t,d)]≤κd≤td，故(r−qhat)+≤1/w。先求和才用一次完整IC，原current/future总额不变；新边密度w*a_ijx≤p_ix=1/t。

## 2. 全图密度

先完全不使用IC定义同客户流：每个正边发h_sx/c_A，current为输入减去全部正边，严格非负；future角色增、past/actual-prefix只终止。所以质量守恒与角色反链先成立。

非actual目标t的首分歧角色k唯一。所有进入t的reset都从actual_<k开始、选择固定g_k，故父节点全部在角色k；父历史可很多，不能误称唯一父亲。每条父边对目标密度c_Vt*h_tx贡献恰为h_sx。同一源客户的k层节点是反链，所以父贡献总和≤Σ_(i<k)a_ix；直接INIT贡献只能来自ownerk且≤p_kx。于是f_tx≤p_kx+Σ_(i<k)a_ix≤Σ_(i≤k)p_ix≤1。actual-prefix目标没有首分歧，必须按实际客户终端处理。

## 3. whole-IC与I出口

f≤1后，L_s=Σf(D_x−N_x)≤ΣD_x=D≤u_i；同一整行可退e+Σ(1−f)D+ΣfN≥0。一个context先合并全部客户，再调用一次完整IC；不同context不能分别领完同一u_i后免费相加。

root另读同行I互补付款原证明：NEW-CAP改变a_ix后按新A_x=Σa_ix重算J_lx即可；H、d总额保持，不继承旧J。先付I后只有R传播，没有past或actual-prefix终端，客户也不再跳到O外。原source标签与actual客户券仍须分开。

## 4. root提出、经inventory/residual另核的共同未来边族

R-only时，保留所有新未来coverer正边h/c_A；每个共同未来covererj>i可额外选η_j h/c_A，0≤η_j≤1。总输出最多(c_A−1)h/c_A，故current≥h/c_A>0；增加输出使current只下降，原whole-IC仍够。

每条新增future边给目标密度贡献≤父h，父角色首分歧与反链不变，所以全部允许选择都保持f≤1、客户库存与future DAG。全η0为difference核，全η1为旧[round3全部coverer均分流](../../round3/credible/increasing_role_capture_flow.md)的同客户角点；旧角点不认领新核。可允许初始future更大以预留当前角色的钱包，但必须满足NEW-CAP与current≤u；同一J重算。

全O若添加共同actual-past边可能付到owner前，不能继承源时间序；本节统一采用先付I、只传播R的一般接口，不是特殊目录类。

## 5. 未付项

共同边可移动付款但不增加钱。常数角色价下最小总费仍是来源质量，不能靠Bellman同义式证明小于预算。实际仍缺Σ_(s:role=i)L_s≤2u_i−d_i−H_i−J_i或更弱总付款关系。密度跨context直接相加有明确非SPE几何反例；这不排除真正SPE的更深激励定理。当前没有得到这样的全树金额不等式。
