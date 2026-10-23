# Boss10：一般半覆盖的真实分支支付

目标 **Q-CAG-HALF** 仍 **OPEN**。采用 [CAG-MODEL](../../../current/customer_attraction/model.md)：有限单位客户、共同有限非空目录、任意人数、每个完整有序历史纯 SPE；重复、空主题、任意平局、零客户均保留。
本 clone 由附件程序恢复 main 后生成本目录身份，复用实际仓库状态；六名指定 gpt-6.1-sol ultra 研究员并行，root 独立检查及汇总提交。旧 Boss10 目录只作为已有资产来源。

## 已产生的数学认识

| 文件 | 数学资产、准确范围与读取时机 |
| --- | --- |
| [exchange/unique_optimum_omission_obstruction.md](exchange/unique_optimum_omission_obstruction.md) | **完整 SPE 反例，否定辅助桥。** 两人六主题71单位客户，实际 W35，唯一最优38，其中遗漏36>W35。因此即使允许选择最优组合/最大化实际交集，也不能要求遗漏由 W 单独支付。连续保护价格 B_D(16)=4>19−16=3。非 half 反例。 |
| [exchange/audit_unique_optimum_omission.py](exchange/audit_unique_optimum_omission.py)、[发现者冻结审计](exchange/unique_optimum_omission_audit.json) | 从单位客户定义核验七节点、42含自身比较、全部21主题对及唯一最优；有限完整证书用于反驳明确的全称辅助桥。 |
| [parent/audit_optimal_omission.py](parent/audit_optimal_omission.py)、[独立冻结审计](parent/optimal_omission_independent_audit.json) | root 仅见原始类型与策略陈述、未读发现代码的独立单位客户重构，全部精确核验通过。外审/新颖性未认证。 |

## 可扩展机制、精确局部正面式与反例

| 文件 | 数学资产、准确范围与接续 |
| --- | --- |
| [induction/two_player_full_terminal_pushforward.md](induction/two_player_full_terminal_pushforward.md) | **解析局部定理。** 任意合法背景、恰两人、任意根查询分布p，真实完整终局作为静态竞争分布时，原首人平均收益D与独立额外查询C满足 D−C≥Σp_x²/((b_x+2)(b_x+3))。仅末位BR足够；单客户空/非空目录取等。root及另一研究员独立重构。 |
| [independent_pushforward/two_player_pushforward_review.md](independent_pushforward/two_player_pushforward_review.md) | 未读发现稿的独立重建、加权BR余量和sharpness；局部正面式不能直接外推多后继。 |
| [representation/terminal_pushforward_D_lt_C.md](representation/terminal_pushforward_D_lt_C.md) | **强一般推送桥的真实反例。** 既有34客户三人例加空主题，完整57节点策略，D=29/30<C=41/40。实际根收益29/3，故弱C≤u仍未被否定。 |
| [parent/audit_integer_push_34.py](parent/audit_integer_push_34.py)、[独立冻结结果](parent/integer_push_34_independent_audit.json) | root只据原始客户类型与策略规则，独立展开34单位客户核验399含自身/342真正比较及D、C、W32/OPT34，不导入发现代码。 |
| [representation/weak_pushforward_individual_reduction.md](representation/weak_pushforward_individual_reduction.md) | **条件归约，非一般定理。** 若任意人数/背景/查询分布的弱C≤u成立，静态m槽安全值与共同目录预算给每人u_i≥OPT_m/(2m)，从而half。待支付真实后继的查询适应性。 |
| [counterexample/reciprocal_isolation_barrier.md](counterexample/reciprocal_isolation_barrier.md) | **任意k的架构锐障碍。** 双向隔离末位惩罚，实际C₁…C_k,D时，OPT/W≤(3k+2)/(2k+2)，旧3/2族逐k取等。只改组大小/公共池不能放大至half反例。 |
| [independent_no_go/reciprocal_isolation_review.md](independent_no_go/reciprocal_isolation_review.md) | 未读发现路线独立得到x_i≥v_i≥d≥x_i/2+y_i，核k=1、零实例、额外目录与非均匀等号。 |
| [counterexample/breaking_isolation_notes.md](counterexample/breaking_isolation_notes.md) | 撤销隔离后的跨分支逃逸缺额E给精确支付式及half反例必要阈值E>(k+2)d/3；多个相同追随者的简单方案也有参数冲突。此接口未被一般SPE自动支付。 |

## 当前真正缺口

早期偏离可以改变所有后继行动。一般跨真实分支福利支付尚未闭合；上述遗漏反例不反驳 OPT_m−W≤m u_i、均值价格桥、真正安全值聚合或主目标。
正在独立攻击：自由选择静态竞争分布的extra-one门槛、更早价格/弱机会缺口、全树客户共同表示、可信完整策略构造、合法背景不变量。强D≥C已失败，弱C≤u仍OPEN；两块复制的暂报阳性因混淆实际收益与额外插入分母被root否决，不能升级。
新推导会先标明 exact statement 和承重义务，成熟结果经独立攻击后再升级。

[精确账本](CLAIMS.md)、[当前义务](RESEARCH_STATE.md)、[失败机制](FAILED_ROUTES.md) 维护本桌面状态；共享 canonical 账本的状态没有因个人备份自动改变。


## 并行同证书与来源核对

同步公屏107后确认 Boss5 的 `R-171cd7d518434f36a48cd50df29c9303/global/optimal_omission_exchange_counterexample.md` 已保存相同71客户证书及参数族。本桌面的发现与root审计保留为独立重现/来源，不主张数学新颖性；正式整理应合并同一数学对象，避免复制共享正文。该核对不改变本证书的精确真值。

## 2026-10-23恢复的完整菜单边界

本clone保留原身份与未提交推导，恢复不算新发现。

| 文件 | 数学资产、范围与读取时机 |
| --- | --- |
| [counterexample/pure_full_root_menu_obstruction.md](counterexample/pure_full_root_menu_obstruction.md) | 八人八主题32单位客户完整DAG，根u=13/4而每个完整根终局都有额外查询37/10；否定纯列阻断。实际W=OPT=32。 |
| [parent/verify_two_block_dag.py](parent/verify_two_block_dag.py)、[独立结果](parent/two_block_dag_independent_audit.json) | 独立单位客户审计13872节点、59496含自身比较，覆盖全部2396745有序决策历史。混合菜单原始/对偶匹配值851/280<13/4。 |
| [exchange/full_menu_potential_rise_obstruction.md](exchange/full_menu_potential_rise_obstruction.md) | 24客户等势与791客户严格降势反例：额外插入超过根u不强制完整终局势上升；不再以标量势排序证明一般菜单。 |
| [tree/full_terminal_reply_column_identity.md](tree/full_terminal_reply_column_identity.md) | 任意剩余人数的联合势遗憾精确身份；恰两人可取裸回复值最大的纯列，一般多后继遗憾没有已证符号。 |
| [induction/full_root_menu_mixed_obligations.md](induction/full_root_menu_mixed_obligations.md)、[tree/full_terminal_menu_interface.md](tree/full_terminal_menu_interface.md) | 混合完整r槽菜单Mfull≤u的minmax/对偶及足够推出half的归约；候选仍OPEN，不与已失败的r−1槽菜单混同。 |
| [representation/meta_price_comparison_boundary.md](representation/meta_price_comparison_boundary.md)、[induction/tail_price_strengthening_counterfamily.md](induction/tail_price_strengthening_counterfamily.md) | 真实后继平均价格不能普遍替代最大查询价格；合法背景族与空背景两人族的范围分别保留。 |
| [tree/virtual_adjacency_handoff.md](tree/virtual_adjacency_handoff.md) | 单色后缀虚拟相邻税VA(r)仍OPEN；r=1可证，静态单色势上包络可证，但跨背景真实后继比较未闭合。 |

本轮六路探索写入round5_mixed/、round5_induction/、round5_credible/、round5_coupling/、round5_audit/、round5_global/；未自动成为已审结果。

## 本轮任意人数归纳障碍

[round5_induction/profit_bellman_counterfamily.md](round5_induction/profit_bellman_counterfamily.md)
精确计算既有完整SPE族的背景最优剩余利润：n≥4，
F_(n−1)(1_A)=2(n−1)(n−2)+(7n−13)/6。故系数二Bellman台阶对每个n≥5失败；
任何固定α<17/6也最终失败。此处F是剩余玩家总利润，不是旧总覆盖补全。
[root独立解析复核](parent/profit_bellman_family_independent_review.md)未读发现者消元证明，
从原始类型得到同一精确最优值；[独立有理回归](parent/profit_bellman_family_independent_audit.json)
枚举n4..8共15501个候选只核实现。原族全历史SPE引用已审现行正文。
新缺口是如何跨深度搬运真实尾部half裕量，不是简单逐步非负式。

[round5_mixed/replicated_menu_minimax.md](round5_mixed/replicated_menu_minimax.md)
给条件n块菜单的精确minmax；四块静态值会超过u，但
[round5_credible/last_low_cut_and_three_block_failure.md](round5_credible/last_low_cut_and_three_block_failure.md)
的单实现整数BI显示三块指定菜单已不能实现。通用last-low截断引理有解析证明，
[mixed独立局部审查](round5_mixed/three_block_last_low_witness.md)只核一个三剩余人代表，
不提升为全部截面独立核验。原mixed接口仍OPEN，条件矩阵不能当SPE反例。

## 本轮主认识：任何固定局部Bellman系数均不成立

更简单的已知all-big完整SPE族已将上述17/6障碍加强为**无界**，不应再把17/6当作尚待调整的候选常数。
[round5_induction/unbounded_profit_bellman_obstruction.md](round5_induction/unbounded_profit_bellman_obstruction.md)
与
[root独立证明](parent/profit_bellman_unbounded_independent_review.md)给：n玩家、
一个n客户主题A、n−1个不交singleton，每个历史全选A是完整SPE，u=1、W=n、OPT=2n−1。
背景一名A后，最佳剩余利润Ftail=2n−h_n，h_n=min_(j=1..n)(j+n/j)。
根台阶OPT−Ftail=h_n−1≥2√n−1，故任何固定局部系数均失败。
实际尾部额外half信用h_n−2恰好补偿根债h_n−3并留下全局余量1。
[独立回归代码](parent/audit_profit_bellman_unbounded.py)与[冻结结果](parent/profit_bellman_unbounded_independent_audit.json)
只核n2..8实现；全n结论来自两份独立解析重构。

[round5_coupling/common_customer_covariance_and_stationary_obstruction.md](round5_coupling/common_customer_covariance_and_stationary_obstruction.md)
记录另一指定核边界：三人6286客户完整SPE的唯一source→uniform终局槽stationary分布，
仍被一个transient查询超根u达123/4；[独立单位审查](round5_audit/stationary_column_candidate_review.md)
核验全部258含自身比较。多个纯列安全，故只否定该stationary选择，不反mixed。

[round5_global/monochrome_dominance_and_va_localization.md](round5_global/monochrome_dominance_and_va_localization.md)
给静态单色弱支配、动态势最大反例、VA真实剩余税，以及M=u_A−q(B)=0时
所有查询q(T)≤u_A的解析端点；root已独立重构。福利推论不声称新已知范围；M>0一般仍OPEN。

当前下一步必须提供非循环的跨深度信用状态，或直接支付真实跨分支损失；
既有局部常数、stationary固定核、块复制表均不能承担该义务。无一般证明或half反例。

[round5_induction/credit_state_obligations.md](round5_induction/credit_state_obligations.md)
再定位一个受限信用模板障碍：若C=sum f_r(b_x,c_x)为实例无关的逐客户可加式，
并只计背景与tail共同覆盖客户（f(0,c)=f(b,0)=0），两个完整SPE无限族
对同一f_(n−1)(1,n−1)强制冲突上下界，n≥16即矛盾。root已独立推导。
此结果不能扩张到有独占项、主题/实例信息或非可加信用。
