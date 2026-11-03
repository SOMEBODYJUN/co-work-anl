# 分阶段提示词

新增执行入口：[2.5第三步](02.5-3-register.md)、[第三阶段](03-map.md)、[Main](research-runtime.md)、[障碍Solver](solver-obstacle.md)、[成果Solver](solver-full.md)。完整命令和部署边界见[IMPLEMENTATION](../research/IMPLEMENTATION.md)。它们承接下面旧的“另定设计”；不重做2.5前两步，也不把工具完成当作全仓完成。

2.5第三步和第三阶段均已扩为可粘贴的完整Boss启动词；内部处理者分别用[02.5-3-worker](02.5-3-worker.md)和[03-map-worker](03-map-worker.md)。后续交付必须搭配支持`--workflow-run`的最新根work.py，不能继续用第二步旧zip。两阶段本轮只准备，实际启动由用户另行指令；总入口见[PHASE3_READINESS](../research/PHASE3_READINESS.md)。

- [02-clean.md](02-clean.md)：第二阶段读冻结原文、比较、归类、写正文与逐来源处置。
- [02.5-research.md](02.5-research.md)：2.5分步总入口。
- [02.5-1-inventory.md](02.5-1-inventory.md)：第一步单Boss与六名gpt-6-sol/high内部代理快速定性、清理，未来由本对话接续执行。
- [02.5-2-distill.md](02.5-2-distill.md)、[02.5-worker.md](02.5-worker.md)：第二步对象群Boss与实质处理者。
- [02.5-3-register.md](02.5-3-register.md)：对象登记、版本、附件owner和读取入口。
- [03-map.md](03-map.md)：分批构图、跨批补边、覆盖和单Boss集成。

前两步的分类/编辑任务不预设最终节点与超边格式，不部署数学研究运行时。方法由实质数学处理者自由选择。程序规格与部署状态见 [CURATION](../research/CURATION.md)。
