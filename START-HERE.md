# 开始与接续

本批 12 个 PDF、项目包及来源/待办信息已获用户明确公开上传授权，见 `docs/publication-authorization.md`；同一批相同范围不再重复询问。

直接使用 [启动词](prompts/launch-prompt.md)。使用 `work/notes` 根 `work.py`；之前数学分支的同名程序不是本入口。

## 启动和认领

1. 从仓库外的本分支程序执行 `--repo 独立目录 start --actor auto --token-file 仓库外凭据路径`。首次生成唯一 Boss，已有目录复用绑定身份。
2. 进入返回的 clone，阅读 `AGENTS.md`、总协调与单份合同，运行 `doctor`。实际检查视觉、Python、子代理能力，安装缺失依赖并运行技能 `selftest.py`。合成自检不是用户笔记完成证据。
3. 新工作执行 `notes init auto`，记住返回的实际 RUN；已有 RUN 用 `notes status 实际RUN`。每个 Boss 独立 clone、唯一 RUN；程序拒绝复用其他 Boss 的 RUN。
4. `notes queue` 读远端；`notes claim 实际RUN --limit 3` 认领当前批次可用任务。也可 `--limit 1` 或 `--note RA06`。远端确认后才识读。
5. `checkpoint work/实际RUN -m "保存认领和工作区"` 保存实际身份、来源、分工及断点。

认领事务使用普通 Git 推送作原子竞争。两个会话抢同一份只有一个成功，失败方重读队列。事务不提交本地其他草稿。全局最多三份 `claimed`，按 `docs/batch-plan.json` 推进。明确 `blocked` 的任务保留未完成及交接；不会自动超时释放或抢占。共享状态以远端 `tasks/` 为准，来源快照不会随动态状态重写。

## 每份笔记

认领返回工作根目录，其中已有 `assignment.json`。切图工具要求输出目录不存在或为空，因此使用新的 `project/` 子目录，例如：

```sh
python .agents/skills/math-notes-evidence-audit/scripts/prepare_pdf.py input/pdf/实分析6.pdf --out work/实际RUN/notes/RA06/project --dpi 300
```

将 manifest、ledger、原件副本、整页/区域图、两份正文、映射、恢复及复核证据保存在该 `project/` 的完整布局中。路径均相对所属 JSON，详见工具合同。不要挪走审计正文后仍沿用旧哈希。

实际执行原图独立初读、第二位新代理全区检查、完整修订、冻结后连续三轮独立全量复核。主代理串行整合与 Git 写入，子代理只写自己的提议稿/报告。发布两份正文到 `output/笔记ID/source-transcript.md` 和 `study-notes.md`，核对与审计锁定正文哈希完全相同。

本批没有对应旧 Markdown。先做已提供 PDF，保留 `previous_notes_status: not_provided`，对照范围明确写“本次提供的原稿；未提供对应旧稿”。不能用 ZIP 示例旧稿、其他研究文档或合成账本替代。后续补旧稿时重新登记、重开受影响任务并核对，不篡改已有冻结报告。

## 保存和交接

下列 RUN、笔记 ID 和路径均取自实际工具结果，无须用户填写：

| 操作 | 命令 |
| --- | --- |
| 保存进度 | `python work.py checkpoint work/实际RUN output/笔记ID -m "识读进度和下一页区"` |
| 读取断点 | `python work.py notes status 实际RUN` |
| 同步并保留草稿 | `python work.py sync` |
| 验收提交 | `python work.py notes submit 实际RUN --note 笔记ID --manifest work/实际RUN/notes/笔记ID/project/manifest.json --ledger work/实际RUN/notes/笔记ID/project/ledger.json --report work/实际RUN/notes/笔记ID/project/audit-reports/final.json` |
| 释放供他人认领 | `python work.py notes release 实际RUN --note 笔记ID --reason "具体原因" --handoff work/实际RUN/handoff.md` |
| 真实阻塞 | `python work.py notes block 实际RUN --note 笔记ID --reason "具体阻塞及范围" --handoff work/实际RUN/handoff.md` |
| 恢复自己的阻塞项 | `python work.py notes resume 实际RUN --note 笔记ID` |

`submit` 运行真实审计，核对全部物理页的原稿指纹、旧稿范围和两份正式正文，先保存完整工作区与正文，再更新共享任务。失败保持未完成。有未决记录则继续修订或保存未完成交接，不标成 `done`。

`release`、`block` 必须引用已推送的非空交接文件，记录页区停点、有效正文/冻结版本、未决项、真实代理参与表及下一动作。保留全部旧工作区，新认领者的 `assignment.json` 含历史交接路径。恢复早前阻塞项不混入另一批正在进行的任务。

认领后本地 RUN 检查点更新活跃、完成、阻塞列表，仍须填写准确页区与下一步并保存。推送只是保存，不是停止条件；当前批次完成后继续认领下一批，直到达到门槛或遇到实际阻塞。

## 工程验证

`validation/test_notes_workflow.py` 验证启动、保存、恢复及草稿同步；`validation/test_notes_queue.py` 用本地 Git 验证认领竞争、身份/RUN、容量、批次、交接、完整合成审计提交与冷恢复。技能 `selftest.py` 验证审计结构边界。它们不接触真实远端、不认证用户笔记。
