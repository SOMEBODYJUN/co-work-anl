# 共同研究：顺序客户吸引的一般半覆盖

成果现已统一到[一般证明工作稿](research/current/customer_attraction/general_half_proof.md)、[全成果总账](research/customer_attraction/RESULTS_LEDGER.md)和[全部个人区恢复索引](research/customer_attraction/WORKSPACE_RESULTS.md)。工作稿逐项标明已证关系和未证步骤，不能据其文件名认定一般证明完成。

当前唯一主攻 **Q-CAG-HALF**，存档 **customer-attraction**：一般共同目录、任意人数、每个完整历史依赖纯子博弈精炼均衡的福利是否至少达到最优的一半。主目标仍 **OPEN**。新对话从本文和[本题短地图](research/customer_attraction/README.md)恢复；不相关机、拥塞和两阶段设施是分别保留的研究线。

## 研究目标与数学对象

有限单位客户集 N，有限非空共同主题目录 S⊆2^N，m≥1名单位权提供者依次观察全部有序历史并选择一个主题。终局 a=(S₁,…,Sₘ) 中，客户 x 的覆盖者数为 cₓ(a)，提供者 i 的收益为 uᵢ(a)=Σₓ∈Sᵢ 1/cₓ(a)，福利 W(a)=|∪ᵢSᵢ|=Σᵢuᵢ(a)。OPTₘ 是 m 个目录主题的最大并集大小。

**精确目标：对每个上述实例、每个 m、每个在全部有序历史最优的纯 SPE σ，证明 2W(a(σ))≥OPTₘ。** 允许重复主题、空主题、零客户和任意历史依赖平局。零福利用乘法不等式，不定义0/0。客户不再作第二阶段负载优化。完整定义和原文范围见[模型](research/current/customer_attraction/model.md)及[文献边界](research/current/customer_attraction/literature.md)。

## 定义、命题与依赖

模型 → 全历史 SPE 的真实偏离不等式 → 已证通用关系 → 待闭合的一般福利结论。小人数与结构定理是已保存地基，没有从它们自动推出一般结论的依赖边。安全值、策略锥、运输和分支支付只是可选择的表示或充分接口，不是方法白名单，也不是已解决的一般桥。

| 数学身份 | 当前认识 | 证明、限制与证据入口 |
| --- | --- | --- |
| Q-CAG-HALF | 任意目录与人数仍OPEN；没有完整证明或真正反例 | [精确目标](research/questions/customer_attraction_half_coverage.md)、[本题账本](research/customer_attraction/CLAIMS.md) |
| 三人、四人一般目录 | 三人锐5/3；四人1499/750<2；内部证明与审查 | [三人证明](research/current/customer_attraction/three_player_sharp.md)、[四人证明](research/current/customer_attraction/four_player_bound.md) |
| 五人一般目录 | 当前上界约2.061695>2，未达半覆盖 | [精确有理界](research/current/customer_attraction/five_player_indexed_bound.md)；模板最优点不是SPE反例 |
| 有限极大覆盖 / 层级结构 | 至多六极大任意人数已证；七极大仅有明确部分范围；另有向日葵与层级关联定理 | [按范围的完整结果表](research/current/customer_attraction/README.md) |
| 分数覆盖受控、无界目录 | 某个最优并集分数覆盖数至多7/2时全人数半覆盖；一般有真实前缀产品预算 | [完整递推与范围](research/current/customer_attraction/fractional_cover_path_budget.md)，无界覆盖数仍未闭合 |
| 极大关联数仅1/k−1/k、无界k与人数 | 全员θ保底及带共同核心锐2−1/m福利界；内部子主题任意 | [真实中继和平稳逐客户支付](research/current/customer_attraction/extreme_maximal_membership_floor.md)，独立内审；一般中间关联仍OPEN |
| 最优遗漏全局私有、无界目录 | 某个最优并集的实际遗漏全为极大全局私有客户时，任意人数锐2−1/m；已覆盖客户可任意共享 | [实际遗漏席位谱](research/current/customer_attraction/uncovered_private_seat_spectrum.md)，共享遗漏仍未闭合 |
| 实际路径的真实末两人菜单 | 倒二主题被全部早期主题包含，或至多r个遗漏且m≥(r+1)²+1时half；人数与目录均不固定 | [正面证明与范围](research/current/customer_attraction/penultimate_few_exceptions.md)，独立内审；一般路径仍OPEN |
| 静态福利比较桥 | 完整三人SPE福利可以低于同实例每个静态CCE的期望福利；更换静态比较对象也失败 | [十三客户CCE反例](research/current/customer_attraction/worst_cce_welfare_counterexample.md)、[八客户简化](research/current/customer_attraction/eight_customer_cce_welfare_gap.md)，均有独立内审 |
| 完整策略计算与证书 | 集合值逆向归纳、客户重数锥、有限精确核验 | [终局全集](research/current/customer_attraction/exact_solver.md)、[策略锥](research/current/customer_attraction/strategy_cone.md)；不构成一般证明 |
| 固定人数覆盖矩与纯负载边界 | 全部真实比较行span已有精确刻画及有理稀疏归约；实际无拥挤SPE仍可有OPT/W趋3/2 | [覆盖矩](research/current/customer_attraction/coverage_moment_geometry.md)、[全人数无拥挤族](research/current/customer_attraction/collision_free_three_halves_family.md)；不构成一般half上界 |

## 真正前沿与失败机制

早期偏离会改变全部后继行动。缺口是跨真实分支的全局福利控制；当前没有可直接归纳的一般支付机制。[研究前沿](research/customer_attraction/RESEARCH_STATE.md)固定剩余义务，[失败地图](research/customer_attraction/FAILED_ROUTES.md)解释逐人保底、逐步非负、根总税和冻结后继为何失败。新方法可以完全绕开这些接口。

主人最新决定：**所有人只研究一般人数、一般共同目录。** 停止特殊人数、固定极大主题数、结构类扩张和局部常数项目；已有成果保持原证明与条件，供一般论证引用。有限实例只检验明确的一般候选或核验真正目标反例，不能用有限阴性替代证明。方法开放到任何数学领域；算法、LP、枚举均为按需工具。做不出来不构成不可能性证据。

Boss自己承担一般推导，清洗者整理全部已有资产，整理者按数学机制整合论证；未完成候选可自由交流，不设开工审核或路线配额。协调者和方向审查者在公屏`owner-general-strategy-2026-10-21`按最新决定跟进，通知不等于对方已读或已转向。完整执行规范见[AGENTS](AGENTS.md)。

## 三个角色与一个程序

| 当前角色 | 工作 | 可直接复制的提示词 |
| --- | --- | --- |
| Boss | 自主带团队研究；自由选路、证明、反例、计算和交流，探索不设前置审核 | [BOSS_START](research/customer_attraction/BOSS_START.md) |
| 清洗者 | 检查对象、证明和证据，处理真实异议；整理自足资产并入库 | [CLEANER](research/customer_attraction/CLEANER.md) |
| 整理者 | 判断独立成稿、拆合与定位；准确突出新增机制、意义和优势 | [EDITOR](research/customer_attraction/EDITOR.md) |

统一程序是根目录 [work.py](work.py)，附件单文件也能恢复独立clone。身份自动使用R-UUID并复用本clone绑定；新会话默认customer-attraction，旧存档不会自动改绑。全部研究提交main，公屏、提及、私聊和个人桌面继续使用同一工具。命令见[RUNBOOK](research/customer_attraction/RUNBOOK.md)。

个人区用于持续备份；清洗后的共享资产按数学对象入库。正式入库的同一次提交更新本题数学README及实际受影响的状态与登记；本页只随主目标、最好已知范围或方向变化更新。README由入库者维护，程序检查漏链和漏登记，不自动编写数学结论。位置、命名和职责见[生产规则](research/REPOSITORY_GUIDE.md)。

## 研究文件地图

| 完整路径 | 内容、作用与读取时机 |
| --- | --- |
| research/customer_attraction/README.md | 当前主攻的短入口与最短阅读链；新boss首先进入 |
| research/customer_attraction/RETAINED_QUESTIONS.md | 保留问题的开放、已闭合、失效接口及暂停旧题，避免重复立项 |
| research/current/customer_attraction/README.md | 每份自足正文、范围、代码和证据的完整索引，按当前义务查阅 |
| research/current/claims.md、research/review_status.json | 全仓精确身份及证明/内审/外审/实现的权威账本，引用和状态提升时读取 |
| research/assets.json、research/graph.json、research/catalog.json | 命题文件合同、真实数学依赖、中文名称与用途；有实质变化时同步 |
| research/questions/customer_attraction_general_handoff.md | 未闭合的数学义务及已失败桥的范围；不再重复存放长角色提示词 |
| research/reviews/customer_attraction/、customer_attraction/、tests/ | 已发生的审查、规范实现及独立验证；以每条合同为准 |
| examples/customer_attraction/、evidence/ | 实际输入、完整策略证书及冻结运行；冻结记录不原位覆盖 |
| research/workspaces/customer-attraction/ | 每位研究者持续备份的个人桌面，含未核验与失败尝试；整理后进入按数学对象组织的共享资产 |

[研究总目录](research/README.md)、[中文资产目录](research/CATALOG.md)、[全仓资产](ASSETS.md)与[生产规则](research/REPOSITORY_GUIDE.md)补充导航。历史来源从[历史入口](history/README.md)进入；本次实际清理与原字节追踪见[整理记录](research/customer_attraction/CURATION.md)。

另行保留的加权拥塞方法研究已整理为[结构用于稳定决策与成本优化](research/current/weighted_congestion/decision_methods/README.md)：含连续成稿、精确校准、原游戏修复、成本拼装、可运行决策器及独立审查；既有线性下界与英文稿从同一成果包恢复入口读取。

另行保留的加权拥塞[结构论文专题](research/current/weighted_congestion/structural_reconstruction/README.md)已从实际资源定义重建端点—面积、共同尺度拼接、权深度和稳定核修复的一般证明，并接通近次数全状态反例与有条件的成本优化。旧[恢复范围对照](research/current/weighted_congestion/decision_methods/previous_structure_scope_comparison.md)保留为历史记录；现行覆盖和审查等级以结构专题及精确账本为准。
