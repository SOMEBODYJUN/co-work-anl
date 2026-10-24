# 一般半覆盖：一次退款不能被固定在原角色

2026-10-24；存档 customer-attraction；程序身份 R-b659ddeec819493bb10dc58441fa7b3d。
本轮六名实际 gpt-6.1-sol / ultra 子研究员与父方共同研究。**Q-CAG-HALF 仍 OPEN，没有一般证明或目标反例，也没有新的无条件福利界。**

本轮可复用的新边界是：即使允许有利重选最优并集，也不能要求每个实际玩家用自己的利润加自己的最优并集外收益，逐期支付最终遗漏集的最优覆盖曲线差额。完整179单位客户例有唯一最优并集，排除了通过重选最优组合修复这个合同。它的福利107、最优111，远不违反half。

## 恢复顺序与文件地图

| 文件 | 内容、数学身份及读取条件 |
| --- | --- |
| [GENERAL_WORKING.md](GENERAL_WORKING.md) | 父方直接一般推导：准确净需求 L−E；PREFIX门槛及平稳回推未付处；新逐期退款候选的充分性和失败；下一步必须证明的共享预算 |
| [CLAIMS.md](CLAIMS.md) | 原主目标与本轮强化候选的精确对象、量词、状态、证据和反对意见；防止把局部反证扩大成half反证 |
| [RESEARCH_STATE.md](RESEARCH_STATE.md) | 当前真实研究边界及下一步，区分新的合同失败、旧机制特化和未证明付款 |
| [FAILED_ROUTES.md](FAILED_ROUTES.md) | 一次角色退款为何失败；可回收总账与何时值得重试 |
| [自足反例正文](refund/unique_optimum_refund_floor_counterexample.md) | 客户类型、完整策略、全部真实收益与唯一最优性；从旧71客户机制派生，只认领本轮精确合同的失败 |
| [冻结原始证书](refund/prefixed_refund_counterexample.json) | 179个单位客户的压缩输入与57个独立有序历史动作；逐定义核验的唯一原始数据 |
| [作者审计](refund/audit_unique_refund.py) | 全单位客户重放与399项IC、84个无序最优比较；输出unique_refund_audit.json |
| [独立盲审](independent/refund_candidate_blind_review.md) | 先自行重构候选，再只读原始证书；不导入作者程序；核验全部历史与唯一最优并集 |
| [父方另路审计](parent/audit_refund_units.py) | 再按179个单位客户核399项IC与343个有序最优比较；[输出](parent/refund_unit_audit.json) 固定JSON的SHA-256 |
| [投影退款接口](refund/shared_refund_projection.md) | 删除最优并集外客户时的真实收益差与实际路径后悔预算；投影计划未必SPE，尚未接入覆盖付款 |
| [多槽补全约束](exchange/multi_slot_completion_exchange.md) | 全输入静态最优补全集合恒等及关联/尾负载矩；没有新动态IC或福利界 |
| [自洽池误差定位](security/reactive_tail_sc_debt.md) | 旧协方差/曲率机制的池化特化，明确旧前缀不产生反应协方差；未证付款，不认领新机制 |

这些是个人阶段研究资产，不自动进入共享canonical数学状态；反例已经作者、独立研究员和父方三种定义级实现核验。没有外审或全球新颖性认证。

## 下一步

需要同一完整策略全部后继IC到共享净覆盖预算的新关系；允许跨角色转移退款，不能再把本轮逐角色合同当作前提。把总容量写成 W+E>=L 恰好是half本身，改名不算付款证明。成熟资产可请清洗者核对来源与去重，探索不等审核。
