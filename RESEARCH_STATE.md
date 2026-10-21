# 当前研究状态：一般目录、任意人数的顺序半覆盖

当前主攻 **Q-CAG-HALF**，存档 **customer-attraction**，状态 **OPEN**。本次切换是用户的研究选择，不是新数学结果；数学陈述、原有证明和冻结证据均按各自版本保留。

## 已知地基

三人一般目录有锐5/3福利界，四人一般目录有1499/750<2界；五人当前约2.061695仍高于2。至多六个不同包含极大覆盖的任意人数半覆盖已证；七极大只有已登记的部分范围。详见[逐范围地图](research/current/customer_attraction/README.md)，不要把它们表述为一般猜想已解。

新增[分数覆盖前缀利润预算](research/current/customer_attraction/fractional_cover_path_budget.md)对任意比较集给乘积福利保证；某个最优并集分数覆盖数至多7/2时，任意人数与无界目录半覆盖成立。覆盖数无界的原目标仍OPEN。

## 当前瓶颈

在同一完整纯SPE中，早期偏离改变后继整条路径。需要利用所有真实分支的最优性控制最终福利；逐人保底、逐步非负、冻结后继和根总税已有反例。全局补偿、真实分支转移及直接全局证明均可自由探索，现有接口不是必选路线。

## 本次工作安排

Boss直接带团队攻一般命题。清洗者处理数学检查、自足改写、身份和证据登记；整理者评估独立文章、拆合及贡献表达。三者都可沟通，探索不等待清洗或写作批准。重要进展及时checkpoint，数学状态只随真实证明和异议处理改变。

下一步从[本题前沿](research/customer_attraction/RESEARCH_STATE.md)和[保留问题](research/customer_attraction/RETAINED_QUESTIONS.md)选择真正未闭合的义务；不要重新从零证明已完成特例。统一入口为[work.py](work.py)，操作见[RUNBOOK](research/customer_attraction/RUNBOOK.md)。

## 暂停而保留的研究

| 模型 | 状态与接续入口 |
| --- | --- |
| 一般不相关机 | UM-TARGET-v1及一般反面均OPEN；[旧题地图](research/current/unrelated_machines/README.md)保留条件结果和方法障碍，暂停默认主攻 |
| 加权拥塞 | 线性全状态下界及Theta(d)推论已有内部完整稿；精确常数、优先权与外审独立开放，见[旧题地图](research/current/weighted_congestion/README.md) |
| 两阶段设施 | 双设施黄金比、实例复杂度、多设施因子二存在等分别保存；一般高效构造与最佳常数仍有缺口，见[设施入口](research/current/README.md) |
| 正占用核 | 表示、交互秩与闭包工具；一般均衡桥未给出，见[专题](research/current/positive_kernels/README.md) |

本次删除的是当前入口里的重复逐轮摘要，旧操作角色原文移入历史；旧模型的独有数学资产未作为垃圾删除。详见[清理记录](research/customer_attraction/CURATION.md)。

本轮已审机制边界：[三人十六客户反例](research/current/customer_attraction/worst_pne_welfare_counterexample.md)使SPE福利低于同实例全部静态PNE福利，排除最差静态PNE福利支配桥；另有[十三客户完整反例](research/current/customer_attraction/worst_cce_welfare_counterexample.md)排除最低静态CCE福利支配（W9<137/15≤min_CCE E[W]=2785/297）。两者均不是一般半覆盖反例，真正聚合安全值桥仍开放。

[覆盖矩表示](research/current/customer_attraction/coverage_moment_geometry.md)及[全人数无拥挤族](research/current/customer_attraction/collision_free_three_halves_family.md)已独立内部重构：线性方向完整不等于非负支付；真实离轨拥挤可维持实际无拥挤而OPT/W趋3/2。一般half及安全值聚合仍OPEN，无外审/新颖性认证。

用户指定的加权拥塞应用方法专题已形成[专题成稿与复现包](research/current/weighted_congestion/decision_methods/README.md)。当前改进是共同尺度证书、原游戏有条件压缩及稳定成本选择；一般位多项式搜索与真实业务效果仍分别需要新证据。其他研究主目标与原有定理范围不变。

用户补充参考后，已明确[旧结构主线仍缺失的内容](research/current/weighted_congestion/decision_methods/previous_structure_scope_comparison.md)。上轮未按完整旧证明复原，新方法专题不代表旧工作已恢复；当前拥塞接续应优先补齐原主结果和结构论文。

更小独立静态桥见证：[八客户四主题计数SPE](research/current/customer_attraction/eight_customer_cce_welfare_gap.md)福利6，最低静态CCE福利恰544/87；它不改变原十三客户版本身份，不否定真正聚合安全值。
