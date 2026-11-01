# recursion2：合法背景利润、完整续局与污染租金

2026-10-22，Boss6 子研究员的个人研究备份。唯一主目标仍为一般共同目录、任意人数、
全部有序历史及任意平局纯 SPE 的 Q-CAG-HALF；本区没有取得一般证明。

- `bounded_core_guard_review.md`：未借助作者审计代码的独立全量词攻击。确认
  `../global2/bounded_core_pollution_guard.md` 的条件性守卫成立，另给利用单位
  客户和整数负载的严格离散强化。该强化是局部同终局不等式，不是跨分支支付。
- `residual_profit_static_interface.md`：合法背景剩余利润与自由分数背景安全值的
  静态比较，及最小背景带来的精确模板强化；没有动态 SPE 聚合支付。
- `weak_outsider_boundary_review.md`：从客户实例独立重建 outside 等号边界
  任意人数族的完整有序历史 SPE；确认其只否定逐人λ及W≥mλ桥，half仍成立。
- `free_fractional_floor_protection_obstruction.md`：五客户精确例与任意人数族，
  单独否定自由分数值w的floor-only保护；没有把非SPE续局误称为FF-LEADER反例。

已读模型、根四入口、数学地图、前沿、失败地图、原 recursion、背景三/四人利润、
末四人提升、旧高背景 K/theta 预算及 prefix penalty。未重复扫描弱逐人 floor、
floor-only 保护或固定理性尾部；原有静态和逐步预算的失败继续保留。

真正未付义务仍是：父节点的不同偏离可分别调用不同完整子 SPE，不能把各分支
污染租金直接记到同一实际路径。需要 incumbent-indexed 租金向量或其他新的联合
不变量；仅保留每个子局的总剩余利润下限会丢掉承重信息。
