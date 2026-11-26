# RA12 收尾后处理交换代数

你是唯一 Boss，使用一个 RUN 完成下面六篇，顺序固定：

```text
RA12 → CA07 → CA09 → CA10 → CA11 → CA12
```

所有 subagent 使用 `gpt-6.2-sol`，推理强度 `max`。每篇固定三名新的 subagent，只处理当前这一篇。当前篇通过审计并记录完成后，三人退出，下一篇换三名新 subagent。

先找到仓库。当前对话已经提供了仓库外的 `work.py` 和 `githubtoken.txt`。若 clone 尚未存在，直接执行：

```bash
python <附件work.py> --repo <独立clone> start \
  --actor auto \
  --remote https://github.com/SOMEBODYJUN/co-work-anl.git \
  --token-file <附件githubtoken.txt路径>
cd <独立clone>
python work.py doctor
python work.py notes init auto
```

然后执行：

```bash
python tools/recovery_inventory.py
python tools/recovery_campaign.py inventory --subject ra12-then-commutative-algebra
python tools/recovery_campaign.py init \
  --subject ra12-then-commutative-algebra \
  --run <实际RUN> \
  --out work/<实际RUN>/recovery-campaign/ra12-then-commutative-algebra.json
```

## RA12

RA12 已有正文、图像证据和审计台账。读取现有 assignment、manifest、ledger、两份正文、最新 audit report 和 `autonomous-recovery/recovery-plan.json`。当前审计列出的三条疑点必须逐条处理：

- RA12-P001-U04 的 Lemma 对象和映射方向；
- RA12-P003-U01 的函数与定义域并写；
- RA12-P006-U02 的 Borel–Cantelli 旁注集合运算符。

三名 subagent 分别完成高分辨率读图、数学上下文恢复和对抗审计。每条疑点至少列两个候选，回原 PDF 做 800 dpi 定向裁图，必要时 1200 dpi，结合作者记号、前后定义、证明和后文引用做正向及反向检验。三份独立记录完成后由 Boss 合并，更新两份正文、source/target 映射、recoveries、issues 和证据哈希。

内容改动后废弃旧终审链。只有新的 `audit_pass=true`、`content_resolved=true`、`unresolved_count=0`、三轮终审完整且正文哈希一致，RA12 才完成。然后执行 `notes submit`、checkpoint，并在战役 `execution_log` 写入三个 subagent、恢复前后记录数、最终快照和 `completed: true`。

## CA07、CA09、CA10、CA11、CA12

交换代数五篇当前没有正文和审计工作。每篇认领后都从原 PDF 新建 project，先完成：

1. 原 PDF 全页图和重叠分区图；
2. 独立首遍逐页逐区读图；
3. `source-transcript.md`；
4. `study-notes.md`；
5. source/target 双向映射、术语表、页区观察和初始疑点表。

首遍完成后，三名 subagent 继续做第二遍检查和疑点恢复。每条模糊字、公式、上下标、理想/商环记号、同态箭头、证明省略和页边内容都必须回原图，列候选，做上下文推断和正反向数学检验。不能从实分析工作区复制正文、审计记录、候选或 reviewer 身份。

每篇必须满足以下条件后才能换篇：

- `audit_pass=true`；
- `content_resolved=true`；
- `unresolved_count=0`；
- source、target、recovery、issue、page_checks、region_checks 全部完成；
- 最新内容快照上的第二遍复核和三轮独立终审完成；
- 两份正式正文与审计正文哈希一致。

任何一项未完成，继续当前三人的工作。完成后才执行 `notes submit`、checkpoint 和 execution log，再认领下一篇。

最后运行：

```bash
python tools/recovery_campaign.py validate \
  --subject ra12-then-commutative-algebra \
  --plan work/<实际RUN>/recovery-campaign/ra12-then-commutative-algebra.json
```

只有六篇全部完成、所有未决记录归零、六条 execution log 都有三个不同 subagent 时，任务结束。
