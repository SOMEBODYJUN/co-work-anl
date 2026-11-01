# 真实最优查询：已有接口、信用与不能重开的失败桥

状态：父方按研究者当前问题回读原文的接续索引。不是新数学、独立完整审查或目标证明。
以下路径相对仓库根。所有关系均保留共同目录、单位客户/玩家、全部有序历史和任意平局。

## 先区分三个不同问题

固定实际路径S、覆盖C、福利W，以及达到OPT的索引m元组T（可重复）。
V_ij是actual前缀强制T_j后沿**同一原策略**的真收益；
F_ij是冻结其他actual行动的静态查询。逐项真实IC只给V_ij≤u_i，不给F_ij≤u_i。

| 命题 | 现行状态 | 原文 |
| --- | --- | --- |
| 存在最优T及排列π使Σ_i V_iπ(i)≥遗漏\|O\C\| | FALSE；两人完整SPE的唯一最优匹配均41<42 | `research/current/customer_attraction/portfolio_matching_counterexample.md` |
| 存在最优T及排列π使Σ_i V_iπ(i)≥OPT−W | 旧OPEN充分桥；上述例的净差仅1，不否定它 | `research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/new_optimal_queries/dynamic_query_credit.md` §1、§4 |
| 存在最优T及排列π使Σ_i F_iπ(i)≤W | FALSE；不同的冻结指派问题 | `research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/static_matching/optimal_static_matching_counterexample.md` |

没有在本次按需检索中找到净差真匹配的完整反例；这不是穷尽全仓或外部文献的声明。
不能因为它仍OPEN，就把再次陈述充分性或再测旧反例计作推进。

## 旧正文已经留下的精确账单

令H=O\C，I=O∩C，G=C\O，c_x为actual覆盖负载，d_x为比较索引重数。
旧正文定义显式L_i≥0，并证明

`Σ_jF_ij=OPT−W+u_i+L_i`，`Q_i=Σ_j(F_ij−V_ij)`，

所以`Σ_jV_ij=OPT−W+u_i+L_i−Q_i`。
Q可正可负；末位Q_m=0，但此前不能冻结后继。
全位置求和后，`Σ_iQ_i≤W+Σ_iL_i`是uniform真匹配的充分桥，
`Σ_iQ_i≤Σ_iL_i`则更强，给2−1/m；均尚未证明。

对单个π，令`L_π=Σ_iF_iπ(i)−(OPT−W)≥0`，
`Q_π=Σ_i(F_iπ(i)−V_iπ(i))`，则

`Σ_iV_iπ(i)=OPT−W+L_π−Q_π`。

因此某个π满足Q_π≤L_π就是原净差匹配接口。它不能靠静态最小指派结果替代。
均匀排列可在固定有限矩阵V上平均；这不交换真实玩家次序，也不随机化策略树。
完整逐客户L、signed分母差和所有层级在上述dynamic_query_credit原稿，勿另抄成新定理。

## 最小可信续局压缩已经存在，简单跨前缀比例已失败

`research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/direct_cover/README.md`
已说明：实际路径第一次偏离的子树互不相交，可以各换成达到强制入场者最小收益的
完整子SPE，保留actual自行动孩子。因此研究最坏V时可以同时取这些min，
但不能把actual自行动孩子也无条件改成min尾而仍称原路径保留。

同目录`actual_prefix_relay_obstruction.md`给完整BAAF实际路径：
`f_4=9<(3/4)f_3=39/4`。所以即使附加行动是actual前缀行动，
`f_r(b,T)≥(r−1)/r f_(r−1)(b+A,T)`仍假。它没有否定净差匹配。

`research/workspaces/customer-attraction/R-92e1d0d449184e2caefa6f4fff13a7db/global_coverage/README.md`
已记录7份现成完整策略锥、66个指定最优支持的净匹配阴性重测并停止；
其中2次浮点端点未通过有理恢复，其余也未恢复全锥对偶。不能重跑同批诊断并记新信息。

该页还保留actual-only客户G的真实分支份额式：未来G利润等于原后缀G利润
加旧前缀G损失减新遗漏信用。旧前缀损失不能丢掉，也不能每个互斥枝各领一份G。

## 真正可复用的修复器及承重前提

`research/workspaces/customer-attraction/R-3bc48d936f044f12b0fa743482ff5eb0/credible/heterogeneous_prefix_repair.md`
已给同人数共同Cartesian目录修复器，要求目标尾本来就是真正完整子SPE。
设各前缀的可信child最小值缺陷为delta_i，R=Σdelta_i、D=maxdelta_i，则

`OPT_new−2W_new=OPT_old−2W_old−(2R+D)`。

这不是actual-node后悔支付。只有旧正坏差严格超过2R+D才给目标反例，尚无这样的输入。
`research/workspaces/customer-attraction/R-a4671b9ccb664300b43d3216ce45c934/security_review/projection_rent_repair_diagnostic.md`
解释：删客户后实际后悔小不控制可信child缺陷；旧末位非BR不能靠完整Cartesian保险修。
这些均是恢复已有机制，不给研究者限定后续方法。
