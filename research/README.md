# 数学整理、关系图与持续研究入口

这里保存共同研究接口、阶段规则、登记和运行恢复信息。完整数学内容在archives，各任务的真实状态以已发布记录为准。

- [Work研究流程与目录安排](RESEARCH_WORKFLOW.md)：Main/Solver如何用代码和资料，计算在哪里执行，研究成果怎样回流，每个目录保存什么，以及哪些云端通道尚未完成实际验收。
- [2.5第三步与第三阶段固定入口](PHASE3_READINESS.md)：完整Boss/worker启动词、稳定身份、冻结输入、分批登记、跨批/跨档整合和阶段隔离。
- [实现与命令](IMPLEMENTATION.md)：research与map命令、v2登记/超边字段、示例、反馈恢复与模板导出。
- [GitHub资源](GITHUB_RESOURCES.md)：直接PAT接口、Codespaces/Actions配置、权益与权限边界。
- [交付及验收记录](DELIVERY.md)、[本轮工程验收](checks/phase3-20261103.json)：已实际执行的检查及其范围；工程通过不证明数学真值。
- [上游代码依据与适配](UPSTREAM_ADAPTATION.md)：Pharos固定版本的具体机制和本项目保留的简化，不宣称其在本题效果最好。

2.5前两步仍使用[CURATION](CURATION.md)、[第一步判据](PHASE25_TRIAGE.md)、[第二步对象群整理](PHASE25_DISTILL.md)、[操作手册](CURATION_OPERATIONS.md)和[程序契约](PHASE25_PROGRAM.md)。第一步只分类和目录，不以标签删原件；第二步由实际执行者按当前任务整理。前两步不替最终节点造ID，也不把来源done或编辑completed当作数学真值认证。

2.5第三步和第三阶段的可执行设计已经确定。真实registry、正式超图、对应任务/身份以及数学Solver运行由实际阶段启动时产生；目录和配置准备好不等于这些任务已完成。

`tools/curation.py`、`tools/maps.py`、旧graph.json以及本目录部分schemas/templates属于[旧准入/运行原型](CURATION_PROTOTYPE_V1.md)，保留兼容和追溯。当前v2以PHASE3_READINESS、IMPLEMENTATION、根prompts和实际程序为准。当前research-runtime.md及两类Solver提示词是已发布研究使用规范，不再把它们笼统标为待定旧原型。

早期准入讨论仍见[上游要求对照](../cleanup/audits/phase25-design/upstream_requirements.md)。其中保全量词/定义、联合前提、版本变化后重判、引用不等于推导等原则继续适用；不同版本的具体schema不能混用。
