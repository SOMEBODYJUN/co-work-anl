# Boss7：完整历史顺序客户吸引的一般半覆盖

研究存档 `customer-attraction`；本对话生成身份 `R-7e9f44beea424d469713364afe7dd180`，独立 clone `co-work-anl-boss7`，分支 main。恢复以本 clone 绑定和根 work.py 为准；凭据不在仓库内。

## 精确目标与现状

唯一主目标 Q-CAG-HALF 仍 **OPEN**：任意有限单位客户、共同有限非空目录、任意人数、所有完整有序历史上的纯 SPE（任意历史依赖平局），证明 `2W >= OPT_m`。原模型、量词和零客户边界均未改变。以下个人资产不自动提升 canonical 状态，没有外审或全球新颖性认证。

## 已有可接续资产

| 文件 | 数学内容、状态与用途 |
| --- | --- |
| [删除最优覆盖外客户的单调归约障碍](global_proof/deleting_opt_external_customers_obstruction.md) | 两人三主题解析无限族：仅添两个唯一最优覆盖外客户，OPT 不变，最差 SPE 福利下降无界。另有 9q 客户、末位无平局族。否定指定删客户归约，不反驳半覆盖。作者按单位客户独立枚举，Boss 另用规范全集求解器与证书核验 Q=4,5,13,100 及 q=1,2,7。 |
| [定义级核验代码](global_proof/deletion_obstruction_audit.py)、[实际报告](global_proof/deletion_obstruction_audit.json) | 无求解器依赖，Fraction 展开单位客户，枚举每个末位 selector 与根 maximizer；报告给精确范围和完整离轨表。任意参数证明在正文。 |
| [末位份额及两倍逐人收益桥反例](credible_counterexample/payoff_cap_failure.json)、[独立审查](independent_mechanism/payoff_cap_independent_review.md) | 三人五主题、23 单位客户，完整 SPE 路径012，收益(5,6,12)，W=OPT=23。故 `2W >= (m+1)u_m` 及 `max u <= 2 min u` 均为假；独立展开单位客户核验全部31历史与124非自偏离，Boss另独验。不是half反例。 |
| [全树收益图与强连通商锥](full_tree_dual/outcome_payoff_graph.md)、[独立审查](background_induction/full_tree_independent_review.md) | 固定任意人数/目录完整形式策略，真实行锥精确分解为全深度 SCC 可双向支付空间加凝聚弧锥。18 客户例将末层平局空间秩1严格扩大到秩3。型映射还可产生额外 lineality，不能误称 SCC 穷尽。一般 half 的非负商图流预算未构造。 |
| [强 iid 福利支付反例](aggregate_security/strong_iid_failure.md)、[精确核验](aggregate_security/verify_strong_iid_failure.py) | 对既有八客户实例，唯一 iid 谐势最大分布给 `Z_3=(4344-156 sqrt(669))/49 > W=6`。自足 KKT/二次域审计，Boss读证并重跑；这是既有输入的新精确蕴含，不是新实例。弱 iid、真正聚合静态安全值及 half 均未被反驳。 |
| [任意玩家最大主题近饱和必要式](independent_mechanism/max_topic_saturation.md) | 任意实际玩家收益t、目录最大主题M、L=OPT/(2m-1)：非末位有 `L <= (m-1)^2 t-(m-2)M`；末位t≥L。含全型非负证书及仅用size cap/后继下限的非SPE松弛障碍；不足以一般half，未称新颖。 |

## 活跃探索与未闭合义务

六名 gpt-6.1-sol ultra 内部研究员分别探索直接全局控制、可信续局闭包、真正聚合安全值、全树对偶、带背景归纳及独立新机制；由 Boss 汇总交流和提交，无独立发布身份。路线随数学信息调整，不设置审批或配额。

目前仍缺少一般跨真实分支支付：须同时控制后继的可信性及其对既有玩家份额的改变。逐人安全值、静态 PNE/CCE 福利支配、强残余覆盖、计数 Markov 终局归约等已有明确反例，不能当作引理。全树收益图的强连通等式空间正在形成自足表示；弱逐人 `u_i >= OPT/(2m-1)`、真正聚合安全值及全局背景补偿仍未证，有限策略锥扫描不提升这些候选。

直接 half 联合 MILP 的一个实际运行边界：五人七标签、路径00112、比较组合23456，39341变量/394950约束，60秒未产出整数候选，不能据此断言可行或不可行。三人五/六标签的弱逐人目标四次短运行均只给精确取等 `OPT/u_1=5`，不是一般证明。详细范围在 [可信续局分支](credible_counterexample/README.md)；有限无反例不增加普遍命题真值。

接续优先义务：在已精确保留全部真实行的 SCC 商图上，共同构造跨分量非负流、可双向内部支付及逐客户非负余项，使 `2c-o` 得证；势计数图的 cycle 核可作为新增资源恒等式。另一承重候选是合法背景中前两位总利润至少两倍真正静态安全值，尚未证明。OPT外客户阈值级联构造在末位出现“未碰撞惩罚主题更盈利”的可信性障碍，须真正修复而不是冻结后继。更多同模板随机样本的信息价值已下降；下一轮应改变解析机制或联合搜索表示。
