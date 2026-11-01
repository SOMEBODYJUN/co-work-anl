# R-2e5 mixed-time-menus reentry evidence

本证据包保存本批两个 clean 源的原件、隔离重放输出和独立字段校验。对象是两个两人单位客户组件及其逐坐标产品；所有结果都保留为有限完整 SPE 审计和同步时刻边界。

## 源与哈希

| clean id | source | bytes | SHA-256 |
|---|---|---:|---|
| `37d7dcf25add304bcf51` | `full_tree_duality/mixed_time_menus/audit_reentry.json` | 987 | `710c251f8c8cb5ee26478823319d3aeee88251841ceae2bd2ce9eeac6df6605a` |
| `0da430519b193fa86a6b` | `full_tree_duality/mixed_time_menus/audit_reentry.py` | 4904 | `f3c98c975a59e4d731ef279c66d63e8f53cabaea169beafb9b7c349c939ddafe` |

## 重放结果

在隔离目录执行 `audit_reentry.py` 返回码 0、标准错误为空，生成 JSON 与冻结 JSON 逐字节相同；`verify_mixed_time_reentry.py` 返回 `PASS`。

冻结字段为：三个实例的客户规模 `[3,4,7]`；三个完整 SPE 的决策/比较计数 `(3,6),(3,6),(5,20)` 且最小 slack 均为 0；单重入向量分别为 `[(2/3,1),(1,2/3),(5/3,5/3)]`；组件分开最小值 `4/3`、产品同步单重入最小值 `5/3`、产品双重入值 `4/3`；端点嵌套检查 27 项、产品恒等式检查 16 项。

这些值只验证本批冻结的两个组件及其笛卡尔积。同步 `5/3 > 4/3` 是固定查询下的严格时刻冲突；它没有给出产品完整 minimax 值，也没有构成福利或六提供者 half 反例。任意人数的菜单归约、产品并集成本和全重入静态极限仍由正文中的解析推导承担。
