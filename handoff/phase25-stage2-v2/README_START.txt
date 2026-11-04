2.5第二步可执行修订包 v2

本包提供实际程序和提示词，不是审计报告。

已有对话：把RESUME_EXISTING.txt全文贴给该对话。它会保全草稿、在原clone运行work.py sync更新，再继续原Boss已领数学。无需换号、重做分类或重领已完成任务。

新Project/新对话：上传本包work.py，另附你原有有效githubtoken.txt（本包不含凭据）；Project说明可用PROJECT_INSTRUCTIONS.txt。把02.5-stage2-prompt.txt全文粘贴给新对话，首行填唯一Boss编号；指定一个协调Boss，其余数学处理。路径由代理自动识别，独立clone从原仓库恢复正文、任务和其它脚本，不新建GitHub仓库。

实际修改：
1. receive-pack的cannot-lock-ref/expected并发竞争也会刷新重试。
2. status聚合、list默认短行，支持owner/state/available/limit；--full保留完整记录。
3. batch一事务处理多个任务，部分冲突单列；claim可合并预留，finish合并提交与完成，handoff-all一次交接。
4. 意图及回执保存在本clone Git缓存，同request_id可retry；旧任务数据和单项CLI仍兼容。
5. 任务事务仅展开必要元数据/输入，Git索引保留原完整树；数学原件不被事务重写。
6. 成熟数学用reuse_paths共享复用，不占独占写锁；资产仍保持path/SHA两字段。
7. 成果广播复用Git对象缓存，同次发布重试不重复验同一资产。
8. 提示词先认领后派工；纯包装由协调者分批，数学Boss不办身份页启动仪式；运行边界一次交接。

文件：
work.py：新版自足启动器（通常只需上传这个程序文件）
02.5-stage2-prompt.txt：完整新对话提示词
RESUME_EXISTING.txt：已有对话直接继续词
PROJECT_INSTRUCTIONS.txt：Project说明
02.5-worker.md：内部处理者词参考，运行时读仓库最新版本
README_START.txt：本说明
BUILD_INFO.json、SHA256SUMS.txt：实际构建版本与文件校验
source/tools/：本次三个实际改动模块的源码备份，正常启动由仓库自动取得，无需单独上传

运行域、公屏和各Boss实际任务归属均保持；这个修订包本身没有替任何Boss认领、释放或修改数学。第三步和超边方案不在此执行。
