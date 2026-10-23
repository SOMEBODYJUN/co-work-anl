# 本工作区精确身份

## Q-CAG-HALF

状态仍 OPEN。沿用 [规范模型](../../../current/customer_attraction/model.md) 的有限单位客户、共同有限非空目录、任意人数、全部有序历史纯 SPE，含空主题、重复、任意历史平局与零客户。目标仍是每个这样的 SPE 的 2W≥OPT_m；本轮没有一般证明或主命题反例。

## PRODUCT-MENU-TIME-v1

- Exact statement / Quantifiers：对每个固定 m≥1，“每个合法实例及其每个完整纯 SPE 的自由完整实际前缀菜单 M≤W/m”当且仅当“存在 λ∈Δ_m，仅依赖 m，对每个上述实例/SPE 及每个查询分布 p 均有 Σ_iλ_i min_A g_p(Z_i(A))≤W/m”。
- Objects / Domain：有限单位客户、不同客户子集组成的非空共同目录、全部有序历史纯 SPE；Z_i(A) 保留实际前缀、在 i 强制 A 后沿同一 σ 的完整 m 槽终局；g_p(Z)=Σ_Tp_TΣ_(x∈T)1/(1+c_x(Z))。
- Assumptions / Definitions：查询与随机背景实现独立；实例的目录与 m 均不预设统一上界，等价陈述逐个固定 m。重复/空主题选择及零福利保留。
- Scope / Conclusion：辅助菜单桥的全实例普遍成立迫使跨实例通用位置混合；无通用混合时至多 m 种实例查询对的有限整数产品给该桥的合法完整 SPE 反例，总复制数不设上界。不是菜单桥已成立或已失败；不是 Q-CAG-HALF 的等价命题。小支撑是等价归约的附属结论，独立证明见正文链接。
- Dependencies：有限产品逐坐标 SPE 引理（已有 P1）、完整菜单有限零和对偶、有限维紧致性与有限 LP 对偶；正文给完整推导。
- Evidence：root 自足解析证明；独立研究员在原稿前按定义盲重构，核对全历史、单射、同步位置与有理复制。另一路独立字面单位客户实现检查273历史、4368比较、768核项及12组关联查询；原始/对偶等值277/54，root重放通过。第三分支独立证明小支撑≤m。
- Counterevidence / Objections：目前没有成立的致命异议；若交换 min_i 与组件求和则错误，正文明确禁止。任意产品 SPE 可分解并未假定。16份指定有限证书没有时间冲突，不能支持全称真值。
- Status：完整解析归约、独立内部定义级审查与计算实现检查通过；外审与新颖性未认证。
- Related files：[正文](parent/product_menu_time_obligation.md)、[独立审查](independent_attack/product_menu_separation_review.md)、[有限诊断及参数](parent/probe_common_time.py)、[实际报告](parent/common_time_diagnostic.json)。

## BANK-PATH-CAPACITY-v1

- Exact statement / Objects：两个不交单位客户宇宙上任意有限非空目录的完整 Cartesian 目录；任意 m≥1、任意完整历史依赖纯 SPE。实际行动 (A_i,B_i)，V_i(a,b) 是在实际前缀联合改成(a,b)后沿原策略的主坐标最终收益。令 d_i=max_a V_i(a,B_i)−u_i^M≥0；银行客户 x 实际覆盖位置 i_1<…<i_(c_x)。则

      Σ_i d_i ≤ H_B := Σ_(x∈∪B_i)[1−Σ_(t=1)^(c_x)1/(m−i_t+t)]
                    ≤ W_B−Σ_x c_x/m ≤ (1−1/m)W_B.

- Domain / Quantifiers / Assumptions：所有上述实例、人数、全部有序离轨历史及任意跨坐标历史平局；允许重复及空主题。无需坐标投影本身是 SPE，也不冻结后继。只在当前偏离时保持银行动作，之后银行可响应主动作变化。
- Definitions / Scope：H_B 是单个实际路径的精确稀释容量。逐客户项非负，H_B=0 当且仅当 B_1⊆…⊆B_m。每个实际玩家子集也有点态 d_i≤u_i^B−Σ_(x∈B_i)1/(p_x^i+m−i+1) 可加。
- Conclusion：沿同一个真实路径的主菜单盈利不能无限重复消费银行客户；嵌套实际银行路径没有这种主菜单盈利容量。互斥离轨子树之间的容量未由根福利支付，本条不解一般 half，不排除所有历史耦合银行。
- Dependencies：完整 tuple 节点 SPE、银行主题客户最终负载上限、逐客户有限求和；无外部定理导入。
- Evidence：tree_dual 从保持当前银行动作独立提出预算；root、global_induction 分别按联合偏离重构。统一正文含 signed R/κ 与 d/ρ 的不同预算及准确边界；有限完整 SPE 实现审计仅检查实现。
- Counterevidence / Objections：ρ、κ 与离轨子树容量无全局根支付；不得省略这些差额或把不同路径银行福利相加。没有发现点态预算成立的致命异议。
- Status：解析证明与独立内部重构通过；外审及新颖性未认证。
- Related files：[统一正文](global_induction/bank_joint_deviation_budget.md)、[独立推导与审查](tree_dual/bank_budget_independent_review.md)。

## BANK-MONOTONE-PROJECTION-v1

- Exact statement / Definitions：同上模型。对主历史 h 递归定义完整联合历史 H(∅)=∅，H(ha)=H(h)·(a,σ_B(H(h)))，诱导主策略 τ(h)=σ_M(H(h))。若在每个映射历史 H(h)，σ 规定的续局中当前银行主题包含于每个未来银行主题，则 τ 是主坐标游戏全部有序历史的纯 SPE。
- Objects / Domain / Quantifiers：所有有限完整产品目录与完整产品纯 SPE；性质必须对每个主历史的映射 H(h) 成立，不是仅根实际路径嵌套。重复、空主题、零客户及任意历史平局保留。
- Assumptions / Conclusion / Scope：当前银行客户在规定续局已全部被未来覆盖，故其当前收益达到任何未来回复下的最小可能值。主动作改变、当前银行动作保持时，银行收益只会增不会减；完整 tuple 最优性强迫主收益不能提高。对每个映射历史重复，得到完整 τ SPE。仅为一个坐标投影保留的充分条件，不是所有银行产品可分解。
- Dependencies：BANK-PATH-CAPACITY-v1 的点态保底；H 映射与同原策略真实续局的归纳一致性。
- Evidence：root 提出条件和映射，tree_dual 与 global_induction 独立核对全部历史和偏离后映射。
- Counterevidence / Objections：仅一条实际路径嵌套不能推出完整主 SPE；没有假定一般产品策略具有该条件。
- Status：完整解析证明、独立内部重构通过；外审及新颖性未认证。
- Related files：[统一正文](global_induction/bank_joint_deviation_budget.md)、[独立证明](tree_dual/bank_budget_independent_review.md)。
