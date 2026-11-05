# 2.5第三步与第三阶段的执行入口

2.5第二步160群与原第二阶段10,921个来源版本均已准确处置，最后56条遗留已核完。后续登记与正式图尚未批量启动。本页固定输入、职责和完成条件；任务/身份在实际启动时产生，不用空表冒充完成。

用户每阶段只需一份完整Boss词、此分支最新版work.py和仓库外凭据。内部worker词、字段说明与现行数学由执行者自行读取，不要求用户再收集Project文档。

| 阶段 | 完整Boss词 | 内部worker | workflow-run / 公屏 |
| --- | --- | --- | --- |
| 2.5第三步：登记数学身份 | [02.5-3-register.md](../prompts/02.5-3-register.md) | [02.5-3-worker.md](../prompts/02.5-3-worker.md) | p25-register-v2 / wcg/board-registration-v2 |
| 第三阶段：解释数学关系 | [03-map.md](../prompts/03-map.md) | [03-map-worker.md](../prompts/03-map-worker.md) | map-v2 / wcg/board-map-v2 |

## 身份与数学作用

原来源ID/材料号追溯版本，object_id标识精确数学对象，edge_id标识一份解释充分的关系，Boss/task/run只管协作。已有稳定Claim/object ID优先；ID不从文件路径或内容hash生成，不一页一编号。正文/证据的版本和pin绑定读取位置，不能替代数学真值。

一页可支持多个独立对象，多份材料可支持同一对象。定义、一般/条件命题、有效反例、构造、可复用方法、算法保证、猜想、障碍和具体开放义务均可登记；普通算术、纯数值、代码与PASS不自动成为节点。精确有限反例的存在性若已证明可proved，普通扫描为finite。数学open不等于身份needs-decision。

## 2.5第三步怎样闭合

lead用research inputs生成真实已发布出口的inputs.json，research freeze固定Git范围和字节。各Boss恢复本人任务，再持续claim-next，内部子代理直接写独立schema:2登记批次。批次先推送、registration-task done核交付；lead边工作边收拢，compose/register唯一总registry，不等全部人结束才整合。

核心命令：registration-task lead show/claim/handoff、plan、list --owner self、claim-next、done --receipt-file、handoff --all --reason。任务/lead位于research/operations/p25-register-v2；具体record字段见[IMPLEMENTATION](IMPLEMENTATION.md)。

完成以真实全仓输入逐项有准确去向、稳定身份、正文/证据与owner可读、跨批身份冲突处理完为准。research registration-check --final只验登记，不要求超边；不重做第二阶段或把全部证明预先拆尽。第三阶段发现遗漏的有用对象，沿用登记批次定向增量，不清空已知数学或重启全仓。

## 第三阶段怎样从内到外

3A先理清对象内部承重链，再比较同子档对象族；3B做存档内跨批/跨子档整合；3C做真实跨档映射；3D由lead统一投影。核心object_ids与输出路径互斥，共同read_object_ids共享，input_pins覆盖两者。本人任务增加已登记共享依赖用map read-add，不重派整个任务。先推送独立边/收据即可map done，不等canonical总表。持续循环与真实交接规则在完整Boss词中。

一条边完整保共同前提、端点作用、模型/量词/条件、推理解释、证据和适用范围。替代证明分开；共同定义和相似度不制造无用hub；引用/启发不混成推导。反例指向精确被否陈述，跨模型写清映射和边界。作者自己实读后accepted，真实疑点再找相关worker研讨，不另造逐边审批流水。

每个对象有准确比较范围与linked、isolated-after-review或needs-decision。明确open问题/proposed联系可以保留；不为完成度强行造边。lead用map collect读完成批，sync后map assemble保留既有边并合入独立边及coverage/integration草稿。它不自动审读或accepted；lead持续完成唯一边清单、map/coverage.json、map/integration.json的实际跨批数学整合，覆盖每个档/子档及明确跨档线索。最终清零身份/版本/交付疑点，数学未知可继续未知。research check/build --final生成子档、档和全仓三级graph-v2.json，不声称找尽所有可能联系。

## 后续研究怎样接住

正文是完整知识，registry定位精确对象，超边提供可调用的联合支持、反驳范围、迁移条件与开放义务。Main/Solver用search定位、show读正文，context按需展开；证明支持不能以固定两跳截断，也不能把替代证明并成一份全部必需的前提。数学方法由研究任务选择，不沿图机械执行。

后续Main与两类Solver的真实输入、接续、云计算分工见[RESEARCH_WORKFLOW](RESEARCH_WORKFLOW.md)和[prompts/research-runtime.md](../prompts/research-runtime.md)。日常计算优先在当前可用环境或明确云端执行，Codespaces用于确有环境/长任务需要的工作；资源调用不替代数学推理。不用测试次数、计算条数或状态表声称研究已经可行，按真实任务和实际产物判断。
