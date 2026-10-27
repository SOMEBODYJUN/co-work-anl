# 七极大、六人：混合 singleton/dense 的条件性半覆盖

**状态：条件性精确证书，个人工作区资产；不是无条件 Q-CAG-HALF-6。**

本页把七极大六人的无 singleton 证书向 mixed incidence 推进了一步。它给出一个可直接检查的“dense 客户质量足以支付非最优 singleton 块”的充分条件，并精确保留完整历史纯 SPE 量词。它不是把局部行族的 Farkas 不可行误报成目标反例。

## 精确对象与结论

设目录恰有七个 distinct inclusion-maximal coverage sets B_0,...,B_6，实际完整 SPE 根路径的最后一个真实最大行动重标为 B_0。对每个客户令 I⊆{0,...,6} 为包含它的极大主题指标集，令 x_j 为 incidence 恰为 {j} 的客户数，并令

H = #{x: |I_x|≥2}.

任何六个极大主题的并集至多六个目录动作可实现；由于任意内部主题包含于某个极大主题，最优六主题覆盖为

OPT_6 = U - min_{0≤j≤6} x_j,   U = |∪_{j=0}^6 B_j|.

取 o∈argmin_j x_j。定义

δ = 15591089/238321440,  d_0 = 7905391/238321440,  d = 34758511/238321440,
p_0 = 111255329/238321440,  p = 84402209/238321440.

若

δ H + p_o x_o ≥ 1_{o≠0} d_0 x_0
                  + d Σ_{j∈{1,...,6}\{o}} x_j                         (MS)

其中 p_o=p_0 当 o=0，否则 p_o=p，则该完整 SPE 满足 2W≥OPT_6。

这包含已有的“singleton 只出现在被省略极大主题”情形（右端为零）；若所有客户均为 dense，亦自动成立。

## 证书行与为何适用于 mixed 类型

沿用 dense 七极大六人证书的合法全历史行：

* M_t=u_t-B_t（t=0,1,2,3），其中 B=(1/21,2/37,1/16,2/27)；
* 六个末位真实最大主题 BR 行 L_j（j=1,...,6）；
* 六个真实两人税行 T_{0j}（j=1,...,6）。

非负乘子分别为

(207/355, 417/710, 253/426, 133/213), 8/71, 7/71.

M_t 的合法性在 singleton 列上来自七极大 mixed-floor 的 private 系数：在 t=0,1,2,3 处它们分别为 1/7,7/74,1/12,1/12，均不小于对应 B_t；在 dense 列上 B_t 正是 shared 系数。故每个实际完整 SPE 都有这些行的非负 slack。末位 BR 与两人税行直接来自真实离轨比较，不冻结偏离后的后继。

固定 comparator 为六个极大主题中除 B_o 外的六个集合。令 J 为实际根路径中覆盖该客户的玩家位置集合；末位最大行动给出 1_{5∈J}=1_{0∈I}。逐客户展开

W - (U-x_o)/2 = Σ_q λ_q S_q + Σ_x r_o(I_x,J_x).                    (1)

audit_mixed_singleton_condition.py 精确枚举了全部 I≠∅ 与全部前五位 membership mask，共七个 o 的完整 literal 域。结果：

* 对所有 dense 列 |I|≥2，r_o(I,J)≥δ；
* 对 singleton I={o}，r_o≥p_o；
* 对 singleton I={0}, o≠0，r_o≥-d_0；
* 对 singleton I={j}, j∈{1,...,6}\{o}，r_o≥-d。

将这些逐客户下界代入 (1) 正好得到 (MS)。因此 (MS) 下右侧所有项非负，目标 half 成立。

## 可复现范围与边界

在仓库根运行：

    python3 research/workspaces/customer-attraction/R-c499e3814bbe4743b298e230b37ddca1/subagent_e/mixed_singleton_condition/audit_mixed_singleton_condition.py

脚本使用 Python Fraction，枚举 7·(2^7−1)·2^5 个列并核验常数：δ 的最小 dense 余项正好在 I={0,1} 的一个列取得；五个 singleton 余项下界也逐一精确命中。

这是对指定行组合的条件性推进，不是对 unrestricted 七极大六人的证明：当 (MS) 失败时，证书出现负 singleton 余项；这只表示本证书没有支付该混合质量，不是原模型反例。完整历史 SPE、重复/空主题和任意历史平局都保留在行的来源中。当前仍缺一个无质量条件的 singleton 跨枝共同付款，或完整原模型反例。
