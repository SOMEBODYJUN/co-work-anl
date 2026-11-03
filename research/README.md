# 数学整理与后续研究设计入口

[上游实读与适配](UPSTREAM_ADAPTATION.md)记录Pharos固定commit、源码/提示词位置和采用的读取机制。

用户已授权把2.5第三步、第三阶段与研究使用一起落实。[IMPLEMENTATION.md](IMPLEMENTATION.md)是已实现v2接口与完整命令，[GITHUB_RESOURCES.md](GITHUB_RESOURCES.md)记录Codespaces/Actions和权益边界。入口为work.py research；新map任务账本与旧curate/map原型分开。此处不自动替2.5前两步作数学判断，也不声称全仓登记和图已完成。下文原型说明仅作历史背景，其“待后续设计”已由这次接口设计承接。

当前执行设计见 [CURATION.md](CURATION.md)：2.5.1材料定性、2.5.2对象群数学整理；[第一步提示词](../prompts/02.5-1-inventory.md)、[第二步Boss](../prompts/02.5-2-distill.md)及[worker](../prompts/02.5-worker.md)已分开。材料分类不是数学真值审查或最终节点准入，原本好内容直接沿用。

[分类判据](PHASE25_TRIAGE.md)、[对象群任务与出口](PHASE25_DISTILL.md)、[新协作域](CURATION_OPERATIONS.md)和[程序规格](PHASE25_PROGRAM.md)供前两步使用。材料批次与对象群任务程序已实现，第一步run正在逐份分类、清理明确非数学页；新公屏尚未创建。

2.5.3重新登记、第三阶段超边格式与数学研究Agent由用户与另一AI另定。前两步保留路径、字节版本、可理解正文、原材料去向和具体缺口即可，不强制按未来节点拆页或造ID。

`tools/curation.py`、`tools/maps.py`、本目录现有准入/packet/result schema、templates与 [research-runtime.md](../prompts/research-runtime.md)均为可参考原型，不表示研究运行框架已定。上一版完整协议见 [CURATION_PROTOTYPE_V1.md](CURATION_PROTOTYPE_V1.md)。不以当前实现限制倒逼前两步数学组织，也不以结构测试通过宣称数学正确。

上游研究对照见[原始规范及代码对照](../cleanup/audits/phase25-design/upstream_requirements.md)。引用不自动构成依赖、未证不能作真前提等数学要求仍有价值；具体schema、读取窗口和运行策略等待后续负责人定案。
