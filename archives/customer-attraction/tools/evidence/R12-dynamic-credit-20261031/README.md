# R12 dynamic credit evidence

本证据包保存 dynamic_credit 五源的冻结指纹、逐源复现代码和精确 JSON 输出。`audit_one_step_closure.py` 重放的是标量一步闭合障碍：响应菜单不是 SPE，但满足所有首步标量条件，且 `W=14, OPT=30`；脚本同时给出终端偏离 `9/2 -> 19/2` 以防误读为真实 SPE。`audit_query_branch_capacity.py` 以 `Fraction` 重放 2394 个查询分支恒等式检查。

背景覆盖信用文档只定义 `E_h=G+P-M_r(B)` 及恒等式 `E_h=E_{hA}+u-δ`，并明确需要真实跨分支 relay；它不是 half 证明。README、脚本、JSON 与 replay 输出的 SHA/来源均在 `manifest.json`。
