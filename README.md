# 数学手记工作存档

本分支 `work/notes` 保存笔记原稿、保真转写、复习稿、来源映射、疑点、复核与接续记录。
入口是 [START-HERE.md](START-HERE.md) 与 [完整启动词](prompts/launch-prompt.md)。

```sh
python work.py --repo <独立目录> start --actor Boss1 --token-file <仓库外凭据>
cd <独立目录>
python work.py doctor
python work.py notes init <唯一RUN>
```

每个新 Boss 使用独立 clone 和 RUN；续接用同一身份及 RUN，执行 `notes status RUN`。
运行中的笔记、独立审阅与 Git 保存规则见 [AGENTS.md](AGENTS.md)。

| 路径 | 保存内容 |
| --- | --- |
| `input/pdf/` | 用户原始 PDF，只读保留 |
| `input/previous-notes/`、`input/teacher/` | 旧稿与教师材料，只读保留 |
| `work/<RUN>/` | 课次/页段配对、哈希、识读台账、图像证据、疑点和检查点 |
| `output/<笔记ID>/` | 按原稿顺序的保真转写、按复习顺序的学习稿及正式导出 |
| `.agents/skills/` | 项目内逐页复核和数学编辑流程、工具与许可 |

保存明确范围，并确认返回 `pushed`：

```sh
python work.py checkpoint input work/<RUN> output/<笔记ID> -m "保存本次识读与断点"
```

暂时无法推送时加 `--local-only`；之后用相同完整范围重跑即可。原件、正文、来源映射、审阅报告、已登记的图像证据和检查点均可提交，只有缓存、编译临时文件与凭据被忽略。主代理串行提交；同步会保留本地草稿，真实冲突需解决后接续。

当前没有导入本批待识读的原始笔记，也没有完成任何用户笔记的复核。工具自检只验证程序行为。锁定版本上的三轮独立全量复核仍由真实读图和审阅完成。

数学研究继续使用 `rebuild/research-v2`。两分支各自维护工作目录，按需迁移具体通用修复。
