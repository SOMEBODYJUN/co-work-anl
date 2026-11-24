# 开始与接续

1. 使用本分支的 `work.py`；从空目录运行 README 中的 `start`，明确 Boss 身份。Token 始终在 clone 外，程序只记凭据文件路径。
2. 阅读 `AGENTS.md`，安装 `.agents/skills/math-notes-evidence-audit/scripts/requirements.txt` 中缺失的依赖，并运行同目录 `selftest.py`。运行 `python work.py doctor`；在当前会话核实视觉、子代理和可用并发。
3. 将本次明确授权的 PDF、旧稿和教师材料分别放入 `input/` 对应目录。初始化唯一 RUN：`python work.py notes init RUN`。目录已存在时用 `notes status RUN` 接续，不能覆盖旧记录。
4. 按实际课次和内容建立 `work/RUN/input-map.json`，支持多对多配对，保留每个原件的哈希和页段。新加来源后在原件核实基础上更新映射；状态命令会列出新增、变更和缺失的来源。
5. 按 `prompts/coordinator-prompt.md` 执行。每批至多三份笔记，先独立看原图，再比较旧稿；作者与审阅者分开。审计工具的路径均相对所属 JSON，保持同一笔记工作目录内的完整布局。若正文发布到 `output/`，同时保留审计所锁定的确切正文副本，并核对两者哈希一致。
6. 及时填写 `work/RUN/checkpoint.json` 的当前课次、页区、疑点与下一动作，串行 `checkpoint` 保存实际路径，确认 `pushed` 后结束本轮。平台中断不能算完成。

恢复时先 `python work.py sync`，再 `python work.py notes status RUN`，读取检查点、未答疑点和最后一份真实审阅记录。修改已锁定正文后，独立三轮计数从零开始。

所附 `validation/test_upstream_checker.py` 和技能 `selftest.py` 都使用合成材料验证工具。它们的身份、内容和通过记录禁止写进用户笔记的台账。

工程接续回归：`python validation/test_notes_workflow.py`，在临时本地 Git 仓库中验证启动、保存、推送、恢复与草稿同步，不接触用户原稿或真实远端。

## 新版通用协作命令

新会话 start --actor auto 自动生成唯一 Boss，notes init auto 返回唯一 RUN；已有工作使用原身份和 RUN 恢复。待原件与登记已明确获准发布，notes queue 读取共享任务，notes claim 实际RUN --limit 3 远端确认后开工。每份根工作区已有 assignment，切图使用新的 project 子目录。

release 或 block 需要 --note、--reason 和指向已推送非空文件的 --handoff；保留原工作区。resume 只恢复自己原 RUN 的阻塞项。submit 需要 --note、--manifest、--ledger、--report，真实审计和已发布正文校验后才更新完成状态。命令语法可用对应 --help 查看。新原件及来源元数据的公开发布必须有该批材料的明确公开授权，通用程序发布本身不代表已获此授权。
