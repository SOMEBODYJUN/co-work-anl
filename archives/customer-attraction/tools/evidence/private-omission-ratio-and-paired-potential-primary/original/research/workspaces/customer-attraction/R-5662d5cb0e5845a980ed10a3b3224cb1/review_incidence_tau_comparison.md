# incidence-tau 与现行分数覆盖预算：范围包含而非新 half 类

状态：父方原文比较；research_6首先指出包含关系。不是对同期作者定量式的反证，
不是新福利定理，也不升级 Q-CAG-HALF-6。

同期正文为
`research/workspaces/customer-attraction/R-c499e3814bbe4743b298e230b37ddca1/research_d/incidence_tau/README.md`。
现行正文为`research/current/customer_attraction/fractional_cover_path_budget.md`，特别是§1、§3、§5。

在极大覆盖B_j上，一个客户的覆盖约束只取决于其非空incidence I。
singleton的约束alpha_j≥1与非singleton的Σ_{j∈I}alpha_j≥1
合起来正是覆盖整个目录并集U的普通分数覆盖LP。允许内部子主题不降低这个最小值：
把每个子主题的权重转给任一包含它的合法极大主题，不增总重、只增加覆盖；
反方向极大主题原本就是合法动作。所以tau_inc=tau_U。

既有路径预算允许比较集C为U，而不限于六主题最优并集O。恰六人时

`W≥U[1−∏_{r=1}^6(1−1/(r tau_U))]`。

现行结果已证明tau_U≤7/2时half（对m≥5通用），因此tau_inc≤149/50的
half条件被它严格包含。更直接地，现行§5的解析式(17)证明乘积下界总不弱于
`U Σ_{r=1}^6[6+(tau_U−1)r]^{-1}`。在tau=3时后者2509/5040<1/2，
不表示这一目录类尚未证half；乘积界早已覆盖它。

应保留的区别：同期定量式为
`W≥c+(U−c)Σ_{r=1}^6[6+(tau_inc−1)r]^{-1}`，其中c是极大主题公共核。
现行上述无core乘积式没有自动给出同样的加法core信用。
也不能删除core后假定原完整SPE仍为新游戏SPE。因此本比较只撤掉“新half范围”
的理解，不否定该core式、其证明或相对原8/3候选的数值加强。

这些边界已回传全体研究线程及原作者，避免继续重建较弱的tau-only half条件。
