# Boss8：完整续局下的一般半覆盖

研究存档 `customer-attraction`；发布身份 `R-d51d7a410c12456aa5c44e84b78708d0`。
精确主目标为 Q-CAG-HALF，模型以 `research/current/customer_attraction/model.md` 为准：
任意有限共同目录、任意人数、每个完整有序历史依赖纯 SPE 的 `2W≥OPT_m`。
主目标仍 **OPEN**；本工作区的备份不自动成为可靠或新颖结论。

## 已改变的认识

本轮接续于 `round2/`。一般目标仍 OPEN。`round2/full_tree/type_map_and_mapped_circulations.md`
给固定总人数收益类型映射的精确秩，以及一个全部非空客户类型均严格为正的完整四人SPE：
收益图 SCC 像空间秩为1，但全部真实激励行锥的线性空间秩为2。
真实行的正组合可在类型映射后抵消，而抽象图的净流量仍不为零。
`round2/direct_global/audit_extra_lineality.py` 从完整策略独立重构全部有序历史，确认该差异。
这否定仅靠 SCC 压缩便把余锥视为 pointed 的步骤，不反驳半覆盖；外审和新颖性未认证。

`independent_attack/residual_cover_family.md` 给一个两人、任意整数参数 q≥2 的完整 SPE 族，
否定加强桥“用至多 m 个目录主题能覆盖的纯残余客户数不超过实际福利”。
实际福利 `4q+5`，最优两主题覆盖和最优纯残余覆盖均为 `4q+6`。
这是加强桥反例，主目标半覆盖仍成立；族的代数证明、定义级核验和独立审查分别记录。

## 材料与读取条件

| 子目录 | 用途与真实状态 |
| --- | --- |
| round2/ | 本轮一般目标研究及可恢复索引；含全树类型核、已独立核验的额外映射环流、仍开放的预算桥与有限探索。逐项见该目录README。 |
| independent_attack/ | 加强残余桥的无限族、完整两人策略及精确单位客户验证；随后继续一般证明 |
| true_counterexample/ | 联合客户重数与目标索引续局 DAG 的 MILP；区别于强制计数 Markov，等价性与数值认证条件须逐条审查；超时没有数学含义 |
| continuation_geometry/ | 完整子 SPE 的最小 mover 收益阈值、任意计数路径累加的候选和可复现实验；有限证据不是普遍定理 |
| global_proof/ | 静态 CCE 比较和总静态偏离宽限的候选；未闭合的全局机制 |
| static_width/ | 对已冻结完整策略锥攻击总静态偏离宽限的浮点 LP；不作为一般证明 |
| security_aggregate/ | 两步静态安全值链的开放加强桥；固定锥内交替 LP 只作探索 |
| branch_transport/ | 真实菜单的分支运输探索，以及加强残余桥的独立定义级审查 |

## 可接续的义务

探索不用等待审查。优先控制真实分支的全局福利损失，或找到具有全部历史证书的目标反例。
残余加强桥失败后不再将其当作主目标的无损改写；其余候选均保留准确量词与未证身份。
共享资产正式入库时再维护相应 Claim、数学地图和登记；个人资产及时 checkpoint。
