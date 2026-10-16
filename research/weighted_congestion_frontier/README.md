# 加权拥塞共同研究入口

本次`Cd/ln d`全类存在命题已有[完整严格否定证明](../current/weighted_congestion/linear_degree_allstate_lower_bound.md)：每整数d≥2^20有全部状态严格(d/10)改善的有限正有理两动作游戏。精确新身份、全部量词与审查在[CLAIMS](CLAIMS.md)，数学从[专题地图](../current/weighted_congestion/README.md)进入。外部评审/新颖性未认证；WC-TARGET v1长期精确门槛身份不改写。

新对话先读根四入口、[MODEL](MODEL.md)、[ACCEPTANCE](ACCEPTANCE.md)、现行数学地图与两份独立审查，再按实际义务读取。当前最重要的后续是核查/简化新证明、常数、有限d与外审，不能仍把全类o(d)存在性列为未解。

## 角色与 Pro 交接顺序

解题前的冻结接题整理见[交接简报 PRO_BRIEF](PRO_BRIEF.md)，其[来源与状态映射](PRO_BRIEF_SOURCES.json)列出所选正文、Claim 与审查。用[冻结导出器](tools/export_pro_packet.py)从已推送的同一 commit 生成仓库外精简包；默认只读任务与简报，`optional/` 是按需原数学正文。[独立审读记录](../reviews/weighted_congestion/pro_brief_scope_review.md)核查自足性与范围，不将整理工作升级为全类数学结论。

| 入口 | 实际任务与交付 |
| --- | --- |
| [清晰者 CLEANER](prompts/CLEANER.md) | 从精确正文与审查筛出 Pro 必须知道的模型、已知事实和障碍；逐项保留否定范围，维护一份自足 PRO_BRIEF，最终从同一已推送版本导出精简包 |
| [提取者 EXTRACTOR](prompts/EXTRACTOR.md) | 重建可复用工具的输入、输出、条件和证明；与清晰者核实按需接口，独立有价值但不助接题的资产仍留仓库 |
| [Pro 攻题 PRO_ATTACK](prompts/PRO_ATTACK.md) | 收到实际整理材料后，自主解决原全类问题；不把 Git 操作、历史审计或写论文作为前置 |
| [论文者 PAPER_WRITER](prompts/PAPER_WRITER.md) | 组织真实成果的贡献、机制、完整证明及实际成稿；不与交给 Pro 的材料筛选混为一个角色 |
| [共同研究 TEAM](prompts/TEAM.md) | 持续攻击唯一题目并维护可复用资产；可以同题独立推导或探索多条路线 |
| [共同操作 OPERATIONS](prompts/OPERATIONS.md) | 各 Work 角色共用的恢复、唯一发布身份、命名地图、阶段核验和完整推送合同；只需共用一份 work.py |

本次准备顺序：清晰者与提取者可并行阅读和核对，清晰者整合及审读后再把精简包和 Pro 任务交出。论文成稿可另行进行，不是 Pro 攻题的先决条件。各角色首次生成不同前缀的随机唯一后缀并显式传入 `start --actor`；同 clone 接续复用，不照抄固定 W1/E1，也不为子 agent 登记。

解题前冻结的派生数学交接正文为 [PRO_BRIEF.md](PRO_BRIEF.md)：自足模型与完成量词、可靠边界、按机制合并的严格障碍及可直接调用的签名/规范形附录；逐节绑定数学源快照和实际审查层级。它是派生读取稿，不另立真值账本。[本次独立盲读与冻结来源核查](../reviews/weighted_congestion/pro_brief_scope_review.md)记录实际修订和覆盖。当前交接须补入新全状态否定证明及审查；旧OPEN判断不代表现行状态。冻结包及其原来源不原位改写，交付状态以实际独立审读和远端推送回执为准。

角色提示词就绪不表示交接材料已整理。`PRO_BRIEF.md` 仅在清晰者实际完成筛选后创建或修订；交付包仅带完整任务、必要数学正文及追溯 manifest，工具数学附录按需。历史聊天、测试日志、全仓文件和未证 idea 清单不作为默认 Pro 输入。方法障碍、断言反例、开放义务和有限观察分开，不将“没做出来”写成“不可能”。整理与提取完成也不表示主问题解决。

## 当前数学地图

健康循环窗口参数→全部类前沿真实端点出口→同类010/101时钟修复非法态→原次数预算→唯一题目严格否定。新下界与单列文献d上界合用给a_*(d)=Θ(d)，不称精确常数。旧奇环T_d及一般cohort实际阈值、结构存在工具、完整selector接口和方法障碍各自保留，具体合同见[数学地图](../current/weighted_congestion/README.md)。

正文第10节接独立重构/攻击、实际输入、版本hash和冻结结果；[既有审查的补充复核](../reviews/weighted_congestion/ordinal_potentials/linear_degree_allstate_review.md#补充复核整数次数预算与完整多类拼装)另接免对数的次数证明与完整多类拼装审计。有限精确计算不是一般证明。候选继续在questions，审查在reviews，数学状态分别登记在review_status/assets/graph；[FILES](FILES.md)和[CATALOG](../CATALOG.md)用于导航。[INTEGRATION](INTEGRATION.json)只用于原件追溯；原始来源不为新证明改写。

## 共同工作

每个 Work 对话使用独立 clone 和一个稳定发布标识；程序可自动生成，无需登记子 agent。各 boss 自主组织团队，同题和多路线都允许，无认领和固定时长。有启发的半成形 idea、卡点、反例和合作问题可随时发到[公屏](https://github.com/SOMEBODYJUN/co-work-anl/blob/wcg/board/research/weighted_congestion_frontier/board/BOARD.md)，注明不确定性；聊天不要求先成稿或审查。普通排错与逐轮日志无需强制汇报。

可复用阶段成果按原 [GROWTH](../GROWTH.md) 入库后立即 checkpoint 到 main，远端确认后再分享入口。main 同时保存候选与已审成果，证据等级不会因推送改变。研究和提交统一 main，不创建研究分支；具体题目、完成标准和命令可直接复制 [TEAM](prompts/TEAM.md)，详细施工和读取规则见[全仓规则](../REPOSITORY_GUIDE.md)。

每次阶段提交把正文、精确登记、中文命名及相关地图一起维护：在 `research/catalog.json` 写具体名称和读取用途，生成 CATALOG、FILES 及受影响的关系图，再运行对应检查。根地图每次审阅，目标、结果、依赖、状态、前沿或导航变化时更新；本题新资产必须从数学地图和资产目录可达。`checkpoint` 负责 Git 保存与远端确认，不代替内容核对或结构检查；默认范围外的入口更新须显式列入完整提交清单。启动提示词同时提供未上传可选 `work.py` 时的恢复办法。
