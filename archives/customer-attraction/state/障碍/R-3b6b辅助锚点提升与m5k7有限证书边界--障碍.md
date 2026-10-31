# R-3b6b 辅助锚点提升与 m5k7 有限证书边界

- **稳定 ID**：R-3b6b-counterexample-20261031
- **类型**：障碍（辅助桥、有限候选、反例边界）
- **来源**：八源，完整清单见 `archives/customer-attraction/tools/evidence/R-3b6b-counterexample-20261031/source-manifest.json`。

## 锚点提升族：完整历史但仍高于半值

`anchor_lift_audit.py` 定义一个含 A/B/T/D/E gadget 与额外 private anchors 的辅助 sequential coverage 桥。策略由计数状态给出；脚本对每个计数状态比较当前动作与全部其他动作，终局再按每个有序历史展开，因此不是只检查一条路径。`--max-players 7` 的 12 条输出与冻结 `anchor_lift_exact.json` 完全一致，最小 scaled slack 均为 0（任意平局保留）。

AB 分支 `m=2..7` 的 `(W,OPT)` 是 `(9,10),(13,14),(17,18),(21,22),(25,26),(29,30)`；DE 分支是 `(8,10),(12,14),(16,18),(20,22),(24,26),(28,30)`。m=7 AB 的 `last_threshold_violation=1` 记录了辅助阈值的另一尺度，不代表 `W<OPT/2`；实际 `29>15`。这族可作为后续比较“完整历史纯策略证书如何仍留下接近最优但非最优路径”的控制样本，不能直接当作当前六人 CAG-HALF 反例。

## m5k7 精确 SPE 点

`certified_m5k7_maximal.json` 给出五玩家、七主题的完整动作表和终局计数。独立定义级 verifier 逐一检查 2801 个决策历史和 16806 个单步偏离，得到 `W=1000`、`OPT=1800`、比值 `9/5`，且终局计数与声明一致。这是一个固定实例的完整纯 SPE 证书；它满足 `2W>OPT`，所以不是半值失败。源状态本身标注“exact SPE point; finite search only”，不能把有限搜索当作全称结论。

## 浮点候选和恢复边界

`last_share_m5k7.json` 明确标注 `floating candidate, not certified`，含 1399 行的浮点锥候选、352 个 prefix/target/action 条目及 `ratio≈1` 的记录。运行 `certify_candidate.py` 后，脚本用候选的有理支持等式恢复整数客户多重集，并对完整策略调用定义级 `verify_certificate`；得到 `W=3, OPT=3, ratio=1` 的精确点，2801 历史均通过。这个结果说明浮点候选必须逐点做有理恢复和完整回放；不能把源文件的浮点比值直接写入结论。

`fork_family_search.py` 的参数网格（5 players, 2 forks, 4 branches, `a,p` 步长 0.25）运行到最佳浮点 ratio `1.7`；`cone_search.py` 的固定 seed smoke（topics=7, players=5, starts=2, steps=2）运行到最佳浮点 ratio `1.8`。两者只生成 LP 支持/延续候选，未证明这些点有完整 SPE；本批保留它们的搜索机制和失败边界。

## 与当前 CAG 目标的接续

这八源研究的是 R-3b6b 辅助桥和五人七主题 sequential coverage 搜索。当前任务要求六人 SPE、六提供者、完整有序历史、目录客户子集、覆盖者间均分价值。没有证据把本批辅助 gadget、浮点锥或 m5k7 证书迁移到该量词；空主题、重复、零客户、离轨历史与任意平局仍需在目标模型内独立处理。后续可用 m5k7 证书的全历史 verifier 作为六人候选的回放模板，并以有理恢复后 `2W>=OPT` 为最低验收项。
