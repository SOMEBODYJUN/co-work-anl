# Q-CAG-HALF：任意纯 SPE 是否覆盖最优的一半？

**状态：开放目标，2026-10-09 建立独立分支。**

## Exact Claim

对 [CAG-MODEL](../current/customer_attraction/model.md) 的每个有限共同目录实例、
每个整数 $m\ge1$、每个完整有序历史上的纯 SPE $\sigma$，

$$
2W(\alpha(\sigma))\ge\operatorname{OPT}_m.
$$

包括全部历史依赖平局选择。Domain 是共用目录、单位提供者权和单位客户价值；
不涵盖异目录或带权提供者。非负整数客户类型重数只是不同单位客户的编码。

## Paper Facts

来源：[Deng 等 arXiv:2307.07174v2](https://arxiv.org/html/2307.07174v2)。
§5 Theorem 5.2 给两位对称提供者的 $3/2$ 上界和一般人数 $2-1/m$ 下界；
§6 明确将超过两人时的 $2$ 上界作为猜想。没有从猜想文字中导入一个现成证明。

下界目录为一个覆盖 $m$ 个客户的大主题和 $m-1$ 个互不相交的单位单例主题。
全选大主题的某个 SPE 终局覆盖 $m$；最优覆盖 $2m-1$。
这个族不排除固定 $m$ 的更强上界 $2-1/m$，也不能证明该更强上界。

## 关键 proof obligations

早提供者改选主题后，全部后继行动都可能改变。需把原终局和真实偏离分支比较，
而不是固定后继行动并套用静态 Nash 的 smoothness 不等式。
同计数历史的续局也可不同，因而不能默认一个匿名 Markov 平局规则。

候选路线为残差收费：固定均衡覆盖 $C$、最优覆盖 $O$，证明
$|O\setminus C|\le W$ 即充分，但未必必要。更强候选
$u_i\ge|T\setminus C|$（每位 $i$、每个主题 $T$）已经被两人、五主题、
十四个单位客户的完整 SPE 反例否定。更弱的 $W\ge m\max_T|T\setminus C|$
也被同一例否定。实际覆盖 9、最优覆盖 10，该例没有否定目标猜想。
失效来自其他交叠主题间的响应循环，不能只检查后继是否直接复制偏离主题。

新的候选应保留最优 $m$ 个主题之间的非重计覆盖结构。曾尝试按原在轨前缀定义
$V_{i,T}$ 为玩家 $i$ 改选 $T$ 后在既定后继策略下的真实终局收益，SPE 只给
$V_{i,T}\le u_i$。若可对某个最优主题组合找到排列 $\pi$ 使
$\sum_iV_{i,T_{\pi(i)}}\ge|O\setminus C|$，即可推出目标。
但这条更弱的桥也已被 [CA-PORTFOLIO-MATCHING-NO](../current/customer_attraction/portfolio_matching_counterexample.md)
否定：唯一最优组合排除了最优选择量词的歧义，真实偏离矩阵两种匹配均为 41，
遗漏数却为 42。该实例实际覆盖 44、最优覆盖 45，仍不是目标反例。

## 当前税项路线及确切缺口

[CA-TWO-REMAINING-TAX](../current/customer_attraction/two_remaining_tax.md)已严格证明：
固定任意合法历史、恰两位剩余玩家时，对任意比较主题 $T,S$，

$$
R_b(T,S)\le R_b(A,B)+\sum_{x\in A}\frac1{(b_x+1)(b_x+2)}.
$$

这里 $R_b$ 只算剩余两人的收益，不能在非零背景时把它等同完整覆盖。
无背景版本重构已发表两人 $3/2$ 上界。

旧首步机会成本不等式现已由 [CA-TAX-BRIDGE-NO](../current/customer_attraction/tax_bridge_counterexample.md)
在空背景三人否定：15>29/2。更弱的任意合法背景总税式也由
[CA-GENERAL-TAX-NO](../current/customer_attraction/general_tax_counterexample.md)否定。
已证明的恰两人税界及其代数恒等式不受影响；零背景总税仍未证明或被反驳。
不能通过仅修补非零背景分母挽回已失败的首步桥。

## 三人边界及新的前沿

[CA-THREE-SHARP-5-3](../current/customer_attraction/three_player_sharp.md)已完整内部证明：
任意共同目录、恰三人、每个完整历史依赖纯 SPE 都有 `OPT_3≤(5/3)W`，匹配下界达到。
跟踪真实离轨L_i及Q,R，八类节点最优性与逐客户非负恒等式闭合；不依赖旧一般税归纳。
[旧142/81](../current/customer_attraction/three_player_bound.md)保留为不同两人税机制。
恰三人目标已解决；这个锐界定理的范围仅限三人，没有外审或新颖性认证。

[CA-FOUR-UPPER-1499-750](../current/customer_attraction/four_player_bound.md)进一步证明
恰四人任意目录、全部完整纯 SPE 满足 `OPT_4≤(1499/750)W`。
两份独立逐客户算术审计及逐节点量词审查均通过，未声称锐性。
新增接口为：保留根偏离至实际末主题后，所有真实后继主题的自身节点最优性，
不能仅保留实际路径的分母保底。

一般目录现从五人起需控制跨分支的全局余额。可独立研究零背景总税，或使用
[完整策略重数锥](../current/customer_attraction/strategy_cone.md)的精确对偶寻找统一不等式。
固定(m,p)有限样本锥中的成功不涵盖任意目录、任意策略；证据范围必须保留。


进一步的[在轨覆盖机会反例](../current/customer_attraction/coverage_opportunity_counterexample.md)
否定 `δ_i≤u_i` 的逐期收费，即使只要求根SPE的实际前缀。
令 `C_t` 为实际前t主题覆盖，仍有
`Σδ_i=OPT_m−W`，因此需要全局 `Σ(u_i−δ_i)≥0`。
更强的所有前缀余额 `Σ_(i≤t)u_i+F_(m-t)(C_t)−OPT_m≥0`
已被 [CA-PREFIX-BALANCE-NO](../current/customer_attraction/prefix_balance_family.md) 否定：
每个m≥4可有完整SPE的B1=4−m−1/m<0，固定首位收益乘数α<2也不普遍足够。
收益始终取原终局份额；终局总余额与根总税仍开放。

## 新的有效接口与边界

[极大花瓣结构定理](../current/customer_attraction/disjoint_maxima_bound.md)
对任意人数证明锐界2−1/m，但必须删除共同核心后不同极大花瓣互不相交。
[平均真实偏离恒等式](../current/customer_attraction/global_new_uniform_portfolio_two.md)
已在任意合法背景、恰两剩余玩家闭合；该页式(6)的任意人数平均接口仍未证明，
后继主题改动会改变再后继的真实回复，不能冻结组合。
[五人模板障碍](../current/customer_attraction/five_player_lift_obstruction.md)
表明指定460行比较单独不足，辅助O>2W可行点不是真实SPE反例。
[可信续局接口](../current/customer_attraction/credible_continuations.md)
扩大完整策略采样范围；均匀菜单全支持与有限样本证明范围必须区分。

## 状态判别

2026-10-10 的新增接口是任意合法固定背景下的
[三剩余人利润锐界](../current/customer_attraction/three_remaining_profit_bound.md)和
[四剩余人利润界](../current/customer_attraction/four_remaining_profit_bound.md)：
分别给 `F3(b)≤(5/3)R_b(实际)`、`F4(b)≤(1499/750)R_b(实际)`，允许全部完整历史平局。
四人界需要明确聚合背景校正；仅平移零背景根税并不成立。
这两个定理只比较剩余玩家利润，不能替换为含既有玩家的全局覆盖。
末四人粗组合接口给 `OPT_m≤(1499m/3000)V4+Σb/(b+1)`，五人时系数1499/600仍不足2。
下一义务是保留最优主题偏离后的多个真实后继分支及其自身其他行动回复；
更强松弛点缺少可信策略，不作为目标反例登记。

[上传工具](../current/customer_attraction/uploaded_tool_audit.md)的全SPE集合递推与规范工具相同。
其双Möbius构造已提升为[独立全历史编译定理](../current/customer_attraction/mobius_compiler.md)，
安全大偏置本身始终半覆盖，因而不直接给一般反例。

全称证明、某个实例的完整 SPE 证书和有限反例搜索分别记录。
未找到反例不提升本猜想。工具或文献附件获取失败不产生数学结论。
若强候选失败，保留确切反例及有效的弱化接口，再决定新的 proof obligation。

本目标与原设施模型的存在某个近似 SPE 构造、$\varphi$ 及全 $k$ 因子 2 定理
没有现成蕴含关系，禁止仅因相同常数或 SPE 名称而互相导入。


## 2026-10-10 新边界

[CA-THREE-MAXIMA-HALF](../current/customer_attraction/three_maxima_bound.md)对至多三个不同
极大覆盖、任意内部子主题及任意人数证明半覆盖，允许交叉关联。
共同极大核心c给n≥2的更强式`OPT_n≤2W−c`；n=1直接最优。
四极大主题的静态私有/共享席位union预算已被整数族否定，但没有SPE福利反例。

[CA-FIVE-UPPER-221-100](../current/customer_attraction/five_player_bound.md)给一般目录恰五人
`OPT_5≤[24236714656727/10967499015623]W≤2.21W`。
两个真实中途偏离补入旧模板没有的回复关系，精确证书仍在二以上。
本页Exact Claim不变；一般五人及以上、四极大覆盖以上的非层级目录仍有未闭合义务。


## 动态最大主题预算后的实际前沿（2026-10-10）

[CA-FIVE-MAXIMA-HALF](../current/customer_attraction/dynamic_maxima_bound.md)已完成任意人数、
至多五个不同包含极大主题、任意内部子主题和全部历史平局的半覆盖。
一般目录仍只在n≤4被无条件解决；n≥5、至少六个极大主题的交叉关联需要新支付机制。
新逐历史D_t与私有/共享包络提供合法接口；它们在全s范围给保底公式，未自动达到因子二。


## 三个真实回复菜单后的精确剩余义务（2026-10-10）

[CA-FIVE-REPLY-UPPER](../current/customer_attraction/five_player_reply_bound.md)现将一般五人界改善至
493266145873827/234749688354196≈2.101243，仍未达到2；旧claim保留原精确常数。
半覆盖未解决结构从至少六个极大主题开始；n≥5仍需共同策略下的全局跨节点预算。
[安全值边界](../current/customer_attraction/continuation_security_barriers.md)证明
普遍去相关及真实根菜单自由混合均不足，其中菜单失败可对每n≥3构造完整SPE。
不限制对偶组合的`u_i≥v_n`或更弱`W≥nv_n`仍开放；若使用菜单之外的主题组合，
需证明新增比较可由实际终局收益支付，不能借静态minimax量词暗中替换顺序回复。
