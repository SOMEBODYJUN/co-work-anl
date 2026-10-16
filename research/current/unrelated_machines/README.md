# 不相关并行机：突破统一常数2壁垒的研究地图

本轮新主攻是 `UM-TARGET-v1`：一般二进制有理输入R∥C_max上，构造确定性位多项式时间、统一常数(2−ε)近似。目标仍OPEN；未形成新算法。旧拥塞/设施研究保留原身份，不作为本题数学依赖。

新阶段边界见[长链替换与固定机器联合投影](long_path_coalition_gap.md)：经典gap可移到任意大围长的简单机器图；只共享单机边际的固定大小联合见证仍有sup gap2。完整多机交叠相容性不在该否定范围，且三机完整相容性已能解决这批树宽2反例。完整证明、独立攻击和有限核验分别登记，未声称原创算法或全球新颖性。

先读[协作入口](../../unrelated_machines/README.md)与[精确账本](../../unrelated_machines/CLAIMS.md)，再读[模型、舍入与配置间隙的自足重构](model_and_classical_barriers.md)。[文献清单](../../unrelated_machines/literature_manifest.json)区分已取得原文、已核结果和待处理来源。[当前前沿](../../unrelated_machines/RESEARCH_STATE.md)说明下一步需要完成什么。

| 定义/Claim | 内容与真实状态 | 依赖和作用 |
| --- | --- | --- |
| UM-MODEL-v1 | 非负有理、不可用边、不可拆分、全部任务必须安排 | 目标、LP与所有算法共同合同；含零最优值 |
| UM-TARGET-v1 | ∃统一ε>0，∃确定性位多项式算法，∀输入输出≤(2−ε)OPT | 开放研究目标；m不能固定，不能用估值代替调度 |
| UM-ST-ROUND-v1 | 给定剪枝LP可行x，槽匹配输出L_i≤fractional load+support max≤2T | 已知结果自足重构；Hall与非增排序；程序仅实现此舍入接口 |
| UM-CONF-GAP-v1 | 配置LP的sup gap=2，甚至每任务两台可选机器 | 两树构造、递推配置证书＋整数下界＋舍入上界；阻止纯粹相对配置值的统一改进 |
| UM-LONG-PATH-GAP-v1 | 任意给定围长下，简单机器图配置gap仍sup2 | 经典两树＋长链阈值保真；[正文](long_path_coalition_gap.md)、[独立审查](../../reviews/unrelated_machines/long_path_coalition_review.md) |
| UM-COALITION-PROJECTION-GAP-v1 | 任意固定r的单机边际相容联合投影仍sup gap2 | 高围长族＋森林耦合；不含全交叠一致性；完整三机相容性在本族精确 |

真实依赖是模型→LP定义→配置边际投影→经典舍入上界；模型→两树族→整数下界与配置可行性→gap下界→与上界合成gap=2。gap只限制一个下界/舍入合同，不推出主目标为假。有限核验只检查所列参数。

研究路线是种子：可以探索跨机器兼容性、更强松弛、组合下界、局部搜索/交换结构、新表示及复杂度归约。每条路线先写精确义务与它如何绕过已知gap；不要求服从固定方法清单，也不要求先完成全领域综述才能检验一个有信息价值的想法。

| 文件 | 数学资产及何时读取/修改 |
| --- | --- |
| research/current/unrelated_machines/model_and_classical_barriers.md | 精确模型、全量词目标、零值边界、槽舍入完整证明、重索引gap构造与障碍准确范围；引入新工具或算法前核对合同 |
| research/unrelated_machines/CLAIMS.md | 逐命题身份与认知层；改假设或结论须新版本 |
| research/unrelated_machines/LITERATURE.md、literature_manifest.json | 文献结果、版本、取得状态、定理位置与PDF哈希；使用外部定理时查原文 |
| research/unrelated_machines/RESEARCH_STATE.md、FAILED_ROUTES.md | 当前未闭合义务和已知障碍；新候选出现时更新，不记录普通流水账 |
| tests/audits/unrelated_machines/rounding_and_gap.py | Fraction舍入、枚举oracle、显式配置证书、特定树族DP；算法或构造变更时运行 |
| evidence/runs/unrelated_machines/classical_baseline_audit.json | 初始有限核验冻结记录；重跑输出到scratch，不覆盖原记录 |
| research/questions/unrelated_machines/barrier_escape_obligations.md | 新算法必须跨过的下界/构造/复杂度义务；具体路线产生后细化 |
| research/unrelated_machines/BOSS_START.md | 可复制到新对话的完整启动提示词；恢复、存档路由、研究与保存要求 |
| research/current/unrelated_machines/long_path_coalition_gap.md | 高围长gap运输、CC_r精确定义及全交叠相容性逃生口；提出局部强化前先核对范围，沿正文进入双路代码/输入/证书/冻结证据 |

## 新增的匹配残余路线与准确边界

[大边匹配残余、简单支撑与共享逃逸容量](heavy_matching_residual_and_escape.md)给出三个新限范围身份：`UM-HEAVY-MATCH-FILTER-v1`安全位多项式过滤、`UM-SIMPLE-SUPPORT-GAP-v1`简单支撑配置gap、`UM-ESCAPE-MATCH-GAP-v1`共享小端容量方法反例。主目标仍OPEN；不是统一低于2算法，未认证全球新颖性。读取顺序：精确账本→正文§1–5→冻结审查→两路代码/证据。真实依赖为模型/经典两树→路径终端配置与整数计数→逃逸族；匹配安全性单独依赖逐次删边与任务权增广。有限核验仅为checks。

| 新长期文件 | 内容、作用及读取条件 |
| --- | --- |
| research/current/unrelated_machines/heavy_matching_residual_and_escape.md | 全量词安全过滤、总位复杂度、三层瓶颈/反例；设计匹配或跨机器容量候选时读 |
| research/reviews/unrelated_machines/heavy_matching_escape_review.md | 独立先重构后冻结攻击，实际hash、边界及未解决义务；引用新Claim前读 |
| tests/audits/unrelated_machines/heavy_matching_residual.py | 任务权匹配、过滤固定点、显式路径/逃逸配置及小矩阵枚举 |
| tests/audits/unrelated_machines/ghmr_independent.py | 不同实现的matching oracle、独立证书与压缩容量DP；交叉核对而非一般证明 |
| evidence/runs/unrelated_machines/heavy_matching_residual_audit.json、heavy_matching_escape_independent.json | 两路实际参数、代码hash与有限结果；重跑写scratch，不覆盖 |

## 计数传播与跨机器相容性接口

[成束任务的二阶相容性、计数传播与细分障碍](bundle_coupling_subdivision_barrier.md)给UM-BUNDLE-MOMENT-v1、UM-CARDINALITY-CLOSURE-v1、UM-PAIR-SUBDIVISION-GAP-v1。原VW族可被二阶相容性或健全计数传播识别；细分保持整数OPT、提升分数证书，令简单图上的完整pair coupling仍sup gap2。新目标不是反复切旧族，而是跨中间容量机器的信息保持与可构造性。

读取链：本题账本→正文→[冻结审查](../../reviews/unrelated_machines/bundle_subdivision_review.md)→规范计数/耦合及不导入核心的独立审计→[完整冻结记录](../../../evidence/runs/unrelated_machines/bundle_subdivision_audit.json)。主目标继续OPEN，新颖性/外审未认证；同存档boss4的长链推广是独立重叠发现，不再把长度2变换当独占新家族。
