# R-2fc aggregate-security 十源证据包

本包记录 Boss2 对十份冻结 JSON 的逐源实际读取、参数摘要、精确锚点比较和 verifier 运行。

## 原始来源

所有来源均位于冻结 commit `68fad804ec5946cb296f77dc5b336308a66abf12` 的
`research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/`。
`sources-summary.json` 保存每项 source id、blob、大小、SHA-256、raw URL、参数、结果和处置；其 `raw_read` 字段记录了逐一通过浏览器读取 raw 内容。当前 clone 的 promisor remote 无可用网络，`tools/cleanup.py show` 因此无法写出本地冻结副本；这不影响 raw 内容读取，也不把 inventory 元数据冒充正文。

## 精确核验

`verify_two_boundaries_summary.json` 是本地运行
`archives/customer-attraction/tools/evidence/coverage-moment-and-potential-ledger-primary/new-definition-check/verify_two_boundaries.py`
的精简输出，退出码 0、`status=pass`。它核对扩大 DR 表的 84/168/252 计数、完整策略 43 节点/258 比较、`P=161`、`v=56` 和 `not_a_CAG_input=true`，并同时核对既有 11 客户 CAG 证书。完整 stdout 暂存为工作区文件，不把巨型逐行表重复入包。

## 证据等级

`dr_boundary_exact.json` 是唯一有理有限证书，已并入既有障碍对象。其余九项为固定参数浮点诊断（包括 `best_objective=0.0` 的三个文件），均只 retained；近零或负浮点值不作为 CAG 结论。
