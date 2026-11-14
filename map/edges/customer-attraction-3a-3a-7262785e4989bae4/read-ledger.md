# M-63c882b0c8414805a43d4d8d4e43f4e3 阅读账本

任务：`customer-attraction-3a-3a-7262785e4989bae4`；对象 pin：`403896c58e3ef32a0658cf8f47cd52451777da770e2e6a2dbb15cd3345668f6e`。

完整正文与证据按 task 的 18 个 reading pass 顺序核对；大 JSON 以字节哈希、结构字段、全列/全行计数和 Main PASS 报告复核，未把有限 LP 当作 SPE 证明。

| pass | path | declared span | bytes/SHA check | 读后核对 |
|---:|---|---|---|---|
| 1 | `archives/customer-attraction/state/引理/共享真实末端的独立初段与折扣尾闭包--引理.md` | L1-162 (chars 0-6396) | 11579 bytes; sha=885e0c46d9b44ecdefa438d6df7dd04e796da94da20030daf302c34fae15a124 | 式(1)-(8)、V=C_h(C_h(T))、共同 v 取 min、边界与下一桥。 |
| 2 | `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md` | L1-129 (chars 0-4094) | 7598 bytes; sha=cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88 | 有限 N/S、完整有序历史纯 SPE、弱 IC、重复/空覆盖与平局域。 |
| 3 | `archives/customer-attraction/state/引理/同源双末对跨枝配对与严格联合投影--引理.md` | L1-355 (chars 0-11108) | 19294 bytes; sha=7547538073d8edf42f2430c5ed0d4139c2129fdaa8817ea0dbcba591552328e5 | 34+PAIR 初段与共同隐藏域；PAIR 自交 E[x_Q^2]=E[x_Q]。 |
| 4 | `archives/customer-attraction/state/引理/同源真实末回复的折扣闭包与二状态精确投影--引理.md` | L1-276 (chars 0-8679) | 15573 bytes; sha=a2aa6f407865993f693ff8338e2c038a7849643d04ed9078fc7c8e0e6f6b5d42 | H_beta、Bellman 三候选、有限目录最大值闭包；同源尾预算。 |
| 5 | `research/workspaces/six-boss2-20261111-cross/coverage_bridge/formal_prefix_tail.md` | L1-148 (chars 0-5936) | 10771 bytes; sha=30d85aeb7d325436bce1de1975ef131d0bbeb0c07f2f8f130e828cd747b1bcda | 正式组合定理复述与有限 5752 证据边界。 |
| 6 | `research/workspaces/six-boss2-20261111-cross/coverage_bridge/selected_prefix_tail_5752.json` | L1-10965 (chars 0-193841) | 193841 bytes; sha=595e7386cfacc591f513fe477453e94d9e2271e4cb63ce3f5c57a8dc34fabd50 | scope=not SPE；16 unique vectors、4849 columns；12 beta 非零、4 beta=0。 |
| 7 | `research/workspaces/six-boss2-20261111-cross/coverage_bridge/prefix_tail_requery.py` | L1-149 (chars 0-8079) | 8079 bytes; sha=bec483fbce411889ee872ccae873fc6395d9d69f487bd60acde5137f2bcf27f7 | 独立 alpha+beta LP 发现器；共同预算归一 alpha_T+alpha_C+beta_source=1。 |
| 8 | `research/workspaces/six-boss2-20261111-cross/coverage_bridge/compact_prefix_tail_cuts.py` | L1-50 (chars 0-3276) | 3276 bytes; sha=3e145aa01fd46739c1521d8ff66f89eb770b679b2fe286dd4800893f8c2151e5 | 共同分母有理压缩；逐列重算 row/slack。 |
| 9 | `research/workspaces/six-boss2-20261111-cross/coverage_bridge/prefix_tail_beta_zero_audit.json` | L1-18 (chars 0-417) | 417 bytes; sha=23a46e86e7f0ab71b4e443c59eada7e296e774c9b702ef1524e1f9d05732cddc | columns=4849，all_equal=true，delta=3/4；beta=0 嵌入精确。 |
| 10 | `research/workspaces/six-boss2-20261111-cross/joint_requery/portfolio_master.py` | L1-184 (chars 0-10566) | 10566 bytes; sha=af8b0a9251d3b42f623ac37fe980235d7b66f3d2f481855174d68b843d99bed3 | 17-query joint portfolio；60 internal + 16×17 query features；不造 SPE/half。 |
| 11 | `research/workspaces/six-boss2-20261111-cross/joint_requery/explore_projection.py` | L1-170 (chars 0-7561) | 7561 bytes; sha=f64d1d08dc52b935432c993d6712a1888dccea216f737a2d5e3cdc4c175b55da | shared-C two-branch local LP；diagonal pair 用 x 而非均值平方。 |
| 12 | `research/workspaces/six-boss2-20261111-cross/joint_requery/separate_master.py` | L1-141 (chars 0-7716) | 7716 bytes; sha=20ccb2656d736e7754a9c79ef9d030358ab2534bd8b14a4b4b6d8726803709af | 逐 query exact rows；six actual indices/all 16 shared states。 |
| 13 | `research/workspaces/six-boss2-20261111-cross/master_cuts/dynamic_5752_exact.json` | L1-39517 (chars 0-592567) | 1535384 bytes; sha=791cbcba1afd841eabe3bc908b300083822739fd8f7ed8b85a8c7ff06f28c787 | exact_feasible=true；verified_rows=5752；4849 columns；exact_optimum_claim=false。 |
| 14 | `research/workspaces/six-boss2-20261111-cross/master_cuts/dynamic_5752_exact.json` | L39518-73327 (chars 592567-1133094) | 1535384 bytes; sha=791cbcba1afd841eabe3bc908b300083822739fd8f7ed8b85a8c7ff06f28c787 | exact_feasible=true；verified_rows=5752；4849 columns；exact_optimum_claim=false。 |
| 15 | `research/workspaces/six-boss2-20261111-cross/master_cuts/dynamic_5752_exact.json` | L73328-99180 (chars 1133094-1535384) | 1535384 bytes; sha=791cbcba1afd841eabe3bc908b300083822739fd8f7ed8b85a8c7ff06f28c787 | exact_feasible=true；verified_rows=5752；4849 columns；exact_optimum_claim=false。 |
| 16 | `research/workspaces/six-boss2-20261111-cross/main_pair_features.py` | L1-23 (chars 0-1346) | 1346 bytes; sha=177057776f9aa3322f907ce073511eb7ef491774fc0871b11fd0c367c833b1ac | 独立 Pair feature identity；预算/交叠项。 |
| 17 | `research/workspaces/six-boss2-20261111-cross/main_verify_prefix_tail_5752.py` | L1-95 (chars 0-5767) | 5767 bytes; sha=989e87e6e799ff81faaca2ba88f0137ee08297300974891053127266c042a875 | 独立四确定策略线性方程、joint/separate/gain exact asserts。 |
| 18 | `research/workspaces/six-boss2-20261111-cross/main_verify_prefix_tail_5752.json` | L1-233 (chars 0-18661) | 18661 bytes; sha=207d0eaeb8b260931d680b05f3db36a1e60754b910cc5fdf3ee331486238d201 | status=PASS；独立 literal-index/shared-v/Bellman 审计；16 rows。 |

## 结论

- 核心正文的普遍结论是 (7)：初段 alpha 与同一真实 V 上的折扣尾 beta 合同共享 `v` 后相加，再对 `(b,c,j,v,s,s')` 联合取 min；全部源/末价/容量预算相加。
- 固定 5752 点有限证据由 `selected_prefix_tail_5752.json`、`dynamic_5752_exact.json` 和 `main_verify_prefix_tail_5752.json` 共同支付：16 条精确负行，12 条 beta 非零且 `separate_slack >= 0 > joint_slack`，4 条 beta=0 只恢复旧投影；不外推全锥严格包含、完整 SPE 或六人 half。
- 现役 canonical 边已完整支付与 M-b233ef00a9c34e189817cdfb7a495107、M-e394b173b9b1419588c6c380da4bd326 的共享末端组合；本任务不重复造同端点边。
