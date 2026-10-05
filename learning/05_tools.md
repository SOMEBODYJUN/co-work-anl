# 05｜把存在性证明拆成可学习的算法工具

本讲属于任意设施数、共同目录的 `MF-MODEL`。先读[任意设施数模型](../research/current/multi_facility/model.md)及[第 03 讲的因子 2 存在性证明](03_arbitrary_k.md)。本讲不要求先学完流算法或参数化复杂度；主课要掌握贪心数据、负载盒和完整续局怎样接起来，深入课再分工核查两个最新条件接口。

**主课必会：**第 1–5 节的对象、公式及证明；能独立处理单设施源消失的客户。**深入课必知：**第 6–7 节的精确条件、为何比旧接口宽、还缺什么；报告人继续按所列源页逐式阅读。第 8 节只选一条路线做专题，不要求背所有子类。

截至本次整理，这些新接口有仓内完整证明及内部复核，没有外部同行评审；被导入的调度算法已经发表，但仓库尚无其规范实现。例子审计不替代一般证明。

## 1. 三层对象不能混同

客户权重为正二进制有理数，目录为有限集 $S$，共有 $k\ge2$ 个显式列出的带标签设施。固定布局的已占地点集为 $O$，地点 $t$ 的设施数为 $q_t$。

若每名已服务客户只选一个地点，再独立均匀选该地点的设施，记地点客户池为 $J_t$，重量为 $W_t$。设施收益是 $W_t/q_t$，但客户 $i\in J_t$ 的条件成本是

$$
w_i+\frac{W_t-w_i}{q_t}.
$$

因此这种策略是精确客户 NE 当且仅当对每个可达已占地点 $v\ne t$，

$$
\frac{W_t-w_i}{q_t}\le\frac{W_v}{q_v}.\tag{RQ}
$$

可行分配、客户 NE、设施因子 2 稳定性是三层要求。前一层成立不会自动给出后一层。下文的上标 $0$ 始终表示**贪心的原始客户池**；选好的在轨 NE 可以有另一个分配 $J_t$。离轨续局还可以重新分配客户。下文 stationary 指未搬迁设施，ordinary 指参与受帽均衡化的设施；forced 指在当前布局仅有一个已占地点可选的客户。

## 2. 贪心先造出哪些可靠数据？

`SC-K-GREEDY-BUDGET` 的每步只放一家设施：

1. 已占地点 $t$ 的分数是 $W_t^0/(q_t+1)$。
2. 未占地点 $r$ 的分数是它当前能新覆盖的客户重量。
3. 选最大分数；若首次开站，把它覆盖的全部未服务客户收为原始池 $J_r^0$。已开站的客户池此后不变。固定地点顺序破同分。

设最后一次入席分数为 $\gamma$。若某个地点的覆盖重量为正，则 $\gamma>0$。各步最大分数不增：增席只降低该站的下一席分数，首次开站只减少其他站的未覆盖客户。若所有地点覆盖重量都是零，任意布局和空续局已经精确稳定，单独处理即可。

从“某站最后一次入席”和“算法结束后的下一席候选”分别得到

$$
q_t\gamma\le W_t^0\le(q_t+1)\gamma\quad(t\in O).\tag{G1}
$$

对始终未开站的 $r$，记真正新覆盖重量

$$
N_r=w\!\left(C_r\setminus\bigcup_{t\in O}C_t\right).
$$

它的最后候选分数至多 $\gamma$，所以

$$
N_r\le\gamma.\tag{G2}
$$

还有一条重要的时间顺序性质：

$$
i\in J_s^0,\quad i\in C_t,\quad t\in O
\quad\Longrightarrow\quad q_t\le q_s.\tag{G3}
$$

证明如下。客户 $i$ 在 $s$ 首开时才被覆盖，所以另一个覆盖它的已占地点 $t$ 必须晚开。在 $s$ 首开之前，$t$ 的新覆盖池至少包含它将来的原始池及额外的 $i$；因此 $W_s^0>W_t^0$。若最终 $q_t>q_s$，则在 $t$ 最后入席之前，已开 $s$ 的候选分数满足

$$
\frac{W_s^0}{q_s^{\rm then}+1}
\ge\frac{W_s^0}{q_s+1}
>\frac{W_t^0}{q_s+1}
\ge\frac{W_t^0}{q_t},
$$

与选择 $t$ 矛盾。这个性质只约束原始归属，客户后来允许返回高重数站。

贪心原始分配还满足主证明的四个迁移预算。对源站 $u$，令 $a^0=W_u^0/q_u$，则

| 源站 | 目标 | 原始池预算 |
| --- | --- | --- |
| $q_u\ge2$ | 其他已占 $t$ | $W_t^0\le(q_t+1)a^0$ |
| $q_u\ge2$ | 未占 $r$ | $N_r\le a^0$ |
| $q_u=1$ | 其他已占 $t$ | $W_t^0+w(J_u^0\cap C_t)\le(q_t+1)a^0$ |
| $q_u=1$ | 未占 $r$ | $N_r+w(J_u^0\cap C_r)\le a^0$ |

源站最后入席之前，它获选的分数正是 $a^0$。对当时已开的目标，客户池已经固定；对当时未开的目标，其未覆盖池包含表中需要计入的客户。与这个时刻的候选分数比较即可证明四行。单设施源的原客户必须计入；只比较 $N_r$ 会漏掉源站消失的客户。

**这一步的输出通常不是客户 NE。**贪心只给我们良好的原始预算与可复用的重置对象。完整原论证见 [polytime_frontier.md 的 GREEDY-BUDGET / MAX-MULT](../research/current/multi_facility/polytime_frontier.md#sc-k-greedy-budget-polynomial-transfer-budgets-alone)。

## 3. 两个可复用的离轨原语

### 3.1 `MF-PACK-2`：总量预算变为设施装箱

若 $a>0$、有 $h\ge1$ 家 stationary 设施、客户总重 $W\le(h+1)a$，可以把客户放进至多 $h$ 个箱子，每箱满足下列之一：总重至多 $2a$；或仅有一名重量超过 $2a$ 的客户。

完整证明很短：先每客一箱，不断合并总重至多 $2a$ 的任意两箱。重于 $2a$ 的单客箱永远不被合并。停止后任意两箱之和都大于 $2a$。若仍有 $b\ge h+1$ 箱，把全部两两不等式相加得到

$$
(b-1)W>2a\binom b2=(b-1)ba,
$$

于是 $W>ba\ge(h+1)a$，矛盾。算法至多合并 $n-1$ 次，不是最优装箱 oracle。

### 3.2 `MF-PURE-CAP-POLY`：可行帽容量初态变为精确纯 NE

固定真实偏离后的布局，给一个可行纯分配。假设每个负载超过 $B>0$ 的设施仅有一名重于 $B$ 的客户，其他 ordinary 设施负载都至多 $B$。称前者为孤立大客户设施。

暂时删去孤立大客户及其设施，其余每名客户保留全部可达 ordinary 设施。它原来的设施仍可用，所以子问题可行。每家设施是一条**相同**链，每名原子客户是一份不可拆的任务；纯客户 NE 条件恰为

$$
L_g\le L_h+w_i.
$$

已发表的 restricted identical-link Nashification 从任意可行分配得到纯 NE，保持最大负载不增。因此 ordinary 负载仍至多 $B$。再插回孤立大客户：它支付自己的权重，已达绝对最低成本；ordinary 客户当前支付至多 $B$，加入大客户设施的成本超过 $B$。得到全游戏精确纯 NE，指定 ordinary 偏离者保持至多 $B$。

这是对公开算法的精确接口。主课可以调用该定理，但要会解释删除、限制和重新插回为何合法。算法的 blocking-flow 内部证明并未在本讲重写；深入报告须读[原论文](https://cgi.csc.liv.ac.uk/~gairing/publications/2004-stoc.pdf)第 4 节的 Figure 3、Corollary 4.3、分阶段流程和 Theorem 4.7。论文对单次 blocking-flow 的上下极值保持有明确结论；整个 Nashification 的最低值保持，还需追踪各子实例及未改变的补集。这是[仓内接口说明](../research/current/multi_facility/adaptive_reset_floor.md#22-capped-pure-nashification)所作的流程推导，不能只用“最大值不增”代替。

**位复杂度为何过关？**若 $w_i=u_i/v_i$，统一乘 $D=\prod_i v_i$。虽然 $D$ 的数值可能巨大，$\log D\le\sum_i\log v_i$，位长是多项式；缩放不改变比较与 NE。论文 Theorem 4.7 的运算界为 $O(rKA(\log W+K^2))$，其中 $r$ 是不同整数权重数、$K$ 是相同链数、$A$ 是允许边总数、$W$ 是缩放后的总重；至多 $r\le n$。这里使用总整数重量的对数，不逐单位重量循环。装箱、排序及预算检查也只处理多项式位长的精确有理数。详细接口见 [MF-PURE-CAP-POLY](../research/current/multi_facility/polytime_frontier.md#mf-pure-cap-poly-polynomial-completion-from-a-capped-pure-assignment)。

## 4. 最容易遗漏的一支：单设施源的原池重置

`SC-K-GREEDY-SINGLETON-RESET` 的条件是：固定贪心布局，$\gamma>0$，源站 $u$ 原本只有一家设施，而已给的在轨 NE 中该设施收益 $a\ge\gamma$。在轨策略可以是任意显式有理独立混合，不要求客户仍在原始池。

目标：为它的每次迁址构造精确纯客户 NE，使偏离者收益至多 $2\gamma\le2a$。

令 $K=\{t\in O:q_t=1\}$，$P=\bigcup_{t\in K}J_t^0$。由 (G3)，$P$ 客户的任何已占选项都在 $K$。在 $K$ 中第一个地点 $s$ 开站时，$P$ 全部还未覆盖；因此对每个 $t\in K$，

$$
w(P\cap C_t)\le W_s^0\le2\gamma.\tag{S1}
$$

偏离后，**先忘掉在轨客户分配**，把原客户放回贪心原池。只有 $J_u^0$ 失去原站，按三类穷尽处理：有 surviving 已占选项就放过去；否则新开的偏离地点覆盖它就给偏离者；两者都没有就不服务。新开目标的真正新客户也给偏离者。

每个 surviving 单设施地点 $t$ 的客户都是 $P\cap C_t$ 的子集，由 (S1) 其负载至多 $2\gamma$。高重数地点保留原池，以 $a=\gamma,h=q_t$ 调用 PACK。已占目标的偏离者可先空着；新开目标 $r$ 的初始偏离者负载由原始 singleton 预算控制：

$$
N_r+w(J_u^0\cap C_r)\le W_u^0\le2\gamma.\tag{S2}
$$

所有实际被覆盖的客户都已分配，再以 $B=2\gamma$ 调用帽容量 Nashification。注意 (S1) 用的是全部原 singleton 池，(S2) 用的是原源池；均不要求在轨 NE 提供私有储备。

## 5. `BOX-TO-2`：给盒内在轨 NE，就能完成总续局

**精确条件：**固定贪心布局，给出 site-pure、站内独立均匀的精确客户 NE，并对每个已占地点有

$$
q_t\gamma\le W_t\le(q_t+1)\gamma.\tag{BOX}
$$

**结论：**该布局和该在轨 NE 能在输入位长多项式时间内补成完整精确因子 2 续局。这是条件算法，没有宣称任意贪心布局都能找到这样的 NE。

证明分两支。源重数为 1 时用第 4 节。源重数 $q_u\ge2$ 时，设偏离者在轨收益 $a=W_u/q_u\ge\gamma$。源站 surviving 的 $h=q_u-1$ 家设施要承接总重

$$
W_u=q_u a=(h+1)a.
$$

其他地点 $t$ 的 stationary 数为 $h=q_t$，承接总重

$$
W_t\le(q_t+1)\gamma\le(h+1)a.
$$

逐站用 PACK。已占目标的偏离者先空着；新开目标给它重量 $N_r\le\gamma\le a$ 的真正新客户。因为源站 surviving，没有旧客户丢失覆盖。以 $B=2a$ 用帽容量 Nashification 得到该项偏离的精确纯 NE。

最后，只有 $k(|S|-1)$ 个实际单坐标偏离。它们是互不相同的带标签布局，给每项保存上述分配；在轨保存所给 NE；其他布局由固定公开 Nashification 规则返回纯 NE。输出的是一个多项式大小、可按查询布局求值的**完整规则**，无需打印 $|S|^k$ 行表格。源页：[SINGLETON-RESET / BOX-TO-2](../research/current/multi_facility/polytime_frontier.md#sc-k-greedy-singleton-reset-and-sc-k-greedy-box-to-2)。

## 6. 深入课：自适应重置不再要求最终在轨状态在盒内

`SC-K-ADAPTIVE-RESET` 仍用原始贪心池，但容量可以随源站实际收益增大。给定显式有理独立混合在轨 NE，所有设施收益 $a_f\ge\gamma$。每个 $q_u\ge2$ 的源站定义

$$
b_u=\min_{f:s_f=u}a_f.
$$

若原始池 $J_u^0$ 能提供一个 $q_u-1$ 箱证书，各箱至多 $2b_u$ 或是重于 $2b_u$ 的单客箱，则完整因子 2 续局可在位长多项式时间构造。也可用已证下界 $\gamma\le\rho_u\le b_u$，按 $2\rho_u$ 检查。

理由：$q_u\ge2$ 时重置全体旧客户到原池；源站用给定删席箱，其他站满足 $W_t^0\le(q_t+1)\gamma\le(q_t+1)\rho_u$，可用 PACK。新客户至多 $\gamma$；于是帽容量 $2\rho_u\le2a_f$ 合法。singleton 源仍用第 4 节。这个接口不寻找删席箱。

为了在客户 NE 之前获得收益下界，`SC-K-FORCED-FLOOR` 使用该布局上**只有一个已占地点可选**的 forced 客户。某站有 $q$ 家设施，forced 权重递减排列 $v_1\ge\cdots$，末尾补零，令

$$
F=\sum_jv_j,\quad H=\sum_{j=1}^{q-1}v_j,\quad D=F-H,
\qquad \eta_s=\min_{0\le h\le q-1}\max\left(v_{h+1},\frac D{q-h}\right).\tag{F}
$$

**每个精确纯客户 NE** 在本站的每家设施收益都至少 $\eta_s$。纯策略限定不能删。证明的关键是取最轻设施负载 $\ell$：重于 $\ell$ 的 forced 客户必须分占不同设施，且不能与另一 forced 客户同居，否则后者愿意转到最轻设施；设它们有 $h\le q-1$ 名。对其余设施分别用最轻 forced 客户作 NE 比较，扣掉至多 $q-h-1$ 个代表，得到 $D\le(q-h)\ell$ 及 $v_{h+1}\le\ell$，推出 (F)。报告人须在[源页第 4 节](../research/current/multi_facility/adaptive_reset_floor.md#4-a-computable-local-floor-for-every-pure-equilibrium)核对代表求和的完整步骤。

`SC-K-ADAPTIVE-DOUBLE-LPT-2` 给一个条件识别算法：原池先按降权、最轻箱放进 $q_s$ 箱，检查每箱至少 $\gamma$；再放进 $q_s-1$ 箱，检查每箱至多 $2\max(\gamma,\eta_s)$。全通过就对第一分配做保持最低负载的纯 Nashification，所得收益至少 $\max(\gamma,\eta_s)$，然后调用 adaptive reset。测试失败返回 **unknown**，并未决定实例无解。此特殊算法的删席箱均要求不超帽；一般 adaptive theorem 仍允许孤立大客户。

必学分离例是[源页第 6 节的异权三角](../research/current/multi_facility/adaptive_reset_floor.md#6-exact-triangle-separating-the-interfaces)：$q=(4,3,1),\gamma=100$，H 原池有四名私有客户 $114,110,110,110$，旧 $200$ 帽不可能放进 3 箱；新帽 $220$ 可装成 $119,220,160$。得到的一项纯在轨 NE 在 M 的总重为 $430>400$，仍能完成因子 2。分离的是旧接口，未证明同布局没有别的盒内 NE。

## 7. 深入课：冻结安全超载，只给偏离者设帽

`MF-FROZEN-OVERLOAD-POLY` 不再要求其他设施最后也都低于偏离者的帽。固定某个真实布局、指定偏离者 $f$、给 $B\ge0$ 及一个可行纯初态，设施负载记为 $M_g$。把初态超过 $B$ 的设施集合记为 $H$，其余 ordinary 集合记为 $U$，要求 $f\in U$。冻结 $H$ 的设施和客户，只对剩余客户及 $U$ 做子游戏。

对子游戏重算 forced 池、ordinary 重数 $q'_s$ 和 (F) 的 $\eta_s$。对每个冻结客户 $i$（位于 $h$）检查

$$
M_h-w_i\le M_{h'}\quad\text{每个其他可达冻结 }h',
\qquad
M_h-w_i\le\eta_{s(g)}\quad\text{每个可达 ordinary }g.\tag{SAFE}
$$

**为什么充分？**对子游戏做保持最大负载的纯 Nashification。其最终 ordinary 成本至多 $B$，而负载至少对应 $\eta_s$。重新插入冻结客户后：ordinary 客户不想加入负载 $>B$ 的冻结设施；冻结客户由 (SAFE) 不想转到其他冻结设施或任何 ordinary 设施。因此得到全游戏精确纯 NE，且 $f$ 的收益至多 $B$。这里的 floor 只断言**最终纯 NE**，不要求中间每步满足。原子大客户单占时外部负载为零，所以旧孤立大客户证书是特例。

`SC-K-FROZEN-OVERLOAD-2` 的完整接口是：给**任意布局**和显式有理独立混合在轨 NE，并为每个实际偏离提供通过 (SAFE) 的纯初态证书，取 $B=2a_f$。即可多项式补完续局；不要求贪心、盒、原池删席装箱。未知的是怎样高效选择在轨状态并产生全部成功初态。$a_f=0$ 时仍须检查 $B=0$，不能跳过该设施。

必学例是[源页第 4 节的 cap-41 分离](../research/current/multi_facility/frozen_overload_completion.md#4-exact-strict-separation-from-global-cap-feasibility)：旧全局帽 $41$ 无任何合法纯初态，冻结 $20+24=44$ 却安全，因为共享客户的外部负载 $20$ 不超过普通目标的 forced floor $20$。完整源页还给出初态、一次严格改善和最终 NE。报告人须逐项核查其实际可达集合；不能只看总负载表。

## 8. 特殊子类怎样学，才不被清单淹没？

这些定理是条件类，不是靠并列很多类就覆盖一般输入。专题只选一条，其余按需查[现行登记](../research/current/claims.md)。

| 技术主线 | 一条代表性阅读 | 需要解释的机制 |
| --- | --- | --- |
| 相同重数的文献接口 | [相关链边界第 2–3 节](../research/current/multi_facility/restricted_related_link_boundary.md) | 等 $q$ 时 (RQ) 约化为相同链；混合 $q$ 时直接代速度不合法 |
| 相同轻权的整数流 | [UNIFORM-LIGHT-FLOW](../research/current/multi_facility/polytime_frontier.md#sc-k-uniform-light-flow-2-partial-overlaps-without-a-common-anchor) | 等单位运输反路径如何排除上盒溢出；异权时哪一步失效 |
| 结构允许一次扫描 | [STAR-LIGHT](../research/current/multi_facility/polytime_frontier.md#sc-k-star-light-greedy-2-unequal-light-weights-on-anchored-star-edges) | 权重队列、目标负载单调性及每客一次如何同时给 NE 和复杂度 |
| 有界结构的精确求解 | [local_weight_box_dp.md](../research/current/multi_facility/local_weight_box_dp.md) | 哪些参数必须固定，指数依赖为何不等于一般输入多项式 |

## 9. 手算任务与核对标准

先遮住答案，每题必须写出使用的对象和适用域。

**T1｜贪心不是 NE。**$k=2$，客户为 $6:\{A,C\},3:\{A,B\},5:\{B\},2:\{C\}$。依次算贪心选址、$\gamma$、客户改善、最终 NE，并区分“旧预算失败”和“因子 2 失败”。

**T2｜盒完成的存活源。**$\gamma=10$，源站 $q_u=3,W_u=36$，另站 $q_t=2,W_t=30$，未开目标 $N_r=7$。源站一家迁到 $r$ 后，分别写 stationary 数、PACK 总量预算和帽 $B$。不必知道客户权重的具体分解。

**T3｜纯 NE 下界。**$q=3$，forced 权重 $100,100,1,1,1,1$。计算 $D$、三项候选及 $\eta_s$。解释为何不能把这个 proof 直接用于混合 NE。

**T4｜最新接口。**在 cap-41 例中，为什么冻结 E 的 $20+24$ 客户可行？如果普通 B 或 G 的最终保证 floor 只有 $19$，这个证书哪条检查失败？

**答案与标准：**

- T1：原始 reach 为 $9,8,8$，贪心先 A 后 B，原始负载 $9,5$，$\gamma=5$。权重 3 客户支付 $9>8$ 而迁到 B；最终 $6,8$ 是唯一客户 NE。A 迁 C 的旧 singleton 预算要求 $2+6\le6$，失败；实际偏离收益 $8\le12$，因子 2 仍通过。两种失败必须分开。
- T2：偏离者原收益 $a=12$，帽 $B=24$。源站剩 2 家，$36=(2+1)12$；另站 2 家 stationary，$30\le(2+1)12$；偏离者先装真正新客户 7。PACK 后普通设施至多 24，再调用帽容量 Nashification。不能误用另站的下一席总数 3 作为 stationary 数。
- T3：$F=204,H=200,D=4$。$h=0,1,2$ 的候选分别为 $100,100,4$，故 $\eta_s=4$。证明利用纯分配中“大客户是否同处一家设施”的结构，未处理混合概率；这个限制须保留。
- T4：共享 24 在 E 的 external load 为 $44-24=20$，B/G 的 residual forced floors 均为 20，所以无严格外出改善；私有 E 客户没有外部选项。若某可达 ordinary floor 只获证 19，则 $20\le19$ 不成立，当前证书不通过；不能据此断言不存在其他成功证书。

离开本讲前，全组应能不查材料讲完 BOX-TO-2 的两支，并明确区分三个动作：**找到证书、检查证书、从证书完成续局**。目前一般输入缺的是第一个动作。
