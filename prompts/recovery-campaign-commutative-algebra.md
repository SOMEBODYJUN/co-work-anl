# GPT Pro 交换代数疑点清扫启动词

你是这场交换代数工作的唯一 Boss。这个启动词用于实分析六篇疑点战役完成后，集中处理仓库中的交换代数原稿：CA07、CA09、CA10、CA11、CA12。目标是逐篇把正文、来源映射、数学恢复和审计疑点全部收敛；不能把“已经登记”“已经写过一稿”或“疑点暂存”当成完成。

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

先确认实分析战役已经通过，再运行：

```bash
python work.py doctor
python tools/recovery_inventory.py
python tools/recovery_campaign.py inventory --subject commutative-algebra
python work.py notes queue
```

创建本战役计划：

```bash
python tools/recovery_campaign.py init \
  --subject commutative-algebra \
  --run <实际RUN> \
  --out work/<实际RUN>/recovery-campaign/commutative-algebra.json
```

## 核心执行约束

按以下顺序逐篇处理：

```text
CA07 → CA09 → CA10 → CA11 → CA12
```

同一个 Boss 和同一个 RUN 贯穿全部五篇。每次只认领一篇，完成全部疑点、修订、冻结和三轮复核后，才换下一篇：

```bash
python work.py notes claim <实际RUN> --note CA07 --limit 1
```

一篇笔记始终由三名互相独立的新 subagent 组成同一核心小组，三人同时只做这篇，不能拆去三篇。完成当前篇后，三人全部更换；下一篇必须是新的一组三人。三人的角色分别是：

1. **视觉恢复者**：整页 → 重叠分区 → 800 dpi 定向裁图 → 必要时 1200 dpi，逐项记录符号、上下标、集合、理想、商环、同态箭头、图表和页边内容。
2. **数学上下文恢复者**：独立列至少两个候选，结合定义、引理条件、证明前后步、例子和后续引用做正向与反向验证；数学成立不等于字迹已确认。
3. **对抗审计者**：核查 source/target 双向映射、重复内容、旧稿去向、页区覆盖、recoveries、issues、哈希和隐藏遗漏，主动找出正文与证据不同步的问题。

三人先各自保存盲读、候选和检查结果，再由 Boss 合并。不能用多数票消灭分歧；分歧必须追加扫描、扩大上下文或补反算。任何仍有未决的条目都回到原 PDF，而不是交给用户。

## 每篇必须做完的循环

1. 读取该篇 assignment、manifest、ledger、最新审计报告、两份正文、所有交接和自动恢复清单；建立 source、target、recovery、issue、全页和全区疑点总表。
2. 每条疑点回到原图做高精度扫描。记录候选笔画、同一作者的记号习惯、邻页和证明上下文；对每个候选做前向和反向数学检验，再回图比较位置与形状。
3. 同步更新两份正文、来源映射、恢复记录、疑点结论、颜色标签和证据哈希。蓝色可以写模型补证或纠错，黑色保留原稿内容，不能把未经证据支持的猜测伪装成原文。
4. 每次实质修改都生成新内容快照，使旧终审链失效；先完成第二遍全页/全区检查，再在新快照上完成连续三轮独立终审。
5. 只有 `audit_pass=true`、`content_resolved=true`、`unresolved_count=0`、双向映射完整、三轮终审完整且正式正文哈希一致，才算当前篇完成。

“看不清”不是结束条件。若仍有两个可成立候选，继续找同一作者的写法、前后定义、证明约束和更高分辨率图；选出证据最强者并登记被排除候选。若视觉工具或原 PDF 真正不可用，保存具体停点，保持任务认领，恢复后继续；不得把内容疑点改成 `NeedsHuman`、`block` 或用户判字任务。

完成当前篇后，先在战役计划的 `execution_log` 追加一条真实记录，至少包含 `note_id`、三个不同的 `subagents`、`unresolved_before`、`unresolved_after: 0`、最终审计报告路径、最终快照、`completed: true` 和实际结束时间；然后才可执行 `notes submit`、checkpoint 并更换三人小组。五篇全部完成后运行：

```bash
python tools/recovery_campaign.py validate \
  --subject commutative-algebra \
  --plan work/<实际RUN>/recovery-campaign/commutative-algebra.json
```

只有 `complete: true` 才能结束交换代数战役。最终汇报逐篇列出疑点记录变化、最终快照、三轮复核和两份正文路径；不以一段总括话替代逐篇证据。
