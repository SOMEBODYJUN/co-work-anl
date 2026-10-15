# 辅助阶跃依赖模型：树与有向无环图独立重构

日期：2026-10-14。贡献来源：`/root/tree_review` 子 agent 独立树重构、DAG 命题重构与定义级精确审查；DAG generalization 的问题陈述由 R1 主对话提出。本审查没有读取主对话的候选证明或 verifier。已读取本分支 MODEL、ACCEPTANCE、MODELS、PEER 以及根研究规则。

**审查结论：** 下述精确 step 模型的振幅最优全状态门槛成立，并且端点取得。树模型是 DAG 模型的特例。一般零振幅、root 零振幅、空 light 图和严格载荷边界均已处理。此结论是辅助工具，不是 WC-TARGET v1 的 polynomial 突破，也不是新颖性或外部同行评审证书。

## 1. 来源核对与模型纠正

一手来源为 Christodoulou–Gairing–Giannakopoulos–Poças–Waldmann，*Existence and Complexity of Approximate Equilibria in Weighted Congestion Games*，arXiv:2002.07466v3，§6 Theorem 5，PDF 印刷页 17–18（PDF 页索引 17–18）：

- <https://arxiv.org/html/2002.07466v3>
- <https://arxiv.org/pdf/2002.07466v3>

原文构造的 heavy 策略是全部 `a` / 全部 `b`；light `i` 使用一侧 strict prefix 加另一侧自身资源，两侧完全对称。原文使用 `w_i=2^{-i}`，root breakpoint 为 1，light breakpoint 为 `1+w_i`，且链振幅与正根 `Phi_m` 相关。下述树是将 strict prefix 改成 strict ancestors；DAG 是将 ancestors 改成 incoming 邻居。

最初转述中的“heavy singleton a0 vs all b；light singleton a_v vs b_v+ancestors a”不是这个对称模型。审查在主对话明确纠正后仅采用以下模型；本结论不适用于该一侧转述。

本次文献核对仅确认这个固定版本及数学适配，没有做完整 tree/DAG generalization 的优先权检索。来源没有在此次核对的位置给出这里的任意振幅 upper theorem。

## 2. 精确 DAG 输入类

令 `D=(V,F)` 是有限 **simple** DAG，`|V|=m>=0`。无平行弧、无自环；策略是资源集合，平行弧若重复计数会破坏后文 path-count 公式。选任意 topological order，将 light 顶点编号 `1,...,m`。额外有 root/heavy 玩家 `0`。

资源为 `a_0,b_0` 以及所有 `a_v,b_v`。玩家权重严格正，满足

    w_0=1,
    sum_{v in V} w_v < 1,
    sum_{v: u->v} w_v < w_u  for every u in V.       (W)

任意这样的实数正权均可；存在性的明确有理证书为 `w_v=2^{-v}`。所有 outgoing 邻居排在 `u` 之后，其总权小于整个 dyadic tail，故 (W) 成立。这个权重选择中每个数的二进制位长为 `O(m)`。

振幅任意 `A_0,A_v>=0`，两侧同名节点使用同一 step：

    c_{a_0}(x)=c_{b_0}(x)=A_0 * 1[x>=1],
    c_{a_v}(x)=c_{b_v}(x)=A_v * 1[x>=1+w_v].       (C)

breakpoint 处取 **闭** 的 `>=`。root 策略为全部 `a` / 全部 `b`。light `v` 的两个策略为

    {a_0} union {a_u: u->v} union {b_v},
    {b_0} union {b_u: u->v} union {a_v}.            (S)

成本不乘玩家权重，近似均衡使用 `C_i<=alpha*C_i(dev)`，`alpha>=1`。

## 3. 真实载荷化简：承重义务

固定 heavy 使用全部 `a`；另一方向由交换 `a,b` 得到。令 `Z` 是自身资源使用 `a_v` 的 light 顶点集合。记

    P_v(Z)=A_0 + sum_{u->v, u in Z} A_u.

真实费用及单边偏离费用严格等于

| 玩家 | 当前费用 | 单边偏离后费用 |
| --- | --- | --- |
| root | `A_0+sum_{v in Z} A_v` | `A_0+sum_{v notin Z} A_v` |
| `v in Z` | `A_v` | `P_v(Z)` |
| `v notin Z` | `P_v(Z)` | `A_v` |

证明：无 heavy 的 `b` side 总载荷小于 1，所有资源不激活。在 heavy side，root 资源必激活。节点 `u` 的载荷为 1 加自身玩家（若 `u in Z`）再加选择含 `a_u` 的 outgoing 邻居。当自身玩家在时，载荷至少 `1+w_u`；当自身玩家不在时，(W) 给严格小于 `1+w_u`。因此 light 节点资源激活当且仅当其自身玩家在 heavy side。

light 偏离后仍有相同 root side；它在 incoming 资源上的加入或离开不能改变这些资源是否激活，因为所有 outgoing 使用者的总权严格小于该资源自身权。自身资源加入/离开则恰好改变自己的 step。root 偏离交换 heavy side 后，激活集恰从 `Z` 变成 `V\Z`。这些事实证明表中每个偏离费用；仅计算当前费用不足以闭合义务。

两个严格条件都是实质条件：若 outgoing 总权等于资源自身权，heavy 加 outgoing-only 的载荷可恰到 breakpoint；若 total-light 权等于 1，无 heavy 的 root side 可激活。审查脚本含两种等号失败的真实载荷 fixture。

## 4. DAG 最优门槛与任意振幅 upper

令 `P_k` 为 `D` 的非空 directed paths 中含恰 `k` 个顶点的数量；`P_1=m`。空 path 不计数。定义 `q_D` 为

    q_D = 1 + sum_{k=1}^m P_k / q_D^k.             (Q)

`m=0` 时定义 `q_D=1`。`m>0` 时右侧在正数区间严格递减、左侧严格递增，且在 1 处右侧大于左侧、无穷处小于左侧，故有唯一解 `q_D>1`。

为任意 `r>0` 定义 topological recurrence

    h_v(r) = (1 + sum_{u->v} h_u(r))/r.            (H)

展开 recurrence，`h_v(r)` 等于所有以 `v` 为终点的非空路径之 `r^{-顶点数}` 的总和。因此

    sum_v h_v(r)=sum_{k=1}^m P_k/r^k,
    sum_v h_v(q_D)=q_D-1.                          (HP)

**精确 upper statement。** 对每个满足 (W) 的权重和每组非负振幅，存在一个 `q_D`-PNE；端点包含在内。

构造：固定 heavy 为全部 `a`，按 topological order 处理顶点。所有 incoming 邻居已处理，计算 `P_v(Z)`；若

    q_D*A_v <= P_v(Z),

则将 `v` 放进 `Z`，否则不放。全过程以不等式实现，无 `0/0`。

若 `v in Z`，`A_v<=P_v/q_D<=q_D*P_v`；若 `v notin Z`，`P_v<q_D*A_v`。故所有 light 均满足近似均衡条件。按 topological order 归纳，对于每个被收入的点，

    A_v <= A_0*h_v(q_D),

因为 incoming 的被收入振幅已受对应 `A_0*h_u` 控制。因此

    sum_{v in Z} A_v <= A_0*sum_v h_v(q_D)
                        = (q_D-1)*A_0.

root 当前费用至多 `q_D*A_0`，偏离费用至少 `A_0`，故 root 也稳定。

此证明不要求 `A_0>0`。若 `A_0=0`，递推只会收入振幅零的点，所有 `P_v=0`；heavy 和所有 light 当前费用均为零，因此所得状态甚至是 exact PNE。`m=0` 时 root 两策略均收费 `A_0`，也为 exact PNE。

## 5. 匹配全状态 lower、端点、有理逼近

取任意 `A_0>0`，并令

    A_v=A_0*h_v(q_D)>0.                            (B)

对任意状态，按 heavy side 定义 `Z`。若 `Z=V`，root 的改善倍率恰为

    (A_0+sum_v A_v)/A_0=q_D.

否则选 topological order 中第一个不在 `Z` 的点 `v`。它的所有 incoming 邻居均在 `Z`；由 (H)，

    P_v(Z)=A_0+sum_{u->v} A_u=q_D*A_v.

所以该玩家的改善倍率恰为 `q_D`。所有分母为正。对每个 `1<=alpha<q_D`，每个状态都有严格 `>` 的偏离，故无 `alpha`-PNE。

upper 已保证 `q_D`-PNE，且这里 `Z=V` 本身是该端点的均衡：root 的比例恰 `q_D`，每个 light 的当前/偏离比例恰 `1/q_D`。`Z=empty` 也是 `q_D`-PNE，因为 `h_v(q_D)>=1/q_D`，light 的当前/偏离比例至多 `q_D`，root 没有改善。故该固定图、合法载荷类的振幅最优阈值 **maximally attained** 为 `q_D`，并非仅证明一个循环或一个 restricted witness。

更一般地，对任意 `r>=1`、`m>0`，取 `A_v=A_0*h_v(r)`。该单参数实例的真实最优近似因子恰为

    beta(r) = min{r, 1+sum_v h_v(r)}.              (R)

任意状态的 first-missing/root 论证给下界。`Z=V` 给第二个值；`Z=empty` 给第一个值，因为每个 `h_v(r)>=1/r`，且非空 DAG 存在一个 source，其 `h_v(r)=1/r`。这两个状态均包含所有 light 和 root 偏离检验。`m=0` 的最佳因子仍为 1。

因此选有理 `1<=r<q_D` 与有理 `A_0>0`，全部振幅、breakpoints、weights 都可有理，且该实例的最佳因子恰为 `r`。它们从下方任意逼近 `q_D`。实数输入类的匹配端点用 (B) 直接取得；不能在没有额外证明时声称全部图的匹配振幅本来就是有理数。

## 6. 树特化与极值

令树 root 为 `0`，light 节点深度为 `d(v)>=1`，`D` 放入每一对 strict light ancestor `u` 与 descendant `v` 的弧 `u->v`。这是 **transitive ancestors** 模型，不是只放 parent-child 弧的图。此时

    h_v(r)=(1/r)*(1+1/r)^{d(v)-1},
    q_T=1+(1/q_T)*sum_v(1+1/q_T)^{d(v)-1},
    A_v=(A_0/q_T)*(1+1/q_T)^{d(v)-1}.

在真实权重层面，(W) 恰要求每个节点 strict descendants 的总权小于自身权，再加 total-light 小于 1。

固定 `m`，star 所有深度 1，

    q_star=(1+sqrt(1+4m))/2.

chain 的深度为 `1,...,m`，几何求和给

    q_chain=(1+1/q_chain)^m,
    (q_chain+1)^m=q_chain^{m+1},

当 `m>=1` 时即来源中的 `Phi_m`；`m=0` 单独取 `q_chain=1`。任意树满足 `q_star<=q_T<=q_chain`。证明：所有深度至少 1；将节点按非降深度排成 `d_(1),...,d_(m)`，有 `d_(j)<=j`，因为每个深度 `d` 节点有一条包含 `d` 个 light 节点的祖先链。于是对任意 `r>0`，深度和在 star 与 chain 的深度和之间；方程的严格单调性传递为根的次序。`m>1` 时下端等号恰为 star，上端等号恰为 chain；`m<=1` 两者相同。

若树最大 light 深度为 `H_m=o(sqrt(m))`，且 `m->infinity`，则 `q_T/sqrt(m)->1`。因为 `q_T>=q_star>=sqrt(m)`，

    m <= q_T^2-q_T
      <= m*exp((H_m-1)/q_T)
      <= m*exp(H_m/sqrt(m)) = m*(1+o(1)).

由此先得 `q_T=O(sqrt(m))` 再除以 `m` 得结论。固定树、小 `m` 或 `m=0` 不使用这条渐近陈述。

## 7. DAG 度界及不可迁移的 height 条件

设最大 incoming light degree 为 `Delta`；`m=0` 时取 `Delta=0`。路径反向计数给

    P_k <= m*Delta^{k-1}.

对 `r>Delta`，

    sum_v h_v(r) <= m/(r-Delta).

取 `(r-1)(r-Delta)=m` 的较大根，得到

    q_D <= [Delta+1+sqrt((Delta-1)^2+4m)]/2.

当 `m>0` 时该根严格大于 `max{1,Delta}`，几何和合法；`m=0` 单独给 `q_D=1`。由 `P_1=m` 得 `q_D>=q_star`。因此 `Delta=o(sqrt(m))` 时，`q_D/sqrt(m)->1`。

还有 `m>=1` 时任意 simple DAG 的统一夹逼：topological order 中每个 `k` 顶点子集至多形成一条按该顺序经过的 path，故 `P_k<=binom(m,k)`，于是

    q_star <= q_D <= Phi_m.

两端分别在无弧图与完整 transitive DAG 取得。若弧集严格缺少一条，则 `P_2<binom(m,2)`，上端为严格不等；只有 `m<=1` 没有这一区别。

**height 误迁移的反例。** 树的浅高度结论不能按一般 DAG 的最长 directed-path 顶点数迁移。令 `D` 为 complete bipartite DAG，两层各 `s` 点，所有弧从第一层指向第二层。最长路径只有两顶点，但 `P_1=2s`、`P_2=s^2`，故

    q^3-q^2-2s*q-s^2=0,
    q ~ s^{2/3}=(m/2)^{2/3}.

这个增长严格大于 `sqrt(m)`。有理 dyadic weights 仍满足合法载荷条件。对应最大 incoming degree `s`，不满足前述小度假设。因此这不是 degree bound 的反例，而是对 height 替换的精确障碍。

## 8. 精确回归的实际范围

独立程序：`independent_audit.py`，不 import 主对话证明或 verifier。执行：

    python tests/audits/weighted_congestion/step_dag/independent_audit.py

实际输出（2026-10-14）：

    status: PASS
    seed: 200207466
    graphs: 103
    real_load_profiles: 5918
    amplitude_instances: 2954
    all_state_amplitude_profiles: 105050
    balanced_exact_instances: 515
    tree_symbolic_specializations: 154
    exact_optimal_endpoints: 3
    rejected_boundary_fixtures: 2

载荷用整数缩放的 dyadic 正权，费用及比较用 `Fraction`，没有浮点阈值判断。覆盖固定 topological 编号的全部 simple DAG `m<=4`；这些代表所有 abstract DAG 的某个 topological relabelling，但没有做同构去重。`m<=3` 的振幅为 `{0,1,2}` 全枚举；`m=4` 为 `{0,1}` 全枚举。额外随机 `m=5,6,7` 各 8 个图，每图 8 组非负有理振幅。每个图对所有 heavy/light 纯状态核对真实策略载荷与 reduced table 的 resource-level coefficient masks；所有偏离状态同在枚举中。

路径 recurrence 与整数 path counts 在多组有理参数处精确相等；universal upper 用 72 步有理 bisection 的 `q_D` 上方括号，endpoint 本身由一般证明及三个恰为整数的实例检验：两点无弧图 `q=2`，五点三弧 branching 与五点三弧 merging 图 `q=3`。单参数 (R) 在每图五组有理参数逐状态精确检验，含 `r>q_D` 的 branch。树特化覆盖 `m<=5` 的全部 increasing-parent trees，且每树四组有理参数核对公式与 star/chain envelope。

两种严格载荷条件的等号 fixture 均显式与 reduced table 不符。随机及有限精确枚举不替代一般证明，也不构成 polynomial cost 模型的证据。

## 9. 审查状态与剩余义务

对象、定义域、全部量词、strict improvement、zero costs、breakpoint endpoint、empty light graph、负载合法性、amplitude upper 与 matching lower 均已独立闭合。未发现针对上述精确命题的 fatal objection。

仍须主对话核对冻结主证明与本重构一致，完成仓库 claim/asset/graph 登记、必需 checks、checkpoint 和 provenance。完整新颖性检索、外部同行评审、step 到 nonnegative polynomial 的桥梁均未完成。具有任意正振幅的真实 step 函数不是有限次数多项式；本辅助最优阈值不得升级 WC-TARGET v1，也不能升级一般 arbitrary-latency games 的普遍上界。


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
