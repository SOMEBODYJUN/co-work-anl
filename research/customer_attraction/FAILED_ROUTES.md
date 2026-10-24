# 顺序客户吸引：失败机制、回收成果与重试条件

研究存档：customer-attraction；目标身份：Q-CAG-HALF。

主目标 `Q-CAG-HALF` 仍 **OPEN**。下列记录只否定写明的桥或模板。完整失败资产按[数学地图](../current/customer_attraction/README.md)进入；每个反例的原始输入、完整策略、审查和冻结证据继续保留。

| 尝试与失败点 | 仍可回收什么 | 改变什么才值得重试 |
| --- | --- | --- |
| 从[最优首动作真实孩子恒等式](../current/customer_attraction/optimal_first_action_branch_gap.md)的全路径预算删去ξ及η，要求存在菜单分布支付全部正ρ：[all-big全人数解析复核](../workspaces/customer-attraction/R-e05f01e191354b028004b433016ae1c9/all_big_completion_slack_obstruction.md)给任意m≥3的完整SPE严格违例，最小差(m²−3m−2)/2+H_m>0 | 原精确恒等式、非负余项与最优首动作真实孩子解释仍成立；相同见证有OPT_m=2W−1，只否定加强。非根ρ=ξ=r−1令ξ原局部系数尖锐 | 保留全部同尾ξ，或提出真正不同的跨枝共同信用；给ξ任意固定比例α<1且其余原系数不变也无法在全人数闭合。仅删η的更弱候选尚未证伪或证明 |
| 从真实根SPE删实际第二位，要求可信修复的上向福利增量≤绝对C倍回放实际regret或每层全部历史regret上确界之和：[已知弱iid族的新删位分析](../workspaces/customer-attraction/R-e05f01e191354b028004b433016ae1c9/actual_root_deletion_upward_repair_obstruction.md)分别给误差2a/(m−2)、4a/(m−2)，但每份真实删后SPE的福利高a | 原完整SPE、回放客户守恒与退款仍准确；命题只否定regret唯一付费的上向合同，不否定半覆盖或带利润/最优边际的修复 | 必须共同支付真实上向reset及OPT_m−OPT_(m−1)，不能将零误差收敛当作真实删后均衡福利的绝对近似 |
| 将倒二真实查询的单末位去相关直接迭代到更早一位，假定各后继IC给非负相关增益：[三人尾部势恒等式及旧34客户完整证书](../workspaces/customer-attraction/R-e05f01e191354b028004b433016ae1c9/three_remaining_decorrelation_residual.md)给两项合法IC合计91/164而删除返还−113/164，净增益−11/82 | 后继IC、精确去相关恒等式与已证倒二真实查询行都保留；这是已知逐人安全反例的另一表示，不否定早期ROW或half | 保留无符号返还并从实际覆盖/比较重复/跨位置信用支付；不把末位最优性重复使用来免费删除中间主题 |
| 允许有利重选最优并集，仍要求纯遗漏数≤W：[71客户完整二人SPE](../workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/exchange/unique_optimum_omission_obstruction.md)有W35、唯一最优OPT38、遗漏36；已有[独立内审](../workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/coupling/optimal_omission_independent_review.md) | 全净差OPT−W=遗漏−实际在最优外覆盖，后者信用不能丢；原共享地图漏列的旧反例在本轮补入口，不认领新发现 | 直接支付OPT−W或完整OPT；仅换最优组合/owner不能无损强制遗漏≤W |
| 强 iid 福利桥 `W≥Z_m`：[静态基准 §1.1](../current/customer_attraction/iid_security_and_flow_barriers.md)与既有八/十三客户 CCE 反例共同给出真正完整 SPE 反例，因为 iid 对称混合 Nash 本身是 CCE | 静态 `mv_m≤Z_m≤OPT_m`、凹势及动态债务恒等式全部保留；该推论不是新实例 | 强iid及弱 `(1−1/(2m))Z_m` 均已否定（弱式见同正文§1.2）；真正安全值聚合仍OPEN，不否定一般half |
| 将[真实末两人菜单证书](../current/customer_attraction/penultimate_few_exceptions.md)无条件外推到大量早期遗漏 | 少量遗漏可由早期/末位联合K支付；一般A低负载要求乘子下界，A外共覆盖给上界，两者可能不相容 | 共同重选非均匀例外权重、调用更早真实回复或换全局不变量；模板负余项不等于合法SPE反例 |
| 仅依实际终局负载校正，要求Σf(c)≥OPT且f0=0、f1=1：[五客户无拥挤完整SPE](../current/customer_attraction/collision_free_occupancy_obstruction.md)给Σf(c)=W4<OPT5；[任意人数族](../current/customer_attraction/collision_free_three_halves_family.md)进一步迫使一般f0=0的普遍支付至少f1≥3/2 | 调和势仍能表示收益差；覆盖矩行空间与SPE真实比较仍可用 | 调整f(2),f(3),…无法影响本例；必须改变单次覆盖信用或使用主题/真实分支信息，不能把这当half反例 |
| 从终局收益低维span推固定非负兴趣类型基：[覆盖矩极射线](../current/customer_attraction/coverage_moment_geometry.md)表明每非空类型在m≥2均承重 | 可依实例有理消元到d种类型，保留全部收益、覆盖、SPE及效率真值 | 允许自适应选支持，或放松精确保留全部数值；span与非负行锥不得混同 |
| 用实际均匀缩放背景αc支付弱安全预算：[完整SPE无限族](../current/customer_attraction/fractional_actual_load_counterexample.md)对每个m≥4满足(m−1/2)M>W；保留精确税的mM≤W+G_C也由[既存13人36客户完整SPE](../workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_counterexample.md)否定，差29481/123025 | OPT≤(2m−1)M及OPT≤mM+W−G_C逐客户代数保留；四主题无限族本身未否定精确税桥，不能混同两反例。13人封闭自动机覆盖全部有序历史，本轮重放112050项IC | 可改选其他静态背景或直接跨分支支付；真正聚合安全值仍OPEN。不能只恢复同一精确实际税重试；另取α=1也有同一旧例的严格反证 |
| 用任意最低静态CCE替代PNE作福利比较：[十三客户完整反例](../current/customer_attraction/worst_cce_welfare_counterexample.md)中W9，全部静态CCE期望福利至少137/15，精确最低2785/297；另有[八客户四主题计数策略](../current/customer_attraction/eight_customer_cce_welfare_gap.md)给W6<544/87=min_CCE E[W] | 比最差PNE失败更强；完整SPE及静态原始/对偶可复核，真正静态安全值v3≤3 | 需要新的跨真实分支预算或真正安全值桥，不能只把PNE换成CCE；不反驳半覆盖 |
| 把顺序 SPE 终局当成静态 NE，套静态次模福利界：[完整反例](../current/customer_attraction/literature.md)中 SPE 终局仍有静态盈利偏离 | 覆盖的次模性、均分收益与静态有效效用结构仍成立 | 比较偏离后**原策略的真实后继**，或另证所用类的 SPE→NE 桥 |
| 用同实例最差静态PNE福利替代SPE终局：[十六客户完整反例](../current/customer_attraction/worst_pne_welfare_counterexample.md)给W(SPE)=15，而全部静态PNE福利16 | 比“SPE终局可以非PNE”更强：不存在另一低福利PNE可供比较；静态福利分析本身保留 | 另造跨分支相关对象并证明其福利支付，不能仅更换一个静态PNE；CCE福利桥也已由上述独立反例否定 |
| 假定同主题计数历史必须同回复、或早晚收益单调：[续局边界](../current/customer_attraction/continuation_lemmas.md)均有完整 SPE 反例 | 子博弈可实现终局**集合**可按计数缓存 | 集合压缩后仍对各有序历史独立重构；限制平局规则须另立模型 |
| 逐人或聚合支付最大残余主题、把最优主题匹配到在轨玩家：[残余反例](../current/customer_attraction/continuation_lemmas.md)、[匹配反例](../current/customer_attraction/portfolio_matching_counterexample.md) | SPE 仍给每次真实偏离的收益上界；保留最优主题的非重计并集 | 改用允许跨玩家、跨节点的共同支付，而非重试同一匹配 |
| 首步机会成本税、任意背景总税、空背景根总税：[首步](../current/customer_attraction/tax_bridge_counterexample.md)、[背景](../current/customer_attraction/general_tax_counterexample.md)、[根](../current/customer_attraction/root_tax_counterexample.md)均已否定 | 恰两人税恒等式和固定背景的三/四人**剩余利润**定理仍成立 | 改变全局收费方式；修分母不能修复空背景已失败的桥 |
| 要求每期机会损失由当期收益支付，或所有实际前缀余额非负：[逐期](../current/customer_attraction/coverage_opportunity_counterexample.md)、[任意人数负前缀族](../current/customer_attraction/prefix_balance_family.md) | 总机会损失的望远镜恒等式保留 | 允许局部欠债，证明终局总余额；不再把全局任务加强为逐步非负 |
| 把末位最坏回复值或真正静态安全值作为每个人保底：[聚合末位值](../current/customer_attraction/aggregate_theta_counterexample.md)、[逐人安全值](../current/customer_attraction/individual_security_counterexample.md)失败 | 末两人保底及静态 \(v_m\ge\operatorname{OPT}_m/(2m-1)\) 仍可用 | 证明真实 SPE 的聚合支付，保留静态对手不观察抽样的量词 |
| 对全部查询分布要求去相关补偿：[全分布预算](../current/customer_attraction/global_security_budget_boundaries.md)失败 | 指定完整策略锥中仍有精确共同 (Q) 证书 | 允许依实例选择安全最优查询与共同静态竞争分布；固定策略锥已闭合时换策略 |
| 所有 (D_ige0)、弱局部 iid 漂移：[安全值链](../current/customer_attraction/security_chain_and_local_boundary.md)、[动态 iid](../current/customer_attraction/dynamic_iid_debt_boundary.md)失败 | 全路径债务恒等式、真实背景安全值单调嵌入仍成立 | 真正安全值总债候选仍需证明；iid总债上界已由§1.2反族否定，恒等式保留 |
| 每节点先平均全部偏离、固定深度权或规定静态运输核：[流模板](../current/customer_attraction/iid_security_and_flow_barriers.md)、[规定核](../current/customer_attraction/stationary_pair_transport.md)失败 | 未压缩的逐历史偏离矩阵、末两人循环运输证书 | 允许每个 ((h,a)) 单独乘子或新的跨节点机制；模板分离向量未必是 SPE |
| 五人的既定有限必要条件模板只调乘子：[索引松弛精确障碍](../current/customer_attraction/five_player_indexed_obstruction.md)仍最优于二以上 | 真实分支下的现有五人上界、可重用原始/对偶精确证书 | 增加本质不同的真实回复关系、策略一致性或换表示；LP 点不能冒充完整 SPE |
| 末回复规范化后固定早期乘子直接提升：[固定提升反例](../current/customer_attraction/terminal_tie_lift_obstruction.md) | 末行拆分和商空间提升接口；同实例可重选乘子成功 | 共同选择早期乘子与误差支付，不把一个固定证书失败扩大成一般不可能 |
| 用均匀大正偏置 Möbius 编译直接产生坏福利：[编译边界](../current/customer_attraction/compiler_security_barrier.md) | 完整历史的有符号表示与合法大偏置嵌入 | 正偏置会改善福利；较小合法偏置或另一真实构造须重新证明 |

重试前只需核对与你当前机制有关的一行及原反例，无需把全表当作探索前审批。新的想法可以直接尝试。工具失败、超时、数值未找到反例和多人赞同都不改变数学状态。


新增精确停界：[极端关联平稳支付§6](../current/customer_attraction/extreme_maximal_membership_floor.md)对private/co-singleton/global类型成立，但四极大2of4类型的无自环、平稳均匀示意菜单已有−1/8逐客户余项。该菜单没有完整SPE认证，不能否定一般theta或half；重试须增加真实后继选择、跨类型或更早中继信用，不能原样逐客户外推。

## 软水位不等于可信续局

[分数尾共同信用](../current/customer_attraction/fractional_tail_waterfill.md)已避开硬删除的纯deficit障碍，不能继续把硬删除反例当成软降权不可能。不过即使阈值取原实例真正安全值，原高尾保1的窄水位合同仍可能翻转原IC，甚至无法保留原实际叶为任何重选加权续局；[真实53客户族及独审](../workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round2/relay/review_waterfill_credibility.md)明确了范围。同一族允许高尾一起缩权则有全共同核心大小的正修复，故该失败不否定宽合同。

统一缩尾可以把单条原规定路径的累计IC失真合账到同终局背景返还，但不同改枝会重置终局；规范变分水位换根亦会重置支撑和对数基线。两份局部账均不能不经新不等式跨子树望远镜。一般half仍OPEN。

## 最优势增量不能直接给首位保底

新PI候选u_first≥P_(r+1)(b)−P_r(b)已被[完整三人SPE精确反例及独立盲审](../workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round2/mixed/review_pi_counterexample.md)否定：430单位客户，首位91，P3=329、P4=873/2。实际及全部真实根终局都达全局P3，故问题甚至不必来自尾部势效率；P_k最优值序列本身不凹。该例W265、OPT3=324，且全部根插入核项≤90<91，WP仍严格成立。此反例不否定half或更弱真正安全值接口。
