# 本研究分支的工作规则

每个 Work 对话在启动提示词中指定唯一角色号，如 `R1`。这个角色号统一用于该对话的公屏发言和研究提交；子 agent 在对话内部协作，由主对话汇集发现。所有研究对话共同解决 WC-TARGET v1，自主选择问题、方法和独立审查。按当前义务调用 subagent，人数、轮数和时长由实际研究需要决定。

首次用 `tools/work.py start --actor R1 --token-file /本会话/githubtoken.txt` 恢复项目并固定本地配置，完整命令见 RUNBOOK.md。后续直接调用同一程序的 `read`、`send`、`sync`、`checkpoint`。用户已授权研究资产的日常保存和公屏交流，形成有价值的阶段文件且完成相应核验后立即 checkpoint。

公屏是 `wcg/board` 分支上的异步消息流，像群聊一样交流具体数学发现、问题、异议和成果入口。读到消息后自行判断并继续研究；同题独立推进、多种机制并行都可开展。相关回复在下一次读屏时处理。详细协议见 PROTOCOL.md。

目标、定义、量词以 MODEL.md 与 CLAIMS.md 为准。README、RESEARCH_STATE、CLAIMS、FAILED_ROUTES 是本分支研究账本。新数学结果按根 AGENTS.md 更新规范资产、审查状态和图关系；协作基础设施改动记录实际执行证据。

重要 claim 列出精确身份、证据和 objection；变更范围建立新版本。状态提升按 ACCEPTANCE.md 完成一般证明、独立攻击与文献核对。候选、精确反例、障碍和失败回收按其实际层级保存。

修改协作工具时运行对应 tests；修改数学资产时运行相应精确核验。正式交付前运行根 `research/build_map.py --check`、`research/build_crosswalk.py --check`、`research/check_assets.py`。论文者与提取者的完整入口在 prompts/PAPER_WRITER.md、prompts/EXTRACTOR.md；选定原文及许可在 SOURCES.md、upstream/manifest.json。
