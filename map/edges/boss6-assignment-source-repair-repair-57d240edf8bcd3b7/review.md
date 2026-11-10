# 第44轮：同一1953客户见证的冻结接受公式修复

本包只替换有效上包 `boss6-fr-status-repair-repair-4de57d1ac5095cea` 中的 `ca-r36-true-query-frozen-assignment-regression`。原26资产逐项处置为 retained25 / replaced1 / retired0；25个未变资产保当前canonical路径与精确SHA，包含第38轮两条FR修复后的新路径。25核心pin不变，覆盖沿用19 linked、6 isolated-after-review。当前任务未声明overlap对象对，故不复制历史closed_overlaps，也无新承接任务。

## 来源及数学身份

变化仅为只读反例 `customer-attraction/frozen-suffix-optimal-topic-assignment-counterexample` 的v5记录和正文来源合同。其原v4到v5记录只变version/body.sha256，模型、精确陈述、量词、假设、作用域、proved地位及证据输入全部保持。v5说明保存的见证、完整策略和作者审计标准库闭包已齐，不需要发现MILP或简化器；历史未运行审计仍如实为未运行。本轮完整读v5正文、目标接受合同、探针源码及原固定输入/策略/报告，复用已成熟完整SPE证明。

## 精确接受公式

同一输入有1953单位客户、63个正重数兴趣型，实际034给利润(1733/3,1736/3,1736/3)，W=1735。完整43历史/258真实IC及最小slack0复用v5已证正文与固定原报告；本轮未重算全树IC。直接Fraction窄核20个三标签支持，仅125覆盖1740。每个标签均有31个私人客户，因此小于三标签的支持可严格扩大，任何含重复的三槽最优元组均被排除。

六个冻结排列中，125、215、251、521费用1736，152、512费用1737。以同一正因子1/1735缩放全部客户质量，W'=1，t=1/1735，全部冻结排列满足cost≥1+t；真实IC与最优性不等式均随客户质量线性缩放。此处使用的是精确接受公式。未运行浮点LP、活跃顶点恢复、原作者审计或16策略探针，不声称算法实际返回该见证。

冻结矩阵按实际玩家为行、125为列，三行为(1736/3,1733/3,1736/3)、(1739/3,1736/3,1739/3)、(1736/3,1736/3,1736/3)。真实改变后缀的查询矩阵前两行均为(1733/3,1733/3,1733/3)，末行均为(1736/3,1736/3,1736/3)。其六个真实matching总和皆为1734，而OPT−W=5。这是同一输入上的两个不同数量；强冻结预算失败不否定真实净差付款候选，也不否定弱冻结预算或half，2W−OPT=1730。

## 边与承接

新边保稳定edge_id、相同source/target、accepted、checks/context、ALL和所有conditions/roles/explanation/scope数学字段。只更新变化的反例端点pin、其正文SHA、Boss6本轮真实审读说明和相应绑定。接受公式比较依然是语境关系，不把已证反例当作完整算法接受合同的逻辑证明。

有效上包receipt、26边合同及supersession已完整读取。第36轮目标边审查与第38轮有效修复审查按精确范围复用。所有39当前任务pins、25旧资产完整绑定及当前源闭包字节均已核；该字节核验不表示重读全部112来源。完整范围见reading-ledger.json，逐项复用见reuse-audit.json。本包没有新来源身份异议或关系证明缺步；原半覆盖及一般付款的开放前件保持原作用域。

本包是外部staging候选，Root仍需将新边安装后标准edge-bind --write、edge-check、checkpoint确认pushed，再done/assemble。worker未操作Git、队列、board或规范文件。
