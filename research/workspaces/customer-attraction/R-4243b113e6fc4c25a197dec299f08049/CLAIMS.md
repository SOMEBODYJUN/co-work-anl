# 本工作区精确身份

## Q-CAG-HALF

状态仍 OPEN。沿用 [规范模型](../../../current/customer_attraction/model.md) 的有限单位客户、共同有限非空目录、任意人数、全部有序历史纯 SPE，含空主题、重复、任意历史平局与零客户。目标仍是每个这样的 SPE 的 2W≥OPT_m；本轮没有一般证明或主命题反例。

## PRODUCT-MENU-TIME-v1

- Exact statement / Quantifiers：对每个固定 m≥1，“每个合法实例及其每个完整纯 SPE 的自由完整实际前缀菜单 M≤W/m”当且仅当“存在 λ∈Δ_m，仅依赖 m，对每个上述实例/SPE 及每个查询分布 p 均有 Σ_iλ_i min_A g_p(Z_i(A))≤W/m”。
- Objects / Domain：有限单位客户、不同客户子集组成的非空共同目录、全部有序历史纯 SPE；Z_i(A) 保留实际前缀、在 i 强制 A 后沿同一 σ 的完整 m 槽终局；g_p(Z)=Σ_Tp_TΣ_(x∈T)1/(1+c_x(Z))。
- Assumptions / Definitions：查询与随机背景实现独立；实例的目录与 m 均不预设统一上界，等价陈述逐个固定 m。重复/空主题选择及零福利保留。
- Scope / Conclusion：辅助菜单桥的全实例普遍成立迫使跨实例通用位置混合；无通用混合时有限整数产品给该桥的合法完整 SPE 反例。不是菜单桥已成立或已失败；不是 Q-CAG-HALF 的等价命题。
- Dependencies：有限产品逐坐标 SPE 引理（已有 P1）、完整菜单有限零和对偶、有限维紧致性与有限 LP 对偶；正文给完整推导。
- Evidence：root 自足解析证明；独立研究员在原稿前按定义盲重构，核对全历史、单射、同步位置与有理复制。另一路独立有限产品审计进行中。
- Counterevidence / Objections：目前没有成立的致命异议；若交换 min_i 与组件求和则错误，正文明确禁止。任意产品 SPE 可分解并未假定。16份指定有限证书没有时间冲突，不能支持全称真值。
- Status：完整解析归约、独立内部定义级审查通过；计算实现检查进行中；外审与新颖性未认证。
- Related files：[正文](parent/product_menu_time_obligation.md)、[独立审查](independent_attack/product_menu_separation_review.md)、[有限诊断及参数](parent/probe_common_time.py)、[实际报告](parent/common_time_diagnostic.json)。
