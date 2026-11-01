# 一般 NET 的既存完整 SPE 诊断

2026-10-23，shared。精确候选是自由最优 matching/owner、Hall允许γ及原递增捕获同一whole-IC系数下，存在 K_i≤u_i(I)+γ_i；同时核较弱总价ΣK≤W。本次没有生成新实例、策略或重数锥，未作固定人数专项。

使用[诊断程序](diagnose_net_existing.py)只读取三份既存完整SPE证书：先从全部有序历史重算原单位收益与每条真实偏离；然后对第一个最优匹配及first-owner构造流价格，求实际Hall γ网络上的NET与总价LP。浮点只提案；所有报告的可行点、对偶符号、逐变量stationarity、原始/对偶目标相等均由Fraction验证。得到一个精确NET见证即停止该证书，不扩更多选择。

| 原始证书 | 原IC比较数 | W / OPT | 所选最优元组（零基标签） | NET最小最大行差 | 最小总价 |
| --- | ---: | ---: | --- | ---: | ---: |
| portfolio_matching_failure，86客户 | 30 | 44 / 45 | (1,3) | −838/39 | 1 |
| root_tax_failure，61客户 | 1554 | 38 / 61 | (0,1,2,3) | −1 | 119/5 |
| eight_cce_welfare_gap，8客户 | 84 | 6 / 8 | (1,2,3) | −1 | 2 |

NET行差是 min_γ max_i(K_i−η_i)，负值给该固定合法选择的确切可行见证。最小总价是另一次优化，可能使用不同γ，不能把两次优化的各项同时当作一个见证。

三份冻结输出分别为[86客户](net_diagnostic_portfolio_matching_failure.json)、[61客户](net_diagnostic_root_tax_failure.json)、[8客户](net_diagnostic_eight_cce_welfare_gap.json)。每份保留γ、I边流、K/η、完整LP对偶与真实价格层rank，并核对[动态rank正文](net_dynamic_rank.md)的greedy取消目标与独立LP最优值一致。

这些点没有反驳NET，也不能支持它的全称真值。它们本身不解决逐角色NET是否过强的问题。最有承重可能的下一义务仍是动态价格cut上界，或使费用小于逐角色NET的共同全树预算；不继续扩样来积累阴性数量。
