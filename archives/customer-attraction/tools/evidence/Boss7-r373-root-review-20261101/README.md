# R-373d 根审计复现包

本目录保留三个冻结源的可复核副本：`audit_uncovered_optimum.py`（`e6b00c3f5833ca19a86a`）、`uncovered_optimum_audit.json`（`b4e8e4749c21cde5c993`）和工作区元数据 `workspace.json`（`aff821168f7ae8b335a0`）。脚本无外部导入，按 71 个单位客户、两名提供者、六主题、7 个有序历史和 42 项含自身动作比较重建收益；重放得到实际 `(0,1)`、`W=35`、`OPT=38`、唯一最优无序对 `(2,3)`、最优外遗漏 36、半覆盖余量 32。

这与既有 `unique-optimal-omission-existence-counterexample-family` 的 `k=3` 实例是同一数学实例；本批没有新增定理或改变量词。脚本和 JSON 作为独立 exact replay 证据保留，不能当作新的六人 half 反例。`workspace.json` 只有 schema/save/actor/instance provenance 元数据，不进入 `state/`。
