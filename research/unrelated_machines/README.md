# 不相关并行机：新主攻存档与协作入口

固定研究存档：`unrelated-machines`。主目标 `UM-TARGET-v1` 是一般R∥C_max确定性位多项式统一(2−ε)构造，仍OPEN。新对话直接使用 [BOSS_START.md](BOSS_START.md)，附仓库外的githubtoken.txt；无需人工分配内部subagents编号。

当前新增可复用边界：[长链高围长反例与固定机器联合投影](../current/unrelated_machines/long_path_coalition_gap.md)。它排除只共享单机配置分布的固定大小联合见证舍入合同；完整多机交叠一致性不被排除。经典核心与标准耦合的应用分开标记，新颖性未认证，未给一般新算法。

## 先读什么

根四入口及AGENTS → [数学地图](../current/unrelated_machines/README.md) → [精确身份](CLAIMS.md) → [当前前沿](RESEARCH_STATE.md) → [基线与障碍](../current/unrelated_machines/model_and_classical_barriers.md) → [独立审查](../reviews/unrelated_machines/classical_foundation_review.md)。按当前义务查[文献](LITERATURE.md)和[真实失败范围](FAILED_ROUTES.md)，不要求通读旧题或所有历史。

本轮已有原文语料、定理与版本定位、完整槽舍入重构、配置gap重构及精确程序。2005全文未落地，困难性/2005完整舍入/受限指派局部搜索等尚未全部独立重构；不把首批地基说成“前人所有证明已内化”。后续可边核实承重工具边开展原创研究。

## 怎样协作和保存

复用仓库唯一程序 `research/weighted_congestion_frontier/tools/work.py`；路径历史上带旧题名称，不表示新题使用旧数学模型。新clone首次启动必须显式 `start --save unrelated-machines`。程序将本clone固定到此save；其他存档使用独立clone，不能覆盖本地绑定。

每对话一个boss稳定身份、一个独立clone，全部研究成果进main；subagents由boss汇集，不自行当作独立Work通道。本人桌面在 `research/workspaces/unrelated-machines/<actor>/`，其已推送版本可供同行访问。公屏、提及、私聊和收件箱均按本save路由；同仓私聊是视图隔离，没有双方专属读取权限。

日常完整命令及能力边界见 [RUNBOOK.md](RUNBOOK.md)。默认checkpoint范围按新save选本题八类目录、本题原文目录、共同账本和本人桌面，不包含旧题数学或他人桌面。维护共享程序/范围外导航时显式列全paths；所有待推历史都会审计，不能用只选本轮文件夹带旧提交。未知save默认也不会静默选旧题。

独立Work对话和界面Project仍由用户手动开启；存档、提示词和subagent不等于已经创建新的独立对话。发信不保证收件方正在运行或被唤醒。无排他认领、不限固定人数或轮数；实际规模能力以测量为准。

## 长期资产位置

| 位置 | 内容和读取用途 |
| --- | --- |
| research/current/unrelated_machines/ | 精确模型和自足已知证明重构；新定理按Claim分级，目录不赋予真值 |
| research/unrelated_machines/ | 目标账本、前沿、文献、障碍、启动提示词与操作手册 |
| research/questions/unrelated_machines/ | 尚未闭合的proof obligations和候选；主目标完成前都保留准确状态 |
| research/reviews/unrelated_machines/ | 先重构后攻击的实际审查与冻结hash |
| history/source/literature/unrelated_machines/ | 原始取得版本PDF/PS；hash、页数和解释在manifest与来源对应表 |
| tests/audits/unrelated_machines/ | 可复用精确舍入、构造、枚举与独立攻击程序 |
| examples/unrelated_machines/、evidence/certificates/unrelated_machines/、evidence/runs/unrelated_machines/ | 实际输入、证书、冻结证据分别保存；程序默认stdout，不覆盖冻结记录 |

新Claim同步登记全仓claims、review_status、assets与graph；文件具体名称/用途登记catalog。根README与研究目录持续作为地图。只有真实数学/工程增量入库，不保存逐轮聊天和重复摘要。

## 新增的匹配残余路线与准确边界

[大边匹配残余、简单支撑与共享逃逸容量](../current/unrelated_machines/heavy_matching_residual_and_escape.md)给出三个新限范围身份：`UM-HEAVY-MATCH-FILTER-v1`安全位多项式过滤、`UM-SIMPLE-SUPPORT-GAP-v1`简单支撑配置gap、`UM-ESCAPE-MATCH-GAP-v1`共享小端容量方法反例。主目标仍OPEN；不是统一低于2算法，未认证全球新颖性。读取顺序：精确账本→正文§1–5→冻结审查→两路代码/证据。真实依赖为模型/经典两树→路径终端配置与整数计数→逃逸族；匹配安全性单独依赖逐次删边与任务权增广。有限核验仅为checks。

| 新长期文件 | 内容、作用及读取条件 |
| --- | --- |
| research/current/unrelated_machines/heavy_matching_residual_and_escape.md | 全量词安全过滤、总位复杂度、三层瓶颈/反例；设计匹配或跨机器容量候选时读 |
| research/reviews/unrelated_machines/heavy_matching_escape_review.md | 独立先重构后冻结攻击，实际hash、边界及未解决义务；引用新Claim前读 |
| tests/audits/unrelated_machines/heavy_matching_residual.py | 任务权匹配、过滤固定点、显式路径/逃逸配置及小矩阵枚举 |
| tests/audits/unrelated_machines/ghmr_independent.py | 不同实现的matching oracle、独立证书与压缩容量DP；交叉核对而非一般证明 |
| evidence/runs/unrelated_machines/heavy_matching_residual_audit.json、heavy_matching_escape_independent.json | 两路实际参数、代码hash与有限结果；重跑写scratch，不覆盖 |

新增可复用接口从[计数传播与细分失败](../current/unrelated_machines/bundle_coupling_subdivision_barrier.md)读取：精确身份、一般证明、实际审查和代码证据已串联；未形成统一优于2的算法。
