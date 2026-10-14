# 本研究分支的工作规则

所有主对话和子 agent 采用 prompts/TEAM.md、prompts/PEER.md 的同一解题协议。所有解题天团不存在固定职能角色、中心 assignment、路线审批或单一整合者。用户额外要求的论文者/清洗者、提取者是辅助入口，不替研究天团派单或批准结论。用户要求平等探索优先于旧协作方案。

目标、定义、量词以 MODEL.md 与 CLAIMS.md 为准。本分支与原设施博弈/顺序客户吸引保持数学身份独立；没有证明 reduction 时不得迁移旧定理。

本分支的 README、RESEARCH_STATE、CLAIMS、FAILED_ROUTES 是这项新研究的账本。建立新数学结论后同时依根 AGENTS 的规则登记规范资产、审查状态和图关系；没有数学新结果的协作基础设施改动不虚构 graph theorem。每个真实阶段 checkpoint commit/push 并核对，公屏结果须已推送资产的 commit/hash。

修改公屏工具后运行本分支 tests/test_board.py；修改数学资产时运行相应精确核验。正式交付前运行根 build_map.py --check、build_crosswalk.py --check、check_assets.py。测试成功不升级数学真值。

普通研究 checkpoint 执行 CHECKPOINT.md：有真实可复用资产、证据层级准确且相关核验完成后，主 agent 立即运行 `bash research/weighted_congestion_frontier/tools/checkpoint.sh`；无需重新向用户请求保存授权，或为了保存重复整轮数学审查。修改 checkpoint 后运行 tests/test_checkpoint.py。候选、精确障碍和有价值的失败回收可保存，不得因此升级 claim。范围外文件显式列入命令；公屏分支仍只能通过 board.py 验证认领。

新成员先按 RUNBOOK.md 用 board.py register 登记真实身份；默认研究轮次约一小时，以实际工具限制与 ACCEPTANCE 为准。新辅助入口为 prompts/PAPER_WRITER.md、prompts/EXTRACTOR.md；原文参考固定在 SOURCES.md 和 upstream/manifest.json，保持原始字节与许可。修改注册/公屏仍跑 test_board.py。不要为了使用归档参考改动上游 SKILL；本项目角色提示词记录必要适配。
