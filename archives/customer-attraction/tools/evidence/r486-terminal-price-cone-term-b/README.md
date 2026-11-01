# R-486 终局价格锥与均匀三二乘子证据

本目录保存 Boss4/term_b 对五个冻结源版本的原始副本、依赖闭包中的重放输出和有理数复核。源版本仍以 `cleanup/sources.json` 及 `clean show` 的冻结提交为准；这里的副本只用于可审计复现。

## 冻结源

- `frozen/four_price_report.json`：`1f25e00563e542a1bbcf`，四提供者、六主题、300 次有限锥攻击的报告，`best=-0.0`，无正候选。
- `frozen/probe_four_price.py`：`a3103150d7c386262951`，seed 602617、300 次四人探针。
- `frozen/probe_three_price.py`：`3c0f253d9e2445d8c37f`，seed 602617、150 次三人探针。
- `frozen/search_mass_two.py`：`7641c0935736b85063fc`，调用冻结的 weak-row helper，在 `pbg=0,...,100` 上累积有限行并分别测试 `discounted`/`W` 右端。
- `frozen/search_uniform_mass_three_halves.py`：`356aa43321c1e2e70c15`，`tau=3/2` 的 5-bit、五个 `(d,l)` 状态和四阶 p 差分有限系统。

`search_mass_two.py` 的 helper `three_price_template_weak.py` 是另一个源版本，未在本批重复登记；运行时从同一冻结内容导出到相邻目录。

## 重放

将 R-18 的 `cone_walk.py` 和 canonical `customer_attraction` 依赖放入原脚本预期的相对根后，直接运行两个 probe。`rerun/four_price_report.json` 与冻结四人报告 SHA-256 相同，均为 300 条 `best=-0.0` 记录；三人重放为 150 条、`best=-0.0`。stdout 只含第 0 次改进记录，未出现正分离候选。

在本目录相邻的 `run/` 中导出 weak helper 后运行 `search_mass_two.py` 与 `search_uniform_mass_three_halves.py`。三二程序输出
`lambda=(0,0,20/23,0,6/23,21/23,0,43/46)`、`min_exact_slack=0`、`rows=800`。它是辅助有限行系统的精确可行乘子，不是完整 CAG 半覆盖证明。

`exact_mass_dual_audit.py` 用 Fraction 重新生成 `search_mass_two.py` 使用的 32 个 bit 状态 × 5 个 `(d,l)` 状态 × 101 个背景 `pbg` 的 16,160 行。它逐项检查两个报告乘子：`discounted` 的最小 slack 为 0，`W` 的最小 slack 为 0，均无负行。该复核确认可行性；原程序的 SciPy 浮点最优性和 `limit_denominator` 选择仍不构成一般对偶最优性证明。

## 数学边界

这些文件只给固定有限锥、有限代数行和有限重放证据。它们没有枚举所有完整历史纯 SPE，也没有给出当前六人 Q-CAG-HALF-6 的全称结论。任何正/负候选都必须另有完整有序策略、精确 IC 和真实客户重数证书；本批没有产生原模型反例。
