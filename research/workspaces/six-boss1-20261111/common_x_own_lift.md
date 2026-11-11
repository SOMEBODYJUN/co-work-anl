# 同一 X 的 own 精确相容层：已冻结并评价新点

RUN `six-boss1-20261111`；Boss1；2026-11-11。仅写本页与 `common_x_own_lift/`，未写 Git/RUN/registry，零优化调用。

## 冻结交付

[完整数学、真实触点、边界与复现](common_x_own_lift/report.md)。
[1260 行稀疏包](common_x_own_lift/own_facets.json)；[独立核验](common_x_own_lift/verification.json)；[冻结清单](common_x_own_lift/freeze_manifest.json)。

- 194 个 R/Z 与 16 个 B4 H1/H2 组，每组六 facet，共 1260 行、5718 非零、21021 列、零新列。
- 全部 16 hist（含六个历史旧零 hist）保留；B4 四原子和等于 H 的原 16 对正反质量行完整记录，未作无付款系数替换。
- 独立核验从原 joint-state-upper 行反推 R/Z 原子归属，再从原新列描述符重建 x/y，核全部1260行。特别修正 `hist_column_old` 是 legacy 编号的易错解读；没有盲抄 own_blocks。
- 八格 β 消元的16比较中十项由既有约束支付，六项为本包新行；逐项对应和六facet各自不可省略的通用局部例见核验。
- 420 个 y 加层后成为真实核心量，不能继续 canonical_min；原 7954 max、2790 min 的语义不变。
- 原22297矩阵未改、23557矩阵未创建或求解；只交可复用稀疏层与21021列未来点接口。

行包 SHA256：`711e0d2b1499784f26fce26d8cc7a7a985c618df52a125f91af61a168bfc70ba`。

## 新点5b1b的固定值结论

[新点完整报告](common_x_own_lift/fullX_5b1b_report.md)；[全部facet/区间/见证](common_x_own_lift/fullX_5b1b_fixed_diagnostic.json)；[既有合同API交叉核验](common_x_own_lift/fullX_5b1b_crosscheck.json)。

数学和行包先冻结，再评价 Main 指定的新点 SHA256 `5b1b649af5fc9d359e31dd03945d12708e599e0eeac75983ed188e60178b3bfe`，未评价旧 cb45 点。

210组基础条件均通过。新增1260行仅5条为负，全部O6；失败组57、59、81、86、115，分属H117、H225、H308，共3个R/Z、2个B4。五组均m11=0，L>0而U=0；其余205组给出β=L的八格见证。既有root合同诊断器独立交叉核一致。

此结果只排这份固定(m,x,y)的共同X解释；不能排重选y或重选X，更不声称新LP不可行或已求得新最优。后续需保420真实边缘核心列联立求解，或给出覆盖全部可重选变量的精确Farkas证书。

六人 `2W≥OPT6` 仍 OPEN。
