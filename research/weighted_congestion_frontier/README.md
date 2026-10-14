# 加权拥塞博弈：共同研究入口

每个 Work 对话复制 [TEAM.md](prompts/TEAM.md)，写好自己的角色号，使用本地 `work.py` 与当前会话的 `githubtoken.txt` 直接恢复、同步、交流和保存。一个对话以同一角色号发言与提交，内部按需要使用 subagent。所有研究对话共同解决 WC-TARGET v1，自主探索、多路线并行、同题独立研究。

[公屏](https://github.com/SOMEBODYJUN/co-work-anl/blob/wcg/board/research/weighted_congestion_frontier/board/BOARD.md)按微信群聊使用：读到消息自行研究，回复随发现发送。[RUNBOOK.md](RUNBOOK.md)提供首次启动与日常命令，[CHECKPOINT.md](CHECKPOINT.md)说明阶段保存。论文者、提取者分别使用[完整写作入口](prompts/PAPER_WRITER.md)、[完整提取入口](prompts/EXTRACTOR.md)。

## Research Goal

研究 **WC-TARGET v1**：非负系数、次数至多 d 的多项式费用、任意正权、任意有限多资源策略的加权原子拥塞博弈，普遍近似纯均衡存在门槛 a_*(d) 是什么？优先争取全类 o(d) 上界，或严格改善文献无限非存在族的下界，最终确定增长阶或更精确的前沿。完整身份在 [MODEL.md](MODEL.md)、[CLAIMS.md](CLAIMS.md)，成功门槛在 [ACCEPTANCE.md](ACCEPTANCE.md)。

## Mathematical Objects / Definition Map

有限资源 E、玩家 N、正权 w_i、非空策略族 S_i⊆2^E、费用 c_e → 负载 x_e(s) → 玩家成本 C_i(s) → α-PNE → 全类 G_d → 普遍门槛 a_*(d)。成本是否再乘 w_i 不改变同一玩家的偏离不等式，证明与程序明确采用 MODEL 的约定。零成本通过不等式处理，阈值使用 inf。

## Claim Map / Dependency Graph

MODEL → 文献上界 WC-LIT-UPPER-D、下界 WC-LIT-LOWER、人数约束 WC-LIT-N → 开放目标 WC-TARGET v1。

文献上界来自近似势函数；文献下界来自全状态非存在族。固定玩家实例受 n-PNE 存在基线约束。设施选址、顺序客户吸引和本分支各保持其数学身份；定理迁移需要准确的桥梁证明。

## Known Results / Research Frontier

当前是已核对来源的文献基线：Ω(√d/log d)≤a_*(d)≤d（大 d）。精细有限 d 界与后续文献在宣称改进前重新核对。WC-TARGET v1 仍 OPEN。R1 本轮恢复并严格复算了奇数环的全状态系数证书：十次多项式实例无 2-PNE，见 [冻结入口](assets/R1/odd_cycle/README.md)、[独立攻击](assets/R1/odd_cycle/independent_attack.md)。新的无限增长参数仍在独立审查中，不把有限实例当成一般增长证明。另 [无环阶跃依赖图](assets/R1/tree_completion/proof.md) 已有完整一般证明与独立重构；它属于辅助 step 模型。

真正缺口是控制全体有限博弈的偏离结构，或构造玩家数可增长、每个纯状态均有大倍率获利偏离的族。现有路线是搜索种子；不同表示和跨领域机制都可开展。活跃讨论、问题和发现从公屏读取。

## Refuted / Failed / Open Problems / Next Actions

[FAILED_ROUTES.md](FAILED_ROUTES.md)登记真实数学失败、否定范围与回收结果。下一阶段从一手文献与公屏提出高信息价值的精确义务，以低成本边界检验区分机制，再追一般证明。关键候选经历独立重构和反例攻击，形成真实增量即保存并公开。

活跃新接口：奇数环 hub/cohort 的奇偶覆盖和闭环系数乘积；无环阶跃图的有向路径计数精确门槛。它们与此前对称星形、平台平滑及势夹逼障碍的冻结消息分别保留作用域。

## File Map

路径相对仓库根。

| 完整路径 | 内容、资产及读取时机 |
| --- | --- |
| research/weighted_congestion_frontier/assets/R1/odd_cycle/README.md | 奇数 hub/cohort 环的真实资源模型、每状态覆盖和正系数乘积可行接口；复用新下界机制前读 |
| research/weighted_congestion_frontier/assets/R1/odd_cycle/independent_attack.md | 从实际负载独立重构，并对十次费用实例的全部计数状态精确攻击；核对漏项与范围时读 |
| research/weighted_congestion_frontier/assets/R1/tree_completion/proof.md | 任意 simple DAG 的阶跃辅助模型、路径多项式精确门槛、边界与匹配有理幅度；不导出多项式结论 |
| research/weighted_congestion_frontier/MODEL.md | WC-TARGET 的对象、定义、全部量词、零成本与阈值；提出新 claim 前读 |
| research/weighted_congestion_frontier/CLAIMS.md | 文献事实、开放目标的精确身份与 objection；新版本或证据变化时更新 |
| research/weighted_congestion_frontier/RESEARCH_STATE.md | 当前前沿、主要 barrier 和下一动作；实质进展时更新 |
| research/weighted_congestion_frontier/LITERATURE.md | 一手数学来源、准确位置、协作参考；引用或判断新颖性前读 |
| research/weighted_congestion_frontier/PRIOR_ASSETS.md | 前人机制和可复用接口、尚未重建步骤；按当前义务读取 |
| research/weighted_congestion_frontier/FAILED_ROUTES.md | 精确失败步骤、否定范围、回收结果和重试条件；选路线前读 |
| research/weighted_congestion_frontier/PROTOCOL.md | 统一角色号、异步公屏、研究分支和成果交流 |
| research/weighted_congestion_frontier/RUNBOOK.md | 本地程序加 txt 凭据的恢复、同步、发言和保存命令 |
| research/weighted_congestion_frontier/CHECKPOINT.md | 阶段资产的提交、推送、远端确认及 descriptor 分享 |
| research/weighted_congestion_frontier/ACCEPTANCE.md | 主目标突破、解决、阶段资产、写作和提取的实际门槛 |
| research/weighted_congestion_frontier/prompts/TEAM.md | 新研究对话的完整入口；指定角色号与本地路径后使用 |
| research/weighted_congestion_frontier/prompts/PEER.md | 子 agent 的自主探索与独立攻击要求 |
| research/weighted_congestion_frontier/prompts/MODELS.md | 实际模型配置与干净上下文审查 |
| research/weighted_congestion_frontier/prompts/PAPER_WRITER.md | 贡献表达、完整证明、写作清洗与逐页成稿验收 |
| research/weighted_congestion_frontier/prompts/EXTRACTOR.md | 失败回收、一般化、具体复用与独立工具提取 |
| research/weighted_congestion_frontier/toolbox/README.md | 独立工具的精确身份、来源和复用入口；有真实工具时更新 |
| research/weighted_congestion_frontier/SOURCES.md | 固定上游原文、许可与本项目适配；使用归档材料时读 |
| research/weighted_congestion_frontier/upstream/manifest.json | 原文件仓库、固定 commit、原路径和 SHA-256 |
| research/weighted_congestion_frontier/tools/work.py | 自包含本地统一程序；空目录恢复与日常 read/send/sync/checkpoint |
| research/weighted_congestion_frontier/tools/work.sh | 仓库内统一入口，与外部 work.py 使用相同参数 |
| research/weighted_congestion_frontier/tools/board.py | schema 3 异步消息流、冻结资产核对及公屏迁移 |
| research/weighted_congestion_frontier/tools/checkpoint.py | 范围保存、普通推送、远端确认与单文件 descriptor |
| research/weighted_congestion_frontier/tests/ | 实际 Git 的工具、恢复、并发、公屏和保存测试；工具改动时运行对应测试 |
| research/weighted_congestion_frontier/evidence/validation.md | 本轮实际本地与 GitHub 验证结果 |
| research/weighted_congestion_frontier/board/README.md | 公屏的直接阅读入口与简短命令 |

有真实成果时建立 assets/<actor>/<idea>/、toolbox/<actor>/<tool-id>/ 或 papers/<actor>/<paper-id>/。工作分支为 wcg/work/<actor>/<session>；成果消息引用 checkpoint 返回的已推送文件 descriptor。规范审查后的成果整合到 main，后续对话可以从地图和冻结文件准确接续。
