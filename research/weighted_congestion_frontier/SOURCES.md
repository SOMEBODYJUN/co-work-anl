# 可核对的开源来源与原文

核验日期：2026-10-14。`upstream/manifest.json` 记录每个原文文件的源仓库、完整 commit、原路径及 SHA-256。归档文件逐字节等于指定 commit 的 blob；保留原 LICENSE 和第三方说明。它们是按本任务选取的源文件快照，不是对外部软件/全部 skill 的完整部署。以后升级重新核对上游，保留版本与差异。上游 novelty_risk_audit.md 原文包含Markdown硬换行所需的行尾空格，仅该原文文件设置 whitespace=-blank-at-eol；其余检查与本项目文件保持原规则，不为消除lint改变原文字节。

## 协作经验

| 来源 | 一手机制与固定原文 | 本项目实际采用 |
| --- | --- | --- |
| Anthropic C compiler，`6f1b99acb2f4ec2414592136c2009fe7713deec3` | 作者说明独立 clone、自主选题、Git 任务协调和失败记录；`current_tasks/`、`ideas/` 各归档一个原文件及 CC0 LICENSE，见 upstream/claudes-c-compiler/ | 自主探索、独立工作目录、可恢复阶段保存和具体反馈 |
| MathLab，`f2beac493aff1868b92b8233fd4427c467812ebe` | prompts.py、ARCHITECTURE.md、MIT LICENSE 已归档；BASE 证据层级、先自主重构的 verifier、跨探索组传播 | 精确数学身份、独立攻击、跨对话异步分享和成果提取 |
| agentsync，`4d190adb7f711f5e64eb358612ecabd97c1b2fd5` | README 与设计采用独立状态分支、普通 Git push、冲突后重读；许可 PolyForm Noncommercial | 公屏独立分支、普通推送后确认及并发消息恢复；工具为本项目自有实现 |

一手来源：[Anthropic 作者说明](https://www.anthropic.com/engineering/building-c-compiler)、[compiler](https://github.com/anthropics/claudes-c-compiler)、[MathLab](https://github.com/adamisntdead/mathlab)、[agentsync](https://github.com/jarmstrong158/agentsync)。

上表的归档原文保持其原项目内容与许可。当前运行规则采用 PROTOCOL.md、RUNBOOK.md：一个 Work 对话一个角色号，内部 subagent，异步消息流与直接保存。上游任务协调方式是来源事实，当前公屏按群聊交流。

## 写作原文

| 归档来源 | 实际要读的材料 | 解决什么问题 |
| --- | --- | --- |
| mathematical-academic-writing，`db948c44a5015f8ba2fd1950b949b850d6ab6465` | SKILL.md；research_article_workflows、mathematical_integrity、genre_profiles、anti_defensive_audit、artifact_verification、source_and_derivation_audit 等 runtime references | 精确 theorem-proof 写作、清楚的数学主语和作者立场、证据与措辞对应、去掉反复自我防御、完整证明和导出检查。归档是数学写作运行所需选集，不包含上游所有课程资料。 |
| polish_skill，`9b2a86ca6ac88879a3d3490fecdb909673fd1562` | 完整 paper-argument-reconstructor、idea-novelty-auditor、problem-driven-literature-review、paper-polisher 目录及 LICENSE | 主动重建论文贡献叙事；核对危险相关工作；把每条贡献接到已证结果；最后保留 TeX 数学语义地润色。尤其 argument reconstruction 原文包含强弱贡献表述的具体对比。 |
| latex-paper-skills，`0f4eab27cf871143c243d854e8154c48612d7a53` | innovation-framing.md、contribution-map-template.yaml 与 LICENSE | 贡献必须同时交代意义、旧结果、缺口、证据与可反驳条件。只取 framing 原文；不强制把数学理论论文改成实验 IMRAD，也不继承固定协作者工具。 |

归档引用指向 [upstream/manifest.json](upstream/manifest.json) 的不可变版本。阅读原文后按用户本轮授权执行；不把外部 skill 的通用确认步骤误当成对已授权写作、保存的额外审批。适用范围、定理身份和真值层级始终由本项目精确记录约束。归档原文没有自动注册成 ChatGPT 插件；角色提示词会明确读取这些本地文件。

一手写作来源：[mathematical-academic-writing](https://github.com/JiahaoLi-creator/mathematical-academic-writing)、[polish_skill](https://github.com/yujie-jason-zhang/polish_skill)、[latex-paper-skills](https://github.com/yunshenwuchuxun/latex-paper-skills)。

## Work 并行

[OpenAI 官方 subagents 文档](https://learn.chatgpt.com/docs/agent-configuration/subagents)介绍 Work 的独立 agent、模型与 reasoning effort 配置。使用当前工具实际提供的能力，按数学义务安排并行；主对话汇集子 agent 发现，用同一角色号交流和提交。实际入口见 RUNBOOK.md、prompts/MODELS.md。
