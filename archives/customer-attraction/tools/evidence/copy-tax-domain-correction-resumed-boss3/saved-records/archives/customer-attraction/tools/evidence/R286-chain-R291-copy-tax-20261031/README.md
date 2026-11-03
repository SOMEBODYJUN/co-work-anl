# R286 链式回复与 R291 复制税边界证据

本证据包保存 Boss3 对 15 个冻结来源的实际导出、原始代码/JSON、有限运行输出和失败日志。原始来源均来自 `legacy-cleanup` 与 `main` 的同 SHA 内容；不把文件名、旧摘要或单个 JSON 报告当成已复现证明。

## 运行记录

- `chain_gap_microcheck.py`：exit 0，精确输出 `linked=-1`, `free=-2`, `gap=1`。
- `check_chain_reply_requery.py`：exit 0；核 `k=3,4,5`、`L=2,3` 全部 `ok`。
- `attack_copy_tax_naive_induction.py`：exit 0；`m=2` 无反例，`m=3` 找到 `actual_budget=51 < deviation_demand=52` 的严格分支归纳反例。
- `verify_copy_tax_induction_boundary.py`：exit 0；13 个历史、39 个行动比较，最小 IC slack 0，精确重现 (17/2)、(26/3)、差 (1/6)。
- `audit_half_restart.py`：exit 0；2940 个 2 状态有理算术案例，正向和反向最小 slack 都为 0。
- `exhaust_copy_tax_three_topics.py`：exit 0；完整小域穷举未 refute 候选，结果保存在同名生成 JSON 中。
- `counterexample_search_m6.py`：exit 1；冻结脚本导入仓库外的 `customer_attraction_search`，当前结果分支没有该模块，`ModuleNotFoundError` 已逐字保存在日志。其冻结 JSON 仍作为来源报告保存，未宣称本次独立复现。
- 所有 Python 文件 `py_compile` exit 0。

`source-manifest.md` 列出每个来源 ID、冻结路径与证据文件；`comparison-notes.md` 说明与既有链式回复资源页和 Q-CAG-HALF 边界的异同。有限搜索、算术审计和候选压力测试都不升级为一般 Q-CAG-HALF 证明或反例。
