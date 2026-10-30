# 本轮精确命题

## Q-CAG-HALF

身份、对象、定义、假设、域、量词、结论以 [原目标](../../../questions/customer_attraction_half_coverage.md) 和 [模型](../../../current/customer_attraction/model.md) 为准。状态OPEN；本轮没有更改任何量词，没有一般证明或真正反例。

## CA-LAST-SUCCESSOR-PEEL-v1

- **Exact Statement / Objects / Domain：** 对原模型任意实例、任意完整历史纯SPE、任意合法有序前缀、任意同一个目录概率分布p，使用[正文](menu_covariance/last_successor_peeling.md)式(1)–(5)全部定义，有PEEL、PAY及PATH-PEEL的精确等式。
- **Quantifiers / Assumptions：** 目录、人数、客户数不设固定上界。节点恒等式甚至对任意完整纯策略成立；非负e与L需要真实当前及真实末位的SPE行。A,T独立同分布，不能按客户分别换源。
- **Definitions / Scope：** 每条强制分支保留原全部后继(A,Y_A,B_A)，h_A=b+c(Y_A)。D为真实当前平均利润，F为删除当前槽的独立查询，C为保留该槽再插入查询。Delta是同一对源的两主题势背景漂移。
- **Conclusion：** D−F=E L+Delta，D−C=E L+Delta+J，u−C=e+E L+Delta+J；e,L,J≥0。全路径W−Σpsi=Σ(e+E L+J+G)+ΣDelta，G≥0。
- **Dependencies：** 两主题逐客户对称恒等式、iid交换、原SPE真实末位最优性；没有外部定理导入。
- **Evidence：** 作者解析推导；父方独立解析重构及标准库Fraction全纯策略审计；dynamic_theta独立检查与真实混合历史递归审查。
- **Counterevidence / Objections：** Delta可为负；中间替换需重置原真实后继，不能默认降深后原有全部非负项继续免费保留。未付总漂移仍与一般菜单预算相连。
- **Status：** 内部解析检查通过的精确工具分解；没有外审或新颖性认证；不是一般half证明，不提升原主目标。
- **Related Files：** [正文](menu_covariance/last_successor_peeling.md)、[父方审查](parent/peeling_independent_review.md)、[独立脚本](parent/audit_peeling_independent.py)、[冻结输出](parent/peeling_independent_audit.json)。
