# round12/geometry：一般 HALF 的随机优先与需求律探索

2026-10-25。任意人数、任意共同有限目录、每个完整历史纯 SPE；HALF 仍 OPEN。
不继续固定策略锥或 fresh-cap 扫描，不以 PSD 重排冒充新资金。

当前探索：共同随机优先耦合全部真实偏离请求，把同一角色上的多 action 请求
接入一份合法偏离预算，将损失按实际 OPT 外客户 G 只付一次。
尚无合法耦合定理。概率边际本身不会把不同 action 的 IC 共同付款。

`request_coupling_working.md` 保存精确对象、正确边际及未付部分。

`one_query_convexification_candidate.md` 给一次查询的准确凸化代价 Vp/2<=gamma/2，
并提出更强的一般候选 C<=D+IC+(Vp+Qstat)/2。没有证明未来重置只留下这一份代价，
故 HALF 以及任意五人压力仍未通过。无新扫描。

`conditional_demand_and_information_budget.md` 保存固定中间动作 fiber 的末位
最优运输需求律，以及共享同一查询样本时的 martingale 总方差预算。
核转换、真实交叉历史重置和信息增量重复计费仍未付；不把二者并列当作闭合证明。

`cross_history_mean_cap_transfer.md` 给同计数交叉 child 尾部对称混合的准确 cap
半差额和 child IC 上界。tree12 独立核验通过局部代数，但父节点补全、
中间 IC 与祖先 cap 尚未保持，故没有 capped-credible 域的对称闭包。

`conservative_raw_tail_replay.md` 构造 freed-tag canonical mean-floor 域中的真正
同根保守 replay：P_i 到 selected Q_i 的终端边际准确，固定 F_i 的 signed
差额只花原 source 银行，并给零统计代价 posterior retag。
对角 work 化成单查询 reverse-martingale 信息增量乘 prefix-load 的精确式；
该 prefix 乘数尚未由曲率/IC 付款，故未闭合 HALF。

`uniform_net_cross_history_symmetry.md` 保存最新 uniform NET-cap 的变化：
canonical M 计数不变，raw 对称尾部没有额外可信性域门，但 NET-cap 准确改变
cross-current minus cross-root 的整差额。统一 mu 可定价，不代表该差额已付款。
最新域只能用组合 net-cap，不能沿用旧 mean-FLOOR 的分别 cap/floor 符号。
