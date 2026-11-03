# 数学研究仓库

这是结果分支 `rebuild/research-v2`：第二阶段整理数学正文；2.5依次做材料定性、对象群整理、对象登记，再分批建立超边并供Work中的数学Solver按需读取。各步完成范围以实际记录为准，不能把脚手架或来源done当作数学质量验收。

- [可运行的登记、超边和研究接口](research/IMPLEMENTATION.md)：v2记录、分批建图账本、两类Solver、具体反馈、持续保存和恢复。工具完成不等于全仓已登记/已建图，2.5前两步继续独立执行。
- [GitHub资源与部署](research/GITHUB_RESOURCES.md)：学生权益、Codespaces环境、Actions检查/计算、实际复现入口及尚未启用的云端部分。

- [研究存档](archives/README.md)：四个主要问题家族、独立数学工具及待确认方向；父子问题明确归档。
- [全仓数学关系图](map/README.md)：旧graph.json原型保留；新接口输出独立graph-v2.json，不自动接纳历史对象。
- [三阶段清洗入口](cleanup/README.md)与[全量逐文件勾选](cleanup/CHECKLIST.md)。
- [第二阶段提示词](prompts/02-clean.md)、[2.5第三步登记](prompts/02.5-3-register.md)、[第三阶段建图](prompts/03-map.md)、[Main研究启动](prompts/research-runtime.md)。
- [2.5分步入口](research/CURATION.md)：本轮执行[第一步材料定性](prompts/02.5-1-inventory.md)并准备[第二步对象群整理](prompts/02.5-2-distill.md)；[worker提示词](prompts/02.5-worker.md)、[协作设计](research/CURATION_OPERATIONS.md)及[程序契约](research/PHASE25_PROGRAM.md)。第三步与超边设计由用户与另一AI负责。
- [程序与协作操作](tools/README.md)、[命名和入库规则](cleanup/OBJECTS.md)。
- [整理质量审查](cleanup/audits/2026-10-30/质量审查.md)：固定快照的来源—正文抽查，记录覆盖矩模型身份冲突和已入库正文的导航缺口；done不等于语义验收通过。

原始资料留在独立来源分支，冻结版本见cleanup/sources.json；本树不再复制成套旧history与工作区。使用work.py读取源文件，持续记录其语义处置。当前主攻仍是客户吸引的恰六人完整历史纯SPE半覆盖；其他存档保留其各自模型、问题和发展性研究，不混合结论。
