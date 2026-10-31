> 统一候选编号、当前状态和本轮最终判断以[候选比较](../BATTLE.md)为准；本文保留来源与推导过程。

# 固定 heavy 残差：三个可审核结果

日期：2026-10-20。独立研究者：boss37 第二轮 fair-parameter。本文是重新选题的实质试攻资产，不是一般多重图 FPT 的证明。所有 `Proof` 是本文独立推导；是否新颖须另行审查。来源身份遵守 A 作者明确原问题 / B 作者建议 / C 我们派生。

## 0. 精确残差模型

输入整数 `s_i>=0`、`h_ij>=0`；s 是已固定边给 i 的价值，h 是 i 对已固定给 j 的边的价值。每对 i,j 有 `m_ij>=0` 条未定向单位边，均对两端价值1；`x_ij` 表示其中分给 i 的条数，故 `x_ij+x_ji=m_ij`。所有剩余边必须定向，不许给非端点。

令 `R_i=s_i+sum_j x_ij`。EF 恰好等价于

    R_i >= h_ij + x_ji = h_ij+m_ij-x_ij       (i != j).

这个等价来自 additivity 与 endpoint support，无近似、无分数变量。没有剩余单位边的 pair 仍有约束 `R_i>=h_ij`。

## 1. FP-COUNTER-BALANCE-v1：普通顶点内部全部平分不保可行

**Objects/domain**：5 顶点对称非负整数 additive multigraph；heavy 定义为某端点价值至少2，k=1。

顶点依次 v,u,w,z,t。v-u 有唯一 heavy 边，两端价值87；u-w、w-z、z-t 各有100条单位平行边；无其他边。

一个 EF orientation：heavy 给v；u-w中87给u、13给w；w-z中74给w、26给z；z-t中50给z、50给t。自身收益依次为

    (87,87,87,76,50).

逐个比较只有如下非零他人估值：v看u为0；u看v为87、看w为13；w看u为87、看z为26；z看w为74、看t为50；t看z为50。均不超过自身收益。

heavy 必须给v，因为若给u，则叶v自身收益0却对u估值87。

现在强制所有两端均非 heavy endpoint 的 pair 平分，即 w-z 与 z-t 各50/50。设u-w给u数量a。则w自身收益为 `100-a+50=150-a`；w不妒忌u要求 `150-a>=a`，即a<=75。可是u不妒忌v要求a>=87，矛盾。

**Status**：完整反例证明；`probe.py` 验证精确不等式。它仅击穿“普通顶点内部所有平行包先全平分再求特殊端点”的具体归约，不否定保留普通组件完整边界函数的压缩，也不否定一般 FPT。

**机制**：普通组件可沿路径传输可分配收益，传输量随离边界距离变化；只记奇偶丢失容量。这里内部 w-z 包必须向w偏置至少74条，差额24，绝非1条奇偶修补。

## 2. FP-FOREST-THRESHOLD-v1：单位支持为森林时的精确阈值 DP

**Theorem（独立证明）**：对0节的任意非负整数 s,h，若简单支持图 `H=({1,...,n}, {{i,j}:m_ij>0})` 是森林，则可用多项式位复杂度判定完整残差可行性并构造解。若 sparse h 已给，算术操作数可按 O(n+|supp h|) 实现；附带的研究验证代码为简洁采用 O(n²) 扫描。multiplicity 可二进制编码，算法无需逐条枚举平行单位边。

**State**：任意定根。节点i的父亲p，子节点集合C。令 `L_i` 是父子包中分给i的最小数量，使i的子树能全部满足EF（i对父亲的EF也包括在内，但父亲自身的EF留上层）。可扩展输入集合恰好是整数区间 `[L_i,m_ip]`；超过包大小表示不可行。

注意 h 允许连接不同树、树上非邻接顶点：它已固定，影响只是常数比较阈值，未产生变量耦合。

**Monotonicity**：保持子树内部方向，若把父包更多单位边分给i，则i收益上升，i对父亲的估值下降，其对其他顶点估值不变；所有严格后代约束不变。因此子树可扩展性对该输入单调向上。

对子节点c已知L_c，父i可从i-c包取得的最大数量为

    U_ic=m_ic-L_c.

如有L_c>m_ic，直接不可行。取所有子包 `x_ic=U_ic` 同时最有利于i：它增加i收益、减少i对c的估值；各子树仍可扩展。因此检查给定父输入x时，无需在子包之间做权衡，只须取所有上限。记 `S_i=sum_c U_ic`。

i对父亲要求

    s_i+x+S_i >= h_ip+m_ip-x,
    x >= ceil((h_ip+m_ip-s_i-S_i)/2).

i对子c要求

    x >= h_ic+m_ic-U_ic-s_i-S_i.

i对其余j（既非i、父亲，也非子）要求

    x >= h_ij-s_i-S_i.

故L_i就是0及上述所有右端的最大值。这给出完整归纳证明：必要性由任意可行子包数量不超过U得到；充分性取全部U并接上子树见证。根没有父输入x，按x=0检查其余所有条件。自顶向下把每个孩子恰给L_c条父包边即可重构。

**Corollary**：任意 additive multigraph，在 Observation3 安全预处理后，若所有剩余非heavy单位边的简单支持为森林，则枚举heavy方向可在 `2^k poly(input-bit-length)` 时间解 EF orientation。heavy 支持本身可有任意结构、与单位边同pair也允许。此处 k 为原实例heavy边总数的上界。

**最强异议**：这个单接口单调阈值 lemma 可能只是常规树DP，单独很难支撑完整文章；它的真正作用是反驳“只能做奇偶”并提供可迁移接口。后续须处理环块、多个接口、matching/flow式整体消元或得到参数界，不能把该保底包装成已解原题。

**Verification**：`python battle_fair_parameter/probe.py`；seed 37042026；n=1..7、每n600个随机森林，总4200；m=1..4，s/h=0..7，h允许非边pair任意方向；与全部整数x枚举比较，可行2395，差异0。此计算检查程序，不替代上述一般证明。

## 3. FP-CHARITY-SIMPLE-v1：simple graph 的 Min-Charity EF 可3^k求解

**Theorem（独立证明，尚待根部或同行复核）**：输入simple loopless graph，nonnegative integer additive endpoint valuations以二进制编码，k为至少一端价值>=2的heavy边数。可以在 `3^k poly(n,m,bit-length)` 时间构造删除边数最少的EF partial orientation。

同一证明也支持每条边任意非负二进制编码 donation cost（最小化删除成本）；后文实验只核删除边数。它不直接解决一般多重图F01。

### 3.1 安全预处理与branch

两端值0边总可保留；单端值0边总可保留并给正价值端点：这样只增其自身收益，另一端对这条边估值0，不会产生新妒忌。nonnegative donation cost保证总保留不劣。把这类边贡献记入s。

其余边两端均正；非heavy均为(1,1)。每条heavy枚举“给第一端、给第二端、删除”三种状态。固定此branch后，计算s_i及

    q_i=max({0} union { i对所有已保留、分给其他端点的heavy边的价值 }).

simple保证不同heavy不会在同一pair相加，也保证heavy pair不会再有单位边。单位支持图H固定，不随branch改变。每个H分量C若有某i满足s_i>0或q_i>0，称C为anchored。

### 3.2 Anchored 分量：部分单位解可补成全单位解

**Lemma**：固定heavy branch。对anchored单位分量C，若有EF partial orientation，则存在EF orientation保留C所有单位边，且heavy状态不变。

**Proof**：任取该partial解。若s_i>0，则i自身收益>=1；若q_i>0，则EF迫使其自身收益>=q_i>=1。因此C至少有一个收益正的顶点。记当前收益>=1的顶点为active。

若有未保留单位边两端都active，把它给任一端：该端自身收益上升；另一端对新收件人的可见估值至多从0升至1，因为该pair在simple图里只有这一条边，且不存在heavy重合；另一端自身收益已经>=1，所以仍EF。

若有单位边连接active i与inactive j，则它在partial解中尚未分配：给i会使j妒忌；给j会使j变active。现把边给j。j收益变为1，它此前收益0且EF，故对所有既有他人包估值0；i自身收益>=1，看到j的新单位物值1，亦不妒忌。其余顶点不受影响。于是active沿H的连通性扩张到整个C，随后所有剩余单位边两端均active，可全部加入。证毕。

这是simple假设承重处，多重图平行包总量可能大于1，不能照抄。

### 3.3 Unanchored 分量

此时所有s_i=q_i=0，也没有已保留heavy在该分量制造可见价值。若C含环，可以沿一个环循环定向，沿生成树把其他顶点激活，最后加回全部边，从而全部保留。

若C是树，则任何保留非空单位边集合形成一个非平凡森林分量D；EF要求每个D顶点自身至少有1条入边，而D只有|V(D)|-1条边，不可能。故必须删除C的全部单位边（不只是删除一条边）。孤立分量边数0自然无成本。

### 3.4 全单位可行性及最优性

先删尽unanchored树分量。其余单位边若全保留，则simple图EF等价于每个i自身收益至少

    d_i=max(q_i, 1 if i仍有单位邻边 else 0).

因此需要至少 `b_i=max(0,d_i-s_i)` 条单位边给i。用二分流：源->顶点i容量b_i；顶点i->每条incident单位边节点容量1；每条边节点->汇容量1。可满足全部quota iff maxflow=sum b；未用于quota的边任意定向，不会损害EF。

若流不可行，该heavy branch没有任何EF partial解：若有，anchored补全lemma及unanchored有环补全可把它改成全部保留，只剩必须全删的树分量，矛盾。若流可行，删掉的unanchored树边是该branch不可避免的全部单位损失，故最优。对3^k个branch取最低总成本，得到全局最优。

**Why bit complexity is honest**：huge q_i只用整数加、比较。若b_i超过incident单位边数可直接拒绝branch。实际流量总额<=m；没有按heavy权重跑伪多项式DP。

**What this is / is not**：完整自足算法结论；不是“有限例子支持猜想”。但新颖性尚未确认，可能只是作者没写的短推论；目前不能当独立论文已完成。新增weighted donation cost、simple min-charity的紧指数/核化、以及multigraph extension才可能组合成更完整成果。

**Verification**：`python battle_fair_parameter/charity_probe.py`；seed37042027；n=1..6，每n200，共1200个随机simple实例；最多8条边；端点权来自(0,0),(0,1),(1,0),(1,1),(1,2),(2,1),(2,2),(2,3)。对每例枚举全部`3^m`partial orientation求真最优，并与实际3^k+maxflow算法比较；差异0。权重整数、算术精确。

## Source Audit appendix（2026-10-20）

已针对[2512.25033v5完整PDF](https://arxiv.org/pdf/2512.25033v5)正文及附录完成直接覆盖审计，详细检查表见README末节。Table1 caption不把heavy第二行扩至charity；Thm7只处理binary；Thm13及Claims29–30只枚举heavy两个方向并保留全部单位边；Thm14/23的删除计数k属于Wshared+treewidth DP，不能读成heavy参数。正式minimum charity模型没有edge deletion cost输入，全文`cost`检索无匹配。未发现本版本已直接给出第3节的simple heavy-FPT/3^k或任意非负donation cost结论。定向primary后续检索未找到独立覆盖，但**新颖性仍未确认，短推论风险仍为最强价值异议**。本结论不等于作者明确提出FP03，不等于全球文献已穷尽，也不等于独立论文已成立。
