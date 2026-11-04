# 数学材料整理仓库

当前正在做 **2.5第二步**：接续已有分类，复用成熟数学，整理数值机制、片段和混合内容，删除无用包装。各对象沿用自己的模型与问题；本步的完成标准是准确处置材料并留下可用正文。

用户只需 **一个work.py、已有仓库外凭据、一份[当前提示词](prompts/02.5-2-distill.txt)**。内部程序和说明由执行者按需读取。已有Boss沿用原身份和草稿，成熟成果立即保存，持续补位至本阶段可处理材料完成。

- [材料分类目录](curation/catalogs/INDEX.md)与[当前任务目录](curation/runs/20261103-boss6-current/TASKS.md)。实时进度查询 `work.py curation-task status --run 20261103-boss6-current`。
- [当前操作说明](research/CURATION_OPERATIONS.md)、[工作规则](AGENTS.md)与[数学对象命名规则](cleanup/OBJECTS.md)。
- [数学正文](archives/README.md)与必要复现证据 `tools/evidence/`。无用日志、旧交付件和重复副本直接删除，不另存历史目录。

其它阶段有独立入口，按用户指定启动：[原第二阶段来源清洗](cleanup/README.md)、[2.5第三步与第三阶段](research/PHASE3_READINESS.md)、[后续研究流程](research/RESEARCH_WORKFLOW.md)、[程序接口](research/IMPLEMENTATION.md)及[GitHub资源](research/GITHUB_RESOURCES.md)。原始来源的冻结版本见 `cleanup/sources.json`；原来源done与数学质量验收分别判断。
