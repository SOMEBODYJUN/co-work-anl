# research_3：本轮稳定交接

## 主目标与停止状态

Q-CAG-HALF-6 仍未解决。本目录没有任意目录六人半覆盖证书，也没有原模型完整有序历史 SPE 反例。下列行保持单位客户、单位提供者、共同目录、重复/空主题、全部离轨有序历史和任意平局。

已停止运行与开新轮。本目录最新自有稳定必要图是 **5112行、1905列、固定旧16直方图支撑**；更晚联合点由 research_5 管理。所有低福利点只是否定各明确必要行系统的充分性，不能称 SPE 或全域福利界。

## 唯一正文和数学增量

| 对象 | 正文、实现和准确状态 |
|---|---|
| 实际源对旧 B_i/C_i 的14基本行独立审查 | cross_source_basic_review.md；audit_cross_source_basic.py。十二安全floor及两容量，43,918次扩大域 Fraction 系数比较通过。未审原图或960投影。 |
| 实际源对新 R_e/Z_e 的36安全floor | new_reply_floor_rows.md；all_reply_actual_floors.py 的 added_rows。真实源 IC 求和，保留原1905 joint状态。作者解析/精确计算；不是新福利界。 |
| 新R/Z与旧已知主题的实际强PAIR | mixed_pair_reply_rows.py 的72行。六actual及两边wi/wj六bit；不冒称包含所有第三索引。old_query_cuts.json 的8行只是这批PAIR的历史重复，**仅因冻结行序依赖而保留，不是独立数学资产**。 |
| 同一真末回复的查询组合与actual价/共同容量 | shared_terminal_portfolio.md；terminal_portfolio_cuts.py。先合查询再min，含alpha/beta成本。research_5/review_terminal_portfolio.md 为独立局部审查；它审13Q恒等式/读出，不审参数LP、全5112图或SPE可实现性。 |
| 既有同源再查询的权重化与新R/Z应用 | weighted_early_reply_requery.md；early_reply_requery_cuts.py。源两IC同一历史，跨枝C/B身份保留；并非新均衡机制。14条负行在early_reply_requery_master_all_queries.json；最新共同点上的2条见pending包。作者解析及逐行Fraction核负；未记录独立完整实现审查。 |
| 同源全后继平均利润运输 | stationary_successor_transfer.md；replay_stationary_successor_transfer.py。一般kappa_r粗支付，父方独立核代数、2880型复算；不把平均后继利润认作实际利润。粗递归不足half。 |

## 最新自有稳定精确点

terminal_capacity_refinement_exact.json 保存：

    W=26911257633451032175939863641789509856404
      /55504137385384445932790297169434443345065
      ≈0.484851380476321,
    O=1.

这是5112条必要行上的精确可行点。逐列非负、归一化、全部行及W均由 Fraction 核验。没有独立整图实现审查；浮点LP只找参数和候选点。

最小重放命令（仓库根；D为本目录）：

    python ${D}/refine_terminal_portfolio.py --capacity --verify

本目录直接依赖：

- all_reply_actual_floors.py、mixed_pair_reply_rows.py；
- old_query_reply_cuts.py 与 old_query_cuts.json（保留冻结8个历史重复行的行序）；
- continuous_old_query_cuts.py 与 continuous_refinement_cuts.json（32行）；
- terminal_portfolio_cuts.py、terminal_portfolio_refinement_cuts.json（8行）、terminal_capacity_refinement_cuts.json（29行）；
- refine_terminal_portfolio.py 与 terminal_capacity_refinement_exact.json。

外部原图入口：research_5/cross_source_graph.py → split_basic_graph.py → 旧 R-c4f1ef099fad483c9f81283b61eb0b53/six_astra/attractive_nested 图及其既有依赖。重放5112点不需要重新运行任何参数发现。

research_5 的联合master另外读取 continuous_old_query_cuts.json 的64个早期连续priced行，因此该文件及其row实现也保留，不应因自有5112点只需32后续行而删除。continuous_refinement_exact.json 被其 tail_reply_subset.py 用作默认分离源，亦保留。

所有已被research_5使用的32/8/29 frozen cuts及其系数合同未改。terminal_portfolio_cuts.py 后续支持16项查询时，旧mu13只读取原前13项，系数严格不变；新三项仅为剩余索引T/B/C的合法查询平均。

## 最新联合点上尚未合账的5条真行

coupled_pending_cuts.json 绑定 research_5/coupled_latest_exact.json 的SHA256。该源为5277行、2033列的联合必要点，W约0.48844904；准确W与来源路径在包内。

包内有3条旧13Q价/容量投影（terminal_portfolio_cuts.row）和2条同源再查询投影（early_reply_requery_cuts.row）。每条均在完整2033列上独立调用row重算且Fraction严格为负；新增实际B分支状态列系数为0，未偷换新主题身份。

**这5条尚未共同重优化，不存在本目录对应的新稳定点。** 它们不是新17Q查询机制：priced3条只使用旧Q，已回写mu13避免引入重复读出模块。父方或接续者可合法加进同一master，再重新核验；不得提前把5条局部分离说成half证书。

## 已停止的未完成方向

保留已知(r,z)的k2同菜单R→Z→Y投影、13Q以外第三索引菜单、以及maxH双分支+全actual报价的单次定向探测未带来额外负行；空输出和重复发现日志已清理，不作为成果或精确不可能性结论。

一个尚未实施、未经核验的后续想法是让 forced T 分支的真正倒二者改选T，得到同一中间前缀下的 (T,T,Y)；保留中间负载s共享，用真实倒二IC而非另一根reset支付差。此仅是接续想法，不加入任何证书、代码或主张。父方要求收束后没有启动该步。
