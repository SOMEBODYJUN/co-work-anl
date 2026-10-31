---
kind: source-review-draft
source_id: ec354cc7f885c94a5e48
source_path: examples/unrelated_machines/normalized_gated_menu_edge_cases.json
source_sha256: 563209b27c1c1b6d969b701bf06185e245f5ccd3ebf23b8c7651ad3b8dbc233b
status: ready-for-parent-review
recommended_disposition: integrated
recommended_target: archives/unrelated-machines/state/审查/归一化门菜单福利与对数调色板padding有限审查--审查.md
---

# `normalized_gated_menu_edge_cases.json` 语义清洗稿

## 来源身份与实际内容

冻结源 `ec354cc7f885c94a5e48` 位于 `examples/unrelated_machines/normalized_gated_menu_edge_cases.json`，两个冻结提交内容相同，SHA-256 为 `563209b27c1c1b6d969b701bf06185e245f5ccd3ebf23b8c7651ad3b8dbc233b`，大小 2314 字节。它是归一化 gated-menu 的输入/结果边界夹具，不是证明脚本，也不含通用 LP 求解器、策略动作表或独立的完整调度审计。

顶层只有 `large_denominator_cases`、`flat_negative_control` 和范围声明。所有数值以字符串形式保存为精确整数或 Fraction；因此可直接重建，不应把它当作浮点实验。

## 两个大分母夹具

第一条夹具含一个两状态、三坐标菜单，分母为 `2^200+1` 的互补系数；`z` 为两项各 `1/2`，`x` 两行均为 `(1/2,1/2,0)`，福利、peak 与 `beta_opt` 均为 1。它有 7 台机器、9 个作业、18 条有限边，2 个零 incidence 作业，`nontrivial_coin_steps=0`，`active_groups=1`。

第二条夹具含两个单坐标状态，`z` 各为 1，`x` 分别为 `1/(2^200+1)` 与 `(2^200)/(2^200+1)`。福利为 1，peak 为 `3/2`，`beta_opt=1/2`，`nontrivial_coin_steps=2`，6 台机器、7 个作业、13 条有限边，零 incidence 作业为 0，`active_groups=1`。

这些记录的用途是压力测试精确有理解析、极小分数和 coin 逻辑。它们不是关于分母位长的复杂度定理，也不证明所有 gated menu 都能达到 `beta_opt`。

## flat/gated 负控制

`flat_negative_control` 固定 `n=2`、每组一个 state、一个资源、所有 private times 为 1。源给出 flat optimum 为 2（4 个原始 assignments），gated optimum 为 `3/2`（搜索 13 个节点）。这只比较该有限输入的两个定义域：门控约束在此控制实例上降低可达到值。它不构成一般 gated-menu 单调性、近似比或 hardness 结论；也不能迁移到裸 Cartesian menu、三叉树 palette 或 customer-attraction 模型。

## 与既有对象的关系和处置

既有《归一化门菜单福利与对数调色板 padding 有限审查》已承载 `normalized_gated_menu_welfare_audit.json` 与独立重放、两个 fractional-z 例、flat negative control 的审计语义；既有 gated-menu 证据 manifest 保存了运行程序和输出。当前输入夹具的独有贡献是：明确给出两条 `2^200+1` 大分母菜单，以及一个不依赖运行程序的最小 flat/gated 控制输入，可作为原始输入身份和边界回归。

建议将本源 `integrated` 到该审查对象并补入 `archives/unrelated-machines/tools/evidence/gated-menu-20261030/` 的 manifest 与源副本；不新建重复数学对象。由于输入本身没有策略或通用证明，不能从它单独声称完整调度定理、归一化菜单一般舍入结论、UM-TARGET-v1 结论，或六人 SPE 半覆盖结论。

## 可复核边界

可用 `clean show ec354cc7f885c94a5e48 --out ...` 重建源副本并验证 SHA-256。进一步的 gated-menu 福利/配置结论必须使用既有审计程序、完整任务矩阵和其明确 scope；本输入只提供精确边界夹具，不能替代那些全历史或 LP 证书检查。
