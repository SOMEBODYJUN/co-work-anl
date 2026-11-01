# R-2e5 omitted-deletion exploratory cluster evidence

本证据包保存五份已领取的 omitted_deletion 源版本、其精确输入/输出和一次隔离重放。它们是既有《实际遗漏客户删除与可信根门槛的无界敏感性》对象的发现与参数扫描输入；本批把此前只在缺件清单中登记的 clean 源取得、实读并逐源核对。

## 源与哈希

| clean id | 源路径 | 字节 | SHA-256 | 处置 |
|---|---|---:|---|---|
| `2d2830667667511eefe4` | `omitted_deletion/breakpoints.json` | 665 | `b99e316ef1debb7e8e296343d258fd4b849563b03ab5330b532b7ad1808c5c11` | 参数切点冻结输入 |
| `6e242beec67849c083e0` | `omitted_deletion/discovery.json` | 3437 | `eec5d795a8d391a60a71657dc3038e10e35de8a5cc057c187cc856349cf3767d` | 发现实例与目标 |
| `802c9677e58ef2b5cfb9` | `omitted_deletion/minimal.json` | 2052 | `4c259f62e2c2211d4348149b02c571f94fc20c4f8fa66e974083576f059e2e6e` | 约简输出冻结记录 |
| `5cfc23dcca78cd034036` | `omitted_deletion/minimize.py` | 1989 | `a3d910eb2740d7df1472f951f4b4af97cc43d9c0f9af7c99db9a25eb12f32af0` | 诊断约简程序 |
| `8f930829ba24af5ed22e` | `omitted_deletion/parameter_scan.json` | 25867 | `0e04fea2d88ffc956ec7533557dc5ad014834e254dfec5aae2d15477985e1902` | 129 代表参数扫描 |

## 约简重放

`discovery.json` 给出五人六主题实例、82 名单位客户、目标计数 `c=(2,0,1,0,0,2)`，发现试次为 135。`minimize.py` 以 `ExactSPESolver` 检查目标在删除后是否仍可实现，按客户行和重数贪心删除；本次在隔离的 `customer_attraction` 依赖布局中退出码为 0、stderr 为空，得到 `minimal.replayed.json`，与冻结 `minimal.json` 逐字节相同。它完成 36 次删除，客户总数从 82 降到 38；这是一条真实约简轨迹，不能仅凭贪心步数宣称全局最小性。

## 参数扫描关系

`breakpoints.json` 有 65 个切点；`parameter_scan.json` 有 129 个代表。证据包同时保存既有参数分区输出的副本，并用独立 verifier 逐条比较：源扫描的四个字段投影与 129 个 `representatives` 完全相同，65 个切点完全相同。扫描中前 96 个代表（`0≤t<3/4`）目标不可实现、根门槛 `33/4`、唯一根结果 `(2,1,1,0,1)`；从 `t=3/4` 起目标可实现且根门槛降为 `7`。在 `t=3/4` 处保留三种根结果，随后 `t=91/120` 起退去其中一项；这些是冻结有限参数输出的字段整理。

## 数学范围

这五份源支持既有参数分区证明和遗漏删除障碍中的发现路径：目标保真性跨 `t=3/4` 的跃迁、贪心约简的 36 步轨迹和参数扫描的冻结表。它们本身没有提供新的完整策略树证明、全局最小客户数证明、一般半覆盖反例或六人 half 结论。`breakpoints` 与 `parameter_scan` 只是冻结扫描表；全参数闭区间与门槛结论仍由既有障碍页的线性分区论证承担。
