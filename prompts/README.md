# 分阶段提示词

每阶段只把该阶段一份完整Boss词、最新版work.py和仓库外凭据交给新对话；内部worker词由Boss自行读取，不要求用户额外粘贴。

| 阶段 | 完整提示词 | 作用 |
| --- | --- | --- |
| 接下来：2.5第三步 | [02.5-3-register.md](02.5-3-register.md) | 稳定对象身份、正文/证据入口、分批集成 |
| 接下来：第三阶段 | [03-map.md](03-map.md) | 从内到外建立解释充分的超边及投影 |
| 后续实际研究 | [research-runtime.md](research-runtime.md) | Main持续调度原Solver，使用完整证据与反馈 |
| 已完成：2.5第二步 | [02.5-2-distill.txt](02.5-2-distill.txt) | 仅用于必要的原任务接续修订 |
| 已完成：2.5第一步 | [02.5-1-inventory.md](02.5-1-inventory.md) | 分类、标号与目录 |
| 已完成：原第二阶段 | [02-clean.md](02-clean.md) | 冻结来源处置与正文清洗 |

登记/构图各自使用独立workflow-run、公屏及同一协作引擎，见[阶段入口](../research/PHASE3_READINESS.md)。后续自由研究的每个新RUN固定三个槽位（obstacle-1/full-1/full-2），输入仅有[障碍组](solver-obstacle.md)和[成果组](solver-full.md)两类，不提前在登记/构图阶段启动。登记与构图使用实际可用并发，不受该三槽研究配置限制。
