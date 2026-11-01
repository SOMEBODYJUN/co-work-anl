# 来源客户不重采核：独立解析核查

2026-10-24。核查 parent 在阅读 round7 坐标初始化后提出的客户保留核。输入是原 CAG-MODEL 的任意共同目录、任意人数、任意完整历史纯 SPE。**本页只核查一种新的合法非负付款表示；没有证明 RESIDUAL-CAP 或 Q-CAG-HALF，也不把此新核归入保持原 full-v 分母的删边 CLIP。**

## 1. 同一真实 context 的符号

固定实际叶 Z 与实际角色 i 的完整利润 u_i。natural context t=(g,i) 的规定动作为 a，规定叶为 B；actual-prefix 重置后强制同一动作 a 的真实完成叶为 A。记

    v_x=1/c_B(x)， D_x=1/c_A(x)    (x∈a)，
    D=Σ_(x∈a)D_x， e=u_i−D≥0。

对每个 x∈a，令 J_A(x)、J_B(x) 为 A、B 中除 i 外覆盖 x 的角色集合。原正价和负价为

    q_jx=1_(j∈J_A\J_B)/[c_A(x)c_B(x)]，
    n_jx=1_(j∈J_B\J_A)/[c_A(x)c_B(x)]，
    P_x=Σ_j q_jx， N_x=Σ_j n_jx。

逐客户恒等式与非负剩余是

    v_x−D_x=P_x−N_x，
    ell_x:=v_x−P_x=D_x−N_x
         =[1+|J_A(x)∩J_B(x)|]/[c_A(x)c_B(x)]>0。

e≥0 是 actual-prefix 上的一条完整收益 IC，不能替换为每客户 IC。past 正价只能进 actual 终点；future 正价进入 A 的真实 prescribed context，仍是原完成域。

## 2. 任意单个固定客户集合 X 的核

固定 X⊆N。在一个有正输入的 context，假设传播标签均在 a∩X，令

    nu_X=Σ_(x∈a∩X)v_x>0， D_X=Σ_(x∈a∩X)D_x，
    P_X=Σ_(x∈a∩X)P_x， N_X=Σ_(x∈a∩X)N_x。

逐客户恒等式相加给

    nu_X−P_X=D_X−N_X>0。

完整 IC 只以 D_X≤D≤u_i 的形式使用。因此

    F_X:=u_i−D_X+N_X
        =e+(D−D_X)+N_X ∈[0,u_i]。

输入 h 取标量 beta=h/nu_X；向每个 X 内原正边送 beta q_jx，当前支付 beta(nu_X−P_X)。该当前金额可从 beta u_i 整行统一退款 beta F_X 得到，所有款项非负，且精确守恒。没有按客户给原 IC 不同权重。

future 正边上的客户仍在 X，接收动作真实覆盖该客户，故接收者 nu_X>0。past 正边仍有合法 actual 标签。严格 future 角色 DAG 因而闭合。X=O 保持传播客户集合 O，但不同 O 客户仍可在该核中重采；不保留每个 origin x。

PRICE 不能从旧分母直接声称继承，但可重证同一个常数。令 p_x=v_x/nu_X，则 p_x≥0 且 Σp_x=1，并且

    q_jx/nu_X=p_x · 1_(j∈J_A\J_B)/c_A(x)。

对任意 k 个角色的集合 K，设 d_x=|K∩(J_A\J_B)|，则

    d_x/c_A(x)≤d_x/(1+d_x)≤k/(k+1)。

因此该 X 核的 K 正出口比例至多 k/(k+1)，相应任意非负角色价格也服从原 uniform-subset PRICE 形式。删正边保持这些界。

该核将分母 v 改成 nu_X≤v。它不是原 full-v CLIP 的纯删边选择，也没有同输入下 beta 不增或实际列容量改进结论。

## 3. 每客户 incoming 保留：一次 max 系数的完整 IC 足够

现在令 h_x≥0 是同一个 context 内合计后的 incoming；只有 x∈a 可有正输入。令

    beta_x=h_x/v_x， beta_*=max_(x∈a) beta_x。

向原正边 (j,x) 送 beta_x q_jx，当前合计金额为

    L=Σ_x beta_x ell_x=Σ_x beta_x(D_x−N_x)≥0。

逐客户账相加给精确守恒

    Σ_x h_x = L+Σ_(j,x) beta_x q_jx。

关键没有调用“按客户 IC”。只使用一次系数 beta_* 的完整 IC；退款有显式非负分解

    F=beta_* u_i−L
     =beta_* e+Σ_x(beta_*−beta_x)D_x+Σ_x beta_x N_x ≥0。

又因 L≥0，F≤beta_*u_i。故从 beta_*u_i 的完整 actual 行按统一比例退 F，恰留下 L，所有券仍非负。u_i=0 时，任何含客户的合法 action 都会使 actual-reset 查询 D>0，与完整 IC 矛盾；因而没有正 incoming 的退化问题。

等价的 layer-cake 证明是 beta_x=∫1_(beta_x≥s)ds：每层在固定 X_s={x:beta_x≥s} 上使用 §2 的单个 restricted 核，完整 IC 总系数恰为 beta_*。这解释了为何不能把不同 singleton 各自得到的“≤u_i”相加后仍只留一份 u_i；正确总系数是 beta_*，不是 1。

## 4. 客户取消、真实域和来源合并

可先在每个 context、每个 x 内取消 min(P_x,N_x) 的同价正负项，只保留原正边子容量 P'_x，并令 N'_x 为剩余负量。仍有

    v_x−D_x=P'_x−N'_x，
    ell'_x=v_x−P'_x=D_x−N'_x≥0。

§3 的证明原样成立，退款式中用 N'_x。若取消后某个 x 的 future 正边仍正，则 c_A(x)>c_B(x)；该真实后继规定叶正是 A，所以沿同 x 的非终端谱系，负载严格增加且至多为 m。

不同 origin 的同客户输入必须先在同一个真实 context 相加再算 beta_x 和 beta_*。输出可按 origin 的输入比例重新分解：正边和每客户当前金额对 h_x 都是线性的，故保留 origin 标签不会制造额外质量。不同有序 context 不因主题或负载相同而合并。

此核的 PRICE 也可直接重证：令 p_x=h_x/(Σ_y h_y)，则正出口比例是 p_x 对各 x 的 q_jx/v_x 的凸组合；每个 x 行都是同一 uniform-subset 子概率行。因此角色 k-cut 常数仍为 k/(k+1)。同客户取消只删正边，保持该界。

## 5. 保留了什么，没有保留什么

保留的是传播阶段的真实客户标签 x，以及每个 origin 的质量。当前支付 L 仍从实际角色 i 的完整钱包领取，actual S_i 不必覆盖来源 x；它不是 actual(i,x) 的物理同客户券。past 正出口的 actual 客户标签则仍可物理核对。

没有证明各 context 的 beta_* 之和、同 actual 角色 current 总额、past 总额或 RESIDUAL-CAP 余额可共同支付。客户库存每单位恰一和同 x 负载严格增加，均不能单独把多个 context 的实际钱包用量合并。

该核通常会让单个正边的系数 beta_x 大于原 full-v 的 h/v，所以不能冒充原量词内的一种 CLIP 子路由。它是新的合法表示；若用来闭合 half，仍须单独证明与初始化共用的钱包容量。

## 6. 保持原 full-v 分母时的局部 X 支持条件

若明确不改原归一化 beta=h/v，并只允许原 SAFE/CLIP 的删正边、当前整行系数≤beta，则把全部剩余正出口限制在客户集合 X 的精确局部可行条件是

    P_X ≥ (v−u_i)_+。

必要性：至少 beta(v−u_i)_+ 质量必须外送，而 X 正边总容量仅 beta P_X。充分性：从 X 正边保留总量 (v−u_i)_+，其余删除；当前正好吸收 beta min(v,u_i)，落在合法 SAFE/CLIP 区间。此条件本身没有被一般 SPE 保证，也没有构造任何存在性 RESIDUAL-CAP 反例。

本页没有新增有限例或扫描。结论依据以上逐客户恒等式、一次完整 IC 与严格角色域关系；是对 parent 候选的独立解析核查，无外审或新颖性声明。
