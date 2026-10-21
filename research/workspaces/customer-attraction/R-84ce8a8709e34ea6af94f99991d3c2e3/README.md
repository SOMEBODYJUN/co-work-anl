# Boss10：一般顺序半覆盖研究桌面

发布身份：`R-84ce8a8709e34ea6af94f99991d3c2e3`；存档：`customer-attraction`。
精确主目标为根模型的 **Q-CAG-HALF**：任意有限共同目录、任意人数、每个完整历史依赖纯SPE满足 `2W>=OPT_m`。允许空主题、重复选择、零客户与任意历史平局。一般命题仍 **OPEN**。

## 可接续资产与真实状态

| 路径 | 内容、证据和用途 |
| --- | --- |
| [duplicate_quotient/duplicate_coverage_quotient.md](duplicate_quotient/duplicate_coverage_quotient.md) | B10-DUPLICATE-COVERAGE-QUOTIENT-v1：相同覆盖标签可合并，完整历史SPE的投影终局、逐人收益、福利和OPT全保留；两路独立重构内审通过，无外审/新颖性认证。它消除一般目标中标签重复与真正子集目录之间的接口缝隙，不提供新福利界。 |
| [duplicate_quotient/audit_duplicate_quotient.py](duplicate_quotient/audit_duplicate_quotient.py) | 双向完整策略构造与有限精确回归，实际结果 `duplicate_quotient_audit.json`；含空目录覆盖、重复标签、交叠、历史依赖平局。 |
| [literature_bridge/priority_valid_utility_counterexample.md](literature_bridge/priority_valid_utility_counterexample.md) | LB-PRIORITY-VALID-UTILITY-SPE：非匿名编号优先分配给共同singleton目录的全历史SPE，W=1、OPT=m；证明valid-utility静态三条件不足以推顺序half，明确非CAG。已独立重构内审，有限审计在同目录；新颖性未认证。 |
| [literature_bridge/primary_source_followup.md](literature_bridge/primary_source_followup.md) | 一手文献适用条件补查；没有发现可直接导入的任意目录/人数/全部平局定理。检索未发现不等于不存在。 |
| [counterexample_search/nonpne_cone_probe.py](counterexample_search/nonpne_cone_probe.py) | 保留正静态盈利偏离的真实完整策略锥攻击接口，防止LP走回PNE极点；有限运行和最佳点证书在同目录。不是一般反例或全称界。 |
| independent_bottleneck/ | 孤立外部主题、漏覆盖客户威胁预算的探索；候选尚未证明。 |

## 当前承重缺口与团队工作

目前仍缺跨真实续局分支的总福利预算。团队研究：带背景非局部归纳、带泄漏的偏离充电、非极小可信续局、incidence保护集合、C/D漏覆盖威胁预算和独立背景桥攻击。逐人混合安全值、根税、每步非负、固定后继等已知失败不再当作引理。

未完成想法按真实状态保存，不能因有限无反例升级。下一步应优先闭合适用于无界人数和目录的匿名均分承重机制；若某加强背景桥被反驳，提取其准确失效项后继续根目标。共享入库需要清洗者检查与登记；此个人备份不自动提升canonical状态。
