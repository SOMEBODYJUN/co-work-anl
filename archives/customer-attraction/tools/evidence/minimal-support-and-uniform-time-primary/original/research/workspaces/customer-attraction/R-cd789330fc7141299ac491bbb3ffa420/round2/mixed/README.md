# round2：自由完整前缀菜单的共同预算

2026-10-23。一般 Q-CAG-HALF 仍 OPEN。已重读根四入口、本题状态、peer 的 PRODUCT-MENU-TIME-v1 与至多 m 种组件分离归约。本轮不追加有限选根规则、不扩固定策略锥、不重做旧查询分布重权，也不重复 peer 的16证书阴性语料。

当前精确候选为 `uniform_time_working.md` 中的全实例关系 Σ_i ψ_i(p)≤W；若证明成立，则给通用时间 λ_i=1/m，并推出该自由完整前缀菜单桥。它比各位置 Mfull≤u_i 弱，但仍未经证明。仅写出这一候选和等价债务不构成一般推进。

当前没有新普遍支付或合法完整 SPE 严格分离；没有把上轮非 SPE 菜单障碍重新当作本轮结果。下一步须找到自由列选择之间的真实中继支付，或直接产生全部子树可核的分离，不再换一个固定时间/根选择规则。

`audit_uniform_debt.py` / `uniform_debt_audit.json` 对一份既有791客户完整SPE从客户和全部57个有序历史重建，399项偏离比较及全位置债务恒等式精确通过。它只核公式实现，没有优化查询、扫描策略或把这个样例作为一般(U)的证据。

`review_waterfill_sharpness.md` 是 parent 指定的 tail 锐性族独立审查：先盲推导再对稿，通过53客户完整400历史策略、真正v4原始/对偶及共同核心无限族；明确root−t恒正，锐性不扩大至最小反例限制类。`audit_waterfill_review.py` / `waterfill_review_audit.json` 从数据独立核全部比较与有理水位区间，并给比率纯有理界 c/(c+94)<Γ/D<c/(c+608/9)。

`weak_push_minimal_support.md` 给 WP 假如失败时的一般最小 unsafe 支撑条件：对角插入税、G=u11ᵀ−sym(K) 的一个负方向/切向严格正定/逆向量逐项负，以及两主题缺口的精确平方阈值。它只是局部必要结构，尚未从完整 child IC 排除该结构；不是一般支付证明。`audit_minimal_support.py` / `minimal_support_audit.json` 重建旧348客户完整SPE的43历史258比较及36个K核项，量化为何其高插入二环仍无二点弱推送缺口；抽象矩阵回归不声称可由CAG实现。

`two_query_cross_child_boundary.md` 专门尝试任意目录、任意人数的两主题查询WP：把两根全部真实child IC展开成更深势遗憾、删除child后的势差及非负IC slack；仍缺正删除势差的平方余量支付。`audit_two_query_recursion.py` / `two_query_recursion_audit.json` 在旧348真SPE核出两边深层遗憾和child slack全0、删除势差各12、交集税各6。没有证明WP2，所以没有将反例最小查询支持提高到3。

`review_pi_counterexample.md` 为 parent 指定的 global PI 辅助桥反例盲审，独立通过。`audit_pi_review.py` / `pi_review_audit.json` 仅读instance+strategy，核430单位客户、43历史258比较、全部56/126计数：root91、P3=329、P4=873/2、Δ4−root=33/2；W265、OPT324。实际及全部根真实终局也达到P3，但根完整插入矩阵最大90<91，故本例不是WP/EI/Mfull/half反例。
