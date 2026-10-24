# payment9：可变所有权、同客户 NET 与真实 ROLE 缺口

2026-10-24。任意人数、一般有限共同目录及每份完整历史纯 SPE；Q-CAG-HALF **OPEN**。只写本个人子目录，未操作 Git、work.py 或凭据。

| 文件 | 中文用途、范围和身份 |
| --- | --- |
| [可变所有权推导](roleobstruction/fractional_ownership_extension.md) | payment9 与实际子研究员 roleobstruction 独立重构 full-O 坐标 H/r/qhat 同点变量化。p_ix k_ix<=1 保证给定所有权可初始化。任意 R owner 分割已有 round3/round5 来源，已补精确引用，不认领新 R 源机制。完整 SPE 参数族严格扩大 round8 固定 T 的付款集合，不声称解决原 LP 失败输入。 |
| [全部 reset 边 NET 独立审查](net_reset_independent_review.md) | root 提出允许删除 mandatory NEW 边、改以 current<=cV h/cA 及全部 reset-coverer edgecap 限制。独立代数、密度、一次 IC、sorted-price DP 及 OWN 合成通过。后读 root §1--6，ROW 整行退款、下游重算及旧 scalar CLIP 归属亦通过；ROW 不可继续用逐客户价格 DP。没有共同资金上界。 |
| [最后所有者及精确缺口](latest_ownership_and_payment_gap.md) | LAST 选择的嵌套 R 支持和同一 query 的 suffix 退款；不同 action 仍没有共同预算。旧 same-action uniform-reset 已去重，不认领新核。 |
| [精确命名候选检验脚本](exact_named_primal_test.py) | 只检验一般候选“每份完整 SPE 有某个最优 T 的 round8 primal 可行”在两个旧输入上的给定 optimal T 表现；不是扫描。scipy 仅选点，Fraction 核验每条线性等式、界及 ROLE；并独立重核全部历史 IC 和最优覆盖。此脚本检验旧 primal，不声称检验全部新增 NET/OWN 允许域。 |
| [冻结精确输出](named_primal_exact.json) | old52 与 old348 两个固定 optimal T 均有精确可行点。old52 只有2个 R context/client 对，old348 为0；没有足够压力，也无一般可行性含义。 |

一般推导的直接 m=5 代入：所有权、INIT/密度、条件充分性、LAST 支持和 NET 域均无条件合法；NET 最少输出使每条 source 路径最多一条 natural-to-natural 边，r<=2 时可全留 current。它们仍不支付同角色多个不同 actions，故任意五人 HALF 与一般 HALF 都未证明。

未取得新的跨 action ROLE 付款或合法目标反例。可变 p 及 NET 是更大合法选择空间，不是新增共同资金；private R 客户无所有权自由度，lambda=1 的总资金仍为原目标。下一步应寻找作用于这些变量的真实全树共同关系，或改用直接一般证明。
