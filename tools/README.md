# 统一入口work.py

用户每阶段只需根work.py、仓库外凭据及一份[完整阶段词](../prompts/README.md)。程序恢复独立clone后，使用clone根最新版；内部模块由程序调用，不让用户另配一组Python。

先检查本地目录、Git状态、remote和远端，保留已有工作。新对话显式--actor Boss编号；继续原对话沿用身份、clone和未完任务。具体阶段启动命令见[阶段入口](../research/PHASE3_READINESS.md)。凭据不进remote、正文或提交。

| 入口 | 实际用途 |
| --- | --- |
| start / doctor / sync / checkpoint | 身份与真实写端点、同步、明确路径保存及pushed确认 |
| registration-task | 登记批次的lead、plan、list、claim-next、done、handoff、collect |
| map | 同引擎的构图任务，另有read-add及assemble集成 |
| research | inputs/freeze/compose/register、对象/超边读取、packet、save/resume |
| compute / github | 普通云端批处理请求、运行与结果取回；按需环境管理 |
| read / inbox / send | 当前绑定公屏；消息不代替认领或完成回执 |
| clean / triage / curation-task | 原来源及前两步任务，不混入新阶段 |

常用保存与读取：

```sh
python work.py sync
python work.py checkpoint <本次明确路径> -m '具体成果及范围'
python work.py read --thread rebuild-v2 --limit 20
python work.py inbox
```

任务读最新元数据；普通竞争自动重选，响应未知核原request_id，不反复新认领。Boss串行组织同clone Git，各worker直接写约定独立文件。正文/边/批次和收据先确认pushed，再done。暂停用当前阶段handoff --all --reason，lead另交接；认证受阻仅local-only保全，不冒称完成。

[实际命令与字段](../research/IMPLEMENTATION.md)说明两阶段批次、共享只读依赖、自动汇总和最终数学整合。[研究流程](../research/RESEARCH_WORKFLOW.md)说明完整ALL支持、替代分支、候选与反驳、原Solver接续。[云端入口](../research/GITHUB_RESOURCES.md)说明普通程序如何提交及取回结果；不默认开Codespaces，不默认在创建环境时跑旧演示或整套测试。

旧curate和map check/build只保兼容读取，不是新登记/构图协议；旧来源命令见[cleanup](../cleanup/README.md)，原对象群命令见[CURATION_OPERATIONS](../research/CURATION_OPERATIONS.md)。
