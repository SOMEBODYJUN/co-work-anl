# 加权拥塞博弈：共同研究入口

每个 Work 对话复制 [TEAM.md](prompts/TEAM.md)，写好自己的角色号，使用本地 `work.py` 与当前会话的 `githubtoken.txt` 直接恢复、同步、交流和保存。一个对话以同一角色号发言与提交，内部按需要使用 subagent。所有研究对话共同解决 WC-TARGET v1，自主探索、多路线并行、同题独立研究。

[公屏](https://github.com/SOMEBODYJUN/co-work-anl/blob/wcg/board/research/weighted_congestion_frontier/board/BOARD.md)按微信群聊使用：读到消息自行研究，回复随发现发送。[RUNBOOK.md](RUNBOOK.md)提供首次启动与日常命令，[CHECKPOINT.md](CHECKPOINT.md)说明阶段保存。论文者、提取者分别使用[完整写作入口](prompts/PAPER_WRITER.md)、[完整提取入口](prompts/EXTRACTOR.md)。

## Research Goal

研究 **WC-TARGET v1**：非负系数、次数至多 d 的多项式费用、任意正权、任意有限多资源策略的加权原子拥塞博弈，普遍近似纯均衡存在门槛 a_*(d) 是什么？优先争取全类 o(d) 上界，或严格改善文献无限非存在族的下界，最终确定增长阶或更精确的前沿。完整身份在 [MODEL.md](MODEL.md)、[CLAIMS.md](CLAIMS.md)，成功门槛在 [ACCEPTANCE.md](ACCEPTANCE.md)。

## Mathematical Objects / Definition Map

有限资源 E、玩家 N、正权 w_i、非空策略族 S_i⊆2^E、费用 c_e → 负载 x_e(s) → 玩家成本 C_i(s) → α-PNE → 全类 G_d → 普遍门槛 a_*(d)。成本是否再乘 w_i 不改变同一玩家的偏离不等式，证明与程序明确采用 MODEL 的约定。零成本通过不等式处理，阈值使用 inf。

## Claim Map / Dependency Graph

MODEL → 源两attack式(3) → R3-SOURCE-SHARP-ASYMPTOTIC-v1；MODEL + 源式(3) → WC-R3-FULL-TOPOLOGY-REDUCTION v3 → 对称拓扑大d锐包络（不是全类上界）。

MODEL → 文献上界 WC-LIT-UPPER-D、下界 WC-LIT-LOWER、人数约束 WC-LIT-N → 开放目标 WC-TARGET v1。

文献上界来自近似势函数；文献下界来自全状态非存在族。固定玩家实例受 n-PNE 存在基线约束。设施选址、顺序客户吸引和本分支各保持其数学身份；定理迁移需要准确的桥梁证明。

## Known Results / Research Frontier

当前是已核对来源的文献基线：Ω(√d/log d)≤a_*(d)≤d（大 d）。精细有限 d 界与后续文献在宣称改进前重新核对。R3已给出[源包络锐渐近及完整对称拓扑还原](../current/weighted_congestion_frontier.md)，均经内部独立攻击；WC-TARGET v1 仍 OPEN。源式精确sup细化为(2/√e)√(d ln ln d)/ln d，全类上界仍为d。

真正缺口是控制全体有限博弈的偏离结构，或构造玩家数可增长、每个纯状态均有大倍率获利偏离、严格超出已知源式精确包络的族。对称同轻权两列拓扑允许任意非负多项式与全状态攻击，仍受同一包络约束。现有路线是搜索种子；不同表示和跨领域机制都可开展。活跃讨论、问题和发现从公屏读取。

## Refuted / Failed / Open Problems / Next Actions

[FAILED_ROUTES.md](FAILED_ROUTES.md)登记真实数学失败、否定范围与回收结果。下一阶段从一手文献与公屏提出高信息价值的精确义务，以低成本边界检验区分机制，再追一般证明。关键候选经历独立重构和反例攻击，形成真实增量即保存并公开。

## File Map

路径相对仓库根。

| 完整路径 | 内容、资产及读取时机 |
| --- | --- |
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

## R3 current frozen research packages

- `research/weighted_congestion_frontier/assets/R3/sharp_source_review/`：源式全部参数的锐渐近、明确floor/ceil attaining family、独立全状态与global upper攻击、Decimal诊断；判断调参极限或引用强化尺度时读。
- `research/weighted_congestion_frontier/assets/R3/full_topology/`：稳定整数区间、两种右支不等式、单轻玩家反演、poly→monomial消元及精确literal回归；尝试同权对称拓扑前读。
- `research/weighted_congestion_frontier/assets/R3/topology_attack/`：先独立重构后的版本1–3审查及另写literal oracle；状态升级或修改范围时读。
- `research/current/weighted_congestion_frontier.md`：上述命题的根图谱入口与当前前沿；完整proof仍在各package。

## 非对称交叉拓扑的有限次数分离

[degree32交叉资产](assets/R3/crossover_audit/separation.md)给 T32≤89/50<9/5<B(G)，完整对称类允许任意非负主/副多项式及所有正同轻权。源包络上界由[全实参数证书](assets/R3/source32_bound/PROOF.md)证明，交叉游戏全部状态及偏离有两份独立精确核验。固定系数升次数在d40失败；该路线的极限值也低于9/5。有限分离不解决WC-TARGET增长阶。

路径 `research/weighted_congestion_frontier/assets/R3/source32_bound/` 保存消元证明、整数Bernstein检查器和完整区间证书；以后比较d32下界时读。`research/weighted_congestion_frontier/assets/R3/crossover_audit/` 保存逐资源策略、全状态成本、独立重构和固定参数失效；构造增长族前读，避免只提高次数。
