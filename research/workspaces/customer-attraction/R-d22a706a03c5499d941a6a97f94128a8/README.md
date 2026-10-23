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
