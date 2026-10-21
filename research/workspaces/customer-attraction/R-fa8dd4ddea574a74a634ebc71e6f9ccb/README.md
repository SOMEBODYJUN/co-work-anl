# Boss9：共同客户耦合与一般顺序半覆盖

研究存档：`customer-attraction`；发布身份：`R-fa8dd4ddea574a74a634ebc71e6f9ccb`。本轮环境没有既存项目 clone，由附件启动程序恢复 main 并生成本身份；旧 Boss9 的 R-c93f 与 R-d7f 资产作为已推送来源读取，不把其显示编号等同本 clone 的发布身份。

## 精确主目标与状态

Q-CAG-HALF 仍 **OPEN**：任意有限单位客户、有限非空共同主题目录、任意 m≥1、每个全部有序历史依赖纯 SPE，证明 2W≥OPT_m。重复主题、空主题、零客户和任意历史平局全部保留。个人探索备份不自动成为共享 canonical 结论。

本轮已读取根四入口、适用 AGENTS、模型、本题地图、前沿、失败地图和 RUNBOOK；复用旧 447 行松弛、收益图稀释障碍及覆盖矩表示。没有把静态 PNE/CCE、强 iid 或逐人安全值桥重新作为已证引理。

## 可接续资产

| 文件 | 数学身份、范围与用途 |
| --- | --- |
| [tree_coupling/support_conservation_obstruction.md](tree_coupling/support_conservation_obstruction.md) | 新的精确模板障碍：旧完整策略的收益图加入全部同主题锋利稀释和所有同支持覆盖守恒后，仍有根支付1、比较支付9/4的非负有理向量。它违反二支持跨主题 Shapley 分配身份，甚至没有共同有符号客户表示，绝非 SPE 反例。发现者和另一研究员的独立定义级 Fraction 重构均通过。 |
| [tree_coupling/support_conservation_obstruction.json](tree_coupling/support_conservation_obstruction.json)、[定义级检查器](tree_coupling/verify_support_conservation.py) | 冻结的有理分离向量和独立于优化器的完整验证；重建真实有序后继、全部稀释、覆盖守恒及不可客户表示身份。 |
| [独立审查](global_proof/potential_probe/support_conservation_independent_review.md) | 另一研究员不调用发现者checker，独立重建全部有理条件和不可客户表示身份。 |
| [tree_coupling/pair_circuit_repair.md](tree_coupling/pair_circuit_repair.md)、[根代理独审](audits/pair_circuit_review.md) | 任意人数的双支持正项收益回路，以及用两条回路、三条真实末位比较和五条稀释，把上述指定策略、指定比较组合修复到精确二支付。不能推广成所有策略或比较组合。根代理独立稀疏行重构通过。 |
| [background_induction/joint_baseline_half_profit.md](background_induction/joint_baseline_half_profit.md)、[独立审查](credible_counterexample/background_independent_review.md) | 任意k≥12、每个可覆盖客户既有负载b_x≥k−5时，所有完整SPE剩余利润P≥F_k(b)/2。联合逐客户使用K和末两人theta保底；独立整系数多项式和真实续局审查通过。统一背景k−6时同一联合预算桥被不交主题族严格否定，但半利润本身未被否定。根b=0一般缺口保留。 |
| [credible_counterexample/README.md](credible_counterexample/README.md) | 原五人64原子支持在1284条共同目录菜单必要行下仍有精确O/W>2的非负有理质量。显式条件对齐穷举和Fraction审计已做；仍没有完整策略，绝非SPE反例。 |
| [terminal_credit/README.md](terminal_credit/README.md) | 旧精确税候选的新有限输入攻击：固定五人七主题的八棵完整策略锥，56个浮点查询没有正点。保存代码哈希、参数和输出，仅供避免重复；候选仍未证，也未被反驳。 |

## 活跃工作与未闭合义务

六名指定模型研究员（五直属、一嵌套）并行直接全局证明、势机制、真正聚合安全值、可信菜单构造、全树客户耦合和背景归纳。根代理另攻击保留精确税的实际分数负载候选；有限结果只按有限结果保存。

下一步需要将**共同覆盖资料对不同主题收益的分配关系**加入全树非负支付，而不只保存各支持的总支付。加入全部线性身份仍不等于使用了客户非负实现锥，也不自动保证存在一般 half 证书。背景局部改进或更强模板障碍均不能替代一般目标。

探索继续；有价值资产以根 work.py checkpoint 保存，仅有 `status=pushed` 回执才表示对其他 clone 可见。成熟结果再请独立审查与整理，本目录不提前声明外审或新颖性。
