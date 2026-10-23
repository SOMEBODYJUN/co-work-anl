# 真安全最优查询与弱额外一槽聚合

2026-10-23，子任务 checkpoint。一般 Q-CAG-HALF 和弱聚合
`sum_i G_i^+(p*) <= W` 均 OPEN；本目录没有新一般证明或 SPE 反例。

已读完整模型、强聚合空稀释反例、完整终局菜单接口及旧截断障碍。
当前任务是利用真正静态 maximin 最优查询 `p*` 或真实中间离轨比较产生支付，
而非再把 `G-D` 与真实根松弛写成等价式。

## 已停止的重复尝试

曾独立重建以下小型非 SPE 形式策略：`m=2k`，`L` 个互不交 singleton 主题，
实际路径 `A^k B_1...B_k`。非末位离轨后复制首次偏离主题，末位选 fresh 主题。
全部在轨真实比较与全部末位 BR 成立；uniform 查询是真安全最优，
`v_(m+1)=1-m/(2L)`，故 `L` 足够大时 `m v > k+1=W`。
第一处明确漏行：在历史 `(T)`（`T!=A`）后复制 `T` 得 `1/(m-1)`，
改选新的 `R` 得 `1`（首偏离 latch 仍为 `T`，后继继续复制 `T`，末位避开 `R`）。

此机制实质重复、更弱于现有
`R-51ca8c2b36184c41818099bc490374ca/cone/hamming_suffix_credibility_obstruction.md`：
旧族已经保留任意固定末尾深度、Hamming 保护带和全部在轨真实行而违反 half。
由 `m v_(m+1)>=OPT_m/2`，旧族本身就自动违反弱安全最优聚合。
本重建唯一简化是 uniform `p*` 可显式计算，不形成新截断量词或新中继机制，
因此不另建正文或审计，不作为一般主线进展。

## 当前接续

正与 relay 分支核对“终局+标记主题”的末次偏离剥离端点，检查静态 `p*`
最优性是否能提供所需端点容量。尚无承重符号结论。

- `safe_optimal_zero_regret_family.md`：经典大主题加私有 singleton 族的显式
  extra-one 安全原始/对偶；完整 σ 每历史都选大主题是真 SPE。所有强制源恰为
  p* 的静态最坏背景，静态遗憾为零，但平均交换 delta^+ 仍严格正，必须保留
  rho 自占用返还。弱聚合净余量在固定 m、目录增大时趋零。它是紧测试与
  精确限制，不是一般新支付。
- `audit_safe_zero_regret_family.py` 及 `safe_zero_regret_family_audit.json`：
  小参数全静态计数和常数策略全历史计数代表的 Fraction 定义级核验。
- `occupied_static_minimizer_counterexample.md`：**新辅助桥反例。** 十客户五主题
  真安全最优 p* 与最优静态 Q* 的纯支撑 B，满足占用收益 2 < 安全值 5/2。
  统一两 core 参数给任意静态竞争人数的唯一最坏背景及 rho 后净换标债 1。
  该背景末位有真实盈利偏离，故没有否定带 Γ 支付的网络或主 half。
- `audit_occupied_static_minimizer.py` 与冻结 JSON：定义级十客户完整矩阵、
  matching 原始/对偶、任意 m 族 m=1,...,6 全静态计数精确审计。
- `occupied_saddle_face_probe.py/.json`：此前随机 saddle-face 重权阴性发现记录，
  已被后来的解析反例取代，不能据此提升候选或继续阴性扩样。
