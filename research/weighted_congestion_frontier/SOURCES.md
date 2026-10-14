# 可核对的开源来源与原文

核验日期：2026-10-14。`upstream/manifest.json` 记录每个原文文件的源仓库、完整 commit、原路径及 SHA-256。归档文件逐字节等于指定 commit 的 blob；保留原 LICENSE 和第三方说明。它们是按本任务选取的源文件快照，不是对外部软件/全部 skill 的完整部署。以后升级重新核对上游，保留版本与差异。上游 novelty_risk_audit.md 原文包含Markdown硬换行所需的行尾空格，仅该原文文件设置 whitespace=-blank-at-eol；其余检查与本项目文件保持原规则，不为消除lint改变原文字节。

## 协作经验

| 来源 | 已核验与使用 | 原文与适配边界 |
| --- | --- | --- |
| Anthropic C compiler，`6f1b99acb2f4ec2414592136c2009fe7713deec3` | 作者说明的独立 clone、自主选题、Git 认领、冲突者换单元、保存失败机制、明确反馈与持续接续工作 | 原仓库 `current_tasks/` 和 `ideas/` 各归档一个真实文件及 CC0 LICENSE。原文见 upstream/claudes-c-compiler/；作者文章见下方链接。该快照未找到完整 AGENT_PROMPT.md，不能声称复制了未公开提示词。原 Docker/CLI 无限重启 loop 没有在 Web Work 部署；也不照搬跳过权限的命令。 |
| MathLab，`f2beac493aff1868b92b8233fd4427c467812ebe` | 持久黑板、真实成员身份、BASE 证据层级、先自主重构的 verifier、跨探索组传播机制 | 完整原始 prompts.py、ARCHITECTURE.md 与 MIT LICENSE 已归档。原 Director 派单不符合用户本轮要求，TEAM 采用自主认领；没有运行原 orchestrator 或声称原架构无中心。 |
| agentsync，`4d190adb7f711f5e64eb358612ecabd97c1b2fd5` | README 与设计中普通 Git push 原子更新、冲突后重读占用、agent ID 与独立状态分支 | 本项目 board.py 是已有自有实现；未安装 MCP。其许可为 PolyForm Noncommercial，未归档它的实现。仅以一手文档核对机制，不能声称完整复制了该项目。 |

一手来源：[Anthropic 作者说明](https://www.anthropic.com/engineering/building-c-compiler)、[compiler](https://github.com/anthropics/claudes-c-compiler)、[MathLab](https://github.com/adamisntdead/mathlab)、[agentsync](https://github.com/jarmstrong158/agentsync)。

用户要求原样采用经验时，执行已经核验的具体做法，并保存可获得且许可允许的原文；没有拿到的源文件和不同产品能力不得描述成“已一模一样部署”。本项目的数学量词、冻结资产、租约、注册和 Web 多对话适配都明确记录。后续 agent 能区分原文事实、原样引用和本项目改造。

## 写作原文

| 归档来源 | 实际要读的材料 | 解决什么问题 |
| --- | --- | --- |
| mathematical-academic-writing，`db948c44a5015f8ba2fd1950b949b850d6ab6465` | SKILL.md；research_article_workflows、mathematical_integrity、genre_profiles、anti_defensive_audit、artifact_verification、source_and_derivation_audit 等 runtime references | 精确 theorem-proof 写作、清楚的数学主语和作者立场、证据与措辞对应、去掉反复自我防御、完整证明和导出检查。归档是数学写作运行所需选集，不包含上游所有课程资料。 |
| polish_skill，`9b2a86ca6ac88879a3d3490fecdb909673fd1562` | 完整 paper-argument-reconstructor、idea-novelty-auditor、problem-driven-literature-review、paper-polisher 目录及 LICENSE | 主动重建论文贡献叙事；核对危险相关工作；把每条贡献接到已证结果；最后保留 TeX 数学语义地润色。尤其 argument reconstruction 原文包含强弱贡献表述的具体对比。 |
| latex-paper-skills，`0f4eab27cf871143c243d854e8154c48612d7a53` | innovation-framing.md、contribution-map-template.yaml 与 LICENSE | 贡献必须同时交代意义、旧结果、缺口、证据与可反驳条件。只取 framing 原文；不强制把数学理论论文改成实验 IMRAD，也不继承固定协作者工具。 |

归档引用指向 [upstream/manifest.json](upstream/manifest.json) 的不可变版本。阅读原文后按用户本轮授权执行；不把外部 skill 的通用确认步骤误当成对已授权写作、保存的额外审批。适用范围、定理身份和真值层级始终由本项目精确记录约束。归档原文没有自动注册成 ChatGPT 插件；角色提示词会明确读取这些本地文件。

一手写作来源：[mathematical-academic-writing](https://github.com/JiahaoLi-creator/mathematical-academic-writing)、[polish_skill](https://github.com/yujie-jason-zhang/polish_skill)、[latex-paper-skills](https://github.com/yunshenwuchuxun/latex-paper-skills)。

## Web 运行边界

[OpenAI 官方 subagents 文档](https://learn.chatgpt.com/docs/agent-configuration/subagents)说明 Work 可以显式启动独立 agent、选择受支持模型和 reasoning effort，并提醒并行写入需要协调。当前工具给出的实际槽位才是本会话上限。本文未找到五个 Web 对话都保证七槽位或任意提示词强制单次运行一小时的官方承诺；不把 CLI/API 配置当 Web 的可调设置。运行计划和时间核算见 RUNBOOK。
