# R-373d background 精确代数、有限缺口探针与三价模板障碍

本批八源来自 `R-373d.../background/`，全部经 `clean show` 导出并登记冻结 SHA/blob/大小。证据包另保存了精确代数审计、有限 ExactSPESolver 探针、SciPy 模板 LP 和 Fraction Farkas 恢复。`customer_attraction` 依赖从已冻结的 R-33e8 证据包复制并单独登记哈希。

## 逐组结果

- `audit_max_theme_branch_capacity.py` 对 `m=3..100`、每个 `c=1..m` 做 5047 个 Fraction 恒等式检查。三玩家新根系数为 `11/75`，旧系数 `2/15`，差 `1/75`；整数缺口倍率 `30/11<3`。`m=4..10` 的新系数均严格高于旧系数。它是作者代数审计，不是均衡求解。
- `deficit_probe.py` 用 ExactSPESolver 在固定 seed `343734` 上运行 1000 个四主题四玩家实例和 5000 个五主题四玩家实例，分别得到 `max_gap=-7` 与 `-24`，没有 `OPT-W>players*min_payoff` 的样本。源 JSON 与重放 JSON 字节相同；这是有限随机 no-hit。
- `three_price_template.py` 在 `bgmax=30` 的有限模板上，`n=1,2` LP 可行，`n=3,4,5,10,20,100` infeasible。`three_price_template_obstruction.py` 对 `n=3,bg=0` 用浮点 LP 找 witness，再用 Fraction 恢复 11 个乘子；700 多重类型中每行 slack 非负，目标整数尺度为 `-1399`。

这些输出保留了两类不同含义：代数恒等式和命名模板 Farkas 障碍是精确的；随机 ExactSPE no-hit 只有有限搜索意义。没有一项建立当前六人 CAG 的普遍半覆盖定理，也没有一项构造合法 SPE 半值反例。
