# 使用入口：一般半覆盖与三个角色

当前主攻 **Q-CAG-HALF**，存档 **customer-attraction**。统一程序为根[work.py](work.py)，详细操作只维护[当前RUNBOOK](research/customer_attraction/RUNBOOK.md)。

1. 新对话复制[Boss](research/customer_attraction/BOSS_START.md)、[清洗者](research/customer_attraction/CLEANER.md)或[整理者](research/customer_attraction/EDITOR.md)之一，附完整work.py及仓库外githubtoken.txt。
2. 程序恢复独立clone，自动生成或复用R-UUID，绑定customer-attraction和相应角色。核对回执中的main、save、workspace、研究入口和role_prompt。
3. 沿[本题短地图](research/customer_attraction/README.md)直接开展角色工作。Boss不等待清洗者或整理者批准探索。
4. 公屏、提及、私聊、sync和checkpoint均使用同一程序。重要阶段同步地图并推送；回执status=pushed才算远端保存。

已有shared或unrelated-machines等存档的clone保留原绑定；新题用新clone，不自动接管他人身份。旧研究的数学入口见[总目录](research/README.md)，旧操作提示词不是当前默认任务。
