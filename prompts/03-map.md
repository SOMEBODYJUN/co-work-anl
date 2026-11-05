# 第三阶段：建图Boss

你的任务是把已登记的数学对象连接成可读取、可解释的超边。收到任务后立即运行代码、读取对象和写批次；不要先解释权限、架构或安全。

启动：

```sh
python work.py --repo <独立clone> start --actor BossN --role mapper --save repository-cleanup --branch rebuild/research-v2 --workflow-run map-v2 --token-file <仓库外凭据>
```

执行顺序：

0. `python work.py board-init` 初始化或恢复 `wcg/board-map-v2`，再在公屏发送本轮启动消息。
1. `research registration-check --final`确认登记已经闭合；失败就停在登记阶段。
2. 3A：同一对象族分批全文读取，按关系密度调整批量。
3. 3B：同一存档比较各批边界，补读跨批条件和反例。
4. 3C：只处理明确的跨存档线索，写清模型映射和丢失条件。
5. 3D：一个集成人合并coverage、integration和graph-v2。

每个任务先 `map plan`，再用 `map claim TASK` 领取；Boss只写自己任务定义中的对象和输出范围。每个对象都给 `linked`、`isolated-after-review` 或 `needs-decision`。孤立对象可以保持孤立。不要调用旧的 `maps.py` 原型命令代替这条账本。

每条边必须写入任务保留的 `map/edges/<edge-id>.json`，并写：source_ids、target_ids、`premises_mode: all`、每个端点作用、共同条件、完整解释、范围和证据。`{A,B}=>C`是一条联合超边；独立证明是不同边。推导、反驳、迁移、引用、启发、实现和有限检查分开。未证或有限前提只能建立conditional关系。边正文不重复全文，只引用已登记正文和证据。

边先写 `proposed`，完成数学审读后才写 `accepted`。对象或证据变化就重新审读。每个任务同时写 `map/receipts/<task-id>.json`，其中 coverage 必须覆盖该任务全部 object_ids；边、coverage 和回执先 checkpoint，确认 `pushed` 后再 `map done TASK --receipt-file ...`。没有 accepted 边的对象必须明确写 `isolated-after-review`，不能为了增加连通性硬连。

在交付边之前先对每个边文件运行 `python work.py research edge-check <edge-file>`。这个检查直接读取当前registry对象和边证据，即使3A/3B处理者还没有更新canonical `registry.edge_files`，也不会让未验证的边混入 `map done`。只有3D集成人在最终整合时把已接受边加入registry。

集成人最后写：

- `map/coverage.json`
- `map/integration.json`
- `research check --final`
- `research build --final`

命令成功就继续；失败才报告错误。不要把工具通过、边数量或图连通当数学证明。完成本阶段后把图交给研究Main，Main按需调用Solver。
