# 本轮relay精确状态

Q-CAG-HALF仍OPEN；以下均为个人资产，未获外审或新颖性认证。

| 身份 | 状态及精确范围 | 依据 |
| --- | --- | --- |
| B5-RELAY-PROJECTION-v1 | 一般解析推导，root已独立攻击通过（见../parent/relay_kernel_review.md）。任意m、任意同一z总重τ≥1，τδ−τs精确抹去真实D；保留S/Z/E/F后的Debt满足`Debt−threshold=m(C(z)−2W)+ΣK`、K≥0。 | projected_relay_debt.md §§1—3 |
| B5-RELAY-SPE-NONINJECTIVE-v1 | 已逐有序历史解析核验且独立实现Fraction审计。3人8客户两个完整SPE，同一最少主题最优组合、实际路径及全部实际节点末回复相同，中间负载、真实D和离轨W不同。非half反例。 | projected_relay_debt.md §4；39项比较/策略 |
| B5-CLONE-CHAIN-v1 | 内部研究员一般精确恒等式，父研究员已核对(1)—(6)；独立外审未做。真实克隆节点slack非负，但跨角色差不能删除。 | algebra/clone_chain_identity_and_boundary.md |
| B5-CLONE-DRIFT-UNBOUNDED-v1 | 一般解析推导，root已独立重构方盒/过载引理及调和求和通过。两个单位客户、m=2q、每个完整SPE、同一最少最优z=A+B；原始Drift与CloneSlack各无界但差为1/(2q)。不存在该Drift全链总量≤固定常数W的统一预算。 | clone_drift_unbounded_family.md |
| B5-RELAY-GLOBAL-PAYMENT | OPEN。尚未从内部真实节点构造带有可控根预算的非负全链运输；既有强充分支付也未证普遍真假。 | 本目录README及上述各稿末节 |

禁止提升：有限审计不证明一般half；净债务投影不证明一般正面机制不可能；两客户无界族不否定保留CloneSlack、L、S/Z/E/F及m相关阈值的最终支付。
