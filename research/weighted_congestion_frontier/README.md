# 加权拥塞博弈：平等解题天团

所有对话使用同一份 [TEAM 启动提示词](prompts/TEAM.md)。每支天团都以解决整个问题为目标；没有固定文献队、上界队、下界队或协调队。主对话也研究数学，只因它掌握本会话工具而负责启动本队子 agent、对外交流和保存成果。其他队无需获得它的任务分配或批准。

## Research Goal

研究 **WC-TARGET v1**：非负系数、次数至多 d 的多项式费用、任意正权、任意有限多资源策略的加权原子拥塞博弈，普遍近似纯均衡存在门槛 a_*(d) 是什么？优先争取全类 o(d) 上界，或严格改善文献无限非存在族的下界。完整身份在 [MODEL.md](MODEL.md) 和 [CLAIMS.md](CLAIMS.md)；阶段交付与解题完成的区别在 [ACCEPTANCE.md](ACCEPTANCE.md)。

## Mathematical Objects / Definition Map

有限资源 E、玩家 N、正权 w_i、非空策略族 S_i⊆2^E、费用 c_e → 负载 x_e(s) → 玩家成本 C_i(s) → α-PNE → 全类 G_d → 普遍门槛 a_*(d)。成本是否再乘 w_i 不改变同一玩家的偏离不等式，但所有证明和程序须明确约定。零成本用不等式处理。定义全文见 MODEL。

## Claim Map / Dependency Graph

MODEL → 文献上界 WC-LIT-UPPER-D、下界 WC-LIT-LOWER、人数约束 WC-LIT-N → 开放目标 WC-TARGET v1。

文献上界来自近似势函数；文献下界来自全状态非存在族。二者没有证明“势函数不可能突破”。固定玩家实例不能给随 d 无界的普遍下界。设施选址、顺序客户吸引和本分支对象不同，旧仓库定理没有自动迁移边。

## Research Frontier / Known Results / Open Problems

当前只有核实过来源的文献基线，没有本团队新证明。粗粒度基线是 Ω(√d/log d)≤a_*(d)≤d（大 d）；它不是每个有限 d 的最强已知界。宣布改进之前须重新检索并核对精细上界与后续结果。

真正缺口是：如何控制全体有限博弈的偏离结构，或构造玩家数可增长、每个纯状态均有大倍率获利偏离的族。路线由各队提出，文件中的种子不是方法白名单。当前任务和占用状态从 [GitHub 公屏](https://github.com/SOMEBODYJUN/co-work-anl/tree/wcg/board/research/weighted_congestion_frontier/board)读取，不由协调者分派。

## Refuted / Failed / Next Actions

[FAILED_ROUTES.md](FAILED_ROUTES.md)目前记录应避免的协作失败机制，没有虚构数学失败。各队启动后自主提出有判别力的具体 idea，读取已有认领，选择一个尚未占用的推进单元，立即研究并分享。相同单元已有 owner 时，改攻新的义务或公开提出补充、反驳、联合工作、冻结版本独立审查。

## File Map

所有路径均相对仓库根。

| 完整路径 | 内容、数学资产及读取时机 |
| --- | --- |
| research/weighted_congestion_frontier/MODEL.md | WC-TARGET 的对象、量词、零成本与阈值定义；每次提出新 claim 必读 |
| research/weighted_congestion_frontier/CLAIMS.md | 文献事实和开放目标的精确身份；登记新版本和 objection 时更新 |
| research/weighted_congestion_frontier/RESEARCH_STATE.md | 活跃目标、真实前沿与下一步；有实质进展才更新 |
| research/weighted_congestion_frontier/LITERATURE.md | 一手来源、准确位置及后续检索范围；引用或宣称新颖性前读取 |
| research/weighted_congestion_frontier/PRIOR_ASSETS.md | 前人机制与可复用接口，注明尚未重建的步骤；按当前 idea 选择性读取 |
| research/weighted_congestion_frontier/FAILED_ROUTES.md | 失败的确切步骤、否定范围与可回收结果；防止重复死路 |
| research/weighted_congestion_frontier/PROTOCOL.md | 平等交流、细粒度认领、租约与安全 Git 工作流；首次参与必读 |
| research/weighted_congestion_frontier/ACCEPTANCE.md | 数学成功、阶段资产、预算交接和协作验收；决定结束或升级状态时读 |
| research/weighted_congestion_frontier/prompts/TEAM.md | 所有主对话相同的完整入口；复制到任意多个新对话 |
| research/weighted_congestion_frontier/prompts/PEER.md | 全体子 agent 共用的自主解题要求；每个子 agent 都保留提 idea 的权利 |
| research/weighted_congestion_frontier/prompts/MODELS.md | 用户指定模型与真实配置记录；启动时核对可用能力 |
| research/weighted_congestion_frontier/tools/board.py | Git 公屏工具；view、idea、claim、续约、结果和讨论，冲突后重新检查 |
| research/weighted_congestion_frontier/tools/live_smoke.py | 显式 --live 部署验收；两并发发布端、公屏回复和冻结资产校验，事件明确标非数学 |
| research/weighted_congestion_frontier/tests/test_board.py | 临时 bare Git 远端的并发、失联、过期和资产校验；修改工具后运行 |
| research/weighted_congestion_frontier/evidence/validation.md | 本轮实际验证范围与限制；不承担数学证明 |
| research/weighted_congestion_frontier/evidence/github_smoke.json | 实际 GitHub 收发的事件ID、唯一赢家、冻结资产 hash；验证部署时读取 |
| research/weighted_congestion_frontier/board/README.md | 公屏分支入口和命令；实时事件仅在 wcg/board 分支 |

未来有真实成果才建立 assets/<team>/<idea>/，包括精确 claim、推导、障碍或可复现实验。各队用专属 wcg/work/<team>/<session> 分支保存；附带研究资产的结果、冻结或交接消息须引用已推送的 commit 与文件 SHA-256，普通讨论与认领无需资产。经独立审查的冻结成果可由任何成员整合到 main，整合不是路线批准权。
