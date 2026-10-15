# 加权拥塞共同研究入口

**数学从[现行整合说明](../current/weighted_congestion/README.md)进入。**主目标 WC-TARGET v1 仍开放，但团队已保存奇数环 T_d∼d/ln d 下界、独立审查及可复用结构工具。不能继续沿用旧版“尚无成果”的描述。

当前天团具体判定全类 O(d/ln d) 近似纯均衡存在命题，给一般证明或严格否定证明才算完成；精确量词、规模无关常数及唯一标准见[本题验收](ACCEPTANCE.md)。局部材料按真实等级保存并继续为该题服务。

新对话读根四入口、[MODEL](MODEL.md)、现行数学 README、[CLAIMS](CLAIMS.md)、[当前状态](RESEARCH_STATE.md)，再按当前义务选择证明与审查。开始工作用[TEAM](prompts/TEAM.md)；修改工具才需要完整读[运行说明](RUNBOOK.md)、[协议](PROTOCOL.md)及程序源码。写作、工具提取各有独立提示词，不要求所有研究者先通读全部上游原文。

## 角色与 Pro 交接顺序

| 入口 | 实际任务与交付 |
| --- | --- |
| [清晰者 CLEANER](prompts/CLEANER.md) | 从精确正文与审查筛出 Pro 必须知道的模型、已知事实和障碍；逐项保留否定范围，维护一份自足 PRO_BRIEF，最终从同一已推送版本导出精简包 |
| [提取者 EXTRACTOR](prompts/EXTRACTOR.md) | 重建可复用工具的输入、输出、条件和证明；与清晰者核实按需接口，独立有价值但不助接题的资产仍留仓库 |
| [Pro 攻题 PRO_ATTACK](prompts/PRO_ATTACK.md) | 收到实际整理材料后，自主解决原全类问题；不把 Git 操作、历史审计或写论文作为前置 |
| [论文者 PAPER_WRITER](prompts/PAPER_WRITER.md) | 组织真实成果的贡献、机制、完整证明及实际成稿；不与交给 Pro 的材料筛选混为一个角色 |
| [共同研究 TEAM](prompts/TEAM.md) | 持续攻击唯一题目并维护可复用资产；可以同题独立推导或探索多条路线 |
| [共同操作 OPERATIONS](prompts/OPERATIONS.md) | 各 Work 角色共用的恢复、唯一发布身份、命名地图、阶段核验和完整推送合同；只需共用一份 work.py |

本次准备顺序：清晰者与提取者可并行阅读和核对，清晰者整合及审读后再把精简包和 Pro 任务交出。论文成稿可另行进行，不是 Pro 攻题的先决条件。各角色首次生成不同前缀的随机唯一后缀并显式传入 `start --actor`；同 clone 接续复用，不照抄固定 W1/E1，也不为子 agent 登记。

角色提示词就绪不表示交接材料已整理。`PRO_BRIEF.md` 仅在清晰者实际完成筛选后创建或修订；交付包仅带完整任务、必要数学正文及追溯 manifest，工具数学附录按需。历史聊天、测试日志、全仓文件和未证 idea 清单不作为默认 Pro 输入。方法障碍、断言反例、开放义务和有限观察分开，不将“没做出来”写成“不可能”。整理与提取完成也不表示主问题解决。

## 当前数学地图

提取者新增的[正占用核专题](../current/positive_kernels/README.md)从boss4正Möbius展开重建独立的秩暴露面、锐截断及准确闭包；来源与具体传感器实例可核。它保留原WC身份，并明确一般签名/均衡桥缺口；工具索引见[toolbox](toolbox/README.md)。

正权有限资源博弈 → 真实成本与 α-PNE → 全类阈值 a_*(d)。奇环策略 → 全状态严格偏离 → 权重及系数闭环 → 有限有理构造 → T_d 下界。文献上界 d 仍留对数缺口；精确目标见 MODEL。[高次份额势](../current/weighted_congestion/high_degree_share.md)、源族、稀疏密度、窄权带、非对称有限例和势方法障碍的范围各自独立。

已审正文在 `research/current/weighted_congestion/`，待审候选在 `research/questions/weighted_congestion/`，实际审查在 `research/reviews/weighted_congestion/`，核验代码在 `tests/audits/weighted_congestion/`，冻结证据在 `evidence/`。完整用途和状态见 [FILES](FILES.md)，不可变原件和分支处置见 [INTEGRATION](INTEGRATION.json)。[LITERATURE](LITERATURE.md)、[PRIOR_ASSETS](PRIOR_ASSETS.md)按需查来源与前人机制；新颖性尚未认证。

## 共同工作

每个 Work 对话使用独立 clone 和一个稳定发布标识；程序可自动生成，无需登记子 agent。各 boss 自主组织团队，同题和多路线都允许，无认领和固定时长。有启发的半成形 idea、卡点、反例和合作问题可随时发到[公屏](https://github.com/SOMEBODYJUN/co-work-anl/blob/wcg/board/research/weighted_congestion_frontier/board/BOARD.md)，注明不确定性；聊天不要求先成稿或审查。普通排错与逐轮日志无需强制汇报。

可复用阶段成果按原 [GROWTH](../GROWTH.md) 入库后立即 checkpoint 到 main，远端确认后再分享入口。main 同时保存候选与已审成果，证据等级不会因推送改变。研究和提交统一 main，不创建研究分支；具体题目、完成标准和命令可直接复制 [TEAM](prompts/TEAM.md)，详细施工和读取规则见[全仓规则](../REPOSITORY_GUIDE.md)。

每次阶段提交把正文、精确登记、中文命名及相关地图一起维护：在 `research/catalog.json` 写具体名称和读取用途，生成 CATALOG、FILES 及受影响的关系图，再运行对应检查。根地图每次审阅，目标、结果、依赖、状态、前沿或导航变化时更新；本题新资产必须从数学地图和资产目录可达。`checkpoint` 负责 Git 保存与远端确认，不代替内容核对或结构检查；默认范围外的入口更新须显式列入完整提交清单。启动提示词同时提供未上传可选 `work.py` 时的恢复办法。

已闭合的方法审查入口：[任意玩家乘子与依游戏可分序势线性障碍](../current/weighted_congestion/separable_ordinal_obstruction.md)。只否定所写全改善边证书，全类匹配上界仍开放。

不预设势的精确接口：[有限动作签名压缩与全状态择证对偶](../current/weighted_congestion/template_certificates/finite_action_duality.md)。固定权重/动作数的所有资源游戏等价于有限单项式系数族；普遍α存在等价于每个全状态selector自有对偶证书。统一于所有模板的倍率仍未证明。

[严格反例的整数单项式规范形与普遍阈值端点](../current/weighted_congestion/template_certificates/integer_counterexample_normal_form.md)接有限动作择证接口：固定实倍率反例可只用整数权和单位单项式资源，且a_*端点可行；无全类规模截止界。配套独立审查、Fraction程序和冻结结果从正文或FILES进入。 [空交反链核心](../current/weighted_congestion/template_certificates/integer_counterexample_normal_form.md#7-去包含支配与必选背景的空交反链核心)进一步把反例限制为人人至少两非空、无包含、空交策略，并给所有α≥1同时有效的单向lift；允许删玩家，不给规模界。

跨尺度结构接口：[有序权组冻结及两权级参数锐式](../current/weighted_congestion/weight_bands/ordered_tail_freezing.md)允许阶段局部势选择，但其最佳潜在尾部参数无统一界；[DAG端点低泄漏预算](../current/weighted_congestion/polynomial_curvature/dag_low_leakage_budget.md)只封闭指定检测系统，不代替全状态多项式证明。独立审查与实际代码/证据均由正文接入。

两权跨尺度新增[双排序混合势](../current/weighted_congestion/weight_bands/two_weight_order_blend.md)：任意两权cohort给统一平方根次数存在界；不依赖潜在尾部量。独立攻击与代码从正文进入。多权共享乘子桥仍OPEN。

[择证平稳与循环支撑边界](../current/weighted_congestion/template_certificates/stationary_selector_obstruction.md)、[有向分叉统一强迫割均衡](../current/weighted_congestion/directed_fanout_forcing_cut.md)连接新的非势路线限制和下界构造限制；逐项Claim、独立审查及可复算证据均从正文/FILES进入，主目标仍OPEN。

真实多项式子类的新边界：[阶跃DAG极值幅度的多项式全入状态](../current/weighted_congestion/step_dag/polynomial_extremal_all_in.md)。请先核对幅度(N)再调用；它不依赖端点低漏测试，仍没有全类幅度/拓扑归约。

[循环窗口复制的真实近d改善环](../current/weighted_congestion/cyclic_clone_improvement_cycles.md)将旧可分势障碍提升为任意全局全边下降势障碍，仍有全空精确PNE。[共同幂混合最小点障碍](../current/weighted_congestion/common_power_mixture_obstruction.md)另直接排除指定连续目标族的全部最小点。全类存在性仍OPEN；环本身不能当无均衡；[锚定三元全状态锁定](../current/weighted_congestion/anchored_cycle_lock.md)已将严格双轮环编译成无α-PNE，但新增次数依实例。[统一低泄漏锚定时钟预算的普适次数障碍](../current/weighted_congestion/uniform_clock_budget_barrier.md)已证明满足现行统一预算的全部输入均有α ln q/q<α/(α+1)<1；负向前沿须改用实际时钟差、非统一预算或其他全状态机制；[三次锚定架构证书](../current/weighted_congestion/anchored_clock_degree_barrier.md)已排除在指定基体上保持原degree的方案，未排常数倍degree。正向仍需选步或超出这些目标族的选态。

[有限可动权类的三角排序势](../current/weighted_congestion/weight_bands/finite_weight_class_potentials.md)已给A_(d,k)隐式界，固定k为d^(1−1/k)，任意固定背景精确吸收、k个R窄簇损失R^d。d≥16且k≤ln d/lnln d的明确子类达到2d/ln d；无界可动类别时A趋d，唯一全类题仍OPEN。真正前沿已收缩为无界可动权类的选态桥或全状态增长反例，不再把固定背景或仅两类稠密cohort当未解接口。

[有限次局部矩与全成本压缩](../current/weighted_congestion/template_certificates/selector_local_moments.md)将签名接口细化为D维完整成本空间、≤D正单项式资源保真表示和≤D+1支撑dual；其仿射全签名刚性另表明：非全等权下，低degree成本不能保真拆成全小用户支持资源，即使提高次数。完整proper锥另可同时实现近d真实唯一坏环和完全暂态dual，任何dual暂态质量必须为正；这是已知两机制的同时化，不给任意selector方法。真正未解仍是每个selector的moment hull与resource polar是否在统一倍率相交。[循环窗口前沿商与不同步反例](../current/weighted_congestion/class_front_phase_quotient.md)提供相对phase表示，但类内clock不能自动给错位front出口，故负向仍需新同步/离front覆盖机制。两包均未完成唯一全类题。

[共享侧资源截断势](../current/weighted_congestion/shared_side_truncated_potential.md)把同权hub、unique-light/source、最坏负载UF子类扩到任意共享hub子集，给A_d≤2d/ln d；独立AS+B判据覆盖部分非UF实例。[实际时钟差分与预算](../current/weighted_congestion/anchored_clock_actual_margins.md)给非统一clock的O(n²)充分LP、必要总预算和κ稳定条件，固定四玩家43次证书优于原uniform91选值但不称最优。原全三元、统一M架构另有80次全状态证书却不满足(U)，故(U)对原架构也非必要；这仍不是增长族。实际接口另证：固定人数/权谱/α/纯三次亦可用private成本压低环余量，阻止任意预给degree cap的保环三元clock；健康余量增长输入仍未排除。真正缺口仍是无界可动权类的全类选态、跨source/预算外反馈或次数效率可增长的全状态族。

[共占图高度与实际改善环必要链](../current/weighted_congestion/weight_bands/finite_weight_class_potentials.md)把三角势参数从全局权类数放宽为同一降权共占图的路径高度；全局权种数可无界。实际严格改善闭词也必须跨越相应高度门槛，各弧可来自不同端点。仍无全类高度控制；动态换秩改变势，缺少高链SCC出口或瞬态dual。
