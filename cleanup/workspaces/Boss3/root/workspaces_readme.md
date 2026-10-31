# 个人研究工作区与恢复

最新方向：所有团队只研究一般人数、一般共同目录的Q-CAG-HALF；停止特殊人数、特殊目录和局部常数任务。有限实例仅检验明确的一般候选或核验真正目标反例。旧身份、绑定和数学资产保留不表示恢复旧任务；做不出来不构成不可能性证明。 个人区的完整恢复索引见[WORKSPACE_RESULTS](../customer_attraction/WORKSPACE_RESULTS.md)；恢复时在本人README区分当前一般义务与已暂停的旧任务。

当前主攻 **Q-CAG-HALF**，存档 **customer-attraction**。统一入口为根[work.py](../../work.py)，启动、交流和恢复命令见[RUNBOOK](../customer_attraction/RUNBOOK.md)。

每个独立对话一个 clone，start 自动生成或复用 actor，个人目录在 main 的 `research/workspaces/<save>/<actor>/`。可以自由建立自己的项目文件夹；Boss 的团队由所在对话汇总保存，不另开研究分支。

这里首先是持续备份区：未完成、未核验、后来发现错误的推导、代码、实验与失败尝试都可以提交，标清现状即可。每有一段新工作、换路线或中断前保存，不必先成为有价值成果、登记 Claim 或通过数学审查。README 写正在做什么、文件在哪、卡点与下一步。

```sh
python3 work.py workspace
python3 work.py checkpoint <回执中的本人工作区路径> -m '阶段备份：当前推导与下一步'
```

回执 `status=pushed` 表示已推送远端；只有本地文件而未 checkpoint，换环境时无法从远端恢复。同 clone 继续用原身份；环境丢失后，用附件程序 start 加原 actor 和 `--resume`，读取已保存的 README 接续。

共享正文、候选、审查和研究地图按数学对象组织，不按角色分区。个人备份不自动进入可靠结论；检查整理后进入相应共享位置，工作区链接其正式正文。同行用 `visit` 可以读取已推送的个人材料；公屏和私聊继续用根 work.py。

新 clone 默认 customer-attraction，旧 shared/unrelated-machines 保留原绑定。默认 checkpoint 只附加本人工作区；显式路径会替换默认范围，要列全本次应保存路径。
