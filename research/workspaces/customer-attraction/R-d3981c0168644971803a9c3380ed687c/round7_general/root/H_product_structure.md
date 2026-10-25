# H 的产品次可加与三名以内剩余者的精确可加

2026-10-25。父方从本轮共同价格定义推导一般产品关系；aggregate 已依据含证明思路的精确合同独立核查通过，未读本作者全文；见 [独立审查](../aggregate/H_product_structure_review.md)。不是 H(1) 一般非负证明，也不是 half 证明。signed 已独立记录 r=3 精确可加；本页把它与任意 r 的不等式及末两人边界统一。

固定 r≥2、同决策次序、合法固定背景/有序前缀的有限不交组件。产品目录必须完整 Cartesian。组件当前强制 A_t 后，下一角色真实门槛为 theta_t(A_t)，产品对应门槛为 theta_P(A)。H 使用**全部真正 grandchild SPE**叶（下一角色动作 B 已被强制，不要求 B 在父节点最优），定义

    H_h(tau)=max_A min_(B,z∈R(h,A,B))
                [u_i(z)−tau(u_(i+1)(z)−theta_h(A))]。

所有 tau≥0、所有组件与产品均用同一 tau。由产品完整SPE拼合，

    theta_P(A)≤Σ_t theta_t(A_t)。

对固定 A，产品的真正 grandchild 集包含每个联合 B 下的组件 grandchild 之积。因此

    min_joint [d_P−tau v_P]+tau theta_P(A)
       ≤Σ_t min_component[d_t−tau v_t]
                      +tau Σ_t theta_t(A_t)。

tau 非负用于后一不等式。对全部联合 A 取最大，利用完整 Cartesian 选择分解，得到

    H_P(tau)≤Σ_t H_t(tau)。                        (SUB)

该式不假设任意产品 SPE 可分解，只用产品策略提供可选子集。

若 r=2，B 后已经终端，所有 joint 叶正好逐坐标分解，下一角色就是末位，其最高利润也可加，所以上面两处不等式均为等式。

若 r=3，B 后只有最后一名决策者。某个 joint 末位动作是 BR，当且仅当每坐标都是该坐标 BR；否则单改一个非最优坐标即可严格改善。全部 BR 集恰为坐标 BR 集的积。在固定 A 后，下一角色的 max_B min_lastBR 利润于是也精确可加，故同样得到

    H_P(tau)=Σ_t H_t(tau)   (r=2或3)。             (ADD)

固定背景只改变数值，不改变这些可加与完整最优性的判断。全部平局都保留；未规定统一匿名tie rule。

r=2 有一个容易混淆的定义：R(h,A,B)是强制最后动作 B 后的终端，含非BR的B。只有总下一利润≥Σtheta的约束才筛出BR。故原 H_t(tau) 不必逐 tau 等于 M_t；其 supremum 才给真实末两人门槛。不能为了证明(ADD)先偷偷删掉菜单中的非BR B。

(ADD)说明在固定 tau 处，r≤3 的复制/异质产品不能把非负 component H 变成负 H；r=2 时真实 M 精确可加，Psi=M，因此此处没有异质共同 sup 的严格下降。r=3 的异质组件可因共同 sup 与分别 sup 不交换而严格改善；同型 N 复制的 Psi_N=N Psi，真实整数 M 的下降则可来自凸化/整数池化，不能把两种原因混称。本轮真实例分别核了这些层次。r≥4 时保留(SUB)，真正非分解 grandchild SPE 可使不等式严格；本页没有构造严格负 H 例，也不声称任意 r≥4 都有严格下降。

同一一般关系用于 m=5：最初 r=5、接着r=4的节点可能使用额外 joint grandchild；末三人以内的 H 单靠继续产品化没有新的逐 tau 负供体。它没有证明所有 H 非负，更没有支付 B+C。应找真正可实现的深层菜单或一般反向金额，不继续用三人 M 节省误当 H(1) 节省。
