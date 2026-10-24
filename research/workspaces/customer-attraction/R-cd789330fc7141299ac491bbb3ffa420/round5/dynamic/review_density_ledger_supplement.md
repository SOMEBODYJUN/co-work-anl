# 自然重分配与 TOTAL-TRIM 的补充独审

2026-10-24，dynamic。审查 [rank 原稿](../rank/incoming_density_diagonal_ledger.md) 新增第6—7节。先按 root 发来的陈述独立重构，再阅读两节正文。**结论：所述守恒、自然 IC、Bellman 最小化与自由比较删源归约通过；没有共同总费用上界，也未证明 half。** 本补审不新增静态 rank 表，不做实例或策略扫描。

## 1. 第6节放宽 recipient 分配仍保留整行账

固定原任意完整 SPE、实际终局、同一 OPT/owner 及同一组固定残源。查询 q 的当前吸收保持 f_q(x)/c_q(x)。对其真正未来 coverer j，选非负出口 t_(q,j)(x)，满足

    Σ_j t_(q,j)(x)=f_q(x)(c_q(x)−1)/c_q(x)。

每条出口必须进入父真叶 B_q 中 j 的规定主题 B_(q,j)，并保留该自然历史。角色严格增加；当前吸收与所有出口之和恰为入口，所以总吸收仍等于总源 M。原 actual-prefix query 及父自然 context 的整条 IC 均未换成别的游戏或人工续局。

对父来源 g=(q,j)，令 f_g=t_(q,j)。局部密度恒等式仅使用 f_g>=0、其支持客户确由 B_q 中 j 覆盖，以及同一自然规定行动见证；它不需要各 recipient 等份。ell_g>=0 仍来自该自然节点完整 IC。tracked R 保证父玩家已经覆盖这些客户，故 c_Bg=c_q>=2，TRACKED-DIAG 也保持。

全部父子首项对固定 q,x 恰为

    Σ_j f_(q,j)(x)/c_B(q,j)(x)
       =[Σ_jt_(q,j)(x)]/c_q(x)
       =f_q(x)(c_q(x)−1)/c_q(x)^2。

因此 DIAGONAL=M−H、GLOBAL-IN 与 GLOBAL-SLACK 全部保持。真正需要的是**总 captured mass 固定、所有自然 child 共享父叶负载**，而非逐 recipient 等份。本补充修正此前审查针对原 fairshare 家族所写的较窄条件。

原等份流的 HIT/BETA、priority marginals 及其它 recipient 密度界不自动保留。把全部 captured mass 送到一人，正说明不能继续引用每 recipient 原等份吸收概率。

## 2. Bellman 与全部来源同时最优

固定 sigma 后，每状态的 u_i、D_s、c_s、未来规定主题及所有真父历史都固定，费用对每个客户密度线性。每单位到达的当前成本为 u_i/(D_s c_s(x))，捕获部分总比例为(c_s−1)/c_s。因此严格逆角色归纳给

    V_s(x)=u_i/[D_s c_s(x)]
        +(c_s(x)−1)/c_s(x) min_(j∈F_s(x))V_(j,B_sj)(x)。

c_s=1 时不取空集最小值。该递推既是下界，又可通过将全部捕获质量送入一个最小 child 达到；选择可以固定为同一 (s,x) 决策，适用于所有父来源与所有源质量。

这里没有跨客户或跨来源的共享容量约束。合流后状态费用仍等于各分量线性相加，所以各客户独立的最优规则可以同时实现，不存在把各自不同不可兼容极小值相加的问题。最后仍合并为唯一整条 query 系数 A_s/D_s；并未按客户分别使用 IC。

原完整 actual IC 给 u_i/D_s>=1，递推即得 V_s(x)>=1。正质量状态 D_s>0；零源、空流和不被源触达的零收益状态可省略。原等份分配是新族的一个可选分配，所以同一源/owner 下新最小价不增。这些都是合法优化归约，不是 V 总价<=W 的证明。

## 3. 第7节自由删源的量词与付款合法性

原实际终局本身是一个合法 m 主题元组，所以 OPT_m>=W。固定任一最优并集 O，设 R=O\C、G=C\O，则

    |R|>=|G|，|R|−|G|=OPT_m−W。

任取固定常数 0<=gamma_x<=1、Σ_Rgamma_x=|G|，只是在比较源中保留 rho_x=1−gamma_x。它不修改客户价值、原目录、原 sigma 或原实际收益。守恒流给总吸收 OPT_m−W；用无条件确定常数 w_s=A_s/D_s 购买原完整 actual-prefix IC，得到

    OPT_m−W=Σ_sw_sD_s<=Σ_sw_su_(role s)=K。

因此**若另能找到该同一删源与路由使 K<=W**，则 half 成立。任意 gamma 不需 actual Hall 可行性，因为此处不把 gamma 当实际 G 运输或退款，只使用比较源的总量恒等式。它也没有提供任何原 eta_i 钱包。

排序必须在同一已固定 OPT 并集、matching/owner 与同一单位价格族 v_x 下进行。Bellman 最优规则可以先统一固定，费用为Σrho_xv_x，所以源选择与路由最小化相容。单位客户下 |R|−|G| 为整数；保留最低价的这些客户即可达到最优，价格并列无影响。允许分数删源不降低这个整数最优值。由此得到最低 |R|−|G| 个 Bellman 价之和及原稿的 layer-cake 表达。

若再优化 OPT/owner，可以把上述最优值的外层再取 min；不能把不同 owner/不同 O 各自的最低价客户拼成一份未固定来源的证书。原稿先固定 matching/owner，符合这一要求。

## 4. source 预付与原 Hall 约束必须分清

自然 recipient 重分配本身保持每个原 source 的当前吸收 rho_x/c_source(x)。所以**若仍保留此前同一份带局部 delta 保证的 Hall 取消**，旧 source 预付的原证明可保持；它不靠 recipient 等份。

第7节允许任意 gamma 后，该局部取消条件与 actual I 流可能全部丢失，SOURCE-NET 与逐行 eta 因而不继承。不能同时取自由 trim 的低价格和另一份 Hall gamma 的预付好处。原稿对第7节的免责声明正确。

第6节裸 Hall rank/greedy 等式应使用 round4/shared/net_dynamic_rank.md 的无额外局部 delta 约束的 Gamma；若坚持 SOURCE-NET 的指定 delta，就须用该旧稿给出的残余网络版本。新路由线性足以复用对应的正确版本，不能把两个 Gamma 混称一份最优取消。

## 5. 审查停点

通过的是任意自然 captured-mass 分配、共同 M−H 账、线性 Bellman 实现及 TOTAL-TRIM 的合法充分归约。其最小总费用可能仍大于 W；本补审没有证明或否定它的全称上界。

目前没有从完整真实孩子 IC 得到能共同支付 T+COV−L 或 Bellman 最低残费的新关系。按本次任务要求，停在这一准确边界，不追加静态重排、阴性扫描或新的摘要障碍。
