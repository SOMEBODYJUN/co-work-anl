---
id: customer-attraction/r3d6f-actual-load-tax-bridge-and-fixed-cone-attack-review
kind: review
type_tag: 审查
title: R-3d6f 实际税项分数桥与固定锥攻击审查
status: exact-tax-candidate-and-finite-cone-audit-reviewed
truth_status: unproved-sufficient-bridge; old-strong-bridge-refuted; no-new-half-counterexample
review_level: complete-source-and-exact-fraction-output-comparison
scope: actual terminal load fractional-tax bridge, fixed complete-SPE cone attacks, and four-player residual margin
source_refs:
  - source:2a7926ae04b70760b78d:research/workspaces/customer-attraction/R-3d6f7a072d5e489eb5a0bdc4d32bb769/mixed_budget/notes.md
  - source:ef0e8e965116970b002a:research/workspaces/customer-attraction/R-3d6f7a072d5e489eb5a0bdc4d32bb769/mixed_budget/probe.py
  - source:05b2b78a3b5cd8eb5259:research/workspaces/customer-attraction/R-3d6f7a072d5e489eb5a0bdc4d32bb769/mixed_budget/results.json
---

# R-3d6f 实际税项分数桥与固定锥攻击审查

## 1. 候选和静态代数

本批在有限非空共同目录、单位客户、任意 m≥1 和完整有序历史纯 SPE 上定义实际终局负载 c，正负载集合 C、W=|C|、α=(m−1)/m，并令：

    g(T) = Σ_{x∈T} 1/(1 + α c_x)
    M = max_T g(T)
    G_C = Σ_{x∈C} 1/(1 + α c_x)
    R = W − G_C.

保留实际税项的充分候选是 mM ≤ W+G_C，等价于 mM+R≤2W。若它能由完整 SPE IC 推出，则 OPT_m≤2W，足以给出 Q-CAG-HALF。候选允许重复选择、空主题、零客户和任意历史依赖平局，不假设终局为静态 PNE。旧的粗桥把 R≤(m−1)M，得到 (m−1/2)M≤W；已知四人族否定粗桥，却没有否定本候选。

取任意 m 个比较主题 T_j，令 d_x 是 x 在比较并集中的重数，B=Σ_j g(T_j)。逐客户有：

    1[d_x>0] ≤ (d_x + α c_x)/(1 + α c_x),
    |⋃T_j| ≤ B + R ≤ mM + W − G_C.

静态 PNE 可以用各玩家的静态偏离证明 B≤W；完整 SPE 的偏离改变后继，不能把终局当静态 PNE，因此这里仍缺统一的跨后继付款关系。

## 2. 已知四人族的边界

四主题十七客户完整 SPE 路径 BBBA，W=16、OPT=17，四个目录值为：

    g(A)=16/7, g(B)=48/13, g(Q)=61/13, g(D)=388/91.

正负载税项为 G_C=544/91、R=912/91，故 4M+R=2620/91<32=2W。该族只否定旧粗桥，不是本候选的半覆盖反例。

## 3. probe.py 和 results.json 的实际范围

probe.py 对固定完整策略证书建立 StrategyCone 的全部有序历史 IC 行。每个主题查询 a 的目标为 m·g_a−welfare−g_C，按 welfare=1 归一化后用 SciPy linprog 发现候选，再以 Fraction 检查锥不等式和归一等式；跳过无法解析动作表、p>8 或 m>6 的输入。它不是全部纯 SPE 的枚举，也不认证浮点 LP 的全局对偶。

results.json 明确标记 status=finite fixed-cone attack only、universal_claim_proved=false，共 16 个固定证书，全部 exact_primal=true。最大 exact_gap（逐查询）为：

| 证书 | m | 主题数 | 节点 | 最大 gap |
| --- | ---: | ---: | ---: | ---: |
| aggregate_theta_failure | 3 | 6 | 43 | −1/3 |
| coverage_opportunity_failure | 3 | 5 | 31 | −1/3 |
| empirical_iid_kernel | 3 | 4 | 21 | −1/3 |
| global_decorrelation_failure | 4 | 6 | 259 | −1/4 |
| individual_security_failure | 3 | 6 | 43 | −1/3 |
| local_security_increment | 3 | 6 | 43 | −1/3 |
| onpath_budget_failure | 3 | 6 | 43 | −1/3 |
| optimal_last_query_failure | 4 | 7 | 400 | −1/4 |
| portfolio_matching_failure / residual_counterexample | 2 | 5 | 6 | −19/39 |
| prefix_balance_failure / root_tax_failure | 4 | 6 | 259 | −1/4 |
| root_stationary_kernel / worst_cce_welfare_failure / worst_pne_welfare_failure | 3 | 4–6 | 21–43 | −1/3 |
| fractional_weak_m4_certificate | 4 | 4 | 85 | −73/364 |

这些 exact 负 gap 只表示固定有限锥未发现违反，不能扩展到任意完整 SPE。

## 4. 去重、结论和缺口

本批独有内容是保留实际税项 R 的弱桥、四人族的严格余量，以及 16 个固定策略锥的 Fraction 重算。它不重复 R-3d6f security_bridge 的连续对数势/笛卡尔耦合边界，也不替代分数负载弱桥的旧反例。

**已确认：** 静态 PNE 层面 mM≤W；四人十七客户族满足新桥；16 个固定锥均无 exact 违反。

**障碍：** 需要从真实续局理性证明 mM+R≤2W，或构造逐历史 IC 通过且使其失败的完整纯 SPE。不能把静态 PNE 支付、归一化 LP、负 gap 或有限证书集合当作一般定理。

**未决：** Q-CAG-HALF 仍 OPEN；候选可被完全绕开，但在出现真实 SPE 反例或统一跨后继支付前不得弃置。
