# R-171 security 池化响应有限审计（2026-10-31）

本目录保留五个冻结源：`7ec5000b9c04e754284d`（README）、`219d041381f777bdcba9`（`audit_pool.py`）、`f849d9ac00dc6a80ab91`（旧36客户 `pool_audit.json`）、`132be9e7831f3d06af00`（29 条 `pool_delete_report.json`）、`303a27238635df798884`（5 条 `pool_full_report.json`）。原字节在 `original/`，直接运行 `audit_pool.py` 的输出在 `replay/`。

旧36客户脚本通过 258 个 SPE 节点动作比较，并精确计算同一 `p={2:1/2,5:1/2}` 下的 unpooled/pooled 负载；两份报告则记录固定 `p` 的 LP/锥探针，在 `extra=false` 的 m-1 删除背景和 `extra=true` 的完整终局背景之间分开保存。报告中的 `ratio` 是各有限样本的数值输出，不能替代一般量词。

本批增量源版本（Boss1 复核）：`4c52f58685795cdfcf9e` 的 `pool_packet_probe.py` 按 counts 降序重建 13 人自动机的真实 targets；`00e6b017434d941748a5` 的报告含 27,243 节点、31,454 条去重 Gamma 行、30 起点/15 轮且最高 ratio=1；`32aaa81a217034da0f7c` 的 `pool_probe.py` 保留完整 Gamma 行并交替运行固定 p 的 LP 与 SLSQP；`d96fc2e90151962cc7fd` 记录两人三标签 81 个形式策略的有限局部扫描，最高 ratio=1。它们都是有限数值发现，不能替代一般量词。
