# 文献条件核验与跨领域机制工作台

2026-10-21。主目标仍是 Q-CAG-HALF；本文目录内的候选、反例和数值探索不改变主命题 OPEN 状态。只修改本目录，不改共享正文、账本或凭据。

## 原始来源核验

本次已实际在线打开以下一手材料；未检得一般可导入定理不等于不存在证明，也不声称研究新颖性。

| 来源 | 本次可核查事实 | 对一般共同目录完整历史 SPE 的边界 |
| --- | --- | --- |
| [Deng 等，arXiv:2307.07174v2](https://arxiv.org/html/2307.07174v2)，§6 | 当前 arXiv 记录仍为 2024-10-10 的 v2；该版仍将超过两人时上界 2 写为猜想。 | 论文未解决本轮一般人数目标；本文没有据此作世界文献不存在/优先权判断。 |
| [Vetta，FOCS 2002](https://web.mit.edu/6.454/www/www_fall_2004/gametheory/VettaNashEquilibria.pdf)，§2.3、§3 | 单调次模社会效用、个人收益至少等于删除该玩家的社会损失、总个人收益不超过福利，给静态 Nash 半福利。 | CAG 的主题行动博弈满足这些条件；SPE 终局未必是该静态游戏的 Nash。见既有非 PNE 证书；下面进一步否定与最坏 PNE 的福利比较。 |
| [Bachrach–Syrgkanis–Tardos–Vojnović，arXiv:1307.2537](https://arxiv.org/pdf/1307.2537)，Definition 1、Theorems 3,7 | 单调参与和 marginal-contribution 条件给 (1,1)-coalitional smoothness；Theorem 3 对 strong Nash 给半福利。证明逐个选出联合偏离的阻挡成员并重新排列。 | SPE 不允许固定其他人的行动后作联合偏离，也不提供强 Nash 的阻挡成员。不能导入。该论文全文检索 sequential 未匹配。 |
| [Konda–Chandan–Grimsman–Marden，arXiv:2406.17791v1](https://arxiv.org/pdf/2406.17791)，§I–II | Round-robin best response 的每次更新相对固定的其他玩家行动作最优反应。 | 所谓 sequential updates 是 myopic 动态，非预见真实后继策略的一次 SPE；令轮数 k=1 不修复时间模型。 |
| [Groenland–Schaefer，arXiv:1804.07107](https://arxiv.org/pdf/1804.07107)，Theorem 20 | Extension-parallel 对称网络拥塞游戏每个 SPO 的 egalitarian social cost 最优。 | 其路径结构有承重作用；任意集合主题未必可表示成该类的共同路径。既有层级关联类已用到相关桥，不将其外推到无界目录。 |

Shapley 分配只是逐客户 1/c 的合作值归属：在随机排列中每位覆盖者成为首位的概率为 1/c。它没有把强 Nash 或静态 smoothness 的偏离稳定性赋予顺序 SPE。

把完整行为策略当作静态行动也不能自动复用 valid-utility 条件。具体定义级例子：共同目录含空主题 E、A={a}、B={b,c}，两玩家；第二人的行为策略在首人 A 后选 B，在 E 后选 E。首人选 A 时福利 3、个人收益 1；首人换成 E 时福利 0。策略形式中的“参与边际”是 3，超过其收益 1。这个策略组合无须是 SPE，因为 valid-utility 假设须对全部静态策略组合成立。此例只攻击这一种自动提升，没有否定存在其他正确提升。

## 新计算反例：SPE 的福利可低于所有静态纯 NE

尝试过的更弱桥是

> 每个完整纯 SPE 的福利，至少等于同一主题行动博弈的最坏静态纯 Nash 福利。

**该桥为假。** 25 名不同单位客户、3 人、4 个共同主题 A,B,C,D 即可。类型用二进制 mask 表示喜欢的全部主题；位 0,1,2,3 对应 A,B,C,D。

| 喜欢主题 | 客户数 |
| --- | ---: |
| A | 3 |
| B | 8 |
| C | 1 |
| B,C | 1 |
| A,B,C | 3 |
| A,D | 2 |
| C,D | 3 |
| A,C,D | 2 |
| B,C,D | 2 |

第一人选 D；第二人在首人 A,B,C,D 后分别选 B,D,B,B。第三人的完整规则为：

| 前两行动 | AA | AB | AC | AD | BA | BB | BC | BD | CA | CB | CC | CD | DA | DB | DC | DD |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 第三人 | B | C | B | B | C | C | A | B | B | A | B | B | B | B | B | B |

根各行动的真实后继收益按 A,B,C,D 顺序为

\[
(7,20/3,15/2,23/3),
\]

所以 D 严格最优。第二人各行真实偏离收益如下，指定行动逐行达到最大：

| 首行动 | A | B | C | D |
| --- | ---: | ---: | ---: | ---: |
| A | 9/2 | 21/2 | 15/2 | 6 |
| B | 7 | 6 | 15/2 | 23/3 |
| C | 7 | 21/2 | 5 | 31/6 |
| D | 13/2 | 20/3 | 37/6 | 25/6 |

第三人所有 16 行的四个行动查询值，完整列在 `static_lower_envelope_exact_audit.json`；指定行动全部最优。因此 21 节点的策略是完整纯 SPE，实际路径 D,B,B：

\[
u=(23/3,20/3,20/3),\qquad W=21.
\]

枚举全部 64 个有序静态行动组合，纯 Nash 恰好是 A,B,C 的六个排列，覆盖均为 25。每个非 NE 均保存了一个严格改善的玩家、行动及精确改善量。A,B,C 已覆盖全部 25 名客户，故 OPT_3=25。

此例只否定相同实例内的福利下包络比较，远未否定半覆盖：2W−OPT=17。根的 on-path 次序不同不会改变计数福利，但本文固定的是完整证书，不默认计数平局匿名。

计算来源与独立性：`static_comparison_probe.py` 用全 SPE 计数递推找到候选，规范 `ExactSPESolver` 再认证该终局并输出完整证书；`audit_static_lower_envelope.py` 不导入规范模型或 solver，展开全部 25 名单位客户，逐历史核验 84 个含自身动作比较，再枚举 64 个静态终局。没有全目录/客户数最小性、新颖性或外审声明。另一队员独立找到 26 客户同类证书，相互印证的是桥失败，不是该例的最小性。

重算：

```sh
python3 research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/literature_mechanism/audit_static_lower_envelope.py
```

## 正在攻击的一般候选

换掉逐人安全值或 max 残余主题后，考虑只支付**总最优覆盖缺口**：

\[
\forall i\qquad m u_i\stackrel{?}{\ge}\operatorname{OPT}_m-W.
\tag{GAP}
\]

求和可得 W≥OPT−W，所以 GAP 若成立足够解决半覆盖；它比原福利结论强，目前**没有证明**。已有逐人 v_m 保底和 max 残余反例均不直接否定它。末人版本可直接证：令 C 为实际覆盖，对任意最优比较元组 T_1,…,T_m，末人改选 T_j 可全额得到 T_j\C；因此 m u_m≥∑_j|T_j\C|≥OPT−W。困难只在早期玩家真实后继会稀释这些缺失客户。

`gap_floor_probe.py`、`gap_sparse_probe.py` 作有限全 SPE 终局攻击。密集随机样本常已 OPT=W，证据很弱；稀疏下界邻域探索更相关，但仍不能替代证明。`gap_cone_lp.py` 在采样完整策略锥内线性优化 OPT−W−m u_i，并对任何正候选要求精确有理恢复和逐历史复验。仍须覆盖新策略，而不是把固定锥的数值零反例误称定理。

下一步：优先寻找 GAP 的真实可信反例或跨节点支付证明；若失败则保留其准确边界，继续主半覆盖，不把加强桥当成主目标本身。
