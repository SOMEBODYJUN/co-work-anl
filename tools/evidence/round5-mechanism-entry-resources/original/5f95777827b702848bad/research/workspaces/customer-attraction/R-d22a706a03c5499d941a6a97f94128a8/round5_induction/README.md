# round5：可变人数利润归纳与直接机会缺口

Q-CAG-HALF仍OPEN，2026-10-23。

- [unbounded_profit_bellman_obstruction.md](unbounded_profit_bellman_obstruction.md)：**本轮主结果，任意固定局部系数均失败。** 原文all-big完整SPE族已给精确根台阶h_n−1≈2sqrt(n)，当前收益恒1；root独立解析通过。尾部信用规模被精确定位于sqrt(n)，但尚未得到一般非循环信用状态。
- [credit_state_obligations.md](credit_state_obligations.md)：**解析模板障碍，root已独立核对。** 只由背景/真实尾部共同覆盖客户贡献的任意实例无关、r依赖可加信用，不能同时承担全背景尾部利润界与每节点信用递推；同两无限族迫使同一核f_r(1,r)上下界矛盾。未找到一般非循环信用状态，正文给出准确剩余proof obligation。
- [profit_bellman_counterfamily.md](profit_bellman_counterfamily.md)：新解析障碍。以既有完整SPE无限族精确计算合法背景剩余最优利润，证明系数二Bellman归纳对每个n≥5失败，固定局部系数至少趋17/6；一般half未被否定。
- [audit_profit_bellman_family.py](audit_profit_bellman_family.py)、[精确输出](profit_bellman_family_exact.json)：直接枚举n=4,…,8共15501个剩余主题多重集合核对新最优值；不是普遍SPE外推。
- [bellman_diagnostic.py](bellman_diagnostic.py)：该明确一般候选的有限诊断工具。首先在既有22客户输入的另一可实现终局中发现系数二亏空；不作为新的单位客户证书。
- [weak_gap_diagnostic.py](weak_gap_diagnostic.py)：有限检查OPT−W≤m min u与更强的插入保底；插入保底被既有输入击穿，弱机会缺口未有证明。
- [weak_gap_cone_probe.py](weak_gap_cone_probe.py)、[运行记录](weak_gap_cone_probe_exact.json)：只对每个既有小输入至多两个终局生成34棵完整策略，单次优化967个“OPT−m u_i”目标；未找到严格违反。最大0.75仅为浮点候选最大值，未恢复全套有理对偶，不能称为这些锥的认证上界，更不能支持一般桥。该固定候选诊断已停止，不继续调人数或乘子。
- [background_gap_diagnostic.py](background_gap_diagnostic.py)：有限合法背景诊断F_r(b)−P≤r min剩余u。已检19个输入2503个背景/SPE终局计数，无违反只作工具运行记录，不支持普遍桥；未把它从背景提升为全局每玩家预算。

当前障碍：F_r(b)自身是合理的同背景可变人数目标，但丢掉尾部信用后，任何人数无关的当前收益倍数都无法局部Bellman传递。下一步必须给跨真实节点可搬运的信用状态，或直接攻击最优与实际福利差额，避免把同类局部floor/安全值接口重写一次。
