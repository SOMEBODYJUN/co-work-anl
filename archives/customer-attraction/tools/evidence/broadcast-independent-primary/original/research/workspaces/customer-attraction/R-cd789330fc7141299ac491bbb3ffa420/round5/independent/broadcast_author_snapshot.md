# 全 fresh 广播的利润归一化消元与真实 slack 保留

2026-10-24，credible_induction。**全输入解析组件，待独立审查；Q-CAG-HALF 仍 OPEN。** 输入始终是任意人数、任意有限共同目录和任意完整历史依赖纯 SPE；单位客户均分。

本稿只证明一种付款表示：自然 incoming 的全部 fresh 广播，包括尚未 tracked 的 R 和真正 outside，可在一个严格角色递增的有限图中一起消元，不必逐次为新客户再领 owner 库存。它不证明实际 C 账只花一次，不证明 K_in 或一般 half 已付。

与 round4 的区别是归一化分母：这里把到达的**利润单位**除以 off-history 规定叶当前玩家的完整利润，不除以 actual-reset query 的吸收量。所得系数一般不等于旧 capture flow 的 w；不能把本稿结果直接套给旧 K_in。

## 1. 真实 context、两个 completion 及原 IC

固定完整 SPE σ，实际叶 Z=(S_1,...,S_m)、覆盖 C、最终利润 u_i。取任意真实有序历史 g，长度 i−1，令

    a=σ_i(g)， B=finish_σ(g)， v_t=u_i(B)，
    A=finish_σ(Z_<i,a)， D_t=u_i(A)，
    W_t=finish_σ(g,S_i)， v_t^S=u_i(W_t)。

称 t=(g,i) 为 natural context。a 是 g 上的原规定动作；不假设 g 在轨。定义两条真实 slack

    e_t=u_i−D_t≥0，    ell_t=v_t−v_t^S≥0。        (IC)

e_t 来自 actual-prefix 上偏离 a，ell_t 来自 g 上偏离实际动作 S_i。以下所有分母只用于由当前动作实际覆盖的客户。v_t=0 时 a 不含任何客户，本稿所有 q、P、J 均为零；没有正利润流入时可删去该 context。

对 x∈a\C，记

    U_t(x)={j>i:x∈A_j}， V_t(x)={j>i:x∈B_j}，
    b_t(x)=|{j<i:x∈g_j}|，
    c_A(x)=1+|U_t(x)|， c_B(x)=b_t(x)+1+|V_t(x)|。

全部真实后继均保留。逐客户的 FRESH 恒等式是

    1/c_B−1/c_A
       =[|U\V|−|V\U|−b]/(c_A c_B)。             (FRESH)

## 2. 全 fresh 正项是一份 sub-Markov 行

对每个 j>i，定义正 recipient 原价

    q_tj = Σ_{x∈a\C: j∈U_t(x)\V_t(x)} 1/[c_A(x)c_B(x)]，
    P_t=Σ_{j>i}q_tj，
    N_t=Σ_{x∈a\C}[b_t(x)+|V_t(x)\U_t(x)|]/[c_A(x)c_B(x)]，
    J_t=Σ_{x∈a\C}1/[c_A(x)c_B(x)]，
    L_t=Σ_{x∈a\C}|U_t(x)∩V_t(x)|/[c_A(x)c_B(x)]。

这里包括 a\C 的**所有**客户；未先筛 tracked、R 或 outside。另记

    X_t=u_i(B;C)， Y_t=u_i(A;C)，
    v_t^F=u_i(B;N\C)。

直接数 U 的元素给出精确式

    u_i(B;N\C)−u_i(A;N\C)=P_t−N_t，            (F-DIFF)
    v_t−P_t=X_t+J_t+L_t。                       (LOSS)

第二式逐客户来自

    1/c_B−|U\V|/(c_A c_B)
       =[1+|U∩V|]/(c_A c_B)。

所以 v_t>0 时 P_t<v_t。若 q_tj>0，则 A_j 是 A 在 j 的真实规定动作，且 j 之后沿 σ；因而

    r(t,j)=(A_<j,j)， B_{r(t,j)}=A，
    v_{r(t,j)}=u_j(A)>0。                       (DOMAIN)

这是合法 natural context 后继边，角色严格增加；没有将未来强制动作下的过去利润当作规定叶利润。

令 Q_tj=q_tj/v_t。由 (LOSS)，Q 是 sub-Markov 行，行和严格小于一。更强的全子集界为：任意 J⊆{i+1,...,m}，k=|J|，

    Σ_{j∈J}Q_tj≤k/(k+1)。                       (SUBSET)

证明：令 p_tx=[1/c_B(x)]/v_t。fresh 的这些 p 之和≤1，而

    Q_tj=Σ_{x∈a\C}p_tx · 1_{j∈U_t(x)\V_t(x)}/[1+|U_t(x)|]。

对固定 x，记 d=|J∩(U\V)|。由 d≤k 和 d≤|U|，有 d/[1+|U|]≤d/(1+d)≤k/(k+1)。求 p 加权和即可。对任意非负角色价格 z_j，同一表示还给出

    Σ_j Q_tj z_j
      ≤max_{U⊆{i+1,...,m}} [Σ_{j∈U}z_j]/(1+|U|)。 (PRICE)

空 U 给零。这只是分析转移核，不是玩家执行隐藏混合承诺。

**范围。** (LOSS)、(SUBSET) 不需 b≥1，新 R/outside 不会破坏它们；也不使用 off-history 最优性 ell≥0。这部分是普遍计数关系和真实 completion 域关系，不冒称已经利用全部后继激励。

## 3. 有限 DAG 中的全 fresh 消元

只对 v_t>0 的 natural contexts 给任意非负初始利润注入 b_t，有限支撑。所有生成的正边终点也有正利润。按角色递增定义

    h_t=b_t+Σ_{s,j:r(s,j)=t} beta_s q_sj，
    beta_t=h_t/v_t。                           (FLOW)

同一真实 context 的平行来源可以相加；不同 context 不能因主题相同就识别。每个正后继严格更深，故是有限确定性递推，无需固定点存在假设。
(SUBSET) 表明每个节点全部 fresh 广播的总出流至多 h_t；其严格剩余为 beta_t(v_t−P_t)。

全节点求和时每条边的出入抵消，得到

    Σ_t b_t=Σ_t beta_t(v_t−P_t)
           =Σ_t beta_t[X_t+J_t+L_t]。      (MASS)

逐节点右项非负。这里没有为一个新鲜客户另造一单位来源，也没有将新 outside 当 actual G；新客户广播占用同一节点现有利润质量 h_t。

再由 (F-DIFF) 及 v_t−D_t=(X_t−Y_t)+(P_t−N_t)，精确有

    v_t=u_i+(X_t−Y_t)+P_t−N_t−e_t。

所以

    Σ_t b_t
      =Σ_t beta_t[u_i+X_t−Y_t−N_t−e_t]。   (C-LEDGER)

这消除了全部 fresh 正 recipient：它们已在 DAG 中匹配到另一份真实 prescribed profit。fresh 负项 N 及 actual IC slack e 保留负号。剩余跨叶迁移只含 actual 覆盖 C 上的 X−Y。

该式不是将 X、u 当两份库存；它们是同一 exact signed 账中的各项，未来必须针对整式证明共同预算。

## 4. 强制 OPT query 的合法初始化

初始 owner query 通常不是某个 g 的规定动作，不能直接当本稿 natural context。正确初始化如下。固定比较元组 T_i、owner 分割 Q_i⊆T_i，给实际遗漏 x∈Q_i\C 一个 0≤rho_x≤1 的原来源。令

    Y^i=finish_σ(Z_<i,T_i)，
    A_i^src=Σ_{x∈Q_i\C}rho_x/c_{Y^i}(x)。

当前 source 吸收 A_i^src。对 j>i，向真实 context (Y^i_<j,j) 注入

    b_{i→j}=Σ_{x∈Q_i\C:x∈Y^i_j}rho_x/c_{Y^i}(x)。

实际前缀不覆盖这些客户，均分恰给

    Σ_x rho_x=Σ_i A_i^src+Σ_{i<j}b_{i→j}。       (INIT)

每个 j>i 在 Y^i 上的动作确由 σ 规定，注入对象符合 (DOMAIN)。单个 source 的 b_{i→j}≤u_j(Y^i)；不同来源相加后不声称仍≤该利润，也不声称 beta≤1。
每位 i 只有一个初始 query，A_i^src≤u_i(Y^i)≤u_i；若接 SOURCE-NET，须沿用同一 rho、gamma 和 actual 钱包。

汇总这些 b 并用 (FLOW)，可按 (C-LEDGER) 消元 (INIT) 全部 future captured 质量。没有因此再得到一份可独立花的 Σ_i u_i：源项和后续 beta_t u_i 可能使用同一玩家钱包多次。

## 5. 全客户升级：过去 actual C coupon 出口与精确缺口

root 同时独立观察了如下全客户推广，本节重构其真实 context 域、出口及共同容量义务。它不是把上一节 C 账已经付款的声明。

对任意 x∈a（包括 C），令

    J_A(x)={j≠i:x∈A_j}， J_B(x)={j≠i:x∈B_j}。

两叶都由当前 i 覆盖 x，所以 c_A=1+|J_A|、c_B=1+|J_B|。定义

    q^+_tj(x)=1_{j∈J_A(x)\J_B(x)}/(c_A c_B)，
    q^-_tj(x)=1_{j∈J_B(x)\J_A(x)}/(c_A c_B)，
    P^>_t=Σ_{x∈a,j>i}q^+_tj(x)，
    P^<_t=Σ_{x∈a,j<i}q^+_tj(x)，
    N^all_t=Σ_{x∈a,j≠i}q^-_tj(x)，
    J^all_t=Σ_{x∈a}1/(c_A c_B)，
    L^all_t=Σ_{x∈a}|J_A(x)∩J_B(x)|/(c_A c_B)。

逐客户直接给

    v_t−D_t=P^>_t+P^<_t−N^all_t，
    v_t−P^>_t−P^<_t=J^all_t+L^all_t
                              =D_t−N^all_t>0。  (ALL-LOSS)

最后严格号只用于 v_t>0；空动作所有项为零。全部正边用 v_t 归一化，仍有第2节形式的所有角色子集界 |J|/(|J|+1)。这里正 recipient 可以早于 i，不能假称全图严格向后。

**合法处理是把两类正边分开。**

* j>i 的边送 natural context (A_<j,j)，其规定叶确为 A，与第2节的 DOMAIN 完全相同。所有 future C 及 fresh 均包含在内。
* j<i 的正边必有 x∈A_j=S_j，但 x∉g_j，因此 x∈C。将它作为带标签 (j,x) 的 actual coupon 出口，量为 beta_t q^+_tj(x)。不调用 A 中过去玩家 j 的原 IC，因为 A 对 j 的未来含强制 query，确实不是该过去节点的规定完成叶。

出口也可形式化为真正 actual context (Z_<j,j)：其规定叶、reset 叶都为 Z，无正转移边，因此一到即终止。出口量 z 对实际利润 u_j 的整行系数为 z/u_j（正出口蕴含 u_j>0）；这没有声称该系数或其全局和≤1。若保留客户标签，则 z 对 x 的实际份额 1/c_Z(x) 需要 coupon 系数 z c_Z(x)。

现在用新的 all-customer 图独立定义

    h_t=b_t+Σ_{s,j>i(s):r(s,j)=t} beta_s Σ_{x∈a_s}q^+_sj(x)，
    beta_t=h_t/v_t。                            (ALL-FLOW)

注意 beta 一般不同于第3节 fresh-only 图；不能两图付款相加。只有 future 正边进入非终端递推，故严格角色 DAG 仍在；past 边只通终端，不会制造回路。

其质量分解为

    Σ_t b_t
      =Σ_t beta_t[J^all_t+L^all_t]
          +Σ_t beta_t P^<_t
      =Σ_t beta_t[u_i+P^<_t−N^all_t−e_t]。       (COUPON-LEDGER)

第一行每项非负，分别是 diagonal/common-coverer 剩余和过去 actual coupon 出口；第二行对 D_t 使用同一 actual IC 并保留 e_t。所有 future C 迁移和所有 fresh 正项均已匹配到真实后继 prescribed profit，不剩互斥叶 X 的独立库存。

**尚无 cap1 定理。** 如果把 beta_t u_i 全部投到原实际利润单位上，则每个实际份额 (j,x)，x∈S_j，当前已出现的正 coupon 系数为

    Lambda_jx
      =Σ_{t:i(t)=j}beta_t
        +c_Z(x)Σ_{t:i(t)>j} beta_t q^+_tj(x)。    (COUPON-LOAD)

初始 source 当次吸收若也用实际整行利润支付，还须把那份整行系数加到同一 Lambda；不能另领钱包。COUPON-LEDGER 中 −Σ beta N^all 和 −Σ beta e 是必须保留的退款，但未证明它们可分配为同一 (j,x) 的非负退券，更未证明退券后 Lambda_jx≤1。

负 q^- 的过去角色来自 g 的旧覆盖者；它未必选实际 S_j，所以不能仅凭同一个客户 x 就将那笔负项假配为某个实际 (j,x) 的退款。未来负项也不能任意指定给另一互斥叶的正 coupon。

因此这里合法解决了 past recipient 的 IC 域和终止性：它是 actual coupon 出口，不是 A 中过去角色的假规定节点。尚未解决的恰是这些出口、whole actual 行支付及初始 source 的**同一份实际 C 共同容量**。

## 6. 同 context、同客户的合法正负取消

COUPON-LEDGER 的负项不能任意跨叶退券，但同一 context、同一客户的正负原价完全相同，可以在传播之前作精确取消。这保留一个有利的可选路由，未解决总容量。

固定 t,x∈a，记

    p=|J_A(x)\J_B(x)|， n=|J_B(x)\J_A(x)|，
    p_< =|(J_A(x)\J_B(x))∩{1,...,i−1}|，
    p_> =p−p_<， d_x=1/[c_A(x)c_B(x)]。

取消 min{p,n} 份正负同价项，优先取消过去正 coupon。具体剩余过去正份数可取

    p'_<=(p_<−n)_+，
    p'_>=(p_>−(n−p_<)_+)_+，
    n'=(n−p)_+。

所保留 future 正份可以在原 future 新覆盖者中任意选取（不足整数时亦可分数保留）；总份数如上。逐客户仍有

    (p'_<+p'_>−n')d_x=(p−n)d_x=1/c_B−1/c_A，
    (p'_<+p'_>)d_x=(c_A−c_B)_+/(c_A c_B)，
    n'd_x=(c_B−c_A)_+/(c_A c_B)。               (NET-CANCEL)

所有保留正边都是原正边的子容量，故其 actual coupon 域和 future natural context 域不变。只用此删减核、保持归一化 v_t 和初始 b 不变，按角色递推得到 beta'_t≤beta_t（先前行输入不增，归纳即可）。因此新的 whole actual 正费用 Σ beta'_t u_i 及 past 正 coupon 费用都不大于原核的对应原始正费用；不声称同时保留了原负退款，新的 signed ledger须用 n' 重算。

令 b_A^<(x)、b_B^<(x) 分别是两叶在 i 前的负载。因为 n 至少包含过去被移除的覆盖者数，残余过去 coupon 有

    p'_< d_x≤[b_A^<(x)−b_B^<(x)]_+/(c_A c_B)。  (PAST-DEFICIT)

特别地，若 off-prefix 在 x 上的负载不少于 actual-prefix，x 的全部过去正 coupon 可在本 context 内取消。取消后的正项只存在于 c_A>c_B 的客户；若所保留边送给 future j，则后继规定叶 B'=A，在这个同一客户上的旧负载从 c_B 严格增加为 c_A。这是同客户性质；整行归一化可在别的客户间重采，不能宣称所有全行路径共享一个递增客户负载势。

这项取消是同 context、同客户的恒等处理，不把另一互斥叶的负项指派给实际券。它使 past-C 的未付正出口只剩 (PAST-DEFICIT) 方向，但没有证明这些前缀负载缺额能在全树共同付款。

## 7. 生成 context 的过去 coupon 有因果区间

对从第4节 INIT 出发的实际生成图，每个非在轨 natural context 都带有一个父 query 角色 k<i，使它的规定叶 B 从 actual-prefix 的 k 位 query 开始；因而 g_j=S_j 对全部 j<k 成立。于是本 context 的过去正、负客户项都只可能发生于

    k≤j<i。                                    (INTERVAL)

若一个 future 正边到达角色 l>i，下一个规定叶为 A=finish(actual_<i,a)，其新的过去差异区间是 [i,l)。因此沿同一非终端谱系，过去 coupon 区间按时间接续，互不重叠；若 A=Z，后继直接是无正边的 actual context。

这项域关系不依赖利润大小，也未给 coupon cap1：不同 source、不同谱系的区间仍可能覆盖同一实际角色，而且 beta 的归一化分母随叶改变。不能将“单谱系每角色只出现一次”升级为“全部谱系每角色总系数≤1”。它只排除了同一谱系对更早实际 prefix 的反复收费，供共同容量选择时使用。

## 8. 一般主线仍缺的关系

已完成：全 fresh 正广播的全子集 sub-Markov 界、严格角色 DAG、非增质量流、精确 C-only 余账；全客户版本又把过去 C 明确化为 actual coupon 出口，并保留 signed 退款。未证明：旧 K_in 下降、新 beta 的 actual 总费用≤W，或 COUPON-LOAD 共同 cap1。

从 (INIT) 接 SOURCE-NET 后，仍须用同一钱包证明

    Σ_i A_i^src
      +Σ_t beta_t[u_i+X_t−Y_t−N_t−e_t]≤W，

或给更弱、直接支付 rho 总量的共同 actual I/G 关系。这个式子左边本身等于 rho 总量；仅重写它不算 half 进展，需要真正控制 C 迁移及 actual u 的重复次数。

不能给互斥叶的 X 各自领取 actual I；不能将逐节点 beta≤1（即使成立）相加当成同角色总系数≤1。也未证明本稿选择能与 SOURCE-NET 的 delta/gamma、动态 Hall cut 或 rank 费用取同一个可行选择。下一步是 C-LEDGER 的 signed C 共同支付，不是再给 fresh 创新开一份 owner 库存。

## 9. 可选备注：保留一部分真实 off-history slack

基础核没有使用 ell≥0，不能称为真实 off-history IC 的共同付款。可固定 κ∈[0,1)，仅取 chi_t≤min{ell_t,κ(v_t−P_t)} 并将归一化数换为 nu_t=v_t−chi_t。因 nu−P≥(1−κ)(v−P)>0，仍得严格 sub-Markov DAG；C-LEDGER 中对应多留一项 −chi_t。

这只是合法可选记账：chi>0 也会增加 beta，故未证净费用改善。不优化 κ、不将新归一化当成已支付容量；当前承重点仍是第5节 actual C 出口只付一次。

## 10. 自核范围

`audit_submarkov_elimination.py` 是作者自核，不是独立审查；只重放既有 portfolio_matching_failure、root_tax_failure 两份证书，不搜索新游戏。精确 Fraction 检查合计1584条原完整历史IC、2411个 sub-Markov 子集界及1916项 past coupon 域，核两种 DAG 的质量与 signed ledger。

原 OPT-owner 初始化在这两份旧证书中没有激活正传播边，不能把这些零次数回归称为已测非零传播。v2 另按本稿允许的任意利润注入，在 root_tax 的历史 (5) 注入一单位，触发一条 all-customer future 边，精确终账为1。两份证书均没有正 fresh 边，因此没有声称已测非零 fresh 链；普遍结论由上文计数证明承担。

`submarkov_elimination_regression.json` 为未带非零 probe 的初版输出；`submarkov_elimination_regression_v2.json` 保留新增 probe 的精确范围，不覆盖旧记录。第6—7节同客户取消与因果区间目前是解析推导，尚未另行独审；它们未用于抬高主目标或 coupon cap 的状态。
