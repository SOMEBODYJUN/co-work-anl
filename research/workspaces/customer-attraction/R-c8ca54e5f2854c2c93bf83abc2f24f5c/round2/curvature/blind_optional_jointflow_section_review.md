# Optional jointflow：遗漏客户的全 action 角色截面盲审

2026-10-25。**合同盲重构通过。** 本文从父方传来的定义独立推导，未先读 jointflow 作者新稿。初稿证明早报父方后，父方确认原 INIT 的有效 source query 覆盖该客户；本文另明确写出不要求此条件的广义版本。没有审查原 INIT 的 d/H/J。

本关系对任意固定纯 policy 成立，不需要 SPE。它是真正全 optional、全 action、允许同一有序 context 多入口合并的有限 DAG 截面预算，不是 `Σ c_V h≤1`，也不要求 common edge 全取满角点。SPE 只用于最后每个 action 组的实际前缀收益比较。

## 1. 审查对象与精确定义

固定原 CAG 实例、一个完整有序历史纯 policy σ 和实际根终局 B。固定一名**实际遗漏**客户 x，即 B 的所有主题都不覆盖 x。所有流、库存和不等式均先针对这一个 x；客户之间不混用库存。

自然 context t=(g,r) 中 |g|=r−1，规定行动为 a_t=σ_r(g)，自然终局为 V_t=finish_σ(g)。定义回到实际前缀的强制查询终局

    A_t=finish_σ(B_<r, a_t).

只允许 a_t 覆盖 x 的 context 接收 x 流。记 h_t≥0 为其全部入流，包括所有 source 边与所有父 context 边；记 c_t=c_x(A_t)。因为 x 实际遗漏，A_t 的前 r−1 槽均不覆盖 x，而当前 a_t 覆盖 x，所以

    c_t=1+|Q_t|≥1,
    Q_t={j>r : A_t 的 j 槽覆盖 x}.                 (1)

对每个 j∈Q_t，child s(t,j) 是终局 A_t 在 j 前的完整有序前缀所定义的真实 context。它规定的行动恰为 A_t 的 j 槽，故覆盖 x，且

    V_{s(t,j)}=A_t.                               (2)

(2) 对任意历史依赖 policy 都精确成立，不要求匿名、SPE 或固定平局。每条边严格增加角色，所以闭包有限且无环。

给边量 z_tj。若自然终局 V_t 的 j 槽不覆盖 x，必须 z_tj=h_t/c_t；若它覆盖 x，允许任意 0≤z_tj≤h_t/c_t。定义当前留量

    L_t=h_t−Σ_(j∈Q_t) z_tj.

由(1)和所有边的上界，有 L_t≥h_t/c_t≥0。

source α 有 owner i、query a_α、终局 W_α=finish_σ(B_<i,a_α) 和库存 p_α≥0，Σ_αp_α≤1。它只能向 W_α 的严格未来 x-coverer j>i 对应自然 context 发初始边 b_αj，满足

    0≤b_αj≤p_α/c_x(W_α).

当 c_x(W_α)=0 时没有合法边，下面该 source 的贡献定义为零。原合同另给 Σ_jb_αj≤p_α；在 x 实际遗漏的范围，这也已由逐边上界和 coverer 数量推出。

## 2. 目标角色上的点态留量界

固定任意目标角色 k。对 context t 定义只供本次截面证明使用的权

    φ_t=1                         若 role(t)<k，
    φ_t=1+|{j>k : V_t 的 j 槽覆盖 x}|   若 role(t)=k。

role>k 的点不计入本截面。

若 role(t)=k，记 C_t 为 Q_t 中 V_t 的同槽也覆盖 x 的 common future coverers，M_t=Q_t\C_t。所有 M_t 边必须发 h_t/c_t，而 common 边非负，因此

    c_t L_t
    ≤[c_t−|M_t|]h_t
    =(1+|C_t|)h_t
    ≤φ_t h_t.                                      (3)

这里 common 边可以任意取值，包含零、满额与所有中间值；没有选取一个特殊角点替代原流。

## 3. 目标角色以前的加权向前流不增

若 role(t)=r<k，只保留其 child 角色 j≤k 的边。设 Q_t 在区间 r<j<k、j=k、j>k 的数量分别为 n_<、ε、n_>，其中 ε∈{0,1}。

j<k 的 child 权为 1；若 j=k 的 child 存在，由(2)，其权为 1+n_>。故

    Σ_(j∈Q_t,j≤k) φ_{s(t,j)}
      =n_<+ε(1+n_>)
      ≤n_<+ε+n_>
      =c_t−1.

逐边上界随即给

    Σ_(j∈Q_t,j≤k) φ_{s(t,j)} z_tj
       ≤[(c_t−1)/c_t]h_t
       ≤h_t=φ_t h_t.                                (4)

此步甚至不需要辨认 mandatory/common 边；它允许所有早期边都取上界，所以对全部 optional 选择同时有效。

## 4. 任意多入口闭包的截面相消

在全部 role≤k 的接收 context 上求和流守恒。令

    M=Σ_(role<k) φ_t h_t,
    K=Σ_(role=k) φ_t h_t,

S 为所有 source 初始边进入 role≤k context 的 φ 加权总量，E 为父 role<k、child role≤k 的内部边 φ 加权总量。严格未来性给精确等式

    M+K=S+E.

由(4)，E≤M，故 K≤S；再由(3)，

    Σ_(role=k) c_t L_t ≤ K ≤ S.                     (5)

这个相消直接使用合并后的 h_t，不需要为每个父入口复制 context，也不要求给各 source 独立选择 optional 比例。多个父、多个 query、多个 source 到达同一历史的情形已包含在(5)中。

## 5. Source 端的准确金额

owner i≥k 的 source 不可能进入目标截面以前，故贡献零。对 owner i<k 的 source，令 c_α=c_x(W_α)，f_α 为 W_α 中严格晚于 i 的 x-coverer 数。与第3节同一计数，并用 child 自然终局等于 W_α，有

    Σ_(j>i,j≤k) φ_{s(α,j)} b_αj
       ≤ p_α f_α/c_α.                               (6)

因此最一般的本合同结论为

    Σ_(role=k) c_t L_t
       ≤Σ_(α:owner<k,c_α>0) p_α f_α/c_α
       ≤Σ_αp_α≤1.                                   (7)

x 实际遗漏，所以 W_α 没有过去 x-coverer。写 η_α=1[x∈a_α]，则 c_α=η_α+f_α。若有效 source 的 query 覆盖 x，即 η_α=1，(7)正好加强为父方待审合同：

    Σ_(role=k) c_t L_t
       ≤Σ_(α:owner<k) p_α(1−1/c_α)
       ≤1.                                          (8)

**Source 条件不可省。** 若只要求 W_α 某人覆盖 x，而允许 query 不覆盖 x，则应使用(7)，不能使用(8)。例如 m=2、owner=1、query 不覆盖 x、W_α 仅末位覆盖 x，c_α=1。初始边可发 p_α，目标 role2 可留下 p_α；(8)的该 source 右端却为零。(7)的系数 f_α/c_α=1 正确。父方确认原 INIT 的有效 source 有 η=1；本例只澄清扩域条件，不反驳原 INIT。

## 6. 每个 action 组的一次真实查询付款

对固定 k、固定合法 action a，所有满足 role(t)=k、a_t=a 的 context 都有相同的实际前缀查询终局 A_(k,a)，记其 x 负载为 c_(k,a),x。定义

    ℓ_(k,a),x=Σ_(t:role k,a_t=a) L_tx,
    K_(k,a)=Σ_(x实际遗漏) ℓ_(k,a),x.

由对每个客户同时覆盖所有 action 的(7)，

    c_(k,a),x ℓ_(k,a),x≤1.

只有 a 覆盖 x 时留量才可能非零，因此

    K_(k,a)
       ≤Σ_(x∈a且实际遗漏) 1/c_(k,a),x
       ≤u_k(A_(k,a)).                               (9)

若 σ 是完整纯 SPE，实际前缀 B_<k 上的一条真实 query IC 给

    u_k(B)≥u_k(A_(k,a))≥K_(k,a).                    (10)

所以同一 action 的多个自然 context 和多个 source 确实合并后只需一次该 action 的实际前缀 IC。不同 action 仍各有一条 IC；(7)的逐客户预算本身没有证明这些 IC 乘子的总行质量≤1，也没有证明 Σ_aK_(k,a)≤u_k(B)。这一总行质量仍是未付款义务。

## 7. 边界、依赖与状态

- 非 SPE 任意纯 policy：第1—5节及(9)全部成立；只在(10)使用 SPE。
- 任意历史依赖、同计数不同续局：保留完整有序前缀，(2)仍成立。
- 零库存或零入流：逐边上界迫使全部对应流为零，无 0/0。
- c_α=0 的 source：无未来 coverer 边，贡献约定为零；不写 1/c_α。
- 空 query 或空接收行动：不能覆盖该 x；前者按广义 source 条件处理，后者不能接收 x 流。
- k=1：所有初始和内部边都严格未来，故没有 role1 入流，左右皆零。m=1 也因此成立。
- k=m：目标权 φ=1，当前 A 无未来 coverer，c_A=1、L=h；同一证明直接成立。
- 实际遗漏是承重条件。它使每个 A_t 的全部 x 负载恰为当前加未来的 `1+|Q_t|`，并使 source 的 c_α=η_α+f_α。没有将过去 coverer 算成未来预算。

本轮审查确认一个适用于原全部输入规模的条件流组件，不确认原 INIT 能否提供这些 p、b、d/H/J，也未支付不同 query 的总 IC 行质量。故它不构成一般 half 或无条件 m=5 福利界；Q-CAG-HALF 仍 OPEN。
