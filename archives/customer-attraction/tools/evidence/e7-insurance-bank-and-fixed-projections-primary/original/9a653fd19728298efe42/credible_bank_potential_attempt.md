# 全树旧人银行势：末步关系与一般单步的明确失败

2026-10-25。独立尝试草稿。对象为原 Q-CAG-HALF：任意人数、有限共同目录、单位客户与单位玩家，允许空主题、重复行动及全部有序历史依赖纯 SPE。**没有一般 half 证明；全 2 统一价格及 exact-M 累计候选仍 OPEN。**

本文没有把下包络的等价表示当作付款。它记录一个有具体终端条件的势候选，并已用已有合法完整 SPE 实例否定其一般单步式。父方建议用旧根总税反例攻击，实际击穿了两个在轨边。

## 1. 精确状态和候选

固定总人数 m。令 b 为长度 k<m 的合法有序前缀的主题计数，r=m-k。记 R(b) 为该前缀后所有真正完整历史纯 SPE 可实现的终局计数集。用计数只描述全集，不要求同计数的指定续局相同。

记 U_a(y) 为终局 y 中选择主题 a 的单个玩家的收益。定义

    V(b,r) = max_{r个合法主题补全 q} W(b+q),
    E(b,r) = min_{y in R(b)} sum_a b_a U_a(y),
    Psi(b,r) = V(b,r)-E(b,r).

E 是固定旧玩家在真正 SPE 后继中的最小**总**收入。它既不等于逐旧玩家最小收入的和，也不能在某个祖先终局条件限制下重算。每个状态的 R 均为未附加祖先承诺的完整子 SPE 全集。

令 M(b,r) 为该状态的真实当前收入下包络，即

    M(b,r)=max_A min_{y in R(b+e_A)} U_A(y).

根处 Psi(0,m)=OPT_m；满历史处 Psi(b,0)=0，因为 V=W(b)，旧人总收入也等于 W(b)。因此以下精确单步式若对每个状态和每个合法 A 成立，就会沿任意形式路径望远镜给出 sum_i M_i >= OPT_m/2：

    Psi(b,r)-Psi(b+e_A,r-1) <= 2 M(b,r).        (BANK-EDGE?)

这是一个充分的全树付款候选，不是其存在性的证明。特别地，A 不必是当前可延伸为 SPE 的动作；E_child 的最小终局与 E_parent 的最小终局通常不同，不能免费将一个最小者延伸为另一个。

另一种等价写法有助于解释，但不增加强度。令 C(b,r)=V(b,r)-W(b) 为最多 r 个主题可新覆盖的人数，并令

    D(b,r)=max_{y in R(b)} sum_{x:b_x>0} (c_x(y)-b_x)/c_x(y).

则 E=W(b)-D，故 Psi=C+D。D 是真实 SPE 能使全部旧人损失的最大总收入，等于后继在已覆盖客户上获得的总份额；不是任意静态补全的最优利润。

## 2. 最后一步确实成立

此段对任意合法背景 b 普遍成立，但只证明 r=1 的 BANK-EDGE，不承担更早步。

令 n(T)=|T\setminus union(b)|，n_max=max_T n(T)，末位收益 f_b(T)=sum_{x in T}1/(b_x+1)。令 M=max_T f_b(T)，并令 n_min 为所有末位最佳回复中的最小 n(T)。此时

    V(b,1)=W(b)+n_max,
    E(b,1)=W(b)+n_min-M,
    Psi(b,1)=n_max-n_min+M <= 2M.

最后一个不等式只用 n_max<=M 及 n_min>=0。任何满历史孩子的 Psi 均为零，所以 r=1 对全部合法 A 成立。推导保留所有最佳回复和平局，没有把末位的某个指定回复借给其他分支。

## 3. 旧根总税实例严格否定一般单步式

来源为已有 [root_tax_counterexample.md](../../../../current/customer_attraction/root_tax_counterexample.md) 和 [单位客户输入](../../../../../examples/customer_attraction/root_tax_failure.json)。该例 m=4，共同主题 A,B,C,D,E,F，客户兴趣及重数为

| 兴趣 | 数量 | 兴趣 | 数量 |
| --- | ---: | --- | ---: |
| A | 12 | B | 8 |
| C | 4 | D | 8 |
| AE | 6 | AF | 6 |
| CE | 3 | CF | 3 |
| AEF | 6 | BEF | 2 |
| CEF | 1 | DEF | 2 |

旧自足证明给完整 SPE：前三人在所有历史选 A；末位最佳回复，平局优先 F>E>D>C>B>A。实际路径 AAAF，收益 (9,9,9,11)，W=38，OPT_4=61。该完整策略的真实性由来源正文证明，不由本势候选假设。

本候选所需的值如下，kA 指 k 位旧人都选择 A：

原始数值与来源绑定保存在 [credible_bank_edge_counterexample.json](credible_bank_edge_counterexample.json)。该文件保存相关状态的完整 R 集、极值实现者，以及原输入、原 259 节点完整策略证书、原证明正文和规范求解器的 SHA256；未改写原冻结证据。

[reproduce_credible_bank_edge.py](reproduce_credible_bank_edge.py) 直接读取该旧输入，调用规范 `ExactSPESolver` 重建本 JSON 的 R、V、E、M 与来源 SHA，并断言以下两条 `19>18`。默认结果只发 stdout；可加 `--check-reference` 核对保存的全部字段。运行命令：

```sh
python research/workspaces/customer-attraction/R-e7c3c9a51d38458aa551eec469e04cf2/dual/reproduce_credible_bank_edge.py --check-reference
```

| 状态 | r | V | E | Psi | M |
| --- | ---: | ---: | ---: | ---: | ---: |
| 空 | 4 | 61 | 0 | 61 | 9 |
| A | 3 | 61 | 9 | 52 | 9 |
| AA | 2 | 51 | 18 | 33 | 9 |
| AAA | 1 | 41 | 27 | 14 | 11 |

这些 E、M 值可直接理解：在任意包含 A 的四人终局中，只要不是 AAAA，选择 A 者收益至少 9；AAAA 的末位不是最佳回复，因其选 A 只得 15/2，而 C、E、F 都给 11。因此从任何固定 kA（1<=k<=3）出发的子 SPE 中，每位旧 A 玩家至少 9。旧完整策略在这些前缀实现 AAAE 或 AAAF，A 玩家恰获 9，故 E(kA,4-k)=9k。

在空、A、AA 三个节点，强制当前 A 后的任何真实子 SPE 均使其至少得到 9；旧完整策略又实现当前恰得 9，所以 M=9。AAA 后末位的最大值为 11。

V(A,3)=61 由 B,C,D 补齐全部客户。V(AA,2)=51：在 A 外，任意两个主题最多由 B+C 或 C+D 覆盖 21 人；E、F 单独在 A 外各覆盖 8 人，其他组合不能更大。V(AAA,1)=41，因为 C 在 A 外覆盖 11 人且为最大者。

于是两条合法且实际到达的边均有严格违例：

    Psi(A,3)-Psi(AA,2)=52-33=19 > 18=2M(A,3),
    Psi(AA,2)-Psi(AAA,1)=33-14=19 > 18=2M(AA,2).

这不是对 Q-CAG-HALF 的反例。该例仍有 2W-OPT=15；也不反驳 exact-M 任意路径累计候选，因为沿这条实际路径 sum M=9+9+9+11=38。它只证明这个具体 Psi 不能逐边无债付款。早期和末期的剩余信用确实支付了这里两个各为 1 的局部缺口；本稿没有证明任何普遍的跨边支付法。

## 4. 自然的新覆盖修正也不能逐边闭合

尝试取 N(b,r)=min_{y in R(b)}[W(y)-W(b)]，并改为 Psi_plus=Psi+N/r（r>0），终端取零。这个修正会在上一例的两个 A 边提供部分末期信用，但一般单步仍为假。

已有 [tax_bridge_counterexample.md](../../../../current/customer_attraction/tax_bridge_counterexample.md) 的三人星形例即可解析击穿：中心 B 覆盖 9 客户，三个两两不交叶 A,C,D 各有 2 私有客户与 3 个 B 共有客户。全历史全选 B 是完整 SPE，每人收益 3，OPT_3=15。任何玩家至少能由 B 保证 3，故根最小 SPE 福利为 9，M_root=3。

根 Psi=15，N=9，故 Psi_plus=18。固定首位 B 后，最多两主题补全与 B 的总覆盖为 13；全部真尾 SPE 中旧 B 收益至少 3，且全 B 尾实现 3，所以 Psi_child=10。全 B 尾无新增覆盖，故 N_child=0，Psi_plus_child=10。因此

    Psi_plus(root)-Psi_plus(B)=8 > 6=2M_root.

只否定此明示修正的逐边式，不否定某种非局部信用或主目标。

## 5. 全树对偶的准确停止点

原全树真实 IC 仍可写成完整策略锥的非负对偶付款。若用 harmonic potential P(y)=sum_x H_{c_x(y)}，则每条当前玩家 i 的真实比较亦恰为

    P(z_h)-P(z_{h,A}) >= P(z_h^{-i})-P(z_{h,A}^{-i}).

两边删除的是各自真实分支中的当前玩家；被删后的终局无需是任何子 SPE。这个恒等式没有自动消除跨分支删除项，不能把它当作闭合的势降。

本轮新检查的 BANK-EDGE 候选已经明确失败；不继续扩大有限阴性。剩余真正任务仍是给所有真实分支的一份可支付跨边信用，或直接构造原策略锥的通用非负付款系数。本稿未完成该任务。
