# terminal_pair / tree_coupling 三源证据

本目录保全 Boss2/cleaner 对三份冻结源的全文阅读结果。`terminal_pair_audit.py` 与 `terminal_pair_audit.json` 是按源 SHA-256 逐字复制的原件；`full_history_walk_summary.json` 是对 317,303 字节冻结 `full_history_walk.json` 的结构化摘要，保留顶层合同、36 轮记录、最佳见证、矩值分布、原源 SHA/字节数和解释边界。因本轮命令行 Git 的 promisor fetch 受 `browser-proxy:8889` 不可达影响，全文是从冻结提交 raw 页面只读解析；摘要明确标注原 JSON 未被本地摘要替代。

`full_history_walk.py`（关联程序 ID `c540b855a9e134400e34`，11,719B，SHA-256 `3e73f28849969d781f512a9f76cdc8c990a8cca0911626d5c9872896b7dafaba`）的全文语义已在审查对象中按函数重构；它是输出解释的关联程序，不是本批三源处置对象：五名玩家、七主题、相邻策略锥步行；每轮先用完整任意历史纯 SPE 递推得到抽象 Shapley 表，再用 `scipy.optimize.linprog` 寻找候选，随后分数转 `Fraction` 并逐行检查。输出只覆盖 36 个固定随机种子轮次，`scope` 明示为截断单调次模共同矩、无客户正实现声明。

`terminal_pair_audit.py` 已在全新临时路径本地重放一次：退出码0、stderr为空，stdout与写出文件相同，并与冻结 `terminal_pair_audit.json` 逐字相同；细节见 `terminal_pair_replay_metadata.json`。
