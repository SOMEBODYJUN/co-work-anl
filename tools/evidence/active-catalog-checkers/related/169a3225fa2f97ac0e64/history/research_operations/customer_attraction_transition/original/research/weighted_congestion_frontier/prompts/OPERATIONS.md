# 当前不相关并行机的共同操作入口

当前主攻 UM-TARGET-v1，save=unrelated-machines。完整目标、恢复、阅读、通信、入库和提交合同在[可复制BOSS提示词](../../unrelated_machines/BOSS_START.md)，逐命令手册在[本题RUNBOOK](../../unrelated_machines/RUNBOOK.md)。本目录的历史名称不选择数学模型。

唯一程序为research/weighted_congestion_frontier/tools/work.py；单文件可恢复仓库，随后使用仓库内最新版，内部调用checkpoint.py和board.py，不要求用户上传后二者。未绑定clone默认新题；已有绑定不改写，新题另用独立clone。首次仍显式指定：

```sh
python3 <附件work.py实际路径> --repo <本对话独立clone> start --save unrelated-machines --actor <本对话唯一编号> --token-file <仓库外凭据>
```

实际路径由agent确定。核对branch=main、save=unrelated-machines、本人编号/桌面、research_entry和research_prompt；已有工作先保留。后续在仓库根用同一work.py的sync、read、inbox、send、dm、ack、visit、pending、retry和checkpoint。正常研究不绕过work.py直接调用board.py；底层旧事件无save仍属于shared，直接board的无save视图还会汇总不同存档。

每个独立Work使用自己的clone和一个稳定发布编号，内部subagents由boss汇集。main保存研究资产，wcg/board保存消息，不创建研究分支。凭据留clone外，不进URL、正文、公屏或Git。公屏和私聊按存档路由；私聊为视图分流，原始同仓记录可读。retry保持原ID和原存档，不将旧待发消息改投新题。

默认checkpoint选择本题专题、原文、共同登记及本人桌面，排除旧题正文、共享工具修改和他人草稿；显式paths替换默认范围，须列全。保存前安全同步、核对实际数学增量和相关登记、运行对应核验及check_active_research/check_assets。程序检查全部待推历史；真实冲突保留双方并按内容处理，禁止force或自动ours/theirs。仅status=pushed且远端含实际提交才报告已保存。

用户明确选择旧题时，使用独立已绑定shared或显式--save shared的clone，数学读取从旧题README/MODEL/CLAIMS进入，不把它当本次默认任务。旧版操作正文可由Git历史恢复。
