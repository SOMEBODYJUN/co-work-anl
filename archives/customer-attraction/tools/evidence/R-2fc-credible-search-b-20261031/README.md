# R-2fc credible-search B（十个冻结 JSON）

本证据包对应 `R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/` 中 Boss2 认领的十个 JSON。每个源先实际调用 `python3 work.py clean show <id>`；十次均只读、退出码 1，错误是 partial clone 的 promisor remote 无法连接 `browser-proxy:8889`，原 stdout/stderr 按源 ID 保存于 `clean-show/`。随后使用冻结 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 的 GitHub blob 页面逐一打开并读取页面内完整只读文本区；浏览器文本字节数比 inventory 少一字节（页面去掉末尾换行），inventory 中的原始 size、blob 和 SHA-256 未改写，逐源记录在 `source-manifest.json`，字段级全量摘要在 `browser-read/summaries.json`，顶层/策略动作/整数克隆/对偶支持长度见 `browser-read/field-inventory.json`。

`run/independent_summary_validator.py` 不导入客户吸引实现、LP 或 MILP，只用标准库 `Fraction` 重算完整有序历史数 `Σ_{d=0}^{m-1}p^d`、非自身比较数、`OPT/u`、`2W-OPT` 及弱逐人余量；十条均通过（`run/independent_summary_validator.json`）。这项重算验证的是已给出的整数客户重数和完整策略证书，不是对所有目录/策略的优化证明。

## 数学读数

* `m3p5_mid_J034` 与 `m3p5_mid_J234`：m=3,p=5，根 11100，MIP status=optimal；各固定候选均 31 个有序历史、124 个非自身比较，精确候选 `W=4, OPT=5, u_target=1, OPT/u=5`。这是完整有限全历史证书；固定 DAG 搜索的 optimal 状态不外推到全部策略。
* `m3p6_111000_a0_mixed`、`m3p6_111000_a0_out`、`m3p6_210000_a1_out`、`m3p6_mid_J034`：m=3,p=6，MIP status=timeout/incumbent；每条固定候选仍由 43 个有序历史、215 个非自身比较的 Fraction 证书完整核验，分别 `W=4,3,3,3`、`OPT=5`、`u_target=1`，均 `OPT/u=5`。timeout 不是无解，也不是全类最优性。
* `m3p6_mid_J345`：同为 m=3,p=6、根 111000，MIP status=optimal；固定候选完整核验得到 `W=3, OPT=5, u_target=1`、`OPT/u=5`，仍只有有限点含义。
* `m4p5_11110_a0`：m=4,p=5，根 11110，status=timeout/incumbent；156 个历史、624 个非自身比较，`W=19, OPT=19, u_target=4`，`OPT/u=19/4<7`。
* `m4p5_21100_a1`：m=4,p=5，根 21100，status=timeout/incumbent；156/624，`W=5, OPT=6, u_target=1`，`OPT/u=6<7`。
* `m5p5_31100_a1`：m=5,p=5，根 31100，status=timeout/incumbent；781 个历史、3124 个非自身比较，`W=1, OPT=1, u_target=1/5`，`OPT/u=5<9`。

所有十条固定策略证书都满足 `2W-OPT>0`（半界没有反例）；若只看弱逐人目标，前三条 m=3 的缺口为 0，其余 m=3 条为 0，m=4 两条为 9 与 1，m=5 条为 4/5。缺口为 0 只表示命中弱桥阈值，不能把比值 5 解释为一般反例，因为这些是固定输入的一个策略及其完整离轨检查。

## 处置边界

十个源均保留为 integrated finite certificates（其中 MIP timeout 的 incumbent 以“搜索未闭合”标注）；没有任何源提供六人、任意人数或全部纯 SPE 的普遍 `OPT/W≤2` 证明，也没有提供 `OPT>2W` 的半界反例。`portfolio`、`target`、root count、浮点 bound、时间限制均是搜索记录，不能替代 exact Fraction 全历史证书或量词。
