# R-2f6cae owner-budget and ten-cycle stationary evidence

本证据包保存四份已领取源的完整原件、隔离重放和独立字段检查。两份源验证单客户归属误差的有限代数回归；两份源验证十环辅助接口中的静态价格与形式策略偏离。它们属于有限核验和障碍诊断，不承担完整 CAG SPE 或六人 half 结论。

## 源哈希

| clean id | source | bytes | SHA-256 | 处置 |
|---|---|---:|---|---|
| `27f7db956b60296d4fed` | `random_portfolio/arbitrary_owner_budget_audit.json` | 459 | `2ef1eff32e8b152add0ea1b3d45227ed1b4826068632a4374cff78d77951d69c` | 冻结回归结果完整读取 |
| `e87d3323feac224b9907` | `random_portfolio/audit_arbitrary_owner_budget.py` | 4606 | `7dcfaf718d9a22bbcbe3bf0168d359a4ed849a6be682175668efd0acbb179b8d` | Fraction 脚本实际重放 |
| `a58cdb23480aefd4cc2a` | `relay/stationary/audit_state_floor_blind.py` | 2788 | `d2890cc366fa982f5bc9ff6c2ae909bd474a99c7c273f6b960dc0ded4aa4b0b4` | Fraction 辅助接口实际重放 |
| `305b18cec769d8fa5743` | `relay/stationary/state_floor_blind_audit.json` | 7863 | `c780550274562c7aa3323819189022a37a2f7a0e362294c460f3e5773ae4cf5a` | 冻结报告完整读取 |

## owner-budget 回归

`audit_arbitrary_owner_budget.py` 在 `m=1,...,8` 上检查了 188,302 个前缀状态、1,793 个任意固定 owner 前缀预算和 510 个均匀 owner 固定端点状态。输出状态为 `PASS`，且明确 scope 为 single-customer algebra regression，包含 rank bound、任意 owner 的 `H_{a-1}` 上界、prefix-only sharpness、uniform endpoint 与 symmetric error monotonicity。脚本只使用 Fraction 和集合枚举，未导入 SPE 求解器或客户目录。

脚本运行退出码为 0，标准错误为空；生成 JSON 与冻结 JSON 逐字节相同。这个回归支持随 m≤8 的定义级恒等式和有限索引核验，不把 8 以内扫描写成任意人数完整博弈定理。

## 十环 state-floor 辅助接口

`audit_state_floor_blind.py` 对十个三窗口主题和十名单位客户，枚举 1,000 个有序三竞争主题元组。均匀查询的下界与旋转对偶都给 `v4=33/20`；指定根收益为 `3/2`，差距 `3/20`。十个旋转 profile 的收益均为 `(3/2,2,5/2)`，每个末位都存在收益 3 的偏离。报告的 scope 明确写着 profiles are not SPE。

该结果与既有十环资源页的形式策略分析相符：逐前缀 floors 和根 IC 可以同时满足，但末位的真实行动 IC 失败。因此它是一个放松接口的精确障碍，不能升级为完整 SPE、自由 extra-one 反例或六人 half 反例。脚本实际运行退出码为 0、标准错误为空；生成 JSON 与冻结报告逐字节相同。

独立 `verify_r2f6.py` 检查四源 SHA、关键计数、`33/20`、`3/20`、十个旋转和两次空 stderr，返回 `PASS`。
