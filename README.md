# 数学手记工作存档

本批 12 个 PDF、项目包及来源/待办信息已获用户明确公开上传授权，见 `docs/publication-authorization.md`；同一批相同范围不再重复询问。

本批原稿已登记，等待 GPT Pro 认领识读。入口：[直接发给 Pro 的 R2 启动词](prompts/notes-pro-launch-r2.md)、[操作说明](START-HERE.md)、[本批任务](docs/ready-to-work.md)。

`work/notes` 已保存 12 个 PDF 上传文件，对应 11 份不同原稿、95 个物理页。《实分析12》的两个文件字节相同，保留两个上传名称但只建一个任务。本次未提供对应旧 Markdown，先做已有原稿，不宣称已完成旧稿对照。初始化没有识读正文，也没有用户笔记的复核通过记录。

每个新会话用本分支 `work.py` 自动创建唯一身份和 RUN：

```sh
python work.py --repo ./co-work-notes start --actor auto --token-file ../githubtoken.txt
cd co-work-notes
python work.py doctor
python work.py notes init auto
python work.py notes queue
```

记住返回的实际 RUN，再用 `notes claim 实际RUN --limit 3` 认领。远端确认后才开工；全局最多同时三份，按固定批次推进。每个 Boss 独立 clone；接续使用原身份和 RUN。

| 路径 | 保存内容 |
| --- | --- |
| `input/pdf/` | 只读原稿，保留上传名称和精确字节 |
| `input/previous-notes/`、`input/teacher/` | 后续明确提供的旧稿和教师材料 |
| `input/workflow/math-notes-project.zip` | 本次原始流程包 |
| `docs/input-map.json` | 来源登记快照、哈希、课次、物理页范围 |
| `tasks/`、`runs/` | 动态认领状态与唯一 RUN 所属，由程序事务更新 |
| `work/实际RUN/notes/笔记ID/` | 独立工作区、图像证据、映射、疑点及真实复核记录 |
| `output/笔记ID/` | 保真转写、学习稿和正式导出 |
| `.agents/skills/` | 逐页复核流程、工具与许可 |

按 [AGENTS.md](AGENTS.md)、[总协调合同](prompts/coordinator-prompt.md) 与 [单份任务合同](prompts/worker-prompt.md) 实做。`notes submit` 运行真实结构审计、核对来源与两份发布正文，保存证据后才把任务标成 `done`。此状态说明记录门槛满足，不证明数学无错或零遗漏。推送只是保存，不是结束条件。

日常用 `checkpoint` 保存明确路径，离线用 `--local-only`。共享认领必须远端确认。交接先保存具体停点，再 `notes release` 或 `notes block`，不自动抢占。命令见 [START-HERE.md](START-HERE.md)。数学研究继续留在 `rebuild/research-v2`。
