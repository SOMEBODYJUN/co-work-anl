# 同 context 安全退券与利润差剪枝

2026-10-24，credible。任意人数、一般单位客户共同目录、全部有序历史纯 SPE。接续 [round5 全客户消元](../../round5/credible/all_fresh_submarkov_elimination.md)。§2 已获 root、shared 按陈述独立重构通过，不称严格盲审；§3—4 为随后加强，待独立核查。**未证明 coupon cap1/cap2 或一般 HALF。**

## 1. 只使用既有 whole-IC ledger

固定实际叶 Z、实际利润 u_i、客户负载 c_Z(x)。natural context t=(g,i) 的规定叶 B 有当前利润 v_t>0；actual-reset query 叶 A 的当前利润为 D_t。actual-prefix 原 IC 给 e_t=u_i−D_t≥0。

全客户正 recipient 原价分为未来 P_t^>、过去 P_t^<，总 P_t；负价 N_t。原覆盖者计数给

    v_t−D_t=P_t−N_t，
    D_t−N_t=J_t+L_t>0。                         (LOSS)

未来正边终点是 A 的真实更深规定 context。过去正边标签(j,x)满足x∈S_j(Z)，只能通actual coupon，不能购买A中过去j的IC。

角色DAG归一化beta_t=h_t/v_t给已有精确账

    Σb_t=Σbeta_t[u_i+P_t^<−N_t−e_t]。           (LEDGER)

以下净化这同一份账，不另加收入，不把当前或过去玩家的完整IC按客户重权。

## 2. 当前 actual 整行可安全承担全部 N/e 退款

LOSS 与 actual IC 给

    0≤N_t≤D_t≤u_i，
    F_t:=N_t+e_t=u_i−(D_t−N_t)∈[0,u_i]。        (SAFE)

从本 context 的 beta_t u_i 当前整行正券，向每个实际份额(i,x)、x∈S_i统一退系数 r_t=beta_t F_t/u_i≤beta_t。退款总额恰为 beta_t F_t；各实际份额均未退成负数。净系数

    kappa_t=beta_t(D_t−N_t)/u_i
           =beta_t(J_t+L_t)/u_i≥0。             (NET-ROW)

于是有全非负支付表示

    Σb_t=Σkappa_t u_i
          +Σ_(t,j<i,x)beta_t q^+_tj(x)。         (POSITIVE)

past正券原标签不动。N只作为同 context 标量退款与当前整行同时净化，没有把off-prefix负q^-假配为过去actual(j,x)的同客户退券。u_i=0时SAFE给D=N=e0，定义r=kappa0；在v>0的真实非空context中LOSS排除该零行。

原whole-IC系数仍为beta。不能把kappa说成新IC系数，也不能先退beta e再让剩券单独支付整份beta D。此步未用off-history slack ell≥0。

若初始source已经用掉券系数Lambda^src，真正净负载为

    Lambda^net_(j,x)=Lambda^src_(j,x)+Σ_(t:i=j)kappa_t
      +c_Z(x)Σ_(t:i>j)beta_t q^+_tj(x)。         (NET-LOAD)

还没有证明此量≤1或≤2。安全退券解决非负分配，不解决共同容量。

## 3. 最大标量取消只保留 off-profit 超过 actual 的缺额

本节为待独审的后续推导。用F=N+e写成 v=u_i+P−F、0≤F≤u_i。从原正 recipient 边中任删总额 c≤min(P,F)，同时令退款为F−c。当前整行净支付从u_i−F增加c，仍在[0,u_i]。保留正边是原边子容量，future context域及past actual标签均不变。

这是利润单位的标量取消，不维持逐客户血缘；原利润归一化流本就可在下一context重采客户。没有逐客户改权IC，也没有把负项直接赋给一个past券。若另要求客户不相混，本加强不能原样套用。

取c=min(P,F)，得到

    P'=(v−u_i)_+，    F'=(u_i−v)_+，
    当前净支付 u_i−F'=min(v,u_i)。              (CLIP)

P'≤P保证可在原正边保留足够子容量。若先删past正边，剩余past最小为(P_t^<−F_t)_+=(v_t−u_i−P_t^>)_+；剩余future为min(P_t^>,(v_t−u_i)_+)。允许分数保留。

所以可选一个仅在v_t>u_i时传播的核；并未假定off-history利润不超过actual。

## 4. 新DAG及 max 分母的非负券

保持v_t、初始b_t不变，用所选future子容量q'重新按角色递推 h'_t=b_t+Σ_(s→t)beta'_s q'_st、beta'_t=h'_t/v_t。因为q'≤q，归纳得beta'≤beta。past边仍只进actual coupon终点。

望远镜给

    Σb_t=Σbeta'_t[min(v_t,u_i)+P'^<_t]，
    kappa'_t=beta'_t min(v_t,u_i)/u_i
             =h'_t/max(v_t,u_i)。              (MAX-DENOM)

若v≤u_i，全部利润质量落当前actual行；若v>u_i，比例u_i/v落当前，剩余1−u_i/v沿原正边子集传播。该净化仍未用ell≥0。

beta'不增不代表净kappa'比§2原kappa小：减正边又减退款可能把终端质量转到当前行。必须按新beta'、kappa'、past子边重算load，不能旧退款与新剪枝各领一遍。不同来源/谱系仍可能重用同一actual行或past券，cap未闭。

## 5. 仅 fresh 利润分母的适用范围

relay另提出取nu_t=v_t(N\C)，仅传播fresh正边。逐客户LOSS给nu−P=J+L>0，正后继具有fresh利润，故严格角色DAG闭合。若Y_t为actual-reset query在C上的利润，则

    nu−P=D_F−N=u_i−Y_t−N−e_t。

于是0≤Y_t+N+e_t≤u_i，可用同一SAFE方法全部从当前actual整行安全退，净券为beta(D_F−N)/u_i，无past出口或正X项。§3的标量剪枝也可将out裁至(nu−u_i)_+。

这项变体beta=h/nu一般更大，不保证费用或load下降，也不证明half；它只在源及传播均为fresh利润时合法。不能将包含C源的初始化直接塞进仅fresh图。该变体由relay写自足稿，本节仅记录已独立核对的接合。
