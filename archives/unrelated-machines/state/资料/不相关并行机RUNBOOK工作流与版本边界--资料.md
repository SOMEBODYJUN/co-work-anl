---
id: unrelated-machines-runbook-operational-scope
kind: resource
type_tag: operational-document
title: 不相关并行机 RUNBOOK 工作流与版本边界
status: retained
summary: 实读旧题 RUNBOOK，保存其独有的启动、通信、凭据隔离和证据回归路线，并明确其与当前 Boss3/rebuild-v2 阶段二规范的版本边界。
source_refs:
  - source:c08edb5d0e1da6b71589:research/unrelated_machines/RUNBOOK.md
  - source:local:cleanup/README.md
  - source:local:cleanup/OBJECTS.md
  - source:local:tools/README.md
---

# 不相关并行机 RUNBOOK 工作流与版本边界

## 对象身份与处置

这是一个操作资料对象，不是新的数学定理或模型假设。原冻结源是 `research/unrelated_machines/RUNBOOK.md`，Claim ID 为 `c08edb5d0e1da6b71589`，源文件 SHA-256 为 `3f81d85b7cd5197c5c758c4b9b9afbfc993100a32650a6a3765be07cddeeccee`，大小 5773 字节。原文已完整复制到 [RUNBOOK 原文证据](../../tools/evidence/runbook-operational-scope-20261031/original/RUNBOOK.md)，逐项比较记录在 [比较记录](../../tools/evidence/runbook-operational-scope-20261031/comparisons/comparison-notes.md)。

处置为 `retained`：RUNBOOK 仍保留独有的历史操作语境和证据路线，不能因其不是数学结论而删除；同时不把它当作当前会话的自动执行说明。当前适用的工作流以 `cleanup/README.md`、`cleanup/OBJECTS.md`、`tools/README.md` 以及本次已登记的 `Boss3` 绑定为准。

## 原文实际规定的工作流

RUNBOOK 把旧 unrelated-machines 题的操作拆成四个连续环节。

1. **独立恢复与身份绑定。** 新会话从仓库外凭据和最新版 `work.py` 启动独立 clone，先绑定唯一会话编号，再复用该 clone 内已绑定的角色和存档。旧绑定 clone 不改绑；确有同一旧对话迁移时才使用 legacy adoption。RUNBOOK 要求核对结果分支、存档入口、研究入口和提示词入口，避免把旧题 clone 误当成新题。
2. **通信与只读访问。** 日常同步、读取公屏、收件箱、定向私聊、访问已推送工作区和显式 ack 都由 `work.py` 统一入口完成。无正文的私聊只读；跨存档合作必须在新消息中准确给出数学来源；ack 只表示已读，不表示采用。
3. **证据、正文与 checkpoint。** RUNBOOK 要求按本次实际变化选择程序复现、目录/图检查和证据更新；冻结 evidence 不原位覆盖。正式资产先 checkpoint，只有回执返回 `status: pushed` 才能报告远端保存；提交成功本身不改变数学真值或完成度。
4. **冲突与重置。** 真实 Git 冲突应保留双方，禁止 force push、自动 ours/theirs 或用新研究分支逃避冲突。`reset plan` 只生成保全清单，`reset apply` 需协调 Boss 明确执行并先核对远端 done；失败不能报告重置完成。

这些流程事实与当前清洗规范的交集在于：实际读源而非看摘要；先形成可复用正文和证据，再逐来源登记语义处置；字段检查不代替数学判断；未决来源不能声称全仓完成。该交集已在 `cleanup/README.md` 和 `tools/README.md` 重新表述，因此 RUNBOOK 的命令文字不应机械复制。

## 版本边界与不能直接继承的内容

RUNBOOK 的具体示例属于旧题上下文：它写的是旧 `R-编号` 命名、`unrelated-machines` 旧存档、旧入口和旧分支；本次会话使用的是 Boss3、结果分支 `rebuild/research-v2`、公屏 `wcg/board-cleanup-20261028` 和存档 `repository-cleanup`。这些身份与路径差异是执行边界，不是数学对象的改名。

RUNBOOK 还指向多个历史 evidence 回归和旧题入口。它们可作为来源定位和历史审计线索，但不能被解释成当前阶段已重新运行的证明，不能把旧回归数或旧目录图直接当成阶段二完成证据。当前每个来源仍须由 `clean claim`、`clean show`、实读、正文 checkpoint 和 `clean done` 逐项形成链条。

文档中出现的凭据说明只表达“凭据在 clone 外、不得进正文/remote/日志/公屏”的约束；本对象和证据没有复制任何 token、URL 中的秘密或认证输出。当前会话继续遵守这一约束。

## 与数学正文的关系

RUNBOOK 不提供六人 SPE 的定义、量词、可行性条件或覆盖结论，因此不进入 `定义`、`定理` 或 `证明` 主类。它为后续数学清洗提供来源处理协议：

- 历史 README、入口和测试只能作线索，需回到冻结源和实际证据；
- 操作资料与数学对象分开存档，避免把“已 checkpoint”误读成“已证明”；
- 旧题、当前题和跨存档合作保持独立身份；
- 任何未来新增数学对象仍需登记稳定 ID、来源、假设、推导或失败机制及接续方式。

因此本资料保留为可追溯的操作历史，并以当前阶段规范覆盖其过时的命令参数和会话身份。
