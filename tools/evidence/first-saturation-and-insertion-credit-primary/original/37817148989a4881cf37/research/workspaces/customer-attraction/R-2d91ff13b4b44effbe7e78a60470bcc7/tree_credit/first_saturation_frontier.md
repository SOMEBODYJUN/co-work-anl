# 首次满行停止：一份共同前沿及其合法随机主题 cut

2026-10-23（按客户端日期），tree_credit 工作稿。身份：以下 §§1–4 的构造、守恒及最优元组不等式以及 §6 的质量抽样耦合有一般解析证明；未获独立审查。§5 及 §§7–8 记录精确未付义务，不是半覆盖定理。没有证明 Q-CAG-HALF，没有以辅助障碍代替主攻。

## 1. 接受 SOURCE-NET，而不是重领 source 预算

固定原一般实例、完整纯 SPE σ、实际完整叶 Z、实际收益 u_i、最优 m 槽 T 及一次 owner 分配 Q_i⊆T_i（Q_i 两两不交且并为 O）。记 C=cover(Z)、R=O\C、I=O∩C、G=C\O。

从 R-cd789 round3/GENERAL_PROOF_WORKING.md 最后一节取一份已经存在的取消量 γ_x∈[0,1]（x∈R）、残源 ρ_x=1−γ_x 及同一行钱包

    η_i=u_i(I)+γ_i,       Σ_i η_i=W,
    K_i^src≤η_i.

这里 γ_i 是 owner i 上取消总量；Σ_xγ_x=|G|。取 δ_i=min(u_i(G),|Q_i∩R|) 后扩充运输给出 SOURCE-NET，并非本稿新证。本文始终用这一份 γ、owner 与 η。

沿用该稿的递增角色真实查询流：状态 (i,a,x) 使用原**实际前缀**下强制 a 后的真实完整终局 Z_i(a)。对所有 x∈a，定义

    c_(i,a)(x)=c_x(Z_i(a)),
    r_(i,a)(x)=1/c_(i,a)(x),
    D_i(a)=当前查询者的完整原单位收益.

当前 query 本身覆盖 x，故这些分母严格正。仅对 x∈R∩a，实际前缀对 x 的负载为零，才进一步有 c_(i,a)(x)=1+该叶更深 coverer 数。I 及其他客户必须保留其真实完整负载；§5 的非 R 稀释项亦使用这里的同一定义。

单位进入质量在当前吸收 r，并向每个更深 coverer 各送 r；后继按已固定的合法 query 选择规则重置。规则可取原捕获者动作；本稿不要求改规则，也不修改原 σ。

源费用与到达费用可线性拆分，即使同一 (i,a) 同时有 source 与 captured 质量：A=A_src+A_in，整条 IC 的唯一系数 A/D=(A_src/D)+(A_in/D)。这不是按客户重加权 IC。

## 2. 首次满行停止的确定构造

按 i=1,…,m 处理。先保证所有初始 source 都进入，预留固定 K_i^src。设到达行 i 的尚未接纳 captured 流为 q_(i,a)(x)，其总原 query 费用为

    F_i=u_i Σ_a [Σ_(x∈R∩a) q_(i,a)(x) r_(i,a)(x)]/D_i(a).

零 D 的 query 不会有正 R 质量；相应项按零。若 u_i=0，SPE 给所有 D_i(a)=0，该行也不会有正 captured R 到达。

令余钱包 e_i=η_i−K_i^src≥0，并取

    θ_i=1                       若 F_i=0,
    θ_i=min(1,e_i/F_i)           若 F_i>0.

对每个 a,x，以同一个 θ_i 接纳 captured 流；其余 (1−θ_i)q 在此停止，不再向后分流。source 不被 θ_i 缩减。接纳后才沿原均分规则吸收、发送未来 captured 流。

这不是按客户选 IC 权：θ_i 是对该行所有 incoming 一致的接纳系数；最终每个 query 仍整体乘

    w_(i,a)=[A_(i,a)^src+θ_i A_(i,a)^in]/D_i(a).

因此 paid fee K_i=K_i^src+θ_iF_i≤η_i。若 θ_i<1，则 K_i=η_i，该行确实满额。令 J={i:θ_i<1}。

源、θ、实际前缀 query、后继规则都固定后，整个有限 DAG 的流唯一，所有定义不循环：F_i 只依赖更早已处理位置发送的质量。

## 3. 一份停止前沿、守恒及 HIT

把确定分流实现为随机粒子。source 先进入其 owner query；每次均匀选择当前吸收或一个更深 coverer；在 captured 到达行 i 时独立以概率 1−θ_i 停止，否则接纳。角色严格增，粒子有限终止。

记 B_i 为在行 i 首次停止总质量，B=Σ_iB_i；A 为全部已接纳 query 的总 R 吸收。每个 source 客户只有一份总质量 ρ_x，故

    A+B=Σ_xρ_x=|R|−|G|.                         (STOP-CONS)

不允许在 B 之后再展开或再次收费。同一随机粒子不可能在两个停止行重复出现。

把接纳抛币全部删除，可与未截断原流耦合。停止事件必先命中 J；source 行不被拒绝。因此复用一般 HIT（见 R-cd789/round3/mixed/capture_hitting_capacity.md），对 source role s(x)，

    B_x≤ρ_x k_x/(k_x+1),
    k_x=|J∩{s(x)+1,…,m}|.                       (STOP-HIT)

特别地单一停止行 i 上，任何非 source 客户的总停止质量≤ρ_x/2；多行只能使用首次命中式，不能把逐行 1/2 相加当成一笔共同信用。J 虽由先前确定流计算得到，构造结束后它是固定 role 集，HIT 的量词允许代入它。

费用和利润必须分开。由 whole-IC 及定义，

    A≤K:=Σ_iK_i≤Σ_iη_i=W.

写 E=K−A≥0、U=W−K≥0，则

    (|R|−|G|)−W=B−E−U.                         (FRONTIER)

所以真正需要的足够前沿界是 B≤E+U。此式本身只是准确余量，不是新增已付福利关系。若 J 为空则 B=0，立即闭合；非空 J 的支付尚缺。不能把 STOP-HIT 单独声称为 B≤E+U。

## 4. 每行随机选一个合法 query 的精确 hybrid cut

本节不要求 SPE。固定任意 role 集 J，以及每个 i∈J 上任意一个合法主题分布 p_i。独立抽 B_i∼p_i，保留 i∉J 的薄 owner 主题 Q_i。

每个实现的薄混合覆盖，扩充保留的 Q_i 为 T_i 后是合法 m 槽覆盖，故至多 |O|。对 x 定义

    p_i(x)=Pr_(a∼p_i)[x∈a].

O 外新增与 owner 库存漏失比较，给出一份共同 cut：

    Σ_(x∉O) [1−Π_(i∈J)(1−p_i(x))]
       ≤ Σ_(x∈O:o(x)∈J) Π_(i∈J)(1−p_i(x)).     (RANDOM-CUT)

证明逐客户即可：owner 不在 J 的 O 客户由其保留 Q_owner 覆盖，不能丢；owner 在 J 的客户恰在所有随机 B_i 均不覆盖时丢失。O 外客户至少一个随机 B_i 覆盖时新增。独立抽样只用来将未覆盖概率写成乘积；若使用任意联合 action law，把每个乘积换成相应联合未覆盖概率，结论仍成立。

重复 T、重复 query、空 Q、空主题、J=∅ 均覆盖。Q_i 不是玩家动作；其扩充合法性是全部论据，绝不对薄 Q_i 调用 SPE。

因此多 query 合流不阻止写出正确 HYB cut：每个停止 role 可合法随机只取一个 query。承重问题是如何选择同一组 action laws，使 cut 中的覆盖/漏失量控制原停止流 B，而不改动其 whole-IC 系数。

## 5. 一个兼容 whole-IC 的 action law 与精确缺口

对行 i 的被拒 incoming 定义

    b_(i,a)(x)=(1−θ_i)q_(i,a)(x),
    A_(i,a)^stop=Σ_(x∈R∩a)b_(i,a)(x)r_(i,a)(x),
    λ_(i,a)=A_(i,a)^stop/D_i(a),
    L_i=Σ_aλ_(i,a).

若 L_i>0，可取 p_i(a)=λ_(i,a)/L_i。每个 λ 乘的仍是一条完整原 IC；这个 action law 的归一化没有按客户改变 λ。令 χ_(i,a)(x)=[b_(i,a)(x)−λ_(i,a)]r_(i,a)(x)（只对 x∈a，R 外 b 取零），则

    Σ_x χ_(i,a)(x)=0,
    Σ_(x∈R)χ_(i,a)(x)=λ_(i,a)D_i^(N\R)(a)≥0.   (COV-STOP)

这表明 λ 比真实客户流 b 小的部分，恰由该 query 的非 R 利润稀释；这部分利润已经降低费用，不能再免费领取第二份。

RANDOM-CUT 使用的是 p_i(x)=Σ_(a∋x)λ_(i,a)/L_i，而停止质量是

    B_i(x)=Σ_a b_(i,a)(x).

二者既分母不同，也没有已证逐客户比较。特别不能从 whole-IC 系数为 λ 推出 B_i(x)≤L_i p_i(x)：那需要 Σ_a b_(i,a)(x)≤Σ_(a∋x)λ_(i,a)，它不由 COV-STOP 给出。把 max_x b_(i,a)(x) 换作系数可保证支配，但会丢失原 D_i 中 I/其他利润的稀释作用，并破坏原 η 财务容量。

故这个 law 是合法的随机 cut 输入，却还不是付款证书。允许改选联合 laws 或其他随机化；但必须同时保留 SOURCE-NET、同一实际取消运输和 whole-IC 常数系数，不可对每个客户另选一行权重。

## 6. 可覆盖停止质量的另一个 action law

有一个不需要额外假设的覆盖耦合，但它具有不同的归一化。令

    b_(i,a)=Σ_x b_(i,a)(x),    B_i=Σ_a b_(i,a),
    p_i^mass(a)=b_(i,a)/B_i     当 B_i>0.

这等价于从该行全部停止粒子中按质量抽一个，再取其合法 query。由于被抽客户一定属于其 query，逐客户有

    p_i^mass(x)≥B_i(x)/B_i.                       (MASS-COVER)

因此独立各行抽样时，联合漏失满足

    Pr(x被全部抽样query遗漏)
        ≤Π_(i∈J:B_i>0)[1−B_i(x)/B_i].             (MASS-MISS)

这里 action law 只按每个 action 的**总**停止质量定义，不用客户依赖的 IC 行权；它可直接输入 RANDOM-CUT。代价是归一常数 B_i，而不是财务 law 的 L_i。两者转换可精确写成

    p_i^mass(a)=λ_(i,a) v_(i,a)/B_i,
    v_(i,a)=b_(i,a)D_i(a)/A_(i,a)^stop.            (PRICE-CONVERT)

正 b 的 A_stop>0；零量项任意补零。v 是明确的 action 级转换因子。虽然 p^mass 本身仍能合法整体组合原 IC，但其转换后的费用没有已证的原 η 界；不能只保留 MASS-COVER 的好处，同时把财务费用继续按旧 λ 计算。

## 7. Hybrid 替换槽与真实付款 role 可分离

RANDOM-CUT 将 query B_i 放入同编号 i 的 OPT 槽只是一个选择，最优覆盖并不要求这个编号匹配。可将真实在 role i 发生的合法 query a 配到 source owner s 的比较槽。whole-IC 仍在真实 role i 上收费；混合覆盖仍只有每个 owner 槽至多一个合法 query。

更精确地，给任意非负数组 z_(s,i,a)，若

    Σ_(i,a)z_(s,i,a)≤1      对每个 owner s,

则可以在 owner 槽 s 以概率 z_(s,i,a) 放入合法 a，剩余概率保留 T_s（或其薄 Q_s）；不同 owner 槽之间可选择任意耦合。无需 Σ_(s,a)z_(s,i,a)≤1 对每个真实 i：同一真实 role 的不同合法 query 可以被放进不同的比较槽；这不会增加比较槽总数，也不假设玩家实际同时执行多个行动。

若按源标签拆分 stop 吸收，得到 λ_(s,i,a)=A_(s,i,a)^stop/D_i(a)，则

    Σ_s λ_(s,i,a)=λ_(i,a).

因此一个具体可攻的兼容条件是：通过合法改变 routing/query、交替 owner 配对或重新选择同一份运输，使每 owner Σ_(i,a)λ_(s,i,a)≤1。若得到它，z=λ 就同时是合法 owner 槽 lottery 和原真实 IC 财务系数，无 PRICE-CONVERT 的重加权债。**这一条件当前没有证明，本文也未验证原固定流必然满足它。**即使获得合法 lottery，仍需使其覆盖/漏失项实际支付 FRONTIER，不能把“可抽样”当作福利界。

owner/source 配对若改变，原 γ、η、已取消库存和实际 I 份额运输必须共同更新；不能沿用另一份旧配对的 SOURCE-NET 而免费重置 owner。这个限制正是交替操作需要保留的财务对象。

## 8. 接续义务与未采用的税势方向

真正可攻接口：对上述首次满行停止前沿 J，使用其真实生成它的后继 SPE 比较，为某份每 role 至多一主题的联合 law 证明一个足够的覆盖/利润耦合，将 RANDOM-CUT 的 owner 库存漏失、同一实际 I 份额流与 COV-STOP 的稀释项合并，支付 B≤E+U 或一个直接足够的全局界。当前没有这一关系，不能把最优性 cut 本身当作已付 captured reset。

曾考察统一缩尾税 g_(b,λ)(c)=1/(b+c)−λ/(b+λc) 的调和库存。若一条真实树查询链每次都覆盖同一个客户，其前缀覆盖数逐次增加，递减 g 确实可由 Σ_(ℓ=1)^n g(ℓ) 一次支付；但 captured 流在这里重置到原实际前缀，R 上前缀始终为零，恰不满足这一进度条件。因此没有把这个不接 SOURCE-NET 的新税势作为本轮正向结果，也不据此宣称任何一般方法不可能。
