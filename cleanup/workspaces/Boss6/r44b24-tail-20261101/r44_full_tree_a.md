# R-44b24 full_tree 前四源实读审查

执行者：并行 full_tree_a；工作树：Boss6 当前 `rebuild/research-v2` clone。四源均通过 `work.py clean show` 导出，按冻结 SHA/字节核对；未修改共享 clone、未登记 done。

## 实际验证

- `b2cc74c6caa0cb212eb3` (`audit_lattice_circulation.py`, 5825 B, SHA-256 `5b38838085c1ece4ba669880aeaf24c06433d0f387abc8e5c9dc6fd535fd5693`)：用隔离导出脚本直接运行，退出 0，输出 `status=passed`；15 单位客户、13 有序历史、39 action comparisons、W=13、OPT=15、payoff-SCC rank=1、SCC+root-row rank=2。脚本自足使用 Fraction，不导入 solver/规范包；检查三标签三角回归、势端点零和、唯一非平凡 SCC、四行相消和所有真实 slack。有限审计不构成一般 half 证明。
- `3fd2ed1ea60aaf51a547` (`audit_truncated_moments.py`, 8252 B, SHA-256 `eae0e1151d35f4196f8f44a576afa257e433ed663a66d35d1769374de83e2bb`)：隔离运行退出 0，输出 `status=passed`；Möbius/payoff rows=1008，检查 p=1..6、m=1..4 的有限行/秩、奇偶核、四组非负压缩、矩非法余量 `7/10`，二次正点 `{010,101}`。其一般结论承重在 `truncated_intersection_moments.md` 的解析证明；本程序是有限审计，不做 SPE 全策略枚举或 half 证明。
- `3fb17764a6930667e3a2` (`count_lattice_circulation.md`, 7624 B, SHA-256 `a4eed1963bae2ce20c13192b5aa7a7c887e31e0b6dcd93d6b7ca91ceb432c918`)：全文读完。核心是任意完整策略真实收益行的两层计数势端点配平机制；给出三标签六边恒等式、15 单位客户/3 主题完整 13 历史纯 SPE（重数 `(3,2,3,2,3,1,1)`）、四条真实行逐类型零和、唯一非平凡 payoff SCC 与严格扩张；明确 Q-CAG-HALF 仍 OPEN、不得把 lineality 自由度升级成全称福利付款。文稿本身是发现稿/自足数学说明，相关精确实现与输出在 `b2cc...`/`0d2...`。
- `279a9b74712bc014f2ab` (`full_tree/README.md`, 1738 B, SHA-256 `da0cb644901cc8bbe62a1970055efb23b4b0b65d1fbcf631e3aed43119914b9e`)：全文读完。纯导航资源，列出 `truncated_intersection_moments.md`（截断矩表示/压缩及奇偶核）、`count_lattice_circulation.md`（真实行势循环/严格 SCC 扩张）、两个候选探针及三类缺口；明确一般 half OPEN、低阶矩不等合法非负坐标、不得把浮点探针当证明。

## 全仓比较和已有去向

1. 截断矩三源：`archives/customer-attraction/subarchives/six-providers/state/审查/截断交集矩的有限差分重构与保策略压缩--审查.md` 已逐项保留发现稿、发现审计和报告的差异（1008 有限 rows、奇偶/压缩、非法矩与 cylinder 边界），并由 `archives/.../tools/evidence/truncated-moments-independent-review-primary/comparison-source-manifest.json` 原字节保存这三个 source。`archives/.../state/资源/截断交集矩独立全收益审计与显式压缩--资源.md` 也列出三源的完整阅读边界和运行合同。
2. 势循环三源：`archives/customer-attraction/subarchives/six-providers/state/引理/两层计数势端点配平的真实行双向支付--引理.md`、`state/构造/十五客户完整策略的势循环严格扩大收益SCC空间--构造.md` 已吸收一般机制与 15 客户实例；`state/审查/计数势格循环的独立Floyd审计与冻结证据--审查.md` 已准确区分发现脚本和独立 Floyd 实现的 finite scope。原字节已在 `tools/evidence/lattice-independent-review-primary/related/` 与 `tools/evidence/two-lineality-discovery-probes-primary/original/...` 保存。
3. `full_tree/README.md` 的导航和缺口已被 `archives/customer-attraction/state/资源/R44b24研究入口的条件结果与恢复边界--资源.md` 吸收（该资源明确把 full_tree 两份资产分别路由到上述定理/审查对象，且保留不把入口当证明的边界）。目前没有独立 canonical theorem 需要新增。

## 逐源处置建议

- `279a9b74712bc014f2ab`：`integrated`；目标 `archives/customer-attraction/state/资源/R44b24研究入口的条件结果与恢复边界--资源.md`。理由：导航路线、候选/缺口和“不得升级”边界已完整吸收；若 receipt 要求原字节路径，可附 `archives/customer-attraction/subarchives/six-providers/tools/evidence/r44b24-full-tree-entry/original/.../full_tree/README.md` 的保全目标（当前资源页是数学/治理去向）。
- `b2cc74c6caa0cb212eb3`：`integrated`；目标 `archives/customer-attraction/subarchives/six-providers/state/审查/计数势格循环的独立Floyd审计与冻结证据--审查.md` 与 `state/构造/十五客户完整策略的势循环严格扩大收益SCC空间--构造.md`。理由：发现审计的 111 三角/秩/势端点/39 slack 范围已经与独立 Floyd 的 13/39/15/13、SCC rank1→2 明确分层；原字节已保留，不能再把它算作独立 Floyd primary。
- `3fb17764a6930667e3a2`：`integrated`；目标 `archives/customer-attraction/subarchives/six-providers/state/引理/两层计数势端点配平的真实行双向支付--引理.md` 与 `state/构造/十五客户完整策略的势循环严格扩大收益SCC空间--构造.md`。理由：发现稿的解析机制、三角恒等式、15 客户构造和 half 缺口均已自足吸收，原稿已在 lattice review related evidence 保存。
- `3fd2ed1ea60aaf51a547`：`integrated`；目标 `archives/customer-attraction/subarchives/six-providers/state/审查/截断交集矩的有限差分重构与保策略压缩--审查.md` 与 `state/资源/截断交集矩独立全收益审计与显式压缩--资源.md`。理由：发现者实现的 1008 rows、Möbius 最高阶、奇偶/压缩、非法矩和二次局部边界均已与独立审计逐项比较；源本身作为 comparison-only 原字节保在 related-original，不能借有限程序宣称新定理。

以上四项均为“正文/证据已有正式去向”的语义处置，不代表六人半覆盖已解决；所有弱平局、重复主题和有限/解析范围边界应保持。
