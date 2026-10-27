# research_5 最后接续状态与最小重放包

**Q-CAG-HALF-6 仍 OPEN。** 本轮没有六人全类型半覆盖证明，没有原模型完整 SPE 反例。
本页给最后真实阶段，先前 README/cross_source/combined_branch_master 的阶段证据继续保留各自范围。
没有把固定旧支撑坏点、凸会员抬升或浮点不可行当作主目标答案。

## 最后稳定的显式联合点：5277 行

`coupled_latest_exact.json` 为 5277 行、2033 列必要图的精确点，230 正列，全部 Fraction 行余量非负、最小 0，
`O=1`，

`W=269468671081390973287603081586427543021284243/551682258751855243720540411834195825411675776≈0.4884490425540351<1/2`。

入口 `coupled_latest_master.py --verify` 依次合并：

- 本目录 `combined_branch_master.py --latest --local-v2` 的旧 Ti 显式第四位枝图、全部冻结已选 priced/portfolio/requery 行、actual2/3/4→actual末 B 的三条全域投影；
- research_2 的 actual4→B 真枝 Q/R/ell 条件状态，以及与旧 Ti/Bi/Ci 直方图的双向报价和 marginal 等号。

`joint_local_v2_cuts.json` 冻结 5 条本地 forced-new-reply 三人枝投影、5 条同源 reply-requery 和 8 条新容量 portfolio。
这 18 行与显式 B 枝在同一点共同满足；W 与 research_2 的较早5259点相同，不能归因于这18行抬高了它。
本地5行的发现器虽容许 inner-middle IC，保存乘子在该 inner IC 上均为0，不能声称新内层最优性起作用。

### 已知新合法行严格切掉此点：B 菜单 Y_i 的 actual末价

令 `Y_i=σ6(h,B,T_i)`，即 actual4→B 真枝第五位强制 T_i 后的真末回复。
实际原末位可合法查询每个 Y_i，因此一定有

`6u6−Σ_i P_actual(Y_i)≥0`。

在条件状态中 `ell=Σ_i1_Yi`，此行可精确读为 `6u6−Σstate ell/(1+actual前五负载)`。
本 5277 点的值为

`−37649034345157581458948354799628857270185177/275841129375927621860270205917097912705837888≈−0.13648810976933004`。

记录在 `B_menu_actual_last_price_check.json`，独立定义级重放 `check_B_menu_actual_last_price.py`。research_2 已确认此普通菜单报价尚未加入本旧图。
因此5277点只能说是**原先明确列出的未闭包图**的精确停止界，不能叫 actual末价完整闭包，更不是 SPE。
本轮在父方停止新轮指令后，没有为这条新行开启新的优化。

另外 research_3 在同一5277点（SHA-256 `303291e7ec19437d226bb8d33d3e689beaf54f52103fde53a12e28f1058f806a`）
精确发现3条新的已有terminal-portfolio方向和2条已有same-source requery方向，
统一保存在 `research_3/coupled_pending_cuts.json`。它们尚未共同重优，
所以本5277点也不声称这些通用参数族已经闭包；下一次接续应先联合这些已知行和Yi菜单普通价，
而非把本点继续叫最新完整价格闭包。

## 最后已精确验证的全 Z 互查/新新 PAIR 联合阶段

`pair_master_exact.json` 是较早 actual 边缘上的10344行完整条件cube点，
入口 `pair_closure.py --master --verify`。
它含旧5108 master加全部 Z→Z、actual强PAIR(R,Z)/PAIR(Z,Z)，
364个Z质量、2528个min交叠，80个自由顶点变量精确恢复，最小余量0。
它的 W 是较早

`7788343487189316604380335059457339/16141009471373384499891913301798724≈0.4825189837724959`。

此阶段**没有**后来5277显式 B 条件状态和新增相应价格/投影，不能把10344与5277两个点免费视作同点。

## 固定5277 R阈值的真正跨新枝实验：只有浮点子支持结论

`cross_branch_slab.py` 固定5277的旧hist质量和R共同阈值模式；每个R slab再分8个actual-B状态α，
每个Z会员拆成条件质量β≤α。这样Q/R与所有新R/Z的共享身份完整保留，而非假设任意pairwise矩共同可实现。
新增两类行：

- 24条：B枝Q安全查询oldR/Z，B枝真末R精确查询oldR/Z，旧R/Z真末反向精确查询B枝Q/R，按3个族/对角轨道分别合账；
- 72条：B枝真实末两人strongPAIR(newR/Z,六actual或wi/wj六旧主题)。

同时仍保留全部Z→Z与actual strongPAIR(R,Z)/PAIR(Z,Z)。ZZ交叠在每个α-sector只以非负系数进入，可统一取min并由条件嵌套Z实现。
完整模型为41649行、19424变量，其中2608为α/β核心质量。

同一固定R支持的浮点消融如下（`cross_branch_slab_ablation.json`）：

| 所加新cross族 | 行数 | HiGHS浮点可行性 |
| --- | ---: | --- |
| 全24报价＋72 B枝PAIR | 41649 | 不可行 |
| 两类新cross都去掉 | 41553 | 可行 |
| 只加24报价 | 41577 | 不可行 |
| 只加72 B枝PAIR | 41625 | 可行 |

这只把该固定R实现的阻碍定位到24报价族。**没有恢复精确Farkas证书，没有验证两个浮点可行点为精确有理点，
也没有检查所有R联合分布/所有旧直方图/全部原模型SPE。** 因此不是无条件行锥不可行性、不是5277粗点全域不可实现性，更不是half证明。
该实验亦尚未补上述Y_i普通actual末价。无新优化在后台继续。

## 原模型种子已交完整BI，结果不是反例

`materialize_diagonal_seeds.py` 从10344阈值构造精确取18主题子目录：6actual、6Ti、6对角R或Z。
输出 `seed18_Rdiag.json`（252客户类型）和 `seed18_Zdiag.json`（288类型）及meta。
删其他目录动作后不继承旧SPE。Ti六主题覆盖全部客户，故OPT6严格等于总客户数。
research_1 已完成两实例的完整精确任意历史BI：各只有一个根SPE终局、福利等于OPT，ratio1。
所以没有目标反例，也不继续追这些seed的小常数。

## 最小精确重放依赖

对最后5277点，只需以下新文件加仓库既有c4f graph源与其冻结旧输入；不需要任何npz、float状态、扫描日志或LP发现输出。

本目录：

- `coupled_latest_master.py`, `coupled_latest_exact.json`；
- `combined_branch_master.py`, `joint_local_v2_cuts.json`, `nested_reply_projection.py`；
- `cross_source_graph.py`, `split_basic_graph.py`。

research_2：

- `coupled_B_branch_master.py`, `max_branch_lp.py`（只调用branch_rows）；
- `tail3_B_projection.py`, `early_B_projection_certificate.json`。

research_3：

- `all_reply_actual_floors.py`, `old_query_reply_cuts.py`, `old_query_cuts.json`；
- `mixed_pair_reply_rows.py`；
- `continuous_old_query_cuts.py`, `continuous_old_query_cuts.json`, `continuous_refinement_cuts.json`；
- `terminal_portfolio_cuts.py`, `terminal_portfolio_refinement_cuts.json`, `terminal_capacity_refinement_cuts.json`；
- `early_reply_requery_cuts.py`。

对旧10344点，再需本目录 `pair_closure.py`, `zz_threshold_closure.py`, `combined_branch_master_exact.json`, `pair_master_exact.json`。
它的入口不用`--latest/--local-v2`，所以不读后来新cut。

跨新枝浮点模型/消融只需另外保存 `cross_branch_slab.py`, `cross_branch_slab_status.json`, `cross_branch_slab_ablation.json`，
不保存其临时npz。它们是明确失败范围和可接续模型，不提升任何数学主结论。

局部多查询投影独立审查：`review_terminal_portfolio.md`, `.py`, `.json`；
一般恒等式与K预算系数通过，28,800次字面Fraction恒等式与3,360次literal/count最小值通过，
不声称第二份完整图实现或外审。
