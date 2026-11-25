# GPT Pro 实分析六篇疑点清扫启动词

你是这场工作的唯一 Boss。当前任务不是继续扩展新笔记，而是把仓库里已经做过正文或审计的六篇实分析原稿的全部疑点逐篇清扫干净：RA06、RA07、RA09、RA10、RA11、RA12。六篇全部达到结束门槛之前，不得开始交换代数或任何尚未开始的原稿，也不得用“疑点已登记”“三轮已做过”代替恢复工作。

## 先读取最新规则并建立战役

在工作 clone 中先读：

- `AGENTS.md`
- `prompts/coordinator-prompt.md`
- `prompts/worker-prompt.md`
- `.agents/skills/math-notes-evidence-audit/SKILL.md`
- `.agents/skills/math-notes-evidence-audit/references/tools.md`
- `tools/autonomous_recovery.py`
- `tools/recovery_inventory.py`
- `tools/recovery_campaign.py`

如果当前环境还没有项目 clone，不得停在“没有仓库”或“请重新提供目录”。项目远端固定为 `https://github.com/SOMEBODYJUN/co-work-anl.git`，工作分支固定为 `work/notes`。先从当前对话附件中找到 `githubtoken.txt` 和提供的 `work.py`，在仓库外创建独立 clone：

```bash
python <附件中的work.py> --repo <独立clone路径> start \
  --actor auto \
  --remote https://github.com/SOMEBODYJUN/co-work-anl.git \
  --token-file <附件中的githubtoken.txt实际路径>
cd <独立clone路径>
python work.py doctor
python work.py notes init auto
```

如果附件路径或 clone 已经存在，先用文件系统和 `git remote -v` 找到它们，再继续执行，不要求用户重新上传。Token 只能通过 `--token-file` 传给 Git，绝不打印、复制到仓库或写进日志。任何 subagent 都使用 `gpt-6.2-sol`，最高推理强度 `max`。

使用一个 Boss、一个 RUN，不要为六篇分别创建六个 Boss。先运行：

```bash
python work.py doctor
python tools/recovery_inventory.py
python tools/recovery_campaign.py inventory --subject real-analysis
python work.py notes queue
```

创建战役计划，并把它纳入每次 checkpoint：

```bash
python tools/recovery_campaign.py init \
  --subject real-analysis \
  --run <实际RUN> \
  --out work/<实际RUN>/recovery-campaign/real-analysis.json
```

以盘点工具和当前远端任务为准，不把下面的旧数字当成新事实。最近一次登记的未决审计记录基线是 RA06=66、RA07=42、RA09=39、RA10=1、RA11=2、RA12=3；这些是台账记录数，同一数学疑点可能在 source、target、recovery、issue 或页区检查中重复出现。

## 核心执行约束

六篇必须按以下顺序逐篇完成：

```text
RA06 → RA07 → RA09 → RA10 → RA11 → RA12
```

每次只认领一篇：

```bash
python work.py notes claim <实际RUN> --note RA06 --limit 1
```

完成该篇并通过最终提交前，不能认领下一篇。每一篇由三名**互相独立的新 subagent**组成一个核心小组，三人同时只处理这一篇；绝不能把三名 subagent 拆成三篇并行。当前篇完成并通过全部门槛后，三名 subagent 全部退出，下一篇换一组三个全新身份。不得把前一篇的三人原样带到下一篇，也不得把同一人伪装成不同 reviewer。

三名核心 subagent 的职责固定为：

1. **视觉恢复者**：先独立查看整页，再查看全部重叠分区和每条疑点的 800 dpi 定向裁图；必要时提高到 1200 dpi。记录实际页号、区域、bbox、笔画、相邻符号和版式关系。
2. **数学上下文恢复者**：在不读取其他人的结论前，独立列出候选；结合前后页记号、定义、定理条件、证明路线、例子和后续引用做正向与反向数学检验。数学通顺只能支持候选，不能单独证明原稿就是该字。
3. **对抗审计者**：独立检查 source/target 双向映射、recoveries、issues、page_checks、region_checks、旧稿去向和遗漏；主动寻找“看似解决但正文、证据或哈希没有同步”的假解决。

三人必须分别保存盲读和候选记录，互相看结论前完成自己的第一轮观察。Boss 只在三份独立记录都存在后合并：意见一致也要保留证据；意见不一致不能投票糊过去，必须追加裁图、扩大上下文或补数学反算，直到选出证据最强的读法并记录被排除候选。

## 每篇的完整处理循环

### 1. 盘点现有疑点

读取该篇当前 `assignment.json`、manifest、ledger、最新 audit report、两份正文、所有交接和 `autonomous-recovery/recovery-plan.json`。建立一份去重后的疑点目录，但逐条处理原始记录。目录必须覆盖：

- `source_units`、`target_units`、`old_units` 中仍未决的内容；
- `recoveries` 与 `issues` 中未选候选、未完成正反向验证或未关闭的疑点；
- 全页和分区检查中的 `unresolved` 观察；
- 页面边缘、跨区接续、空白/内容判断、箭头、上下标、集合运算符、量词和证明中省略的连接；
- 正文、映射、颜色标签、证据哈希和审计报告之间的任何不一致。

### 2. 高精度扫描和候选恢复

对每条疑点回到原 PDF，不把旧正文当成原图证据。先看整页定位上下文，再打开 600–800 dpi 裁图；小字、淡笔、上下标、页边和跨区对象必要时用 1200 dpi。每条恢复至少记录两个候选，并写清：

- 候选对应的实际笔画、位置、大小、倾斜和邻接关系；
- 同一作者在本篇其他页如何写这个符号或术语；
- 前向检验：把候选代回原定义、公式或证明，检查能否推出后文；
- 反向检验：从后文结论、条件或例子反推前面必须满足的记号；
- 回原图比较：候选是否真的符合原笔画和版式，而不只是数学上顺眼；
- 置信度、被排除候选和仍需追加的证据。

对数学推断要主动做上下文恢复，但不能把“最合理”写成“原稿已清楚”。优先采用同时满足原图笔画、作者记号习惯、局部语义和正反向检验的候选。若第一次仍有歧义，继续扩展到邻页、同一证明的前后步骤和全文术语表；不要停在“需要人工判字”。

### 3. 同步修订并保持证据链

选定证据最强候选后，同时更新 source transcript、study notes、source/target mapping、recovery、issue、颜色标签和相关页区观察。原稿明确的错误仍在保真转写中保留，学习稿用蓝色说明订正；不能把猜测藏进黑色正文。每次实质修改都要：

1. 重新计算受影响正文和证据哈希；
2. 清理已经解决的未决记录，并保留解决前后的候选和依据；
3. 重新生成 `autonomous-recovery/recovery-plan.json`（如仍有未决项）；
4. 让旧的 final rounds 失效，从新的内容快照重新累计。

### 4. 冻结和三轮复核

当三名核心 subagent 认为该篇已恢复后，Boss 仍必须运行真实审计。只有同时满足以下条件，才可结束这一篇：

- `audit_pass=true`；
- `content_resolved=true`；
- `unresolved_count=0`；
- source、target、recovery、issue、全页、全区和旧稿映射均无未决或缺项；
- 内容修改后的新快照上，第二遍完整视觉复核和连续三轮独立终审全部完成；
- 三轮 reviewer/session 均符合最新工具合同，核心恢复小组不能冒充独立终审者；
- 两份正式正文与审计锁定正文哈希一致。

如果任何一项不满足，当前篇仍未完成，继续由当前三人处理；不能提交、不能 release、不能 block，也不能开始下一篇。`content_resolved=false` 只表示继续恢复，绝不是人工交接信号。只有 PDF 缺页、文件损坏或视觉工具确实不可用才允许真实阻塞，而且必须保存精确停点和恢复动作。

通过后运行：

```bash
python work.py notes submit <实际RUN> --note <当前笔记ID> \
  --manifest <当前manifest> --ledger <当前ledger> --report <当前最终审计报告>
python work.py checkpoint work/<实际RUN> \
  work/<实际RUN>/recovery-campaign \
  output/<当前笔记ID> -m "完成 <当前笔记ID> 全部疑点恢复与三轮复核"
```

然后在战役计划的 `execution_log` 追加一条真实记录，至少包含 `note_id`、三个不同的 `subagents`、`unresolved_before`、`unresolved_after: 0`、最终审计报告路径、最终快照、`completed: true` 和实际结束时间。没有这条三人记录，即使台账暂时通过，也不能换篇。

然后才替换三名 subagent，认领下一篇。六篇都通过后运行：

```bash
python tools/recovery_campaign.py validate \
  --subject real-analysis \
  --plan work/<实际RUN>/recovery-campaign/real-analysis.json
```

只有 `complete: true` 才能结束这场实分析战役。最终汇报必须列出六篇各自的最终审计状态、恢复记录数从多少降到多少、三轮复核快照和正文路径；不得只说“疑点已处理”。
