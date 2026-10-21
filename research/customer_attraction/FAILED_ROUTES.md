# 顺序客户吸引：失败机制、回收成果与重试条件

研究存档：customer-attraction；目标身份：Q-CAG-HALF。

主目标 `Q-CAG-HALF` 仍 **OPEN**。下列记录只否定写明的桥或模板。完整失败资产按[数学地图](../current/customer_attraction/README.md)进入；每个反例的原始输入、完整策略、审查和冻结证据继续保留。

| 尝试与失败点 | 仍可回收什么 | 改变什么才值得重试 |
| --- | --- | --- |
| 强 iid 福利桥 `W≥Z_m`：[静态基准 §1.1](../current/customer_attraction/iid_security_and_flow_barriers.md)与既有八/十三客户 CCE 反例共同给出真正完整 SPE 反例，因为 iid 对称混合 Nash 本身是 CCE | 静态 `mv_m≤Z_m≤OPT_m`、凹势及动态债务恒等式全部保留；该推论不是新实例 | 改攻较弱 `(1−1/(2m))Z_m` 或真正安全值聚合，不能继续将强 iid 桥称开放；不否定一般half |
| 将[真实末两人菜单证书](../current/customer_attraction/penultimate_few_exceptions.md)无条件外推到大量早期遗漏 | 少量遗漏可由早期/末位联合K支付；一般A低负载要求乘子下界，A外共覆盖给上界，两者可能不相容 | 共同重选非均匀例外权重、调用更早真实回复或换全局不变量；模板负余项不等于合法SPE反例 |
| 仅依实际终局负载校正，要求Σf(c)≥OPT且f0=0、f1=1：[五客户无拥挤完整SPE](../current/customer_attraction/collision_free_occupancy_obstruction.md)给Σf(c)=W4<OPT5；[任意人数族](../current/customer_attraction/collision_free_three_halves_family.md)进一步迫使一般f0=0的普遍支付至少f1≥3/2 | 调和势仍能表示收益差；覆盖矩行空间与SPE真实比较仍可用 | 调整f(2),f(3),…无法影响本例；必须改变单次覆盖信用或使用主题/真实分支信息，不能把这当half反例 |
| 从终局收益低维span推固定非负兴趣类型基：[覆盖矩极射线](../current/customer_attraction/coverage_moment_geometry.md)表明每非空类型在m≥2均承重 | 可依实例有理消元到d种类型，保留全部收益、覆盖、SPE及效率真值 | 允许自适应选支持，或放松精确保留全部数值；span与非负行锥不得混同 |
| 用实际均匀缩放背景αc支付弱安全预算：[完整SPE无限族](../current/customer_attraction/fractional_actual_load_counterexample.md)对每个m≥4满足(m−1/2)M>W | OPT≤(2m−1)M的逐客户代数保留，四人17客户差11/26；完整离轨策略以有限BI奖金续局证明，不用错误的固定tie贪心 | 可改选其他静态背景、保留精确税G_C或直接跨分支支付；真正聚合安全值及mM≤W+G_C另行研究，本族均未否定 |
| 用任意最低静态CCE替代PNE作福利比较：[十三客户完整反例](../current/customer_attraction/worst_cce_welfare_counterexample.md)中W9，全部静态CCE期望福利至少137/15，精确最低2785/297；另有[八客户四主题计数策略](../current/customer_attraction/eight_customer_cce_welfare_gap.md)给W6<544/87=min_CCE E[W] | 比最差PNE失败更强；完整SPE及静态原始/对偶可复核，真正静态安全值v3≤3 | 需要新的跨真实分支预算或真正安全值桥，不能只把PNE换成CCE；不反驳半覆盖 |
| 把顺序 SPE 终局当成静态 NE，套静态次模福利界：[完整反例](../current/customer_attraction/literature.md)中 SPE 终局仍有静态盈利偏离 | 覆盖的次模性、均分收益与静态有效效用结构仍成立 | 比较偏离后**原策略的真实后继**，或另证所用类的 SPE→NE 桥 |
| 用同实例最差静态PNE福利替代SPE终局：[十六客户完整反例](../current/customer_attraction/worst_pne_welfare_counterexample.md)给W(SPE)=15，而全部静态PNE福利16 | 比“SPE终局可以非PNE”更强：不存在另一低福利PNE可供比较；静态福利分析本身保留 | 另造跨分支相关对象并证明其福利支付，不能仅更换一个静态PNE；CCE福利桥也已由上述独立反例否定 |
| 假定同主题计数历史必须同回复、或早晚收益单调：[续局边界](../current/customer_attraction/continuation_lemmas.md)均有完整 SPE 反例 | 子博弈可实现终局**集合**可按计数缓存 | 集合压缩后仍对各有序历史独立重构；限制平局规则须另立模型 |
| 逐人或聚合支付最大残余主题、把最优主题匹配到在轨玩家：[残余反例](../current/customer_attraction/continuation_lemmas.md)、[匹配反例](../current/customer_attraction/portfolio_matching_counterexample.md) | SPE 仍给每次真实偏离的收益上界；保留最优主题的非重计并集 | 改用允许跨玩家、跨节点的共同支付，而非重试同一匹配 |
| 首步机会成本税、任意背景总税、空背景根总税：[首步](../current/customer_attraction/tax_bridge_counterexample.md)、[背景](../current/customer_attraction/general_tax_counterexample.md)、[根](../current/customer_attraction/root_tax_counterexample.md)均已否定 | 恰两人税恒等式和固定背景的三/四人**剩余利润**定理仍成立 | 改变全局收费方式；修分母不能修复空背景已失败的桥 |
| 要求每期机会损失由当期收益支付，或所有实际前缀余额非负：[逐期](../current/customer_attraction/coverage_opportunity_counterexample.md)、[任意人数负前缀族](../current/customer_attraction/prefix_balance_family.md) | 总机会损失的望远镜恒等式保留 | 允许局部欠债，证明终局总余额；不再把全局任务加强为逐步非负 |
| 把末位最坏回复值或真正静态安全值作为每个人保底：[聚合末位值](../current/customer_attraction/aggregate_theta_counterexample.md)、[逐人安全值](../current/customer_attraction/individual_security_counterexample.md)失败 | 末两人保底及静态 \(v_m\ge\operatorname{OPT}_m/(2m-1)\) 仍可用 | 证明真实 SPE 的聚合支付，保留静态对手不观察抽样的量词 |
| 对全部查询分布要求去相关补偿：[全分布预算](../current/customer_attraction/global_security_budget_boundaries.md)失败 | 指定完整策略锥中仍有精确共同 (Q) 证书 | 允许依实例选择安全最优查询与共同静态竞争分布；固定策略锥已闭合时换策略 |
| 所有 (D_ige0)、弱局部 iid 漂移：[安全值链](../current/customer_attraction/security_chain_and_local_boundary.md)、[动态 iid](../current/customer_attraction/dynamic_iid_debt_boundary.md)失败 | 全路径债务恒等式、真实背景安全值单调嵌入仍成立 | 控制总债务，不逐步加强；两种候选全局桥均仍需证明 |
| 每节点先平均全部偏离、固定深度权或规定静态运输核：[流模板](../current/customer_attraction/iid_security_and_flow_barriers.md)、[规定核](../current/customer_attraction/stationary_pair_transport.md)失败 | 未压缩的逐历史偏离矩阵、末两人循环运输证书 | 允许每个 ((h,a)) 单独乘子或新的跨节点机制；模板分离向量未必是 SPE |
| 五人的既定有限必要条件模板只调乘子：[索引松弛精确障碍](../current/customer_attraction/five_player_indexed_obstruction.md)仍最优于二以上 | 真实分支下的现有五人上界、可重用原始/对偶精确证书 | 增加本质不同的真实回复关系、策略一致性或换表示；LP 点不能冒充完整 SPE |
| 末回复规范化后固定早期乘子直接提升：[固定提升反例](../current/customer_attraction/terminal_tie_lift_obstruction.md) | 末行拆分和商空间提升接口；同实例可重选乘子成功 | 共同选择早期乘子与误差支付，不把一个固定证书失败扩大成一般不可能 |
| 用均匀大正偏置 Möbius 编译直接产生坏福利：[编译边界](../current/customer_attraction/compiler_security_barrier.md) | 完整历史的有符号表示与合法大偏置嵌入 | 正偏置会改善福利；较小合法偏置或另一真实构造须重新证明 |

重试前只需核对与你当前机制有关的一行及原反例，无需把全表当作探索前审批。新的想法可以直接尝试。工具失败、超时、数值未找到反例和多人赞同都不改变数学状态。
