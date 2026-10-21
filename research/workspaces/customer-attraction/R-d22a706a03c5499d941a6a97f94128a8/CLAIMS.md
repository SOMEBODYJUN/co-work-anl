# 本桌面的精确 Claim

## Q-CAG-HALF

精确模型、量词和目标均按 [主目标](../../../questions/customer_attraction_half_coverage.md)。本轮状态 **OPEN**；没有一般证明或目标反例。

## B10-UNIQUE-OPTIMUM-OMISSION-OBSTRUCTION-v1

- **Exact Statement / Conclusion：** 存在二人、六个两两不同主题、71名单位客户的合法共同目录游戏及完整历史纯 SPE，其实际覆盖 C 的 W=35；唯一最优无序二主题组合的并集 O 满足 |O|=OPT₂=38，|O∩C|=2，|O\C|=36>35。故“每个实例每个纯 SPE 存在最优 O 使 |O\C|≤W”是假。
- **Objects / Domain / Quantifiers：** 存在性反例，m=2；一般主模型允许的单位客户、共同目录、完整全部有序历史策略。最优组合允许重复；唯一性按无序主题多重集，不排除两个有序排列。
- **Assumptions / Definitions：** [CAG-MODEL](../../../current/customer_attraction/model.md)；不限制通用模型的平局规则。
- **Dependencies：** 仅模型及正文所列14类单位客户与七节点完整策略，不导入静态 Nash 桥或外部定理。
- **Evidence：** 发现者和 root 各自从定义展开71单位客户、Fraction 核验42含自身比较，穷尽21个无序二主题多重集。
- **Counterevidence / Objections：** 尚无成立异议；一般半覆盖在此例余量 2W−OPT₂=32，故本结果不能反驳主目标。真实范围仅所述辅助桥及该唯一最优遗漏集的更强价格预算。
- **Status：** 完整解析有限证书、独立内部重构通过；未外审，未认证新颖性，未整理为共享 canonical。
- **Related Files：** [正文](exchange/unique_optimum_omission_obstruction.md)、[发现者审计](exchange/audit_unique_optimum_omission.py)、[root独立审计](parent/audit_optimal_omission.py)及各自冻结JSON。
