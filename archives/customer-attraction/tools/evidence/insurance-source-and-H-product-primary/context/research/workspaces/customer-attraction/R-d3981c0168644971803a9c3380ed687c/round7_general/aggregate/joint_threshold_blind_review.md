# joint-threshold 产品合同：独立盲核

2026-10-25。审查对象是父方和 signed 以消息给出的合同；消息已含“一个总约束的极点至多一组两项混合、向较高 v 一次舍入”的证明提示。本页对其独立核查，**不是无提示发现或完全无提示重构**。完成本页时**没有读取作者稿** `signed/pooled_successor_transfer.md`。对象保持原 CAG 的单位客户、共同有限目录、任意完整有序历史纯 SPE；以下合同只构造可信产品续局，不证明一般 half。

**结论：未发现 fatal；在下面明确的量词和 D 定义下合同成立。** 独立证明见第2–5节。r=2 可取 D=0；零客户和零副本均给零。共同乘子不需达到最大，也不要求 H 凹。作者关于“共同 t 可能严格优于逐项 sup”的代数说法正确；本核没有提供原 CAG 可实现菜单中的严格改善例。

## 1. 精确对象

各 component 有相同剩余角色数 r≥2，允许不同有限共同目录和不同合法有序前缀；亦可把背景固定为非负整数负载。客户在 component 间不交，产品目录取完整 Cartesian。类型 k 有整数 n_k≥0 个相同副本。

对 component k 的当前强制 A，下一角色选 B 后，保留 B 后的**全部真正完整历史纯 SPE**。每份这样的 grandchild 记 z，记录完整终局的

    d=u_current(z),   v=u_next(z).

菜单有限非空；不同 grandchild 策略可有相同数值，但保留至少一个实现者。定义

    θ_k(A)=max_B min_(true grandchild z after A,B) v(z),
    f_kA(t)=min_(B,z) [d(z)−t(v(z)−θ_k(A))],
    H_k(t)=max_A f_kA(t),
    Ψ(n)=sup_(t≥0) Σ_k n_k H_k(t),
    D=max_(k:n_k>0,A) [max_(B,z)d−min_(B,z)d].

D 必须覆盖全部有正副本数的类型和全部当前强制 A，不能只取最优选项或实际 A 的范围。若无副本，约定 D=0。

本文的 M_product 精确指

    max_(joint A) min_(full-history SPE of child after joint A)
                         current total payoff.

它亦是该产品节点上当前玩家可被完整 SPE 实现的最低可信利润。若 M 使用其他含义，需另核；本结论不把它当作福利或实际固定策略的当前利润下界。

## 2. 一个总 v 门槛足以构造真正 child SPE

固定任意 joint A。每坐标选一个选项 (B,z)，若其下一角色收益之和满足

    Σ_coords v ≥ Σ_coords θ(A),                     (1)

就能实现当前总利润为 Σd 的完整 child SPE。

证明：在选定 joint B 孩子，逐坐标执行所选的完整 grandchild SPE，取完整策略 Cartesian 产品。对每个其他 joint B'，每坐标独立选达到该 B'_coord 对应最小 v 的真正 grandchild，并取产品。下一玩家在该联合偏离下的总利润为

    Σ_coords min_(true z after A_coord,B'_coord) v
      ≤Σ_coords θ(A)
      ≤选定 joint B 的总 v.

故下一玩家对所有联合 B' 都最优，包括只改一坐标、多坐标和所有坐标。选定 joint B 自己无需换成最小退出：它就是规定孩子，收益已满足 (1)。其他 joint B' 中即使某坐标 B'_coord=B_coord，也允许给该坐标重新选最小退出 grandchild；这不是一次坐标策略改变，而是在**不同完整联合历史**下指定续局，原全历史模型明确允许。

每个 grandchild 产品在其全部有序联合历史为 SPE：任意联合行动偏离的收益增量等于各 component 合法偏离增量之和。各 joint B' 是不同有序孩子，可独立拼合。因此没有冻结尾部、没有把 joint B' 当单 component 偏离，也不只验证在轨历史。

## 3. 固定 joint A 的 LP 与一副本舍入

按 (k,A) 分组，组质量 n_kA 为该类型被强制 A 的副本数，都是整数且 Σ_A n_kA=n_k。删去零质量组。LP 为

    minimize Σ_(g,o) X_go d_go
    subject to Σ_o X_go=n_g  (each group),
               Σ_(g,o) X_go(v_go−θ_g)≥0,
               X_go≥0.                                 (P)

可行性不能省略：对每组取一个达到 max_B min_z v 的 B；该 B 的每个 grandchild 都有 v≥θ，所以任选一个实现者就给整数可行点。可行域有限紧，故存在最优极点。

若正质量组数为 G，则极点正变量至多 G+1。直接线性相关证明：若大于 G+1，有非零双向可行扰动同时保持所有 G 个组质量和一条总 v 等式，故不是极点。总 v 不等式若不活跃，最多 G 个正变量。因此每组至少一项，至多一组有两项，其余组都是单项，且单项质量是整数 n_g。

唯一可能混合组设两项为 lo、hi，v_hi≥v_lo，总质量 n_g 为整数。将 X_hi 向上取整，X_lo=n_g−X_hi；这最多改一个副本的选项，保持非负和组质量，总 v 只增不减。d 增量为

    (ceil X_hi−X_hi)(d_hi−d_lo) ≤ D.

若 d_hi≤d_lo 则成本不增；若 v 相等，可任选方向，且真正极点也可选成单项。由于 X_lo>0 时 X_hi<n_g，ceil 不超过 n_g。整数化后的每份副本都选一个真正 grandchild，用第2节得到完整 child SPE。

所以对该**任意固定 joint A**，存在 child SPE 使

    current total d ≤ value(P)+D.                    (2)

这是存在构造，不声称每份 child SPE 都有该上界，也不保留任意预先指定的 child 策略。

## 4. 对偶和全部当前强制

有限 LP 强对偶给

    value(P)=sup_(t≥0) Σ_(k,A) n_kA f_kA(t).          (3)

符号为减 t(v−θ)，因为原约束为总 v−θ≥0。每组 θ 常数已经计入 f，不能在总阈值另加或漏减一次。

由 (2) 对全部 joint A 取最大。所有最大/上确界都是同向 supremum，故交换不需要任何凸凹条件：

    M_product
      ≤ max_(joint A) sup_(t≥0) Σ_coords f_(k,A)(t)+D
      = sup_(t≥0) Σ_k n_k max_A f_kA(t)+D
      = Ψ(n)+D.                                      (4)

等式利用完整 Cartesian 当前行动域，各坐标 A 可独立选择；若产品目录不是完整 Cartesian，该等式需改为对应可行联合最大。

对每个 joint A 独立选择已构造的 child，然后让当前角色选择其中当前利润最大的 joint A，就得到该节点的一份完整 SPE，其当前利润仍≤Ψ+D。因此所有强制孩子可同时指定，不需要它们采用同一组 grandchild 或同一舍入结果；它们位于不同完整有序历史。

同理

    Ψ(n)≤Σ_k n_k sup_(t≥0)H_k(t).

共同 t 可以在抽象有限菜单上严格小于分别 sup；但要声称某原 CAG 实例确有严格收益，需要给原 CAG 可实现菜单。不能把抽象 d,v 表当作 CAG 反例或正面福利证据。

## 5. 端点

- **r=2：** grandchild 已终端，无后继策略选择。每个 B 的 v≤θ=max_Bv。因此总 v≥Σθ 强迫所有坐标使用 v=θ 的末位 BR。固定 joint A 的最小当前 d 精确逐坐标相加；全 joint A 也可逐坐标最大。因此 M_product=Σ_k n_k M_k，D=0。LP 自动可取整数，无须舍入。
- **r=1：** 原 statement 的 next 与 θ 未定义，应单独处理。当前强制 A 即终端，产品利润直接可加。若统一约定每 A 一个选项 v=θ=0，则同式退化且固定 A 范围 D=0。
- **零客户：** 所有 d,v,θ 为零，D=Ψ=M=0。
- **零副本：** 组全空，空产品当单一空坐标行动，current/next 利润零；D=Ψ=M=0。不得让空 max 的 D 未定义。
- **固定背景：** 只改变 d,v 的数值，不改变有限性、产品可加、真正 subgame 拼合或舍入。合法有序前缀的量词不被计数压缩替代。
- **零质量组、相同选项、平局：** 零组删除；重复选项可保留实现者或去重；全部平局任选真正 grandchild，证明不要求规范 tie rule。

## 6. 审查等级和精确核

解析核查覆盖极点、舍入、全部强制、所有联合下一角色偏离及完整历史拼合。已经收到合同中的极点/舍入提示，全文未读；未认证外审或新颖性。合同本身不支付 Ψ 或 D，更不推出 OPT≤2W。

附 [独立精确核](audit_joint_threshold_blind.py) 与 [输出](joint_threshold_blind_audit.json)。核只服务本一般合同：分数精确枚举一个抽象菜单的全部极点并核共同 t 严格差，以及在一个明确三角色 CAG 产品的每个 joint A 下构造并逐联合历史核查 child SPE。它不穷尽一般输入，也不把有限输出当作一般证明。
