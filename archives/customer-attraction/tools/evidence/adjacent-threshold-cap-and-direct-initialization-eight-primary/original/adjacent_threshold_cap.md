# 实际相邻上升的无承诺阈值上限：已被反驳的辅助候选

2026-10-24。**候选C为FALSE**；Q-CAG-HALF仍OPEN。normal_form给出解析反例：[原文](../normal_form/swap_ascent_payment_counterexample.md)。本分支先未读其证明而从客户定义重构全部IC，见 [独立核对](review_threshold_cap_counterexample.md)。其delta/(beta-alpha)=k/(2e)无界，所以任何固定有限倍数的实际上升付款也失败。下面保留反驳前推导历史，不再将C列为OPEN。

## 1. 精确对象与候选

采用 CAG-MODEL 全部量词，固定任意合法有序前缀h、背景b、余r>=2人。
给定一份完整纯SPE，实际首对为A,B，after-AB完整尾为tau，整叶两人的利润为alpha,beta。
无祖先承诺阈值

    mu_B = M_(r-1)(b+1_B)

是固定B背景后全部完整SPE首利的最小值。它不指原sigma的B偏离收益，不受保持原叶或祖先收益上限的约束。

当时提出、现已反驳的候选C是

    alpha < beta  ==>  mu_B <= beta.                 (C?)

这适用于任意人数、任意目录、任意合法背景、全部离轨历史。r=2的尾为空。空主题、重复、零客户保留；严格上升时A与B不可能为同一覆盖集合。

(C?)等价于：在固定b+B之后，存在一份首位收益至多beta的完整子SPE。这里只是存在另一份子SPE，未声称原sigma采用它。

## 2. 它若成立会付哪一笔账

新换位来源已证明：保留原AB尾并改成BA时，唯一第二节点的最小缺陷为

    delta=(mu_B-alpha)_+.

所以(C?)会给同一个原q上的真实钱包

    delta <= beta-alpha.

在同q收益序列lex最大的实现中，严格上升已经给mu_B>alpha；候选将把障碍精确夹在

    alpha < mu_B <= beta.

但这**不自动证明half**。若以tau=2W/(2m-1)定位最后低点，来源只给alpha<tau<=beta及mu_B>alpha，不能把mu_B升级为>=tau。即使已知上述cap，也没有证明所有障碍总成本可由同一W不重计支付。

## 3. 不能跳过的构造缺口

原b+A孩子中，第二人B收益beta并且对每个合法X有一份真实after-A,X尾使X收益<=beta。想得到新b+B孩子的首利<=beta，需要对每个X分别找到after-B,X的**完整**尾SPE，使X收益<=beta。

仅把原after-A,X尾平移不够：它在固定背景A改成B后，所有更深真实比较均可能改变。把旧固定A移回尾部、从原尾移去B来保持同计数也不够，因为原after-A,X真实尾未必包含B。这里没有得到普遍的重构操作，不能宣称(C?)已由可信拼合闭合。

## 4. 两剩余人的解析形式

当r=2，令

    F(T)=sum_(x in T) 1/(b_x+1),
    C(T,Q)=sum_(x in T intersect Q) 1/[(b_x+1)(b_x+2)].

于是U(T,Q)=F(T)-C(T,Q)，C对称且是非负交集Gram核。原AB满足

    alpha=F(A)-C(A,B),  beta=F(B)-C(A,B),  F(A)<F(B).

B是A后真实末位BR；对每个根X，其原规定BR R_X满足

    F(X)-C(X,R_X) <= alpha.

欲证(C?)即须推出

    max_X [F(X)-C(X,B)] <= beta.

这仍是一个整菜单关系，不能只用B对A的实际BR。
若存在X使gamma=U(X,B)>beta，则R_X的真实BR与根cap至少给

    F(R_X) >= F(B)+gamma-alpha.

证明：R_X对B为合法BR比较，给
`F(R_X)-C(R_X,X)>=F(B)-C(B,X)`；根cap给`C(R_X,X)>=F(X)-alpha`，相加即得。

此必要式只迫使R_X比B的F更大，不必比X更大。因而不能据此宣称沿R迭代F严格增加并有限终止。反驳前未证明交集Gram正性和全部菜单比较足以排除这种状态；现已有上述合法完整SPE反例。该式只是反驳前本候选证明尝试的定位，不计为新的福利下界。反例证明这些必要式并不推出C；它在r=2即失效。

## 5. 一次明确候选诊断的范围

`check_adjacent_threshold_cap.py` 使用已有规范ExactSPESolver的集合值递归，检查以下五份原输入全部可实现有序路径上的相邻严格上升：

| 原输入 | 检查的相邻上升数 | 违反(C?) |
|---|---:|---:|
| root_tax_failure |105|0|
| aggregate_theta_failure |36|0|
| portfolio_matching_failure |1|0|
| worst_pne_welfare_failure |0|0|
| coverage_opportunity_failure |18|0|

共160项。阈值按新固定计数b+B重新求全部SPE最小值；没有把旧sigma冻结为新孩子，也未限制一般策略同计数同回复。此有限阴性不提供一般证明，不继续扩样。
