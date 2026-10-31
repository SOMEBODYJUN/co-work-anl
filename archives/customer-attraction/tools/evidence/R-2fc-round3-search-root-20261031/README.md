# R-2fc round3 search root（2026-10-31）

本批由 Boss2 逐源实读并复放七个 `round3_search` 导出：三份 `.best.json` 完整历史纯 SPE 证书、三份同实验的有限锥扫描报告、以及一份六记录 `unit_point_audit.json`。原始来源通过 `clean show` 导出到 `source/`，标准元数据和本地字节核对见 `source-manifest.json`。

## 精确核验

`validate_search.py` 用 `fractions.Fraction` 重算顾客覆盖、终局客户价值、所有有序历史的当前动作与每个单步偏离，并穷举有限实例的终局最优值。`validation.json` 全部通过：

- `m5p7_pos1.best.json`：五人七主题，`W=6`、`OPT=9`，实际路径 `(0,2,0,0,0)`，19607 个比较，最小松弛 0；
- `m5p7_pos2_multi.best.json`：五人七主题，`W=5`、`OPT=9`，实际路径 `(0,0,5,0,0)`，19607 个比较，最小松弛 0；
- `m5p8_pos0_multi.best.json`：五人八主题，`W=6`、`OPT=9`，实际路径 `(0,7,2,2,0)`，37448 个比较，最小松弛 0；
- 三份扫描均标明有限步数/固定种子与“缺少反例不构成证明”；六条 unit-point 记录均为完整历史 SPE、无偏离违规，`2W>=OPT`。

这批提供的是有限实例证书和搜索边界。它不能推出六人模型的普遍半最优定理，也没有把搜索中的候选当作证明。三份 `.best.json` 的终局覆盖率相对其各自 `OPT` 都为 `9` 的目标比值记录；半值检查由精确 `2W>=OPT` 完成。
